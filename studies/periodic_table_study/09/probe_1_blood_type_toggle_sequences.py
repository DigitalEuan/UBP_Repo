#!/usr/bin/env python3.11
"""
Probe 1: All 8 Blood Types as Toggle Sequences
Watch the OffBit decide to persist - using REAL UBP 3.5
"""
import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y
from geometric_error_correction import restore_coherence

def toggle(state: CoherenceState, label: str) -> CoherenceState:
    """Apply a toggle (+1/-1 phase shift)."""
    # Multiply by -1 to flip phase
    return CoherenceState(
        value=state.value * -1.0,
        log_nrci_error=state.log_nrci_error,
        net_refinements=state.net_refinements
    )

def survive_restore(state: CoherenceState) -> tuple:
    """Attempt coherence restoration. Return (state, survived?, delta_nrci)"""
    initial_nrci = state.nrci
    restored = restore_coherence(state, Y)
    
    # Check if survived (NRCI didn't collapse)
    survived = restored.nrci > 0.99
    delta_nrci = abs(restored.nrci - initial_nrci)
    
    return restored, survived, delta_nrci

def simulate_blood_type(name: str, toggles: list) -> dict:
    """Simulate a blood type's toggle sequence"""
    print(f"\n{'='*60}")
    print(f"Simulating: {name}")
    print(f"Toggle sequence: {toggles}")
    print(f"{'='*60}")
    
    # Start with OffBit (pure potential)
    state = CoherenceState(1.0)  # Default NRCI = 0.999997
    
    history = [{
        "step": "OffBit",
        "value": state.value,
        "nrci": state.nrci,
        "log_nrci_error": state.log_nrci_error,
        "delta_nrci": 0.0,
        "survived": True
    }]
    
    print(f"  OffBit:        value={state.value:+.6f}, NRCI={state.nrci:.9f}, log_err={state.log_nrci_error:.6f}")
    
    # Apply toggles
    for i, toggle_label in enumerate(toggles):
        state = toggle(state, toggle_label)
        state, survived, delta_nrci = survive_restore(state)
        
        history.append({
            "step": f"Toggle({toggle_label})",
            "value": state.value,
            "nrci": state.nrci,
            "log_nrci_error": state.log_nrci_error,
            "delta_nrci": delta_nrci,
            "survived": survived
        })
        
        print(f"  Toggle({toggle_label:3s}): value={state.value:+.6f}, NRCI={state.nrci:.9f}, ΔNRCI={delta_nrci:.9f}, survived={survived}")
        
        if not survived:
            print(f"  ❌ COLLAPSED - sequence terminated")
            break
    
    # Observer binding (if survived all toggles)
    if history[-1]["survived"]:
        O_OBSERVER = 3.778212425957375  # From Y_INVERSE
        state = CoherenceState(
            value=state.value * O_OBSERVER,
            log_nrci_error=state.log_nrci_error,
            net_refinements=state.net_refinements
        )
        
        history.append({
            "step": "Bind(Observer)",
            "value": state.value,
            "nrci": state.nrci,
            "log_nrci_error": state.log_nrci_error,
            "delta_nrci": 0.0,
            "survived": True
        })
        
        print(f"  Bind(Observer): value={state.value:+.6f}, NRCI={state.nrci:.9f}")
        print(f"  ✅ STABLE - blood type persists")
    
    return {
        "name": name,
        "toggles": toggles,
        "history": history,
        "final_nrci": state.nrci,
        "final_log_error": state.log_nrci_error,
        "survived": history[-1]["survived"]
    }

def compute_jaccard_distance(toggles1: list, toggles2: list) -> dict:
    """Compute Jaccard distance between two toggle sequences"""
    set1 = set(toggles1)
    set2 = set(toggles2)
    
    intersection = set1 & set2
    union = set1 | set2
    
    if len(union) == 0:
        jaccard = 1.0  # Both empty = identical
    else:
        jaccard = len(intersection) / len(union)
    
    distance = 1.0 - jaccard
    
    return {
        "shared": sorted(list(intersection)),
        "different": sorted(list(set1 ^ set2)),
        "jaccard_similarity": jaccard,
        "jaccard_distance": distance
    }

def main():
    print("\n" + "="*80)
    print("PROBE 1: ALL 8 BLOOD TYPES AS TOGGLE SEQUENCES")
    print("Using REAL UBP 3.5 CoherenceState")
    print("="*80)
    
    # Define all 8 blood types
    blood_types = {
        "O-": [],
        "O+": ["RhD"],
        "A-": ["A"],
        "A+": ["A", "RhD"],
        "B-": ["B"],
        "B+": ["B", "RhD"],
        "AB-": ["A", "B"],
        "AB+": ["A", "B", "RhD"]
    }
    
    # Simulate all
    results = {}
    for name, toggles in blood_types.items():
        results[name] = simulate_blood_type(name, toggles)
    
    # Compute Jaccard distance matrix
    print("\n" + "="*80)
    print("JACCARD DISTANCE MATRIX (Toggle History Overlap)")
    print("="*80 + "\n")
    
    blood_type_names = list(blood_types.keys())
    
    # Header
    print(f"{'':6s}", end="")
    for name in blood_type_names:
        print(f"{name:8s}", end="")
    print()
    
    # Matrix
    jaccard_matrix = {}
    for name1 in blood_type_names:
        print(f"{name1:6s}", end="")
        jaccard_matrix[name1] = {}
        for name2 in blood_type_names:
            jac_data = compute_jaccard_distance(blood_types[name1], blood_types[name2])
            dist = jac_data["jaccard_distance"]
            jaccard_matrix[name1][name2] = dist
            print(f"{dist:8.4f}", end="")
        print()
    
    # Analysis
    print("\n" + "="*80)
    print("ANALYSIS: What Did We Learn?")
    print("="*80 + "\n")
    
    print("1. SURVIVAL RATE:")
    survived_count = sum(1 for r in results.values() if r["survived"])
    print(f"   {survived_count}/8 blood types survived all toggles")
    if survived_count == 8:
        print(f"   ✅ All 8 survived - validates 2^3 = 8 stable states hypothesis\n")
    else:
        print(f"   ❌ Some failed - need to investigate why\n")
    
    print("2. NRCI DEGRADATION:")
    for name, result in results.items():
        if result["survived"]:
            nrci_changes = [h["delta_nrci"] for h in result["history"] if h["delta_nrci"] > 0]
            if nrci_changes:
                avg_delta = sum(nrci_changes) / len(nrci_changes)
                print(f"   {name:4s}: avg ΔNRCI = {avg_delta:.9f} per toggle, final NRCI = {result['final_nrci']:.9f}")
    
    print("\n3. JACCARD PATTERNS:")
    print("   Closest pairs (most shared toggles):")
    pairs = []
    for i, name1 in enumerate(blood_type_names):
        for name2 in blood_type_names[i+1:]:
            dist = jaccard_matrix[name1][name2]
            pairs.append((name1, name2, dist))
    pairs.sort(key=lambda x: x[2])
    
    for name1, name2, dist in pairs[:5]:
        jac_data = compute_jaccard_distance(blood_types[name1], blood_types[name2])
        print(f"   {name1} ↔ {name2}: d={dist:.4f}, shared={jac_data['shared']}")
    
    print("\n   Farthest pairs (no shared toggles):")
    for name1, name2, dist in pairs[-5:]:
        jac_data = compute_jaccard_distance(blood_types[name1], blood_types[name2])
        print(f"   {name1} ↔ {name2}: d={dist:.4f}, different={jac_data['different']}")
    
    # Save
    output = {
        "blood_types": results,
        "jaccard_matrix": jaccard_matrix,
        "analysis": {
            "survival_rate": f"{survived_count}/8",
            "all_survived": survived_count == 8
        }
    }
    
    with open("/home/ubuntu/ubp_probes/probe_1_results.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*80)
    print("Results saved to: probe_1_results.json")
    print("="*80)

if __name__ == "__main__":
    main()
