"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - Energy System
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Energy as coherence in UBP 3.5.

**Paradigm Shift in 3.5**:
Energy isn't a separate calculation - it's the value of a CoherenceState.
The SOC equation becomes: E = CoherenceState.value

**Zero Dependencies**: Only Python stdlib + coherence_substrate + soc_energy
"""

import math
from typing import Optional, Dict, Any
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET
from soc_energy import SOCCalculator
# observer_framework not yet migrated - will use basic observer
from system_constants import UBPConstants


# ============================================================================
# ENERGY AS COHERENCE
# ============================================================================

@dataclass
class EnergyResult:
    """
    Energy calculation result.
    
    In 3.5, energy IS a CoherenceState - this is just a convenient wrapper.
    """
    energy_state: CoherenceState
    energy_cu: float  # Coherence Units
    nrci: float
    metadata: Dict[str, Any]
    
    @property
    def energy_joules(self) -> float:
        """
        Convert to Joules (for physical interpretation).
        
        Note: This is a calibration, not a fundamental conversion.
        """
        return self.energy_cu * UBPConstants.CU_TO_JOULES_CALIBRATION


class EnergyCalculator:
    """
    Unified energy calculator for UBP 3.5.
    
    In 3.5, there's only one energy equation: E = CoherenceState.value
    The SOC calculator provides the coherence-native implementation.
    """
    
    def __init__(self):
        """Initialize energy calculator."""
        self.soc_calc = SOCCalculator()
        self.observer = None  # Will use default observer cost
    
    def calculate(
        self,
        modal_sum: float = 1.0,
        pgci_target: Optional[float] = None,
        realm: Optional[str] = None,
        **metadata
    ) -> EnergyResult:
        """
        Calculate energy as coherence.
        
        Args:
            modal_sum: Modal sum parameter (default 1.0)
            pgci_target: Target PGCI/NRCI (default NRCI_TARGET)
            realm: Optional realm context
            **metadata: Additional metadata
            
        Returns:
            EnergyResult with coherence-native energy
            
        Example:
            >>> calc = EnergyCalculator()
            >>> result = calc.calculate(modal_sum=1.0, realm='quantum')
            >>> print(f"Energy: {result.energy_cu:.6e} CU")
        """
        if pgci_target is None:
            pgci_target = NRCI_TARGET
        
        # Calculate SOC energy
        soc_result = self.soc_calc.calculate_soc_energy(modal_sum=modal_sum)
        
        # Create energy state
        energy_state = CoherenceState(
            soc_result.energy_cu,
            log_nrci_error=math.log(1 - soc_result.nrci)
        )
        
        # Build metadata
        full_metadata = {
            'modal_sum': modal_sum,
            'pgci_target': pgci_target,
            'realm': realm,
            'Y_emergent': soc_result.Y_emergent,
            'O_observer': soc_result.O_observer,
            **metadata
        }
        
        return EnergyResult(
            energy_state=energy_state,
            energy_cu=soc_result.energy_cu,
            nrci=soc_result.nrci,
            metadata=full_metadata
        )
    
    def calculate_realm_energy(
        self,
        realm: str,
        frequency: float,
        modal_sum: float = 1.0
    ) -> EnergyResult:
        """
        Calculate energy for a specific realm.
        
        Args:
            realm: Realm name ('quantum', 'gravitational', etc.)
            frequency: Characteristic frequency (Hz)
            modal_sum: Modal sum parameter
            
        Returns:
            EnergyResult for the realm
            
        Example:
            >>> calc = EnergyCalculator()
            >>> result = calc.calculate_realm_energy('quantum', frequency=1e15)
        """
        # Get realm-specific observer cost (use default for now)
        from coherence_substrate import O_OBSERVER
        o_observer = O_OBSERVER
        
        # Calculate energy
        return self.calculate(
            modal_sum=modal_sum,
            realm=realm,
            frequency=frequency,
            o_observer=o_observer
        )
    
    def compare_energies(
        self,
        energy1: EnergyResult,
        energy2: EnergyResult
    ) -> Dict[str, Any]:
        """
        Compare two energy results.
        
        Args:
            energy1: First energy result
            energy2: Second energy result
            
        Returns:
            Comparison metrics
        """
        return {
            'energy_ratio': energy2.energy_cu / energy1.energy_cu if energy1.energy_cu != 0 else float('inf'),
            'nrci_diff': energy2.nrci - energy1.nrci,
            'coherence_comparison': {
                'state1_nrci': energy1.nrci,
                'state2_nrci': energy2.nrci,
                'state1_value': energy1.energy_cu,
                'state2_value': energy2.energy_cu
            }
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def calculate_energy(
    modal_sum: float = 1.0,
    pgci_target: Optional[float] = None,
    realm: Optional[str] = None
) -> float:
    """
    Quick energy calculation (returns float in CU).
    
    Args:
        modal_sum: Modal sum parameter
        pgci_target: Target PGCI/NRCI
        realm: Optional realm context
        
    Returns:
        Energy in Coherence Units (CU)
        
    Example:
        >>> energy = calculate_energy(modal_sum=1.0)
        >>> print(f"Energy: {energy:.6e} CU")
    """
    calc = EnergyCalculator()
    result = calc.calculate(modal_sum=modal_sum, pgci_target=pgci_target, realm=realm)
    return result.energy_cu


def calculate_realm_energy(realm: str, frequency: float) -> float:
    """
    Quick realm energy calculation.
    
    Args:
        realm: Realm name
        frequency: Characteristic frequency
        
    Returns:
        Energy in Coherence Units (CU)
        
    Example:
        >>> energy = calculate_realm_energy('quantum', 1e15)
    """
    calc = EnergyCalculator()
    result = calc.calculate_realm_energy(realm, frequency)
    return result.energy_cu


def energy_to_joules(energy_cu: float) -> float:
    """
    Convert energy from CU to Joules.
    
    Note: This is a calibration factor, not a fundamental conversion.
    
    Args:
        energy_cu: Energy in Coherence Units
        
    Returns:
        Energy in Joules
    """
    return energy_cu * UBPConstants.CU_TO_JOULES_CALIBRATION


def joules_to_energy(energy_joules: float) -> float:
    """
    Convert energy from Joules to CU.
    
    Args:
        energy_joules: Energy in Joules
        
    Returns:
        Energy in Coherence Units
    """
    return energy_joules / UBPConstants.CU_TO_JOULES_CALIBRATION


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 ENERGY SYSTEM - Energy as Coherence")
    print("=" * 80)
    
    # Create calculator
    print("\n1. Creating Energy Calculator:")
    calc = EnergyCalculator()
    print("   Calculator initialized")
    
    # Calculate basic energy
    print("\n2. Basic Energy Calculation:")
    result = calc.calculate(modal_sum=1.0)
    print(f"   Energy: {result.energy_cu:.6e} CU")
    print(f"   NRCI: {result.nrci:.10f}")
    print(f"   Energy (Joules): {result.energy_joules:.6e} J")
    
    # Realm-specific energy
    print("\n3. Realm-Specific Energy:")
    realms = ['quantum', 'gravitational', 'electromagnetic']
    for realm in realms:
        result = calc.calculate_realm_energy(realm, frequency=1e15, modal_sum=1.0)
        print(f"   {realm:20s}: {result.energy_cu:.6e} CU, NRCI: {result.nrci:.6f}")
    
    # Compare energies
    print("\n4. Energy Comparison:")
    result1 = calc.calculate(modal_sum=1.0)
    result2 = calc.calculate(modal_sum=2.0)
    comparison = calc.compare_energies(result1, result2)
    print(f"   Energy ratio: {comparison['energy_ratio']:.4f}")
    print(f"   NRCI difference: {comparison['nrci_diff']:.10f}")
    
    # Quick functions
    print("\n5. Quick Energy Functions:")
    energy = calculate_energy(modal_sum=1.0)
    print(f"   Quick energy: {energy:.6e} CU")
    
    energy_j = energy_to_joules(energy)
    print(f"   In Joules: {energy_j:.6e} J")
    
    energy_back = joules_to_energy(energy_j)
    print(f"   Back to CU: {energy_back:.6e} CU")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Energy IS Coherence")
    print("E = CoherenceState.value")
    print("Zero external dependencies - Pure coherence")
    print("=" * 80)
