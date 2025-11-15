"""
================================================================================
Experiment 1: Substrate Seeding - Growing Blood Type Attractors De Novo
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

LEVEL-0 UBP STUDY: Can 8 blood-type attractors emerge spontaneously from
random coherence substrate through recursive evolution?

Hypothesis: The ABO/Rh system is not a biological classification but a
natural partition of the coherence landscape into 8 stable attractors,
determined by the Y/GLR/O geometry.

Why 8? Because 8 = 2^3, and 2 ≈ R = 1.996997 = Y × GLR_k × O_observer
"""

import sys
import os
import json
import math
import random
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5/advanced_modules')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from state import OffBit
from geometric_error_correction import restore_coherence
from field_dynamics import FieldState, FieldTopology, FieldDynamics


# ============================================================================
# SUBSTRATE SEEDING EXPERIMENT
# ============================================================================

class SubstrateSeedingExperiment:
    """
    Grow blood type attractors from random coherence soup.
    """
    
    def __init__(self, field_size: int = 1000, seed: int = 42):
        self.field_size = field_size
        self.seed = seed
        random.seed(seed)
        self.field_dynamics = FieldDynamics()
    
    def run_experiment(self, evolution_steps: int = 2000) -> Dict[str, Any]:
        """
        Main experiment: seed random field and evolve to find attractors.
        """
        print("=" * 80)
        print("Experiment 1: Substrate Seeding - Growing Blood Type Attractors")
        print("=" * 80)
        print()
        print(f"Field size: {self.field_size} coherence states")
        print(f"Evolution steps: {evolution_steps}")
        print(f"Random seed: {self.seed}")
        print()
        
        # Step 1: Initialize random coherence field
        print("Step 1: Initializing random coherence field...")
        initial_field = self._create_random_field()
        
        initial_state = FieldState(
            timestamp=CoherenceState(0.0),
            field_values=initial_field,
            topology=FieldTopology.CYCLOID,
            recursion_level=0,
            metadata={"experiment": "substrate_seeding"}
        )
        
        print(f"  Initial mean NRCI: {initial_state.mean_nrci:.6f}")
        print(f"  Initial energy: {initial_state.energy.value:.6e}")
        print()
        
        # Step 2: Apply recursive evolution with TGIC and observer binding
        print("Step 2: Applying recursive evolution with TGIC constraints...")
        evolved_field = self._evolve_with_tgic_and_observer(
            initial_field, steps=evolution_steps
        )
        
        evolved_state = FieldState(
            timestamp=CoherenceState(float(evolution_steps)),
            field_values=evolved_field,
            topology=FieldTopology.CYCLOID,
            recursion_level=evolution_steps,
        )
        
        print(f"  Final mean NRCI: {evolved_state.mean_nrci:.6f}")
        print(f"  Final energy: {evolved_state.energy.value:.6e}")
        print()
        
        # Step 3: Identify emergent attractors
        print("Step 3: Identifying emergent attractors...")
        attractors = self._identify_attractors(evolved_field)
        
        print(f"  Number of attractors found: {len(attractors)}")
        print()
        
        # Step 4: Characterize each attractor
        print("Step 4: Characterizing attractors...")
        attractor_profiles = self._characterize_attractors(attractors)
        
        # Step 5: Map to blood types (if 8 attractors found)
        print("Step 5: Mapping to blood type hypothesis...")
        blood_type_mapping = self._map_to_blood_types(attractor_profiles)
        
        results = {
            "metadata": {
                "field_size": self.field_size,
                "evolution_steps": evolution_steps,
                "seed": self.seed,
            },
            "initial_state": {
                "mean_nrci": initial_state.mean_nrci,
                "energy": initial_state.energy.value,
            },
            "evolved_state": {
                "mean_nrci": evolved_state.mean_nrci,
                "energy": evolved_state.energy.value,
            },
            "attractors": {
                "count": len(attractors),
                "profiles": attractor_profiles,
            },
            "blood_type_mapping": blood_type_mapping,
            "hypothesis_validated": len(attractors) == 8,
        }
        
        print()
        print("=" * 80)
        print("Substrate Seeding Experiment Complete")
        print("=" * 80)
        
        return results
    
    def _create_random_field(self) -> List[CoherenceState]:
        """Create random coherence field with NRCI ~ 0.5 (decoherent)."""
        field = []
        
        for _ in range(self.field_size):
            # Random value
            value = random.uniform(-1.0, 1.0)
            
            # Random NRCI around 0.5 (decoherent regime)
            nrci = random.uniform(0.3, 0.7)
            log_nrci_error = math.log(1.0 - nrci)
            
            field.append(CoherenceState(value, log_nrci_error=log_nrci_error))
        
        return field
    
    def _evolve_with_tgic_and_observer(
        self, field: List[CoherenceState], steps: int
    ) -> List[CoherenceState]:
        """
        Evolve field with TGIC constraints and observer binding.
        
        Key dynamics:
        1. Toggle each state
        2. Restore coherence using Y_CONSTANT
        3. Apply observer binding (multiply by O_observer if NRCI > 0.999)
        4. Check TGIC constraints
        """
        current_field = field[:]
        
        # Evolution loop (sample every 100 steps to save time)
        sample_interval = max(1, steps // 20)
        
        for step in range(steps):
            if step % sample_interval == 0:
                mean_nrci = sum(cs.nrci for cs in current_field) / len(current_field)
                print(f"    Step {step}/{steps}: mean NRCI = {mean_nrci:.6f}")
            
            # Apply one evolution step
            new_field = []
            
            for cs in current_field:
                # 1. Toggle (simulate state change)
                toggled = cs * CoherenceState(-1.0)  # Simple toggle
                
                # 2. Restore coherence
                restored, details = restore_coherence(toggled)
                
                # 3. Observer binding (only if high coherence)
                if restored.nrci > 0.999:
                    observed = restored * CoherenceState(Y_INVERSE)  # Multiply by O_observer
                else:
                    observed = restored
                
                # 4. Y-refinement
                refined = observed * CoherenceState(Y)
                
                new_field.append(refined)
            
            current_field = new_field
        
        return current_field
    
    def _identify_attractors(self, field: List[CoherenceState]) -> List[Dict[str, Any]]:
        """
        Identify stable attractors in the evolved field using clustering.
        
        Attractors are regions of high NRCI with similar values.
        """
        # Extract values and NRCIs
        values = [cs.value for cs in field]
        nrcis = [cs.nrci for cs in field]
        
        # Simple clustering: group by value ranges
        # Sort by value
        sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
        
        # Find clusters (gaps in value space)
        attractors = []
        current_cluster = [sorted_indices[0]]
        
        for i in range(1, len(sorted_indices)):
            idx = sorted_indices[i]
            prev_idx = sorted_indices[i-1]
            
            # Check if gap is large
            gap = abs(values[idx] - values[prev_idx])
            
            if gap > 0.5:  # Threshold for new cluster
                # Save current cluster
                if len(current_cluster) > 10:  # Minimum cluster size
                    attractors.append({
                        "indices": current_cluster,
                        "size": len(current_cluster),
                    })
                current_cluster = [idx]
            else:
                current_cluster.append(idx)
        
        # Save last cluster
        if len(current_cluster) > 10:
            attractors.append({
                "indices": current_cluster,
                "size": len(current_cluster),
            })
        
        return attractors
    
    def _characterize_attractors(self, attractors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Characterize each attractor."""
        profiles = []
        
        for i, attractor in enumerate(attractors):
            indices = attractor["indices"]
            
            # Compute statistics
            values = [self.field_dynamics.recursive_evolution([CoherenceState(float(idx))], depth=1)[0].value for idx in indices[:10]]
            nrcis = [self.field_dynamics.recursive_evolution([CoherenceState(float(idx))], depth=1)[0].nrci for idx in indices[:10]]
            
            mean_value = sum(values) / len(values) if values else 0.0
            mean_nrci = sum(nrcis) / len(nrcis) if nrcis else 0.0
            
            # Calculate δ-deficit
            delta_deficit = 1.0 - mean_nrci
            
            profiles.append({
                "attractor_id": i,
                "size": attractor["size"],
                "mean_value": mean_value,
                "mean_nrci": mean_nrci,
                "delta_deficit": delta_deficit,
            })
        
        return profiles
    
    def _map_to_blood_types(self, attractor_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Map attractors to blood types if 8 are found.
        
        Hypothesis:
        - O = baseline (closest to Y × Y^-1 = 1)
        - A/B = orthogonal toggles (+1, -1)
        - AB = superposition
        - Rh± = parity bit
        """
        if len(attractor_profiles) != 8:
            return {
                "mapping_possible": False,
                "reason": f"Expected 8 attractors, found {len(attractor_profiles)}",
            }
        
        # Sort by mean_value
        sorted_profiles = sorted(attractor_profiles, key=lambda x: x["mean_value"])
        
        # Hypothetical mapping (simplified)
        blood_types = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
        
        mapping = {}
        for i, profile in enumerate(sorted_profiles):
            mapping[blood_types[i]] = {
                "attractor_id": profile["attractor_id"],
                "mean_value": profile["mean_value"],
                "mean_nrci": profile["mean_nrci"],
                "delta_deficit": profile["delta_deficit"],
            }
        
        return {
            "mapping_possible": True,
            "mapping": mapping,
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    experiment = SubstrateSeedingExperiment(field_size=1000, seed=42)
    results = experiment.run_experiment(evolution_steps=100)  # Reduced for speed
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/experiment_1_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Attractors found: {results['attractors']['count']}")
    print(f"Hypothesis (8 attractors): {'VALIDATED' if results['hypothesis_validated'] else 'NOT VALIDATED'}")
    print()
    
    if results['blood_type_mapping']['mapping_possible']:
        print("Blood Type Mapping:")
        for bt, data in results['blood_type_mapping']['mapping'].items():
            print(f"  {bt:4s}: δ={data['delta_deficit']:.6f}, NRCI={data['mean_nrci']:.6f}")
    else:
        print(f"Mapping not possible: {results['blood_type_mapping']['reason']}")
