#!/usr/bin/env python3.11
"""
Direct UBP Evaluation Using Pre-Computed Bitfields
UBP Symbol Study Phase 2 (Refined)

Directly evaluates candidates using their pre-computed bitfields,
bypassing the encoder to avoid format mismatches.

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

# Calibrated scales from Phase 2
REFINEMENT_SCALE = 1.0
DEGRADATION_SCALE = 500.0

def compute_nrci_direct(candidate: Dict) -> Dict:
    """
    Compute NRCI directly from candidate bitfield.
    
    Uses the validated Phase 2 methodology:
    1. Initialize CoherenceState from bitfield
    2. Apply refinements based on positive properties
    3. Apply degradation based on negative properties
    4. Extract final NRCI
    """
    # Extract bitfield
    bitfield = candidate["bitfield"]
    
    # Compute deterministic seed from bitfield
    bitfield_str = ''.join(f"{x:.6f}" for x in bitfield)
    unicode_seed = (hash(bitfield_str) % 1000000) / 1000000.0
    
    # Compute bitfield magnitude
    bitfield_magnitude = np.linalg.norm(bitfield)
    
    # Initialize CoherenceState with combined value (matching Phase 2)
    combined_value = (unicode_seed + bitfield_magnitude) / 2.0
    cs = CoherenceState(
        value=combined_value,
        metadata={'symbol_name': candidate['name']}
    )
    
    # Apply refinements (positive properties)
    refinement_count = 0
    
    # D4: Commutativity
    if candidate["D4"] > 0.5:
        cs = cs.refine_forward()
        refinement_count += 1
    
    # D7: Closure
    if candidate["D7"] > 0.5:
        cs = cs.refine_forward()
        refinement_count += 1
    
    # D3: Invertibility
    if candidate["D3"] > 0.5:
        cs = cs.refine_forward()
        refinement_count += 1
    
    # Apply degradation (negative properties)
    degradation_amount = 0.0
    
    # D5: Ambiguity (meaning count)
    degradation_amount += candidate["D5"] * DEGRADATION_SCALE
    
    # D6: Complexity (dependency depth)
    degradation_amount += candidate["D6"] * DEGRADATION_SCALE
    
    # D8: Overloading
    degradation_amount += candidate["D8"] * DEGRADATION_SCALE
    
    # Apply total degradation
    if degradation_amount > 0:
        cs = cs.degrade_by(degradation_amount)
    
    # Extract NRCI
    nrci = cs.nrci
    
    return {
        "id": candidate["id"],
        "glyph": candidate["glyph"],
        "name": candidate["name"],
        "NRCI_meas": float(nrci),
        "refinement_count": refinement_count,
        "degradation_amount": float(degradation_amount),
        "net_refinements": refinement_count,
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
    """Evaluate all candidates"""
    print("="*70)
    print("DIRECT UBP EVALUATION")
    print("="*70)
    print(f"Evaluating {len(candidates)} candidates")
    print(f"Refinement scale: {REFINEMENT_SCALE}")
    print(f"Degradation scale: {DEGRADATION_SCALE}")
    print()
    
    results = []
    
    for i, cand in enumerate(candidates):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(candidates)}")
        
        result = compute_nrci_direct(cand)
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
    print("UBP SYMBOL STUDY - DIRECT EVALUATION")
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
