# Cell 66 from UBP_UNIFIED_SYSTEM_1.ipynb


# @title First Principles Mathematical Library

"""
First Principles Mathematical Library
======================================

This module implements fundamental mathematical functions using ONLY:
- Basic arithmetic operations (+, -, *, /, **)
- Integer operations
- Loops and conditionals

NO external libraries are used. Everything is built from Taylor/Maclaurin series
and fundamental algorithms.

Author: Manus AI
Date: December 06, 2025
"""

def factorial(n: int) -> int:
    """
    Calculate n! using only multiplication.

    Args:
        n: Non-negative integer

    Returns:
        n! = n × (n-1) × ... × 2 × 1

    Example:
        factorial(5) = 120
    """
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def abs_value(x: float) -> float:
    """
    Absolute value using only conditional logic.

    Args:
        x: Any real number

    Returns:
        |x|
    """
    return x if x >= 0 else -x


def sqrt_newton(x: float, tolerance: float = 1e-15, max_iterations: int = 100) -> float:
    """
    Calculate square root using Newton-Raphson method.
    Uses only arithmetic operations - no library functions.

    Newton's method for sqrt(x):
        y_{n+1} = (y_n + x/y_n) / 2

    Starting guess: y_0 = x/2 for x > 1, y_0 = x for x <= 1

    Args:
        x: Number to take square root of (must be non-negative)
        tolerance: Convergence criterion
        max_iterations: Maximum iterations before giving up

    Returns:
        sqrt(x) accurate to tolerance

    Raises:
        ValueError: If x < 0
        RuntimeError: If doesn't converge
    """
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0

    # Initial guess: use x/2 for large x, x for small x
    y = x / 2 if x > 1 else x

    for iteration in range(max_iterations):
        y_new = (y + x / y) / 2

        # Check convergence
        if abs_value(y_new - y) < tolerance:
            return y_new

        y = y_new

    raise RuntimeError(f"sqrt did not converge after {max_iterations} iterations")


def sin_taylor(x: float, terms: int = 20) -> float:
    """
    Calculate sin(x) using Taylor series expansion around 0.
    Uses only arithmetic and factorial - no library functions.

    sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
           = Σ((-1)^n × x^(2n+1) / (2n+1)!)  for n=0,1,2,...

    Args:
        x: Angle in radians
        terms: Number of terms in series (default 20 gives ~15 digit accuracy)

    Returns:
        sin(x) accurate to machine precision for |x| < 2π

    Note:
        For large |x|, should reduce to range [-π, π] first, but that requires
        knowing π! For our use case (Archimedes method), x will always be small.
    """
    result = 0.0

    for n in range(terms):
        # Calculate term: (-1)^n × x^(2n+1) / (2n+1)!
        power = 2 * n + 1
        sign = 1 if n % 2 == 0 else -1

        # Calculate x^power
        x_power = 1.0
        for _ in range(power):
            x_power *= x

        # Calculate (2n+1)!
        fact = factorial(power)

        # Add term to sum
        term = sign * x_power / fact
        result += term

        # Early termination if term becomes negligible
        if abs_value(term) < 1e-16:
            break

    return result


def cos_taylor(x: float, terms: int = 20) -> float:
    """
    Calculate cos(x) using Taylor series expansion around 0.
    Uses only arithmetic and factorial - no library functions.

    cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
           = Σ((-1)^n × x^(2n) / (2n)!)  for n=0,1,2,...

    Args:
        x: Angle in radians
        terms: Number of terms in series

    Returns:
        cos(x) accurate to machine precision for |x| < 2π
    """
    result = 0.0

    for n in range(terms):
        # Calculate term: (-1)^n × x^(2n) / (2n)!
        power = 2 * n
        sign = 1 if n % 2 == 0 else -1

        # Calculate x^power
        x_power = 1.0
        for _ in range(power):
            x_power *= x

        # Calculate (2n)!
        fact = factorial(power)

        # Add term to sum
        term = sign * x_power / fact
        result += term

        # Early termination if term becomes negligible
        if abs_value(term) < 1e-16:
            break

    return result


def power_int(base: float, exponent: int) -> float:
    """
    Calculate base^exponent for integer exponents using only multiplication.

    Args:
        base: The base number
        exponent: Integer exponent (can be negative)

    Returns:
        base^exponent
    """
    if exponent == 0:
        return 1.0

    if exponent < 0:
        return 1.0 / power_int(base, -exponent)

    result = 1.0
    for _ in range(exponent):
        result *= base

    return result


# ============================================================================
# Validation and Testing Functions
# ============================================================================

def validate_first_principles_math():
    """
    Validate all first principles functions against known values.
    This uses NO external libraries for the validation itself.
    """
    print("=" * 80)
    print("VALIDATING FIRST PRINCIPLES MATHEMATICAL LIBRARY")
    print("=" * 80)
    print()

    # Test factorial
    print("1. Testing factorial():")
    test_cases_factorial = [(0, 1), (1, 1), (5, 120), (10, 3628800)]
    for n, expected in test_cases_factorial:
        result = factorial(n)
        status = "✓" if result == expected else "✗"
        print(f"   {status} factorial({n}) = {result} (expected {expected})")
    print()

    # Test sqrt
    print("2. Testing sqrt_newton():")
    test_cases_sqrt = [
        (0, 0.0),
        (1, 1.0),
        (4, 2.0),
        (9, 3.0),
        (2, 1.41421356237),  # Known value
        (0.25, 0.5)
    ]
    for x, expected in test_cases_sqrt:
        result = sqrt_newton(x)
        error = abs_value(result - expected)
        status = "✓" if error < 1e-10 else "✗"
        print(f"   {status} sqrt({x}) = {result:.11f} (expected {expected:.11f}, error {error:.2e})")
    print()

    # Test sin - we'll use known exact values
    print("3. Testing sin_taylor():")
    test_cases_sin = [
        (0.0, 0.0),           # sin(0) = 0
        (1.0, 0.8414709848),  # sin(1) ≈ 0.8414709848
        (0.5, 0.4794255386),  # sin(0.5) ≈ 0.4794255386
    ]
    for x, expected in test_cases_sin:
        result = sin_taylor(x)
        error = abs_value(result - expected)
        status = "✓" if error < 1e-10 else "✗"
        print(f"   {status} sin({x}) = {result:.10f} (expected {expected:.10f}, error {error:.2e})")
    print()

    # Test cos
    print("4. Testing cos_taylor():")
    test_cases_cos = [
        (0.0, 1.0),           # cos(0) = 1
        (1.0, 0.5403023059),  # cos(1) ≈ 0.5403023059
        (0.5, 0.8775825619),  # cos(0.5) ≈ 0.8775825619
    ]
    for x, expected in test_cases_cos:
        result = cos_taylor(x)
        error = abs_value(result - expected)
        status = "✓" if error < 1e-10 else "✗"
        print(f"   {status} cos({x}) = {result:.10f} (expected {expected:.10f}, error {error:.2e})")
    print()

    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    validate_first_principles_math()