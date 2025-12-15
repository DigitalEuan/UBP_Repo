# Cell 6 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
from typing import List, Tuple, Optional, Dict, Union
from dataclasses import dataclass
import random
from fractions import Fraction

# Re-extract relevant functions from the original cell
def identity_matrix(n: int) -> List[List[int]]:
    """Create n×n identity matrix."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def hstack_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Horizontally stack two matrices (side by side)."""
    if len(A) != len(B):
        raise ValueError("Matrices must have same number of rows")
    return [A[i] + B[i] for i in range(len(A))]

def get_matrix_transpose(M: List[List[int]]) -> List[List[int]]:
    """Transpose a matrix."""
    if not M:
        return []
    rows, cols = len(M), len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]

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


class GolaySpringMechanism:
    """
    The 'spring mechanism' - generates Golay syndromes on-demand geometrically.

    Instead of storing 2048 syndrome table entries, we compute them from
    the geometric structure of the Golay code. The geometry "springs" the
    correct syndrome into being when needed.
    """

    # The 12×12 matrix A for Golay G₂₄ (hexacode construction)
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
        """Initialize the spring mechanism."""
        self.I_12 = identity_matrix(12)
        self.G_MATRIX = hstack_matrices(self.I_12, self.A_MATRIX)
        self.H_MATRIX = hstack_matrices(get_matrix_transpose(self.A_MATRIX), self.I_12)

        # Verify G × H^T = 0 (mod 2)
        GHT = matrix_multiply_binary(self.G_MATRIX, get_matrix_transpose(self.H_MATRIX))
        zero_matrix = [[0] * 12 for _ in range(12)]
        assert are_matrices_equal_binary(GHT, zero_matrix), "G × H^T must be zero"

        # Cache for computed syndromes (lazy initialization)
        self._syndrome_cache = {}

    def compute_syndrome(self, received: List[int]) -> Tuple[int, ...]:
        """
        Compute syndrome for received word using the spring mechanism.

        The syndrome is computed geometrically from the parity-check matrix,
        not looked up from a table. This is the "spring" - the geometry
        generates the correct syndrome on demand.
        """
        if len(received) != 24:
            raise ValueError("Received word must be 24 bits")

        # Convert to column vector format for matrix multiplication
        received_col = [[bit] for bit in received]

        # Compute syndrome: s = H × r^T (mod 2)
        syndrome_col = matrix_multiply_binary(self.H_MATRIX, received_col)

        # Extract as tuple
        syndrome = tuple(row[0] for row in syndrome_col)

        return syndrome

    def find_error_pattern(self, syndrome: Tuple[int, ...], max_weight: int = 3) -> Optional[List[int]]:
        """
        Find error pattern for given syndrome using geometric spring mechanism.

        Instead of table lookup, we generate error patterns geometrically
        and check which one produces this syndrome.
        """
        if syndrome in self._syndrome_cache:
            return self._syndrome_cache[syndrome]

        n = 24

        # Weight 0 (no errors)
        e = [0] * n
        if self.compute_syndrome(e) == syndrome:
            self._syndrome_cache[syndrome] = e
            return e

        # Weight 1 (single-bit errors)
        for i in range(n):
            e = [0] * n
            e[i] = 1
            if self.compute_syndrome(e) == syndrome:
                self._syndrome_cache[syndrome] = e
                return e

        # Weight 2 (two-bit errors)
        for i in range(n):
            for j in range(i + 1, n):
                e = [0] * n
                e[i] = 1
                e[j] = 1
                if self.compute_syndrome(e) == syndrome:
                    self._syndrome_cache[syndrome] = e
                    return e

        # Weight 3 (three-bit errors)
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
        """Encode 12-bit message into 24-bit Golay codeword."""
        if len(message) != 12:
            raise ValueError("Message must be 12 bits")

        # c = m × G (mod 2)
        message_row = [message]
        codeword_row = matrix_multiply_binary(message_row, self.G_MATRIX)
        return codeword_row[0]

    def decode(self, received: List[int]) -> Tuple[List[int], int, bool]:
        """
        Decode received 24-bit word, correcting up to 3 errors.

        Returns: (decoded_message, num_errors_corrected, success)
        """
        if len(received) != 24:
            raise ValueError("Received word must be 24 bits")

        # Compute syndrome
        syndrome = self.compute_syndrome(received)

        # Find error pattern
        error_pattern = self.find_error_pattern(syndrome)

        if error_pattern is None:
            # Cannot correct - more than 3 errors
            return received[:12], -1, False

        # Correct the received word
        corrected = [(r + e) % 2 for r, e in zip(received, error_pattern)]

        # Extract message (first 12 bits in standard form)
        decoded_message = corrected[:12]
        num_errors = sum(error_pattern)

        return decoded_message, num_errors, True


# Instantiate the mechanism to get the matrices
golay_mechanism = GolaySpringMechanism()

print("A_MATRIX (12x12):")
for row in golay_mechanism.A_MATRIX:
    print(row)

print("\nG_MATRIX (12x24, [I_12 | A_MATRIX]):")
for row in golay_mechanism.G_MATRIX:
    print(row)
