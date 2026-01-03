#!/usr/bin/env python3
"""
Step 6: Visualization
Creates publication-quality figures for the UBP chemical analysis study.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Set publication-quality plot parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.dpi'] = 150

print("="*80)
print("STEP 6: VISUALIZATION")
print("="*80)

print("\n[1/5] Loading data...")
metrics_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_metrics.csv")
df = pd.read_csv(metrics_path)
print(f"  ✓ Loaded {len(df)} materials")

# Create figures directory if needed
fig_dir = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/figures")
fig_dir.mkdir(exist_ok=True)

print("\n[2/5] Creating Figure 1: Symmetry Tax vs. Persistence Score...")

fig1, ax1 = plt.subplots(figsize=(8, 6))

# Color by biodegradability
colors = ['#2ecc71' if biodeg else '#e74c3c' for biodeg in df['biodegradable']]
markers = ['o' if biodeg else 's' for biodeg in df['biodegradable']]

for idx, row in df.iterrows():
    ax1.scatter(row['persistence_score'], row['symmetry_tax'],
                c=colors[idx], marker=markers[idx], s=120,
                edgecolors='black', linewidths=0.8, alpha=0.7)

    # Add labels for interesting materials
    if row['abbrev'] in ['PVC', 'PTFE', 'PLA', 'PHB', 'PE-LD', 'PMMA']:
        ax1.annotate(row['abbrev'],
                     xy=(row['persistence_score'], row['symmetry_tax']),
                     xytext=(5, 5), textcoords='offset points',
                     fontsize=8, alpha=0.8)

ax1.set_xlabel('Environmental Persistence Score (1=low, 5=very high)', fontsize=11, fontweight='bold')
ax1.set_ylabel('UBP Symmetry Tax', fontsize=11, fontweight='bold')
ax1.set_title('UBP Symmetry Tax vs. Environmental Persistence\n(Chemicals & Plastics Analysis)',
              fontsize=13, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle='--')

# Add correlation info
from scipy.stats import spearmanr
corr, pval = spearmanr(df['persistence_score'], df['symmetry_tax'])
ax1.text(0.05, 0.95, f"Spearman r = {corr:.3f}\np = {pval:.3f}",
         transform=ax1.transAxes, fontsize=10,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Legend
biodeg_patch = mpatches.Patch(color='#2ecc71', label='Biodegradable')
non_biodeg_patch = mpatches.Patch(color='#e74c3c', label='Non-biodegradable')
ax1.legend(handles=[biodeg_patch, non_biodeg_patch], loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig(fig_dir / 'fig1_symmetry_tax_vs_persistence.png', dpi=300, bbox_inches='tight')
plt.savefig(fig_dir / 'fig1_symmetry_tax_vs_persistence.pdf', bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: fig1_symmetry_tax_vs_persistence.png/.pdf")

print("\n[3/5] Creating Figure 2: UBP Metrics by Material Category...")

fig2, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Symmetry Tax by category
categories = df['category'].unique()
cat_data = [df[df['category'] == cat]['symmetry_tax'].values for cat in categories]
cat_labels = [cat.replace(' Plastic', '').replace(' ', '\n') for cat in categories]

bp1 = axes[0].boxplot(cat_data, labels=cat_labels, patch_artist=True,
                       boxprops=dict(facecolor='#3498db', alpha=0.6),
                       medianprops=dict(color='red', linewidth=2),
                       whiskerprops=dict(linewidth=1.5),
                       capprops=dict(linewidth=1.5))

axes[0].set_ylabel('UBP Symmetry Tax', fontsize=11, fontweight='bold')
axes[0].set_title('A. Symmetry Tax by Material Category', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y', linestyle='--')

# Panel B: NRCI by category
cat_data_nrci = [df[df['category'] == cat]['nrci'].values for cat in categories]

bp2 = axes[1].boxplot(cat_data_nrci, labels=cat_labels, patch_artist=True,
                       boxprops=dict(facecolor='#9b59b6', alpha=0.6),
                       medianprops=dict(color='red', linewidth=2),
                       whiskerprops=dict(linewidth=1.5),
                       capprops=dict(linewidth=1.5))

axes[1].set_ylabel('UBP NRCI (Coherence)', fontsize=11, fontweight='bold')
axes[1].set_title('B. NRCI by Material Category', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.savefig(fig_dir / 'fig2_metrics_by_category.png', dpi=300, bbox_inches='tight')
plt.savefig(fig_dir / 'fig2_metrics_by_category.pdf', bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: fig2_metrics_by_category.png/.pdf")

print("\n[4/5] Creating Figure 3: Heatmap of All UBP Metrics...")

fig3, ax3 = plt.subplots(figsize=(10, 8))

# Prepare data for heatmap
heatmap_data = df[['material', 'nrci', 'symmetry_tax', 'persistence_score', 'toxicity_score']].copy()
heatmap_data = heatmap_data.set_index('material')

# Normalize each column to 0-1 for better visualization
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
heatmap_normalized = pd.DataFrame(
    scaler.fit_transform(heatmap_data),
    columns=heatmap_data.columns,
    index=heatmap_data.index
)

# Create heatmap
im = ax3.imshow(heatmap_normalized.T, cmap='YlOrRd', aspect='auto', interpolation='nearest')

# Set ticks
ax3.set_xticks(np.arange(len(heatmap_normalized.index)))
ax3.set_yticks(np.arange(len(heatmap_normalized.columns)))
ax3.set_xticklabels([abbr for abbr in df['abbrev']], rotation=45, ha='right', fontsize=9)
ax3.set_yticklabels(['NRCI', 'Symmetry Tax', 'Persistence', 'Toxicity'], fontsize=10)

# Add colorbar
cbar = plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label('Normalized Value (0-1)', rotation=270, labelpad=20, fontsize=10)

# Add grid
ax3.set_xticks(np.arange(len(heatmap_normalized.index)) - 0.5, minor=True)
ax3.set_yticks(np.arange(len(heatmap_normalized.columns)) - 0.5, minor=True)
ax3.grid(which='minor', color='white', linestyle='-', linewidth=1.5)

ax3.set_title('Normalized Heatmap: UBP Metrics & Material Properties',
              fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig(fig_dir / 'fig3_heatmap_all_metrics.png', dpi=300, bbox_inches='tight')
plt.savefig(fig_dir / 'fig3_heatmap_all_metrics.pdf', bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: fig3_heatmap_all_metrics.png/.pdf")

print("\n[5/5] Creating Figure 4: Biodegradable vs. Non-biodegradable Comparison...")

fig4, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Violin plot of Symmetry Tax
biodeg_data = df[df['biodegradable'] == True]['symmetry_tax']
non_biodeg_data = df[df['biodegradable'] == False]['symmetry_tax']

parts1 = axes[0].violinplot([non_biodeg_data, biodeg_data],
                             positions=[1, 2],
                             showmeans=True, showmedians=True,
                             widths=0.7)

for pc in parts1['bodies']:
    pc.set_facecolor('#3498db')
    pc.set_alpha(0.6)

axes[0].set_xticks([1, 2])
axes[0].set_xticklabels(['Non-biodegradable\n(n=11)', 'Biodegradable\n(n=4)'], fontsize=10)
axes[0].set_ylabel('UBP Symmetry Tax', fontsize=11, fontweight='bold')
axes[0].set_title('A. Symmetry Tax Distribution', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y', linestyle='--')

# Add statistical test result
axes[0].text(0.5, 0.95, 'Mann-Whitney U\np = 0.507 (n.s.)',
             transform=axes[0].transAxes, fontsize=9,
             verticalalignment='top', ha='center',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

# Panel B: Scatter plot with jitter
np.random.seed(42)
jitter_amount = 0.05

x_non_biodeg = np.ones(len(non_biodeg_data)) + np.random.normal(0, jitter_amount, len(non_biodeg_data))
x_biodeg = 2 * np.ones(len(biodeg_data)) + np.random.normal(0, jitter_amount, len(biodeg_data))

axes[1].scatter(x_non_biodeg, non_biodeg_data, c='#e74c3c', s=100, alpha=0.6,
                edgecolors='black', linewidths=0.8, label='Non-biodegradable')
axes[1].scatter(x_biodeg, biodeg_data, c='#2ecc71', s=100, alpha=0.6,
                edgecolors='black', linewidths=0.8, label='Biodegradable')

# Add mean lines
axes[1].hlines(non_biodeg_data.mean(), 0.7, 1.3, colors='red', linewidth=2, label='Mean')
axes[1].hlines(biodeg_data.mean(), 1.7, 2.3, colors='red', linewidth=2)

axes[1].set_xlim(0.5, 2.5)
axes[1].set_xticks([1, 2])
axes[1].set_xticklabels(['Non-biodegradable', 'Biodegradable'], fontsize=10)
axes[1].set_ylabel('UBP Symmetry Tax', fontsize=11, fontweight='bold')
axes[1].set_title('B. Individual Materials', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y', linestyle='--')
axes[1].legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig(fig_dir / 'fig4_biodegradable_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig(fig_dir / 'fig4_biodegradable_comparison.pdf', bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: fig4_biodegradable_comparison.png/.pdf")

print("\n" + "="*80)
print("VISUALIZATION COMPLETE")
print("="*80)

print("\nGenerated figures:")
print("  1. fig1_symmetry_tax_vs_persistence.png/.pdf - Scatter plot with correlation")
print("  2. fig2_metrics_by_category.png/.pdf - Box plots by material category")
print("  3. fig3_heatmap_all_metrics.png/.pdf - Normalized heatmap of all metrics")
print("  4. fig4_biodegradable_comparison.png/.pdf - Violin and scatter plots")

print("\n✓ Ready for sensitivity analysis and documentation")
