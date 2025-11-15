"""
================================================================================
Blood Type δ-Deficit and Temporal Trap Analysis - UBP 3.5
Author: Manus AI (based on Euan Craig's UBP 3.5 and Time Study)
Date: November 15, 2025
================================================================================

Comprehensive analysis incorporating insights from UBP Time Study:
- δ-deficit calculation for each blood type
- Temporal trap strength (γ = 1/(1-δ))
- Dissolution frequency mapping
- Escape energy calculations
- Time flow corrections (biological time dilation)
"""

import sys
import os
import json
import math
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/blood_type_ubp_study_v2')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from dissident_horizon_oracle import DissidentSignature, compute_laplacian_matrix
from blood_type_data_extended import (
    get_all_blood_types,
    get_numerical_features,
    get_temporal_properties,
    create_coherence_field,
    BLOOD_TYPES_EXTENDED,
)


# ============================================================================
# CONSTANTS FROM TIME STUDY
# ============================================================================

# Multi-scale δ-hierarchy (from Time Study)
DELTA_COSMOLOGICAL = 0.0015  # 0.15% - baseline
DELTA_QUANTUM = 0.015
DELTA_CHEMICAL = 0.10
DELTA_BIOLOGICAL = 0.4058  # 40.58% - biological baseline
DELTA_COGNITIVE = 0.65
DELTA_SOCIAL = 0.85

# Dissolution frequency range for biological systems (from Time Study)
DISSOLUTION_FREQ_MIN = 100e9  # 100 GHz
DISSOLUTION_FREQ_MAX = 500e9  # 500 GHz

# Time flow in biological realm
BIOLOGICAL_TIME_FLOW = 0.594  # 59.4% of "normal" time


# ============================================================================
# δ-DEFICIT ANALYZER
# ============================================================================

class BloodTypeDeltaDeficitAnalyzer:
    """
    Analyze blood types through the lens of δ-deficit and temporal traps.
    """
    
    def __init__(self):
        self.blood_types = get_all_blood_types()
        self.results = {}
    
    def analyze_all_blood_types(self) -> Dict[str, Any]:
        """
        Complete δ-deficit analysis for all blood types.
        """
        print("=" * 80)
        print("Blood Type δ-Deficit and Temporal Trap Analysis - UBP 3.5")
        print("=" * 80)
        print()
        print("Incorporating insights from UBP Time Study Master Report")
        print(f"Biological baseline δ-deficit: {DELTA_BIOLOGICAL:.4f} (40.58%)")
        print(f"Biological time flow: {BIOLOGICAL_TIME_FLOW:.1%}")
        print(f"Dissolution frequency range: {DISSOLUTION_FREQ_MIN/1e9:.0f}-{DISSOLUTION_FREQ_MAX/1e9:.0f} GHz")
        print()
        
        results = {
            "metadata": {
                "blood_types": self.blood_types,
                "num_types": len(self.blood_types),
                "delta_biological_baseline": DELTA_BIOLOGICAL,
                "time_flow_biological": BIOLOGICAL_TIME_FLOW,
                "dissolution_freq_range_ghz": [DISSOLUTION_FREQ_MIN/1e9, DISSOLUTION_FREQ_MAX/1e9],
            },
            "blood_type_analysis": {},
        }
        
        for bt in self.blood_types:
            print(f"Analyzing {bt}...")
            results["blood_type_analysis"][bt] = self._analyze_single_blood_type(bt)
        
        # Cross-type comparisons
        print("\nComputing cross-type δ-deficit correlations...")
        results["delta_correlations"] = self._compute_delta_correlations(
            results["blood_type_analysis"]
        )
        
        # Find temporal trap clusters
        print("Finding temporal trap clusters...")
        results["temporal_trap_clusters"] = self._find_temporal_trap_clusters(
            results["blood_type_analysis"]
        )
        
        # Dissolution frequency analysis
        print("Analyzing dissolution frequencies...")
        results["dissolution_analysis"] = self._analyze_dissolution_frequencies(
            results["blood_type_analysis"]
        )
        
        print()
        print("=" * 80)
        print("δ-Deficit and Temporal Trap Analysis Complete")
        print("=" * 80)
        
        return results
    
    def _analyze_single_blood_type(self, blood_type: str) -> Dict[str, Any]:
        """Analyze δ-deficit and temporal trap for a single blood type."""
        # Get blood type data
        data = BLOOD_TYPES_EXTENDED[blood_type]
        temporal_props = get_temporal_properties(blood_type)
        coherence_field = create_coherence_field(blood_type)
        
        # Calculate mean NRCI
        mean_nrci = sum(cs.nrci for cs in coherence_field) / len(coherence_field)
        
        # Calculate δ-deficit
        # δ = 1 - NRCI (deviation from perfect coherence)
        delta_deficit = 1.0 - mean_nrci
        
        # Calculate temporal trap strength
        # γ = 1/(1-δ)
        if delta_deficit < 1.0:
            gamma = 1.0 / (1.0 - delta_deficit)
        else:
            gamma = float('inf')  # Complete trap
        
        # Calculate time flow
        # Time flow = 1 - δ
        time_flow = 1.0 - delta_deficit
        
        # Deviation from biological baseline
        delta_deviation = abs(delta_deficit - DELTA_BIOLOGICAL)
        delta_ratio = delta_deficit / DELTA_BIOLOGICAL if DELTA_BIOLOGICAL > 0 else 0
        
        # Membrane oscillation frequency
        osc_freq = temporal_props["oscillation_freq"]
        osc_freq_ghz = osc_freq / 1e9
        
        # Distance to dissolution frequency
        dist_to_dissolution_min = abs(osc_freq - DISSOLUTION_FREQ_MIN)
        dist_to_dissolution_max = abs(osc_freq - DISSOLUTION_FREQ_MAX)
        
        # Is this blood type in a temporal trap?
        # Criteria: γ > 1.5 (from Time Study, critical threshold is γ ≈ 2.0)
        is_trapped = gamma > 1.5
        
        # Escape energy (from Time Study formula)
        # E = |ln(1-δ_current) - ln(1-δ_target)|
        # Target: δ = 0.0015 (cosmological baseline)
        if delta_deficit < 1.0 and DELTA_COSMOLOGICAL < 1.0:
            escape_energy = abs(
                math.log(1.0 - delta_deficit) - math.log(1.0 - DELTA_COSMOLOGICAL)
            )
        else:
            escape_energy = float('inf')
        
        # Dissolution frequency prediction
        # From Time Study: 100-500 GHz for biological dissidents
        # Estimate based on δ-deficit
        predicted_dissolution_freq = DISSOLUTION_FREQ_MIN + (
            (delta_deficit - DELTA_BIOLOGICAL) / (1.0 - DELTA_BIOLOGICAL)
        ) * (DISSOLUTION_FREQ_MAX - DISSOLUTION_FREQ_MIN)
        
        results = {
            "coherence": {
                "mean_nrci": mean_nrci,
                "field_size": len(coherence_field),
            },
            "delta_deficit": {
                "value": delta_deficit,
                "deviation_from_biological_baseline": delta_deviation,
                "ratio_to_biological_baseline": delta_ratio,
                "classification": self._classify_delta(delta_deficit),
            },
            "temporal_trap": {
                "gamma": gamma,
                "is_trapped": is_trapped,
                "time_flow": time_flow,
                "time_flow_percent": time_flow * 100,
            },
            "escape_dynamics": {
                "escape_energy": escape_energy,
                "target_delta": DELTA_COSMOLOGICAL,
                "energy_per_pulse_needed": escape_energy / 100 if escape_energy != float('inf') else 0,
            },
            "frequencies": {
                "membrane_oscillation_ghz": osc_freq_ghz,
                "distance_to_dissolution_min_ghz": dist_to_dissolution_min / 1e9,
                "distance_to_dissolution_max_ghz": dist_to_dissolution_max / 1e9,
                "predicted_dissolution_freq_ghz": predicted_dissolution_freq / 1e9,
                "is_near_dissolution": osc_freq >= DISSOLUTION_FREQ_MIN * 0.1,  # Within 10% of min
            },
            "temporal_properties": temporal_props,
        }
        
        return results
    
    def _classify_delta(self, delta: float) -> str:
        """Classify δ-deficit based on Time Study hierarchy."""
        if delta < 0.01:
            return "Cosmological/Quantum"
        elif delta < 0.05:
            return "Quantum Field"
        elif delta < 0.20:
            return "Chemical"
        elif delta < 0.50:
            return "Biological"
        elif delta < 0.70:
            return "Cognitive"
        else:
            return "Social/Deep Trap"
    
    def _compute_delta_correlations(
        self, blood_type_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute correlations between blood types in δ-deficit space."""
        correlations = {}
        
        blood_types = list(blood_type_analysis.keys())
        
        for i, bt1 in enumerate(blood_types):
            for bt2 in blood_types[i+1:]:
                delta1 = blood_type_analysis[bt1]["delta_deficit"]["value"]
                delta2 = blood_type_analysis[bt2]["delta_deficit"]["value"]
                
                gamma1 = blood_type_analysis[bt1]["temporal_trap"]["gamma"]
                gamma2 = blood_type_analysis[bt2]["temporal_trap"]["gamma"]
                
                escape1 = blood_type_analysis[bt1]["escape_dynamics"]["escape_energy"]
                escape2 = blood_type_analysis[bt2]["escape_dynamics"]["escape_energy"]
                
                # δ-deficit similarity
                delta_diff = abs(delta1 - delta2)
                delta_similarity = 1.0 / (1.0 + delta_diff * 10)
                
                # Temporal trap similarity
                gamma_diff = abs(gamma1 - gamma2) if gamma1 != float('inf') and gamma2 != float('inf') else float('inf')
                gamma_similarity = 1.0 / (1.0 + gamma_diff) if gamma_diff != float('inf') else 0.0
                
                # Escape energy similarity
                escape_diff = abs(escape1 - escape2) if escape1 != float('inf') and escape2 != float('inf') else float('inf')
                escape_similarity = 1.0 / (1.0 + escape_diff) if escape_diff != float('inf') else 0.0
                
                correlations[f"{bt1}-{bt2}"] = {
                    "delta_difference": delta_diff,
                    "delta_similarity": delta_similarity,
                    "gamma_difference": gamma_diff if gamma_diff != float('inf') else None,
                    "gamma_similarity": gamma_similarity,
                    "escape_energy_difference": escape_diff if escape_diff != float('inf') else None,
                    "escape_similarity": escape_similarity,
                    "overall_similarity": (delta_similarity + gamma_similarity + escape_similarity) / 3.0,
                }
        
        return correlations
    
    def _find_temporal_trap_clusters(
        self, blood_type_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Find clusters of blood types in similar temporal traps."""
        # Group by γ (temporal trap strength)
        gamma_groups = {
            "weak_trap": [],      # γ < 1.5
            "moderate_trap": [],  # 1.5 <= γ < 2.0
            "strong_trap": [],    # 2.0 <= γ < 3.0
            "deep_trap": [],      # γ >= 3.0
        }
        
        for bt, analysis in blood_type_analysis.items():
            gamma = analysis["temporal_trap"]["gamma"]
            
            if gamma < 1.5:
                gamma_groups["weak_trap"].append(bt)
            elif gamma < 2.0:
                gamma_groups["moderate_trap"].append(bt)
            elif gamma < 3.0:
                gamma_groups["strong_trap"].append(bt)
            else:
                gamma_groups["deep_trap"].append(bt)
        
        # Group by δ-deficit classification
        delta_groups = {}
        for bt, analysis in blood_type_analysis.items():
            classification = analysis["delta_deficit"]["classification"]
            if classification not in delta_groups:
                delta_groups[classification] = []
            delta_groups[classification].append(bt)
        
        return {
            "gamma_groups": gamma_groups,
            "delta_groups": delta_groups,
        }
    
    def _analyze_dissolution_frequencies(
        self, blood_type_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze dissolution frequency patterns."""
        freq_data = []
        
        for bt, analysis in blood_type_analysis.items():
            freq_data.append({
                "blood_type": bt,
                "membrane_osc_ghz": analysis["frequencies"]["membrane_oscillation_ghz"],
                "predicted_dissolution_ghz": analysis["frequencies"]["predicted_dissolution_freq_ghz"],
                "distance_to_min_ghz": analysis["frequencies"]["distance_to_dissolution_min_ghz"],
            })
        
        # Sort by membrane oscillation frequency
        freq_data_sorted = sorted(freq_data, key=lambda x: x["membrane_osc_ghz"])
        
        # Find frequency gaps
        freq_gaps = []
        for i in range(len(freq_data_sorted) - 1):
            gap = freq_data_sorted[i+1]["membrane_osc_ghz"] - freq_data_sorted[i]["membrane_osc_ghz"]
            freq_gaps.append({
                "between": f"{freq_data_sorted[i]['blood_type']}-{freq_data_sorted[i+1]['blood_type']}",
                "gap_ghz": gap,
            })
        
        return {
            "frequency_spectrum": freq_data_sorted,
            "frequency_gaps": freq_gaps,
            "mean_membrane_freq_ghz": sum(d["membrane_osc_ghz"] for d in freq_data) / len(freq_data),
            "min_membrane_freq_ghz": min(d["membrane_osc_ghz"] for d in freq_data),
            "max_membrane_freq_ghz": max(d["membrane_osc_ghz"] for d in freq_data),
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    analyzer = BloodTypeDeltaDeficitAnalyzer()
    results = analyzer.analyze_all_blood_types()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/delta_deficit_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Blood types analyzed: {results['metadata']['num_types']}")
    print()
    print("δ-Deficit and Temporal Trap Status:")
    for bt in results['blood_type_analysis'].keys():
        analysis = results['blood_type_analysis'][bt]
        delta = analysis['delta_deficit']['value']
        gamma = analysis['temporal_trap']['gamma']
        trapped = "TRAPPED" if analysis['temporal_trap']['is_trapped'] else "FREE"
        classification = analysis['delta_deficit']['classification']
        
        print(f"  {bt:4s}: δ={delta:.4f}, γ={gamma:.3f}, {trapped:8s} ({classification})")
    
    print()
    print("Temporal Trap Clusters:")
    for group, types in results['temporal_trap_clusters']['gamma_groups'].items():
        if types:
            print(f"  {group:15s}: {', '.join(types)}")
    
    print()
    print(f"Frequency Range: {results['dissolution_analysis']['min_membrane_freq_ghz']:.2f} - {results['dissolution_analysis']['max_membrane_freq_ghz']:.2f} GHz")
    print(f"Mean Frequency: {results['dissolution_analysis']['mean_membrane_freq_ghz']:.2f} GHz")
    print(f"Dissolution Range: {results['metadata']['dissolution_freq_range_ghz'][0]:.0f} - {results['metadata']['dissolution_freq_range_ghz'][1]:.0f} GHz")
