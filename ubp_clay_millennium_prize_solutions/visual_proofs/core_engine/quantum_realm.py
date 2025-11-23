"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6.2 - Quantum Realm
Author: Euan Craig, New Zealand
Date: November 20, 2025
================================================================================

Quantum realm as coherence dynamics.

**Paradigm Shift in 3.5**:
Quantum phenomena aren't special - they're natural coherence dynamics.
Superposition, entanglement, tunneling - all emerge from coherence geometry.

**Enhancements in 3.6.2**:
- Coherence Field ELITE integration for resonance detection
- Temporal evolution with resonance history tracking
- Parameter optimization for maximum coherence
- Perception reset detection in quantum processes

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.6
"""

import math
from typing import Dict, Optional, List
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET, Y
from system_constants import UBPConstants, PhysicalConstants, get_crv_for_realm
from energy_dual import EnergyCalculator
import coherence_field as cf
from state import OffBit
import toggle_ops as to


# ============================================================================
# QUANTUM STATE (as CoherenceState)
# ============================================================================

@dataclass
class QuantumState:
    """
    Quantum state in UBP 3.5.
    
    In 3.5, quantum states ARE coherence states. The "quantum" properties
    (superposition, entanglement) are just different aspects of coherence.
    """
    coherence: CoherenceState
    amplitude: complex = 1.0+0j
    phase: float = 0.0
    entanglement_degree: float = 0.0
    
    @property
    def nrci(self) -> float:
        """NRCI of this quantum state."""
        return self.coherence.nrci
    
    @property
    def is_supercoherent(self) -> bool:
        """Check if state is in supercoherent (quantum) regime."""
        return self.nrci >= NRCI_TARGET
    
    @classmethod
    def create(cls, amplitude: complex = 1.0+0j, coherence_level: float = NRCI_TARGET) -> 'QuantumState':
        """
        Create a quantum state with specified coherence.
        
        Args:
            amplitude: Complex amplitude
            coherence_level: Target NRCI level
            
        Returns:
            QuantumState
        """
        log_error = math.log(1 - coherence_level)
        coherence = CoherenceState(abs(amplitude), log_nrci_error=log_error)
        phase = math.atan2(amplitude.imag, amplitude.real)
        
        return cls(coherence=coherence, amplitude=amplitude, phase=phase)


# ============================================================================
# QUANTUM REALM CALCULATOR
# ============================================================================

class QuantumRealm:
    """
    Quantum realm calculator for UBP 3.5.
    
    The quantum realm is the natural regime where coherence is highest.
    """
    
    # Realm constants
    REALM_NAME = "quantum"
    
    def __init__(self):
        """Initialize quantum realm calculator."""
        self.energy_calc = EnergyCalculator()
        self.crv = get_crv_for_realm(self.REALM_NAME)
        self.planck_h = PhysicalConstants.PLANCK_CONSTANT
        self.planck_hbar = PhysicalConstants.PLANCK_REDUCED
    
    def calculate_quantum_energy(
        self,
        quantum_state: QuantumState,
        frequency: float
    ) -> Dict[str, any]:
        """
        Calculate energy of a quantum state.
        
        Args:
            quantum_state: QuantumState to calculate
            frequency: Characteristic frequency (Hz)
            
        Returns:
            Dictionary with energy results
            
        Example:
            >>> realm = QuantumRealm()
            >>> state = QuantumState.create(amplitude=1.0+0j)
            >>> result = realm.calculate_quantum_energy(state, frequency=1e15)
        """
        # Modal sum from quantum properties
        modal_sum = self._calculate_modal_sum(quantum_state, frequency)
        
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
            'quantum_nrci': quantum_state.nrci,
            'frequency': frequency,
            'modal_sum': modal_sum
        }
    
    def _calculate_modal_sum(
        self,
        state: QuantumState,
        frequency: float
    ) -> float:
        """
        Calculate modal sum from quantum state.
        
        Modal sum incorporates quantum properties naturally.
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
    
    def model_quantum_tunneling(
        self,
        barrier_height_eV: float,
        particle_energy_eV: float,
        barrier_width_nm: float
    ) -> Dict[str, float]:
        """
        Model quantum tunneling as coherence transmission.
        
        In 3.5, tunneling isn't "quantum weirdness" - it's coherence
        propagation through a barrier.
        
        Args:
            barrier_height_eV: Barrier height (eV)
            particle_energy_eV: Particle energy (eV)
            barrier_width_nm: Barrier width (nm)
            
        Returns:
            Tunneling results
            
        Example:
            >>> realm = QuantumRealm()
            >>> result = realm.model_quantum_tunneling(5.0, 3.0, 1.0)
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
        state1: QuantumState,
        state2: QuantumState
    ) -> QuantumState:
        """
        Model entanglement between two quantum states.
        
        In 3.5, entanglement is coherence coupling.
        
        Args:
            state1: First quantum state
            state2: Second quantum state
            
        Returns:
            Entangled quantum state
            
        Example:
            >>> realm = QuantumRealm()
            >>> s1 = QuantumState.create(amplitude=1.0+0j)
            >>> s2 = QuantumState.create(amplitude=0.0+1.0j)
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
        
        return QuantumState(
            coherence=entangled_coherence,
            amplitude=entangled_amplitude,
            phase=math.atan2(entangled_amplitude.imag, entangled_amplitude.real),
            entanglement_degree=entanglement_degree
        )
    
    def detect_resonances(self, states: List[CoherenceState]) -> Optional[cf.ResonanceInfo]:
        """
        Detect resonances in quantum state sequence.
        
        Uses Coherence Field ELITE to detect resonance patterns in
        quantum energy spectra, tunneling probabilities, or entanglement
        evolution.
        
        Args:
            states: List of CoherenceState objects from quantum calculations
            
        Returns:
            Resonance object if detected, None otherwise
            
        Example:
            >>> realm = QuantumRealm()
            >>> states = [quantum_state.coherence for quantum_state in spectrum]
            >>> resonance = realm.detect_resonances(states)
            >>> if resonance:
            ...     print(f"Detected {resonance.p}/{resonance.q} resonance")
        """
        if not states:
            return None
        
        detector = cf.ResonanceDetector()
        return detector.detect_resonance(states)
    
    def analyze_temporal_evolution(
        self,
        initial_offbit: OffBit,
        frequency: float,
        steps: int,
        k: float = 0.0002
    ) -> Dict:
        """
        Analyze temporal evolution of quantum state with resonance tracking.
        
        Evolves quantum state through resonance toggles and tracks coherence
        evolution, detecting resonances, perception resets, and coherence valleys.
        
        Args:
            initial_offbit: Initial OffBit state
            frequency: Characteristic quantum frequency (Hz)
            steps: Number of evolution steps
            k: Resonance parameter (default 0.0002)
            
        Returns:
            Dictionary with evolution results
            
        Example:
            >>> realm = QuantumRealm()
            >>> offbit = OffBit(0x123456)
            >>> result = realm.analyze_temporal_evolution(offbit, 1e15, 100)
            >>> print(f"Resonance detected: {result['resonance_detected']}")
            >>> print(f"Reset points: {len(result['reset_points'])}")
        """
        # Evolve state
        offbit = initial_offbit
        for t in range(steps):
            offbit = to.resonance_toggle(offbit, frequency, t * 1e-9, k=k)
        
        # Analyze with Coherence Field ELITE
        analysis = offbit.analyze_with_coherence_field()
        
        # Detect perception resets
        reset_points = offbit.detect_perception_reset_points(threshold=0.95)
        
        # Find coherence valleys
        valleys = offbit.get_coherence_valleys(window_size=5)
        
        # Get statistics
        stats = offbit.get_resonance_statistics()
        
        return {
            'final_state': offbit,
            'resonance_analysis': analysis,
            'resonance_detected': analysis.get('resonance_detected', False) if analysis else False,
            'reset_points': reset_points,
            'coherence_valleys': valleys,
            'statistics': stats,
            'history_length': offbit.resonance_history_length
        }
    
    def optimize_parameters(
        self,
        states: List[CoherenceState],
        target_param: str = 'frequency'
    ) -> Dict:
        """
        Optimize quantum parameters for maximum coherence.
        
        Uses Coherence Field ELITE's parameter space optimizer to find
        optimal quantum parameters (frequency, energy, coupling, etc.).
        
        Args:
            states: List of CoherenceState objects
            target_param: Parameter to optimize ('frequency', 'energy', etc.)
            
        Returns:
            Dictionary with optimization results
            
        Example:
            >>> realm = QuantumRealm()
            >>> states = [...]  # Quantum states at different parameters
            >>> result = realm.optimize_parameters(states, 'frequency')
            >>> print(f"Optimal frequency: {result['optimal_value']}")
        """
        if not states:
            return {'error': 'No states provided'}
        
        # Find state with highest NRCI
        best_idx = max(range(len(states)), key=lambda i: states[i].nrci)
        return {
            'optimal_index': best_idx,
            'optimal_nrci': states[best_idx].nrci,
            'optimal_value': states[best_idx].value,
            'target_param': target_param
        }
    
    def model_superposition(
        self,
        states: list,
        weights: list
    ) -> QuantumState:
        """
        Model superposition of quantum states.
        
        In 3.5, superposition is coherence superposition.
        
        Args:
            states: List of QuantumStates
            weights: List of probability weights
            
        Returns:
            Superposed QuantumState
            
        Example:
            >>> realm = QuantumRealm()
            >>> states = [QuantumState.create(1.0+0j), QuantumState.create(0.0+1.0j)]
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
        
        return QuantumState(
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
    print("UBP 3.6.2 QUANTUM REALM - Quantum as Coherence + Field Intelligence")
    print("=" * 80)
    
    # Create realm
    print("\n1. Creating Quantum Realm:")
    realm = QuantumRealm()
    print(f"   Realm: {realm.REALM_NAME}")
    print(f"   CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
    
    # Create quantum state
    print("\n2. Creating Quantum State:")
    state = QuantumState.create(amplitude=1.0+0j, coherence_level=NRCI_TARGET)
    print(f"   Amplitude: {state.amplitude}")
    print(f"   NRCI: {state.nrci:.10f}")
    print(f"   Supercoherent: {state.is_supercoherent}")
    
    # Calculate energy
    print("\n3. Quantum Energy Calculation:")
    energy = realm.calculate_quantum_energy(state, frequency=1e15)
    print(f"   Energy: {energy['energy_cu']:.6e} CU")
    print(f"   NRCI: {energy['nrci']:.10f}")
    
    # Quantum tunneling
    print("\n4. Quantum Tunneling:")
    tunneling = realm.model_quantum_tunneling(
        barrier_height_eV=5.0,
        particle_energy_eV=3.0,
        barrier_width_nm=1.0
    )
    print(f"   Transmission: {tunneling['transmission_probability']:.6e}")
    print(f"   Reflection: {tunneling['reflection_probability']:.6e}")
    
    # Entanglement
    print("\n5. Quantum Entanglement:")
    state1 = QuantumState.create(amplitude=1.0+0j)
    state2 = QuantumState.create(amplitude=0.0+1.0j)
    entangled = realm.model_entanglement(state1, state2)
    print(f"   Entangled amplitude: {entangled.amplitude}")
    print(f"   Entanglement degree: {entangled.entanglement_degree}")
    print(f"   NRCI: {entangled.nrci:.10f}")
    
    # Superposition
    print("\n6. Quantum Superposition:")
    states_list = [QuantumState.create(1.0+0j), QuantumState.create(0.0+1.0j)]
    weights = [0.7, 0.3]
    superposed = realm.model_superposition(states_list, weights)
    print(f"   Superposed amplitude: {superposed.amplitude}")
    print(f"   NRCI: {superposed.nrci:.10f}")
    
    # NEW: Temporal Evolution with Resonance Tracking
    print("\n7. Temporal Evolution (NEW in 3.6.2):")
    offbit = OffBit(0x123456)
    evolution = realm.analyze_temporal_evolution(offbit, frequency=1e15, steps=50)
    print(f"   History length: {evolution['history_length']}")
    print(f"   Resonance detected: {evolution['resonance_detected']}")
    print(f"   Reset points: {len(evolution['reset_points'])}")
    print(f"   Coherence valleys: {len(evolution['coherence_valleys'])}")
    if evolution['statistics']['history_length'] > 0:
        print(f"   Avg resonance factor: {evolution['statistics']['avg_resonance_factor']:.6f}")
    
    # NEW: Resonance Detection in Spectrum
    print("\n8. Resonance Detection in Spectrum (NEW in 3.6.2):")
    # Create quantum spectrum
    spectrum_states = []
    for i in range(20):
        freq = 1e15 * (1 + i * 0.1)
        q_state = QuantumState.create(amplitude=1.0+0j)
        energy = realm.calculate_quantum_energy(q_state, frequency=freq)
        spectrum_states.append(CoherenceState(energy['energy_cu'], 
                                             log_nrci_error=math.log(1 - energy['nrci'])))
    
    resonance = realm.detect_resonances(spectrum_states)
    if resonance:
        print(f"   Detected {resonance.p}/{resonance.q} resonance")
        print(f"   Confidence: {resonance.confidence:.1%}")
    else:
        print(f"   No strong resonance detected")
    
    print("\n" + "=" * 80)
    print("UBP 3.6.2: Quantum + Coherence Field ELITE Integration")
    print("Resonance detection, temporal evolution, parameter optimization")
    print("=" * 80)
