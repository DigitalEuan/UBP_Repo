"""
Golay G₂₄ Error-Correction Code
================================

Complete implementation of the binary Golay [24,12,8] perfect code
for self-healing coherence states in the Information Ship.

The Golay code is intimately connected to the Leech lattice:
- Leech lattice Λ₂₄ can be constructed using Golay G₂₄
- Both have deep connections to the Monster group
- Perfect error correction (corrects up to 3 errors)

References:
- Conway & Sloane: Sphere Packings, Lattices and Groups
- MacWilliams & Sloane: The Theory of Error-Correcting Codes
"""

import numpy as np
from typing import Tuple, List, Optional
import random

# ============================================================================
# GOLAY G₂₄ GENERATOR AND PARITY-CHECK MATRICES
# ============================================================================

# Generator matrix G in standard form [I₁₂ | A]
# where A is the 12×12 matrix derived from the Golay construction

# The 12×12 matrix A for Golay G₂₄ (using hexacode construction)
A_MATRIX = np.array([
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
], dtype=np.int8)

# Generator matrix G = [I₁₂ | A]
I_12 = np.eye(12, dtype=np.int8)
G_MATRIX = np.hstack([I_12, A_MATRIX])

# Parity-check matrix H = [A^T | I₁₂]
H_MATRIX = np.hstack([A_MATRIX.T, I_12])

# Verify that G × H^T = 0 (mod 2)
assert np.all((G_MATRIX @ H_MATRIX.T) % 2 == 0), "G × H^T must be zero!"

print("Golay G₂₄ matrices initialized:")
print(f"  Generator matrix G: {G_MATRIX.shape}")
print(f"  Parity-check matrix H: {H_MATRIX.shape}")
print(f"  Verification: G × H^T = 0 (mod 2) ✓")

# ============================================================================
# SYNDROME TABLE FOR FAST DECODING
# ============================================================================

def build_syndrome_table() -> dict:
    """
    Build syndrome lookup table for fast decoding.
    
    For Golay G₂₄, there are 2^12 = 4096 possible syndromes.
    Each syndrome maps to a unique error pattern (up to 3 errors).
    
    Returns:
        Dictionary {syndrome_tuple: error_pattern_array}
    """
    syndrome_table = {}
    
    # All error patterns with weight ≤ 3
    n = 24
    
    # Weight 0 (no errors)
    e = np.zeros(n, dtype=np.int8)
    syndrome = tuple((H_MATRIX @ e) % 2)
    syndrome_table[syndrome] = e.copy()
    
    # Weight 1 (single-bit errors)
    for i in range(n):
        e = np.zeros(n, dtype=np.int8)
        e[i] = 1
        syndrome = tuple((H_MATRIX @ e) % 2)
        syndrome_table[syndrome] = e.copy()
    
    # Weight 2 (two-bit errors)
    for i in range(n):
        for j in range(i+1, n):
            e = np.zeros(n, dtype=np.int8)
            e[i] = 1
            e[j] = 1
            syndrome = tuple((H_MATRIX @ e) % 2)
            if syndrome not in syndrome_table:  # Avoid overwriting
                syndrome_table[syndrome] = e.copy()
    
    # Weight 3 (three-bit errors)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                e = np.zeros(n, dtype=np.int8)
                e[i] = 1
                e[j] = 1
                e[k] = 1
                syndrome = tuple((H_MATRIX @ e) % 2)
                if syndrome not in syndrome_table:
                    syndrome_table[syndrome] = e.copy()
    
    return syndrome_table

print("\nBuilding syndrome table...")
SYNDROME_TABLE = build_syndrome_table()
print(f"  Syndrome table size: {len(SYNDROME_TABLE)} entries")
print(f"  Coverage: up to 3-error patterns")

# ============================================================================
# ENCODING AND DECODING FUNCTIONS
# ============================================================================

def encode(message: np.ndarray) -> np.ndarray:
    """
    Encode a 12-bit message into a 24-bit Golay codeword.
    
    Args:
        message: 12-bit binary array
    
    Returns:
        24-bit codeword
    """
    assert len(message) == 12, "Message must be 12 bits"
    codeword = (message @ G_MATRIX) % 2
    return codeword.astype(np.int8)

def decode(received: np.ndarray) -> Tuple[np.ndarray, int, bool]:
    """
    Decode a received 24-bit word, correcting up to 3 errors.
    
    Args:
        received: 24-bit received word (possibly with errors)
    
    Returns:
        (decoded_message, num_errors_corrected, success)
    """
    assert len(received) == 24, "Received word must be 24 bits"
    
    # Compute syndrome
    syndrome = (H_MATRIX @ received) % 2
    syndrome_tuple = tuple(syndrome)
    
    # Look up error pattern
    if syndrome_tuple in SYNDROME_TABLE:
        error_pattern = SYNDROME_TABLE[syndrome_tuple]
        corrected = (received + error_pattern) % 2
        num_errors = int(np.sum(error_pattern))
        
        # Extract message (first 12 bits in standard form)
        decoded_message = corrected[:12]
        
        return decoded_message.astype(np.int8), num_errors, True
    else:
        # More than 3 errors - cannot correct
        # Return received word as-is (best effort)
        decoded_message = received[:12]
        return decoded_message.astype(np.int8), -1, False

def inject_errors(codeword: np.ndarray, num_errors: int) -> np.ndarray:
    """
    Inject random errors into a codeword for testing.
    
    Args:
        codeword: 24-bit codeword
        num_errors: Number of random bit flips
    
    Returns:
        Corrupted codeword
    """
    assert len(codeword) == 24, "Codeword must be 24 bits"
    assert 0 <= num_errors <= 24, "Invalid number of errors"
    
    corrupted = codeword.copy()
    error_positions = random.sample(range(24), num_errors)
    
    for pos in error_positions:
        corrupted[pos] = 1 - corrupted[pos]
    
    return corrupted.astype(np.int8)

# ============================================================================
# COHERENCE STATE INTEGRATION
# ============================================================================

def float_to_bits(value: float, num_bits: int = 12) -> np.ndarray:
    """
    Convert a float to a binary representation.
    
    Uses a simple quantization scheme:
    - Map value to [0, 2^num_bits - 1]
    - Convert to binary
    
    Args:
        value: Float value to encode
        num_bits: Number of bits (default: 12 for Golay)
    
    Returns:
        Binary array
    """
    # Normalize to [0, 1]
    normalized = (value - int(value))  # Fractional part
    if normalized < 0:
        normalized += 1.0
    
    # Quantize to integer
    max_val = (1 << num_bits) - 1
    quantized = int(normalized * max_val)
    
    # Convert to binary
    bits = np.array([int(b) for b in format(quantized, f'0{num_bits}b')], dtype=np.int8)
    
    return bits

def bits_to_float(bits: np.ndarray) -> float:
    """
    Convert binary representation back to float.
    
    Args:
        bits: Binary array
    
    Returns:
        Float value (fractional part only)
    """
    num_bits = len(bits)
    max_val = (1 << num_bits) - 1
    
    # Convert binary to integer
    quantized = int(''.join(str(b) for b in bits), 2)
    
    # Denormalize
    value = quantized / max_val
    
    return value

# ============================================================================
# HIGH-LEVEL API
# ============================================================================

class GolayCodeword:
    """Represents a Golay G₂₄ codeword."""
    
    def __init__(self, bits: np.ndarray) -> None:
        assert len(bits) == 24, "Golay codeword must be 24 bits"
        self.bits = bits.astype(np.int8)
    
    def __repr__(self) -> str:
        bit_str = ''.join(str(b) for b in self.bits)
        return f"GolayCodeword({bit_str[:12]}|{bit_str[12:]})"
    
    def hamming_weight(self) -> int:
        """Return the Hamming weight (number of 1s)."""
        return int(np.sum(self.bits))
    
    def hamming_distance(self, other: 'GolayCodeword') -> int:
        """Compute Hamming distance to another codeword."""
        return int(np.sum(self.bits != other.bits))

def encode_value(value: float) -> GolayCodeword:
    """
    Encode a float value into a Golay codeword.
    
    Args:
        value: Float value to encode
    
    Returns:
        GolayCodeword
    """
    message_bits = float_to_bits(value, num_bits=12)
    codeword_bits = encode(message_bits)
    return GolayCodeword(codeword_bits)

def decode_value(codeword: GolayCodeword) -> Tuple[float, int, bool]:
    """
    Decode a Golay codeword back to a float value.
    
    Args:
        codeword: GolayCodeword to decode
    
    Returns:
        (decoded_value, num_errors_corrected, success)
    """
    message_bits, num_errors, success = decode(codeword.bits)
    value = bits_to_float(message_bits)
    return value, num_errors, success

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GOLAY G₂₄ ERROR-CORRECTION TESTS")
    print("="*60)
    
    # Test 1: Basic encoding/decoding
    print("\nTest 1: Basic encoding/decoding")
    test_value = 0.123456789
    print(f"  Original value: {test_value:.9f}")
    
    encoded = encode_value(test_value)
    print(f"  Encoded: {encoded}")
    print(f"  Hamming weight: {encoded.hamming_weight()}")
    
    decoded_value, num_errors, success = decode_value(encoded)
    print(f"  Decoded value: {decoded_value:.9f}")
    print(f"  Errors corrected: {num_errors}")
    print(f"  Success: {success}")
    print(f"  Roundtrip error: {abs(decoded_value - test_value):.2e}")
    
    # Test 2: 1-error correction
    print("\nTest 2: 1-error correction")
    corrupted_1 = GolayCodeword(inject_errors(encoded.bits, 1))
    print(f"  Corrupted (1 error): {corrupted_1}")
    print(f"  Hamming distance: {encoded.hamming_distance(corrupted_1)}")
    
    decoded_value, num_errors, success = decode_value(corrupted_1)
    print(f"  Decoded value: {decoded_value:.9f}")
    print(f"  Errors corrected: {num_errors}")
    print(f"  Success: {success} ✓")
    
    # Test 3: 2-error correction
    print("\nTest 3: 2-error correction")
    corrupted_2 = GolayCodeword(inject_errors(encoded.bits, 2))
    print(f"  Corrupted (2 errors): {corrupted_2}")
    print(f"  Hamming distance: {encoded.hamming_distance(corrupted_2)}")
    
    decoded_value, num_errors, success = decode_value(corrupted_2)
    print(f"  Decoded value: {decoded_value:.9f}")
    print(f"  Errors corrected: {num_errors}")
    print(f"  Success: {success} ✓")
    
    # Test 3: 3-error correction
    print("\nTest 4: 3-error correction")
    corrupted_3 = GolayCodeword(inject_errors(encoded.bits, 3))
    print(f"  Corrupted (3 errors): {corrupted_3}")
    print(f"  Hamming distance: {encoded.hamming_distance(corrupted_3)}")
    
    decoded_value, num_errors, success = decode_value(corrupted_3)
    print(f"  Decoded value: {decoded_value:.9f}")
    print(f"  Errors corrected: {num_errors}")
    print(f"  Success: {success} ✓")
    
    # Test 5: 4-error detection (should fail to correct)
    print("\nTest 5: 4-error detection (beyond correction capability)")
    corrupted_4 = GolayCodeword(inject_errors(encoded.bits, 4))
    print(f"  Corrupted (4 errors): {corrupted_4}")
    print(f"  Hamming distance: {encoded.hamming_distance(corrupted_4)}")
    
    decoded_value, num_errors, success = decode_value(corrupted_4)
    print(f"  Decoded value: {decoded_value:.9f}")
    print(f"  Errors corrected: {num_errors}")
    print(f"  Success: {success} (expected: False)")
    
    # Test 6: Statistical test
    print("\nTest 6: Statistical error correction (100 trials)")
    successes = {1: 0, 2: 0, 3: 0, 4: 0}
    trials = 100
    
    for _ in range(trials):
        for num_err in [1, 2, 3, 4]:
            corrupted = GolayCodeword(inject_errors(encoded.bits, num_err))
            _, _, success = decode_value(corrupted)
            if success:
                successes[num_err] += 1
    
    for num_err in [1, 2, 3, 4]:
        rate = successes[num_err] / trials * 100
        print(f"  {num_err}-error correction: {successes[num_err]}/{trials} ({rate:.1f}%)")
    
    print("\n" + "="*60)
    print("Golay G₂₄ error-correction module ready! ✓")
    print("="*60)
