"""
UBP × MathNet v2.0 — Comprehensive Analysis and Visualisation
Compares v1 vs v2 performance, analyses all new metrics, generates publication-quality plots.
"""

import json
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict

BASE = "/home/ubuntu/ubp_mathnet_investigation"
RESULTS_DIR = os.path.join(BASE, "results")
PLOTS_DIR = os.path.join(BASE, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with open(os.path.join(RESULTS_DIR, "ubp_mathnet_results.json")) as f:
    v1_data = json.load(f)
with open(os.path.join(RESULTS_DIR, "ubp_mathnet_results_v2.json")) as f:
    v2_data = json.load(f)

v1_results = v1_data["results"]
v2_results = v2_data["results"]

# ─── COLOUR PALETTE ──────────────────────────────────────────────────────────
DOMAIN_COLOURS = {
    "Number Theory": "#2196F3",
    "Algebra": "#4CAF50",
    "Geometry": "#FF9800",
    "Combinatorics": "#9C27B0"
}
GRADE_COLOURS = {"CORRECT": "#4CAF50", "PARTIAL": "#FF9800", "INCORRECT": "#F44336"}
UBP_DARK = "#1a1a2e"
UBP_MID = "#16213e"
UBP_ACCENT = "#0f3460"
UBP_GOLD = "#e94560"

plt.rcParams.update({
    'figure.facecolor': UBP_DARK,
    'axes.facecolor': UBP_MID,
    'axes.edgecolor': '#444466',
    'axes.labelcolor': '#ccccee',
    'xtick.color': '#aaaacc',
    'ytick.color': '#aaaacc',
    'text.color': '#ccccee',
    'grid.color': '#333355',
    'grid.alpha': 0.5,
    'font.family': 'monospace',
    'font.size': 10
})

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def get_v1_metrics(results):
    metrics = []
    for r in results:
        mc = r.get("math_column", r.get("math_col", {}))
        sc = r.get("sovereign_column", r.get("sovereign_col", {}))
        lc = r.get("language_column", r.get("language_col", {}))
        g = r.get("grading", {})
        metrics.append({
            "id": r["problem_id"],
            "domain": r["domain"],
            "nrci": mc.get("mean_nrci", 0),
            "soc": sc.get("soc_energy", 0),
            "alignment": g.get("alignment_score", r.get("alignment_score", 0)),
            "label": g.get("correctness_label", r.get("correctness_label", "INCORRECT")),
            "score": g.get("correctness_score", r.get("correctness_score", 0)),
        })
    return metrics

def get_v2_metrics(results):
    metrics = []
    for r in results:
        mc = r["math_column"]
        sc = r["sovereign_column"]
        lc = r["language_column"]
        g = r["grading"]
        metrics.append({
            "id": r["problem_id"],
            "domain": r["domain"],
            "nrci": mc["mean_nrci"],
            "tgic": mc["mean_tgic_stability"],
            "bw256": mc["bw256_macro_nrci"],
            "prime_density": mc["prime_density"],
            "soc": sc["soc_energy"],
            "tgic_total": sc["tgic_total_stability"],
            "rune_xy": sc["rune_xy_tax"],
            "rune_xz": sc["rune_xz_tax"],
            "rune_yz": sc["rune_yz_tax"],
            "convergence": g["tct_convergence"],
            "alignment": g["alignment_score"],
            "ubp_conf": g["ubp_confidence"],
            "label": g["correctness_label"],
            "score": g["correctness_score"],
            "brain_uid": lc["brain_result_uid"],
            "ontology": lc["ontology_class"],
            "code_ok": lc["code_verified"],
            "attempts": lc["attempts"],
            "self_corr": lc["self_correction_applied"],
        })
    return metrics

v1m = get_v1_metrics(v1_results)
v2m = get_v2_metrics(v2_results)

# ─── FIGURE 1: V1 vs V2 PERFORMANCE COMPARISON ───────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("UBP × MathNet: v1.0 vs v2.0 Performance Comparison", 
             fontsize=14, fontweight='bold', color='#eeeeff', y=1.02)

# 1a: Grade distribution
for ax, data, title in zip(axes, [v1m, v2m], ["v1.0 (Baseline)", "v2.0 (Full System)"]):
    counts = defaultdict(int)
    for m in data:
        counts[m["label"]] += 1
    labels = ["CORRECT", "PARTIAL", "INCORRECT"]
    vals = [counts[l] for l in labels]
    colours = [GRADE_COLOURS[l] for l in labels]
    bars = ax.bar(labels, vals, color=colours, alpha=0.85, edgecolor='#ffffff33', linewidth=1.2)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                str(val), ha='center', va='bottom', fontweight='bold', fontsize=12, color='white')
    ax.set_title(title, fontsize=12, fontweight='bold', color='#eeeeff', pad=10)
    ax.set_ylabel("Problems", color='#aaaacc')
    ax.set_ylim(0, 22)
    ax.grid(axis='y', alpha=0.3)
    total = len(data)
    adj = 100 * (counts["CORRECT"] + 0.5 * counts["PARTIAL"]) / total
    ax.text(0.5, 0.92, f"Adj Score: {adj:.1f}%", transform=ax.transAxes,
            ha='center', fontsize=11, color=UBP_GOLD, fontweight='bold')

# 1c: Adjusted score comparison bar
ax3 = axes[2]
versions = ["v1.0\n(Baseline)", "v2.0\n(Full System)"]
adj_scores = []
for data in [v1m, v2m]:
    counts = defaultdict(int)
    for m in data:
        counts[m["label"]] += 1
    total = len(data)
    adj_scores.append(100 * (counts["CORRECT"] + 0.5 * counts["PARTIAL"]) / total)

bars = ax3.bar(versions, adj_scores, color=["#5588aa", "#44bb88"], alpha=0.9,
               edgecolor='#ffffff44', linewidth=1.5, width=0.5)
for bar, val in zip(bars, adj_scores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{val:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=14, color='white')
ax3.set_title("Adjusted Score Comparison", fontsize=12, fontweight='bold', color='#eeeeff', pad=10)
ax3.set_ylabel("Adjusted Score (%)", color='#aaaacc')
ax3.set_ylim(0, 80)
ax3.axhline(y=adj_scores[0], color='#5588aa', linestyle='--', alpha=0.5, linewidth=1)
ax3.grid(axis='y', alpha=0.3)
delta = adj_scores[1] - adj_scores[0]
ax3.text(0.5, 0.85, f"Δ = +{delta:.1f}%", transform=ax3.transAxes,
         ha='center', fontsize=12, color='#88ff88', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig1_v1_v2_comparison.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 1 saved.")

# ─── FIGURE 2: V2 NEW METRICS DASHBOARD ──────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle("UBP v2.0 — New Metrics Dashboard (TGIC, BW256, Brain, Convergence)", 
             fontsize=14, fontweight='bold', color='#eeeeff')

domains = list(DOMAIN_COLOURS.keys())
domain_data = {d: [m for m in v2m if m["domain"] == d] for d in domains}

# 2a: NRCI vs TGIC scatter
ax = axes[0, 0]
for d, colour in DOMAIN_COLOURS.items():
    pts = domain_data[d]
    ax.scatter([m["nrci"] for m in pts], [m["tgic"] for m in pts],
               c=colour, s=120, alpha=0.85, label=d, edgecolors='white', linewidth=0.8, zorder=5)
    for m in pts:
        ax.annotate(m["id"].split("_")[-1], (m["nrci"], m["tgic"]),
                    fontsize=6, color='#cccccc', ha='center', va='bottom')
ax.set_xlabel("Mean NRCI (Golay Coherence)")
ax.set_ylabel("Mean TGIC Stability (3-6-9 Audit)")
ax.set_title("NRCI vs TGIC Stability", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=8, framealpha=0.3)
ax.grid(True, alpha=0.3)

# 2b: TCT Convergence by domain
ax = axes[0, 1]
for i, (d, colour) in enumerate(DOMAIN_COLOURS.items()):
    pts = domain_data[d]
    convs = [m["convergence"] for m in pts]
    ax.bar([i + j*0.18 for j in range(len(convs))], convs,
           width=0.16, color=colour, alpha=0.8, label=d if i == 0 else "")
    ax.scatter([i + j*0.18 for j in range(len(convs))], convs,
               c='white', s=20, zorder=5, alpha=0.7)
ax.set_xticks(range(len(domains)))
ax.set_xticklabels([d[:4] for d in domains])
ax.set_ylabel("TCT Convergence Score")
ax.set_title("TCT Convergence by Domain", fontweight='bold', color='#eeeeff')
ax.set_ylim(0.85, 0.95)
ax.grid(axis='y', alpha=0.3)
avg_conv = sum(m["convergence"] for m in v2m) / len(v2m)
ax.axhline(y=avg_conv, color=UBP_GOLD, linestyle='--', linewidth=1.5, label=f"Mean={avg_conv:.3f}")
ax.legend(fontsize=8, framealpha=0.3)

# 2c: BW256 Macro NRCI distribution
ax = axes[0, 2]
bw_vals = [m["bw256"] for m in v2m]
colours_list = [DOMAIN_COLOURS[m["domain"]] for m in v2m]
ids = [m["id"].replace("MN_", "").replace("_00", "_") for m in v2m]
bars = ax.barh(ids, bw_vals, color=colours_list, alpha=0.8, edgecolor='#ffffff22')
ax.axvline(x=sum(bw_vals)/len(bw_vals), color=UBP_GOLD, linestyle='--', linewidth=1.5,
           label=f"Mean={sum(bw_vals)/len(bw_vals):.4f}")
ax.set_xlabel("BW256 Macro NRCI")
ax.set_title("Barnes-Wall 256D Macro Coherence", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=8, framealpha=0.3)
ax.grid(axis='x', alpha=0.3)

# 2d: RuneCube face taxes (XY/XZ/YZ)
ax = axes[1, 0]
x = np.arange(len(v2m))
width = 0.28
xy_taxes = [m["rune_xy"] for m in v2m]
xz_taxes = [m["rune_xz"] for m in v2m]
yz_taxes = [m["rune_yz"] for m in v2m]
ax.bar(x - width, xy_taxes, width, label="XY face", color="#2196F3", alpha=0.8)
ax.bar(x, xz_taxes, width, label="XZ face", color="#4CAF50", alpha=0.8)
ax.bar(x + width, yz_taxes, width, label="YZ face", color="#FF9800", alpha=0.8)
ax.set_xlabel("Problem Index")
ax.set_ylabel("Symmetry Tax")
ax.set_title("RuneCube Face Symmetry Taxes", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=8, framealpha=0.3)
ax.grid(axis='y', alpha=0.3)

# 2e: Brain v7.2 UID distribution
ax = axes[1, 1]
brain_counts = defaultdict(int)
for m in v2m:
    uid = m["brain_uid"].split("_")[0] + "_" + m["brain_uid"].split("_")[1] if "_" in m["brain_uid"] else m["brain_uid"]
    brain_counts[uid] += 1
uids = list(brain_counts.keys())
counts = [brain_counts[u] for u in uids]
colours_b = plt.cm.Set3(np.linspace(0, 1, len(uids)))
wedges, texts, autotexts = ax.pie(counts, labels=uids, autopct='%1.0f%%',
                                   colors=colours_b, startangle=90,
                                   textprops={'fontsize': 8, 'color': '#ccccee'})
for at in autotexts:
    at.set_fontsize(8)
    at.set_color('white')
ax.set_title("UBP Brain v7.2 — Law Distribution", fontweight='bold', color='#eeeeff')

# 2f: Grade vs NRCI + Convergence bubble chart
ax = axes[1, 2]
grade_map = {"CORRECT": 1.0, "PARTIAL": 0.5, "INCORRECT": 0.0}
for m in v2m:
    colour = GRADE_COLOURS[m["label"]]
    size = 200 + 400 * m["convergence"]
    ax.scatter(m["nrci"], m["ubp_conf"], s=size, c=colour, alpha=0.7,
               edgecolors='white', linewidth=0.8, zorder=5)
    ax.annotate(m["id"].replace("MN_", "")[:8], (m["nrci"], m["ubp_conf"]),
                fontsize=6, color='#cccccc', ha='center', va='bottom')
ax.set_xlabel("Mean NRCI")
ax.set_ylabel("UBP Confidence")
ax.set_title("Grade vs NRCI + Confidence\n(bubble size = TCT Convergence)",
             fontweight='bold', color='#eeeeff')
patches = [mpatches.Patch(color=GRADE_COLOURS[l], label=l) for l in ["CORRECT", "PARTIAL", "INCORRECT"]]
ax.legend(handles=patches, fontsize=8, framealpha=0.3)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig2_v2_metrics_dashboard.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 2 saved.")

# ─── FIGURE 3: DOMAIN-LEVEL DEEP DIVE ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("UBP v2.0 — Domain-Level Analysis", fontsize=14, fontweight='bold', color='#eeeeff')

metric_keys = ["nrci", "tgic", "bw256", "convergence", "alignment", "ubp_conf"]
metric_labels = ["NRCI", "TGIC", "BW256", "Convergence", "Alignment", "UBP Conf"]

for ax, (domain, colour) in zip(axes.flat, DOMAIN_COLOURS.items()):
    pts = domain_data[domain]
    ids = [m["id"].split("_")[-1] for m in pts]
    x = np.arange(len(metric_keys))
    
    for i, m in enumerate(pts):
        vals = [m[k] for k in metric_keys]
        ax.plot(x, vals, 'o-', color=colour, alpha=0.5 + 0.1*i, linewidth=1.5,
                markersize=6, label=m["id"].replace("MN_", ""))
    
    # Mean line
    means = [sum(m[k] for m in pts)/len(pts) for k in metric_keys]
    ax.plot(x, means, 's--', color='white', alpha=0.9, linewidth=2.5,
            markersize=8, label="Mean", zorder=10)
    
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.set_title(f"{domain}", fontweight='bold', color=colour, fontsize=12)
    ax.legend(fontsize=7, framealpha=0.3, loc='lower right')
    ax.grid(True, alpha=0.3)
    
    # Annotate grade for each problem
    for i, m in enumerate(pts):
        label_colour = GRADE_COLOURS[m["label"]]
        ax.text(x[-1] + 0.15, [m[k] for k in metric_keys][-1],
                m["label"][:1], fontsize=8, color=label_colour, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig3_domain_deep_dive.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 3 saved.")

# ─── FIGURE 4: V1 vs V2 METRIC EVOLUTION ─────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("UBP × MathNet: Metric Evolution v1.0 → v2.0", 
             fontsize=14, fontweight='bold', color='#eeeeff')

# 4a: NRCI comparison
ax = axes[0]
v1_nrci = [m["nrci"] for m in v1m]
v2_nrci = [m["nrci"] for m in v2m]
x = np.arange(len(v1_nrci))
ax.plot(x, v1_nrci, 'o--', color='#5588aa', alpha=0.8, label="v1.0 NRCI", linewidth=1.5)
ax.plot(x, v2_nrci, 's-', color='#44bb88', alpha=0.9, label="v2.0 NRCI", linewidth=2)
ax.axhline(y=sum(v1_nrci)/len(v1_nrci), color='#5588aa', linestyle=':', alpha=0.6)
ax.axhline(y=sum(v2_nrci)/len(v2_nrci), color='#44bb88', linestyle=':', alpha=0.6)
ax.set_xlabel("Problem Index")
ax.set_ylabel("Mean NRCI")
ax.set_title("NRCI: v1 vs v2", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=9, framealpha=0.3)
ax.grid(True, alpha=0.3)

# 4b: Alignment vs Convergence
ax = axes[1]
v1_align = [m["alignment"] for m in v1m]
v2_align = [m["alignment"] for m in v2m]
v2_conv = [m["convergence"] for m in v2m]
ax.plot(x, v1_align, 'o--', color='#5588aa', alpha=0.8, label="v1.0 Alignment", linewidth=1.5)
ax.plot(x, v2_align, 's-', color='#44bb88', alpha=0.9, label="v2.0 Alignment", linewidth=2)
ax.plot(x, v2_conv, '^-', color=UBP_GOLD, alpha=0.9, label="v2.0 Convergence", linewidth=2)
ax.set_xlabel("Problem Index")
ax.set_ylabel("Score")
ax.set_title("Alignment & Convergence", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=9, framealpha=0.3)
ax.grid(True, alpha=0.3)

# 4c: SOC Energy comparison
ax = axes[2]
v1_soc = [m["soc"]/1e6 for m in v1m]
v2_soc = [m["soc"]/1e6 for m in v2m]
ax.fill_between(x, v1_soc, alpha=0.3, color='#5588aa', label="v1.0 SOC")
ax.fill_between(x, v2_soc, alpha=0.3, color='#44bb88', label="v2.0 SOC")
ax.plot(x, v1_soc, 'o--', color='#5588aa', alpha=0.8, linewidth=1.5)
ax.plot(x, v2_soc, 's-', color='#44bb88', alpha=0.9, linewidth=2)
ax.set_xlabel("Problem Index")
ax.set_ylabel("SOC Energy (MCU)")
ax.set_title("SOC Energy: v1 vs v2", fontweight='bold', color='#eeeeff')
ax.legend(fontsize=9, framealpha=0.3)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig4_metric_evolution.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 4 saved.")

# ─── FIGURE 5: TGIC 3-6-9 STABILITY HEATMAP ──────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 8))
fig.suptitle("UBP v2.0 — TGIC 3-6-9 Stability Scores per Problem × Key Number",
             fontsize=13, fontweight='bold', color='#eeeeff')

# Build matrix: problems × key numbers (up to 6)
max_nums = 6
matrix = []
problem_ids = []
for r in v2_results:
    mc = r["math_column"]
    tgic_scores = mc.get("tgic_stability_scores", [0.5]*max_nums)
    row = tgic_scores[:max_nums] + [None] * (max_nums - len(tgic_scores[:max_nums]))
    matrix.append(row)
    problem_ids.append(r["problem_id"].replace("MN_", ""))

matrix_np = np.array([[v if v is not None else np.nan for v in row] for row in matrix])

im = ax.imshow(matrix_np, cmap='RdYlGn', aspect='auto', vmin=0.4, vmax=1.0)
ax.set_yticks(range(len(problem_ids)))
ax.set_yticklabels(problem_ids, fontsize=8)
ax.set_xticks(range(max_nums))
ax.set_xticklabels([f"Key #{i+1}" for i in range(max_nums)], fontsize=9)
ax.set_xlabel("Key Number Index")
ax.set_ylabel("Problem")
ax.set_title("TGIC 3-6-9 Stability (green=stable, red=unstable)", 
             fontsize=11, color='#aaaacc', pad=8)

# Annotate cells
for i in range(len(problem_ids)):
    for j in range(max_nums):
        val = matrix_np[i, j]
        if not np.isnan(val):
            ax.text(j, i, f"{val:.2f}", ha='center', va='center',
                    fontsize=7, color='black' if val > 0.7 else 'white', fontweight='bold')

plt.colorbar(im, ax=ax, label="TGIC Stability Score", shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig5_tgic_heatmap.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 5 saved.")

# ─── FIGURE 6: SYSTEM ARCHITECTURE DIAGRAM ───────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor(UBP_DARK)
ax.set_facecolor(UBP_DARK)
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title("UBP Swarm TCT MathNet v2.0 — Full System Architecture",
             fontsize=14, fontweight='bold', color='#eeeeff', pad=15)

def draw_box(ax, x, y, w, h, label, sublabel, colour, fontsize=9):
    rect = plt.Rectangle((x, y), w, h, facecolor=colour, edgecolor='#ffffff55',
                          linewidth=1.5, alpha=0.85, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color='white', zorder=4)
    ax.text(x + w/2, y + h*0.25, sublabel, ha='center', va='center',
            fontsize=7, color='#ccccdd', zorder=4, style='italic')

def draw_arrow(ax, x1, y1, x2, y2, colour='#888899'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=colour, lw=1.5), zorder=2)

# Input
draw_box(ax, 7.5, 8.5, 3, 1.2, "MathNet Problem", "20 Olympiad Problems\n(NT/Alg/Geo/Comb)", "#37474F", fontsize=10)

# Column 1
draw_box(ax, 0.3, 5.5, 4.5, 2.5, "COLUMN 1\nMath Architect v2", 
         "EML ALU + TGIC 3-6-9\nBW256 Macro Coherence\nAnalog EM Verification\nPrime Factorisation", "#1565C0")

# Column 2
draw_box(ax, 6.75, 5.5, 4.5, 2.5, "COLUMN 2\nSovereign Physicist v2",
         "Golay Snap + Leech Lattice\nRuneCube XY/XZ/YZ Taxes\nOffBit Phase Tracking\nTGIC Total Stability", "#1B5E20")

# Column 3
draw_box(ax, 13.2, 5.5, 4.5, 2.5, "COLUMN 3\nLanguage Scribe v2",
         "UBP Brain v7.2 (ID Lock)\nPython Code Generator\nAnalog Arithmetic Check\nLLM + Self-Correction", "#4A148C")

# Arrows from input to columns
draw_arrow(ax, 9, 8.5, 2.55, 8.0)
draw_arrow(ax, 9, 8.5, 9, 8.0)
draw_arrow(ax, 9, 8.5, 15.45, 8.0)

# Sub-engines
engines = [
    (0.5, 3.2, 1.8, 1.8, "GOLAY\nENGINE", "4096 codewords", "#0D47A1"),
    (2.5, 3.2, 1.8, 1.8, "LEECH\nLATTICE", "Λ₂₄ symmetry", "#0D47A1"),
    (4.5, 3.2, 1.8, 1.8, "EML ALU\nSOVEREIGN", "Exact arithmetic", "#0D47A1"),
    (6.5, 3.2, 1.8, 1.8, "TGIC\nENGINE", "3-6-9 audit", "#1B5E20"),
    (8.5, 3.2, 1.8, 1.8, "BW256\nENGINE", "256D macro", "#1B5E20"),
    (10.5, 3.2, 1.8, 1.8, "OBSERVER\nDYNAMICS", "SOC energy", "#1B5E20"),
    (12.5, 3.2, 1.8, 1.8, "UBP BRAIN\nv7.2", "ID Lock", "#4A148C"),
    (14.5, 3.2, 1.8, 1.8, "PYTHON\nCODE GEN", "Exec verify", "#4A148C"),
    (16.5, 3.2, 1.8, 1.8, "ANALOG\nEM SUITE", "EM compute", "#4A148C"),
]
for ex, ey, ew, eh, el, esl, ec in engines:
    draw_box(ax, ex, ey, ew, eh, el, esl, ec, fontsize=8)

# TCT Auditor
draw_box(ax, 6.75, 1.0, 4.5, 1.8, "TCT AUDITOR v2",
         "Alignment + Convergence\nGrader + Self-Correction", "#B71C1C", fontsize=10)

# Output
draw_box(ax, 7.0, -0.2, 4.0, 1.0, "RESULTS", "JSON + Plots + Paper", "#37474F", fontsize=10)

# Stats overlay
stats_text = (
    "v2.0 RESULTS:\n"
    "CORRECT: 4/20 (20%)\n"
    "PARTIAL: 16/20 (80%)\n"
    "Adj Score: 60.0%\n"
    "Avg NRCI: 0.6962\n"
    "Avg TGIC: 0.644\n"
    "Avg Conv: 0.920\n"
    "Code OK: 20/20"
)
ax.text(16.5, 1.5, stats_text, fontsize=8, color='#aaffaa',
        va='top', ha='left', family='monospace',
        bbox=dict(boxstyle='round', facecolor='#1a2a1a', alpha=0.8, edgecolor='#44aa44'))

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "fig6_system_architecture.png"), dpi=150, bbox_inches='tight',
            facecolor=UBP_DARK)
plt.close()
print("Fig 6 saved.")

# ─── SUMMARY STATISTICS ───────────────────────────────────────────────────────
print("\n" + "="*70)
print("COMPREHENSIVE ANALYSIS SUMMARY")
print("="*70)

v1_counts = defaultdict(int)
v2_counts = defaultdict(int)
for m in v1m: v1_counts[m["label"]] += 1
for m in v2m: v2_counts[m["label"]] += 1

total = len(v2m)
print(f"\nV1 → V2 Performance:")
print(f"  CORRECT:   {v1_counts['CORRECT']}/20 ({100*v1_counts['CORRECT']/20:.1f}%) → {v2_counts['CORRECT']}/20 ({100*v2_counts['CORRECT']/20:.1f}%)")
print(f"  PARTIAL:   {v1_counts['PARTIAL']}/20 ({100*v1_counts['PARTIAL']/20:.1f}%) → {v2_counts['PARTIAL']}/20 ({100*v2_counts['PARTIAL']/20:.1f}%)")
print(f"  INCORRECT: {v1_counts['INCORRECT']}/20 ({100*v1_counts['INCORRECT']/20:.1f}%) → {v2_counts['INCORRECT']}/20 ({100*v2_counts['INCORRECT']/20:.1f}%)")
v1_adj = 100*(v1_counts['CORRECT']+0.5*v1_counts['PARTIAL'])/20
v2_adj = 100*(v2_counts['CORRECT']+0.5*v2_counts['PARTIAL'])/20
print(f"  Adj Score: {v1_adj:.1f}% → {v2_adj:.1f}% (Δ = +{v2_adj-v1_adj:.1f}%)")

print(f"\nV2 New Metrics:")
print(f"  Avg NRCI:        {sum(m['nrci'] for m in v2m)/total:.4f}")
print(f"  Avg TGIC:        {sum(m['tgic'] for m in v2m)/total:.4f}")
print(f"  Avg BW256:       {sum(m['bw256'] for m in v2m)/total:.4f}")
print(f"  Avg Convergence: {sum(m['convergence'] for m in v2m)/total:.4f}")
print(f"  Avg Alignment:   {sum(m['alignment'] for m in v2m)/total:.4f}")
print(f"  Code Verified:   {sum(1 for m in v2m if m['code_ok'])}/20")
print(f"  Self-Corrected:  {sum(1 for m in v2m if m['self_corr'])}/20")

print(f"\nDomain Breakdown (v2):")
for d in domains:
    pts = domain_data[d]
    counts = defaultdict(int)
    for m in pts: counts[m["label"]] += 1
    adj = 100*(counts['CORRECT']+0.5*counts['PARTIAL'])/len(pts)
    print(f"  {d:<16}: NRCI={sum(m['nrci'] for m in pts)/len(pts):.4f} "
          f"TGIC={sum(m['tgic'] for m in pts)/len(pts):.3f} "
          f"Conv={sum(m['convergence'] for m in pts)/len(pts):.3f} "
          f"Adj={adj:.1f}%")

# Save summary JSON
summary = {
    "v1": {"correct": v1_counts['CORRECT'], "partial": v1_counts['PARTIAL'],
            "incorrect": v1_counts['INCORRECT'], "adj_score": v1_adj,
            "avg_nrci": sum(m['nrci'] for m in v1m)/len(v1m),
            "avg_alignment": sum(m['alignment'] for m in v1m)/len(v1m)},
    "v2": {"correct": v2_counts['CORRECT'], "partial": v2_counts['PARTIAL'],
            "incorrect": v2_counts['INCORRECT'], "adj_score": v2_adj,
            "avg_nrci": sum(m['nrci'] for m in v2m)/total,
            "avg_tgic": sum(m['tgic'] for m in v2m)/total,
            "avg_bw256": sum(m['bw256'] for m in v2m)/total,
            "avg_convergence": sum(m['convergence'] for m in v2m)/total,
            "avg_alignment": sum(m['alignment'] for m in v2m)/total,
            "code_verified": sum(1 for m in v2m if m['code_ok']),
            "self_corrected": sum(1 for m in v2m if m['self_corr'])},
    "delta": {"adj_score": v2_adj - v1_adj,
              "correct": v2_counts['CORRECT'] - v1_counts['CORRECT']}
}
with open(os.path.join(RESULTS_DIR, "ubp_mathnet_summary_v2.json"), 'w') as f:
    json.dump(summary, f, indent=2)
print("\nSummary saved.")
print("All 6 figures saved to:", PLOTS_DIR)
