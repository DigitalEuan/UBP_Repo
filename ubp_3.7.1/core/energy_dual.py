"""
Universal Binary Principle (UBP) Framework v3.7 - Dual-Mode Energy System
Author: Euan Craig, New Zealand
Date: 31 October 2025
================================================================================

This module implements dual-mode energy calculations:
1. SOC Mode (UBP 3.4): Simplified Observer Coherence equation
2. Legacy Mode (UBP 3.2): Full energy equation with explicit factors

The SOC mode is the primary calculation method for UBP 3.4, representing
first-principles computational emergence. The legacy mode is maintained for
backward compatibility and educational purposes.

Usage:
    # SOC mode (default)
    E_cu = energy_auto(mode='soc', modal_sum=1.0)
    
    # Legacy mode
    E_joules = energy_auto(mode='legacy', M=1000, w_sum=0.1)
    
    # Automatic mode selection
    E = energy_auto(M=1000)  # Uses SOC by default
"""

import math
from typing import List, Optional, Dict, Any, Union
import warnings

# UBP 3.4 modules
from core.y_constants import (
    calculate_y_constant,
    calculate_y_emergent,
    YConstants
)
from core.soc_energy import (
    SOCCalculator,
    calculate_soc_energy,
    SOCEnergyResult
)
from core.observer_framework import (
    SelfActualizingObserver,
    calculate_realm_specific_observer_cost
)
from core.system_constants import UBPConstants

# UBP 3.2 modules (for legacy mode)
try:
    from ubp_config import get_config, UBPConfig
    from global_coherence import GlobalCoherenceIndex
    from observer_scaling import ObserverScaling
    _config = get_config()
    _global_coherence_system = GlobalCoherenceIndex()
    LEGACY_MODE_AVAILABLE = True
except ImportError:
    LEGACY_MODE_AVAILABLE = False
    warnings.warn("Legacy mode dependencies not available. SOC mode only.")


class EnergyMode:
    """Energy calculation mode selector."""
    SOC = "soc"          # Simplified Observer Coherence (UBP 3.4)
    LEGACY = "legacy"    # Full equation (UBP 3.2)
    AUTO = "auto"        # Automatic selection


class DualModeEnergyCalculator:
    """
    Dual-mode energy calculator supporting both SOC and legacy equations.
    """
    
    def __init__(
        self,
        default_mode: str = EnergyMode.SOC,
        auto_calibrate: bool = True
    ):
        """
        Initialize dual-mode energy calculator.
        
        Args:
            default_mode: Default calculation mode ('soc' or 'legacy')
            auto_calibrate: Automatically calibrate CU to Joules conversion
        """
        self.default_mode = default_mode
        self.auto_calibrate = auto_calibrate
        
        # Initialize SOC calculator
        self.soc_calc = SOCCalculator()
        
        # Initialize observer
        self.observer = SelfActualizingObserver()
        
        # Calibration factor (CU to Joules)
        self.calibration_factor = UBPConstants.CU_TO_JOULES_CALIBRATION
    
    def calculate(
        self,
        mode: Optional[str] = None,
        **kwargs
    ) -> Union[float, SOCEnergyResult]:
        """
        Calculate energy in specified mode.
        
        Args:
            mode: Calculation mode ('soc', 'legacy', or 'auto')
            **kwargs: Mode-specific parameters
                For SOC mode (RECOMMENDED):
                    state: OffBit or CoherenceState (automatic bit counting)
                For SOC mode (LEGACY):
                    modal_sum: Pre-calculated modal sum
                    M: Manual bit count (deprecated)
            
        Returns:
            Energy value (float for legacy, SOCEnergyResult for SOC)
        
        Example:
            >>> from core.state import OffBit
            >>> calc = DualModeEnergyCalculator()
            >>> state = OffBit(1000)
            >>> result = calc.calculate(mode='soc', state=state)  # RECOMMENDED
            >>> print(f"M={result.M}, E={result.energy_cu:.6e} CU")
        """
        mode = mode or self.default_mode
        
        if mode == EnergyMode.AUTO:
            # Auto-select based on available parameters
            if 'modal_sum' in kwargs or 'weights' in kwargs:
                mode = EnergyMode.SOC
            else:
                mode = EnergyMode.LEGACY if LEGACY_MODE_AVAILABLE else EnergyMode.SOC
        
        if mode == EnergyMode.SOC:
            return self._calculate_soc(**kwargs)
        elif mode == EnergyMode.LEGACY:
            if not LEGACY_MODE_AVAILABLE:
                raise ValueError("Legacy mode not available. Missing dependencies.")
            return self._calculate_legacy(**kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'soc', 'legacy', or 'auto'")
    
    def _calculate_soc(
        self,
        state: Optional[Any] = None,
        modal_sum: Optional[float] = None,
        weights: Optional[List[float]] = None,
        modes: Optional[List[float]] = None,
        M: Optional[float] = None,
        C: Optional[float] = None,
        Y_emergent: Optional[float] = None,
        o_observer: Optional[float] = None,
        current_nrci: Optional[float] = None,
        **kwargs
    ) -> SOCEnergyResult:
        """
        Calculate energy using SOC equation.
        
        PREFERRED: Pass `state` (OffBit or CoherenceState) for automatic bit counting.
        LEGACY: Pass `modal_sum` or `M` manually (deprecated).
        
        Args:
            state: OffBit or CoherenceState object (RECOMMENDED - counts bits automatically)
            modal_sum: Pre-calculated resonant modal sum (legacy)
            weights: Interaction weights (if modal_sum not provided)
            modes: Modal values (if modal_sum not provided)
            M: Meta-Temporal Primitive (optional override - deprecated, use state instead)
            C: Celeritas (optional override)
            Y_emergent: Observer-Coherence Ratio (optional override)
            o_observer: Observer cost (for Y_emergent calculation)
            current_nrci: Current NRCI (optional)
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # PREFERRED PATH: Use real bit count from state
        if state is not None:
            # Delegate to the TRUE SOC calculation with automatic bit counting
            return self.soc_calc.calculate_soc_energy_from_state(
                state=state,
                modal_sum=modal_sum if modal_sum is not None else 1.0,
                current_nrci=current_nrci
            )
        
        # LEGACY PATH: Manual M or modal_sum (deprecated)
        if M is not None or modal_sum is not None:
            warnings.warn(
                "Using manual M or modal_sum is deprecated. "
                "Pass 'state' parameter for automatic bit counting.",
                DeprecationWarning,
                stacklevel=2
            )
        # Calculate modal sum if not provided
        if modal_sum is None:
            if weights is not None and modes is not None:
                modal_sum = self.soc_calc.calculate_modal_sum(weights, modes)
            else:
                # Default modal sum
                modal_sum = 1.0
        
        # Calculate Y_emergent if not provided
        if Y_emergent is None:
            if o_observer is None:
                o_observer = UBPConstants.O_OBSERVER
            Y_emergent = calculate_y_emergent(
                UBPConstants.PGCI_TARGET,
                o_observer
            )
        
        # Calculate SOC energy
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            M=M,
            C=C,
            Y_emergent=Y_emergent
        )
        
        return result
    
    def _calculate_legacy(
        self,
        M: int,
        C_speed: Optional[float] = None,
        R: Optional[float] = None,
        S_opt: Optional[float] = None,
        P_GCI: Optional[float] = None,
        O_observer: Optional[float] = None,
        c_infinity: Optional[float] = None,
        I_spin: float = 1.0,
        w_sum: float = 0.1,
        **kwargs
    ) -> float:
        """
        Calculate energy using legacy equation (UBP 3.2).
        
        E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × Σ(w_ij M_ij)
        
        Args:
            M: Active OffBits count
            C_speed: Speed of light (m/s)
            R: Resonance strength
            S_opt: Structural optimality factor
            P_GCI: Global Coherence Invariant
            O_observer: Observer effect factor
            c_infinity: Cosmic constant
            I_spin: Spin information factor
            w_sum: Weighted toggle matrix sum
            
        Returns:
            Energy in Joules (approximate)
        """
        # Use defaults from config
        if C_speed is None:
            C_speed = UBPConstants.SPEED_OF_LIGHT
        if c_infinity is None:
            c_infinity = UBPConstants.C_INFINITY
        if P_GCI is None:
            P_GCI = _global_coherence_system.compute_global_coherence_index()
        if O_observer is None:
            O_observer = 1.0  # Neutral observer
        if R is None:
            R = 1.0  # Default resonance
        if S_opt is None:
            S_opt = 1.0  # Default structural optimality
        
        energy_value = (
            M * C_speed * (R * S_opt) * P_GCI * O_observer *
            c_infinity * I_spin * w_sum
        )
        
        return energy_value


def energy_soc(
    modal_sum: float,
    M: Optional[float] = None,
    C: Optional[float] = None,
    Y_emergent: Optional[float] = None,
    o_observer: Optional[float] = None
) -> SOCEnergyResult:
    """
    Calculate energy using SOC equation.
    
    E = M × C × Y_Emergent × Σ(w_ij M_ij)
    
    Args:
        modal_sum: Resonant Modal Sum
        M: Meta-Temporal Primitive (defaults to π)
        C: Celeritas (defaults to speed of light)
        Y_emergent: Observer-Coherence Ratio (calculated if not provided)
        o_observer: Observer cost (for Y_emergent calculation)
        
    Returns:
        SOCEnergyResult with energy in CU
    """
    calc = DualModeEnergyCalculator()
    return calc._calculate_soc(
        modal_sum=modal_sum,
        M=M,
        C=C,
        Y_emergent=Y_emergent,
        o_observer=o_observer
    )


def energy_legacy(
    M: int,
    C_speed: Optional[float] = None,
    R: Optional[float] = None,
    S_opt: Optional[float] = None,
    P_GCI: Optional[float] = None,
    O_observer: Optional[float] = None,
    c_infinity: Optional[float] = None,
    I_spin: float = 1.0,
    w_sum: float = 0.1
) -> float:
    """
    Calculate energy using legacy equation (UBP 3.2).
    
    E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × Σ(w_ij M_ij)
    
    Args:
        M: Active OffBits count
        C_speed: Speed of light (m/s)
        R: Resonance strength
        S_opt: Structural optimality factor
        P_GCI: Global Coherence Invariant
        O_observer: Observer effect factor
        c_infinity: Cosmic constant
        I_spin: Spin information factor
        w_sum: Weighted toggle matrix sum
        
    Returns:
        Energy in Joules (approximate)
    """
    if not LEGACY_MODE_AVAILABLE:
        raise ValueError("Legacy mode not available. Missing dependencies.")
    
    calc = DualModeEnergyCalculator()
    return calc._calculate_legacy(
        M=M,
        C_speed=C_speed,
        R=R,
        S_opt=S_opt,
        P_GCI=P_GCI,
        O_observer=O_observer,
        c_infinity=c_infinity,
        I_spin=I_spin,
        w_sum=w_sum
    )


def energy_auto(
    mode: str = EnergyMode.SOC,
    **kwargs
) -> Union[float, SOCEnergyResult]:
    """
    Automatic energy calculation with mode selection.
    
    Args:
        mode: Calculation mode ('soc', 'legacy', or 'auto')
        **kwargs: Mode-specific parameters
            For SOC mode (RECOMMENDED):
                state: OffBit or CoherenceState (automatic bit counting)
            For SOC mode (LEGACY):
                modal_sum: Pre-calculated modal sum
                M: Manual bit count (deprecated)
        
    Returns:
        Energy value (type depends on mode)
        
    Examples:
        # SOC mode with state (RECOMMENDED)
        >>> from core.state import OffBit
        >>> state = OffBit(1000)
        >>> result = energy_auto(mode='soc', state=state)
        >>> print(f"M={result.M}, E={result.energy_cu:.6e} CU")
        
        # SOC mode with manual modal_sum (DEPRECATED)
        >>> result = energy_auto(mode='soc', modal_sum=1.0)
        >>> print(f"E = {result.energy_cu:.6e} CU")
        
        # Legacy mode
        >>> E = energy_auto(mode='legacy', M=1000, w_sum=0.1)
        >>> print(f"E = {E:.6e} J")
    """
    calc = DualModeEnergyCalculator()
    return calc.calculate(mode=mode, **kwargs)


def compare_modes(
    M: int = 1000,
    modal_sum: float = 1.0,
    w_sum: float = 0.1,
    **kwargs
) -> Dict[str, Any]:
    """
    Compare SOC and legacy energy calculations.
    
    Args:
        M: Active OffBits count
        modal_sum: Resonant Modal Sum
        w_sum: Weighted toggle matrix sum
        **kwargs: Additional parameters
        
    Returns:
        Dictionary with comparison results
    """
    calc = DualModeEnergyCalculator()
    
    # Calculate SOC energy
    soc_result = calc._calculate_soc(modal_sum=modal_sum, **kwargs)
    
    # Calculate legacy energy (if available)
    if LEGACY_MODE_AVAILABLE:
        legacy_energy = calc._calculate_legacy(M=M, w_sum=w_sum, **kwargs)
    else:
        legacy_energy = None
    
    comparison = {
        'soc': {
            'energy_cu': soc_result.energy_cu,
            'energy_joules': soc_result.energy_joules,
            'Y_emergent': soc_result.Y_emergent,
            'modal_sum': soc_result.modal_sum
        },
        'legacy': {
            'energy_joules': legacy_energy,
            'M': M,
            'w_sum': w_sum
        } if legacy_energy is not None else None,
        'mode_available': {
            'soc': True,
            'legacy': LEGACY_MODE_AVAILABLE
        }
    }
    
    return comparison


def demonstrate_dual_mode():
    """
    Demonstrate dual-mode energy calculations.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("DUAL-MODE ENERGY SYSTEM DEMONSTRATION")
    print("=" * 80)
    
    calc = DualModeEnergyCalculator()
    
    print(f"\nDefault Mode: {calc.default_mode.upper()}")
    print(f"SOC Mode Available: True")
    print(f"Legacy Mode Available: {LEGACY_MODE_AVAILABLE}")
    
    # Test SOC mode
    print("\n" + "-" * 80)
    print("SOC Mode (UBP 3.4):")
    print("-" * 80)
    
    modal_sum = 1.0
    soc_result = calc._calculate_soc(modal_sum=modal_sum)
    
    print(f"\nModal Sum: {modal_sum}")
    print(f"M (Meta-Temporal): {soc_result.M:.15f}")
    print(f"C (Celeritas): {soc_result.C:.0f} m/s")
    print(f"Y_Emergent: {soc_result.Y_emergent:.15f}")
    print(f"\nE = {soc_result.energy_cu:.6e} CU")
    print(f"Output Units: Coherence-Units (computational emergence)")
    print(f"Physical Meaning: Phenomenal intensity / reality weight")
    
    # Test legacy mode (if available)
    if LEGACY_MODE_AVAILABLE:
        print("\n" + "-" * 80)
        print("Legacy Mode (UBP 3.2):")
        print("-" * 80)
        
        M = 1000
        w_sum = 0.1
        legacy_energy = calc._calculate_legacy(M=M, w_sum=w_sum)
        
        print(f"\nActive OffBits (M): {M}")
        print(f"Weighted Sum: {w_sum}")
        print(f"\nE = {legacy_energy:.6e} J (approximate)")
        print(f"Output Units: Joules (physical energy approximation)")
    
    # Compare modes
    print("\n" + "-" * 80)
    print("Mode Comparison:")
    print("-" * 80)
    
    comparison = compare_modes(M=1000, modal_sum=1.0, w_sum=0.1)
    
    print(f"\nSOC Energy: {comparison['soc']['energy_cu']:.6e} CU")
    if comparison['legacy'] is not None:
        print(f"Legacy Energy: {comparison['legacy']['energy_joules']:.6e} J")
        print(f"\nNote: Direct comparison requires CU to Joules calibration")
    
    print("\n" + "=" * 80)
    
    return {
        'calculator': calc,
        'soc_result': soc_result,
        'comparison': comparison
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_dual_mode()
    
    print("\nDual-mode energy system demonstration complete.")
    print("SOC mode (UBP 3.4) is the primary calculation method.")
    print("Legacy mode (UBP 3.2) is maintained for compatibility.")
    print("\nModule ready for import into UBP 3.4 system.")
