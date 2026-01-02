"""
UBP Metrics (Exact) v4.x
=======================

Version: 4.2.6 Combined (Production - 100% Complete)
Author: Euan R A Craig, New Zealand
Date: 02 January 2026

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
    PI_TERMS: int = 6  
    PGCI_TARGET: Fraction = Fraction(9999999, 10000000)  

    def pi(self) -> Fraction:
        return pi_approx(self.PI_TERMS)

    def observer_fixed_point(self) -> Fraction:
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
        return self.get_base_cost() * realm_complexity * Fraction(dimensions, 6)

class UBPCoherenceExact:
    @staticmethod
    def clamp01(x: Fraction) -> Fraction:
        if x < 0: return Fraction(0,1)
        if x > 1: return Fraction(1,1)
        return x

    @staticmethod
    def calculate_nrci(observed_variance: Fraction, theoretical_variance: Fraction = Fraction(1,1)) -> Fraction:
        if theoretical_variance == 0:
            raise ZeroDivisionError("theoretical_variance must be nonzero")
        return UBPCoherenceExact.clamp01(Fraction(1,1) - (observed_variance / theoretical_variance))

    @staticmethod
    def get_regime(nrci_value: Fraction, target: Fraction) -> CoherenceRegime:
        if nrci_value >= target: return CoherenceRegime.ONBIT
        if nrci_value >= Fraction(1,2): return CoherenceRegime.COHERENT
        if nrci_value >= Fraction(1,10): return CoherenceRegime.TRANSITIONAL
        return CoherenceRegime.SUBCOHERENT

class UBPMetricsExact:
    def __init__(self, constants: Optional[UBPConstantsExact] = None):
        self.constants = constants or UBPConstantsExact()
        self.observer = UBPObserverExact(self.constants)
        self.coherence = UBPCoherenceExact()

    def analyze_state(self, variance: Fraction, realm: str = "standard") -> Dict[str, object]:
        nrci = self.coherence.calculate_nrci(variance)
        regime = self.coherence.get_regime(nrci, self.constants.PGCI_TARGET)
        return {
            "nrci": nrci,
            "regime": regime.value,
            "observer_cost": self.observer.get_base_cost(),
            "is_stable": nrci >= Fraction(1,2),
        }

METRICS_EXACT = UBPMetricsExact()
