#!/usr/bin/env python3.11
"""
blood_type_dissident_analysis.py - Use dissident_horizon_oracle.py to analyze blood types
Answer: Why do blood types have δ ≈ 0.0009 when biological systems should have δ ≈ 0.4058?
"""
import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, NRCI_TARGET
from geometric_error_correction import restore_coherence
from dissident_horizon_oracle import DissidentHorizonOracle
from coherence_state_history import HistoryAwareState

# Blood type data with molecular properties
BLOOD_TYPE_DATA = {
    "O-": {
        "toggles": [],
        "membrane_freq_ghz": 2.30,
        "antigen_density": 0,  # No A or B antigens
        "antibodies": ["anti-A", "anti-B"]
    },
    "O+": {
        "toggles": ["RhD"],
        "membrane_freq_ghz": 2.50,
        "antigen_density": 100000,  # RhD only
        "antibodies": ["anti-A", "anti-B"]
    },
    "A-": {
        "toggles": ["A"],
        "membrane_freq_ghz": 2.70,
        "antigen_density": 800000,  # A antigen
        "antibodies": ["anti-B"]
    },
    "A+": {
        "toggles": ["A", "RhD"],
        "membrane_freq_ghz": 2.90,
        "antigen_density": 900000,  # A + RhD
        "antibodies": ["anti-B"]
    },
    "B-": {
        "toggles": ["B"],
        "membrane_freq_ghz": 2.60,
        "antigen_density": 750000,  # B antigen
        "antibodies": ["anti-A"]
    },
    "B+": {
        "toggles": ["B", "RhD"],
        "membrane_freq_ghz": 2.80,
        "antigen_density": 850000,  # B + RhD
        "antibodies": ["anti-A"]
    },
    "AB-": {
        "toggles": ["A", "B"],
        "membrane_freq_ghz": 3.10,
        "antigen_density": 1500000,  # A + B
        "antibodies": []
    },
    "AB+": {
        "toggles": ["A", "B", "RhD"],
        "membrane_freq_ghz": 3.30,
        "antigen_density": 1600000,  # A + B + RhD
        "antibodies": []
    }
}

def build_blood_type_state(blood_type: str) -> tuple:
    """Build CoherenceState and history for a blood type"""
    data = BLOOD_TYPE_DATA[blood_type]
    toggles = data["toggles"]
    
    # Build state with history
    state = HistoryAwareState(CoherenceState(1.0))
    for antigen in toggles:
        state = state.toggle(antigen).restore()
    state = state.bind_observer()
    
    # Also build just the final CoherenceState for oracle
    final_state = state.state
    
    return final_state, state.history, data

def create_data_matrix_for_blood_type(blood_type: str) -> list:
    """Create data matrix for spectral/PCA analysis"""
    data = BLOOD_TYPE_DATA[blood_type]
    
    # Create feature vector: [freq, density, num_toggles, num_antibodies]
    feature_vector = [
        data["membrane_freq_ghz"],
        data["antigen_density"] / 1e6,  # Normalize
        len(data["toggles"]),
        len(data["antibodies"])
    ]
    
    # Create matrix with slight perturbations for analysis
    matrix = []
    for i in range(10):
        perturbed = [f * (1.0 + 0.01 * (i - 5)) for f in feature_vector]
        matrix.append(perturbed)
    
    return matrix

def analyze_all_blood_types():
    """Analyze all 8 blood types with dissident oracle"""
    print("\n" + "="*80)
    print("BLOOD TYPE DISSIDENT ANALYSIS")
    print("="*80 + "\n")
    
    oracle = DissidentHorizonOracle()
    results = {}
    
    for blood_type in ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]:
        print(f"\n{blood_type}:")
        print("-" * 40)
        
        # Build state and data
        final_state, history, data = build_blood_type_state(blood_type)
        data_matrix = create_data_matrix_for_blood_type(blood_type)
        
        # Analyze with oracle
        analysis = oracle.analyze_system(
            data_matrix=data_matrix,
            coherence_states=[final_state],
            states_history=None  # We'll add temporal evolution later
        )
        
        signature = analysis.signature
        
        print(f"  δ-deficit:           {signature.delta_deficit:.6f}")
        print(f"  Expected (bio):      0.405800")
        print(f"  Discrepancy:         {abs(signature.delta_deficit - 0.4058):.6f}")
        print(f"  Dissident score:     {signature.dissident_score:.4f}")
        print(f"  Is dissident:        {signature.is_dissident}")
        print(f"  Type:                {signature.dissident_type}")
        print(f"  Laplacian λ:         {signature.laplacian_eigenvalue:.6f}")
        print(f"  PCA variance:        {signature.pca_variance_ratio:.4f}")
        print(f"  Temporal stability:  {signature.temporal_stability:.4f}")
        
        results[blood_type] = {
            "delta_deficit": signature.delta_deficit,
            "expected_delta": 0.4058,
            "discrepancy": abs(signature.delta_deficit - 0.4058),
            "dissident_score": signature.dissident_score,
            "is_dissident": signature.is_dissident,
            "dissident_type": signature.dissident_type,
            "laplacian_eigenvalue": signature.laplacian_eigenvalue,
            "pca_variance_ratio": signature.pca_variance_ratio,
            "temporal_stability": signature.temporal_stability,
            "membrane_freq_ghz": data["membrane_freq_ghz"],
            "num_toggles": len(data["toggles"])
        }
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    avg_delta = sum(r["delta_deficit"] for r in results.values()) / len(results)
    avg_discrepancy = sum(r["discrepancy"] for r in results.values()) / len(results)
    
    print(f"\nAverage δ-deficit:     {avg_delta:.6f}")
    print(f"Expected (biological): 0.405800")
    print(f"Average discrepancy:   {avg_discrepancy:.6f}")
    print(f"Discrepancy ratio:     {avg_discrepancy / 0.4058:.2f}× smaller than expected")
    
    dissident_count = sum(1 for r in results.values() if r["is_dissident"])
    print(f"\nDissident blood types: {dissident_count}/8")
    
    # Save results
    with open("/home/ubuntu/blood_type_ubp_study_v4/dissident_analysis_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to: dissident_analysis_results.json")
    
    return results

if __name__ == "__main__":
    analyze_all_blood_types()
