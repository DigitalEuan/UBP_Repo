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
        