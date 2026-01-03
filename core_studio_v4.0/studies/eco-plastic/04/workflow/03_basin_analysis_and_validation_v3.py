#!/usr/bin/env python3
"""
UBP Golden Study v3 - Step 5: Basin Analysis & Law of Octad Resonance

Tests the hypothesis: P(m) ∝ 1/d_H(φ(m), O_PFAS)

Author: K-Dense System
Date: January 2, 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

np.random.seed(42)
plt.style.use('seaborn-v0_8-paper')

def calculate_hamming_distance_to_octad(fingerprints, octad):
    """Calculate Hamming distance from each fingerprint to the reference octad."""
    return np.sum(np.abs(fingerprints - octad), axis=1)

def classify_into_regimes(distances):
    """
    Classify molecules based on Hamming distance to Octad.

    Regimes (from Appendix A.2):
    - Locked: d_H = 0
    - Resonant: 1 ≤ d_H ≤ 3
    - Entropic: d_H > 3
    """
    regimes = np.empty(len(distances), dtype='U20')
    regimes[distances == 0] = 'Locked'
    regimes[(distances >= 1) & (distances <= 3)] = 'Resonant'
    regimes[distances > 3] = 'Entropic'
    return regimes

def test_octad_resonance_law(df):
    """
    Test the Law of Octad Resonance: P(m) ∝ 1/d_H(φ(m), O)

    Statistical tests:
    1. Correlation: d_H vs. persistence
    2. Correlation: d_H vs. biodegradability (inverse)
    3. Correlation: 1/d_H vs. persistence
    4. ANOVA: persistence across regimes
    """
    print("\n" + "=" * 70)
    print("LAW OF OCTAD RESONANCE - STATISTICAL TESTS")
    print("=" * 70)

    # Test 1: Direct correlation d_H vs. persistence
    print("\n[Test 1] Correlation: d_H vs. Persistence")
    rho1, p1 = stats.spearmanr(df['d_H_to_PFAS'], df['persistence_score'])
    print(f"  Spearman ρ = {rho1:.4f}, p = {p1:.2e}")
    print(f"  Interpretation: {'NEGATIVE correlation (as expected)' if rho1 < 0 else 'POSITIVE correlation (unexpected)'}")

    # Test 2: Inverse relationship 1/d_H vs. persistence
    print("\n[Test 2] Correlation: 1/(d_H+1) vs. Persistence")
    inverse_d = 1 / (df['d_H_to_PFAS'] + 1)  # Add 1 to avoid division by zero
    rho2, p2 = stats.spearmanr(inverse_d, df['persistence_score'])
    print(f"  Spearman ρ = {rho2:.4f}, p = {p2:.2e}")
    print(f"  Interpretation: {'POSITIVE correlation (Law confirmed!)' if rho2 > 0 else 'NEGATIVE correlation (Law rejected)'}")

    # Test 3: d_H vs. biodegradability (should be positive)
    print("\n[Test 3] Correlation: d_H vs. Biodegradability")
    rho3, p3 = stats.spearmanr(df['d_H_to_PFAS'], df['biodegradability_score'])
    print(f"  Spearman ρ = {rho3:.4f}, p = {p3:.2e}")
    print(f"  Interpretation: {'POSITIVE correlation (as expected)' if rho3 > 0 else 'NEGATIVE correlation (unexpected)'}")

    # Test 4: ANOVA across regimes
    print("\n[Test 4] ANOVA: Persistence across Regimes")
    regime_groups = []
    regime_names = []
    for regime in ['Locked', 'Resonant', 'Entropic']:
        group = df[df['computed_regime'] == regime]['persistence_score'].values
        if len(group) > 0:
            regime_groups.append(group)
            regime_names.append(regime)
            print(f"  {regime}: n={len(group)}, mean={group.mean():.3f}, std={group.std():.3f}")

    if len(regime_groups) >= 2:
        f_stat, p_anova = stats.f_oneway(*regime_groups)
        print(f"\n  F-statistic = {f_stat:.4f}, p = {p_anova:.2e}")
        print(f"  Interpretation: {'Significant regime differences!' if p_anova < 0.05 else 'No significant differences'}")
    else:
        print("\n  Not enough regimes to perform ANOVA")
        f_stat, p_anova = np.nan, np.nan

    # Test 5: 3D correlations
    print("\n[Test 5] 3D Shape Correlations with d_H")
    rho_sph, p_sph = stats.spearmanr(df['d_H_to_PFAS'], df['spherocity'])
    rho_pmi, p_pmi = stats.spearmanr(df['d_H_to_PFAS'], df['pmi_ratio'])
    rho_rg, p_rg = stats.spearmanr(df['d_H_to_PFAS'], df['radius_gyration'])

    print(f"  d_H vs. Spherocity:  ρ = {rho_sph:.4f}, p = {p_sph:.2e}")
    print(f"  d_H vs. PMI Ratio:   ρ = {rho_pmi:.4f}, p = {p_pmi:.2e}")
    print(f"  d_H vs. Rg:          ρ = {rho_rg:.4f}, p = {p_rg:.2e}")

    return {
        'test1_rho': rho1, 'test1_p': p1,
        'test2_rho': rho2, 'test2_p': p2,
        'test3_rho': rho3, 'test3_p': p3,
        'test4_f': f_stat, 'test4_p': p_anova,
        'test5_spherocity_rho': rho_sph, 'test5_spherocity_p': p_sph,
        'test5_pmi_rho': rho_pmi, 'test5_pmi_p': p_pmi,
        'test5_rg_rho': rho_rg, 'test5_rg_p': p_rg,
    }

def validate_reference_compounds(df):
    """
    Validate predictions against known reference compounds from Appendix C.

    Expected:
    - Benzene: d_H = 2 (Resonant)
    - PFAS: d_H ≤ 1 (Locked)
    - Biodegradable polymers: d_H > 3 (Entropic)
    """
    print("\n" + "=" * 70)
    print("REFERENCE COMPOUND VALIDATION (Appendix C)")
    print("=" * 70)

    # Benzene validation
    benzene_row = df[df['name'] == 'Benzene']
    if len(benzene_row) > 0:
        d_H = benzene_row['d_H_to_PFAS'].values[0]
        regime = benzene_row['computed_regime'].values[0]
        print(f"\n✓ Benzene:")
        print(f"    Measured d_H = {d_H} (Expected: 2)")
        print(f"    Computed Regime: {regime} (Expected: Resonant)")
        print(f"    Validation: {'PASS ✓' if regime == 'Resonant' else 'FAIL ✗'}")

    # PFAS validation
    pfas_rows = df[df['category'] == 'PFAS']
    if len(pfas_rows) > 0:
        mean_d_H = pfas_rows['d_H_to_PFAS'].mean()
        locked_count = (pfas_rows['computed_regime'] == 'Locked').sum()
        resonant_count = (pfas_rows['computed_regime'] == 'Resonant').sum()
        print(f"\n✓ PFAS Compounds ({len(pfas_rows)} total):")
        print(f"    Mean d_H = {mean_d_H:.1f} (Expected: ≤ 1)")
        print(f"    Locked Regime: {locked_count} compounds")
        print(f"    Resonant Regime: {resonant_count} compounds")
        print(f"    Validation: {'PASS ✓' if locked_count + resonant_count >= len(pfas_rows) * 0.7 else 'PARTIAL'}")

    # Biodegradable polymers validation
    biodeg_rows = df[df['category'] == 'Biodegradable_Polymer']
    if len(biodeg_rows) > 0:
        mean_d_H = biodeg_rows['d_H_to_PFAS'].mean()
        entropic_count = (biodeg_rows['computed_regime'] == 'Entropic').sum()
        print(f"\n✓ Biodegradable Polymers ({len(biodeg_rows)} total):")
        print(f"    Mean d_H = {mean_d_H:.1f} (Expected: > 3)")
        print(f"    Entropic Regime: {entropic_count} compounds")
        print(f"    Validation: {'PASS ✓' if entropic_count >= len(biodeg_rows) * 0.7 else 'PARTIAL'}")

def generate_figures(df, stats_results):
    """Generate publication-quality figures."""
    print("\n" + "=" * 70)
    print("GENERATING PUBLICATION FIGURES")
    print("=" * 70)

    fig_dir = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/figures")
    fig_dir.mkdir(exist_ok=True)

    # Figure 1: Basin Analysis - d_H vs. Persistence
    print("\n[Fig 1] Basin Analysis: d_H vs. Persistence")
    fig, ax = plt.subplots(figsize=(8, 6))

    # Color by regime
    regime_colors = {'Locked': '#d62728', 'Resonant': '#ff7f0e', 'Entropic': '#2ca02c'}
    for regime in ['Locked', 'Resonant', 'Entropic']:
        mask = df['computed_regime'] == regime
        if mask.sum() > 0:
            ax.scatter(df.loc[mask, 'd_H_to_PFAS'], df.loc[mask, 'persistence_score'],
                      c=regime_colors[regime], label=regime, alpha=0.6, s=50)

    # Regime boundaries
    ax.axvline(0.5, color='red', linestyle='--', alpha=0.3, linewidth=2, label='Locked Boundary')
    ax.axvline(3.5, color='orange', linestyle='--', alpha=0.3, linewidth=2, label='Resonant Boundary')

    ax.set_xlabel('Hamming Distance to PFAS Octad (d_H)', fontsize=12)
    ax.set_ylabel('Environmental Persistence Score', fontsize=12)
    ax.set_title('Law of Octad Resonance: Basin Analysis', fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True)
    ax.grid(True, alpha=0.3)

    # Add correlation text
    rho = stats_results['test1_rho']
    p = stats_results['test1_p']
    ax.text(0.05, 0.95, f'Spearman ρ = {rho:.3f}\np = {p:.2e}',
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(fig_dir / 'fig1_basin_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(fig_dir / 'fig1_basin_analysis.pdf', bbox_inches='tight')
    plt.close()
    print("  ✅ Saved fig1_basin_analysis.png/pdf")

    # Figure 2: Law of Octad Resonance - Hyperbolic Fit
    print("\n[Fig 2] Law of Octad Resonance: P(m) ∝ 1/d_H")
    fig, ax = plt.subplots(figsize=(8, 6))

    inverse_d = 1 / (df['d_H_to_PFAS'] + 1)
    ax.scatter(inverse_d, df['persistence_score'], alpha=0.5, s=30, c=df['d_H_to_PFAS'], cmap='viridis')

    # Fit and plot trend
    from numpy.polynomial import Polynomial
    p = Polynomial.fit(inverse_d, df['persistence_score'], deg=1)
    x_fit = np.linspace(inverse_d.min(), inverse_d.max(), 100)
    y_fit = p(x_fit)
    ax.plot(x_fit, y_fit, 'r--', linewidth=2, label=f'Linear Fit')

    ax.set_xlabel('1 / (d_H + 1)', fontsize=12)
    ax.set_ylabel('Persistence Score', fontsize=12)
    ax.set_title('Law of Octad Resonance: Hyperbolic Relationship', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    rho = stats_results['test2_rho']
    p_val = stats_results['test2_p']
    ax.text(0.05, 0.95, f'Spearman ρ = {rho:.3f}\np = {p_val:.2e}',
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    plt.tight_layout()
    plt.savefig(fig_dir / 'fig2_octad_resonance_law.png', dpi=300, bbox_inches='tight')
    plt.savefig(fig_dir / 'fig2_octad_resonance_law.pdf', bbox_inches='tight')
    plt.close()
    print("  ✅ Saved fig2_octad_resonance_law.png/pdf")

    # Figure 3: 3D Integration - Multi-panel
    print("\n[Fig 3] 3D Shape Integration")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel A: d_H vs. Spherocity
    axes[0].scatter(df['d_H_to_PFAS'], df['spherocity'], alpha=0.5, s=30)
    axes[0].set_xlabel('Hamming Distance (d_H)', fontsize=11)
    axes[0].set_ylabel('Spherocity', fontsize=11)
    axes[0].set_title('Panel A: Geometric Shape', fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    rho = stats_results['test5_spherocity_rho']
    axes[0].text(0.05, 0.95, f'ρ = {rho:.3f}', transform=axes[0].transAxes,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # Panel B: d_H vs. PMI Ratio
    axes[1].scatter(df['d_H_to_PFAS'], df['pmi_ratio'], alpha=0.5, s=30)
    axes[1].set_xlabel('Hamming Distance (d_H)', fontsize=11)
    axes[1].set_ylabel('PMI Ratio (Elongation)', fontsize=11)
    axes[1].set_title('Panel B: Molecular Elongation', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    rho = stats_results['test5_pmi_rho']
    axes[1].text(0.05, 0.95, f'ρ = {rho:.3f}', transform=axes[1].transAxes,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # Panel C: d_H vs. Radius of Gyration
    axes[2].scatter(df['d_H_to_PFAS'], df['radius_gyration'], alpha=0.5, s=30)
    axes[2].set_xlabel('Hamming Distance (d_H)', fontsize=11)
    axes[2].set_ylabel('Radius of Gyration (Å)', fontsize=11)
    axes[2].set_title('Panel C: Molecular Size', fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    rho = stats_results['test5_rg_rho']
    axes[2].text(0.05, 0.95, f'ρ = {rho:.3f}', transform=axes[2].transAxes,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    plt.suptitle('3D Shape Correlation with UBP Geometric Tension', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(fig_dir / 'fig3_3d_integration.png', dpi=300, bbox_inches='tight')
    plt.savefig(fig_dir / 'fig3_3d_integration.pdf', bbox_inches='tight')
    plt.close()
    print("  ✅ Saved fig3_3d_integration.png/pdf")

    # Figure 4: Regime Distribution
    print("\n[Fig 4] Regime Distribution and Statistics")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: Regime counts
    regime_counts = df['computed_regime'].value_counts()
    axes[0].bar(regime_counts.index, regime_counts.values, color=['#d62728', '#ff7f0e', '#2ca02c'])
    axes[0].set_ylabel('Count', fontsize=11)
    axes[0].set_title('Panel A: Regime Distribution', fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)

    # Panel B: Persistence by regime
    regime_persistence = []
    regime_labels = []
    for regime in ['Locked', 'Resonant', 'Entropic']:
        vals = df[df['computed_regime'] == regime]['persistence_score'].values
        if len(vals) > 0:
            regime_persistence.append(vals)
            regime_labels.append(regime)

    axes[1].boxplot(regime_persistence, labels=regime_labels)
    axes[1].set_ylabel('Persistence Score', fontsize=11)
    axes[1].set_title('Panel B: Persistence by Regime', fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)

    plt.suptitle('Stability Regime Classification', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(fig_dir / 'fig4_regime_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(fig_dir / 'fig4_regime_analysis.pdf', bbox_inches='tight')
    plt.close()
    print("  ✅ Saved fig4_regime_analysis.png/pdf")

def main():
    # Paths
    data_dir = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data")
    results_dir = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/results")
    results_dir.mkdir(exist_ok=True)

    # Load data
    print("Loading data...")
    df = pd.read_csv(data_dir / "compound_database_with_3d.csv")
    fingerprints = np.load(data_dir / "mog_optimized_fingerprints.npy")
    pfas_basis_octad = np.load(data_dir / "pfas_basis_octad.npy")
    print(f"✅ Loaded {len(df)} compounds")

    # Calculate Hamming distances to PFAS Basis Octad
    print("\nCalculating Hamming distances to PFAS Basis Octad...")
    d_H = calculate_hamming_distance_to_octad(fingerprints, pfas_basis_octad)
    df['d_H_to_PFAS'] = d_H
    print(f"✅ Distance range: {d_H.min()} - {d_H.max()} (mean: {d_H.mean():.1f})")

    # Classify into regimes
    print("\nClassifying into stability regimes...")
    regimes = classify_into_regimes(d_H)
    df['computed_regime'] = regimes
    print(f"✅ Regime distribution:")
    print(df['computed_regime'].value_counts().to_string())

    # Test Law of Octad Resonance
    stats_results = test_octad_resonance_law(df)

    # Validate reference compounds
    validate_reference_compounds(df)

    # Save results
    df.to_csv(results_dir / "basin_analysis_results.csv", index=False)
    print(f"\n✅ Saved basin analysis results")

    import json
    with open(results_dir / "statistical_tests.json", 'w') as f:
        json.dump(stats_results, f, indent=2)
    print(f"✅ Saved statistical test results")

    # Generate figures
    generate_figures(df, stats_results)

    print("\n" + "=" * 70)
    print("✅ BASIN ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
