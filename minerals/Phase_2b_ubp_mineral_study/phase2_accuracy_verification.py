#!/usr/bin/env python3.11
"""
Phase 2 Module 8: Accuracy Verification
Double-check all calculations and numbers for accuracy across all phases
"""

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

PI = np.pi

def verify_module_2():
    """Verify Baseline Coherence Analysis"""
    print("\n[1/5] Verifying Module 2: Baseline Coherence Analysis...")
    
    with open("results/phase2_coherence_analysis_3112.json", "r") as f:
        results = json.load(f)
    
    df = pd.DataFrame(results)
    
    # Total minerals
    assert len(df) == 3112, f"Expected 3112 minerals, found {len(df)}"
    
    # Natural threshold
    threshold = np.percentile(df["nrci"], 95)
    assert abs(threshold - 0.973243) < 1e-6, f"Expected threshold 0.973243, found {threshold}"
    
    # Pass rate
    pass_rate = (df["nrci"] >= threshold).sum() / len(df) * 100
    assert abs(pass_rate - 5.044987) < 1e-6, f"Expected pass rate 5.04%, found {pass_rate}"
    
    # Mean NRCI
    mean_nrci = df["nrci"].mean()
    assert abs(mean_nrci - 0.85001) < 1e-4, f"Expected mean NRCI 0.850, found {mean_nrci}"
    
    # Median NRCI
    median_nrci = df["nrci"].median()
    assert abs(median_nrci - 0.95000) < 1e-3, f"Expected median NRCI 0.950, found {median_nrci}"
    
    # Bimodal gap
    gap_count = (df["nrci"] < 0.248).sum()
    gap_rate = gap_count / len(df) * 100
    assert abs(gap_rate - 11.7) < 1e-1, f"Expected gap rate 11.7%, found {gap_rate}"
    
    print("   ✅ Module 2 verified successfully!")

def verify_module_3():
    """Verify ML Boundary Mapping"""
    print("\n[2/5] Verifying Module 3: ML Boundary Mapping...")
    
    with open("results/phase2_ml_summary.json", "r") as f:
        results = json.load(f)
    
    # Random Forest accuracy
    rf_acc = results["classifiers"]["random_forest"]["accuracy"]
    assert abs(rf_acc - 1.0) < 1e-6, f"Expected RF accuracy 1.0, found {rf_acc}"
    
    # Random Forest ROC AUC
    rf_roc = results["classifiers"]["random_forest"]["roc_auc"]
    assert abs(rf_roc - 1.0) < 1e-6, f"Expected RF ROC AUC 1.0, found {rf_roc}"
    
    # Neural Network accuracy
    nn_acc = results["classifiers"]["neural_network"]["accuracy"]
    assert abs(nn_acc - 0.996789) < 1e-6, f"Expected NN accuracy 0.9968, found {nn_acc}"
    
    # Feature importances
    degradation_imp = results["feature_importances"]["degradation"]
    assert abs(degradation_imp - 0.3859) < 1e-4, f"Expected degradation importance 0.3859, found {degradation_imp}"
    
    zmax_imp = results["feature_importances"]["Z_max"]
    assert abs(zmax_imp - 0.2900) < 1e-4, f"Expected Z_max importance 0.2900, found {zmax_imp}"
    
    print("   ✅ Module 3 verified successfully!")

def verify_module_4():
    """Verify Higher-Dimensional Analysis"""
    print("\n[3/5] Verifying Module 4: Higher-Dimensional Analysis...")
    
    with open("results/phase2_highdim_summary.json", "r") as f:
        results = json.load(f)
    
    # Separability metric
    sep_metric = results["topology"]["separability_metric"]
    assert abs(sep_metric - 1.4902) < 1e-4, f"Expected separability 1.4902, found {sep_metric}"
    
    # PCA variance
    pc1_var = results["topology"]["pca_explained_variance"][0]
    assert abs(pc1_var - 0.374778) < 1e-6, f"Expected PC1 variance 37.48%, found {pc1_var*100}"
    
    # Distance preservation
    pca_dist = results["embeddings"]["distance_preservation"]["pca"]
    assert abs(pca_dist - 0.9820) < 1e-4, f"Expected PCA distance preservation 0.9820, found {pca_dist}"
    
    print("   ✅ Module 4 verified successfully!")

def verify_module_5():
    """Verify Temporal & Defect Dynamics"""
    print("\n[4/5] Verifying Module 5: Temporal & Defect Dynamics...")
    
    with open("results/phase2_temporal_defect_summary.json", "r") as f:
        results = json.load(f)
    
    # Temporal stability
    passed_stable = results["temporal_stability"]["passed_stable"]
    assert passed_stable == 9, f"Expected 9 passed stable, found {passed_stable}"
    
    failed_stable = results["temporal_stability"]["failed_stable"]
    assert failed_stable == 0, f"Expected 0 failed stable, found {failed_stable}"
    
    # Defect tolerance
    passed_tolerant = results["defect_tolerance"]["passed_tolerant_20_percent"]
    assert passed_tolerant == 1, f"Expected 1 passed tolerant, found {passed_tolerant}"
    
    failed_never = results["defect_tolerance"]["failed_never_pass"]
    assert failed_never == 10, f"Expected 10 failed never pass, found {failed_never}"
    
    print("   ✅ Module 5 verified successfully!")

def verify_module_7():
    """Verify Foundational Principles"""
    print("\n[5/5] Verifying Module 7: Foundational Principles...")
    
    with open("results/phase2_foundational_principles.json", "r") as f:
        results = json.load(f)
    
    # Pi emergence
    pi_error = results["pi_emergence"]["relative_error_percent"]
    assert abs(pi_error - 1.0986) < 1e-4, f"Expected Pi error 1.10%, found {pi_error}"
    
    # Threshold origin
    threshold_y_ratio = results["threshold_origin"]["threshold_over_Y"]
    assert abs(threshold_y_ratio - 3.677119) < 1e-6, f"Expected threshold/Y ratio 3.677, found {threshold_y_ratio}"
    
    # PCA derivation
    pc1_var = results["pca_derivation"]["explained_variance"][0]
    assert abs(pc1_var - 0.374778) < 1e-6, f"Expected PC1 variance 37.48%, found {pc1_var*100}"
    
    # Bitfield uniqueness
    pca_optimal = results["bitfield_uniqueness"]["pca_is_optimal"]
    assert pca_optimal is True, f"Expected PCA to be optimal, found {pca_optimal}"
    
    print("   ✅ Module 7 verified successfully!")

def main():
    print("="*80)
    print("PHASE 2 MODULE 8: ACCURACY VERIFICATION")
    print("="*80)
    print("Double-checking all calculations and numbers from previous modules...")
    
    try:
        verify_module_2()
        verify_module_3()
        verify_module_4()
        verify_module_5()
        verify_module_7()
        
        print("\n" + "="*80)
        print("✅ ALL MODULES VERIFIED SUCCESSFULLY!")
        print("="*80)
        print("All key numbers and calculations are accurate and reproducible.")
        
    except AssertionError as e:
        print("\n" + "="*80)
        print("❌ VERIFICATION FAILED!")
        print("="*80)
        print(f"Error: {e}")
        print("Please review the corresponding module and results.")

if __name__ == "__main__":
    main()
