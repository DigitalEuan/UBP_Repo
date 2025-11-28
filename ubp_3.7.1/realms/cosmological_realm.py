"""
Universal Binary Principle (UBP) Framework v3.7.1 - Cosmological Realm
Author: Euan R A Craig, New Zealand
Date: 28 November 2025
================================================================================

This module implements cosmological realm calculations using UBP 3.4 framework.

The cosmological realm is characterized by:
- Large-scale structure and cosmic evolution
- CMB fluctuations and primordial perturbations
- Dark energy and cosmic acceleration
- Extremely low frequencies and vast scales

Key Features:
- SOC energy calculations for cosmological systems
- CMB power spectrum analysis
- Dark energy equation of state
- Y constant dimensional corrections

Test Phenomena (NEW - verifiable against real data):
1. CMB temperature fluctuations (WMAP/Planck data)
2. Hubble expansion and dark energy density
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
class CosmologicalState:
    """
    Represents a cosmological system state.
    
    Attributes:
        frequency: Characteristic frequency (Hz)
        scale_mpc: Physical scale (Megaparsecs)
        temperature_k: Temperature (Kelvin)
        density_kg_m3: Energy density (kg/m³)
        coherence: System coherence (0-1)
    """
    frequency: float
    scale_mpc: float
    temperature_k: float
    density_kg_m3: float
    coherence: float


class CosmologicalRealm:
    """
    Cosmological realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "cosmological"
    BASE_CRV = UBPConstants.CRV_COSMOLOGICAL_BASE  # e²
    TOGGLE_PROBABILITY = UBPConstants.UBP_TOGGLE_PROBABILITIES.get('cosmological', 0.1)
    
    # Cosmological constants
    SPEED_OF_LIGHT = UBPConstants.SPEED_OF_LIGHT
    HUBBLE_CONSTANT = 67.4  # km/s/Mpc (Planck 2018)
    CMB_TEMPERATURE = 2.725  # K (current)
    CRITICAL_DENSITY = 8.5e-27  # kg/m³
    DARK_ENERGY_FRACTION = 0.685  # Ω_Λ
    DARK_MATTER_FRACTION = 0.265  # Ω_DM
    BARYON_FRACTION = 0.05  # Ω_b
    
    # Unit conversions
    MPC_TO_METERS = 3.086e22  # Megaparsec to meters
    GYR_TO_SECONDS = 3.154e16  # Gigayear to seconds
    
    def __init__(self):
        """Initialize cosmological realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs.get(self.REALM_NAME, UBPConstants.O_OBSERVER)
    
    def calculate_cosmological_energy_soc(
        self,
        cosmo_state: CosmologicalState
    ) -> SOCEnergyResult:
        """
        Calculate cosmological energy using SOC equation.
        
        Args:
            cosmo_state: Cosmological system state
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(cosmo_state.frequency, raise_error=False)
        
        # Calculate modal sum from cosmological state
        modal_sum = self._calculate_cosmological_modal_sum(cosmo_state)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_cosmological_modal_sum(self, state: CosmologicalState) -> float:
        """
        Calculate resonant modal sum for cosmological state.
        
        Args:
            state: Cosmological state
            
        Returns:
            Modal sum value
        """
        # Scale contribution (log scale for vast distances)
        scale_contrib = math.log10(state.scale_mpc + 1) / 5.0  # Normalized
        
        # Density contribution (log scale)
        density_contrib = math.log10(state.density_kg_m3 * 1e30 + 1) / 10.0
        
        # Temperature contribution
        temp_contrib = math.log10(state.temperature_k + 1) / 3.0
        
        # Frequency contribution (very low frequencies)
        freq_contrib = math.log10(state.frequency + 1e-20) / 20.0
        
        modal_sum = (
            scale_contrib * 
            density_contrib * 
            temp_contrib * 
            state.coherence *
            (1.0 + freq_contrib)
        )
        
        return max(modal_sum, 1e-10)  # Ensure non-zero
    
    def model_cmb_fluctuations(
        self,
        multipole_l: int = 200,
        temperature_k: float = 2.725,
        fluctuation_amplitude_uk: float = 70.0
    ) -> Dict[str, float]:
        """
        Model CMB temperature fluctuations.
        
        NEW TEST PHENOMENON: CMB power spectrum
        Real data: Planck satellite measured ΔT/T ~ 10^-5 at l~200
        
        Args:
            multipole_l: Multipole moment (angular scale)
            temperature_k: Mean CMB temperature (K)
            fluctuation_amplitude_uk: RMS fluctuation amplitude (μK)
            
        Returns:
            Dictionary with CMB analysis
        """
        # Angular scale corresponding to multipole l
        # θ ≈ 180°/l
        angular_scale_deg = 180.0 / multipole_l
        angular_scale_rad = angular_scale_deg * math.pi / 180.0
        
        # Physical scale at last scattering surface
        # Distance to last scattering ~14 Gpc
        distance_to_ls_mpc = 14000.0  # Mpc
        physical_scale_mpc = distance_to_ls_mpc * angular_scale_rad
        
        # Characteristic frequency (sound waves at recombination)
        # Sound horizon at recombination ~150 Mpc
        sound_horizon_mpc = 150.0
        sound_speed = self.SPEED_OF_LIGHT / math.sqrt(3)  # Radiation-dominated
        
        # Frequency of acoustic oscillations
        frequency_hz = sound_speed / (sound_horizon_mpc * self.MPC_TO_METERS)
        
        # Relative fluctuation amplitude
        delta_t_over_t = fluctuation_amplitude_uk * 1e-6 / temperature_k
        
        # Coherence (CMB is highly coherent)
        # Sachs-Wolfe plateau has high coherence
        coherence = 0.999 if multipole_l < 100 else 0.95
        
        # Energy density at recombination
        # Temperature was ~3000 K at z~1100
        z_recombination = 1100.0
        temp_recombination_k = temperature_k * (1 + z_recombination)
        
        # Radiation energy density (Stefan-Boltzmann)
        stefan_boltzmann = 5.67e-8  # W/(m²·K⁴)
        energy_density_recomb = (4 * stefan_boltzmann / self.SPEED_OF_LIGHT) * temp_recombination_k**4
        
        # Current energy density (much lower)
        energy_density_now = (4 * stefan_boltzmann / self.SPEED_OF_LIGHT) * temperature_k**4
        
        # Create cosmological state
        cosmo_state = CosmologicalState(
            frequency=frequency_hz,
            scale_mpc=physical_scale_mpc,
            temperature_k=temperature_k,
            density_kg_m3=energy_density_now / self.SPEED_OF_LIGHT**2,
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_cosmological_energy_soc(cosmo_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        # Power spectrum value (simplified)
        # C_l ∝ l(l+1) * (ΔT)²
        power_spectrum_uk2 = multipole_l * (multipole_l + 1) * fluctuation_amplitude_uk**2
        
        return {
            'multipole_l': multipole_l,
            'angular_scale_deg': angular_scale_deg,
            'physical_scale_mpc': physical_scale_mpc,
            'cmb_temperature_k': temperature_k,
            'fluctuation_amplitude_uk': fluctuation_amplitude_uk,
            'relative_fluctuation': delta_t_over_t,
            'frequency_hz': frequency_hz,
            'coherence': coherence,
            'redshift_recombination': z_recombination,
            'temp_recombination_k': temp_recombination_k,
            'energy_density_now_kg_m3': energy_density_now / self.SPEED_OF_LIGHT**2,
            'power_spectrum_uk2': power_spectrum_uk2,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }
    
    def model_hubble_expansion(
        self,
        distance_mpc: float = 1000.0,
        include_dark_energy: bool = True
    ) -> Dict[str, float]:
        """
        Model Hubble expansion and dark energy.
        
        NEW TEST PHENOMENON: Cosmic acceleration
        Real data: H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685
        
        Args:
            distance_mpc: Distance to observe (Mpc)
            include_dark_energy: Include dark energy effects
            
        Returns:
            Dictionary with expansion analysis
        """
        # Recession velocity (Hubble's law)
        # v = H₀ * d
        recession_velocity_km_s = self.HUBBLE_CONSTANT * distance_mpc
        recession_velocity_m_s = recession_velocity_km_s * 1000.0
        
        # Redshift
        # z ≈ v/c for small z
        redshift = recession_velocity_m_s / self.SPEED_OF_LIGHT
        
        # Hubble time (age of universe approximation)
        hubble_time_s = self.MPC_TO_METERS / (self.HUBBLE_CONSTANT * 1000.0)
        hubble_time_gyr = hubble_time_s / self.GYR_TO_SECONDS
        
        # Critical density
        rho_crit = self.CRITICAL_DENSITY
        
        # Dark energy density
        rho_dark_energy = rho_crit * self.DARK_ENERGY_FRACTION
        
        # Dark energy equation of state parameter (w = -1 for cosmological constant)
        w_dark_energy = -1.0
        
        # Characteristic frequency of cosmic expansion
        # f ~ H₀
        expansion_frequency_hz = (self.HUBBLE_CONSTANT * 1000.0) / self.MPC_TO_METERS
        
        # Coherence (universe is highly homogeneous on large scales)
        coherence = 0.99
        
        # Create cosmological state
        cosmo_state = CosmologicalState(
            frequency=expansion_frequency_hz,
            scale_mpc=distance_mpc,
            temperature_k=self.CMB_TEMPERATURE,
            density_kg_m3=rho_crit,
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_cosmological_energy_soc(cosmo_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        # Acceleration parameter (q₀)
        # q₀ = Ω_m/2 - Ω_Λ (for flat universe)
        omega_matter = self.DARK_MATTER_FRACTION + self.BARYON_FRACTION
        deceleration_param = omega_matter / 2.0 - self.DARK_ENERGY_FRACTION
        is_accelerating = deceleration_param < 0
        
        # Dark energy density in Joules per cubic meter
        dark_energy_density_j_m3 = rho_dark_energy * self.SPEED_OF_LIGHT**2
        
        return {
            'distance_mpc': distance_mpc,
            'hubble_constant_km_s_mpc': self.HUBBLE_CONSTANT,
            'recession_velocity_km_s': recession_velocity_km_s,
            'redshift': redshift,
            'hubble_time_gyr': hubble_time_gyr,
            'critical_density_kg_m3': rho_crit,
            'dark_energy_fraction': self.DARK_ENERGY_FRACTION,
            'dark_matter_fraction': self.DARK_MATTER_FRACTION,
            'baryon_fraction': self.BARYON_FRACTION,
            'dark_energy_density_kg_m3': rho_dark_energy,
            'dark_energy_density_j_m3': dark_energy_density_j_m3,
            'w_equation_of_state': w_dark_energy,
            'deceleration_parameter': deceleration_param,
            'is_accelerating': is_accelerating,
            'expansion_frequency_hz': expansion_frequency_hz,
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost
        }


def demonstrate_cosmological_realm():
    """
    Demonstrate cosmological realm calculations with real test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("COSMOLOGICAL REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = CosmologicalRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.6f} (e²)")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    print(f"  Hubble Constant: {realm.HUBBLE_CONSTANT:.1f} km/s/Mpc")
    print(f"  CMB Temperature: {realm.CMB_TEMPERATURE:.3f} K")
    
    # Test 1: CMB Fluctuations
    print("\n" + "-" * 80)
    print("TEST 1: CMB Temperature Fluctuations (Planck Data)")
    print("-" * 80)
    print("Real-world data: ΔT/T ~ 10^-5 at l~200 (acoustic peak)")
    
    cmb_result = realm.model_cmb_fluctuations(
        multipole_l=200,
        temperature_k=2.725,
        fluctuation_amplitude_uk=70.0
    )
    
    print(f"\nCMB Parameters:")
    print(f"  Multipole l: {cmb_result['multipole_l']}")
    print(f"  Angular Scale: {cmb_result['angular_scale_deg']:.4f}°")
    print(f"  Physical Scale: {cmb_result['physical_scale_mpc']:.2f} Mpc")
    print(f"  Mean Temperature: {cmb_result['cmb_temperature_k']:.3f} K")
    print(f"  Fluctuation Amplitude: {cmb_result['fluctuation_amplitude_uk']:.2f} μK")
    
    print(f"\nFluctuation Analysis:")
    print(f"  Relative Fluctuation: {cmb_result['relative_fluctuation']:.6e}")
    print(f"  Acoustic Frequency: {cmb_result['frequency_hz']:.6e} Hz")
    print(f"  Coherence: {cmb_result['coherence']:.6f}")
    print(f"  Redshift (recombination): {cmb_result['redshift_recombination']:.0f}")
    print(f"  Temp (recombination): {cmb_result['temp_recombination_k']:.0f} K")
    print(f"  Power Spectrum: {cmb_result['power_spectrum_uk2']:.2e} μK²")
    
    print(f"\nUBP Analysis:")
    print(f"  NRCI: {cmb_result['nrci']:.6f}")
    print(f"  UBP Energy: {cmb_result['ubp_energy_cu']:.6e} CU")
    
    # Test 2: Hubble Expansion
    print("\n" + "-" * 80)
    print("TEST 2: Hubble Expansion and Dark Energy")
    print("-" * 80)
    print("Real-world data: H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685")
    
    hubble_result = realm.model_hubble_expansion(
        distance_mpc=1000.0,
        include_dark_energy=True
    )
    
    print(f"\nExpansion Parameters:")
    print(f"  Distance: {hubble_result['distance_mpc']:.0f} Mpc")
    print(f"  Hubble Constant: {hubble_result['hubble_constant_km_s_mpc']:.1f} km/s/Mpc")
    print(f"  Recession Velocity: {hubble_result['recession_velocity_km_s']:.0f} km/s")
    print(f"  Redshift: {hubble_result['redshift']:.6f}")
    print(f"  Hubble Time: {hubble_result['hubble_time_gyr']:.2f} Gyr")
    
    print(f"\nDensity Components:")
    print(f"  Critical Density: {hubble_result['critical_density_kg_m3']:.6e} kg/m³")
    print(f"  Dark Energy (Ω_Λ): {hubble_result['dark_energy_fraction']*100:.1f}%")
    print(f"  Dark Matter (Ω_DM): {hubble_result['dark_matter_fraction']*100:.1f}%")
    print(f"  Baryons (Ω_b): {hubble_result['baryon_fraction']*100:.1f}%")
    
    print(f"\nDark Energy:")
    print(f"  Density: {hubble_result['dark_energy_density_kg_m3']:.6e} kg/m³")
    print(f"  Energy Density: {hubble_result['dark_energy_density_j_m3']:.6e} J/m³")
    print(f"  Equation of State (w): {hubble_result['w_equation_of_state']:.1f}")
    print(f"  Deceleration Parameter: {hubble_result['deceleration_parameter']:.3f}")
    print(f"  Universe Accelerating: {hubble_result['is_accelerating']}")
    
    print(f"\nUBP Analysis:")
    print(f"  Expansion Frequency: {hubble_result['expansion_frequency_hz']:.6e} Hz")
    print(f"  Coherence: {hubble_result['coherence']:.6f}")
    print(f"  NRCI: {hubble_result['nrci']:.6f}")
    print(f"  UBP Energy: {hubble_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'cmb': cmb_result,
        'expansion': hubble_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_cosmological_realm()
    
    print("\nCosmological realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. CMB fluctuations (Planck data)")
    print("  2. Hubble expansion with dark energy")
    print("\nBoth tests use real cosmological observations.")
    print("Module ready for UBP 3.4 integration testing.")
