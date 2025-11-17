#!/usr/bin/env python3.11
"""
Geometric Uncertainty Quantification
Bootstrap CI for UBP constant relationships (Pi, Y, O_observer)
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# UBP Constants (from y_constants.py)
PI = np.pi
Y = 0.2647
O_OBSERVER = 3.7782

def load_data():
    """Load Phase 2 results"""
    print("\n[1/4] Loading data...")
    
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    with open('results/validation_threshold_bimodality.json', 'r') as f:
        threshold_results = json.load(f)
    
    df = pd.DataFrame(results)
    
    print(f"   Loaded {len(df)} minerals")
    
    return df, threshold_results

def bootstrap_threshold_ratio(df, threshold_results, n_bootstrap=2000):
    """
    Bootstrap CI for threshold / O_observer ratio
    Test if it equals Y
    """
    print("\n[2/4] Bootstrap CI for threshold / O_observer...")
    print(f"   Testing if threshold / O_observer ≈ Y = {Y}")
    
    nrcis = df['nrci'].values
    
    # Bootstrap
    ratios = []
    thresholds = []
    
    for i in range(n_bootstrap):
        if (i + 1) % 400 == 0:
            print(f"      Bootstrap sample {i+1}/{n_bootstrap}...")
        
        sample = np.random.choice(nrcis, size=len(nrcis), replace=True)
        threshold = np.percentile(sample, 95)
        ratio = threshold / O_OBSERVER
        
        thresholds.append(threshold)
        ratios.append(ratio)
    
    ratios = np.array(ratios)
    thresholds = np.array(thresholds)
    
    # Compute CI
    ratio_ci = np.percentile(ratios, [2.5, 50, 97.5])
    
    # Original
    threshold_original = threshold_results['bootstrap_threshold_ci']['original_threshold']
    ratio_original = threshold_original / O_OBSERVER
    
    # Test if ratio ≈ Y
    diff_from_Y = ratio_original - Y
    diff_pct = abs(diff_from_Y) / Y * 100
    
    # p-value: proportion of bootstrap samples where ratio ≥ Y
    p_value = np.mean(ratios >= Y)
    
    print(f"\n   Results:")
    print(f"      Original threshold: {threshold_original:.6f}")
    print(f"      Original ratio (threshold / O_observer): {ratio_original:.6f}")
    print(f"      Y constant: {Y:.6f}")
    print(f"      Difference: {diff_from_Y:+.6f} ({diff_pct:.2f}%)")
    print(f"      Bootstrap ratio 95% CI: [{ratio_ci[0]:.6f}, {ratio_ci[2]:.6f}]")
    print(f"      p-value (ratio ≥ Y): {p_value:.4f}")
    
    # Does CI contain Y?
    contains_Y = (ratio_ci[0] <= Y <= ratio_ci[2])
    print(f"      CI contains Y: {contains_Y}")
    
    return {
        'threshold_original': float(threshold_original),
        'ratio_original': float(ratio_original),
        'Y_constant': float(Y),
        'difference_from_Y': float(diff_from_Y),
        'difference_pct': float(diff_pct),
        'ratio_ci_lower': float(ratio_ci[0]),
        'ratio_ci_median': float(ratio_ci[1]),
        'ratio_ci_upper': float(ratio_ci[2]),
        'p_value': float(p_value),
        'ci_contains_Y': bool(contains_Y),
        'bootstrap_distribution': ratios.tolist()
    }

def bootstrap_pi_symmetry_ratio(df, n_bootstrap=2000):
    """
    Bootstrap CI for 12 / PI ratio
    Test if it equals O_observer
    """
    print("\n[3/4] Bootstrap CI for 12 / π...")
    print(f"   Testing if 12 / π ≈ O_observer = {O_OBSERVER}")
    
    # This is a deterministic calculation, but we can test sensitivity
    # by bootstrapping the symmetry threshold from data
    
    # Find the symmetry threshold from data
    # (the minimum symmetry operations for minerals that pass)
    threshold_nrci = 0.973243
    passed = df[df['nrci'] >= threshold_nrci]
    
    if len(passed) > 0:
        min_symmetry_passed = passed['symmetry_operations'].min()
        max_symmetry_failed = df[df['nrci'] < threshold_nrci]['symmetry_operations'].max()
        
        print(f"   Min symmetry (passed): {min_symmetry_passed}")
        print(f"   Max symmetry (failed): {max_symmetry_failed}")
    else:
        min_symmetry_passed = 12  # Default from Phase 1
    
    # Bootstrap the symmetry threshold
    symmetry_thresholds = []
    
    for i in range(n_bootstrap):
        if (i + 1) % 400 == 0:
            print(f"      Bootstrap sample {i+1}/{n_bootstrap}...")
        
        # Resample minerals
        sample_indices = np.random.choice(len(df), size=len(df), replace=True)
        sample_df = df.iloc[sample_indices]
        
        # Find threshold
        sample_passed = sample_df[sample_df['nrci'] >= threshold_nrci]
        if len(sample_passed) > 0:
            symmetry_thresholds.append(sample_passed['symmetry_operations'].min())
        else:
            symmetry_thresholds.append(12)
    
    symmetry_thresholds = np.array(symmetry_thresholds)
    
    # Compute ratios
    ratios = symmetry_thresholds / PI
    
    # CI
    ratio_ci = np.percentile(ratios, [2.5, 50, 97.5])
    
    # Original
    ratio_original = min_symmetry_passed / PI
    diff_from_O = ratio_original - O_OBSERVER
    diff_pct = abs(diff_from_O) / O_OBSERVER * 100
    
    print(f"\n   Results:")
    print(f"      Symmetry threshold: {min_symmetry_passed}")
    print(f"      Original ratio (symmetry / π): {ratio_original:.6f}")
    print(f"      O_observer constant: {O_OBSERVER:.6f}")
    print(f"      Difference: {diff_from_O:+.6f} ({diff_pct:.2f}%)")
    print(f"      Bootstrap ratio 95% CI: [{ratio_ci[0]:.6f}, {ratio_ci[2]:.6f}]")
    
    # Does CI contain O_observer?
    contains_O = (ratio_ci[0] <= O_OBSERVER <= ratio_ci[2])
    print(f"      CI contains O_observer: {contains_O}")
    
    return {
        'symmetry_threshold': int(min_symmetry_passed),
        'ratio_original': float(ratio_original),
        'O_observer_constant': float(O_OBSERVER),
        'difference_from_O': float(diff_from_O),
        'difference_pct': float(diff_pct),
        'ratio_ci_lower': float(ratio_ci[0]),
        'ratio_ci_median': float(ratio_ci[1]),
        'ratio_ci_upper': float(ratio_ci[2]),
        'ci_contains_O_observer': bool(contains_O),
        'bootstrap_distribution': ratios.tolist()
    }

def correlation_analysis(df):
    """
    Analyze correlations between key variables
    """
    print("\n[4/4] Correlation Analysis...")
    
    # Key variables
    vars_of_interest = ['Z_max', 'symmetry_operations', 'degradation', 
                       'refinements', 'nrci']
    
    # Compute correlation matrix
    corr_matrix = df[vars_of_interest].corr()
    
    print("\n   Correlation Matrix:")
    print("   " + " ".join(f"{v:15s}" for v in vars_of_interest))
    for i, var1 in enumerate(vars_of_interest):
        row = "   " + f"{var1:15s}"
        for j, var2 in enumerate(vars_of_interest):
            row += f" {corr_matrix.iloc[i, j]:14.4f}"
        print(row)
    
    # Key correlations
    print("\n   Key Correlations:")
    print(f"      Z_max ↔ degradation: {corr_matrix.loc['Z_max', 'degradation']:.4f}")
    print(f"      symmetry ↔ refinements: {corr_matrix.loc['symmetry_operations', 'refinements']:.4f}")
    print(f"      degradation ↔ NRCI: {corr_matrix.loc['degradation', 'nrci']:.4f}")
    
    return {
        'correlation_matrix': corr_matrix.to_dict(),
        'key_correlations': {
            'Z_max_degradation': float(corr_matrix.loc['Z_max', 'degradation']),
            'symmetry_refinements': float(corr_matrix.loc['symmetry_operations', 'refinements']),
            'degradation_nrci': float(corr_matrix.loc['degradation', 'nrci'])
        }
    }

def visualize_results(threshold_ratio_results, pi_ratio_results):
    """
    Create visualizations
    """
    print("\n   Creating visualizations...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. threshold / O_observer distribution
    ax = axes[0]
    ratios = threshold_ratio_results['bootstrap_distribution']
    ax.hist(ratios, bins=50, alpha=0.7, edgecolor='black')
    ax.axvline(threshold_ratio_results['ratio_original'], color='blue', 
               linestyle='--', linewidth=2, label='Observed')
    ax.axvline(Y, color='red', linestyle='--', linewidth=2, label=f'Y = {Y:.4f}')
    ax.axvline(threshold_ratio_results['ratio_ci_lower'], color='orange', 
               linestyle=':', linewidth=2, label='95% CI')
    ax.axvline(threshold_ratio_results['ratio_ci_upper'], color='orange', 
               linestyle=':', linewidth=2)
    ax.set_xlabel('threshold / O_observer')
    ax.set_ylabel('Frequency')
    ax.set_title('Bootstrap Distribution: threshold / O_observer')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. symmetry / π distribution
    ax = axes[1]
    ratios = pi_ratio_results['bootstrap_distribution']
    ax.hist(ratios, bins=50, alpha=0.7, edgecolor='black')
    ax.axvline(pi_ratio_results['ratio_original'], color='blue', 
               linestyle='--', linewidth=2, label='Observed')
    ax.axvline(O_OBSERVER, color='red', linestyle='--', linewidth=2, 
               label=f'O_observer = {O_OBSERVER:.4f}')
    ax.axvline(pi_ratio_results['ratio_ci_lower'], color='orange', 
               linestyle=':', linewidth=2, label='95% CI')
    ax.axvline(pi_ratio_results['ratio_ci_upper'], color='orange', 
               linestyle=':', linewidth=2)
    ax.set_xlabel('symmetry_threshold / π')
    ax.set_ylabel('Frequency')
    ax.set_title('Bootstrap Distribution: symmetry / π')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/validation_geometric_uncertainty.png', dpi=150)
    print("   ✓ Saved validation_geometric_uncertainty.png")

def save_results(threshold_ratio, pi_ratio, correlations):
    """Save results"""
    print("\n   Saving results...")
    
    summary = {
        'random_seed': RANDOM_SEED,
        'ubp_constants': {
            'PI': float(PI),
            'Y': float(Y),
            'O_observer': float(O_OBSERVER)
        },
        'threshold_O_observer_ratio': threshold_ratio,
        'symmetry_pi_ratio': pi_ratio,
        'correlations': correlations
    }
    
    with open('results/validation_geometric_uncertainty.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved validation_geometric_uncertainty.json")

def main():
    print("="*80)
    print("GEOMETRIC UNCERTAINTY QUANTIFICATION")
    print("="*80)
    print("Bootstrap CI for UBP constant relationships")
    print("="*80)
    
    # Load data
    df, threshold_results = load_data()
    
    # 1. threshold / O_observer ratio
    threshold_ratio_results = bootstrap_threshold_ratio(df, threshold_results, n_bootstrap=2000)
    
    # 2. symmetry / π ratio
    pi_ratio_results = bootstrap_pi_symmetry_ratio(df, n_bootstrap=2000)
    
    # 3. Correlations
    correlation_results = correlation_analysis(df)
    
    # 4. Visualize
    visualize_results(threshold_ratio_results, pi_ratio_results)
    
    # 5. Save
    save_results(threshold_ratio_results, pi_ratio_results, correlation_results)
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE!")
    print("="*80)
    print("\nKey Findings:")
    print(f"   threshold / O_observer = {threshold_ratio_results['ratio_original']:.6f}")
    print(f"   Difference from Y: {threshold_ratio_results['difference_pct']:.2f}%")
    print(f"   CI contains Y: {threshold_ratio_results['ci_contains_Y']}")
    print(f"\n   symmetry / π = {pi_ratio_results['ratio_original']:.6f}")
    print(f"   Difference from O_observer: {pi_ratio_results['difference_pct']:.2f}%")
    print(f"   CI contains O_observer: {pi_ratio_results['ci_contains_O_observer']}")

if __name__ == '__main__':
    main()
