# Cell 19 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
import random
from fractions import Fraction


# ============================================================================
# SECTION 1: PURE PYTHON ARITHMETIC & MATRIX OPERATIONS (Re-extracted)
# ============================================================================
class ExactNumber:
    """
    Represents exact numbers as integers or half-integers.
    Internally stored as 2*value to maintain integer arithmetic.
    """
    def __init__(self, value: Union[int, float, 'ExactNumber']):
        if isinstance(value, ExactNumber):
            self.doubled = value.doubled
        elif isinstance(value, Fraction):
            if value.denominator == 1:
                self.doubled = value.numerator * 2
            elif value.denominator == 2:
                self.doubled = value.numerator
            else:
                raise ValueError(f"Cannot represent {value} as integer or half-integer")
        elif isinstance(value, float):
            frac = Fraction(value).limit_denominator(1000)
            if frac.denominator == 1:
                self.doubled = int(frac.numerator * 2)
            elif frac.denominator == 2:
                self.doubled = int(frac.numerator)
            else:
                raise ValueError(f"Cannot represent {value} as integer or half-integer")
        else:
            self.doubled = int(value) * 2

    def to_float(self) -> float:
        return self.doubled / 2.0

    def to_fraction(self) -> Fraction:
        return Fraction(self.doubled, 2)

    def __add__(self, other):
        if isinstance(other, ExactNumber):
            result = ExactNumber(0)
            result.doubled = self.doubled + other.doubled
            return result
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, ExactNumber):
            result = ExactNumber(0)
            result.doubled = self.doubled - other.doubled
            return result
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            result = ExactNumber(0)
            result.doubled = int(self.doubled * scalar)
            return result
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __eq__(self, other):
        if isinstance(other, ExactNumber):
            return self.doubled == other.doubled
        return False

    def __repr__(self):
        if self.doubled % 2 == 0:
            return f"{self.doubled // 2}"
        else:
            return f"{self.doubled}/2"


def identity_matrix(n: int) -> List[List[int]]:
    """Create n×n identity matrix."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def matrix_multiply_binary(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices over GF(2) (binary field).
    All operations mod 2.
    """
    rows_A, cols_A = len(A), len(A[0]) if A else 0
    rows_B, cols_B = len(B), len(B[0]) if B else 0

    if cols_A != rows_B:
        raise ValueError(f"Incompatible dimensions: {rows_A}×{cols_A} × {rows_B}×{cols_B}")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            sum_val = 0
            for k in range(cols_A):
                sum_val += A[i][k] * B[k][j]
            result[i][j] = sum_val % 2

    return result


def get_matrix_transpose(M: List[List[int]]) -> List[List[int]]:
    """Transpose a matrix."""
    if not M:
        return []
    rows, cols = len(M), len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]


def hstack_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Horizontally stack two matrices (side by side)."""
    if len(A) != len(B):
        raise ValueError("Matrices must have same number of rows")
    return [A[i] + B[i] for i in range(len(A))]


def are_matrices_equal_binary(A: List[List[int]], B: List[List[int]]) -> bool:
    """Check if two binary matrices are equal."""
    if len(A) != len(B):
        return False
    for i in range(len(A)):
        if len(A[i]) != len(B[i]):
            return False
        for j in range(len(A[i])):
            if (A[i][j] % 2) != (B[i][j] % 2):
                return False
    return True


def vector_add(v1: List[float], v2: List[float]) -> List[float]:
    """Add two vectors."""
    return [a + b for a, b in zip(v1, v2)]


def vector_subtract(v1: List[float], v2: List[float]) -> List[float]:
    """Subtract two vectors."""
    return [a - b for a, b in zip(v1, v2)]


def scalar_vector_multiply(scalar: float, v: List[float]) -> List[float]:
    """Multiply vector by scalar."""
    return [scalar * x for x in v]


def dot_product(v1: List[float], v2: List[float]) -> float:
    """Compute dot product of two vectors."""
    return sum(a * b for a, b in zip(v1, v2))


def euclidean_norm(v: List[float]) -> float:
    """Compute Euclidean norm of a vector."""
    return (sum(x * x for x in v)) ** 0.5


def matrix_vector_multiply(M: List[List[float]], v: List[float]) -> List[float]:
    """Multiply matrix by vector."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def all_close(a: Union[float, List[float]], b: Union[float, List[float]], tol: float = 1e-9) -> bool:
    """Check if values are close within tolerance."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < tol
    elif isinstance(a, list) and isinstance(b, list):
        return all(abs(x - y) < tol for x, y in zip(a, b))
    return False


def solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    """
    Solve Ax = b using Gaussian elimination.
    Returns x such that A @ x = b.
    """
    n = len(A)
    if n == 0:
        return []

    aug = [A[i][:] + [b[i]] for i in range(n)]

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]

        for k in range(i + 1, n):
            if abs(aug[i][i]) < 1e-10:
                continue
            c = aug[k][i] / aug[i][i]
            for j in range(i, n + 1):
                aug[k][j] -= c * aug[i][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = aug[i][n]
        for j in range(i + 1, n):
            x[i] -= aug[i][j] * x[j]
        if abs(aug[i][i]) > 1e-10:
            x[i] /= aug[i][i]

    return x


# ============================================================================
# SECTION 2: GOLAY G₂₄ ERROR CORRECTION WITH SPRING MECHANISM (Re-extracted)
# ============================================================================

class GolaySpringMechanism:
    """
    The 'spring mechanism' - generates Golay syndromes on-demand geometrically.
    """

    A_MATRIX = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1]
    ]

    def __init__(self):
        self.I_12 = identity_matrix(12)
        self.G_MATRIX = hstack_matrices(self.I_12, self.A_MATRIX)
        self.H_MATRIX = hstack_matrices(get_matrix_transpose(self.A_MATRIX), self.I_12)

        GHT = matrix_multiply_binary(self.G_MATRIX, get_matrix_transpose(self.H_MATRIX))
        zero_matrix = [[0] * 12 for _ in range(12)]
        assert are_matrices_equal_binary(GHT, zero_matrix), "G × H^T must be zero"

        self._syndrome_cache = {}

    def compute_syndrome(self, received: List[int]) -> Tuple[int, ...]:
        if len(received) != 24:
            raise ValueError("Received word must be 24 bits")

        received_col = [[bit] for bit in received]
        syndrome_col = matrix_multiply_binary(self.H_MATRIX, received_col)
        syndrome = tuple(row[0] for row in syndrome_col)

        return syndrome

    def find_error_pattern(self, syndrome: Tuple[int, ...], max_weight: int = 3) -> Optional[List[int]]:
        if syndrome in self._syndrome_cache:
            return self._syndrome_cache[syndrome]

        n = 24

        e = [0] * n
        if self.compute_syndrome(e) == syndrome:
            self._syndrome_cache[syndrome] = e
            return e

        for i in range(n):
            e = [0] * n
            e[i] = 1
            if self.compute_syndrome(e) == syndrome:
                self._syndrome_cache[syndrome] = e
                return e

        for i in range(n):
            for j in range(i + 1, n):
                e = [0] * n
                e[i] = 1
                e[j] = 1
                if self.compute_syndrome(e) == syndrome:
                    self._syndrome_cache[syndrome] = e
                    return e

        if max_weight >= 3:
            for i in range(n):
                for j in range(i + 1, n):
                    for k in range(j + 1, n):
                        e = [0] * n
                        e[i] = 1
                        e[j] = 1
                        e[k] = 1
                        if self.compute_syndrome(e) == syndrome:
                            self._syndrome_cache[syndrome] = e
                            return e

        return None

    def encode(self, message: List[int]) -> List[int]:
        if len(message) != 12:
            raise ValueError("Message must be 12 bits")

        message_row = [message]
        codeword_row = matrix_multiply_binary(message_row, self.G_MATRIX)
        return codeword_row[0]

    def decode(self, received: List[int]) -> Tuple[List[int], int, bool]:
        if len(received) != 24:
            raise ValueError("Received word must be 24 bits")

        syndrome = self.compute_syndrome(received)
        error_pattern = self.find_error_pattern(syndrome)

        if error_pattern is None:
            return received[:12], -1, False

        corrected = [(r + e) % 2 for r, e in zip(received, error_pattern)]
        decoded_message = corrected[:12]
        num_errors = sum(error_pattern)

        return decoded_message, num_errors, True


@dataclass
class GolayCodeword:
    """Represents a Golay G₂₄ codeword."""
    bits: List[int]

    def __post_init__(self):
        if len(self.bits) != 24:
            raise ValueError("Golay codeword must be 24 bits")

    def hamming_weight(self) -> int:
        return sum(self.bits)

    def hamming_distance(self, other: 'GolayCodeword') -> int:
        return sum(1 for b1, b2 in zip(self.bits, other.bits) if b1 != b2)

    def __repr__(self) -> str:
        bit_str = ''.join(str(b) for b in self.bits)
        return f"GolayCodeword({bit_str[:12]}|{bit_str[12:]})"


# ============================================================================
# SECTION 3: LEECH LATTICE Λ₂₄ COHERENCE VALIDATION (Re-extracted)
# ============================================================================

@dataclass
class LeechLatticePoint:
    """
    A point in the Leech lattice Λ₂₄.
    Stored as 24-dimensional integer or half-integer vector.
    """
    coordinates: List[float]

    def __post_init__(self):
        if len(self.coordinates) != 24:
            raise ValueError(f"Leech lattice points must be 24-dimensional, got {len(self.coordinates)}")

        doubled = [2.0 * x for x in self.coordinates]
        if not all(abs(d - round(d)) < 1e-9 for d in doubled):
            raise ValueError("Coordinates must be integer or half-integer")

        coord_sum = sum(self.coordinates)
        if abs(coord_sum - round(coord_sum)) > 1e-9:
            raise ValueError("Sum of coordinates must be integer")
        if int(round(coord_sum)) % 2 != 0:
            raise ValueError("Sum of coordinates must be even")

        norm_sq = self.norm_squared
        if norm_sq == 2:
            raise ValueError("No norm²=2 vectors in Leech lattice")
        if norm_sq != 0 and norm_sq < 4:
            raise ValueError(f"Invalid norm²={norm_sq}. Leech minimum nonzero norm²=4")

    @property
    def norm_squared(self) -> int:
        return int(round(dot_product(self.coordinates, self.coordinates)))

    def __add__(self, other: 'LeechLatticePoint') -> 'LeechLatticePoint':
        return LeechLatticePoint(vector_add(self.coordinates, other.coordinates))

    def __sub__(self, other: 'LeechLatticePoint') -> 'LeechLatticePoint':
        return LeechLatticePoint(vector_subtract(self.coordinates, other.coordinates))

    def __mul__(self, scalar: Union[int, float]) -> 'LeechLatticePoint':
        return LeechLatticePoint(scalar_vector_multiply(float(scalar), self.coordinates))

    def __repr__(self):
        return f"LeechLatticePoint(norm²={self.norm_squared}, coords={self.coordinates[:4]}...)"


class LeechLattice:
    """
    The Leech lattice Λ₂₄ - 24-dimensional even unimodular lattice.
    """

    def __init__(self):
        self._basis = self._generate_basis()

    def _generate_basis(self) -> List[List[float]]:
        basis = [[0.0 for _ in range(24)] for _ in range(24)]

        for i in range(24):
            basis[i][i] = 2.0

        for i in range(23):
            basis[i][i + 1] = -1.0
            basis[i + 1][i] = -1.0

        basis[0][23] = -1.0
        basis[23][0] = -1.0

        return basis

    @property
    def basis(self) -> List[List[float]]:
        return [row[:] for row in self._basis]

    @property
    def dimension(self) -> int:
        return 24

    def point_from_coordinates(self, coords: List[float]) -> LeechLatticePoint:
        if len(coords) != 24:
            raise ValueError(f"Coordinates must be 24-dimensional, got {len(coords)}")
        return LeechLatticePoint(list(coords))

    def zero_point(self) -> LeechLatticePoint:
        return LeechLatticePoint([0.0] * 24)

    def nearest_lattice_point(self, vector: List[float]) -> LeechLatticePoint:
        if len(vector) != 24:
            raise ValueError(f"Vector must be 24-dimensional, got {len(vector)}")

        basis_transpose = get_matrix_transpose(self._basis)
        basis_coords = solve_linear_system(basis_transpose, vector)

        rounded = [round(x) for x in basis_coords]

        lattice_coords = matrix_vector_multiply(get_matrix_transpose(self._basis), rounded)

        return LeechLatticePoint(lattice_coords)

    def distance_to_lattice(self, vector: List[float]) -> float:
        nearest = self.nearest_lattice_point(vector)
        diff = vector_subtract(vector, nearest.coordinates)
        return euclidean_norm(diff)

    def generate_shell(self, norm_squared: int, max_points: int = 1000) -> List[LeechLatticePoint]:
        points = []

        if norm_squared == 4:
            for i in range(24):
                for sign in [1.0, -1.0]:
                    coords = [0.0] * 24
                    coords[i] = sign * 2.0
                    points.append(LeechLatticePoint(coords))
                    if len(points) >= max_points:
                        return points

            for i in range(23):
                for j in range(i + 1, 24):
                    for signs in [(1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)]:
                        coords = [0.0] * 24
                        coords[i] = signs[0]
                        coords[j] = signs[1]
                        if dot_product(coords, coords) == norm_squared:
                            try:
                                test_point = LeechLatticePoint(coords)
                                if test_point.norm_squared == norm_squared:
                                    points.append(test_point)
                                    if len(points) >= max_points:
                                        return points
                            except ValueError:
                                pass

        return points

    @property
    def kissing_number(self) -> int:
        return 196560

    def is_in_lattice(self, point: LeechLatticePoint) -> bool:
        if len(point.coordinates) != 24:
            return False

        twice_coords = [2.0 * x for x in point.coordinates]
        if not all(abs(d - round(d)) < 1e-9 for d in twice_coords):
            return False

        coord_sum = sum(point.coordinates)
        if abs(coord_sum - round(coord_sum)) > 1e-9:
            return False
        if int(round(coord_sum)) % 2 != 0:
            return False

        return True

    def __repr__(self):
        return f"LeechLattice(dim=24, kissing_number=196560, min_norm=4)"


# ============================================================================
# SECTION 4: GOLAY ↔ LEECH CONSTRUCTION A BRIDGE (Re-extracted)
# ============================================================================

def golay_to_leech(golay_codeword: List[int]) -> LeechLatticePoint:
    """
    Convert Golay G₂₄ codeword to Leech lattice point via Construction A.
    """
    if len(golay_codeword) != 24:
        raise ValueError(f"Golay codeword must be 24-dimensional, got {len(golay_codeword)}")

    signed = [2.0 * bit - 1.0 for bit in golay_codeword]

    return LeechLatticePoint(signed)


def leech_to_golay(lattice_point: LeechLatticePoint) -> Optional[List[int]]:
    """
    Convert Leech lattice point back to Golay codeword if possible.
    """
    coords = lattice_point.coordinates

    if not all(abs(abs(x) - 1.0) < 1e-9 for x in coords):
        return None

    binary = [int(round((x + 1.0) / 2.0)) for x in coords]

    return binary


# ============================================================================
# SECTION 5: UBP GEOMETRIC FOUNDATION (Re-extracted)
# ============================================================================

class UBPGeometricState:
    """
    Represents a UBP geometric state in 24 dimensions.
    """

    def __init__(self, bits: List[int], lattice: LeechLattice):
        if len(bits) != 24:
            raise ValueError("UBP state must be 24 bits")

        self.bits = bits
        self.lattice = lattice

        self.leech_point = golay_to_leech(bits)

        if not lattice.is_in_lattice(self.leech_point):
            raise ValueError("State does not maintain Leech lattice coherence")

    def hamming_weight(self) -> int:
        return sum(self.bits)

    def to_golay_codeword(self) -> GolayCodeword:
        return GolayCodeword(self.bits)

    def to_leech_point(self) -> LeechLatticePoint:
        return self.leech_point

    def verify_coherence(self) -> bool:
        return self.lattice.is_in_lattice(self.leech_point)

    def __repr__(self):
        bit_str = ''.join(str(b) for b in self.bits)
        return f"UBPGeometricState({bit_str}, weight={self.hamming_weight()}, coherent={self.verify_coherence()})"


# ============================================================================
# SECTION 7: BIDIRECTIONAL DATA FLOW (Re-extracted)
# ============================================================================

class DataEncoder:
    """
    Encode observable data into UBP geometric states.
    """

    @staticmethod
    def blood_type_to_ubp(blood_type: str) -> List[int]:
        blood_type = blood_type.upper().strip()

        if blood_type.startswith("AB"):
            abo_bits = [1, 1]
            rh_part = blood_type[2:]
        elif blood_type.startswith("A"):
            abo_bits = [0, 1]
            rh_part = blood_type[1:]
        elif blood_type.startswith("B"):
            abo_bits = [1, 0]
            rh_part = blood_type[1:]
        elif blood_type.startswith("O"):
            abo_bits = [0, 0]
            rh_part = blood_type[1:]
        else:
            raise ValueError(f"Invalid blood type: {blood_type}")

        rh_bit = 1 if "+" in rh_part else 0

        bits = [0] * 24
        bits[0:2] = abo_bits
        bits[2] = rh_bit

        for i in range(3, 24):
            bits[i] = (i + sum(bits[:3])) % 2

        return bits

    @staticmethod
    def ubp_to_blood_type(bits: List[int]) -> str:
        if len(bits) != 24:
            raise ValueError("UBP state must be 24 bits")

        abo_bits = bits[0:2]
        if abo_bits == [0, 0]:
            abo = "O"
        elif abo_bits == [0, 1]:
            abo = "A"
        elif abo_bits == [1, 0]:
            abo = "B"
        elif abo_bits == [1, 1]:
            abo = "AB"
        else:
            abo = "?"

        rh = "+" if bits[2] == 1 else "-"

        return f"{abo}{rh}"
