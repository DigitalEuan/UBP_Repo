"""
Information Layer Detection Metrics for Study 2
================================================

This module implements refined metrics to detect "information layer activity"
in quantum entanglement data, as predicted by the Universal Binary Principle (UBP).

Key innovations from Study 1:
1. NRCI-Information: Analyzes information content, not just correlation stability
2. Temporal pattern analysis: Searches for sequential dependencies
3. Computational complexity measures: Quantifies "computational cost"
4. Multi-scale analysis: Examines patterns at different time scales

Author: Manus AI, on behalf of Euan R A Craig
Date: October 29, 2025
"""

import numpy as np
from scipy import stats
from scipy.signal import correlate
import json

class InformationLayerMetrics:
    """
    Comprehensive suite of metrics for detecting information layer signatures
    in quantum entanglement experiments.
    """
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        
    def shannon_entropy(self, binary_stream):
        """
        Calculate Shannon entropy of a binary outcome stream.
        
        H = -Σ p(x) log₂ p(x)
        
        For a truly random binary stream, H = 1.0 bit.
        Deviations indicate structure.
        """
        if len(binary_stream) == 0:
            return 0.0
            
        # Count 0s and 1s
        unique, counts = np.unique(binary_stream, return_counts=True)
        probabilities = counts / len(binary_stream)
        
        # Calculate entropy
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        return entropy
    
    def lempel_ziv_complexity(self, binary_stream):
        """
        Calculate Lempel-Ziv complexity - a measure of compressibility.
        
        Higher complexity = less compressible = more random
        Lower complexity = more compressible = more structured
        
        Normalized to [0, 1] range.
        """
        if len(binary_stream) < 2:
            return 0.0
            
        # Convert to string for pattern matching
        s = ''.join(map(str, binary_stream))
        n = len(s)
        
        # LZ76 algorithm
        complexity = 1
        prefix_len = 1
        i = 0
        
        while prefix_len + i < n:
            # Check if substring is in dictionary
            if s[i:i+prefix_len] in s[0:i+prefix_len]:
                prefix_len += 1
            else:
                complexity += 1
                i += prefix_len
                prefix_len = 1
                
        # Normalize by theoretical maximum
        # For random binary string: C_max ≈ n / log₂(n)
        c_max = n / (np.log2(n) + 1e-10)
        normalized_complexity = complexity / (c_max + 1e-10)
        
        return min(normalized_complexity, 1.0)
    
    def mutual_information(self, stream_a, stream_b):
        """
        Calculate mutual information between Alice and Bob streams.
        
        I(A;B) = H(A) + H(B) - H(A,B)
        
        Measures how much information is shared.
        """
        if len(stream_a) != len(stream_b) or len(stream_a) == 0:
            return 0.0
            
        # Individual entropies
        h_a = self.shannon_entropy(stream_a)
        h_b = self.shannon_entropy(stream_b)
        
        # Joint entropy
        joint_stream = np.array([stream_a, stream_b]).T
        unique_pairs, counts = np.unique(joint_stream, axis=0, return_counts=True)
        probabilities = counts / len(stream_a)
        h_joint = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        # Mutual information
        mi = h_a + h_b - h_joint
        
        return mi
    
    def autocorrelation_signature(self, binary_stream, max_lag=100):
        """
        Calculate autocorrelation function to detect temporal patterns.
        
        Returns:
            lags: Array of lag values
            acf: Autocorrelation function values
            anomaly_score: Measure of non-random structure
        """
        if len(binary_stream) < max_lag:
            max_lag = len(binary_stream) // 2
            
        # Convert to +1/-1 for correlation
        signal = 2 * binary_stream - 1
        
        # Calculate autocorrelation
        acf = correlate(signal, signal, mode='full')
        acf = acf[len(acf)//2:]  # Keep only positive lags
        acf = acf / acf[0]  # Normalize
        
        # Trim to max_lag
        lags = np.arange(min(max_lag, len(acf)))
        acf = acf[:len(lags)]
        
        # Anomaly score: sum of squared deviations from zero (excluding lag=0)
        # For truly random data, ACF should be ~0 for all lags > 0
        anomaly_score = np.sum(acf[1:]**2) / (len(acf) - 1)
        
        return lags, acf, anomaly_score
    
    def cross_correlation_signature(self, stream_a, stream_b, max_lag=50):
        """
        Calculate cross-correlation between Alice and Bob streams.
        
        Detects temporal dependencies beyond instantaneous correlation.
        """
        if len(stream_a) != len(stream_b) or len(stream_a) < max_lag:
            return np.array([0]), np.array([0.0]), 0.0
            
        # Convert to +1/-1
        signal_a = 2 * stream_a - 1
        signal_b = 2 * stream_b - 1
        
        # Calculate cross-correlation
        ccf = correlate(signal_a, signal_b, mode='full')
        ccf = ccf / (len(signal_a) * np.std(signal_a) * np.std(signal_b) + 1e-10)
        
        # Center and trim
        center = len(ccf) // 2
        lags = np.arange(-max_lag, max_lag + 1)
        ccf = ccf[center-max_lag:center+max_lag+1]
        
        # Anomaly score: excluding the central peak (instantaneous correlation)
        # Look for unexpected correlations at non-zero lags
        mask = np.abs(lags) > 5  # Exclude ±5 lags around center
        anomaly_score = np.sum(ccf[mask]**2) / np.sum(mask)
        
        return lags, ccf, anomaly_score
    
    def nrci_information(self, alice_stream, bob_stream, settings_a, settings_b):
        """
        NRCI-Information: Refined coherence index based on information content.
        
        This is the key innovation of Study 2. Instead of measuring correlation
        stability, we measure the information-theoretic properties.
        
        Components:
        1. Entropy balance: How well-balanced is the randomness?
        2. Mutual information: How much information is shared?
        3. Complexity: Is there hidden structure?
        4. Temporal coherence: Are there unexpected patterns over time?
        
        Returns value in [0, 1] where higher = more coherent information structure.
        """
        # Component 1: Entropy balance
        # Quantum data should have high entropy (near 1.0) for individual streams
        h_a = self.shannon_entropy(alice_stream)
        h_b = self.shannon_entropy(bob_stream)
        entropy_score = (h_a + h_b) / 2.0  # Average entropy
        
        # Component 2: Mutual information (normalized)
        mi = self.mutual_information(alice_stream, bob_stream)
        mi_score = mi  # Already in [0, 1] range for binary data
        
        # Component 3: Complexity balance
        # Quantum should be complex (incompressible) but not maximally so
        lz_a = self.lempel_ziv_complexity(alice_stream)
        lz_b = self.lempel_ziv_complexity(bob_stream)
        complexity_score = (lz_a + lz_b) / 2.0
        
        # Component 4: Temporal coherence
        # Quantum should have minimal autocorrelation (truly random over time)
        _, _, acf_anomaly_a = self.autocorrelation_signature(alice_stream, max_lag=50)
        _, _, acf_anomaly_b = self.autocorrelation_signature(bob_stream, max_lag=50)
        temporal_score = 1.0 - np.clip((acf_anomaly_a + acf_anomaly_b) / 2.0, 0, 1)
        
        # Weighted combination
        # These weights can be tuned based on UBP theory
        w_entropy = 0.25
        w_mi = 0.35  # Emphasize shared information
        w_complexity = 0.20
        w_temporal = 0.20
        
        nrci_i = (w_entropy * entropy_score + 
                  w_mi * mi_score + 
                  w_complexity * complexity_score + 
                  w_temporal * temporal_score)
        
        components = {
            'entropy': float(entropy_score),
            'mutual_information': float(mi_score),
            'complexity': float(complexity_score),
            'temporal_coherence': float(temporal_score)
        }
        
        return float(nrci_i), components
    
    def information_layer_signature(self, alice_stream, bob_stream, 
                                    settings_a, settings_b):
        """
        Comprehensive information layer analysis.
        
        Returns a detailed signature that can be compared between:
        - Quantum data
        - Classical data
        - Random data
        
        The hypothesis is that quantum data will show a unique pattern.
        """
        signature = {}
        
        # Basic information metrics
        signature['shannon_entropy_alice'] = self.shannon_entropy(alice_stream)
        signature['shannon_entropy_bob'] = self.shannon_entropy(bob_stream)
        signature['lz_complexity_alice'] = self.lempel_ziv_complexity(alice_stream)
        signature['lz_complexity_bob'] = self.lempel_ziv_complexity(bob_stream)
        signature['mutual_information'] = self.mutual_information(alice_stream, bob_stream)
        
        # Temporal patterns
        _, acf_a, acf_anomaly_a = self.autocorrelation_signature(alice_stream)
        _, acf_b, acf_anomaly_b = self.autocorrelation_signature(bob_stream)
        signature['autocorr_anomaly_alice'] = float(acf_anomaly_a)
        signature['autocorr_anomaly_bob'] = float(acf_anomaly_b)
        
        _, ccf, ccf_anomaly = self.cross_correlation_signature(alice_stream, bob_stream)
        signature['crosscorr_anomaly'] = float(ccf_anomaly)
        
        # NRCI-Information
        nrci_i, components = self.nrci_information(alice_stream, bob_stream, 
                                                   settings_a, settings_b)
        signature['nrci_information'] = float(nrci_i)
        signature['nrci_components'] = components
        
        # Statistical tests for randomness
        # Runs test: checks for clustering of 0s and 1s
        runs_stat_a, runs_p_a = self._runs_test(alice_stream)
        runs_stat_b, runs_p_b = self._runs_test(bob_stream)
        signature['runs_test_alice'] = {'statistic': float(runs_stat_a), 'p_value': float(runs_p_a)}
        signature['runs_test_bob'] = {'statistic': float(runs_stat_b), 'p_value': float(runs_p_b)}
        
        return signature
    
    def _runs_test(self, binary_stream):
        """
        Wald-Wolfowitz runs test for randomness.
        
        Tests whether the sequence of 0s and 1s is random.
        Low p-value indicates non-randomness.
        """
        if len(binary_stream) < 10:
            return 0.0, 1.0
            
        # Count runs (sequences of same value)
        runs = 1
        for i in range(1, len(binary_stream)):
            if binary_stream[i] != binary_stream[i-1]:
                runs += 1
                
        # Count 0s and 1s
        n0 = np.sum(binary_stream == 0)
        n1 = np.sum(binary_stream == 1)
        
        if n0 == 0 or n1 == 0:
            return 0.0, 1.0
            
        # Expected runs and variance under null hypothesis (randomness)
        n = n0 + n1
        expected_runs = (2 * n0 * n1) / n + 1
        variance_runs = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n**2 * (n - 1))
        
        # Z-score
        z = (runs - expected_runs) / (np.sqrt(variance_runs) + 1e-10)
        
        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        return z, p_value
    
    def weighted_nrci_scan(self, alice_stream, bob_stream, settings_a, settings_b,
                          weight_range=(1.0, 2.5), n_points=100):
        """
        Scan geometric weights to find optimal NRCI-I.
        
        This is analogous to Study 1's weight scan, but using the refined metric.
        """
        weights = np.linspace(weight_range[0], weight_range[1], n_points)
        nrci_values = []
        
        for w in weights:
            # Apply geometric weight to the mutual information component
            # This is a simplified model; full UBP would weight the bitfield operations
            nrci_i, _ = self.nrci_information(alice_stream, bob_stream, 
                                             settings_a, settings_b)
            
            # Weight the mutual information component
            mi = self.mutual_information(alice_stream, bob_stream)
            weighted_mi = mi * w / 2.0  # Normalize
            
            # Recalculate NRCI-I with weighted MI
            h_a = self.shannon_entropy(alice_stream)
            h_b = self.shannon_entropy(bob_stream)
            entropy_score = (h_a + h_b) / 2.0
            
            lz_a = self.lempel_ziv_complexity(alice_stream)
            lz_b = self.lempel_ziv_complexity(bob_stream)
            complexity_score = (lz_a + lz_b) / 2.0
            
            _, _, acf_anomaly_a = self.autocorrelation_signature(alice_stream, max_lag=50)
            _, _, acf_anomaly_b = self.autocorrelation_signature(bob_stream, max_lag=50)
            temporal_score = 1.0 - np.clip((acf_anomaly_a + acf_anomaly_b) / 2.0, 0, 1)
            
            # Weighted NRCI-I
            nrci_i_weighted = (0.25 * entropy_score + 
                              0.35 * np.clip(weighted_mi, 0, 1) + 
                              0.20 * complexity_score + 
                              0.20 * temporal_score)
            
            nrci_values.append(nrci_i_weighted)
        
        nrci_values = np.array(nrci_values)
        
        # Find optimal weight
        best_idx = np.argmax(nrci_values)
        best_weight = weights[best_idx]
        best_nrci = nrci_values[best_idx]
        
        return weights, nrci_values, best_weight, best_nrci


def analyze_dataset(data, label="Dataset"):
    """
    Convenience function to analyze a complete dataset.
    
    Args:
        data: Dictionary with keys 'alice_outcomes', 'bob_outcomes', 
              'alice_settings', 'bob_settings'
        label: Name for the dataset
    
    Returns:
        Dictionary of analysis results
    """
    metrics = InformationLayerMetrics()
    
    alice_stream = np.array(data['alice_outcomes'])
    bob_stream = np.array(data['bob_outcomes'])
    settings_a = np.array(data['alice_settings'])
    settings_b = np.array(data['bob_settings'])
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {label}")
    print(f"{'='*60}")
    print(f"Sample size: {len(alice_stream)} events")
    
    # Full signature
    signature = metrics.information_layer_signature(alice_stream, bob_stream,
                                                   settings_a, settings_b)
    
    print(f"\nInformation Layer Signature:")
    print(f"  Shannon Entropy (Alice): {signature['shannon_entropy_alice']:.4f}")
    print(f"  Shannon Entropy (Bob):   {signature['shannon_entropy_bob']:.4f}")
    print(f"  LZ Complexity (Alice):   {signature['lz_complexity_alice']:.4f}")
    print(f"  LZ Complexity (Bob):     {signature['lz_complexity_bob']:.4f}")
    print(f"  Mutual Information:      {signature['mutual_information']:.4f}")
    print(f"  NRCI-Information:        {signature['nrci_information']:.4f}")
    
    print(f"\nNRCI-I Components:")
    for key, value in signature['nrci_components'].items():
        print(f"  {key:20s}: {value:.4f}")
    
    print(f"\nTemporal Anomalies:")
    print(f"  Autocorr Anomaly (Alice): {signature['autocorr_anomaly_alice']:.6f}")
    print(f"  Autocorr Anomaly (Bob):   {signature['autocorr_anomaly_bob']:.6f}")
    print(f"  Crosscorr Anomaly:        {signature['crosscorr_anomaly']:.6f}")
    
    print(f"\nRandomness Tests:")
    print(f"  Runs Test (Alice): z={signature['runs_test_alice']['statistic']:.3f}, p={signature['runs_test_alice']['p_value']:.4f}")
    print(f"  Runs Test (Bob):   z={signature['runs_test_bob']['statistic']:.3f}, p={signature['runs_test_bob']['p_value']:.4f}")
    
    # Weight scan
    print(f"\nPerforming geometric weight scan...")
    weights, nrci_values, best_weight, best_nrci = metrics.weighted_nrci_scan(
        alice_stream, bob_stream, settings_a, settings_b
    )
    
    print(f"  Optimal weight: {best_weight:.4f}")
    print(f"  Maximum NRCI-I: {best_nrci:.4f}")
    
    # Add weight scan to results
    signature['weight_scan'] = {
        'weights': weights.tolist(),
        'nrci_values': nrci_values.tolist(),
        'best_weight': float(best_weight),
        'best_nrci': float(best_nrci)
    }
    
    return signature


if __name__ == "__main__":
    print("Information Layer Metrics Module")
    print("=================================")
    print("This module provides tools for detecting information layer")
    print("signatures in quantum entanglement data.")
    print("\nUse analyze_dataset(data, label) to analyze your data.")

