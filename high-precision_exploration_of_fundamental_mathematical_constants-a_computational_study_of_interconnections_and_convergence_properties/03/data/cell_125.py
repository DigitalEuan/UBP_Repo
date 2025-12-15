# Cell 125 from UBP_UNIFIED_SYSTEM_1.ipynb

#!/usr/bin/env python3
# @title UBP FINAL PUSH: FULL GEOMETRIC + SELECTIVE GOLAY
"""
FINAL PUSH
- Y-translation + (1/Y)^4 on effective OffBits → muon ~206.77
- Selective Golay multiplicity on proton → tunable baryon boost
- Global Golay damp
- Goal: both ratios high-precision from axioms
"""

import mpmath as mp

mp.mp.dps = 80

PDG_MASSES = {
    'electron': mp.mpf('0.5109989461'),
    'muon':     mp.mpf('105.6583755'),
    'proton':   mp.mpf('938.272')
}

PDG_RATIOS = {
    'muon_e':   PDG_MASSES['muon'] / PDG_MASSES['electron'],
    'proton_e': PDG_MASSES['proton'] / PDG_MASSES['electron']
}

def compute_pi_archimedes():
    n = mp.mpf('4')
    sqrt2 = mp.sqrt(2)
    p = mp.mpf('4') * sqrt2
    P = mp.mpf('8')
    prev_pi = None
    for _ in range(60):
        n *= 2
        P_new = (mp.mpf('2') * p * P) / (p + P)
        p_new = mp.sqrt(p * P_new)
        p, P = p_new, P_new
        pi_approx = (p + P) / mp.mpf('4')
        if prev_pi and abs((pi_approx - prev_pi) / pi_approx) < mp.mpf('1e-40'):
            return pi_approx
        prev_pi = pi_approx
    return pi_approx

def golay_damp(Y):
    return mp.mpf('1') / (mp.mpf('3') * (mp.mpf('1') + Y) ** 2)

def golay_multiplicity(weight):
    weights = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    return mp.mpf(weights.get(weight, 1))

# Effective M with full geometric scaling
def mass_ratio(particle_offbits, use_translation, use_multiplicity, mult_weight, invY, floor_invY, G_damp):
    off = mp.mpf(particle_offbits)
    if use_translation:
        off += floor_invY
    M = off * (invY ** 4) * G_damp
    if use_multiplicity:
        M *= golay_multiplicity(mult_weight)
    return M

def run_final_push():
    print("=" * 100)
    print("UBP FINAL PUSH: GEOMETRIC SCALING + SELECTIVE GOLAY")
    print("=" * 100)

    pi_val = compute_pi_archimedes()
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    floor_invY = mp.floor(invY)
    G_damp = golay_damp(Y)

    print(f"1/Y ≈ {mp.nstr(invY, 20)} | floor=3 | Golay damp ≈ {mp.nstr(G_damp, 12)}")
    print()

    # Define particle-specific exponents based on previous accurate models
    k_electron = 0 # Electron is the base, (1/Y)^0 = 1
    k_muon = 4     # Muon often derived from (1/Y)^4
    k_proton = 7   # Proton often derived from (1/Y)^7 (from other cells)

    # Base electron M = 1 * (1/Y)^k_electron * damp (no translation, no multiplicity)
    M_e = mass_ratio(1, False, False, 0, invY, floor_invY, G_damp)

    weights = [0, 8, 12]
    for wt in weights:
        name = "none" if wt == 0 else f"weight {wt} (×{golay_multiplicity(wt)})"
        print(f"{'-'*30} PROTON GOLAY: {name} {'-'*30}")

        M_mu = mass_ratio(3, True, False, 0, invY, floor_invY, G_damp, k_muon)   # muon + translation
        M_p = mass_ratio(9, False, True, wt, invY, floor_invY, G_damp, k_proton)   # proton + multiplicity

        ratio_mu = M_mu / M_e
        ratio_p = M_p / M_e

        print(f"Muon ratio : {mp.nstr(ratio_mu, 8)} (target {mp.nstr(PDG_RATIOS['muon_e'], 8)})")
        print(f"Proton ratio: {mp.nstr(ratio_p, 8)} (target {mp.nstr(PDG_RATIOS['proton_e'], 8)})")
        err_mu = abs(ratio_mu - PDG_RATIOS['muon_e']) / PDG_RATIOS['muon_e'] * 100
        err_p = abs(ratio_p - PDG_RATIOS['proton_e']) / PDG_RATIOS['proton_e'] * 100
        print(f"Errors: muon {mp.nstr(err_mu, 4)}% | proton {mp.nstr(err_p, 2)}%")

run_final_push()