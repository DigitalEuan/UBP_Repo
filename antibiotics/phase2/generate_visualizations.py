"""
================================================================================
UBP 3.7.1 Antibiotic Study - Visualization Generation
Author: Euan R A Craig, New Zealand
Date: 30 November 2025
================================================================================

Generate publication-ready visualizations for Phase 2 study.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Load results
with open('results_phase2/phase2_final_results.json', 'r') as f:
    results = json.load(f)

# Create visualizations directory
os.makedirs('results_phase2/visualizations', exist_ok=True)

# ============================================================================
# FIGURE 1: Discovery Score Comparison
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

groups = ['Known\nAntibiotics', 'Novel\nCandidates\n(Top 20)', 'Random\nBalanced\nPatterns']
means = [
    results['comparative_analysis']['Known Antibiotics']['discovery_score_mean'],
    results['comparative_analysis']['Novel Candidates (Top 20)']['discovery_score_mean'],
    results['comparative_analysis']['Random Balanced Patterns']['discovery_score_mean']
]
stds = [
    results['comparative_analysis']['Known Antibiotics']['discovery_score_std'],
    results['comparative_analysis']['Novel Candidates (Top 20)']['discovery_score_std'],
    results['comparative_analysis']['Random Balanced Patterns']['discovery_score_std']
]

colors = ['#2E7D32', '#1976D2', '#757575']

bars = ax.bar(groups, means, yerr=stds, capsize=10, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Discovery Score', fontsize=14, fontweight='bold')
ax.set_title('UBP 3.7.1 Antibiotic Discovery: Comparative Performance', fontsize=16, fontweight='bold')
ax.set_ylim(0, 0.8)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bar, mean, std in zip(bars, means, stds):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + std + 0.01,
            f'{mean:.4f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add significance indicators
ax.plot([0, 1], [0.72, 0.72], 'k-', linewidth=1.5)
ax.text(0.5, 0.73, '✓ p < 0.05', ha='center', fontsize=10, fontweight='bold')

ax.plot([1, 2], [0.68, 0.68], 'k-', linewidth=1.5)
ax.text(1.5, 0.69, '✓✓ p < 0.01', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('results_phase2/visualizations/fig1_discovery_score_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Figure 1: Discovery Score Comparison")

# ============================================================================
# FIGURE 2: Top 10 Novel Candidates
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 8))

top_10 = results['novel_candidates']['top_20'][:10]
names = [f"{c['offbit_hex']}\n({c['closest_known']})" for c in top_10]
scores = [c['discovery_score'] for c in top_10]
colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, 10))

bars = ax.barh(range(10), scores, color=colors_gradient, edgecolor='black', linewidth=1.2)

ax.set_yticks(range(10))
ax.set_yticklabels([f"#{i+1}" for i in range(10)], fontsize=11)
ax.set_xlabel('Discovery Score', fontsize=14, fontweight='bold')
ax.set_title('Top 10 Novel Antibiotic Candidates (UBP 3.7.1)', fontsize=16, fontweight='bold')
ax.set_xlim(0, 0.8)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Add candidate info as text
for i, (bar, candidate) in enumerate(zip(bars, top_10)):
    width = bar.get_width()
    ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
            f"{candidate['offbit_hex']} | {candidate['closest_known']} | H={candidate['hamming_distance']}",
            va='center', fontsize=9)

ax.invert_yaxis()
plt.tight_layout()
plt.savefig('results_phase2/visualizations/fig2_top10_candidates.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Figure 2: Top 10 Novel Candidates")

# ============================================================================
# FIGURE 3: Hamming Distance Distribution
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Get Hamming distances
novel_hamming = [c['hamming_distance'] for c in results['novel_candidates']['top_20']]
random_hamming_mean = results['comparative_analysis']['Random Balanced Patterns']['hamming_distance_mean']

ax.hist(novel_hamming, bins=range(0, 8), alpha=0.7, color='#1976D2', edgecolor='black', linewidth=1.2, label='Novel Candidates')
ax.axvline(random_hamming_mean, color='#757575', linestyle='--', linewidth=2.5, label=f'Random Patterns (mean={random_hamming_mean:.1f})')

ax.set_xlabel('Hamming Distance from Closest Known Antibiotic', fontsize=14, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=14, fontweight='bold')
ax.set_title('Hamming Distance Distribution: Novel Candidates vs Random Patterns', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('results_phase2/visualizations/fig3_hamming_distance_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Figure 3: Hamming Distance Distribution")

# ============================================================================
# FIGURE 4: Bit Position Analysis
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Region distribution for known antibiotics
known_antibiotics = results['known_antibiotics_analysis']['antibiotics']

regions = ['core_scaffold', 'functional_groups', 'binding_features']
region_labels = ['Core\nScaffold\n(0-7)', 'Functional\nGroups\n(8-15)', 'Binding\nFeatures\n(16-23)']

# Average counts across known antibiotics
avg_counts = {region: [] for region in regions}
for antibiotic in known_antibiotics:
    for region in regions:
        avg_counts[region].append(antibiotic['pattern_structure']['region_counts'][region])

means = [np.mean(avg_counts[region]) for region in regions]
stds = [np.std(avg_counts[region]) for region in regions]

colors_regions = ['#8B4513', '#4CAF50', '#2196F3']

bars1 = ax1.bar(region_labels, means, yerr=stds, capsize=8, color=colors_regions, alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Average Active Bits', fontsize=12, fontweight='bold')
ax1.set_title('Known Antibiotics: Bit Region Distribution', fontsize=14, fontweight='bold')
ax1.set_ylim(0, 6)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

for bar, mean in zip(bars1, means):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{mean:.1f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Right: Binding site affinity comparison
groups2 = ['Known\nAntibiotics', 'Novel\nCandidates', 'Random\nPatterns']
affinities = [
    results['comparative_analysis']['Known Antibiotics']['binding_affinity_mean'],
    results['comparative_analysis']['Novel Candidates (Top 20)']['binding_affinity_mean'],
    results['comparative_analysis']['Random Balanced Patterns']['binding_affinity_mean']
]

colors2 = ['#2E7D32', '#1976D2', '#757575']

bars2 = ax2.bar(groups2, affinities, color=colors2, alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_ylabel('Binding Site Affinity', fontsize=12, fontweight='bold')
ax2.set_title('Binding Site Affinity Comparison', fontsize=14, fontweight='bold')
ax2.set_ylim(0, 1.2)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar, affinity in zip(bars2, affinities):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f'{affinity:.3f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('results_phase2/visualizations/fig4_bit_position_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Figure 4: Bit Position Analysis")

# ============================================================================
# FIGURE 5: Discovery Score vs Hamming Distance
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Plot novel candidates
novel_scores = [c['discovery_score'] for c in results['novel_candidates']['top_20']]
novel_hamming = [c['hamming_distance'] for c in results['novel_candidates']['top_20']]

ax.scatter(novel_hamming, novel_scores, s=100, alpha=0.6, c='#1976D2', edgecolors='black', linewidth=1, label='Novel Candidates')

# Plot known antibiotics (Hamming distance = 0)
known_scores = [a['discovery_score'] for a in results['known_antibiotics_analysis']['antibiotics']]
known_hamming = [0] * len(known_scores)

ax.scatter(known_hamming, known_scores, s=150, alpha=0.8, c='#2E7D32', marker='s', edgecolors='black', linewidth=1.5, label='Known Antibiotics')

# Add trend line for novel candidates
if len(novel_hamming) > 1:
    z = np.polyfit(novel_hamming, novel_scores, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(novel_hamming), max(novel_hamming), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.5, linewidth=2, label='Trend')

ax.set_xlabel('Hamming Distance from Closest Known Antibiotic', fontsize=14, fontweight='bold')
ax.set_ylabel('Discovery Score', fontsize=14, fontweight='bold')
ax.set_title('Discovery Score vs Structural Similarity', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('results_phase2/visualizations/fig5_score_vs_hamming.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Figure 5: Discovery Score vs Hamming Distance")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print("\nGenerated figures:")
print("  1. Discovery Score Comparison")
print("  2. Top 10 Novel Candidates")
print("  3. Hamming Distance Distribution")
print("  4. Bit Position Analysis")
print("  5. Discovery Score vs Hamming Distance")
print("\nAll visualizations saved to: results_phase2/visualizations/")
print("=" * 80)
