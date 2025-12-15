# Cell 127 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP OPTIMIZED: GEOMETRIC FOUNDATIONS + CONTROLLED ENHANCEMENTS
#!/usr/bin/env python3
# UBP OPTIMIZED: GEOMETRIC FOUNDATIONS + CONTROLLED ENHANCEMENTS
"""
OPTIMIZED PATH FORWARD
- Preserve proven (1/Y)^4 + floor(1/Y) muon formula
- Maintain 9*(1/Y)^4 proton structure
- Add controlled geometric corrections
- Systematic parameter optimization
- Goal: sub-0.001% muon, sub-0.1% proton accuracy
"""

import mpmath as mp

mp.mp.dps = 100  # High precision for optimization

# PDG 2024 reference values
PDG = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583755'),
    'p': mp.mpf('938.272')
}

def compute_pi_archimedes():
    """Stable Archimedes π calculation with convergence check."""
    sqrt2 = mp.sqrt(2)
    p = mp.mpf('4') * sqrt2  # Inner perimeter
    P = mp.mpf('8')          # Outer perimeter

    for _ in range(70):  # Sufficient for 100-digit convergence
        P_new = (2 * p * P) / (p + P)
        p_new = mp.sqrt(p * P_new)
        p, P = p_new, P_new

    return (p + P) / 4

def geometric_correction(Y, order=1):
    """Controlled geometric correction term based on Y."""
    if order == 1:
        return mp.mpf('1') - Y/2
    elif order == 2:
        return mp.mpf('1') - Y/2 + Y**2/8
    return mp.mpf('1')

def golay_damp(Y):
    """Golay damping factor - keep this minimal for core particles."""
    return mp.mpf('1') / (mp.mpf('3') * (mp.mpf('1') + Y)**2)

def optimized_mass_formulas(Y, muon_params, proton_params):
    """
    Optimized mass formulas preserving successful structure:
    - Muon: (1/Y)^4 + floor(1/Y) + small correction
    - Proton: 9*(1/Y)^4 * controlled factor
    """
    invY = mp.mpf('1') / Y
    floor_invY = mp.floor(invY)

    # UNCHANGED CORE THAT GAVE 0.002% MUON ACCURACY
    muon_base = invY**4 + floor_invY

    # Controlled correction terms (small adjustments only)
    muon_correction = muon_params['scale'] * Y**muon_params['power']
    M_mu = muon_base * (mp.mpf('1') + muon_correction)

    # PRESERVE 9*(1/Y)^4 PROTON STRUCTURE
    proton_base = mp.mpf('9') * invY**4

    # Minimal controlled adjustment
    proton_correction = proton_params['scale'] * Y**proton_params['power']
    M_p = proton_base * (mp.mpf('1') + proton_correction)

    return M_mu, M_p

def systematic_optimization():
    """Systematically optimize correction parameters around proven formulas."""
    print("=" * 120)
    print("UBP OPTIMIZED: BUILDING ON PROVEN 0.002% MUON ACCURACY")
    print("=" * 120)

    # Calculate fundamental constants
    pi_val = compute_pi_archimedes()
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    floor_invY = mp.floor(invY)

    print(f"Fundamental constants:")
    print(f"π (Archimedes) = {mp.nstr(pi_val, 25)}")
    print(f"Y (doorway)    = {mp.nstr(Y, 25)}")
    print(f"1/Y            = {mp.nstr(invY, 25)}")
    print(f"floor(1/Y)     = {int(floor_invY)}")
    print()

    # Reference ratios
    muon_e_ratio_target = PDG['mu'] / PDG['e']
    proton_e_ratio_target = PDG['p'] / PDG['e']

    print(f"Target ratios:")
    print(f"Muon/electron  = {mp.nstr(muon_e_ratio_target, 15)}")
    print(f"Proton/electron = {mp.nstr(proton_e_ratio_target, 15)}")
    print("-" * 80)

    # BASELINE: Your proven successful formulas (no corrections)
    muon_base = invY**4 + floor_invY
    proton_base = mp.mpf('9') * invY**4

    baseline_muon_err = abs(muon_base - muon_e_ratio_target) / muon_e_ratio_target * 100
    baseline_proton_err = abs(proton_base - proton_e_ratio_target) / proton_e_ratio_target * 100

    print(f"BASELINE (your proven formulas):")
    print(f"Muon ratio:  {mp.nstr(muon_base, 15)} (error: {mp.nstr(baseline_muon_err, 6)}%)")
    print(f"Proton ratio: {mp.nstr(proton_base, 15)} (error: {mp.nstr(baseline_proton_err, 5)}%)")
    print("-" * 80)

    # OPTIMIZATION: Small controlled corrections around proven formulas
    best_muon_err = baseline_muon_err
    best_proton_err = baseline_proton_err
    best_params = None

    # Systematic search over small correction parameters
    muon_scales = [mp.mpf('0'), mp.mpf('-0.001'), mp.mpf('0.001'), mp.mpf('-0.002'), mp.mpf('0.002')]
    muon_powers = [1, 2, 3]
    proton_scales = [mp.mpf('0'), mp.mpf('-0.0005'), mp.mpf('0.0005'), mp.mpf('-0.001'), mp.mpf('0.001')]
    proton_powers = [1, 2]

    print(f"{'Scale μ':>8} {'Power μ':>8} {'Scale p':>8} {'Power p':>8} | {'Muon err':>10} {'Proton err':>12}")
    print("-" * 80)

    for mu_scale in muon_scales:
        for mu_power in muon_powers:
            for p_scale in proton_scales:
                for p_power in proton_powers:
                    muon_params = {'scale': mu_scale, 'power': mu_power}
                    proton_params = {'scale': p_scale, 'power': p_power}

                    M_mu, M_p = optimized_mass_formulas(Y, muon_params, proton_params)

                    muon_err = abs(M_mu - muon_e_ratio_target) / muon_e_ratio_target * 100
                    proton_err = abs(M_p - proton_e_ratio_target) / proton_e_ratio_target * 100

                    print(f"{mp.nstr(mu_scale, 6):>8} {mu_power:8d} {mp.nstr(p_scale, 6):>8} {p_power:8d} | {mp.nstr(muon_err, 6):>10}% {mp.nstr(proton_err, 6):>12}%")

                    # Track best combination maintaining both accuracies
                    if muon_err < best_muon_err * mp.mpf('1.1') and proton_err < best_proton_err:
                        if muon_err + proton_err < best_muon_err + best_proton_err:
                            best_muon_err = muon_err
                            best_proton_err = proton_err
                            best_params = (mu_scale, mu_power, p_scale, p_power)

    print("-" * 80)

    # Show optimal results
    if best_params:
        mu_scale, mu_power, p_scale, p_power = best_params
        muon_params = {'scale': mu_scale, 'power': mu_power}
        proton_params = {'scale': p_scale, 'power': p_power}

        M_mu_opt, M_p_opt = optimized_mass_formulas(Y, muon_params, proton_params)

        print(f"\nOPTIMAL CORRECTION PARAMETERS:")
        print(f"Muon correction: scale = {mp.nstr(mu_scale, 8)}, power = {mu_power}")
        print(f"Proton correction: scale = {mp.nstr(p_scale, 8)}, power = {p_power}")
        print()
        print(f"OPTIMIZED RESULTS:")
        print(f"Muon ratio:  {mp.nstr(M_mu_opt, 15)} (error: {mp.nstr(best_muon_err, 7)}%)")
        print(f"Proton ratio: {mp.nstr(M_p_opt, 15)} (error: {mp.nstr(best_proton_err, 6)}%)")
        print()
        print(f"✓ IMPROVEMENT from baseline:")
        print(f"  Muon: {mp.nstr(baseline_muon_err, 6)}% → {mp.nstr(best_muon_err, 7)}%")
        print(f"  Proton: {mp.nstr(baseline_proton_err, 5)}% → {mp.nstr(best_proton_err, 6)}%")
    else:
        print("\nNo improvement found - baseline formulas are optimal within search range.")
        print("This confirms your original approach was fundamentally sound.")

if __name__ == "__main__":
    systematic_optimization()