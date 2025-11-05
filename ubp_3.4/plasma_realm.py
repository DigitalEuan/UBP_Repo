"""
Universal Binary Principle (UBP) Framework v3.4 - Plasma Realm
Author: Euan Craig, New Zealand
Date: 31 October 2025
================================================================================

This module implements plasma realm calculations using UBP 3.4 framework.

The plasma realm is characterized by:
- Collective oscillations and plasma waves
- Magnetic confinement and instabilities
- High-temperature ionized gas dynamics
- Moderate to high observer computational cost

Key Features:
- SOC energy calculations for plasma systems
- Plasma frequency and Debye length modeling
- Tokamak confinement analysis
- Y constant dimensional corrections

Test Phenomena (NEW - verifiable against real data):
1. Tokamak plasma confinement (ITER parameters)
2. Solar corona plasma dynamics
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# UBP 3.4 modules
from system_constants import UBPConstants
from y_constants import get_y_correction_for_realm
from soc_energy import SOCCalculator, SOCEnergyResult
from observer_framework import get_default_realm_observer_costs
from wall_of_reality import WallOfReality


@dataclass
class PlasmaState:
    """
    Represents a plasma system state.
    
    Attributes:
        electron_density_m3: Electron number density (m⁻³)
        temperature_ev: Plasma temperature (eV)
        magnetic_field_t: Magnetic field strength (Tesla)
        frequency: Characteristic frequency (Hz)
        coherence: System coherence (0-1)
    """
    electron_density_m3: float
    temperature_ev: float
    magnetic_field_t: float
    frequency: float
    coherence: float


class PlasmaRealm:
    """
    Plasma realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "plasma"
    BASE_CRV = UBPConstants.CRV_PLASMA_BASE  # 2π
    TOGGLE_PROBABILITY = UBPConstants.UBP_TOGGLE_PROBABILITIES.get('plasma', 0.6)
    
    # Plasma constants
    ELECTRON_MASS = UBPConstants.ELECTRON_MASS
    ELECTRON_CHARGE = UBPConstants.ELEMENTARY_CHARGE
    VACUUM_PERMITTIVITY = UBPConstants.VACUUM_PERMITTIVITY
    BOLTZMANN_CONSTANT = UBPConstants.BOLTZMANN_CONSTANT
    
    def __init__(self):
        """Initialize plasma realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs.get(self.REALM_NAME, UBPConstants.O_OBSERVER)
    
    def calculate_plasma_energy_soc(
        self,
        plasma_state: PlasmaState
    ) -> SOCEnergyResult:
        """
        Calculate plasma energy using SOC equation.
        
        Args:
            plasma_state: Plasma system state
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(plasma_state.frequency, raise_error=False)
        
        # Calculate modal sum from plasma state
        modal_sum = self._calculate_plasma_modal_sum(plasma_state)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_plasma_modal_sum(self, state: PlasmaState) -> float:
        """
        Calculate resonant modal sum for plasma state.
        
        Args:
            state: Plasma state
            
        Returns:
            Modal sum value
        """
        # Density contribution (log scale)
        density_contrib = math.log10(state.electron_density_m3 + 1) / 25.0  # Normalized
        
        # Temperature contribution (log scale for eV)
        temp_contrib = math.log10(state.temperature_ev + 1) / 5.0
        
        # Magnetic field contribution
        b_field_contrib = math.log10(state.magnetic_field_t + 1) / 2.0
        
        # Frequency contribution
        freq_contrib = math.log10(state.frequency + 1) / 15.0
        
        modal_sum = (
            density_contrib * 
            temp_contrib * 
            (1.0 + b_field_contrib) *
            freq_contrib * 
            state.coherence
        )
        
        return max(modal_sum, 1e-10)  # Ensure non-zero
    
    def calculate_plasma_parameters(
        self,
        electron_density_m3: float,
        temperature_ev: float
    ) -> Dict[str, float]:
        """
        Calculate fundamental plasma parameters.
        
        Args:
            electron_density_m3: Electron density (m⁻³)
            temperature_ev: Temperature (eV)
            
        Returns:
            Dictionary with plasma parameters
        """
        # Plasma frequency
        # ω_p = sqrt(n_e * e² / (ε₀ * m_e))
        omega_p = math.sqrt(
            electron_density_m3 * self.ELECTRON_CHARGE**2 / 
            (self.VACUUM_PERMITTIVITY * self.ELECTRON_MASS)
        )
        f_p = omega_p / (2 * math.pi)
        
        # Debye length
        # λ_D = sqrt(ε₀ * k_B * T / (n_e * e²))
        temp_joules = temperature_ev * self.ELECTRON_CHARGE
        lambda_d = math.sqrt(
            self.VACUUM_PERMITTIVITY * temp_joules / 
            (electron_density_m3 * self.ELECTRON_CHARGE**2)
        )
        
        # Number of particles in Debye sphere
        # N_D = n_e * (4π/3) * λ_D³
        n_d = electron_density_m3 * (4 * math.pi / 3) * lambda_d**3
        
        # Thermal velocity
        # v_th = sqrt(k_B * T / m_e)
        v_th = math.sqrt(temp_joules / self.ELECTRON_MASS)
        
        return {
            'plasma_frequency_hz': f_p,
            'debye_length_m': lambda_d,
            'debye_number': n_d,
            'thermal_velocity_m_s': v_th
        }
    
    def model_tokamak_plasma(
        self,
        major_radius_m: float = 6.2,
        minor_radius_m: float = 2.0,
        electron_density_m3: float = 1e20,
        temperature_kev: float = 15.0,
        magnetic_field_t: float = 5.3,
        confinement_time_s: float = 3.7
    ) -> Dict[str, float]:
        """
        Model tokamak plasma confinement.
        
        NEW TEST PHENOMENON: ITER-like tokamak parameters
        Real data: ITER design - R=6.2m, T=15keV, B=5.3T
        
        Args:
            major_radius_m: Major radius (m)
            minor_radius_m: Minor radius (m)
            electron_density_m3: Electron density (m⁻³)
            temperature_kev: Temperature (keV)
            magnetic_field_t: Toroidal magnetic field (T)
            confinement_time_s: Energy confinement time (s)
            
        Returns:
            Dictionary with tokamak analysis
        """
        # Convert temperature to eV
        temperature_ev = temperature_kev * 1000.0
        
        # Calculate plasma parameters
        plasma_params = self.calculate_plasma_parameters(electron_density_m3, temperature_ev)
        
        # Plasma volume
        volume_m3 = 2 * math.pi**2 * major_radius_m * minor_radius_m**2
        
        # Total number of electrons
        n_electrons = electron_density_m3 * volume_m3
        
        # Plasma pressure (n * k * T)
        temp_joules = temperature_ev * self.ELECTRON_CHARGE
        pressure_pa = electron_density_m3 * temp_joules
        
        # Magnetic pressure (B² / 2μ₀)
        mu_0 = 4 * math.pi * 1e-7  # Vacuum permeability
        magnetic_pressure_pa = magnetic_field_t**2 / (2 * mu_0)
        
        # Beta (plasma pressure / magnetic pressure)
        beta = pressure_pa / magnetic_pressure_pa
        
        # Lawson criterion parameter (n * τ_E * T)
        lawson_param = electron_density_m3 * confinement_time_s * temperature_ev
        lawson_criterion = 3e21  # m⁻³·s·eV for D-T fusion
        meets_lawson = lawson_param >= lawson_criterion
        
        # Gyrofrequency (cyclotron frequency)
        # ω_c = e * B / m_e
        omega_c = self.ELECTRON_CHARGE * magnetic_field_t / self.ELECTRON_MASS
        f_c = omega_c / (2 * math.pi)
        
        # Coherence (high for well-confined plasma)
        # Based on confinement quality
        coherence = min(0.95, 0.5 + (confinement_time_s / 10.0) * 0.45)
        
        # Create plasma state
        plasma_state = PlasmaState(
            electron_density_m3=electron_density_m3,
            temperature_ev=temperature_ev,
            magnetic_field_t=magnetic_field_t,
            frequency=plasma_params['plasma_frequency_hz'],
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_plasma_energy_soc(plasma_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        return {
            'tokamak_type': 'ITER-like',
            'major_radius_m': major_radius_m,
            'minor_radius_m': minor_radius_m,
            'volume_m3': volume_m3,
            'electron_density_m3': electron_density_m3,
            'temperature_kev': temperature_kev,
            'temperature_ev': temperature_ev,
            'magnetic_field_t': magnetic_field_t,
            'confinement_time_s': confinement_time_s,
            'plasma_frequency_hz': plasma_params['plasma_frequency_hz'],
            'plasma_frequency_ghz': plasma_params['plasma_frequency_hz'] / 1e9,
            'debye_length_m': plasma_params['debye_length_m'],
            'debye_number': plasma_params['debye_number'],
            'thermal_velocity_m_s': plasma_params['thermal_velocity_m_s'],
            'gyrofrequency_hz': f_c,
            'gyrofrequency_ghz': f_c / 1e9,
            'pressure_pa': pressure_pa,
            'magnetic_pressure_pa': magnetic_pressure_pa,
            'beta': beta,
            'lawson_parameter': lawson_param,
            'lawson_criterion': lawson_criterion,
            'meets_lawson': meets_lawson,
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }
    
    def model_solar_corona(
        self,
        electron_density_m3: float = 1e15,
        temperature_mk: float = 2.0,
        magnetic_field_t: float = 0.01,
        loop_length_mm: float = 100.0
    ) -> Dict[str, float]:
        """
        Model solar corona plasma dynamics.
        
        NEW TEST PHENOMENON: Coronal loops
        Real data: T~2MK, n~10^15 m⁻³, B~0.01T
        
        Args:
            electron_density_m3: Electron density (m⁻³)
            temperature_mk: Temperature (Mega-Kelvin)
            magnetic_field_t: Magnetic field (T)
            loop_length_mm: Coronal loop length (Mm)
            
        Returns:
            Dictionary with corona analysis
        """
        # Convert temperature to eV
        # 1 MK ≈ 86 eV
        temperature_ev = temperature_mk * 1e6 * self.BOLTZMANN_CONSTANT / self.ELECTRON_CHARGE
        
        # Calculate plasma parameters
        plasma_params = self.calculate_plasma_parameters(electron_density_m3, temperature_ev)
        
        # Sound speed in plasma
        # c_s = sqrt(k_B * T / m_i) where m_i is ion mass (assume protons)
        proton_mass = 1.673e-27  # kg
        temp_joules = temperature_ev * self.ELECTRON_CHARGE
        sound_speed_m_s = math.sqrt(temp_joules / proton_mass)
        
        # Alfvén speed
        # v_A = B / sqrt(μ₀ * ρ) where ρ = n * m_i
        mu_0 = 4 * math.pi * 1e-7
        mass_density = electron_density_m3 * proton_mass
        alfven_speed_m_s = magnetic_field_t / math.sqrt(mu_0 * mass_density)
        
        # Plasma beta
        pressure_pa = electron_density_m3 * temp_joules
        magnetic_pressure_pa = magnetic_field_t**2 / (2 * mu_0)
        beta = pressure_pa / magnetic_pressure_pa
        
        # Loop oscillation period (kink mode)
        # P ≈ 2L / v_A
        loop_length_m = loop_length_mm * 1e6
        oscillation_period_s = 2 * loop_length_m / alfven_speed_m_s
        oscillation_frequency_hz = 1.0 / oscillation_period_s
        
        # Coherence (coronal loops are moderately coherent)
        coherence = 0.70
        
        # Create plasma state
        plasma_state = PlasmaState(
            electron_density_m3=electron_density_m3,
            temperature_ev=temperature_ev,
            magnetic_field_t=magnetic_field_t,
            frequency=oscillation_frequency_hz,
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_plasma_energy_soc(plasma_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        return {
            'system': 'Solar Corona',
            'electron_density_m3': electron_density_m3,
            'temperature_mk': temperature_mk,
            'temperature_ev': temperature_ev,
            'magnetic_field_t': magnetic_field_t,
            'loop_length_mm': loop_length_mm,
            'plasma_frequency_hz': plasma_params['plasma_frequency_hz'],
            'plasma_frequency_mhz': plasma_params['plasma_frequency_hz'] / 1e6,
            'debye_length_m': plasma_params['debye_length_m'],
            'sound_speed_km_s': sound_speed_m_s / 1000,
            'alfven_speed_km_s': alfven_speed_m_s / 1000,
            'beta': beta,
            'oscillation_period_s': oscillation_period_s,
            'oscillation_frequency_hz': oscillation_frequency_hz,
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost
        }


def demonstrate_plasma_realm():
    """
    Demonstrate plasma realm calculations with real test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("PLASMA REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = PlasmaRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.6f} (2π)")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    
    # Test 1: Tokamak Plasma
    print("\n" + "-" * 80)
    print("TEST 1: Tokamak Plasma Confinement (ITER-like)")
    print("-" * 80)
    print("Real-world data: ITER design parameters")
    
    tokamak_result = realm.model_tokamak_plasma(
        major_radius_m=6.2,
        minor_radius_m=2.0,
        electron_density_m3=1e20,
        temperature_kev=15.0,
        magnetic_field_t=5.3,
        confinement_time_s=3.7
    )
    
    print(f"\nTokamak Parameters:")
    print(f"  Type: {tokamak_result['tokamak_type']}")
    print(f"  Major Radius: {tokamak_result['major_radius_m']:.1f} m")
    print(f"  Minor Radius: {tokamak_result['minor_radius_m']:.1f} m")
    print(f"  Volume: {tokamak_result['volume_m3']:.1f} m³")
    print(f"  Electron Density: {tokamak_result['electron_density_m3']:.2e} m⁻³")
    print(f"  Temperature: {tokamak_result['temperature_kev']:.1f} keV")
    print(f"  Magnetic Field: {tokamak_result['magnetic_field_t']:.1f} T")
    print(f"  Confinement Time: {tokamak_result['confinement_time_s']:.1f} s")
    
    print(f"\nPlasma Properties:")
    print(f"  Plasma Frequency: {tokamak_result['plasma_frequency_ghz']:.2f} GHz")
    print(f"  Debye Length: {tokamak_result['debye_length_m']:.6e} m")
    print(f"  Debye Number: {tokamak_result['debye_number']:.2e}")
    print(f"  Thermal Velocity: {tokamak_result['thermal_velocity_m_s']:.2e} m/s")
    print(f"  Gyrofrequency: {tokamak_result['gyrofrequency_ghz']:.2f} GHz")
    
    print(f"\nConfinement Analysis:")
    print(f"  Plasma Pressure: {tokamak_result['pressure_pa']:.2e} Pa")
    print(f"  Magnetic Pressure: {tokamak_result['magnetic_pressure_pa']:.2e} Pa")
    print(f"  Beta: {tokamak_result['beta']:.4f}")
    print(f"  Lawson Parameter: {tokamak_result['lawson_parameter']:.2e}")
    print(f"  Lawson Criterion: {tokamak_result['lawson_criterion']:.2e}")
    print(f"  Meets Lawson: {tokamak_result['meets_lawson']}")
    
    print(f"\nUBP Analysis:")
    print(f"  Coherence: {tokamak_result['coherence']:.6f}")
    print(f"  NRCI: {tokamak_result['nrci']:.6f}")
    print(f"  UBP Energy: {tokamak_result['ubp_energy_cu']:.6e} CU")
    
    # Test 2: Solar Corona
    print("\n" + "-" * 80)
    print("TEST 2: Solar Corona Plasma Dynamics")
    print("-" * 80)
    print("Real-world data: Coronal loops T~2MK, n~10^15 m⁻³")
    
    corona_result = realm.model_solar_corona(
        electron_density_m3=1e15,
        temperature_mk=2.0,
        magnetic_field_t=0.01,
        loop_length_mm=100.0
    )
    
    print(f"\nCorona Parameters:")
    print(f"  System: {corona_result['system']}")
    print(f"  Electron Density: {corona_result['electron_density_m3']:.2e} m⁻³")
    print(f"  Temperature: {corona_result['temperature_mk']:.1f} MK ({corona_result['temperature_ev']:.0f} eV)")
    print(f"  Magnetic Field: {corona_result['magnetic_field_t']:.3f} T")
    print(f"  Loop Length: {corona_result['loop_length_mm']:.0f} Mm")
    
    print(f"\nPlasma Properties:")
    print(f"  Plasma Frequency: {corona_result['plasma_frequency_mhz']:.2f} MHz")
    print(f"  Debye Length: {corona_result['debye_length_m']:.6e} m")
    print(f"  Sound Speed: {corona_result['sound_speed_km_s']:.0f} km/s")
    print(f"  Alfvén Speed: {corona_result['alfven_speed_km_s']:.0f} km/s")
    print(f"  Beta: {corona_result['beta']:.4f}")
    
    print(f"\nOscillation Analysis:")
    print(f"  Period: {corona_result['oscillation_period_s']:.0f} s")
    print(f"  Frequency: {corona_result['oscillation_frequency_hz']:.6e} Hz")
    
    print(f"\nUBP Analysis:")
    print(f"  Coherence: {corona_result['coherence']:.6f}")
    print(f"  NRCI: {corona_result['nrci']:.6f}")
    print(f"  UBP Energy: {corona_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'tokamak': tokamak_result,
        'corona': corona_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_plasma_realm()
    
    print("\nPlasma realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. ITER-like tokamak (15 keV, 5.3 T)")
    print("  2. Solar corona loops (2 MK, 100 Mm)")
    print("\nBoth tests use real plasma physics parameters.")
    print("Module ready for UBP 3.4 integration testing.")
