"""
NQ3 — Out-of-sample predictions.

Push #1 tested in-sample constants (G, α, mp/me, etc.) whose values are well-
known and could have influenced the search design. This script tests:

  1. H_0 (Hubble constant) — current CMB vs SNe tension:
       Planck 2018 CMB:     H_0 = 67.36 ± 0.54 km/s/Mpc
       SH0ES SNe:           H_0 = 73.04 ± 1.04 km/s/Mpc
     Question: does the substrate predict a specific value in this contested range?

  2. W/Z boson mass ratio:
       m_W = 80.379 GeV  (PDG 2024)
       m_Z = 91.1876 GeV
       m_W/m_Z = 0.88153
     Question: does the substrate hit this without it being in the search design?

  3. α drift rate bound:
       Current observational bound: |dα/dt|/α < 10^-17 /yr  (Oklo, atomic clocks)
       Predicted substrate drift (if any): TBD
     Question: does the substrate predict a specific drift rate?

  4. Bonus: λ_QCD (QCD confinement scale) ≈ 200 MeV — unmeasured to high precision

We use the same grammar as Push #1's Phase B. Crucially, NONE of these
constants were used to design the grammar or the substrate, so any hit is
truly out-of-sample.
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

# Sanity: reproduce G_UBP
G_CODATA = F(667430, 10**16)
G_UBP = F(39, 29) * Y**18 / W
print(f"[sanity] G_UBP error = {float(abs(G_UBP - G_CODATA)/G_CODATA*100):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# OUT-OF-SAMPLE TARGETS
# ─────────────────────────────────────────────────────────────────────────────
TARGETS = {
    # H_0 in km/s/Mpc — both CMB and SNe values, and the midpoint
    "H0_CMB_planck":   {"value": F(6736, 100),    "unit": "km/s/Mpc",  "source": "Planck 2018 CMB"},
    "H0_SH0ES_SNe":    {"value": F(7304, 100),    "unit": "km/s/Mpc",  "source": "SH0ES 2022 SNe"},
    "H0_midpoint":     {"value": F((6736+7304), 200), "unit": "km/s/Mpc", "source": "CMB-SNe midpoint"},
    # W/Z mass ratio — dimensionless
    "mW/mZ":           {"value": F(80379, 911876), "unit": "dimensionless", "source": "PDG 2024 (m_W=80.379 GeV / m_Z=91.1876 GeV)"},
    # α drift rate bound — dimensionless per year
    "alpha_drift_bound": {"value": F(1, 10**17), "unit": "per year", "source": "Oklo + atomic clocks bound"},
    # λ_QCD ≈ 200 MeV — but expressed in MeV/c² (use m_e in MeV as unit)
    "lambda_QCD_over_me": {"value": F(200000, 511), "unit": "dimensionless", "source": "λ_QCD ≈ 200 MeV / m_e ≈ 0.511 MeV"},
    # Bonus: neutron-proton mass difference (dimensionless in units of m_e)
    "mn-mp_over_me":    {"value": F(1293, 1000) / F(511, 1000), "unit": "dimensionless", "source": "(m_n - m_p) ≈ 1.293 MeV / m_e ≈ 0.511 MeV"},
    # Bonus: electron g-2 anomaly (the muon g-2 anomaly is currently in tension)
    "g-2_anomaly_mu":   {"value": F(251, 10**9), "unit": "dimensionless", "source": "Fermilab 2021 muon g-2 anomaly ≈ 2.51e-9"},
}

# ─────────────────────────────────────────────────────────────────────────────
# EXPANDED GRAMMAR (same as Push #1 Phase B)
# ─────────────────────────────────────────────────────────────────────────────
BASES = {
    "Y":     Y, "Y_inv": YINV, "L": L, "L_s": L_s,
    "pi":    PI, "phi": PHI, "e": E, "w": W, "U_e": U_e,
    "NRCI":  F(7623, 10000),
}
Y_POWERS = {f"Y^{k}": Y**k for k in range(1, 41)}
Y_POWERS.update({f"Y_inv^{k}": YINV**k for k in range(1, 11)})
OTHER_SCALES = {
    "1/U_e": F(1, U_e), "1/U_e^2": F(1, U_e**2),
    "1/c":   F(1, C),   "1/c^2":   F(1, C**2),
    "1":     F(1, 1),
}
SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)
SQRT3 = u.ExactMath.sqrt_frac(F(3, 1), prec=30)
MULTIPLIERS = {
    "1": F(1,1), "2": F(2,1), "3": F(3,1), "4": F(4,1),
    "8": F(8,1), "12": F(12,1), "24": F(24,1),
    "1/2": F(1,2), "1/3": F(1,3), "1/4": F(1,4),
    "1/8": F(1,8), "1/12": F(1,12), "1/24": F(1,24),
    "sqrt2": SQRT2, "sqrt3": SQRT3,
    "5": F(5,1), "6": F(6,1), "7": F(7,1),
    "1/5": F(1,5), "1/6": F(1,6), "1/7": F(1,7),
    "29": F(29,1), "39": F(39,1), "13": F(13,1),
    "1/29": F(1,29), "1/39": F(1,39), "1/13": F(1,13),
    "169": F(169,1), "2197": F(2197,1),  # 13^2, 13^3
    "1/169": F(1,169), "1/2197": F(1,2197),
}

ALL_SCALES = {**Y_POWERS, **OTHER_SCALES}

# ─────────────────────────────────────────────────────────────────────────────
# RUN SEARCH
# ─────────────────────────────────────────────────────────────────────────────
def run_search(target_value: Fraction, top_k: int = 5):
    candidates = []
    for bn, bv in BASES.items():
        for sn, sv in ALL_SCALES.items():
            for mn, mv in MULTIPLIERS.items():
                for fwd in (True, False):
                    try:
                        b = bv if fwd else (F(1)/bv if bv != 0 else None)
                        if b is None:
                            continue
                        val = mv * b * sv
                        if val > 0:
                            err = abs(val - target_value) / target_value * 100
                            candidates.append({
                                "formula": f"{mn}{'*' if fwd else '/'}{bn}*{sn}",
                                "value":   float(val),
                                "err_pct": float(err),
                                "ypower":  sn if sn.startswith("Y") else "",
                            })
                    except Exception:
                        pass
    candidates.sort(key=lambda c: c["err_pct"])
    return {
        "n_candidates":        len(candidates),
        "band_counts": {
            "le_0.01pct": sum(1 for c in candidates if c["err_pct"] <= 0.01),
            "le_0.05pct": sum(1 for c in candidates if c["err_pct"] <= 0.05),
            "le_0.13pct": sum(1 for c in candidates if c["err_pct"] <= 0.13),
            "le_0.50pct": sum(1 for c in candidates if c["err_pct"] <= 0.50),
            "le_1.00pct": sum(1 for c in candidates if c["err_pct"] <= 1.00),
            "le_5.00pct": sum(1 for c in candidates if c["err_pct"] <= 5.00),
        },
        "top_k":               candidates[:top_k],
        "best_err_pct":        candidates[0]["err_pct"] if candidates else None,
        "best_ypower":         candidates[0]["ypower"] if candidates else None,
    }

print("\n" + "=" * 82)
print("NQ3 — Out-of-sample predictions")
print("=" * 82)
print(f"Search space: {len(BASES)*2*len(ALL_SCALES)*len(MULTIPLIERS)} candidates per target\n")

results = {}
for tname, tinfo in TARGETS.items():
    print(f"\n--- {tname}  (target = {float(tinfo['value']):.6e} {tinfo['unit']}) ---")
    print(f"    source: {tinfo['source']}")
    r = run_search(tinfo["value"])
    results[tname] = {**r, "target_value": float(tinfo["value"]), "unit": tinfo["unit"], "source": tinfo["source"]}
    print(f"    candidates: {r['n_candidates']}")
    print(f"    band counts: {r['band_counts']}")
    print(f"    best: {r['best_err_pct']:.4f}%  (Y-power: {r['best_ypower']!r})")
    print(f"    top 5:")
    for i, c in enumerate(r["top_k"]):
        print(f"      [{i+1}] {c['formula']:42s} = {c['value']:.6e}  err={c['err_pct']:.4f}%  Yp={c['ypower']}")

# ─────────────────────────────────────────────────────────────────────────────
# SPECIAL ANALYSIS — H_0 in CMB-SNe tension range
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 82)
print("H_0 analysis — does the substrate predict a specific value in the tension range?")
print("=" * 82)
# For each candidate formula that hits H_0_CMB within 5%, what value does it predict?
# For each candidate formula that hits H_0_SNe within 5%, what value does it predict?
# Is there a formula whose prediction falls strictly within the tension interval?

# Get top 20 candidates for each H_0 target
h0_cmb_results = run_search(TARGETS["H0_CMB_planck"]["value"], top_k=20)
h0_sne_results = run_search(TARGETS["H0_SH0ES_SNe"]["value"], top_k=20)

# Find formulas that appear in both top-20 lists (would be robust predictions)
cmb_formulas = {c["formula"]: c for c in h0_cmb_results["top_k"]}
sne_formulas = {c["formula"]: c for c in h0_sne_results["top_k"]}
common = set(cmb_formulas.keys()) & set(sne_formulas.keys())
print(f"\nFormulas in BOTH top-20 for H_0_CMB and H_0_SNe: {len(common)}")
for f in list(common)[:5]:
    cmb = cmb_formulas[f]
    sne = sne_formulas[f]
    print(f"  {f}: predicts {cmb['value']:.4f} (CMB err {cmb['err_pct']:.2f}%)  "
          f"or {sne['value']:.4f} (SNe err {sne['err_pct']:.2f}%)")

# Alternative: find the formula that gives a value BETWEEN CMB and SNe
print(f"\nFormulas predicting H_0 strictly in the tension interval [67.36, 73.04]:")
h0_mid = F((6736+7304), 200)
h0_lo = F(6736, 100)
h0_hi = F(7304, 100)

# Sample formulas across the grammar
predictions_in_tension = []
for bn, bv in BASES.items():
    for sn, sv in ALL_SCALES.items():
        for mn, mv in MULTIPLIERS.items():
            for fwd in (True, False):
                try:
                    b = bv if fwd else (F(1)/bv if bv != 0 else None)
                    if b is None:
                        continue
                    val = mv * b * sv
                    if h0_lo <= val <= h0_hi:
                        err_from_mid = abs(val - h0_mid) / h0_mid * 100
                        predictions_in_tension.append({
                            "formula": f"{mn}{'*' if fwd else '/'}{bn}*{sn}",
                            "value": float(val),
                            "err_from_midpoint_pct": float(err_from_mid),
                        })
                except Exception:
                    pass

predictions_in_tension.sort(key=lambda c: c["err_from_midpoint_pct"])
print(f"  Found {len(predictions_in_tension)} formulas predicting H_0 in [67.36, 73.04]")
print(f"  Top 10 (closest to midpoint 70.20):")
for p in predictions_in_tension[:10]:
    print(f"    {p['formula']:42s} = {p['value']:.4f}  err_from_mid={p['err_from_midpoint_pct']:.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# α drift rate — substrate prediction
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 82)
print("α drift rate analysis — does the substrate predict a non-zero drift?")
print("=" * 82)
print("If α = (1/8)·π·Y³ (Push #1 finding, 0.22% err), and Y = π/(π²+2) is substrate-")
print("internal, then any 'drift' in α would correspond to a drift in π. But π is a")
print("mathematical constant. Therefore under the substrate view, α should NOT drift.")
print()
print("This is consistent with the observational bound |dα/dt|/α < 10⁻¹⁷/yr.")
print("The substrate view PREDICTS dα/dt = 0 exactly, which is consistent with but")
print("not more informative than the observational bound.")
print()
print("A falsifiable prediction: if future observations detect dα/dt > 0 above the")
print("current bound, the substrate view would be falsified for α.")

# Save
outp = Path("/home/z/my-project/results/nq3_out_of_sample.json")
with open(outp, "w") as f:
    json.dump({
        "targets": {k: {"value": float(v["value"]), "unit": v["unit"], "source": v["source"]}
                    for k, v in TARGETS.items()},
        "search_results": {k: {kk: vv for kk, vv in v.items() if kk != "top_k"} | {"top_5": v["top_k"][:5]}
                            for k, v in results.items()},
        "h0_tension_predictions": {
            "n_formulas_in_tension_interval": len(predictions_in_tension),
            "top_10_closest_to_midpoint": predictions_in_tension[:10],
        },
        "alpha_drift_analysis": {
            "substrate_prediction": "dα/dt = 0 (since α is substrate-determined and substrate is mathematical)",
            "observational_bound": "|dα/dt|/α < 1e-17 /yr",
            "consistency": "consistent (substrate predicts 0, observational bound is upper limit)",
            "falsifiable": "if dα/dt > 1e-17 /yr detected, substrate view for α is falsified",
        },
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
