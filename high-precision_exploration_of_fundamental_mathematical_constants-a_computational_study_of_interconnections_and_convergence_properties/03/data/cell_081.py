# Cell 81 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title Symbolic nested-radical expression engine + Archimedes exact π bounds + mu/tau pipeline.

#!/usr/bin/env python3
"""
ubp_symbolic_pi_mu_tau.py

Symbolic nested-radical expression engine + Archimedes exact π bounds + mu/tau pipeline.

- Expressions are stored exactly as expression trees (Rational, Add, Mul, Div, Sqrt).
- No Fraction denominator explosion occurs because we do not rationalize into huge Fractions.
- Numeric evaluation uses decimal.Decimal at arbitrary precision (no floats).
- Intended as a first-principles engine: symbolic -> high-precision numeric when required.
"""

from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Union, List, Any, Dict
import json

# ---------------------------
# Expression tree classes
# ---------------------------

class Expr:
    """Base class for exact symbolic expressions."""
    def __add__(self, other: "Expr") -> "Expr":
        return Add([self, ensure_expr(other)]).simplify()
    def __radd__(self, other: "Expr") -> "Expr":
        return ensure_expr(other) + self
    def __sub__(self, other: "Expr") -> "Expr":
        return Add([self, Mul([Rational(Fraction(-1)), ensure_expr(other)])]).simplify()
    def __rsub__(self, other: "Expr") -> "Expr":
        return ensure_expr(other) - self
    def __mul__(self, other: "Expr") -> "Expr":
        return Mul([self, ensure_expr(other)]).simplify()
    def __rmul__(self, other: "Expr") -> "Expr":
        return ensure_expr(other) * self
    def __truediv__(self, other: "Expr") -> "Expr":
        return Div(self, ensure_expr(other)).simplify()
    def __rtruediv__(self, other: "Expr") -> "Expr":
        return ensure_expr(other) / self
    def sqrt(self) -> "Expr":
        return Sqrt(self)
    def to_decimal(self, prec: int) -> Decimal:
        """Evaluate expression to Decimal with precision prec."""
        raise NotImplementedError()
    def simplify(self) -> "Expr":
        return self
    def __str__(self) -> str:
        raise NotImplementedError()

@dataclass(frozen=True)
class Rational(Expr):
    val: Fraction
    def __init__(self, v: Union[int, Fraction]):
        object.__setattr__(self, "val", v if isinstance(v, Fraction) else Fraction(v))
    def to_decimal(self, prec: int) -> Decimal:
        ctx = getcontext().copy()
        ctx.prec = prec
        ctx.rounding = ROUND_HALF_EVEN
        # convert Fraction -> Decimal exactly by dividing Decimal(n)/Decimal(d)
        n = Decimal(self.val.numerator)
        d = Decimal(self.val.denominator)
        return + (n / d)  # unary + applies context precision
    def simplify(self):
        return self
    def __str__(self) -> str:
        if self.val.denominator == 1:
            return str(self.val.numerator)
        return f"({self.val.numerator}/{self.val.denominator})"

@dataclass(frozen=True)
class Add(Expr):
    terms: List[Expr]
    def __init__(self, terms: List[Expr]):
        # flatten nested Adds
        flat: List[Expr] = []
        for t in terms:
            te = ensure_expr(t)
            if isinstance(te, Add):
                flat.extend(te.terms)
            else:
                flat.append(te)
        object.__setattr__(self, "terms", flat)
    def to_decimal(self, prec: int) -> Decimal:
        ctx = getcontext().copy()
        ctx.prec = prec
        s = Decimal(0)
        for t in self.terms:
            s += t.to_decimal(prec)
        return +s
    def simplify(self) -> Expr:
        # combine trivial zero terms
        new_terms: List[Expr] = []
        rational_sum = Fraction(0)
        for t in self.terms:
            if isinstance(t, Rational):
                rational_sum += t.val
            else:
                new_terms.append(t)
        if rational_sum != 0:
            new_terms.insert(0, Rational(rational_sum))
        if len(new_terms) == 0:
            return Rational(0)
        if len(new_terms) == 1:
            return new_terms[0]
        return Add(new_terms)
    def __str__(self) -> str:
        return " + ".join(str(t) for t in self.terms)

@dataclass(frozen=True)
class Mul(Expr):
    factors: List[Expr]
    def __init__(self, factors: List[Expr]):
        flat: List[Expr] = []
        for f in factors:
            fe = ensure_expr(f)
            if isinstance(fe, Mul):
                flat.extend(fe.factors)
            else:
                flat.append(fe)
        object.__setattr__(self, "factors", flat)
    def to_decimal(self, prec: int) -> Decimal:
        ctx = getcontext().copy()
        ctx.prec = prec
        p = Decimal(1)
        for f in self.factors:
            p *= f.to_decimal(prec)
        return +p
    def simplify(self) -> Expr:
        # combine rational factors
        rational_prod = Fraction(1)
        new_factors: List[Expr] = []
        for f in self.factors:
            if isinstance(f, Rational):
                rational_prod *= f.val
            else:
                new_factors.append(f)
        if rational_prod == 0:
            return Rational(0)
        if rational_prod != 1:
            new_factors.insert(0, Rational(rational_prod))
        if len(new_factors) == 0:
            return Rational(rational_prod)
        if len(new_factors) == 1:
            return new_factors[0]
        return Mul(new_factors)
    def __str__(self) -> str:
        return " * ".join(str(f) for f in self.factors)

@dataclass(frozen=True)
class Div(Expr):
    num: Expr
    den: Expr
    def to_decimal(self, prec: int) -> Decimal:
        ctx = getcontext().copy()
        ctx.prec = prec
        n = self.num.to_decimal(prec)
        d = self.den.to_decimal(prec)
        return + (n / d)
    def simplify(self) -> Expr:
        n = self.num.simplify()
        d = self.den.simplify()
        # division by 1
        if isinstance(d, Rational) and d.val == 1:
            return n
        # if both rational, return rational
        if isinstance(n, Rational) and isinstance(d, Rational):
            return Rational(n.val / d.val)
        return Div(n, d)
    def __str__(self) -> str:
        return f"({self.num}) / ({self.den})"

@dataclass(frozen=True)
class Sqrt(Expr):
    child: Expr
    def to_decimal(self, prec: int) -> Decimal:
        # Use Decimal sqrt via Newton method on Decimal evaluation of child
        ctx = getcontext().copy()
        ctx.prec = prec + 10  # extra guard digits for iteration
        getcontext().prec = ctx.prec
        val = self.child.to_decimal(ctx.prec)
        if val < 0:
            raise ValueError("sqrt of negative")
        if val == 0:
            return Decimal(0)
        # Newton iteration for sqrt with Decimal (no python float used)
        x = val if val >= 1 else Decimal(1)
        two = Decimal(2)
        for _ in range(ctx.prec + 5):
            x_next = (x + val / x) / two
            if abs(x_next - x) <= Decimal(10) ** (-(ctx.prec - 2)):
                x = x_next
                break
            x = x_next
        # Round to requested precision
        getcontext().prec = prec
        return +x
    def simplify(self) -> Expr:
        # if child is Rational perfect square, return Rational
        c = self.child.simplify()
        if isinstance(c, Rational):
            num = c.val.numerator
            den = c.val.denominator
            # check perfect square
            import math
            if int(math.isqrt(num))**2 == num and int(math.isqrt(den))**2 == den:
                return Rational(Fraction(int(math.isqrt(num)), int(math.isqrt(den))))
        return Sqrt(c)
    def __str__(self) -> str:
        return f"√({self.child})"

def ensure_expr(x: Union[int, Fraction, Expr]) -> Expr:
    if isinstance(x, Expr):
        return x
    if isinstance(x, Fraction):
        return Rational(x)
    if isinstance(x, int):
        return Rational(Fraction(x))
    raise TypeError(f"Cannot convert {type(x)} to Expr")

# ---------------------------
# Archimedes half-angle functions (symbolic)
# ---------------------------

def initial_sin_cos_expr():
    # sin(pi/4) = sqrt(2)/2 ; cos(pi/4) = sqrt(2)/2
    two = Rational(Fraction(2))
    sqrt2 = Sqrt(Rational(Fraction(2)))
    sin4 = Div(sqrt2, Rational(Fraction(2))).simplify()
    cos4 = sin4
    return sin4, cos4

def half_angle_symbolic(sin_x: Expr, cos_x: Expr):
    # cos_half = sqrt((1 + cos_x)/2)
    # sin_half = sqrt((1 - cos_x)/2)   (or sin_half = sqrt((1 - cos)/2))
    one = Rational(Fraction(1))
    two = Rational(Fraction(2))
    cos_half = Sqrt(Div(Add([one, cos_x]).simplify(), two).simplify()).simplify()
    sin_half = Sqrt(Div(Add([one, Mul([Rational(Fraction(-1)), cos_x])]).simplify(), two).simplify()).simplify()
    return sin_half, cos_half

def archimedes_bounds_symbolic(ticks: int = 6):
    sin_x, cos_x = initial_sin_cos_expr()
    n = 4
    for _ in range(ticks):
        sin_x, cos_x = half_angle_symbolic(sin_x, cos_x)
        n *= 2
    lower = Mul([Rational(Fraction(n)), sin_x]).simplify()
    upper = Mul([Rational(Fraction(n)), Div(sin_x, cos_x)]).simplify()
    return {
        "ticks": ticks,
        "sides": n,
        "lower_expr": lower,
        "upper_expr": upper
    }

# ---------------------------
# Utilities: evaluate expressions and compute mass ratios
# ---------------------------

def eval_expr_decimal(expr: Expr, prec: int) -> Decimal:
    """Evaluate a symbolic expr to Decimal using specified precision (no floats)."""
    # set context
    getcontext().prec = prec
    getcontext().rounding = ROUND_HALF_EVEN
    return expr.to_decimal(prec)

def compute_Y_mu_tau_from_pi(pi_decimal: Decimal, prec: int) -> Dict[str, Decimal]:
    """Compute Y, 1/Y, mu/e, tau/e using Decimal math at prec digits."""
    getcontext().prec = prec
    getcontext().rounding = ROUND_HALF_EVEN
    two = Decimal(2)
    one = Decimal(1)
    pi = +pi_decimal
    Y = pi / (pi * pi + two)
    invY = + (one / Y)
    mu_e = +(invY ** 4)
    tau_e = +(invY ** 6)
    return {"Y": Y, "1/Y": invY, "mu/e": mu_e, "tau/e": tau_e}

# ---------------------------
# Driver: produce symbolic bounds, midpoint π, evaluate series
# ---------------------------

def run_symbolic_series(max_tick: int = 12, eval_prec_base: int = 80) -> Dict[str, Any]:
    results = []
    for t in range(max_tick + 1):
        info = archimedes_bounds_symbolic(t)
        n = info["sides"]
        lower_expr = info["lower_expr"]
        upper_expr = info["upper_expr"]

        # choose precision heuristic: base + 6*doublings
        prec = max(eval_prec_base, 60 + (t * 6))

        lower_dec = eval_expr_decimal(lower_expr, prec)
        upper_dec = eval_expr_decimal(upper_expr, prec)

        # midpoint pi estimate (center of bounds)
        pi_mid = +( (lower_dec + upper_dec) / Decimal(2) )

        ratios = compute_Y_mu_tau_from_pi(pi_mid, prec)

        # experimental references
        exp_mu_e = Decimal('206.768283')
        exp_tau_e = Decimal('3477.23')

        err_mu = (abs(ratios["mu/e"] - exp_mu_e) / exp_mu_e) * Decimal(100)
        err_tau = (abs(ratios["tau/e"] - exp_tau_e) / exp_tau_e) * Decimal(100)

        entry = {
            "tick": t,
            "sides": n,
            "precision_used": prec,
            "pi_lower_symbolic": str(lower_expr),
            "pi_upper_symbolic": str(upper_expr),
            "pi_lower_decimal": format(lower_dec, 'f'),
            "pi_upper_decimal": format(upper_dec, 'f'),
            "pi_mid_decimal": format(pi_mid, 'f'),
            "Y": format(ratios["Y"], 'f'),
            "1/Y": format(ratios["1/Y"], 'f'),
            "mu_over_e": format(ratios["mu/e"], 'f'),
            "tau_over_e": format(ratios["tau/e"], 'f'),
            "err_mu_%": format(err_mu, 'f'),
            "err_tau_%": format(err_tau, 'f')
        }
        results.append(entry)

        # print compact summary
        print(f"Tick {t}: sides={n} prec={prec} pi≈{pi_mid:.12f} μ/e={ratios['mu/e']:.6f} err_μ%={err_mu:.6f}")

    return {"results": results}

# ---------------------------
# Save & run
# ---------------------------

if __name__ == "__main__":
    # Quick run (defaults moderate)
    series = run_symbolic_series(max_tick=42, eval_prec_base=80)

    with open("pi_symbolic_series.json", "w") as f:
        json.dump(series, f, indent=2)

    print("\nSaved series -> pi_symbolic_series.json")
    print("Sample symbolic lower/upper for a final tick (human readable):")
    sample = series["results"][-1]
    print("  tick", sample["tick"], "sides", sample["sides"])
    print("  lower (symbolic):", sample["pi_lower_symbolic"])
    print("  upper (symbolic):", sample["pi_upper_symbolic"])
    print("  mid π decimal:", sample["pi_mid_decimal"])
    print("  μ/e:", sample["mu_over_e"])
    print("  τ/e:", sample["tau_over_e"])
    print("  errors (%): μ/e", sample["err_mu_%"], " τ/e", sample["err_tau_%"])