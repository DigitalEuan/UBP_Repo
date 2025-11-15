"""
================================================================================
Bitfield Resonance Deep Analysis - Blood Types in UBP Space
Author: Euan Craig, New Zealand
Date: November 15, 2025
================================================================================

This module performs deep analysis of how blood type bitfields resonate
in UBP geometric space, exploring:
- Hamming space geometry
- Coherence field patterns
- Bitfield-to-substance affinity correlations
- Novel resonance discoveries
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple, Any

# Add UBP 3.5 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET

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
# BITFIELD GEOMETRY ANALYSIS
# ============================================================================

def analyze_hamming_cube_structure() -> Dict[str, Any]:
    """
    Analyze blood types as vertices in an 8-dimensional Hamming cube.
    
    Key insights:
    - Blood types occupy specific positions in binary space
    - Hamming distance represents minimum bit flips between types
    - Geometric relationships may correlate with biological compatibility
    """
    results = {
        "vertices": {},
        "edges": [],
        "hamming_distances": {},
        "cube_dimension": 8,
        "occupied_vertices": len(BLOOD_TYPE_BITFIELDS),
        "total_possible_vertices": 2**8,
    }
    
    # Map each blood type to its position in Hamming cube
    for bt, bitfield in BLOOD_TYPE_BITFIELDS.items():
        hamming_weight = bin(bitfield).count('1')
        binary = bitfield_to_binary_string(bitfield)
        
        results["vertices"][bt] = {
            "bitfield": bitfield,
            "binary": binary,
            "hamming_weight": hamming_weight,
            "coordinates": [int(b) for b in binary],
        }
    
    # Calculate all pairwise Hamming distances
    blood_types = list(BLOOD_TYPE_BITFIELDS.keys())
    for i, bt1 in enumerate(blood_types):
        results["hamming_distances"][bt1] = {}
        
        for bt2 in blood_types:
            bf1 = BLOOD_TYPE_BITFIELDS[bt1]
            bf2 = BLOOD_TYPE_BITFIELDS[bt2]
            
            # Hamming distance = number of differing bits
            hamming_dist = bin(bf1 ^ bf2).count('1')
            results["hamming_distances"][bt1][bt2] = hamming_dist
            
            # Record edges (adjacent vertices)
            if hamming_dist == 1 and bt1 < bt2:  # Avoid duplicates
                differing_bit = (bf1 ^ bf2).bit_length() - 1
                results["edges"].append({
                    "pair": [bt1, bt2],
                    "hamming_distance": hamming_dist,
                    "differing_bit": differing_bit,
                })
    
    return results


def analyze_bitfield_coherence_field() -> Dict[str, Any]:
    """
    Map bitfields to coherence substrate and analyze the resulting field.
    
    Each bitfield becomes a point in coherence space, and we analyze
    the geometric structure of this field.
    """
    results = {
        "coherence_points": {},
        "field_statistics": {},
        "y_refinement_patterns": {},
    }
    
    # Convert each bitfield to coherence state
    coherence_points = {}
    for bt, bitfield in BLOOD_TYPE_BITFIELDS.items():
        # Normalize to [0, 1]
        normalized = bitfield / 255.0
        coherence_state = CoherenceState(normalized)
        
        coherence_points[bt] = {
            "value": coherence_state.value,
            "nrci": coherence_state.nrci,
            "log_nrci_error": coherence_state.log_nrci_error,
        }
        
        # Apply Y-refinement and observe behavior
        refined_forward = coherence_state.refine_forward()
        refined_backward = coherence_state.refine_backward()
        
        results["y_refinement_patterns"][bt] = {
            "original": coherence_state.value,
            "forward": refined_forward.value,
            "backward": refined_backward.value,
            "forward_nrci": refined_forward.nrci,
            "backward_nrci": refined_backward.nrci,
        }
    
    results["coherence_points"] = coherence_points
    
    # Field statistics
    values = [cp["value"] for cp in coherence_points.values()]
    nrcis = [cp["nrci"] for cp in coherence_points.values()]
    
    results["field_statistics"] = {
        "mean_value": sum(values) / len(values),
        "std_value": math.sqrt(sum((v - sum(values)/len(values))**2 for v in values) / len(values)),
        "min_value": min(values),
        "max_value": max(values),
        "mean_nrci": sum(nrcis) / len(nrcis),
        "min_nrci": min(nrcis),
        "max_nrci": max(nrcis),
    }
    
    return results


def analyze_bitfield_substance_correlation() -> Dict[str, Any]:
    """
    Analyze correlation between bitfield patterns and substance affinities.
    
    KEY RESEARCH QUESTION: Do specific bit patterns correlate with
    specific substance affinities? This could reveal geometric origins
    of biochemical interactions.
    """
    results = {
        "correlations": {},
        "bit_position_analysis": {},
        "pattern_discoveries": [],
    }
    
    blood_types = list(BLOOD_TYPES.keys())
    
    # For each substance, analyze correlation with bitfield patterns
    for substance_name, substance_data in SUBSTANCE_AFFINITIES.items():
        if not isinstance(substance_data, dict):
            continue
        
        # Get affinity values for each blood type
        affinities = []
        bitfields = []
        
        for bt in blood_types:
            abo_group = bt.rstrip('+-')
            if abo_group in substance_data:
                affinities.append(substance_data[abo_group])
                bitfields.append(BLOOD_TYPE_BITFIELDS[bt])
        
        if len(affinities) < 2:
            continue
        
        # Calculate correlation between bitfield value and affinity
        mean_affinity = sum(affinities) / len(affinities)
        mean_bitfield = sum(bitfields) / len(bitfields)
        
        covariance = sum((a - mean_affinity) * (b - mean_bitfield) 
                        for a, b in zip(affinities, bitfields)) / len(affinities)
        
        std_affinity = math.sqrt(sum((a - mean_affinity)**2 for a in affinities) / len(affinities))
        std_bitfield = math.sqrt(sum((b - mean_bitfield)**2 for b in bitfields) / len(bitfields))
        
        correlation = covariance / (std_affinity * std_bitfield) if std_affinity > 0 and std_bitfield > 0 else 0
        
        results["correlations"][substance_name] = {
            "correlation": correlation,
            "strength": "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.4 else "weak",
            "direction": "positive" if correlation > 0 else "negative",
        }
        
        # Analyze individual bit positions
        bit_analysis = {}
        for bit_pos in range(8):
            mask = 1 << bit_pos
            
            # Separate blood types by this bit
            with_bit = [affinities[i] for i, bf in enumerate(bitfields) if bf & mask]
            without_bit = [affinities[i] for i, bf in enumerate(bitfields) if not (bf & mask)]
            
            if with_bit and without_bit:
                mean_with = sum(with_bit) / len(with_bit)
                mean_without = sum(without_bit) / len(without_bit)
                difference = mean_with - mean_without
                
                bit_analysis[f"bit_{bit_pos}"] = {
                    "mean_with_bit": mean_with,
                    "mean_without_bit": mean_without,
                    "difference": difference,
                    "significant": abs(difference) > 0.2,
                }
        
        results["bit_position_analysis"][substance_name] = bit_analysis
    
    # Identify pattern discoveries
    for substance, corr_data in results["correlations"].items():
        if corr_data["strength"] in ["strong", "moderate"]:
            results["pattern_discoveries"].append({
                "substance": substance,
                "correlation": corr_data["correlation"],
                "interpretation": f"{substance} shows {corr_data['strength']} {corr_data['direction']} correlation with bitfield values",
            })
    
    return results


def analyze_bitfield_y_resonance() -> Dict[str, Any]:
    """
    Analyze how bitfield values resonate with Y-constant.
    
    Do certain bitfield patterns align better with Y-refinement geometry?
    """
    results = {
        "y_alignment": {},
        "resonance_scores": {},
        "optimal_bitfields": [],
    }
    
    for bt, bitfield in BLOOD_TYPE_BITFIELDS.items():
        # Normalize bitfield
        normalized = bitfield / 255.0
        
        # Calculate "distance" from Y-constant
        y_distance = abs(normalized - Y)
        y_inv_distance = abs(normalized - Y_INVERSE)
        
        # Calculate resonance score (inverse of distance)
        y_resonance = 1.0 / (1.0 + y_distance)
        y_inv_resonance = 1.0 / (1.0 + y_inv_distance)
        
        # Combined resonance
        combined_resonance = (y_resonance + y_inv_resonance) / 2.0
        
        results["y_alignment"][bt] = {
            "normalized_bitfield": normalized,
            "y_distance": y_distance,
            "y_inv_distance": y_inv_distance,
            "y_resonance": y_resonance,
            "y_inv_resonance": y_inv_resonance,
            "combined_resonance": combined_resonance,
        }
        
        results["resonance_scores"][bt] = combined_resonance
    
    # Find optimal bitfields (highest resonance)
    sorted_by_resonance = sorted(results["resonance_scores"].items(), 
                                 key=lambda x: x[1], reverse=True)
    
    results["optimal_bitfields"] = [
        {
            "blood_type": bt,
            "resonance": score,
            "bitfield": BLOOD_TYPE_BITFIELDS[bt],
            "binary": bitfield_to_binary_string(BLOOD_TYPE_BITFIELDS[bt]),
        }
        for bt, score in sorted_by_resonance[:3]
    ]
    
    return results


# ============================================================================
# MAIN ANALYSIS RUNNER
# ============================================================================

def run_bitfield_deep_analysis() -> Dict[str, Any]:
    """
    Run comprehensive bitfield resonance analysis.
    """
    print("=" * 80)
    print("Bitfield Resonance Deep Analysis")
    print("=" * 80)
    print()
    
    all_results = {
        "metadata": {
            "analysis_type": "bitfield_resonance",
            "ubp_version": "3.5",
        },
        "hamming_cube": {},
        "coherence_field": {},
        "substance_correlation": {},
        "y_resonance": {},
    }
    
    # 1. Hamming Cube Structure
    print("Phase 1: Hamming Cube Structure Analysis")
    print("-" * 80)
    hamming_results = analyze_hamming_cube_structure()
    all_results["hamming_cube"] = hamming_results
    print(f"  Occupied vertices: {hamming_results['occupied_vertices']}/{hamming_results['total_possible_vertices']}")
    print(f"  Adjacent pairs (edges): {len(hamming_results['edges'])}")
    print()
    
    # 2. Coherence Field Analysis
    print("Phase 2: Coherence Field Analysis")
    print("-" * 80)
    coherence_results = analyze_bitfield_coherence_field()
    all_results["coherence_field"] = coherence_results
    print(f"  Mean field value: {coherence_results['field_statistics']['mean_value']:.6f}")
    print(f"  Field std dev: {coherence_results['field_statistics']['std_value']:.6f}")
    print(f"  Mean NRCI: {coherence_results['field_statistics']['mean_nrci']:.6f}")
    print()
    
    # 3. Substance Correlation Analysis
    print("Phase 3: Bitfield-Substance Correlation Analysis")
    print("-" * 80)
    correlation_results = analyze_bitfield_substance_correlation()
    all_results["substance_correlation"] = correlation_results
    print(f"  Substances analyzed: {len(correlation_results['correlations'])}")
    print(f"  Pattern discoveries: {len(correlation_results['pattern_discoveries'])}")
    for discovery in correlation_results['pattern_discoveries'][:5]:
        print(f"    - {discovery['interpretation']}")
    print()
    
    # 4. Y-Resonance Analysis
    print("Phase 4: Y-Resonance Analysis")
    print("-" * 80)
    y_resonance_results = analyze_bitfield_y_resonance()
    all_results["y_resonance"] = y_resonance_results
    print(f"  Optimal resonance blood types:")
    for optimal in y_resonance_results['optimal_bitfields']:
        print(f"    {optimal['blood_type']:4s}: resonance = {optimal['resonance']:.6f}, binary = {optimal['binary']}")
    print()
    
    print("=" * 80)
    print("Bitfield Analysis Complete")
    print("=" * 80)
    
    return all_results


if __name__ == "__main__":
    results = run_bitfield_deep_analysis()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study/bitfield_resonance_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
