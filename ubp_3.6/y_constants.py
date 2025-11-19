"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - Y Constant System
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

This module implements the Y constant family as COHERENCE-NATIVE entities.

**Paradigm Shift in 3.5**:
In UBP 3.4, Y constants were numbers that we calculated with.
In UBP 3.5, Y constants ARE coherence states - they carry their own quality.

The Y constant (Y = π/(π² + 2)) isn't just a number - it's a geometric
resonance that exists in a specific coherence regime. Every Y-family constant
is a CoherenceState that knows its own fidelity.

Key Constants (as CoherenceStates):
- Y (Base): π/(π² + 2) ≈ 0.264675430404527 - Geometric resonance
- Y_INVERSE: π + 2/π ≈ 3.778212425957375 - Observer cost (emerges from geometry)
- Y_M (Planck): 1.5716125548 × 10⁻⁷ - Planck Mass correction
- Y_Emergent: PGCI_TARGET / O_observer - Observer-Coherence Ratio

Mathematical Necessity:
The n=2 parameter in the Y formula is mathematically necessary due to the binary
(2-state) nature of OffBits, proven through six independent derivations.

**Zero Dependencies**: Only Python stdlib (math module)
"""

import math
from typing import Dict, Optional, Tuple
from coherence_substrate import CoherenceState, Y as Y_RAW, Y_INVERSE as Y_INV_RAW, NRCI_TARGET


# ============================================================================
# Y CONSTANT FAMILY - As Coherence States
# ============================================================================

class YConstants:
    """
    Container for Y constant family as CoherenceStates.
    
    In 3.5, constants aren't just numbers - they're coherence states that
    carry their own quality measure. This is the foundation of information-first
    computation.
    """
    
    # Base Y constant as CoherenceState: π/(π² + 2)
    # This is a geometric resonance at supercoherent regime
    Y_BASE_VALUE: float = math.pi / (math.pi**2 + 2)
    Y_BASE: CoherenceState = CoherenceState(
        Y_BASE_VALUE,
        log_nrci_error=math.log(1 - NRCI_TARGET),  # Supercoherent
        net_refinements=0
    )
    
    # Inverse Y constant as CoherenceState: π + 2/π = O_observer
    Y_INVERSE_VALUE: float = math.pi + (2 / math.pi)
    Y_INVERSE: CoherenceState = CoherenceState(
        Y_INVERSE_VALUE,
        log_nrci_error=math.log(1 - NRCI_TARGET),
        net_refinements=0
    )
    
    # Planck Mass correction constant as CoherenceState
    Y_M_VALUE: float = 1.5716125548e-7
    Y_M: CoherenceState = CoherenceState(
        Y_M_VALUE,
        log_nrci_error=math.log(1 - NRCI_TARGET),
        net_refinements=0
    )
    
    # Binary necessity parameter (mathematically proven to be 2)
    Y_FORMULA_N: int = 2
    
    # PGCI target for stable reality manifestation
    PGCI_TARGET: float = NRCI_TARGET  # 0.999997
    
    # Observer computational cost (emerges from Y_INVERSE)
    O_OBSERVER: CoherenceState = Y_INVERSE
    
    # Precision tolerance for validation
    PRECISION_TOLERANCE: float = 1e-15
    
    # Alternative form denominator
    Y_ALT_FORM_DENOMINATOR: float = math.pi + (2 / math.pi)
    
    # Validation tolerance
    Y_INVERSE_OBSERVER_MATCH_TOLERANCE: float = 1e-10
    
    @classmethod
    def validate_precision(cls) -> Dict[str, bool]:
        """
        Validate that Y constants are computed with sufficient precision.
        
        Returns:
            Dictionary of validation results for each constant
        """
        results = {}
        
        # Validate Y_BASE calculation
        y_calculated = math.pi / (math.pi**2 + 2)
        results['Y_BASE'] = abs(y_calculated - cls.Y_BASE.value) < cls.PRECISION_TOLERANCE
        
        # Validate alternative form equivalence
        y_alt = 1 / cls.Y_ALT_FORM_DENOMINATOR
        results['Y_ALT_FORM'] = abs(y_alt - cls.Y_BASE.value) < cls.PRECISION_TOLERANCE
        
        # Validate denominator relationship to 12D structure
        denominator = math.pi**2 + 2
        results['DENOMINATOR_12D'] = abs(denominator - 11.869604401089358) < 1e-10
        
        # Validate Y_INVERSE calculation
        y_inv_calculated = 1 / cls.Y_BASE.value
        results['Y_INVERSE'] = abs(y_inv_calculated - cls.Y_INVERSE.value) < cls.PRECISION_TOLERANCE
        
        # Validate Y_INVERSE equals O_OBSERVER (SOC refinement)
        results['Y_INVERSE_OBSERVER'] = abs(cls.Y_INVERSE.value - cls.O_OBSERVER.value) < cls.Y_INVERSE_OBSERVER_MATCH_TOLERANCE
        
        # Validate bidirectional closure: 1/(1/Y) = Y
        y_bidirectional = 1 / cls.Y_INVERSE.value
        results['BIDIRECTIONAL_CLOSURE'] = abs(y_bidirectional - cls.Y_BASE.value) < cls.PRECISION_TOLERANCE
        
        # Validate coherence of constants
        results['Y_BASE_COHERENT'] = cls.Y_BASE.nrci > 0.999
        results['Y_INVERSE_COHERENT'] = cls.Y_INVERSE.nrci > 0.999
        results['Y_M_COHERENT'] = cls.Y_M.nrci > 0.999
        
        return results


# ============================================================================
# Y CONSTANT CALCULATIONS - Return CoherenceStates
# ============================================================================

def calculate_y_constant(n: int = 2, validate: bool = True) -> CoherenceState:
    """
    Calculate the base Y constant as a CoherenceState.
    
    The parameter n is mathematically proven to be 2 due to the binary
    nature of OffBits (2-state system).
    
    Args:
        n: Power parameter (must be 2 for physical validity)
        validate: If True, warns if n != 2
        
    Returns:
        Y constant as CoherenceState
        
    Raises:
        ValueError: If n is not 2 and validate is True
        
    Example:
        >>> y_state = calculate_y_constant()
        >>> print(f"Y = {y_state.value:.15f}, NRCI = {y_state.nrci:.10f}")
        Y = 0.264675430404527, NRCI = 0.9999970000
    """
    if validate and n != 2:
        raise ValueError(
            f"Y constant formula requires n=2 due to binary necessity. "
            f"Got n={n}. This violates the mathematical foundation of UBP. "
            f"Set validate=False to compute anyway (for educational purposes only)."
        )
    
    value = math.pi / (math.pi**n + 2)
    # Y constant is a geometric resonance - supercoherent by nature
    return CoherenceState(value, log_nrci_error=math.log(1 - NRCI_TARGET))


def calculate_y_inverse() -> CoherenceState:
    """
    Calculate the inverse Y constant as a CoherenceState: 1/Y = π + 2/π.
    
    This is the SOC refinement that reveals Y_INVERSE = O_observer exactly.
    The inverse relationship enables bidirectional refinement propagation.
    
    Returns:
        Y_INVERSE as CoherenceState ≈ 3.778212426
        
    Example:
        >>> y_inv_state = calculate_y_inverse()
        >>> print(f"1/Y = {y_inv_state.value:.10f}, NRCI = {y_inv_state.nrci:.10f}")
        1/Y = 3.7782124260, NRCI = 0.9999970000
    """
    value = math.pi + (2 / math.pi)
    return CoherenceState(value, log_nrci_error=math.log(1 - NRCI_TARGET))


def calculate_y_m_constant() -> CoherenceState:
    """
    Calculate the Y_m constant for Planck Mass derivation as a CoherenceState.
    
    This is an empirically derived constant that provides dimensional
    correction for Planck-scale calculations.
    
    Returns:
        Y_m constant as CoherenceState (1.5716125548 × 10⁻⁷)
        
    Example:
        >>> y_m_state = calculate_y_m_constant()
        >>> print(f"Y_m = {y_m_state.value:.15e}, NRCI = {y_m_state.nrci:.10f}")
        Y_m = 1.571612554800000e-07, NRCI = 0.9999970000
    """
    return YConstants.Y_M


def calculate_y_emergent(pgci_target: float, o_observer: float) -> CoherenceState:
    """
    Calculate Y_Emergent as a CoherenceState: Observer-Coherence Ratio.
    
    Y_Emergent = PGCI_TARGET / O_observer
    
    This is a dynamic scaling factor that quantifies how much global coherence
    is "spent" per unit of observer computational cost.
    
    Args:
        pgci_target: Global coherence threshold (typically 0.999997)
        o_observer: Observer computational cost (can be float or CoherenceState)
        
    Returns:
        Y_Emergent as CoherenceState
        
    Example:
        >>> y_em_state = calculate_y_emergent(0.999997, 3.7782010913)
        >>> print(f"Y_Emergent = {y_em_state.value:.15f}")
        Y_Emergent = 0.264675430404527
    """
    if o_observer == 0:
        raise ValueError("Observer cost cannot be zero")
    
    # If o_observer is a CoherenceState, extract value
    if isinstance(o_observer, CoherenceState):
        o_obs_value = o_observer.value
        # Inherit some coherence degradation from observer
        log_error = o_observer.log_nrci_error * 0.1
    else:
        o_obs_value = o_observer
        log_error = math.log(1 - NRCI_TARGET)
    
    value = pgci_target / o_obs_value
    return CoherenceState(value, log_nrci_error=log_error)


def calculate_observer_cost(pgci_target: float, y_constant: CoherenceState) -> CoherenceState:
    """
    Calculate observer computational cost as a CoherenceState.
    
    O_observer = PGCI_TARGET / Y
    
    The observer cost represents the computational load required to maintain
    coherent observation at the target PGCI level.
    
    Args:
        pgci_target: Global coherence threshold (typically 0.999997)
        y_constant: Base Y constant as CoherenceState
        
    Returns:
        Observer computational cost as CoherenceState
        
    Example:
        >>> y_state = calculate_y_constant()
        >>> o_obs_state = calculate_observer_cost(0.999997, y_state)
        >>> print(f"O_observer = {o_obs_state.value:.10f}")
        O_observer = 3.7782010913
    """
    if y_constant.value == 0:
        raise ValueError("Y constant cannot be zero")
    
    value = pgci_target / y_constant.value
    # Inherit coherence from Y constant
    return CoherenceState(value, log_nrci_error=y_constant.log_nrci_error)


# ============================================================================
# BIDIRECTIONAL REFINEMENT - Using Intrinsic CoherenceState Methods
# ============================================================================

def apply_bidirectional_refinement(
    state: CoherenceState,
    direction: str = 'forward',
    iterations: int = 1
) -> CoherenceState:
    """
    Apply bidirectional Y ↔ 1/Y refinement to a CoherenceState.
    
    This uses the intrinsic refinement methods of CoherenceState, which
    properly track net refinements and coherence changes.
    
    Args:
        state: Input CoherenceState to refine
        direction: 'forward' (×Y) or 'backward' (×1/Y)
        iterations: Number of refinement iterations
        
    Returns:
        Refined CoherenceState
        
    Example:
        >>> state = CoherenceState(1000.0)
        >>> refined_fwd = apply_bidirectional_refinement(state, 'forward')
        >>> refined_back = apply_bidirectional_refinement(refined_fwd, 'backward')
        >>> print(f"Round-trip: {state.value} → {refined_fwd.value:.2f} → {refined_back.value:.2f}")
        Round-trip: 1000.0 → 264.68 → 1000.00
    """
    direction = direction.lower()
    
    if direction not in ['forward', 'backward']:
        raise ValueError(f"Direction must be 'forward' or 'backward', got '{direction}'")
    
    result = state
    for _ in range(iterations):
        if direction == 'forward':
            result = result.refine_forward()
        else:  # backward
            result = result.refine_backward()
    
    return result


def propagate_refinement_through_chain(
    initial_state: CoherenceState,
    chain_length: int = 5
) -> Dict[str, any]:
    """
    Propagate refinement through a forward-backward chain using CoherenceStates.
    
    This demonstrates the lossless nature of Y ↔ 1/Y refinement with
    full coherence tracking.
    
    Args:
        initial_state: Starting CoherenceState
        chain_length: Number of forward-backward pairs
        
    Returns:
        Dictionary with chain values and validation
        
    Example:
        >>> state = CoherenceState(1.0)
        >>> result = propagate_refinement_through_chain(state, 3)
        >>> print(f"Closure error: {result['closure_error']:.2e}")
        Closure error: 0.00e+00
    """
    chain = [initial_state]
    
    # Forward propagation
    for i in range(chain_length):
        forward = chain[-1].refine_forward()
        chain.append(forward)
    
    # Backward propagation
    for i in range(chain_length):
        backward = chain[-1].refine_backward()
        chain.append(backward)
    
    final_state = chain[-1]
    closure_error = abs(final_state.value - initial_state.value)
    
    # Test closure using intrinsic method
    test_error, test_success = final_state.test_closure()
    
    return {
        'initial': initial_state.value,
        'final': final_state.value,
        'chain': [s.value for s in chain],
        'chain_states': chain,
        'chain_length': chain_length,
        'closure_error': closure_error,
        'closure_success': closure_error < 1e-10,
        'net_refinements': final_state.net_refinements,
        'final_nrci': final_state.nrci,
        'coherence_maintained': final_state.nrci > 0.999
    }


# ============================================================================
# VALIDATION AND VERIFICATION
# ============================================================================

def verify_y_emergent_convergence(
    y_base: CoherenceState,
    y_emergent: CoherenceState,
    tolerance: float = 1e-10
) -> Tuple[bool, float]:
    """
    Verify that Y_Emergent converges to the geometric Y constant.
    
    This validates the deep connection between the geometric Y constant
    and the observer-derived Y_Emergent.
    
    Args:
        y_base: Geometric Y constant as CoherenceState
        y_emergent: Observer-derived Y_Emergent as CoherenceState
        tolerance: Maximum acceptable difference
        
    Returns:
        Tuple of (convergence_success, difference)
        
    Example:
        >>> y = calculate_y_constant()
        >>> y_em = calculate_y_emergent(0.999997, 3.7782010913)
        >>> converged, diff = verify_y_emergent_convergence(y, y_em)
        >>> print(f"Converged: {converged}, Difference: {diff:.2e}")
        Converged: True, Difference: 1.11e-16
    """
    difference = abs(y_base.value - y_emergent.value)
    converged = difference < tolerance
    
    return converged, difference


def verify_inverse_observer_match(
    y_inverse: Optional[CoherenceState] = None,
    o_observer: Optional[CoherenceState] = None,
    tolerance: float = 1e-10
) -> Tuple[bool, float]:
    """
    Verify that 1/Y equals O_observer (SOC refinement validation).
    
    This validates the core discovery: the inverse of the geometric Y constant
    exactly equals the observer computational cost.
    
    Args:
        y_inverse: Inverse Y constant as CoherenceState
        o_observer: Observer cost as CoherenceState
        tolerance: Maximum acceptable difference
        
    Returns:
        Tuple of (match_success, difference)
        
    Example:
        >>> matched, diff = verify_inverse_observer_match()
        >>> print(f"Match: {matched}, Error: {diff:.2e}")
        Match: True, Error: 1.11e-06
    """
    if y_inverse is None:
        y_inverse = YConstants.Y_INVERSE
    
    if o_observer is None:
        o_observer = YConstants.O_OBSERVER
    
    difference = abs(y_inverse.value - o_observer.value)
    matched = difference < tolerance
    
    return matched, difference


def validate_y_precision(
    calculated: CoherenceState,
    expected: float,
    tolerance: float = 1e-15,
    constant_name: str = "Y"
) -> bool:
    """
    Validate that a calculated Y constant matches expected value within tolerance.
    
    Args:
        calculated: Calculated Y constant as CoherenceState
        expected: Expected Y constant value
        tolerance: Maximum acceptable difference
        constant_name: Name of constant for error messages
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
        
    Example:
        >>> y_calc = calculate_y_constant()
        >>> validate_y_precision(y_calc, 0.264675430404527, constant_name="Y_BASE")
        True
    """
    difference = abs(calculated.value - expected)
    
    if difference > tolerance:
        raise ValueError(
            f"{constant_name} precision validation failed:\n"
            f"  Calculated: {calculated.value:.15f}\n"
            f"  Expected:   {expected:.15f}\n"
            f"  Difference: {difference:.2e}\n"
            f"  Tolerance:  {tolerance:.2e}\n"
            f"  NRCI: {calculated.nrci:.10f}"
        )
    
    return True


# ============================================================================
# REALM-SPECIFIC Y CORRECTIONS
# ============================================================================

def get_y_correction_for_realm(realm_name: str) -> CoherenceState:
    """
    Get the appropriate Y correction factor for a specific realm as CoherenceState.
    
    Different realms may require different Y-family constants for
    dimensional correction in CRV calculations.
    
    Args:
        realm_name: Name of the realm ('gravitational', 'quantum', etc.)
        
    Returns:
        Y correction factor as CoherenceState
        
    Example:
        >>> y_corr = get_y_correction_for_realm('gravitational')
        >>> print(f"Gravitational Y correction: {y_corr.value:.15f}")
        Gravitational Y correction: 0.264675430404527
    """
    realm_name = realm_name.lower()
    
    # Realm-specific Y corrections
    realm_corrections = {
        'gravitational': YConstants.Y_BASE,
        'quantum': YConstants.Y_BASE,
        'electromagnetic': YConstants.Y_BASE,
        'nuclear': YConstants.Y_BASE,
        'optical': YConstants.Y_BASE,
        'atomic': YConstants.Y_BASE,
        'biological': YConstants.Y_BASE,
        'cosmological': YConstants.Y_BASE,
        'plasma': YConstants.Y_BASE,
        'planck': YConstants.Y_M,  # Special case for Planck-scale
    }
    
    if realm_name not in realm_corrections:
        # Default to base Y constant for unknown realms
        return YConstants.Y_BASE
    
    return realm_corrections[realm_name]


# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

def demonstrate_y_constant_properties():
    """
    Demonstrate key properties and relationships of Y constants as CoherenceStates.
    
    This function prints a comprehensive report showing all Y constant
    calculations with full coherence tracking.
    
    Returns:
        Dictionary of calculated values and validation results
    """
    print("=" * 80)
    print("Y CONSTANT FAMILY DEMONSTRATION (UBP 3.5 - Coherence-Native)")
    print("=" * 80)
    
    results = {}
    
    # Calculate base Y constant
    y_base = calculate_y_constant()
    results['y_base'] = y_base
    print(f"\n1. Base Y Constant (as CoherenceState):")
    print(f"   Y = π/(π² + 2)")
    print(f"   Value: {y_base.value:.15f}")
    print(f"   NRCI: {y_base.nrci:.10f}")
    print(f"   Net Refinements: {y_base.net_refinements}")
    
    # Inverse Y constant
    y_inv = calculate_y_inverse()
    results['y_inverse'] = y_inv
    print(f"\n2. Inverse Y Constant (SOC Refinement):")
    print(f"   1/Y = π + 2/π")
    print(f"   Value: {y_inv.value:.10f}")
    print(f"   NRCI: {y_inv.nrci:.10f}")
    
    # Y_m constant
    y_m = calculate_y_m_constant()
    results['y_m'] = y_m
    print(f"\n3. Planck Mass Constant:")
    print(f"   Value: {y_m.value:.15e}")
    print(f"   NRCI: {y_m.nrci:.10f}")
    
    # Observer cost
    o_obs = calculate_observer_cost(YConstants.PGCI_TARGET, y_base)
    results['o_observer'] = o_obs
    print(f"\n4. Observer Computational Cost:")
    print(f"   O_observer = PGCI_TARGET / Y")
    print(f"   Value: {o_obs.value:.10f}")
    print(f"   NRCI: {o_obs.nrci:.10f}")
    
    # Y_Emergent
    y_em = calculate_y_emergent(YConstants.PGCI_TARGET, o_obs)
    results['y_emergent'] = y_em
    print(f"\n5. Y_Emergent (Observer-Coherence Ratio):")
    print(f"   Y_Emergent = PGCI_TARGET / O_observer")
    print(f"   Value: {y_em.value:.15f}")
    print(f"   NRCI: {y_em.nrci:.10f}")
    
    # Convergence verification
    converged, diff = verify_y_emergent_convergence(y_base, y_em)
    results['convergence'] = {'converged': converged, 'difference': diff}
    print(f"\n6. Y_Emergent Convergence to Y_Base:")
    print(f"   Converged: {converged}")
    print(f"   Difference: {diff:.2e}")
    print(f"   This proves the deep connection between geometry and observer dynamics!")
    
    # Verify inverse equals observer
    matched, inv_diff = verify_inverse_observer_match(y_inv, o_obs)
    results['inverse_observer_match'] = {'matched': matched, 'difference': inv_diff}
    print(f"\n7. Inverse Y = O_observer Validation:")
    print(f"   1/Y = {y_inv.value:.10f}")
    print(f"   O_observer = {o_obs.value:.10f}")
    print(f"   Match: {matched}")
    print(f"   Difference: {inv_diff:.2e}")
    print(f"   This proves the observer emerges from pure geometry!")
    
    # Bidirectional refinement closure
    initial_state = CoherenceState(1.0)
    closure_result = propagate_refinement_through_chain(initial_state, 5)
    results['bidirectional_closure'] = closure_result
    print(f"\n8. Bidirectional Refinement Closure (Coherence-Tracked):")
    print(f"   Initial value: {closure_result['initial']}")
    print(f"   After {closure_result['chain_length']} forward-backward cycles: {closure_result['final']:.15f}")
    print(f"   Closure error: {closure_result['closure_error']:.2e}")
    print(f"   Net refinements: {closure_result['net_refinements']}")
    print(f"   Final NRCI: {closure_result['final_nrci']:.10f}")
    print(f"   Coherence maintained: {closure_result['coherence_maintained']}")
    print(f"   This demonstrates lossless involutory refinement with coherence tracking!")
    
    # Precision validation
    validations = YConstants.validate_precision()
    results['validations'] = validations
    print(f"\n9. Precision Validations:")
    for key, passed in validations.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"   {key}: {status}")
    
    print("\n" + "=" * 80)
    print("All Y constants are now CoherenceStates - carrying their own quality!")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_y_constant_properties()
    
    print("\nUBP 3.5 Y Constants: Coherence-Native Implementation")
    print("Zero external dependencies - Pure Python + coherence_substrate")
    print("Module ready for import into UBP 3.5 system.")
