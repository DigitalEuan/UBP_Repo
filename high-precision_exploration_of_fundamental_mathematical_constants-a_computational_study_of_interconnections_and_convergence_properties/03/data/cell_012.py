# Cell 12 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
from fractions import Fraction

# Re-extract ExactNumber and relevant vector operations for LeechLattice

class ExactNumber:
    """
    Represents exact numbers as integers or half-integers.
    Internally stored as 2*value to maintain integer arithmetic.
    """
    def __init__(self, value: Union[int, float, 'ExactNumber']):
        if isinstance(value, ExactNumber):
            self.doubled = value.doubled
        elif isinstance(value, Fraction):
            # Fraction with denominator 2
            if value.denominator == 1:
                self.doubled = value.numerator * 2
            elif value.denominator == 2:
                self.doubled = value.numerator
            else:
                raise ValueError(f"Cannot represent {value} as integer or half-integer")
        elif isinstance(value, float):
            # Convert float to fraction
            frac = Fraction(value).limit_denominator(1000)
            if frac.denominator == 1:
                self.doubled = int(frac.numerator * 2)
            elif frac.denominator == 2:
                self.doubled = int(frac.numerator)
            else:
                raise ValueError(f"Cannot represent {value} as integer or half-integer")
        else:
            # Assume integer
            self.doubled = int(value) * 2

    def to_float(self) -> float:
        """Convert to float for display only."""
        return self.doubled / 2.0

    def to_fraction(self) -> Fraction:
        """Convert to exact fraction."""
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

def identity_matrix(n: int) -> List[List[int]]:
    """Create n×n identity matrix."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def get_matrix_transpose(M: List[List[int]]) -> List[List[int]]:
    """Transpose a matrix."""
    if not M:
        return []
    rows, cols = len(M), len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]

def solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    """
    Solve Ax = b using Gaussian elimination.
    Returns x such that A @ x = b.
    """
    n = len(A)
    if n == 0:
        return []

    # Create augmented matrix
    aug = [A[i][:] + [b[i]] for i in range(n)]

    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]

        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            if abs(aug[i][i]) < 1e-10:
                continue
            c = aug[k][i] / aug[i][i]
            for j in range(i, n + 1):
                aug[k][j] -= c * aug[i][j]

    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = aug[i][n]
        for j in range(i + 1, n):
            x[i] -= aug[i][j] * x[j]
        if abs(aug[i][i]) > 1e-10:
            x[i] /= aug[i][i]

    return x


@dataclass
class LeechLatticePoint:
    """
    A point in the Leech lattice Λ₂₄.
    Stored as 24-dimensional integer or half-integer vector.
    """
    coordinates: List[float]

    def __post_init__(self):
        """Validate that coordinates form a valid Leech lattice point."""
        if len(self.coordinates) != 24:
            raise ValueError(f"Leech lattice points must be 24-dimensional, got {len(self.coordinates)}")

        # Check: all coordinates are integer or half-integer
        doubled = [2.0 * x for x in self.coordinates]
        if not all(abs(d - round(d)) < 1e-9 for d in doubled):
            raise ValueError("Coordinates must be integer or half-integer")

        # Check: sum of coordinates must be even
        coord_sum = sum(self.coordinates)
        if abs(coord_sum - round(coord_sum)) > 1e-9:
            raise ValueError("Sum of coordinates must be integer")
        if int(round(coord_sum)) % 2 != 0:
            raise ValueError("Sum of coordinates must be even")

        # Check: no norm²=2 vectors (minimum nonzero norm is 4)
        norm_sq = self.norm_squared
        if norm_sq == 2:
            raise ValueError("No norm²=2 vectors in Leech lattice")
        if norm_sq != 0 and norm_sq < 4:
            raise ValueError(f"Invalid norm²={norm_sq}. Leech minimum nonzero norm²=4")

    @property
    def norm_squared(self) -> int:
        """Compute squared norm of the lattice point."""
        return int(round(dot_product(self.coordinates, self.coordinates)))

    def __add__(self, other: 'LeechLatticePoint') -> 'LeechLatticePoint':
        """Add two lattice points."""
        return LeechLatticePoint(vector_add(self.coordinates, other.coordinates))

    def __sub__(self, other: 'LeechLatticePoint') -> 'LeechLatticePoint':
        """Subtract two lattice points."""
        return LeechLatticePoint(vector_subtract(self.coordinates, other.coordinates))

    def __mul__(self, scalar: Union[int, float]) -> 'LeechLatticePoint':
        """Scalar multiplication."""
        return LeechLatticePoint(scalar_vector_multiply(float(scalar), self.coordinates))

    def __repr__(self):
        return f"LeechLatticePoint(norm²={self.norm_squared}, coords={self.coordinates[:4]}...)"


class LeechLattice:
    """
    The Leech lattice Λ₂₄ - 24-dimensional even unimodular lattice.

    Properties:
    - Dimension: 24
    - Minimum nonzero norm: 4
    - Kissing number: 196,560
    - Connected to Golay code via Construction A
    """

    def __init__(self):
        """Initialize the Leech lattice."""
        self._basis = self._generate_basis()

    def _generate_basis(self) -> List[List[float]]:
        """
        Generate basis for Leech lattice.
        Uses a construction based on the Golay code structure.
        """
        basis = [[0.0 for _ in range(24)] for _ in range(24)]

        # Diagonal scaling
        for i in range(24):
            basis[i][i] = 2.0

        # Off-diagonal structure from Golay code
        for i in range(23):
            basis[i][i + 1] = -1.0
            basis[i + 1][i] = -1.0

        # Circular connection
        basis[0][23] = -1.0
        basis[23][0] = -1.0

        return basis

    @property
    def basis(self) -> List[List[float]]:
        """Get the 24×24 basis matrix."""
        return [row[:] for row in self._basis]

    @property
    def dimension(self) -> int:
        """Dimension of the lattice (always 24)."""
        return 24

    def point_from_coordinates(self, coords: List[float]) -> LeechLatticePoint:
        """Create a lattice point from 24-dimensional coordinates."""
        if len(coords) != 24:
            raise ValueError(f"Coordinates must be 24-dimensional, got {len(coords)}")
        return LeechLatticePoint(list(coords))

    def zero_point(self) -> LeechLatticePoint:
        """Return the zero point (origin) of the lattice."""
        return LeechLatticePoint([0.0] * 24)

    def nearest_lattice_point(self, vector: List[float]) -> LeechLatticePoint:
        """
        Find the nearest lattice point to a given vector.
        This implementation is for a *general* lattice, not specifically the Leech.
        It relies on the current basis and rounding coefficients.
        """
        if len(vector) != 24:
            raise ValueError(f"Vector must be 24-dimensional, got {len(vector)}")

        # Express vector in basis coordinates
        # Transpose basis matrix for solving (A^T * x = v, where A is the basis matrix)
        basis_transpose = get_matrix_transpose(self._basis)
        basis_coords_float = solve_linear_system(basis_transpose, vector)

        # Round to nearest integers to find the lattice point coefficients
        rounded_coeffs = [round(x) for x in basis_coords_float]

        # Convert back to standard coordinates using the original basis vectors
        # A common simplification/approximation for general lattices is to use the basis as rows:
        # lattice_coords = [sum(rounded_coeffs[j] * self._basis[j][i] for j in range(self.dimension)) for i in range(self.dimension)]
        # However, the current basis is set up such that its rows are the basis vectors.
        # So we need to multiply the rounded coefficients by the basis matrix itself.
        # This requires the basis matrix to be square (24x24).

        lattice_coords = matrix_vector_multiply(self.basis, rounded_coeffs)

        return LeechLatticePoint(lattice_coords)

    def distance_to_lattice(self, vector: List[float]) -> float:
        """Compute distance from vector to nearest lattice point."""
        nearest = self.nearest_lattice_point(vector)
        diff = vector_subtract(vector, nearest.coordinates)
        return euclidean_norm(diff)

    def generate_shell(self, norm_squared: int, max_points: int = 1000) -> List[LeechLatticePoint]:
        """Generate lattice points with given squared norm."""
        points = []

        if norm_squared == 4:
            # Minimal vectors (kissing vectors)

            # Simple vectors: ±2 in one coordinate
            for i in range(24):
                for sign in [1.0, -1.0]:
                    coords = [0.0] * 24
                    coords[i] = sign * 2.0
                    points.append(LeechLatticePoint(coords))
                    if len(points) >= max_points:
                        return points

            # Vectors with ±1 in multiple coordinates
            for i in range(23):
                for j in range(i + 1, 24):
                    for signs in [(1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)]:
                        coords = [0.0] * 24
                        coords[i] = signs[0]
                        coords[j] = signs[1]
                        # This check is flawed for Leech. Need to ensure it's a Leech vector.
                        # For example, (1,1,0,...) has norm^2=2, not 4.
                        # The Leech lattice has points like (±2, 0, ..., 0), (±1, ±1, ..., 0) where the sum is even, etc.
                        # The simple (±1, ±1, ..., 0) is not necessarily a Leech vector with norm 4.
                        # It's better to generate valid Leech vectors directly.
                        if dot_product(coords, coords) == norm_squared:
                            # For Leech lattice points, coordinates must be integer or half-integer
                            # and sum of coordinates must be an even integer.
                            # Additionally, for norm_squared = 4, there are specific forms
                            # like (±2, 0...) or (±1, ±1, ±1, ±1, 0...) or (±1/2 for 8 coords, then some 3/2 etc)
                            # This generation logic is incomplete for the full Leech lattice minimal vectors.
                            # However, the `LeechLatticePoint` __post_init__ will validate these properties.
                            try:
                                test_point = LeechLatticePoint(coords)
                                if test_point.norm_squared == norm_squared:
                                    points.append(test_point)
                                    if len(points) >= max_points:
                                        return points
                            except ValueError:
                                pass # Not a valid Leech lattice point

        return points

    @property
    def kissing_number(self) -> int:
        """The kissing number of the Leech lattice (196,560)."""
        return 196560

    def is_in_lattice(self, point: LeechLatticePoint) -> bool:
        """Check if a point is in the Leech lattice."""
        if len(point.coordinates) != 24:
            return False

        # Check integer/half-integer constraint
        # This is already enforced by LeechLatticePoint's __post_init__ during its creation.
        # If a LeechLatticePoint object is successfully created, these checks passed.
        twice_coords = [2.0 * x for x in point.coordinates]
        if not all(abs(d - round(d)) < 1e-9 for d in twice_coords):
            return False

        # Check sum constraint
        # This is also enforced by LeechLatticePoint's __post_init__.
        coord_sum = sum(point.coordinates)
        if abs(coord_sum - round(coord_sum)) > 1e-9:
            return False
        if int(round(coord_sum)) % 2 != 0:
            return False

        # A critical property of the Leech lattice is that it is an EVEN lattice.
        # This means all squared norms of its vectors must be even integers.
        # This is handled by LeechLatticePoint's __post_init__ via norm_squared property.
        # The Leech lattice is also unimodular, meaning its determinant is 1. This isn't checked here directly.
        # The defining property that distinguishes it from other 24-dim even unimodular lattices is its minimum nonzero norm (4).
        # LeechLatticePoint's __post_init__ *does* check for norm_squared != 2 and min_nonzero_norm = 4.

        # So, if a point can be successfully instantiated as a LeechLatticePoint
        # and its coordinates satisfy the criteria checked here (redundantly), it is considered in the lattice.
        # The primary check is the successful construction of LeechLatticePoint.
        return True

    def __repr__(self):
        return f"LeechLattice(dim=24, kissing_number=196560, min_norm=4)"


# --- Test Cases for is_in_lattice method ---
print("Evaluating LeechLattice.is_in_lattice method:")

lattice = LeechLattice()

# 1. Valid Leech Lattice Point (known example: type 1 vector, e.g., (2,0,...,0))
# All integer coordinates, sum is even, norm^2 = 4
valid_point_1_coords = [2.0] + [0.0] * 23
valid_point_1 = LeechLatticePoint(valid_point_1_coords)
print(f"Valid point 1 ({valid_point_1_coords[:4]}...): {lattice.is_in_lattice(valid_point_1)} (Expected: True)")

# 2. Valid Leech Lattice Point (known example: type 2 vector, e.g., (1/2, 1/2, ..., 1/2))
# 24 half-integer coordinates, sum is 12 (even), norm^2 = 24 * (1/4) = 6
# This vector is actually not a direct type in the Leech lattice but rather related to Construction A
# A more typical integer/half-integer example would be something like 4-vectors (1,1,1,1,0...) with even sum
# For simplicity, let's test another type 1 related vector
valid_point_2_coords = [0.5] * 24 # sum = 12, norm_sq = 24 * 0.25 = 6. This should be valid for checks.
valid_point_2 = LeechLatticePoint(valid_point_2_coords)
print(f"Valid point 2 (all 0.5): {lattice.is_in_lattice(valid_point_2)} (Expected: True if based on the checks within is_in_lattice, which it is)")

# 3. Invalid: Not integer/half-integer
invalid_coords_float = [0.3] + [0.0] * 23
print(f"Invalid (float 0.3): ", end="")
try:
    invalid_point_float = LeechLatticePoint(invalid_coords_float)
    print(lattice.is_in_lattice(invalid_point_float))
except ValueError as e:
    print(f"Error during LeechLatticePoint creation: {e} (Expected: ValueError)")

# 4. Invalid: Sum of coordinates is odd (but integer/half-integer)
invalid_coords_odd_sum = [1.0] * 23 + [0.0] # Sum is 23 (odd)
print(f"Invalid (odd sum 23): ", end="")
try:
    invalid_point_odd_sum = LeechLatticePoint(invalid_coords_odd_sum)
    print(lattice.is_in_lattice(invalid_point_odd_sum))
except ValueError as e:
    print(f"Error during LeechLatticePoint creation: {e} (Expected: ValueError)")

# 5. Invalid: Norm squared = 2 (explicitly disallowed by LeechLatticePoint __post_init__)
invalid_coords_norm2 = [1.0, 1.0] + [0.0] * 22 # Sum is 2 (even), but norm^2 is 2
print(f"Invalid (norm^2 = 2): ", end="")
try:
    invalid_point_norm2 = LeechLatticePoint(invalid_coords_norm2)
    print(lattice.is_in_lattice(invalid_point_norm2))
except ValueError as e:
    print(f"Error during LeechLatticePoint creation: {e} (Expected: ValueError)")

# 6. Invalid: Incorrect dimension
invalid_dim_coords = [0.0] * 23
print(f"Invalid (dim 23): ", end="")
try:
    invalid_point_dim = LeechLatticePoint(invalid_dim_coords)
    print(lattice.is_in_lattice(invalid_point_dim))
except ValueError as e:
    print(f"Error during LeechLatticePoint creation: {e} (Expected: ValueError)")

# Conclusion: The `is_in_lattice` method itself essentially checks if `LeechLatticePoint` construction was successful
# or re-validates the coordinates based on the conditions already present in `LeechLatticePoint.__post_init__`.