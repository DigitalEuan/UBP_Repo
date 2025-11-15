#!/usr/bin/env python3.11
"""
archaeology_v2_history_aware.py - Rerun with history-aware HexDictionary
"""
import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState
from coherence_state_history import HistoryAwareState
from hexdictionary_history_aware import history_distance, extract_toggle_sequence

# Ground truth
GROUND_TRUTH = {
    "O-": [],
    "O+": ["RhD"],
    "A-": ["A"],
    "A+": ["A", "RhD"],
    "B-": ["B"],
    "B+": ["B", "RhD"],
    "AB-": ["A", "B"],
    "AB+": ["A", "B", "RhD"]
}

def build_state_with_history(toggles: list) -> HistoryAwareState:
    """Build a HistoryAwareState from toggle sequence"""
    state = HistoryAwareState(CoherenceState(1.0))
    for antigen in toggles:
        state = state.toggle(antigen).restore()
    state = state.bind_observer()
    return state

def reconstruct_with_history_aware(final_state: HistoryAwareState) -> list:
    """Reconstruct toggle sequence using history-aware distance"""
    candidates = []
    
    # Try all 8 possible toggle combinations
    for i in range(8):
        toggles = []
        if i & 1: toggles.append("A")
        if i & 2: toggles.append("B")
        if i & 4: toggles.append("RhD")
        
        candidate_state = build_state_with_history(toggles)
        distance = history_distance(final_state, candidate_state)
        candidates.append((distance, toggles))
    
    # Return closest match
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def validate_all():
    """Validate all 8 blood types"""
    print("\n" + "="*80)
    print("ARCHAEOLOGY V2: History-Aware HexDictionary")
    print("="*80 + "\n")
    
    results = []
    
    for blood_type in ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]:
        ground_truth = GROUND_TRUTH[blood_type]
        final_state = build_state_with_history(ground_truth)
        reconstructed = reconstruct_with_history_aware(final_state)
        
        match = reconstructed == ground_truth
        
        print(f"{blood_type:4s}: Ground={ground_truth}, Reconstructed={reconstructed} {'✓' if match else '✗'}")
        
        # Test confession protocol
        if blood_type == "A+":
            print(f"\n  Confession: {final_state.confess()}\n")
        
        results.append({
            "blood_type": blood_type,
            "ground_truth": ground_truth,
            "reconstructed": reconstructed,
            "match": match
        })
    
    # Summary
    matches = sum(1 for r in results if r['match'])
    print(f"\n{'='*80}")
    print(f"RESULT: {matches}/8 correct reconstructions")
    print(f"{'='*80}\n")
    
    # Save
    with open("/home/ubuntu/blood_type_ubp_study_v4/archaeology_v2_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    validate_all()
