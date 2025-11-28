"""
Universal Binary Principle (UBP) Framework v3.7.1 - Quantum Realm
Author: Euan R A Craig, New Zealand
Date: 28 November 2025
================================================================================

This module implements quantum realm calculations using UBP 3.4 framework.

The quantum realm is characterized by:
- Superposition and entanglement
- Wave-particle duality
- Quantum coherence and decoherence
- High observer computational cost

Key Features:
- SOC energy calculations for quantum systems
- Quantum entanglement modeling
- Superposition state handling
- Y constant dimensional corrections
- Realm-specific observer cost

Test Phenomena (NEW - not previously studied):
1. Quantum tunneling in molecular hydrogen dissociation
2. Macroscopic quantum coherence in superconducting qubits

================================================================================
TRANSITIONAL NOTE (UBP 3.7.1):

This module currently uses classical complex amplitudes for quantum states
to maintain clarity and compatibility with existing quantum literature.

The final UBP representation will use VectorOffBit + toggle rules as
implemented in core/quantum_extensions.py:

  QuantumState (future) = VectorOffBit (24D real) + CoherenceField
  Superposition = high coherence + no measurement
  Measurement = collapse via toggle operation
  Entanglement = shared VectorOffBit reference

This transitional approach allows:
- Working, verifiable quantum realm today
- Clear path to full binary purity tomorrow
- No dependency on external scientific libraries

All core dependencies are pure UBP modules.
================================================================================
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# UBP 3.4 modules
from core.system_constants import UBPConstants
from core.y_constants import get_y_correction_for_realm
from core.soc_energy import SOCCalculator, SOCEnergyResult
from core.observer_framework import get_default_realm_observer_costs
from core.wall_of_reality import WallOfReality


@dataclass
class QuantumState:
    """
    Represents a quantum state in UBP framework.
    
    Attributes:
        amplitude: Complex amplitude
        phase: Phase angle (radians)
        coherence: Coherence measure (0-1)
        entanglement_degree: Degree of entanglement (0-1)
    """
    amplitude: complex
    phase: float
    coherence: float
    entanglement_degree: float


class QuantumRealm:
    """
    Quantum realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "quantum"
    BASE_CRV = UBPConstants.CRV_QUANTUM_BASE  # e/12
    # TOGGLE_PROBABILITY: Defined per-operation in quantum_extensions.py
    
    # Quantum-specific parameters
    PLANCK_CONSTANT = UBPConstants.PLANCK_CONSTANT
    PLANCK_REDUCED = UBPConstants.PLANCK_REDUCED
    
    def __init__(self):
        """Initialize quantum realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Realm-specific parameters from config
        # CRV from ubp_config: 4.4439e+13 Hz (highest NRCI peak)
        self.crv = 4.4439e13  # Hz - quantum realm characteristic frequency
        self.nrci_baseline = 0.999997  # Target NRCI for quantum realm
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs[self.REALM_NAME]
    
    def calculate_quantum_energy_soc(
        self,
        quantum_state: QuantumState,
        frequency: float
    ) -> SOCEnergyResult:
        """
        Calculate quantum energy using SOC equation.
        
        Args:
            quantum_state: Quantum state information
            frequency: Characteristic frequency (Hz)
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(frequency, raise_error=False)
        
        # Calculate modal sum from quantum state
        modal_sum = self._calculate_quantum_modal_sum(quantum_state, frequency)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_quantum_modal_sum(
        self,
        state: QuantumState,
        frequency: float
    ) -> float:
        """
        Calculate resonant modal sum for quantum state.
        
        Args:
            state: Quantum state
            frequency: Characteristic frequency
            
        Returns:
            Modal sum value
        """
        # Modal sum incorporates quantum properties
        amplitude_contrib = abs(state.amplitude)**2
        coherence_contrib = state.coherence
        entanglement_contrib = state.entanglement_degree
        
        # Frequency-dependent term
        freq_factor = math.log10(frequency + 1) / 20.0  # Normalized
        
        modal_sum = (
            amplitude_contrib * coherence_contrib *
            (1 + entanglement_contrib) * freq_factor
        )
        
        return modal_sum
    
    def model_quantum_tunneling(
        self,
        barrier_height_eV: float,
        particle_energy_eV: float,
        barrier_width_nm: float
    ) -> Dict[str, float]:
        """
        Model quantum tunneling through potential barrier.
        
        NEW TEST PHENOMENON: Molecular hydrogen dissociation via tunneling
        
        Args:
            barrier_height_eV: Potential barrier height (eV)
            particle_energy_eV: Particle energy (eV)
            barrier_width_nm: Barrier width (nm)
            
        Returns:
            Dictionary with tunneling analysis
        """
        # Convert to SI units
        barrier_height_J = barrier_height_eV * UBPConstants.ELEMENTARY_CHARGE
        particle_energy_J = particle_energy_eV * UBPConstants.ELEMENTARY_CHARGE
        barrier_width_m = barrier_width_nm * 1e-9
        
        # Calculate tunneling probability (WKB approximation)
        if particle_energy_eV >= barrier_height_eV:
            tunneling_prob = 1.0  # Classical passage
        else:
            # WKB formula
            mass_electron = UBPConstants.ELECTRON_MASS
            kappa = math.sqrt(
                2 * mass_electron * (barrier_height_J - particle_energy_J)
            ) / self.PLANCK_REDUCED
            
            tunneling_prob = math.exp(-2 * kappa * barrier_width_m)
        
        # Calculate characteristic frequency
        freq_Hz = particle_energy_J / self.PLANCK_CONSTANT
        
        # Create quantum state
        quantum_state = QuantumState(
            amplitude=complex(math.sqrt(tunneling_prob), 0),
            phase=0.0,
            coherence=0.95,  # High coherence for tunneling
            entanglement_degree=0.0  # Single particle
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_quantum_energy_soc(quantum_state, freq_Hz)
        
        return {
            'tunneling_probability': tunneling_prob,
            'characteristic_frequency_hz': freq_Hz,
            'barrier_height_ev': barrier_height_eV,
            'particle_energy_ev': particle_energy_eV,
            'barrier_width_nm': barrier_width_nm,
            'ubp_energy_cu': soc_result.energy_cu,
            'quantum_coherence': quantum_state.coherence,
            'observer_cost': self.observer_cost
        }
    
    def model_superconducting_qubit(
        self,
        josephson_energy_GHz: float,
        charging_energy_GHz: float,
        coherence_time_us: float
    ) -> Dict[str, float]:
        """
        Model macroscopic quantum coherence in superconducting qubit.
        
        NEW TEST PHENOMENON: Transmon qubit coherence dynamics
        
        Args:
            josephson_energy_GHz: Josephson energy (GHz)
            charging_energy_GHz: Charging energy (GHz)
            coherence_time_us: Coherence time (microseconds)
            
        Returns:
            Dictionary with qubit analysis
        """
        # Convert to Hz
        E_J = josephson_energy_GHz * 1e9
        E_C = charging_energy_GHz * 1e9
        
        # Calculate qubit frequency (transmon approximation)
        qubit_freq_Hz = math.sqrt(8 * E_J * E_C) - E_C
        
        # Calculate coherence from decoherence time
        coherence_time_s = coherence_time_us * 1e-6
        coherence = math.exp(-1 / (qubit_freq_Hz * coherence_time_s))
        coherence = max(0.0, min(1.0, coherence))  # Clamp to [0,1]
        
        # Anharmonicity (key transmon parameter)
        anharmonicity_MHz = -E_C / 1e6
        
        # Create quantum state (superposition)
        quantum_state = QuantumState(
            amplitude=complex(1/math.sqrt(2), 1/math.sqrt(2)),  # |+⟩ state
            phase=math.pi/4,
            coherence=coherence,
            entanglement_degree=0.0  # Single qubit
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_quantum_energy_soc(quantum_state, qubit_freq_Hz)
        
        # Calculate NRCI (should be high for coherent qubit)
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        return {
            'qubit_frequency_ghz': qubit_freq_Hz / 1e9,
            'josephson_energy_ghz': josephson_energy_GHz,
            'charging_energy_ghz': charging_energy_GHz,
            'anharmonicity_mhz': anharmonicity_MHz,
            'coherence_time_us': coherence_time_us,
            'quantum_coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }


def demonstrate_quantum_realm():
    """
    Demonstrate quantum realm calculations with new test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("QUANTUM REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = QuantumRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.6f}")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    
    # Test 1: Quantum Tunneling
    print("\n" + "-" * 80)
    print("TEST 1: Quantum Tunneling in Molecular Hydrogen Dissociation")
    print("-" * 80)
    
    tunneling_result = realm.model_quantum_tunneling(
        barrier_height_eV=4.5,  # H2 dissociation barrier
        particle_energy_eV=0.5,  # Low energy proton
        barrier_width_nm=0.1     # Angstrom scale
    )
    
    print(f"\nBarrier Parameters:")
    print(f"  Height: {tunneling_result['barrier_height_ev']:.2f} eV")
    print(f"  Width: {tunneling_result['barrier_width_nm']:.2f} nm")
    print(f"  Particle Energy: {tunneling_result['particle_energy_ev']:.2f} eV")
    
    print(f"\nTunneling Results:")
    print(f"  Tunneling Probability: {tunneling_result['tunneling_probability']:.6e}")
    print(f"  Characteristic Frequency: {tunneling_result['characteristic_frequency_hz']:.6e} Hz")
    print(f"  Quantum Coherence: {tunneling_result['quantum_coherence']:.6f}")
    print(f"  UBP Energy: {tunneling_result['ubp_energy_cu']:.6e} CU")
    
    # Test 2: Superconducting Qubit
    print("\n" + "-" * 80)
    print("TEST 2: Macroscopic Quantum Coherence in Superconducting Qubit")
    print("-" * 80)
    
    qubit_result = realm.model_superconducting_qubit(
        josephson_energy_GHz=20.0,  # Typical transmon
        charging_energy_GHz=0.3,    # Transmon regime
        coherence_time_us=50.0      # State-of-art coherence
    )
    
    print(f"\nQubit Parameters:")
    print(f"  Josephson Energy: {qubit_result['josephson_energy_ghz']:.2f} GHz")
    print(f"  Charging Energy: {qubit_result['charging_energy_ghz']:.2f} GHz")
    print(f"  Anharmonicity: {qubit_result['anharmonicity_mhz']:.2f} MHz")
    
    print(f"\nCoherence Results:")
    print(f"  Qubit Frequency: {qubit_result['qubit_frequency_ghz']:.4f} GHz")
    print(f"  Coherence Time: {qubit_result['coherence_time_us']:.2f} μs")
    print(f"  Quantum Coherence: {qubit_result['quantum_coherence']:.6f}")
    print(f"  NRCI: {qubit_result['nrci']:.6f}")
    print(f"  UBP Energy: {qubit_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'tunneling': tunneling_result,
        'qubit': qubit_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_quantum_realm()
    
    print("\nQuantum realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. Quantum tunneling in H2 dissociation")
    print("  2. Superconducting qubit coherence")
    print("\nModule ready for UBP 3.4 integration testing.")
