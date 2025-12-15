# Cell 89 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP SYMBOLIC / EXACT RATIONAL MUON-TAU TUNING PIPELINE
#!/usr/bin/env python3
"""
================================================================================
UBP SYMBOLIC / EXACT RATIONAL MUON-TAU TUNING PIPELINE
================================================================================
Purpose:
- Solve symbolically for Y to match a target muon/electron ratio
- Produce exact nested radical / rational powers for tau/e and tau/mu
- No floats, no numpy, all ExactNumber / Fraction arithmetic
- Outputs table ready for UBP geometric or lattice mapping
================================================================================
"""

from fractions import Fraction
from typing import Dict, Any
from sympy import symbols, Rational, simplify, Pow, sqrt, pprint

# ============================================================================
# SECTION 1: Define symbolic variables
# ============================================================================

Z = symbols("Z", positive=True)  # Z = 1/Y

# ============================================================================
# SECTION 2: Function to compute exact nested radical given target mu/e
# ============================================================================

def compute_symbolic_mu_tau(mu_target: Fraction) -> Dict[str, Any]:
    """
    Compute symbolic Y, 1/Y, mu/e, tau/e, tau/mu for a given target mu/e
    mu_target: Fraction
    Returns dictionary with exact rational/power forms
    """
    # Z^4 = mu_target => Z = (mu_target)^(1/4)
    Z_value = Pow(mu_target, Rational(1, 4))
    Y_value = 1 / Z_value

    # Tau/e = Z^6 = (Z^4)*(Z^2) = mu_target * Z^2
    tau_over_e = mu_target * Pow(Z_value, 2)

    # Tau/mu = Z^2
    tau_over_mu = Pow(Z_value, 2)

    return {
        "Y": simplify(Y_value),
        "1/Y": simplify(Z_value),
        "mu/e": simplify(mu_target),
        "tau/e": simplify(tau_over_e),
        "tau/mu": simplify(tau_over_mu),
    }

# ============================================================================
# SECTION 3: Build table of multiple ticks (optional)
# ============================================================================

def build_mu_tau_table(targets: Dict[int, Fraction]):
    """
    targets: dict mapping tick -> mu/e target
    returns list of dictionaries
    """
    table = []
    for tick, mu in targets.items():
        table.append({"tick": tick, **compute_symbolic_mu_tau(mu)})
    return table

# ============================================================================
# SECTION 4: Pretty print table
# ============================================================================

def print_table(table):
    headers = ["Tick", "Y", "1/Y", "μ/e", "τ/e", "τ/μ"]
    print("="*120)
    print(f"{' | '.join(headers)}")
    print("-"*120)
    for row in table:
        print(f"{row['tick']:>4} | {row['Y']} | {row['1/Y']} | {row['mu/e']} | {row['tau/e']} | {row['tau/mu']}")
    print("="*120)

# ============================================================================
# SECTION 5: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example: tune to real muon/electron ratio (exact fraction approximation)
    # You can change these fractions to experiment with UBP tuning
    mu_targets = {
        1: Fraction(206768283, 1000000),  # Approx 206.768283
        2: Fraction(206768283, 1000000),
        3: Fraction(206768283, 1000000),
    }

    mu_tau_table = build_mu_tau_table(mu_targets)

    print("\nUBP EXACT / SYMBOLIC MUON-TAU TUNING TABLE")
    print_table(mu_tau_table)

    # Optionally: print nested radicals nicely
    print("\nSYMBOLIC NESTED RADICAL FOR TICK 1:")
    tick1 = mu_tau_table[0]
    print("Y = ")
    pprint(tick1["Y"])
    print("1/Y = ")
    pprint(tick1["1/Y"])
    print("τ/mu = ")
    pprint(tick1["tau/mu"])