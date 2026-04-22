"""
================================================================================
UBP × MathNet ANALYSIS & VISUALIZATION
================================================================================
Produces all plots and summary statistics for the investigation report.
================================================================================
"""

import json
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from collections import defaultdict

# ─── LOAD RESULTS ────────────────────────────────────────────────────────────

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(BASE, "results", "ubp_mathnet_results.json")
PLOTS_DIR = os.path.join(BASE, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

with open(RESULTS_PATH) as f:
    data = json.load(f)

results = data["results"]
meta = data["metadata"]

print(f"Loaded {len(results)} results from {meta['date']}")
print(f"System: {meta['system']} | Benchmark: {meta['benchmark']}")

# ─── EXTRACT KEY METRICS ─────────────────────────────────────────────────────

domains = [r["domain"] for r in results]
nrci_vals = [r["math_column"]["mean_nrci"] for r in results]
soc_vals = [r["sovereign_column"]["soc_energy"] / 1e6 for r in results]  # in MCU
coherence_vals = [r["sovereign_column"]["coherence_score"] for r in results]
alignment_vals = [r["grading"]["alignment_score"] for r in results]
correctness_scores = [r["grading"]["correctness_score"] for r in results]
correctness_labels = [r["grading"]["correctness_label"] for r in results]
ubp_conf = [r["grading"]["ubp_confidence"] for r in results]
prime_density = [r["math_column"]["prime_density"] for r in results]
geo_complexity = [r["math_column"]["geometric_complexity"] for r in results]
semantic_res = [r["language_column"]["semantic_resonance"] for r in results]
manifestation = [r["sovereign_column"]["manifestation"] for r in results]
sym_tax = [r["sovereign_column"]["symmetry_tax"] for r in results]
golay_addr = [r["sovereign_column"]["golay_address"] for r in results]
problem_ids = [r["problem_id"] for r in results]

# Domain grouping
domain_set = sorted(set(domains))
domain_colors = {
    "Number Theory": "#e74c3c",
    "Algebra": "#3498db",
    "Geometry": "#2ecc71",
    "Combinatorics": "#f39c12"
}

# ─── SUMMARY STATISTICS ──────────────────────────────────────────────────────

print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)

correct = correctness_labels.count("CORRECT")
partial = correctness_labels.count("PARTIAL")
incorrect = correctness_labels.count("INCORRECT")
total = len(results)

print(f"Correctness: CORRECT={correct} ({100*correct/total:.1f}%), "
      f"PARTIAL={partial} ({100*partial/total:.1f}%), "
      f"INCORRECT={incorrect} ({100*incorrect/total:.1f}%)")
print(f"Mean NRCI:       {np.mean(nrci_vals):.4f} ± {np.std(nrci_vals):.4f}")
print(f"Mean SOC:        {np.mean(soc_vals):.1f} MCU ± {np.std(soc_vals):.1f}")
print(f"Mean Coherence:  {np.mean(coherence_vals):.4f}")
print(f"Mean Alignment:  {np.mean(alignment_vals):.4f}")
print(f"Mean UBP Conf:   {np.mean(ubp_conf):.4f}")
print(f"Mean Sem. Res.:  {np.mean(semantic_res):.4f}")

# Per-domain stats
print("\nPer-Domain Statistics:")
print(f"{'Domain':<20} {'N':<5} {'NRCI':<10} {'SOC(M)':<12} {'Correct%':<12}")
print("-"*60)
for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    d_nrci = np.mean([nrci_vals[i] for i in idx])
    d_soc = np.mean([soc_vals[i] for i in idx])
    d_corr = sum(1 for i in idx if correctness_labels[i] == "CORRECT")
    d_part = sum(1 for i in idx if correctness_labels[i] == "PARTIAL")
    print(f"{dom:<20} {len(idx):<5} {d_nrci:.4f}     {d_soc:.1f}M       "
          f"{100*(d_corr+0.5*d_part)/len(idx):.1f}%")

# ─── PLOT 1: TCT OVERVIEW DASHBOARD ──────────────────────────────────────────

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor('#0d1117')
gs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

ax_title = fig.add_subplot(gs[0, :])
ax_title.axis('off')
ax_title.text(0.5, 0.7, 'UBP × MathNet Benchmark — Three Column Thinking Analysis',
              ha='center', va='center', fontsize=16, fontweight='bold',
              color='white', transform=ax_title.transAxes)
ax_title.text(0.5, 0.2,
              f'UBP core_studio_v4.0 | Golay [24,12,8] + Leech Λ₂₄ | {total} Olympiad Problems',
              ha='center', va='center', fontsize=10, color='#aaaaaa',
              transform=ax_title.transAxes)

# Plot 1a: NRCI by domain
ax1 = fig.add_subplot(gs[1, 0])
ax1.set_facecolor('#161b22')
for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    vals = [nrci_vals[i] for i in idx]
    ax1.scatter([dom[:4]]*len(vals), vals, color=domain_colors[dom],
                s=60, alpha=0.8, zorder=3)
    ax1.plot([dom[:4]], [np.mean(vals)], 'w_', markersize=20, markeredgewidth=2)
ax1.set_xlabel('Domain', color='white', fontsize=9)
ax1.set_ylabel('NRCI', color='white', fontsize=9)
ax1.set_title('Col 1: NRCI by Domain', color='white', fontsize=10, fontweight='bold')
ax1.tick_params(colors='white', labelsize=8)
ax1.spines['bottom'].set_color('#444')
ax1.spines['left'].set_color('#444')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.axhline(0.7, color='#f39c12', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(3.4, 0.705, 'MANIFEST', color='#f39c12', fontsize=7)

# Plot 1b: SOC Energy distribution
ax2 = fig.add_subplot(gs[1, 1])
ax2.set_facecolor('#161b22')
colors_soc = [domain_colors[d] for d in domains]
bars = ax2.bar(range(total), soc_vals, color=colors_soc, alpha=0.85, edgecolor='none')
ax2.set_xlabel('Problem Index', color='white', fontsize=9)
ax2.set_ylabel('SOC Energy (MCU)', color='white', fontsize=9)
ax2.set_title('Col 2: SOC Energy Profile', color='white', fontsize=10, fontweight='bold')
ax2.tick_params(colors='white', labelsize=8)
ax2.spines['bottom'].set_color('#444')
ax2.spines['left'].set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Plot 1c: Semantic resonance
ax3 = fig.add_subplot(gs[1, 2])
ax3.set_facecolor('#161b22')
for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    vals = [semantic_res[i] for i in idx]
    ax3.scatter([dom[:4]]*len(vals), vals, color=domain_colors[dom],
                s=60, alpha=0.8, zorder=3)
ax3.set_xlabel('Domain', color='white', fontsize=9)
ax3.set_ylabel('Semantic Resonance', color='white', fontsize=9)
ax3.set_title('Col 3: Semantic Resonance', color='white', fontsize=10, fontweight='bold')
ax3.tick_params(colors='white', labelsize=8)
ax3.spines['bottom'].set_color('#444')
ax3.spines['left'].set_color('#444')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Plot 1d: Correctness pie
ax4 = fig.add_subplot(gs[1, 3])
ax4.set_facecolor('#161b22')
sizes = [correct, partial, incorrect]
labels = [f'CORRECT\n{correct}', f'PARTIAL\n{partial}', f'INCORRECT\n{incorrect}']
colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
wedges, texts, autotexts = ax4.pie(
    sizes, labels=labels, colors=colors_pie,
    autopct='%1.0f%%', startangle=90,
    textprops={'color': 'white', 'fontsize': 8}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(9)
ax4.set_title('Correctness Distribution', color='white', fontsize=10, fontweight='bold')

# Plot 1e: TCT Alignment heatmap
ax5 = fig.add_subplot(gs[2, :2])
ax5.set_facecolor('#161b22')
# Create alignment matrix: problem vs metric
metrics = ['NRCI', 'SOC/M', 'Coherence', 'Alignment', 'Sem.Res.']
matrix = []
for i in range(total):
    row = [
        nrci_vals[i],
        min(1.0, soc_vals[i] / max(soc_vals)),
        coherence_vals[i],
        alignment_vals[i],
        min(1.0, semantic_res[i])
    ]
    matrix.append(row)
matrix = np.array(matrix).T  # shape: (5, 20)
im = ax5.imshow(matrix, aspect='auto', cmap='plasma', vmin=0, vmax=1)
ax5.set_yticks(range(len(metrics)))
ax5.set_yticklabels(metrics, color='white', fontsize=8)
ax5.set_xticks(range(total))
ax5.set_xticklabels([p.split('_')[1]+'_'+p.split('_')[2] for p in problem_ids],
                    rotation=45, ha='right', color='white', fontsize=7)
ax5.set_title('TCT Metric Heatmap (all 20 problems × 5 metrics)', color='white',
              fontsize=10, fontweight='bold')
plt.colorbar(im, ax=ax5, fraction=0.02, pad=0.02).ax.tick_params(colors='white')

# Plot 1f: NRCI vs Correctness scatter
ax6 = fig.add_subplot(gs[2, 2])
ax6.set_facecolor('#161b22')
label_colors = {'CORRECT': '#2ecc71', 'PARTIAL': '#f39c12', 'INCORRECT': '#e74c3c'}
for i in range(total):
    ax6.scatter(nrci_vals[i], alignment_vals[i],
                color=label_colors[correctness_labels[i]],
                s=80, alpha=0.85, edgecolors='white', linewidths=0.5)
ax6.set_xlabel('Mean NRCI', color='white', fontsize=9)
ax6.set_ylabel('TCT Alignment', color='white', fontsize=9)
ax6.set_title('NRCI vs TCT Alignment', color='white', fontsize=10, fontweight='bold')
ax6.tick_params(colors='white', labelsize=8)
ax6.spines['bottom'].set_color('#444')
ax6.spines['left'].set_color('#444')
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
patches = [mpatches.Patch(color=c, label=l) for l, c in label_colors.items()]
ax6.legend(handles=patches, fontsize=7, framealpha=0.3,
           labelcolor='white', facecolor='#0d1117')

# Plot 1g: Golay address distribution
ax7 = fig.add_subplot(gs[2, 3])
ax7.set_facecolor('#161b22')
ax7.hist(golay_addr, bins=15, color='#9b59b6', edgecolor='white', linewidth=0.5, alpha=0.85)
ax7.set_xlabel('Golay Address', color='white', fontsize=9)
ax7.set_ylabel('Count', color='white', fontsize=9)
ax7.set_title('Golay Address Distribution', color='white', fontsize=10, fontweight='bold')
ax7.tick_params(colors='white', labelsize=8)
ax7.spines['bottom'].set_color('#444')
ax7.spines['left'].set_color('#444')
ax7.spines['top'].set_visible(False)
ax7.spines['right'].set_visible(False)

# Legend for domain colors
legend_patches = [mpatches.Patch(color=c, label=d) for d, c in domain_colors.items()]
fig.legend(handles=legend_patches, loc='lower center', ncol=4,
           fontsize=9, framealpha=0.3, labelcolor='white', facecolor='#0d1117',
           bbox_to_anchor=(0.5, 0.01))

plt.savefig(os.path.join(PLOTS_DIR, 'ubp_mathnet_dashboard.png'),
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: ubp_mathnet_dashboard.png")

# ─── PLOT 2: SOVEREIGN COLUMN DEEP DIVE ──────────────────────────────────────

fig2, axes = plt.subplots(2, 3, figsize=(16, 10))
fig2.patch.set_facecolor('#0d1117')
fig2.suptitle('UBP Sovereign Column Analysis — Golay/Leech Lattice Geometry',
              fontsize=14, fontweight='bold', color='white', y=0.98)

# 2a: Symmetry tax by domain
ax = axes[0, 0]
ax.set_facecolor('#161b22')
for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    vals = [sym_tax[i] for i in idx]
    ax.scatter([dom[:4]]*len(vals), vals, color=domain_colors[dom], s=70, alpha=0.85)
    ax.plot([dom[:4]], [np.mean(vals)], 'w_', markersize=20, markeredgewidth=2)
ax.set_title('Leech Symmetry Tax by Domain', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel('Symmetry Tax (Λ₂₄)', color='white', fontsize=9)
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

# 2b: Manifestation status distribution
ax = axes[0, 1]
ax.set_facecolor('#161b22')
manif_counts = defaultdict(int)
for m in manifestation:
    manif_counts[m] += 1
manif_labels = list(manif_counts.keys())
manif_vals = [manif_counts[k] for k in manif_labels]
manif_colors = {'MANIFESTED': '#2ecc71', 'SUBLIMINAL': '#f39c12',
                'LATENT': '#e74c3c', 'UNKNOWN': '#95a5a6'}
bar_colors = [manif_colors.get(m, '#95a5a6') for m in manif_labels]
ax.bar(manif_labels, manif_vals, color=bar_colors, edgecolor='white', linewidth=0.5)
ax.set_title('Observer Manifestation Status', color='white', fontsize=10, fontweight='bold')
ax.set_ylabel('Count', color='white', fontsize=9)
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

# 2c: SOC Energy vs Symmetry Tax
ax = axes[0, 2]
ax.set_facecolor('#161b22')
for i in range(total):
    ax.scatter(sym_tax[i], soc_vals[i],
               color=domain_colors[domains[i]], s=70, alpha=0.85,
               edgecolors='white', linewidths=0.5)
ax.set_xlabel('Symmetry Tax (Λ₂₄)', color='white', fontsize=9)
ax.set_ylabel('SOC Energy (MCU)', color='white', fontsize=9)
ax.set_title('SOC Energy vs Symmetry Tax', color='white', fontsize=10, fontweight='bold')
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

# 2d: Coherence score radar-style bar
ax = axes[1, 0]
ax.set_facecolor('#161b22')
x = range(total)
bar_colors_coh = [domain_colors[d] for d in domains]
ax.bar(x, coherence_vals, color=bar_colors_coh, alpha=0.85, edgecolor='none')
ax.axhline(np.mean(coherence_vals), color='white', linestyle='--', linewidth=1, alpha=0.7)
ax.set_xlabel('Problem Index', color='white', fontsize=9)
ax.set_ylabel('Coherence Score', color='white', fontsize=9)
ax.set_title('Sovereign Coherence per Problem', color='white', fontsize=10, fontweight='bold')
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

# 2e: Golay address vs NRCI
ax = axes[1, 1]
ax.set_facecolor('#161b22')
for i in range(total):
    ax.scatter(golay_addr[i], nrci_vals[i],
               color=domain_colors[domains[i]], s=70, alpha=0.85,
               edgecolors='white', linewidths=0.5)
ax.set_xlabel('Golay Codeword Address', color='white', fontsize=9)
ax.set_ylabel('Mean NRCI', color='white', fontsize=9)
ax.set_title('Golay Address vs NRCI', color='white', fontsize=10, fontweight='bold')
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

# 2f: Prime density vs geometric complexity
ax = axes[1, 2]
ax.set_facecolor('#161b22')
for i in range(total):
    ax.scatter(prime_density[i], geo_complexity[i],
               color=domain_colors[domains[i]], s=70, alpha=0.85,
               edgecolors='white', linewidths=0.5)
ax.set_xlabel('Prime Density', color='white', fontsize=9)
ax.set_ylabel('Geometric Complexity', color='white', fontsize=9)
ax.set_title('Prime Density vs Geometric Complexity', color='white', fontsize=10, fontweight='bold')
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

legend_patches = [mpatches.Patch(color=c, label=d) for d, c in domain_colors.items()]
fig2.legend(handles=legend_patches, loc='lower center', ncol=4,
            fontsize=9, framealpha=0.3, labelcolor='white', facecolor='#0d1117',
            bbox_to_anchor=(0.5, 0.01))

plt.savefig(os.path.join(PLOTS_DIR, 'ubp_sovereign_analysis.png'),
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: ubp_sovereign_analysis.png")

# ─── PLOT 3: NRCI SPECTRUM — ALL PROBLEMS ────────────────────────────────────

fig3, ax = plt.subplots(figsize=(16, 6))
fig3.patch.set_facecolor('#0d1117')
ax.set_facecolor('#161b22')

x = np.arange(total)
bar_colors_nrci = [domain_colors[d] for d in domains]
bars = ax.bar(x, nrci_vals, color=bar_colors_nrci, alpha=0.85, edgecolor='none', width=0.7)

# Overlay correctness markers
for i, (nrci, label) in enumerate(zip(nrci_vals, correctness_labels)):
    marker = '★' if label == 'CORRECT' else ('◐' if label == 'PARTIAL' else '✗')
    color = '#2ecc71' if label == 'CORRECT' else ('#f39c12' if label == 'PARTIAL' else '#e74c3c')
    ax.text(i, nrci + 0.005, marker, ha='center', va='bottom', fontsize=10, color=color)

# Reference lines
ax.axhline(0.7, color='#f39c12', linestyle='--', linewidth=1, alpha=0.7, label='Manifestation threshold (0.70)')
ax.axhline(np.mean(nrci_vals), color='white', linestyle=':', linewidth=1, alpha=0.7,
           label=f'Mean NRCI ({np.mean(nrci_vals):.4f})')

ax.set_xticks(x)
ax.set_xticklabels(problem_ids, rotation=45, ha='right', color='white', fontsize=8)
ax.set_ylabel('Mean NRCI (Normalised Resonance Coherence Index)', color='white', fontsize=10)
ax.set_title('UBP NRCI Spectrum — All 20 MathNet Problems\n'
             '★=CORRECT  ◐=PARTIAL  ✗=INCORRECT',
             color='white', fontsize=12, fontweight='bold')
ax.tick_params(colors='white', labelsize=8)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444')

legend_patches = [mpatches.Patch(color=c, label=d) for d, c in domain_colors.items()]
ax.legend(handles=legend_patches + [
    mpatches.Patch(color='#f39c12', label='Manifest threshold'),
    mpatches.Patch(color='white', label=f'Mean NRCI={np.mean(nrci_vals):.4f}')
], fontsize=8, framealpha=0.3, labelcolor='white', facecolor='#0d1117', loc='upper right')

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'ubp_nrci_spectrum.png'),
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: ubp_nrci_spectrum.png")

# ─── PLOT 4: DOMAIN PERFORMANCE RADAR ────────────────────────────────────────

fig4 = plt.figure(figsize=(12, 8))
fig4.patch.set_facecolor('#0d1117')
fig4.suptitle('UBP × MathNet — Domain Performance Radar',
              fontsize=13, fontweight='bold', color='white')

categories = ['NRCI', 'SOC\n(norm)', 'Coherence', 'Alignment', 'Sem.Res.', 'Correct\n(adj)']
N = len(categories)
angles = [n / float(N) * 2 * math.pi for n in range(N)]
angles += angles[:1]

ax_radar = fig4.add_subplot(111, polar=True)
ax_radar.set_facecolor('#161b22')
ax_radar.spines['polar'].set_color('#444')

for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    d_nrci = np.mean([nrci_vals[i] for i in idx])
    d_soc_norm = np.mean([min(1.0, soc_vals[i] / max(soc_vals)) for i in idx])
    d_coh = np.mean([coherence_vals[i] for i in idx])
    d_align = np.mean([alignment_vals[i] for i in idx])
    d_semres = np.mean([min(1.0, semantic_res[i]) for i in idx])
    d_corr = sum(1 for i in idx if correctness_labels[i] == "CORRECT")
    d_part = sum(1 for i in idx if correctness_labels[i] == "PARTIAL")
    d_corr_adj = (d_corr + 0.5 * d_part) / len(idx)

    values = [d_nrci, d_soc_norm, d_coh, d_align, d_semres, d_corr_adj]
    values += values[:1]

    ax_radar.plot(angles, values, color=domain_colors[dom], linewidth=2, alpha=0.9)
    ax_radar.fill(angles, values, color=domain_colors[dom], alpha=0.15)

ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(categories, color='white', fontsize=9)
ax_radar.set_ylim(0, 1)
ax_radar.tick_params(colors='white', labelsize=8)
ax_radar.yaxis.set_tick_params(labelcolor='#888')
ax_radar.grid(color='#444', linewidth=0.5)

legend_patches = [mpatches.Patch(color=c, label=d) for d, c in domain_colors.items()]
ax_radar.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(1.3, 1.1),
                fontsize=9, framealpha=0.3, labelcolor='white', facecolor='#0d1117')

plt.savefig(os.path.join(PLOTS_DIR, 'ubp_domain_radar.png'),
            dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Saved: ubp_domain_radar.png")

# ─── GENERATE SUMMARY JSON ───────────────────────────────────────────────────

summary = {
    "system": meta["system"],
    "benchmark": meta["benchmark"],
    "date": meta["date"],
    "total_problems": total,
    "correctness": {
        "correct": correct,
        "partial": partial,
        "incorrect": incorrect,
        "correct_pct": round(100 * correct / total, 1),
        "partial_pct": round(100 * partial / total, 1),
        "incorrect_pct": round(100 * incorrect / total, 1),
        "adjusted_score_pct": round(100 * (correct + 0.5 * partial) / total, 1)
    },
    "ubp_metrics": {
        "mean_nrci": round(float(np.mean(nrci_vals)), 4),
        "std_nrci": round(float(np.std(nrci_vals)), 4),
        "mean_soc_mcu": round(float(np.mean(soc_vals)), 2),
        "mean_coherence": round(float(np.mean(coherence_vals)), 4),
        "mean_alignment": round(float(np.mean(alignment_vals)), 4),
        "mean_semantic_resonance": round(float(np.mean(semantic_res)), 4),
        "mean_ubp_confidence": round(float(np.mean(ubp_conf)), 4),
        "mean_prime_density": round(float(np.mean(prime_density)), 4),
        "mean_geometric_complexity": round(float(np.mean(geo_complexity)), 4),
        "manifestation_distribution": dict(manif_counts)
    },
    "per_domain": {}
}

for dom in domain_set:
    idx = [i for i, d in enumerate(domains) if d == dom]
    d_corr = sum(1 for i in idx if correctness_labels[i] == "CORRECT")
    d_part = sum(1 for i in idx if correctness_labels[i] == "PARTIAL")
    summary["per_domain"][dom] = {
        "n": len(idx),
        "mean_nrci": round(float(np.mean([nrci_vals[i] for i in idx])), 4),
        "mean_soc_mcu": round(float(np.mean([soc_vals[i] for i in idx])), 2),
        "mean_coherence": round(float(np.mean([coherence_vals[i] for i in idx])), 4),
        "correct": d_corr,
        "partial": d_part,
        "incorrect": len(idx) - d_corr - d_part,
        "adjusted_score_pct": round(100 * (d_corr + 0.5 * d_part) / len(idx), 1)
    }

summary_path = os.path.join(BASE, "results", "ubp_mathnet_summary.json")
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"\nSaved summary to {summary_path}")
print("\nAnalysis complete. All plots saved to:", PLOTS_DIR)
