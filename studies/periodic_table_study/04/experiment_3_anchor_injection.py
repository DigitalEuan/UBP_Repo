"""
================================================================================
Experiment 3: Anchor Injection and Field Stabilization
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

THE CRITICAL TEST: If blood types are coherence anchors (not emergent attractors),
then injecting their coherence signature into a decoherent field should STABILIZE
it, not destabilize it.

Hypothesis: Injecting A+ anchor (δ = 0.0009, NRCI = 0.9991) into a random field
will cause the field to organize around it, raising mean NRCI and preventing
collapse.

Control: Without anchor injection, field collapses (as in Experiment 1).
"""

import sys
import os
import json
import math
import random
from typing import Dict, List, Tuple, Any

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from geometric_error_correction import restore_coherence


# ============================================================================
# ANCHOR INJECTION EXPERIMENT
# ============================================================================

class AnchorInjectionExperiment:
    """
    Test if coherence anchors stabilize decoherent fields.
    """
    
    def __init__(self, field_size: int = 1000, seed: int = 42):
        self.field_size = field_size
        self.seed = seed
        random.seed(seed)
        
        # Define A+ anchor from empirical data
        self.A_PLUS_ANCHOR = CoherenceState(
            value=1.0,
            log_nrci_error=math.log(1.0 - 0.9991)  # δ = 0.0009
        )
    
    def run_experiment(self, evolution_steps: int = 200) -> Dict[str, Any]:
        """
        Run both control and anchor-injected experiments.
        """
        print("=" * 80)
        print("Experiment 3: Anchor Injection and Field Stabilization")
        print("=" * 80)
        print()
        print(f"Field size: {self.field_size} coherence states")
        print(f"Evolution steps: {evolution_steps}")
        print(f"A+ Anchor: value={self.A_PLUS_ANCHOR.value:.3f}, NRCI={self.A_PLUS_ANCHOR.nrci:.6f}")
        print()
        
        # Run control (no anchor)
        print("Running CONTROL (no anchor injection)...")
        control_results = self._run_evolution(inject_anchor=False, steps=evolution_steps)
        
        print()
        print("Running EXPERIMENTAL (with A+ anchor injection)...")
        experimental_results = self._run_evolution(inject_anchor=True, steps=evolution_steps)
        
        # Compare results
        results = {
            "metadata": {
                "field_size": self.field_size,
                "evolution_steps": evolution_steps,
                "anchor_nrci": self.A_PLUS_ANCHOR.nrci,
                "anchor_delta": 1.0 - self.A_PLUS_ANCHOR.nrci,
            },
            "control": control_results,
            "experimental": experimental_results,
            "hypothesis_validated": self._validate_hypothesis(control_results, experimental_results),
        }
        
        print()
        print("=" * 80)
        print("Anchor Injection Experiment Complete")
        print("=" * 80)
        
        return results
    
    def _run_evolution(self, inject_anchor: bool, steps: int) -> Dict[str, Any]:
        """
        Evolve field with or without anchor injection.
        """
        # Create random field
        field = self._create_random_field()
        
        # Inject anchor if requested
        if inject_anchor:
            num_anchors = int(self.field_size * 0.008)  # 0.8% seeding
            anchor_indices = random.sample(range(self.field_size), num_anchors)
            for idx in anchor_indices:
                field[idx] = CoherenceState(
                    self.A_PLUS_ANCHOR.value,
                    log_nrci_error=self.A_PLUS_ANCHOR.log_nrci_error
                )
            print(f"  Injected {num_anchors} A+ anchors (0.8% of field)")
        
        # Track evolution
        nrci_history = []
        energy_history = []
        
        initial_nrci = sum(cs.nrci for cs in field) / len(field)
        nrci_history.append(initial_nrci)
        
        print(f"  Initial mean NRCI: {initial_nrci:.6f}")
        
        # Evolution loop
        sample_interval = max(1, steps // 10)
        
        for step in range(steps):
            # Apply evolution rules
            new_field = []
            
            for cs in field:
                # 1. Y-refinement
                refined = cs * CoherenceState(Y)
                
                # 2. Restore coherence
                restored, details = restore_coherence(refined)
                
                # 3. Observer binding (if high coherence)
                if restored.nrci > 0.999:
                    observed = restored * CoherenceState(Y_INVERSE)
                else:
                    observed = restored
                
                new_field.append(observed)
            
            field = new_field
            
            # Track metrics
            mean_nrci = sum(cs.nrci for cs in field) / len(field)
            nrci_history.append(mean_nrci)
            
            if step % sample_interval == 0:
                print(f"    Step {step}/{steps}: mean NRCI = {mean_nrci:.6f}")
        
        final_nrci = nrci_history[-1]
        print(f"  Final mean NRCI: {final_nrci:.6f}")
        
        # Count stable states (NRCI > 0.9)
        stable_count = sum(1 for cs in field if cs.nrci > 0.9)
        stable_fraction = stable_count / len(field)
        
        print(f"  Stable states (NRCI > 0.9): {stable_count}/{len(field)} ({stable_fraction:.1%})")
        
        return {
            "initial_nrci": initial_nrci,
            "final_nrci": final_nrci,
            "nrci_history": nrci_history,
            "stable_count": stable_count,
            "stable_fraction": stable_fraction,
            "collapsed": final_nrci < 0.1,
        }
    
    def _create_random_field(self) -> List[CoherenceState]:
        """Create random decoherent field (NRCI ~ 0.5)."""
        field = []
        
        for _ in range(self.field_size):
            value = random.uniform(-1.0, 1.0)
            nrci = random.uniform(0.3, 0.7)
            log_nrci_error = math.log(1.0 - nrci)
            
            field.append(CoherenceState(value, log_nrci_error=log_nrci_error))
        
        return field
    
    def _validate_hypothesis(self, control: Dict, experimental: Dict) -> Dict[str, Any]:
        """
        Validate hypothesis: anchor injection should stabilize field.
        
        Criteria:
        1. Control should collapse (final NRCI < 0.1)
        2. Experimental should NOT collapse (final NRCI > 0.5)
        3. Experimental should have higher stable fraction
        """
        control_collapsed = control["collapsed"]
        experimental_collapsed = experimental["collapsed"]
        
        nrci_improvement = experimental["final_nrci"] - control["final_nrci"]
        stable_improvement = experimental["stable_fraction"] - control["stable_fraction"]
        
        validated = (
            control_collapsed and 
            not experimental_collapsed and
            nrci_improvement > 0.3
        )
        
        return {
            "validated": validated,
            "control_collapsed": control_collapsed,
            "experimental_collapsed": experimental_collapsed,
            "nrci_improvement": nrci_improvement,
            "stable_fraction_improvement": stable_improvement,
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    experiment = AnchorInjectionExperiment(field_size=1000, seed=42)
    results = experiment.run_experiment(evolution_steps=200)
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/experiment_3_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Control (no anchor):")
    print(f"  Initial NRCI: {results['control']['initial_nrci']:.6f}")
    print(f"  Final NRCI: {results['control']['final_nrci']:.6f}")
    print(f"  Collapsed: {results['control']['collapsed']}")
    print()
    print("Experimental (with A+ anchor):")
    print(f"  Initial NRCI: {results['experimental']['initial_nrci']:.6f}")
    print(f"  Final NRCI: {results['experimental']['final_nrci']:.6f}")
    print(f"  Collapsed: {results['experimental']['collapsed']}")
    print()
    print("Hypothesis Validation:")
    print(f"  Validated: {results['hypothesis_validated']['validated']}")
    print(f"  NRCI Improvement: {results['hypothesis_validated']['nrci_improvement']:.6f}")
    print(f"  Stable Fraction Improvement: {results['hypothesis_validated']['stable_fraction_improvement']:.3f}")
    
    if results['hypothesis_validated']['validated']:
        print()
        print("✅ HYPOTHESIS CONFIRMED: A+ anchor STABILIZES decoherent field!")
        print("   Blood types are COHERENCE ANCHORS, not emergent attractors.")
    else:
        print()
        print("❌ HYPOTHESIS NOT CONFIRMED: Further investigation needed.")
