"""
UBP Nuclear Physics – Deep Dive Analysis
=========================================
Focus: Magic numbers, iron peak, decay chain analysis,
       particle physics predictions vs known nuclear data,
       and UBP geometric interpretation of nuclear phenomena.
"""

import sys
import json
import math
import numpy as np
import pandas as pd
from fractions import Fraction
from pathlib import Path
from scipy import stats

SESSION  = Path("/app/sandbox/session_20260327_124022_fb146e883394")
USER_DATA = SESSION / "user_data"
DATA_DIR  = SESSION / "data"
RESULTS_DIR = SESSION / "results"
sys.path.insert(0, str(USER_DATA))

from core import (
    GolayCodeEngine, LeechLatticeEngine, UBPUltimateSubstrate,
    UBPSourceCodeParticlePhysics, BinaryLinearAlgebra,
)
from physics import UBPMetricsExact, METRICS_EXACT

GOLAY     = GolayCodeEngine()
LEECH     = LeechLatticeEngine()
SUBSTRATE = UBPUltimateSubstrate()
CONSTANTS = UBPUltimateSubstrate.get_constants(precision=50)
Y_CONST   = CONSTANTS["Y"]

# ── load merged data ────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / "ubp_vs_experiment.csv")
print(f"Loaded {len(df)} elements")

# Load KB
with open(USER_DATA / "ubp_system_kb.json") as f:
    KB = json.load(f)

# ── 1. Binding Energy Landscape Analysis ──────────────────────────────────
print("\n[A] Binding Energy Landscape")

# A.1  UBP predicted vs semi-empirical BE/A
# Hypothesis: be_proxy correlates with actual BE/A after scaling
# Find the best linear fit: be_per_A_semi = α × be_proxy + β
mask = df["be_proxy"].notna() & df["be_per_A_semi"].notna() & np.isfinite(df["be_proxy"])
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df.loc[mask, "be_proxy"], df.loc[mask, "be_per_A_semi"])
print(f"  BE proxy linear fit: r={r_value:.4f}, p={p_value:.4e}, slope={slope:.6f}")

# A.2  Spearman rank correlation (non-parametric, handles non-linearity)
rho_nrci, p_rho = stats.spearmanr(
    df.loc[mask, "nrci_score"], df.loc[mask, "be_per_A_semi"])
rho_tax, p_rho_tax = stats.spearmanr(
    df.loc[mask, "symmetry_tax"], df.loc[mask, "be_per_A_semi"])
print(f"  Spearman NRCI ↔ BE/A: ρ={rho_nrci:.4f}, p={p_rho:.4e}")
print(f"  Spearman Tax  ↔ BE/A: ρ={rho_tax:.4f}, p={p_rho_tax:.4e}")

# A.3  Iron peak analysis (Z=24-30 region)
iron_region = df[(df["Z"]>=20) & (df["Z"]<=35)].copy()
print(f"\n  Iron Region (Z=20-35) UBP Analysis:")
print(f"  {'Z':3s} {'Sym':4s} {'BE/A':7s} {'NRCI':8s} {'NCI':8s} {'Tax':10s} {'Phase'}")
print("  " + "-"*60)
for _, row in iron_region.iterrows():
    marker = " ←FE" if row["Z"] == 26 else ("←Ni" if row["Z"]==28 else "")
    print(f"  {int(row['Z']):3d} {row['symbol']:4s} {row['be_per_A_semi']:7.3f} "
          f"{row['nrci_score']:8.4f} {row['nci']:8.4f} {row['symmetry_tax']:10.4f} "
          f"{row['phase_lock']:12s}{marker}")

# ── 2. Magic Number Analysis ───────────────────────────────────────────────
print("\n[B] Magic Number UBP Analysis")
MAGIC = {2, 8, 20, 28, 50, 82, 126}

magic_Z_elements = df[df["is_magic_Z"]].copy()
non_magic = df[~df["is_magic_Z"]].copy()

print(f"\n  Magic-Z elements (Z in {sorted(MAGIC)}):")
print(f"  {'Z':3s} {'Sym':4s} {'NRCI':8s} {'Tax':10s} {'Drift':6s} {'NCI':8s} {'BE/A':7s}")
print("  " + "-"*58)
for _, row in magic_Z_elements.iterrows():
    print(f"  {int(row['Z']):3d} {row['symbol']:4s} {row['nrci_score']:8.6f} "
          f"{row['symmetry_tax']:10.4f} {row['ontological_drift']:6.0f} "
          f"{row['nci']:8.6f} {row['be_per_A_semi']:7.3f}")

# Statistical test
t_stat, p_t = stats.ttest_ind(
    magic_Z_elements["nrci_score"].dropna(),
    non_magic["nrci_score"].dropna())
print(f"\n  t-test (magic vs non-magic NRCI): t={t_stat:.3f}, p={p_t:.4f}")

# Drift analysis for magic numbers
t_drift, p_drift = stats.ttest_ind(
    magic_Z_elements["ontological_drift"].dropna(),
    non_magic["ontological_drift"].dropna())
print(f"  t-test (magic vs non-magic Drift): t={t_drift:.3f}, p={p_drift:.4f}")

# ── 3. Radioactive Decay Rate Analysis ────────────────────────────────────
print("\n[C] Radioactive Decay Rate Analysis")
radioactive = df[~df["is_stable"] & df["log10_half_life"].notna()
                 & (df["log10_half_life"] < 100)].copy()
print(f"  Radioactive elements with known half-lives: {len(radioactive)}")

if len(radioactive) >= 5:
    corr_sp, p_sp = stats.spearmanr(
        radioactive["stability_pressure"], radioactive["log10_half_life"])
    corr_nrci, p_nrci_hl = stats.spearmanr(
        radioactive["nrci_score"], radioactive["log10_half_life"])
    corr_tax, p_tax_hl = stats.spearmanr(
        radioactive["symmetry_tax"], radioactive["log10_half_life"])
    print(f"  Spearman StabPressure ↔ log₁₀(t½): ρ={corr_sp:.4f}, p={p_sp:.4f}")
    print(f"  Spearman NRCI         ↔ log₁₀(t½): ρ={corr_nrci:.4f}, p={p_nrci_hl:.4f}")
    print(f"  Spearman Tax          ↔ log₁₀(t½): ρ={corr_tax:.4f}, p={p_tax_hl:.4f}")

    print(f"\n  Radioactive elements detail:")
    print(f"  {'Z':3s} {'Sym':4s} {'NRCI':8s} {'Tax':10s} {'StbPrss':8s} {'log₁₀t½':8s}")
    print("  " + "-"*56)
    for _, row in radioactive.sort_values("Z").iterrows():
        print(f"  {int(row['Z']):3d} {row['symbol']:4s} {row['nrci_score']:8.6f} "
              f"{row['symmetry_tax']:10.4f} {row['stability_pressure']:8.4f} "
              f"{row['log10_half_life']:8.2f}")

# ── 4. Particle Physics Predictions vs Nuclear Data ────────────────────────
print("\n[D] UBP 13D Sink Protocol – Particle Physics Predictions")
pp = UBPSourceCodeParticlePhysics(precision=50)
preds = pp.get_ultimate_predictions()

print(f"\n  {'Particle/Const':<22} {'Predicted':>12} {'Target':>12} {'Error%':>9} {'Grade'}")
print("  " + "-"*72)
for key, data in preds.items():
    if key in ["global_error", "sink_metadata"]:
        continue
    err = data["error_percent"]
    grade = "★★★ PHASE-LOCK" if err < 0.05 else ("★★ SSS" if err < 0.1 else
            ("★ Good" if err < 1.0 else ""))
    print(f"  {key:<22} {data['val']:>12.4f} {data['target']:>12.4f} {err:>9.4f}%  {grade}")
print(f"\n  GLOBAL ERROR: {preds['global_error']:.5f}%")

meta = preds["sink_metadata"]
print(f"\n  13D Sink Metadata:")
print(f"    Triadic Monad:    {meta['monad']:.10f}")
print(f"    Residue Wobble:   {meta['wobble']:.10f}")
print(f"    13D Leakage L:    {meta['leakage_L']:.10f}")

# ── 5. Leech Lattice Expansion & Nuclear Binding ────────────────────────────
print("\n[E] Leech Lattice Expansion Analysis (Iron Peak Region)")
fe_entry = [v for v in KB.values() if v["ubp_id"] == "ELEM_Fe_026"]
if fe_entry:
    fe = fe_entry[0]
    vec = fe["atlas"]["vector"]
    octads = GOLAY.get_octads()
    # Find nearest octad to Fe vector
    distances = [(i, BinaryLinearAlgebra.hamming_distance(vec, oct))
                 for i, oct in enumerate(octads)]
    nearest_idx, nearest_dist = min(distances, key=lambda x: x[1])
    fe_octad = octads[nearest_idx]
    expanded = LEECH.expand_octad_to_physical(fe_octad)
    norms = [sum(x**2 for x in pt) for pt in expanded]
    print(f"  Fe-56 vector drift to nearest octad: {nearest_dist} bits")
    print(f"  Leech expansion: {len(expanded)} physical addresses")
    print(f"  Norm² range: min={min(norms)}, max={max(norms)}, unique={len(set(norms))}")
    print(f"  Expected norm² = 32 → match: {norms[0] == 32}")

# ── 6. UBP NRCI Range for Stable vs Unstable Nuclei ─────────────────────
print("\n[F] UBP NRCI Distribution: Stable vs Unstable Nuclei")
stable_nrci   = df[df["is_stable"]]["nrci_score"]
unstable_nrci = df[~df["is_stable"]]["nrci_score"]
print(f"  Stable   (n={len(stable_nrci)}): "
      f"mean={stable_nrci.mean():.6f} ± {stable_nrci.std():.6f}, "
      f"range=[{stable_nrci.min():.4f}, {stable_nrci.max():.4f}]")
print(f"  Unstable (n={len(unstable_nrci)}): "
      f"mean={unstable_nrci.mean():.6f} ± {unstable_nrci.std():.6f}, "
      f"range=[{unstable_nrci.min():.4f}, {unstable_nrci.max():.4f}]")
t_stab, p_stab = stats.ttest_ind(stable_nrci.dropna(), unstable_nrci.dropna())
print(f"  Welch t-test: t={t_stab:.3f}, p={p_stab:.4f}")

# Effect size (Cohen's d)
n1, n2 = len(stable_nrci), len(unstable_nrci)
pooled_std = math.sqrt(((n1-1)*stable_nrci.std()**2 + (n2-1)*unstable_nrci.std()**2) / (n1+n2-2))
cohens_d = (stable_nrci.mean() - unstable_nrci.mean()) / pooled_std if pooled_std > 0 else 0
print(f"  Effect size (Cohen's d): {cohens_d:.4f}")

# ── 7. Nuclear Shell Energy vs UBP Symmetry Tax gradient ──────────────────
print("\n[G] Nuclear Shell Closures: UBP Symmetry Tax Gradient")
# The "kink" in BE/A curve at magic numbers should show up in tax gradient
df_sorted = df.sort_values("Z")
tax_gradient = np.gradient(df_sorted["symmetry_tax"].values, df_sorted["Z"].values)
be_gradient  = np.gradient(df_sorted["be_per_A_semi"].values, df_sorted["Z"].values)
# Pearson correlation of gradients
r_grad, p_grad = stats.pearsonr(tax_gradient, be_gradient)
print(f"  Pearson r(∇Tax, ∇BE/A) = {r_grad:.4f}, p={p_grad:.4e}")

# Local tax kinks at magic-Z positions
magic_Zs_present = [z for z in [2,8,20,28,50,82] if z in df["Z"].values]
print(f"\n  Symmetry Tax gradient at magic Z values:")
for z in magic_Zs_present:
    idx = df_sorted[df_sorted["Z"]==z].index[0]
    pos = list(df_sorted.index).index(idx)
    if 0 < pos < len(tax_gradient)-1:
        local_grad = tax_gradient[pos]
        print(f"    Z={z:3d}: ∇Tax = {local_grad:+.6f}")

# ── 8. Save deep dive results ─────────────────────────────────────────────
print("\n[H] Saving deep dive results...")

deep_results = {
    "binding_energy_analysis": {
        "be_proxy_linear_fit": {"r": round(r_value, 4), "p": round(p_value, 6),
                                "slope": round(slope, 8), "intercept": round(intercept, 6)},
        "spearman_nrci_vs_BE": {"rho": round(rho_nrci, 4), "p": round(p_rho, 6)},
        "spearman_tax_vs_BE":  {"rho": round(rho_tax, 4),  "p": round(p_rho_tax, 6)},
    },
    "magic_number_analysis": {
        "t_test_nrci": {"t": round(t_stat, 4), "p": round(p_t, 6)},
        "t_test_drift": {"t": round(t_drift, 4), "p": round(p_drift, 6)},
        "magic_mean_nrci": round(float(magic_Z_elements["nrci_score"].mean()), 6),
        "nonmagic_mean_nrci": round(float(non_magic["nrci_score"].mean()), 6),
    },
    "decay_analysis": {
        "n_radioactive_with_hl": len(radioactive),
        "spearman_stability_pressure_vs_log_hl": {
            "rho": round(corr_sp, 4) if len(radioactive)>=5 else None,
            "p": round(p_sp, 6) if len(radioactive)>=5 else None,
        },
        "spearman_nrci_vs_log_hl": {
            "rho": round(corr_nrci, 4) if len(radioactive)>=5 else None,
            "p": round(p_nrci_hl, 6) if len(radioactive)>=5 else None,
        },
    },
    "stable_vs_unstable_nrci": {
        "stable_mean": round(float(stable_nrci.mean()), 6),
        "unstable_mean": round(float(unstable_nrci.mean()), 6),
        "cohens_d": round(cohens_d, 4),
        "t_stat": round(t_stab, 4),
        "p_value": round(p_stab, 6),
    },
    "gradient_analysis": {
        "r_grad_tax_vs_BE": round(r_grad, 4),
        "p_grad": round(p_grad, 6),
    },
    "particle_physics_predictions": {
        k: {"val": round(v["val"], 4), "target": v["target"],
            "error_pct": round(v["error_percent"], 5), "lens": v["lens"]}
        for k, v in preds.items() if k not in ["global_error", "sink_metadata"]
    },
    "particle_physics_global_error_pct": round(preds["global_error"], 5),
    "13d_sink_metadata": preds["sink_metadata"],
}

with open(RESULTS_DIR / "ubp_nuclear_deep_dive.json", "w") as f:
    json.dump(deep_results, f, indent=2, default=str)

# Save the iron-region table
iron_region_out = iron_region[["Z","symbol","be_per_A_semi","nrci_score",
                                "symmetry_tax","nci","stability_pressure",
                                "phase_lock","magic_factor"]].copy()
iron_region_out.to_csv(RESULTS_DIR / "iron_peak_analysis.csv", index=False)

# Save radioactive elements table
if len(radioactive) > 0:
    radio_out = radioactive[["Z","symbol","A","nrci_score","symmetry_tax",
                              "stability_pressure","log10_half_life",
                              "decay_mode","phase_lock"]].sort_values("Z")
    radio_out.to_csv(RESULTS_DIR / "decay_rate_analysis.csv", index=False)

# Save full particle physics predictions
pp_rows = []
for k, v in preds.items():
    if k not in ["global_error", "sink_metadata"]:
        pp_rows.append({"particle": k, "predicted": round(v["val"], 4),
                        "target": v["target"],
                        "error_pct": round(v["error_percent"], 5),
                        "lens": v["lens"]})
pd.DataFrame(pp_rows).to_csv(RESULTS_DIR / "particle_physics_predictions.csv", index=False)

print("  Saved: results/ubp_nuclear_deep_dive.json")
print("  Saved: results/iron_peak_analysis.csv")
print("  Saved: results/decay_rate_analysis.csv")
print("  Saved: results/particle_physics_predictions.csv")
print("\nDEEP DIVE COMPLETE")
