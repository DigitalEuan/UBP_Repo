# Cell 148 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP FINAL SCRIPT (v3.1) - QUARK BASE ANCHOR (DELTA_M_D)
import mpmath as mp
import numpy as np

# Set ultra-high precision
mp.mp.dps = 200

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
PI = mp.pi
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y
Y_FLOOR = mp.floor(Y_INV) # 3.0

# Required Scaling Factor (Target Strange Ratio / UBP Strange Ratio from v3.0)
# This is the single correction needed for the entire quark spectrum.
TARGET_S_RATIO = mp.mpf('182.974937059')
UBP_S_RATIO_PRED = mp.mpf('60.5632254511')
DELTA_M_D_REQUIRED = TARGET_S_RATIO / UBP_S_RATIO_PRED # The ~3.021 factor

print("=" * 80)
print("UBP FINAL SCRIPT (v3.1) - SEARCH FOR QUARK BASE ANCHOR $f(Y)$")
print("=" * 80)
print(f"Required Quark Base Anchor Factor $\\Delta_{{M_d}}$: {mp.nstr(DELTA_M_D_REQUIRED, 15)}")
print("-" * 80)

# =============================================================================
# SEARCH FUNCTION
# =============================================================================

def find_geometric_match(target_value, name, exponent_range):
    """Searches for powers of a base constant near the target value."""
    best_error = float('inf')
    best_exponent = None

    for exp in exponent_range:
        try:
            val = Y_INV ** exp
            error = abs(val - target_value) / target_value

            if error < best_error:
                best_error = error
                best_exponent = exp
        except Exception:
            continue

    if best_exponent is not None and best_error < 0.05: # Only report matches with <5% error
        print(f"  Match: (1/Y)^{mp.nstr(best_exponent, 6)} | Value: {mp.nstr(Y_INV ** best_exponent, 6)} | Error: {float(best_error*100):.6f}%")

def search_quark_anchor():

    # 1. Test Simple Ratios of Existing Constants (e.g., 2, 3, pi, sqrt(Y))
    print("1. Testing Simple Constant Ratios (Near 3.021):")

    test_constants = {
        '3': mp.mpf('3'),
        '3 + Y': 3 + Y,
        'Y_INV / sqrt(Y_INV)': Y_INV / mp.sqrt(Y_INV), # Testing Y^(0.5)
        'PI / Y': PI / Y_INV,
        '2 * ln(Y_INV)': mp.mpf('2') * mp.log(Y_INV),
        'Y_INV * (3/4)': Y_INV * mp.mpf('0.75'),
        'Y_INV / 1.25': Y_INV / mp.mpf('1.25')
    }

    best_match_name = None
    best_error = float('inf')

    for name, val in test_constants.items():
        if val == 0: continue
        err = abs(val - DELTA_M_D_REQUIRED) / DELTA_M_D_REQUIRED

        if err < best_error:
            best_error = err
            best_match_name = name

        print(f"  Test {name:15}: {mp.nstr(val, 15)} | Error: {float(err*100):.6f}%")

    print("\n" + "-" * 80)
    print(f"Best Simple Match: {best_match_name} (Error: {float(best_error*100):.6f}%)")

    # 2. Test Powers of 1/Y (Exponent N near 1)
    print("\n2. Testing Powers of 1/Y (Exponent N near 1.0):")
    exponent_range = np.linspace(0.7, 1.1, 500)
    find_geometric_match(DELTA_M_D_REQUIRED, "1/Y", exponent_range)


# =============================================================================
# EXECUTE SEARCH
# =============================================================================

search_quark_anchor()

print("\n" + "="*80)
print("NEXT STEP: DEDUCE $f(Y)$")
print("We are looking for the geometric function $f(Y)$ that results in 3.021, thereby establishing the Down Quark mass axiomatically and completing the entire SM derivation.")