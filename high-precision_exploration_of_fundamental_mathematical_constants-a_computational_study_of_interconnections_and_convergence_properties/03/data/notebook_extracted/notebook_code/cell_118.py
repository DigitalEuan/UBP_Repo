# Cell 118 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP DISCRETE VIEW ENGINE E_obs = M * C_max^2 WITH Y AS SCALING DOORWAY
#!/usr/bin/env python3
# UBP DISCRETE VIEW ENGINE
# E_obs = M * C_max^2 WITH Y AS SCALING DOORWAY
# ---------------------------------------------
# Intent:
#   - Keep structure as integer/rational as possible.
#   - Separate:
#       * Particle config: OffBit count, shell index, Golay weight.
#       * View config: how Y enters mass exponent and rate factor.
#   - Compute E_obs for different "views" without tuning floats,
#     then evaluate numerically only for inspection.

import mpmath as mp

mp.mp.dps = 80  # high precision for final evaluation

# ------------------------------------------------------------
# 1. Bitfield π via Archimedean method (conceptual primitive)
# ------------------------------------------------------------
def compute_pi_archimedes(max_steps=60, tol=mp.mpf('1e-40')):
    """
    Compute π from a 4-gon via inscribed/circumscribed perimeters.
    This is your Bitfield/OffBit π construction.
    """
    n = mp.mpf('4')
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

# ------------------------------------------------------------
# 2. Y constant and basic integer operators
# ------------------------------------------------------------
def compute_Y(pi_val):
    """
    Y = π / (π^2 + 2)
    1/Y is kept as exact reciprocal (symbolically) until evaluation.
    """
    Y = pi_val / (pi_val**2 + mp.mpf('2'))
    invY = mp.mpf('1') / Y
    return Y, invY

# ------------------------------------------------------------
# 3. Particle configuration (discrete)
# ------------------------------------------------------------
class ParticleConfig:
    """
    Minimal discrete description of a particle-like object.

    Attributes:
      - name: label ("electron","muon","proton", etc.)
      - offbits: integer count of OffBits (information content).
      - shell_index: integer shell / level index (e.g. 0,4,6,8...).
      - golay_weight: integer Hamming weight / code weight (optional).
    """
    def __init__(self, name, offbits, shell_index, golay_weight=None):
        self.name = name
        self.offbits = int(offbits)
        self.shell_index = int(shell_index)
        self.golay_weight = int(golay_weight) if golay_weight is not None else None

# ------------------------------------------------------------
# 4. View configuration (how Y enters)
# ------------------------------------------------------------
class ViewConfig:
    """
    Defines how to read Y into:
      - mass exponent k (integer)
      - rate factor R (rational/integer combination)

    Modes:
      - mass_exponent_mode:
          "shell":  k = shell_index
          "twice_shell": k = 2 * shell_index
          "fixed": k = fixed_exponent (e.g. 4,6,8)
      - rate_mode:
          "invY":       C_max ~ base_rate * (1/Y)
          "Y":          C_max ~ base_rate * Y
          "invY_plus_Y": C_max ~ base_rate * (1/Y + Y)
          "none":       C_max ~ base_rate (Y only in M)
    """
    def __init__(self,
                 name,
                 mass_exponent_mode="fixed",
                 fixed_exponent=4,
                 rate_mode="invY"):
        self.name = name
        self.mass_exponent_mode = mass_exponent_mode
        self.fixed_exponent = int(fixed_exponent)
        self.rate_mode = rate_mode

    def mass_exponent(self, particle: ParticleConfig):
        if self.mass_exponent_mode == "shell":
            return particle.shell_index
        elif self.mass_exponent_mode == "twice_shell":
            return 2 * particle.shell_index
        elif self.mass_exponent_mode == "fixed":
            return self.fixed_exponent
        else:
            raise ValueError(f"Unknown mass_exponent_mode: {self.mass_exponent_mode}")

    def rate_factor(self, Y, invY):
        if self.rate_mode == "invY":
            return invY
        elif self.rate_mode == "Y":
            return Y
        elif self.rate_mode == "invY_plus_Y":
            return invY + Y
        elif self.rate_mode == "none":
            return mp.mpf('1')
        else:
            raise ValueError(f"Unknown rate_mode: {self.rate_mode}")

# ------------------------------------------------------------
# 5. Mass factor M and max rate C_max
# ------------------------------------------------------------
def mass_factor_M(particle: ParticleConfig, view: ViewConfig, invY):
    """
    Very simple first-principles rule:
      M ~ offbits * (1/Y)^k
    where k is an integer exponent determined by view and shell_index.

    This is deliberately discrete:
      - offbits is integer
      - k is integer
      - invY^k is pure power; no floating structure beyond π, Y.
    """
    k = view.mass_exponent(particle)
    # M = OffBit count * (invY^k)
    return mp.mpf(particle.offbits) * (invY ** k)

def max_computational_rate(base_rate, Y, invY, view: ViewConfig):
    """
    C_max = base_rate * R(Y,invY)
    where R is chosen by the view.
    """
    R = view.rate_factor(Y, invY)
    return base_rate * R

def E_observable(particle: ParticleConfig,
                 view: ViewConfig,
                 base_rate,
                 Y,
                 invY):
    """
    E_obs = M * C_max^2
    with:
      M      = mass_factor_M(...)
      C_max  = max_computational_rate(...)
    """
    M = mass_factor_M(particle, view, invY)
    C_max = max_computational_rate(base_rate, Y, invY, view)
    E = M * (C_max ** 2)
    return M, C_max, E

# ------------------------------------------------------------
# 6. Demo runner
# ------------------------------------------------------------
def run_discrete_view_demo():
    print("="*90)
    print("UBP DISCRETE VIEW ENGINE: E_obs = M * C_max^2 WITH Y AS DOORWAY")
    print("="*90)

    # Step 1: Bitfield π
    pi_val, steps = compute_pi_archimedes()
    print(f"π(Bitfield)  ≈ {mp.nstr(pi_val, 30)} (stabilized in {steps} steps)")

    # Step 2: Y and 1/Y
    Y, invY = compute_Y(pi_val)
    print(f"Y           ≈ {mp.nstr(Y, 25)}")
    print(f"1 / Y       ≈ {mp.nstr(invY, 25)}")
    print()

    # Step 3: define some toy particles with discrete structure
    # You can later replace OffBits/shell_index with real UBP values.
    particles = [
        ParticleConfig("electron_like", offbits=1, shell_index=0),
        ParticleConfig("muon_like",     offbits=3, shell_index=4),  # shell ~ 4
        ParticleConfig("proton_like",   offbits=9, shell_index=4),
    ]

    # Step 4: define several view families
    views = [
        ViewConfig(
            name="fixed_k4_invY_rate",
            mass_exponent_mode="fixed",
            fixed_exponent=4,     # like your μ exponent
            rate_mode="invY"
        ),
        ViewConfig(
            name="shell_exponent_invY_rate",
            mass_exponent_mode="shell",
            fixed_exponent=0,
            rate_mode="invY"
        ),
        ViewConfig(
            name="fixed_k4_no_rate_Y_only_in_M",
            mass_exponent_mode="fixed",
            fixed_exponent=4,
            rate_mode="none"
        ),
        ViewConfig(
            name="fixed_k4_symmetric_rate",
            mass_exponent_mode="fixed",
            fixed_exponent=4,
            rate_mode="invY_plus_Y"
        ),
    ]

    # Step 5: choose a base rate (as a pure scalar; c = 1 in natural units)
    base_rate = mp.mpf('1')

    for view in views:
        print("-" * 90)
        print(f"VIEW: {view.name}")
        for p in particles:
            M, C_max, E = E_observable(
                particle=p,
                view=view,
                base_rate=base_rate,
                Y=Y,
                invY=invY
            )
            print(f"  Particle: {p.name}")
            print(f"    offbits      = {p.offbits}")
            print(f"    shell_index  = {p.shell_index}")
            print(f"    exponent k   = {view.mass_exponent(p)}")
            print(f"    M            = {mp.nstr(M, 20)}")
            print(f"    C_max        = {mp.nstr(C_max, 20)}")
            print(f"    E_obs        = {mp.nstr(E, 20)}")
        print()

    print("-" * 90)
    print("Notes:")
    print("  • This engine is still schematic, but now:")
    print("      - M is built from integer OffBits and integer exponents on 1/Y.")
    print("      - C_max is a discrete choice of how Y enters the rate.")
    print("  • To push toward physical masses, you would:")
    print("      - Assign OffBits and shell_index from your Leech/Golay/UBP rules.")
    print("      - Use electron_like as a unit and compare E_mu/E_e, E_p/E_e, etc.")
    print("      - Introduce NRCI/coherence scoring over view families.")

# ------------------------------------------------------------
if __name__ == "__main__":
    run_discrete_view_demo()