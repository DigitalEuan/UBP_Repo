# Cell 95 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP LATTICE-COUPLED PHYSICAL MUON-TAU ENGINE. Λ₂₄ SHELLS WITH PHYSICAL-TUNED Y-INTEGRATION
# =======================================================================
# UBP LATTICE-COUPLED PHYSICAL MUON-TAU ENGINE
# Λ₂₄ SHELLS WITH PHYSICAL-TUNED Y-INTEGRATION
# =======================================================================

from fractions import Fraction
from math import sqrt
import json
from scipy.optimize import minimize_scalar

MU_PHYS = 105.6583745
TAU_PHYS = 1776.86

# Define Λ₂₄ lattice shell norms (squared)
lattice_norms_squared = [4,6,8,10,12,14,16,18,20,22]

def symbolic_Y(norm_sq):
    # Initial fraction estimate based on lattice shell
    return Fraction(1, norm_sq + 9)

def mu_tau_numeric(Y):
    # Basic UBP functional forms
    mu_e = float((1/Y)**2)
    tau_e = float((1/Y)**3)
    tau_mu = tau_e / mu_e
    return mu_e, tau_e, tau_mu

def scale_to_physical(mu_e, tau_e):
    # Scale to match experimental muon
    scale = MU_PHYS / mu_e
    mu_mev = mu_e * scale
    tau_mev = tau_e * scale
    return mu_mev, tau_mev

def objective(Y_guess):
    mu_e, tau_e, _ = mu_tau_numeric(Y_guess)
    mu_mev, tau_mev = scale_to_physical(mu_e, tau_e)
    # Error relative to physical masses
    return ((mu_mev - MU_PHYS)/MU_PHYS)**2 + ((tau_mev - TAU_PHYS)/TAU_PHYS)**2

def optimize_Y(norm_sq):
    # Optimize Y to minimize physical error
    res = minimize_scalar(objective, bounds=(0.01, 2), method='bounded')
    return Fraction(res.x).limit_denominator(10**9)

def build_lattice_table(norms):
    table = []
    for idx, norm_sq in enumerate(norms, 1):
        Y_opt = optimize_Y(norm_sq)
        inv_Y = 1 / Y_opt
        mu_e, tau_e, tau_mu = mu_tau_numeric(Y_opt)
        mu_mev, tau_mev = scale_to_physical(mu_e, tau_e)
        table.append({
            "Index": idx,
            "Norm²": norm_sq,
            "Y": str(Y_opt),           # symbolic-friendly
            "1/Y": str(inv_Y),         # symbolic-friendly
            "mu/e": mu_e,
            "tau/e": tau_e,
            "tau/mu": tau_mu,
            "mu/e (MeV)": mu_mev,
            "tau/e (MeV)": tau_mev
        })
    return table

def print_lattice_table(table):
    header = (
        f"{'Index':>6} | {'Norm²':>6} | {'Y':>20} | {'1/Y':>20} | "
        f"{'mu/e':>10} | {'tau/e':>12} | {'tau/mu':>8} | "
        f"{'mu/e (MeV)':>12} | {'tau/e (MeV)':>12}"
    )
    print("="*120)
    print(header)
    print("-"*120)
    for row in table:
        print(f"{row['Index']:>6} | {row['Norm²']:>6} | {row['Y']:>20} | {row['1/Y']:>20} | "
              f"{row['mu/e']:>10.6f} | {row['tau/e']:>12.6f} | {row['tau/mu']:>8.6f} | "
              f"{row['mu/e (MeV)']:>12.6f} | {row['tau/e (MeV)']:>12.6f}")

if __name__ == "__main__":
    lattice_table = build_lattice_table(lattice_norms_squared)
    print_lattice_table(lattice_table)

    # JSON-safe save
    with open("muon_tau_ubp_lattice_integrated.json", "w") as f:
        json.dump(lattice_table, f, indent=2)

    print("\nResults saved to muon_tau_ubp_lattice_integrated.json")