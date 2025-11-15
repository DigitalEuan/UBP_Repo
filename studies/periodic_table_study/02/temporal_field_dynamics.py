"""
================================================================================
Temporal Dynamics and Field Evolution Analysis - UBP 3.5
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

Complete temporal dynamics analysis using:
- Recursive field evolution
- Zitterbewegung modeling
- Temporal alignment
- Coherence substrate integration
"""

import sys
import os
import json
import math
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5/advanced_modules')
sys.path.insert(0, '/home/ubuntu/blood_type_ubp_study_v2')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from field_dynamics import (
    FieldState,
    FieldTopology,
    EvolutionMode,
    FieldDynamics,
)
from blood_type_data_extended import (
    get_all_blood_types,
    get_numerical_features,
    get_temporal_properties,
    create_coherence_field,
)


# ============================================================================
# TEMPORAL DYNAMICS ANALYZER
# ============================================================================

class BloodTypeTemporalAnalyzer:
    """
    Analyze blood type temporal dynamics using full UBP 3.5 field dynamics.
    """
    
    def __init__(self):
        self.blood_types = get_all_blood_types()
        self.field_dynamics = FieldDynamics()
        self.results = {}
    
    def analyze_all_temporal_dynamics(self) -> Dict[str, Any]:
        """
        Run complete temporal dynamics analysis on all blood types.
        """
        print("=" * 80)
        print("Temporal Dynamics and Field Evolution Analysis - UBP 3.5")
        print("=" * 80)
        print()
        
        results = {
            "metadata": {
                "blood_types": self.blood_types,
                "num_types": len(self.blood_types),
                "analysis_methods": [
                    "recursive_evolution",
                    "zitterbewegung",
                    "temporal_alignment",
                    "field_energy",
                ],
            },
            "blood_type_dynamics": {},
        }
        
        for bt in self.blood_types:
            print(f"Analyzing {bt}...")
            results["blood_type_dynamics"][bt] = self._analyze_single_blood_type(bt)
        
        # Cross-type comparisons
        print("\nComputing cross-type temporal correlations...")
        results["temporal_correlations"] = self._compute_temporal_correlations(
            results["blood_type_dynamics"]
        )
        
        # Find resonance patterns
        print("Finding resonance patterns...")
        results["resonance_patterns"] = self._find_resonance_patterns(
            results["blood_type_dynamics"]
        )
        
        print()
        print("=" * 80)
        print("Temporal Dynamics Analysis Complete")
        print("=" * 80)
        
        return results
    
    def _analyze_single_blood_type(self, blood_type: str) -> Dict[str, Any]:
        """Analyze temporal dynamics for a single blood type."""
        # Get blood type data
        temporal_props = get_temporal_properties(blood_type)
        coherence_field = create_coherence_field(blood_type)
        
        # Create initial field state
        initial_state = FieldState(
            timestamp=CoherenceState(0.0),
            field_values=coherence_field,
            topology=FieldTopology.CYCLOID,
            recursion_level=0,
            metadata={"blood_type": blood_type}
        )
        
        results = {
            "initial_state": {
                "mean_nrci": initial_state.mean_nrci,
                "energy": initial_state.energy.value,
                "field_size": initial_state.size,
            },
            "temporal_properties": temporal_props,
        }
        
        # 1. Recursive Evolution
        print(f"  - Recursive evolution...")
        evolution_depth = 5
        evolved_field = self.field_dynamics.recursive_evolution(
            coherence_field, depth=evolution_depth
        )
        
        evolved_state = FieldState(
            timestamp=CoherenceState(0.0),
            field_values=evolved_field,
            topology=FieldTopology.CYCLOID,
            recursion_level=evolution_depth,
        )
        
        results["recursive_evolution"] = {
            "depth": evolution_depth,
            "final_mean_nrci": evolved_state.mean_nrci,
            "final_energy": evolved_state.energy.value,
            "nrci_change": evolved_state.mean_nrci - initial_state.mean_nrci,
            "energy_change": evolved_state.energy.value - initial_state.energy.value,
        }
        
        # 2. Zitterbewegung Analysis
        print(f"  - Zitterbewegung dynamics...")
        # Use membrane oscillation frequency
        osc_freq = temporal_props["oscillation_freq"]
        
        # Short duration zitterbewegung (10 cycles)
        zitter_duration = 10.0 / osc_freq if osc_freq > 0 else 1e-9
        
        try:
            zitter_states = self.field_dynamics.zitterbewegung_evolution(
                initial_state, duration=zitter_duration
            )
            
            # Analyze zitterbewegung oscillation
            energies = [s.energy.value for s in zitter_states]
            nrcis = [s.mean_nrci for s in zitter_states]
            
            results["zitterbewegung"] = {
                "duration": zitter_duration,
                "num_states": len(zitter_states),
                "energy_oscillation_amplitude": (max(energies) - min(energies)) / 2.0,
                "mean_energy": sum(energies) / len(energies),
                "nrci_stability": max(nrcis) - min(nrcis),
                "characteristic_frequency": osc_freq,
            }
        except Exception as e:
            results["zitterbewegung"] = {
                "error": str(e),
                "characteristic_frequency": osc_freq,
            }
        
        # 3. Field Energy Analysis
        print(f"  - Field energy...")
        results["field_energy"] = {
            "initial": initial_state.energy.value,
            "initial_nrci": initial_state.energy.nrci,
            "evolved": evolved_state.energy.value,
            "evolved_nrci": evolved_state.energy.nrci,
        }
        
        # 4. Temporal Stability
        print(f"  - Temporal stability...")
        # Measure how stable the field is under evolution
        stability_metric = abs(evolved_state.mean_nrci - initial_state.mean_nrci)
        
        results["temporal_stability"] = {
            "nrci_stability": stability_metric,
            "is_stable": stability_metric < 0.001,  # Threshold for stability
            "turnover_rate": temporal_props["turnover_rate"],
        }
        
        return results
    
    def _compute_temporal_correlations(
        self, blood_type_dynamics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute correlations between blood types in temporal space."""
        correlations = {}
        
        blood_types = list(blood_type_dynamics.keys())
        
        for i, bt1 in enumerate(blood_types):
            for bt2 in blood_types[i+1:]:
                # Compare temporal properties
                props1 = blood_type_dynamics[bt1]["temporal_properties"]
                props2 = blood_type_dynamics[bt2]["temporal_properties"]
                
                # Frequency correlation
                freq_diff = abs(
                    props1["oscillation_freq"] - props2["oscillation_freq"]
                )
                
                # Energy evolution correlation
                energy1 = blood_type_dynamics[bt1]["recursive_evolution"]["energy_change"]
                energy2 = blood_type_dynamics[bt2]["recursive_evolution"]["energy_change"]
                energy_corr = 1.0 / (1.0 + abs(energy1 - energy2))
                
                # NRCI evolution correlation
                nrci1 = blood_type_dynamics[bt1]["recursive_evolution"]["nrci_change"]
                nrci2 = blood_type_dynamics[bt2]["recursive_evolution"]["nrci_change"]
                nrci_corr = 1.0 / (1.0 + abs(nrci1 - nrci2) * 1000)
                
                correlations[f"{bt1}-{bt2}"] = {
                    "frequency_difference": freq_diff,
                    "energy_correlation": energy_corr,
                    "nrci_correlation": nrci_corr,
                    "overall_correlation": (energy_corr + nrci_corr) / 2.0,
                }
        
        return correlations
    
    def _find_resonance_patterns(
        self, blood_type_dynamics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Find resonance patterns across blood types."""
        # Group by similar oscillation frequencies
        freq_groups = {}
        
        for bt, dynamics in blood_type_dynamics.items():
            freq = dynamics["temporal_properties"]["oscillation_freq"]
            
            # Round to nearest 0.1 GHz
            freq_ghz = freq / 1e9
            freq_key = round(freq_ghz, 1)
            
            if freq_key not in freq_groups:
                freq_groups[freq_key] = []
            freq_groups[freq_key].append(bt)
        
        # Find energy resonances
        energy_patterns = {}
        for bt, dynamics in blood_type_dynamics.items():
            energy = dynamics["field_energy"]["initial"]
            energy_key = f"{energy:.2e}"
            
            if energy_key not in energy_patterns:
                energy_patterns[energy_key] = []
            energy_patterns[energy_key].append(bt)
        
        return {
            "frequency_groups": freq_groups,
            "energy_patterns": energy_patterns,
            "num_frequency_groups": len(freq_groups),
            "num_energy_patterns": len(energy_patterns),
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    analyzer = BloodTypeTemporalAnalyzer()
    results = analyzer.analyze_all_temporal_dynamics()
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/temporal_dynamics_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Blood types analyzed: {results['metadata']['num_types']}")
    print()
    print("Temporal Stability:")
    for bt in results['blood_type_dynamics'].keys():
        stability = results['blood_type_dynamics'][bt]['temporal_stability']
        status = "STABLE" if stability['is_stable'] else "UNSTABLE"
        print(f"  {bt:4s}: {status} (NRCI change: {stability['nrci_stability']:.6f})")
    print()
    print(f"Frequency groups found: {results['resonance_patterns']['num_frequency_groups']}")
    print(f"Energy patterns found: {results['resonance_patterns']['num_energy_patterns']}")
