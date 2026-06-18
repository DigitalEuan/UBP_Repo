"""
ATLAS INTEGRATION — combine new D-Sink^k/L candidates with the existing
PARTICLE_PHYSICS atlas and produce a unified comparison table.

Output: /home/z/my-project/results/atlas_integration.json
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

pp = u.PARTICLE_PHYSICS
L = pp.L
w = pp.wobble
Y = pp.Y
Y_inv = pp.Y_INV
L_s = pp.L_s
U_e = pp.U_e
phi = pp.phi
e_const = pp.e_const

# Existing atlas (lens-based predictions)
atlas = pp.get_ultimate_predictions()

# New candidate formulas (D-Sink^k/L family and NQ3 out-of-sample hits)
NEW_CANDIDATES = {
    # D-Sink^k / L family
    "m_μ/m_e  (NEW: 13/L = 169/w)":          {"pred": F(13)/L,         "target": F(2067682830, 10**7),    "lens": "D-Sink^1/L"},
    "m_μ/m_e  (ATLAS: 206 + 12L)":            {"pred_atlas_key": "Muon/e- Ratio"},
    "m_τ/m_e  (NEW: 13²/L = 169²/w = 28561/w)": {"pred": F(13)**2/L,    "target": F(3477228280, 10**6),    "lens": "D-Sink^2/L"},
    "m_τ/m_e  (ATLAS: 24D MPG Lever)":        {"pred_atlas_key": "Tau (tau-)"},
    "m_p/m_e  (NEW: 13²/L_s = 2197/(29w/24))":  {"pred": F(13)**2/L_s, "target": F(183615267343, 10**8),  "lens": "D-Sink^2/L_s"},
    "m_p/m_e  (ATLAS: 1836 + 2L_s)":           {"pred_atlas_key": "Proton/e- Ratio"},
    # NQ3 out-of-sample hits
    "m_W/m_Z  (NEW: U_e · Y^9)":              {"pred": F(13824) * Y**9, "target": F(80379, 911876),        "lens": "Existence-Unit × Y^9"},
    "λ_QCD/m_e (NEW: (1/39)/e · Y_inv^8)":    {"pred": F(1,39)/pp.e_const * Y_inv**8, "target": F(200000, 511), "lens": "1/(3·D-Sink·e) · Y_inv^8"},
    "α_drift_bound (NEW: 39·NRCI·Y^32)":      {"pred": F(39)*F(7623,10000)*Y**32, "target": F(1, 10**17),   "lens": "Triad·D-Sink × NRCI × Y^32"},
    "g-2 anomaly (NEW: 13/phi · Y^13)":       {"pred": F(13)/pp.phi * Y**13, "target": F(251, 10**11),     "lens": "D-Sink/φ × Y^13"},
    "(m_n-m_p)/m_e (NEW: 2197/(L·U_e))":      {"pred": F(2197)/(L*F(13824)), "target": F(1293, 511),       "lens": "D-Sink^3 / (L · U_e)"},
    # Push #1's gravity formula (for reference)
    "G (gravity, Push #1: (39/29)·Y^18/w)":   {"pred": F(39,29)*Y**18/w, "target": F(667430, 10**16),   "lens": "Triad·D-Sink/Monster-prime × Y^18/w"},
}

# Build unified comparison table
unified = []
for label, info in NEW_CANDIDATES.items():
    if "pred_atlas_key" in info:
        # Reference existing atlas entry
        key = info["pred_atlas_key"]
        a = atlas[key]
        unified.append({
            "label": label,
            "lens": a["lens"],
            "pred": a["val"],
            "target": a["target"],
            "err_pct": a["error_percent"],
            "source": "ATLAS (existing)",
        })
    else:
        pred = info["pred"]
        target = info["target"]
        err = abs(pred - target) / target * 100
        unified.append({
            "label": label,
            "lens": info["lens"],
            "pred": float(pred),
            "target": float(target),
            "err_pct": float(err),
            "source": "NEW (Push #2)",
        })

# Print summary
print("=" * 100)
print("ATLAS INTEGRATION — existing lens formulas vs new D-Sink/NQ3 candidates")
print("=" * 100)
print(f"\n{'Label':<55} {'Lens':<32} {'Error %':<10} {'Source':<20}")
print("-" * 120)
for u in unified:
    print(f"{u['label']:<55} {u['lens']:<32} {u['err_pct']:<10.4f} {u['source']:<20}")

# Save
outp = Path("/home/z/my-project/results/atlas_integration.json")
with open(outp, "w") as f:
    json.dump({"unified_table": unified}, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
