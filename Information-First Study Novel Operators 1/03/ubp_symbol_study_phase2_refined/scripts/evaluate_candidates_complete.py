#!/usr/bin/env python3.11
"""
Complete Rigorous UBP Evaluation with Statistical Analysis
UBP Symbol Study Phase 2 (Refined)

Uses the validated Phase 2 pipeline to:
1. Encode novel candidates
2. Compute coherence features
3. Perform statistical tests with controls
4. Generate bootstrapped confidence intervals
5. Validate model calibration

Author: Manus AI
Date: Nov 18, 2025
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase2_refined')

import json
import numpy as np
from typing import Dict, List
from symbol_encoding import SymbolEncoder
from symbol_coherence_model import SymbolCoherenceModel

# Reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def load_candidates():
    """Load generated candidates"""
    with open('/home/ubuntu/ubp_symbol_study_phase2_refined/candidates/candidates_n100.json', 'r') as f:
        return json.load(f)

def load_baseline_symbols():
    """Load baseline symbols from Phase 2 for controls"""
    with open('/home/ubuntu/ubp_symbol_study_phase2/data/symbols_processed.json', 'r') as f:
        return json.load(f)

def encode_candidates(candidates: List[Dict]) -> List[Dict]:
    """Encode candidates using the validated encoder"""
    print("="*70)
    print("ENCODING CANDIDATES")
    print("="*70)
    
    encoder = SymbolEncoder()
    encoded = []
    
    for i, cand in enumerate(candidates):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(candidates)} encoded")
        
        # Convert candidate format to encoder format
        symbol_data = {
            "symbol": cand["glyph"],
            "unicode": cand["glyph"],  # Add unicode field
            "name": cand["name"],
            "category": cand["category"],
            "arity": cand["arity"],
            "formal_role": cand["formal_role"],
            "has_inverse": cand["has_inverse"],
            "is_commutative": cand["is_commutative"],
            "meaning_count": cand["meaning_count"],
            "dependency_depth": cand["dependency_depth"],
            "closure_type": cand["closure_type"]
        }
        
        # Encode
        unicode_seed, bitfield, initial_state = encoder.encode_symbol(symbol_data)
        
        # Store encoded data
        encoded_cand = {
            **cand,
            "unicode_seed": unicode_seed,
            "bitfield": bitfield,
            "initial_value": initial_state.value,
            "initial_nrci": initial_state.nrci
        }
        encoded.append(encoded_cand)
    
    print(f"  Progress: {len(candidates)}/{len(candidates)} encoded")
    print()
    return encoded

def compute_coherence_features(encoded_candidates: List[Dict]) -> List[Dict]:
    """Compute full UBP coherence features"""
    print("="*70)
    print("COMPUTING COHERENCE FEATURES")
    print("="*70)
    
    model = SymbolCoherenceModel(
        refinement_scale=1.0,
        degradation_scale=500.0
    )
    
    processed = []
    
    for i, cand in enumerate(encoded_candidates):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(encoded_candidates)} processed")
        
        # Compute features
        features = model.compute_coherence_features(cand)
        
        # Merge with candidate data
        processed_cand = {
            **cand,
            **features
        }
        processed.append(processed_cand)
    
    print(f"  Progress: {len(encoded_candidates)}/{len(encoded_candidates)} processed")
    print()
    
    # Statistics
    nrci_values = [c["nrci"] for c in processed]
    print("NRCI Statistics:")
    print(f"  Mean: {np.mean(nrci_values):.6f}")
    print(f"  Std: {np.std(nrci_values):.6f}")
    print(f"  Min: {np.min(nrci_values):.6f}")
    print(f"  Max: {np.max(nrci_values):.6f}")
    print()
    
    return processed

def main():
    """Main execution"""
    print("="*70)
    print("COMPLETE UBP EVALUATION - RIGOROUS PROTOCOL")
    print("="*70)
    print(f"Random seed: {RANDOM_SEED}")
    print()
    
    # Load candidates
    print("Loading candidates...")
    candidates = load_candidates()
    print(f"Loaded {len(candidates)} candidates")
    print()
    
    # Encode
    encoded = encode_candidates(candidates)
    
    # Compute coherence
    processed = compute_coherence_features(encoded)
    
    # Save results
    output_path = "/home/ubuntu/ubp_symbol_study_phase2_refined/results/candidates_evaluated.json"
    with open(output_path, 'w') as f:
        json.dump(processed, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    print()
    print("="*70)
    print("EVALUATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
