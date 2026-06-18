"""
Push #6 D.3 (Option A / NQ24) — Y^21 bit-inversion partner hunt.

OBJECTIVE
---------
The validated bit-inversion pairing rule (Push #5 D.3) predicts:
  Y_inv³ (α⁻¹, Reality layer, bits 0-5) ↔ Y^21 (Potential layer, bits 18-23)
  3 + 21 = 24 = Leech rank

This script searches for a Y^21-scale Potential-layer constant. We test:
  - Dark energy density (in dimensionless form)
  - Cosmological constant ratios
  - Planck-scale dimensionless quantities
  - Hubble-scale quantities
  - CMB-S4 forecast quantities

Per Push #5's structural pattern, Potential-layer formulas use:
  - 24 (scaffolding) × Y^(24−k) × U_e (manifestation compensation)
  - For Y^21: candidate form is 24·Y^21·U_e or similar

Y^21 ≈ 7.5 × 10⁻¹³ — this is a very small scale, suggesting the target is a
dimensionless cosmological quantity.
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
Y_inv = pp.Y_INV
L = pp.L
L_s = pp.L_s
U_e = pp.U_e
w = pp.wobble
pi = pp.pi
phi = pp.phi
e_const = pp.e_const

# Leech tax for Symmetry Tax rebate corrections
octad = list(u.GOLAY_ENGINE.get_octads()[0])
tax = u.LEECH_ENGINE.symmetry_tax(octad)

print("=" * 80)
print("Push #6 D.3 — Y^21 bit-inversion partner hunt")
print("=" * 80)
print(f"\nY^21 = {float(Y**21):.6e}")
print(f"Predicted partner of Y_inv³ (α⁻¹, Reality)")
print(f"3 + 21 = 24 = Leech rank (confirms bit-inversion pairing)")

# ─────────────────────────────────────────────────────────────────────────────
# Y^21-scale targets — dimensionless cosmological quantities
# ─────────────────────────────────────────────────────────────────────────────
# Y^21 ≈ 7.5e-13
# We need dimensionless quantities at this scale

TARGETS_D3 = {
    # Cosmological constant in various dimensionless forms
    "Λ (SI, s⁻²)":                    F(110, 10**55),         # 1.1e-53 s⁻² (Planck 2018)
    "Λ (Planck units, ℓ_P⁻²)":        F(11, 10**124),         # 1.1e-123 (dimensionless)
    "Λ·(c/H_0)²":                     F(11, 100) * F(1, 10**60),  # rough estimate
    # Dark energy density (dimensionless)
    "ρ_Λ/ρ_crit (= Ω_Λ)":             F(6889, 10000),         # 0.6889 (Planck 2018)
    # Hubble parameter in Planck units
    "H_0·t_P (Hubble in Planck time)":F(6736, 10000) * F(1, 10**61),  # ~6.7e3 m/s/Mpc × Planck time
    # CMB photon-to-baryon ratio
    "n_γ/n_b (photon/baryon)":        F(169, 10**11),         # ~1.69e-9
    # Baryon-to-photon ratio (inverse)
    "n_b/n_γ (baryon/photon)":        F(61, 10**11),          # ~6.1e-10
    # Curvature-radius-to-Hubble-radius ratio
    "√|Ω_k| (curvature scale)":       F(265, 10000),   # sqrt(0.0007) ≈ 0.0265 (computed as float)
    # Vacuum energy density (in Planck units, dimensionless)
    "ρ_vac/ρ_P (vac/Planck density)": F(11, 10**124),         # ~1e-123 (same as Λ in Planck units)
    # Cosmological constant in GeV units (dimensionless ratio to m_P⁴)
    "Λ/m_P⁴ (cosm. const / Planck⁴)": F(11, 10**124),         # same
    # Dark energy density (in GeV⁴, dimensionless to m_P⁴)
    "ρ_Λ GeV⁴ / m_P⁴":                F(35, 10**47),          # ~3.5e-47 GeV⁴ / (1.22e19 GeV)⁴
    # Some particle-physics dimensionless ratios
    "m_ν/m_P (neutrino/Planck)":      F(6, 10**13),           # 0.06 eV / 1.22e28 eV ~ 5e-30 (way too small)
    "G_F·m_P² (Fermi×Planck²)":       F(11664, 10**13) * F(122, 10) ** 2,  # G_F in GeV⁻² × m_P² in GeV²
}

# Filter to manageable targets (those at the Y^21 ~ 7.5e-13 scale)
print(f"\nTargets and their scales:")
TARGETS_FILTERED = {}
for name, val in TARGETS_D3.items():
    try:
        v = float(val)
        # Look for targets within ~10 orders of magnitude of Y^21
        ratio = v / float(Y**21)
        if 1e-15 < ratio < 1e15:
            TARGETS_FILTERED[name] = val
            print(f"  {name:<45} = {v:.4e}  (ratio to Y^21: {ratio:.2e})  ✓ in range")
        else:
            print(f"  {name:<45} = {v:.4e}  (ratio to Y^21: {ratio:.2e})  ✗ out of range")
    except Exception as e:
        print(f"  {name:<45} ERROR: {e}")

# Add more Y^21-scale targets specifically
Y21_float = float(Y**21)
print(f"\n--- Additional Y^21-scale targets (specific to ~{Y21_float:.2e}) ---")
# Y^21 ≈ 7.5e-13. Quantities at this scale:
# - Vacuum energy density ratio ~ 10⁻¹²³ (way too small)
# - Some cosmological ratios ~ 10⁻¹²
# Let's also test "10⁻¹²" scale dimensionless quantities
additional_targets = {
    # Specific Y^21-scale dimensionless quantities
    "Λ × (c/H_0)² (proper dim-less)":   F(11, 10) ** 2 / F(10**60, 1),  # rough estimate
    # Electron-to-Planck mass ratio squared
    "(m_e/m_P)²":                       F(511, 10**6) ** 2 / F(122, 10**19) ** 2,  # ~1.7e-46 (too small)
    # Fine structure × gravitational coupling ratio
    "α/α_G":                            F(72973525643, 10**13) / F(5675, 10**42),
    # Some specific Planck-2018 cosmological parameters
    "σ₈ (matter fluctuation amplitude)":F(811, 1000),  # 0.811 (Planck 2018)
    "n_s (scalar spectral index)":      F(965, 1000),  # 0.965 (Planck 2018)
    "τ (optical depth)":                F(54, 1000),   # 0.054 (Planck 2018)
    # Dark energy equation of state
    "w (DE equation of state)":         F(-1, 1),      # -1 (cosmological constant)
    "1+w":                              F(0, 1),       # 0 (deviation from -1)
    # Specific Y^21-scale prediction: 24·Y^21·U_e
    "24·Y^21·U_e (Push #5 form)":       F(24) * Y**21 * U_e,
    # 24·Y^21·U_e × NRCI (with α=1/8 like Ω_k)
    "24·Y^21·U_e × 10/(10+⅛·tax)":      F(24) * Y**21 * U_e * (F(10) / (F(10) + F(1,8) * tax)),
    # α⁻¹-related: since α⁻¹ uses Y_inv³, its mirror should use Y^21
    # α⁻¹ = 137 + L ≈ 137.036; the Y^21 partner should be a small dimensionless number
    # related to α⁻¹ in the same way Ω_k is related to m_τ/m_e
    # m_τ/m_e ≈ 3477.23, Ω_k ≈ 7e-4; ratio = 3477.23 / 7e-4 ≈ 5e6
    # If the Y^21 partner follows the same pattern: α⁻¹ / Y^21_partner ≈ 5e6
    # → Y^21_partner ≈ 137 / 5e6 ≈ 2.7e-5
    "predicted partner of α⁻¹ (137/5e6)": F(137, 5_000_000),
    # But this is just a guess based on the m_τ/m_e ↔ Ω_k ratio
}

for name, val in additional_targets.items():
    try:
        v = float(val)
        ratio = v / Y21_float
        if 1e-15 < ratio < 1e15:
            TARGETS_FILTERED[name] = val
            print(f"  {name:<45} = {v:.4e}  (ratio to Y^21: {ratio:.2e})  ✓ in range")
        else:
            print(f"  {name:<45} = {v:.4e}  (ratio to Y^21: {ratio:.2e})  ✗ out of range")
    except Exception as e:
        print(f"  {name:<45} ERROR: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Generate Y^21-based formulas (similar to D.3 in Push #5)
# ─────────────────────────────────────────────────────────────────────────────
def y21_predictions():
    preds = {}
    for mult_name, mult_val in [("1", F(1)), ("2", F(2)), ("3", F(3)),
                                  ("4", F(4)), ("8", F(8)), ("12", F(12)),
                                  ("24", F(24)), ("29", F(29)), ("39", F(39)),
                                  ("137", F(137)), ("169", F(169)),
                                  ("1/2", F(1,2)), ("1/3", F(1,3)),
                                  ("1/4", F(1,4)), ("1/8", F(1,8)),
                                  ("1/12", F(1,12)), ("1/24", F(1,24)),
                                  ("1/29", F(1,29)), ("1/39", F(1,39)),
                                  ("1/137", F(1,137)), ("1/169", F(1,169)),
                                  ("39/29", F(39,29)), ("29/24", F(29,24))]:
        for base_name, base_val in [("Y^21", Y**21), ("Y^21·w", Y**21*w),
                                      ("Y^21/w", Y**21/w), ("Y^21·Y", Y**21*Y),
                                      ("Y^21·Y²", Y**21*Y**2),
                                      ("Y^21·L", Y**21*L), ("Y^21·L_s", Y**21*L_s),
                                      ("Y^21·U_e", Y**21*U_e),
                                      ("Y^21·pi", Y**21*pi),
                                      ("Y^21·phi", Y**21*phi),
                                      ("Y^21·e", Y**21*e_const),
                                      # With Symmetry Tax rebate (the Ω_k correction)
                                      ("Y^21·U_e·NRCI(1/8)", Y**21*U_e * (F(10)/(F(10)+F(1,8)*tax))),
                                      ("Y^21·U_e·NRCI(1)", Y**21*U_e * (F(10)/(F(10)+F(1)*tax))),
                                      ("Y^21·U_e·NRCI(2)", Y**21*U_e * (F(10)/(F(10)+F(2)*tax))),
                                      ("Y^21·U_e·NRCI(12)", Y**21*U_e * (F(10)/(F(10)+F(12)*tax))),
                                      ("Y^21·U_e·NRCI(13)", Y**21*U_e * (F(10)/(F(10)+F(13)*tax))),
                                     ]:
            preds[f"{mult_name}·{base_name}"] = mult_val * base_val
    return preds

preds_d3 = y21_predictions()
print(f"\n{len(preds_d3)} Y^21-based candidate formulas generated")
print(f"Testing against {len(TARGETS_FILTERED)} targets in range\n")

# ─────────────────────────────────────────────────────────────────────────────
# Run search
# ─────────────────────────────────────────────────────────────────────────────
print(f"{'Target':<45} {'Target value':<14} {'Best formula':<35} {'Err %':<10}")
print("-" * 110)

d3_results = {}
for tname, tval in TARGETS_FILTERED.items():
    best_pred = None
    best_err = float('inf')
    best_formula = None
    for pname, pval in preds_d3.items():
        try:
            pv = float(pval)
            tv = float(tval)
            if pv <= 0 or tv <= 0: continue
            err = abs(pv - tv) / tv * 100
            if err < best_err:
                best_err = err
                best_pred = pv
                best_formula = pname
        except: continue
    d3_results[tname] = {
        "target": float(tval),
        "best_formula": best_formula,
        "best_pred": best_pred,
        "best_err_pct": best_err,
    }
    marker = "  <-- HIT" if best_err < 5 else ("  <-- sub-1%" if best_err < 1 else "")
    print(f"{tname[:43]:<45} {float(tval):<14.4e} {(best_formula or '—')[:33]:<35} {best_err:<10.4f}{marker}")

# ─────────────────────────────────────────────────────────────────────────────
# Focused null on the best hit
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Focused null on the best Y^21 hit (if sub-5%)")
print("=" * 80)

# Find best sub-5% hit
best_target = min(d3_results.items(), key=lambda x: x[1]["best_err_pct"])
print(f"\nBest Y^21 hit: {best_target[0]}")
print(f"  Target: {best_target[1]['target']:.6e}")
print(f"  Formula: {best_target[1]['best_formula']}")
print(f"  Prediction: {best_target[1]['best_pred']:.6e}")
print(f"  Error: {best_target[1]['best_err_pct']:.4f}%")

if best_target[1]["best_err_pct"] < 5:
    print(f"\n  Running focused null (5000 trials, scramble Y, hold integers fixed)...")
    random.seed(60606)
    N_TRIALS = 5000
    null_errs = []
    target_val = best_target[1]["target"]
    best_err_real = best_target[1]["best_err_pct"]
    best_formula_name = best_target[1]["best_formula"]

    # Parse the formula to determine which constants to hold/scramble
    # Y^21 always uses Y (scramble Y). U_e is integer (hold). NRCI uses tax (depends on Y too, but tax uses Y).
    # We'll scramble Y and recompute the formula

    # We need to recompute the formula from its name
    import re
    mult_match = re.match(r"^([\d/]+)·(.+)$", best_formula_name)
    if mult_match:
        mult_str = mult_match.group(1)
        base_str = mult_match.group(2)
        # Parse multiplier
        if "/" in mult_str:
            num, den = mult_str.split("/")
            mult_val = float(num) / float(den)
        else:
            mult_val = float(mult_str)
    else:
        mult_val = 1.0
        base_str = best_formula_name

    for trial in range(N_TRIALS):
        Y_mult = random.uniform(0.1, 10.0)
        Y_s = float(Y) * Y_mult
        # Recompute Y^21-based portion
        y21_s = Y_s ** 21
        # Parse the base
        if base_str == "Y^21":
            base = y21_s
        elif base_str == "Y^21·w":
            base = y21_s * float(w)
        elif base_str == "Y^21/w":
            base = y21_s / float(w)
        elif base_str == "Y^21·Y":
            base = y21_s * Y_s
        elif base_str == "Y^21·Y²":
            base = y21_s * Y_s**2
        elif base_str == "Y^21·L":
            base = y21_s * float(L)
        elif base_str == "Y^21·L_s":
            base = y21_s * float(L_s)
        elif base_str == "Y^21·U_e":
            base = y21_s * float(U_e)
        elif base_str == "Y^21·pi":
            base = y21_s * float(pi)
        elif base_str == "Y^21·phi":
            base = y21_s * float(phi)
        elif base_str == "Y^21·e":
            base = y21_s * float(e_const)
        elif "NRCI" in base_str:
            # Y^21·U_e·NRCI(α) — NRCI = 10/(10+α·tax) where tax depends on Y
            # tax = 8·Y + 8/8 = 8·Y + 1 (canonical octad tax)
            # Actually tax uses Y: tax = hw·Y + ns/8 = 8·Y + 1 (for canonical octad)
            tax_s = 8 * Y_s + 1  # canonical octad tax with scrambled Y
            nrci_alpha_match = re.search(r"NRCI\(([\d/]+)\)", base_str)
            if nrci_alpha_match:
                a_str = nrci_alpha_match.group(1)
                if "/" in a_str:
                    num, den = a_str.split("/")
                    a_val = float(num) / float(den)
                else:
                    a_val = float(a_str)
                nrci_val = 10.0 / (10.0 + a_val * tax_s)
                base = y21_s * float(U_e) * nrci_val
            else:
                continue
        else:
            continue

        pred = mult_val * base
        if pred > 0:
            err = abs(pred - target_val) / target_val * 100
            null_errs.append(err)

    if null_errs:
        null_errs.sort()
        hits = sum(1 for e in null_errs if e <= best_err_real)
        fp_rate = hits / len(null_errs) * 100
        print(f"  Real error: {best_err_real:.4f}%")
        print(f"  Null distribution ({len(null_errs)} trials):")
        print(f"    min: {null_errs[0]:.4f}%   p10: {null_errs[len(null_errs)//10]:.4f}%   "
              f"p50: {null_errs[len(null_errs)//2]:.4f}%   p90: {null_errs[9*len(null_errs)//10]:.4f}%")
        print(f"  Trials with err ≤ real: {hits}/{len(null_errs)} = {fp_rate:.2f}%")
        if fp_rate < 5:
            verdict = "SURPRISING — Y^21 partner is the 5th statistically surprising formula"
        elif fp_rate < 20:
            verdict = "MARGINALLY SURPRISING"
        else:
            verdict = "NOT surprising"
        print(f"  VERDICT: {verdict}")

        d3_results[best_target[0]]["null_model"] = {
            "n_trials": len(null_errs),
            "null_min_pct": null_errs[0],
            "null_p50_pct": null_errs[len(null_errs)//2],
            "hits_at_real": hits,
            "fp_rate_pct": fp_rate,
            "verdict": verdict,
        }

# Save
outp = Path("/home/z/my-project/results/push6_d3_y21_hunt.json")
with open(outp, "w") as f:
    json.dump({
        "y21_value": float(Y**21),
        "bit_inversion_prediction": "Y_inv³ (α⁻¹, Reality) ↔ Y^21 (Potential). 3+21=24=Leech rank.",
        "targets_tested": len(TARGETS_FILTERED),
        "candidates_tested": len(preds_d3),
        "results": d3_results,
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
