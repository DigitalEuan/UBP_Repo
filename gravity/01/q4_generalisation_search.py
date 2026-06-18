"""
Q4 (FALSIFIER) — Generalisation test of the gravity-style formula.

QUESTION
--------
The gravity study's Phase-4 search found  G_UBP = (39/29) * Y^18 / w  with
0.1327% error against CODATA using a combinatorial grammar:

    candidate = multiplier * base * scale

  bases     : Y, Y^2, Y_inv, U_e_inv, NRCI_Univ, L_s, pi, phi, e, w
  scales    : 1/U_e, 1/U_e^2, 1/c, 1/c^2, Y^10, Y^12, Y^18
  multipliers: 1, 2, 3, 4, 8, 12, 24, 1/2, 1/3, 1/4, 1/8, 1/12, 1/24, sqrt(2), sqrt(3)
  + (each base also tested inverted)

This script runs the SAME search grammar against the following dimensionless
physical constants:

    alpha            (fine-structure constant)            ≈ 7.2973525643e-3
    alpha_inv        (inverse fine-structure)             ≈ 137.035999177
    mp/me            (proton/electron mass ratio)         ≈ 1836.15267343
    mmu/me           (muon/electron mass ratio)           ≈ 206.7682830
    alpha_G          (dimensionless gravitational coupling)= G*m_p^2/(hbar*c) ≈ 5.675e-39
    Lambda_lp2       (dimensionless cosmological const)   = Lambda * lp^2 ≈ 1.09e-123

If the grammar finds formulas with errors comparable to 0.13% for several of
these targets, that is EVIDENCE FOR the substrate being real.
If the grammar fails to find sub-1% hits for most targets, the gravity 0.13%
hit is more likely a coincidence (falsifier).

We also report, for each target, the best 5 candidates and the count of
candidates within 0.13%, 0.5%, 1%, 5% error bands.

Critical-stance notes (per user instruction "explore coincidences, mark clearly"):
  - We DO NOT round measured values to integers (the existing particle atlas
    does this implicitly via lens formulas like 220 - 83 + L).  The gravity
    formula doesn't, so we don't.
  - We DO NOT add per-constant bespoke corrections; the grammar is identical
    across all targets.
  - We DO require the formula to use the same dimensional convention as the
    gravity formula (pure substrate, no hbar/c/k_B constants).  This means
    Planck length / mass / time, which are dimensional, are tested via their
    DIMENSIONLESS combinations only.
"""
from __future__ import annotations
import json, sys, os
from fractions import Fraction
from pathlib import Path
from itertools import product

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

# ─────────────────────────────────────────────────────────────────────────────
# SUBSTRATE CONSTANTS (from v5.3)
# ─────────────────────────────────────────────────────────────────────────────
sub = u.SUBSTRATE
constants = sub.get_v6_constants()

PI   = constants["PI"]
PHI  = constants["PHI"]
E    = constants["E"]
Y    = constants["Y"]
YINV = constants["Y_INV"]
MONAD = constants["MONAD"]
W     = constants["WOBBLE"]
L     = constants["SINK_L"]
L_s   = u.PARTICLE_PHYSICS.L_s
U_e   = u.PARTICLE_PHYSICS.U_e       # 24^3 = 13824
NRCI_UNIV = F(10, 10 + 13)           # placeholder; see note below

# Re-compute NRCI_Univ from the actual compound substrate tax.
# Per the gravity paper, "NRCI_Univ" is the universe-level NRCI.  We don't have
# direct access to it; instead we use LEECH_ENGINE.calculate_nrci() on a
# representative point.
try:
    nrci_univ_raw = u.LEECH_ENGINE.calculate_nrci(list(u.LEECH_ENGINE.golay.get_octads()[0]))
    NRCI_UNIV = F(nrci_univ_raw.numerator, nrci_univ_raw.denominator) \
        if isinstance(nrci_univ_raw, Fraction) else F(nrci_univ_raw).limit_denominator(10**6)
except Exception:
    NRCI_UNIV = F(7623, 10000)   # fallback to the 0.7623 seen in the paper

# Speed of light c is used as a *dimensionless* scale factor in the original
# search (the paper used "1/c" as a scale).  We follow the same convention.
C = F(299792458, 1)

# Sanity check: reproduce G_UBP and confirm 0.13% error
G_CODATA = F(667430, 10**16)        # 6.67430e-11
G_UBP    = F(39, 29) * Y**18 / W
g_err    = abs(G_UBP - G_CODATA) / G_CODATA * 100
print(f"[sanity] G_UBP    = {float(G_UBP):.10e}")
print(f"[sanity] G_CODATA = {float(G_CODATA):.10e}")
print(f"[sanity] error    = {float(g_err):.4f}%")
assert float(g_err) < 0.2, "Sanity check failed: cannot reproduce G formula"

# ─────────────────────────────────────────────────────────────────────────────
# SEARCH GRAMMAR (identical to gravity paper Phase 4)
# ─────────────────────────────────────────────────────────────────────────────
BASES = {
    "Y":       Y,
    "Y^2":     Y**2,
    "Y_inv":   YINV,
    "U_e_inv": F(1, U_e),
    "NRCI_Univ": NRCI_UNIV,
    "L_s":     L_s,
    "pi":      PI,
    "phi":     PHI,
    "e":       E,
    "w":       W,
}

SCALES = {
    "1/U_e":   F(1, U_e),
    "1/U_e^2": F(1, U_e**2),
    "1/c":     F(1, C),
    "1/c^2":   F(1, C**2),
    "Y^10":    Y**10,
    "Y^12":    Y**12,
    "Y^18":    Y**18,
    "1":       F(1, 1),
}

# Multipliers — pure rationals (the original paper included sqrt(2), sqrt(3)
# which we represent as Fraction approximations to 30 digits)
SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)
SQRT3 = u.ExactMath.sqrt_frac(F(3, 1), prec=30)

MULTIPLIERS = {
    "1":    F(1, 1),
    "2":    F(2, 1),
    "3":    F(3, 1),
    "4":    F(4, 1),
    "8":    F(8, 1),
    "12":   F(12, 1),
    "24":   F(24, 1),
    "1/2":  F(1, 2),
    "1/3":  F(1, 3),
    "1/4":  F(1, 4),
    "1/8":  F(1, 8),
    "1/12": F(1, 12),
    "1/24": F(1, 24),
    "sqrt2": SQRT2,
    "sqrt3": SQRT3,
}

# ─────────────────────────────────────────────────────────────────────────────
# TARGETS  (all dimensionless)
# ─────────────────────────────────────────────────────────────────────────────
TARGETS = {
    "G (gravity)": {
        "value": G_CODATA,
        "note": "Newtonian G in SI units; dimensional but the substrate formula ignores this (see Section 6 of prior study)."
    },
    "alpha": {
        "value": F(72973525643, 10**13),     # 7.2973525643e-3 (CODATA 2022)
        "note": "Fine-structure constant, dimensionless."
    },
    "alpha_inv": {
        "value": F(137035999177, 10**9),      # 137.035999177
        "note": "Inverse fine-structure constant, dimensionless."
    },
    "mp/me": {
        "value": F(183615267343, 10**8),      # 1836.15267343 (CODATA 2022)
        "note": "Proton/electron mass ratio, dimensionless."
    },
    "mmu/me": {
        "value": F(2067682830, 10**7),        # 206.7682830
        "note": "Muon/electron mass ratio, dimensionless."
    },
    "alpha_G (G mp^2 / hbar c)": {
        # G * m_p^2 / (hbar * c) ≈ 5.675e-39
        # Compute exactly: G * (1.67262192369e-27)^2 / (1.054571817e-34 * 2.99792458e8)
        "value": F(5675, 10**42),             # 5.675e-39
        "note": "Dimensionless gravitational coupling (proton scale)."
    },
    "Lambda * lp^2": {
        "value": F(109, 10**125),             # 1.09e-123 (Planck 2018)
        "note": "Dimensionless cosmological constant."
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# RUN THE SEARCH
# ─────────────────────────────────────────────────────────────────────────────
def run_search(target_value: Fraction, target_name: str, top_k: int = 5):
    """Run the full combinatorial search; return all candidates sorted by error."""
    candidates = []
    for bn, bv in BASES.items():
        for sn, sv in SCALES.items():
            for mn, mv in MULTIPLIERS.items():
                # forward candidate
                try:
                    val = mv * bv * sv
                    if val <= 0:
                        continue
                    err = abs(val - target_value) / target_value * 100
                    candidates.append({
                        "formula": f"{mn} * {bn} * {sn}",
                        "value":   float(val),
                        "err_pct": float(err),
                        "value_exact": f"{val.numerator}/{val.denominator}"[:200],
                    })
                except Exception:
                    pass

                # inverted base candidate
                try:
                    if bv == 0:
                        continue
                    val = mv * (F(1, 1) / bv) * sv
                    if val <= 0:
                        continue
                    err = abs(val - target_value) / target_value * 100
                    candidates.append({
                        "formula": f"{mn} * 1/({bn}) * {sn}",
                        "value":   float(val),
                        "err_pct": float(err),
                        "value_exact": f"{val.numerator}/{val.denominator}"[:200],
                    })
                except Exception:
                    pass

    candidates.sort(key=lambda c: c["err_pct"])
    # count hits in bands
    band_counts = {
        "le_0.01pct": sum(1 for c in candidates if c["err_pct"] <= 0.01),
        "le_0.05pct": sum(1 for c in candidates if c["err_pct"] <= 0.05),
        "le_0.13pct": sum(1 for c in candidates if c["err_pct"] <= 0.13),
        "le_0.50pct": sum(1 for c in candidates if c["err_pct"] <= 0.50),
        "le_1.00pct": sum(1 for c in candidates if c["err_pct"] <= 1.00),
        "le_5.00pct": sum(1 for c in candidates if c["err_pct"] <= 5.00),
    }
    return {
        "target":              target_name,
        "target_value":        float(target_value),
        "n_candidates":        len(candidates),
        "band_counts":         band_counts,
        "top_k":               candidates[:top_k],
        "best_err_pct":        candidates[0]["err_pct"] if candidates else None,
    }

# ─────────────────────────────────────────────────────────────────────────────
# EXECUTE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*78)
print("Q4 GENERALISATION TEST — gravity-style grammar on dimensionless constants")
print("="*78)
print(f"Search space: {len(BASES)} bases * 2 (forward/inverse) * "
      f"{len(SCALES)} scales * {len(MULTIPLIERS)} multipliers = "
      f"{len(BASES)*2*len(SCALES)*len(MULTIPLIERS)} candidates per target\n")

results = {}
for tname, tinfo in TARGETS.items():
    print(f"\n--- Target: {tname} ---")
    print(f"    value = {float(tinfo['value']):.10e}")
    print(f"    note:  {tinfo['note']}")
    r = run_search(tinfo["value"], tname)
    results[tname] = r
    print(f"    candidates evaluated: {r['n_candidates']}")
    print(f"    band counts: {r['band_counts']}")
    print(f"    best error:  {r['best_err_pct']:.6f}%")
    print(f"    top 5:")
    for i, c in enumerate(r["top_k"]):
        print(f"      [{i+1}] {c['formula']:50s} = {c['value']:.6e}  err={c['err_pct']:.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out = Path("/home/z/my-project/results/q4_generalisation.json")
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n[ok] Results saved to {out}")
