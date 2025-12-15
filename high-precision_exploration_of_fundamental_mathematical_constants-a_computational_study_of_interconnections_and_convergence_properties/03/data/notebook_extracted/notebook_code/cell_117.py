# Cell 117 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP VIEW EXPLORER: E = M * C_max^2 WITH Y-SQUEEZE

# UBP VIEW EXPLORER: E = M * C_max^2 WITH Y-SQUEEZE
# --------------------------------------------------
# Idea:
#   Physical observables (E) are read as:
#       E_obs = M * C_max^2
#   where:
#       M      = effective "mass-like" factor (information content / OffBits)
#       C_max  = maximum computational rate for that configuration
#   and the Y-constant squeezes or scales these quantities in different ways.
#
#   This script:
#     - Computes π via an Archimedean process (your Bitfield π).
#     - Defines Y = π / (π^2 + 2) and invY = 1/Y.
#     - Defines several "views" of how Y can enter M and C_max.
#     - For each view, computes E_obs for a simple toy mass scale and prints
#       the resulting effective "mass-energy" and interpretation.

import mpmath as mp

mp.mp.dps = 80  # High precision for clean Y / invY behavior

# --------------------------------------------------
# 1. Archimedean π (Bitfield geometric primitive)
# --------------------------------------------------
def compute_pi_archimedes(max_steps=50, tol=mp.mpf('1e-30')):
    """
    Compute π using the classic Archimedean polygon method:
    start from a square, double the sides, and converge via
    inscribed/circumscribed perimeters.

    Interpretation in UBP terms:
      - n = number of polygon sides = discrete refinement level
      - The process is a 'temporal' flow on a 2D OffBit square.
    """
    n = mp.mpf('4')  # initial square
    sqrt2 = mp.sqrt(2)
    p = mp.mpf('4') * sqrt2  # inscribed perimeter
    P = mp.mpf('8')          # circumscribed perimeter
    prev_pi = None

    for step in range(1, max_steps + 1):
        n *= 2
        P_new = (mp.mpf('2') * p * P) / (p + P)
        p_new = mp.sqrt(p * P_new)
        p, P = p_new, P_new

        pi_approx = (p + P) / mp.mpf('4')

        if prev_pi is not None:
            rel_delta = abs((pi_approx - prev_pi) / prev_pi)
            if rel_delta < tol:
                return pi_approx, step

        prev_pi = pi_approx

    return pi_approx, max_steps

# --------------------------------------------------
# 2. Y-constant and basic OffBit / rate models
# --------------------------------------------------
def compute_Y(pi_val):
    """
    Your Y constant:
        Y = π / (π^2 + 2)
      and:
        invY = 1 / Y
    """
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    return Y, invY

def offbit_mass_factor(n_offbits, invY, mode="invY_power"):
    """
    Map a count of OffBits (information content) to an effective 'mass factor' M.

    Simple illustrative models:
      - mode='invY_power': M ~ invY^n_offbits
      - mode='linear':     M ~ n_offbits
      - mode='log':        M ~ log(1 + n_offbits) * invY

    This is a place to plug in UBP-specific mass rules later.
    """
    if mode == "invY_power":
        return invY ** n_offbits
    elif mode == "linear":
        return mp.mpf(n_offbits)
    elif mode == "log":
        return mp.log(1 + n_offbits) * invY
    else:
        raise ValueError(f"Unknown offbit mass mode: {mode}")

def max_computational_rate(base_rate, Y, view="Y_scales_rate"):
    """
    Define how Y affects the maximum computational rate C_max.

    Examples:
      - view='Y_scales_rate':
          C_max = base_rate * (1 / Y)
          (Y squeezes time so that smaller Y -> larger C_max)
      - view='Y_scales_inverse':
          C_max = base_rate * Y
          (Y acts as a throttling factor)
      - view='symmetric':
          C_max = base_rate * (1/Y + Y)
          (symmetric in Y and 1/Y)
    """
    if view == "Y_scales_rate":
        return base_rate * (mp.mpf('1') / Y)
    elif view == "Y_scales_inverse":
        return base_rate * Y
    elif view == "symmetric":
        return base_rate * ((mp.mpf('1') / Y) + Y)
    else:
        raise ValueError(f"Unknown rate view: {view}")

# --------------------------------------------------
# 3. E = M * C_max^2 with different Y-views
# --------------------------------------------------
def compute_E_observable(n_offbits, base_rate, invY, Y,
                         M_mode="invY_power",
                         C_view="Y_scales_rate"):
    """
    Core relation:
        E_obs = M * C_max^2
      with:
        M      = offbit_mass_factor(...)
        C_max  = max_computational_rate(...)

    Different choices of M_mode and C_view represent different
    'views' (reading rules) on how Y enters the physics.
    """
    M = offbit_mass_factor(n_offbits, invY, mode=M_mode)
    C_max = max_computational_rate(base_rate, Y, view=C_view)
    E_obs = M * (C_max ** 2)
    return M, C_max, E_obs

# --------------------------------------------------
# 4. Demonstration / scan over views
# --------------------------------------------------
def run_demo():
    print("="*80)
    print("UBP VIEW DEMO: E = M * C_max^2 WITH Y-SQUEEZE")
    print("="*80)

    # Step 1: Get Bitfield π
    pi_val, steps = compute_pi_archimedes()
    print(f"π(Bitfield)  ≈ {mp.nstr(pi_val, 25)} (stabilized in {steps} steps)")

    # Step 2: Y and 1/Y
    Y, invY = compute_Y(pi_val)
    print(f"Y           ≈ {mp.nstr(Y, 25)}")
    print(f"1 / Y       ≈ {mp.nstr(invY, 25)}")
    print()

    # Choose a toy "OffBit mass scale" and base rate
    n_offbits = 4              # e.g. small structured object (can vary)
    base_rate = mp.mpf('1.0')  # arbitrary unit rate (you can map to c later)

    # Define some views for M and C_max
    M_modes = ["invY_power", "linear", "log"]
    C_views = ["Y_scales_rate", "Y_scales_inverse", "symmetric"]

    print(f"Using n_offbits = {n_offbits}, base_rate = {base_rate}")
    print()

    # Scan all combinations of views
    for M_mode in M_modes:
        for C_view in C_views:
            M, C_max, E_obs = compute_E_observable(
                n_offbits=n_offbits,
                base_rate=base_rate,
                invY=invY,
                Y=Y,
                M_mode=M_mode,
                C_view=C_view
            )
            print("-" * 80)
            print(f"M_mode  = {M_mode}")
            print(f"C_view  = {C_view}")
            print(f"M       = {mp.nstr(M, 20)}")
            print(f"C_max   = {mp.nstr(C_max, 20)}")
            print(f"E_obs   = {mp.nstr(E_obs, 20)}")
    print("-" * 80)
    print("Interpretation:")
    print("  • Different (M_mode, C_view) pairs are different 'readings' of")
    print("    the same underlying Y / π / OffBit configuration.")
    print("  • In a full UBP particle model, you would:")
    print("      - Fix n_offbits per particle/species (information content).")
    print("      - Fix a physically motivated base_rate (e.g. c, c/Y, etc.).")
    print("      - Use NRCI/coherence to test which view-family reproduces")
    print("        empirical mass-energy patterns across many particles.")

# --------------------------------------------------
if __name__ == "__main__":
    run_demo()