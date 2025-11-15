"""
================================================================================
Experiment 2: δ-Resonance Scan - Finding Fixed Points and Attractor Count
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

LEVEL-0 UBP STUDY: Is δ = 0.0009 a fixed point? At what δ-deficit do we
observe exactly 8 attractors?

Hypothesis: The number of stable attractors is a function of δ-deficit.
At δ ≈ 0.0009, the substrate naturally partitions into 8 stable states.
"""

import sys
import os
import json
import math
import random
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET


# ============================================================================
# δ-RESONANCE SCAN EXPERIMENT
# ============================================================================

class DeltaResonanceScanExperiment:
    """
    Scan δ-deficit space to find attractor count as a function of δ.
    """
    
    def __init__(self, field_size: int = 500, seed: int = 42):
        self.field_size = field_size
        self.seed = seed
        random.seed(seed)
    
    def run_experiment(
        self, 
        delta_min: float = 1e-6,
        delta_max: float = 0.1,
        num_samples: int = 50
    ) -> Dict[str, Any]:
        """
        Scan δ-deficit space to find attractor count.
        """
        print("=" * 80)
        print("Experiment 2: δ-Resonance Scan - Finding Fixed Points")
        print("=" * 80)
        print()
        print(f"Field size: {self.field_size} coherence states")
        print(f"δ-deficit range: {delta_min:.2e} to {delta_max:.2e}")
        print(f"Number of samples: {num_samples}")
        print()
        
        # Generate δ values (logarithmic spacing)
        delta_values = [
            delta_min * (delta_max / delta_min) ** (i / (num_samples - 1))
            for i in range(num_samples)
        ]
        
        results = {
            "metadata": {
                "field_size": self.field_size,
                "delta_min": delta_min,
                "delta_max": delta_max,
                "num_samples": num_samples,
            },
            "scan_results": [],
        }
        
        print("Scanning δ-deficit space...")
        print()
        
        for i, delta in enumerate(delta_values):
            print(f"  Sample {i+1}/{num_samples}: δ = {delta:.6e}", end="")
            
            # Create field with target δ-deficit
            field = self._create_field_with_delta(delta)
            
            # Evolve field
            evolved_field = self._evolve_field(field, steps=50)
            
            # Count attractors
            attractor_count = self._count_attractors(evolved_field)
            
            # Calculate mean NRCI
            mean_nrci = sum(cs.nrci for cs in evolved_field) / len(evolved_field)
            
            print(f" → {attractor_count} attractors, mean NRCI = {mean_nrci:.6f}")
            
            results["scan_results"].append({
                "delta": delta,
                "attractor_count": attractor_count,
                "mean_nrci": mean_nrci,
            })
        
        # Find δ values that produce 8 attractors
        eight_attractor_deltas = [
            r["delta"] for r in results["scan_results"] 
            if r["attractor_count"] == 8
        ]
        
        results["eight_attractor_deltas"] = eight_attractor_deltas
        results["hypothesis_validated"] = len(eight_attractor_deltas) > 0
        
        if eight_attractor_deltas:
            results["optimal_delta"] = eight_attractor_deltas[len(eight_attractor_deltas)//2]
        else:
            results["optimal_delta"] = None
        
        print()
        print("=" * 80)
        print("δ-Resonance Scan Complete")
        print("=" * 80)
        
        return results
    
    def _create_field_with_delta(self, target_delta: float) -> List[CoherenceState]:
        """
        Create coherence field with specific target δ-deficit.
        
        δ = 1 - NRCI, so NRCI = 1 - δ
        """
        target_nrci = 1.0 - target_delta
        
        field = []
        for _ in range(self.field_size):
            # Random value
            value = random.uniform(-1.0, 1.0)
            
            # Set NRCI to target (with small random variation)
            nrci = target_nrci + random.uniform(-0.001, 0.001)
            nrci = max(0.0, min(1.0, nrci))  # Clamp to [0, 1]
            
            log_nrci_error = math.log(1.0 - nrci) if nrci < 1.0 else -1e10
            
            field.append(CoherenceState(value, log_nrci_error=log_nrci_error))
        
        return field
    
    def _evolve_field(self, field: List[CoherenceState], steps: int) -> List[CoherenceState]:
        """
        Evolve field using Y-refinement and observer binding.
        """
        current_field = field[:]
        
        for _ in range(steps):
            new_field = []
            
            for cs in current_field:
                # Y-refinement
                refined = cs * CoherenceState(Y)
                
                # Observer binding (if high coherence)
                if refined.nrci > 0.999:
                    observed = refined * CoherenceState(Y_INVERSE)
                else:
                    observed = refined
                
                new_field.append(observed)
            
            current_field = new_field
        
        return current_field
    
    def _count_attractors(self, field: List[CoherenceState]) -> int:
        """
        Count number of distinct attractors in field.
        
        Attractors are clusters of similar values with high NRCI.
        """
        # Extract values
        values = [cs.value for cs in field if cs.nrci > 0.9]
        
        if not values:
            return 0
        
        # Sort values
        sorted_values = sorted(values)
        
        # Count clusters (gaps > 0.3)
        clusters = 1
        for i in range(1, len(sorted_values)):
            if sorted_values[i] - sorted_values[i-1] > 0.3:
                clusters += 1
        
        return clusters


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    experiment = DeltaResonanceScanExperiment(field_size=500, seed=42)
    results = experiment.run_experiment(
        delta_min=1e-6,
        delta_max=0.1,
        num_samples=50
    )
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/experiment_2_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"δ values producing 8 attractors: {len(results['eight_attractor_deltas'])}")
    
    if results['hypothesis_validated']:
        print(f"Optimal δ for 8 attractors: {results['optimal_delta']:.6e}")
    else:
        print("No δ value produced exactly 8 attractors")
    
    # Show attractor count distribution
    print("\nAttractor Count Distribution:")
    attractor_counts = {}
    for r in results['scan_results']:
        count = r['attractor_count']
        if count not in attractor_counts:
            attractor_counts[count] = 0
        attractor_counts[count] += 1
    
    for count in sorted(attractor_counts.keys()):
        print(f"  {count} attractors: {attractor_counts[count]} samples")
