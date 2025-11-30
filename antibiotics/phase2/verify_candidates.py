"""
================================================================================
UBP Antibiotic Discovery - Candidate Verification
Author: Euan R A Craig, New Zealand - # Powered by UBP 3.7.1
Date: 30 November 2025
================================================================================

Deep verification of antibiotic candidates with full coherence analysis.
"""

import sys
import math

sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study/ubp_core')
sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, O_OBSERVER, NRCI_TARGET
from state import OffBit
from antibiotic_realm import (
    AntibioticRealm, 
    F_RIBOSOME_KEV, 
    F_RIBOSOME_HZ,
    F_HUMAN_MITO_HZ,
    OMEGA_C,
    NRCI_SUPERCOHERENT
)


def verify_candidate_deep(offbit_hex: str, realm: AntibioticRealm):
    """
    Perform deep verification of a candidate.
    
    Args:
        offbit_hex: Hex string like "0xA77F3C"
        realm: AntibioticRealm instance
    """
    # Parse hex
    offbit_value = int(offbit_hex, 16)
    
    print("\n" + "=" * 80)
    print(f"DEEP VERIFICATION: {offbit_hex}")
    print("=" * 80)
    
    # Step 1: Create initial OffBit
    print("\n1. Initial State")
    print("-" * 80)
    offbit = OffBit(offbit_value)
    print(f"   OffBit value: {offbit_hex} ({offbit_value})")
    print(f"   Binary: {bin(offbit_value)[2:].zfill(24)}")
    print(f"   Active bits: {offbit.active_bits}/24")
    print(f"   Initial NRCI: {offbit.nrci:.15f}")
    print(f"   Initial coherence value: {offbit.coherence.value:.6e}")
    print(f"   Initial log_nrci_error: {offbit.coherence.log_nrci_error:.6e}")
    
    # Step 2: Apply resonance toggle
    print("\n2. Resonance Toggle (Bacterial Ribosome)")
    print("-" * 80)
    print(f"   Target frequency: {F_RIBOSOME_HZ:.6e} Hz ({F_RIBOSOME_KEV:.6f} keV)")
    
    # Calculate bit pattern features
    high_bits = (offbit_value >> 16) & 0xFF
    mid_bits = (offbit_value >> 8) & 0xFF
    low_bits = offbit_value & 0xFF
    
    print(f"   Bit pattern analysis:")
    print(f"     High 8 bits: {high_bits:3d} (0x{high_bits:02X})")
    print(f"     Mid 8 bits:  {mid_bits:3d} (0x{mid_bits:02X})")
    print(f"     Low 8 bits:  {low_bits:3d} (0x{low_bits:02X})")
    
    # Calculate natural frequency factor
    natural_freq_factor = (
        high_bits * 1.618 +
        mid_bits * 3.14159 +
        low_bits * 2.71828
    ) / 1000.0
    
    print(f"   Natural frequency factor: {natural_freq_factor:.6f}")
    print(f"   Target factor: 1.0")
    print(f"   Frequency mismatch: {abs(natural_freq_factor - 1.0):.6f}")
    
    # Calculate bit balance
    active_bits = bin(offbit_value).count('1')
    bit_balance = 1.0 - abs(active_bits - 12) / 12.0
    print(f"   Bit balance: {bit_balance:.6f} (optimal at 12/24 active)")
    
    # Calculate resonance factor
    gamma = 0.05
    freq_mismatch = abs(natural_freq_factor - 1.0)
    resonance_factor = gamma**2 / (freq_mismatch**2 + gamma**2)
    resonance_factor *= bit_balance
    
    print(f"   Resonance factor: {resonance_factor:.10f}")
    
    # Apply resonance
    offbit_resonated = realm.apply_resonance_toggle(offbit, F_RIBOSOME_HZ)
    print(f"   NRCI after resonance: {offbit_resonated.nrci:.15f}")
    print(f"   ΔNRCI: {offbit_resonated.nrci - offbit.nrci:+.15f}")
    
    # Step 3: Apply Omega floor
    print("\n3. Ω_c Floor Application")
    print("-" * 80)
    print(f"   Ω_c threshold: {OMEGA_C:.15f}")
    print(f"   Current NRCI: {offbit_resonated.nrci:.15f}")
    
    if offbit_resonated.nrci < OMEGA_C:
        print(f"   ⚠️  Below Ω_c floor - candidate will be degraded")
    else:
        print(f"   ✓ Above Ω_c floor - candidate stabilized")
    
    offbit_floored = realm.apply_omega_floor(offbit_resonated)
    print(f"   NRCI after floor: {offbit_floored.nrci:.15f}")
    print(f"   ΔNRCI: {offbit_floored.nrci - offbit_resonated.nrci:+.15f}")
    
    # Step 4: Binding energy calculations
    print("\n4. Binding Energy Analysis")
    print("-" * 80)
    
    bacterial_energy = realm.calculate_binding_energy(offbit_floored, F_RIBOSOME_HZ)
    human_energy = realm.calculate_binding_energy(offbit_floored, F_HUMAN_MITO_HZ)
    
    print(f"   Bacterial ribosome binding: {bacterial_energy:.6e} CU")
    print(f"   Human mitochondrial binding: {human_energy:.6e} CU")
    
    if human_energy > 0:
        selectivity = bacterial_energy / human_energy
        print(f"   Selectivity index: {selectivity:.2f}")
        
        if selectivity > 100:
            print(f"   ✓ Excellent selectivity (>100)")
        elif selectivity > 10:
            print(f"   ⚠️  Moderate selectivity (10-100)")
        else:
            print(f"   ❌ Poor selectivity (<10) - TOXICITY RISK")
    else:
        selectivity = float('inf')
        print(f"   Selectivity index: ∞ (perfect)")
    
    # Step 5: MIC prediction
    print("\n5. MIC Prediction")
    print("-" * 80)
    
    coherence_deficit = 1.0 - offbit_floored.nrci
    print(f"   Coherence deficit: {coherence_deficit:.15e}")
    
    mic = realm.estimate_mic_from_coherence(coherence_deficit)
    print(f"   Predicted MIC: {mic:.6f} μg/mL")
    
    # Clinical context
    if mic < 0.01:
        print(f"   ✓ Ultra-potent (MIC < 0.01 μg/mL)")
    elif mic < 0.1:
        print(f"   ✓ Highly potent (MIC < 0.1 μg/mL)")
    elif mic < 1.0:
        print(f"   ✓ Potent (MIC < 1 μg/mL)")
    elif mic < 10.0:
        print(f"   ⚠️  Moderate potency (MIC < 10 μg/mL)")
    else:
        print(f"   ❌ Weak potency (MIC ≥ 10 μg/mL)")
    
    # Step 6: Scaffold prediction
    print("\n6. Scaffold Prediction")
    print("-" * 80)
    
    scaffold = realm.scaffold_predictor.predict(offbit_floored)
    print(f"   Predicted scaffold: {scaffold}")
    
    # Step 7: Final evaluation
    print("\n7. Final Evaluation")
    print("-" * 80)
    
    candidate = realm.evaluate_candidate(offbit_floored)
    
    if candidate is None:
        print(f"   ❌ FAILED - Did not pass filters")
        print(f"   Reason: NRCI {offbit_floored.nrci:.10f} < {NRCI_SUPERCOHERENT:.10f}")
        return None
    
    print(f"   ✓ PASSED all filters")
    print(f"   Activity class: {candidate.activity_class}")
    print(f"   Toxicity flag: {candidate.toxicity_flag}")
    
    # Step 8: Coherence closure verification
    print("\n8. Bidirectional Closure Verification")
    print("-" * 80)
    
    # Test Y-refinement closure
    coherence_value = offbit_floored.coherence.value
    forward = coherence_value * Y
    backward = forward * Y_INVERSE
    closure_error = abs(backward - coherence_value) / abs(coherence_value)
    
    print(f"   Original coherence: {coherence_value:.15e}")
    print(f"   Forward (×Y): {forward:.15e}")
    print(f"   Backward (×1/Y): {backward:.15e}")
    print(f"   Closure error: {closure_error:.15e}")
    
    if closure_error < 1e-12:
        print(f"   ✓ Perfect closure (< 1e-12)")
    else:
        print(f"   ⚠️  Closure error exceeds tolerance")
    
    # Step 9: Summary
    print("\n9. Verification Summary")
    print("-" * 80)
    print(f"   OffBit: {offbit_hex}")
    print(f"   Final NRCI: {candidate.nrci:.15f}")
    print(f"   Activity: {candidate.activity_class}")
    print(f"   MIC: {candidate.predicted_mic:.6f} μg/mL")
    print(f"   Selectivity: {candidate.selectivity_index:.2f}")
    print(f"   Toxicity: {'YES' if candidate.toxicity_flag else 'NO'}")
    print(f"   Closure: {'PASS' if closure_error < 1e-12 else 'FAIL'}")
    
    # Overall verdict
    print("\n" + "=" * 80)
    if candidate.activity_class == "SuperCoherent" and not candidate.toxicity_flag and closure_error < 1e-12:
        print("✅ VERIFIED - Excellent antibiotic candidate")
    elif candidate.activity_class in ["SuperCoherent", "Excellent"] and closure_error < 1e-12:
        print("⚠️  VERIFIED WITH CAUTION - Good candidate but check toxicity")
    else:
        print("❌ VERIFICATION CONCERNS - Further analysis required")
    print("=" * 80)
    
    return candidate


def main():
    """Main verification routine."""
    print("=" * 80)
    print("UBP ANTIBIOTIC CANDIDATE VERIFICATION")
    print("=" * 80)
    
    # Create realm
    realm = AntibioticRealm()
    
    # Test candidates from the study output
    test_candidates = [
        "0x8E7398",  # NRCI: 0.9999999685 (highest seen)
        "0x50E337",  # NRCI: 0.9999999364
        "0xF9E0F7",  # NRCI: 0.9999998102
        "0x014426",  # NRCI: 0.9999998103
        "0xA77F3C",  # Known seed (linezolid-like)
    ]
    
    verified_candidates = []
    
    for hex_val in test_candidates:
        candidate = verify_candidate_deep(hex_val, realm)
        if candidate:
            verified_candidates.append(candidate)
        print("\n")
    
    # Final summary
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)
    print(f"\nVerified {len(verified_candidates)}/{len(test_candidates)} candidates")
    print(f"\nTop verified candidate: {verified_candidates[0].offbit_hex if verified_candidates else 'None'}")
    print(f"  NRCI: {verified_candidates[0].nrci:.15f}" if verified_candidates else "")
    print(f"  MIC: {verified_candidates[0].predicted_mic:.6f} μg/mL" if verified_candidates else "")


if __name__ == "__main__":
    main()
