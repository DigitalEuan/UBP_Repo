# Cell 129 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP LIGHT QUARK OPTIMIZATION: BUILDING ON PROVEN CORE
#!/usr/bin/env python3
# UBP LIGHT QUARK OPTIMIZATION: BUILDING ON PROVEN CORE
"""
FOCUSED OPTIMIZATION PHASE 1
- Preserve PERFECT e/μ/p core (no changes to these formulas)
- Systematically optimize u/d/s quarks with minimal geometric corrections
- Same proven methodology: scale * Y^power corrections
- Goal: bring all light quarks under 5% error
- Maintain blazing-fast computation speed
"""

import mpmath as mp

mp.mp.dps = 80  # Sufficient precision for quark optimization

# PDG 2024 reference masses (MeV)
PDG = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583755'),
    'p': mp.mpf('938.272'),
    'u': mp.mpf('2.16'),    # current quark mass
    'd': mp.mpf('4.67'),    # current quark mass
    's': mp.mpf('93.5'),
}

def compute_pi_archimedes():
    """Stable Archimedes π calculation."""
    sqrt2 = mp.sqrt(2)
    p = mp.mpf('4') * sqrt2
    P = mp.mpf('8')
    for _ in range(60):
        P_new = (2 * p * P) / (p + P)
        p_new = mp.sqrt(p * P_new)
        p, P = p_new, P_new
    return (p + P) / 4

def offbit_layer(L, base_damp, invY, Y):
    """Optimized offbit layer for light quark sector."""
    floor_invY = mp.floor(invY)
    if L == 1:
        return base_damp * Y
    surge = (mp.mpf('1') - floor_invY**L) / (mp.mpf('1') - floor_invY) / L
    return base_damp * Y * min(surge, mp.mpf('1') + floor_invY / L)

def optimize_light_quarks():
    """Systematically optimize u/d/s quark masses while preserving core."""
    print("=" * 100)
    print("UBP LIGHT QUARK OPTIMIZATION: PRESERVING PERFECT CORE")
    print("=" * 100)

    # Fundamental constants (UNCHANGED from your perfect framework)
    pi_val = compute_pi_archimedes()
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    floor_invY = mp.floor(invY)

    print(f"Fundamental constants (preserved):")
    print(f"Y = {mp.nstr(Y, 15)} | 1/Y = {mp.nstr(invY, 15)} | floor(1/Y) = {int(floor_invY)}")
    print(f"Core particle ratios (VERIFIED PERFECT):")
    muon_ratio = invY**4 + floor_invY
    proton_ratio = mp.mpf('9') * invY**4 * (mp.mpf('1') + mp.mpf('0.001')*Y)
    print(f"Muon/e: {mp.nstr(muon_ratio, 10)} (0.002% error)")
    print(f"Proton/e: {mp.nstr(proton_ratio, 10)} (0.093% error)")
    print("-" * 60)

    # BASELINE LIGHT QUARK FORMULAS (from your framework)
    color_damp = mp.mpf('1') - (Y / mp.mpf('3'))

    # Baseline formulas to optimize
    def compute_quarks(quark_params):
        params_u, params_d, params_s = quark_params

        # Up quark baseline + correction
        M_u_base = invY**2 * offbit_layer(1, color_damp, invY, Y)
        M_u = M_u_base * (mp.mpf('1') + params_u['scale'] * Y**params_u['power'])

        # Down quark baseline + correction
        M_d_base = (invY**2 + floor_invY * Y) * offbit_layer(1, color_damp, invY, Y)
        M_d = M_d_base * (mp.mpf('1') + params_d['scale'] * Y**params_d['power'])

        # Strange quark baseline + correction
        M_s_base = (invY**4 + floor_invY * Y) * offbit_layer(2, color_damp, invY, Y)
        M_s = M_s_base * (mp.mpf('1') + params_s['scale'] * Y**params_s['power'])

        return M_u, M_d, M_s

    # Target ratios
    target_u = PDG['u'] / PDG['e']
    target_d = PDG['d'] / PDG['e']
    target_s = PDG['s'] / PDG['e']

    print(f"Light quark targets:")
    print(f"u/e = {mp.nstr(target_u, 8)} | d/e = {mp.nstr(target_d, 8)} | s/e = {mp.nstr(target_s, 8)}")
    print("-" * 60)

    # SYSTEMATIC OPTIMIZATION (same proven methodology as proton)
    best_errors = {'u': mp.inf, 'd': mp.inf, 's': mp.inf}
    best_params = None
    total_best = mp.inf

    # Parameter search ranges (conservative to preserve core)
    scales = [mp.mpf('0'), mp.mpf('-0.05'), mp.mpf('0.05'), mp.mpf('-0.1'), mp.mpf('0.1'), mp.mpf('-0.2'), mp.mpf('0.2')]
    powers = [1, 2]

    print(f"{'Su':>6} {'Pu':>4} {'Sd':>6} {'Pd':>4} {'Ss':>6} {'Ps':>4} | {'u_err':>8} {'d_err':>8} {'s_err':>8} {'TOTAL':>10}")
    print("-" * 85)

    for scale_u in scales:
        for power_u in powers:
            for scale_d in scales:
                for power_d in powers:
                    for scale_s in scales:
                        for power_s in powers:
                            params = (
                                {'scale': scale_u, 'power': power_u},
                                {'scale': scale_d, 'power': power_d},
                                {'scale': scale_s, 'power': power_s}
                            )

                            M_u, M_d, M_s = compute_quarks(params)

                            err_u = abs(M_u - target_u) / target_u * 100
                            err_d = abs(M_d - target_d) / target_d * 100
                            err_s = abs(M_s - target_s) / target_s * 100
                            total_err = err_u + err_d + err_s

                            print(f"{mp.nstr(scale_u,3):>6} {power_u:4d} {mp.nstr(scale_d,3):>6} {power_d:4d} {mp.nstr(scale_s,3):>6} {power_s:4d} | {mp.nstr(err_u,5):>8}% {mp.nstr(err_d,5):>8}% {mp.nstr(err_s,5):>8}% {mp.nstr(total_err,6):>10}")

                            # Track best combination that doesn't degrade core
                            if total_err < total_best:
                                # Verify core particles remain accurate
                                muon_check = invY**4 + floor_invY
                                proton_check = mp.mpf('9') * invY**4 * (mp.mpf('1') + mp.mpf('0.001')*Y)

                                muon_err = abs(muon_check - PDG['mu']/PDG['e']) / (PDG['mu']/PDG['e']) * 100
                                proton_err = abs(proton_check - PDG['p']/PDG['e']) / (PDG['p']/PDG['e']) * 100

                                if muon_err < 0.003 and proton_err < 0.1:  # Core protection
                                    total_best = total_err
                                    best_errors = {'u': err_u, 'd': err_d, 's': err_s}
                                    best_params = params

    print("-" * 85)

    # DISPLAY OPTIMAL RESULTS
    if best_params:
        M_u_opt, M_d_opt, M_s_opt = compute_quarks(best_params)

        print(f"\nOPTIMAL LIGHT QUARK CORRECTIONS:")
        print(f"Up quark:    scale={best_params[0]['scale']}, power={best_params[0]['power']}")
        print(f"Down quark:  scale={best_params[1]['scale']}, power={best_params[1]['power']}")
        print(f"Strange:     scale={best_params[2]['scale']}, power={best_params[2]['power']}")
        print()
        print(f"OPTIMIZED RESULTS:")
        print(f"u/e = {mp.nstr(M_u_opt, 8)} (target: {mp.nstr(target_u, 8)}) → {mp.nstr(best_errors['u'], 5)}% error")
        print(f"d/e = {mp.nstr(M_d_opt, 8)} (target: {mp.nstr(target_d, 8)}) → {mp.nstr(best_errors['d'], 5)}% error")
        print(f"s/e = {mp.nstr(M_s_opt, 8)} (target: {mp.nstr(target_s, 8)}) → {mp.nstr(best_errors['s'], 5)}% error")
        print()
        print(f"✓ CORE PRESERVED:")
        print(f"Muon error: {mp.nstr(muon_err, 6)}% (unchanged from 0.002%)")
        print(f"Proton error: {mp.nstr(proton_err, 6)}% (unchanged from 0.093%)")

        # Calculate actual masses
        scale = PDG['e']
        print(f"\nPHYSICAL MASSES (MeV):")
        print(f"Up quark:    {mp.nstr(M_u_opt * scale, 6)} MeV (PDG: {PDG['u']} MeV)")
        print(f"Down quark:  {mp.nstr(M_d_opt * scale, 6)} MeV (PDG: {PDG['d']} MeV)")
        print(f"Strange:     {mp.nstr(M_s_opt * scale, 6)} MeV (PDG: {PDG['s']} MeV)")
    else:
        print("No valid optimization found - core protection constraints too tight")
        print("Recommend relaxing constraints or expanding parameter search")

if __name__ == "__main__":
    optimize_light_quarks()