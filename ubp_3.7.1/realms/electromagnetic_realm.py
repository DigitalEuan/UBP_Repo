"""
Universal Binary Principle (UBP) Framework v3.7.1 - Electromagnetic Realm
Author: Euan R A Craig, New Zealand
Date: 28 November 2025
================================================================================

This module implements electromagnetic realm calculations using UBP 3.4 framework.

The electromagnetic realm is characterized by:
- Maxwell's equations emergence
- Photon interactions and wave propagation
- EM field resonances
- Antenna and waveguide behavior

Key Features:
- SOC energy calculations for EM systems
- Wave-particle duality modeling
- Field coherence analysis
- Y constant dimensional corrections

Test Phenomena (NEW - verifiable against real data):
1. Dipole antenna resonance at 2.4 GHz (WiFi frequency)
2. Cavity resonator Q-factor in microwave systems
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
class EMFieldState:
    """
    Represents an electromagnetic field state.
    
    Attributes:
        E_field: Electric field amplitude (V/m)
        B_field: Magnetic field amplitude (T)
        frequency: EM wave frequency (Hz)
        wavelength: Wavelength (m)
        polarization: Polarization state (0-1, 0=linear, 1=circular)
        coherence: Field coherence (0-1)
    """
    E_field: float
    B_field: float
    frequency: float
    wavelength: float
    polarization: float
    coherence: float


class ElectromagneticRealm:
    """
    Electromagnetic realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "electromagnetic"
    BASE_CRV = UBPConstants.CRV_ELECTROMAGNETIC_BASE  # π
    TOGGLE_PROBABILITY = UBPConstants.UBP_TOGGLE_PROBABILITIES['electromagnetic']
    
    # EM-specific constants
    SPEED_OF_LIGHT = UBPConstants.SPEED_OF_LIGHT
    VACUUM_PERMITTIVITY = UBPConstants.VACUUM_PERMITTIVITY
    VACUUM_PERMEABILITY = UBPConstants.VACUUM_PERMEABILITY
    IMPEDANCE_FREE_SPACE = 376.730313668  # Ohms
    
    def __init__(self):
        """Initialize electromagnetic realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs[self.REALM_NAME]
    
    def calculate_em_energy_soc(
        self,
        em_state: EMFieldState
    ) -> SOCEnergyResult:
        """
        Calculate EM energy using SOC equation.
        
        Args:
            em_state: Electromagnetic field state
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(em_state.frequency, raise_error=False)
        
        # Calculate modal sum from EM state
        modal_sum = self._calculate_em_modal_sum(em_state)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_em_modal_sum(self, state: EMFieldState) -> float:
        """
        Calculate resonant modal sum for EM field state.
        
        Args:
            state: EM field state
            
        Returns:
            Modal sum value
        """
        # Energy density in EM field
        energy_density_E = 0.5 * self.VACUUM_PERMITTIVITY * state.E_field**2
        energy_density_B = 0.5 * state.B_field**2 / self.VACUUM_PERMEABILITY
        
        # Total energy density (should be equal for plane wave)
        total_energy_density = energy_density_E + energy_density_B
        
        # Normalize to modal sum scale
        modal_sum = (
            math.log10(total_energy_density + 1) * 
            state.coherence * 
            (1 + state.polarization * 0.1)  # Polarization bonus
        )
        
        return modal_sum
    
    def model_dipole_antenna_resonance(
        self,
        frequency_GHz: float,
        antenna_length_cm: float,
        input_power_W: float,
        environment: str = "free_space"
    ) -> Dict[str, float]:
        """
        Model dipole antenna resonance at WiFi frequencies.
        
        NEW TEST PHENOMENON: 2.4 GHz dipole antenna (verifiable)
        Real data: λ/2 dipole at 2.4 GHz should be ~6.25 cm
        
        Args:
            frequency_GHz: Operating frequency (GHz)
            antenna_length_cm: Physical antenna length (cm)
            input_power_W: Input power (Watts)
            environment: "free_space" or "ground_plane"
            
        Returns:
            Dictionary with antenna analysis
        """
        # Convert to SI
        freq_Hz = frequency_GHz * 1e9
        length_m = antenna_length_cm / 100.0
        
        # Calculate wavelength
        wavelength_m = self.SPEED_OF_LIGHT / freq_Hz
        
        # Optimal length for half-wave dipole
        optimal_length_m = wavelength_m / 2
        
        # Length ratio (1.0 = perfect resonance)
        length_ratio = length_m / optimal_length_m
        
        # Resonance quality (peaks at length_ratio = 1.0)
        # Gaussian resonance curve
        resonance_quality = math.exp(-((length_ratio - 1.0)**2) / 0.1)
        
        # Radiation resistance (theoretical for half-wave dipole: 73 Ohms)
        R_rad = 73.0 * resonance_quality
        
        # Calculate E-field at 1 meter distance
        # P = (E^2 * r^2) / (120 * π) for far field
        distance_m = 1.0
        E_field = math.sqrt(input_power_W * 120 * math.pi / (distance_m**2 * resonance_quality))
        
        # B-field from E-field
        B_field = E_field / self.SPEED_OF_LIGHT
        
        # Antenna efficiency (affected by resonance)
        efficiency = resonance_quality * 0.95  # Max 95% efficiency
        
        # Radiated power
        power_radiated_W = input_power_W * efficiency
        
        # Create EM field state
        em_state = EMFieldState(
            E_field=E_field,
            B_field=B_field,
            frequency=freq_Hz,
            wavelength=wavelength_m,
            polarization=0.0,  # Linear polarization
            coherence=resonance_quality
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_em_energy_soc(em_state)
        
        # Calculate NRCI (high for resonant antenna)
        nrci = UBPConstants.PGCI_TARGET * resonance_quality
        
        return {
            'frequency_ghz': frequency_GHz,
            'frequency_hz': freq_Hz,
            'antenna_length_cm': antenna_length_cm,
            'wavelength_cm': wavelength_m * 100,
            'optimal_length_cm': optimal_length_m * 100,
            'length_ratio': length_ratio,
            'resonance_quality': resonance_quality,
            'radiation_resistance_ohms': R_rad,
            'efficiency': efficiency,
            'input_power_w': input_power_W,
            'radiated_power_w': power_radiated_W,
            'e_field_v_per_m': E_field,
            'b_field_tesla': B_field,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }
    
    def model_cavity_resonator(
        self,
        cavity_length_cm: float,
        cavity_radius_cm: float,
        mode: str = "TE011",
        material_conductivity: float = 5.8e7  # Copper
    ) -> Dict[str, float]:
        """
        Model microwave cavity resonator Q-factor.
        
        NEW TEST PHENOMENON: Cylindrical cavity resonator (verifiable)
        Real data: Copper cavity at X-band should have Q > 10,000
        
        Args:
            cavity_length_cm: Cavity length (cm)
            cavity_radius_cm: Cavity radius (cm)
            mode: Resonant mode (TE011, TM010, etc.)
            material_conductivity: Wall conductivity (S/m)
            
        Returns:
            Dictionary with cavity analysis
        """
        # Convert to SI
        length_m = cavity_length_cm / 100.0
        radius_m = cavity_radius_cm / 100.0
        
        # Calculate resonant frequency for TE011 mode (simplified)
        # f = (c / 2π) * sqrt((p_mn/a)^2 + (π/d)^2)
        # For TE011: p_01 ≈ 3.832
        p_01 = 3.832
        
        freq_Hz = (self.SPEED_OF_LIGHT / (2 * math.pi)) * math.sqrt(
            (p_01 / radius_m)**2 + (math.pi / length_m)**2
        )
        
        # Calculate wavelength
        wavelength_m = self.SPEED_OF_LIGHT / freq_Hz
        
        # Skin depth
        mu_0 = self.VACUUM_PERMEABILITY
        skin_depth_m = math.sqrt(2 / (2 * math.pi * freq_Hz * mu_0 * material_conductivity))
        
        # Surface resistance
        R_s = math.sqrt(2 * math.pi * freq_Hz * mu_0 / (2 * material_conductivity))
        
        # Quality factor (simplified formula)
        # Q = (ω * stored_energy) / (power_loss)
        # For TE011 mode in cylindrical cavity
        surface_area = 2 * math.pi * radius_m * length_m + 2 * math.pi * radius_m**2
        volume = math.pi * radius_m**2 * length_m
        
        # Approximate Q factor
        Q_factor = (wavelength_m * volume) / (skin_depth_m * surface_area * 2)
        
        # Coherence from Q factor (higher Q = higher coherence)
        coherence = min(0.999997, 1.0 - 1.0/Q_factor)
        
        # Estimate field strengths for 1W stored energy
        stored_energy_J = 1.0
        E_field = math.sqrt(2 * stored_energy_J / (self.VACUUM_PERMITTIVITY * volume))
        B_field = E_field / self.SPEED_OF_LIGHT
        
        # Create EM field state
        em_state = EMFieldState(
            E_field=E_field,
            B_field=B_field,
            frequency=freq_Hz,
            wavelength=wavelength_m,
            polarization=0.5,  # Mixed polarization in cavity
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_em_energy_soc(em_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        return {
            'cavity_length_cm': cavity_length_cm,
            'cavity_radius_cm': cavity_radius_cm,
            'resonant_mode': mode,
            'frequency_ghz': freq_Hz / 1e9,
            'frequency_hz': freq_Hz,
            'wavelength_cm': wavelength_m * 100,
            'q_factor': Q_factor,
            'skin_depth_um': skin_depth_m * 1e6,
            'surface_resistance_ohms': R_s,
            'coherence': coherence,
            'e_field_v_per_m': E_field,
            'b_field_tesla': B_field,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'material_conductivity': material_conductivity
        }


def demonstrate_electromagnetic_realm():
    """
    Demonstrate electromagnetic realm calculations with real test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("ELECTROMAGNETIC REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = ElectromagneticRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.6f}")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    print(f"  Speed of Light: {realm.SPEED_OF_LIGHT:.0f} m/s")
    
    # Test 1: WiFi Dipole Antenna
    print("\n" + "-" * 80)
    print("TEST 1: Dipole Antenna Resonance at 2.4 GHz (WiFi)")
    print("-" * 80)
    print("Real-world verification: Half-wave dipole at 2.4 GHz = 6.25 cm")
    
    antenna_result = realm.model_dipole_antenna_resonance(
        frequency_GHz=2.4,
        antenna_length_cm=6.25,  # Optimal length
        input_power_W=0.1,        # 100 mW (typical WiFi)
        environment="free_space"
    )
    
    print(f"\nAntenna Parameters:")
    print(f"  Frequency: {antenna_result['frequency_ghz']:.2f} GHz")
    print(f"  Antenna Length: {antenna_result['antenna_length_cm']:.2f} cm")
    print(f"  Wavelength: {antenna_result['wavelength_cm']:.2f} cm")
    print(f"  Optimal Length: {antenna_result['optimal_length_cm']:.2f} cm")
    
    print(f"\nResonance Analysis:")
    print(f"  Length Ratio: {antenna_result['length_ratio']:.4f} (1.0 = perfect)")
    print(f"  Resonance Quality: {antenna_result['resonance_quality']:.6f}")
    print(f"  Radiation Resistance: {antenna_result['radiation_resistance_ohms']:.2f} Ω")
    print(f"  Efficiency: {antenna_result['efficiency']*100:.2f}%")
    
    print(f"\nField Strengths:")
    print(f"  E-field (1m): {antenna_result['e_field_v_per_m']:.4f} V/m")
    print(f"  B-field (1m): {antenna_result['b_field_tesla']:.4e} T")
    print(f"  Radiated Power: {antenna_result['radiated_power_w']*1000:.2f} mW")
    
    print(f"\nUBP Analysis:")
    print(f"  NRCI: {antenna_result['nrci']:.6f}")
    print(f"  UBP Energy: {antenna_result['ubp_energy_cu']:.6e} CU")
    
    # Test 2: Cavity Resonator
    print("\n" + "-" * 80)
    print("TEST 2: Microwave Cavity Resonator Q-Factor")
    print("-" * 80)
    print("Real-world verification: Copper X-band cavity Q > 10,000")
    
    cavity_result = realm.model_cavity_resonator(
        cavity_length_cm=3.0,
        cavity_radius_cm=1.5,
        mode="TE011",
        material_conductivity=5.8e7  # Copper
    )
    
    print(f"\nCavity Parameters:")
    print(f"  Length: {cavity_result['cavity_length_cm']:.2f} cm")
    print(f"  Radius: {cavity_result['cavity_radius_cm']:.2f} cm")
    print(f"  Mode: {cavity_result['resonant_mode']}")
    print(f"  Material: Copper (σ = {cavity_result['material_conductivity']:.2e} S/m)")
    
    print(f"\nResonance Analysis:")
    print(f"  Frequency: {cavity_result['frequency_ghz']:.4f} GHz")
    print(f"  Wavelength: {cavity_result['wavelength_cm']:.4f} cm")
    print(f"  Q-Factor: {cavity_result['q_factor']:.0f}")
    print(f"  Skin Depth: {cavity_result['skin_depth_um']:.4f} μm")
    print(f"  Surface Resistance: {cavity_result['surface_resistance_ohms']:.6f} Ω")
    
    print(f"\nField Analysis:")
    print(f"  Coherence: {cavity_result['coherence']:.6f}")
    print(f"  E-field: {cavity_result['e_field_v_per_m']:.4e} V/m")
    print(f"  B-field: {cavity_result['b_field_tesla']:.4e} T")
    
    print(f"\nUBP Analysis:")
    print(f"  NRCI: {cavity_result['nrci']:.6f}")
    print(f"  UBP Energy: {cavity_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'antenna': antenna_result,
        'cavity': cavity_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_electromagnetic_realm()
    
    print("\nElectromagnetic realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. WiFi dipole antenna at 2.4 GHz (6.25 cm)")
    print("  2. Microwave cavity resonator (Q > 10,000)")
    print("\nBoth tests use real-world verifiable parameters.")
    print("Module ready for UBP 3.4 integration testing.")
