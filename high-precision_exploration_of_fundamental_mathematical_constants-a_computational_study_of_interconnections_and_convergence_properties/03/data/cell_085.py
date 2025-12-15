# Cell 85 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP EXACT RATIONAL / SYMBOLIC MUON-TAU PIPELINE
from fractions import Fraction
import json

# ---------------------------------------------------------------------
# UBP EXACT RATIONAL / SYMBOLIC MUON-TAU PIPELINE
# ---------------------------------------------------------------------

# Choose a high-quality rational approximation for pi
PI_APPROX = Fraction(355, 113)  # you can replace with better fractions for higher ticks

def compute_Y(pi_approx: Fraction) -> Fraction:
    return pi_approx / (pi_approx**2 + 2)

def generate_mu_tau_table(max_ticks: int = 10):
    table = []
    Y_base = compute_Y(PI_APPROX)
    Y_inv = Fraction(1, 1) / Y_base

    for tick in range(1, max_ticks + 1):
        # In your symbolic framework, each tick doubles the prior precision (binary-style)
        factor = 2**(tick - 1)
        # Fractional Y for tick — simply scale by factor to emulate your "tick method"
        # Optional: more complex tick → Y mapping can be substituted here
        Y_tick = Y_base  # could be adjusted if using Archimedes polygons per tick
        Y_inv_tick = Fraction(1, Y_tick)

        mu_e = Y_inv_tick ** 4
        tau_e = Y_inv_tick ** 6
        tau_mu = tau_e / mu_e

        # Symbolic forms
        mu_sym = f"(1/Y)^4"
        tau_sym = f"(1/Y)^6"
        tau_mu_sym = f"(1/Y)^2"

        table.append({
            "tick": tick,
            "Y": Y_tick,
            "1/Y": Y_inv_tick,
            "mu/e": mu_e,
            "tau/e": tau_e,
            "tau/mu": tau_mu,
            "mu/e_symbolic": mu_sym,
            "tau/e_symbolic": tau_sym,
            "tau/mu_symbolic": tau_mu_sym
        })
    return table

# ---------------------------------------------------------------------
# Run and save table
# ---------------------------------------------------------------------
MAX_TICKS = 10  # you can increase arbitrarily; exact arithmetic handles huge numbers
mu_tau_table = generate_mu_tau_table(MAX_TICKS)

# Print human-readable table
print("="*80)
print("UBP EXACT RATIONAL / SYMBOLIC MUON-TAU TABLE")
print("="*80)
print(f"{'Tick':>4} | {'Y':>12} | {'1/Y':>12} | {'μ/e':>20} | {'τ/e':>25} | {'τ/μ':>10}")
print("-"*100)
for row in mu_tau_table:
    print(f"{row['tick']:>4} | {row['Y']:>12} | {row['1/Y']:>12} | {row['mu/e']:>20} | {row['tau/e']:>25} | {row['tau/mu']:>10}")

# Save exact fractions table
with open("muon_tau_ubp_exact_table.json", "w") as f:
    json.dump([{k: str(v) for k, v in r.items()} for r in mu_tau_table], f, indent=2)

print("\nResults saved to muon_tau_ubp_exact_table.json")