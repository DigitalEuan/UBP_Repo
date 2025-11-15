"""
================================================================================
Substance Affinity UBP Analysis - Geometric Origins of Biochemical Interactions
Author: Euan Craig, New Zealand
Date: November 15, 2025
================================================================================

This module investigates the deep question:
"Why do some blood types have affinity with some substances and not others?"

From the UBP perspective, we explore:
1. Coherence matching between blood type and substance
2. Geometric resonance patterns
3. Y-refinement alignment
4. Information-theoretic explanations
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
    coherence_weighted_distance,
    spectral_distance,
    frequency_domain_distance,
)

# Import blood type data
sys.path.insert(0, '/home/ubuntu/blood_type_ubp_study')
from blood_type_data import (
    BLOOD_TYPES,
    BLOOD_TYPE_BITFIELDS,
    SUBSTANCE_AFFINITIES,
    get_numerical_features,
    get_substance_affinity_vector,
)


# ============================================================================
# COHERENCE MATCHING ANALYSIS
# ============================================================================

def analyze_coherence_matching() -> Dict[str, Any]:
    """
    Analyze if substance affinities correlate with coherence state similarity.
    
    Hypothesis: Blood types with similar coherence profiles should have
    similar substance affinities.
    """
    results = {
        "coherence_affinity_correlation": {},
        "predictions": {},
        "validation": {},
    }
    
    blood_types = list(BLOOD_TYPES.keys())
    
    # Convert each blood type to coherence states
    coherence_profiles = {}
    affinity_profiles = {}
    
    for bt in blood_types:
        features = get_numerical_features(bt)
        coherence_states = [CoherenceState(f) for f in features]
        coherence_profiles[bt] = coherence_states
        
        affinities = get_substance_affinity_vector(bt)
        affinity_profiles[bt] = affinities
    
    # For each pair of blood types, calculate:
    # 1. Coherence distance
    # 2. Affinity profile distance
    # 3. Correlation between them
    
    coherence_distances = []
    affinity_distances = []
    
    for i, bt1 in enumerate(blood_types):
        for bt2 in blood_types[i+1:]:
            # Coherence distance
            coh_dist = coherence_weighted_distance(
                coherence_profiles[bt1],
                coherence_profiles[bt2]
            )
            
            # Affinity distance (Euclidean)
            aff1 = affinity_profiles[bt1]
            aff2 = affinity_profiles[bt2]
            
            if len(aff1) == len(aff2):
                aff_dist = math.sqrt(sum((a1 - a2)**2 for a1, a2 in zip(aff1, aff2)))
                
                coherence_distances.append(coh_dist)
                affinity_distances.append(aff_dist)
    
    # Calculate correlation
    if coherence_distances and affinity_distances:
        mean_coh = sum(coherence_distances) / len(coherence_distances)
        mean_aff = sum(affinity_distances) / len(affinity_distances)
        
        covariance = sum((c - mean_coh) * (a - mean_aff) 
                        for c, a in zip(coherence_distances, affinity_distances)) / len(coherence_distances)
        
        std_coh = math.sqrt(sum((c - mean_coh)**2 for c in coherence_distances) / len(coherence_distances))
        std_aff = math.sqrt(sum((a - mean_aff)**2 for a in affinity_distances) / len(affinity_distances))
        
        correlation = covariance / (std_coh * std_aff) if std_coh > 0 and std_aff > 0 else 0
        
        results["coherence_affinity_correlation"] = {
            "correlation": correlation,
            "p_value_estimate": 1.0 - abs(correlation),  # Rough estimate
            "interpretation": "Coherence similarity predicts affinity similarity" if correlation > 0.5 else "Weak correlation",
            "strength": "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.4 else "weak",
        }
    
    return results


def analyze_substance_specific_resonance() -> Dict[str, Any]:
    """
    For each substance, analyze its resonance pattern across blood types.
    
    Key Question: Do substances with similar affinity patterns have
    similar geometric signatures?
    """
    results = {
        "substance_resonance_profiles": {},
        "geometric_clusters": [],
        "novel_insights": [],
    }
    
    for substance_name, substance_data in SUBSTANCE_AFFINITIES.items():
        if not isinstance(substance_data, dict):
            continue
        
        # Get affinity pattern
        affinity_pattern = []
        for abo_group in ["O", "A", "B", "AB"]:
            if abo_group in substance_data:
                affinity_pattern.append(substance_data[abo_group])
        
        if len(affinity_pattern) < 4:
            continue
        
        # Convert to coherence states
        coherence_pattern = [CoherenceState(a) for a in affinity_pattern]
        
        # Calculate pattern statistics
        mean_affinity = sum(affinity_pattern) / len(affinity_pattern)
        std_affinity = math.sqrt(sum((a - mean_affinity)**2 for a in affinity_pattern) / len(affinity_pattern))
        
        # Calculate "selectivity" - how much the substance discriminates
        selectivity = std_affinity / mean_affinity if mean_affinity > 0 else 0
        
        # Y-refinement analysis
        refined_pattern = [cs.refine_forward() for cs in coherence_pattern]
        refined_values = [cs.value for cs in refined_pattern]
        
        # Check if Y-refinement preserves pattern structure
        original_range = max(affinity_pattern) - min(affinity_pattern)
        refined_range = max(refined_values) - min(refined_values)
        
        pattern_preservation = 1.0 - abs(refined_range - original_range * Y) / (original_range * Y) if original_range > 0 else 1.0
        
        results["substance_resonance_profiles"][substance_name] = {
            "affinity_pattern": affinity_pattern,
            "mean_affinity": mean_affinity,
            "std_affinity": std_affinity,
            "selectivity": selectivity,
            "pattern_preservation_under_y": pattern_preservation,
            "interpretation": "Highly selective" if selectivity > 0.5 else "Moderately selective" if selectivity > 0.3 else "Non-selective",
        }
        
        # Identify novel insights
        if selectivity > 0.5 and pattern_preservation > 0.9:
            results["novel_insights"].append({
                "substance": substance_name,
                "insight": f"{substance_name} shows high selectivity ({selectivity:.2f}) with strong Y-refinement preservation ({pattern_preservation:.2f})",
                "implication": "Geometric origin of selectivity - pattern is Y-stable",
            })
    
    return results


def analyze_affinity_y_alignment() -> Dict[str, Any]:
    """
    Analyze if substance affinities align with Y-constant multiples.
    
    Hypothesis: Affinities that are multiples of Y or Y_INVERSE may
    represent fundamental geometric relationships.
    """
    results = {
        "y_aligned_affinities": [],
        "y_inverse_aligned_affinities": [],
        "geometric_ratios": {},
    }
    
    # Tolerance for Y-alignment
    tolerance = 0.05
    
    for substance_name, substance_data in SUBSTANCE_AFFINITIES.items():
        if not isinstance(substance_data, dict):
            continue
        
        for abo_group, affinity in substance_data.items():
            # Skip non-numeric values
            if not isinstance(affinity, (int, float)):
                continue
            if affinity == 0:
                continue
            
            # Check alignment with Y
            y_multiple = affinity / Y
            y_remainder = y_multiple - round(y_multiple)
            
            if abs(y_remainder) < tolerance:
                results["y_aligned_affinities"].append({
                    "substance": substance_name,
                    "blood_group": abo_group,
                    "affinity": affinity,
                    "y_multiple": round(y_multiple),
                    "error": abs(y_remainder),
                })
            
            # Check alignment with Y_INVERSE
            y_inv_multiple = affinity / Y_INVERSE
            y_inv_remainder = y_inv_multiple - round(y_inv_multiple)
            
            if abs(y_inv_remainder) < tolerance:
                results["y_inverse_aligned_affinities"].append({
                    "substance": substance_name,
                    "blood_group": abo_group,
                    "affinity": affinity,
                    "y_inverse_multiple": round(y_inv_multiple),
                    "error": abs(y_inv_remainder),
                })
    
    # Analyze geometric ratios between affinities
    for substance_name, substance_data in SUBSTANCE_AFFINITIES.items():
        if not isinstance(substance_data, dict):
            continue
        
        ratios = {}
        abo_groups = ["O", "A", "B", "AB"]
        
        for i, group1 in enumerate(abo_groups):
            if group1 not in substance_data:
                continue
            
            for group2 in abo_groups[i+1:]:
                if group2 not in substance_data:
                    continue
                
                aff1 = substance_data[group1]
                aff2 = substance_data[group2]
                
                if aff2 != 0:
                    ratio = aff1 / aff2
                    
                    # Check if ratio is close to Y or Y_INVERSE
                    if abs(ratio - Y) < tolerance:
                        ratios[f"{group1}/{group2}"] = {
                            "ratio": ratio,
                            "type": "Y",
                            "error": abs(ratio - Y),
                        }
                    elif abs(ratio - Y_INVERSE) < tolerance:
                        ratios[f"{group1}/{group2}"] = {
                            "ratio": ratio,
                            "type": "Y_INVERSE",
                            "error": abs(ratio - Y_INVERSE),
                        }
        
        if ratios:
            results["geometric_ratios"][substance_name] = ratios
    
    return results


def analyze_affinity_coherence_substrate() -> Dict[str, Any]:
    """
    Map substance affinities to coherence substrate and analyze emergent patterns.
    """
    results = {
        "coherence_mapping": {},
        "nrci_patterns": {},
        "emergent_clusters": [],
    }
    
    # Map each substance's affinity profile to coherence space
    for substance_name, substance_data in SUBSTANCE_AFFINITIES.items():
        if not isinstance(substance_data, dict):
            continue
        
        affinity_values = []
        for abo_group in ["O", "A", "B", "AB"]:
            if abo_group in substance_data:
                affinity_values.append(substance_data[abo_group])
        
        if len(affinity_values) < 4:
            continue
        
        # Convert to coherence states
        coherence_states = [CoherenceState(a) for a in affinity_values]
        
        # Calculate aggregate NRCI
        mean_nrci = sum(cs.nrci for cs in coherence_states) / len(coherence_states)
        
        # Calculate coherence "spread"
        values = [cs.value for cs in coherence_states]
        mean_value = sum(values) / len(values)
        spread = math.sqrt(sum((v - mean_value)**2 for v in values) / len(values))
        
        results["coherence_mapping"][substance_name] = {
            "affinity_values": affinity_values,
            "mean_nrci": mean_nrci,
            "coherence_spread": spread,
            "nrci_values": [cs.nrci for cs in coherence_states],
        }
        
        # Analyze NRCI patterns
        nrci_values = [cs.nrci for cs in coherence_states]
        nrci_std = math.sqrt(sum((n - mean_nrci)**2 for n in nrci_values) / len(nrci_values))
        
        results["nrci_patterns"][substance_name] = {
            "mean_nrci": mean_nrci,
            "nrci_std": nrci_std,
            "uniformity": 1.0 - nrci_std,  # High uniformity = low std
        }
    
    return results


# ============================================================================
# MAIN ANALYSIS RUNNER
# ============================================================================

def run_substance_affinity_analysis() -> Dict[str, Any]:
    """
    Run comprehensive substance affinity analysis from UBP perspective.
    """
    print("=" * 80)
    print("Substance Affinity UBP Analysis")
    print("=" * 80)
    print()
    
    all_results = {
        "metadata": {
            "analysis_type": "substance_affinity",
            "ubp_version": "3.5",
            "research_question": "Why do blood types have different substance affinities?",
        },
        "coherence_matching": {},
        "substance_resonance": {},
        "y_alignment": {},
        "coherence_substrate_mapping": {},
    }
    
    # 1. Coherence Matching Analysis
    print("Phase 1: Coherence Matching Analysis")
    print("-" * 80)
    coherence_results = analyze_coherence_matching()
    all_results["coherence_matching"] = coherence_results
    if "coherence_affinity_correlation" in coherence_results:
        corr = coherence_results["coherence_affinity_correlation"]
        print(f"  Correlation: {corr.get('correlation', 0):.4f}")
        print(f"  Strength: {corr.get('strength', 'unknown')}")
        print(f"  Interpretation: {corr.get('interpretation', 'N/A')}")
    print()
    
    # 2. Substance-Specific Resonance
    print("Phase 2: Substance-Specific Resonance Analysis")
    print("-" * 80)
    resonance_results = analyze_substance_specific_resonance()
    all_results["substance_resonance"] = resonance_results
    print(f"  Substances analyzed: {len(resonance_results['substance_resonance_profiles'])}")
    print(f"  Novel insights: {len(resonance_results['novel_insights'])}")
    for insight in resonance_results['novel_insights'][:3]:
        print(f"    - {insight['insight']}")
    print()
    
    # 3. Y-Alignment Analysis
    print("Phase 3: Y-Alignment Analysis")
    print("-" * 80)
    y_alignment_results = analyze_affinity_y_alignment()
    all_results["y_alignment"] = y_alignment_results
    print(f"  Y-aligned affinities: {len(y_alignment_results['y_aligned_affinities'])}")
    print(f"  Y-inverse aligned affinities: {len(y_alignment_results['y_inverse_aligned_affinities'])}")
    print(f"  Geometric ratios found: {len(y_alignment_results['geometric_ratios'])}")
    print()
    
    # 4. Coherence Substrate Mapping
    print("Phase 4: Coherence Substrate Mapping")
    print("-" * 80)
    substrate_results = analyze_affinity_coherence_substrate()
    all_results["coherence_substrate_mapping"] = substrate_results
    print(f"  Substances mapped: {len(substrate_results['coherence_mapping'])}")
    
    # Find most uniform NRCI patterns
    if substrate_results['nrci_patterns']:
        sorted_by_uniformity = sorted(
            substrate_results['nrci_patterns'].items(),
            key=lambda x: x[1]['uniformity'],
            reverse=True
        )
        print(f"  Most uniform NRCI patterns:")
        for substance, data in sorted_by_uniformity[:3]:
            print(f"    {substance}: uniformity = {data['uniformity']:.4f}")
    print()
    
    print("=" * 80)
    print("Substance Affinity Analysis Complete")
    print("=" * 80)
    
    return all_results


if __name__ == "__main__":
    results = run_substance_affinity_analysis()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study/substance_affinity_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
