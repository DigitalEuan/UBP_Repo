# Cell 79 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title High-precision Decimal Archimedes π engine + muon/tau derivation
#!/usr/bin/env python3
"""
High-precision Decimal Archimedes π engine + muon/tau derivation
- No floats used in the numerical core (Decimal everywhere).
- First-principles Newton sqrt with precision-aware stopping.
- Archimedes half-angle method (sin-halving) using Decimal arithmetic.
- Euan Craig, New Zealand - this version by ChatGPT
- 12 December 2025
"""

from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction
import json
import math
from typing import Dict, Any


def decimal_sqrt(x: Decimal, prec: int) -> Decimal:
    """Compute sqrt(x) using Newton iteration with Decimal, precision-aware.
    Returns Decimal with context.prec = prec (caller must set context).
    """
    if x < 0:
        raise ValueError("sqrt of negative")
    if x == 0:
        return Decimal(0)
    ctx = getcontext()
    # A good initial guess: use Decimal.log10 via float estimate only for initial guess size,
    # but avoid using float in the Newton iterations themselves.
    # Start with x / 2 as a safe initial guess (works well with high precision)
    guess = x if x < 1 else (x / 2)
    # Iterate until improvement smaller than 1 ulp for requested precision
    one = Decimal(1)
    two = Decimal(2)
    target_ulp = Decimal(10) ** (-(prec - 2))  # somewhat conservative
    for _ in range(prec + 5):
        new_guess = (guess + x / guess) / two
        if abs(new_guess - guess) <= target_ulp:
            return +new_guess  # unary plus applies context precision/rounding
        guess = new_guess
    return +guess


def required_precision_for_sides(sides: int) -> int:
    """Heuristic precision selection: scale with log2(sides).
    Archimedes error scales ~ O(1/n^2) for polygon perimeter; we want enough digits
    so that computing Y and powers does not lose significance.
    """
    if sides <= 8:
        return 60
    doublings = int(math.log2(sides // 4))
    # base 60 + 6 digits per doubling as a practical heuristic; clamp to reasonable bounds
    prec = 60 + max(0, doublings) * 6
    return min(max(prec, 60), 1000)


def archimedes_pi_decimal(sides: int, prec: int = None) -> Decimal:
    """Compute π approximation for a regular polygon with `sides` sides using the
    half-angle (doubling) Archimedes method. Returns Decimal with given precision.
    """
    if sides < 4 or (sides % 4) != 0:
        raise ValueError("sides must be 4 * 2^k (i.e., 4, 8, 16, ...)")
    if prec is None:
        prec = required_precision_for_sides(sides)

    # Set context precision and rounding
    ctx = getcontext().copy()
    ctx.prec = prec
    ctx.rounding = ROUND_HALF_EVEN
    getcontext().prec = prec
    getcontext().rounding = ROUND_HALF_EVEN

    # constants in Decimal
    D1 = Decimal(1)
    D2 = Decimal(2)

    # Start at n = 4: sin(pi/4) = sqrt(2)/2
    root2 = decimal_sqrt(Decimal(2), prec)
    sin_half = root2 / D2

    # Determine doublings: sides = 4 * 2^doublings
    doublings = int(math.log2(sides // 4))

    for i in range(doublings):
        # cos = sqrt(1 - sin^2)
        sin_sq = sin_half * sin_half
        inner_cos = D1 - sin_sq
        if inner_cos < 0:
            # numerical safeguard: clamp to zero if tiny negative rounding occurred
            inner_cos = Decimal(0)
        cos_half = decimal_sqrt(inner_cos, prec)

        # denominator = sqrt(2*(1 + cos))
        inner = D1 + cos_half
        denom = decimal_sqrt(D2 * inner, prec)

        # new sin = sin / denom
        sin_half = sin_half / denom

    # final n = sides
    n_final = Decimal(sides)
    pi_approx = n_final * sin_half
    # normalize to context precision
    return +pi_approx


def compute_mu_tau_from_pi(pi: Decimal, prec: int):
    """Compute Y, 1/Y, mu/e = (1/Y)^4, tau/e = (1/Y)^6, tau/mu."""
    getcontext().prec = prec
    D2 = Decimal(2)
    one = Decimal(1)

    pi_sq = pi * pi
    Y = pi / (pi_sq + D2)
    Y_inv = one / Y

    mu_e = Y_inv ** 4
    tau_e = Y_inv ** 6
    tau_mu = tau_e / mu_e

    return {
        "Y": +Y,
        "1_over_Y": +Y_inv,
        "mu_over_e": +mu_e,
        "tau_over_e": +tau_e,
        "tau_over_mu": +tau_mu
    }


def run_archimedes_series(max_tick: int = 6) -> Dict[str, Any]:
    """Run a small series of ticks (0..max_tick) and return results. Default max_tick moderate.
    ticks: sides = 2**(tick + 2)
    """
    results = []
    for t in range(max_tick + 1):
        sides = 2 ** (t + 2)
        prec = required_precision_for_sides(sides)
        pi_approx = archimedes_pi_decimal(sides, prec=prec)
        vals = compute_mu_tau_from_pi(pi_approx, prec=prec)
        # experimental references (Decimal strings)
        exp_mu_e = Decimal('206.768283')
        exp_tau_e = Decimal('3477.23')

        mu_e = vals["mu_over_e"]
        tau_e = vals["tau_over_e"]

        # compute percentage errors (relative)
        err_mu = (abs(mu_e - exp_mu_e) / exp_mu_e) * Decimal(100)
        err_tau = (abs(tau_e - exp_tau_e) / exp_tau_e) * Decimal(100)

        entry = {
            "tick": t,
            "sides": sides,
            "precision_digits": getcontext().prec,
            "pi": format(pi_approx, 'f'),
            "Y": format(vals["Y"], 'f'),
            "1/Y": format(vals["1_over_Y"], 'f'),
            "mu_over_e": format(mu_e, 'f'),
            "tau_over_e": format(tau_e, 'f'),
            "tau_over_mu": format(vals["tau_over_mu"], 'f'),
            "error_mu_e_percent": format(err_mu, 'f'),
            "error_tau_e_percent": format(err_tau, 'f')
        }
        results.append(entry)
        # Print compact progress line
        print(f"Tick {t}: sides={sides} prec={getcontext().prec} digits π≈{pi_approx:.12f} μ/e={mu_e:.6f} err_μ%={err_mu:.6f}")
    return {"results": results}


def final_run(tick_for_final: int = 20) -> Dict[str, Any]:
    """Compute final high-precision result at a large tick (default tick 20 -> 4,194,304 sides).
    NOTE: precision chosen heuristically; large ticks may be expensive depending on environment.
    """
    sides = 2 ** (tick_for_final + 2)
    prec = required_precision_for_sides(sides)
    # for very large sides, increase precision proportionally to doublings
    doublings = int(math.log2(sides // 4))
    prec += doublings * 4  # extra margin for powers and subtraction
    # clamp to reasonable maximum (avoid extremely huge memory use)
    prec = min(prec, 2000)

    print(f"Final run: tick={tick_for_final}, sides={sides}, precision={prec} digits")
    pi_final = archimedes_pi_decimal(sides, prec=prec)
    vals = compute_mu_tau_from_pi(pi_final, prec=prec)

    exp_mu_e = Decimal('206.768283')
    exp_tau_e = Decimal('3477.23')

    mu_e = vals["mu_over_e"]
    tau_e = vals["tau_over_e"]

    err_mu = (abs(mu_e - exp_mu_e) / exp_mu_e) * Decimal(100)
    err_tau = (abs(tau_e - exp_tau_e) / exp_tau_e) * Decimal(100)

    final = {
        "tick": tick_for_final,
        "sides": sides,
        "precision_digits": prec,
        "pi": format(pi_final, 'f'),
        "Y": format(vals["Y"], 'f'),
        "1/Y": format(vals["1_over_Y"], 'f'),
        "mu_over_e": format(mu_e, 'f'),
        "tau_over_e": format(tau_e, 'f'),
        "tau_over_mu": format(vals["tau_over_mu"], 'f'),
        "error_mu_e_percent": format(err_mu, 'f'),
        "error_tau_e_percent": format(err_tau, 'f')
    }
    return final


if __name__ == "__main__":
    # Example quick run: ticks 0..4 (4..64 sides)
    series = run_archimedes_series(max_tick=64)
    with open('pi_ubp_decimal_series.json', 'w') as f:
        json.dump(series, f, indent=2)

    # Perform a final (larger) run but not too huge by default.
    # You may change tick_for_final to 10, 12, or 20 depending on the time you accept.
    final = final_run(tick_for_final=40)
    with open('muon_tau_decimal_final.json', 'w') as f:
        json.dump(final, f, indent=2)

    print("\nFinal results summary:")
    for k, v in final.items():
        print(f"  {k}: {v}")
    print("\nSaved series -> pi_ubp_decimal_series.json")
    print("Saved final  -> muon_tau_decimal_final.json")