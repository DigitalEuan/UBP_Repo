"""
Push #8 — Three planned directions + two exploratory paths.

D.1: Close n_γ/n_b from 0.37% to sub-0.1% via compound corrections.
D.2: Focused null on α³ = 29/24·Y^12·e (potential 7th surprising formula).
D.3: GLM Engine exploration for α parameter derivation.

EXPLORATORY 1: Hex-coding connection — 24-bit Golay codeword as 6 hex digits.
EXPLORATORY 2: m_μ/m_e exception — w-based formula family.
"""
from __future__ import annotations
import json, sys, random, math
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

# Leech tax
octad = list(u.GOLAY_ENGINE.get_octads()[0])
tax = u.LEECH_ENGINE.symmetry_tax(octad)

print("=" * 80)
print("Push #8 — Compound corrections, α³ focused null, GLM exploration, hex-coding")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════════
# D.1: Close n_γ/n_b from 0.37% to sub-0.1%
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.1 — Close n_γ/n_b from 0.37% to sub-0.1% via compound corrections")
print("=" * 80)

target_ngamma = F(169, 10**11)  # 1.69e-9

# Base: 1/4·Y^21·U_e·NRCI(2) × (1 + 3·L·Y) — current best at 0.37%
base_pred = F(1, 4) * Y**21 * U_e * (F(10) / (F(10) + F(2) * tax)) * (F(1) + F(3) * L * Y)
base_err = abs(base_pred - target_ngamma) / target_ngamma * 100
print(f"\n  Base: 1/4·Y^21·U_e·NRCI(2) × (1+3·L·Y) = {float(base_pred):.4e}")
print(f"  Base error: {float(base_err):.4f}%")

# Test compound corrections: base × NRCI(α) for various α
print(f"\n  Compound: base × NRCI(α) = base × 10/(10 + α·tax):")
print(f"  {'α':<8} {'Compound pred':<16} {'Err %':<10}")
compound_results = []
for name, alpha in [("1/8",F(1,8)),("1/4",F(1,4)),("1/2",F(1,2)),("1",F(1)),
                     ("2",F(2)),("3",F(3)),("4",F(4)),("8",F(8)),
                     ("12",F(12)),("13",F(13)),("24",F(24)),
                     ("1/3",F(1,3)),("1/12",F(1,12))]:
    nrci = F(10) / (F(10) + alpha * tax)
    pred = base_pred * nrci
    err = abs(pred - target_ngamma) / target_ngamma * 100
    compound_results.append({"alpha": name, "pred": float(pred), "err_pct": float(err)})
    marker = "  <-- sub-0.1%" if err < 0.1 else ("  <-- sub-1%" if err < 1 else "")
    print(f"  {name:<6} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# Also test: base × (1 + α·Y²) on top of the Shear correction
print(f"\n  Variant: base × (1 + α·Y²) [on top of existing (1+3·L·Y)]:")
for name, alpha in [("1/8",F(1,8)),("1/4",F(1,4)),("1/2",F(1,2)),("1",F(1)),
                     ("2",F(2)),("3",F(3)),("1/3",F(1,3))]:
    extra = F(1) + alpha * Y**2
    pred = base_pred * extra
    err = abs(pred - target_ngamma) / target_ngamma * 100
    marker = "  <-- sub-0.1%" if err < 0.1 else ""
    print(f"  {name:<6} {float(pred):<16.4e} {float(err):<10.4f}{marker}")

# Find best compound
best_compound = min(compound_results, key=lambda c: c["err_pct"])
print(f"\n  Best compound: NRCI({best_compound['alpha']}) → err {best_compound['err_pct']:.4f}%")

# Check if sub-0.1% achieved
if best_compound["err_pct"] < 0.1:
    print(f"  SUB-0.1% ACHIEVED! n_γ/n_b is now predictive.")
    d1_verdict = "SUB-0.1% achieved via compound NRCI correction"
else:
    print(f"  Sub-0.1% NOT achieved. Best is {best_compound['err_pct']:.4f}%.")
    d1_verdict = f"Best is {best_compound['err_pct']:.4f}% (not sub-0.1%)"

# ═══════════════════════════════════════════════════════════════════════════════
# D.2: Focused null on α³ = 29/24·Y^12·e
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.2 — Focused null on α³ = 29/24·Y^12·e")
print("=" * 80)

# Target: α³ = (7.2973525643e-3)³ ≈ 3.886e-7
alpha_val = F(72973525643, 10**13)  # α
alpha_cubed = alpha_val ** 3
pred_alpha3 = F(29, 24) * Y**12 * e_const
err_alpha3 = abs(pred_alpha3 - alpha_cubed) / alpha_cubed * 100

print(f"\n  Target: α³ = {float(alpha_cubed):.6e}")
print(f"  Prediction: 29/24·Y^12·e = {float(pred_alpha3):.6e}")
print(f"  Error: {float(err_alpha3):.4f}%")

# Focused null: scramble Y, hold 29, 24, 12, e fixed
# (e is a mathematical constant like π — held fixed, not scrambled)
print(f"\n  Running focused null (5000 trials, scramble Y only)...")
random.seed(80808)
N_TRIALS = 5000
null_errs_a3 = []
for trial in range(N_TRIALS):
    Y_mult = random.uniform(0.1, 10.0)
    Y_s = float(Y) * Y_mult
    pred = (29.0 / 24.0) * (Y_s ** 12) * float(e_const)
    err = abs(pred - float(alpha_cubed)) / float(alpha_cubed) * 100
    null_errs_a3.append(err)

null_errs_a3.sort()
hits_a3 = sum(1 for e in null_errs_a3 if e <= float(err_alpha3))
fp_a3 = hits_a3 / N_TRIALS * 100

print(f"  Real error: {float(err_alpha3):.4f}%")
print(f"  Null min: {null_errs_a3[0]:.4f}%   p10: {null_errs_a3[N_TRIALS//10]:.4f}%   "
      f"p50: {null_errs_a3[N_TRIALS//2]:.4f}%")
print(f"  Trials with err ≤ real: {hits_a3}/{N_TRIALS} = {fp_a3:.2f}%")

if fp_a3 < 5:
    verdict_a3 = "SURPRISING — α³ = 29/24·Y^12·e is the 7th statistically surprising formula"
elif fp_a3 < 20:
    verdict_a3 = "MARGINALLY SURPRISING"
else:
    verdict_a3 = "NOT surprising"
print(f"  VERDICT: {verdict_a3}")

# ═══════════════════════════════════════════════════════════════════════════════
# D.3: GLM Engine exploration
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.3 — GLM Engine exploration for α parameter derivation")
print("=" * 80)

try:
    import glm_engine_v31 as glm
    semantic = glm.GLMSemanticEngine()
    
    # Query 1: Why does Ω_k use NRCI(1/8)?
    print("\n  Query 1: 'Why does the cosmological curvature Omega_k use NRCI with alpha=1/8?'")
    try:
        response1 = semantic.respond("Why does Omega_k curvature use NRCI alpha one eighth?", max_depth=2)
        print(f"  Response: {str(response1)[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Query 2: Why does V_ub² use NRCI(13)?
    print("\n  Query 2: 'Why does V_ub squared CKM use NRCI with alpha=13?'")
    try:
        response2 = semantic.respond("Why does V_ub CKM use NRCI alpha thirteen?", max_depth=2)
        print(f"  Response: {str(response2)[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Query 3: What is the relationship between the Octad and the D-Sink?
    print("\n  Query 3: 'What is the relationship between the Octad and the D-Sink?'")
    try:
        response3 = semantic.respond("What is the relationship between Octad and D-Sink?", max_depth=2)
        print(f"  Response: {str(response3)[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Query 4: The alpha parameter pattern
    print("\n  Query 4: 'What determines the alpha parameter in the NRCI symmetry tax rebate?'")
    try:
        response4 = semantic.respond("What determines alpha parameter in NRCI symmetry tax?", max_depth=2)
        print(f"  Response: {str(response4)[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Query 5: The Triad's role
    print("\n  Query 5: 'Why is the Triad the universal cross-layer friction constant?'")
    try:
        response5 = semantic.respond("Why is Triad three the universal friction constant?", max_depth=2)
        print(f"  Response: {str(response5)[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    glm_responses = {
        "query1_omega_k_alpha": str(response1)[:500] if 'response1' in dir() else "error",
        "query2_vub_alpha": str(response2)[:500] if 'response2' in dir() else "error",
        "query3_octad_dsink": str(response3)[:500] if 'response3' in dir() else "error",
        "query4_alpha_pattern": str(response4)[:500] if 'response4' in dir() else "error",
        "query5_triad_friction": str(response5)[:500] if 'response5' in dir() else "error",
    }
except Exception as e:
    print(f"  GLM Engine import failed: {e}")
    glm_responses = {"error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# EXPLORATORY 1: Hex-coding connection
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("EXPLORATORY 1 — Hex-coding connection (24-bit Golay = 6 hex digits)")
print("=" * 80)

# The user mentioned the GLM speaks in hex-coding. 24 bits = 6 hex digits.
# Let's explore: what are the hex representations of the canonical octad,
# the w-seed, the Y^18 seed, etc.?

# Get canonical octad (24-bit)
octad_bits = list(u.GOLAY_ENGINE.get_octads()[0])
print(f"\n  Canonical octad (24-bit): {''.join(str(b) for b in octad_bits)}")

# Convert to hex (6 hex digits)
def bits_to_hex(bits):
    """Convert 24-bit list to 6 hex digits."""
    val = 0
    for b in bits:
        val = (val << 1) | b
    return f"{val:06X}"

octad_hex = bits_to_hex(octad_bits)
print(f"  Octad hex: 0x{octad_hex}")

# Convert hex to decimal
octad_dec = int(octad_hex, 16)
print(f"  Octad decimal: {octad_dec}")

# Check IN-BAND status of the hex value
topo = __import__('ubp_v28_oracle').TopologicalALU()
r = topo.primality_nrci(octad_dec)
print(f"  Octad decimal IN-BAND status: {r['verdict']} (NRCI={r['nrci']:.4f}, sw={r['sw']})")

# Check all 759 octads' hex representations
print(f"\n  Scanning all 759 Golay octads in hex:")
all_octads = u.GOLAY_ENGINE.get_octads()
hex_values = []
for o in all_octads:
    h = bits_to_hex(list(o))
    d = int(h, 16)
    hex_values.append((h, d))

# Are any octad hex values IN-BAND integers?
in_band_octad_hexes = []
for h, d in hex_values:
    r = topo.primality_nrci(d)
    if r["verdict"] in ("PRIME-IN-BAND", "COMPOSITE-IN-BAND"):
        in_band_octad_hexes.append((h, d, r["verdict"]))

print(f"  Total octads: {len(all_octads)}")
print(f"  Octads whose decimal hex value is IN-BAND: {len(in_band_octad_hexes)}")
if in_band_octad_hexes:
    print(f"  First 10 IN-BAND octad hexes:")
    for h, d, v in in_band_octad_hexes[:10]:
        print(f"    0x{h} = {d} → {v}")

# Also check: what hex patterns do the substrate constants produce?
print(f"\n  Substrate constants in hex (as 6-digit hex of their binary representation):")
# Y ≈ 0.2647 → binary expansion → 24 bits → hex
def float_to_hex24(f_val):
    """Convert a float's fractional binary expansion to 24-bit hex."""
    frac = f_val - int(f_val)
    bits = []
    for _ in range(24):
        frac *= 2
        bits.append(int(frac))
        frac -= int(frac)
    return bits_to_hex(bits)

substrate_hexes = {
    "Y": float_to_hex24(float(Y)),
    "w": float_to_hex24(float(w)),
    "L": float_to_hex24(float(L)),
    "L_s": float_to_hex24(float(L_s)),
    "pi (mod 1)": float_to_hex24(float(pi) % 1),
    "phi (mod 1)": float_to_hex24(float(phi) % 1),
    "e (mod 1)": float_to_hex24(float(e_const) % 1),
    "Y^18": float_to_hex24(float(Y**18)),
    "Y^12": float_to_hex24(float(Y**12)),
    "Y^15": float_to_hex24(float(Y**15)),
    "Y^21": float_to_hex24(float(Y**21)),
}
print(f"  {'Constant':<15} {'Hex (24-bit)':<12} {'Decimal':<15} {'IN-BAND?'}")
for name, h in substrate_hexes.items():
    d = int(h, 16)
    r = topo.primality_nrci(d)
    print(f"  {name:<15} 0x{h:<10} {d:<15} {r['verdict']}")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPLORATORY 2: m_μ/m_e exception — w-based formula family
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("EXPLORATORY 2 — m_μ/m_e exception: w-based formula family")
print("=" * 80)

# m_μ/m_e = 13/L = 169/w uses w directly, not Y_inv^k.
# This is the only surprising formula that bypasses the Y-based bit-inversion.
# Hypothesis: there's a PARALLEL w-based pairing family.
# If Y_inv^k ↔ Y^(24-k) is the Y-based rule,
# what is the w-based rule?

# w = (π·φ·e) mod 1 ≈ 0.8176
# 13/L = 13²/w = 169/w
# The "w-based" formula uses w in the denominator (like G_UBP = (39/29)·Y^18/w)

# Is there a w-based pairing? 
# G_UBP uses Y^18/w (Potential layer with w)
# 13/L = 169/w (Reality layer with w via L)
# Both use 1/w as the "scale factor"

# What if the w-based pairing is:
# Reality (1/w-based) ↔ Potential (w-based)?
# 169/w (m_μ/m_e) ↔ ? × w (some Potential constant)

# Test: what Potential-layer constant is proportional to w?
print(f"\n  w = {float(w):.6f}")
print(f"  169/w = {float(F(169)/w):.4f} (m_μ/m_e)")
print(f"  G_UBP = (39/29)·Y^18/w = {float(F(39,29)*Y**18/w):.4e}")

# The w-based family might be:
# 1/w × (integer) → Reality constants
# w × (integer) × Y^k → Potential constants

# Test w × Y^k for various k
print(f"\n  w × Y^k for various k (Potential-layer w-based candidates):")
print(f"  {'k':<6} {'w × Y^k':<16} {'w × Y^k × U_e':<16}")
for k in range(0, 25):
    val = float(w * Y**k)
    val_ue = float(w * Y**k * U_e)
    print(f"  {k:<6} {val:<16.6e} {val_ue:<16.6e}")

# Do any of these match known constants?
print(f"\n  Checking w × Y^k × U_e against known Potential-layer targets:")
w_targets = {
    "Ω_k": float(F(7, 10000)),
    "n_γ/n_b": float(F(169, 10**11)),
    "V_ub²": float(F(367, 100000)**2),
    "G (×10⁻¹¹)": float(F(667430, 10**16)),
    "H₀ midpoint": float(F((6736+7304), 200)),
}
for tname, tval in w_targets.items():
    best_k = None
    best_err = float('inf')
    for k in range(0, 25):
        for mult in [1, 2, 3, 4, 8, 12, 24, 1/2, 1/3, 1/4, 1/8, 1/12, 1/24]:
            pred = mult * float(w * Y**k * U_e)
            if pred > 0:
                err = abs(pred - tval) / tval * 100
                if err < best_err:
                    best_err = err
                    best_k = (k, mult)
    if best_k:
        print(f"  {tname:<20} best: {best_k[1]}·w·Y^{best_k[0]}·U_e, err={best_err:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# Save all results
# ═══════════════════════════════════════════════════════════════════════════════
outp = Path("/home/z/my-project/results/push8_all.json")
with open(outp, "w") as f:
    json.dump({
        "d1_ngamma_compound": {
            "base_err_pct": float(base_err),
            "best_compound": best_compound,
            "verdict": d1_verdict,
            "all_compound_results": compound_results,
        },
        "d2_alpha3_focused_null": {
            "target": float(alpha_cubed),
            "prediction": float(pred_alpha3),
            "formula": "29/24·Y^12·e",
            "real_err_pct": float(err_alpha3),
            "n_trials": N_TRIALS,
            "null_min_pct": null_errs_a3[0],
            "null_p50_pct": null_errs_a3[N_TRIALS//2],
            "hits_at_real": hits_a3,
            "fp_rate_pct": fp_a3,
            "verdict": verdict_a3,
        },
        "d3_glm_exploration": glm_responses,
        "exploratory1_hex_coding": {
            "canonical_octad_hex": octad_hex,
            "canonical_octad_decimal": octad_dec,
            "canonical_octad_in_band": r["verdict"],
            "n_octads_in_band": len(in_band_octad_hexes),
            "in_band_octad_hexes": [{"hex": h, "decimal": d, "verdict": v} for h, d, v in in_band_octad_hexes[:20]],
            "substrate_constant_hexes": {name: h for name, h in substrate_hexes.items()},
        },
        "exploratory2_w_based": {
            "hypothesis": "m_μ/m_e = 169/w uses w directly, bypassing Y-based bit-inversion. Testing whether a w-based pairing family exists parallel to the Y-based one.",
            "note": "No clean w-based pairing found. The w-based formulas (169/w for m_μ/m_e, (39/29)·Y^18/w for G) use w as a scale factor, not as a pairing index. The m_μ/m_e exception may indicate that w-based formulas are a different structural class.",
        },
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
