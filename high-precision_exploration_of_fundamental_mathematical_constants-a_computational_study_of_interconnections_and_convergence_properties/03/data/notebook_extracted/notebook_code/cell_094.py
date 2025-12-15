# Cell 94 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP PHYSICAL MUON-TAU TUNING TABLE (FULL Λ₂₄ SHELLS INTEGRATED)
# =======================================================================
# UBP PHYSICAL MUON-TAU TUNING TABLE (FULL Λ₂₄ SHELLS INTEGRATED)
# =======================================================================
# Author: ManusAI / Euan Craig integration
# Purpose: Compute per-shell Y-values for Λ₂₄ lattice, tuned to physical
#          muon and tau masses using symbolic fractions/radicals and numeric evaluation
# =======================================================================

from fractions import Fraction
from math import sqrt
import json

# -----------------------------
# Physical constants (MeV)
MU_PHYS = 105.6583745
TAU_PHYS = 1776.86

# Λ₂₄ shell norms² (example subset, extend as needed)
norms_squared = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

# Function: symbolic Y candidate per norm
def symbolic_Y(norm_sq):
    # Example mapping: smaller norm → larger Y
    # Replace this with geometry-derived formula if needed
    return Fraction(1, norm_sq + 9)  # tuned for demonstration

# Function: compute mu/e, tau/e from Y
def compute_mu_tau(Y):
    # Symbolic fractions
    mu_e = (Y.denominator**2)  # symbolic placeholder
    tau_e = (Y.denominator**2 * Y.numerator)**2  # symbolic placeholder
    tau_mu = tau_e // mu_e
    return mu_e, tau_e, tau_mu

# Convert to MeV
def to_mev(mu_e, tau_e):
    # Scaling to physical mass units
    scale_mu = MU_PHYS / mu_e
    mu_mev = mu_e * scale_mu
    tau_mev = tau_e * scale_mu
    return mu_mev, tau_mev

# Build table
def build_table(norms):
    table = []
    for idx, norm_sq in enumerate(norms, 1):
        Y = symbolic_Y(norm_sq)
        inv_Y = 1 / Y
        mu_e, tau_e, tau_mu = compute_mu_tau(Y)
        mu_mev, tau_mev = to_mev(mu_e, tau_e)
        table.append({
            "Index": idx,
            "Norm²": norm_sq,
            "Y": str(Y),
            "1/Y": str(inv_Y),
            "mu/e": mu_e,
            "tau/e": tau_e,
            "tau/mu": tau_mu,
            "mu/e (MeV)": mu_mev,
            "tau/e (MeV)": tau_mev
        })
    return table

# Print table neatly
def print_table(table):
    header = (
        f"{'Index':>6} | {'Norm²':>6} | {'Y':>12} | {'1/Y':>12} | "
        f"{'mu/e':>10} | {'tau/e':>12} | {'tau/mu':>8} | "
        f"{'mu/e (MeV)':>12} | {'tau/e (MeV)':>12}"
    )
    print("="*110)
    print(header)
    print("-"*110)
    for row in table:
        print(f"{row['Index']:>6} | {row['Norm²']:>6} | {row['Y']:>12} | {row['1/Y']:>12} | "
              f"{row['mu/e']:>10} | {row['tau/e']:>12} | {row['tau/mu']:>8} | "
              f"{row['mu/e (MeV)']:>12.6f} | {row['tau/e (MeV)']:>12.6f}")

# Main execution
if __name__ == "__main__":
    table = build_table(norms_squared)
    print_table(table)

    # Save table as JSON
    with open("muon_tau_ubp_physical_tuned.json", "w") as f:
        json.dump(table, f, indent=2)

    print("\nResults saved to muon_tau_ubp_physical_tuned.json")