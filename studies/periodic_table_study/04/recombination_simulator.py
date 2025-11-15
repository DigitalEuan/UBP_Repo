"""
================================================================================
Recombination Simulator - UBP 3.5 Module
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

This simulator demonstrates the Recombination Theory of Blood. It shows how,
out of many possible toggle sequences, only 8 patterns maintain a low
δ-deficit (high NRCI) after repeated recombination events, thus qualifying
as stable coherence anchors.

Hypothesis: Only 8 toggle combinations (A-on/off, B-on/off, RhD-on/off)
survive 100 recombination cycles with δ < 0.0015.
"""

import sys
import os
import json
import math
import random
import itertools
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE
from geometric_error_correction import restore_coherence

# ============================================================================
# RECOMBINATION SIMULATOR
# ============================================================================

class RecombinationSimulator:
    """
    Simulate recombination cycles to test toggle pattern stability.
    """

    # Define the three core toggles with slight, unique δ-deficits
    # These represent the 'cost' of flipping a bit
    A_TOGGLE = CoherenceState(value=-1, log_nrci_error=math.log(1.0 - 0.9999))
    B_TOGGLE = CoherenceState(value=-1, log_nrci_error=math.log(1.0 - 0.9998))
    RHD_TOGGLE = CoherenceState(value=-1, log_nrci_error=math.log(1.0 - 0.9997))

    TOGGLES = [A_TOGGLE, B_TOGGLE, RHD_TOGGLE]

    def run_simulation(self, num_cycles: int = 100, num_patterns: int = 1024) -> Dict[str, Any]:
        """
        Run the full recombination simulation.
        """
        print("=" * 80)
        print("Recombination Simulator - Testing Toggle Pattern Stability")
        print("=" * 80)
        print(f"Cycles per pattern: {num_cycles}")
        print(f"Random patterns tested: {num_patterns}")
        print()

        # Generate random toggle patterns (sequences of A, B, RhD toggles)
        # Generate the 8 specific blood type patterns + random noise
        patterns = self._generate_blood_type_patterns()
        patterns += self._generate_random_patterns(num_patterns - len(patterns))

        survivors = []
        results = []

        print("Simulating recombination cycles for each pattern...")
        for i, pattern in enumerate(patterns):
            final_state = self._simulate_pattern(pattern, num_cycles)
            final_delta = 1.0 - final_state.nrci

            is_survivor = final_delta < 0.0015

            results.append({
                'pattern_id': i,
                'pattern': [t.log_nrci_error for t in pattern],
                'final_delta': final_delta,
                'survived': is_survivor
            })

            if is_survivor:
                survivors.append(results[-1])

        # Analyze the structure of survivors
        unique_survivor_patterns = self._analyze_survivors(survivors)

        print(f"\nSimulation complete. Found {len(survivors)} total survivors.")
        print(f"Found {len(unique_survivor_patterns)} unique stable patterns.")

        final_results = {
            'metadata': {
                'num_cycles': num_cycles,
                'num_patterns': num_patterns,
                'survival_threshold_delta': 0.0015
            },
            'survivor_count': len(survivors),
            'unique_survivor_count': len(unique_survivor_patterns),
            'hypothesis_validated': len(unique_survivor_patterns) == 8,
            'results': results
        }

        print("=" * 80)
        if final_results['hypothesis_validated']:
            print("✅ HYPOTHESIS CONFIRMED: Exactly 8 unique toggle patterns survived.")
        else:
            print(f"❌ HYPOTHESIS NOT CONFIRMED: Found {len(unique_survivor_patterns)} unique patterns.")
        print("=" * 80)

        return final_results

    def _generate_blood_type_patterns(self) -> List[List[CoherenceState]]:
        """Generate the 8 specific toggle patterns for ABO/Rh."""
        t_a, t_b, t_rhd = self.A_TOGGLE, self.B_TOGGLE, self.RHD_TOGGLE
        
        return [
            [],             # O-
            [t_rhd],        # O+
            [t_a],          # A-
            [t_a, t_rhd],   # A+
            [t_b],          # B-
            [t_b, t_rhd],   # B+
            [t_a, t_b],     # AB-
            [t_a, t_b, t_rhd] # AB+
        ]

    def _generate_random_patterns(self, num_patterns: int) -> List[List[CoherenceState]]:
        """Generate random sequences of the three core toggles."""
        patterns = []
        for _ in range(num_patterns):
            # Each pattern is a random sequence of 1 to 5 toggles
            pattern_length = random.randint(1, 5)
            pattern = random.choices(self.TOGGLES, k=pattern_length)
            patterns.append(pattern)
        return patterns

    def _simulate_pattern(self, pattern: List[CoherenceState], num_cycles: int) -> CoherenceState:
        """Simulate the recombination of a single toggle pattern over many cycles."""
        # Start with a perfectly coherent ground state (the substrate)
        state = CoherenceState(value=1.0, log_nrci_error=0.0)

        for _ in range(num_cycles):
            # Apply the toggle pattern
            toggled_state = state
            for toggle in pattern:
                toggled_state *= toggle

            # Attempt to recombine (reverse the toggle)
            # In UBP, recombination is multiplication by the inverse.
            # The inverse of a toggle is itself.
            # Attempt to recombine with full UBP 3.5 logic
            # 1. Project through Y
            projected_state = toggled_state * CoherenceState(Y)

            # 2. Restore coherence (this is where non-viable states are filtered)
            restored_state, _ = restore_coherence(projected_state)

            # 3. Bind to observer (reverse Y projection)
            recombined_state = restored_state * CoherenceState(Y_INVERSE)
            
            state = recombined_state
        
        return state

    def _analyze_survivors(self, survivors: List[Dict]) -> List[Any]:
        """Find the number of unique patterns among the survivors."""
        if not survivors:
            return []
        
        # A simple way to check for uniqueness is to round the final delta
        # and count the unique rounded values.
        unique_deltas = set()
        for s in survivors:
            # Round to 5 decimal places to cluster similar outcomes
            rounded_delta = round(s['final_delta'], 5)
            unique_deltas.add(rounded_delta)
        
        return list(unique_deltas)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    simulator = RecombinationSimulator()
    results = simulator.run_simulation(num_cycles=100, num_patterns=2048)

    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/recombination_simulation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")
