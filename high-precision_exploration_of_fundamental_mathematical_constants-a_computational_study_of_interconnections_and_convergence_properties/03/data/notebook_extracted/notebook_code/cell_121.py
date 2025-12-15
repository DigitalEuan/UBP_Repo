# Cell 121 from UBP_UNIFIED_SYSTEM_1.ipynb


#!/usr/bin/env python3
# @title UBP FINAL VIEW ENGINE + GOLAY CODEWORDS
"""
UBP FINAL VIEW ENGINE + GOLAY CODEWORDS
E_obs = M * C_max^2 → FULL PDG + GOLAY CORRECTION
-------------------------------------------------
Golay Integration:
  - golay_damp(Y) = 1/[3(1+Y)^2] → error-correction overhead
  - codeword_multiplicity → # active Golay codewords per Hamming weight class
  - M = offbits × (1/Y)^k × golay_damp × codeword_mult
"""

import mpmath as mp

mp.mp.dps = 80

# PDG 2024 masses (MeV)
PDG_MASSES = {
    'electron': mp.mpf('0.5109989461'),
    'muon':     mp.mpf('105.6583755'),
    'proton':   mp.mpf('938.272')
}

PDG_RATIOS = {
    'muon_e':   PDG_MASSES['muon'] / PDG_MASSES['electron'],
    'proton_e': PDG_MASSES['proton'] / PDG_MASSES['electron']
}

# ------------------------------------------------------------
# GOLAY CODEWORD FUNCTIONS
# ------------------------------------------------------------
def golay_damp(Y):
    """Golay(24,12,8) error-correction overhead: 1/[3(1+Y)^2]."""
    return mp.mpf('1') / (mp.mpf('3') * (mp.mpf('1') + Y) ** 2)

def codeword_multiplicity(golay_weight):
    """Number of active Golay codewords for given Hamming weight class."""
    # Binary Golay codeword distribution (weights 0,8,12,16,24)
    weights = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    return mp.mpf(weights.get(golay_weight, 1))

# ------------------------------------------------------------
# CORE FUNCTIONS
# ------------------------------------------------------------
def compute_pi_archimedes(max_steps=60, tol=mp.mpf('1e-40')):
    """Bitfield π via Archimedean polygon refinement."""
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

        if prev_pi is not None:
            rel_delta = abs((pi_approx - prev_pi) / prev_pi)
            if rel_delta < tol:
                return pi_approx, step
        prev_pi = pi_approx
    return pi_approx, max_steps

def compute_Y(pi_val):
    """Y = π/(π²+2) - the UBP doorway constant."""
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    return Y, invY

class ParticleConfig:
    """Discrete particle description with Golay weight."""
    def __init__(self, name, offbits, shell_index, golay_weight=8):
        self.name = name
        self.offbits = int(offbits)
        self.shell_index = int(shell_index)
        self.golay_weight = int(golay_weight)  # Hamming weight class

class ViewConfig:
    """Reading rules for exponent k and rate factor R."""
    def __init__(self, name, mass_exponent_mode="fixed", fixed_exponent=4, rate_mode="invY"):
        self.name = name
        self.mass_exponent_mode = mass_exponent_mode
        self.fixed_exponent = int(fixed_exponent)
        self.rate_mode = rate_mode

    def mass_exponent(self, particle):
        if self.mass_exponent_mode == "shell":
            return particle.shell_index
        elif self.mass_exponent_mode == "twice_shell":
            return 2 * particle.shell_index
        return self.fixed_exponent  # default "fixed"

    def rate_factor(self, Y, invY):
        if self.rate_mode == "invY":
            return invY
        elif self.rate_mode == "Y":
            return Y
        elif self.rate_mode == "invY_plus_Y":
            return invY + Y
        return mp.mpf('1')  # "none" or default

def mass_factor_M(particle, view, invY, Y, G_damp):
    """M = offbits × (1/Y)^k × golay_damp × codeword_mult."""
    k = view.mass_exponent(particle)
    code_mult = codeword_multiplicity(particle.golay_weight)
    return mp.mpf(particle.offbits) * (invY ** k) * G_damp * code_mult

def max_computational_rate(base_rate, Y, invY, view):
    """C_max = base_rate × R(Y)."""
    return base_rate * view.rate_factor(Y, invY)

def E_observable(particle, view, base_rate, Y, invY, G_damp):
    """E_obs = M × C_max²."""
    M = mass_factor_M(particle, view, invY, Y, G_damp)
    C_max = max_computational_rate(base_rate, Y, invY, view)
    return M * (C_max ** 2)

# ------------------------------------------------------------
# PHYSICAL MAPPING + NRCI SCORING
# ------------------------------------------------------------
def compute_physical_masses(results, electron_E_obs):
    """Normalize to real electron mass."""
    scale_factor = PDG_MASSES['electron'] / electron_E_obs
    return {name: E_obs * scale_factor for name, E_obs in results.items()}

def coherence_score(ubp_ratios, pdg_ratios):
    """NRCI: higher = better ratio match."""
    score = mp.mpf('0')
    count = 0
    for key in pdg_ratios:
        if key in ubp_ratios:
            deviation = abs(mp.log(ubp_ratios[key] / pdg_ratios[key]))
            score += mp.mpf('1') / (mp.mpf('1') + deviation**2)
            count += 1
    return score / count if count > 0 else mp.mpf('0')

# ------------------------------------------------------------
# MAIN GOLAY VALIDATION
# ------------------------------------------------------------
def run_golay_validation():
    print("=" * 100)
    print("UBP + GOLAY(24,12,8) VALIDATION")
    print("=" * 100)

    # UBP fundamentals
    pi_val, steps = compute_pi_archimedes()
    Y, invY = compute_Y(pi_val)
    G_damp = golay_damp(Y)

    print(f"π(Bitfield)    ≈ {mp.nstr(pi_val, 25)} (converged in {steps} steps)")
    print(f"Y (doorway)   ≈ {mp.nstr(Y, 25)}")
    print(f"1/Y (scaling) ≈ {mp.nstr(invY, 25)}")
    print(f"Golay damp    ≈ {mp.nstr(G_damp, 12)}")
    print()

    # UBP + Golay particle assignments
    particles = [
        ParticleConfig("electron", offbits=1, shell_index=0, golay_weight=0),   # trivial
        ParticleConfig("muon",     offbits=3, shell_index=4, golay_weight=8),   # min nonzero wt
        ParticleConfig("proton",   offbits=9, shell_index=4, golay_weight=12),  # valence peak
    ]

    # Test the promising view with Golay correction
    views = [ViewConfig("shell_exp_golay", mass_exponent_mode="shell", rate_mode="invY")]
    base_rate = mp.mpf('1')

    for view in views:
        print(f"{'='*20} VIEW: {view.name} {'='*20}")
        results = {}
        for particle in particles:
            E_obs = E_observable(particle, view, base_rate, Y, invY, G_damp)
            results[particle.name] = E_obs
            code_mult = codeword_multiplicity(particle.golay_weight)
            print(f"{particle.name:8} | offbits:{particle.offbits:2} | golay_wt:{particle.golay_weight:2} | "
                  f"mult:{float(code_mult):5.0f} | k:{view.mass_exponent(particle):2} | "
                  f"E:{mp.nstr(E_obs,12)}")

        # Physical mapping
        electron_E = results['electron']
        physical = compute_physical_masses(results, electron_E)
        ubp_ratios = {
            'muon_e':   physical['muon'] / physical['electron'],
            'proton_e': physical['proton'] / physical['electron']
        }
        nrc_score = coherence_score(ubp_ratios, PDG_RATIOS)

        print("\nPHYSICAL MASSES (Golay corrected + normalized):")
        for name in ['electron', 'muon', 'proton']:
            print(f"  {name:8}: {float(physical[name]):8.3f} MeV (PDG: {float(PDG_MASSES[name]):8.3f})")
        print(f"\nRATIOS:")
        print(f"  μ/e = {float(ubp_ratios['muon_e']):7.3f} (PDG: {float(PDG_RATIOS['muon_e']):6.3f})")
        print(f"  p/e = {float(ubp_ratios['proton_e']):7.1f} (PDG: {float(PDG_RATIOS['proton_e']):6.1f})")
        print(f"NRCI Score: {float(nrc_score):.8f} (1.0 = perfect match)")

if __name__ == "__main__":
    run_golay_validation()