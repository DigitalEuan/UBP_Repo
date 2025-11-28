#!/usr/bin/env python3
"""
UBP 3.7.1 - Golay(24,12) Error Correcting Code
=========================================================

REAL, CORRECT implementation of the extended binary Golay code G24.

The Golay(24,12) code is a perfect error-correcting code that:
- Encodes 12 data bits into 24 code bits
- Corrects up to 3 bit errors
- Detects up to 7 bit errors
- Has minimum distance 8

This implementation uses the CORRECT generator matrix based on the
extended Golay code construction from G23.

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

import numpy as np
from typing import Tuple, Optional


class GolayG24:
    """
    Binary Golay(24,12) error correcting code.
    
    This implementation uses the extended Golay construction.
    """
    
    def __init__(self):
        """Initialize the Golay code with the correct generator matrix."""
        self.n = 24  # Code length
        self.k = 12  # Message length
        self.d = 8   # Minimum distance
        self.t = 3   # Error correction capability
        
        # Build the CORRECT generator matrix
        self.G = self._build_correct_generator_matrix()
        
        # Build the parity-check matrix
        self.H = self._build_parity_check_matrix()
        
        # Build syndrome lookup table for fast decoding
        self.syndrome_table = self._build_syndrome_table()
    
    def _build_correct_generator_matrix(self) -> np.ndarray:
        """
        Build the CORRECT generator matrix for Golay(24,12).
        
        Uses the extended Golay code construction.
        The generator matrix is constructed from the Golay(23,12) code
        by adding an overall parity bit.
        
        Returns:
            12×24 generator matrix with minimum distance 8
        """
        # The correct Golay(24,12) generator matrix in systematic form [I | P]
        # This is based on the standard construction that guarantees d=8
        
        # Identity part
        I = np.eye(12, dtype=int)
        
        # Parity part - this is the CORRECT matrix for Golay(24,12)
        # Based on the quadratic residue construction
        P = np.array([
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ], dtype=int)
        
        # Concatenate [I | P]
        G = np.hstack([I, P])
        
        return G
    
    def _build_parity_check_matrix(self) -> np.ndarray:
        """
        Build the parity-check matrix for Golay(24,12).
        
        H = [P^T | I_12]
        
        Returns:
            12×24 parity-check matrix
        """
        # Extract P from G
        P = self.G[:, 12:]
        
        # Identity matrix
        I = np.eye(12, dtype=int)
        
        # Concatenate [P^T | I]
        H = np.hstack([P.T, I])
        
        return H
    
    def _compute_syndrome(self, received: np.ndarray) -> np.ndarray:
        """
        Compute syndrome S = H * r^T (mod 2).
        
        Args:
            received: 24-bit received vector
        
        Returns:
            12-bit syndrome vector
        """
        syndrome = (self.H @ received) % 2
        return syndrome
    
    def _build_syndrome_table(self) -> dict:
        """
        Build COMPLETE syndrome lookup table for ALL correctable error patterns.
        
        For Golay(24,12), this includes:
        - 1 pattern with 0 errors
        - 24 patterns with 1 error
        - C(24,2) = 276 patterns with 2 errors
        - C(24,3) = 2024 patterns with 3 errors
        Total: 2325 patterns
        
        Returns:
            Dictionary mapping syndrome (as tuple) to error pattern
        """
        syndrome_table = {}
        
        # No error
        zero_error = np.zeros(24, dtype=int)
        syndrome = self._compute_syndrome(zero_error)
        syndrome_table[tuple(syndrome)] = zero_error
        
        # Single-bit errors (24 patterns)
        for i in range(24):
            error = np.zeros(24, dtype=int)
            error[i] = 1
            syndrome = self._compute_syndrome(error)
            syndrome_table[tuple(syndrome)] = error.copy()
        
        # Two-bit errors (276 patterns)
        for i in range(24):
            for j in range(i + 1, 24):
                error = np.zeros(24, dtype=int)
                error[i] = 1
                error[j] = 1
                syndrome = self._compute_syndrome(error)
                syndrome_table[tuple(syndrome)] = error.copy()
        
        # Three-bit errors (2024 patterns)
        for i in range(24):
            for j in range(i + 1, 24):
                for k in range(j + 1, 24):
                    error = np.zeros(24, dtype=int)
                    error[i] = 1
                    error[j] = 1
                    error[k] = 1
                    syndrome = self._compute_syndrome(error)
                    syndrome_table[tuple(syndrome)] = error.copy()
        
        return syndrome_table
    
    def encode(self, message: np.ndarray) -> np.ndarray:
        """
        Encode a 12-bit message into a 24-bit codeword.
        
        c = m * G (mod 2)
        
        Args:
            message: 12-bit message vector
        
        Returns:
            24-bit codeword
        """
        if len(message) != self.k:
            raise ValueError(f"Message must be {self.k} bits, got {len(message)}")
        
        # Ensure binary
        message = np.array(message, dtype=int) % 2
        
        # Encode: c = m * G (mod 2)
        codeword = (message @ self.G) % 2
        
        return codeword
    
    def correct_errors(self, received: np.ndarray) -> np.ndarray:
        """
        Correct errors in a received 24-bit vector.
        
        Uses syndrome decoding to identify and correct up to 3 bit errors.
        
        Args:
            received: 24-bit received vector (possibly corrupted)
        
        Returns:
            24-bit corrected codeword
        """
        if len(received) != self.n:
            raise ValueError(f"Received vector must be {self.n} bits, got {len(received)}")
        
        # Ensure binary
        received = np.array(received, dtype=int) % 2
        
        # Compute syndrome
        syndrome = self._compute_syndrome(received)
        
        # Look up error pattern
        syndrome_key = tuple(syndrome)
        
        if syndrome_key in self.syndrome_table:
            error_pattern = self.syndrome_table[syndrome_key]
            # Correct the error
            corrected = (received + error_pattern) % 2
            return corrected
        else:
            # More than 3 errors - cannot correct
            # Return received vector unchanged
            return received
    
    def decode(self, codeword: np.ndarray) -> np.ndarray:
        """
        Decode a 24-bit codeword to extract the 12-bit message.
        
        Args:
            codeword: 24-bit codeword
        
        Returns:
            12-bit message
        """
        if len(codeword) != self.n:
            raise ValueError(f"Codeword must be {self.n} bits, got {len(codeword)}")
        
        # Ensure binary
        codeword = np.array(codeword, dtype=int) % 2
        
        # First 12 bits are the message (systematic encoding)
        message = codeword[:self.k]
        
        return message
    
    def detect_errors(self, received: np.ndarray) -> Tuple[bool, int]:
        """
        Detect if there are errors in a received vector.
        
        Args:
            received: 24-bit received vector
        
        Returns:
            (has_errors, estimated_error_count)
        """
        syndrome = self._compute_syndrome(received)
        
        # If syndrome is all zeros, no errors detected
        if np.all(syndrome == 0):
            return False, 0
        
        # Look up in syndrome table
        syndrome_key = tuple(syndrome)
        if syndrome_key in self.syndrome_table:
            error_pattern = self.syndrome_table[syndrome_key]
            error_count = np.sum(error_pattern)
            return True, error_count
        else:
            # More than 3 errors
            return True, -1  # Unknown number of errors
    
    def hamming_weight(self, vector: np.ndarray) -> int:
        """Compute Hamming weight (number of 1s)."""
        return int(np.sum(vector))
    
    def hamming_distance(self, v1: np.ndarray, v2: np.ndarray) -> int:
        """Compute Hamming distance between two vectors."""
        return self.hamming_weight((v1 + v2) % 2)
    
    def is_codeword(self, vector: np.ndarray) -> bool:
        """
        Check if a vector is a valid codeword.
        
        A vector is a codeword if H * v^T = 0 (mod 2).
        """
        syndrome = self._compute_syndrome(vector)
        return np.all(syndrome == 0)
    
    def __repr__(self):
        return f"GolayG24(n={self.n}, k={self.k}, d={self.d}, t={self.t})"


# ============================================================================
# VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("GOLAY(24,12) - CORRECTED IMPLEMENTATION")
    print("="*70)
    
    # Create Golay code
    golay = GolayG24()
    print(f"\n{golay}")
    print(f"Generator matrix shape: {golay.G.shape}")
    print(f"Parity-check matrix shape: {golay.H.shape}")
    print(f"Syndrome table size: {len(golay.syndrome_table)}")
    
    # Verify minimum distance
    print(f"\nVerifying minimum distance...")
    codewords = []
    for i in range(100):
        msg = np.random.randint(0, 2, 12)
        cw = golay.encode(msg)
        codewords.append(cw)
    
    min_dist = float('inf')
    for i in range(len(codewords)):
        for j in range(i+1, len(codewords)):
            dist = golay.hamming_distance(codewords[i], codewords[j])
            if dist > 0:
                min_dist = min(min_dist, dist)
    
    print(f"Minimum distance found: {min_dist}")
    print(f"Expected: {golay.d}")
    print(f"✓ CORRECT" if min_dist >= golay.d else "✗ WRONG")
    
    # Test error correction
    print(f"\nTesting error correction...")
    test_msg = np.array([1,0,1,0,1,0,1,0,1,0,1,0])
    test_cw = golay.encode(test_msg)
    
    for num_errors in [1, 2, 3]:
        success_count = 0
        trials = 50
        
        for _ in range(trials):
            corrupted = test_cw.copy()
            error_positions = np.random.choice(24, num_errors, replace=False)
            for pos in error_positions:
                corrupted[pos] = 1 - corrupted[pos]
            
            corrected = golay.correct_errors(corrupted)
            if np.array_equal(corrected, test_cw):
                success_count += 1
        
        print(f"  {num_errors}-bit errors: {success_count}/{trials} corrected ({100*success_count/trials:.0f}%)")
    
    print("="*70)
