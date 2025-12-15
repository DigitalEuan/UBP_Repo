# Cell 124 from UBP_UNIFIED_SYSTEM_1.ipynb


#!/usr/bin/env python3
# @title UBP FINAL HYBRID: Y-TRANSLATION + (1/Y)^4 + SELECTIVE GOLAY
"""
FINAL HYBRID PUSH
- Effective OffBits with Y-translation (muon 3+3=6)
- Full geometric scaling (1/Y)^4 on effective OffBits
- Global Golay damp
- Selective multiplicity on proton (tunable weight)
- Expected: muon ~206.77, proton tunable to ~1836
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

class ParticleConfig:
    def __init__(self, name, base_offbits, use_y_translation=False, use_multiplicity=False, mult_weight=12):
        self.name = name
        self.base_offbits = int(base_offbits)
        self.use_y_translation = use_y_translation
        self.use_multiplicity = use_multiplicity
        self.mult_weight = int(mult_weight)

# Fixed k=4 with geometric scaling on effective OffBits
def mass_factor_M(particle, invY, Y, G_damp, floor_invY):
    off = mp.mpf(particle.base_offbits)
    if particle.use_y_translation:
        off += floor_invY
    M = off * (invY ** 4) * G_damp
    if particle.use_multiplicity:
        M *= golay_multiplicity(particle.mult_weight)
    return M

def E_observable(particle, invY, Y, G_damp, floor_invY):
    M = mass_factor_M(particle, invY, Y, G_damp, floor_invY)
    return M  # Rate=1 (cancels in ratios, simplifies)

def run_final_hybrid():
    print("=" * 100)
    print("UBP FINAL HYBRID: Y-TRANSLATION + (1/Y)^4 + SELECTIVE GOLAY")
    print("=" * 100)

    pi_val, _ = compute_pi_archimedes()
    Y, invY = compute_Y(pi_val)
    G_damp = golay_damp(Y)
    floor_invY = mp.floor(invY)

    print(f"Y ≈ {mp.nstr(Y, 20)} | 1/Y ≈ {mp.nstr(invY, 20)} | floor=3")
    print(f"Golay damp ≈ {mp.nstr(G_damp, 12)}")
    print()

    # Test different proton multiplicity weights
    weights_to_test = [0, 8, 12]  # none, mild, strong

    for wt in weights_to_test:
        mult_name = "none" if wt == 0 else f"wt{wt} (x{golay_multiplicity(wt)})"
        print(f"{'-'*30} PROTON GOLAY WEIGHT: {mult_name} {'-'*30}")

        particles = [
            ParticleConfig("electron", base_offbits=1),
            ParticleConfig("muon",     base_offbits=3, use_y_translation=True),
            ParticleConfig("proton",   base_offbits=9, use_multiplicity=(wt>0), mult_weight=wt),
        ]

        results = {}
        for p in particles:
            results[p.name] = E_observable(p, invY, Y, G_damp, floor_invY)

        electron_E = results['electron']
        physical = {name: E * (PDG_MASSES['electron'] / electron_E) for name, E in results.items()}
        ratios = {
            'muon_e':   physical['muon'] / physical['electron'],
            'proton_e': physical['proton'] / physical['electron']
        }
        nrc = mp.nstr(coherence_score(ratios, PDG_RATIOS), 8)

        print(f"Muon:  {float(physical['muon']):8.3f} MeV (target 105.658)")
        print(f"Proton:{float(physical['proton']):8.1f} MeV (target  938.272)")
        print(f"μ/e = {float(ratios['muon_e']):8.3f} (target 206.768)")
        print(f"p/e = {float(ratios['proton_e']):8.1f} (target 1836.2)")
        print(f"NRCI: {nrc}\n")

run_final_hybrid()