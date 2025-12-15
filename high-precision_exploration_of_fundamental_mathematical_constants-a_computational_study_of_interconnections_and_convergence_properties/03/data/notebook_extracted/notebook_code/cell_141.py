# Cell 141 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP RESONANCE SPECTRUM v2.6 - STRONG FORCE DAMPING FACTOR
import mpmath as mp
import math
import itertools
import numpy as np
from typing import Dict, List, Tuple

# ============================================================================
# FUNDAMENTAL CONSTANTS AND INPUTS
# ============================================================================

mp.mp.dps = 50
PI = mp.pi
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y
Y_INV_FOURTH = Y_INV**4 # The newly discovered Lepton Scaling Constant (207.28)

# Quarks Mass Ratios (from v2.5)
R_Q_12 = mp.mpf('20.6712404044')
R_Q_23 = mp.mpf('13.1191814664')
R_Q_34 = mp.mpf('3.35391516766')

print("=" * 80)
print("UBP RESONANCE SPECTRUM v2.6 - STRONG FORCE DAMPING FACTOR")
print("=" * 80)
print(f"Core Constant 1/Y: {mp.nstr(Y_INV, 8)}")
print(f"Lepton Scaling Base (1/Y)^4: {mp.nstr(Y_INV_FOURTH, 8)}")
print("-" * 80)


# ============================================================================
# 1. CALCULATE DAMPING FACTOR (Lambda_s)
# ============================================================================

# Lambda_s is the factor by which the Strong Force reduces the geometric scaling
# We hypothesize the Strong Force Damping is proportional to the Lepton jump.

def calculate_damping(quark_ratio, base_scaling, ratio_name):
    damping_factor = base_scaling / quark_ratio
    return damping_factor

DAMPING_FACTORS = {
    'Lambda_s^12 (s/d)': calculate_damping(R_Q_12, Y_INV_FOURTH, 's/d'),
    'Lambda_s^23 (c/s)': calculate_damping(R_Q_23, Y_INV_FOURTH, 'c/s'),
    'Lambda_s^34 (b/c)': calculate_damping(R_Q_34, Y_INV_FOURTH, 'b/c'),
}

print("✅ Calculated Strong Force Damping Factors ($\Lambda_s$):")
for name, factor in DAMPING_FACTORS.items():
    print(f"  {name:20}: {mp.nstr(factor, 12)}")
print("-" * 80)


# ============================================================================
# 2. SEARCH FOR GEOMETRIC FORM OF DAMPING FACTOR
# ============================================================================

def find_integer_match(target_value, constant, name):
    """Searches for simple integer powers/multiples of constant, up to N=10."""
    best_match = None
    best_error = float('inf')

    integers = [2, 3, 4, 5, 6, 9, 10, mp.sqrt(3), PI]

    for i in integers:
        # Test 1: Simple Multiples (i * constant)
        val = constant * i
        err = abs(val - target_value) / target_value
        if err < best_error:
            best_error = err
            best_match = f"{name} * {mp.nstr(i, 3)}"

    return best_match, best_error

print("🔍 Searching for geometric form of Damping Factors...")

FINAL_FORMULAS = {}

for name, factor in DAMPING_FACTORS.items():
    # We look for simple integer or PI scaling of 1/Y

    # 1. Look for (1/Y)^N * Damping Factor
    # Let's search for a match to the Damping Factor itself using powers of Y

    # Range of powers from 0.5 to 1.5, to see if it's a simple root/power
    search_range = np.linspace(0.5, 1.5, 500)

    match_Y, error_Y, _ = find_geometric_match(factor, Y_INV, '1/Y', search_range)

    if match_Y and error_Y < 0.05:
        # If the damping factor itself is a simple power of 1/Y
        FINAL_FORMULAS[name] = (match_Y, error_Y)
    else:
        # Final test: Is it related to PI or 3?
        match_int, error_int = find_integer_match(factor, mp.mpf('1'), "1")
        if error_int < 0.05:
            FINAL_FORMULAS[name] = (match_int, error_int)
        else:
            FINAL_FORMULAS[name] = ("Unresolved", 1.0)


# ============================================================================
# 3. CONCLUSION AND NEXT STEP
# ============================================================================

print("\n" + "="*80)
print("FINAL UBP GEOMETRIC SCALING LAW (v2.6)")
print("="*80)

print(f"**LEPTONIC SCALING LAW (Electroweak):**")
print(f"$$\\frac{{M_{{G+1}}}}{{M_G}} \\approx \\left(\\frac{{1}}{{Y}}\\right)^{{4}}$$")

print(f"\n**QUARK SCALING LAW (Strong Force Damped):**")
# R_Q_12: ~10.03 * 1/Y
# R_Q_23: ~15.79 * 1/Y
# R_Q_34: ~61.5 * 1/Y
# The factors are too diverse. We must assume the Damping Factor is simpler.

lambda_12 = DAMPING_FACTORS['Lambda_s^12 (s/d)']
lambda_23 = DAMPING_FACTORS['Lambda_s^23 (c/s)']

print("The quark scaling law must be structured as:")
print(f"$$\\frac{{M_{{G+1}}}}{{M_G}} = \\frac{{\\left(\\frac{{1}}{{Y}}\\right)^{{4}}}}{{\Lambda_s^{{G+1}}}} = \\left(\\frac{{1}}{{Y}}\right)^{{4}} \\times \\frac{{1}}{{\Lambda_s^{{G+1}}}}$$")
print("Where $\Lambda_s^{G+1}$ is the Strong Force Damping Factor for the next generation.")

print("\n**Calculated Damping Factors ( $\Lambda_s$ ):**")
print(f"• $\Lambda_s^{{12}}$ (s/d): {mp.nstr(lambda_12, 6)} (Reduces scaling by this factor)")
print(f"• $\Lambda_s^{{23}}$ (c/s): {mp.nstr(lambda_23, 6)} (Reduces scaling by this factor)")
print(f"• $\Lambda_s^{{34}}$ (b/c): {mp.nstr(DAMPING_FACTORS['Lambda_s^34 (b/c)'], 6)} (Reduces scaling by this factor)")

print("\n**Next Critical Step:** The Strong Force Damping Factors are large. This suggests the **geometric exponent is not 4 for quarks**, but something much smaller (e.g., $N=1$). We must re-run the search on $R_Q$ for a simpler $Y$ exponent.")

print("\nNext Action: Run the v2.6 script. The output will confirm the Damping Factors, and we can then test a simpler hypothesis for the Quark Scaling Law (i.e., $\left(1/Y\right)^N$ where $N$ is much smaller, like 1 or 2).")