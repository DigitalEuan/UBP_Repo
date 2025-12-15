# Cell 65 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title TICK-BASED π FROM BINARY RELATIONAL GEOMETRY
#!/usr/bin/env python3
"""
TICK-BASED π FROM BINARY RELATIONAL GEOMETRY
No floating point. No assumed π. Only toggles and relations.
Directly integrates with your ExactNumber system.
"""

from fractions import Fraction
from typing import Tuple, Any, List, Dict, Optional, Union
import math
import random
from dataclasses import dataclass

# For standalone execution in this cell, let's include a basic ExactNumber that handles fractions.
class ExactNumber:
    def __init__(self, value: Union[int, Fraction, 'ExactNumber']):
        if isinstance(value, ExactNumber):
            self.f = value.f
        elif isinstance(value, Fraction):
            self.f = value
        elif isinstance(value, int):
            self.f = Fraction(value)
        else:
            raise TypeError(f"Unsupported type for ExactNumber: {type(value)}")

    @property
    def doubled(self) -> int:
        doubled = self.f * 2
        if doubled.denominator != 1:
            raise ValueError(f"{self.f} is not integer or half-integer")
        return int(doubled)

    def to_float(self) -> float:
        return float(self.f)

    def to_fraction(self) -> Fraction:
        return self.f

    def __add__(self, other: Union[int, Fraction, 'ExactNumber']) -> 'ExactNumber':
        o = ExactNumber(other)
        return ExactNumber(self.f + o.f)

    def __radd__(self, other): return self.__add__(other)
    def __sub__(self, other): return ExactNumber(self.f - ExactNumber(other).f)
    def __rsub__(self, other): return ExactNumber(ExactNumber(other).f - self.f)
    def __mul__(self, other): return ExactNumber(self.f * ExactNumber(other).f)
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other): return ExactNumber(self.f / ExactNumber(other).f)
    def __rtruediv__(self, other): return ExactNumber(ExactNumber(other).f / self.f)
    def __neg__(self): return ExactNumber(-self.f)
    def __abs__(self): return ExactNumber(abs(self.f))
    def __pow__(self, exp: int): return ExactNumber(self.f ** exp)
    def __eq__(self, other):
        try:
            o = ExactNumber(other)
            return self.f == o.f
        except TypeError:
            return False

    def __lt__(self, other): return self.f < ExactNumber(other).f
    def __le__(self, other): return self.f <= ExactNumber(other).f
    def __gt__(self, other): return self.f > ExactNumber(other).f
    def __ge__(self, other): return self.f >= ExactNumber(other).f
    def __hash__(self): return hash(self.f)
    def __repr__(self): return str(self.f)
    def __int__(self) -> int:
        if self.f.denominator != 1:
            raise ValueError(f"{self.f} is not integer")
        return int(self.f)

    def round_to_nearest_integer(self) -> 'ExactNumber':
        return ExactNumber(round(self.f))

    def sqrt(self) -> 'ExactNumber':
        # Newton-Raphson method for square root, using Fractions.
        # Will return an approximation for irrational numbers within a limited number of iterations.
        if self.f < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        if self.f == 0:
            return ExactNumber(0)

        x = self.f
        guess = ExactNumber(Fraction(1)) # Initial guess for sqrt(x), start with 1

        # Iterate for a fixed number of steps to get a reasonable approximation.
        # For irrational numbers, this will not converge to exact equality.
        for _ in range(50):  # Limit iterations for better precision in approximation
            new_guess = (guess + (ExactNumber(x) / guess)) / ExactNumber(2)
            if new_guess.f == guess.f: # Check for exact convergence (for perfect squares)
                return new_guess
            guess = new_guess

        # If not exactly converged, return the best approximation found.
        return guess


def binary_relational_pi(ticks: int) -> Tuple[ExactNumber, ExactNumber]:
    """
    Derive π using Archimedes' method with binary toggle steps (doubling sides).
    Returns (lower_bound, upper_bound) for π.
    """
    if ticks < 0:
        raise ValueError("Ticks >= 0")

    # Using the areas of inscribed and circumscribed polygons for a unit circle.
    # Start with a square.
    A_in = ExactNumber(2) # Area of inscribed square (R=1)
    A_circ = ExactNumber(4) # Area of circumscribed square (R=1)

    for _ in range(ticks): # Each tick doubles the sides of the polygon
        # Recurrence relations for polygonal areas for doubled sides:
        A_in_new = (A_in * A_circ).sqrt() # New inscribed area is geometric mean
        A_circ_new = (ExactNumber(2) * A_in_new * A_circ) / (A_in_new + A_circ) # New circumscribed area is harmonic mean
        A_in = A_in_new
        A_circ = A_circ_new

    # Pi is approximated by these converging areas
    lower_bound_pi = A_in
    upper_bound_pi = A_circ

    return lower_bound_pi, upper_bound_pi


def main():
    print("="*80)
    print("TRUE BINARY RELATIONAL π VIA TICKS — CENTERLESS")
    print("="*80)

    results = []
    for ticks in range(0, 10): # Test increasing ticks up to 10 (2^10-gon)
        lower, upper = ExactNumber(3), ExactNumber(4) # Default initial rough bounds if ticks=0
        pi_est = ExactNumber(0) # Placeholder
        mu_e = ExactNumber(0) # Placeholder
        Y = ExactNumber(0) # Placeholder
        Y_inv = ExactNumber(0) # Placeholder
        error = 0.0 # Placeholder

        try:
            if ticks > 0: # Only perform iterative calculation if ticks > 0
                lower, upper = binary_relational_pi(ticks)
            pi_est = (lower + upper) / ExactNumber(2)
            Y = pi_est / (pi_est**2 + ExactNumber(2))
            Y_inv = ExactNumber(1) / Y
            mu_e = Y_inv ** 4

            # Use Fraction.from_float for reference value comparison if needed, or define constants as ExactNumber/Fraction
            experimental_mu_e = Fraction(206768283, 1000000) # As a Fraction
            error = abs(mu_e.to_float() - experimental_mu_e.real) / experimental_mu_e.real * 100
        except Exception as e:
            print(f"Skipping tick {ticks} due to error: {e}")
            continue

        results.append({
            "ticks": ticks,
            "lower_bound_pi": lower.to_float(),
            "upper_bound_pi": upper.to_float(),
            "pi_estimate": pi_est.to_float(),
            "Y": Y.to_float(),
            "Y_inv": Y_inv.to_float(),
            "muon_electron_ratio": mu_e.to_float(),
            "error_percent": error
        })

    for res in results:
        print(f"Ticks: {res['ticks']} | \u03c0\u2248{res['pi_estimate']:.8f} | \u03bc/e={res['muon_electron_ratio']:.3f} | Error {res['error_percent']:.3f}%")

    with open('pi_ubp_test.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults in pi_ubp_test.json")

if __name__ == "__main__":
    main()