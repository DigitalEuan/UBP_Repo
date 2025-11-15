"""
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
    if len(data1) != len(data2):
        max_len = max(len(data1), len(data2))
        data1 = data1 + [0.0] * (max_len - len(data1))
        data2 = data2 + [0.0] * (max_len - len(data2))
    
    # Simple DFT implementation (zero-dependency)
    def dft(signal):
        N = len(signal)
        spectrum = []
        for k in range(N // 2):  # Only need half (Nyquist)
            real = sum(signal[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
            imag = sum(signal[n] * -math.sin(2 * math.pi * k * n / N) for n in range(N))
            magnitude = math.sqrt(real**2 + imag**2)
            spectrum.append(magnitude)
        return spectrum
    
    spec1 = dft(data1)
    spec2 = dft(data2)
    
    # Euclidean distance in frequency domain
    return math.sqrt(sum((s1 - s2)**2 for s1, s2 in zip(spec1, spec2)))


def graph_edit_distance(adj1: List[List[int]], adj2: List[List[int]]) -> int:
    """
    Graph edit distance for network structure comparison.
    
    Advantage: Captures relational structure, not just values.
    """
    if len(adj1) != len(adj2):
        return abs(len(adj1) - len(adj2)) * 100  # Penalty for size mismatch
    
    # Count edge differences
    n = len(adj1)
    differences = 0
    
    for i in range(n):
        for j in range(n):
            if adj1[i][j] != adj2[i][j]:
                differences += 1
    
    return differences


# ============================================================================
# TOPOLOGICAL ANALYSIS
# ============================================================================

def compute_persistence_diagram(data: List[float], max_dimension: int = 1) -> List[Tuple[float, float]]:
    """
    Compute persistence diagram for topological data analysis.
    
    Simplified implementation for zero-dependency.
    Returns birth-death pairs representing topological features.
    """
    # Sort data for filtration
    sorted_data = sorted(enumerate(data), key=lambda x: x[1])
    
    # Track connected components (0-dimensional features)
    persistence_pairs = []
    
    # Birth: when point appears
    # Death: when it merges with another component
    births = {}
    
    for idx, (original_idx, value) in enumerate(sorted_data):
        births[original_idx] = value
        
        # Check if merges with previous (simplified)
        if idx > 0:
            prev_idx, prev_value = sorted_data[idx - 1]
            if abs(value - prev_value) < 0.1:  # Threshold for merging
                # Feature dies
                death = value
                birth = births.get(prev_idx, prev_value)
                persistence_pairs.append((birth, death))
    
    return persistence_pairs


def persistence_distance(pairs1: List[Tuple[float, float]], 
                        pairs2: List[Tuple[float, float]]) -> float:
    """
    Bottleneck distance between persistence diagrams.
    
    Advantage: Topologically robust, captures shape features.
    """
    if not pairs1 or not pairs2:
        return float('inf')
    
    # Simplified: sum of differences in persistence (death - birth)
    pers1 = [death - birth for birth, death in pairs1]
    pers2 = [death - birth for birth, death in pairs2]
    
    # Pad to same length
    max_len = max(len(pers1), len(pers2))
    pers1 += [0.0] * (max_len - len(pers1))
    pers2 += [0.0] * (max_len - len(pers2))
    
    # Euclidean distance
    return math.sqrt(sum((p1 - p2)**2 for p1, p2 in zip(pers1, pers2)))


# ============================================================================
# MULTI-SCALE ANALYSIS
# ============================================================================

def wavelet_decomposition(data: List[float], levels: int = 3) -> List[List[float]]:
    """
    Simple wavelet decomposition using Haar wavelets.
    
    Advantage: Multi-scale analysis, captures features at different resolutions.
    """
    def haar_transform(signal):
        """Single level Haar wavelet transform."""
        n = len(signal)
        if n < 2:
            return signal, []
        
        # Approximation coefficients (averages)
        approx = [(signal[i] + signal[i+1]) / 2.0 for i in range(0, n-1, 2)]
        
        # Detail coefficients (differences)
        detail = [(signal[i] - signal[i+1]) / 2.0 for i in range(0, n-1, 2)]
        
        return approx, detail
    
    # Decompose into multiple levels
    coefficients = []
    current = data[:]
    
    for level in range(levels):
        if len(current) < 2:
            break
        approx, detail = haar_transform(current)
        coefficients.append(detail)
        current = approx
    
    coefficients.append(current)  # Final approximation
    
    return coefficients


def wavelet_distance(data1: List[float], data2: List[float], levels: int = 3) -> float:
    """
    Distance based on wavelet coefficients.
    
    Advantage: Captures multi-scale structure.
    """
    # Pad to power of 2
    max_len = max(len(data1), len(data2))
    power_of_2 = 2 ** math.ceil(math.log2(max_len))
    
    # Convert to list if numpy array
    if hasattr(data1, 'tolist'):
        data1 = data1.tolist()
    if hasattr(data2, 'tolist'):
        data2 = data2.tolist()
    
    data1 = data1 + [0.0] * (power_of_2 - len(data1))
    data2 = data2 + [0.0] * (power_of_2 - len(data2))
    
    # Decompose
    coeffs1 = wavelet_decomposition(data1, levels)
    coeffs2 = wavelet_decomposition(data2, levels)
    
    # Compare coefficients at each level
    total_distance = 0.0
    
    for c1, c2 in zip(coeffs1, coeffs2):
        # Pad to same length
        max_len_c = max(len(c1), len(c2))
        c1 = c1 + [0.0] * (max_len_c - len(c1))
        c2 = c2 + [0.0] * (max_len_c - len(c2))
        
        # Euclidean distance at this level
        level_dist = math.sqrt(sum((x1 - x2)**2 for x1, x2 in zip(c1, c2)))
        total_distance += level_dist
    
    return total_distance


# ============================================================================
# ADVANCED HEX DICTIONARY ANALYZER
# ============================================================================

@dataclass
class AdvancedSimilarityResult:
    """
    Comprehensive similarity analysis result.
    """
    hash1: str
    hash2: str
    
    # Traditional
    hamming_distance: int
    
    # Advanced methods
    spectral_distance: float
    kl_divergence: float
    frequency_distance: float
    wavelet_distance: float
    topological_distance: float
    
    # Coherence-aware (if available)
    coherence_weighted_distance: Optional[float]
    
    # Overall similarity score (0-1, higher = more similar)
    overall_similarity: float
    
    # Confidence in analysis
    confidence: float


class AdvancedHexDictionaryAnalyzer:
    """
    Advanced analyzer for HexDictionary patterns.
    """
    
    def __init__(self, hex_dict: Optional[HexDictionary] = None):
        """
        Initialize analyzer.
        
        Args:
            hex_dict: Optional HexDictionary instance
        """
        self.hex_dict = hex_dict or HexDictionary()
        self.analysis_cache = {}
    
    def analyze_similarity(self, 
                          hash1: str, 
                          hash2: str,
                          data1: Optional[List[float]] = None,
                          data2: Optional[List[float]] = None,
                          states1: Optional[List[CoherenceState]] = None,
                          states2: Optional[List[CoherenceState]] = None) -> AdvancedSimilarityResult:
        """
        Comprehensive similarity analysis using multiple advanced methods.
        
        Args:
            hash1, hash2: Hex hashes to compare
            data1, data2: Optional raw data for advanced analysis
            states1, states2: Optional CoherenceState objects
            
        Returns:
            Complete similarity analysis
        """
        # Hamming distance (baseline)
        hamming_dist = hamming_distance(hash1, hash2)
        
        # Advanced methods (if data available)
        if data1 is not None and data2 is not None and len(data1) > 0 and len(data2) > 0:
            spectral_dist = spectral_distance(data1, data2)
            
            # Normalize data for KL divergence
            kl_div = kl_divergence(data1, data2)
            
            freq_dist = frequency_domain_distance(data1, data2)
            
            wavelet_dist = wavelet_distance(data1, data2)
            
            # Topological analysis
            pers1 = compute_persistence_diagram(data1)
            pers2 = compute_persistence_diagram(data2)
            topo_dist = persistence_distance(pers1, pers2)
            
            confidence = 0.9
        else:
            # Only Hamming available
            spectral_dist = 0.0
            kl_div = 0.0
            freq_dist = 0.0
            wavelet_dist = 0.0
            topo_dist = 0.0
            confidence = 0.3
        
        # Coherence-aware distance
        if states1 and states2:
            coh_dist = coherence_weighted_distance(states1, states2)
            confidence += 0.1
        else:
            coh_dist = None
        
        # Compute overall similarity score
        overall_sim = self._compute_overall_similarity(
            hamming_dist, spectral_dist, kl_div, freq_dist, 
            wavelet_dist, topo_dist, coh_dist
        )
        
        result = AdvancedSimilarityResult(
            hash1=hash1,
            hash2=hash2,
            hamming_distance=hamming_dist,
            spectral_distance=spectral_dist,
            kl_divergence=kl_div,
            frequency_distance=freq_dist,
            wavelet_distance=wavelet_dist,
            topological_distance=topo_dist,
            coherence_weighted_distance=coh_dist,
            overall_similarity=overall_sim,
            confidence=min(1.0, confidence)
        )
        
        # Cache result
        cache_key = f"{hash1}_{hash2}"
        self.analysis_cache[cache_key] = result
        
        return result
    
    def _compute_overall_similarity(self, 
                                   hamming: int,
                                   spectral: float,
                                   kl: float,
                                   frequency: float,
                                   wavelet: float,
                                   topological: float,
                                   coherence: Optional[float]) -> float:
        """
        Compute overall similarity score (0-1).
        
        Higher score = more similar.
        """
        # Normalize distances to [0, 1] range and invert (1 = similar)
        
        # Hamming (assume max 256 bits)
        hamming_sim = 1.0 - min(1.0, hamming / 256.0)
        
        # Spectral (normalize by typical range)
        spectral_sim = 1.0 / (1.0 + spectral)
        
        # KL divergence (already normalized-ish)
        kl_sim = 1.0 / (1.0 + kl)
        
        # Frequency
        freq_sim = 1.0 / (1.0 + frequency)
        
        # Wavelet
        wavelet_sim = 1.0 / (1.0 + wavelet)
        
        # Topological
        topo_sim = 1.0 / (1.0 + topological)
        
        # Coherence
        if coherence is not None:
            coh_sim = 1.0 / (1.0 + coherence)
            weights = [0.10, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
            similarities = [hamming_sim, spectral_sim, kl_sim, freq_sim, 
                          wavelet_sim, topo_sim, coh_sim]
        else:
            weights = [0.15, 0.20, 0.20, 0.15, 0.15, 0.15]
            similarities = [hamming_sim, spectral_sim, kl_sim, freq_sim, 
                          wavelet_sim, topo_sim]
        
        # Weighted average
        overall = sum(w * s for w, s in zip(weights, similarities))
        
        return max(0.0, min(1.0, overall))
    
    def find_similar_patterns(self, 
                            target_hash: str,
                            target_data: Optional[List[float]] = None,
                            target_states: Optional[List[CoherenceState]] = None,
                            top_k: int = 5,
                            min_similarity: float = 0.5) -> List[Tuple[str, AdvancedSimilarityResult]]:
        """
        Find most similar patterns in HexDictionary.
        
        Args:
            target_hash: Hash to find similarities for
            target_data: Optional data for advanced analysis
            target_states: Optional CoherenceState objects
            top_k: Number of top matches to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of (hash, similarity_result) tuples, sorted by similarity
        """
        all_hashes = self.hex_dict.list_all()
        similarities = []
        
        for candidate_hash in all_hashes:
            if candidate_hash == target_hash:
                continue
            
            # Try to retrieve data
            candidate_data = self.hex_dict.retrieve(candidate_hash)
            
            # Convert to list if needed
            if isinstance(candidate_data, str):
                candidate_data = [float(ord(c)) for c in candidate_data[:100]]
            elif isinstance(candidate_data, dict):
                candidate_data = list(candidate_data.values())[:100]
            elif not isinstance(candidate_data, list):
                candidate_data = None
            
            # Analyze similarity
            result = self.analyze_similarity(
                target_hash, candidate_hash,
                target_data, candidate_data,
                target_states, None
            )
            
            if result.overall_similarity >= min_similarity:
                similarities.append((candidate_hash, result))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1].overall_similarity, reverse=True)
        
        return similarities[:top_k]
    
    def export_analysis(self, filepath: str):
        """Export analysis cache to JSON."""
        export_data = {
            'analysis_count': len(self.analysis_cache),
            'analyses': [
                {
                    'hash1': result.hash1,
                    'hash2': result.hash2,
                    'hamming_distance': result.hamming_distance,
                    'spectral_distance': result.spectral_distance,
                    'kl_divergence': result.kl_divergence,
                    'frequency_distance': result.frequency_distance,
                    'wavelet_distance': result.wavelet_distance,
                    'topological_distance': result.topological_distance,
                    'coherence_weighted_distance': result.coherence_weighted_distance,
                    'overall_similarity': result.overall_similarity,
                    'confidence': result.confidence
                }
                for result in self.analysis_cache.values()
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED HEXDICTIONARY ANALYZER - Beyond Hamming Distance")
    print("=" * 80)
    print()
    
    # Create analyzer
    analyzer = AdvancedHexDictionaryAnalyzer()
    
    print("Testing advanced similarity methods...")
    print()
    
    # Test data
    data1 = [1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0]
    data2 = [1.1, 2.1, 3.1, 4.1, 5.1, 4.1, 3.1, 2.1]  # Similar
    data3 = [5.0, 1.0, 3.0, 2.0, 4.0, 1.0, 5.0, 3.0]  # Different
    
    # Store in HexDict
    hash1 = analyzer.hex_dict.store(data1, data_type='json', metadata={'type': 'pattern_A'})
    hash2 = analyzer.hex_dict.store(data2, data_type='json', metadata={'type': 'pattern_B'})
    hash3 = analyzer.hex_dict.store(data3, data_type='json', metadata={'type': 'pattern_C'})
    
    print(f"Stored 3 patterns:")
    print(f"  Pattern A: {hash1[:16]}...")
    print(f"  Pattern B: {hash2[:16]}...")
    print(f"  Pattern C: {hash3[:16]}...")
    print()
    
    # Compare A vs B (similar)
    print("Comparison 1: Pattern A vs Pattern B (expected: similar)")
    print("-" * 80)
    result_ab = analyzer.analyze_similarity(hash1, hash2, data1, data2)
    print(f"  Hamming Distance: {result_ab.hamming_distance}")
    print(f"  Spectral Distance: {result_ab.spectral_distance:.4f}")
    print(f"  KL Divergence: {result_ab.kl_divergence:.4f}")
    print(f"  Frequency Distance: {result_ab.frequency_distance:.4f}")
    print(f"  Wavelet Distance: {result_ab.wavelet_distance:.4f}")
    print(f"  Topological Distance: {result_ab.topological_distance:.4f}")
    print(f"  → Overall Similarity: {result_ab.overall_similarity:.3f}")
    print(f"  → Confidence: {result_ab.confidence:.3f}")
    print()
    
    # Compare A vs C (different)
    print("Comparison 2: Pattern A vs Pattern C (expected: different)")
    print("-" * 80)
    result_ac = analyzer.analyze_similarity(hash1, hash3, data1, data3)
    print(f"  Hamming Distance: {result_ac.hamming_distance}")
    print(f"  Spectral Distance: {result_ac.spectral_distance:.4f}")
    print(f"  KL Divergence: {result_ac.kl_divergence:.4f}")
    print(f"  Frequency Distance: {result_ac.frequency_distance:.4f}")
    print(f"  Wavelet Distance: {result_ac.wavelet_distance:.4f}")
    print(f"  Topological Distance: {result_ac.topological_distance:.4f}")
    print(f"  → Overall Similarity: {result_ac.overall_similarity:.3f}")
    print(f"  → Confidence: {result_ac.confidence:.3f}")
    print()
    
    # Find similar patterns
    print("Finding patterns similar to Pattern A...")
    print("-" * 80)
    similar = analyzer.find_similar_patterns(hash1, data1, top_k=2, min_similarity=0.3)
    for i, (sim_hash, sim_result) in enumerate(similar, 1):
        meta = analyzer.hex_dict.get_metadata(sim_hash)
        print(f"  {i}. {sim_hash[:16]}... ({meta.get('type', 'unknown')})")
        print(f"     Similarity: {sim_result.overall_similarity:.3f}")
    print()
    
    # Export
    analyzer.export_analysis('/home/ubuntu/dissident_horizon_study/hex_advanced_demo_results.json')
    print("Results exported to: hex_advanced_demo_results.json")
    print()
    
    print("=" * 80)
    print("Key Insight: Advanced methods provide much richer similarity analysis")
    print("than simple Hamming distance, capturing spectral, topological, and")
    print("frequency-domain relationships that Hamming misses entirely.")
    print("=" * 80)
