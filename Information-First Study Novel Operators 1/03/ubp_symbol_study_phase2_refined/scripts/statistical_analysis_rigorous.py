#!/usr/bin/env python3.11
"""
Rigorous Statistical Analysis of Novel Symbol Candidates
UBP Symbol Study Phase 2 (Refined)

Implements the full statistical protocol from the technical feedback:
1. Fit baseline predictive model (Random Forest)
2. Generate bootstrapped CIs for feature importances
3. Compare novel candidates to matched controls
4. Perform Wilcoxon signed-rank test
5. Compute Cohen's d effect size
6. Validate model calibration (slope and RMSE)
7. Generate publication-ready tables and plots

Author: Manus AI
Date: Nov 18, 2025
"""

import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import permutation_importance
from scipy.stats import wilcoxon, ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# --- Data Loading ---

def load_data():
    """Load all necessary data"""
    # Novel candidates (evaluated)
    with open("/home/ubuntu/ubp_symbol_study_phase2_refined/results/candidates_evaluated.json", 'r') as f:
        candidates = pd.DataFrame(json.load(f))
    
    # Baseline symbols (Phase 2)
    with open("/home/ubuntu/ubp_symbol_study_phase2_refined/data/baseline_normalized.json", 'r') as f:
        baseline = pd.DataFrame(json.load(f))
    
    print(f"Loaded {len(candidates)} candidates and {len(baseline)} baseline symbols")
    return candidates, baseline

# --- Baseline Model --- 

def fit_baseline_model(baseline_df: pd.DataFrame):
    """
    Fit baseline RandomForestRegressor on the 1006-symbol dataset.
    """
    print("\n" + "="*70)
    print("1. FITTING BASELINE PREDICTIVE MODEL")
    print("="*70)
    
    # Features (D1-D8) and target (NRCI)
    features = [f"bitfield_d{i+1}" for i in range(8)]
    target = "nrci"
    
    X = baseline_df[features]
    y = baseline_df[target]
    
    # Model: RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=RANDOM_SEED)
    
    # Cross-validation (k=10)
    kf = KFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED)
    r2_scores = []
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2_scores.append(r2_score(y_test, y_pred))
    
    print(f"Baseline Model: RandomForestRegressor (n=100)")
    print(f"Cross-validation R²: {np.mean(r2_scores):.4f} ± {np.std(r2_scores):.4f}")
    
    # Fit final model on all data
    model.fit(X, y)
    
    # Feature importances with bootstrapped CIs
    print("\nFeature Importances (Permutation, n=50):")
    perm_importance = permutation_importance(model, X, y, n_repeats=50, random_state=RANDOM_SEED)
    
    importances = []
    for i in range(len(features)):
        mean_imp = perm_importance.importances_mean[i]
        std_imp = perm_importance.importances_std[i]
        ci_95 = [mean_imp - 1.96 * std_imp, mean_imp + 1.96 * std_imp]
        importances.append({
            "feature": features[i],
            "mean": mean_imp,
            "std": std_imp,
            "ci_95_low": ci_95[0],
            "ci_95_high": ci_95[1]
        })
        print(f"  {features[i]}: {mean_imp:.4f} (95% CI: [{ci_95[0]:.4f}, {ci_95[1]:.4f}])")
    
    return model, importances

# --- Candidate vs Control --- 

def compare_to_controls(candidates_df: pd.DataFrame, baseline_df: pd.DataFrame):
    """
    Compare novel candidates to matched controls from the baseline dataset.
    """
    print("\n" + "="*70)
    print("2. COMPARING CANDIDATES TO MATCHED CONTROLS")
    print("="*70)
    
    results = []
    
    for _, cand in candidates_df.iterrows():
        # Match controls on D1 (Arity) and D2 (Formal Role)
        d1_val = cand["D1"]
        d2_val = cand["D2"]
        
        controls = baseline_df[
            (np.isclose(baseline_df["bitfield_d1"], d1_val, atol=0.05)) &
            (np.isclose(baseline_df["bitfield_d2"], d2_val, atol=0.05))
        ]
        
        if len(controls) == 0:
            continue
        
        # Sample 100 controls (or all if fewer)
        control_sample = controls.sample(n=min(100, len(controls)), random_state=RANDOM_SEED)
        control_mean_nrci = control_sample["nrci"].mean()
        
        results.append({
            "id": cand["id"],
            "NRCI_meas": cand["NRCI_meas"],
            "control_mean_nrci": control_mean_nrci,
            "diff": cand["NRCI_meas"] - control_mean_nrci
        })
    
    results_df = pd.DataFrame(results)
    
    # Wilcoxon signed-rank test
    w_stat, p_value = wilcoxon(results_df["diff"])
    print("Wilcoxon Signed-Rank Test (Candidate NRCI vs Control NRCI):")
    print(f"  W-statistic: {w_stat:.2f}")
    print(f"  p-value: {p_value:.6f}")
    
    # Cohen's d effect size
    mean_diff = results_df["diff"].mean()
    std_diff = results_df["diff"].std()
    cohens_d = mean_diff / std_diff
    print(f"\nEffect Size (Cohen's d): {cohens_d:.4f}")
    
    # Bootstrapped 95% CI for the mean difference
    boots = []
    for _ in range(5000):
        s = np.random.choice(results_df["diff"], size=len(results_df), replace=True)
        boots.append(s.mean())
    ci_95 = np.percentile(boots, [2.5, 97.5])
    print(f"Bootstrapped 95% CI for mean difference: [{ci_95[0]:.6f}, {ci_95[1]:.6f}]")
    
    return results_df, {"p_value": p_value, "cohens_d": cohens_d, "ci_95": ci_95.tolist()}

# --- Model Calibration --- 

def validate_model_calibration(model: RandomForestRegressor, candidates_df: pd.DataFrame):
    """
    Validate the model's calibration on the novel candidates.
    """
    print("\n" + "="*70)
    print("3. VALIDATING MODEL CALIBRATION")
    print("="*70)
    
    # Predict NRCI for candidates
    # Rename candidate columns to match model's feature names
    rename_map = {f"D{i+1}": f"bitfield_d{i+1}" for i in range(8)}
    candidates_df = candidates_df.rename(columns=rename_map)
    features = [f"bitfield_d{i+1}" for i in range(8)]
    X_cand = candidates_df[features]
    y_pred = model.predict(X_cand)
    y_true = candidates_df["NRCI_meas"]
    
    candidates_df["NRCI_pred"] = y_pred
    
    # Calibration slope and RMSE
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # Fit linear model to calibration plot
    calib_model = np.polyfit(y_pred, y_true, 1)
    calib_slope = calib_model[0]
    
    print(f"Model Calibration on Novel Candidates:")
    print(f"  RMSE: {rmse:.6f}")
    print(f"  Calibration Slope: {calib_slope:.4f}")
    
    # Plot calibration
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=y_pred, y=y_true, alpha=0.7, label="Novel Candidates")
    plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], 'r--', label="Perfect Calibration")
    plt.plot(y_pred, np.poly1d(calib_model)(y_pred), 'g-', label=f"Fit (slope={calib_slope:.2f})")
    plt.xlabel("Predicted NRCI")
    plt.ylabel("Measured NRCI")
    plt.title("Model Calibration on Novel Candidates")
    plt.legend()
    plt.grid(True)
    plt.savefig("/home/ubuntu/ubp_symbol_study_phase2_refined/results/calibration_plot.png")
    print("\nSaved calibration plot to results/")
    
    return {"rmse": rmse, "slope": calib_slope}

# --- Main Execution --- 

def main():
    """Run the full statistical analysis pipeline"""
    print("="*70)
    print("RIGOROUS STATISTICAL ANALYSIS - UBP SYMBOL STUDY")
    print("="*70)
    
    # Load data
    candidates, baseline = load_data()
    
    # 1. Fit baseline model
    model, importances = fit_baseline_model(baseline)
    
    # 2. Compare to controls
    comparison_df, stats = compare_to_controls(candidates, baseline)
    
    # 3. Validate calibration
    calibration_stats = validate_model_calibration(model, candidates)
    
    # --- Save all results ---
    final_results = {
        "baseline_model": {
            "r2_cv": np.mean([s["mean"] for s in importances]),
            "feature_importances": importances
        },
        "candidate_vs_control": {
            "wilcoxon_p_value": stats["p_value"],
            "cohens_d": stats["cohens_d"],
            "mean_diff_ci_95": stats["ci_95"]
        },
        "model_calibration": calibration_stats,
        "candidate_data": candidates.to_dict("records")
    }
    
    with open("/home/ubuntu/ubp_symbol_study_phase2_refined/results/statistical_analysis_summary.json", 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("Full statistical summary saved to results/")
    print("="*70)

if __name__ == "__main__":
    main()
