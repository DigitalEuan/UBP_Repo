# Cell 142 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP RESONANCE SPECTRUM v2.7 - MINIMAL QUARK EXPONENT SEARCH
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
print("UBP RESONANCE SPECTRUM v2.7 - MINIMAL QUARK EXPONENT SEARCH")
print("=" * 80)
print(f"Core Constant 1/Y: {mp.nstr(Y_INV, 8)}")
print("-" * 80)

# ============================================================================
# 1. SEARCH FUNCTION (Modified for Small Exponents)
# ============================================================================

def find_geometric_match(target_ratio, constant, name, exponent_range):
    """Searches for powers of constant within the specified small range."""
    best_error = float('inf')
    best_exponent = None

    for exp in exponent_range:
        try:
            val = constant ** exp
            error = abs(val - target_ratio) / target_ratio

            if error < best_error:
                best_error = error
                best_exponent = exp
        except Exception:
            continue

    if best_exponent is not None and best_error < 0.05: # Only report matches with <5% error
        return f"{name}^{mp.nstr(best_exponent, 6)}", best_error, best_exponent
    return None, None, None

def search_quark_scaling(target_ratio, ratio_name):
    print(f"🔍 Searching for simple exponent N in (1/Y)^N for {ratio_name} ({mp.nstr(target_ratio, 6)})...")

    # Test Range: N from 0.5 to 2.5 (Focusing on 1 and 2)
    exponent_range = np.linspace(0.5, 2.5, 500)

    # Test 1: Powers of 1/Y (3.77...)
    match, error, exp = find_geometric_match(target_ratio, Y_INV, "1/Y", exponent_range)

    if match:
        print(f"  Best Match: {match}")
        print(f"  Error: {float(error*100):.5f}%")
        return match, error
    else:
        # If no Y-match is found, check for simple integer relationship (e.g., 5 * 4 = 20)
        closest_int_ratio = int(round(float(target_ratio)))
        error_int = abs(closest_int_ratio - target_ratio) / target_ratio

        if error_int < 0.05:
            print(f"  Alternative: Simple Integer {closest_int_ratio}")
            print(f"  Error: {float(error_int*100):.5f}%")
            return f"{closest_int_ratio}", error_int

        print("  No simple geometric match found (Y^N or integer).")
        return None, None

# ============================================================================
# 2. EXECUTE SEARCH
# ============================================================================

quark_scaling_results = {}

quark_scaling_results['R_Q_12 (s/d)'] = search_quark_scaling(R_Q_12, 'Quark G1->G2 (s/d)')
quark_scaling_results['R_Q_23 (c/s)'] = search_quark_scaling(R_Q_23, 'Quark G2->G3 (c/s)')
quark_scaling_results['R_Q_34 (b/c)'] = search_quark_scaling(R_Q_34, 'Quark G3->G4 (b/c)')

print("\n" + "="*80)
print("FINAL RESULT: QUARK SCALING EXPONENTS")
print("="*80)

# ============================================================================
# 3. INTERPRETATION
# ============================================================================

print("The model now suggests the following fundamental scaling laws:")
print("\n**1. LEPTONIC LAW (Electroweak):**")
print(f"$$ \\frac{{M_{{G+1}}}}{{M_G}} \\approx \\left(\\frac{{1}}{{Y}}\\right)^{{4}} $$")
print("This suggests 4 dimensional leaps in the geometric core.")

print("\n**2. QUARK LAW (Strong/Electroweak Interaction):**")

def interpret_quark_result(key, name):
    match, error = quark_scaling_results[key]
    ratio = [R_Q_12, R_Q_23, R_Q_34][['R_Q_12 (s/d)', 'R_Q_23 (c/s)', 'R_Q_34 (b/c)'].index(key)]

    if match and match.startswith('1/Y^'):
        print(f"• {name:15}: $\\left(\\frac{{1}}{{Y}}\\right)^{{{match.split('^')[1]}}}$ (Ratio $\\approx {mp.nstr(ratio, 4)}$)")
    elif match and error < 0.05:
        print(f"• {name:15}: Simple Integer Scaling {match} (Ratio $\\approx {mp.nstr(ratio, 4)}$)")
    else:
        print(f"• {name:15}: Unresolved/Complex Scaling")

interpret_quark_result('R_Q_12 (s/d)', 'Strange/Down')
interpret_quark_result('R_Q_23 (c/s)', 'Charm/Strange')
interpret_quark_result('R_Q_34 (b/c)', 'Bottom/Charm')

print("\n" + "="*80)
print("NEXT STEP: DEDUCE THE QUARK EXPONENT")
print("This search will define the true geometric difference between quark generations, revealing the simpler pattern hidden by the Strong Force.")