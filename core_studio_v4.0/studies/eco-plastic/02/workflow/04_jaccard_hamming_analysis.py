#!/usr/bin/env python3
"""
Jaccard and Hamming Distance Analysis for OffBits
===================================================
Apply binary similarity metrics as specified in UBP KB
- Jaccard similarity/distance for OffBits analysis
- Hamming distance for bit-level differences
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.spatial.distance import jaccard, hamming
from scipy.stats import spearmanr, pearsonr
from sklearn.metrics import pairwise_distances
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")

print("=" * 70)
print("JACCARD AND HAMMING DISTANCE ANALYSIS")
print("=" * 70)

# Load data
df = pd.read_csv(BASE_DIR / "data" / "large_chemicals_dataset.csv")
print(f"\nLoaded {len(df)} compounds")

# Load fingerprints
strategies = [
    "strategy_1_functional_groups",
    "strategy_2_lack_protection",
    "strategy_3_balanced",
    "strategy_4_persistence"
]

fingerprints = {}
for strategy in strategies:
    fp_file = BASE_DIR / "data" / "fingerprints" / f"{strategy}.npy"
    fingerprints[strategy] = np.load(fp_file)
    print(f"   Loaded {strategy}: {fingerprints[strategy].shape}")


# ============================================================================
# JACCARD DISTANCE FOR OFFBITS
# ============================================================================

def jaccard_offbits(fp1, fp2):
    """
    Jaccard distance focusing on OffBits (0s)
    OffBits_A = indices where fp1 == 0
    OffBits_B = indices where fp2 == 0
    Jaccard = |A ∩ B| / |A ∪ B|
    """
    offbits_a = set(np.where(fp1 == 0)[0])
    offbits_b = set(np.where(fp2 == 0)[0])

    if len(offbits_a.union(offbits_b)) == 0:
        return 0.0  # Identical (all OnBits)

    intersection = len(offbits_a.intersection(offbits_b))
    union = len(offbits_a.union(offbits_b))

    return 1.0 - (intersection / union)  # Distance (0=identical, 1=completely different)


def jaccard_onbits(fp1, fp2):
    """
    Standard Jaccard distance for OnBits (1s)
    """
    onbits_a = set(np.where(fp1 == 1)[0])
    onbits_b = set(np.where(fp2 == 1)[0])

    if len(onbits_a.union(onbits_b)) == 0:
        return 0.0  # Identical (all OffBits)

    intersection = len(onbits_a.intersection(onbits_b))
    union = len(onbits_a.union(onbits_b))

    return 1.0 - (intersection / union)


def hamming_distance(fp1, fp2):
    """
    Hamming distance: count of differing bits
    """
    return np.sum(fp1 != fp2)


# ============================================================================
# COMPUTE DISTANCE MATRICES
# ============================================================================

print("\n[1/4] Computing distance matrices...")

results = {}
for strategy in strategies:
    print(f"\n   Strategy: {strategy}")
    fps = fingerprints[strategy]
    n = len(fps)

    # Initialize distance matrices
    jaccard_offbits_matrix = np.zeros((n, n))
    jaccard_onbits_matrix = np.zeros((n, n))
    hamming_matrix = np.zeros((n, n))

    # Compute pairwise distances
    for i in range(n):
        if i % 20 == 0:
            print(f"      Progress: {i}/{n} ({100*i/n:.1f}%)")
        for j in range(i+1, n):
            jaccard_offbits_matrix[i, j] = jaccard_offbits(fps[i], fps[j])
            jaccard_offbits_matrix[j, i] = jaccard_offbits_matrix[i, j]

            jaccard_onbits_matrix[i, j] = jaccard_onbits(fps[i], fps[j])
            jaccard_onbits_matrix[j, i] = jaccard_onbits_matrix[i, j]

            hamming_matrix[i, j] = hamming_distance(fps[i], fps[j])
            hamming_matrix[j, i] = hamming_matrix[i, j]

    print(f"      ✓ Computed {n*n} pairwise distances")

    results[strategy] = {
        "jaccard_offbits": jaccard_offbits_matrix,
        "jaccard_onbits": jaccard_onbits_matrix,
        "hamming": hamming_matrix
    }

    # Save matrices
    np.save(BASE_DIR / "data" / f"{strategy}_jaccard_offbits.npy", jaccard_offbits_matrix)
    np.save(BASE_DIR / "data" / f"{strategy}_jaccard_onbits.npy", jaccard_onbits_matrix)
    np.save(BASE_DIR / "data" / f"{strategy}_hamming.npy", hamming_matrix)


# ============================================================================
# CORRELATION WITH PROPERTIES
# ============================================================================

print("\n[2/4] Computing correlations with chemical properties...")

target_properties = ['persistent', 'biodegradable', 'toxic']
correlation_results = []

for strategy in strategies:
    print(f"\n   Strategy: {strategy}")
    matrices = results[strategy]

    for prop in target_properties:
        prop_values = df[prop].values

        # For each distance metric, compute average distance to compounds with high/low property
        for metric_name, matrix in matrices.items():
            # Average distance from each compound to all others
            avg_distances = np.mean(matrix, axis=1)

            # Correlation between average distance and property value
            corr_spearman, p_spearman = spearmanr(avg_distances, prop_values)
            corr_pearson, p_pearson = pearsonr(avg_distances, prop_values)

            correlation_results.append({
                "strategy": strategy,
                "metric": metric_name,
                "property": prop,
                "correlation_spearman": corr_spearman,
                "p_value_spearman": p_spearman,
                "correlation_pearson": corr_pearson,
                "p_value_pearson": p_pearson,
                "significant": p_spearman < 0.05
            })

            if p_spearman < 0.05:
                print(f"      ✓ {metric_name} × {prop}: r={corr_spearman:.3f}, p={p_spearman:.4f} ***")
            else:
                print(f"        {metric_name} × {prop}: r={corr_spearman:.3f}, p={p_spearman:.4f}")

# Save correlation results
corr_df = pd.DataFrame(correlation_results)
corr_file = BASE_DIR / "results" / "jaccard_hamming_correlations.csv"
corr_df.to_csv(corr_file, index=False)
print(f"\n✓ Correlations saved to: {corr_file}")


# ============================================================================
# FIND BEST PERFORMING STRATEGY
# ============================================================================

print("\n[3/4] Identifying best performing strategies...")

# Find significant correlations
significant = corr_df[corr_df['significant'] == True].sort_values('correlation_spearman', key=abs, ascending=False)

if len(significant) > 0:
    print(f"\n✓ Found {len(significant)} significant correlations!")
    print("\nTop 5 correlations:")
    print(significant[['strategy', 'metric', 'property', 'correlation_spearman', 'p_value_spearman']].head(10))

    best_result = significant.iloc[0]
    print(f"\n🎯 BEST RESULT:")
    print(f"   Strategy: {best_result['strategy']}")
    print(f"   Metric: {best_result['metric']}")
    print(f"   Property: {best_result['property']}")
    print(f"   Correlation: {best_result['correlation_spearman']:.4f}")
    print(f"   P-value: {best_result['p_value_spearman']:.6f}")
else:
    print("\n⚠ No significant correlations found at p < 0.05")
    print("\nTop correlations (by absolute value):")
    top_abs = corr_df.iloc[corr_df['correlation_spearman'].abs().argsort()[::-1]].head(10)
    print(top_abs[['strategy', 'metric', 'property', 'correlation_spearman', 'p_value_spearman']])


# ============================================================================
# OFFBITS VS ONBITS COMPARISON
# ============================================================================

print("\n[4/4] Comparing OffBits vs OnBits performance...")

# Group by strategy and property, compare Jaccard OffBits vs OnBits
comparison = []
for strategy in strategies:
    for prop in target_properties:
        offbits_row = corr_df[(corr_df['strategy'] == strategy) &
                               (corr_df['metric'] == 'jaccard_offbits') &
                               (corr_df['property'] == prop)].iloc[0]

        onbits_row = corr_df[(corr_df['strategy'] == strategy) &
                              (corr_df['metric'] == 'jaccard_onbits') &
                              (corr_df['property'] == prop)].iloc[0]

        improvement = abs(offbits_row['correlation_spearman']) - abs(onbits_row['correlation_spearman'])

        comparison.append({
            "strategy": strategy,
            "property": prop,
            "offbits_r": offbits_row['correlation_spearman'],
            "onbits_r": onbits_row['correlation_spearman'],
            "improvement": improvement,
            "offbits_better": improvement > 0
        })

comparison_df = pd.DataFrame(comparison)
comparison_file = BASE_DIR / "results" / "offbits_vs_onbits_comparison.csv"
comparison_df.to_csv(comparison_file, index=False)

print(f"\n✓ Comparison saved to: {comparison_file}")

# Summary: Does OffBits outperform OnBits?
offbits_wins = np.sum(comparison_df['offbits_better'])
onbits_wins = len(comparison_df) - offbits_wins

print(f"\n📊 OffBits vs OnBits Performance:")
print(f"   OffBits better: {offbits_wins}/{len(comparison_df)} cases ({100*offbits_wins/len(comparison_df):.1f}%)")
print(f"   OnBits better: {onbits_wins}/{len(comparison_df)} cases ({100*onbits_wins/len(comparison_df):.1f}%)")

if offbits_wins > onbits_wins:
    print(f"\n🎯 OffBits approach shows advantage!")
else:
    print(f"\n⚠ OnBits approach performs better in this dataset")


# ============================================================================
# SAVE SUMMARY
# ============================================================================

summary = {
    "num_compounds": len(df),
    "num_strategies": len(strategies),
    "num_comparisons": len(corr_df),
    "significant_correlations": len(significant) if len(significant) > 0 else 0,
    "best_result": {
        "strategy": str(best_result['strategy']) if len(significant) > 0 else None,
        "metric": str(best_result['metric']) if len(significant) > 0 else None,
        "property": str(best_result['property']) if len(significant) > 0 else None,
        "correlation": float(best_result['correlation_spearman']) if len(significant) > 0 else None,
        "p_value": float(best_result['p_value_spearman']) if len(significant) > 0 else None
    },
    "offbits_vs_onbits": {
        "offbits_wins": int(offbits_wins),
        "onbits_wins": int(onbits_wins),
        "total_comparisons": len(comparison_df)
    }
}

summary_file = BASE_DIR / "results" / "jaccard_hamming_summary.json"
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\n✓ Summary saved to: {summary_file}")
print("\n" + "=" * 70)
print("✓ JACCARD AND HAMMING ANALYSIS COMPLETE")
print("=" * 70)
print("\nNext: Run 05_iterative_refinement.py to optimize mapping strategies")
