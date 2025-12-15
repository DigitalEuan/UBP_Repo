# Cell 86 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title ExactNumber for rational arithmetic
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Dict, Any

# ===========================
# ExactNumber for rational arithmetic
# ===========================
class ExactNumber:
    def __init__(self, value):
        if isinstance(value, ExactNumber):
            self.f = value.f
        elif isinstance(value, Fraction):
            self.f = value
        elif isinstance(value, int):
            self.f = Fraction(value)
        else:
            raise TypeError(f"Unsupported type {type(value)}")
    def __add__(self, other): return ExactNumber(self.f + ExactNumber(other).f)
    def __radd__(self, other): return self.__add__(other)
    def __sub__(self, other): return ExactNumber(self.f - ExactNumber(other).f)
    def __rsub__(self, other): return ExactNumber(ExactNumber(other).f - self.f)
    def __mul__(self, other): return ExactNumber(self.f * ExactNumber(other).f)
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other): return ExactNumber(self.f / ExactNumber(other).f)
    def __rtruediv__(self, other): return ExactNumber(ExactNumber(other).f / self.f)
    def __pow__(self, exp: int): return ExactNumber(self.f ** exp)
    def __repr__(self): return str(self.f)

# ===========================
# Golay G24 → Leech Λ24 mechanism
# ===========================
class GolaySpringMechanism:
    A_MATRIX = [
        [1,1,1,1,1,1,1,1,1,1,1,0],
        [1,0,1,1,1,0,0,0,1,0,0,1],
        [1,1,0,1,0,1,0,0,0,1,0,1],
        [1,1,1,0,0,0,1,0,0,0,1,1],
        [1,1,0,0,0,1,1,1,0,0,0,1],
        [1,0,1,0,1,0,1,0,1,0,0,1],
        [1,0,0,1,1,1,0,1,0,0,0,1],
        [1,0,0,0,1,0,0,1,1,1,0,1],
        [1,1,0,0,0,1,0,1,0,1,1,0],
        [1,0,1,0,0,0,0,1,1,0,1,1],
        [1,0,0,1,0,0,1,0,1,1,1,0],
        [0,1,1,1,1,1,1,1,0,0,0,1]
    ]

    def encode(self, message: List[int]) -> List[int]:
        return [(sum(row[i] * message[i] for i in range(12)) % 2) for row in self.A_MATRIX]

# ===========================
# Leech Lattice placeholder
# ===========================
@dataclass
class LeechPoint:
    coordinates: List[ExactNumber]

def golay_to_leech(bits: List[int]) -> LeechPoint:
    return LeechPoint([ExactNumber(2*b-1) for b in bits])

# ===========================
# True UBP geometric Y computation
# ===========================
def compute_Y_from_point(p: LeechPoint, ticks: int) -> Fraction:
    """
    Compute Y from UBP geometry:
    - Consider the number of positive coordinates (shells)
    - Use a centerless Archimedes polygon-like fraction: ticks → rational approximation
    - Pure rational arithmetic
    """
    pos_count = sum(1 for c in p.coordinates if c.f > 0)
    neg_count = sum(1 for c in p.coordinates if c.f < 0)

    # Example UBP-inspired rational: positive fraction of coordinates, scaled by ticks
    numerator = Fraction(pos_count * (2**ticks))
    denominator = Fraction(pos_count**2 + neg_count**2 + 2)

    return numerator / denominator

# ===========================
# μ/τ derivation from geometry
# ===========================
def generate_mu_tau_table(max_ticks: int = 7) -> List[Dict[str, Any]]:
    golay = GolaySpringMechanism()
    table = []
    for tick in range(1, max_ticks+1):
        msg = [(i+tick)%2 for i in range(12)]
        code = golay.encode(msg)
        leech_point = golay_to_leech(code)
        Y = compute_Y_from_point(leech_point, tick)
        Y_inv = Fraction(1, Y)
        mu_e = Y_inv ** 4
        tau_e = Y_inv ** 6
        tau_mu = tau_e / mu_e
        table.append({
            "tick": tick,
            "Y": Y,
            "1/Y": Y_inv,
            "mu/e": mu_e,
            "tau/e": tau_e,
            "tau/mu": tau_mu,
            "mu/e_symbolic": "(1/Y)^4",
            "tau/e_symbolic": "(1/Y)^6",
            "tau/mu_symbolic": "(1/Y)^2"
        })
    return table

# ===========================
# Table print
# ===========================
def print_mu_tau_table(table: List[Dict[str, Any]]):
    print("="*120)
    print("UBP EXACT RATIONAL / SYMBOLIC MUON-TAU TABLE (UBP GEOMETRY)")
    print("="*120)
    print(f"{'Tick':>4} | {'Y':>20} | {'1/Y':>20} | {'μ/e':>25} | {'τ/e':>30} | {'τ/μ':>20}")
    print("-"*130)
    for row in table:
        print(f"{row['tick']:>4} | {str(row['Y']):>20} | {str(row['1/Y']):>20} | "
              f"{str(row['mu/e']):>25} | {str(row['tau/e']):>30} | {str(row['tau/mu']):>20}")

# ===========================
# Main execution
# ===========================
if __name__ == "__main__":
    mu_tau_table = generate_mu_tau_table(max_ticks=7)
    print_mu_tau_table(mu_tau_table)

    import json
    with open("muon_tau_ubp_geometry_table.json", "w") as f:
        json.dump([{k:str(v) for k,v in r.items()} for r in mu_tau_table], f, indent=2)
    print("\nResults saved to muon_tau_ubp_geometry_table.json")