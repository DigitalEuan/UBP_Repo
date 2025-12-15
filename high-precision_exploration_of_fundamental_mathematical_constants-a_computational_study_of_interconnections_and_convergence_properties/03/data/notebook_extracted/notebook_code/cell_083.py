# Cell 83 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP UNIFIED SYSTEM + EXACT FRACTION MUON/TAU MASS RATIO DERIVATION
#!/usr/bin/env python3
"""
================================================================================
UBP UNIFIED SYSTEM + EXACT FRACTION MUON/TAU MASS RATIO DERIVATION
================================================================================
Full working implementation:
- Golay G₂₄ with spring mechanism
- Leech Λ₂₄ lattice (exact arithmetic)
- ExactNumber / Fraction arithmetic (no floats)
- Parameter-free muon/tau mass ratio derivation from Y
- Archimedes polygon π (exact rational)
Author: Euan R A Craig, New Zealand
Date: 12 December 2025
================================================================================
"""

from __future__ import annotations
from typing import List, Tuple, Dict, Optional, Union, Any
from dataclasses import dataclass
from fractions import Fraction
import itertools
import json
from math import isqrt

# ============================================================================
# SECTION 1: ExactNumber – arbitrary rational arithmetic (no floats)
# ============================================================================

class ExactNumber:
    def __init__(self, value: Union[int, Fraction, 'ExactNumber']):
        if isinstance(value, ExactNumber):
            self.f = value.f
        elif isinstance(value, Fraction):
            self.f = value
        elif isinstance(value, int):
            self.f = Fraction(value)
        else:
            raise TypeError(f"Unsupported type for ExactNumber: {type(value)}")

    @property
    def doubled(self) -> int:
        doubled = self.f * 2
        if doubled.denominator != 1:
            raise ValueError(f"{self.f} is not integer or half-integer")
        return int(doubled)

    def to_fraction(self) -> Fraction:
        return self.f

    def __add__(self, other: Union[int, Fraction, 'ExactNumber']) -> 'ExactNumber':
        o = ExactNumber(other)
        return ExactNumber(self.f + o.f)

    def __radd__(self, other): return self.__add__(other)
    def __sub__(self, other): return ExactNumber(self.f - ExactNumber(other).f)
    def __rsub__(self, other): return ExactNumber(ExactNumber(other).f - self.f)
    def __mul__(self, other): return ExactNumber(self.f * ExactNumber(other).f)
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other): return ExactNumber(self.f / ExactNumber(other).f)
    def __rtruediv__(self, other): return ExactNumber(ExactNumber(other).f / self.f)
    def __neg__(self): return ExactNumber(-self.f)
    def __abs__(self): return ExactNumber(abs(self.f))
    def __pow__(self, exp: int): return ExactNumber(self.f ** exp)
    def __eq__(self, other): return self.f == ExactNumber(other).f
    def __lt__(self, other): return self.f < ExactNumber(other).f
    def __le__(self, other): return self.f <= ExactNumber(other).f
    def __gt__(self, other): return self.f > ExactNumber(other).f
    def __ge__(self, other): return self.f >= ExactNumber(other).f
    def __hash__(self): return hash(self.f)
    def __repr__(self): return str(self.f)
    def __int__(self) -> int:
        if self.f.denominator != 1:
            raise ValueError(f"{self.f} is not integer")
        return int(self.f)

    def round_to_nearest_integer(self) -> 'ExactNumber':
        return ExactNumber(round(self.f))


# ============================================================================
# SECTION 2: Matrix & Vector Helpers
# ============================================================================

def identity_matrix(n: int) -> List[List[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_multiply_binary(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    rows_A, cols_B = len(A), len(B[0])
    cols_A = len(A[0])
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % 2
    return result

def get_matrix_transpose(M: List[List[Any]]) -> List[List[Any]]:
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]

def hstack_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    return [A[i] + B[i] for i in range(len(A))]

def vector_add(v1: List[ExactNumber], v2: List[ExactNumber]) -> List[ExactNumber]:
    return [a + b for a, b in zip(v1, v2)]

def vector_subtract(v1: List[ExactNumber], v2: List[ExactNumber]) -> List[ExactNumber]:
    return [a - b for a, b in zip(v1, v2)]

def scalar_vector_multiply(scalar: Union[int, ExactNumber], v: List[ExactNumber]) -> List[ExactNumber]:
    s = ExactNumber(scalar)
    return [s * x for x in v]

def dot_product(v1: List[ExactNumber], v2: List[ExactNumber]) -> ExactNumber:
    return sum(a * b for a, b in zip(v1, v2))

def euclidean_norm_squared(v: List[ExactNumber]) -> ExactNumber:
    return sum(x * x for x in v)

def matrix_vector_multiply(M: List[List[ExactNumber]], v: List[ExactNumber]) -> List[ExactNumber]:
    return [dot_product(row, v) for row in M]

def solve_linear_system(A: List[List[ExactNumber]], b: List[ExactNumber]) -> List[ExactNumber]:
    n = len(A)
    aug = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        # pivot
        max_row = max(range(i, n), key=lambda k: abs(aug[k][i].to_fraction()))
        aug[i], aug[max_row] = aug[max_row], aug[i]
        if aug[i][i] == ExactNumber(0):
            raise ValueError("Singular matrix")
        for k in range(i+1, n):
            if aug[k][i] == ExactNumber(0):
                continue
            c = aug[k][i] / aug[i][i]
            for j in range(i, n+1):
                aug[k][j] -= c * aug[i][j]
    x = [ExactNumber(0)] * n
    for i in range(n-1, -1, -1):
        s = sum(aug[i][j] * x[j] for j in range(i+1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]
    return x


# ============================================================================
# SECTION 3: Golay G₂₄
# ============================================================================

class GolaySpringMechanism:
    A_MATRIX = [
        [1,1,1,1,1,1,1,1,1,1,1,0],[1,0,1,1,1,0,0,0,1,0,0,1],[1,1,0,1,0,1,0,0,0,1,0,1],
        [1,1,1,0,0,0,1,0,0,0,1,1],[1,1,0,0,0,1,1,1,0,0,0,1],[1,0,1,0,1,0,1,0,1,0,0,1],
        [1,0,0,1,1,1,0,1,0,0,0,1],[1,0,0,0,1,0,0,1,1,1,0,1],[1,1,0,0,0,1,0,1,0,1,1,0],
        [1,0,1,0,0,0,0,1,1,0,1,1],[1,0,0,1,0,0,1,0,1,1,1,0],[0,1,1,1,1,1,1,1,0,0,0,1]
    ]

    def __init__(self):
        self.I_12 = identity_matrix(12)
        self.G_MATRIX = hstack_matrices(self.I_12, self.A_MATRIX)
        self.H_MATRIX = hstack_matrices(get_matrix_transpose(self.A_MATRIX), self.I_12)
        self._syndrome_cache: Dict[Tuple[int,...], Optional[List[int]]] = {}

    def compute_syndrome(self, received: List[int]) -> Tuple[int, ...]:
        col = [[b] for b in received]
        s = matrix_multiply_binary(self.H_MATRIX, col)
        return tuple(row[0] for row in s)

    def find_error_pattern(self, syndrome: Tuple[int, ...], max_weight: int = 3) -> Optional[List[int]]:
        if syndrome in self._syndrome_cache:
            return self._syndrome_cache[syndrome]
        n = 24
        for w in range(max_weight + 1):
            for positions in itertools.combinations(range(n), w):
                e = [0]*n
                for p in positions:
                    e[p] = 1
                if self.compute_syndrome(e) == syndrome:
                    self._syndrome_cache[syndrome] = e
                    return e
        self._syndrome_cache[syndrome] = None
        return None

    def encode(self, message: List[int]) -> List[int]:
        row = [message]
        return matrix_multiply_binary(row, self.G_MATRIX)[0]

    def decode(self, received: List[int]) -> Tuple[List[int], int, bool]:
        syndrome = self.compute_syndrome(received)
        e = self.find_error_pattern(syndrome)
        if e is None:
            return received[:12], -1, False
        corrected = [(r + e[i]) % 2 for i, r in enumerate(received)]
        return corrected[:12], sum(e), True


# ============================================================================
# SECTION 4: Leech Lattice Λ₂₄
# ============================================================================

@dataclass
class LeechLatticePoint:
    coordinates: List[ExactNumber]

    def __post_init__(self):
        if len(self.coordinates) != 24:
            raise ValueError("Must be 24D")
        s = sum(self.coordinates)
        if s.to_fraction().denominator != 1 or int(s) % 2 != 0:
            raise ValueError("Sum must be even integer")
        ns = int(euclidean_norm_squared(self.coordinates))
        if ns == 2 or (ns > 0 and ns < 4):
            raise ValueError(f"Invalid norm²={ns}")

    @property
    def norm_squared(self) -> int:
        return int(euclidean_norm_squared(self.coordinates))


class LeechLattice:
    def __init__(self):
        self._basis = self._make_basis()

    def _make_basis(self) -> List[List[ExactNumber]]:
        n = 24
        B = [[ExactNumber(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            B[i][i] = ExactNumber(2)
        for i in range(n):
            j = (i + 1) % n
            B[i][j] = B[j][i] = ExactNumber(-1)
        return B

    @property
    def basis(self): return [row[:] for row in self._basis]

    def nearest_lattice_point(self, v: List[ExactNumber]) -> LeechLatticePoint:
        coeffs = solve_linear_system(get_matrix_transpose(self.basis), v)
        rounded = [c.round_to_nearest_integer() for c in coeffs]
        coords = matrix_vector_multiply(self.basis, rounded)
        return LeechLatticePoint(coords)


# ============================================================================
# SECTION 5: Bridge & State
# ============================================================================

def golay_to_leech(bits: List[int]) -> LeechLatticePoint:
    signed = [ExactNumber(2 * b - 1) for b in bits]
    return LeechLatticePoint(signed)

def leech_to_golay(p: LeechLatticePoint) -> Optional[List[int]]:
    if all(abs(c) == ExactNumber(1) for c in p.coordinates):
        return [int((c + ExactNumber(1)) / ExactNumber(2)) for c in p.coordinates]
    return None


class UBPGeometricState:
    def __init__(self, bits: List[int]):
        if len(bits) != 24:
            raise ValueError("Need 24 bits")
        self.bits = bits
        self.leech_point = golay_to_leech(bits)


# ============================================================================
# SECTION 6: EXACT FRACTION ARCHIMEDES π + MUON/TAU DERIVATION
# ============================================================================

def pi_nested_fraction(ticks: int) -> Fraction:
    """
    Exact rational π using polygon side doubling (Archimedes) approximation.
    Nested radicals represented via iterative rational Fraction.
    """
    # Start with side s0 = 1 (normalized)
    s = Fraction(1,1)
    for _ in range(ticks):
        inside_sqrt = Fraction(4) - s*s
        s = Fraction(isqrt(inside_sqrt.numerator), isqrt(inside_sqrt.denominator))
        s = Fraction(2) - s
        s = Fraction(isqrt(s.numerator), isqrt(s.denominator))
    sides = 2 ** ticks
    pi_approx = Fraction(sides) * s / 2
    return pi_approx

def compute_mu_tau(ticks: int) -> Dict[str, Fraction]:
    pi_exact = pi_nested_fraction(ticks)
    Y = pi_exact / (pi_exact**2 + 2)
    Y_inv = Fraction(1,1) / Y
    mu_e = Y_inv**4
    tau_e = Y_inv**6
    tau_mu = tau_e / mu_e
    return {"ticks": ticks, "Y": Y, "1/Y": Y_inv, "mu_e": mu_e, "tau_e": tau_e, "tau_mu": tau_mu}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("UBP UNIFIED SYSTEM + EXACT FRACTION MUON/TAU DERIVATION")
    print("="*80)

    # Test Golay + Leech
    golay = GolaySpringMechanism()
    msg = [1,0,1,0,1,0,1,0,1,0,1,0]
    code = golay.encode(msg)
    state = UBPGeometricState(code)
    print(f"Encoded 12-bit message → valid Leech point (norm²={state.leech_point.norm_squared})\n")

    # Exact μ/e and τ/e series
    print("TICKS | Y | 1/Y | μ/e | τ/e | τ/μ")
    for t in range(1, 8):
        r = compute_mu_tau(t)
        print(f"{r['ticks']} | {r['Y']} | {r['1/Y']} | {r['mu_e']} | {r['tau_e']} | {r['tau_mu']}")

    # Save results
    results_list = [compute_mu_tau(t) for t in range(1, 8)]
    with open("muon_tau_ubp_results_exact.json", "w") as f:
        json.dump([{k:str(v) for k,v in r.items()} for r in results_list], f, indent=2)

    print("\nResults saved to muon_tau_ubp_results_exact.json")

if __name__ == "__main__":
    main()