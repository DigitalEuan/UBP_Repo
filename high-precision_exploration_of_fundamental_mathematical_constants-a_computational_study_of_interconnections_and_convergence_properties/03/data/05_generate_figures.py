#!/usr/bin/env python3
"""
Generate Publication-Quality Figures and Tables

Create comprehensive visualizations of UBP results for academic paper.
"""

import mpmath as mp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
from pathlib import Path

# Set publication-quality parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.dpi'] = 300

# Matplotlib backend for non-interactive
plt.switch_backend('Agg')

print("="*80)
print("GENERATING PUBLICATION FIGURES")
print("="*80)

# =============================================================================
# LOAD RESULTS
# =============================================================================
with open('/app/sandbox/session_20251215_122025_664f88889fdc/results/ubp_v4_validation.json', 'r') as f:
    validation = json.load(f)

with open('/app/sandbox/session_20251215_122025_664f88889fdc/results/delta_tau_search.json', 'r') as f:
    delta_tau_results = json.load(f)

with open('/app/sandbox/session_20251215_122025_664f88889fdc/results/delta_w_search.json', 'r') as f:
    delta_w_results = json.load(f)

with open('/app/sandbox/session_20251215_122025_664f88889fdc/results/ckm_alpha_analysis.json', 'r') as f:
    ckm_alpha = json.load(f)

print("✅ Results loaded")

# =============================================================================
# FIGURE 1: UBP MASS SPECTRUM OVERVIEW
# =============================================================================
print("\nGenerating Figure 1: Mass Spectrum Overview...")

fig, ax = plt.subplots(figsize=(12, 8))

# Particle data (MeV)
particles = ['e', 'μ', 'τ', 'd', 's', 'c', 'b', 't', 'W', 'Z', 'H']
pdg_masses = [
    0.511, 105.66, 1776.86,
    4.7, 93.5, 1273, 4183, 173000,  # quarks (top added)
    80379, 91188, 125100  # bosons
]

colors = ['#2E86AB', '#2E86AB', '#2E86AB',  # Leptons (blue)
          '#A23B72', '#A23B72', '#A23B72', '#A23B72', '#A23B72',  # Quarks (purple)
          '#F18F01', '#F18F01', '#F18F01']  # Bosons (orange)

ax.barh(particles, pdg_masses, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_xscale('log')
ax.set_xlabel('Mass (MeV)', fontsize=12, fontweight='bold')
ax.set_title('Standard Model Particle Mass Spectrum', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add legend
lepton_patch = mpatches.Patch(color='#2E86AB', label='Leptons')
quark_patch = mpatches.Patch(color='#A23B72', label='Quarks')
boson_patch = mpatches.Patch(color='#F18F01', label='Bosons')
ax.legend(handles=[lepton_patch, quark_patch, boson_patch], loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/01_mass_spectrum.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/01_mass_spectrum.pdf', bbox_inches='tight')
plt.close()
print("✅ Saved: 01_mass_spectrum.png/pdf")

# =============================================================================
# FIGURE 2: GEOMETRIC LAW VALIDATION
# =============================================================================
print("\nGenerating Figure 2: Geometric Law Validation...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: Muon prediction accuracy
Y = validation['fundamental_constants']['Y']
Y_inv = validation['fundamental_constants']['Y_inv']
M_e = validation['pdg_targets']['electron']
M_mu_predicted = M_e * (Y_inv**4 + np.floor(Y_inv))
M_mu_target = validation['pdg_targets']['muon']

ax1.bar(['Electron\n(Baseline)', 'Muon\n(Predicted)', 'Muon\n(PDG)'],
        [M_e, M_mu_predicted, M_mu_target],
        color=['#2E86AB', '#4CAF50', '#2E86AB'],
        alpha=0.7, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Mass (MeV)', fontsize=12, fontweight='bold')
ax1.set_title('A. Electron-Muon Geometric Law', fontsize=12, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3, axis='y')
ax1.text(1, M_mu_predicted * 1.1, f'Error: {validation["geometric_laws_validated"]["muon"]["error_percent"]:.4f}%',
         ha='center', fontsize=10, color='red', fontweight='bold')

# Panel B: Error comparison
particles_validated = ['μ', 'δ_τ', 'δ_W']
errors = [
    validation['geometric_laws_validated']['muon']['error_percent'],
    delta_tau_results['best_integer_ratio']['error_percent'],
    delta_w_results['best_integer_multiple']['error_percent']
]
colors_bar = ['#4CAF50', '#FFC107', '#FF9800']

ax2.bar(particles_validated, errors, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Prediction Error (%)', fontsize=12, fontweight='bold')
ax2.set_title('B. Geometric Expression Accuracy', fontsize=12, fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, axis='y')
ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1, label='1% threshold')
ax2.axhline(y=0.1, color='green', linestyle='--', linewidth=1, label='0.1% threshold')
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/02_geometric_law_validation.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/02_geometric_law_validation.pdf', bbox_inches='tight')
plt.close()
print("✅ Saved: 02_geometric_law_validation.png/pdf")

# =============================================================================
# FIGURE 3: DELTA TAU SEARCH RESULTS
# =============================================================================
print("\nGenerating Figure 3: Delta Tau Search Results...")

fig, ax = plt.subplots(figsize=(10, 6))

# Top 20 candidates
top_candidates = delta_tau_results['top_50_candidates'][:20]
expressions = [c['expression'] for c in top_candidates]
errors = [c['error_percent'] for c in top_candidates]

colors_grad = ['#4CAF50' if e < 1 else '#FFC107' if e < 5 else '#FF9800' for e in errors]

ax.barh(expressions, errors, color=colors_grad, alpha=0.7, edgecolor='black', linewidth=1)
ax.set_xlabel('Error (%)', fontsize=12, fontweight='bold')
ax.set_title('δ_τ Candidate Expressions (Ranked by Accuracy)', fontsize=14, fontweight='bold')
ax.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='1% threshold')
ax.axvline(x=0.1, color='green', linestyle='--', linewidth=1.5, label='0.1% threshold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='x')

# Highlight best match
best_expr = delta_tau_results['best_integer_ratio']
ax.text(0.5, 19, f"Best: ({best_expr['numerator']}/{best_expr['denominator']})×Y\nError: {best_expr['error_percent']:.4f}%",
        fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7), fontweight='bold')

plt.tight_layout()
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/03_delta_tau_search.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/03_delta_tau_search.pdf', bbox_inches='tight')
plt.close()
print("✅ Saved: 03_delta_tau_search.png/pdf")

# =============================================================================
# FIGURE 4: DELTA W SEARCH RESULTS
# =============================================================================
print("\nGenerating Figure 4: Delta W Search Results...")

fig, ax = plt.subplots(figsize=(10, 6))

# Top 15 candidates
top_candidates_w = delta_w_results['top_50_candidates'][:15]
expressions_w = [c['expression'] for c in top_candidates_w]
errors_w = [c['error_percent'] for c in top_candidates_w]

colors_grad_w = ['#4CAF50' if e < 1 else '#FFC107' if e < 5 else '#FF9800' for e in errors_w]

ax.barh(expressions_w, errors_w, color=colors_grad_w, alpha=0.7, edgecolor='black', linewidth=1)
ax.set_xlabel('Error (%)', fontsize=12, fontweight='bold')
ax.set_title('δ_W Candidate Expressions (Ranked by Accuracy)', fontsize=14, fontweight='bold')
ax.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='1% threshold')
ax.axvline(x=0.1, color='green', linestyle='--', linewidth=1.5, label='0.1% threshold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='x')

# Highlight top 3
best_w = delta_w_results['best_integer_multiple']
ax.text(0.3, 13, f"Best: {best_w['multiplier']}×(1/Y)\nError: {best_w['error_percent']:.4f}%",
        fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7), fontweight='bold')

plt.tight_layout()
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/04_delta_w_search.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/04_delta_w_search.pdf', bbox_inches='tight')
plt.close()
print("✅ Saved: 04_delta_w_search.png/pdf")

# =============================================================================
# FIGURE 5: CKM MATRIX GEOMETRIC RELATIONSHIPS
# =============================================================================
print("\nGenerating Figure 5: CKM Matrix Results...")

fig, ax = plt.subplots(figsize=(10, 6))

# Best 10 CKM matches
top_ckm = ckm_alpha['ckm_matrix']['test_results'][:10]
ckm_labels = [f"{c['target']}: {c['expression']}" for c in top_ckm]
ckm_errors = [c['error_percent'] for c in top_ckm]

colors_ckm = ['#4CAF50' if e < 1 else '#FFC107' if e < 5 else '#FF9800' for e in ckm_errors]

ax.barh(ckm_labels, ckm_errors, color=colors_ckm, alpha=0.7, edgecolor='black', linewidth=1)
ax.set_xlabel('Error (%)', fontsize=12, fontweight='bold')
ax.set_title('CKM Matrix Element Geometric Expressions', fontsize=14, fontweight='bold')
ax.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='1% threshold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/05_ckm_matrix.png', dpi=300, bbox_inches='tight')
plt.savefig('/app/sandbox/session_20251215_122025_664f88889fdc/figures/05_ckm_matrix.pdf', bbox_inches='tight')
plt.close()
print("✅ Saved: 05_ckm_matrix.png/pdf")

# =============================================================================
# GENERATE SUMMARY TABLE (CSV)
# =============================================================================
print("\nGenerating summary table...")

import csv

summary_data = [
    ["Particle/Observable", "PDG Value", "UBP Expression", "Predicted Value", "Error (%)"],
    ["", "", "", "", ""],
    ["LEPTONS", "", "", "", ""],
    ["Muon (μ)", "105.658 MeV", "(1/Y)⁴ + ⌊1/Y⌋", f"{M_mu_predicted:.3f} MeV", f"{validation['geometric_laws_validated']['muon']['error_percent']:.4f}"],
    ["Tau (τ) correction", f"{delta_tau_results['target']:.6f}", f"(29/93)×Y", f"{delta_tau_results['best_integer_ratio']['value']:.6f}", f"{delta_tau_results['best_integer_ratio']['error_percent']:.4f}"],
    ["", "", "", "", ""],
    ["WEAK BOSONS", "", "", "", ""],
    ["W correction", f"{delta_w_results['target']:.2f}", "75e or 54(1/Y)", f"{delta_w_results['top_50_candidates'][0]['value']:.2f}", f"{delta_w_results['top_50_candidates'][0]['error_percent']:.3f}"],
    ["", "", "", "", ""],
    ["QUARK MIXING", "", "", "", ""],
    ["V_ud (CKM)", "0.97435", "cos(π/14)", f"{ckm_alpha['ckm_matrix']['test_results'][0]['value']:.5f}", f"{ckm_alpha['ckm_matrix']['test_results'][0]['error_percent']:.3f}"],
    ["V_us (CKM)", "0.22500", "sin(π/14) or 2/9", f"{ckm_alpha['ckm_matrix']['test_results'][3]['value']:.5f}", f"{ckm_alpha['ckm_matrix']['test_results'][3]['error_percent']:.3f}"],
]

output_table = Path('/app/sandbox/session_20251215_122025_664f88889fdc/results/ubp_final_summary.csv')
with open(output_table, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(summary_data)

print(f"✅ Saved: ubp_final_summary.csv")

print("\n" + "="*80)
print("✅ All figures generated successfully!")
print("="*80)
print("\nGenerated files:")
print("  📊 01_mass_spectrum.png/pdf")
print("  📊 02_geometric_law_validation.png/pdf")
print("  📊 03_delta_tau_search.png/pdf")
print("  📊 04_delta_w_search.png/pdf")
print("  📊 05_ckm_matrix.png/pdf")
print("  📄 ubp_final_summary.csv")
