"""
================================================================================
Cross-Realm Dissident Validation Study
Author: Euan Craig, New Zealand
Date: November 14, 2025
================================================================================

This study validates the Dissident Horizon Oracle across multiple UBP realms,
testing whether dissident signatures are universal or domain-specific.

**Test Realms**:
1. Quantum - Anomalous particle behavior
2. Biological - Disease persistence patterns  
3. Cosmological - Dark matter/energy distributions
4. Electromagnetic - Resonance anomalies

**Validation Metrics**:
- Cross-realm consistency of dissident scores
- δ-deficit universality (0.15% threshold)
- Temporal memory patterns
- Spectral signature preservation
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple

# Add paths
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/dissident_horizon_study')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
from dissident_horizon_oracle import DissidentHorizonOracle, DissidentSignature
from quantum_realm import QuantumRealm
from biological_realm import BiologicalRealm
from cosmological_realm import CosmologicalRealm
from electromagnetic_realm import ElectromagneticRealm


# ============================================================================
# REALM-SPECIFIC DISSIDENT SCENARIOS
# ============================================================================

def create_quantum_dissident_scenario():
    """
    Quantum dissident: Particle exhibiting anomalous tunneling behavior.
    
    Example: Electron in potential barrier with unexpected transmission rate.
    """
    # Create data representing energy states
    # Dissident: Trapped in metastable state (local minimum)
    energy_states = [
        [1.0, 1.05, 1.02, 1.03],  # Clustered near local minimum
        [1.01, 1.04, 1.03, 1.02],
        [1.02, 1.03, 1.01, 1.04],
        [1.0, 1.05, 1.02, 1.03]
    ]
    
    # Coherence states with slight deficit
    nrci_deficit = NRCI_TARGET - 0.0015  # 0.15% deficit
    coherence_states = [
        CoherenceState(value=1.0, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=1.05, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=1.02, log_nrci_error=math.log(1 - nrci_deficit))
    ]
    
    return {
        'realm': 'quantum',
        'scenario': 'Anomalous tunneling - metastable trap',
        'data_matrix': energy_states,
        'coherence_states': coherence_states,
        'states_history': coherence_states,
        'expected_type': 'harmful'
    }


def create_biological_dissident_scenario():
    """
    Biological dissident: Chronic disease persistence pattern.
    
    Example: Lyme disease maintaining stable but pathological state.
    """
    # Immune response patterns (should oscillate, but stuck)
    immune_patterns = [
        [0.5, 0.52, 0.51, 0.53],  # Low-level persistent activation
        [0.51, 0.53, 0.52, 0.50],
        [0.52, 0.51, 0.53, 0.52],
        [0.50, 0.52, 0.51, 0.53]
    ]
    
    # Coherence with deficit
    nrci_deficit = NRCI_TARGET - 0.0014
    coherence_states = [
        CoherenceState(value=0.5, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=0.52, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=0.51, log_nrci_error=math.log(1 - nrci_deficit))
    ]
    
    return {
        'realm': 'biological',
        'scenario': 'Chronic Lyme persistence',
        'data_matrix': immune_patterns,
        'coherence_states': coherence_states,
        'states_history': coherence_states,
        'expected_type': 'harmful'
    }


def create_cosmological_dissident_scenario():
    """
    Cosmological dissident: Dark matter distribution anomaly.
    
    Example: Galaxy rotation curve deviation from expected.
    """
    # Rotation velocities (flat instead of declining)
    rotation_data = [
        [200.0, 205.0, 203.0, 202.0],  # Should decline, but flat
        [201.0, 204.0, 202.0, 203.0],
        [203.0, 202.0, 204.0, 201.0],
        [200.0, 205.0, 203.0, 202.0]
    ]
    
    # Coherence with dark matter deficit
    nrci_deficit = NRCI_TARGET - 0.0015  # Exactly 0.15%
    coherence_states = [
        CoherenceState(value=200.0, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=205.0, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=203.0, log_nrci_error=math.log(1 - nrci_deficit))
    ]
    
    return {
        'realm': 'cosmological',
        'scenario': 'Dark matter - flat rotation curve',
        'data_matrix': rotation_data,
        'coherence_states': coherence_states,
        'states_history': coherence_states,
        'expected_type': 'neutral'  # Not harmful, just different
    }


def create_electromagnetic_dissident_scenario():
    """
    Electromagnetic dissident: Resonance anomaly.
    
    Example: Cavity exhibiting unexpected mode locking.
    """
    # Resonance frequencies (locked to unexpected mode)
    resonance_data = [
        [2.4e9, 2.401e9, 2.399e9, 2.4e9],  # Locked around 2.4 GHz
        [2.399e9, 2.401e9, 2.4e9, 2.401e9],
        [2.4e9, 2.399e9, 2.401e9, 2.4e9],
        [2.401e9, 2.4e9, 2.399e9, 2.401e9]
    ]
    
    # Coherence with deficit
    nrci_deficit = NRCI_TARGET - 0.0016
    coherence_states = [
        CoherenceState(value=2.4e9, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=2.401e9, log_nrci_error=math.log(1 - nrci_deficit)),
        CoherenceState(value=2.399e9, log_nrci_error=math.log(1 - nrci_deficit))
    ]
    
    return {
        'realm': 'electromagnetic',
        'scenario': 'Unexpected mode locking',
        'data_matrix': resonance_data,
        'coherence_states': coherence_states,
        'states_history': coherence_states,
        'expected_type': 'beneficial'  # Stable, could be useful
    }


def create_healthy_control_scenario():
    """
    Healthy control: No dissident characteristics.
    """
    # Well-distributed, high-variance data
    healthy_data = [
        [1.0, 2.0, 3.0, 4.0],
        [1.5, 2.5, 3.5, 4.5],
        [0.5, 1.5, 2.5, 3.5],
        [2.0, 3.0, 4.0, 5.0]
    ]
    
    # Coherence at target (no deficit)
    coherence_states = [
        CoherenceState(value=1.0),  # Default NRCI_TARGET
        CoherenceState(value=2.0),
        CoherenceState(value=3.0)
    ]
    
    return {
        'realm': 'control',
        'scenario': 'Healthy system (no dissidence)',
        'data_matrix': healthy_data,
        'coherence_states': coherence_states,
        'states_history': coherence_states,
        'expected_type': 'neutral'
    }


# ============================================================================
# VALIDATION STUDY
# ============================================================================

def run_cross_realm_validation():
    """
    Run comprehensive cross-realm validation study.
    """
    print("=" * 80)
    print("CROSS-REALM DISSIDENT VALIDATION STUDY")
    print("=" * 80)
    print()
    
    # Create oracle
    oracle = DissidentHorizonOracle(delta_deficit_threshold=0.0015)
    
    # Create scenarios
    scenarios = [
        create_quantum_dissident_scenario(),
        create_biological_dissident_scenario(),
        create_cosmological_dissident_scenario(),
        create_electromagnetic_dissident_scenario(),
        create_healthy_control_scenario()
    ]
    
    results = []
    
    print(f"Testing {len(scenarios)} scenarios across realms...")
    print()
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['realm'].upper()} - {scenario['scenario']}")
        print("-" * 80)
        
        # Analyze
        result = oracle.analyze_system(
            data_matrix=scenario['data_matrix'],
            coherence_states=scenario['coherence_states'],
            states_history=scenario['states_history']
        )
        
        # Display results
        sig = result.signature
        print(f"  Dissident Score: {sig.dissident_score:.3f}")
        print(f"  Type: {sig.dissident_type} (expected: {scenario['expected_type']})")
        print(f"  δ-Deficit: {sig.delta_deficit:.6f} (threshold: 0.001500)")
        print(f"  Laplacian Eigenvalue: {sig.laplacian_eigenvalue:.6f}")
        print(f"  PCA Variance Ratio: {sig.pca_variance_ratio:.3f}")
        print(f"  Memory Persistence: {sig.memory_persistence:.3f}")
        print(f"  Temporal Stability: {sig.temporal_stability:.3f}")
        print(f"  Confidence: {result.confidence:.3f}")
        
        # Check if type matches expectation
        type_match = sig.dissident_type == scenario['expected_type']
        print(f"  Type Match: {'✓' if type_match else '✗'}")
        
        # Check if δ-deficit is near threshold for dissidents
        if sig.is_dissident:
            deficit_match = abs(sig.delta_deficit - 0.0015) < 0.0005
            print(f"  δ-Deficit Match: {'✓' if deficit_match else '✗'}")
        
        print()
        
        # Store result
        results.append({
            'realm': scenario['realm'],
            'scenario': scenario['scenario'],
            'dissident_score': sig.dissident_score,
            'dissident_type': sig.dissident_type,
            'expected_type': scenario['expected_type'],
            'type_match': type_match,
            'delta_deficit': sig.delta_deficit,
            'laplacian_eigenvalue': sig.laplacian_eigenvalue,
            'pca_variance_ratio': sig.pca_variance_ratio,
            'memory_persistence': sig.memory_persistence,
            'temporal_stability': sig.temporal_stability,
            'confidence': result.confidence
        })
    
    # Summary statistics
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    # Type match rate
    type_matches = sum(1 for r in results if r['type_match'])
    type_match_rate = type_matches / len(results)
    print(f"Type Classification Accuracy: {type_match_rate:.1%} ({type_matches}/{len(results)})")
    
    # Dissident detection rate
    dissidents = [r for r in results if r['dissident_score'] > 0.5]
    dissident_rate = len(dissidents) / len(results)
    print(f"Dissident Detection Rate: {dissident_rate:.1%} ({len(dissidents)}/{len(results)})")
    
    # δ-deficit consistency (for dissidents)
    if dissidents:
        avg_deficit = sum(r['delta_deficit'] for r in dissidents) / len(dissidents)
        deficit_std = math.sqrt(
            sum((r['delta_deficit'] - avg_deficit)**2 for r in dissidents) / len(dissidents)
        )
        print(f"Average δ-Deficit (dissidents): {avg_deficit:.6f} ± {deficit_std:.6f}")
        print(f"Expected δ-Deficit: 0.001500 (0.15%)")
        print(f"Deficit Consistency: {'✓' if abs(avg_deficit - 0.0015) < 0.0005 else '✗'}")
    
    # Cross-realm score consistency
    dissident_scores = [r['dissident_score'] for r in results if r['realm'] != 'control']
    if dissident_scores:
        avg_score = sum(dissident_scores) / len(dissident_scores)
        score_std = math.sqrt(
            sum((s - avg_score)**2 for s in dissident_scores) / len(dissident_scores)
        )
        print(f"Cross-Realm Score Consistency: {avg_score:.3f} ± {score_std:.3f}")
    
    # Average confidence
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    print(f"Average Confidence: {avg_confidence:.3f}")
    
    print()
    
    # Key findings
    print("KEY FINDINGS:")
    print("-" * 80)
    
    if type_match_rate >= 0.8:
        print("✓ Strong type classification accuracy across realms")
    else:
        print("⚠ Type classification needs refinement")
    
    if dissidents and abs(avg_deficit - 0.0015) < 0.0005:
        print("✓ δ-deficit threshold (0.15%) is universal across realms")
    elif dissidents:
        print("⚠ δ-deficit shows realm-specific variation")
    
    if score_std < 0.2:
        print("✓ Dissident signatures are consistent across realms")
    else:
        print("⚠ Dissident signatures show realm-specific characteristics")
    
    print()
    
    # Export results
    export_path = '/home/ubuntu/dissident_horizon_study/cross_realm_validation_results.json'
    with open(export_path, 'w') as f:
        json.dump({
            'summary': {
                'type_match_rate': type_match_rate,
                'dissident_detection_rate': dissident_rate,
                'average_deficit': avg_deficit if dissidents else None,
                'average_confidence': avg_confidence,
                'cross_realm_consistency': score_std if dissident_scores else None
            },
            'results': results
        }, f, indent=2)
    
    print(f"Results exported to: {export_path}")
    print()
    print("=" * 80)
    
    return results


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    results = run_cross_realm_validation()
