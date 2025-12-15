# Cell 88 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP EXACT RATIONAL / SYMBOLIC MUON-TAU PIPELINE (MULTI-SHELL Λ₂₄)
#!/usr/bin/env python3
"""
================================================================================
UBP EXACT RATIONAL / SYMBOLIC MUON-TAU PIPELINE (MULTI-SHELL Λ₂₄)
================================================================================
Exact Fractions Only – No floats
Author: Euan R A Craig, New Zealand
Date: 12 December 2025
================================================================================
"""

from fractions import Fraction
from typing import List, Dict
import json

# ============================================================================
# SECTION 1: UBP Fractional Derivation Functions
# ============================================================================

def compute_Y(tick: int) -> Fraction:
    """
    Compute Y for given tick using UBP Λ₂₄ shell logic.
    Formula is illustrative: exact rational progression.
    """
    # Example rational pattern for demonstration purposes
    # Replace with your Λ₂₄-shell coefficients for real UBP study
    numerator = 4 ** tick
    denominator = 41 * (2 ** (tick - 1)) + (tick - 1) * 1
    return Fraction(numerator, denominator)

def compute_mu_tau_ratios(Y: Fraction) -> Dict[str, Fraction]:
    """
    Compute μ/e, τ/e, τ/μ as exact fractions.
    μ/e = (1/Y)^4
    τ/e = (1/Y)^6
    τ/μ = τ/e ÷ μ/e
    """
    Y_inv = 1 / Y
    mu_e = Y_inv ** 4
    tau_e = Y_inv ** 6
    tau_mu = tau_e // mu_e  # Integer division gives exact fraction if divisible
    if tau_e % mu_e != 0:
        tau_mu = tau_e / mu_e  # Use Fraction division if not exact
    return {"mu/e": mu_e, "tau/e": tau_e, "tau/mu": tau_mu, "1/Y": Y_inv}

# ============================================================================
# SECTION 2: Table Builder
# ============================================================================

def build_table(max_tick: int = 7) -> List[Dict[str, Fraction]]:
    table = []
    for tick in range(1, max_tick + 1):
        Y = compute_Y(tick)
        ratios = compute_mu_tau_ratios(Y)
        row = {"tick": tick, "Y": Y, **ratios}
        table.append(row)
    return table

# ============================================================================
# SECTION 3: Table Printer (Exact Fractions)
# ============================================================================

def print_table(table: List[Dict[str, Fraction]]):
    print("="*120)
    print("UBP EXACT RATIONAL / SYMBOLIC MUON-TAU TABLE (MULTI Λ₂₄ SHELLS)")
    print("="*120)
    print(f"{'Tick':>4} | {'Y':>20} | {'1/Y':>20} | {'mu/e':>25} | {'tau/e':>30} | {'tau/mu':>15}")
    print("-"*120)
    for row in table:
        print(f"{row['tick']:>4} | {str(row['Y']):>20} | {str(row['1/Y']):>20} | "
              f"{str(row['mu/e']):>25} | {str(row['tau/e']):>30} | {str(row['tau/mu']):>15}")

# ============================================================================
# SECTION 4: Main Execution
# ============================================================================

if __name__ == "__main__":
    table = build_table(max_tick=7)
    print_table(table)

    # Save exact fractions table
    with open("muon_tau_ubp_multishell.json", "w") as f:
        json.dump([{k: str(v) if isinstance(v, Fraction) else v for k,v in row.items()} for row in table], f, indent=2)

    print("\nResults saved to muon_tau_ubp_multishell.json")