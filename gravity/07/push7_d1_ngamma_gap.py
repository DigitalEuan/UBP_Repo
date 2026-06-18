"""
Push #7 D.1 (NQ27/NQ31) — Close n_γ/n_b's 5.1% error gap via Symmetry Tax rebate sweep.

Per the UBP Core Studio AI's plan:
  "Because it is a Potential-layer formula (like Ω_k), it likely requires a
   Symmetry Tax Rebate. Take the exact formula and sweep it against the canonical
   UBP α parameters: × 10/(10 + α·tax), testing α ∈ {1/8, 1/4, 1/2, 1, 2, 3, 4,
   8, 12, 13, 24}. We will see if one of these geometrically significant fractions
   snaps the 5.1% error down to sub-0.1%."

The base formula from Push #6 D.3:
  n_γ/n_b = 1/4 · Y^21 · U_e · NRCI(2)
  = 1/4 · Y^21 · U_e · 10/(10 + 2·tax)
  = 1.60 × 10^-9  (target 1.69 × 10^-9, error 5.10%)

This script applies an ADDITIONAL Symmetry Tax rebate on top of the existing NRCI(2),
testing whether a compound rebate (NRCI(α₁) × NRCI(α₂)) closes the gap. We also test
replacing the existing α=2 with other α values, and adding Topological Shear corrections.

If a canonical correction closes the gap to sub-0.1%, n_γ/n_b becomes the 5th
predictive formula.
"""
from __future__ import annotations
import json, sys, random
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

pp = u.PARTICLE_PHYSICS
Y = pp.Y
L = pp.L
L_s = pp.L_s
U_e = pp.U_e
w = pp.wobble
pi = pp.pi

# Leech tax for Symmetry Tax rebate
octad = list(u.GOLAY_ENGINE.get_octads()[0])
tax = u.LEECH_ENGINE.symmetry_tax(octad)
print(f"Canonical octad tax = {float(tax):.6f}")

# Target: n_γ/n_b = 1.69e-9 (Planck 2018)
target = F(169, 10**11)  # 1.69e-9

# Base formula from Push #6 D.3: 1/4 · Y^21 · U_e · NRCI(2)
# where NRCI(α) = 10/(10 + α·tax)
base_pred = F(1, 4) * Y**21 * U_e * (F(10) / (F(10) + F(2) * tax))
base_err = abs(base_pred - target) / target * 100

print("=" * 80)
print("Push #7 D.1 — Close n_γ/n_b error gap via Symmetry Tax rebate sweep")
print("=" * 80)
print(f"\n  Target n_γ/n_b = {float(target):.4e}")
print(f"  Base formula: 1/4·Y^21·U_e·NRCI(2) = {float(base_pred):.4e}")
print(f"  Base error: {float(base_err):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Sweep α for the EXISTING NRCI(2) — try replacing 2 with other α values
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(1) Sweep α in NRCI(α) = 10/(10 + α·tax), replacing the existing α=2")
print("=" * 80)

canonical_alphas = [
    ("1/8", F(1, 8)), ("1/4", F(1, 4)), ("1/2", F(1, 2)),
    ("1", F(1)), ("2", F(2)), ("3", F(3)), ("4", F(4)),
    ("8", F(8)), ("12", F(12)), ("13", F(13)), ("24", F(24)),
    ("1/3", F(1, 3)), ("1/12", F(1, 12)), ("1/13", F(1, 13)),
    ("1/24", F(1, 24)), ("5", F(5)), ("6", F(6)), ("7", F(7)),
    ("1/6", F(1, 6)), ("1/7", F(1, 7)),
]

print(f"\n{'α':<8} {'NRCI(α)':<14} {'Prediction':<16} {'Error %':<10}")
print("-" * 50)
results_single = []
for name, alpha in canonical_alphas:
    nrci = F(10) / (F(10) + alpha * tax)
    pred = F(1, 4) * Y**21 * U_e * nrci
    err = abs(pred - target) / target * 100
    results_single.append({"alpha": name, "alpha_val": float(alpha), "nrci": float(nrci),
                            "pred": float(pred), "err_pct": float(err)})
    marker = "  <-- HIT" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {name:<6} {float(nrci):<14.6f} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Compound rebate: NRCI(α₁) × NRCI(α₂) on top of the base formula
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(2) Compound rebate: 1/4·Y^21·U_e·NRCI(α₁)·NRCI(α₂)")
print("=" * 80)

# Test compound rebates with canonical α pairs
compound_alphas = [
    ("2", "1/8"), ("2", "1/4"), ("2", "1/2"), ("2", "1"),
    ("1/8", "1/8"), ("1/4", "1/4"), ("1/2", "1/2"),
    ("1", "1"), ("2", "2"), ("3", "1/8"), ("4", "1/8"),
    ("1/8", "1/4"), ("1/4", "1/2"), ("1/2", "1"),
]

print(f"\n{'α₁':<6} {'α₂':<6} {'NRCI(α₁)':<12} {'NRCI(α₂)':<12} {'Prediction':<16} {'Error %':<10}")
print("-" * 70)
results_compound = []
for a1_name, a2_name in compound_alphas:
    a1 = dict(canonical_alphas)[a1_name]
    a2 = dict(canonical_alphas)[a2_name]
    nrci1 = F(10) / (F(10) + a1 * tax)
    nrci2 = F(10) / (F(10) + a2 * tax)
    pred = F(1, 4) * Y**21 * U_e * nrci1 * nrci2
    err = abs(pred - target) / target * 100
    results_compound.append({"alpha1": a1_name, "alpha2": a2_name,
                              "pred": float(pred), "err_pct": float(err)})
    marker = "  <-- HIT" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {a1_name:<4} {a2_name:<4} {float(nrci1):<12.6f} {float(nrci2):<12.6f} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Additive Topological Shear: base × (1 + α·L·Y) on top of the base formula
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(3) Topological Shear: 1/4·Y^21·U_e·NRCI(2) × (1 + α·L·Y)")
print("=" * 80)

shear_alphas = [
    ("1/8", F(1, 8)), ("1/4", F(1, 4)), ("1/2", F(1, 2)),
    ("1", F(1)), ("2", F(2)), ("3", F(3)), ("4", F(4)),
    ("8", F(8)), ("12", F(12)), ("13", F(13)), ("24", F(24)),
    ("1/3", F(1, 3)), ("1/12", F(1, 12)),
]

print(f"\n{'α':<8} {'Shear factor':<14} {'Prediction':<16} {'Error %':<10}")
print("-" * 50)
results_shear = []
for name, alpha in shear_alphas:
    shear = F(1) + alpha * L * Y
    pred = base_pred * shear
    err = abs(pred - target) / target * 100
    results_shear.append({"alpha": name, "shear_factor": float(shear),
                           "pred": float(pred), "err_pct": float(err)})
    marker = "  <-- HIT" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {name:<6} {float(shear):<14.6f} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# Also test (1 + α·L_s·Y) and (1 + α·Y²) variants
print(f"\n  --- Variant: × (1 + α·L_s·Y) ---")
for name, alpha in shear_alphas[:8]:
    shear = F(1) + alpha * L_s * Y
    pred = base_pred * shear
    err = abs(pred - target) / target * 100
    marker = "  <-- HIT" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {name:<6} {float(shear):<14.6f} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

print(f"\n  --- Variant: × (1 + α·Y²) ---")
for name, alpha in shear_alphas[:8]:
    shear = F(1) + alpha * Y**2
    pred = base_pred * shear
    err = abs(pred - target) / target * 100
    marker = "  <-- HIT" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {name:<6} {float(shear):<14.6f} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Best correction overall
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(4) Best correction overall (combined search)")
print("=" * 80)

all_results = []
for r in results_single:
    all_results.append({"type": "single NRCI(α)", **r})
for r in results_compound:
    all_results.append({"type": "compound NRCI(α₁)·NRCI(α₂)", **r})
for r in results_shear:
    all_results.append({"type": "Topological Shear × (1+α·L·Y)", **r})

all_results.sort(key=lambda c: c["err_pct"])

print(f"\nTop 10 corrections overall:")
print(f"  {'Type':<35} {'Details':<25} {'Pred':<14} {'Err %':<10}")
for c in all_results[:10]:
    if "alpha1" in c:
        details = f"α₁={c['alpha1']}, α₂={c['alpha2']}"
    elif "alpha" in c:
        details = f"α={c['alpha']}"
    else:
        details = ""
    print(f"  {c['type']:<35} {details:<25} {c['pred']:<14.4e} {c['err_pct']:<10.4f}")

best = all_results[0]
print(f"\nBest correction: {best['type']}, details = {best.get('alpha', best.get('alpha1', ''))}")
print(f"  Prediction: {best['pred']:.4e}")
print(f"  Error: {best['err_pct']:.4f}%")
print(f"  Sub-0.1%? {'YES — n_γ/n_b is now predictive' if best['err_pct'] < 0.1 else 'NO'}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. If best is sub-0.1%, run focused null to verify
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(5) Focused null on the best correction (if sub-1%)")
print("=" * 80)

if best["err_pct"] < 1.0:
    print(f"\n  Best correction is sub-1% ({best['err_pct']:.4f}%). Running focused null...")
    random.seed(70707)
    N_TRIALS = 5000
    null_errs = []
    for trial in range(N_TRIALS):
        Y_mult = random.uniform(0.1, 10.0)
        Y_s = float(Y) * Y_mult
        Y21_s = Y_s ** 21
        # Recompute tax with scrambled Y (tax = 8·Y + 1 for canonical octad)
        tax_s = 8 * Y_s + 1
        # Recompute the best correction
        if best["type"] == "single NRCI(α)":
            alpha_val = float(dict(canonical_alphas)[best["alpha"]])
            nrci_s = 10.0 / (10.0 + alpha_val * tax_s)
            pred = 0.25 * Y21_s * float(U_e) * nrci_s
        elif best["type"] == "compound NRCI(α₁)·NRCI(α₂)":
            a1 = float(dict(canonical_alphas)[best["alpha1"]])
            a2 = float(dict(canonical_alphas)[best["alpha2"]])
            nrci1_s = 10.0 / (10.0 + a1 * tax_s)
            nrci2_s = 10.0 / (10.0 + a2 * tax_s)
            pred = 0.25 * Y21_s * float(U_e) * nrci1_s * nrci2_s
        elif best["type"] == "Topological Shear × (1+α·L·Y)":
            alpha_val = float(dict(canonical_alphas)[best["alpha"]])
            # Note: L = w/13 doesn't depend on Y, so L stays fixed when scrambling Y
            nrci_base = 10.0 / (10.0 + 2.0 * tax_s)  # base NRCI(2)
            shear_s = 1.0 + alpha_val * float(L) * Y_s
            pred = 0.25 * Y21_s * float(U_e) * nrci_base * shear_s
        else:
            continue
        if pred > 0:
            err = abs(pred - float(target)) / float(target) * 100
            null_errs.append(err)

    if null_errs:
        null_errs.sort()
        hits = sum(1 for e in null_errs if e <= best["err_pct"])
        fp_rate = hits / len(null_errs) * 100
        print(f"  Real error: {best['err_pct']:.4f}%")
        print(f"  Null distribution ({len(null_errs)} trials):")
        print(f"    min: {null_errs[0]:.4f}%   p10: {null_errs[len(null_errs)//10]:.4f}%   "
              f"p50: {null_errs[len(null_errs)//2]:.4f}%   p90: {null_errs[9*len(null_errs)//10]:.4f}%")
        print(f"  Trials with err ≤ real: {hits}/{len(null_errs)} = {fp_rate:.2f}%")
        if fp_rate < 5:
            verdict = "SURPRISING — corrected n_γ/n_b formula is statistically surprising"
        elif fp_rate < 20:
            verdict = "MARGINALLY SURPRISING"
        else:
            verdict = "NOT surprising"
        print(f"  VERDICT: {verdict}")
else:
    print(f"\n  Best correction is {best['err_pct']:.4f}% — not sub-1%. No focused null run.")
    verdict = "not applicable"

# Save
outp = Path("/home/z/my-project/results/push7_d1_ngamma_gap.json")
with open(outp, "w") as f:
    json.dump({
        "target": float(target),
        "base_pred": float(base_pred),
        "base_err_pct": float(base_err),
        "single_alpha_sweep": results_single,
        "compound_rebate_sweep": results_compound,
        "topological_shear_sweep": results_shear,
        "best_correction": best,
        "focused_null": {
            "n_trials": len(null_errs) if best["err_pct"] < 1.0 else 0,
            "fp_rate_pct": fp_rate if best["err_pct"] < 1.0 else None,
            "verdict": verdict if best["err_pct"] < 1.0 else "not applicable",
        } if best["err_pct"] < 1.0 else None,
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
