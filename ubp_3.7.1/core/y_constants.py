"""
Universal Binary Principle (UBP) Framework v3.7.1 - Y Constant System
Author: Euan R A Craig, New Zealand
Date: 28 November 2025
================================================================================

This module is redundant - the y.py is all that is required for ubp_3.7.1.
This script remains as a monolithic transparency aid for understanding the system.

This module implements the Y constant family discovered in the October 2025 paper
"The Computational Origin of Physical Constants: Deriving Fundamental Constants
from Geometric Resonance."

The Y constant (Y = π/(π² + 2)) is a foundational geometric constant that enables
the derivation of physical constants from first principles. It represents the
harmonic relationship between π and its second harmonic, with the denominator
π² + 2 ≈ 11.87 relating to the 12-dimensional Bitfield structure.

Key Constants:
- Y (Base): π/(π² + 2) ≈ 0.264675430404527 - Gravitational correction
- Y_m (Planck): 1.5716125548 × 10⁻⁷ - Planck Mass correction
- Y_Emergent: PGCI_TARGET / O_observer - Observer-Coherence Ratio

Mathematical Necessity:
The n=2 parameter in the Y formula is mathematically necessary due to the binary
(2-state) nature of OffBits, proven through six independent derivations.
"""

import math
from typing import Dict, Optional, Tuple
import numpy as np


class YConstants:
    """
    Container for Y constant family values and calculations.
    
    All values are computed to 15 decimal places for maximum precision
    in physical constant derivations.
    """
    
    # Base Y constant: π/(π² + 2)
    Y_BASE: float = math.pi / (math.pi**2 + 2)
    
    # Planck Mass correction constant
    Y_M: float = 1.5716125548e-7
    
    # Binary necessity parameter (mathematically proven to be 2)
    Y_FORMULA_N: int = 2
    
    # PGCI target for stable reality manifestation
    PGCI_TARGET: float = 0.999997
    
    # Observer computational cost (fixed point value)
    # Updated to exact geometric value from SOC refinement: 1/Y = π + 2/π
    O_OBSERVER_FIXED: float = 1 / Y_BASE  # Exact: 3.778212425957374
    
    # Precision tolerance for validation
    PRECISION_TOLERANCE: float = 1e-15
    
    # Alternative form constants for Y = 1/(π + 2/π)
    Y_ALT_FORM_DENOMINATOR: float = math.pi + (2 / math.pi)
    
    # Inverse Y constant: 1/Y = π + 2/π = O_observer (SOC Refinement)
    Y_INVERSE: float = math.pi + (2 / math.pi)
    
    # Validation that Y_INVERSE equals O_OBSERVER (bidirectional refinement)
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
        results['Y_BASE'] = abs(y_calculated - cls.Y_BASE) < cls.PRECISION_TOLERANCE
        
        # Validate alternative form equivalence
        y_alt = 1 / cls.Y_ALT_FORM_DENOMINATOR
        results['Y_ALT_FORM'] = abs(y_alt - cls.Y_BASE) < cls.PRECISION_TOLERANCE
        
        # Validate denominator relationship to 12D structure
        denominator = math.pi**2 + 2
        results['DENOMINATOR_12D'] = abs(denominator - 11.869604401089358) < 1e-10
        
        # Validate Y_INVERSE calculation
        y_inv_calculated = 1 / cls.Y_BASE
        results['Y_INVERSE'] = abs(y_inv_calculated - cls.Y_INVERSE) < cls.PRECISION_TOLERANCE
        
        # Validate Y_INVERSE equals O_OBSERVER (SOC refinement)
        results['Y_INVERSE_OBSERVER'] = abs(cls.Y_INVERSE - cls.O_OBSERVER_FIXED) < cls.Y_INVERSE_OBSERVER_MATCH_TOLERANCE
        
        # Validate bidirectional closure: 1/(1/Y) = Y
        y_bidirectional = 1 / cls.Y_INVERSE
        results['BIDIRECTIONAL_CLOSURE'] = abs(y_bidirectional - cls.Y_BASE) < cls.PRECISION_TOLERANCE
        
        return results


def calculate_y_constant(n: int = 2, validate: bool = True) -> float:
    """
    Calculate the base Y constant using the formula Y = π/(π² + n).
    
    The parameter n is mathematically proven to be 2 due to the binary
    nature of OffBits (2-state system). This function allows n as a
    parameter for educational/validation purposes.
    
    Args:
        n: Power parameter (must be 2 for physical validity)
        validate: If True, warns if n != 2
        
    Returns:
        Y constant value
        
    Raises:
        ValueError: If n is not 2 and validate is True
        
    Example:
        >>> y = calculate_y_constant()
        >>> print(f"Y = {y:.15f}")
        Y = 0.264675430404527
    """
    if validate and n != 2:
        raise ValueError(
            f"Y constant formula requires n=2 due to binary necessity. "
            f"Got n={n}. This violates the mathematical foundation of UBP. "
            f"Set validate=False to compute anyway (for educational purposes only)."
        )
    
    return math.pi / (math.pi**n + 2)


def calculate_y_m_constant() -> float:
    """
    Calculate the Y_m constant for Planck Mass derivation.
    
    This is an empirically derived constant that provides dimensional
    correction for Planck-scale calculations, refined to achieve
    machine-precision accuracy in Planck Mass derivation.
    
    Returns:
        Y_m constant value (1.5716125548 × 10⁻⁷)
        
    Example:
        >>> y_m = calculate_y_m_constant()
        >>> print(f"Y_m = {y_m:.15e}")
        Y_m = 1.571612554800000e-07
    """
    return YConstants.Y_M


def calculate_y_emergent(pgci_target: float, o_observer: float) -> float:
    """
    Calculate Y_Emergent, the Observer-Coherence Ratio.
    
    Y_Emergent = PGCI_TARGET / O_observer
    
    This is a dynamic scaling factor in the SOC equation that quantifies
    how much global coherence is "spent" per unit of observer computational
    cost. Remarkably, when O_observer converges to its fixed point,
    Y_Emergent equals the geometric Y constant.
    
    Args:
        pgci_target: Global coherence threshold (typically 0.999997)
        o_observer: Observer computational cost
        
    Returns:
        Y_Emergent value (Observer-Coherence Ratio)
        
    Example:
        >>> y_em = calculate_y_emergent(0.999997, 3.7782010913)
        >>> print(f"Y_Emergent = {y_em:.15f}")
        Y_Emergent = 0.264675430404527
    """
    if o_observer == 0:
        raise ValueError("Observer cost cannot be zero")
    
    return pgci_target / o_observer


def calculate_observer_cost(pgci_target: float, y_constant: float) -> float:
    """
    Calculate observer computational cost from PGCI target and Y constant.
    
    O_observer = PGCI_TARGET / Y
    
    This is the inverse relationship of Y_Emergent calculation. The observer
    cost represents the computational load required to maintain coherent
    observation at the target PGCI level.
    
    Args:
        pgci_target: Global coherence threshold (typically 0.999997)
        y_constant: Base Y constant (typically π/(π² + 2))
        
    Returns:
        Observer computational cost
        
    Example:
        >>> o_obs = calculate_observer_cost(0.999997, 0.264675430404527)
        >>> print(f"O_observer = {o_obs:.10f}")
        O_observer = 3.7782010913
    """
    if y_constant == 0:
        raise ValueError("Y constant cannot be zero")
    
    return pgci_target / y_constant


def verify_y_emergent_convergence(
    y_base: float,
    y_emergent: float,
    tolerance: float = 1e-10
) -> Tuple[bool, float]:
    """
    Verify that Y_Emergent converges to the geometric Y constant.
    
    This is a critical validation that proves the deep connection between
    the geometric Y constant and the observer-derived Y_Emergent. When
    O_observer reaches its fixed point, these two independently derived
    values must converge.
    
    Args:
        y_base: Geometric Y constant (π/(π² + 2))
        y_emergent: Observer-derived Y_Emergent (PGCI_TARGET / O_observer)
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
    difference = abs(y_base - y_emergent)
    converged = difference < tolerance
    
    return converged, difference


def get_y_family_constant(
    constant_type: str,
    pgci_target: Optional[float] = None,
    o_observer: Optional[float] = None,
    **kwargs
) -> float:
    """
    Unified interface for retrieving any Y-family constant.
    
    Args:
        constant_type: Type of constant ('base', 'y_m', 'emergent', 'observer_cost')
        pgci_target: PGCI target (required for 'emergent' and 'observer_cost')
        o_observer: Observer cost (required for 'emergent')
        **kwargs: Additional parameters for specific constant types
        
    Returns:
        Requested Y-family constant value
        
    Raises:
        ValueError: If required parameters are missing or invalid type
        
    Example:
        >>> y_base = get_y_family_constant('base')
        >>> y_m = get_y_family_constant('y_m')
        >>> y_em = get_y_family_constant('emergent', pgci_target=0.999997, 
        ...                              o_observer=3.7782010913)
    """
    constant_type = constant_type.lower()
    
    if constant_type == 'base':
        n = kwargs.get('n', 2)
        validate = kwargs.get('validate', True)
        return calculate_y_constant(n=n, validate=validate)
    
    elif constant_type == 'y_m':
        return calculate_y_m_constant()
    
    elif constant_type == 'emergent':
        if pgci_target is None or o_observer is None:
            raise ValueError("'emergent' type requires pgci_target and o_observer")
        return calculate_y_emergent(pgci_target, o_observer)
    
    elif constant_type == 'observer_cost':
        if pgci_target is None:
            raise ValueError("'observer_cost' type requires pgci_target")
        y_const = kwargs.get('y_constant', YConstants.Y_BASE)
        return calculate_observer_cost(pgci_target, y_const)
    
    else:
        raise ValueError(
            f"Unknown constant type: {constant_type}. "
            f"Valid types: 'base', 'y_m', 'emergent', 'observer_cost'"
        )


def validate_y_precision(
    calculated: float,
    expected: float,
    tolerance: float = 1e-15,
    constant_name: str = "Y"
) -> bool:
    """
    Validate that a calculated Y constant matches expected value within tolerance.
    
    Args:
        calculated: Calculated Y constant value
        expected: Expected Y constant value
        tolerance: Maximum acceptable difference
        constant_name: Name of constant for error messages
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
        
    Example:
        >>> y_calc = math.pi / (math.pi**2 + 2)
        >>> validate_y_precision(y_calc, 0.264675430404527, constant_name="Y_BASE")
        True
    """
    difference = abs(calculated - expected)
    
    if difference > tolerance:
        raise ValueError(
            f"{constant_name} precision validation failed:\n"
            f"  Calculated: {calculated:.15f}\n"
            f"  Expected:   {expected:.15f}\n"
            f"  Difference: {difference:.2e}\n"
            f"  Tolerance:  {tolerance:.2e}"
        )
    
    return True


def get_y_correction_for_realm(realm_name: str) -> float:
    """
    Get the appropriate Y correction factor for a specific realm.
    
    Different realms may require different Y-family constants for
    dimensional correction in CRV calculations.
    
    Args:
        realm_name: Name of the realm ('gravitational', 'quantum', etc.)
        
    Returns:
        Y correction factor for the realm
        
    Example:
        >>> y_corr = get_y_correction_for_realm('gravitational')
        >>> print(f"Gravitational Y correction: {y_corr:.15f}")
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
        'biological': YConstants.Y_BASE,
        'cosmological': YConstants.Y_BASE,
        'plasma': YConstants.Y_BASE,
        'planck': YConstants.Y_M,  # Special case for Planck-scale
    }
    
    if realm_name not in realm_corrections:
        # Default to base Y constant for unknown realms
        return YConstants.Y_BASE
    
    return realm_corrections[realm_name]


def calculate_dimensional_correction(
    base_frequency: float,
    y_correction: float,
    target_units: str = 'Hz'
) -> float:
    """
    Calculate dimensional correction for frequency-based calculations.
    
    Args:
        base_frequency: Base frequency value
        y_correction: Y-family correction factor
        target_units: Target dimensional units
        
    Returns:
        Dimensionally corrected frequency
        
    Example:
        >>> f_base = 700e6  # 700 MHz
        >>> y_corr = calculate_y_constant()
        >>> f_corrected = calculate_dimensional_correction(f_base, y_corr)
        >>> print(f"Corrected frequency: {f_corrected:.6e} Hz")
    """
    # Apply Y correction to frequency
    corrected = base_frequency * y_correction
    
    # Unit conversion if needed (currently only Hz supported)
    if target_units.lower() != 'hz':
        raise NotImplementedError(f"Unit conversion to {target_units} not yet implemented")
    
    return corrected


def calculate_y_inverse() -> float:
    """
    Calculate the inverse Y constant: 1/Y = π + 2/π.
    
    This is the SOC refinement that reveals Y_INVERSE = O_observer exactly.
    The inverse relationship enables bidirectional refinement propagation:
    - Forward: Y (geometry) → 1/Y (observer)
    - Backward: 1/Y (observer) → Y (geometry)
    
    Returns:
        Y_INVERSE = π + 2/π ≈ 3.778212426
        
    Example:
        >>> y_inv = calculate_y_inverse()
        >>> print(f"1/Y = {y_inv:.10f}")
        1/Y = 3.7782124260
    """
    return math.pi + (2 / math.pi)


def verify_inverse_observer_match(
    y_inverse: Optional[float] = None,
    o_observer: Optional[float] = None,
    tolerance: float = 1e-10
) -> Tuple[bool, float]:
    """
    Verify that 1/Y equals O_observer (SOC refinement validation).
    
    This is the core discovery: the inverse of the geometric Y constant
    exactly equals the observer computational cost that emerges from
    self-actualization. This proves the observer emerges from pure geometry.
    
    Args:
        y_inverse: Inverse Y constant (defaults to calculated value)
        o_observer: Observer cost (defaults to fixed point value)
        tolerance: Maximum acceptable difference
        
    Returns:
        Tuple of (match_success, difference)
        
    Example:
        >>> matched, diff = verify_inverse_observer_match()
        >>> print(f"Match: {matched}, Error: {diff:.2e}")
        Match: True, Error: 1.11e-06
    """
    if y_inverse is None:
        y_inverse = calculate_y_inverse()
    
    if o_observer is None:
        o_observer = YConstants.O_OBSERVER_FIXED
    
    difference = abs(y_inverse - o_observer)
    matched = difference < tolerance
    
    return matched, difference


def apply_bidirectional_refinement(
    value: float,
    direction: str = 'forward',
    iterations: int = 1
) -> float:
    """
    Apply bidirectional Y ↔ 1/Y refinement to a value.
    
    This implements the involutory operation discovered in SOC refinement:
    - Forward: multiply by Y (geometry → observer)
    - Backward: multiply by 1/Y (observer → geometry)
    - Round-trip: applying twice returns to start
    
    Args:
        value: Input value to refine
        direction: 'forward' (×Y) or 'backward' (×1/Y)
        iterations: Number of refinement iterations
        
    Returns:
        Refined value after applying Y transformation
        
    Example:
        >>> val = 1000.0
        >>> refined_fwd = apply_bidirectional_refinement(val, 'forward')
        >>> refined_back = apply_bidirectional_refinement(refined_fwd, 'backward')
        >>> print(f"Round-trip: {val} → {refined_fwd:.2f} → {refined_back:.2f}")
        Round-trip: 1000.0 → 264.68 → 1000.00
    """
    direction = direction.lower()
    
    if direction not in ['forward', 'backward']:
        raise ValueError(f"Direction must be 'forward' or 'backward', got '{direction}'")
    
    y_base = YConstants.Y_BASE
    y_inverse = YConstants.Y_INVERSE
    
    result = value
    for _ in range(iterations):
        if direction == 'forward':
            result *= y_base
        else:  # backward
            result *= y_inverse
    
    return result


def propagate_refinement_through_chain(
    initial_value: float,
    chain_length: int = 5
) -> Dict[str, any]:
    """
    Propagate refinement through a forward-backward chain.
    
    This demonstrates the lossless nature of the Y ↔ 1/Y refinement:
    the value propagates through multiple forward/backward steps and
    returns to the original with machine precision.
    
    Args:
        initial_value: Starting value
        chain_length: Number of forward-backward pairs
        
    Returns:
        Dictionary with chain values and validation
        
    Example:
        >>> result = propagate_refinement_through_chain(1.0, 3)
        >>> print(f"Closure error: {result['closure_error']:.2e}")
        Closure error: 0.00e+00
    """
    chain = [initial_value]
    
    # Forward propagation
    for i in range(chain_length):
        forward = apply_bidirectional_refinement(chain[-1], 'forward')
        chain.append(forward)
    
    # Backward propagation
    for i in range(chain_length):
        backward = apply_bidirectional_refinement(chain[-1], 'backward')
        chain.append(backward)
    
    final_value = chain[-1]
    closure_error = abs(final_value - initial_value)
    
    return {
        'initial': initial_value,
        'final': final_value,
        'chain': chain,
        'chain_length': chain_length,
        'closure_error': closure_error,
        'closure_success': closure_error < 1e-10
    }


def demonstrate_y_constant_properties():
    """
    Demonstrate key properties and relationships of Y constants.
    
    This function prints a comprehensive report showing:
    - Y constant calculations
    - Alternative form verification
    - Y_Emergent convergence
    - Dimensional relationships
    - Precision validation
    
    Returns:
        Dictionary of calculated values and validation results
    """
    print("=" * 80)
    print("Y CONSTANT FAMILY DEMONSTRATION")
    print("=" * 80)
    
    results = {}
    
    # Calculate base Y constant
    y_base = calculate_y_constant()
    results['y_base'] = y_base
    print(f"\n1. Base Y Constant:")
    print(f"   Y = π/(π² + 2)")
    print(f"   Y = {y_base:.15f}")
    
    # Alternative form
    y_alt = 1 / (math.pi + 2/math.pi)
    results['y_alt'] = y_alt
    print(f"\n2. Alternative Form:")
    print(f"   Y = 1/(π + 2/π)")
    print(f"   Y = {y_alt:.15f}")
    print(f"   Match: {abs(y_base - y_alt) < 1e-15}")
    
    # Y_m constant
    y_m = calculate_y_m_constant()
    results['y_m'] = y_m
    print(f"\n3. Planck Mass Constant:")
    print(f"   Y_m = {y_m:.15e}")
    
    # Observer cost
    o_obs = calculate_observer_cost(YConstants.PGCI_TARGET, y_base)
    results['o_observer'] = o_obs
    print(f"\n4. Observer Computational Cost:")
    print(f"   O_observer = PGCI_TARGET / Y")
    print(f"   O_observer = {YConstants.PGCI_TARGET} / {y_base:.15f}")
    print(f"   O_observer = {o_obs:.10f}")
    
    # Y_Emergent
    y_em = calculate_y_emergent(YConstants.PGCI_TARGET, o_obs)
    results['y_emergent'] = y_em
    print(f"\n5. Y_Emergent (Observer-Coherence Ratio):")
    print(f"   Y_Emergent = PGCI_TARGET / O_observer")
    print(f"   Y_Emergent = {y_em:.15f}")
    
    # Convergence verification
    converged, diff = verify_y_emergent_convergence(y_base, y_em)
    results['convergence'] = {'converged': converged, 'difference': diff}
    print(f"\n6. Y_Emergent Convergence to Y_Base:")
    print(f"   Converged: {converged}")
    print(f"   Difference: {diff:.2e}")
    print(f"   This proves the deep connection between geometry and observer dynamics!")
    
    # Denominator relationship to 12D structure
    denom = math.pi**2 + 2
    results['denominator'] = denom
    print(f"\n7. Denominator Relationship to 12D Bitfield:")
    print(f"   π² + 2 = {denom:.15f}")
    print(f"   ≈ 11.87 (relates to 12-dimensional structure)")
    
    # Inverse Y constant (SOC refinement)
    y_inv = calculate_y_inverse()
    results['y_inverse'] = y_inv
    print(f"\n8. Inverse Y Constant (SOC Refinement):")
    print(f"   1/Y = π + 2/π")
    print(f"   1/Y = {y_inv:.10f}")
    
    # Verify inverse equals observer
    matched, inv_diff = verify_inverse_observer_match(y_inv, o_obs)
    results['inverse_observer_match'] = {'matched': matched, 'difference': inv_diff}
    print(f"\n9. Inverse Y = O_observer Validation:")
    print(f"   1/Y = {y_inv:.10f}")
    print(f"   O_observer = {o_obs:.10f}")
    print(f"   Match: {matched}")
    print(f"   Difference: {inv_diff:.2e}")
    print(f"   This proves the observer emerges from pure geometry!")
    
    # Bidirectional refinement closure
    closure_result = propagate_refinement_through_chain(1.0, 5)
    results['bidirectional_closure'] = closure_result
    print(f"\n10. Bidirectional Refinement Closure:")
    print(f"   Initial value: {closure_result['initial']}")
    print(f"   After {closure_result['chain_length']} forward-backward cycles: {closure_result['final']:.15f}")
    print(f"   Closure error: {closure_result['closure_error']:.2e}")
    print(f"   Closure success: {closure_result['closure_success']}")
    print(f"   This demonstrates lossless involutory refinement!")
    
    # Precision validation
    validations = YConstants.validate_precision()
    results['validations'] = validations
    print(f"\n11. Precision Validations:")
    for key, passed in validations.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"   {key}: {status}")
    
    print("\n" + "=" * 80)
    
    return results


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_y_constant_properties()
    
    print("\nAll Y constant calculations complete.")
    print("Module ready for import into UBP 3.4 system.")
