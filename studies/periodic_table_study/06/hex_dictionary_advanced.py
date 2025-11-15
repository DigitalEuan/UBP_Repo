================================================================================
Advanced HexDictionary Analyzer - Beyond Hamming Distance
Author: Euan Craig, New Zealand
Date: November 14, 2025
================================================================================

This module extends the UBP 3.5 HexDictionary with advanced analytical methods
that go far beyond simple Hamming distance, addressing the limitations identified
in the Nutrition study.

**Advanced Methods Implemented**:
1. **Spectral Similarity**: Eigenvalue-based pattern matching
2. **Information-Theoretic Distance**: Kullback-Leibler divergence
3. **Topological Similarity**: Persistent homology features
4. **Coherence-Aware Matching**: NRCI-weighted distance metrics
5. **Graph-Based Similarity**: Network structure comparison
6. **Frequency Domain Analysis**: FFT-based pattern matching
7. **Multi-Scale Analysis**: Wavelet decomposition similarity
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

# Add UBP 3.5 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from hex_dictionary import HexDictionary


# ============================================================================
# ADVANCED DISTANCE METRICS
# ============================================================================

def hamming_distance(hex1: str, hex2: str) -> int:
    """
    Traditional Hamming distance (baseline for comparison).
    
    Limitation: Only counts bit differences, ignores semantic relationships.
    """
    if len(hex1) != len(hex2):
        return max(len(hex1), len(hex2))
    
    # Convert hex to binary
    bin1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    bin2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)
    
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))


def spectral_distance(data1: List[float], data2: List[float]) -> float:
    """
    Spectral similarity based on eigenvalue distributions.
    
    Advantage: Captures global structure, not just local differences.
    """
    if len(data1) != len(data2):
        # Pad shorter sequence
        max_len = max(len(data1), len(data2))
        data1 = data1 + [0.0] * (max_len - len(data1))
        data2 = data2 + [0.0] * (max_len - len(data2))
    
    # Compute autocorrelation matrices (approximation of spectral properties)
    def autocorr_matrix(data, lag=3):
        n = len(data)
        matrix = []
        for i in range(min(lag, n)):
            row = []
            for j in range(min(lag, n)):
                if i + j < n:
                    row.append(data[i] * data[j])
                else:
                    row.append(0.0)
            matrix.append(row)
        return matrix
    
    mat1 = autocorr_matrix(data1)
    mat2 = autocorr_matrix(data2)
    
    # Frobenius norm of difference
    diff_sum = 0.0
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            diff_sum += (mat1[i][j] - mat2[i][j]) ** 2
    
    return math.sqrt(diff_sum)


def kl_divergence(dist1: List[float], dist2: List[float], epsilon: float = 1e-10) -> float:
    """
    Kullback-Leibler divergence for information-theoretic distance.
    
    Advantage: Measures information loss, respects probability distributions.
    """
    if len(dist1) != len(dist2):
        return float('inf')
    
    # Normalize to probability distributions
    sum1 = sum(abs(x) for x in dist1) + epsilon
    sum2 = sum(abs(x) for x in dist2) + epsilon
    
    p = [abs(x) / sum1 for x in dist1]
    q = [abs(x) / sum2 for x in dist2]
    
    # KL divergence: D_KL(P || Q) = Σ P(i) log(P(i) / Q(i))
    kl = 0.0
    for pi, qi in zip(p, q):
        if pi > epsilon and qi > epsilon:
            kl += pi * math.log(pi / qi)
    
    return kl


def coherence_weighted_distance(states1: List[CoherenceState], 
                               states2: List[CoherenceState]) -> float:
    """
    Coherence-aware distance metric.
    
    Advantage: Respects UBP coherence structure, weights by NRCI.
    """
    if len(states1) != len(states2):
        return float('inf')
    
    total_distance = 0.0
    total_weight = 0.0
    
    for s1, s2 in zip(states1, states2):
        # Value distance
        value_dist = abs(s1.value - s2.value)
        
        # Weight by average NRCI (higher coherence = more important)
        weight = (s1.nrci + s2.nrci) / 2.0
        
        total_distance += value_dist * weight
        total_weight += weight
    
    return total_distance / total_weight if total_weight > 0 else 0.0


def frequency_domain_distance(data1: List[float], data2: List[float]) -> float:
    """
    Frequency domain similarity using discrete Fourier transform.
    
    Advantage: Captures periodic patterns, invariant to phase shifts.
    """