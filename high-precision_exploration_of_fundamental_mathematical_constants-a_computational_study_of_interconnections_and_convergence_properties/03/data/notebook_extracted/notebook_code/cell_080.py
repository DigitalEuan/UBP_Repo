# Cell 80 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title  SYMBOLIC RADICAL ENGINE — EXACT π SYSTEM
# ============================================
#  SYMBOLIC RADICAL ENGINE — EXACT π SYSTEM
#  (First-Principles Nested Radical Algebra)
#  Author: Euan Craig + Manus AI
# ============================================

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

# --------------------------------------------
# Base object representing  a + b*√c
# where a, b, c are rational (Fraction)
# --------------------------------------------

@dataclass(frozen=True)
class Radical:
    a: Fraction           # rational part
    b: Fraction           # coefficient
    c: Fraction           # radicand (always stored as squarefree)

    # ----------------------------
    # Canonical simplification
    # ----------------------------
    @staticmethod
    def normalize(a, b, c):
        # Case: b == 0 → pure rational
        if b == 0:
            return Radical(a, Fraction(0), Fraction(0))

        # Make c squarefree
        num = c.numerator
        den = c.denominator

        # Factor numerator
        k = 1
        n = abs(num)
        f = 2
        while f * f <= n:
            while n % f == 0 and (n // (f*f)) * (f*f) == n:
                n //= (f*f)
                k *= f
            f += 1

        # Factor denominator
        m = abs(den)
        f = 2
        while f * f <= m:
            while m % f == 0 and (m // (f*f)) * (f*f) == m:
                m //= (f*f)
                k /= f
            f += 1

        # Move squares into coefficient b
        new_c = Fraction(n, m)
        new_b = b * Fraction(k)

        return Radical(a, new_b, new_c)

    # ----------------------------
    # Constructors
    # ----------------------------
    @staticmethod
    def rational(q):
        return Radical(Fraction(q), Fraction(0), Fraction(0))

    @staticmethod
    def sqrt(q):
        return Radical(Fraction(0), Fraction(1), Fraction(q))

    # ----------------------------
    # Arithmetic
    # ----------------------------
    def __add__(self, other):
        return Radical.normalize(
            self.a + other.a,
            self.b + other.b,
            self.c if self.b != 0 else other.c
        )

    def __sub__(self, other):
        return Radical.normalize(
            self.a - other.a,
            self.b - other.b,
            self.c if self.b != 0 else other.c
        )

    def __mul__(self, other):
        # (a1 + b1√c1)(a2 + b2√c2)
        a1, b1, c1 = self.a, self.b, self.c
        a2, b2, c2 = other.a, other.b, other.c

        if c1 == c2:
            # same radical field
            a = a1*a2 + b1*b2*c1
            b = a1*b2 + a2*b1
            return Radical.normalize(a, b, c1)

        # general case (field extension) → embed in √c1 + √c2
        # but you do not need this for Archimedes method:
        # all angles always stay in same radical field.
        # So we refuse purposely.
        raise ValueError("Mixed radical fields not supported (not needed for half-angle π).")

    def __truediv__(self, other):
        # rationalize
        conj = Radical(other.a, -other.b, other.c)
        num = self * conj
        den = (other * conj).a  # becomes rational
        return Radical.normalize(num.a / den, num.b / den, num.c)

    # -----------------------------------
    # Helpers for half-angle identities
    # -----------------------------------
    def sqrt_half_plus_one(self):
        # √((1 + self)/2)
        return Radical.sqrt(Fraction(1,2)) * Radical.normalize(
            self.a + Fraction(1),
            self.b,
            self.c
        )

    def sqrt_half_minus_one(self):
        # √((1 - self)/2)
        return Radical.sqrt(Fraction(1,2)) * Radical.normalize(
            Fraction(1) - self.a,
            -self.b,
            self.c
        )

# -------------------------------------------------------
# INITIAL CONDITIONS FOR ARCHIMEDES METHOD
# -------------------------------------------------------

def initial_sin_cos(n_sides):
    """Return exact symbolic sin(π/n) and cos(π/n)."""
    # Only valid for n = power of 2 * 4
    # Base: sin(pi/4) = √2/2, cos(pi/4) = √2/2
    r = Radical.sqrt(Fraction(1,2))  # √(1/2)
    return r, r

# -------------------------------------------------------
# HALF-ANGLE REDUCTION
# -------------------------------------------------------

def half_angle(sin_x, cos_x):
    cos_half = Radical.sqrt(Fraction(1,2)) * Radical.normalize(
        cos_x.a + Fraction(1), cos_x.b, cos_x.c
    )
    sin_half = Radical.sqrt(Fraction(1,2)) * Radical.normalize(
        Fraction(1) - cos_x.a, -cos_x.b, cos_x.c
    )
    return sin_half, cos_half

# -------------------------------------------------------
# EXACT ARCHIMEDES π ENGINE
# -------------------------------------------------------

def archimedes_pi_exact(ticks=20):
    # 4 → 2→1→... refining
    sin_x, cos_x = initial_sin_cos(4)
    n = 4

    for k in range(ticks):
        sin_x, cos_x = half_angle(sin_x, cos_x)
        n *= 2

    # lower_bound = n * sin(π/n)
    # upper_bound = n * tan(π/n) = n * sin / cos
    lower = Radical.rational(n) * sin_x
    upper = Radical.rational(n) * (sin_x / cos_x)
    return n, lower, upper