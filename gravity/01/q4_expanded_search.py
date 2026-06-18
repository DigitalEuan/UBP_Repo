"""
Q4-EXPANDED — Generalisation test with extended Y-power sweep.

The gravity paper's Phase-4 search used scales {1/U_e, 1/U_e^2, 1/c, 1/c^2,
Y^10, Y^12, Y^18}.  The Y^18 was curated to bracket G's order of magnitude
(10^-11).  For a fair falsification of Q4 we MUST let the search pick the
appropriate Y-power for each target.

This script expands the search to:
  - Y^k for k = 1..40  (full spectrum)
  - Y_inv^k for k = 1..10
  - Same multiplier * base * scale grammar

For each target we report:
  - Best hit (formula, value, error)
  - Count of formulas within 0.01%, 0.05%, 0.13%, 0.50%, 1.00%, 5.00%
  - The Y-power that the best hit uses

This is the test that asks:  "Is the 0.13% G hit structurally surprising,
or would the grammar have hit ANY value within 0.13% given enough Y-powers?"
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

sub = u.SUBSTRATE
constants = sub.get_v6_constants()
PI   = constants["PI"]
PHI  = constants["PHI"]
E    = constants["E"]
Y    = constants["Y"]
YINV = constants["Y_INV"]
W    = constants["WOBBLE"]
L    = constants["SINK_L"]
L_s  = u.PARTICLE_PHYSICS.L_s
U_e  = u.PARTICLE_PHYSICS.U_e
C    = F(299792458, 1)

try:
    nrci_univ_raw = u.LEECH_ENGINE.calculate_nrci(list(u.LEECH_ENGINE.golay.get_octads()[0]))
    NRCI_UNIV = F(nrci_univ_raw) if not isinstance(nrci_univ_raw, Fraction) else nrci_univ_raw
    NRCI_UNIV = F(NRCI_UNIV.numerator, NRCI_UNIV.denominator).limit_denominator(10**6)
except Exception:
    NRCI_UNIV = F(7623, 10000)

G_CODATA = F(667430, 10**16)

# Sanity check
G_UBP = F(39, 29) * Y**18 / W
print(f"[sanity] G_UBP error = {float(abs(G_UBP - G_CODATA)/G_CODATA*100):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# EXPANDED GRAMMAR
# ─────────────────────────────────────────────────────────────────────────────
# Base = any single substrate constant
BASES = {
    "Y":     Y,
    "Y_inv": YINV,
    "L":     L,
    "L_s":   L_s,
    "pi":    PI,
    "phi":   PHI,
    "e":     E,
    "w":     W,
    "U_e":   U_e,
    "NRCI":  NRCI_UNIV,
}

# Y-power spectrum 1..40 (both forward and inverted)
Y_POWERS = {f"Y^{k}":     Y**k  for k in range(1, 41)}
Y_POWERS.update({f"Y_inv^{k}": YINV**k for k in range(1, 11)})

# Other scales (kept from original grammar)
OTHER_SCALES = {
    "1/U_e":   F(1, U_e),
    "1/U_e^2": F(1, U_e**2),
    "1/c":     F(1, C),
    "1/c^2":   F(1, C**2),
    "1":       F(1, 1),
}

SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)
SQRT3 = u.ExactMath.sqrt_frac(F(3, 1), prec=30)

MULTIPLIERS = {
    "1":    F(1, 1),
    "2":    F(2, 1),    "3":    F(3, 1),    "4":    F(4, 1),
    "8":    F(8, 1),    "12":   F(12, 1),   "24":   F(24, 1),
    "1/2":  F(1, 2),    "1/3":  F(1, 3),    "1/4":  F(1, 4),
    "1/8":  F(1, 8),    "1/12": F(1, 12),   "1/24": F(1, 24),
    "sqrt1": SQRT2, "sqrt3": SQRT3,
    # extended multipliers — to give the grammar a fairer chance
    "5":    F(5, 1),    "6":    F(6, 1),    "7":    F(7, 1),
    "1/5":  F(1, 5),    "1/6":  F(1, 6),    "1/7":  F(1, 7),
    "29":   F(29, 1),   "39":   F(39, 1),   "13":   F(13, 1),
    "1/29": F(1, 29),   "1/39": F(1, 39),   "1/13": F(1, 13),
}

TARGETS = {
    "G":           {"value": G_CODATA,                           "unit": "SI"},
    "alpha":       {"value": F(72973525643, 10**13),             "unit": "dimensionless"},
    "alpha_inv":   {"value": F(137035999177, 10**9),             "unit": "dimensionless"},
    "mp/me":       {"value": F(183615267343, 10**8),             "unit": "dimensionless"},
    "mmu/me":      {"value": F(2067682830, 10**7),               "unit": "dimensionless"},
    "mtau/me":     {"value": F(34778621, 100),                    "unit": "dimensionless"},
    "alpha_G":     {"value": F(5675, 10**42),                    "unit": "dimensionless"},
    "Lambda_lp2":  {"value": F(109, 10**125),                    "unit": "dimensionless"},
}

def run_search(target_value: Fraction, top_k: int = 5):
    candidates = []
    # Combine Y-powers and other scales into one scale list
    ALL_SCALES = {**Y_POWERS, **OTHER_SCALES}
    for bn, bv in BASES.items():
        for sn, sv in ALL_SCALES.items():
            for mn, mv in MULTIPLIERS.items():
                # forward
                try:
                    val = mv * bv * sv
                    if val > 0:
                        err = abs(val - target_value) / target_value * 100
                        candidates.append({
                            "formula": f"{mn}*{bn}*{sn}",
                            "value":   float(val),
                            "err_pct": float(err),
                            "ypower":  sn if sn.startswith("Y") else "",
                        })
                except Exception:
                    pass
                # inverted base
                try:
                    if bv == 0:
                        continue
                    val = mv * (F(1)/bv) * sv
                    if val > 0:
                        err = abs(val - target_value) / target_value * 100
                        candidates.append({
                            "formula": f"{mn}/({bn})*{sn}",
                            "value":   float(val),
                            "err_pct": float(err),
                            "ypower":  sn if sn.startswith("Y") else "",
                        })
                except Exception:
                    pass
    candidates.sort(key=lambda c: c["err_pct"])
    band_counts = {
        "le_0.01pct": sum(1 for c in candidates if c["err_pct"] <= 0.01),
        "le_0.05pct": sum(1 for c in candidates if c["err_pct"] <= 0.05),
        "le_0.13pct": sum(1 for c in candidates if c["err_pct"] <= 0.13),
        "le_0.50pct": sum(1 for c in candidates if c["err_pct"] <= 0.50),
        "le_1.00pct": sum(1 for c in candidates if c["err_pct"] <= 1.00),
        "le_5.00pct": sum(1 for c in candidates if c["err_pct"] <= 5.00),
    }
    return {
        "n_candidates":        len(candidates),
        "band_counts":         band_counts,
        "top_k":               candidates[:top_k],
        "best_err_pct":        candidates[0]["err_pct"] if candidates else None,
        "best_ypower":         candidates[0]["ypower"] if candidates else None,
    }

print("\n" + "="*82)
print("Q4-EXPANDED  —  Y-power sweep 1..40, extended multipliers")
print("="*82)
print(f"Search space: {len(BASES)}*2 * {len(Y_POWERS)+len(OTHER_SCALES)} * "
      f"{len(MULTIPLIERS)} = "
      f"{len(BASES)*2*(len(Y_POWERS)+len(OTHER_SCALES))*len(MULTIPLIERS)} candidates per target\n")

results = {}
for tname, tinfo in TARGETS.items():
    print(f"\n--- {tname}  (target = {float(tinfo['value']):.6e} {tinfo['unit']}) ---")
    r = run_search(tinfo["value"])
    results[tname] = {**r, "target_value": float(tinfo["value"]), "unit": tinfo["unit"]}
    print(f"    candidates: {r['n_candidates']}")
    print(f"    band counts: {r['band_counts']}")
    print(f"    best: {r['best_err_pct']:.4f}%  (Y-power: {r['best_ypower']!r})")
    print(f"    top 5:")
    for i, c in enumerate(r["top_k"]):
        print(f"      [{i+1}] {c['formula']:38s} = {c['value']:.6e}  err={c['err_pct']:.4f}%  Yp={c['ypower']}")

out = Path("/home/z/my-project/results/q4_expanded.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n[ok] Results saved to {out}")
