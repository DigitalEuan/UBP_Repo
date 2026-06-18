"""
D.2 — Atlas-wide reconciliation.

Push #3 Direction 3 showed that the atlas formula 206 + 12·L for m_μ/m_e is a
UBP-canonical refinement of the structural formula 13/L (where 206 = floor(13/L)
and 12 = Leech-rank/2). This script performs the same "unpacking" for every
entry in the PARTICLE_PHYSICS atlas.

For each atlas entry, we:
  1. Identify the embedded integer (e.g., 137 in 137 + L for α⁻¹)
  2. Search for a structural skeleton (clean formula without embedded integers)
     that gives a value close to the target, such that the embedded integer =
     floor() or round() of the skeleton
  3. Compute the optimal correction coefficient α such that
     embedded_integer + α·substrate_correction = skeleton exactly
  4. Check if the atlas's chosen coefficient is UBP-canonical
  5. Compute the "bridge formula" that unifies the structural skeleton and the
     atlas formula

The atlas has 24 entries (per Push #1's inspection of get_ultimate_predictions()).
We focus on the entries with simple lens formulas:
  - Alpha Inv:           220 - 83 + L = 137 + L
  - Proton/e- Ratio:     1836 + 2·L_s
  - Muon/e- Ratio:       206 + 12·L  (already reconciled in Push #3)
  - Electron (e-):       24·Y/(4π) + L·7/80
  - Tau (tau-):          (17·Y_inv⁴ + 2·Y_inv + Y + Y_inv·24/23 + 8·Y) × m_e
  - Higgs Boson:         U_e·(9 + L)
  - Top Quark:           25/2·U_e - 12·Y + L
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
pi = pp.pi
phi = pp.phi
e_const = pp.e_const

# Get the atlas
atlas = pp.get_ultimate_predictions()

# ─────────────────────────────────────────────────────────────────────────────
# For each atlas entry with a simple lens formula, unpack it
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 80)
print("D.2 — Atlas-wide reconciliation")
print("=" * 80)
print("\nFor each atlas entry with a simple lens formula, we identify:")
print("  (a) the embedded integer")
print("  (b) a structural skeleton whose floor/round gives that integer")
print("  (c) the optimal correction coefficient α")
print("  (d) whether the atlas's chosen coefficient is UBP-canonical")
print()

# Define candidate structural skeletons (from Push #1 Phase B top-5 lists)
# These are the best clean formulas for each target
SKELETONS = {
    "Alpha Inv": [
        ("8/π·Y_inv³",         F(8) / pi * Y_inv**3),    # Push #1 best
        ("Y_inv³·8/π",         Y_inv**3 * F(8) / pi),
        ("24·Y^6·U_e",         F(24) * Y**6 * U_e),       # alt
        ("Y_inv·24",           Y_inv * 24),                # simpler
    ],
    "Proton/e- Ratio": [
        ("(1/6)/Y·Y_inv⁶",     F(1,6) / Y * Y_inv**6),   # Push #1 best
        ("(1/6)·Y_inv⁵",       F(1,6) * Y_inv**5),
        ("U_e·Y_inv³/2",       U_e * Y_inv**3 / 2),
        ("U_e/2·Y",            U_e / 2 * Y),               # Push #1 #5
    ],
    "Muon/e- Ratio": [
        ("13/L = 169/w",       F(13) / L),                 # Push #2 best (already reconciled)
        ("13²/w",              F(169) / w),
    ],
    "Electron (e-)": [
        # Atlas uses 24·Y/(4π) + L·7/80 = 6Y/π + 7L/80
        # Target m_e = 0.51099895 MeV (as Fraction)
        ("Y²·5·U_e/12",        Y**2 * 5 * U_e / 12),
        ("L·13/2",             L * 13 / 2),
        ("Y·L·U_e/2",          Y * L * U_e / 2),
    ],
    "Muon (mu-)": [
        # Atlas: m_mu = (206 + 12L) × m_e_target
        # Same structural skeleton as Muon/e- Ratio (since m_e_target is fixed)
        ("13/L × m_e_target",  F(13) / L * F(51099895, 100000000)),
    ],
    "Tau (tau-)": [
        # Atlas uses complex Y_inv formula. Push #1 best was 6/e·Y_inv⁹
        ("6/e·Y_inv⁹",         F(6) / e_const * Y_inv**9),
        ("Y_inv⁹·6/e",         Y_inv**9 * F(6) / e_const),
    ],
    "Proton (p+)": [
        # Atlas: m_p = (1836 + 2·L_s) × m_e_target
        ("(1/6)/Y·Y_inv⁶ × m_e",  F(1,6) / Y * Y_inv**6 * F(51099895, 100000000)),
    ],
    "Neutron (n0)": [
        # Atlas: m_p + g13_isospin where g13_isospin = (Y_inv·L + Y/2)·(Y_inv - Y)
        ("m_p_struct + (Y_inv·L + Y/2)·(Y_inv - Y)",
         (F(1,6)/Y*Y_inv**6 + (Y_inv*L + Y/2)*(Y_inv - Y)) * F(51099895, 100000000)),
    ],
    "Higgs Boson": [
        # Atlas: U_e·(9 + L) = 13824·(9 + 0.0629) = 125292.7 (target 125250)
        # Structural skeleton? 9 = ?
        # U_e·9 = 124416; U_e·L = 869.5; total 125285.5
        # Can we derive 9 structurally? 9 = U_e^(1/3) - 15 = 24 - 15? Or 9 = (Leech rank - 15)?
        ("U_e·(Y_inv + 8)",    U_e * (Y_inv + 8)),         # Y_inv ≈ 3.78, +8 = 11.78, ×13824 ≈ 162864 (too big)
        ("U_e·(L_s·12 + 8)",   U_e * (L_s * 12 + 8)),      # alt
        ("U_e·(8 + L·U_e^0)",  U_e * (8 + L)),             # 9 replaced by 8+L = 8.063
    ],
    "Top Quark": [
        # Atlas: 25/2·U_e - 12·Y + L = 12.5·13824 - 3.176 + 0.063 = 172800 - 3.113 = 172796.9
        # Target 172760. Structural skeleton?
        ("25/2·U_e",           F(25, 2) * U_e),            # = 172800 (close to 172760)
        ("12.5·U_e - Y_inv",   F(25, 2) * U_e - Y_inv),
    ],
}

# Process each atlas entry
results = {}
for atlas_key, skeleton_candidates in SKELETONS.items():
    print(f"\n--- {atlas_key} ---")
    if atlas_key not in atlas:
        print(f"  (not in atlas)")
        continue
    a = atlas[atlas_key]
    target_val = F(a["target"]).limit_denominator(10**15) if not isinstance(a["target"], F) else a["target"]
    # Atlas stores target as float; reconstruct as Fraction
    target_float = a["target"]
    # Use the Fraction target from the atlas source directly
    # Atlas source uses F(n, d) for targets; we can recover from get_ultimate_predictions internal data
    # For simplicity, use float and convert
    target = F(target_float).limit_denominator(10**12)

    atlas_pred = a["val"]
    atlas_err = a["error_percent"]
    lens = a["lens"]
    print(f"  Target: {target_float:.6f}  (atlas lens: {lens})")
    print(f"  Atlas prediction: {atlas_pred:.6f}  (err {atlas_err:.4f}%)")

    # Find the best structural skeleton
    best_skeleton = None
    best_skeleton_err = float('inf')
    for name, skel in skeleton_candidates:
        try:
            skel_val = float(skel)
            err = abs(skel_val - target_float) / target_float * 100
            if err < best_skeleton_err:
                best_skeleton_err = err
                best_skeleton = (name, skel, skel_val, err)
        except Exception as e:
            print(f"    skeleton {name}: error {e}")

    if best_skeleton is None:
        print(f"  No valid skeleton found")
        continue

    skel_name, skel_frac, skel_val, skel_err = best_skeleton
    print(f"  Best structural skeleton: {skel_name} = {skel_val:.6f}  (err {skel_err:.4f}%)")

    # Compute the embedded integer (floor or round of skeleton)
    floor_val = int(skel_val)
    round_val = round(skel_val)
    print(f"    floor(skeleton) = {floor_val}")
    print(f"    round(skeleton) = {round_val}")

    # Which integer appears in the atlas formula?
    # We need to extract this from the atlas lens name or formula
    # For the user-provided examples:
    #   α⁻¹ = 137 + L → integer 137 = floor(8/π·Y_inv³) = floor(137.34) = 137 ✓
    #   m_μ/m_e = 206 + 12·L → integer 206 = floor(13/L) = floor(206.71) = 206 ✓
    #   m_p/m_e = 1836 + 2·L_s → integer 1836 = round((1/6)/Y·Y_inv⁶) = round(1831.7) = 1832 ≠ 1836 ✗

    # Check floor and round against the atlas formula's embedded integer
    # The atlas formula structure is "integer + correction" — extract integer from lens name
    import re
    # Common patterns: "137 + L", "206 + 12L", "1836 + 2·L_s", "220 - 83 + L"
    embedded_int = None
    if atlas_key == "Alpha Inv":
        embedded_int = 137  # 220 - 83 + L = 137 + L
    elif atlas_key == "Proton/e- Ratio":
        embedded_int = 1836
    elif atlas_key == "Muon/e- Ratio":
        embedded_int = 206
    elif atlas_key == "Higgs Boson":
        embedded_int = 9  # U_e·(9 + L) — integer 9
    elif atlas_key == "Top Quark":
        embedded_int = None  # 25/2·U_e - 12·Y + L — no simple embedded integer
    elif atlas_key == "Electron (e-)":
        embedded_int = None  # 24·Y/(4π) + L·7/80 — no embedded integer
    elif atlas_key == "Tau (tau-)":
        embedded_int = None  # complex Y_inv formula
    elif atlas_key in ("Muon (mu-)", "Proton (p+)", "Neutron (n0)"):
        # These use mass ratios × m_e_target; the integer comes from the ratio
        if atlas_key == "Muon (mu-)":
            embedded_int = 206
        elif atlas_key == "Proton (p+)":
            embedded_int = 1836
        elif atlas_key == "Neutron (n0)":
            embedded_int = 1836  # m_p + g13_isospin

    if embedded_int is not None:
        floor_match = (floor_val == embedded_int)
        round_match = (round_val == embedded_int)
        print(f"  Atlas embedded integer: {embedded_int}")
        print(f"    = floor(skeleton)? {'YES' if floor_match else 'NO (floor=' + str(floor_val) + ')'}")
        print(f"    = round(skeleton)? {'YES' if round_match else 'NO (round=' + str(round_val) + ')'}")

        # Compute the optimal correction coefficient α
        # such that embedded_int + α·correction = skeleton exactly
        # We need to identify the "correction" substrate term in the atlas formula
        # For m_μ/m_e: correction = L, atlas uses α=12
        # For α⁻¹: correction = L, atlas uses α=1
        # For m_p/m_e: correction = L_s, atlas uses α=2
        # For Higgs: correction = L (atlas uses U_e·(9 + L), so correction = L, α=U_e)

        if atlas_key in ("Alpha Inv", "Muon/e- Ratio", "Muon (mu-)"):
            correction_term = L
            correction_name = "L"
        elif atlas_key in ("Proton/e- Ratio", "Proton (p+)", "Neutron (n0)"):
            correction_term = L_s
            correction_name = "L_s"
        elif atlas_key == "Higgs Boson":
            correction_term = L
            correction_name = "L"
        else:
            correction_term = None
            correction_name = None

        if correction_term is not None and correction_term != 0:
            # α_optimal = (skeleton - embedded_int) / correction_term
            alpha_opt = (skel_frac - F(embedded_int)) / correction_term
            print(f"  Correction term: {correction_name}")
            print(f"  Optimal α: (skeleton - {embedded_int}) / {correction_name} = {float(alpha_opt):.6f} = {alpha_opt}")

            # Atlas's chosen α
            atlas_alpha = {"Alpha Inv": 1, "Muon/e- Ratio": 12, "Muon (mu-)": 12,
                           "Proton/e- Ratio": 2, "Proton (p+)": 2, "Neutron (n0)": 2,
                           "Higgs Boson": U_e}.get(atlas_key)
            if atlas_alpha is not None:
                if isinstance(atlas_alpha, F):
                    print(f"  Atlas α: {atlas_alpha} = {float(atlas_alpha):.6f}")
                else:
                    print(f"  Atlas α: {atlas_alpha}")
                # Difference
                diff = float(F(atlas_alpha) - alpha_opt) if not isinstance(atlas_alpha, F) else float(atlas_alpha - alpha_opt)
                print(f"  Difference (atlas - optimal): {diff:.6f}")

                # Is atlas α UBP-canonical?
                ubp_canonical_alphas = {1, 2, 3, 4, 6, 8, 12, 13, 24, 29, 39}
                if isinstance(atlas_alpha, F) and atlas_alpha.denominator == 1:
                    is_canonical = int(atlas_alpha) in ubp_canonical_alphas
                elif isinstance(atlas_alpha, int):
                    is_canonical = atlas_alpha in ubp_canonical_alphas
                else:
                    is_canonical = False  # U_e is not in the small set
                print(f"  Atlas α UBP-canonical? {'YES' if is_canonical else 'NO (or non-integer)'}")

                # Bridge formula: embedded_int + α_optimal·correction = skeleton
                bridge_pred = F(embedded_int) + alpha_opt * correction_term
                bridge_err = abs(float(bridge_pred) - target_float) / target_float * 100
                print(f"  Bridge formula: {embedded_int} + ({alpha_opt})·{correction_name} = {float(bridge_pred):.6f}  (err {bridge_err:.6f}%)")
                print(f"  → Bridge formula matches skeleton: {'YES' if abs(float(bridge_pred) - skel_val) < 1e-9 else 'NO'}")

    results[atlas_key] = {
        "target": target_float,
        "atlas_pred": atlas_pred,
        "atlas_err_pct": atlas_err,
        "atlas_lens": lens,
        "structural_skeleton": skel_name,
        "skeleton_value": skel_val,
        "skeleton_err_pct": skel_err,
        "embedded_integer": embedded_int,
        "floor_of_skeleton": floor_val,
        "round_of_skeleton": round_val,
        "floor_match": floor_match if embedded_int else None,
        "round_match": round_match if embedded_int else None,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("SUMMARY — Atlas-wide reconciliation")
print("=" * 80)
print(f"\n{'Atlas entry':<22} {'Embedded int':<14} {'Skeleton':<25} {'floor(skel)':<14} {'round(skel)':<14} {'Match?':<10}")
print("-" * 100)
for key, r in results.items():
    if r["embedded_integer"] is None:
        print(f"{key:<22} {'(none)':<14} {r['structural_skeleton'][:24]:<25} {'—':<14} {'—':<14} {'—':<10}")
    else:
        match = "floor" if r["floor_match"] else ("round" if r["round_match"] else "NEITHER")
        print(f"{key:<22} {r['embedded_integer']:<14} {r['structural_skeleton'][:24]:<25} {r['floor_of_skeleton']:<14} {r['round_of_skeleton']:<14} {match:<10}")

# Save
outp = Path("/home/z/my-project/results/d2_atlas_reconciliation.json")
with open(outp, "w") as f:
    json.dump({"atlas_reconciliation": results}, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
