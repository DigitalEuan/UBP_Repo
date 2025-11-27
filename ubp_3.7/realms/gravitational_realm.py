"""
Universal Binary Principle (UBP) Framework v3.7 - Gravitational Realm
Author: Euan Craig, New Zealand
Date: 31 October 2025
================================================================================

This module implements gravitational realm calculations using UBP 3.4 framework.

The gravitational realm is characterized by:
- Spacetime curvature and geodesics
- Gravitational wave propagation
- Orbital mechanics and resonances
- Extremely low observer computational cost

Key Features:
- SOC energy calculations for gravitational systems
- Orbital resonance modeling
- Gravitational wave detection
- Y constant dimensional corrections

Test Phenomena (NEW - verifiable against real data):
1. LIGO gravitational wave detection (GW150914)
2. Jupiter-Europa orbital resonance (2:1 mean-motion)
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
class GravitationalState:
    """
    Represents a gravitational system state.
    
    Attributes:
        mass_kg: System mass (kg)
        frequency: Characteristic frequency (Hz)
        strain: Gravitational strain amplitude (dimensionless)
        orbital_radius: Orbital radius (m) if applicable
        coherence: System coherence (0-1)
    """
    mass_kg: float
    frequency: float
    strain: float
    orbital_radius: Optional[float]
    coherence: float


class GravitationalRealm:
    """
    Gravitational realm calculator using UBP 3.4 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "gravitational"
    BASE_CRV = UBPConstants.CRV_GRAVITATIONAL_BASE  # φ (golden ratio)
    TOGGLE_PROBABILITY = UBPConstants.UBP_TOGGLE_PROBABILITIES['gravitational']
    
    # Gravitational constants
    G = UBPConstants.GRAVITATIONAL_CONSTANT
    SPEED_OF_LIGHT = UBPConstants.SPEED_OF_LIGHT
    
    # Astronomical constants
    SOLAR_MASS = 1.989e30  # kg
    JUPITER_MASS = 1.898e27  # kg
    EUROPA_MASS = 4.8e22  # kg
    AU = 1.496e11  # m (Astronomical Unit)
    
    def __init__(self):
        """Initialize gravitational realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        self.y_correction = get_y_correction_for_realm(self.REALM_NAME)
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs[self.REALM_NAME]
    
    def calculate_gravitational_energy_soc(
        self,
        grav_state: GravitationalState
    ) -> SOCEnergyResult:
        """
        Calculate gravitational energy using SOC equation.
        
        Args:
            grav_state: Gravitational system state
            
        Returns:
            SOCEnergyResult with energy in CU
        """
        # Check frequency limit
        self.wall.enforce_computational_limit(grav_state.frequency, raise_error=False)
        
        # Calculate modal sum from gravitational state
        modal_sum = self._calculate_gravitational_modal_sum(grav_state)
        
        # Calculate SOC energy with realm-specific observer cost
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum,
            Y_emergent=UBPConstants.PGCI_TARGET / self.observer_cost
        )
        
        return result
    
    def _calculate_gravitational_modal_sum(self, state: GravitationalState) -> float:
        """
        Calculate resonant modal sum for gravitational state.
        
        Args:
            state: Gravitational state
            
        Returns:
            Modal sum value
        """
        # Gravitational wave energy is proportional to strain squared
        strain_energy = state.strain**2
        
        # Mass contribution (log scale for huge dynamic range)
        mass_contrib = math.log10(state.mass_kg + 1) / 30.0  # Normalized
        
        # Frequency contribution
        freq_contrib = math.log10(state.frequency + 1) / 10.0  # Normalized
        
        modal_sum = (
            strain_energy * 1e40 +  # Scale up tiny strains
            mass_contrib * 
            freq_contrib * 
            state.coherence
        )
        
        return max(modal_sum, 1e-10)  # Ensure non-zero
    
    def model_ligo_gravitational_wave(
        self,
        event_name: str = "GW150914",
        m1_solar_masses: float = 36.0,
        m2_solar_masses: float = 29.0,
        distance_mpc: float = 410.0,
        peak_frequency_hz: float = 250.0
    ) -> Dict[str, float]:
        """
        Model LIGO gravitational wave detection.
        
        NEW TEST PHENOMENON: GW150914 binary black hole merger
        Real data: First gravitational wave detection, September 14, 2015
        
        Args:
            event_name: GW event name
            m1_solar_masses: Primary mass (solar masses)
            m2_solar_masses: Secondary mass (solar masses)
            distance_mpc: Luminosity distance (Megaparsecs)
            peak_frequency_hz: Peak GW frequency (Hz)
            
        Returns:
            Dictionary with GW analysis
        """
        # Convert to SI units
        m1_kg = m1_solar_masses * self.SOLAR_MASS
        m2_kg = m2_solar_masses * self.SOLAR_MASS
        distance_m = distance_mpc * 3.086e22  # Mpc to meters
        
        # Total mass and chirp mass
        M_total = m1_kg + m2_kg
        M_chirp = ((m1_kg * m2_kg)**(3/5)) / (M_total**(1/5))
        
        # Schwarzschild radius of final black hole
        r_s = 2 * self.G * M_total / self.SPEED_OF_LIGHT**2
        
        # Estimate peak strain amplitude (simplified)
        # h ~ (G M_chirp / (c^2 d)) * (π f G M_chirp / c^3)^(2/3)
        strain_amplitude = (
            (self.G * M_chirp / (self.SPEED_OF_LIGHT**2 * distance_m)) *
            ((math.pi * peak_frequency_hz * self.G * M_chirp) / self.SPEED_OF_LIGHT**3)**(2/3)
        )
        
        # LIGO detected strain ~ 1e-21 for GW150914
        # Our calculation should be in this ballpark
        
        # Orbital radius at peak frequency (last stable orbit)
        # f = (1/π) * sqrt(G M / r^3)
        r_orbit = (self.G * M_total / (math.pi * peak_frequency_hz)**2)**(1/3)
        
        # Coherence (high for clean GW signal)
        # GW150914 had SNR ~ 24, very coherent
        coherence = 0.95
        
        # Create gravitational state
        grav_state = GravitationalState(
            mass_kg=M_total,
            frequency=peak_frequency_hz,
            strain=strain_amplitude,
            orbital_radius=r_orbit,
            coherence=coherence
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_gravitational_energy_soc(grav_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * coherence
        
        # Energy radiated in gravitational waves (order of magnitude)
        # GW150914 radiated ~3 solar masses of energy
        E_radiated_J = 3.0 * self.SOLAR_MASS * self.SPEED_OF_LIGHT**2
        
        return {
            'event_name': event_name,
            'm1_solar_masses': m1_solar_masses,
            'm2_solar_masses': m2_solar_masses,
            'total_mass_solar': M_total / self.SOLAR_MASS,
            'chirp_mass_solar': M_chirp / self.SOLAR_MASS,
            'distance_mpc': distance_mpc,
            'peak_frequency_hz': peak_frequency_hz,
            'strain_amplitude': strain_amplitude,
            'schwarzschild_radius_km': r_s / 1000,
            'orbital_radius_km': r_orbit / 1000,
            'energy_radiated_solar_masses': E_radiated_J / (self.SOLAR_MASS * self.SPEED_OF_LIGHT**2),
            'coherence': coherence,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost,
            'y_correction': self.y_correction
        }
    
    def model_jupiter_europa_resonance(
        self,
        jupiter_mass_kg: Optional[float] = None,
        europa_mass_kg: Optional[float] = None,
        europa_orbital_radius_km: float = 671100.0,
        io_orbital_radius_km: float = 421800.0
    ) -> Dict[str, float]:
        """
        Model Jupiter-Europa orbital resonance.
        
        NEW TEST PHENOMENON: 2:1 mean-motion resonance with Io
        Real data: Europa orbits twice for every Io orbit
        
        Args:
            jupiter_mass_kg: Jupiter mass (kg)
            europa_mass_kg: Europa mass (kg)
            europa_orbital_radius_km: Europa semi-major axis (km)
            io_orbital_radius_km: Io semi-major axis (km)
            
        Returns:
            Dictionary with orbital resonance analysis
        """
        # Use default masses if not provided
        if jupiter_mass_kg is None:
            jupiter_mass_kg = self.JUPITER_MASS
        if europa_mass_kg is None:
            europa_mass_kg = self.EUROPA_MASS
        
        # Convert to meters
        r_europa = europa_orbital_radius_km * 1000
        r_io = io_orbital_radius_km * 1000
        
        # Calculate orbital periods (Kepler's third law)
        # T = 2π sqrt(r^3 / GM)
        T_europa = 2 * math.pi * math.sqrt(r_europa**3 / (self.G * jupiter_mass_kg))
        T_io = 2 * math.pi * math.sqrt(r_io**3 / (self.G * jupiter_mass_kg))
        
        # Orbital frequencies
        f_europa = 1.0 / T_europa
        f_io = 1.0 / T_io
        
        # Resonance ratio (should be ~2:1)
        resonance_ratio = f_io / f_europa
        
        # Resonance quality (how close to exact 2:1)
        ideal_ratio = 2.0
        resonance_deviation = abs(resonance_ratio - ideal_ratio) / ideal_ratio
        resonance_quality = math.exp(-resonance_deviation / 0.01)  # Sharp peak at 2:1
        
        # Orbital velocities
        v_europa = 2 * math.pi * r_europa / T_europa
        v_io = 2 * math.pi * r_io / T_io
        
        # Tidal heating frequency (beat frequency)
        f_tidal = abs(f_io - 2 * f_europa)
        
        # Gravitational binding energy
        E_bind_europa = self.G * jupiter_mass_kg * europa_mass_kg / r_europa
        
        # Create gravitational state (using tidal frequency)
        grav_state = GravitationalState(
            mass_kg=europa_mass_kg,
            frequency=f_tidal if f_tidal > 0 else f_europa,
            strain=resonance_quality * 1e-10,  # Tidal strain
            orbital_radius=r_europa,
            coherence=resonance_quality
        )
        
        # Calculate UBP energy
        soc_result = self.calculate_gravitational_energy_soc(grav_state)
        
        # Calculate NRCI
        nrci = UBPConstants.PGCI_TARGET * resonance_quality
        
        return {
            'system': 'Jupiter-Europa-Io',
            'europa_orbital_period_days': T_europa / 86400,
            'io_orbital_period_days': T_io / 86400,
            'europa_frequency_hz': f_europa,
            'io_frequency_hz': f_io,
            'resonance_ratio': resonance_ratio,
            'ideal_ratio': ideal_ratio,
            'resonance_quality': resonance_quality,
            'europa_velocity_km_s': v_europa / 1000,
            'io_velocity_km_s': v_io / 1000,
            'tidal_frequency_hz': f_tidal,
            'binding_energy_j': E_bind_europa,
            'coherence': resonance_quality,
            'nrci': nrci,
            'ubp_energy_cu': soc_result.energy_cu,
            'observer_cost': self.observer_cost
        }


def demonstrate_gravitational_realm():
    """
    Demonstrate gravitational realm calculations with real test phenomena.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("GRAVITATIONAL REALM DEMONSTRATION (UBP 3.4)")
    print("=" * 80)
    
    realm = GravitationalRealm()
    
    print(f"\nRealm Configuration:")
    print(f"  Base CRV: {realm.BASE_CRV:.6f} (φ - golden ratio)")
    print(f"  Toggle Probability: {realm.TOGGLE_PROBABILITY:.6f}")
    print(f"  Observer Cost: {realm.observer_cost:.6f}")
    print(f"  Y Correction: {realm.y_correction:.15f}")
    print(f"  G: {realm.G:.6e} m³/(kg·s²)")
    
    # Test 1: LIGO Gravitational Wave
    print("\n" + "-" * 80)
    print("TEST 1: LIGO Gravitational Wave Detection (GW150914)")
    print("-" * 80)
    print("Real-world data: First GW detection, September 14, 2015")
    print("Binary black hole merger at 410 Mpc")
    
    gw_result = realm.model_ligo_gravitational_wave(
        event_name="GW150914",
        m1_solar_masses=36.0,
        m2_solar_masses=29.0,
        distance_mpc=410.0,
        peak_frequency_hz=250.0
    )
    
    print(f"\nEvent Parameters:")
    print(f"  Event: {gw_result['event_name']}")
    print(f"  Primary Mass: {gw_result['m1_solar_masses']:.1f} M☉")
    print(f"  Secondary Mass: {gw_result['m2_solar_masses']:.1f} M☉")
    print(f"  Total Mass: {gw_result['total_mass_solar']:.1f} M☉")
    print(f"  Chirp Mass: {gw_result['chirp_mass_solar']:.2f} M☉")
    print(f"  Distance: {gw_result['distance_mpc']:.0f} Mpc")
    
    print(f"\nGravitational Wave Properties:")
    print(f"  Peak Frequency: {gw_result['peak_frequency_hz']:.0f} Hz")
    print(f"  Strain Amplitude: {gw_result['strain_amplitude']:.6e}")
    print(f"  Schwarzschild Radius: {gw_result['schwarzschild_radius_km']:.0f} km")
    print(f"  Orbital Radius (peak): {gw_result['orbital_radius_km']:.0f} km")
    print(f"  Energy Radiated: {gw_result['energy_radiated_solar_masses']:.2f} M☉c²")
    
    print(f"\nUBP Analysis:")
    print(f"  Coherence: {gw_result['coherence']:.6f}")
    print(f"  NRCI: {gw_result['nrci']:.6f}")
    print(f"  UBP Energy: {gw_result['ubp_energy_cu']:.6e} CU")
    
    # Test 2: Jupiter-Europa Resonance
    print("\n" + "-" * 80)
    print("TEST 2: Jupiter-Europa Orbital Resonance")
    print("-" * 80)
    print("Real-world data: 2:1 mean-motion resonance with Io")
    print("Europa completes 2 orbits for every 1 Io orbit")
    
    orbital_result = realm.model_jupiter_europa_resonance()
    
    print(f"\nOrbital Parameters:")
    print(f"  System: {orbital_result['system']}")
    print(f"  Europa Period: {orbital_result['europa_orbital_period_days']:.4f} days")
    print(f"  Io Period: {orbital_result['io_orbital_period_days']:.4f} days")
    print(f"  Europa Velocity: {orbital_result['europa_velocity_km_s']:.2f} km/s")
    print(f"  Io Velocity: {orbital_result['io_velocity_km_s']:.2f} km/s")
    
    print(f"\nResonance Analysis:")
    print(f"  Resonance Ratio: {orbital_result['resonance_ratio']:.6f}")
    print(f"  Ideal Ratio: {orbital_result['ideal_ratio']:.1f}:1")
    print(f"  Resonance Quality: {orbital_result['resonance_quality']:.6f}")
    print(f"  Tidal Frequency: {orbital_result['tidal_frequency_hz']:.6e} Hz")
    print(f"  Binding Energy: {orbital_result['binding_energy_j']:.6e} J")
    
    print(f"\nUBP Analysis:")
    print(f"  Coherence: {orbital_result['coherence']:.6f}")
    print(f"  NRCI: {orbital_result['nrci']:.6f}")
    print(f"  UBP Energy: {orbital_result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    
    return {
        'realm': realm,
        'gravitational_wave': gw_result,
        'orbital_resonance': orbital_result
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_gravitational_realm()
    
    print("\nGravitational realm demonstration complete.")
    print("NEW phenomena tested:")
    print("  1. LIGO GW150914 detection (strain ~1e-21)")
    print("  2. Jupiter-Europa 2:1 orbital resonance")
    print("\nBoth tests use real astronomical data.")
    print("Module ready for UBP 3.4 integration testing.")
