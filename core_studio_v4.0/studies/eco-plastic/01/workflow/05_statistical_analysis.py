#!/usr/bin/env python3
"""
Step 5: Statistical Analysis
Performs correlation analysis and hypothesis testing on UBP metrics vs. real-world properties.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.stats import mannwhitneyu, spearmanr, kruskal
import json

print("="*80)
print("STEP 5: STATISTICAL ANALYSIS")
print("="*80)

# Set random seed for reproducibility
np.random.seed(42)

print("\n[1/6] Loading UBP metrics...")
metrics_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_metrics.csv")
df = pd.read_csv(metrics_path)
print(f"  ✓ Loaded {len(df)} materials with UBP metrics")

print("\n[2/6] Descriptive statistics...")
print("\nUBP Metrics Summary:")
ubp_cols = ['nrci', 'symmetry_tax', 'stability_score']
print(df[ubp_cols].describe().to_string())

print("\n\nGrouped by Biodegradability:")
print(df.groupby('biodegradable')[ubp_cols].agg(['mean', 'std', 'min', 'max']).to_string())

print("\n\nGrouped by Category:")
print(df.groupby('category')[['symmetry_tax']].agg(['mean', 'count']).to_string())

print("\n[3/6] Correlation analysis...")

# Since stability_score is constant (all 0), use symmetry_tax instead
# Lower symmetry tax might correlate with lower persistence (hypothesis)

correlations = []

# Correlation 1: Symmetry Tax vs. Persistence Score
spearman_corr, p_val = spearmanr(df['symmetry_tax'], df['persistence_score'])
correlations.append({
    'metric_1': 'symmetry_tax',
    'metric_2': 'persistence_score',
    'correlation': 'Spearman',
    'coefficient': spearman_corr,
    'p_value': p_val,
    'significant': p_val < 0.05,
    'interpretation': 'Higher tax = higher persistence?' if spearman_corr > 0 else 'Lower tax = higher persistence?'
})

print(f"\n  Symmetry Tax vs. Persistence Score:")
print(f"    Spearman r = {spearman_corr:.4f}, p = {p_val:.4f}")
if p_val < 0.05:
    print(f"    ✓ Significant correlation (p < 0.05)")
else:
    print(f"    ✗ Not significant (p >= 0.05)")

# Correlation 2: Symmetry Tax vs. Toxicity Score
spearman_corr2, p_val2 = spearmanr(df['symmetry_tax'], df['toxicity_score'])
correlations.append({
    'metric_1': 'symmetry_tax',
    'metric_2': 'toxicity_score',
    'correlation': 'Spearman',
    'coefficient': spearman_corr2,
    'p_value': p_val2,
    'significant': p_val2 < 0.05,
    'interpretation': 'Higher tax = higher toxicity?' if spearman_corr2 > 0 else 'Lower tax = higher toxicity?'
})

print(f"\n  Symmetry Tax vs. Toxicity Score:")
print(f"    Spearman r = {spearman_corr2:.4f}, p = {p_val2:.4f}")
if p_val2 < 0.05:
    print(f"    ✓ Significant correlation (p < 0.05)")
else:
    print(f"    ✗ Not significant (p >= 0.05)")

# Correlation 3: NRCI vs. Persistence Score
spearman_corr3, p_val3 = spearmanr(df['nrci'], df['persistence_score'])
correlations.append({
    'metric_1': 'nrci',
    'metric_2': 'persistence_score',
    'correlation': 'Spearman',
    'coefficient': spearman_corr3,
    'p_value': p_val3,
    'significant': p_val3 < 0.05,
    'interpretation': 'Coherence vs. persistence'
})

print(f"\n  NRCI vs. Persistence Score:")
print(f"    Spearman r = {spearman_corr3:.4f}, p = {p_val3:.4f}")

# Correlation 4: Symmetry Tax vs. Molecular Weight
spearman_corr4, p_val4 = spearmanr(df['symmetry_tax'], df['molecular_weight'])
correlations.append({
    'metric_1': 'symmetry_tax',
    'metric_2': 'molecular_weight',
    'correlation': 'Spearman',
    'coefficient': spearman_corr4,
    'p_value': p_val4,
    'significant': p_val4 < 0.05,
    'interpretation': 'Molecular size effect'
})

print(f"\n  Symmetry Tax vs. Molecular Weight:")
print(f"    Spearman r = {spearman_corr4:.4f}, p = {p_val4:.4f}")

print("\n[4/6] Group comparisons...")

# Test hypothesis: Biodegradable vs. Non-biodegradable
biodeg = df[df['biodegradable'] == True]['symmetry_tax']
non_biodeg = df[df['biodegradable'] == False]['symmetry_tax']

print(f"\n  Biodegradable vs. Non-biodegradable (Symmetry Tax):")
print(f"    Biodegradable (n={len(biodeg)}): mean={biodeg.mean():.4f}, std={biodeg.std():.4f}")
print(f"    Non-biodegradable (n={len(non_biodeg)}): mean={non_biodeg.mean():.4f}, std={non_biodeg.std():.4f}")

# Mann-Whitney U test (non-parametric)
u_stat, u_pval = mannwhitneyu(biodeg, non_biodeg, alternative='two-sided')
effect_size = u_stat / (len(biodeg) * len(non_biodeg))  # Rank-biserial correlation approximation

print(f"    Mann-Whitney U = {u_stat:.2f}, p = {u_pval:.4f}")
print(f"    Effect size (rank-biserial) ≈ {effect_size:.4f}")

if u_pval < 0.05:
    print(f"    ✓ Significant difference (p < 0.05)")
    if biodeg.mean() < non_biodeg.mean():
        print(f"    → Biodegradable materials have LOWER symmetry tax")
    else:
        print(f"    → Biodegradable materials have HIGHER symmetry tax")
else:
    print(f"    ✗ No significant difference (p >= 0.05)")

group_comparison = {
    'comparison': 'Biodegradable vs. Non-biodegradable',
    'metric': 'symmetry_tax',
    'group1_n': int(len(biodeg)),
    'group1_mean': float(biodeg.mean()),
    'group1_std': float(biodeg.std()),
    'group2_n': int(len(non_biodeg)),
    'group2_mean': float(non_biodeg.mean()),
    'group2_std': float(non_biodeg.std()),
    'test': 'Mann-Whitney U',
    'statistic': float(u_stat),
    'p_value': float(u_pval),
    'effect_size': float(effect_size),
    'significant': bool(u_pval < 0.05)
}

# Test 2: Commodity vs. Engineering plastics (excluding biodegradable)
commodity = df[df['category'] == 'Commodity Plastic']['symmetry_tax']
engineering = df[df['category'] == 'Engineering Plastic']['symmetry_tax']

print(f"\n  Commodity vs. Engineering Plastics (Symmetry Tax):")
print(f"    Commodity (n={len(commodity)}): mean={commodity.mean():.4f}, std={commodity.std():.4f}")
print(f"    Engineering (n={len(engineering)}): mean={engineering.mean():.4f}, std={engineering.std():.4f}")

u_stat2, u_pval2 = mannwhitneyu(commodity, engineering, alternative='two-sided')
print(f"    Mann-Whitney U = {u_stat2:.2f}, p = {u_pval2:.4f}")

if u_pval2 < 0.05:
    print(f"    ✓ Significant difference (p < 0.05)")
else:
    print(f"    ✗ No significant difference (p >= 0.05)")

print("\n[5/6] Multiple group comparison (Kruskal-Wallis)...")

# Test across all categories
categories = df['category'].unique()
groups = [df[df['category'] == cat]['symmetry_tax'].values for cat in categories]

h_stat, h_pval = kruskal(*groups)
print(f"\n  Kruskal-Wallis test across {len(categories)} categories:")
print(f"    H = {h_stat:.4f}, p = {h_pval:.4f}")

if h_pval < 0.05:
    print(f"    ✓ Significant differences among categories (p < 0.05)")
else:
    print(f"    ✗ No significant differences (p >= 0.05)")

print("\n[6/6] Saving statistical results...")

# Save correlation matrix
corr_df = pd.DataFrame(correlations)
corr_csv = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/results/correlation_matrix.csv")
corr_df.to_csv(corr_csv, index=False)
print(f"  ✓ Correlations saved to: {corr_csv}")

# Save group comparisons
comp_json = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/results/group_comparisons.json")
with open(comp_json, 'w') as f:
    json.dump({
        'biodegradable_comparison': group_comparison,
        'kruskal_wallis': {
            'test': 'Kruskal-Wallis',
            'categories': list(categories),
            'H_statistic': float(h_stat),
            'p_value': float(h_pval),
            'significant': bool(h_pval < 0.05)
        }
    }, f, indent=2)
print(f"  ✓ Group comparisons saved to: {comp_json}")

# Create summary statistics table
summary_stats = df.groupby('category').agg({
    'symmetry_tax': ['count', 'mean', 'std', 'min', 'max'],
    'nrci': ['mean', 'std'],
    'persistence_score': 'mean',
    'toxicity_score': 'mean'
}).round(4)

summary_csv = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/results/summary_statistics.csv")
summary_stats.to_csv(summary_csv)
print(f"  ✓ Summary statistics saved to: {summary_csv}")

print("\n" + "="*80)
print("STATISTICAL ANALYSIS COMPLETE")
print("="*80)

print("\nKey Findings:")
print(f"  1. Symmetry Tax range: {df['symmetry_tax'].min():.4f} - {df['symmetry_tax'].max():.4f}")
print(f"  2. Correlation with persistence: r = {spearman_corr:.4f} (p = {p_val:.4f})")
print(f"  3. Biodegradable vs. Non-biodegradable: p = {u_pval:.4f}")

if u_pval < 0.05:
    if biodeg.mean() < non_biodeg.mean():
        print(f"     → Biodegradable materials show LOWER symmetry tax")
    else:
        print(f"     → Biodegradable materials show HIGHER symmetry tax")
else:
    print(f"     → No significant difference detected")

print("\n✓ Ready for visualization")
