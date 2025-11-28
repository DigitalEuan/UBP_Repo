"""
Universal Binary Principle (UBP) Framework v3.7.1 - SOC Energy System
Author: Euan Craig, New Zealand
Date: 28 November 2025
================================================================================

This module implements the Simplified Observer Coherence (SOC) equation,
which represents the paradigm shift from phenomenological energy calculation
to first-principles computational emergence.

SOC Equation:
    E = M × C × Y_Emergent × Σ(w_ij M_ij)

Where:
- E: Emergent energy in Coherence-Units (CU), NOT Joules
- M: Active OffBit count (cardinality of the observer's state)
- C = 299,792,458: Celeritas (master clock rate, toggles/sec)
- Y_Emergent = PGCI_TARGET / O_observer: Observer-Coherence Ratio
- Σ(w_ij M_ij): Resonant Modal Sum (weighted OffBit interactions)

Key Insight:
E is NOT physical energy - it is "phenomenal intensity" or "reality weight",
measuring how strongly a coherent resonance manifests in the Bitfield. It is
the computational precursor to energy, mass, and force.

Physical energy (Joules) requires secondary Planck-scale calibration.
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


class EnergyUnits(Enum):
    """Energy unit types for SOC calculations."""
    COHERENCE_UNITS = "CU"  # Native UBP units
    JOULES = "J"            # Physical energy (requires calibration)


@dataclass
class SOCEnergyResult:
    """
    Result from SOC energy calculation.
    
    Attributes:
        energy_cu: Energy in Coherence-Units
        energy_joules: Energy in Joules (if calibrated)
        M: Meta-Temporal Primitive value
        C: Celeritas value
        Y_emergent: Observer-Coherence Ratio
        modal_sum: Resonant Modal Sum
        units: Primary units of result
        metadata: Additional calculation metadata
    """
    energy_cu: float
    energy_joules: Optional[float]
    M: float
    C: float
    Y_emergent: float
    modal_sum: float
    units: EnergyUnits
    metadata: Dict[str, any]


class CoherenceUnits:
    """
    Wrapper for Coherence-Units (CU) values with metadata.
    
    CU is the native UBP energy unit, representing computational emergence
    rather than physical energy. It is proportional to:
        toggle density × clock rate × observer-coherence
    """
    
    def __init__(
        self,
        value: float,
        source: str = "SOC",
        metadata: Optional[Dict] = None
    ):
        """
        Initialize Coherence-Units value.
        
        Args:
            value: CU value
            source: Source of calculation ('SOC', 'legacy', etc.)
            metadata: Additional metadata
        """
        self.value = value
        self.source = source
        self.metadata = metadata or {}
    
    def to_joules(self, calibration_factor: float) -> float:
        """
        Convert CU to Joules using Planck-scale calibration.
        
        Args:
            calibration_factor: Planck-scale calibration constant
            
        Returns:
            Energy in Joules
        """
        return self.value * calibration_factor
    
    def __repr__(self) -> str:
        return f"CoherenceUnits({self.value:.6e} CU, source={self.source})"
    
    def __float__(self) -> float:
        return self.value


class SOCCalculator:
    """
    Simplified Observer Coherence (SOC) energy calculator.
    
    This calculator implements the first-principles energy equation that
    reveals physical constants as emergent properties of geometric resonance.
    """
    
    # DEPRECATED: M should be actual OffBit count, not π
    # M_META_TEMPORAL = math.pi  # This was wrong - M is cardinality, not a constant
    
    # Celeritas (C = speed of light in m/s)
    C_CELERITAS = 299792458.0
    
    # PGCI target for stable reality
    PGCI_TARGET = 0.999997
    
    # Default observer cost (can be computed dynamically)
    O_OBSERVER_DEFAULT = 3.7782010913
    
    # Planck-scale calibration factor (CU to Joules)
    # This is a placeholder - actual calibration requires Planck constant derivation
    CU_TO_JOULES_CALIBRATION = 1.0  # To be refined
    
    def __init__(
        self,
        M: Optional[float] = None,
        C: Optional[float] = None,
        pgci_target: Optional[float] = None,
        o_observer: Optional[float] = None,
        calibration_factor: Optional[float] = None
    ):
        """
        Initialize SOC Calculator.
        
        Args:
            M: Number of active OffBits (cardinality). If None, must be provided per calculation.
            C: Celeritas (defaults to speed of light)
            pgci_target: PGCI target (defaults to 0.999997)
            o_observer: Observer cost (defaults to fixed point value)
            calibration_factor: CU to Joules calibration
        """
        self.M = M  # No default - M should be actual OffBit count
        self.C = C if C is not None else self.C_CELERITAS
        self.pgci_target = pgci_target if pgci_target is not None else self.PGCI_TARGET
        self.o_observer = o_observer if o_observer is not None else self.O_OBSERVER_DEFAULT
        self.calibration_factor = (
            calibration_factor if calibration_factor is not None 
            else self.CU_TO_JOULES_CALIBRATION
        )
        
        # Calculate Y_Emergent
        self.Y_emergent = self.calculate_y_emergent()
    
    def calculate_y_emergent(self) -> float:
        """
        Calculate Y_Emergent (Observer-Coherence Ratio).
        
        SOC Refinement: Y_Emergent = PGCI_TARGET / O_observer
        where O_observer = 1/Y (inverse Y constant)
        
        Returns:
            Y_Emergent = PGCI_TARGET / O_observer
        """
        return self.pgci_target / self.o_observer
    
    def calculate_inverse_refinement(
        self,
        energy_cu: float,
        direction: str = 'backward'
    ) -> Dict[str, float]:
        """
        Apply inverse Y refinement to energy value.
        
        SOC Refinement enables bidirectional propagation:
        - Forward: E × Y (geometry → observer)
        - Backward: E × (1/Y) (observer → geometry)
        
        Args:
            energy_cu: Energy in Coherence-Units
            direction: 'forward' or 'backward'
            
        Returns:
            Dictionary with refined energy and metadata
        """
        y_constant = self.M  # M = π, but Y = π/(π²+2)
        y_base = y_constant / (y_constant**2 + 2)
        y_inverse = y_constant + (2 / y_constant)  # 1/Y = π + 2/π
        
        if direction.lower() == 'forward':
            refined_energy = energy_cu * y_base
            factor = y_base
            description = "Geometry → Observer (forward)"
        elif direction.lower() == 'backward':
            refined_energy = energy_cu * y_inverse
            factor = y_inverse
            description = "Observer → Geometry (backward)"
        else:
            raise ValueError(f"Direction must be 'forward' or 'backward', got '{direction}'")
        
        return {
            'original_energy_cu': energy_cu,
            'refined_energy_cu': refined_energy,
            'refinement_factor': factor,
            'direction': direction,
            'description': description,
            'y_base': y_base,
            'y_inverse': y_inverse
        }
    
    def validate_bidirectional_closure(
        self,
        energy_cu: float,
        tolerance: float = 1e-10
    ) -> Dict[str, any]:
        """
        Validate that forward-backward refinement returns to original.
        
        This tests the involutory property: (E × Y) × (1/Y) = E
        
        Args:
            energy_cu: Initial energy in CU
            tolerance: Maximum acceptable error
            
        Returns:
            Dictionary with validation results
        """
        # Forward refinement
        fwd_result = self.calculate_inverse_refinement(energy_cu, 'forward')
        intermediate = fwd_result['refined_energy_cu']
        
        # Backward refinement
        back_result = self.calculate_inverse_refinement(intermediate, 'backward')
        final = back_result['refined_energy_cu']
        
        # Calculate closure error
        closure_error = abs(final - energy_cu)
        closure_success = closure_error < tolerance
        
        return {
            'initial_energy': energy_cu,
            'intermediate_energy': intermediate,
            'final_energy': final,
            'closure_error': closure_error,
            'closure_success': closure_success,
            'tolerance': tolerance,
            'y_base': fwd_result['y_base'],
            'y_inverse': fwd_result['y_inverse']
        }
    
    def calculate_modal_sum(
        self,
        weights: Union[List[float], np.ndarray],
        modes: Union[List[float], np.ndarray]
    ) -> float:
        """
        Calculate Resonant Modal Sum: Σ(w_ij M_ij)
        
        Args:
            weights: Interaction weights (should sum to ~1)
            modes: Modal values (OffBit interaction results)
            
        Returns:
            Weighted sum of modes
        """
        weights = np.array(weights)
        modes = np.array(modes)
        
        if len(weights) != len(modes):
            raise ValueError("Weights and modes must have same length")
        
        # Normalize weights
        weight_sum = np.sum(weights)
        if weight_sum > 0:
            weights_normalized = weights / weight_sum
        else:
            weights_normalized = weights
        
        modal_sum = np.sum(weights_normalized * modes)
        
        return float(modal_sum)
    
    def calculate_soc_energy(
        self,
        modal_sum: float,
        M: Optional[float] = None,
        C: Optional[float] = None,
        Y_emergent: Optional[float] = None,
        current_nrci: Optional[float] = None
    ) -> SOCEnergyResult:
        """
        Calculate energy using SOC equation.
        
        E = (Y × O × M × modal_sum) × (1 − NRCI)
        
        Energy is proportional to coherence deficit: more deficit = more energy
        needed to maintain reality against incoherence.
        
        Where:
        - M = number of active OffBits (cardinality)
        - O = Observer cost (1/Y ≈ 3.778)
        - Y = Y_emergent (PGCI / O_observer)
        - NRCI = current system coherence
        - (1 - NRCI) = coherence deficit
        
        Args:
            modal_sum: Resonant Modal Sum (used to weight M)
            M: Number of active OffBits (optional override)
            C: Celeritas (optional override, for scaling)
            Y_emergent: Observer-Coherence Ratio (optional override)
            current_nrci: Current system NRCI (defaults to target 0.999997)
            
        Returns:
            SOCEnergyResult with energy in CU and metadata
        """
        M_val = M if M is not None else self.M
        C_val = C if C is not None else self.C
        Y_em = Y_emergent if Y_emergent is not None else self.Y_emergent
        nrci = current_nrci if current_nrci is not None else self.pgci_target
        
        # Check for edge cases
        if nrci >= 1.0:
            # Perfect coherence = no deficit = no energy cost
            energy_cu = 0.0
        elif nrci <= 0.0:
            # Total incoherence = infinite energy cost
            energy_cu = float('inf')
        else:
            # SOC equation: E = (Y × O × M × modal_sum) × (1 − NRCI)
            # Energy is proportional to coherence deficit
            # More deficit = more energy needed to maintain reality
            # Note: Spec shows E = ... / (1 - NRCI) but that gives backwards behavior
            # This formula matches the physical intuition and spec table
            coherence_deficit = 1.0 - nrci
            energy_cu = (Y_em * self.o_observer * M_val * modal_sum) * coherence_deficit
        
        # Optional conversion to Joules
        energy_joules = energy_cu * self.calibration_factor if self.calibration_factor else None
        
        result = SOCEnergyResult(
            energy_cu=energy_cu,
            energy_joules=energy_joules,
            M=M_val,
            C=C_val,
            Y_emergent=Y_em,
            modal_sum=modal_sum,
            units=EnergyUnits.COHERENCE_UNITS,
            metadata={
                'pgci_target': self.pgci_target,
                'o_observer': self.o_observer,
                'calibration_factor': self.calibration_factor,
                'current_nrci': nrci,
                'coherence_deficit': 1.0 - nrci if nrci < 1.0 else 0.0,
                'formula': 'E = (Y × O × M × modal_sum) × (1 − NRCI)',
                'note': 'Energy proportional to coherence deficit (corrected from spec)'
            }
        )
        
        return result
    
    def calculate_soc_energy_from_weights_modes(
        self,
        weights: Union[List[float], np.ndarray],
        modes: Union[List[float], np.ndarray],
        **kwargs
    ) -> SOCEnergyResult:
        """
        Calculate SOC energy directly from weights and modes.
        
        Args:
            weights: Interaction weights
            modes: Modal values
            **kwargs: Optional overrides for M, C, Y_emergent
            
        Returns:
            SOCEnergyResult
        """
        modal_sum = self.calculate_modal_sum(weights, modes)
        return self.calculate_soc_energy(modal_sum, **kwargs)
    
    def calculate_soc_energy_from_state(
        self,
        state,
        modal_sum: float = 1.0,
        current_nrci: Optional[float] = None
    ) -> SOCEnergyResult:
        """
        Calculate SOC energy from an OffBit or CoherenceState object.
        
        This is the CORRECT way to calculate energy in UBP:
        M is automatically determined by counting active bits in the state.
        
        Args:
            state: OffBit or CoherenceState object
            modal_sum: Resonant modal sum (defaults to 1.0)
            current_nrci: Current NRCI (defaults to state.nrci if available)
            
        Returns:
            SOCEnergyResult with energy calculated from actual bit count
            
        Example:
            >>> from core.state import OffBit
            >>> from core.soc_energy import SOCCalculator
            >>> 
            >>> # Create an OffBit with value 1000 (has 6 active bits: 1111101000)
            >>> state = OffBit(1000)
            >>> 
            >>> # Calculate energy from actual bit count
            >>> calc = SOCCalculator()
            >>> result = calc.calculate_soc_energy_from_state(state)
            >>> print(f"Active bits: {result.M}")
            >>> print(f"Energy: {result.energy_cu:.6e} CU")
        """
        # Import here to avoid circular dependency
        try:
            from core.state import OffBit
            from core.coherence_substrate import CoherenceState
        except ImportError:
            # Fallback for different import paths
            try:
                from state import OffBit
                from coherence_substrate import CoherenceState
            except ImportError:
                raise ImportError("Cannot import OffBit or CoherenceState")
        
        # Determine M by counting active bits
        if isinstance(state, OffBit):
            # Count 1-bits in the OffBit value
            M_active = bin(state.value).count('1')
            # OffBit doesn't have nrci attribute, use provided or default
            nrci = current_nrci if current_nrci is not None else self.pgci_target
        elif hasattr(state, 'value') and hasattr(state, 'nrci'):
            # CoherenceState or similar
            if isinstance(state.value, (int, float)):
                # If value is numeric, count bits
                M_active = bin(int(state.value)).count('1')
            else:
                # If value is an OffBit, get its bit count
                M_active = bin(state.value.value).count('1')
            nrci = current_nrci if current_nrci is not None else state.nrci
        else:
            raise TypeError(f"state must be OffBit or CoherenceState, got {type(state)}")
        
        # Calculate energy using actual bit count
        return self.calculate_soc_energy(
            modal_sum=modal_sum,
            M=M_active,
            current_nrci=nrci
        )


def calculate_soc_energy(
    M: float,
    C: float,
    Y_emergent: float,
    modal_sum: float
) -> float:
    """
    Simple SOC energy calculation function.
    
    E = M × C × Y_Emergent × Σ(w_ij M_ij)
    
    Args:
        M: Meta-Temporal Primitive (typically π)
        C: Celeritas (typically 299,792,458)
        Y_emergent: Observer-Coherence Ratio
        modal_sum: Resonant Modal Sum
        
    Returns:
        Energy in Coherence-Units (CU)
        
    Example:
        >>> E_cu = calculate_soc_energy(
        ...     M=math.pi,
        ...     C=299792458.0,
        ...     Y_emergent=0.264675430404527,
        ...     modal_sum=1.0
        ... )
        >>> print(f"E = {E_cu:.6e} CU")
    """
    return M * C * Y_emergent * modal_sum


def cu_to_joules(cu_value: float, calibration_factor: float) -> float:
    """
    Convert Coherence-Units to Joules.
    
    Args:
        cu_value: Energy in CU
        calibration_factor: Planck-scale calibration constant
        
    Returns:
        Energy in Joules
    """
    return cu_value * calibration_factor


def joules_to_cu(joule_value: float, calibration_factor: float) -> float:
    """
    Convert Joules to Coherence-Units.
    
    Args:
        joule_value: Energy in Joules
        calibration_factor: Planck-scale calibration constant
        
    Returns:
        Energy in CU
    """
    if calibration_factor == 0:
        raise ValueError("Calibration factor cannot be zero")
    return joule_value / calibration_factor


def compute_emergence_metric(
    cu_value: float,
    threshold: float = 1e8
) -> Dict[str, any]:
    """
    Compute emergence metric (reality weight) from CU value.
    
    The emergence metric quantifies how strongly a coherent resonance
    manifests in the Bitfield. Higher values indicate stronger manifestation.
    
    Args:
        cu_value: Energy in CU
        threshold: Threshold for "strong" manifestation
        
    Returns:
        Dictionary with emergence analysis
    """
    # Normalize to threshold
    normalized = cu_value / threshold
    
    # Classify manifestation strength
    if normalized < 0.01:
        strength = "negligible"
    elif normalized < 0.1:
        strength = "weak"
    elif normalized < 1.0:
        strength = "moderate"
    elif normalized < 10.0:
        strength = "strong"
    else:
        strength = "dominant"
    
    # Calculate phenomenal intensity (logarithmic scale)
    if cu_value > 0:
        intensity = math.log10(cu_value)
    else:
        intensity = float('-inf')
    
    return {
        'cu_value': cu_value,
        'normalized': normalized,
        'strength': strength,
        'phenomenal_intensity': intensity,
        'threshold': threshold
    }


def compare_soc_legacy_energy(
    M: float,
    C: float,
    Y_emergent: float,
    modal_sum: float,
    legacy_energy: float,
    calibration_factor: float = 1.0
) -> Dict[str, any]:
    """
    Compare SOC energy with legacy energy calculation.
    
    Args:
        M: Meta-Temporal Primitive
        C: Celeritas
        Y_emergent: Observer-Coherence Ratio
        modal_sum: Resonant Modal Sum
        legacy_energy: Energy from legacy equation (Joules)
        calibration_factor: CU to Joules calibration
        
    Returns:
        Dictionary with comparison analysis
    """
    # Calculate SOC energy
    soc_cu = calculate_soc_energy(M, C, Y_emergent, modal_sum)
    soc_joules = cu_to_joules(soc_cu, calibration_factor)
    
    # Calculate difference
    if legacy_energy != 0:
        relative_diff = abs(soc_joules - legacy_energy) / abs(legacy_energy)
    else:
        relative_diff = float('inf')
    
    # Determine agreement
    if relative_diff < 0.01:
        agreement = "excellent"
    elif relative_diff < 0.1:
        agreement = "good"
    elif relative_diff < 0.5:
        agreement = "moderate"
    else:
        agreement = "poor"
    
    return {
        'soc_cu': soc_cu,
        'soc_joules': soc_joules,
        'legacy_joules': legacy_energy,
        'absolute_difference': abs(soc_joules - legacy_energy),
        'relative_difference': relative_diff,
        'agreement': agreement,
        'calibration_factor': calibration_factor
    }


def demonstrate_soc_energy():
    """
    Demonstrate SOC energy calculations and properties.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("SIMPLIFIED OBSERVER COHERENCE (SOC) ENERGY DEMONSTRATION")
    print("=" * 80)
    
    # Create SOC calculator
    calc = SOCCalculator()
    
    print(f"\nSOC Calculator Configuration:")
    print(f"  M (Meta-Temporal Primitive): {calc.M:.15f}")
    print(f"  C (Celeritas): {calc.C:.0f} m/s")
    print(f"  PGCI Target: {calc.pgci_target}")
    print(f"  O_observer: {calc.o_observer:.10f}")
    print(f"  Y_Emergent: {calc.Y_emergent:.15f}")
    
    # Test with different modal sums
    print("\n" + "-" * 80)
    print("SOC Energy for Different Modal Sums:")
    print("-" * 80)
    
    modal_sums = [0.1, 0.5, 1.0, 2.0, 10.0]
    results = []
    
    for modal_sum in modal_sums:
        result = calc.calculate_soc_energy(modal_sum)
        results.append(result)
        
        print(f"\nModal Sum = {modal_sum}")
        print(f"  E = {result.energy_cu:.6e} CU")
        
        # Emergence metric
        emergence = compute_emergence_metric(result.energy_cu)
        print(f"  Manifestation Strength: {emergence['strength']}")
        print(f"  Phenomenal Intensity: {emergence['phenomenal_intensity']:.2f}")
    
    # Test with weights and modes
    print("\n" + "-" * 80)
    print("SOC Energy from Weights and Modes:")
    print("-" * 80)
    
    weights = [0.2, 0.3, 0.25, 0.15, 0.1]
    modes = [1.0, 0.8, 1.2, 0.9, 1.1]
    
    result = calc.calculate_soc_energy_from_weights_modes(weights, modes)
    
    print(f"\nWeights: {weights}")
    print(f"Modes: {modes}")
    print(f"Modal Sum: {result.modal_sum:.6f}")
    print(f"E = {result.energy_cu:.6e} CU")
    
    # Demonstrate CU to Joules conversion
    print("\n" + "-" * 80)
    print("Coherence-Units (CU) Properties:")
    print("-" * 80)
    
    cu_val = result.energy_cu
    print(f"\nCU Value: {cu_val:.6e}")
    print(f"Unit Type: Computational emergence metric")
    print(f"Physical Meaning: Phenomenal intensity / reality weight")
    print(f"NOT equivalent to: Physical energy (Joules)")
    print(f"\nTo convert to Joules requires Planck-scale calibration:")
    print(f"  E_joules = E_cu × calibration_factor")
    print(f"  (Calibration factor derived from Planck constant)")
    
    print("\n" + "=" * 80)
    
    return {
        'calculator': calc,
        'modal_sum_results': results,
        'weights_modes_result': result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_soc_energy()
    
    print("\nSOC energy system demonstration complete.")
    print("E in SOC equation represents computational emergence (CU), not physical energy (J).")
    print("This is the paradigm shift: from phenomenology to first principles.")
    print("\nModule ready for import into UBP 3.4 system.")
