"""
================================================================================
UBP 3.5 Blood Type Analysis - Coherence Substrate Study
Author: Euan Craig, New Zealand
Date: November 15, 2025
================================================================================

This module conducts a comprehensive UBP 3.5 analysis of human blood types
using the coherence substrate, Advanced HexDictionary, and full system.

Research Questions:
1. What are the coherence signatures of different blood types?
2. How do blood types resonate in the UBP bitfield space?
3. Can we explain substance affinities through geometric coherence?
4. Do blood type patterns reveal novel UBP insights?
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple, Any

# Add UBP 3.5 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from hex_dictionary_advanced import (
    hamming_distance,
    spectral_distance,
    kl_divergence,
    coherence_weighted_distance,
    frequency_domain_distance,
    wavelet_distance,
    compute_persistence_diagram,
    persistence_distance,
)
from soc_energy import SOCCalculator

# Import blood type data
sys.path.insert(0, '/home/ubuntu/blood_type_ubp_study')
from blood_type_data import (
    BLOOD_TYPES,
    BLOOD_TYPE_BITFIELDS,
    SUBSTANCE_AFFINITIES,
    get_numerical_features,
    get_substance_affinity_vector,
    bitfield_to_binary_string,
)


# ============================================================================
# COHERENCE STATE CONVERSION
# ============================================================================

def blood_type_to_coherence_states(blood_type: str) -> List[CoherenceState]:
    """
    Convert blood type properties to coherence states.
    
    This is the foundation of UBP analysis - every property becomes
    a CoherenceState that carries its own quality measure.
    """
    features = get_numerical_features(blood_type)
    
    # Convert each feature to a CoherenceState
    coherence_states = []
    for i, value in enumerate(features):
        # Initialize with high coherence (NRCI ≈ 0.999997)
        state = CoherenceState(value)
        coherence_states.append(state)
    
    return coherence_states


def bitfield_to_coherence_state(bitfield: int) -> CoherenceState:
    """
    Convert bitfield to a single coherence state.
    
    The bitfield represents the discrete structure, which we map
    to the continuous coherence substrate.
    """
    # Normalize bitfield to [0, 1] range
    max_bitfield = 0xFF  # 8 bits
    normalized_value = bitfield / max_bitfield
    
    return CoherenceState(normalized_value)


# ============================================================================
# Y-REFINEMENT ANALYSIS
# ============================================================================

def analyze_y_refinement_closure(blood_type: str, levels: int = 5) -> Dict[str, Any]:
    """
    Test Y-refinement closure for blood type properties.
    
    Key Question: Do blood type properties exhibit Y-refinement closure?
    This would suggest they are fundamental geometric structures.
    """
    coherence_states = blood_type_to_coherence_states(blood_type)
    
    results = {
        "blood_type": blood_type,
        "initial_nrci": [s.nrci for s in coherence_states],
        "refinement_paths": [],
        "closure_errors": [],
        "geometric_stability": [],
    }
    
    for i, state in enumerate(coherence_states):
        # Forward refinement path
        forward_path = [state]
        current = state
        for _ in range(levels):
            current = current.refine_forward()
            forward_path.append(current)
        
        # Backward refinement to test closure
        backward_path = [forward_path[-1]]
        current = forward_path[-1]
        for _ in range(levels):
            current = current.refine_backward()
            backward_path.append(current)
        
        # Test closure
        final_state = backward_path[-1]
        closure_error = abs(final_state.value - state.value) / abs(state.value) if state.value != 0 else 0
        
        # Geometric stability: NRCI degradation over round trip
        nrci_degradation = state.nrci - final_state.nrci
        
        results["refinement_paths"].append({
            "feature_index": i,
            "forward": [s.value for s in forward_path],
            "backward": [s.value for s in backward_path],
            "forward_nrci": [s.nrci for s in forward_path],
            "backward_nrci": [s.nrci for s in backward_path],
        })
        
        results["closure_errors"].append(closure_error)
        results["geometric_stability"].append(nrci_degradation)
    
    # Overall metrics
    results["mean_closure_error"] = sum(results["closure_errors"]) / len(results["closure_errors"])
    results["max_closure_error"] = max(results["closure_errors"])
    results["mean_stability"] = sum(results["geometric_stability"]) / len(results["geometric_stability"])
    
    return results


# ============================================================================
# SOC ENERGY ANALYSIS
# ============================================================================

def calculate_blood_type_soc_energy(blood_type: str) -> Dict[str, Any]:
    """
    Calculate Simplified Observer Coherence (SOC) energy for blood type.
    
    SOC energy represents the "cost" of observing/maintaining this blood type
    in the UBP framework.
    """
    coherence_states = blood_type_to_coherence_states(blood_type)
    
    # Calculate SOC energy for the entire blood type profile
    # Use SOC calculator with coherence states
    calc = SOCCalculator()
    # Convert coherence states to weights and modes for SOC calculation
    weights = [1.0] * len(coherence_states)
    modes = [state.value for state in coherence_states]
    modal_sum = calc.calculate_modal_sum(weights, modes)
    total_energy_result = calc.calculate_soc_energy(modal_sum)
    total_energy = total_energy_result.energy_cu
    
    # Per-feature energy
    feature_energies = []
    for state in coherence_states:
        result = calc.calculate_soc_energy(state.value)
        feature_energies.append(result.energy_cu)
    
    return {
        "blood_type": blood_type,
        "total_soc_energy": total_energy,
        "feature_energies": feature_energies,
        "mean_feature_energy": sum(feature_energies) / len(feature_energies),
        "energy_nrci": total_energy_result.nrci,
    }


# ============================================================================
# ADVANCED HEXDICTIONARY SIMILARITY ANALYSIS
# ============================================================================

def analyze_blood_type_similarities(method: str = "all") -> Dict[str, Any]:
    """
    Analyze blood type similarities using Advanced HexDictionary methods.
    
    Methods available:
    - hamming: Traditional bit-level distance
    - spectral: Eigenvalue-based pattern matching
    - kl_divergence: Information-theoretic distance
    - coherence: NRCI-weighted distance
    - frequency: FFT-based pattern matching
    - wavelet: Multi-scale analysis
    - topological: Persistent homology
    """
    blood_types = list(BLOOD_TYPES.keys())
    
    results = {
        "method": method,
        "similarity_matrices": {},
        "nearest_neighbors": {},
        "clustering_structure": {},
    }
    
    # Prepare data for each blood type
    blood_type_data = {}
    for bt in blood_types:
        blood_type_data[bt] = {
            "features": get_numerical_features(bt),
            "coherence_states": blood_type_to_coherence_states(bt),
            "bitfield": BLOOD_TYPE_BITFIELDS[bt],
            "affinities": get_substance_affinity_vector(bt),
        }
    
    # Calculate similarity matrices for different methods
    methods_to_test = []
    if method == "all":
        methods_to_test = ["hamming", "spectral", "kl_divergence", "coherence", "frequency", "wavelet", "topological"]
    else:
        methods_to_test = [method]
    
    for m in methods_to_test:
        similarity_matrix = {}
        
        for bt1 in blood_types:
            similarity_matrix[bt1] = {}
            
            for bt2 in blood_types:
                if m == "hamming":
                    # Bitfield distance
                    bf1 = BLOOD_TYPE_BITFIELDS[bt1]
                    bf2 = BLOOD_TYPE_BITFIELDS[bt2]
                    hex1 = format(bf1, '02x')
                    hex2 = format(bf2, '02x')
                    distance = hamming_distance(hex1, hex2)
                    similarity = 1.0 / (1.0 + distance)
                
                elif m == "spectral":
                    features1 = blood_type_data[bt1]["features"]
                    features2 = blood_type_data[bt2]["features"]
                    distance = spectral_distance(features1, features2)
                    similarity = 1.0 / (1.0 + distance)
                
                elif m == "kl_divergence":
                    features1 = blood_type_data[bt1]["features"]
                    features2 = blood_type_data[bt2]["features"]
                    distance = kl_divergence(features1, features2)
                    similarity = 1.0 / (1.0 + distance) if distance != float('inf') else 0.0
                
                elif m == "coherence":
                    states1 = blood_type_data[bt1]["coherence_states"]
                    states2 = blood_type_data[bt2]["coherence_states"]
                    distance = coherence_weighted_distance(states1, states2)
                    similarity = 1.0 / (1.0 + distance)
                
                elif m == "frequency":
                    features1 = blood_type_data[bt1]["features"]
                    features2 = blood_type_data[bt2]["features"]
                    distance = frequency_domain_distance(features1, features2)
                    similarity = 1.0 / (1.0 + distance)
                
                elif m == "wavelet":
                    features1 = blood_type_data[bt1]["features"]
                    features2 = blood_type_data[bt2]["features"]
                    distance = wavelet_distance(features1, features2)
                    similarity = 1.0 / (1.0 + distance)
                
                elif m == "topological":
                    features1 = blood_type_data[bt1]["features"]
                    features2 = blood_type_data[bt2]["features"]
                    pers1 = compute_persistence_diagram(features1)
                    pers2 = compute_persistence_diagram(features2)
                    distance = persistence_distance(pers1, pers2)
                    similarity = 1.0 / (1.0 + distance) if distance != float('inf') else 0.0
                
                similarity_matrix[bt1][bt2] = similarity
        
        results["similarity_matrices"][m] = similarity_matrix
        
        # Find nearest neighbors for each blood type
        nearest_neighbors = {}
        for bt in blood_types:
            similarities = [(other_bt, similarity_matrix[bt][other_bt]) 
                          for other_bt in blood_types if other_bt != bt]
            similarities.sort(key=lambda x: x[1], reverse=True)
            nearest_neighbors[bt] = similarities[:3]  # Top 3 neighbors
        
        results["nearest_neighbors"][m] = nearest_neighbors
    
    return results


# ============================================================================
# BITFIELD RESONANCE ANALYSIS
# ============================================================================

def analyze_bitfield_resonance() -> Dict[str, Any]:
    """
    Analyze how blood type bitfields resonate in UBP space.
    
    Key Questions:
    - Do certain bit patterns have higher coherence?
    - Are there geometric relationships between bitfields?
    - Do bitfields correlate with substance affinities?
    """
    results = {
        "bitfield_coherence": {},
        "bit_pattern_analysis": {},
        "hamming_weight_correlation": {},
        "geometric_relationships": [],
    }
    
    # Analyze each bitfield
    for bt, bitfield in BLOOD_TYPE_BITFIELDS.items():
        # Convert to coherence state
        coherence_state = bitfield_to_coherence_state(bitfield)
        
        # Hamming weight (number of 1s)
        hamming_weight = bin(bitfield).count('1')
        
        # Binary representation
        binary = bitfield_to_binary_string(bitfield)
        
        results["bitfield_coherence"][bt] = {
            "bitfield": bitfield,
            "binary": binary,
            "hamming_weight": hamming_weight,
            "coherence_value": coherence_state.value,
            "nrci": coherence_state.nrci,
        }
    
    # Analyze bit patterns
    bit_positions = 8
    for bit_pos in range(bit_positions):
        mask = 1 << bit_pos
        blood_types_with_bit = [bt for bt, bf in BLOOD_TYPE_BITFIELDS.items() if bf & mask]
        blood_types_without_bit = [bt for bt, bf in BLOOD_TYPE_BITFIELDS.items() if not (bf & mask)]
        
        results["bit_pattern_analysis"][f"bit_{bit_pos}"] = {
            "with_bit": blood_types_with_bit,
            "without_bit": blood_types_without_bit,
            "count_with": len(blood_types_with_bit),
            "count_without": len(blood_types_without_bit),
        }
    
    # Hamming weight correlation with properties
    hamming_weights = [results["bitfield_coherence"][bt]["hamming_weight"] for bt in BLOOD_TYPES.keys()]
    frequencies = [BLOOD_TYPES[bt]["frequency_global"] for bt in BLOOD_TYPES.keys()]
    
    # Simple correlation
    mean_hw = sum(hamming_weights) / len(hamming_weights)
    mean_freq = sum(frequencies) / len(frequencies)
    
    covariance = sum((hw - mean_hw) * (freq - mean_freq) 
                    for hw, freq in zip(hamming_weights, frequencies)) / len(hamming_weights)
    
    std_hw = math.sqrt(sum((hw - mean_hw)**2 for hw in hamming_weights) / len(hamming_weights))
    std_freq = math.sqrt(sum((freq - mean_freq)**2 for freq in frequencies) / len(frequencies))
    
    correlation = covariance / (std_hw * std_freq) if std_hw > 0 and std_freq > 0 else 0
    
    results["hamming_weight_correlation"] = {
        "correlation_with_frequency": correlation,
        "interpretation": "positive" if correlation > 0 else "negative",
    }
    
    # Geometric relationships (XOR distance)
    for i, bt1 in enumerate(BLOOD_TYPES.keys()):
        for bt2 in list(BLOOD_TYPES.keys())[i+1:]:
            bf1 = BLOOD_TYPE_BITFIELDS[bt1]
            bf2 = BLOOD_TYPE_BITFIELDS[bt2]
            
            xor_distance = bin(bf1 ^ bf2).count('1')
            
            # Check if they differ by exactly 1 bit (adjacent in Hamming space)
            if xor_distance == 1:
                results["geometric_relationships"].append({
                    "pair": [bt1, bt2],
                    "xor_distance": xor_distance,
                    "relationship": "adjacent",
                    "differing_bit": (bf1 ^ bf2).bit_length() - 1,
                })
    
    return results


# ============================================================================
# MAIN ANALYSIS RUNNER
# ============================================================================

def run_comprehensive_analysis() -> Dict[str, Any]:
    """
    Run comprehensive UBP analysis on all blood types.
    """
    print("=" * 80)
    print("UBP 3.5 Blood Type Analysis - Comprehensive Study")
    print("=" * 80)
    print()
    
    all_results = {
        "metadata": {
            "ubp_version": "3.5",
            "coherence_substrate": True,
            "advanced_hexdictionary": True,
            "blood_types_analyzed": len(BLOOD_TYPES),
        },
        "y_refinement_analysis": {},
        "soc_energy_analysis": {},
        "similarity_analysis": {},
        "bitfield_resonance": {},
    }
    
    # 1. Y-Refinement Closure Analysis
    print("Phase 1: Y-Refinement Closure Analysis")
    print("-" * 80)
    for bt in BLOOD_TYPES.keys():
        print(f"  Analyzing {bt}...")
        results = analyze_y_refinement_closure(bt, levels=5)
        all_results["y_refinement_analysis"][bt] = results
        print(f"    Mean closure error: {results['mean_closure_error']:.2e}")
        print(f"    Max closure error: {results['max_closure_error']:.2e}")
    print()
    
    # 2. SOC Energy Analysis
    print("Phase 2: SOC Energy Analysis")
    print("-" * 80)
    for bt in BLOOD_TYPES.keys():
        print(f"  Analyzing {bt}...")
        results = calculate_blood_type_soc_energy(bt)
        all_results["soc_energy_analysis"][bt] = results
        print(f"    Total SOC energy: {results['total_soc_energy']:.6f}")
        print(f"    Mean feature energy: {results['mean_feature_energy']:.6f}")
    print()
    
    # 3. Advanced HexDictionary Similarity Analysis
    print("Phase 3: Advanced HexDictionary Similarity Analysis")
    print("-" * 80)
    similarity_results = analyze_blood_type_similarities(method="all")
    all_results["similarity_analysis"] = similarity_results
    print("  Completed similarity analysis with 7 methods")
    print()
    
    # 4. Bitfield Resonance Analysis
    print("Phase 4: Bitfield Resonance Analysis")
    print("-" * 80)
    bitfield_results = analyze_bitfield_resonance()
    all_results["bitfield_resonance"] = bitfield_results
    print(f"  Analyzed {len(BLOOD_TYPE_BITFIELDS)} bitfield patterns")
    print(f"  Found {len(bitfield_results['geometric_relationships'])} adjacent pairs")
    print()
    
    print("=" * 80)
    print("Analysis Complete")
    print("=" * 80)
    
    return all_results


if __name__ == "__main__":
    results = run_comprehensive_analysis()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study/analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
