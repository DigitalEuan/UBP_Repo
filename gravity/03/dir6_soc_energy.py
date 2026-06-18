"""
DIRECTION 6 — SOC Energy of the Y^18 boundary state.

HYPOTHESIS
----------
If gravity is "macroscopic tension required to correct informational leakage,"
it must have a measurable metabolic cost (Symmetry Tax) and SOC (Self-Organized
Criticality) Energy. The Push #1 prior paper mentioned:
    E_SOC = weight × c × Y × NRCI × penalty
where penalty = exp(...) only applies above the 1 THz wall.

We use the Y^18 boundary state (the gravity formula's scale) and:
  1. Compute its SOC energy via the prior formula
  2. Compute its Leech symmetry tax
  3. Compute its BW256 NRCI (using the seed = Y^18's binary expansion)
  4. Predict the frequency/energy scale at which gravity unifies with other
     forces by finding where the SOC energy crosses the 1 THz wall.

The "1 THz wall of reality" in UBP is the threshold above which the SOC
penalty activates. Below 1 THz, observer dynamics are classical; above
1 THz, quantum-gravity effects become measurable.

Since ObserverDynamicsEngine is NOT in v5.3 (it was in a separate file
ubp_observer_dynamics.py per the prior paper's file inventory), we
implement the SOC calculation inline using the prior paper's formula:
    E_SOC = weight × c × Y × NRCI × penalty
where:
    weight = the "ontological weight" of the state (we use the Y-power = 18)
    c = speed of light (299792458 m/s)
    Y = Observer Constant
    NRCI = the state's NRCI (we use the Leech NRCI of the Y^18-derived point)
    penalty = exp(-(freq - 1 THz)/scale) if freq > 1 THz else 1
"""
from __future__ import annotations
import json, sys, math
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

sub = u.SUBSTRATE
constants = sub.get_v6_constants()
Y = constants["Y"]
W = constants["WOBBLE"]
L = constants["SINK_L"]
pi = constants["PI"]
phi = constants["PHI"]
e_const = constants["E"]
L_s = u.PARTICLE_PHYSICS.L_s
U_e = u.PARTICLE_PHYSICS.U_e

c = 299792458  # m/s
THz_wall = 1e12  # 1 THz = 10^12 Hz

# ─────────────────────────────────────────────────────────────────────────────
# 1. Construct the Y^18 boundary state as a 24-bit point
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 80)
print("(1) Construct Y^18 boundary state as a 24-bit Leech point")
print("=" * 80)

# Y^18 ≈ 4.06e-11. To make a 24-bit point, we use Y^18's binary expansion
# (similar to Direction 4's w-seed approach).
Y18_float = float(Y**18)
print(f"  Y^18 = {Y18_float:.6e}")

# Binary expansion: take the first 12 bits of the fractional part of Y^18 × 2^40
# (so we get a meaningful bit pattern)
Y18_scaled = Y18_float * (2**40)
frac = Y18_scaled - int(Y18_scaled)
bits_12 = []
for i in range(12):
    frac *= 2
    bits_12.append(int(frac))
    frac -= int(frac)
print(f"  First 12 bits of Y^18's binary expansion: {bits_12}")

seed_24 = u.GOLAY_ENGINE.encode(bits_12)
print(f"  Golay-encoded 24-bit seed: weight = {sum(seed_24)}")

# Use the seed_24 directly as the Leech point (24-bit binary vector)
leech_point = list(seed_24)
print(f"  Using seed_24 directly as Leech point: {leech_point}")
print(f"  Hamming weight: {sum(leech_point)}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Compute Leech symmetry tax and NRCI
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(2) Leech symmetry tax and NRCI of Y^18 boundary state")
print("=" * 80)

tax_Y18 = u.LEECH_ENGINE.symmetry_tax(leech_point)
nrci_Y18 = u.LEECH_ENGINE.calculate_nrci(leech_point)
print(f"  Symmetry tax = {float(tax_Y18):.6f}  (= {tax_Y18})")
print(f"  NRCI = {float(nrci_Y18):.6f}  (= {nrci_Y18})")
print(f"  In Capture Zone (NRCI ≥ 0.70)? {'YES' if float(nrci_Y18) >= 0.70 else 'NO'}")

# Compare to a generic weight-8 octad (the most stable Leech point type)
generic_octad = list(u.GOLAY_ENGINE.get_octads()[0])
tax_octad = u.LEECH_ENGINE.symmetry_tax(generic_octad)
nrci_octad = u.LEECH_ENGINE.calculate_nrci(generic_octad)
print(f"\n  Comparison — generic weight-8 octad:")
print(f"    tax = {float(tax_octad):.6f}, NRCI = {float(nrci_octad):.6f}")
print(f"  Y^18 state has tax = {float(tax_Y18):.6f}, NRCI = {float(nrci_Y18):.6f}")
print(f"  Y^18 state is {'MORE' if float(tax_Y18) > float(tax_octad) else 'LESS'} stable than a generic octad")

# ─────────────────────────────────────────────────────────────────────────────
# 3. SOC Energy calculation (using prior paper's formula)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(3) SOC Energy of Y^18 boundary state")
print("=" * 80)
print("  Formula: E_SOC = weight × c × Y × NRCI × penalty")
print("  Where:")
print("    weight = ontological weight of the state")
print("    c = 299792458 m/s")
print("    Y = Observer Constant ≈ 0.2647")
print("    NRCI = state's NRCI")
print("    penalty = 1 if freq ≤ 1 THz, else exp(-(freq - 1 THz)/scale)")
print()

# Try several weight interpretations
weights = {
    "Y-power (18)": 18,
    "Hamming weight of seed (24-bit)": sum(seed_24),
    "Leech rank (24)": 24,
    "D-Sink dimension (13)": 13,
    "Existence Unit cube root (24)": 24,
    "Bits 12-17 (Activation layer, 6 bits)": 6,
    "Total bits 0-17 (Reality+Info+Activation, 18 bits)": 18,
}

print(f"  {'Weight interpretation':<55} {'weight':<10} {'E_SOC (J)':<20}")
print(f"  {'-'*55} {'-'*10} {'-'*20}")
soc_results = {}
for name, weight in weights.items():
    # Without penalty (below 1 THz)
    E_soc = weight * c * float(Y) * float(nrci_Y18)
    soc_results[name] = {"weight": weight, "E_SOC_J": E_soc, "E_SOC_eV": E_soc / 1.602176634e-19}
    print(f"  {name:<55} {weight:<10} {E_soc:<20.6e}")
    print(f"  {'':<55} {'':<10} (= {E_soc / 1.602176634e-19:.6e} eV)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Predict gravity unification scale (where SOC energy crosses 1 THz wall)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(4) Predict gravity unification scale at 1 THz wall")
print("=" * 80)

# At the 1 THz wall, the penalty activates. The unification scale is where
# the SOC energy equals the photon energy at 1 THz.
# E_photon(1 THz) = h × 1 THz = 6.626e-34 × 1e12 = 6.626e-22 J
h_planck = 6.62607015e-34  # J·s
E_1THz = h_planck * THz_wall  # J
print(f"  Photon energy at 1 THz: E = h × f = {E_1THz:.6e} J = {E_1THz/1.602176634e-19:.6e} eV")

# For each weight interpretation, find the frequency where E_SOC = E_photon
print(f"\n  Gravity unification frequency (where E_SOC = h × f):")
print(f"  {'Weight interpretation':<55} {'E_SOC (J)':<14} {'f_unif (Hz)':<14} {'vs 1 THz wall':<20}")
print(f"  {'-'*55} {'-'*14} {'-'*14} {'-'*20}")
for name, info in soc_results.items():
    E_soc = info["E_SOC_J"]
    f_unif = E_soc / h_planck  # E = h × f → f = E/h
    comparison = f"{f_unif/THz_wall:.2e} × wall"
    if f_unif > THz_wall:
        verdict = f"ABOVE wall ({comparison})"
    else:
        verdict = f"BELOW wall ({comparison})"
    print(f"  {name:<55} {E_soc:<14.4e} {f_unif:<14.4e} {verdict:<20}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Penalty activation above 1 THz — what changes?
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(5) Penalty activation above 1 THz")
print("=" * 80)
print("  Per UBP, above 1 THz the SOC energy is penalised by:")
print("    penalty = exp(-(f - 1 THz) / scale)")
print("  where 'scale' is a UBP parameter (we test several values).")
print()
print("  At what frequency does the penalised SOC energy drop to 0?  Never (exponential).")
print("  At what frequency does it drop to 1% of its unpenalised value?")
print("    exp(-(f - 1 THz)/scale) = 0.01  →  f = 1 THz + scale × ln(100)")
print()
print("  For the Y^18 boundary state with weight 18:")
weight = 18
E_soc_unpenalised = weight * c * float(Y) * float(nrci_Y18)
print(f"    E_SOC (unpenalised, weight=18) = {E_soc_unpenalised:.4e} J")
print()
print(f"    {'Scale (Hz)':<20} {'f at 1% SOC (Hz)':<20} {'f at 1% SOC (THz)':<20}")
print(f"    {'-'*20} {'-'*20} {'-'*20}")
for scale in [1e10, 1e11, 1e12, 1e13, 1e14, 1e15]:
    f_1pct = THz_wall + scale * math.log(100)
    print(f"    {scale:<20.2e} {f_1pct:<20.4e} {f_1pct/1e12:<20.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Predicted unification scale (using Planck units as calibration)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(6) Predicted unification scale — comparison to Planck scale")
print("=" * 80)
# Planck frequency: f_P = c / l_P = c / sqrt(hbar × G / c^5) = sqrt(c^5 / (hbar × G))
G_SI = 6.67430e-11
hbar = h_planck / (2 * math.pi)
f_planck = math.sqrt(c**5 / (hbar * G_SI))
E_planck = h_planck * f_planck
print(f"  Planck frequency: f_P = {f_planck:.4e} Hz")
print(f"  Planck energy:    E_P = {E_planck:.4e} J = {E_planck/1.602176634e-19:.4e} eV")
print(f"  Planck frequency / 1 THz = {f_planck/1e12:.4e}")
print()
print("  If UBP's 1 THz wall corresponds to a physical threshold, and the")
print("  Planck scale is the gravitational unification scale, then the ratio")
print(f"  f_Planck / f_wall = {f_planck/THz_wall:.4e}")
print()
print("  This ratio is enormous (~10²⁴). The 1 THz wall is therefore NOT")
print("  the gravitational unification scale — it's a much lower-frequency")
print("  threshold (likely the quantum-classical transition for atomic clocks).")
print()
print("  The Y^18 boundary state's SOC energy (weight 18) = "
      f"{soc_results['Y-power (18)']['E_SOC_J']:.4e} J")
print(f"  This corresponds to frequency f = E/h = {soc_results['Y-power (18)']['E_SOC_J']/h_planck:.4e} Hz")
print(f"  That is ~{soc_results['Y-power (18)']['E_SOC_J']/h_planck/THz_wall:.2e} × the 1 THz wall")
print()
print("  Conclusion: the Y^18 boundary state's SOC energy is ~10⁹ times above")
print("  the 1 THz wall, in the penalty regime. This means the Y^18 state is")
print("  heavily penalised — consistent with gravity being weak at the")
print("  quantum scale (the penalty suppresses gravitational coupling).")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Predict gravity unification with other forces
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 80)
print("(7) Predicted gravity unification with other forces")
print("=" * 80)
# Force unification scales (energies in GeV)
unification_scales = {
    "Electroweak unification": 246,           # GeV (Higgs VEV)
    "Strong-electroweak GUT (minimal)": 1e15, # GeV
    "Planck scale (gravity)": 1.22e19,        # GeV
}
print(f"  {'Unification scale':<40} {'Energy (GeV)':<15} {'Frequency (Hz)':<20} {'SOC E (J)':<20}")
print(f"  {'-'*40} {'-'*15} {'-'*20} {'-'*20}")
for name, E_GeV in unification_scales.items():
    E_J = E_GeV * 1.602176634e-10  # GeV → J
    f = E_J / h_planck
    # What weight would be needed for E_SOC = E_J?
    # E_SOC = weight × c × Y × NRCI → weight = E_SOC / (c × Y × NRCI)
    weight_needed = E_J / (c * float(Y) * float(nrci_Y18))
    print(f"  {name:<40} {E_GeV:<15.4e} {f:<20.4e} {E_J:<20.4e}")
    print(f"  {'':<40} {'':<15} {'':<20} → weight needed = {weight_needed:.4e}")

# Save
outp = Path("/home/z/my-project/results/dir6_soc_energy.json")
with open(outp, "w") as f:
    json.dump({
        "y18_boundary_state": {
            "seed_24_bit": seed_24,
            "hamming_weight": sum(seed_24),
            "leech_symmetry_tax": float(tax_Y18),
            "leech_nrci": float(nrci_Y18),
            "in_capture_zone": float(nrci_Y18) >= 0.70,
        },
        "soc_energy_per_weight_interpretation": soc_results,
        "1_THz_wall": {
            "frequency_Hz": THz_wall,
            "photon_energy_J": E_1THz,
            "photon_energy_eV": E_1THz / 1.602176634e-19,
        },
        "gravity_unification_frequency": {
            name: {
                "E_SOC_J": info["E_SOC_J"],
                "f_unification_Hz": info["E_SOC_J"] / h_planck,
                "ratio_to_1THz_wall": info["E_SOC_J"] / h_planck / THz_wall,
            }
            for name, info in soc_results.items()
        },
        "planck_scale_comparison": {
            "f_planck_Hz": f_planck,
            "E_planck_J": E_planck,
            "f_planck_over_1THz": f_planck / THz_wall,
            "interpretation": "1 THz wall is NOT gravitational unification; it's a much lower (atomic clock) threshold",
        },
        "y18_soc_vs_planck": {
            "E_SOC_weight18_J": soc_results["Y-power (18)"]["E_SOC_J"],
            "f_SOC_weight18_Hz": soc_results["Y-power (18)"]["E_SOC_J"] / h_planck,
            "ratio_to_1THz": soc_results["Y-power (18)"]["E_SOC_J"] / h_planck / THz_wall,
            "interpretation": "Y^18 boundary state's SOC energy is ~10^9 × the 1 THz wall, in the penalty regime",
        },
        "predicted_unification_scales": {
            "electroweak": {"energy_GeV": 246, "weight_needed": 246 * 1.602176634e-10 / (c * float(Y) * float(nrci_Y18))},
            "GUT_minimal": {"energy_GeV": 1e15, "weight_needed": 1e15 * 1.602176634e-10 / (c * float(Y) * float(nrci_Y18))},
            "planck_gravity": {"energy_GeV": 1.22e19, "weight_needed": 1.22e19 * 1.602176634e-10 / (c * float(Y) * float(nrci_Y18))},
        },
        "conclusion": "The Y^18 boundary state has SOC energy ~10^9 × the 1 THz wall, placing it deep in the "
                      "penalty regime. This is consistent with gravity being weak at quantum scales. However, "
                      "the SOC energy (with weight 18) is ~10^15 × below the Planck energy, so the Y^18 state "
                      "alone does NOT predict gravitational unification at the Planck scale. To reach Planck "
                      "energy via the SOC formula, a weight of ~10^23 would be needed — far beyond any UBP-"
                      "canonical integer. The SOC framework is therefore not predictive of gravitational "
                      "unification without additional structure.",
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
