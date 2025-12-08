"""
Moonshine Data for Monster Group Corrections
=============================================

Key coefficients from j-invariant q-expansion and McKay-Thompson series
for implementing higher-order Monster corrections in mass predictions.

References:
- Wikipedia: j-invariant
- OEIS A000521: Coefficients of j-invariant
- Conway & Norton: Monstrous Moonshine
"""

import math

# j-invariant q-expansion coefficients
# j(τ) = q^(-1) + 744 + 196884q + 21493760q^2 + 864299970q^3 + ...
J_INVARIANT_COEFFS = {
    -1: 1,
    0: 744,
    1: 196884,      # = dim(Griess algebra) = 196883 + 1
    2: 21493760,
    3: 864299970,
    4: 20245856256,
    5: 333202640600,
    6: 4252023300096,
    7: 44656994071935,
    8: 401490886656000
}

# Monster group order
MONSTER_ORDER = 808017424794512875886459904961710757005754368000000000  # ~8×10^53

# Conway group Co₁ order (automorphism group of Leech lattice mod center)
CONWAY_CO1_ORDER = 4157776806543360000  # ~4×10^18

# Leech lattice shell orbit sizes under Co₁
# These are the number of vectors at each norm² under Conway group action
CONWAY_ORBITS = {
    0: 1,           # Origin
    2: 196560,      # First shell (Leech lattice minimal vectors)
    4: 16773120,    # Second shell
    6: 398034000,   # Third shell
    8: 4629381120,  # Fourth shell
    # Higher shells (approximate, based on growth rate)
    10: 37500000000,
    12: 244713984000,
    14: 1357170000000,
    16: 6563000000000,
    18: 28227000000000,
    20: 110000000000000
}

# McKay-Thompson series coefficients for key conjugacy classes
# T_g(τ) for different elements g ∈ Monster
# Format: {class_name: {power: coefficient}}

# Class 1A (identity) - same as j-invariant
MCKAY_THOMPSON_1A = J_INVARIANT_COEFFS

# Class 2A (involution)
MCKAY_THOMPSON_2A = {
    -1: 1,
    0: 104,
    1: 4372,
    2: 96256,
    3: 1240002,
    4: 10698752,
    5: 68752500,
    6: 355176960
}

# Class 3A
MCKAY_THOMPSON_3A = {
    -1: 1,
    0: 42,
    1: 783,
    2: 8672,
    3: 65367,
    4: 371520,
    5: 1741655,
    6: 6949264
}

# Class 2B (another involution class)
MCKAY_THOMPSON_2B = {
    -1: 1,
    0: -104,
    1: 4372,
    2: -96256,
    3: 1240002,
    4: -10698752,
    5: 68752500,
    6: -355176960
}

# Moonshine correction factors derived from coefficient ratios
# These capture the "extra structure" beyond simple shell densities

def get_moonshine_correction(norm_sq_from: int, norm_sq_to: int, 
                             conjugacy_class: str = '1A') -> float:
    """
    Compute Moonshine correction factor for shell transition.
    
    Args:
        norm_sq_from: Starting shell norm²
        norm_sq_to: Target shell norm²
        conjugacy_class: Monster conjugacy class ('1A', '2A', '3A', '2B')
    
    Returns:
        Moonshine correction factor
    """
    # Select McKay-Thompson series
    if conjugacy_class == '1A':
        series = MCKAY_THOMPSON_1A
    elif conjugacy_class == '2A':
        series = MCKAY_THOMPSON_2A
    elif conjugacy_class == '3A':
        series = MCKAY_THOMPSON_3A
    elif conjugacy_class == '2B':
        series = MCKAY_THOMPSON_2B
    else:
        series = MCKAY_THOMPSON_1A
    
    # Map norm² to q-power (heuristic: norm²/2)
    q_from = norm_sq_from // 2
    q_to = norm_sq_to // 2
    
    # Get coefficients (default to 1 if not in table)
    coeff_from = series.get(q_from, 1)
    coeff_to = series.get(q_to, 1)
    
    # Correction is ratio of coefficients
    if coeff_from == 0:
        return 1.0
    
    correction = abs(coeff_to / coeff_from)
    
    # Normalize to reasonable range (avoid extreme values)
    if correction > 1e6:
        correction = math.log(correction)
    if correction < 1e-6:
        correction = 1.0 / math.log(1.0 / correction) if correction > 0 else 1.0
    
    return correction

def get_conway_orbit_correction(norm_sq_from: int, norm_sq_to: int) -> float:
    """
    Compute Conway orbit correction factor.
    
    This uses the ratio of orbit sizes under Co₁ action.
    
    Args:
        norm_sq_from: Starting shell norm²
        norm_sq_to: Target shell norm²
    
    Returns:
        Conway orbit correction factor
    """
    orbit_from = CONWAY_ORBITS.get(norm_sq_from, 1)
    orbit_to = CONWAY_ORBITS.get(norm_sq_to, 1)
    
    if orbit_from == 0:
        return 1.0
    
    # Correction is ratio of orbit sizes
    correction = orbit_to / orbit_from
    
    # Take fractional power to moderate the effect
    # (full ratio would be too large)
    correction = correction ** 0.25
    
    return correction

def get_triple_shell_coupling(norm_sq_1: int, norm_sq_2: int, norm_sq_3: int,
                              shell_densities: dict) -> float:
    """
    Compute triple-shell coupling correction.
    
    This captures higher-order interactions beyond pairwise.
    
    Args:
        norm_sq_1, norm_sq_2, norm_sq_3: Three shell norm² values
        shell_densities: Dictionary of {norm²: density}
    
    Returns:
        Triple coupling correction factor
    """
    n1 = shell_densities.get(norm_sq_1, 1)
    n2 = shell_densities.get(norm_sq_2, 1)
    n3 = shell_densities.get(norm_sq_3, 1)
    
    # Geometric mean of three densities
    coupling = (n1 * n2 * n3) ** (1/3)
    
    # Distance factors
    d12 = abs(norm_sq_1 - norm_sq_2)
    d23 = abs(norm_sq_2 - norm_sq_3)
    d13 = abs(norm_sq_1 - norm_sq_3)
    
    # Total distance (with smoothing)
    total_distance = (d12 + d23 + d13) / 3 + 1
    
    # Coupling strength inversely proportional to distance
    coupling_strength = coupling / (total_distance ** 2)
    
    # Normalize
    coupling_strength = coupling_strength ** 0.1  # Moderate the effect
    
    return coupling_strength

# Test the corrections
if __name__ == "__main__":
    print("Moonshine Correction Data")
    print("=" * 60)
    
    # Test j-invariant coefficients
    print("\nj-invariant q-expansion (first few terms):")
    for power in sorted(J_INVARIANT_COEFFS.keys())[:5]:
        coeff = J_INVARIANT_COEFFS[power]
        print(f"  q^{power:2d}: {coeff:15,d}")
    
    # Test Moonshine corrections
    print("\nMoonshine corrections (electron → muon, norm² 4 → 6):")
    for conjugacy_class in ['1A', '2A', '3A', '2B']:
        corr = get_moonshine_correction(4, 6, conjugacy_class)
        print(f"  Class {conjugacy_class}: {corr:.6f}")
    
    # Test Conway orbit corrections
    print("\nConway orbit corrections:")
    for (n1, n2) in [(4, 6), (6, 8), (4, 8)]:
        corr = get_conway_orbit_correction(n1, n2)
        print(f"  norm² {n1} → {n2}: {corr:.6f}")
    
    # Test triple coupling
    print("\nTriple-shell coupling (4, 6, 8):")
    shell_densities = CONWAY_ORBITS
    coupling = get_triple_shell_coupling(4, 6, 8, shell_densities)
    print(f"  Coupling strength: {coupling:.6e}")
    
    print("\n" + "=" * 60)
    print("Moonshine data loaded successfully!")
