"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Biological Realm
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Biological realm as coherence dynamics.

**Paradigm Shift in 3.5**:
Biological phenomena aren't special - they're natural coherence dynamics.
Superposition, entanglement, tunneling - all emerge from coherence geometry.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.5
"""

import math
from typing import Dict, Optional
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET, Y
from system_constants import UBPConstants, PhysicalConstants, get_crv_for_realm
from energy_dual import EnergyCalculator


# ============================================================================
# BIOLOGICAL STATE (as CoherenceState)
# ============================================================================

@dataclass
class BiologicalState:
    """
    Biological state in UBP 3.5.
    
    In 3.5, biological states ARE coherence states. The "biological" properties
    (superposition, entanglement) are just different aspects of coherence.
    """
    coherence: CoherenceState
    amplitude: complex = 1.0+0j
    phase: float = 0.0
    entanglement_degree: float = 0.0
    
    @property
    def nrci(self) -> float:
        """NRCI of this biological state."""
        return self.coherence.nrci
    
    @property
    def is_supercoherent(self) -> bool:
        """Check if state is in supercoherent (biological) regime."""
        return self.nrci >= NRCI_TARGET
    
    @classmethod
    def create(cls, amplitude: complex = 1.0+0j, coherence_level: float = NRCI_TARGET) -> 'BiologicalState':
        """
        Create a biological state with specified coherence.
        
        Args:
            amplitude: Complex amplitude
            coherence_level: Target NRCI level
            
        Returns:
            BiologicalState
        """
        log_error = math.log(1 - coherence_level)
        coherence = CoherenceState(abs(amplitude), log_nrci_error=log_error)
        phase = math.atan2(amplitude.imag, amplitude.real)
        
        return cls(coherence=coherence, amplitude=amplitude, phase=phase)


# ============================================================================
# BIOLOGICAL REALM CALCULATOR
# ============================================================================

class BiologicalRealm:
    """
    Biological realm calculator for UBP 3.5.
    
    The biological realm is the natural regime where coherence is highest.
    """
    
    # Realm constants
    REALM_NAME = "biological"
    
    def __init__(self):
        """Initialize biological realm calculator."""
        self.energy_calc = EnergyCalculator()
        self.crv = get_crv_for_realm(self.REALM_NAME)
        self.planck_h = PhysicalConstants.PLANCK_CONSTANT
        self.planck_hbar = PhysicalConstants.PLANCK_REDUCED
    
    def calculate_biological_energy(
        self,
        biological_state: BiologicalState,
        frequency: float
    ) -> Dict[str, any]:
        """
        Calculate energy of a biological state.
        
        Args:
            biological_state: BiologicalState to calculate
            frequency: Characteristic frequency (Hz)
            
        Returns:
            Dictionary with energy results
            
        Example:
            >>> realm = BiologicalRealm()
            >>> state = BiologicalState.create(amplitude=1.0+0j)
            >>> result = realm.calculate_biological_energy(state, frequency=1e15)
        """
        # Modal sum from biological properties
        modal_sum = self._calculate_modal_sum(biological_state, frequency)
        
        # Calculate energy
        energy_result = self.energy_calc.calculate(
            modal_sum=modal_sum,
            realm=self.REALM_NAME,
            frequency=frequency
        )
        
        return {
            'energy_cu': energy_result.energy_cu,
            'energy_joules': energy_result.energy_joules,
            'nrci': energy_result.nrci,
            'biological_nrci': biological_state.nrci,
            'frequency': frequency,
            'modal_sum': modal_sum
        }
    
    def _calculate_modal_sum(
        self,
        state: BiologicalState,
        frequency: float
    ) -> float:
        """
        Calculate modal sum from biological state.
        
        Modal sum incorporates biological properties naturally.
        """
        # Amplitude contribution
        amplitude_factor = abs(state.amplitude) ** 2
        
        # Coherence contribution
        coherence_factor = state.coherence.nrci
        
        # Entanglement contribution
        entanglement_factor = 1.0 + state.entanglement_degree
        
        # Frequency contribution (logarithmic)
        freq_factor = math.log10(frequency + 1) / 20.0
        
        modal_sum = amplitude_factor * coherence_factor * entanglement_factor * freq_factor
        
        return modal_sum
    
    def model_biological_tunneling(
        self,
        barrier_height_eV: float,
        particle_energy_eV: float,
        barrier_width_nm: float
    ) -> Dict[str, float]:
        """
        Model biological tunneling as coherence transmission.
        
        In 3.5, tunneling isn't "biological weirdness" - it's coherence
        propagation through a barrier.
        
        Args:
            barrier_height_eV: Barrier height (eV)
            particle_energy_eV: Particle energy (eV)
            barrier_width_nm: Barrier width (nm)
            
        Returns:
            Tunneling results
            
        Example:
            >>> realm = BiologicalRealm()
            >>> result = realm.model_biological_tunneling(5.0, 3.0, 1.0)
            >>> print(f"Transmission: {result['transmission_probability']:.6f}")
        """
        # Convert to SI units
        eV_to_J = PhysicalConstants.ELEMENTARY_CHARGE
        barrier_height_J = barrier_height_eV * eV_to_J
        particle_energy_J = particle_energy_eV * eV_to_J
        barrier_width_m = barrier_width_nm * 1e-9
        
        # Particle mass (electron for now)
        mass = PhysicalConstants.ELECTRON_MASS
        
        # Wave number inside barrier
        if barrier_height_J > particle_energy_J:
            # Classically forbidden - exponential decay
            kappa = math.sqrt(2 * mass * (barrier_height_J - particle_energy_J)) / self.planck_hbar
            
            # Transmission coefficient (WKB approximation)
            transmission = math.exp(-2 * kappa * barrier_width_m)
        else:
            # Classically allowed
            transmission = 1.0
        
        # Create coherence state for transmitted particle
        transmitted_coherence = CoherenceState(
            transmission,
            log_nrci_error=math.log(1 - NRCI_TARGET)
        )
        
        return {
            'transmission_probability': transmission,
            'reflection_probability': 1.0 - transmission,
            'transmitted_nrci': transmitted_coherence.nrci,
            'barrier_height_eV': barrier_height_eV,
            'particle_energy_eV': particle_energy_eV,
            'barrier_width_nm': barrier_width_nm
        }
    
    def model_entanglement(
        self,
        state1: BiologicalState,
        state2: BiologicalState
    ) -> BiologicalState:
        """
        Model entanglement between two biological states.
        
        In 3.5, entanglement is coherence coupling.
        
        Args:
            state1: First biological state
            state2: Second biological state
            
        Returns:
            Entangled biological state
            
        Example:
            >>> realm = BiologicalRealm()
            >>> s1 = BiologicalState.create(amplitude=1.0+0j)
            >>> s2 = BiologicalState.create(amplitude=0.0+1.0j)
            >>> entangled = realm.model_entanglement(s1, s2)
        """
        # Entangled amplitude (Bell state)
        entangled_amplitude = (state1.amplitude + state2.amplitude) / math.sqrt(2)
        
        # Entangled coherence (average of both)
        avg_value = (state1.coherence.value + state2.coherence.value) / 2
        avg_log_error = (state1.coherence.log_nrci_error + state2.coherence.log_nrci_error) / 2
        entangled_coherence = CoherenceState(avg_value, log_nrci_error=avg_log_error)
        
        # Entanglement degree (maximum for Bell state)
        entanglement_degree = 1.0
        
        return BiologicalState(
            coherence=entangled_coherence,
            amplitude=entangled_amplitude,
            phase=math.atan2(entangled_amplitude.imag, entangled_amplitude.real),
            entanglement_degree=entanglement_degree
        )
    
    def model_superposition(
        self,
        states: list,
        weights: list
    ) -> BiologicalState:
        """
        Model superposition of biological states.
        
        In 3.5, superposition is coherence superposition.
        
        Args:
            states: List of BiologicalStates
            weights: List of probability weights
            
        Returns:
            Superposed BiologicalState
            
        Example:
            >>> realm = BiologicalRealm()
            >>> states = [BiologicalState.create(1.0+0j), BiologicalState.create(0.0+1.0j)]
            >>> weights = [0.7, 0.3]
            >>> superposed = realm.model_superposition(states, weights)
        """
        if len(states) != len(weights):
            raise ValueError("States and weights must have same length")
        
        # Normalize weights
        total_weight = sum(weights)
        norm_weights = [w / total_weight for w in weights]
        
        # Superposed amplitude
        superposed_amp = sum(s.amplitude * w for s, w in zip(states, norm_weights))
        
        # Superposed coherence (weighted average)
        weighted_value = sum(s.coherence.value * w for s, w in zip(states, norm_weights))
        weighted_log_error = sum(s.coherence.log_nrci_error * w for s, w in zip(states, norm_weights))
        superposed_coherence = CoherenceState(weighted_value, log_nrci_error=weighted_log_error)
        
        return BiologicalState(
            coherence=superposed_coherence,
            amplitude=superposed_amp,
            phase=math.atan2(superposed_amp.imag, superposed_amp.real),
            entanglement_degree=0.0
        )


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 BIOLOGICAL REALM - Biological as Coherence")
    print("=" * 80)
    
    # Create realm
    print("\n1. Creating Biological Realm:")
    realm = BiologicalRealm()
    print(f"   Realm: {realm.REALM_NAME}")
    print(f"   CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
    
    # Create biological state
    print("\n2. Creating Biological State:")
    state = BiologicalState.create(amplitude=1.0+0j, coherence_level=NRCI_TARGET)
    print(f"   Amplitude: {state.amplitude}")
    print(f"   NRCI: {state.nrci:.10f}")
    print(f"   Supercoherent: {state.is_supercoherent}")
    
    # Calculate energy
    print("\n3. Biological Energy Calculation:")
    energy = realm.calculate_biological_energy(state, frequency=1e15)
    print(f"   Energy: {energy['energy_cu']:.6e} CU")
    print(f"   NRCI: {energy['nrci']:.10f}")
    
    # Biological tunneling
    print("\n4. Biological Tunneling:")
    tunneling = realm.model_biological_tunneling(
        barrier_height_eV=5.0,
        particle_energy_eV=3.0,
        barrier_width_nm=1.0
    )
    print(f"   Transmission: {tunneling['transmission_probability']:.6e}")
    print(f"   Reflection: {tunneling['reflection_probability']:.6e}")
    
    # Entanglement
    print("\n5. Biological Entanglement:")
    state1 = BiologicalState.create(amplitude=1.0+0j)
    state2 = BiologicalState.create(amplitude=0.0+1.0j)
    entangled = realm.model_entanglement(state1, state2)
    print(f"   Entangled amplitude: {entangled.amplitude}")
    print(f"   Entanglement degree: {entangled.entanglement_degree}")
    print(f"   NRCI: {entangled.nrci:.10f}")
    
    # Superposition
    print("\n6. Biological Superposition:")
    states = [BiologicalState.create(1.0+0j), BiologicalState.create(0.0+1.0j)]
    weights = [0.7, 0.3]
    superposed = realm.model_superposition(states, weights)
    print(f"   Superposed amplitude: {superposed.amplitude}")
    print(f"   NRCI: {superposed.nrci:.10f}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Biological Phenomena are Coherence Dynamics")
    print("Zero external dependencies - Pure coherence")
    print("=" * 80)
