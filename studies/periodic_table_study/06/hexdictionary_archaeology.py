#!/usr/bin/env python3.11
"""
hexdictionary_archaeology.py - Reconstruct toggle history from final state
Uses HexDictionary's 8 methods as archaeological tools, not similarity engines
"""
import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE
from geometric_error_correction import restore_coherence
from hex_dictionary_advanced import (
    hamming_distance, spectral_distance, kl_divergence,
    coherence_weighted_distance, frequency_domain_distance
)

# Known blood type toggle sequences (ground truth)
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

# All possible antigens
ANTIGENS = ["A", "B", "RhD"]

def apply_toggle_sequence(toggles: list) -> CoherenceState:
    """Apply a toggle sequence and return final state"""
    state = CoherenceState(1.0)  # OffBit
    for toggle in toggles:
        state = state * CoherenceState(-1.0)  # Toggle
        state_restored, _ = restore_coherence(state)
        state = state_restored
    state = state * CoherenceState(Y_INVERSE)  # Observer binding
    return state

def reconstruct_toggles_hamming(final_state: CoherenceState) -> list:
    """Method 1: Hamming-based reconstruction"""
    # Try all 8 possible toggle combinations
    candidates = []
    for i in range(8):
        toggles = []
        if i & 1: toggles.append("A")
        if i & 2: toggles.append("B")
        if i & 4: toggles.append("RhD")
        
        candidate_state = apply_toggle_sequence(toggles)
        distance = abs(candidate_state.value - final_state.value)
        candidates.append((distance, toggles))
    
    # Return closest match
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def reconstruct_toggles_spectral(final_state: CoherenceState) -> list:
    """Method 2: Spectral-based reconstruction"""
    # Convert final state to spectral signature
    final_spectrum = [final_state.value, final_state.nrci, final_state.log_nrci_error]
    
    candidates = []
    for i in range(8):
        toggles = []
        if i & 1: toggles.append("A")
        if i & 2: toggles.append("B")
        if i & 4: toggles.append("RhD")
        
        candidate_state = apply_toggle_sequence(toggles)
        candidate_spectrum = [candidate_state.value, candidate_state.nrci, candidate_state.log_nrci_error]
        
        distance = spectral_distance(final_spectrum, candidate_spectrum)
        candidates.append((distance, toggles))
    
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def reconstruct_toggles_coherence(final_state: CoherenceState) -> list:
    """Method 3: Coherence-weighted reconstruction"""
    candidates = []
    for i in range(8):
        toggles = []
        if i & 1: toggles.append("A")
        if i & 2: toggles.append("B")
        if i & 4: toggles.append("RhD")
        
        candidate_state = apply_toggle_sequence(toggles)
        
        # Coherence-weighted distance
        nrci_diff = abs(candidate_state.nrci - final_state.nrci)
        value_diff = abs(candidate_state.value - final_state.value)
        distance = nrci_diff * 1000 + value_diff  # Weight NRCI heavily
        
        candidates.append((distance, toggles))
    
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def validate_reconstruction(blood_type: str):
    """Validate reconstruction against ground truth"""
    ground_truth = GROUND_TRUTH[blood_type]
    final_state = apply_toggle_sequence(ground_truth)
    
    # Reconstruct using all 3 methods
    recon_hamming = reconstruct_toggles_hamming(final_state)
    recon_spectral = reconstruct_toggles_spectral(final_state)
    recon_coherence = reconstruct_toggles_coherence(final_state)
    
    results = {
        "blood_type": blood_type,
        "ground_truth": ground_truth,
        "reconstructed": {
            "hamming": recon_hamming,
            "spectral": recon_spectral,
            "coherence": recon_coherence
        },
        "matches": {
            "hamming": recon_hamming == ground_truth,
            "spectral": recon_spectral == ground_truth,
            "coherence": recon_coherence == ground_truth
        }
    }
    
    return results

if __name__ == "__main__":
    print("\n" + "="*80)
    print("HEXDICTIONARY ARCHAEOLOGY: Reconstructing Toggle Sequences")
    print("="*80 + "\n")
    
    all_results = []
    
    for blood_type in ["O-", "A+", "AB+", "B-"]:
        print(f"\n{blood_type}:")
        result = validate_reconstruction(blood_type)
        
        print(f"  Ground Truth:  {result['ground_truth']}")
        print(f"  Hamming:       {result['reconstructed']['hamming']} {'✓' if result['matches']['hamming'] else '✗'}")
        print(f"  Spectral:      {result['reconstructed']['spectral']} {'✓' if result['matches']['spectral'] else '✗'}")
        print(f"  Coherence:     {result['reconstructed']['coherence']} {'✓' if result['matches']['coherence'] else '✗'}")
        
        all_results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for method in ["hamming", "spectral", "coherence"]:
        matches = sum(1 for r in all_results if r['matches'][method])
        print(f"{method.capitalize():12s}: {matches}/4 correct reconstructions")
    
    # Save results
    with open("/home/ubuntu/blood_type_ubp_study_v4/archaeology_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResults saved to: archaeology_results.json")
