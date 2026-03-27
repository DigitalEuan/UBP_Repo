"""
UBP Nuclear Physics – Figure Generation
========================================
Generates publication-quality figures for the research paper.
"""

import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from pathlib import Path

SESSION   = Path("/app/sandbox/session_20260327_124022_fb146e883394")
DATA_DIR  = SESSION / "data"
RESULTS_DIR = SESSION / "results"
FIGURES_DIR = SESSION / "figures"
FIGURES_DIR.mkdir(exist_ok=True)
USER_DATA = SESSION / "user_data"
sys.path.insert(0, str(USER_DATA))

# Publication style
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

COLORS = {
    "ubp_blue":    "#1a6faf",
    "stable":      "#2ca02c",
    "unstable":    "#d62728",
    "magic":       "#ff7f0e",
    "highlight":   "#9467bd",
    "iron":        "#8c564b",
    "phase_lock":  "#17becf",
    "light_gray":  "#e0e0e0",
    "dark_gray":   "#555555",
}

df = pd.read_csv(DATA_DIR / "ubp_vs_experiment.csv")
with open(RESULTS_DIR / "ubp_nuclear_deep_dive.json") as f:
    deep = json.load(f)

# ── Figure 1: Overview – NRCI across the periodic table ──────────────────
print("[Fig 1] NRCI across the periodic table + BE/A overlay...")
MAGIC_Z = [2, 8, 20, 28, 50, 82]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

# Top: NRCI
colors = [COLORS["stable"] if row["is_stable"] else COLORS["unstable"]
          for _, row in df.iterrows()]
ax1.bar(df["Z"], df["nrci_score"], color=colors, alpha=0.7, width=0.8)
for z in MAGIC_Z:
    ax1.axvline(z, color=COLORS["magic"], linestyle="--", linewidth=0.8, alpha=0.8)
ax1.axhline(0.60, color=COLORS["dark_gray"], linestyle=":", linewidth=0.7, label="Phase-Lock lower bound")
ax1.axhline(0.70, color=COLORS["dark_gray"], linestyle="-.", linewidth=0.7, label="Phase-Lock upper bound")
ax1.set_ylabel("UBP NRCI Score")
ax1.set_title("UBP Non-Recursive Compositional Index (NRCI) across the Chart of Nuclides")
ax1.set_ylim(0.54, 0.72)
ax1.legend(loc="upper right", framealpha=0.8)
stable_patch   = mpatches.Patch(color=COLORS["stable"],   label="Stable element")
unstable_patch = mpatches.Patch(color=COLORS["unstable"], label="Radioactive element")
magic_line     = mpatches.Patch(color=COLORS["magic"],    label="Magic proton number", alpha=0.7)
ax1.legend(handles=[stable_patch, unstable_patch, magic_line,
                     mpatches.Patch(color=COLORS["dark_gray"], label="Phase-Lock band [0.60–0.70]")],
           loc="upper right", framealpha=0.85)

# Bottom: BE/A
ax2.plot(df["Z"], df["be_per_A_semi"], color=COLORS["ubp_blue"],
         linewidth=1.5, label="BE/A (semi-empirical AME2020)")
ax2.fill_between(df["Z"], df["be_per_A_semi"],
                  alpha=0.15, color=COLORS["ubp_blue"])
for z in MAGIC_Z:
    ax2.axvline(z, color=COLORS["magic"], linestyle="--", linewidth=0.8, alpha=0.8)
ax2.axvline(26, color=COLORS["iron"], linestyle="-", linewidth=1.0, alpha=0.7)
ax2.text(27, 2.5, "Fe-56\n(iron peak)", fontsize=7, color=COLORS["iron"])
ax2.set_xlabel("Atomic Number (Z)")
ax2.set_ylabel("Binding Energy / Nucleon (MeV/A)")
ax2.set_title("Nuclear Binding Energy per Nucleon (Bethe-Weizsäcker Semi-empirical)")
ax2.legend(loc="lower right")

for ax in [ax1, ax2]:
    for z in MAGIC_Z:
        ax.text(z, ax.get_ylim()[0], str(z), fontsize=6,
                color=COLORS["magic"], ha="center", va="bottom", rotation=0)

plt.tight_layout(h_pad=0.5)
plt.savefig(FIGURES_DIR / "fig1_nrci_periodic_table.png")
plt.close()
print("  Saved figures/fig1_nrci_periodic_table.png")

# ── Figure 2: NRCI vs BE/A scatter with regression ───────────────────────
print("[Fig 2] NRCI vs BE/A scatter...")
from scipy import stats

fig, ax = plt.subplots(1, 1, figsize=(7, 5))
stable_mask = df["is_stable"].astype(bool)

ax.scatter(df.loc[stable_mask, "nrci_score"],
           df.loc[stable_mask, "be_per_A_semi"],
           c=COLORS["stable"], s=30, alpha=0.7, label="Stable elements", zorder=3)
ax.scatter(df.loc[~stable_mask, "nrci_score"],
           df.loc[~stable_mask, "be_per_A_semi"],
           c=COLORS["unstable"], s=30, alpha=0.7, marker="^", label="Radioactive elements", zorder=3)

# Highlight magic numbers
magic_df = df[df["is_magic_Z"]]
for _, row in magic_df.iterrows():
    ax.scatter(row["nrci_score"], row["be_per_A_semi"],
               s=90, c=COLORS["magic"], alpha=0.9, zorder=5, edgecolors="black", linewidths=0.5)
    ax.annotate(row["symbol"], (row["nrci_score"], row["be_per_A_semi"]),
                fontsize=7, ha="left", va="bottom", color=COLORS["magic"],
                xytext=(3, 3), textcoords="offset points")

# Highlight Fe
fe = df[df["Z"]==26].iloc[0]
ax.scatter(fe["nrci_score"], fe["be_per_A_semi"], s=120, c=COLORS["iron"],
           zorder=6, edgecolors="black", linewidths=0.8, marker="*")
ax.annotate("Fe-56\n(iron peak)", (fe["nrci_score"], fe["be_per_A_semi"]),
            fontsize=7, ha="right", va="top", color=COLORS["iron"],
            xytext=(-5, -5), textcoords="offset points")

# Regression line
mask = df["be_per_A_semi"].notna() & df["nrci_score"].notna()
x_fit = df.loc[mask, "nrci_score"].values
y_fit = df.loc[mask, "be_per_A_semi"].values
slope, intercept, r, p, _ = stats.linregress(x_fit, y_fit)
xr = np.linspace(x_fit.min(), x_fit.max(), 100)
ax.plot(xr, slope*xr + intercept, color=COLORS["dark_gray"],
        linewidth=1.5, linestyle="--", label=f"Linear fit (r={r:.3f}, p={p:.3e})", zorder=2)

ax.set_xlabel("UBP NRCI Score")
ax.set_ylabel("BE / Nucleon (MeV/A)")
ax.set_title("UBP Geometric Stability (NRCI) vs Nuclear Binding Energy per Nucleon")
magic_patch = mpatches.Patch(color=COLORS["magic"], label="Magic-Z nuclides")
ax.legend(handles=[
    mpatches.Patch(color=COLORS["stable"], label="Stable elements"),
    mpatches.Patch(color=COLORS["unstable"], label="Radioactive elements"),
    magic_patch,
    plt.Line2D([0],[0], color=COLORS["dark_gray"], linestyle="--",
               label=f"Spearman ρ = {deep['binding_energy_analysis']['spearman_nrci_vs_BE']['rho']:.3f}")
], loc="upper right", framealpha=0.85)

spearman_rho = deep["binding_energy_analysis"]["spearman_nrci_vs_BE"]["rho"]
ax.text(0.03, 0.97,
        f"Spearman ρ = {spearman_rho:.4f}\np < 1×10⁻⁹",
        transform=ax.transAxes, fontsize=9, va="top",
        bbox=dict(boxstyle="round", fc="white", alpha=0.8))

plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig2_nrci_vs_be.png")
plt.close()
print("  Saved figures/fig2_nrci_vs_be.png")

# ── Figure 3: Magic Numbers – UBP Metric Comparison ──────────────────────
print("[Fig 3] Magic number analysis...")
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# Left: NRCI boxplot by magic status
magic_groups = {
    "Magic-Z\nnuclei": df[df["is_magic_Z"]]["nrci_score"].dropna().values,
    "Non-magic\nnuclei": df[~df["is_magic_Z"]]["nrci_score"].dropna().values,
}
ax = axes[0]
bp = ax.boxplot(list(magic_groups.values()), labels=list(magic_groups.keys()),
                patch_artist=True, notch=False)
bp["boxes"][0].set_facecolor(COLORS["magic"])
bp["boxes"][0].set_alpha(0.7)
bp["boxes"][1].set_facecolor(COLORS["ubp_blue"])
bp["boxes"][1].set_alpha(0.6)
ax.set_ylabel("UBP NRCI Score")
ax.set_title("NRCI: Magic vs Non-Magic Nuclei")
ax.text(0.97, 0.97,
        f"t = {deep['magic_number_analysis']['t_test_nrci']['t']:.3f}\n"
        f"p = {deep['magic_number_analysis']['t_test_nrci']['p']:.4f}",
        transform=ax.transAxes, fontsize=9, va="top", ha="right",
        bbox=dict(boxstyle="round", fc="white", alpha=0.8))

# Right: Symmetry Tax by magic status
tax_groups = {
    "Magic-Z\nnuclei": df[df["is_magic_Z"]]["symmetry_tax"].dropna().values,
    "Non-magic\nnuclei": df[~df["is_magic_Z"]]["symmetry_tax"].dropna().values,
}
ax = axes[1]
bp2 = ax.boxplot(list(tax_groups.values()), labels=list(tax_groups.keys()),
                  patch_artist=True, notch=False)
bp2["boxes"][0].set_facecolor(COLORS["magic"])
bp2["boxes"][0].set_alpha(0.7)
bp2["boxes"][1].set_facecolor(COLORS["ubp_blue"])
bp2["boxes"][1].set_alpha(0.6)
ax.set_ylabel("UBP Symmetry Tax")
ax.set_title("Symmetry Tax: Magic vs Non-Magic Nuclei")

# Show individual magic Z values
for z, label in zip(MAGIC_Z, ["He","O","Ca","Ni","Sn","Pb"]):
    row = df[df["Z"]==z]
    if len(row) > 0:
        ax.scatter(1, row.iloc[0]["symmetry_tax"], s=50, c=COLORS["iron"],
                   zorder=5, alpha=0.9)
        ax.annotate(label, (1, row.iloc[0]["symmetry_tax"]),
                    fontsize=6, ha="right", xytext=(-4, 0), textcoords="offset points")

plt.suptitle("UBP Geometric Analysis of Nuclear Magic Numbers (Z = 2, 8, 20, 28, 50, 82)",
             fontsize=11)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig3_magic_numbers.png")
plt.close()
print("  Saved figures/fig3_magic_numbers.png")

# ── Figure 4: Radioactive Decay – NRCI vs log10(t½) ─────────────────────
print("[Fig 4] Decay rate analysis...")
radioactive = df[~df["is_stable"] & df["log10_half_life"].notna()
                 & (df["log10_half_life"] < 100)].copy()

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Left: NRCI vs log10(half-life)
ax = axes[0]
sc = ax.scatter(radioactive["nrci_score"], radioactive["log10_half_life"],
                c=radioactive["Z"], cmap="plasma", s=60, alpha=0.8, zorder=3)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Z (Atomic Number)")
for _, row in radioactive.iterrows():
    ax.annotate(row["symbol"], (row["nrci_score"], row["log10_half_life"]),
                fontsize=6.5, ha="left", xytext=(3, 2), textcoords="offset points",
                color=COLORS["dark_gray"])

# Regression
if len(radioactive) >= 5:
    slope, intercept, r, p, _ = stats.linregress(
        radioactive["nrci_score"], radioactive["log10_half_life"])
    xr = np.linspace(radioactive["nrci_score"].min(), radioactive["nrci_score"].max(), 50)
    ax.plot(xr, slope*xr + intercept, color=COLORS["dark_gray"],
            linestyle="--", linewidth=1.5, zorder=2)
    rho = deep["decay_analysis"]["spearman_nrci_vs_log_hl"]["rho"]
    p_val = deep["decay_analysis"]["spearman_nrci_vs_log_hl"]["p"]
    ax.text(0.03, 0.97,
            f"Spearman ρ = {rho:.3f}\np = {p_val:.4f}",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round", fc="white", alpha=0.8))

ax.set_xlabel("UBP NRCI Score")
ax.set_ylabel("log₁₀(half-life / s)")
ax.set_title("UBP NRCI vs Radioactive Half-Life")

# Right: Symmetry Tax vs log10(half-life)
ax = axes[1]
sc2 = ax.scatter(radioactive["symmetry_tax"], radioactive["log10_half_life"],
                  c=radioactive["Z"], cmap="plasma", s=60, alpha=0.8, zorder=3)
plt.colorbar(sc2, ax=ax).set_label("Z (Atomic Number)")
for _, row in radioactive.iterrows():
    ax.annotate(row["symbol"], (row["symmetry_tax"], row["log10_half_life"]),
                fontsize=6.5, ha="left", xytext=(3, 2), textcoords="offset points",
                color=COLORS["dark_gray"])

if len(radioactive) >= 5:
    slope2, intercept2, r2, p2, _ = stats.linregress(
        radioactive["symmetry_tax"], radioactive["log10_half_life"])
    xr2 = np.linspace(radioactive["symmetry_tax"].min(), radioactive["symmetry_tax"].max(), 50)
    ax.plot(xr2, slope2*xr2 + intercept2, color=COLORS["dark_gray"],
            linestyle="--", linewidth=1.5, zorder=2)

ax.set_xlabel("UBP Symmetry Tax")
ax.set_ylabel("log₁₀(half-life / s)")
ax.set_title("UBP Symmetry Tax vs Radioactive Half-Life")

plt.suptitle("UBP Geometric Metrics as Predictors of Nuclear Half-Lives (Radioactive Elements Z=43–98)",
             fontsize=10)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig4_decay_rates.png")
plt.close()
print("  Saved figures/fig4_decay_rates.png")

# ── Figure 5: Particle Physics Predictions ────────────────────────────────
print("[Fig 5] Particle physics predictions...")
pp_df = pd.read_csv(RESULTS_DIR / "particle_physics_predictions.csv")
pp_df = pp_df.sort_values("error_pct")

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = [COLORS["ubp_blue"] if e < 0.05 else
              (COLORS["phase_lock"] if e < 0.1 else
               (COLORS["stable"] if e < 1.0 else COLORS["unstable"]))
              for e in pp_df["error_pct"]]
bars = ax.barh(pp_df["particle"], pp_df["error_pct"], color=bar_colors, alpha=0.8)
ax.axvline(0.05, color=COLORS["magic"], linestyle="--", linewidth=1.0,
           label="Phase-Lock threshold (0.05%)")
ax.axvline(0.1, color=COLORS["stable"], linestyle=":", linewidth=0.8,
           label="SSS threshold (0.1%)")
ax.set_xlabel("Prediction Error (%)")
ax.set_title("UBP 13D Sink Protocol: Particle Mass Predictions vs Experimental Targets\n"
             f"(Global Average Error = {deep['particle_physics_global_error_pct']:.5f}%)")
ax.set_xlim(0, pp_df["error_pct"].max() * 1.15)
legend_patches = [
    mpatches.Patch(color=COLORS["ubp_blue"], label="★★★ Phase-Lock (<0.05%)"),
    mpatches.Patch(color=COLORS["phase_lock"], label="★★ SSS Grade (<0.1%)"),
    mpatches.Patch(color=COLORS["stable"], label="★ Good (<1.0%)"),
    mpatches.Patch(color=COLORS["magic"], label=""),
]
ax.legend(handles=legend_patches[:3] + [
    plt.Line2D([0],[0], color=COLORS["magic"], linestyle="--", label="Phase-Lock threshold (0.05%)")
], loc="lower right", framealpha=0.9)

# Add error values on bars
for bar, val in zip(bars, pp_df["error_pct"]):
    ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
            f"{val:.4f}%", va="center", fontsize=7)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig5_particle_predictions.png")
plt.close()
print("  Saved figures/fig5_particle_predictions.png")

# ── Figure 6: Iron Peak Deep Dive ─────────────────────────────────────────
print("[Fig 6] Iron peak deep dive...")
iron = pd.read_csv(RESULTS_DIR / "iron_peak_analysis.csv")

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

# BE/A profile
ax = axes[0]
ax.plot(iron["Z"], iron["be_per_A_semi"], "o-", color=COLORS["ubp_blue"],
        linewidth=1.5, markersize=5)
fe_row = iron[iron["Z"]==26]
ax.scatter(fe_row["Z"], fe_row["be_per_A_semi"], s=120, c=COLORS["iron"],
           zorder=5, edgecolors="black", linewidths=0.8, marker="*", label="Fe-56")
ax.set_xlabel("Z")
ax.set_ylabel("BE/A (MeV)")
ax.set_title("(a) Binding Energy/Nucleon")
ax.legend()
MAGIC_Z_SET = {2, 8, 20, 28, 50, 82, 126}
for _, r in iron.iterrows():
    if int(r["Z"]) in MAGIC_Z_SET:
        ax.axvline(r["Z"], color=COLORS["magic"], alpha=0.5, linestyle="--", linewidth=0.8)

# NRCI profile
ax = axes[1]
phase_colors = [COLORS["phase_lock"] if p == "PHASE_LOCK" else COLORS["unstable"]
                for p in iron["phase_lock"]]
ax.bar(iron["Z"], iron["nrci_score"], color=phase_colors, alpha=0.75, width=0.7)
ax.axhline(0.60, color=COLORS["dark_gray"], linestyle=":", linewidth=0.8)
ax.axhline(0.70, color=COLORS["dark_gray"], linestyle="-.", linewidth=0.8)
fe_row2 = iron[iron["Z"]==26].iloc[0]
ax.scatter(26, fe_row2["nrci_score"], s=120, c=COLORS["iron"],
           zorder=5, edgecolors="black", linewidths=0.8, marker="*")
ax.set_xlabel("Z")
ax.set_ylabel("UBP NRCI Score")
ax.set_title("(b) UBP NRCI\n(cyan = Phase-Lock band)")
pl_patch = mpatches.Patch(color=COLORS["phase_lock"], label="Phase-Lock [0.60–0.70]")
un_patch = mpatches.Patch(color=COLORS["unstable"],   label="Outside Phase-Lock")
ax.legend(handles=[pl_patch, un_patch], loc="upper right", fontsize=7)

# NCI profile
ax = axes[2]
ax.plot(iron["Z"], iron["nci"], "s-", color=COLORS["highlight"],
        linewidth=1.5, markersize=5)
fe_nci = iron[iron["Z"]==26].iloc[0]
ax.scatter(26, fe_nci["nci"], s=120, c=COLORS["iron"],
           zorder=5, edgecolors="black", linewidths=0.8, marker="*", label="Fe-56")
ax.set_xlabel("Z")
ax.set_ylabel("UBP Nuclear Coherence Index (NCI)")
ax.set_title("(c) UBP Nuclear Coherence Index")
ax.legend()

plt.suptitle("Iron Peak Region (Z = 20–35): Binding Energy and UBP Geometric Analysis",
             fontsize=11)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig6_iron_peak.png")
plt.close()
print("  Saved figures/fig6_iron_peak.png")

# ── Figure 7: UBP "Phase Lock" distribution across periodic table ─────────
print("[Fig 7] Phase lock distribution...")
fig, ax = plt.subplots(figsize=(10, 4))

phase_lock_by_Z = {
    "PHASE_LOCK":  df[df["phase_lock"]=="PHASE_LOCK"]["Z"].tolist(),
    "UNSTABLE":    df[df["phase_lock"]=="UNSTABLE"]["Z"].tolist(),
    "SUPER_STABLE":df[df["phase_lock"]=="SUPER_STABLE"]["Z"].tolist(),
}

y_pos = {"PHASE_LOCK": 1, "SUPER_STABLE": 2, "UNSTABLE": 0}
y_labels = {0: "Outside Phase-Lock\n(Unstable)", 1: "Phase-Lock\n[0.60–0.70]",
            2: "Super-Stable\n(NRCI>0.70)"}
for phase, zlist in phase_lock_by_Z.items():
    yval = y_pos[phase]
    col  = COLORS["phase_lock"] if phase == "PHASE_LOCK" else (
           COLORS["magic"] if phase == "SUPER_STABLE" else COLORS["unstable"])
    for z in zlist:
        ax.scatter(z, yval, c=col, s=25, alpha=0.75, zorder=3)

for z in MAGIC_Z:
    ax.axvline(z, color=COLORS["dark_gray"], linestyle="--", linewidth=0.6, alpha=0.6)
    ax.text(z, 2.55, str(z), fontsize=7, ha="center", color=COLORS["dark_gray"])

ax.set_xlim(0, 120)
ax.set_ylim(-0.4, 2.8)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels([y_labels[i] for i in [0,1,2]])
ax.set_xlabel("Atomic Number (Z)")
ax.set_title("UBP Phase-Lock Classification Across the Periodic Table\n(vertical dashed lines = magic proton numbers)")

counts = df["phase_lock"].value_counts()
ax.text(0.98, 0.05,
        "\n".join([f"{k}: {v}" for k, v in counts.items()]),
        transform=ax.transAxes, fontsize=8, va="bottom", ha="right",
        bbox=dict(boxstyle="round", fc="white", alpha=0.8))

plt.tight_layout()
plt.savefig(FIGURES_DIR / "fig7_phase_lock_distribution.png")
plt.close()
print("  Saved figures/fig7_phase_lock_distribution.png")

print("\nAll figures generated successfully.")
print("Files saved to:", FIGURES_DIR)
