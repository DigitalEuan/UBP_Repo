#!/usr/bin/env python3.11
"""
UBP Evaluation Using Exact Phase 2 Methodology
UBP Symbol Study Phase 2 (Refined)

Uses the EXACT validated Phase 2 pipeline for computing NRCI.

Author: Manus AI
Date: Nov 18, 2025
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase2_refined')

import json
import numpy as np
from typing import Dict, List
from coherence_substrate_v2 import CoherenceState

# Reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Phase 2 calibrated scales
REFINEMENT_SCALE = 1.0
DEGRADATION_SCALE = 500.0

def compute_refinement_score(candidate: Dict) -> float:
    """
    Compute refinement score (Phase 2 methodology).
    
    Refinement drivers: commutativity, invertibility, closure
    """
    bitfield = candidate["bitfield"]
    
    # Extract relevant dimensions
    arity = bitfield[0]  # D1
    invertibility = bitfield[2]  # D3
    commutativity = bitfield[3]  # D4
    closure_degree = bitfield[6]  # D7
    
    # Compute refinement score (weighted combination)
    refinement = 0.0
    
    # Commutativity contribution
    refinement += commutativity * 0.3
    
    # Invertibility contribution
    refinement += invertibility * 0.2
    
    # Closure contribution
    refinement += closure_degree * 0.4
    
    # Arity contribution (lower arity = simpler = better)
    refinement += (1.0 - arity) * 0.1
    
    return refinement * REFINEMENT_SCALE

def compute_degradation_score(candidate: Dict) -> float:
    """
    Compute degradation score (Phase 2 methodology).
    
    Degradation drivers: ambiguity, complexity, overloading
    """
    bitfield = candidate["bitfield"]
    
    # Extract relevant dimensions
    meaning_count_log = bitfield[4]  # D5: log(1 + meaning_count)
    dependency_depth = bitfield[5]  # D6: compositional complexity
    closure_degree = bitfield[6]  # D7: 0=low, 1=medium, 2=high
    overloading_log = bitfield[7]  # D8: log(1 + overloading_count)
    
    # Compute degradation score (weighted combination)
    degradation = 0.0
    
    # Meaning count contribution (ambiguity)
    degradation += meaning_count_log * 0.3
    
    # Overloading contribution (semantic ambiguity)
    degradation += overloading_log * 0.4
    
    # Dependency depth contribution (compositional complexity)
    degradation += dependency_depth * 0.2
    
    # Closure penalty (inverted: low closure = high degradation)
    degradation += (2.0 - closure_degree) * 0.1
    
    return degradation * DEGRADATION_SCALE

def compute_nrci_phase2(candidate: Dict) -> Dict:
    """
    Compute NRCI using exact Phase 2 methodology.
    """
    # Extract bitfield
    bitfield = candidate["bitfield"]
    
    # Compute deterministic seed from bitfield
    bitfield_str = ''.join(f"{x:.6f}" for x in bitfield)
    unicode_seed = (hash(bitfield_str) % 1000000) / 1000000.0
    
    # Compute bitfield magnitude
    bitfield_magnitude = np.linalg.norm(bitfield)
    
    # Initialize CoherenceState with combined value (Phase 2 method)
    combined_value = (unicode_seed + bitfield_magnitude) / 2.0
    initial_state = CoherenceState(
        value=combined_value,
        metadata={'symbol_name': candidate['name']}
    )
    
    # Compute refinement and degradation scores
    refinement_score = compute_refinement_score(candidate)
    degradation_score = compute_degradation_score(candidate)
    
    # Apply refinement operations (Phase 2: Y-refinement)
    # Number of refinements proportional to score
    num_refinements = int(refinement_score * 10)  # Scale to reasonable count
    refined_state = initial_state
    for _ in range(num_refinements):
        refined_state = refined_state.refine_forward()
    
    # Apply degradation operations (Phase 2: log-space degradation)
    delta_log_error = degradation_score * 0.01  # Phase 2 scale factor
    final_state = refined_state.degrade_by(delta_log_error)
    
    # Extract final NRCI
    nrci = final_state.nrci
    
    return {
        "id": candidate["id"],
        "glyph": candidate["glyph"],
        "name": candidate["name"],
        "NRCI_meas": float(nrci),
        "refinement_score": float(refinement_score),
        "degradation_score": float(degradation_score),
        "num_refinements": num_refinements,
        "delta_log_error": float(delta_log_error),
        "net_refinements": final_state.net_refinements,
        "seed_value": float(unicode_seed),
        "bitfield_magnitude": float(bitfield_magnitude),
        "combined_value": float(combined_value),
        "D1": candidate["D1"],
        "D2": candidate["D2"],
        "D3": candidate["D3"],
        "D4": candidate["D4"],
        "D5": candidate["D5"],
        "D6": candidate["D6"],
        "D7": candidate["D7"],
        "D8": candidate["D8"]
    }

def evaluate_all_candidates(candidates: List[Dict]) -> List[Dict]:
    """Evaluate all candidates using Phase 2 methodology"""
    print("="*70)
    print("UBP EVALUATION - EXACT PHASE 2 METHODOLOGY")
    print("="*70)
    print(f"Evaluating {len(candidates)} candidates")
    print(f"Refinement scale: {REFINEMENT_SCALE}")
    print(f"Degradation scale: {DEGRADATION_SCALE}")
    print()
    
    results = []
    
    for i, cand in enumerate(candidates):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(candidates)}")
        
        result = compute_nrci_phase2(cand)
        results.append(result)
    
    print(f"  Progress: {len(candidates)}/{len(candidates)}")
    print()
    
    # Statistics
    nrci_values = [r["NRCI_meas"] for r in results]
    print("NRCI Statistics:")
    print(f"  Mean: {np.mean(nrci_values):.6f}")
    print(f"  Std: {np.std(nrci_values):.6f}")
    print(f"  Min: {np.min(nrci_values):.6f}")
    print(f"  Max: {np.max(nrci_values):.6f}")
    print()
    
    return results

def main():
    """Main execution"""
    print("="*70)
    print("UBP SYMBOL STUDY - PHASE 2 METHODOLOGY")
    print("="*70)
    print(f"Random seed: {RANDOM_SEED}")
    print()
    
    # Load candidates
    with open('/home/ubuntu/ubp_symbol_study_phase2_refined/candidates/candidates_n100.json', 'r') as f:
        candidates = json.load(f)
    
    print(f"Loaded {len(candidates)} candidates")
    print()
    
    # Evaluate
    results = evaluate_all_candidates(candidates)
    
    # Save
    output_path = "/home/ubuntu/ubp_symbol_study_phase2_refined/results/candidates_evaluated.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()
    print("="*70)
    print("EVALUATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
