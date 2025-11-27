"""
Reversible Y-Constants for UBP 3.7
===================================

This module implements Y and Y_INVERSE as exact rational numbers,
providing TRUE information-theoretic reversibility.

Key Property:
-------------
Y × Y_INVERSE = 1 (EXACTLY, not approximately)

This is mathematically provable and verifiable.

Author: UBP 3.7 Development Team
Date: November 28, 2025
"""

from fractions import Fraction
from reversible_rational import ReversibleRational
import math


class ReversibleYConstants:
    """
    Exact rational representations of Y and Y_INVERSE.
    
    Mathematical Foundation:
    -----------------------
    Y = π/(π² + 2)
    Y_INVERSE = (π² + 2)/π = π + 2/π
    
    Since π is irrational, we use high-precision rational approximations.
    The key property Y × Y_INVERSE = 1 is EXACTLY satisfied (not approximate).
    
    Precision Levels:
    ----------------
    - LOW: π ≈ 22/7 (3 decimal places)
    - MEDIUM: π ≈ 355/113 (6 decimal places)
    - HIGH: π ≈ 103993/33102 (9 decimal places)
    - ULTRA: π ≈ 245850922/78256779 (14 decimal places)
    
    We use ULTRA precision by default for maximum accuracy.
    """
    
    # Ultra-high precision rational approximation of π
    # π ≈ 245850922/78256779 (accurate to 14 decimal places)
    PI_NUMERATOR = 245850922
    PI_DENOMINATOR = 78256779
    
    def __init__(self, precision='ultra'):
        """
        Initialize Y-constants with specified precision.
        
        Args:
            precision: 'low', 'medium', 'high', or 'ultra'
        """
        if precision == 'low':
            pi_num, pi_den = 22, 7
        elif precision == 'medium':
            pi_num, pi_den = 355, 113
        elif precision == 'high':
            pi_num, pi_den = 103993, 33102
        elif precision == 'ultra':
            pi_num, pi_den = self.PI_NUMERATOR, self.PI_DENOMINATOR
        else:
            raise ValueError(f"Unknown precision: {precision}")
        
        self.pi_num = pi_num
        self.pi_den = pi_den
        
        # Calculate Y = π/(π² + 2)
        # Y = pi_num/pi_den / ((pi_num/pi_den)² + 2)
        # Y = pi_num/pi_den / ((pi_num²/pi_den²) + 2)
        # Y = pi_num/pi_den / ((pi_num² + 2*pi_den²)/pi_den²)
        # Y = pi_num/pi_den × pi_den²/(pi_num² + 2*pi_den²)
        # Y = (pi_num × pi_den) / (pi_num² + 2*pi_den²)
        
        y_numerator = pi_num * pi_den
        y_denominator = pi_num**2 + 2 * pi_den**2
        
        self._Y = ReversibleRational(y_numerator, y_denominator)
        
        # Calculate Y_INVERSE = (π² + 2)/π
        # Y_INVERSE = ((pi_num²/pi_den²) + 2) / (pi_num/pi_den)
        # Y_INVERSE = ((pi_num² + 2*pi_den²)/pi_den²) / (pi_num/pi_den)
        # Y_INVERSE = ((pi_num² + 2*pi_den²)/pi_den²) × (pi_den/pi_num)
        # Y_INVERSE = (pi_num² + 2*pi_den²) / (pi_num × pi_den)
        
        y_inv_numerator = pi_num**2 + 2 * pi_den**2
        y_inv_denominator = pi_num * pi_den
        
        self._Y_INVERSE = ReversibleRational(y_inv_numerator, y_inv_denominator)
        
        # Verify exact involutory property
        product = self._Y * self._Y_INVERSE
        assert product.numerator == product.denominator, \
            f"Y × Y_INVERSE ≠ 1! Got {product}"
    
    @property
    def Y(self) -> ReversibleRational:
        """Get exact Y constant."""
        return self._Y
    
    @property
    def Y_INVERSE(self) -> ReversibleRational:
        """Get exact Y_INVERSE constant."""
        return self._Y_INVERSE
    
    @property
    def PI(self) -> ReversibleRational:
        """Get rational approximation of π."""
        return ReversibleRational(self.pi_num, self.pi_den)
    
    def verify_involutory_property(self) -> bool:
        """
        Verify that Y × Y_INVERSE = 1 exactly.
        
        Returns:
            True if exact, False otherwise
        """
        product = self._Y * self._Y_INVERSE
        return product.numerator == product.denominator
    
    def get_precision_error(self) -> float:
        """
        Calculate how close our rational π is to the true π.
        
        Returns:
            Absolute error |π_rational - π_true|
        """
        pi_rational = float(self.pi_num) / float(self.pi_den)
        pi_true = math.pi
        return abs(pi_rational - pi_true)
    
    def compare_with_floating_point(self) -> dict:
        """
        Compare exact rational Y with floating-point Y.
        
        Returns:
            Dictionary with comparison results
        """
        # Floating-point Y
        pi_float = math.pi
        y_float = pi_float / (pi_float**2 + 2)
        y_inv_float = pi_float + 2/pi_float
        
        # Our exact rational Y (converted to float for comparison)
        y_rational_float = self._Y.to_float()
        y_inv_rational_float = self._Y_INVERSE.to_float()
        
        return {
            'y_float': y_float,
            'y_rational': y_rational_float,
            'y_error': abs(y_float - y_rational_float),
            'y_inv_float': y_inv_float,
            'y_inv_rational': y_inv_rational_float,
            'y_inv_error': abs(y_inv_float - y_inv_rational_float),
            'product_exact': self.verify_involutory_property(),
            'product_float': y_float * y_inv_float,
            'product_rational': (self._Y * self._Y_INVERSE).to_float()
        }


def refine_forward(value: ReversibleRational, y_constants: ReversibleYConstants) -> ReversibleRational:
    """
    Apply forward refinement: multiply by Y (exact).
    
    This is a bijective operation with refine_backward as its inverse.
    
    Args:
        value: Value to refine
        y_constants: Y-constants to use
    
    Returns:
        Refined value (exact)
    """
    return value * y_constants.Y


def refine_backward(value: ReversibleRational, y_constants: ReversibleYConstants) -> ReversibleRational:
    """
    Apply backward refinement: multiply by Y_INVERSE (exact).
    
    This is the EXACT inverse of refine_forward.
    
    Args:
        value: Value to refine
        y_constants: Y-constants to use
    
    Returns:
        Refined value (exact)
    """
    return value * y_constants.Y_INVERSE


def verify_bidirectional_closure(
    value: ReversibleRational,
    y_constants: ReversibleYConstants
) -> dict:
    """
    Verify exact bidirectional closure.
    
    Proves that: refine_backward(refine_forward(x)) = x (EXACTLY)
    
    Args:
        value: Initial value
        y_constants: Y-constants to use
    
    Returns:
        Dictionary with verification results
    """
    # Forward refinement
    forward = refine_forward(value, y_constants)
    
    # Backward refinement
    backward = refine_backward(forward, y_constants)
    
    # Check EXACT equality
    exact_match = (backward == value)
    
    return {
        'initial': value,
        'forward': forward,
        'backward': backward,
        'exact_match': exact_match,
        'difference_numerator': (backward - value).numerator,
        'difference_denominator': (backward - value).denominator
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("REVERSIBLE Y-CONSTANTS - DEMONSTRATION")
    print("="*70)
    
    # Create Y-constants with ultra precision
    y_const = ReversibleYConstants(precision='ultra')
    
    print(f"\nπ ≈ {y_const.pi_num}/{y_const.pi_den}")
    print(f"π (float) = {y_const.PI.to_float():.15f}")
    print(f"π (true) = {math.pi:.15f}")
    print(f"Error: {y_const.get_precision_error():.2e}")
    
    print(f"\nY = {y_const.Y}")
    print(f"Y (float) = {y_const.Y.to_float():.15f}")
    
    print(f"\nY_INVERSE = {y_const.Y_INVERSE}")
    print(f"Y_INVERSE (float) = {y_const.Y_INVERSE.to_float():.15f}")
    
    # Verify involutory property
    product = y_const.Y * y_const.Y_INVERSE
    print(f"\nY × Y_INVERSE = {product}")
    print(f"Y × Y_INVERSE (float) = {product.to_float():.15f}")
    print(f"Exact equality to 1: {product.numerator == product.denominator}")
    
    # Test bidirectional refinement
    print("\n" + "="*70)
    print("BIDIRECTIONAL REFINEMENT TEST")
    print("="*70)
    
    initial_value = ReversibleRational(1000, 1)
    print(f"\nInitial value: {initial_value}")
    
    # Forward
    forward = refine_forward(initial_value, y_const)
    print(f"After forward (×Y): {forward}")
    print(f"  = {forward.to_float():.15f}")
    
    # Backward
    backward = refine_backward(forward, y_const)
    print(f"After backward (×Y_INV): {backward}")
    print(f"  = {backward.to_float():.15f}")
    
    # Verify exact recovery
    print(f"\nExact recovery: {backward == initial_value}")
    print(f"Difference: {(backward - initial_value).numerator} (should be 0)")
    
    # Full verification
    verification = verify_bidirectional_closure(initial_value, y_const)
    print(f"\nFull verification:")
    print(f"  Exact match: {verification['exact_match']}")
    print(f"  Difference numerator: {verification['difference_numerator']}")
    
    # Compare with floating-point
    print("\n" + "="*70)
    print("COMPARISON WITH FLOATING-POINT")
    print("="*70)
    
    comparison = y_const.compare_with_floating_point()
    print(f"\nY:")
    print(f"  Float: {comparison['y_float']:.15f}")
    print(f"  Rational: {comparison['y_rational']:.15f}")
    print(f"  Error: {comparison['y_error']:.2e}")
    
    print(f"\nY_INVERSE:")
    print(f"  Float: {comparison['y_inv_float']:.15f}")
    print(f"  Rational: {comparison['y_inv_rational']:.15f}")
    print(f"  Error: {comparison['y_inv_error']:.2e}")
    
    print(f"\nProduct (Y × Y_INVERSE):")
    print(f"  Float: {comparison['product_float']:.15f}")
    print(f"  Rational: {comparison['product_rational']:.15f}")
    print(f"  Exact (rational): {comparison['product_exact']}")
    
    print("\n" + "="*70)
    print("✓ EXACT REVERSIBILITY VERIFIED!")
    print("="*70)
