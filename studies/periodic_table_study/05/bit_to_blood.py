"""
================================================================================
bit_to_blood.py - Pure OffBit Lifecycle Simulation
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

This module demonstrates the information-layer dynamics of blood type formation.
It shows how an OffBit, through a sequence of toggles and coherence restoration,
becomes a stable blood type antigen pattern.

This is NOT a biological simulation. It is a substrate-first view of how
information structures emerge and stabilize in the coherence landscape.
"""

import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE
from geometric_error_correction import restore_coherence
from state import OffBit

# ============================================================================
# BIT-TO-BLOOD: THE OFFBIT LIFECYCLE
# ============================================================================

def bit_to_blood(toggle_sequence: list, blood_type_name: str) -> dict:
    """
    Trace the full lifecycle of an OffBit as it becomes a blood type.
    
    Args:
        toggle_sequence: List of toggle names (e.g., ["A", "RhD"])
        blood_type_name: Human-readable name (e.g., "A+")
    
    Returns:
        dict containing the full history and final state
    """
    print(f"\n{'='*80}")
    print(f"Tracing OffBit Lifecycle → {blood_type_name}")
    print(f"{'='*80}\n")
    
    # Level 0: The OffBit - Pure Potential
    bit = OffBit(value=0)  # Start with all bits off
    print(f"[Level 0] OffBit Initialized")
    print(f"  Value: {bit.value}")
    print(f"  NRCI: {bit.nrci:.10f}")
    print(f"  Status: Pure Potential\n")
    
    history = []
    
    # Level 1-N: Toggle Sequence
    for i, toggle_name in enumerate(toggle_sequence, 1):
        print(f"[Level {i}] Toggle: {toggle_name}-antigen")
        
        # Apply toggle (this is a coherence transformation, not just bit flip)
        bit_before_toggle = bit
        bit = bit.toggle()
        
        print(f"  Before toggle: NRCI = {bit_before_toggle.nrci:.10f}")
        print(f"  After toggle:  NRCI = {bit.nrci:.10f}")
        
        # Attempt coherence restoration (the critical filter)
        bit_before_restore = bit
        result = restore_coherence(bit.coherence)
        
        # Check if GLR absorption occurred
        # GLR absorption means the pattern was "healed" - absorbed back into substrate
        glr_absorbed = isinstance(result, dict) and result.get('success', False)
        
        if glr_absorbed:
            bit_restored = result
        else:
            bit_restored, _ = result
        
        # Create new OffBit with restored coherence
        if not glr_absorbed:
            bit = OffBit(value=bit.value, coherence=bit_restored)
        
        delta_deficit = 1.0 - bit.nrci if not glr_absorbed else 0.0
        
        print(f"  After restore: NRCI = {bit.nrci if not glr_absorbed else 'N/A':.10f}")
        print(f"  δ-deficit: {delta_deficit:.10f}")
        print(f"  GLR Absorbed (healed): {glr_absorbed}")
        
        if glr_absorbed:
            print(f"  ❌ Toggle sequence FAILED - absorbed by GLR\n")
            return {
                'blood_type': blood_type_name,
                'success': False,
                'failure_stage': toggle_name,
                'history': history
            }
        
        if delta_deficit > 0.0015:
            print(f"  ❌ Toggle sequence FAILED - δ too high\n")
            return {
                'blood_type': blood_type_name,
                'success': False,
                'failure_stage': toggle_name,
                'final_delta': delta_deficit,
                'history': history
            }
        
        print(f"  ✓ Toggle survived\n")
        
        history.append({
            'stage': toggle_name,
            'operation': 'toggle',
            'delta': delta_deficit,
            'glr_absorbed': glr_absorbed,
            'nrci': bit.nrci
        })
    
    # Final Level: Observer Binding
    print(f"[Final Level] Observer Binding")
    bit_before_binding = bit
    
    # Bind to observer (multiply by O_observer, which is Y_INVERSE)
    observer_state = CoherenceState(Y_INVERSE)
    final_coherence = bit.coherence * observer_state
    bit = OffBit(value=bit.value, coherence=final_coherence)
    
    print(f"  Before binding: NRCI = {bit_before_binding.nrci:.10f}")
    print(f"  After binding:  NRCI = {bit.nrci:.10f}")
    print(f"  Observer cost: {Y_INVERSE:.15f}")
    
    history.append({
        'stage': 'Observer',
        'operation': 'bind',
        'cost': Y_INVERSE,
        'nrci': bit.nrci
    })
    
    final_delta = 1.0 - bit.nrci
    
    print(f"\n{'='*80}")
    print(f"✅ OffBit Lifecycle Complete: {blood_type_name}")
    print(f"{'='*80}")
    print(f"Final δ-deficit: {final_delta:.10f}")
    print(f"Final NRCI: {bit.nrci:.10f}")
    print(f"History: {' → '.join([h['stage'] for h in history])}")
    print(f"\n")
    
    return {
        'blood_type': blood_type_name,
        'success': True,
        'toggle_sequence': toggle_sequence,
        'final_delta': final_delta,
        'final_nrci': bit.nrci,
        'history': history
    }


# ============================================================================
# MAIN EXECUTION: ALL 8 BLOOD TYPES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("BIT-TO-BLOOD: Tracing the OffBit's Information Layer")
    print("="*80)
    print("\nThis simulation traces how an OffBit becomes each of the 8 blood types")
    print("through toggle sequences and coherence restoration.\n")
    
    # Define the 8 blood types as toggle sequences
    blood_types = [
        ([], "O-"),
        (["RhD"], "O+"),
        (["A"], "A-"),
        (["A", "RhD"], "A+"),
        (["B"], "B-"),
        (["B", "RhD"], "B+"),
        (["A", "B"], "AB-"),
        (["A", "B", "RhD"], "AB+")
    ]
    
    results = []
    
    for toggle_seq, blood_type_name in blood_types:
        result = bit_to_blood(toggle_seq, blood_type_name)
        results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY: All 8 Blood Types")
    print("="*80 + "\n")
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"Successful: {len(successful)}/8")
    print(f"Failed: {len(failed)}/8\n")
    
    if successful:
        print("Successful Blood Types:")
        for r in successful:
            print(f"  {r['blood_type']:4s}: δ = {r['final_delta']:.10f}, NRCI = {r['final_nrci']:.10f}")
    
    if failed:
        print("\nFailed Blood Types:")
        for r in failed:
            print(f"  {r['blood_type']:4s}: Failed at {r.get('failure_stage', 'unknown')}")
    
    # Save results
    output_file = "/home/ubuntu/blood_type_ubp_study_v3/bit_to_blood_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
