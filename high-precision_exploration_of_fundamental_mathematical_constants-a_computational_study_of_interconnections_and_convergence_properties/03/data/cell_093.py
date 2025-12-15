# Cell 93 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
#!/usr/bin/env python3
"""
================================================================================
UBP PHYSICAL MUON-TAU TUNING (FULL Λ₂₄ SHELLS INTEGRATED)
================================================================================
"""

from fractions import Fraction
import json
import math

# -----------------------------
# Physical constants
electron_mass = 0.5109989461  # MeV
muon_mass_phys = 105.6583745  # MeV
tau_mass_phys = 1776.86       # MeV

# -----------------------------
# Λ₂₄ lattice shell norms
shell_norms = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

# -----------------------------
# Compute Y from lattice norms and tune toward physical masses
def compute_Y_tuned(norm2):
    # Use exact fraction based on lattice shell
    base_fraction = Fraction(1, norm2 + 1)  # UBP-inspired base
    # Tune factor to approach muon mass
    tuning_factor = Fraction(int(muon_mass_phys / electron_mass))
    Y_tuned = base_fraction * tuning_factor**Fraction(1, 4)
    return Y_tuned

# -----------------------------
# Build table
def build_mu_tau_table(shell_norms):
    table = []
    for i, norm2 in enumerate(shell_norms, start=1):
        Y = compute_Y_tuned(norm2)
        invY = 1 / Y

        # μ/e = (1/Y)^4, τ/e = (1/Y)^6
        mu_e = invY**4
        tau_e = invY**6
        tau_mu = tau_e / mu_e

        mu_e_MeV = float(mu_e) * electron_mass
        tau_e_MeV = float(tau_e) * electron_mass

        table.append({
            "Index": i,
            "Norm²": norm2,
            "Y": str(Y),
            "1/Y": str(invY),
            "mu/e": str(mu_e),
            "tau/e": str(tau_e),
            "tau/mu": str(tau_mu),
            "mu/e (MeV)": mu_e_MeV,
            "tau/e (MeV)": tau_e_MeV
        })
    return table

# -----------------------------
# Print table
def print_table(table):
    headers = ["Index", "Norm²", "Y", "1/Y", "mu/e", "tau/e", "tau/mu", "mu/e (MeV)", "tau/e (MeV)"]
    print("="*120)
    print("UBP PHYSICAL MUON-TAU TUNING TABLE (FULL Λ₂₄ SHELLS INTEGRATED)")
    print("="*120)
    print(f"{' | '.join(f'{h:>12}' for h in headers)}")
    print("-"*120)
    for row in table:
        print(f"{row['Index']:>12} | {row['Norm²']:>12} | {row['Y']:>12} | {row['1/Y']:>12} | "
              f"{row['mu/e']:>20} | {row['tau/e']:>25} | {row['tau/mu']:>12} | "
              f"{row['mu/e (MeV)']:>12.6f} | {row['tau/e (MeV)']:>12.6f}")
    print("="*120)

# -----------------------------
# Main execution
if __name__ == "__main__":
    table = build_mu_tau_table(shell_norms)
    print_table(table)

    # Save as JSON
    with open("muon_tau_ubp_physical_tuned.json", "w") as f:
        json.dump(table, f, indent=2)
    print("\nResults saved to muon_tau_ubp_physical_tuned.json")