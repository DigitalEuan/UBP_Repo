UBP Metrics (Exact) v4.x
=======================

Goal: strict float-free metrics suitable for core UBP logic.

Design rules:
- No floats, no math.pi, no numpy.
- All computations return Fractions (or ints / enums).
- π is represented as a rational approximation derived from *integer* continued fraction coefficients.
  This keeps the entire system float-free while remaining deterministic and reproducible.

IMPORTANT:
- If you want an absolutely symbolic π (unevaluated), replace `pi_approx()` usage with an expression
  object of your choice. This module keeps things runnable without external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Dict, Optional

class CoherenceRegime(Enum):
    ONBIT = "OnBit"               # NRCI >= target
    COHERENT = "Coherent"         # 1/2 <= NRCI < target
    TRANSITIONAL = "Transitional" # 1/10 <= NRCI < 1/2
    SUBCOHERENT = "Subcoherent"   # NRCI < 1/10

# Continued-fraction coefficients for π: [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, ...]
# Source is standard and widely published; coefficients are integers, so representation is exact.
_PI_CF = [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2, 2, 2, 1, 84, 2, 1, 1, 15]

def _cf_to_fraction(a) -> Fraction:
    """Convert continued fraction coefficients to a Fraction, exact."""
    if not a:
        raise ValueError("continued fraction coefficients empty")
    x = Fraction(a[-1], 1)
    for c in reversed(a[:-1]):
        x = Fraction(c, 1) + Fraction(1, x)
    return x

def pi_approx(terms: int = 10) -> Fraction:
    """
    Deterministic rational approximation of π using `terms` CF coefficients.

    terms=5 gives 355/113.
    """
    if terms < 1:
        raise ValueError("terms must be >= 1")
    terms = min(terms, len(_PI_CF))
    return _cf_to_fraction(_PI_CF[:terms])

@dataclass(frozen=True)
class UBPConstantsExact:
    # Precision knob: more CF terms => larger numerator/denominator (still exact).
    PI_TERMS: int = 6  # 6 already includes 355/113 (excellent) and stays lightweight.

    # Coherence target as an exact rational
    PGCI_TARGET: Fraction = Fraction(9999999, 10000000)  # 0.9999999

    def pi(self) -> Fraction:
        return pi_approx(self.PI_TERMS)

    def observer_fixed_point(self) -> Fraction:
        # π + 2/π, exact under the rational π approximation
        p = self.pi()
        return p + Fraction(2, 1) / p

    def y_constant(self) -> Fraction:
        return Fraction(1, 1) / self.observer_fixed_point()

class UBPObserverExact:
    def __init__(self, c: UBPConstantsExact):
        self.c = c

    def get_base_cost(self) -> Fraction:
        return self.c.observer_fixed_point()

    def calculate_realm_cost(self, realm_complexity: Fraction = Fraction(1,1), dimensions: int = 6) -> Fraction:
        # (dimensions/6) is exact
        return self.get_base_cost() * realm_complexity * Fraction(dimensions, 6)

class UBPCoherenceExact:
    @staticmethod
    def clamp01(x: Fraction) -> Fraction:
        if x < 0:
            return Fraction(0,1)
        if x > 1:
            return Fraction(1,1)
        return x

    @staticmethod
    def calculate_nrci(observed_variance: Fraction, theoretical_variance: Fraction = Fraction(1,1)) -> Fraction:
        # NRCI = 1 - observed/theoretical
        if theoretical_variance == 0:
            raise ZeroDivisionError("theoretical_variance must be nonzero")
        return UBPCoherenceExact.clamp01(Fraction(1,1) - (observed_variance / theoretical_variance))

    @staticmethod
    def calculate_glr_nrci(error_sum: int, n_toggles: int) -> Fraction:
        # denominator = 9 * n_toggles, exact
        if n_toggles <= 0:
            raise ValueError("n_toggles must be > 0")
        denom = 9 * n_toggles
        return UBPCoherenceExact.clamp01(Fraction(1,1) - Fraction(error_sum, denom))

    @staticmethod
    def get_regime(nrci_value: Fraction, target: Fraction) -> CoherenceRegime:
        if nrci_value >= target:
            return CoherenceRegime.ONBIT
        if nrci_value >= Fraction(1,2):
            return CoherenceRegime.COHERENT
        if nrci_value >= Fraction(1,10):
            return CoherenceRegime.TRANSITIONAL
        return CoherenceRegime.SUBCOHERENT

class UBPMetricsExact:
    def __init__(self, constants: Optional[UBPConstantsExact] = None):
        self.constants = constants or UBPConstantsExact()
        self.observer = UBPObserverExact(self.constants)
        self.coherence = UBPCoherenceExact()

    # --- Compatibility helpers (float-free) ---
    def analyze_state(self, variance: Fraction, realm: str = "standard") -> Dict[str, object]:
        nrci = self.coherence.calculate_nrci(variance)
        regime = self.coherence.get_regime(nrci, self.constants.PGCI_TARGET)
        return {
            "nrci": nrci,
            "regime": regime.value,
            "observer_cost": self.observer.get_base_cost(),
            "is_stable": nrci >= Fraction(1,2),
        }

# Global instance (mirrors prior API style, but exact)
METRICS_EXACT = UBPMetricsExact()

if __name__ == "__main__":
    c = METRICS_EXACT.constants
    print("UBP Metrics (Exact) Initialized")
    print("  π approx =", c.pi(), "≈", float(c.pi()))
    print("  observer_fixed_point =", c.observer_fixed_point(), "≈", float(c.observer_fixed_point()))
    print("  Y =", c.y_constant(), "≈", float(c.y_constant()))