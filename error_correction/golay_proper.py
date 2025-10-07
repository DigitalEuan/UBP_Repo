"""
Proper Golay[23,12] Error Correction Implementation

This module provides a mathematically correct implementation of the Golay[23,12]
error correction code based on the generator matrix construction using the
complement of the icosahedron adjacency matrix.

Author: Euan Craig, New Zealand
Date: 7 October 2025
"""

import numpy as np

class GolayCode:
    """
    Proper implementation of the Golay[23,12] error correction code.
    """
    
    def __init__(self):
        # Generator matrix G = [I | A] where I is 12x12 identity and A is complement of icosahedron adjacency
        self.I = np.eye(12, dtype=int)
        
        # Complement of icosahedron adjacency matrix (12x11)
        # This is the standard construction for Golay[23,12]
        self.A = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
        ], dtype=int)
        
        # Generator matrix [I | A]
        self.G = np.hstack([self.I, self.A])
        
        # Parity check matrix H = [A^T | I]
        self.H = np.hstack([self.A.T, np.eye(11, dtype=int)])
        
        # Precompute syndrome table for fast decoding
        self.syndrome_table = self._build_syndrome_table()
    
    def _build_syndrome_table(self):
        """Build syndrome lookup table for error patterns up to weight 3."""
        syndrome_table = {}
        
        # No error
        syndrome_table[tuple(np.zeros(11, dtype=int))] = np.zeros(23, dtype=int)
        
        # Single bit errors
        for i in range(23):
            error = np.zeros(23, dtype=int)
            error[i] = 1
            syndrome = self._compute_syndrome(error)
            syndrome_table[tuple(syndrome)] = error
        
        # Double bit errors
        for i in range(23):
            for j in range(i+1, 23):
                error = np.zeros(23, dtype=int)
                error[i] = 1
                error[j] = 1
                syndrome = self._compute_syndrome(error)
                syndrome_table[tuple(syndrome)] = error
        
        # Triple bit errors
        for i in range(23):
            for j in range(i+1, 23):
                for k in range(j+1, 23):
                    error = np.zeros(23, dtype=int)
                    error[i] = 1
                    error[j] = 1
                    error[k] = 1
                    syndrome = self._compute_syndrome(error)
                    syndrome_table[tuple(syndrome)] = error
        
        return syndrome_table
    
    def _compute_syndrome(self, received):
        """Compute syndrome for received codeword."""
        return np.dot(received, self.H.T) % 2
    
    def encode(self, message):
        """
        Encode a 12-bit message into a 23-bit codeword.
        
        Args:
            message: numpy array of 12 bits or list/string of 12 bits
            
        Returns:
            numpy array of 23 bits
        """
        if isinstance(message, str):
            message = np.array([int(b) for b in message], dtype=int)
        elif isinstance(message, list):
            message = np.array(message, dtype=int)
        
        if len(message) != 12:
            raise ValueError("Message must be 12 bits long")
        
        # Encode: c = m * G
        codeword = np.dot(message, self.G) % 2
        return codeword
    
    def decode(self, received):
        """
        Decode a received 23-bit word, correcting up to 3 errors.
        
        Args:
            received: numpy array of 23 bits or list/string of 23 bits
            
        Returns:
            tuple: (corrected_message, error_detected, error_corrected)
        """
        if isinstance(received, str):
            received = np.array([int(b) for b in received], dtype=int)
        elif isinstance(received, list):
            received = np.array(received, dtype=int)
        
        if len(received) != 23:
            raise ValueError("Received word must be 23 bits long")
        
        # Compute syndrome
        syndrome = self._compute_syndrome(received)
        syndrome_tuple = tuple(syndrome)
        
        # Look up error pattern
        if syndrome_tuple in self.syndrome_table:
            error_pattern = self.syndrome_table[syndrome_tuple]
            corrected = (received + error_pattern) % 2
            message = corrected[:12]  # Extract message bits
            
            error_detected = not np.array_equal(syndrome, np.zeros(11, dtype=int))
            error_corrected = error_detected
            
            return message, error_detected, error_corrected
        else:
            # More than 3 errors - uncorrectable
            message = received[:12]  # Return uncorrected message bits
            return message, True, False
    
    def get_distance(self):
        """Return the minimum distance of the code."""
        return 7
    
    def get_error_correction_capability(self):
        """Return the error correction capability."""
        return 3

def test_golay_code():
    """Test the Golay code implementation."""
    golay = GolayCode()
    
    print("Testing Golay[23,12] Code Implementation")
    print("=" * 50)
    
    # Test 1: Basic encoding/decoding
    message = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1], dtype=int)
    print(f"Original message: {message}")
    
    encoded = golay.encode(message)
    print(f"Encoded codeword: {encoded}")
    
    decoded, error_detected, error_corrected = golay.decode(encoded)
    print(f"Decoded message:  {decoded}")
    print(f"Error detected: {error_detected}, Error corrected: {error_corrected}")
    print(f"Decoding correct: {np.array_equal(message, decoded)}")
    print()
    
    # Test 2: Single error correction
    print("Testing single error correction:")
    corrupted = encoded.copy()
    corrupted[5] = 1 - corrupted[5]  # Flip bit 5
    print(f"Corrupted word:   {corrupted}")
    
    decoded, error_detected, error_corrected = golay.decode(corrupted)
    print(f"Decoded message:  {decoded}")
    print(f"Error detected: {error_detected}, Error corrected: {error_corrected}")
    print(f"Correction successful: {np.array_equal(message, decoded)}")
    print()
    
    # Test 3: Triple error correction
    print("Testing triple error correction:")
    corrupted = encoded.copy()
    corrupted[2] = 1 - corrupted[2]   # Flip bit 2
    corrupted[7] = 1 - corrupted[7]   # Flip bit 7
    corrupted[15] = 1 - corrupted[15] # Flip bit 15
    print(f"Corrupted word:   {corrupted}")
    
    decoded, error_detected, error_corrected = golay.decode(corrupted)
    print(f"Decoded message:  {decoded}")
    print(f"Error detected: {error_detected}, Error corrected: {error_corrected}")
    print(f"Correction successful: {np.array_equal(message, decoded)}")
    print()
    
    # Test 4: String input
    print("Testing string input:")
    message_str = "101100101101"
    encoded_str = golay.encode(message_str)
    decoded_str, _, _ = golay.decode(encoded_str)
    print(f"String message: {message_str}")
    print(f"Decoded back:   {''.join(map(str, decoded_str))}")
    print(f"String test successful: {message_str == ''.join(map(str, decoded_str))}")

if __name__ == "__main__":
    test_golay_code()
