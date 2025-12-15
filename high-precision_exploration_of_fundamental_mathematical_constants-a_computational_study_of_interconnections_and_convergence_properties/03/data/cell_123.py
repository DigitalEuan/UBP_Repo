# Cell 123 from UBP_UNIFIED_SYSTEM_1.ipynb


#!/usr/bin/env python3
# @title UBP HYBRID: Y-TRANSLATION + SELECTIVE GOLAY (TARGET ~207 & ~1836)
"""
UBP HYBRID VIEW: Best of both
- Y-translation for muon (offbits 3 + floor(1/Y)=3 → 6 effective)
- Fixed k=4 power law ((1/Y)^4)
- Global Golay damp (coherence overhead)
- Selective Golay multiplicity on proton only (baryon valence boost)
- Goal: muon ~206.77, proton tunable to ~1836
"""

import mpmath as mp

mp.mp.dps = 80

# PDG targets
PDG_MASSES = {
    'electron': mp.mpf('0.5109989461'),
    'muon':     mp.mpf('105.6583755'),
    'proton':   mp.mpf('938.272')
}

PDG_RATIOS = {
    'muon_e':   PDG_MASSES['muon'] / PDG_MASSES['electron'],
    'proton_e': PDG_MASSES['proton'] / PDG_MASSES['electron']
}

# Core functions (π, Y, Golay)
def compute_pi_archimedes(max_steps=60, tol=mp.mpf('1e-40')):
    n = mp.mpf('4')
    sqrt2 = mp.sqrt(2)
    p = mp.mpf('4') * sqrt2
    P = mp.mpf('8')
    prev_pi = None
    for step in range(1, max_steps + 1):
        n *= 2
        P_new = (mp.mpf('2') * p * P) / (p + P)
        p_new = mp.sqrt(p * P_new)
        p, P = p_new, P_new
        pi_approx = (p + P) / mp.mpf('4')
        if prev_pi is not None and abs((pi_approx - prev_pi) / prev_pi) < tol:
            return pi_approx, step
        prev_pi = pi_approx
    return pi_approx, max_steps

def compute_Y(pi_val):
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    return Y, invY

def golay_damp(Y):
    return mp.mpf('1') / (mp.mpf('3') * (mp.mpf('1') + Y) ** 2)

def golay_multiplicity(weight):
    weights = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    return mp.mpf(weights.get(weight, 1))

# Particle with Y-translation flag
class ParticleConfig:
    def __init__(self, name, base_offbits, use_y_translation=False, use_multiplicity=False, mult_weight=12):
        self.name = name
        self.base_offbits = int(base_offbits)
        self.use_y_translation = use_y_translation
        self.use_multiplicity = use_multiplicity
        self.mult_weight = int(mult_weight)

# Fixed k=4 view
class ViewConfig:
    def __init__(self, name, rate_mode="invY"):
        self.name = name
        self.rate_mode = rate_mode

    def rate_factor(self, Y, invY):
        return invY if self.rate_mode == "invY" else mp.mpf('1')

def effective_offbits(particle, floor_invY):
    off = mp.mpf(particle.base_offbits)
    if particle.use_y_translation:
        off += floor_invY  # Whole/partial bridge
    return off

def mass_factor_M(particle, view, invY, Y, G_damp, floor_invY):
    off = effective_offbits(particle, floor_invY)
    M = off * (invY ** 4) * G_damp
    if particle.use_multiplicity:
        M *= golay_multiplicity(particle.mult_weight)
    return M

def E_observable(particle, view, base_rate, Y, invY, G_damp, floor_invY):
    M = mass_factor_M(particle, view, invY, Y, G_damp, floor_invY)
    R = view.rate_factor(Y, invY)
    return M * (R ** 2)

def compute_physical_masses(results, electron_E):
    scale = PDG_MASSES['electron'] / electron_E
    return {name: E * scale for name, E in results.items()}

def coherence_score(ubp_ratios, pdg_ratios):
    score = mp.mpf('0')
    count = 0
    for key in pdg_ratios:
        if key in ubp_ratios:
            dev = abs(mp.log(ubp_ratios[key] / pdg_ratios[key]))
            score += mp.mpf('1') / (mp.mpf('1') + dev**2)
            count += 1
    return score / count if count > 0 else mp.mpf('0')

def run_hybrid_validation():
    print("=" * 100)
    print("UBP HYBRID: Y-TRANSLATION + SELECTIVE GOLAY (LEPTON + BARYON SCALING)")
    print("=" * 100)

    pi_val, _ = compute_pi_archimedes()
    Y, invY = compute_Y(pi_val)
    G_damp = golay_damp(Y)
    floor_invY = mp.floor(invY)  # = 3

    print(f"Y ≈ {mp.nstr(Y, 20)} | 1/Y ≈ {mp.nstr(invY, 20)} | floor(1/Y) = {floor_invY}")
    print(f"Golay damp ≈ {mp.nstr(G_damp, 12)}")
    print()

    particles = [
        ParticleConfig("electron", base_offbits=1, use_y_translation=False),
        ParticleConfig("muon",     base_offbits=3, use_y_translation=True),   # +3 → 6
        ParticleConfig("proton",   base_offbits=9, use_multiplicity=True, mult_weight=12),  # 2576×
    ]

    views = [
        ViewConfig("hybrid_invY", rate_mode="invY"),
        ViewConfig("hybrid_no_rate", rate_mode="none"),
    ]

    base_rate = mp.mpf('1')

    for view in views:
        print(f"{'='*25} VIEW: {view.name} {'='*25}")
        results = {}
        for particle in particles:
            E_obs = E_observable(particle, view, base_rate, Y, invY, G_damp, floor_invY)
            results[particle.name] = E_obs
            eff_off = effective_offbits(particle, floor_invY)
            mult = golay_multiplicity(particle.mult_weight) if particle.use_multiplicity else 1
            print(f"{particle.name:8} | base:{particle.base_offbits} | eff:{float(eff_off):.0f} | mult:{float(mult):.0f} | "
                  f"E_raw:{mp.nstr(E_obs,12)}")

        electron_E = results['electron']
        physical = compute_physical_masses(results, electron_E)
        ubp_ratios = {
            'muon_e':   physical['muon'] / physical['electron'],
            'proton_e': physical['proton'] / physical['electron']
        }
        nrc = coherence_score(ubp_ratios, PDG_RATIOS)

        print("\nPHYSICAL MASSES:")
        for n in ['electron', 'muon', 'proton']:
            print(f"  {n:8}: {float(physical[n]):8.3f} MeV (PDG: {float(PDG_MASSES[n]):8.3f})")
        print(f"\nRATIOS:")
        print(f"  μ/e = {float(ubp_ratios['muon_e']):8.3f} (target 206.768)")
        print(f"  p/e = {float(ubp_ratios['proton_e']):8.1f} (target 1836.2)")
        print(f"NRCI: {float(nrc):.8f}\n")

run_hybrid_validation()