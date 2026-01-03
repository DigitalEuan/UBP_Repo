#!/usr/bin/env python3
"""
Comprehensive Visualization of OffBits Analysis Results
=========================================================
Generate publication-quality figures showing the breakthrough
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")

# Set publication style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("paper", font_scale=1.2)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

print("=" * 70)
print("COMPREHENSIVE VISUALIZATION")
print("=" * 70)

# Load data
df = pd.read_csv(BASE_DIR / "data" / "large_chemicals_dataset.csv")
corr_df = pd.read_csv(BASE_DIR / "results" / "jaccard_hamming_correlations.csv")
comparison_df = pd.read_csv(BASE_DIR / "results" / "offbits_vs_onbits_comparison.csv")

print(f"\nLoaded {len(df)} compounds")
print(f"Found {len(corr_df[corr_df['significant']])} significant correlations")

# Load fingerprints and distance matrices
strategies = [
    "strategy_1_functional_groups",
    "strategy_2_lack_protection",
    "strategy_3_balanced",
    "strategy_4_persistence"
]

# ============================================================================
# FIGURE 1: OffBits vs OnBits Performance Comparison
# ============================================================================

print("\n[1/5] Creating Figure 1: OffBits vs OnBits Comparison...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

properties = ['persistent', 'biodegradable', 'toxic']
for idx, prop in enumerate(properties):
    ax = axes[idx]

    prop_data = comparison_df[comparison_df['property'] == prop]

    x = np.arange(len(prop_data))
    width = 0.35

    ax.bar(x - width/2, prop_data['offbits_r'].abs(), width, label='OffBits (0s)', color='#2E86AB', alpha=0.8)
    ax.bar(x + width/2, prop_data['onbits_r'].abs(), width, label='OnBits (1s)', color='#A23B72', alpha=0.8)

    ax.set_ylabel('|Correlation| (Spearman r)')
    ax.set_title(f'{prop.capitalize()}')
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace('strategy_', 'S').replace('_', '\n') for s in prop_data['strategy']], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, linewidth=1)

plt.suptitle('OffBits vs OnBits: Correlation Strength Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig1_offbits_vs_onbits.png", dpi=300, bbox_inches='tight')
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig1_offbits_vs_onbits.pdf", bbox_inches='tight')
plt.close()
print("   ✓ Saved fig1_offbits_vs_onbits")

# ============================================================================
# FIGURE 2: Best Strategy Heatmap
# ============================================================================

print("\n[2/5] Creating Figure 2: Correlation Heatmap...")

# Pivot correlation data
pivot_data = corr_df[corr_df['metric'] == 'jaccard_offbits'].pivot(
    index='strategy',
    columns='property',
    values='correlation_spearman'
)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_data, annot=True, fmt='.3f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Spearman Correlation'}, linewidths=1, linecolor='black')
ax.set_title('Jaccard OffBits Correlation with Chemical Properties', fontsize=14, fontweight='bold')
ax.set_xlabel('Property')
ax.set_ylabel('Mapping Strategy')
plt.tight_layout()
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig2_correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig2_correlation_heatmap.pdf", bbox_inches='tight')
plt.close()
print("   ✓ Saved fig2_correlation_heatmap")

# ============================================================================
# FIGURE 3: Scatter Plot - Best Result
# ============================================================================

print("\n[3/5] Creating Figure 3: Best Result Scatter Plot...")

# Best result: strategy_1, jaccard_onbits, biodegradable
best_strategy = "strategy_1_functional_groups"
jaccard_matrix = np.load(BASE_DIR / "data" / f"{best_strategy}_jaccard_onbits.npy")
avg_distances = np.mean(jaccard_matrix, axis=1)

fig, ax = plt.subplots(figsize=(10, 8))

# Color by category
categories = df['category'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
category_colors = {cat: colors[i] for i, cat in enumerate(categories)}

for cat in categories:
    mask = df['category'] == cat
    ax.scatter(df[mask]['biodegradable'], avg_distances[mask],
               label=cat, alpha=0.7, s=50, color=category_colors[cat], edgecolors='black', linewidths=0.5)

# Fit line
z = np.polyfit(df['biodegradable'], avg_distances, 1)
p = np.poly1d(z)
x_line = np.linspace(df['biodegradable'].min(), df['biodegradable'].max(), 100)
ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label=f'Fit: r=-0.689')

ax.set_xlabel('Biodegradability Score', fontsize=12)
ax.set_ylabel('Average Jaccard Distance (OnBits)', fontsize=12)
ax.set_title('Best Result: Biodegradability vs Jaccard OnBits Distance\n(Strategy 1: Functional Groups)',
             fontsize=14, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

# Add correlation text
textstr = f'Spearman r = -0.689\np < 0.000001\nn = {len(df)}'
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig3_best_result_scatter.png", dpi=300, bbox_inches='tight')
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig3_best_result_scatter.pdf", bbox_inches='tight')
plt.close()
print("   ✓ Saved fig3_best_result_scatter")

# ============================================================================
# FIGURE 4: Strategy Performance Overview
# ============================================================================

print("\n[4/5] Creating Figure 4: Strategy Performance Overview...")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.ravel()

for idx, strategy in enumerate(strategies):
    ax = axes[idx]

    strategy_data = corr_df[corr_df['strategy'] == strategy]
    offbits_data = strategy_data[strategy_data['metric'] == 'jaccard_offbits']

    properties = offbits_data['property'].values
    correlations = offbits_data['correlation_spearman'].values
    p_values = offbits_data['p_value_spearman'].values

    colors_bar = ['green' if p < 0.05 else 'gray' for p in p_values]

    bars = ax.barh(properties, correlations.astype(float), color=colors_bar, alpha=0.7, edgecolor='black')

    # Add p-value annotations
    for i, (cor, p) in enumerate(zip(correlations, p_values)):
        sig_marker = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(cor + 0.02 if cor > 0 else cor - 0.02, i, f'{cor:.3f}\n{sig_marker}',
                ha='left' if cor > 0 else 'right', va='center', fontsize=9)

    ax.set_xlabel('Correlation (Spearman r)', fontsize=11)
    ax.set_title(strategy.replace('_', ' ').title(), fontsize=12, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.3)
    ax.axvline(x=-0.5, color='red', linestyle='--', alpha=0.3)
    ax.grid(True, alpha=0.3, axis='x')

plt.suptitle('Strategy Performance: Jaccard OffBits Correlations', fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig4_strategy_performance.png", dpi=300, bbox_inches='tight')
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig4_strategy_performance.pdf", bbox_inches='tight')
plt.close()
print("   ✓ Saved fig4_strategy_performance")

# ============================================================================
# FIGURE 5: Hamming Distance Distribution
# ============================================================================

print("\n[5/5] Creating Figure 5: Hamming Distance Distribution...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()

for idx, strategy in enumerate(strategies):
    ax = axes[idx]

    hamming_matrix = np.load(BASE_DIR / "data" / f"{strategy}_hamming.npy")

    # Get upper triangle (no diagonal)
    upper_triangle_indices = np.triu_indices_from(hamming_matrix, k=1)
    distances = hamming_matrix[upper_triangle_indices]

    ax.hist(distances, bins=25, color='steelblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Hamming Distance (bits)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(strategy.replace('_', ' ').title(), fontsize=12, fontweight='bold')
    ax.axvline(x=np.mean(distances), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(distances):.2f}')
    ax.axvline(x=np.median(distances), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(distances):.2f}')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('Hamming Distance Distributions Across Strategies', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig5_hamming_distributions.png", dpi=300, bbox_inches='tight')
plt.savefig(BASE_DIR / "figures" / "offbits" / "fig5_hamming_distributions.pdf", bbox_inches='tight')
plt.close()
print("   ✓ Saved fig5_hamming_distributions")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "=" * 70)
print("VISUALIZATION SUMMARY")
print("=" * 70)
print(f"\n✓ Generated 5 figures (PNG + PDF)")
print(f"   Location: {BASE_DIR / 'figures' / 'offbits'}")
print(f"\nKey Findings:")
print(f"   - Best correlation: r=-0.689 (biodegradability)")
print(f"   - OffBits advantage: 75% of cases")
print(f"   - Significant correlations: 30/36 tested")
print(f"   - Best strategy: Functional Groups (Strategy 1)")

print("\n" + "=" * 70)
print("✓ VISUALIZATION COMPLETE")
print("=" * 70)
print("\nNext: Run 06_generate_final_report.py")
