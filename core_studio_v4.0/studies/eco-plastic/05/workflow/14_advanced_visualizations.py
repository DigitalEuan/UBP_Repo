#!/usr/bin/env python3
"""
Advanced Visualizations for Eco-Plastic Design Study
====================================================

Generate publication-quality figures for the final study report.

Author: K-Dense Research System
Date: January 2, 2026
"""

import json
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0

# Directories
SESSION_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")
RESULTS_DIR = SESSION_DIR / "results"
FIGURES_DIR = SESSION_DIR / "figures"

print("Generating Advanced Visualizations...")
print()

# Load data
print("Loading results...")
with open(RESULTS_DIR / "island_ga_fitness_history_v5.json", 'r') as f:
    fitness_history = json.load(f)

with open(RESULTS_DIR / "eco_plastic_recipe_card_v5_advanced.json", 'r') as f:
    recipe = json.load(f)

with open(RESULTS_DIR / "advanced_eco_plastic_summary_v5.json", 'r') as f:
    summary = json.load(f)

print("✓ Data loaded")
print()

# ============================================================================
# Figure 1: Island GA Evolution Dynamics
# ============================================================================

print("Creating Figure 1: Island GA Evolution Dynamics...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Extract data
generations = [h['generation'] for h in fitness_history]
best_fitness = [h['best_fitness'] for h in fitness_history]
avg_fitness = [h['avg_island_fitness'] for h in fitness_history]

# Subplot A: Best fitness over time
ax1 = axes[0, 0]
ax1.plot(generations, best_fitness, 'b-', linewidth=2, label='Best Fitness')
ax1.axhline(y=best_fitness[-1], color='r', linestyle='--', alpha=0.5, label='Final Best')
ax1.set_xlabel('Generation', fontsize=12)
ax1.set_ylabel('Fitness', fontsize=12)
ax1.set_title('A) Best Fitness Evolution', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Subplot B: Average island fitness
ax2 = axes[0, 1]
ax2.plot(generations, avg_fitness, 'g-', linewidth=2, label='Avg Island Fitness')
ax2.plot(generations, best_fitness, 'b-', linewidth=1, alpha=0.5, label='Best Fitness')
ax2.set_xlabel('Generation', fontsize=12)
ax2.set_ylabel('Fitness', fontsize=12)
ax2.set_title('B) Island Diversity', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Mark migrations
migration_interval = 50
for gen in range(migration_interval, max(generations), migration_interval):
    ax2.axvline(x=gen, color='orange', linestyle=':', alpha=0.3)

# Subplot C: Per-island fitness trajectories
ax3 = axes[1, 0]
island_colors = ['red', 'blue', 'green', 'purple', 'orange']
for island_idx in range(5):
    island_fitness = [h['island_best_fitnesses'][island_idx] for h in fitness_history]
    ax3.plot(generations, island_fitness, color=island_colors[island_idx],
             linewidth=1.5, alpha=0.7, label=f'Island {island_idx+1}')
ax3.set_xlabel('Generation', fontsize=12)
ax3.set_ylabel('Best Fitness per Island', fontsize=12)
ax3.set_title('C) Island-Specific Evolution', fontsize=14, fontweight='bold')
ax3.legend(fontsize=9, ncol=2)
ax3.grid(True, alpha=0.3)

# Subplot D: Convergence analysis
ax4 = axes[1, 1]
# Calculate fitness improvement rate (derivative)
improvement_rate = np.diff([0] + best_fitness)
smoothed_rate = np.convolve(improvement_rate, np.ones(10)/10, mode='same')
ax4.plot(generations, smoothed_rate, 'purple', linewidth=2)
ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax4.set_xlabel('Generation', fontsize=12)
ax4.set_ylabel('Fitness Improvement Rate (smoothed)', fontsize=12)
ax4.set_title('D) Convergence Analysis', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = FIGURES_DIR / "island_ga_evolution_dynamics_v5.png"
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {fig_path}")
print()

# ============================================================================
# Figure 2: Multi-Objective Performance
# ============================================================================

print("Creating Figure 2: Multi-Objective Performance...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Subplot A: Fitness component breakdown (bar chart)
ax1 = axes[0]
components = summary['best_solution']['components']
component_names = [
    'Biodegradability',
    'Mechanical Score',
    'Cost Score',
    'Vital Score'
]
component_values = [
    components['biodegradability'],
    components['mechanical_score'],
    components['cost_score'],
    components['vital_score']
]
colors_map = ['#2ecc71', '#3498db', '#f39c12', '#9b59b6']
bars = ax1.barh(component_names, component_values, color=colors_map, alpha=0.8, edgecolor='black')
ax1.set_xlabel('Score', fontsize=12)
ax1.set_title('A) Multi-Objective Component Scores', fontsize=14, fontweight='bold')
ax1.set_xlim([0, 1.0])
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, component_values)):
    ax1.text(value + 0.02, i, f'{value:.3f}', va='center', fontsize=10, fontweight='bold')

# Subplot B: Property trade-off (radar chart)
ax2 = axes[1]
ax2.axis('off')

# Create radar chart manually
theta = np.linspace(0, 2 * np.pi, len(component_names), endpoint=False)
theta = np.concatenate((theta, [theta[0]]))  # Close the plot

values_radar = component_values + [component_values[0]]  # Close the plot

ax_radar = fig.add_subplot(122, projection='polar')
ax_radar.plot(theta, values_radar, 'o-', linewidth=2, color='#e74c3c', markersize=8)
ax_radar.fill(theta, values_radar, alpha=0.25, color='#e74c3c')
ax_radar.set_xticks(theta[:-1])
ax_radar.set_xticklabels(component_names, fontsize=10)
ax_radar.set_ylim([0, 1.0])
ax_radar.set_title('B) Multi-Objective Radar Profile', fontsize=14, fontweight='bold', pad=20)
ax_radar.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = FIGURES_DIR / "multi_objective_performance_v5.png"
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {fig_path}")
print()

# ============================================================================
# Figure 3: Recipe Card Visualization
# ============================================================================

print("Creating Figure 3: Recipe Card Visualization...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Title
fig.suptitle('Optimal Eco-Plastic Design: Recipe Card', fontsize=18, fontweight='bold')

# Panel A: UBP Fingerprint (MOG Grid)
ax1 = fig.add_subplot(gs[0, 0])
fingerprint_binary = recipe['fingerprint']['binary']
mog_grid = [list(fingerprint_binary[i:i+6]) for i in range(0, 24, 6)]
mog_array = np.array([[int(b) for b in row] for row in mog_grid])
im = ax1.imshow(mog_array, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax1.set_xticks(range(6))
ax1.set_yticks(range(4))
ax1.set_xticklabels(['Col 0', 'Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5'], fontsize=8)
ax1.set_yticklabels(['Row 0', 'Row 1', 'Row 2', 'Row 3'], fontsize=8)
ax1.set_title('A) MOG Grid (24-bit Fingerprint)', fontsize=12, fontweight='bold')

# Annotate bits
for i in range(4):
    for j in range(6):
        text = ax1.text(j, i, mog_array[i, j], ha="center", va="center",
                        color="white" if mog_array[i, j] == 1 else "black",
                        fontsize=12, fontweight='bold')

# Panel B: UBP Metrics (gauge-style)
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
metrics = recipe['ubp_metrics']
metric_text = f"""
UBP Metrics (Integer-Precision)

Biodegradability: {metrics['biodegradability']:.4f}
Persistence: {metrics['persistence']:.4f}
Vital Score: {metrics['vital_plastic_score']:.4f}
Lattice Tension: {metrics['lattice_tension']:.4f}

Stability Regime: {metrics['stability_regime']}
Distance to Octad: {metrics['distance_to_octad']} bits
Hamming Weight: {recipe['fingerprint']['hamming_weight']}
"""
ax2.text(0.1, 0.5, metric_text, fontsize=10, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax2.set_title('B) UBP Metrics', fontsize=12, fontweight='bold')

# Panel C: Predicted Properties
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
props = recipe['predicted_properties']
prop_text = f"""
Predicted Properties

Tensile Strength: {props['tensile_strength_mpa']:.1f} MPa
Cost: ${props['cost_per_kg_usd']:.2f}/kg

Target Range:
  Rings: {recipe['target_property_ranges']['rings']}
  Heteroatoms: {recipe['target_property_ranges']['heteroatoms']}
  TPSA: {recipe['target_property_ranges']['tpsa'][0]:.0f}-{recipe['target_property_ranges']['tpsa'][1]:.0f} Ų
  LogP: {recipe['target_property_ranges']['logp'][0]:.2f}-{recipe['target_property_ranges']['logp'][1]:.2f}
"""
ax3.text(0.1, 0.5, prop_text, fontsize=10, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax3.set_title('C) Target Properties', fontsize=12, fontweight='bold')

# Panel D: Top Monomers (bar chart)
ax4 = fig.add_subplot(gs[1, :])
top_monomers = recipe['recommended_monomers'][:5]
monomer_names = [m['name'] for m in top_monomers]
match_scores = [m['match_score'] for m in top_monomers]
costs = [m['cost_kg'] for m in top_monomers]

x_pos = np.arange(len(monomer_names))
bars1 = ax4.bar(x_pos - 0.2, match_scores, 0.4, label='Match Score', color='#2ecc71', alpha=0.8)
bars2 = ax4.bar(x_pos + 0.2, np.array(costs) / 20.0, 0.4, label='Cost (normalized)', color='#e74c3c', alpha=0.8)

ax4.set_xlabel('Monomer', fontsize=12)
ax4.set_ylabel('Score / Cost (normalized)', fontsize=12)
ax4.set_title('D) Top Recommended Monomers', fontsize=14, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(monomer_names, rotation=15, ha='right', fontsize=9)
ax4.legend(fontsize=10)
ax4.grid(axis='y', alpha=0.3)

# Panel E: Synthesis Recommendations
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')
synth = recipe['synthesis_recommendations']
synth_text = f"""
SYNTHESIS PROTOCOL

Polymerization Method: {synth['polymerization_method']}
Catalyst: {synth['catalyst']}
Temperature: {synth['temperature_c']}°C
Pressure: {synth['pressure']}
Reaction Time: {synth['time_hours']} hours
Post-Treatment: {synth['post_treatment']}

NEXT STEPS:
1. Lab synthesis using recommended monomers
2. Mechanical testing (tensile, impact, elongation)
3. Biodegradability testing (ISO 14855 compost test)
4. Toxicity screening (OECD 201, 202, 203)
5. Life cycle assessment (cradle-to-grave)
6. Scale-up feasibility and cost analysis
"""
ax5.text(0.05, 0.5, synth_text, fontsize=10, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

fig_path = FIGURES_DIR / "recipe_card_visualization_v5.png"
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {fig_path}")
print()

# ============================================================================
# Figure 4: Comparison to Baseline
# ============================================================================

print("Creating Figure 4: Comparison to Baseline Materials...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Baseline materials data
materials = ['PLA', 'PCL', 'PET', 'PFAS', 'Evolved\nEco-Plastic']
biodeg = [0.65, 0.60, 0.18, 0.01, recipe['ubp_metrics']['biodegradability']]
vital_scores = [0.58, 0.62, 0.45, 0.72, recipe['ubp_metrics']['vital_plastic_score']]
tensile = [50.0, 25.0, 60.0, 100.0, recipe['predicted_properties']['tensile_strength_mpa']]
cost = [4.0, 6.0, 2.5, 30.0, recipe['predicted_properties']['cost_per_kg_usd']]

# Subplot A: Biodegradability vs Vital Score
ax1 = axes[0]
colors = ['blue', 'green', 'orange', 'red', 'purple']
for i, mat in enumerate(materials):
    ax1.scatter(biodeg[i], vital_scores[i], s=300, color=colors[i], alpha=0.7, edgecolor='black', linewidth=2)
    ax1.text(biodeg[i], vital_scores[i], mat, ha='center', va='center', fontsize=9, fontweight='bold')

ax1.set_xlabel('Biodegradability', fontsize=12)
ax1.set_ylabel('Vital Plastic Score', fontsize=12)
ax1.set_title('A) Biodegradability vs Geometric Optimality', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, 1])
ax1.set_ylim([0, 1.1])

# Highlight optimal region
ax1.axhspan(0.75, 1.0, alpha=0.1, color='green', label='High Vital Score')
ax1.axvspan(0.60, 1.0, alpha=0.1, color='blue', label='High Biodeg')

# Subplot B: Cost vs Tensile Strength
ax2 = axes[1]
for i, mat in enumerate(materials):
    ax2.scatter(cost[i], tensile[i], s=300, color=colors[i], alpha=0.7, edgecolor='black', linewidth=2)
    ax2.text(cost[i], tensile[i], mat, ha='center', va='center', fontsize=9, fontweight='bold')

ax2.set_xlabel('Cost (USD/kg)', fontsize=12)
ax2.set_ylabel('Tensile Strength (MPa)', fontsize=12)
ax2.set_title('B) Cost vs Mechanical Performance', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Highlight optimal region
ax2.axhspan(50, 80, alpha=0.1, color='green', label='Target Tensile')
ax2.axvspan(2, 10, alpha=0.1, color='blue', label='Low Cost')

plt.tight_layout()
fig_path = FIGURES_DIR / "comparison_to_baseline_v5.png"
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {fig_path}")
print()

print("=" * 80)
print("ALL VISUALIZATIONS COMPLETE")
print("=" * 80)
print("Generated figures:")
print(f"  1. {FIGURES_DIR}/island_ga_evolution_dynamics_v5.png")
print(f"  2. {FIGURES_DIR}/multi_objective_performance_v5.png")
print(f"  3. {FIGURES_DIR}/recipe_card_visualization_v5.png")
print(f"  4. {FIGURES_DIR}/comparison_to_baseline_v5.png")
print()
