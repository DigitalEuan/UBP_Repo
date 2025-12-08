#!/usr/bin/env python3
"""
Information Ship v5.0 Enhancements - Moonshine Edition 🌙
=========================================================

This module demonstrates the new features in v5.0:
1. Monster group corrections for improved mass predictions
2. Golay G₂₄ error-correction for self-healing coherence states

Usage:
    from information_ship_v5_enhancements import (
        predict_mass_with_moonshine,
        create_self_healing_state,
        run_moonshine_resonance_trial
    )

Author: Euan Craig (polished by Manus AI)
Date: December 8, 2025
Version: 5.0.0
"""

import math
import numpy as np
from typing import Tuple, Dict, Any, Optional
import json

# Import the enhancement modules
from moonshine_data import (
    get_moonshine_correction,
    get_conway_orbit_correction,
    get_triple_shell_coupling,
    CONWAY_ORBITS
)

from golay_g24 import (
    encode_value,
    decode_value,
    inject_errors,
    GolayCodeword
)

# ============================================================================
# ENHANCED MASS PREDICTION WITH MONSTER CORRECTIONS
# ============================================================================

print("="*80)
print("🌙 INFORMATION SHIP v5.0 - MOONSHINE ENHANCEMENTS")
print("="*80)

# Core constants (from v4.0)
PI = math.pi
Y = PI / (PI**2 + 2)
Y_INVERSE = PI + 2/PI

# Physical constants
M_ELECTRON = 9.1093837015e-31  # kg
M_MUON = 1.883531627e-28  # kg
M_TAU = 3.16754e-27  # kg

def predict_mass_with_moonshine(particle: str, reference: str = 'electron',
                                conjugacy_class: str = '1A',
                                use_conway: bool = True,
                                use_triple_coupling: bool = True) -> Dict[str, float]:
    """
    Predict mass ratio using Monster group corrections.
    
    This is the v5.0 enhanced prediction that includes:
    1. Basic geometric prediction (Y_INVERSE^(Δnorm²/2))
    2. Moonshine modular correction (from McKay-Thompson series)
    3. Conway orbit correction (from Co₁ automorphisms)
    4. Triple-shell coupling (higher-order interactions)
    
    Args:
        particle: Target particle ('muon', 'tau', etc.)
        reference: Reference particle (default: 'electron')
        conjugacy_class: Monster conjugacy class ('1A', '2A', '3A', '2B')
        use_conway: Include Conway orbit corrections
        use_triple_coupling: Include triple-shell coupling
    
    Returns:
        Dictionary with all correction factors and final prediction
    """
    # Shell assignments (from v4.0)
    shell_map = {
        'electron': 4,
        'muon': 6,
        'tau': 8
    }
    
    norm_sq_particle = shell_map.get(particle, 0)
    norm_sq_ref = shell_map.get(reference, 4)
    
    # 1. Basic geometric prediction
    delta_norm_sq = norm_sq_particle - norm_sq_ref
    basic_ratio = Y_INVERSE ** (delta_norm_sq / 2.0)
    
    # 2. Moonshine modular correction (CALIBRATED as perturbative)
    moonshine_raw = get_moonshine_correction(norm_sq_ref, norm_sq_particle, conjugacy_class)
    # Use logarithmic scaling to make it perturbative
    moonshine_corr = 1.0 + 0.01 * math.log(moonshine_raw)  # Small perturbation
    
    # 3. Conway orbit correction (CALIBRATED)
    conway_corr = 1.0
    if use_conway:
        conway_raw = get_conway_orbit_correction(norm_sq_ref, norm_sq_particle)
        # Use square root to moderate the effect
        conway_corr = 1.0 + 0.05 * (math.sqrt(conway_raw) - 1.0)
    
    # 4. Triple-shell coupling (CALIBRATED)
    triple_corr = 1.0
    if use_triple_coupling and delta_norm_sq >= 4:
        # For tau (4→6→8), use triple coupling
        intermediate = norm_sq_ref + 2
        triple_raw = get_triple_shell_coupling(norm_sq_ref, intermediate, norm_sq_particle, CONWAY_ORBITS)
        # Use logarithmic scaling
        triple_corr = 1.0 + 0.02 * math.log(triple_raw)
    
    # Combined prediction (perturbative corrections)
    final_ratio = basic_ratio * moonshine_corr * conway_corr * triple_corr
    
    # Monster group simple correction (from v4.0)
    monster_simple = 196883 / 196560
    final_ratio *= monster_simple
    
    return {
        'basic_ratio': basic_ratio,
        'moonshine_correction': moonshine_corr,
        'conway_correction': conway_corr,
        'triple_coupling': triple_corr,
        'monster_simple': monster_simple,
        'final_ratio': final_ratio,
        'norm_sq_from': norm_sq_ref,
        'norm_sq_to': norm_sq_particle
    }

# ============================================================================
# SELF-HEALING COHERENCE STATE WITH GOLAY G₂₄
# ============================================================================

class SelfHealingCoherenceState:
    """
    Enhanced CoherenceState with Golay G₂₄ error-correction.
    
    NEW in v5.0: Automatic error detection and correction using
    the perfect Golay [24,12,8] code.
    """
    
    def __init__(self, value: float, log_nrci_error: Optional[float] = None):
        self.value = value
        self.log_nrci_error = log_nrci_error if log_nrci_error is not None else math.log(1 - 0.999997)
        self.golay_codeword: Optional[GolayCodeword] = None
        self.error_history: list = []
    
    @property
    def nrci(self) -> float:
        """Compute NRCI from log-error."""
        return 1.0 - math.exp(self.log_nrci_error)
    
    def encode_golay(self) -> GolayCodeword:
        """Encode state value into Golay G₂₄ codeword."""
        self.golay_codeword = encode_value(self.value)
        return self.golay_codeword
    
    def inject_errors(self, num_errors: int) -> None:
        """
        Inject random errors for testing self-healing.
        
        Args:
            num_errors: Number of bit flips (1-3 correctable, 4+ detectable)
        """
        if self.golay_codeword is None:
            self.encode_golay()
        
        corrupted_bits = inject_errors(self.golay_codeword.bits, num_errors)
        self.golay_codeword = GolayCodeword(corrupted_bits)
        
        # Record error injection
        self.error_history.append({
            'type': 'injection',
            'num_errors': num_errors,
            'nrci_before': self.nrci
        })
    
    def self_heal(self) -> Tuple[bool, int]:
        """
        Automatic error detection and correction using Golay decoding.
        
        Returns:
            (success, num_errors_corrected)
        """
        if self.golay_codeword is None:
            return (False, 0)
        
        # Decode with error correction
        decoded_value, num_errors, success = decode_value(self.golay_codeword)
        
        if success:
            # Update value with corrected version
            self.value = decoded_value
            
            # Improve NRCI after successful healing
            if num_errors > 0:
                self.log_nrci_error -= 0.5 * num_errors  # Healing improves coherence
            
            # Record healing
            self.error_history.append({
                'type': 'healing',
                'num_errors_corrected': num_errors,
                'nrci_after': self.nrci,
                'success': True
            })
            
            return (True, num_errors)
        else:
            # Healing failed (too many errors)
            self.error_history.append({
                'type': 'healing',
                'num_errors_corrected': -1,
                'nrci_after': self.nrci,
                'success': False
            })
            
            return (False, -1)
    
    def get_error_report(self) -> Dict[str, Any]:
        """Get comprehensive error history report."""
        return {
            'current_value': self.value,
            'current_nrci': self.nrci,
            'error_history': self.error_history,
            'total_injections': sum(1 for e in self.error_history if e['type'] == 'injection'),
            'total_healings': sum(1 for e in self.error_history if e['type'] == 'healing'),
            'successful_healings': sum(1 for e in self.error_history if e.get('success', False))
        }

def create_self_healing_state(value: float) -> SelfHealingCoherenceState:
    """Create a new self-healing coherence state."""
    return SelfHealingCoherenceState(value)

# ============================================================================
# MOONSHINE RESONANCE SEA TRIAL (NEW in v5.0)
# ============================================================================

def run_moonshine_resonance_trial() -> Dict[str, Any]:
    """
    NEW SEA TRIAL: Moonshine Resonance
    
    Tests:
    1. Monster corrections on lepton mass predictions
    2. Golay error-correction on coherence states
    3. Combined self-healing under Monster symmetry
    
    Returns:
        Comprehensive trial results
    """
    print("\n" + "="*80)
    print("SEA TRIAL: Moonshine Resonance 🌙")
    print("="*80)
    
    results = {
        'trial_name': 'Moonshine Resonance',
        'description': 'Monster corrections + Golay self-healing',
        'mass_predictions': {},
        'error_correction': {},
        'combined_test': {}
    }
    
    # Part 1: Mass predictions with Monster corrections
    print("\nPart 1: Mass Predictions with Monster Corrections")
    print("-" * 60)
    
    for particle in ['muon', 'tau']:
        pred = predict_mass_with_moonshine(particle, 'electron', conjugacy_class='1A')
        
        # Get experimental value
        exp_values = {
            'muon': M_MUON / M_ELECTRON,
            'tau': M_TAU / M_ELECTRON
        }
        exp_value = exp_values[particle]
        
        # Compute error
        error = abs(pred['final_ratio'] - exp_value) / exp_value * 100
        
        results['mass_predictions'][particle] = {
            'predicted': pred['final_ratio'],
            'experimental': exp_value,
            'error_percent': error,
            'corrections': {
                'basic': pred['basic_ratio'],
                'moonshine': pred['moonshine_correction'],
                'conway': pred['conway_correction'],
                'triple': pred['triple_coupling']
            }
        }
        
        print(f"{particle.capitalize()}:")
        print(f"  Predicted: {pred['final_ratio']:.2f}")
        print(f"  Experimental: {exp_value:.2f}")
        print(f"  Error: {error:.2f}%")
        print(f"  Moonshine correction: {pred['moonshine_correction']:.3f}×")
        print(f"  Conway correction: {pred['conway_correction']:.3f}×")
    
    # Part 2: Golay error-correction tests
    print("\nPart 2: Golay G₂₄ Error-Correction Tests")
    print("-" * 60)
    
    test_value = 0.123456789
    state = create_self_healing_state(test_value)
    state.encode_golay()
    
    error_correction_results = []
    
    for num_errors in [1, 2, 3]:
        # Inject errors
        state_test = create_self_healing_state(test_value)
        state_test.encode_golay()
        state_test.inject_errors(num_errors)
        
        # Attempt self-healing
        success, corrected = state_test.self_heal()
        
        # Measure recovery
        recovery_error = abs(state_test.value - test_value)
        
        error_correction_results.append({
            'num_errors': num_errors,
            'success': success,
            'errors_corrected': corrected,
            'recovery_error': recovery_error,
            'nrci_after_healing': state_test.nrci
        })
        
        print(f"{num_errors}-error correction:")
        print(f"  Success: {success}")
        print(f"  Errors corrected: {corrected}")
        print(f"  Recovery error: {recovery_error:.2e}")
        print(f"  NRCI after healing: {state_test.nrci:.6f}")
    
    results['error_correction'] = error_correction_results
    
    # Part 3: Combined test (Monster symmetry + self-healing)
    print("\nPart 3: Combined Monster Symmetry + Self-Healing")
    print("-" * 60)
    
    # Create a coherence state representing muon mass ratio
    muon_pred = predict_mass_with_moonshine('muon', 'electron')
    muon_state = create_self_healing_state(muon_pred['final_ratio'])
    muon_state.encode_golay()
    
    # Inject 2 errors (simulating coherence degradation)
    muon_state.inject_errors(2)
    print(f"Muon mass ratio (corrupted): {muon_state.value:.2f}")
    
    # Self-heal
    success, corrected = muon_state.self_heal()
    print(f"Self-healing: {success} ({corrected} errors corrected)")
    print(f"Muon mass ratio (healed): {muon_state.value:.2f}")
    print(f"NRCI after healing: {muon_state.nrci:.6f}")
    
    results['combined_test'] = {
        'particle': 'muon',
        'predicted_ratio': muon_pred['final_ratio'],
        'after_corruption': muon_state.value,
        'after_healing': muon_state.value,
        'healing_success': success,
        'final_nrci': muon_state.nrci
    }
    
    print("\n" + "="*80)
    print("Moonshine Resonance Trial Complete!")
    print("="*80)
    
    return results

# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("DEMONSTRATION: Information Ship v5.0 Enhancements")
    print("="*80)
    
    # Demo 1: Mass predictions with Monster corrections
    print("\n--- Demo 1: Mass Predictions with Monster Corrections ---")
    
    muon_pred = predict_mass_with_moonshine('muon', 'electron', conjugacy_class='1A')
    print(f"\nMuon mass ratio prediction:")
    print(f"  Basic (v4.0): {muon_pred['basic_ratio']:.2f}")
    print(f"  + Moonshine: ×{muon_pred['moonshine_correction']:.3f}")
    print(f"  + Conway: ×{muon_pred['conway_correction']:.3f}")
    print(f"  Final (v5.0): {muon_pred['final_ratio']:.2f}")
    print(f"  Experimental: {M_MUON/M_ELECTRON:.2f}")
    print(f"  Error: {abs(muon_pred['final_ratio'] - M_MUON/M_ELECTRON) / (M_MUON/M_ELECTRON) * 100:.2f}%")
    
    # Demo 2: Self-healing coherence state
    print("\n--- Demo 2: Self-Healing Coherence State ---")
    
    test_value = 0.987654321
    state = create_self_healing_state(test_value)
    print(f"\nOriginal value: {test_value:.9f}")
    print(f"Initial NRCI: {state.nrci:.6f}")
    
    # Encode
    state.encode_golay()
    print(f"Encoded to Golay G₂₄: {state.golay_codeword}")
    
    # Inject 3 errors
    state.inject_errors(3)
    print(f"\nAfter 3-error injection:")
    print(f"  Corrupted codeword: {state.golay_codeword}")
    
    # Self-heal
    success, corrected = state.self_heal()
    print(f"\nSelf-healing:")
    print(f"  Success: {success}")
    print(f"  Errors corrected: {corrected}")
    print(f"  Recovered value: {state.value:.9f}")
    print(f"  Recovery error: {abs(state.value - test_value):.2e}")
    print(f"  Final NRCI: {state.nrci:.6f}")
    
    # Demo 3: Full Moonshine Resonance Trial
    print("\n--- Demo 3: Full Moonshine Resonance Trial ---")
    
    trial_results = run_moonshine_resonance_trial()
    
    # Save results
    with open('moonshine_resonance_results.json', 'w') as f:
        json.dump(trial_results, f, indent=2)
    
    print(f"\n✓ Results saved to: moonshine_resonance_results.json")
    
    print("\n" + "="*80)
    print("🌙 Information Ship v5.0 Moonshine Edition - Ready to Sail!")
    print("="*80)
