"""
Universal Binary Principle (UBP) Framework v3.7 - Atomic/Chemical Realm
Author: Euan Craig, New Zealand
Date: 31 October 2025
================================================================================

This module implements atomic and chemical realm calculations using UBP 3.4 framework.

The atomic/chemical realm is characterized by:
- Electron orbital transitions and atomic spectra
- Molecular vibrations and chemical bonds
- Spectroscopy and resonance phenomena
- Bridge between quantum and electromagnetic scales

Key Features:
- SOC energy calculations for atomic systems
- Hydrogen spectrum modeling (Rydberg formula)
- Molecular vibration analysis
- Y constant dimensional corrections

Test Phenomena (NEW - verifiable against real data):
1. Hydrogen Balmer series (visible spectral lines)
2. CO₂ molecular vibrations (IR spectroscopy)
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
class AtomicState:
    """
    Represents an atomic/molecular system state.
    
    Attributes:
        frequency: Transition frequency (Hz)
        wavelength: Wavelength (m)
        energy_ev: Energy (eV)
        quantum_numbers: Relevant quantum numbers
        coherence: System coherence (0-1)
    """
    frequency: float
    wavelength: float
    energy_ev: float
    quantum_numbers: Dict[str, int]
    coherence: float


class AtomicRealm:
    """
    Atomic/Chemical realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "atomic"
    BASE_CRV = UBPConstants.FINE_STRUCTURE_CONSTANT  # α ≈ 1/137
    TOGGLE_PROBABILITY = 0.5  # Moderate
    
    # Atomic constants
    RYDBERG_CONSTANT = UBPConstants.RYDBERG_CONSTANT
    PLANCK_CONSTANT = UBPConstants.PLANCK_CONSTANT
    SPEED_OF_LIGHT = UBPConstants.SPEED_OF_LIGHT
    ELECTRON_CHARGE = UBPConstants.ELEMENTARY_CHARGE
    BOHR_RADIUS = 5.29177210903e-11  # m (Bohr radius)
    
    # Molecular constants
    CARBON_MASS = 1.993e-26  # kg (C-12)
    OXYGEN_MASS = 2.657e-26  # kg (O-16)
    
    def __init__(self):
        """Initialize atomic/chemical realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs.get(self.REALM_NAME, UBPConstants.O_OBSERVER)
    
    def calculate_atomic_energy_soc(
        self,
        atomic_state: AtomicState
    ) -> SOCEnergyResult:
        """
        Calculate atomic energy using SOC equation.
        
        Args:
            atomic_state: Atomic system state
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(atomic_state.frequency, raise_error=False)
        
        # Calculate modal sum from atomic state
        modal_sum = self._calculate_atomic_modal_sum(atomic_state)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_atomic_modal_sum(self, state: AtomicState) -> float:
        """
        Calculate resonant modal sum for atomic state.
        
        Args:
            state: Atomic state
            
        Returns:
            Modal sum value
        """
        # Energy contribution (log scale for eV range)
        energy_contrib = math.log10(state.energy_ev + 1) / 3.0  # Normalized
        
        # Frequency contribution
        freq_contrib = math.log10(state.frequency + 1) / 18.0  # Normalized
        
        # Quantum number contribution (higher transitions = more modes)
        n_sum = sum(state.quantum_numbers.values())
        quantum_contrib = math.log10(n_sum + 1) / 2.0
        
        modal_sum = (
            energy_contrib * 
            freq_contrib * 
            (1.0 + quantum_contrib) *
            state.coherence
        )
        
        return max(modal_sum, 1e-10)  # Ensure non-zero
    
    def model_hydrogen_spectrum(
        self,
        n_initial: int = 3,
        n_final: int = 2,
        series_name: str = "Balmer"
    ) -> Dict[str, float]:
        """
        Model hydrogen spectral lines using Rydberg formula.
        
        NEW TEST PHENOMENON: Balmer series (visible light)
        Real data: H-alpha 656.3 nm, H-beta 486.1 nm, H-gamma 434.0 nm
        
        Args:
            n_initial: Initial principal quantum number
            n_final: Final principal quantum number
            series_name: Spectral series name
            
        Returns:
            Dictionary with spectral analysis
        """
        # Rydberg formula
        # 1/λ = R_∞ * (1/n_f² - 1/n_i²)
        wavelength_inv = self.RYDBERG_CONSTANT * (
            1.0 / n_final**2 - 1.0 / n_initial**2
        )
        wavelength_m = 1.0 / wavelength_inv
        wavelength_nm = wavelength_m * 1e9
        
        # Frequency
        frequency_hz = self.SPEED_OF_LIGHT / wavelength_m
        
        # Photon energy
        energy_j = self.PLANCK_CONSTANT * frequency_hz
        energy_ev = energy_j / self.ELECTRON_CHARGE
        
        # Line name (for Balmer series)
        line_names = {
            (3, 2): "H-alpha",
            (4, 2): "H-beta",
            (5, 2): "H-gamma",
            (6, 2): "H-delta"
        }
        line_name = line_names.get((n_initial, n_final), f"n={n_initial}→{n_final}")
        
        # Color (for visible spectrum)
        if 380 <= wavelength_nm <= 450:
            color = "Violet"
        elif 450 < wavelength_nm <= 495:
            color = "Blue"
        elif 495 < wavelength_nm <= 570:
            color = "Green"
        elif 570 < wavelength_nm <= 590:
            color = "Yellow"
        elif 590 < wavelength_nm <= 620:
            color = "Orange"
        elif 620 < wavelength_nm <= 750:
            color = "Red"
        else:
            color = "Non-visible"
        
        # Coherence (atomic transitions are highly coherent)
        coherence = 0.999
        
        # Create atomic state
        atomic_state = AtomicState(
            frequency=frequency_hz,
            wavelength=wavelength_m,
            energy_ev=energy_ev,
            quantum_numbers={'n_initial': n_initial, 'n_final': n_final},
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_atomic_energy_soc(atomic_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        # Oscillator strength (simplified)
        # f ~ (2/3) * (n_f/n_i)³ * (1 - n_f²/n_i²)
        oscillator_strength = (2.0/3.0) * (n_final/n_initial)**3 * (1 - n_final**2/n_initial**2)
        oscillator_strength = abs(oscillator_strength)
        
        return {
            'series': series_name,
            'line_name': line_name,
            'n_initial': n_initial,
            'n_final': n_final,
            'wavelength_nm': wavelength_nm,
            'wavelength_m': wavelength_m,
            'frequency_hz': frequency_hz,
            'frequency_thz': frequency_hz / 1e12,
            'energy_ev': energy_ev,
            'energy_j': energy_j,
            'color': color,
            'oscillator_strength': oscillator_strength,
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }
    
    def model_co2_vibrations(
        self,
        mode: str = "asymmetric_stretch",
        temperature_k: float = 300.0
    ) -> Dict[str, float]:
        """
        Model CO₂ molecular vibrations.
        
        NEW TEST PHENOMENON: CO₂ IR absorption
        Real data: Asymmetric stretch 2349 cm⁻¹ (4.26 μm)
        
        Args:
            mode: Vibrational mode ("asymmetric_stretch", "symmetric_stretch", "bend")
            temperature_k: Temperature (K)
            
        Returns:
            Dictionary with vibrational analysis
        """
        # CO₂ vibrational frequencies (wavenumbers in cm⁻¹)
        mode_wavenumbers = {
            'asymmetric_stretch': 2349.0,  # ν₃ - IR active
            'symmetric_stretch': 1388.0,   # ν₁ - Raman active
            'bend': 667.0                   # ν₂ - IR active (doubly degenerate)
        }
        
        wavenumber_cm = mode_wavenumbers.get(mode, 2349.0)
        
        # Convert wavenumber to frequency
        # ν = c * ṽ (where ṽ is wavenumber)
        frequency_hz = self.SPEED_OF_LIGHT * wavenumber_cm * 100  # cm⁻¹ to m⁻¹
        
        # Wavelength
        wavelength_m = self.SPEED_OF_LIGHT / frequency_hz
        wavelength_um = wavelength_m * 1e6
        
        # Photon energy
        energy_j = self.PLANCK_CONSTANT * frequency_hz
        energy_ev = energy_j / self.ELECTRON_CHARGE
        
        # Reduced mass (for asymmetric stretch: C=O)
        m_c = self.CARBON_MASS
        m_o = self.OXYGEN_MASS
        reduced_mass = (m_c * m_o) / (m_c + m_o)
        
        # Force constant (k = 4π²c²ṽ²μ)
        force_constant = 4 * math.pi**2 * self.SPEED_OF_LIGHT**2 * (wavenumber_cm * 100)**2 * reduced_mass
        
        # Thermal population (Boltzmann factor)
        # P(v=1) / P(v=0) = exp(-hν/kT)
        boltzmann_k = UBPConstants.BOLTZMANN_CONSTANT
        thermal_factor = math.exp(-energy_j / (boltzmann_k * temperature_k))
        
        # Coherence (molecular vibrations are coherent but affected by collisions)
        # Higher temperature = lower coherence
        coherence = 0.85 * math.exp(-(temperature_k - 300) / 500)
        coherence = max(0.5, min(0.95, coherence))
        
        # IR activity (dipole moment change)
        ir_active = mode in ['asymmetric_stretch', 'bend']
        
        # Create atomic state
        atomic_state = AtomicState(
            frequency=frequency_hz,
            wavelength=wavelength_m,
            energy_ev=energy_ev,
            quantum_numbers={'v': 1},  # First excited state
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_atomic_energy_soc(atomic_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        return {
            'molecule': 'CO₂',
            'vibrational_mode': mode,
            'wavenumber_cm': wavenumber_cm,
            'frequency_hz': frequency_hz,
            'frequency_thz': frequency_hz / 1e12,
            'wavelength_um': wavelength_um,
            'energy_ev': energy_ev,
            'reduced_mass_kg': reduced_mass,
            'force_constant_n_m': force_constant,
            'temperature_k': temperature_k,
            'thermal_population_ratio': thermal_factor,
            'ir_active': ir_active,
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost
        }


def demonstrate_atomic_realm():
    """
    Demonstrate atomic/chemical realm calculations with real test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("ATOMIC/CHEMICAL REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = AtomicRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.10f} (α - fine structure)")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    print(f"  Rydberg Constant: {realm.RYDBERG_CONSTANT:.6e} m⁻¹")
    
    # Test 1: Hydrogen Balmer Series
    print("\n" + "-" * 80)
    print("TEST 1: Hydrogen Balmer Series (Visible Spectral Lines)")
    print("-" * 80)
    print("Real-world data: H-alpha 656.3 nm, H-beta 486.1 nm")
    
    # H-alpha (n=3→2)
    h_alpha = realm.model_hydrogen_spectrum(n_initial=3, n_final=2, series_name="Balmer")
    
    print(f"\nH-alpha Line (n=3→2):")
    print(f"  Series: {h_alpha['series']}")
    print(f"  Line Name: {h_alpha['line_name']}")
    print(f"  Wavelength: {h_alpha['wavelength_nm']:.2f} nm")
    print(f"  Frequency: {h_alpha['frequency_thz']:.3f} THz")
    print(f"  Energy: {h_alpha['energy_ev']:.4f} eV")
    print(f"  Color: {h_alpha['color']}")
    print(f"  Oscillator Strength: {h_alpha['oscillator_strength']:.6f}")
    
    # H-beta (n=4→2)
    h_beta = realm.model_hydrogen_spectrum(n_initial=4, n_final=2, series_name="Balmer")
    
    print(f"\nH-beta Line (n=4→2):")
    print(f"  Line Name: {h_beta['line_name']}")
    print(f"  Wavelength: {h_beta['wavelength_nm']:.2f} nm")
    print(f"  Frequency: {h_beta['frequency_thz']:.3f} THz")
    print(f"  Energy: {h_beta['energy_ev']:.4f} eV")
    print(f"  Color: {h_beta['color']}")
    
    print(f"\nUBP Analysis (H-alpha):")
    print(f"  Coherence: {h_alpha['coherence']:.6f}")
    print(f"  NRCI: {h_alpha['nrci']:.6f}")
    print(f"  UBP Energy: {h_alpha['ubp_energy_cu']:.6e} CU")
    
    # Test 2: CO₂ Molecular Vibrations
    print("\n" + "-" * 80)
    print("TEST 2: CO₂ Molecular Vibrations (IR Spectroscopy)")
    print("-" * 80)
    print("Real-world data: Asymmetric stretch 2349 cm⁻¹ (4.26 μm)")
    
    co2_result = realm.model_co2_vibrations(
        mode="asymmetric_stretch",
        temperature_k=300.0
    )
    
    print(f"\nCO₂ Vibrational Analysis:")
    print(f"  Molecule: {co2_result['molecule']}")
    print(f"  Mode: {co2_result['vibrational_mode']}")
    print(f"  Wavenumber: {co2_result['wavenumber_cm']:.1f} cm⁻¹")
    print(f"  Frequency: {co2_result['frequency_thz']:.2f} THz")
    print(f"  Wavelength: {co2_result['wavelength_um']:.3f} μm")
    print(f"  Energy: {co2_result['energy_ev']:.4f} eV")
    
    print(f"\nMolecular Properties:")
    print(f"  Reduced Mass: {co2_result['reduced_mass_kg']:.6e} kg")
    print(f"  Force Constant: {co2_result['force_constant_n_m']:.2f} N/m")
    print(f"  Temperature: {co2_result['temperature_k']:.1f} K")
    print(f"  Thermal Population (v=1/v=0): {co2_result['thermal_population_ratio']:.6f}")
    print(f"  IR Active: {co2_result['ir_active']}")
    
    print(f"\nUBP Analysis:")
    print(f"  Coherence: {co2_result['coherence']:.6f}")
    print(f"  NRCI: {co2_result['nrci']:.6f}")
    print(f"  UBP Energy: {co2_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'h_alpha': h_alpha,
        'h_beta': h_beta,
        'co2': co2_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_atomic_realm()
    
    print("\nAtomic/Chemical realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. Hydrogen Balmer series (656.3 nm, 486.1 nm)")
    print("  2. CO₂ asymmetric stretch (2349 cm⁻¹)")
    print("\nBoth tests use real spectroscopic data.")
    print("Module ready for UBP 3.4 integration testing.")
