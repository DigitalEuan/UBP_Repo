"""
================================================================================
Full Advanced HexDictionary Analysis - All 8 Methods
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

Comprehensive analysis using ALL Advanced HexDictionary methods:
1. Hamming Distance (baseline)
2. Spectral Similarity
3. Information-Theoretic Distance (KL Divergence)
4. Topological Similarity (Persistence)
5. Coherence-Aware Matching
6. Graph-Based Similarity
7. Frequency Domain Analysis
8. Multi-Scale Analysis (Wavelet)
"""

import sys
import os
import json
import math
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/blood_type_ubp_study_v2')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from hex_dictionary_advanced import (
    hamming_distance,
    spectral_distance,
    kl_divergence,
    coherence_weighted_distance,
    frequency_domain_distance,
    graph_edit_distance,
    wavelet_distance,
    compute_persistence_diagram,
    persistence_distance,
)
from blood_type_data_extended import (
    get_all_blood_types,
    get_numerical_features,
    create_coherence_field,
)


# ============================================================================
# FULL HEXDICTIONARY ANALYSIS
# ============================================================================

class FullHexDictionaryAnalyzer:
    """
    Comprehensive HexDictionary analyzer using all 8 advanced methods.
    """
    
    def __init__(self):
        self.blood_types = get_all_blood_types()
        self.results = {}
    
    def analyze_all_methods(self) -> Dict[str, Any]:
        """
        Run all 8 similarity methods on all blood type pairs.
        
        Returns comprehensive results dictionary.
        """
        print("=" * 80)
        print("Full Advanced HexDictionary Analysis - All 8 Methods")
        print("=" * 80)
        print()
        
        results = {
            "metadata": {
                "blood_types": self.blood_types,
                "num_types": len(self.blood_types),
                "num_comparisons": len(self.blood_types) * (len(self.blood_types) - 1) // 2,
                "methods": 8,
            },
            "method_results": {},
        }
        
        # Method 1: Hamming Distance (baseline)
        print("Method 1/8: Hamming Distance...")
        results["method_results"]["hamming"] = self._hamming_analysis()
        
        # Method 2: Spectral Similarity
        print("Method 2/8: Spectral Similarity...")
        results["method_results"]["spectral"] = self._spectral_analysis()
        
        # Method 3: Information-Theoretic (KL Divergence)
        print("Method 3/8: Information-Theoretic Distance...")
        results["method_results"]["kl_divergence"] = self._kl_analysis()
        
        # Method 4: Topological Similarity
        print("Method 4/8: Topological Similarity...")
        results["method_results"]["topological"] = self._topological_analysis()
        
        # Method 5: Coherence-Aware Matching
        print("Method 5/8: Coherence-Aware Matching...")
        results["method_results"]["coherence_aware"] = self._coherence_aware_analysis()
        
        # Method 6: Graph-Based Similarity
        print("Method 6/8: Graph-Based Similarity...")
        results["method_results"]["graph_based"] = self._graph_analysis()
        
        # Method 7: Frequency Domain Analysis
        print("Method 7/8: Frequency Domain Analysis...")
        results["method_results"]["frequency_domain"] = self._frequency_analysis()
        
        # Method 8: Multi-Scale (Wavelet) Analysis
        print("Method 8/8: Multi-Scale Wavelet Analysis...")
        results["method_results"]["wavelet"] = self._wavelet_analysis()
        
        # Cross-method correlation
        print("\nComputing cross-method correlations...")
        results["cross_correlations"] = self._compute_cross_correlations(results["method_results"])
        
        # Find consensus clusters
        print("Finding consensus clusters...")
        results["consensus_clusters"] = self._find_consensus_clusters(results["method_results"])
        
        print()
        print("=" * 80)
        print("Full HexDictionary Analysis Complete")
        print("=" * 80)
        
        return results
    
    def _hamming_analysis(self) -> Dict[str, Any]:
        """Hamming distance analysis."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                # Convert to hex representation (simplified)
                hex1 = hex(hash(bt1) & 0xFFFFFFFF)[2:]
                hex2 = hex(hash(bt2) & 0xFFFFFFFF)[2:]
                
                dist = hamming_distance(hex1, hex2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _spectral_analysis(self) -> Dict[str, Any]:
        """Spectral similarity analysis."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                dist = spectral_distance(features1, features2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _kl_analysis(self) -> Dict[str, Any]:
        """KL divergence analysis."""
        divergences = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                div = kl_divergence(features1, features2)
                divergences[f"{bt1}-{bt2}"] = div
        
        return {
            "divergences": divergences,
            "mean": sum(divergences.values()) / len(divergences),
            "min": min(divergences.values()),
            "max": max(divergences.values()),
        }
    
    def _topological_analysis(self) -> Dict[str, Any]:
        """Topological similarity using persistence diagrams."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                pers1 = compute_persistence_diagram(features1)
                pers2 = compute_persistence_diagram(features2)
                
                dist = persistence_distance(pers1, pers2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _coherence_aware_analysis(self) -> Dict[str, Any]:
        """Coherence-aware distance metric."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                field1 = create_coherence_field(bt1)
                field2 = create_coherence_field(bt2)
                
                dist = coherence_weighted_distance(field1, field2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _graph_analysis(self) -> Dict[str, Any]:
        """Graph-based similarity."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                # Create adjacency matrices from features
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                # Simple adjacency: connect if difference < threshold
                adj1 = self._create_adjacency_matrix(features1)
                adj2 = self._create_adjacency_matrix(features2)
                
                dist = graph_edit_distance(adj1, adj2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _frequency_analysis(self) -> Dict[str, Any]:
        """Frequency domain analysis."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                dist = frequency_domain_distance(features1, features2)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _wavelet_analysis(self) -> Dict[str, Any]:
        """Multi-scale wavelet analysis."""
        distances = {}
        
        for i, bt1 in enumerate(self.blood_types):
            for bt2 in self.blood_types[i+1:]:
                features1 = get_numerical_features(bt1)
                features2 = get_numerical_features(bt2)
                
                dist = wavelet_distance(features1, features2, levels=3)
                distances[f"{bt1}-{bt2}"] = dist
        
        return {
            "distances": distances,
            "mean": sum(distances.values()) / len(distances),
            "min": min(distances.values()),
            "max": max(distances.values()),
        }
    
    def _create_adjacency_matrix(self, features: List[float]) -> List[List[int]]:
        """Create adjacency matrix from features."""
        n = len(features)
        adj = [[0 for _ in range(n)] for _ in range(n)]
        
        # Normalize features
        max_val = max(abs(f) for f in features) if features else 1.0
        norm_features = [f / max_val for f in features] if max_val > 0 else features
        
        # Connect if difference < threshold
        threshold = 0.3
        for i in range(n):
            for j in range(i+1, n):
                if abs(norm_features[i] - norm_features[j]) < threshold:
                    adj[i][j] = 1
                    adj[j][i] = 1
        
        return adj
    
    def _compute_cross_correlations(self, method_results: Dict[str, Any]) -> Dict[str, float]:
        """Compute correlations between different methods."""
        correlations = {}
        
        methods = list(method_results.keys())
        
        for i, method1 in enumerate(methods):
            for method2 in methods[i+1:]:
                # Get distance/divergence values
                values1 = list(method_results[method1].get("distances", method_results[method1].get("divergences", {})).values())
                values2 = list(method_results[method2].get("distances", method_results[method2].get("divergences", {})).values())
                
                if len(values1) == len(values2) and len(values1) > 0:
                    # Pearson correlation
                    mean1 = sum(values1) / len(values1)
                    mean2 = sum(values2) / len(values2)
                    
                    cov = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2)) / len(values1)
                    std1 = math.sqrt(sum((v1 - mean1)**2 for v1 in values1) / len(values1))
                    std2 = math.sqrt(sum((v2 - mean2)**2 for v2 in values2) / len(values2))
                    
                    corr = cov / (std1 * std2) if std1 > 0 and std2 > 0 else 0.0
                    correlations[f"{method1}-{method2}"] = corr
        
        return correlations
    
    def _find_consensus_clusters(self, method_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find consensus clusters across all methods."""
        # Simple clustering: find pairs that are consistently similar
        pair_scores = {}
        
        for method, results in method_results.items():
            distances = results.get("distances", results.get("divergences", {}))
            
            # Normalize to 0-1 range
            if distances:
                min_dist = min(distances.values())
                max_dist = max(distances.values())
                range_dist = max_dist - min_dist if max_dist > min_dist else 1.0
                
                for pair, dist in distances.items():
                    normalized = (dist - min_dist) / range_dist
                    if pair not in pair_scores:
                        pair_scores[pair] = []
                    pair_scores[pair].append(1.0 - normalized)  # Convert to similarity
        
        # Average similarity across methods
        consensus = {}
        for pair, scores in pair_scores.items():
            consensus[pair] = sum(scores) / len(scores)
        
        # Find most similar pairs
        sorted_pairs = sorted(consensus.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "consensus_similarities": consensus,
            "top_5_similar": sorted_pairs[:5],
            "bottom_5_similar": sorted_pairs[-5:],
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    analyzer = FullHexDictionaryAnalyzer()
    results = analyzer.analyze_all_methods()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/full_hexdictionary_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Blood types analyzed: {results['metadata']['num_types']}")
    print(f"Pairwise comparisons: {results['metadata']['num_comparisons']}")
    print(f"Methods applied: {results['metadata']['methods']}")
    print()
    print("Top 3 most similar pairs (consensus):")
    for pair, similarity in results['consensus_clusters']['top_5_similar'][:3]:
        print(f"  {pair}: {similarity:.4f}")
    print()
    print("Method correlations (sample):")
    for pair, corr in list(results['cross_correlations'].items())[:3]:
        print(f"  {pair}: {corr:.4f}")
