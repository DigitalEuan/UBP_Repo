#!/usr/bin/env python3.11
"""
Module 1: Golay(24,12) Code Generator
Author: Euan R A Craig
Date: October 15, 2025
Framework: Universal Binary Principle (UBP) v3.2

This module implements the extended binary Golay code G24, which is fundamental
to the Leech lattice construction and the UBP's error correction framework.

The Golay(24,12) code is a perfect error-correcting code that can:
- Encode 12 information bits into 24 code bits
- Correct up to 3 bit errors
- Detect up to 7 bit errors
- Forms the foundation of the Leech lattice in 24 dimensions
"""

import numpy as np
import pandas as pd
from typing import List, Tuple
import os

# Directories
DATA_DIR = '/home/ubuntu/black_holes_quantum_tunnelling_3/data'
FIG_DIR = '/home/ubuntu/black_holes_quantum_tunnelling_3/figures'

class GolayCode24:
    """
    Extended binary Golay code G24.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: The Golay(24,12) code is a perfect error-correcting code that
    maps 12-bit messages to 24-bit codewords. It is the unique code with
    parameters [24, 12, 8], meaning 24 bits total, 12 information bits, and
    minimum Hamming distance 8. This code is deeply connected to the Mathieu
    group M24 and forms the basis of the Leech lattice.
    
    MATHEMATICS:
    - Generator matrix G: 12×24 matrix [I₁₂ | A]
    - Parity check matrix H: 12×24 matrix [Aᵀ | I₁₂]
    - A is a 12×12 circulant matrix with first row: 11100010011
    - Codeword: c = m · G (mod 2), where m is 12-bit message
    - Syndrome: s = c · Hᵀ (mod 2)
    
    SCRIPT: Initialize generator matrix, encode messages, compute parity
    statistics, generate all 4096 codewords.
    """
    
    def __init__(self):
        """Initialize Golay(24,12) code with generator matrix."""
        # First row of circulant matrix A (from standard Golay construction)
        self.a_first_row = np.array([1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0], dtype=np.uint8)
        
        # Build 12x12 circulant matrix A
        self.A = self._build_circulant_matrix(self.a_first_row)
        
        # Generator matrix G = [I_12 | A]
        I12 = np.eye(12, dtype=np.uint8)
        self.G = np.hstack([I12, self.A])
        
        # Parity check matrix H = [A^T | I_12]
        self.H = np.hstack([self.A.T, I12])
        
        print("Golay(24,12) Code initialized:")
        print(f"  Generator matrix G: {self.G.shape}")
        print(f"  Parity check matrix H: {self.H.shape}")
        print(f"  Code parameters: [n=24, k=12, d=8]")
        print(f"  Total codewords: 2^12 = 4096\n")
    
    def _build_circulant_matrix(self, first_row: np.ndarray) -> np.ndarray:
        """Build circulant matrix from first row."""
        n = len(first_row)
        matrix = np.zeros((n, n), dtype=np.uint8)
        for i in range(n):
            matrix[i] = np.roll(first_row, i)
        return matrix
    
    def encode(self, message: np.ndarray) -> np.ndarray:
        """
        Encode 12-bit message to 24-bit codeword.
        
        Parameters:
        -----------
        message : ndarray
            12-bit message vector
            
        Returns:
        --------
        codeword : ndarray
            24-bit Golay codeword
        """
        if len(message) != 12:
            raise ValueError("Message must be 12 bits")
        
        # c = m · G (mod 2)
        codeword = (message @ self.G) % 2
        return codeword.astype(np.uint8)
    
    def compute_hamming_weight(self, codeword: np.ndarray) -> int:
        """Compute Hamming weight (number of 1s) in codeword."""
        return int(np.sum(codeword))
    
    def is_even_parity(self, codeword: np.ndarray) -> bool:
        """Check if codeword has even Hamming weight."""
        return self.compute_hamming_weight(codeword) % 2 == 0
    
    def generate_all_codewords(self) -> np.ndarray:
        """
        Generate all 4096 Golay codewords.
        
        Returns:
        --------
        codewords : ndarray
            4096 × 24 array of all codewords
        """
        print("Generating all 4096 Golay codewords...")
        codewords = np.zeros((4096, 24), dtype=np.uint8)
        
        for i in range(4096):
            # Convert i to 12-bit binary message
            message = np.array([int(b) for b in format(i, '012b')], dtype=np.uint8)
            codewords[i] = self.encode(message)
            
            if i % 1000 == 0:
                print(f"  Generated {i}/4096 codewords...")
        
        print(f"✓ All 4096 codewords generated\n")
        return codewords
    
    def compute_parity_statistics(self, codewords: np.ndarray) -> dict:
        """
        Compute parity statistics for Golay codewords.
        
        Parameters:
        -----------
        codewords : ndarray
            Array of codewords (N × 24)
            
        Returns:
        --------
        stats : dict
            Parity statistics
        """
        hamming_weights = np.array([self.compute_hamming_weight(c) for c in codewords])
        even_parity = (hamming_weights % 2 == 0)
        
        stats = {
            'n_codewords': len(codewords),
            'mean_hamming_weight': hamming_weights.mean(),
            'std_hamming_weight': hamming_weights.std(),
            'min_hamming_weight': hamming_weights.min(),
            'max_hamming_weight': hamming_weights.max(),
            'even_parity_count': even_parity.sum(),
            'odd_parity_count': (~even_parity).sum(),
            'even_parity_pct': (even_parity.sum() / len(codewords)) * 100,
            'hamming_weight_distribution': np.bincount(hamming_weights, minlength=25)
        }
        
        return stats, hamming_weights

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("MODULE 1: GOLAY(24,12) CODE GENERATOR")
    print("="*80)
    print("Framework: Universal Binary Principle (UBP) v3.2")
    print("Author: Euan R A Craig")
    print("="*80 + "\n")
    
    # Initialize Golay code
    golay = GolayCode24()
    
    # Generate all codewords
    all_codewords = golay.generate_all_codewords()
    
    # Compute parity statistics
    print("Computing parity statistics...")
    stats, hamming_weights = golay.compute_parity_statistics(all_codewords)
    
    print("\nGolay Code Parity Statistics:")
    print("-"*80)
    print(f"  Total codewords: {stats['n_codewords']:,}")
    print(f"  Mean Hamming weight: {stats['mean_hamming_weight']:.4f}")
    print(f"  Std Hamming weight: {stats['std_hamming_weight']:.4f}")
    print(f"  Min Hamming weight: {stats['min_hamming_weight']}")
    print(f"  Max Hamming weight: {stats['max_hamming_weight']}")
    print(f"  Even parity count: {stats['even_parity_count']:,}")
    print(f"  Odd parity count: {stats['odd_parity_count']:,}")
    print(f"  Even parity %: {stats['even_parity_pct']:.2f}%")
    print()
    
    # Save codewords
    codewords_file = f'{DATA_DIR}/golay_codewords.npy'
    np.save(codewords_file, all_codewords)
    print(f"✓ Saved codewords: {codewords_file}")
    
    # Save statistics
    stats_df = pd.DataFrame([{k: v for k, v in stats.items() if k != 'hamming_weight_distribution'}])
    stats_file = f'{DATA_DIR}/golay_parity_stats.csv'
    stats_df.to_csv(stats_file, index=False)
    print(f"✓ Saved statistics: {stats_file}")
    
    # Save Hamming weight distribution
    hw_dist_df = pd.DataFrame({
        'hamming_weight': range(len(stats['hamming_weight_distribution'])),
        'count': stats['hamming_weight_distribution']
    })
    hw_dist_file = f'{DATA_DIR}/golay_hamming_weight_distribution.csv'
    hw_dist_df.to_csv(hw_dist_file, index=False)
    print(f"✓ Saved Hamming weight distribution: {hw_dist_file}")
    
    # Sample some codewords
    print("\nSample Golay Codewords:")
    print("-"*80)
    for i in [0, 1, 2, 3, 4095]:
        cw = all_codewords[i]
        hw = golay.compute_hamming_weight(cw)
        parity = "even" if golay.is_even_parity(cw) else "odd"
        print(f"  Codeword {i:4d}: {''.join(map(str, cw))} (weight={hw:2d}, parity={parity})")
    
    print("\n" + "="*80)
    print("MODULE 1 COMPLETE")
    print("="*80)
    print(f"Key Result: Golay(24,12) even parity = {stats['even_parity_pct']:.2f}%")
    print("="*80 + "\n")
    
    return golay, all_codewords, stats

if __name__ == "__main__":
    golay, codewords, stats = main()

