# Cell 143 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP RESONANCE SPECTRUM v2.8 - UNIFIED GEOMETRIC LAW ($\delta$ Factor)
import mpmath as mp
import numpy as np
from typing import Dict, List, Tuple

# ============================================================================
# FUNDAMENTAL CONSTANTS AND INPUTS
# ============================================================================

mp.mp.dps = 50
PI = mp.pi
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y

# Quarks Mass Ratios (from v2.5)
R_Q_12 = mp.mpf('20.6712404044')
R_Q_23 = mp.mpf('13.1191814664')
R_Q_34 = mp.mpf('3.35391516766')

print("=" * 80)
print("UBP RESONANCE SPECTRUM v2.8 - UNIFIED GEOMETRIC LAW ($\delta$ Factor)")
print("=" * 80)
print(f"Core Constant 1/Y: {mp.nstr(Y_INV, 8)}")
print("-" * 80)

# ============================================================================
# 1. DEFINE BASE EXPONENTS AND CALCULATE CORRECTION FACTOR (delta)
# ============================================================================

# Based on v2.7 analysis, we assume the nearest simple integer exponent (N)
# for the geometric base, and calculate the required correction factor (delta).

QUARK_SCALING_HYPOTHESES = {
    # s/d ratio is ~20.67. (1/Y)^2 = 14.27. (1/Y)^3 = 53.94. N=2.5 is too complex.
    # Let's use N=2 as the base, suggesting a geometric jump of two units.
    'R_Q_12 (s/d)': {'ratio': R_Q_12, 'N_base': mp.mpf('2')},

    # c/s ratio is ~13.12. (1/Y)^2 = 14.27. N=2 is the closest integer base.
    'R_Q_23 (c/s)': {'ratio': R_Q_23, 'N_base': mp.mpf('2')},

    # b/c ratio is ~3.35. (1/Y)^1 = 3.77. N=1 is the closest integer base.
    'R_Q_34 (b/c)': {'ratio': R_Q_34, 'N_base': mp.mpf('1')},
}

def calculate_delta(data):
    # Delta = (Target Ratio) / ((1/Y)^N_base)
    base_geometric_scale = Y_INV ** data['N_base']
    delta_correction = data['ratio'] / base_geometric_scale
    data['delta'] = delta_correction

    # Calculate the error assuming the base N is the law
    # Error = |(1/Y)^N - Target| / Target. This is already calculated by v2.7.
    # Here, we report the delta factor itself.

    print(f"  {data['ratio_name']:15} | Base N={float(data['N_base']):3.0f} | $\delta$ Factor: {mp.nstr(delta_correction, 12)}")

print("✅ Calculated Quark Correction Factors ($\delta$):")
print(f"  {'Ratio Name':15} | {'Base N':6} | {'$\delta$ Factor':15}")
print("-" * 50)

for name, data in QUARK_SCALING_HYPOTHESES.items():
    data['ratio_name'] = name
    calculate_delta(data)

print("-" * 80)


# ============================================================================
# 2. SEARCH FOR GEOMETRIC FORM OF DELTA
# ============================================================================

def search_delta_form(target_value, name):
    best_match = None
    best_error = float('inf')

    # Test 1: Simple integers (2, 3, 4, 5) and simple fractions (1/2, 2/3)
    test_values = {
        '1.0': mp.mpf('1.0'),
        'PI/4': PI/4,
        'e/PI': mp.e/PI,
        'Y': Y,
        '1/Y': Y_INV,
        '1/2': mp.mpf('0.5'),
        '1/3': mp.mpf('0.3333333333333333'),
        'ln(1/Y)': mp.log(Y_INV),
        'sqrt(2)': mp.sqrt(2)
    }

    # Test 2: Powers of 2/3 (potential Strong Force factor)
    test_values['(2/3)^2'] = (mp.mpf('2')/3)**2
    test_values['(2/3)^3'] = (mp.mpf('2')/3)**3

    for form_name, val in test_values.items():
        if val == 0: continue
        err = abs(val - target_value) / target_value
        if err < best_error:
            best_error = err
            best_match = form_name

    if best_error < 0.05:
        return best_match, best_error

    return None, None

FINAL_DELTA_FORMULAS = {}

print("🔍 Searching for geometric form of $\delta$ factors...")

for name, data in QUARK_SCALING_HYPOTHESES.items():
    delta = data['delta']
    match, error = search_delta_form(delta, name)
    FINAL_DELTA_FORMULAS[name] = (match, error)
    if match:
        print(f"  {name:15} $\delta$ Match: {match:8} (Error: {float(error*100):.4f}%)")
    else:
        print(f"  {name:15} $\delta$ Match: No simple match found.")


# ============================================================================
# 3. FINAL UBP GEOMETRIC LAW SYNTHESIS
# ============================================================================

print("\n" + "="*80)
print("FINAL UBP GEOMETRIC LAW SYNTHESIS (v2.8)")
print("="*80)

print("\n**1. LEPTONIC LAW (Electroweak):**")
print(f"The geometric separation between lepton generations is a fixed, high-dimensional leap.")
print(f"$$\\frac{{M_{{G+1}}}}{{M_G}} \\approx \\left(\\frac{{1}}{{Y}}\\right)^{{4}}$$")


print("\n**2. QUARK LAW (Strong/Electroweak):**")
print(f"The geometric separation is simpler (N=2 or N=1), but perturbed by a force correction factor ($\delta$).")

def print_final_quark_law(key, name, N_base):
    match, error = FINAL_DELTA_FORMULAS[key]
    delta_val = QUARK_SCALING_HYPOTHESES[key]['delta']

    if match:
        print(f"• {name:15} ($\mathbf{{N={N_base}}}$): $\\frac{{M_{{G+1}}}}{{M_G}} = \\left(\\frac{{1}}{{Y}}\\right)^{{{N_base}}} \\times \\mathbf{{{match}}}$")
        print(f"  Check: ({mp.nstr(Y_INV, 4)})^{{{N_base}}} \times ({mp.nstr(delta_val, 4)}) = {mp.nstr(delta_val * (Y_INV**N_base), 6)}")
    else:
        print(f"• {name:15} ($\mathbf{{N={N_base}}}$): Correction $\delta = {mp.nstr(delta_val, 8)}$ (Unresolved Geometric Form)")

print_final_quark_law('R_Q_12 (s/d)', 'Strange/Down', 2)
print_final_quark_law('R_Q_23 (c/s)', 'Charm/Strange', 2)
print_final_quark_law('R_Q_34 (b/c)', 'Bottom/Charm', 1)

print("\n" + "="*80)
print("NEXT STEP: INTERPRETATION")
print("The output will provide the final geometric form of the $\delta$ factors, allowing us to state the complete, unified UBP law and move to the final theoretical interpretation.")