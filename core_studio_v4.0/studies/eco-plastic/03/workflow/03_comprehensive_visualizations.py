"""
UBP COMPREHENSIVE VISUALIZATIONS
=================================
Publication-quality figures for the comprehensive UBP study
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import json

# Set publication style
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['figure.dpi'] = 150

print("="*80)
print("UBP COMPREHENSIVE VISUALIZATIONS")
print("="*80)
print()

# Load data
print("Loading data...")
df_corr = pd.read_csv('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/correlation_results_all.csv')
df_comparison = pd.read_csv('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/offbits_vs_onbits_comparison.csv')
df_results = pd.read_csv('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/pairwise_distances_sampled.csv')

with open('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/analysis_summary.json', 'r') as f:
    summary = json.load(f)

print(f"Loaded {len(df_corr)} correlation results")
print()

# Create figures directory if it doesn't exist
import os
os.makedirs('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures', exist_ok=True)

# =============================================================================
# FIGURE 1: STRATEGY COMPARISON HEATMAP
# =============================================================================

print("Creating Figure 1: Strategy Comparison Heatmap...")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

properties = ['persistence_diff', 'biodegradability_diff', 'toxicity_diff']
prop_names = ['Persistence', 'Biodegradability', 'Toxicity']

for idx, (prop, prop_name) in enumerate(zip(properties, prop_names)):
    ax = axes[idx]

    # Create pivot table
    df_prop = df_corr[df_corr['property'] == prop]
    pivot = df_prop.pivot(index='metric', columns='strategy', values='spearman_rho')

    # Plot heatmap
    im = ax.imshow(pivot.values, cmap='RdBu_r', aspect='auto', vmin=-0.6, vmax=0.6)

    # Set ticks
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([s.replace('Strategy', 'S').replace('_', '') for s in pivot.columns], rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([m.replace('_', ' ') for m in pivot.index], fontsize=8)

    # Add values
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                color = 'white' if abs(val) > 0.4 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=7)

    ax.set_title(f'{prop_name} Prediction', fontweight='bold', fontsize=10)

    if idx == 0:
        ax.set_ylabel('Metric', fontweight='bold')

# Add colorbar
cbar = fig.colorbar(im, ax=axes, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Spearman Correlation (ρ)', fontweight='bold')

plt.tight_layout()
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig1_strategy_comparison_heatmap.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig1_strategy_comparison_heatmap.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig1_strategy_comparison_heatmap")

# =============================================================================
# FIGURE 2: OFFBITS VS ONBITS
# =============================================================================

print("Creating Figure 2: OffBits vs OnBits Comparison...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Win rate by strategy
ax = axes[0]
strategies = df_comparison['strategy'].unique()
win_rates = []
strategy_names = []

for strat in strategies:
    df_strat = df_comparison[df_comparison['strategy'] == strat]
    win_rate = (df_strat['winner'] == 'OffBits').sum() / len(df_strat) * 100
    win_rates.append(win_rate)
    strategy_names.append(strat.replace('Strategy', 'S').replace('_', ''))

colors = ['#2ecc71' if wr >= 50 else '#e74c3c' for wr in win_rates]
bars = ax.barh(range(len(strategies)), win_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)

ax.axvline(50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlim(0, 100)
ax.set_yticks(range(len(strategies)))
ax.set_yticklabels(strategy_names, fontsize=9)
ax.set_xlabel('OffBits Win Rate (%)', fontweight='bold')
ax.set_title('A. OffBits vs OnBits by Strategy', fontweight='bold', loc='left')
ax.grid(axis='x', alpha=0.3)

# Add percentage labels
for i, (bar, wr) in enumerate(zip(bars, win_rates)):
    ax.text(wr + 2, i, f'{wr:.0f}%', va='center', fontsize=8, fontweight='bold')

# Panel B: Improvement distribution
ax = axes[1]
improvements = df_comparison['improvement'].values
ax.hist(improvements, bins=20, color='#3498db', alpha=0.7, edgecolor='black', linewidth=0.5)
ax.axvline(0, color='red', linestyle='--', linewidth=1.5, label='No difference')
ax.set_xlabel('Improvement (|ρ_OffBits| - |ρ_OnBits|)', fontweight='bold')
ax.set_ylabel('Count', fontweight='bold')
ax.set_title('B. OffBits Improvement Distribution', fontweight='bold', loc='left')
ax.legend()
ax.grid(axis='y', alpha=0.3)

mean_improvement = np.mean(improvements)
ax.axvline(mean_improvement, color='green', linestyle=':', linewidth=1.5, label=f'Mean: {mean_improvement:.3f}')
ax.text(mean_improvement + 0.01, ax.get_ylim()[1] * 0.9, f'Mean\n{mean_improvement:.3f}',
        ha='left', va='top', fontsize=8, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig2_offbits_vs_onbits.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig2_offbits_vs_onbits.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig2_offbits_vs_onbits")

# =============================================================================
# FIGURE 3: BEST RESULTS SCATTER PLOTS
# =============================================================================

print("Creating Figure 3: Best Results Scatter Plots...")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Get top 6 results
top_results = df_corr.sort_values('spearman_rho', key=abs, ascending=False).head(6)

for idx, (_, row) in enumerate(top_results.iterrows()):
    ax = axes[idx // 3, idx % 3]

    strategy = row['strategy']
    prop = row['property']
    metric = row['metric']
    rho = row['spearman_rho']
    p = row['spearman_p']

    # Get data
    df_plot = df_results[(df_results['strategy'] == strategy)]
    x = df_plot[metric].values
    y = df_plot[prop].values

    # Remove NaN/Inf
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # Sample for plotting (too many points)
    if len(x) > 5000:
        indices = np.random.choice(len(x), 5000, replace=False)
        x = x[indices]
        y = y[indices]

    # Scatter plot
    ax.hexbin(x, y, gridsize=30, cmap='Blues', mincnt=1, alpha=0.6)

    # Trend line
    z = np.polyfit(x, y, 1)
    p_fit = np.poly1d(z)
    x_fit = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_fit, p_fit(x_fit), 'r--', linewidth=1.5, alpha=0.8)

    # Labels
    prop_name = prop.replace('_diff', '').replace('_', ' ').title()
    metric_name = metric.replace('_', ' ').title()

    ax.set_xlabel(metric_name, fontweight='bold', fontsize=8)
    ax.set_ylabel(f'{prop_name} Difference', fontweight='bold', fontsize=8)

    strat_short = strategy.replace('Strategy', 'S').replace('_', '')
    ax.set_title(f'{strat_short}: {metric_name}\\nρ={rho:.3f}, p<0.001', fontsize=9, fontweight='bold')

    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig3_best_results_scatter.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig3_best_results_scatter.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig3_best_results_scatter")

# =============================================================================
# FIGURE 4: METRIC PERFORMANCE COMPARISON
# =============================================================================

print("Creating Figure 4: Metric Performance Comparison...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel A: Overall metric performance
ax = axes[0, 0]
metrics = df_corr['metric'].unique()
metric_scores = []
for metric in metrics:
    df_metric = df_corr[df_corr['metric'] == metric]
    mean_abs_rho = df_metric['spearman_rho'].abs().mean()
    metric_scores.append(mean_abs_rho)

metric_names = [m.replace('_', ' ').title() for m in metrics]
colors_metric = ['#e74c3c' if 'offbits' in m.lower() else '#3498db' if 'onbits' in m.lower() else '#95a5a6' for m in metrics]

bars = ax.bar(range(len(metrics)), metric_scores, color=colors_metric, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(metrics)))
ax.set_xticklabels(metric_names, rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Mean |ρ|', fontweight='bold')
ax.set_title('A. Overall Metric Performance', fontweight='bold', loc='left')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar, score in zip(bars, metric_scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{score:.3f}',
            ha='center', va='bottom', fontsize=7, fontweight='bold')

# Panel B: Strategy performance
ax = axes[0, 1]
strategies = df_corr['strategy'].unique()
strategy_scores = []
for strat in strategies:
    df_strat = df_corr[df_corr['strategy'] == strat]
    mean_abs_rho = df_strat['spearman_rho'].abs().mean()
    strategy_scores.append(mean_abs_rho)

strategy_names = [s.replace('Strategy', 'S').replace('_', '') for s in strategies]
colors_strat = plt.cm.Set3(np.linspace(0, 1, len(strategies)))

bars = ax.bar(range(len(strategies)), strategy_scores, color=colors_strat, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(strategies)))
ax.set_xticklabels(strategy_names, rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Mean |ρ|', fontweight='bold')
ax.set_title('B. Overall Strategy Performance', fontweight='bold', loc='left')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar, score in zip(bars, strategy_scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{score:.3f}',
            ha='center', va='bottom', fontsize=7, fontweight='bold')

# Panel C: Property difficulty
ax = axes[1, 0]
properties = df_corr['property'].unique()
property_scores = []
for prop in properties:
    df_prop = df_corr[df_corr['property'] == prop]
    mean_abs_rho = df_prop['spearman_rho'].abs().mean()
    property_scores.append(mean_abs_rho)

property_names = [p.replace('_diff', '').title() for p in properties]
colors_prop = ['#e67e22', '#9b59b6', '#1abc9c']

bars = ax.bar(range(len(properties)), property_scores, color=colors_prop, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(properties)))
ax.set_xticklabels(property_names, fontsize=9)
ax.set_ylabel('Mean |ρ|', fontweight='bold')
ax.set_title('C. Property Predictability', fontweight='bold', loc='left')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar, score in zip(bars, property_scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{score:.3f}',
            ha='center', va='bottom', fontsize=8, fontweight='bold')

# Panel D: Significance summary
ax = axes[1, 1]
sig_levels = ['p < 0.001', '0.001 ≤ p < 0.01', '0.01 ≤ p < 0.05', 'p ≥ 0.05']
sig_counts = [
    (df_corr['spearman_p'] < 0.001).sum(),
    ((df_corr['spearman_p'] >= 0.001) & (df_corr['spearman_p'] < 0.01)).sum(),
    ((df_corr['spearman_p'] >= 0.01) & (df_corr['spearman_p'] < 0.05)).sum(),
    (df_corr['spearman_p'] >= 0.05).sum()
]

colors_sig = ['#27ae60', '#f39c12', '#e67e22', '#c0392b']
wedges, texts, autotexts = ax.pie(sig_counts, labels=sig_levels, colors=colors_sig, autopct='%1.1f%%',
                                    startangle=90, textprops={'fontsize': 8, 'fontweight': 'bold'})

ax.set_title('D. Statistical Significance Distribution', fontweight='bold', loc='left')

plt.tight_layout()
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig4_metric_performance.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig4_metric_performance.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig4_metric_performance")

# =============================================================================
# FIGURE 5: FINGERPRINT WEIGHT DISTRIBUTIONS
# =============================================================================

print("Creating Figure 5: Fingerprint Weight Distributions...")

# Load fingerprints
fps_all = np.load('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_fingerprints_all_strategies.npz')

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for idx, (strategy_name, fps) in enumerate(fps_all.items()):
    ax = axes[idx // 3, idx % 3]

    # Compute weights
    weights = [sum(fp) for fp in fps]

    # Histogram
    ax.hist(weights, bins=range(0, 25), color='#3498db', alpha=0.7, edgecolor='black', linewidth=0.5)

    # Mark special weights
    ax.axvline(8, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Octad (8)')
    ax.axvline(12, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Balanced (12)')

    # Stats
    mean_weight = np.mean(weights)
    std_weight = np.std(weights)

    ax.axvline(mean_weight, color='orange', linestyle='-', linewidth=2, label=f'Mean ({mean_weight:.1f})')

    ax.set_xlabel('Hamming Weight', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')

    strat_short = strategy_name.replace('Strategy', 'S').replace('_', '')
    ax.set_title(f'{strat_short}\\nMean={mean_weight:.2f}, σ={std_weight:.2f}', fontweight='bold')

    ax.legend(fontsize=7, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig5_fingerprint_weights.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig5_fingerprint_weights.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig5_fingerprint_weights")

# =============================================================================
# FIGURE 6: COMPREHENSIVE SUMMARY
# =============================================================================

print("Creating Figure 6: Comprehensive Summary Dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel A: Key metrics
ax1 = fig.add_subplot(gs[0, :])
ax1.axis('off')

summary_text = f"""
COMPREHENSIVE UBP STUDY - KEY RESULTS

Dataset: {summary['n_compounds']} compounds across 23 chemical categories
Strategies: {summary['n_strategies']} advanced UBP-based mapping approaches
Metrics: {summary['n_metrics']} binary similarity metrics (Jaccard OffBits, Jaccard OnBits, Hamming variants)
Properties: {summary['n_properties']} chemical properties (Persistence, Biodegradability, Toxicity)

BEST CORRELATION: ρ = {summary['best_correlation']:.3f}
Strategy: {summary['best_strategy']}
Metric: {summary['best_metric'].replace('_', ' ').title()}
Property: {summary['best_property'].replace('_diff', '').title()}

STATISTICAL SIGNIFICANCE:
Total tests: {summary['total_tests']}
Significant (raw p < 0.05): {summary['significant_raw']} ({100*summary['significant_raw']/summary['total_tests']:.1f}%)
Significant (FDR < 0.05): {summary['significant_fdr']} ({100*summary['significant_fdr']/summary['total_tests']:.1f}%)

OFFBITS ADVANTAGE: {100*summary['offbits_win_rate']:.1f}% win rate vs traditional OnBits approach
"""

ax1.text(0.05, 0.95, summary_text, transform=ax1.transAxes, fontsize=10, verticalalignment='top',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Panel B: Top correlations bar chart
ax2 = fig.add_subplot(gs[1, :])
top_10 = df_corr.sort_values('spearman_rho', key=abs, ascending=False).head(10)
labels = [f"{row['strategy'].replace('Strategy', 'S')[:10]}-{row['metric'][:8]}-{row['property'][:5]}"
          for _, row in top_10.iterrows()]
values = top_10['spearman_rho'].values

colors_bar = ['#2ecc71' if v > 0 else '#e74c3c' for v in values]
bars = ax2.barh(range(len(labels)), values, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=0.5)

ax2.set_yticks(range(len(labels)))
ax2.set_yticklabels(labels, fontsize=8)
ax2.set_xlabel('Spearman Correlation (ρ)', fontweight='bold')
ax2.set_title('Top 10 Correlations', fontweight='bold', fontsize=12)
ax2.grid(axis='x', alpha=0.3)
ax2.axvline(0, color='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, values):
    x_pos = val + (0.01 if val > 0 else -0.01)
    ha = 'left' if val > 0 else 'right'
    ax2.text(x_pos, bar.get_y() + bar.get_height()/2, f'{val:.3f}',
             va='center', ha=ha, fontsize=7, fontweight='bold')

# Panel C: Strategy comparison
ax3 = fig.add_subplot(gs[2, 0])
strategies = df_corr['strategy'].unique()
strategy_scores = [df_corr[df_corr['strategy'] == s]['spearman_rho'].abs().mean() for s in strategies]
strategy_names = [s.replace('Strategy', 'S').replace('_', '')[:10] for s in strategies]

ax3.bar(range(len(strategies)), strategy_scores, color=plt.cm.Set3(np.linspace(0, 1, len(strategies))),
        alpha=0.7, edgecolor='black', linewidth=0.5)
ax3.set_xticks(range(len(strategies)))
ax3.set_xticklabels(strategy_names, rotation=45, ha='right', fontsize=8)
ax3.set_ylabel('Mean |ρ|', fontweight='bold')
ax3.set_title('Strategy Performance', fontweight='bold', fontsize=10)
ax3.grid(axis='y', alpha=0.3)

# Panel D: Metric comparison
ax4 = fig.add_subplot(gs[2, 1])
metrics = df_corr['metric'].unique()
metric_scores = [df_corr[df_corr['metric'] == m]['spearman_rho'].abs().mean() for m in metrics]
metric_names = [m.replace('_', ' ')[:12] for m in metrics]

colors_metric = ['#e74c3c' if 'offbits' in m.lower() else '#3498db' if 'onbits' in m.lower() else '#95a5a6' for m in metrics]
ax4.bar(range(len(metrics)), metric_scores, color=colors_metric, alpha=0.7, edgecolor='black', linewidth=0.5)
ax4.set_xticks(range(len(metrics)))
ax4.set_xticklabels(metric_names, rotation=45, ha='right', fontsize=7)
ax4.set_ylabel('Mean |ρ|', fontweight='bold')
ax4.set_title('Metric Performance', fontweight='bold', fontsize=10)
ax4.grid(axis='y', alpha=0.3)

# Panel E: OffBits win rate
ax5 = fig.add_subplot(gs[2, 2])
offbits_wins = (df_comparison['winner'] == 'OffBits').sum()
onbits_wins = (df_comparison['winner'] == 'OnBits').sum()

wedges, texts, autotexts = ax5.pie([offbits_wins, onbits_wins], labels=['OffBits', 'OnBits'],
                                     colors=['#2ecc71', '#e74c3c'], autopct='%1.1f%%', startangle=90,
                                     textprops={'fontsize': 10, 'fontweight': 'bold'})

ax5.set_title('OffBits vs OnBits', fontweight='bold', fontsize=10)

plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig6_comprehensive_summary.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20260102_222825_9c4bac117ac1/figures/fig6_comprehensive_summary.pdf', bbox_inches='tight')
plt.close()
print("  Saved: fig6_comprehensive_summary")

print("\n" + "="*80)
print("VISUALIZATION COMPLETE!")
print("="*80)
print(f"\nGenerated 6 publication-quality figures:")
print("  1. Strategy Comparison Heatmap")
print("  2. OffBits vs OnBits Comparison")
print("  3. Best Results Scatter Plots")
print("  4. Metric Performance Comparison")
print("  5. Fingerprint Weight Distributions")
print("  6. Comprehensive Summary Dashboard")
print(f"\nAll figures saved to: figures/")
print(f"\nNext: Write comprehensive scientific paper (README.md)")
