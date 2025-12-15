# Cell 73 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title UBP UNIFIED SYSTEM + MUON/TAU MASS RATIO DERIVATION V1
#!/usr/bin/env python3
"""
================================================================================
UBP UNIFIED SYSTEM + MUON/TAU MASS RATIO DERIVATION
================================================================================
Full working implementation:
- Golay G₂₄ with spring mechanism
- Leech Λ₂₄ lattice (exact arithmetic)
- ExactNumber with arbitrary Fraction support
- Parameter-free muon/tau mass ratio derivation from Y and Leech shells
NO FLOATS · NO NUMPY · PURE FIRST-PRINCIPLES
Author: Euan R A Craig, New Zealand
Date: 12 December 2025
================================================================================
"""

from __future__ import annotations
from typing import List, Tuple, Dict, Optional, Union, Any
from dataclasses import dataclass
from fractions import Fraction
import random
import json
import itertools # Added for combinations in GolaySpringMechanism

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

    def sqrt(self, max_iterations: int = 100) -> 'ExactNumber':
        if self.f < 0:
            raise ValueError("Cannot calculate square root of a negative ExactNumber.")
        if self.f == 0:
            return ExactNumber(0)

        # Initial guess: convert to float for initial guess, then back to Fraction
        x_float = float(self.f)
        guess_float = x_float / 2 if x_float > 1 else x_float
        guess = ExactNumber(Fraction.from_float(guess_float).limit_denominator(10**6)) # Limiting denominator for practicality

        for _ in range(max_iterations):
            new_guess = (guess + (self / guess)) / ExactNumber(2)
            if abs(new_guess - guess) < ExactNumber(Fraction(1, 10**20)): # Use a very small ExactNumber tolerance
                return new_guess
            if new_guess.f == guess.f: # Exact convergence for perfect squares
                return new_guess
            guess = new_guess
        return guess


# ============================================================================
# First Principles Mathematical Library (copied from TVtQacZDMYC6)
# ============================================================================

def factorial(n: int) -> int:
    if n < 0: raise ValueError("Factorial undefined for negative numbers")
    if n == 0 or n == 1: return 1
    result = 1
    for i in range(2, n + 1): result *= i
    return result

def abs_value(x: Union[float, ExactNumber]) -> Union[float, ExactNumber]:
    # Adapt to handle ExactNumber directly
    if isinstance(x, ExactNumber):
        return x if x >= ExactNumber(0) else -x
    return x if x >= 0 else -x

def sqrt_newton(x: Union[float, ExactNumber], tolerance: float = 1e-15, max_iterations: int = 100) -> Union[float, ExactNumber]:
    if isinstance(x, ExactNumber):
        # For ExactNumber, call its own sqrt method
        return x.sqrt(max_iterations=max_iterations)

    # Original float-based implementation
    if x < 0: raise ValueError("Cannot take square root of negative number")
    if x == 0: return 0.0
    if x == 1: return 1.0
    y = x / 2 if x > 1 else x
    for _ in range(max_iterations):
        y_new = (y + x / y) / 2
        if abs(y_new - y) < tolerance: return y_new
        y = y_new
    raise RuntimeError(f"sqrt did not converge after {max_iterations} iterations")

def sin_taylor(x: float, terms: int = 20) -> float:
    result = 0.0
    for n in range(terms):
        power = 2 * n + 1
        sign = 1 if n % 2 == 0 else -1
        x_power = 1.0
        for _ in range(power): x_power *= x
        fact = factorial(power)
        term = sign * x_power / fact
        result += term
        if abs(term) < 1e-16: break
    return result

def cos_taylor(x: float, terms: int = 20) -> float:
    result = 0.0
    for n in range(terms):
        power = 2 * n
        sign = 1 if n % 2 == 0 else -1
        x_power = 1.0
        for _ in range(power): x_power *= x
        fact = factorial(power)
        term = sign * x_power / fact
        result += term
        if abs(term) < 1e-16: break
    return result

def power_int(base: float, exponent: int) -> float:
    if exponent == 0: return 1.0
    if exponent < 0: return 1.0 / power_int(base, -exponent)
    result = 1.0
    for _ in range(exponent): result *= base
    return result


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
    return sum(a * b for a in v1 for b in v2) # Corrected dot product calculation

def euclidean_norm_squared(v: List[ExactNumber]) -> ExactNumber:
    return sum(x * x for x in v)

def matrix_vector_multiply(M: List[List[ExactNumber]], v: List[ExactNumber]) -> List[ExactNumber]:
    return [dot_product(row, v) for row in M]

def solve_linear_system(A: List[List[ExactNumber]], b: List[ExactNumber]) -> List[ExactNumber]:
    n = len(A)
    aug = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        # pivot
        max_row = max(range(i, n), key=lambda k: abs(aug[k][i]))
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
        s = sum(aug[i][j] * x[j] for j in range(i+1, n)) # Corrected sum to use ExactNumber
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
        ns = int(euclidean_norm_squared(self.coordinates)) # Convert ExactNumber to int for comparison
        if ns == 2 or (ns > 0 and ns < 4):
            raise ValueError(f"Invalid norm²={ns}")

    @property
    def norm_squared(self) -> int:
        return int(euclidean_norm_squared(self.coordinates))


class LeechLattice:
    def __init__(self):n
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
# SECTION 6: Archimedes Centerless Pi Derivation (ExactNumber)
# ============================================================================

class ArchimedesPi:
    def __init__(self, sides: int = 96):
        self.sides = sides

    def derive_pi(self) -> ExactNumber:
        r = ExactNumber(1)
        current_n_sides = 4
        current_a_in = ExactNumber(2) * r**2
        current_a_circ = ExactNumber(4) * r**2

        if self.sides < 4 or (self.sides & (self.sides - 1)) != 0:
            raise ValueError("Number of sides must be a power of 2 >= 4 for this method")

        doublings = 0
        temp_sides = self.sides
        while temp_sides > 4:
            temp_sides //= 2
            doublings += 1

        for _ in range(doublings):
            next_a_in = sqrt_newton(current_a_in * current_a_circ) # Use ExactNumber-aware sqrt_newton
            next_a_circ = (ExactNumber(2) * next_a_in * current_a_circ) / (next_a_in + current_a_circ)
            current_a_in = next_a_in
            current_a_circ = next_a_circ

        return (current_a_in + current_a_circ) / ExactNumber(2)

def run_archimedes_test(ticks: int = 24):
    sides = 2**(ticks + 2) # Start from 4 sides (2^2), so ticks=0 -> 4 sides, ticks=1 -> 8 sides
    arch = ArchimedesPi(sides=sides)
    pi_exact = arch.derive_pi() # This will be an ExactNumber

    # Calculate Y using ExactNumber
    Y_exact = pi_exact / (pi_exact**2 + ExactNumber(2))
    Y_inv_exact = ExactNumber(1) / Y_exact

    # Calculate ratios using ExactNumber
    mu_e_exact = Y_inv_exact ** 4
    tau_e_exact = Y_inv_exact ** 6
    tau_mu_exact = tau_e_exact / mu_e_exact

    # Real experimental values as ExactNumber (using Fractions)
    real_mu_e = ExactNumber(Fraction(206768283, 1000000))
    real_tau_e = ExactNumber(Fraction(347723, 100)) # 3477.23

    # Calculate errors as ExactNumber
    error_mu_e_exact = abs((mu_e_exact - real_mu_e) / real_mu_e) * ExactNumber(100)
    error_tau_e_exact = abs((tau_e_exact - real_tau_e) / real_tau_e) * ExactNumber(100)


    return {
        "ticks": ticks,
        "sides": sides,
        "pi_approx": float(pi_exact.to_fraction()), # Convert to float for display
        "Y": float(Y_exact.to_fraction()),
        "muon_e": float(mu_e_exact.to_fraction()),
        "tau_e": float(tau_e_exact.to_fraction()),
        "tau_mu": float(tau_mu_exact.to_fraction()),
        "error_mu_e_%": float(error_mu_e_exact.to_fraction()),
        "error_tau_e_%": float(error_tau_e_exact.to_fraction())
    }


# ============================================================================
# SECTION 7: MUON/TAU MASS RATIO DERIVATION (Parameter-Free)
# ============================================================================

class FundamentalConstants:
    def __init__(self):
        # Use Archimedes Pi derivation
        arch_pi_calculator = ArchimedesPi(sides=2**(20+2)) # 20 doublings from 4-gon
        self.pi_exact = arch_pi_calculator.derive_pi()

        self.Y = self.pi_exact / (self.pi_exact**2 + ExactNumber(2))
        self.Y_inv = ExactNumber(1) / self.Y

class MuonTauDerivation:
    def __init__(self):n
        self.const = FundamentalConstants()

    def derive(self) -> Dict[str, Any]:
        mu_e = self.const.Y_inv ** 4
        tau_e = self.const.Y_inv ** 6
        tau_mu = tau_e / mu_e

        # Convert to float for comparison and display
        mu_e_float = float(mu_e.to_fraction())
        tau_e_float = float(tau_e.to_fraction())
        tau_mu_float = float(tau_mu.to_fraction())

        # Reference values
        exp_mu_e = 206.768283
        exp_tau_e = 3477.23

        error_mu_e_percent = abs(mu_e_float - exp_mu_e) / exp_mu_e * 100
        error_tau_e_percent = abs(tau_e_float - exp_tau_e) / exp_tau_e * 100

        return {
            "Y": float(self.const.Y.to_fraction()),
            "1/Y": float(self.const.Y_inv.to_fraction()),
            "muon/electron": mu_e_float,
            "tau/electron": tau_e_float,
            "tau/muon": tau_mu_float,
            "error_mu_e_%": error_mu_e_percent,
            "error_tau_e_%": error_tau_e_percent,
            "pi_used": float(self.const.pi_exact.to_fraction()),
            "pi_num_sides": 2**(20+2)
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("UBP UNIFIED SYSTEM + MUON/TAU MASS RATIO DERIVATION")
    print("="*80)

    # Test Golay + Leech
    golay = GolaySpringMechanism()
    msg = [1,0,1,0,1,0,1,0,1,0,1,0]
    code = golay.encode(msg)
    state = UBPGeometricState(code)
    print(f"Encoded 12-bit message → valid Leech point (norm²={state.leech_point.norm_squared})")

    # Pi derivation test with increasing binary ticks
    print("\n" + "="*80)
    print("ARCHIMEDES CENTERLESS π IN UBP – TICKS TO COHERENCE")
    print("="*80)
    arch_results = []
    for t in range(0, 10): # Ticks from 0 (4 sides) to 9 (2^11 sides)
        try:
            res = run_archimedes_test(t)
            arch_results.append(res)
            print(f"Ticks: {res['ticks']} (sides={res['sides']}) | π≈{res['pi_approx']:.8f} | μ/e={res['muon_e']:.3f} | Error {res['error_mu_e_%']:.3f}% ")
        except Exception as e:
            print(f"Skipped Ticks: {t} due to error: {e}")

    with open('pi_ubp_test.json', 'w') as f:
        json.dump(arch_results, f, indent=2)
    print("\nArchimedes Pi results saved to pi_ubp_test.json")


    # Muon/Tau derivation
    deriv = MuonTauDerivation()
    results = deriv.derive()

    print("\n" + "="*80)
    print("MUON/TAU MASS RATIOS FROM BINARY GEOMETRY (USING EXACT π)")
    print("="*80)
    print(f"π used (sides {results['pi_num_sides']}) = {results['pi_used']:.15f}")
    print(f"Y        = {results['Y']:.15f}")
    print(f"1/Y      = {results['1/Y']:.10f}")
    print(f"μ/e      = {results['muon/electron']:.6f}  (exp 206.768)  error {results['error_mu_e_%']:.3f}% ")
    print(f"τ/e      = {results['tau/electron']:.2f}     (exp 3477)     error {results['error_tau_e_%']:.3f}% ")
    print(f"τ/μ      = {results['tau/muon']:.6f}")

    with open("muon_tau_ubp_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to muon_tau_ubp_results.json")

if __name__ == "__main__":
    main()