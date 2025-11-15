#!/usr/bin/env python3.11
"""
Generate All Figures for UBP Time & Dissident Horizon Paper
Using real data from comprehensive analysis
"""

import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, '/home/ubuntu/UBP_Repo/nutrition')
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from expanded_nutrient_database import ExpandedNutrientDatabase

# Load results
with open('comprehensive_real_analysis_results.json', 'r') as f:
    results = json.load(f)

# Load nutrients
nutrients = ExpandedNutrientDatabase.get_all_nutrients()

print("Generating comprehensive figures from real data...")
print()

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'synergy': '#2ecc71',
    'antagonism': '#e74c3c',
    'neutral': '#95a5a6',
    'dissident': '#e67e22',
    'optimal': '#3498db'
}

# ==============================================================================
# FIGURE 1: Frequency Coherence Hypothesis Test
# ==============================================================================

fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel A: Frequency ratio distributions
syn_ratios = results['frequency_coherence']['synergies']['ratios']
ant_ratios = results['frequency_coherence']['antagonisms']['ratios']

ax1.hist(syn_ratios, bins=20, alpha=0.7, color=colors['synergy'], 
         label=f'Synergies (n={len(syn_ratios)})', edgecolor='black')
ax1.hist(ant_ratios, bins=20, alpha=0.7, color=colors['antagonism'], 
         label=f'Antagonisms (n={len(ant_ratios)})', edgecolor='black')
ax1.axvline(np.mean(syn_ratios), color=colors['synergy'], linestyle='--', linewidth=2, 
            label=f'Synergy mean: {np.mean(syn_ratios):.2f}')
ax1.axvline(np.mean(ant_ratios), color=colors['antagonism'], linestyle='--', linewidth=2,
            label=f'Antagonism mean: {np.mean(ant_ratios):.2f}')
ax1.set_xlabel('Frequency Ratio (max/min)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
ax1.set_title('A. Frequency Ratio Distributions', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Panel B: Box plot comparison
data_to_plot = [syn_ratios, ant_ratios]
bp = ax2.boxplot(data_to_plot, labels=['Synergies', 'Antagonisms'],
                 patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor(colors['synergy'])
bp['boxes'][1].set_facecolor(colors['antagonism'])
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color='black', linewidth=1.5)
ax2.set_ylabel('Frequency Ratio', fontsize=12, fontweight='bold')
ax2.set_title('B. Statistical Comparison', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add significance annotation
cohens_d = results['frequency_coherence']['effect_size']
ax2.text(1.5, max(max(syn_ratios), max(ant_ratios)) * 0.9,
         f"Cohen's d = {cohens_d:.3f}\n({results['frequency_coherence']['effect_interpretation']} effect)",
         fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
         ha='center')

# Panel C: Scatter plot of individual interactions
# Get frequency data for scatter
syn_freqs_x = []
syn_freqs_y = []
ant_freqs_x = []
ant_freqs_y = []

for name, nutrient in nutrients.items():
    for synergist in nutrient.synergists:
        if synergist in nutrients:
            syn_freqs_x.append(nutrient.coherence_frequency)
            syn_freqs_y.append(nutrients[synergist].coherence_frequency)
    
    for antagonist in nutrient.antagonists:
        if antagonist in nutrients:
            ant_freqs_x.append(nutrient.coherence_frequency)
            ant_freqs_y.append(nutrients[antagonist].coherence_frequency)

ax3.scatter(syn_freqs_x, syn_freqs_y, c=colors['synergy'], s=100, alpha=0.6,
            label='Synergies', edgecolors='black', linewidth=0.5)
ax3.scatter(ant_freqs_x, ant_freqs_y, c=colors['antagonism'], s=100, alpha=0.6,
            label='Antagonisms', edgecolors='black', linewidth=0.5, marker='s')

# Add diagonal line (equal frequencies)
min_freq = min(min(syn_freqs_x + ant_freqs_x), min(syn_freqs_y + ant_freqs_y))
max_freq = max(max(syn_freqs_x + ant_freqs_x), max(syn_freqs_y + ant_freqs_y))
ax3.plot([min_freq, max_freq], [min_freq, max_freq], 'k--', alpha=0.3, linewidth=2,
         label='Equal frequencies')

ax3.set_xlabel('Nutrient 1 Frequency (Hz)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Nutrient 2 Frequency (Hz)', fontsize=12, fontweight='bold')
ax3.set_title('C. Frequency Space Distribution', fontsize=14, fontweight='bold')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, which='both')

# Panel D: Effect size interpretation
effect_sizes = ['Negligible\n(<0.2)', 'Small\n(0.2-0.5)', 'Medium\n(0.5-0.8)', 'Large\n(>0.8)']
effect_values = [0.1, 0.35, 0.65, 0.9]
effect_colors_bar = ['#95a5a6', '#f39c12', '#e67e22', '#e74c3c']

bars = ax4.barh(effect_sizes, effect_values, color=effect_colors_bar, alpha=0.7,
                edgecolor='black', linewidth=2)
ax4.axvline(abs(cohens_d), color='blue', linestyle='--', linewidth=3,
            label=f'Observed: |{cohens_d:.3f}|')
ax4.set_xlabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
ax4.set_title('D. Effect Size Context', fontsize=14, fontweight='bold')
ax4.legend(fontsize=11)
ax4.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('figure1_frequency_coherence_test.png', dpi=300, bbox_inches='tight')
print("✓ Generated Figure 1: Frequency Coherence Test")

# ==============================================================================
# FIGURE 2: Coherence Deficit & Dissident Analysis
# ==============================================================================

fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel A: NRCI distribution
nrci_values = [n.bioavailability for n in nutrients.values()]
ax1.hist(nrci_values, bins=30, color=colors['optimal'], alpha=0.7, 
         edgecolor='black', linewidth=1.5)
ax1.axvline(results['coherence_deficit']['nrci_mean'], color='red', 
            linestyle='--', linewidth=2, label=f"Mean: {results['coherence_deficit']['nrci_mean']:.3f}")
ax1.axvline(results['dissidents']['threshold'], color='orange', 
            linestyle=':', linewidth=2, label=f"Dissident threshold: {results['dissidents']['threshold']:.3f}")
ax1.set_xlabel('NRCI (Bioavailability)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
ax1.set_title('A. NRCI Distribution (n=84)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Panel B: Deficit comparison
deficits = ['Biological\n(This Study)', 'Cosmological\n(Time Study)']
deficit_values = [results['coherence_deficit']['delta_deficit_percent'],
                  results['coherence_deficit']['theoretical_deficit'] * 100]
deficit_colors_bar = [colors['dissident'], colors['optimal']]

bars = ax2.bar(deficits, deficit_values, color=deficit_colors_bar, alpha=0.7,
               edgecolor='black', linewidth=2, width=0.6)
ax2.set_ylabel('δ-Deficit (%)', fontsize=12, fontweight='bold')
ax2.set_title(f'B. Coherence Deficit Comparison\n(Ratio: {results["coherence_deficit"]["ratio_to_theory"]:.1f}×)', 
              fontsize=14, fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, axis='y', which='both')

# Add value labels
for bar, val in zip(bars, deficit_values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.2f}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Panel C: Dissidents by category
dissidents_list = results['dissidents']['list']
dissident_names = [d[0] for d in dissidents_list[:15]]
dissident_nrcis = [d[1] for d in dissidents_list[:15]]

y_pos = np.arange(len(dissident_names))
bars = ax3.barh(y_pos, dissident_nrcis, color=colors['dissident'], alpha=0.7,
                edgecolor='black', linewidth=1)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(dissident_names, fontsize=9)
ax3.set_xlabel('NRCI (Bioavailability)', fontsize=12, fontweight='bold')
ax3.set_title('C. Top 15 Dissident Nutrients', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='x')
ax3.invert_yaxis()

# Panel D: Time dilation
time_dilation_mean = results['temporal_trap']['mean_time_dilation']
time_slowdown = results['temporal_trap']['time_slowdown_percent']

# Create visualization of time flow
normal_time = np.linspace(0, 10, 100)
dissident_time = normal_time / time_dilation_mean

ax4.plot(normal_time, normal_time, 'b-', linewidth=3, label='Normal time flow', alpha=0.7)
ax4.plot(normal_time, dissident_time, 'r-', linewidth=3, label='Dissident time flow', alpha=0.7)
ax4.fill_between(normal_time, normal_time, dissident_time, alpha=0.2, color='orange')
ax4.set_xlabel('External Time', fontsize=12, fontweight='bold')
ax4.set_ylabel('Internal Time', fontsize=12, fontweight='bold')
ax4.set_title(f'D. Temporal Trap Effect\n(~{time_slowdown:.1f}% slower in dissidents)', 
              fontsize=14, fontweight='bold')
ax4.legend(fontsize=11)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figure2_coherence_deficit_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Generated Figure 2: Coherence Deficit Analysis")

# ==============================================================================
# FIGURE 3: Category Analysis
# ==============================================================================

fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: NRCI by category
categories = sorted(results['category_stats'].keys())
nrci_means = [results['category_stats'][cat]['nrci_mean'] for cat in categories]
nrci_stds = [results['category_stats'][cat]['nrci_std'] for cat in categories]
counts = [results['category_stats'][cat]['count'] for cat in categories]

x_pos = np.arange(len(categories))
bars = ax1.bar(x_pos, nrci_means, yerr=nrci_stds, capsize=5,
               color=colors['optimal'], alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_xticks(x_pos)
ax1.set_xticklabels([cat.replace('_', '\n') for cat in categories], fontsize=10)
ax1.set_ylabel('Mean NRCI ± SD', fontsize=12, fontweight='bold')
ax1.set_title('A. Coherence by Nutrient Category', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Add count labels
for i, (bar, count) in enumerate(zip(bars, counts)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + nrci_stds[i] + 0.02,
             f'n={count}',
             ha='center', va='bottom', fontsize=9)

# Panel B: Frequency CV by category
freq_cvs = [results['category_stats'][cat]['freq_cv'] for cat in categories]

bars = ax2.bar(x_pos, freq_cvs, color=colors['synergy'], alpha=0.7,
               edgecolor='black', linewidth=2)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([cat.replace('_', '\n') for cat in categories], fontsize=10)
ax2.set_ylabel('Frequency Coefficient of Variation', fontsize=12, fontweight='bold')
ax2.set_title('B. Frequency Clustering by Category', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('figure3_category_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Generated Figure 3: Category Analysis")

# ==============================================================================
# FIGURE 4: Comprehensive Summary
# ==============================================================================

fig4 = plt.figure(figsize=(16, 10))
gs = fig4.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel A: Key findings summary (text)
ax1 = fig4.add_subplot(gs[0, :])
ax1.axis('off')

summary_text = f"""
KEY FINDINGS FROM REAL DATA ANALYSIS (n=84 nutrients)

1. FREQUENCY COHERENCE HYPOTHESIS
   • Synergies: {results['frequency_coherence']['synergies']['mean_ratio']:.2f} ± {results['frequency_coherence']['synergies']['std_ratio']:.2f} (n={results['frequency_coherence']['synergies']['count']})
   • Antagonisms: {results['frequency_coherence']['antagonisms']['mean_ratio']:.2f} ± {results['frequency_coherence']['antagonisms']['std_ratio']:.2f} (n={results['frequency_coherence']['antagonisms']['count']})
   • Effect: {results['frequency_coherence']['effect_interpretation'].upper()} (Cohen's d = {results['frequency_coherence']['effect_size']:.3f})
   • RESULT: HYPOTHESIS REVERSED - Antagonisms have HIGHER frequency ratios than synergies

2. COHERENCE DEFICIT
   • Biological δ-deficit: {results['coherence_deficit']['delta_deficit_percent']:.2f}%
   • Cosmological δ-deficit: {results['coherence_deficit']['theoretical_deficit']*100:.2f}%
   • Ratio: {results['coherence_deficit']['ratio_to_theory']:.1f}× larger in biological systems
   • INTERPRETATION: Different dissident mechanisms or scales between biology and cosmology

3. DISSIDENT STATES
   • Identified: {results['dissidents']['count']} nutrients below threshold
   • Time dilation: ~{results['temporal_trap']['time_slowdown_percent']:.1f}% slower
   • IMPLICATION: Suboptimal states are temporally trapped, explaining persistence
"""

ax1.text(0.05, 0.95, summary_text, transform=ax1.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Panel B: Frequency ratio violin plot
ax2 = fig4.add_subplot(gs[1, 0])
parts = ax2.violinplot([syn_ratios, ant_ratios], positions=[1, 2],
                       showmeans=True, showextrema=True)
for pc, color in zip(parts['bodies'], [colors['synergy'], colors['antagonism']]):
    pc.set_facecolor(color)
    pc.set_alpha(0.7)
ax2.set_xticks([1, 2])
ax2.set_xticklabels(['Synergies', 'Antagonisms'])
ax2.set_ylabel('Frequency Ratio', fontsize=10, fontweight='bold')
ax2.set_title('Frequency Distributions', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Panel C: Deficit comparison pie
ax3 = fig4.add_subplot(gs[1, 1])
deficit_bio = results['coherence_deficit']['delta_deficit_percent']
deficit_cos = results['coherence_deficit']['theoretical_deficit'] * 100
sizes = [deficit_bio, 100 - deficit_bio]
labels = [f'δ-deficit\n{deficit_bio:.1f}%', f'Coherence\n{100-deficit_bio:.1f}%']
colors_pie = [colors['dissident'], colors['optimal']]
ax3.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax3.set_title('Biological Coherence Budget', fontsize=11, fontweight='bold')

# Panel D: Dissident count
ax4 = fig4.add_subplot(gs[1, 2])
dissident_count = results['dissidents']['count']
optimal_count = 84 - dissident_count
bars = ax4.bar(['Dissidents', 'Optimal'], [dissident_count, optimal_count],
               color=[colors['dissident'], colors['optimal']], alpha=0.7,
               edgecolor='black', linewidth=2)
ax4.set_ylabel('Count', fontsize=10, fontweight='bold')
ax4.set_title('Nutrient State Distribution', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Panel E: Scale comparison
ax5 = fig4.add_subplot(gs[2, :])
scales = ['Cosmological\n(Time Study)', 'Biological\n(This Study)']
scale_deficits = [0.15, deficit_bio]
bars = ax5.bar(scales, scale_deficits, color=[colors['optimal'], colors['dissident']],
               alpha=0.7, edgecolor='black', linewidth=2, width=0.5)
ax5.set_ylabel('δ-Deficit (%)', fontsize=12, fontweight='bold')
ax5.set_title(f'Cross-Scale Comparison: {results["coherence_deficit"]["ratio_to_theory"]:.1f}× Difference', 
              fontsize=13, fontweight='bold')
ax5.set_yscale('log')
ax5.grid(True, alpha=0.3, axis='y', which='both')

for bar, val in zip(bars, scale_deficits):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.2f}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.savefig('figure4_comprehensive_summary.png', dpi=300, bbox_inches='tight')
print("✓ Generated Figure 4: Comprehensive Summary")

print()
print("=" * 80)
print("ALL FIGURES GENERATED")
print("=" * 80)
print()
print("Generated files:")
print("  1. figure1_frequency_coherence_test.png")
print("  2. figure2_coherence_deficit_analysis.png")
print("  3. figure3_category_analysis.png")
print("  4. figure4_comprehensive_summary.png")
print()
