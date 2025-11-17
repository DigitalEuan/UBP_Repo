#!/usr/bin/env python3.11
"""
Statistical Validation of Threshold and Bimodality
Bootstrap confidence intervals, GMM fitting, and gap significance testing
"""

import json
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from scipy import stats
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def load_data():
    """Load NRCI values"""
    print("\n[1/6] Loading data...")
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    df = pd.DataFrame(results)
    nrcis = df['nrci'].values
    
    print(f"   Loaded {len(nrcis)} NRCI values")
    print(f"   Range: [{nrcis.min():.6f}, {nrcis.max():.6f}]")
    print(f"   Mean: {nrcis.mean():.6f}")
    print(f"   Median: {np.median(nrcis):.6f}")
    
    return nrcis

def bootstrap_threshold_ci(nrcis, percentile=95, n_bootstrap=2000):
    """
    Bootstrap confidence interval for threshold
    """
    print(f"\n[2/6] Bootstrap Confidence Interval for {percentile}th Percentile...")
    print(f"   Running {n_bootstrap} bootstrap samples...")
    
    percentiles = []
    for i in range(n_bootstrap):
        if (i + 1) % 400 == 0:
            print(f"      Bootstrap sample {i+1}/{n_bootstrap}...")
        
        sample = np.random.choice(nrcis, size=len(nrcis), replace=True)
        percentiles.append(np.percentile(sample, percentile))
    
    percentiles = np.array(percentiles)
    
    # Compute CI
    ci_lower = np.percentile(percentiles, 2.5)
    ci_median = np.percentile(percentiles, 50)
    ci_upper = np.percentile(percentiles, 97.5)
    
    # Original threshold
    threshold_original = np.percentile(nrcis, percentile)
    
    print(f"\n   Bootstrap Results:")
    print(f"      Original {percentile}th percentile: {threshold_original:.6f}")
    print(f"      Bootstrap median:  {ci_median:.6f}")
    print(f"      95% CI: [{ci_lower:.6f}, {ci_upper:.6f}]")
    print(f"      CI width: {ci_upper - ci_lower:.6f}")
    print(f"      Relative uncertainty: {(ci_upper - ci_lower) / ci_median * 100:.4f}%")
    
    return {
        'percentile': percentile,
        'original_threshold': float(threshold_original),
        'bootstrap_median': float(ci_median),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'ci_width': float(ci_upper - ci_lower),
        'relative_uncertainty_pct': float((ci_upper - ci_lower) / ci_median * 100),
        'n_bootstrap': n_bootstrap,
        'bootstrap_distribution': percentiles.tolist()
    }

def test_bimodality_gmm(nrcis):
    """
    Test bimodality using Gaussian Mixture Model
    """
    print("\n[3/6] Bimodality Testing with Gaussian Mixture Model...")
    
    X = nrcis.reshape(-1, 1)
    
    # Fit 1-component GMM
    print("   Fitting 1-component GMM...")
    gmm1 = GaussianMixture(n_components=1, random_state=RANDOM_SEED)
    gmm1.fit(X)
    bic1 = gmm1.bic(X)
    aic1 = gmm1.aic(X)
    
    print(f"      BIC: {bic1:.2f}")
    print(f"      AIC: {aic1:.2f}")
    
    # Fit 2-component GMM
    print("\n   Fitting 2-component GMM...")
    gmm2 = GaussianMixture(n_components=2, random_state=RANDOM_SEED)
    gmm2.fit(X)
    bic2 = gmm2.bic(X)
    aic2 = gmm2.aic(X)
    
    print(f"      BIC: {bic2:.2f}")
    print(f"      AIC: {aic2:.2f}")
    
    # Compare
    print(f"\n   Model Comparison:")
    print(f"      ΔBIC (1-comp vs 2-comp): {bic1 - bic2:.2f}")
    print(f"      ΔAIC (1-comp vs 2-comp): {aic1 - aic2:.2f}")
    
    if bic2 < bic1:
        print(f"      ✓ 2-component model is BETTER (lower BIC)")
        print(f"      Interpretation: Data exhibits bimodality")
    else:
        print(f"      ✗ 1-component model is better")
    
    # Extract component parameters
    labels = gmm2.predict(X)
    means = gmm2.means_.flatten()
    stds = np.sqrt(gmm2.covariances_.flatten())
    weights = gmm2.weights_
    
    # Sort by mean
    order = np.argsort(means)
    means = means[order]
    stds = stds[order]
    weights = weights[order]
    
    print(f"\n   2-Component GMM Parameters:")
    print(f"      Component 1 (low NRCI):")
    print(f"         Mean: {means[0]:.6f}")
    print(f"         Std:  {stds[0]:.6f}")
    print(f"         Weight: {weights[0]:.4f} ({weights[0]*100:.2f}%)")
    print(f"      Component 2 (high NRCI):")
    print(f"         Mean: {means[1]:.6f}")
    print(f"         Std:  {stds[1]:.6f}")
    print(f"         Weight: {weights[1]:.4f} ({weights[1]*100:.2f}%)")
    
    # Separation
    separation = (means[1] - means[0]) / np.mean(stds)
    print(f"\n   Separation (in std units): {separation:.4f}")
    
    return {
        'gmm_1_component': {
            'bic': float(bic1),
            'aic': float(aic1)
        },
        'gmm_2_component': {
            'bic': float(bic2),
            'aic': float(aic2),
            'component_1': {
                'mean': float(means[0]),
                'std': float(stds[0]),
                'weight': float(weights[0])
            },
            'component_2': {
                'mean': float(means[1]),
                'std': float(stds[1]),
                'weight': float(weights[1])
            },
            'separation_std_units': float(separation)
        },
        'delta_bic': float(bic1 - bic2),
        'delta_aic': float(aic1 - aic2),
        'bimodal': bool(bic2 < bic1)
    }

def test_gap_significance(nrcis, gap_center=0.248, gap_width=0.03):
    """
    Test significance of the gap at NRCI ≈ 0.248
    """
    print(f"\n[4/6] Gap Significance Testing...")
    print(f"   Testing gap at {gap_center:.3f} ± {gap_width:.3f}")
    
    # Count samples in gap region
    gap_lower = gap_center - gap_width / 2
    gap_upper = gap_center + gap_width / 2
    
    in_gap = np.sum((nrcis >= gap_lower) & (nrcis <= gap_upper))
    below_gap = np.sum(nrcis < gap_lower)
    above_gap = np.sum(nrcis > gap_upper)
    
    print(f"\n   Sample counts:")
    print(f"      Below gap (<{gap_lower:.3f}): {below_gap} ({below_gap/len(nrcis)*100:.2f}%)")
    print(f"      In gap [{gap_lower:.3f}, {gap_upper:.3f}]: {in_gap} ({in_gap/len(nrcis)*100:.2f}%)")
    print(f"      Above gap (>{gap_upper:.3f}): {above_gap} ({above_gap/len(nrcis)*100:.2f}%)")
    
    # Kernel density estimate
    kde = gaussian_kde(nrcis)
    
    # Density at gap center vs neighboring regions
    density_gap = kde(gap_center)[0]
    density_below = kde(gap_lower - 0.05)[0]
    density_above = kde(gap_upper + 0.05)[0]
    
    print(f"\n   Kernel density estimates:")
    print(f"      Density at gap center ({gap_center:.3f}): {density_gap:.6f}")
    print(f"      Density below gap ({gap_lower - 0.05:.3f}): {density_below:.6f}")
    print(f"      Density above gap ({gap_upper + 0.05:.3f}): {density_above:.6f}")
    
    # Relative density drop
    avg_neighbor_density = (density_below + density_above) / 2
    relative_drop = (avg_neighbor_density - density_gap) / avg_neighbor_density * 100
    
    print(f"      Relative density drop at gap: {relative_drop:.2f}%")
    
    # Bootstrap CI for gap density
    print(f"\n   Bootstrap CI for gap density...")
    n_bootstrap = 1000
    gap_densities = []
    
    for _ in range(n_bootstrap):
        sample = np.random.choice(nrcis, size=len(nrcis), replace=True)
        kde_boot = gaussian_kde(sample)
        gap_densities.append(kde_boot(gap_center)[0])
    
    gap_densities = np.array(gap_densities)
    gap_density_ci = np.percentile(gap_densities, [2.5, 50, 97.5])
    
    print(f"      Gap density 95% CI: [{gap_density_ci[0]:.6f}, {gap_density_ci[2]:.6f}]")
    
    return {
        'gap_center': float(gap_center),
        'gap_width': float(gap_width),
        'counts': {
            'below_gap': int(below_gap),
            'in_gap': int(in_gap),
            'above_gap': int(above_gap)
        },
        'densities': {
            'gap_center': float(density_gap),
            'below_gap': float(density_below),
            'above_gap': float(density_above),
            'relative_drop_pct': float(relative_drop)
        },
        'gap_density_ci': {
            'lower': float(gap_density_ci[0]),
            'median': float(gap_density_ci[1]),
            'upper': float(gap_density_ci[2])
        }
    }

def sensitivity_analysis(nrcis):
    """
    Test sensitivity of threshold to data perturbation
    """
    print(f"\n[5/6] Sensitivity Analysis...")
    print("   Testing threshold stability under feature perturbation")
    
    # Original threshold
    threshold_original = np.percentile(nrcis, 95)
    
    # Add noise and recompute
    noise_levels = [0.001, 0.005, 0.01, 0.02, 0.05]
    n_trials = 100
    
    print(f"\n   Noise Level | Mean Threshold | Std | Relative Change")
    print("   " + "-"*60)
    
    sensitivity_results = {}
    
    for noise_level in noise_levels:
        thresholds = []
        for _ in range(n_trials):
            noisy_nrcis = nrcis + np.random.normal(0, noise_level, size=len(nrcis))
            # Clip to valid range
            noisy_nrcis = np.clip(noisy_nrcis, -1, 1)
            thresholds.append(np.percentile(noisy_nrcis, 95))
        
        thresholds = np.array(thresholds)
        mean_threshold = np.mean(thresholds)
        std_threshold = np.std(thresholds)
        relative_change = abs(mean_threshold - threshold_original) / threshold_original * 100
        
        print(f"   {noise_level:11.3f} | {mean_threshold:14.6f} | {std_threshold:.6f} | {relative_change:14.4f}%")
        
        sensitivity_results[f'noise_{noise_level}'] = {
            'noise_level': float(noise_level),
            'mean_threshold': float(mean_threshold),
            'std_threshold': float(std_threshold),
            'relative_change_pct': float(relative_change)
        }
    
    return {
        'original_threshold': float(threshold_original),
        'perturbations': sensitivity_results
    }

def visualize_results(nrcis, bootstrap_results, gmm_results, gap_results):
    """
    Create comprehensive visualizations
    """
    print("\n[6/6] Creating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. NRCI histogram + KDE + GMM components
    ax = axes[0, 0]
    ax.hist(nrcis, bins=100, density=True, alpha=0.5, label='Data')
    
    # KDE
    kde = gaussian_kde(nrcis)
    x_range = np.linspace(nrcis.min(), nrcis.max(), 1000)
    ax.plot(x_range, kde(x_range), 'k-', linewidth=2, label='KDE')
    
    # GMM components
    if gmm_results['bimodal']:
        comp1 = gmm_results['gmm_2_component']['component_1']
        comp2 = gmm_results['gmm_2_component']['component_2']
        
        from scipy.stats import norm
        ax.plot(x_range, 
                comp1['weight'] * norm.pdf(x_range, comp1['mean'], comp1['std']),
                'r--', label='Component 1')
        ax.plot(x_range,
                comp2['weight'] * norm.pdf(x_range, comp2['mean'], comp2['std']),
                'b--', label='Component 2')
    
    # Gap
    gap_center = gap_results['gap_center']
    ax.axvline(gap_center, color='orange', linestyle=':', linewidth=2, label=f'Gap ({gap_center:.3f})')
    
    # Threshold
    threshold = bootstrap_results['original_threshold']
    ax.axvline(threshold, color='green', linestyle='--', linewidth=2, label=f'Threshold ({threshold:.3f})')
    
    ax.set_xlabel('NRCI')
    ax.set_ylabel('Density')
    ax.set_title('NRCI Distribution with Bimodal Fit')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Bootstrap distribution
    ax = axes[0, 1]
    bootstrap_dist = bootstrap_results['bootstrap_distribution']
    ax.hist(bootstrap_dist, bins=50, alpha=0.7, edgecolor='black')
    ax.axvline(bootstrap_results['bootstrap_median'], color='red', linestyle='--', 
               linewidth=2, label='Median')
    ax.axvline(bootstrap_results['ci_lower'], color='orange', linestyle=':', 
               linewidth=2, label='95% CI')
    ax.axvline(bootstrap_results['ci_upper'], color='orange', linestyle=':', linewidth=2)
    ax.set_xlabel('95th Percentile')
    ax.set_ylabel('Frequency')
    ax.set_title('Bootstrap Distribution of Threshold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Gap region detail
    ax = axes[1, 0]
    gap_center = gap_results['gap_center']
    gap_width = gap_results['gap_width']
    
    # Zoom into gap region
    gap_region = nrcis[(nrcis >= gap_center - 0.1) & (nrcis <= gap_center + 0.1)]
    ax.hist(gap_region, bins=50, alpha=0.7, edgecolor='black')
    ax.axvline(gap_center - gap_width/2, color='red', linestyle='--', linewidth=2)
    ax.axvline(gap_center + gap_width/2, color='red', linestyle='--', linewidth=2)
    ax.set_xlabel('NRCI')
    ax.set_ylabel('Count')
    ax.set_title(f'Gap Region Detail ({gap_center:.3f} ± {gap_width:.3f})')
    ax.grid(True, alpha=0.3)
    
    # 4. Cumulative distribution
    ax = axes[1, 1]
    sorted_nrcis = np.sort(nrcis)
    cumulative = np.arange(1, len(sorted_nrcis) + 1) / len(sorted_nrcis) * 100
    ax.plot(sorted_nrcis, cumulative, 'b-', linewidth=2)
    ax.axhline(95, color='green', linestyle='--', linewidth=2, label='95th percentile')
    ax.axvline(threshold, color='green', linestyle='--', linewidth=2)
    ax.set_xlabel('NRCI')
    ax.set_ylabel('Cumulative Percentage')
    ax.set_title('Cumulative Distribution Function')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/validation_threshold_bimodality.png', dpi=150)
    print("   ✓ Saved validation_threshold_bimodality.png")

def save_results(bootstrap, gmm, gap, sensitivity):
    """Save all validation results"""
    print("\n   Saving results...")
    
    summary = {
        'random_seed': RANDOM_SEED,
        'bootstrap_threshold_ci': bootstrap,
        'bimodality_gmm': gmm,
        'gap_significance': gap,
        'sensitivity_analysis': sensitivity
    }
    
    with open('results/validation_threshold_bimodality.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved validation_threshold_bimodality.json")

def main():
    print("="*80)
    print("STATISTICAL VALIDATION: THRESHOLD AND BIMODALITY")
    print("="*80)
    print("Bootstrap CI, GMM fitting, gap significance, sensitivity analysis")
    print("="*80)
    
    # Load data
    nrcis = load_data()
    
    # 1. Bootstrap CI for threshold
    bootstrap_results = bootstrap_threshold_ci(nrcis, percentile=95, n_bootstrap=2000)
    
    # 2. Bimodality testing with GMM
    gmm_results = test_bimodality_gmm(nrcis)
    
    # 3. Gap significance
    gap_results = test_gap_significance(nrcis, gap_center=0.248, gap_width=0.03)
    
    # 4. Sensitivity analysis
    sensitivity_results = sensitivity_analysis(nrcis)
    
    # 5. Visualize
    visualize_results(nrcis, bootstrap_results, gmm_results, gap_results)
    
    # 6. Save
    save_results(bootstrap_results, gmm_results, gap_results, sensitivity_results)
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE!")
    print("="*80)
    print("\nKey Findings:")
    print(f"   Threshold 95% CI: [{bootstrap_results['ci_lower']:.6f}, {bootstrap_results['ci_upper']:.6f}]")
    print(f"   Bimodal: {gmm_results['bimodal']}")
    print(f"   Gap density drop: {gap_results['densities']['relative_drop_pct']:.2f}%")

if __name__ == '__main__':
    main()
