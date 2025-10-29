"""
Connecting w = 2.5 to Leech Lattice Geometry
=============================================

This script investigates the mathematical connection between the observed
geometric weight w = 2.5 (from magnetic phase transitions) and the properties
of the Leech lattice (Λ₂₄), which is central to UBP's GLR mechanism.

Key Leech Lattice Properties:
- Dimension: 24
- Kissing number: 196,560
- Minimum vector norm: 2
- First shell (norm 4): 196,560 vectors
- Unimodular and even

Author: Euan R A Craig & Manus AI
Date: October 29, 2025
"""

import numpy as np
import json

print("="*70)
print("CONNECTING w = 2.5 TO LEECH LATTICE GEOMETRY")
print("="*70)

# ============================================================================
# PART 1: LEECH LATTICE KEY PROPERTIES
# ============================================================================

print(f"\n{'='*70}")
print("PART 1: Leech Lattice Key Properties")
print("="*70)

# Fundamental properties
DIMENSION = 24
KISSING_NUMBER = 196560
MIN_NORM = 2
FIRST_SHELL_NORM = 4
FIRST_SHELL_COUNT = 196560

print(f"\nLeech Lattice (Λ₂₄) Properties:")
print(f"  Dimension:        {DIMENSION}")
print(f"  Kissing number:   {KISSING_NUMBER:,}")
print(f"  Minimum norm:     {MIN_NORM}")
print(f"  First shell norm: {FIRST_SHELL_NORM}")
print(f"  First shell size: {FIRST_SHELL_COUNT:,}")

# ============================================================================
# PART 2: INVESTIGATING RATIOS THAT YIELD 2.5
# ============================================================================

print(f"\n{'='*70}")
print("PART 2: Searching for Ratios That Yield 2.5")
print("="*70)

w_observed = 2.5
print(f"\nTarget value: w = {w_observed}")

# Generate candidate ratios from Leech lattice properties
candidates = []

# Simple ratios
candidates.append(("5/2", 5/2, "Simple rational"))
candidates.append(("FIRST_SHELL_NORM / MIN_NORM", FIRST_SHELL_NORM / MIN_NORM, "Shell norm ratio"))

# Ratios involving dimension
candidates.append(("DIMENSION / 10", DIMENSION / 10, "Dimension scaled"))
candidates.append(("DIMENSION / (2*5)", DIMENSION / (2*5), "Dimension / 10"))
candidates.append(("√(DIMENSION/4)", np.sqrt(DIMENSION/4), "Sqrt dimension ratio"))

# Kissing number ratios
candidates.append(("∛(KISSING_NUMBER) / 23", np.cbrt(KISSING_NUMBER) / 23, "Cube root kissing / 23"))
candidates.append(("∛(KISSING_NUMBER) / 24", np.cbrt(KISSING_NUMBER) / 24, "Cube root kissing / 24"))

# Shell ratios
candidates.append(("log₂(KISSING_NUMBER) / 7", np.log2(KISSING_NUMBER) / 7, "Log kissing / 7"))
candidates.append(("√(KISSING_NUMBER) / 177", np.sqrt(KISSING_NUMBER) / 177, "Sqrt kissing / 177"))

# Theta series coefficients (first few)
# From Wikipedia: 196560 vectors of norm 4, 16773120 of norm 6, 398034000 of norm 8
theta_coeffs = {
    4: 196560,
    6: 16773120,
    8: 398034000
}

candidates.append(("theta(6) / theta(4) / 85", theta_coeffs[6] / theta_coeffs[4] / 85, "Theta ratio"))
candidates.append(("∛(theta(8) / theta(4))", np.cbrt(theta_coeffs[8] / theta_coeffs[4]), "Cube root theta ratio"))

# Connection to 24 (the dimension)
candidates.append(("24 / 10", 24 / 10, "24/10"))
candidates.append(("12 / 5", 12 / 5, "12/5 (half dimension)"))
candidates.append(("60 / 24", 60 / 24, "60/24"))

# Golden ratio connections
phi = (1 + np.sqrt(5)) / 2
candidates.append(("φ + 1/φ + 1/2", phi + 1/phi + 0.5, "Golden ratio expression"))
candidates.append(("2φ - 1/2", 2*phi - 0.5, "2φ - 1/2"))
candidates.append(("φ² - 1/2", phi**2 - 0.5, "φ² - 1/2"))

# Geometric ratios
candidates.append(("5/(2·1)", 5/(2*1), "5/2 (simple)"))
candidates.append(("(1 + 3/2)", 1 + 3/2, "1 + 3/2"))

# Sort by closeness to 2.5
candidates_sorted = sorted(candidates, key=lambda x: abs(x[1] - w_observed))

print(f"\n{'Expression':<40} {'Value':<15} {'Difference':<15} {'Description':<25}")
print("-"*105)

exact_matches = []
close_matches = []

for expr, value, desc in candidates_sorted:
    diff = abs(value - w_observed)
    rel_error = (diff / w_observed) * 100
    
    print(f"{expr:<40} {value:<15.10f} {diff:<15.10f} {desc:<25}")
    
    if diff < 0.001:  # Exact match
        exact_matches.append((expr, value, diff, desc))
    elif rel_error < 5:  # Within 5%
        close_matches.append((expr, value, diff, rel_error, desc))

# ============================================================================
# PART 3: THETA SERIES ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PART 3: Theta Series Analysis")
print("="*70)

print(f"\nThe theta series of the Leech lattice encodes the number of")
print(f"vectors at each squared norm. The first few coefficients are:")

print(f"\n{'Squared Norm':<15} {'Count':<15} {'Ratio to Previous':<20}")
print("-"*50)

prev_count = 1  # The origin
for norm, count in sorted(theta_coeffs.items()):
    ratio = count / prev_count
    print(f"{norm:<15} {count:<15,} {ratio:<20.6f}")
    prev_count = count

print(f"\nInvestigating if 2.5 relates to theta series ratios...")

# Check ratios between consecutive shells
ratio_4_to_0 = theta_coeffs[4] / 1  # 196560
ratio_6_to_4 = theta_coeffs[6] / theta_coeffs[4]  # ~85.3
ratio_8_to_6 = theta_coeffs[8] / theta_coeffs[6]  # ~23.7

print(f"\nShell growth ratios:")
print(f"  N(4) / N(0) = {ratio_4_to_0:.2f}")
print(f"  N(6) / N(4) = {ratio_6_to_4:.6f}")
print(f"  N(8) / N(6) = {ratio_8_to_6:.6f}")

# Check if any combination yields 2.5
print(f"\nSearching for combinations that yield 2.5...")
theta_candidates = [
    ("N(4) / N(0) / 78624", theta_coeffs[4] / 1 / 78624),
    ("√(N(6) / N(4))", np.sqrt(ratio_6_to_4)),
    ("∛(N(8) / N(6))", np.cbrt(ratio_8_to_6)),
    ("log₁₀(N(4)) / 2.1", np.log10(theta_coeffs[4]) / 2.1),
]

for expr, value in theta_candidates:
    diff = abs(value - 2.5)
    print(f"  {expr:<30} = {value:.6f} (Δ = {diff:.6f})")

# ============================================================================
# PART 4: KISSING NUMBER CONNECTIONS
# ============================================================================

print(f"\n{'='*70}")
print("PART 4: Kissing Number Analysis")
print("="*70)

print(f"\nThe kissing number 196,560 is the number of unit spheres that")
print(f"can simultaneously touch a central sphere in 24 dimensions.")

# Factor 196560
print(f"\nFactorization of 196,560:")
n = KISSING_NUMBER
factors = []
temp = n

for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
    count = 0
    while temp % p == 0:
        count += 1
        temp //= p
    if count > 0:
        factors.append((p, count))

print(f"  196,560 = ", end="")
print(" × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors]))

# Calculate: 196560 = 2^4 × 3^2 × 5 × 7 × 13
print(f"  196,560 = 16 × 9 × 5 × 7 × 13")
print(f"  196,560 = 16 × 12,285")

# Check if 2.5 relates to these factors
print(f"\nInvestigating factor-based ratios:")
print(f"  5 / 2 = {5/2} ✓ EXACT MATCH")
print(f"  (This is the simplest expression for 2.5)")

# ============================================================================
# PART 5: DIMENSION AND GEOMETRY
# ============================================================================

print(f"\n{'='*70}")
print("PART 5: Dimensional Geometry")
print("="*70)

print(f"\nThe Leech lattice exists in 24 dimensions.")
print(f"UBP operates in 12D+ (simulated in 6D).")
print(f"\nKey dimensional ratios:")
print(f"  24 / 12 = {24/12}")
print(f"  24 / 10 = {24/10}")
print(f"  12 / 5  = {12/5} ✓ CLOSE TO 2.5")
print(f"  5 / 2   = {5/2} ✓ EXACT")

# ============================================================================
# PART 6: HYPOTHESIS AND INTERPRETATION
# ============================================================================

print(f"\n{'='*70}")
print("PART 6: Hypothesis and Interpretation")
print("="*70)

if exact_matches:
    print(f"\n✓ EXACT MATCHES FOUND:")
    for expr, value, diff, desc in exact_matches:
        print(f"  {expr} = {value}")
        print(f"    Description: {desc}")
        print(f"    Difference: {diff:.10f}")
else:
    print(f"\n⚠ No exact Leech lattice-derived expressions found.")

print(f"\n{'='*70}")
print("PROPOSED INTERPRETATION")
print("="*70)

print(f"""
w = 2.5 = 5/2 is a SIMPLE RATIONAL that appears in magnetic phase transitions.

While it doesn't directly derive from complex Leech lattice properties
(like kissing numbers or theta series), its simplicity is significant:

1. **Rational Simplicity**: 5/2 is one of the simplest non-integer rationals.
   This suggests a fundamental computational mode, not a complex geometric
   constraint.

2. **Relationship to UBP Dimensions**:
   - 12 / 5 = 2.4 (close to 2.5)
   - This may relate to the 12D structure of UBP
   - The factor of 5 could relate to the 5-dimensional subspace in the
     6D operational space (170×170×170×5×2×2)

3. **Phase Transition Interpretation**:
   - w = 1.0 (ordered) → w = 2.5 (critical/disordered)
   - The shift from 1 to 5/2 represents a 2.5× increase in geometric weight
   - This could represent the computational "cost" of entropy and fluctuations

4. **Leech Lattice Connection (Indirect)**:
   - The Leech lattice is central to UBP's GLR (Golay-Leech-Resonance)
   - GLR provides error correction and stability
   - w = 2.5 may represent a breakdown or relaxation of GLR constraints
     during phase transitions (high entropy states)
   - At critical points, the system is "deciding" which phase to enter,
     requiring maximum computational resources and reduced error correction

5. **Contrast with w ≈ 1.53**:
   - w ≈ 1.53 (Information Layer): Complex, irrational, φ-related
   - w = 2.5 (Unactivated Layer): Simple, rational, 5/2
   - This distinction supports different computational modes for different layers

CONCLUSION:
w = 2.5 is best understood as a SIMPLE RATIONAL representing a fundamental
computational mode shift during phase transitions, rather than a complex
geometric invariant derived from Leech lattice structure. Its simplicity
(5/2) may be its most important feature, indicating a basic computational
state rather than a sophisticated geometric constraint.

The Leech lattice connection is INDIRECT: the lattice provides the stable
computational substrate (via GLR), but w = 2.5 represents what happens when
that stability is temporarily relaxed during high-entropy transitions.
""")

# ============================================================================
# PART 7: SAVE RESULTS
# ============================================================================

results = {
    'w_observed': 2.5,
    'exact_match': '5/2',
    'leech_properties': {
        'dimension': DIMENSION,
        'kissing_number': KISSING_NUMBER,
        'min_norm': MIN_NORM,
        'first_shell_norm': FIRST_SHELL_NORM,
        'first_shell_count': FIRST_SHELL_COUNT
    },
    'theta_series': {
        'norm_4': theta_coeffs[4],
        'norm_6': theta_coeffs[6],
        'norm_8': theta_coeffs[8]
    },
    'interpretation': {
        'primary': 'Simple rational 5/2',
        'layer': 'Unactivated Layer',
        'context': 'Phase transitions and high-entropy states',
        'relationship_to_leech': 'Indirect - represents relaxation of GLR constraints'
    },
    'dimensional_connection': {
        '12/5': 12/5,
        'note': 'May relate to UBP 12D structure'
    }
}

with open('/home/ubuntu/leech_connection_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Results saved to: leech_connection_results.json")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print("="*70)

