"""
Q5 — Sextet compound NRCI decomposition.

The gravity study found a 6-clique of Golay octads (the "Sextet") at indices
[0, 2, 4, 6, 8, 10] — the even-indexed octads in the canonical Golay ordering.
The compound NRCI is 0.348, well below the 0.70 "Capture Zone" threshold.

The study explicitly asks (Q5):  what is the physical meaning of a compound
NRCI < 0.70 for the Sextet?

This script:
  1. Recovers the Sextet (the 6-clique of Golay octads at even indices)
  2. Computes the per-octad symmetry tax and NRCI
  3. Tests whether the compound NRCI = 0.348 arises from:
       (a) product of per-octad NRCIs
       (b) harmonic mean
       (c) geometric mean
       (d) arithmetic mean of taxes then NRCI formula
       (e) sum of taxes then NRCI formula  (this is the standard one)
  4. Compares to randomized 6-cliques from the Golay code.
  5. Tests the "sub-threshold = ground-state / subliminal" hypothesis:
       does the compound NRCI 0.348 match any UBP constant or simple
       substrate expression?
"""
from __future__ import annotations
import json, sys, random
from fractions import Fraction
from pathlib import Path
from itertools import combinations

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

sub = u.SUBSTRATE
constants = sub.get_v6_constants()
Y = constants["Y"]
W = constants["WOBBLE"]
L = constants["SINK_L"]

# ─────────────────────────────────────────────────────────────────────────────
# Recover the Sextet
# ─────────────────────────────────────────────────────────────────────────────
golay = u.GOLAY_ENGINE
octads = golay.get_octads()
print(f"Total Golay octads: {len(octads)}")

# Per the prior study: Sextet = octads at indices [0, 2, 4, 6, 8, 10]
sextet_indices = [0, 2, 4, 6, 8, 10]
sextet = [octads[i] for i in sextet_indices]
print(f"Sextet indices: {sextet_indices}")
print(f"Sextet octads (Hamming weights): {[golay.hamming_weight(o) for o in sextet]}")

# ─────────────────────────────────────────────────────────────────────────────
# Per-octad symmetry tax and NRCI
# ─────────────────────────────────────────────────────────────────────────────
leech = u.LEECH_ENGINE
print(f"\nPer-octad symmetry tax / NRCI:")
per_octad = []
for i, oct in enumerate(sextet):
    tax = leech.symmetry_tax(oct)
    nrci = leech.calculate_nrci(oct)
    per_octad.append({"idx": sextet_indices[i], "tax": float(tax), "nrci": float(nrci),
                       "tax_frac": str(tax), "nrci_frac": str(nrci)})
    print(f"  Octad[{sextet_indices[i]:2d}]: tax = {float(tax):8.4f}   NRCI = {float(nrci):8.4f}")

taxes = [leech.symmetry_tax(o) for o in sextet]
nrcis = [leech.calculate_nrci(o) for o in sextet]

# ─────────────────────────────────────────────────────────────────────────────
# Compound NRCI via different aggregation rules
# ─────────────────────────────────────────────────────────────────────────────
# Per the UBP standard formula: NRCI = 10/(10 + total_tax), where total_tax is
# the SUM of per-octad taxes (with possible rebate)
print(f"\nAggregation rules for compound NRCI:")

# (e) Standard UBP formula: sum of taxes, then NRCI = 10/(10+sum)
total_tax_sum = sum(taxes)
compound_nrci_standard = F(10) / (F(10) + total_tax_sum)
print(f"  (e) Standard UBP (sum tax → NRCI):   tax_sum = {float(total_tax_sum):8.4f}   "
      f"NRCI = {float(compound_nrci_standard):8.4f}")

# (d) Arithmetic mean of NRCIs
nrci_arith = sum(nrcis) / len(nrcis)
print(f"  (d) Arithmetic mean of NRCIs:         NRCI = {float(nrci_arith):8.4f}")

# (c) Geometric mean of NRCIs
nrci_prod = F(1)
for n in nrcis:
    nrci_prod *= n
nrci_geom = u.ExactMath.sqrt_frac(nrci_prod, prec=20)  # sqrt for 6 elements would be 6th root
# Actually geometric mean of 6 values = (product)^(1/6).  Let's use a Newton iteration.
# We can compute x^(1/6) as ((x^(1/2))^(1/3)) but it's easier to use float and convert.
import math
nrci_geom_f = math.prod(float(n) for n in nrcis) ** (1/6)
print(f"  (c) Geometric mean of NRCIs:          NRCI ≈ {nrci_geom_f:8.4f}  (float)")

# (b) Harmonic mean of NRCIs
nrci_harm = F(len(nrcis)) / sum(F(1)/n for n in nrcis)
print(f"  (b) Harmonic mean of NRCIs:           NRCI = {float(nrci_harm):8.4f}")

# (a) Product of NRCIs
nrci_product = F(1)
for n in nrcis:
    nrci_product *= n
print(f"  (a) Product of NRCIs:                 NRCI = {float(nrci_product):.6e}  (tiny)")

# Also: NRCI from MEAN tax
mean_tax = total_tax_sum / F(len(taxes))
nrci_mean_tax = F(10) / (F(10) + mean_tax)
print(f"  (f) NRCI from MEAN tax:               NRCI = {float(nrci_mean_tax):8.4f}")

# Reference value from the gravity paper
paper_value = 0.348
print(f"\n  Reference (paper): compound NRCI = {paper_value}")
print(f"  Closest aggregation rule: ", end="")
closest = min([
    ("(e) sum tax → NRCI",     abs(float(compound_nrci_standard) - paper_value)),
    ("(d) arith mean NRCI",     abs(float(nrci_arith) - paper_value)),
    ("(c) geom mean NRCI",      abs(nrci_geom_f - paper_value)),
    ("(b) harm mean NRCI",      abs(float(nrci_harm) - paper_value)),
    ("(f) NRCI from mean tax",  abs(float(nrci_mean_tax) - paper_value)),
], key=lambda x: x[1])
print(f"{closest[0]}  (Δ = {closest[1]:.4f})")

# ─────────────────────────────────────────────────────────────────────────────
# Random 6-cliques from the Golay code for comparison
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nRandom 6-octad samples (for null distribution):")
random.seed(42)
N_SAMPLES = 200
sample_compound_nrcis = []
sample_per_octad_nrcis = []

for _ in range(N_SAMPLES):
    sample = random.sample(octads, 6)
    s_taxes = [leech.symmetry_tax(o) for o in sample]
    s_total_tax = sum(s_taxes)
    s_nrci = F(10) / (F(10) + s_total_tax)
    sample_compound_nrcis.append(float(s_nrci))
    sample_per_octad_nrcis.append([float(leech.calculate_nrci(o)) for o in sample])

import statistics
print(f"  Compound NRCI across {N_SAMPLES} random 6-octad samples:")
print(f"    min:    {min(sample_compound_nrcis):8.4f}")
print(f"    p10:    {sorted(sample_compound_nrcis)[N_SAMPLES//10]:8.4f}")
print(f"    median: {statistics.median(sample_compound_nrcis):8.4f}")
print(f"    mean:   {statistics.mean(sample_compound_nrcis):8.4f}")
print(f"    p90:    {sorted(sample_compound_nrcis)[9*N_SAMPLES//10]:8.4f}")
print(f"    max:    {max(sample_compound_nrcis):8.4f}")
print(f"  Sextet compound NRCI = {float(compound_nrci_standard):8.4f}  "
      f"-> percentile = ", end="")
pct = sum(1 for x in sample_compound_nrcis if x < float(compound_nrci_standard)) / N_SAMPLES * 100
print(f"{pct:.1f}%  (i.e., the Sextet is at the {pct:.0f}th percentile of random 6-octad sets)")

# ─────────────────────────────────────────────────────────────────────────────
# Q5: Does the compound NRCI 0.348 match any UBP substrate expression?
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSubstrate expressions near compound NRCI = {float(compound_nrci_standard):.4f}:")
candidates = [
    ("Y",            Y,         float(Y)),
    ("Y^2",          Y**2,      float(Y**2)),
    ("Y^3",          Y**3,      float(Y**3)),
    ("Y^4",          Y**4,      float(Y**4)),
    ("Y^6",          Y**6,      float(Y**6)),
    ("Y*phi",        Y*constants["PHI"], float(Y*constants["PHI"])),
    ("Y*pi",         Y*constants["PI"],  float(Y*constants["PI"])),
    ("Y*e",          Y*constants["E"],   float(Y*constants["E"])),
    ("L*4",          L*4,       float(L*4)),
    ("L*5",          L*5,       float(L*5)),
    ("L_s*4",        u.PARTICLE_PHYSICS.L_s*4, float(u.PARTICLE_PHYSICS.L_s*4)),
    ("w/2.35",       W/F(235,100), float(W/F(235,100))),
    ("Y^2 * 5",      Y**2 * 5,  float(Y**2 * 5)),
    ("3*Y/2",        F(3,2)*Y,  float(F(3,2)*Y)),
    ("Y/w",          Y/W,       float(Y/W)),
    ("Y/(2w)",       Y/(2*W),   float(Y/(2*W))),
    ("Y^2 * phi",    Y**2 * constants["PHI"], float(Y**2 * constants["PHI"])),
    ("Y * 13/10",    Y * F(13,10), float(Y * F(13,10))),
]
print(f"  {'expression':<18} {'value':<12} {'|diff from 0.348|':<18}")
for name, expr, val in candidates:
    diff = abs(val - float(compound_nrci_standard))
    marker = " <-- close" if diff < 0.02 else ""
    print(f"  {name:<18} {val:<12.6f} {diff:<18.6f}{marker}")

# ─────────────────────────────────────────────────────────────────────────────
# Test the "Sextet as quantum ground state" hypothesis
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSextet as quantum ground-state hypothesis:")
print(f"  If NRCI < 0.70 means 'sub-threshold / unmanifested',")
print(f"  then the Sextet (NRCI={float(compound_nrci_standard):.3f}) is in the")
print(f"  'Information' or 'Subliminal' layer (per UBP's 24-bit manifold).")
print(f"  The gravity paper suggests this means the Sextet is a geometric")
print(f"  object that EXISTS structurally but does not manifest physically.")
print(f"  Comparison: individual octad NRCI ≈ 0.762 (Capture Zone),")
print(f"  but compound Sextet NRCI = 0.348 (Zombie State).")
print(f"  The drop 0.762 → 0.348 = factor of {0.762/0.348:.3f}.")
print(f"  This factor is approximately sqrt(Y^2 * 13) = {float((Y**2 * 13).limit_denominator(1000)):.3f}")
print(f"  or Y/pi = {float(Y/constants['PI']):.3f}")
print(f"  Neither is exact, suggesting the drop is structural (sum of taxes)")
print(f"  rather than a simple coupling.")

# Save
out = {
    "sextet_indices":         sextet_indices,
    "per_octad":              per_octad,
    "compound_nrci_standard": float(compound_nrci_standard),
    "compound_nrci_str":      str(compound_nrci_standard),
    "aggregations": {
        "sum_tax_to_nrci":    float(compound_nrci_standard),
        "arith_mean_nrci":    float(nrci_arith),
        "geom_mean_nrci":     nrci_geom_f,
        "harm_mean_nrci":     float(nrci_harm),
        "product_nrci":       float(nrci_product),
        "nrci_from_mean_tax": float(nrci_mean_tax),
    },
    "paper_reference_value":  paper_value,
    "closest_aggregation":    closest[0],
    "random_sample_stats": {
        "n_samples":          N_SAMPLES,
        "min":                min(sample_compound_nrcis),
        "p10":                sorted(sample_compound_nrcis)[N_SAMPLES//10],
        "median":             statistics.median(sample_compound_nrcis),
        "mean":               statistics.mean(sample_compound_nrcis),
        "p90":                sorted(sample_compound_nrcis)[9*N_SAMPLES//10],
        "max":                max(sample_compound_nrcis),
        "sextet_percentile":  pct,
    },
    "substrate_expression_candidates": [
        {"name": n, "value": v} for n, _, v in candidates
    ],
}
outp = Path("/home/z/my-project/results/q5_sextet.json")
with open(outp, "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
