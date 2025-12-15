# Cell 96 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP Exact / Symbolic Muon-Tau Pipeline (Λ₂₄ Shells Integrated)
# =====================================================================
# UBP Exact / Symbolic Muon-Tau Pipeline (Λ₂₄ Shells Integrated)
# Author: Euan Craig (via ChatGPT)
# Date: 12 Dec 2025
# =====================================================================

from fractions import Fraction
from math import sqrt
import json

# -------------------------------
# Define Λ₂₄ shell norms (example up to 16 shells)
# -------------------------------
lambda24_shells = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

# -------------------------------
# Function to compute rational Y for a shell
# Can be adapted for multi-shell superpositions
# -------------------------------
def compute_Y(norm_squared):
    # Example: Y = 1 / (norm + offset) (tunable)
    return Fraction(1, norm_squared + 9)  # simple illustrative mapping

# -------------------------------
# Functions to compute exact mass ratios symbolically
# -------------------------------
def mu_over_e(Y: Fraction) -> Fraction:
    # mu/e ~ Y^(-2) (example rational form, tunable for UBP)
    return Y.denominator**2 // Y.numerator**2

def tau_over_e(Y: Fraction) -> Fraction:
    # tau/e ~ Y^(-4) (example rational form, tunable for UBP)
    return (Y.denominator**4) // (Y.numerator**4)

def tau_over_mu(mu_e: Fraction, tau_e: Fraction) -> Fraction:
    return tau_e // mu_e

# -------------------------------
# Build table
# -------------------------------
def build_table(shells):
    table = []
    for idx, norm in enumerate(shells, 1):
        Y = compute_Y(norm)
        Y_inv = Fraction(1, 1) / Y
        mu_e = mu_over_e(Y)
        tau_e = tau_over_e(Y)
        tau_mu = tau_over_mu(mu_e, tau_e)
        # Convert to MeV (physical units) using e mass ~ 0.511 MeV
        mu_e_MeV = float(mu_e) * 0.5109989461
        tau_e_MeV = float(tau_e) * 0.5109989461
        table.append({
            "Index": idx,
            "Norm²": norm,
            "Y": str(Y),
            "1/Y": str(Y_inv),
            "mu/e": str(mu_e),
            "tau/e": str(tau_e),
            "tau/mu": str(tau_mu),
            "mu/e (MeV)": round(mu_e_MeV, 6),
            "tau/e (MeV)": round(tau_e_MeV, 6)
        })
    return table

# -------------------------------
# Pretty print
# -------------------------------
def print_table(table):
    headers = ["Index","Norm²","Y","1/Y","mu/e","tau/e","tau/mu","mu/e (MeV)","tau/e (MeV)"]
    print(" | ".join(f"{h:>12}" for h in headers))
    print("-"*120)
    for row in table:
        print(" | ".join(f"{row[h]:>12}" for h in headers))

# -------------------------------
# Main execution
# -------------------------------
if __name__ == "__main__":
    ubp_table = build_table(lambda24_shells)
    print_table(ubp_table)

    # Save results as JSON
    with open("muon_tau_ubp_lattice_integrated.json", "w") as f:
        json.dump(ubp_table, f, indent=2)
    print("\nResults saved to muon_tau_ubp_lattice_integrated.json")