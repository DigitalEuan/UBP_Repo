"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Gravitational Realm
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Gravitational realm as coherence geometry.

**Paradigm Shift in 3.5**:
Gravity isn't a force - it's coherence curvature. Gravitational waves are
coherence ripples. Orbital resonances are coherence harmonics.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.5
"""

import math
from typing import Dict, Optional
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET
from system_constants import UBPConstants, PhysicalConstants, get_crv_for_realm
from energy_dual import EnergyCalculator


# ============================================================================
# GRAVITATIONAL STATE
# ============================================================================

@dataclass
class GravitationalState:
    """
    Gravitational system state in UBP 3.5.
    
    In 3.5, gravitational states are coherence configurations.
    """
    coherence: CoherenceState
    mass_kg: float
    frequency: float
    strain: float  # Gravitational strain amplitude
    orbital_radius: Optional[float] = None
    
    @property
    def nrci(self) -> float:
        """NRCI of this gravitational state."""
        return self.coherence.nrci


# ============================================================================
# GRAVITATIONAL REALM CALCULATOR
# ============================================================================

class GravitationalRealm:
    """
    Gravitational realm calculator for UBP 3.5.
    
    Gravity is coherence curvature.
    """
    
    # Realm constants
    REALM_NAME = "gravitational"
    
    # Physical constants
    G = PhysicalConstants.GRAVITATIONAL_CONSTANT
    SPEED_OF_LIGHT = PhysicalConstants.SPEED_OF_LIGHT
    
    # Astronomical constants
    SOLAR_MASS = 1.989e30  # kg
    JUPITER_MASS = 1.898e27  # kg
    EUROPA_MASS = 4.8e22  # kg
    AU = 1.496e11  # m
    
    def __init__(self):
        """Initialize gravitational realm calculator."""
        self.energy_calc = EnergyCalculator()
        self.crv = get_crv_for_realm(self.REALM_NAME)
    
    def calculate_gravitational_energy(
        self,
        grav_state: GravitationalState
    ) -> Dict[str, any]:
        """
        Calculate gravitational energy.
        
        Args:
            grav_state: GravitationalState to calculate
            
        Returns:
            Dictionary with energy results
        """
        # Modal sum from gravitational properties
        modal_sum = self._calculate_modal_sum(grav_state)
        
        # Calculate energy
        energy_result = self.energy_calc.calculate(
            modal_sum=modal_sum,
            realm=self.REALM_NAME,
            frequency=grav_state.frequency
        )
        
        return {
            'energy_cu': energy_result.energy_cu,
            'energy_joules': energy_result.energy_joules,
            'nrci': energy_result.nrci,
            'grav_nrci': grav_state.nrci,
            'frequency': grav_state.frequency,
            'strain': grav_state.strain,
            'mass_kg': grav_state.mass_kg
        }
    
    def _calculate_modal_sum(self, state: GravitationalState) -> float:
        """
        Calculate modal sum from gravitational state.
        
        Gravitational wave energy ∝ strain²
        """
        # Strain energy (gravitational waves)
        strain_energy = state.strain ** 2
        
        # Mass contribution (log scale for huge range)
        mass_contrib = math.log10(state.mass_kg + 1) / 30.0
        
        # Frequency contribution
        freq_contrib = math.log10(state.frequency + 1) / 10.0
        
        # Coherence contribution
        coherence_contrib = state.coherence.nrci
        
        modal_sum = (
            strain_energy * 1e40 +  # Scale up tiny strains
            mass_contrib * freq_contrib * coherence_contrib
        )
        
        return max(modal_sum, 1e-10)
    
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
        
        Real data: GW150914 binary black hole merger (Sept 14, 2015)
        First direct detection of gravitational waves.
        
        Args:
            event_name: GW event name
            m1_solar_masses: Primary mass (solar masses)
            m2_solar_masses: Secondary mass (solar masses)
            distance_mpc: Luminosity distance (Megaparsecs)
            peak_frequency_hz: Peak GW frequency (Hz)
            
        Returns:
            Dictionary with GW analysis
            
        Example:
            >>> realm = GravitationalRealm()
            >>> gw = realm.model_ligo_gravitational_wave()
            >>> print(f"Strain: {gw['strain_amplitude']:.2e}")
        """
        # Convert to SI units
        m1_kg = m1_solar_masses * self.SOLAR_MASS
        m2_kg = m2_solar_masses * self.SOLAR_MASS
        distance_m = distance_mpc * 3.086e22  # Mpc to meters
        
        # Total mass and chirp mass
        M_total = m1_kg + m2_kg
        M_chirp = ((m1_kg * m2_kg) ** (3/5)) / (M_total ** (1/5))
        
        # Schwarzschild radius
        r_s = 2 * self.G * M_total / self.SPEED_OF_LIGHT ** 2
        
        # Estimate peak strain amplitude
        # h ~ (G M_chirp / (c² d)) * (π f G M_chirp / c³)^(2/3)
        strain_amplitude = (
            (self.G * M_chirp / (self.SPEED_OF_LIGHT ** 2 * distance_m)) *
            ((math.pi * peak_frequency_hz * self.G * M_chirp) / self.SPEED_OF_LIGHT ** 3) ** (2/3)
        )
        
        # Orbital radius at peak frequency
        # f = (1/π) * sqrt(G M / r³)
        r_orbit = (self.G * M_total / (math.pi * peak_frequency_hz) ** 2) ** (1/3)
        
        # Coherence (GW150914 had SNR ~ 24, very coherent)
        coherence_level = 0.95
        
        # Create gravitational state
        coherence = CoherenceState(
            M_total,
            log_nrci_error=math.log(1 - coherence_level * NRCI_TARGET)
        )
        
        grav_state = GravitationalState(
            coherence=coherence,
            mass_kg=M_total,
            frequency=peak_frequency_hz,
            strain=strain_amplitude,
            orbital_radius=r_orbit
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_gravitational_energy(grav_state)
        
        # Energy radiated (GW150914 radiated ~3 solar masses)
        E_radiated_J = 3.0 * self.SOLAR_MASS * self.SPEED_OF_LIGHT ** 2
        
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
            'energy_radiated_solar_masses': E_radiated_J / (self.SOLAR_MASS * self.SPEED_OF_LIGHT ** 2),
            'coherence': coherence_level,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
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
        
        Real data: 2:1 mean-motion resonance with Io
        Europa orbits twice for every Io orbit.
        
        Args:
            jupiter_mass_kg: Jupiter mass (kg)
            europa_mass_kg: Europa mass (kg)
            europa_orbital_radius_km: Europa semi-major axis (km)
            io_orbital_radius_km: Io semi-major axis (km)
            
        Returns:
            Dictionary with orbital resonance analysis
            
        Example:
            >>> realm = GravitationalRealm()
            >>> resonance = realm.model_jupiter_europa_resonance()
            >>> print(f"Resonance ratio: {resonance['resonance_ratio']:.4f}")
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
        # T = 2π sqrt(r³ / GM)
        T_europa = 2 * math.pi * math.sqrt(r_europa ** 3 / (self.G * jupiter_mass_kg))
        T_io = 2 * math.pi * math.sqrt(r_io ** 3 / (self.G * jupiter_mass_kg))
        
        # Orbital frequencies
        f_europa = 1.0 / T_europa
        f_io = 1.0 / T_io
        
        # Resonance ratio (should be ~2:1)
        resonance_ratio = f_io / f_europa
        
        # Resonance quality (how close to exact 2:1)
        ideal_ratio = 2.0
        resonance_deviation = abs(resonance_ratio - ideal_ratio) / ideal_ratio
        resonance_quality = math.exp(-resonance_deviation / 0.01)
        
        # Orbital velocities
        v_europa = 2 * math.pi * r_europa / T_europa
        v_io = 2 * math.pi * r_io / T_io
        
        # Tidal heating frequency (beat frequency)
        f_tidal = abs(f_io - 2 * f_europa)
        
        # Gravitational binding energy
        E_bind_europa = self.G * jupiter_mass_kg * europa_mass_kg / r_europa
        
        # Create gravitational state
        coherence = CoherenceState(
            europa_mass_kg,
            log_nrci_error=math.log(1 - resonance_quality * NRCI_TARGET)
        )
        
        grav_state = GravitationalState(
            coherence=coherence,
            mass_kg=europa_mass_kg,
            frequency=f_tidal if f_tidal > 0 else f_europa,
            strain=resonance_quality * 1e-10,
            orbital_radius=r_europa
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_gravitational_energy(grav_state)
        
        return {
            'europa_orbital_period_days': T_europa / 86400,
            'io_orbital_period_days': T_io / 86400,
            'europa_frequency_hz': f_europa,
            'io_frequency_hz': f_io,
            'resonance_ratio': resonance_ratio,
            'resonance_deviation': resonance_deviation,
            'resonance_quality': resonance_quality,
            'europa_velocity_km_s': v_europa / 1000,
            'io_velocity_km_s': v_io / 1000,
            'tidal_frequency_hz': f_tidal,
            'binding_energy_joules': E_bind_europa,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 GRAVITATIONAL REALM - Gravity as Coherence Curvature")
    print("=" * 80)
    
    # Create realm
    print("\n1. Creating Gravitational Realm:")
    realm = GravitationalRealm()
    print(f"   Realm: {realm.REALM_NAME}")
    print(f"   CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
    
    # LIGO GW150914
    print("\n2. LIGO GW150914 Gravitational Wave:")
    gw = realm.model_ligo_gravitational_wave()
    print(f"   Event: {gw['event_name']}")
    print(f"   Total mass: {gw['total_mass_solar']:.1f} solar masses")
    print(f"   Chirp mass: {gw['chirp_mass_solar']:.1f} solar masses")
    print(f"   Distance: {gw['distance_mpc']:.0f} Mpc")
    print(f"   Peak frequency: {gw['peak_frequency_hz']:.0f} Hz")
    print(f"   Strain amplitude: {gw['strain_amplitude']:.2e}")
    print(f"   Energy radiated: {gw['energy_radiated_solar_masses']:.1f} solar masses")
    print(f"   NRCI: {gw['nrci']:.10f}")
    print(f"   UBP Energy: {gw['ubp_energy_cu']:.6e} CU")
    
    # Jupiter-Europa resonance
    print("\n3. Jupiter-Europa Orbital Resonance:")
    resonance = realm.model_jupiter_europa_resonance()
    print(f"   Europa period: {resonance['europa_orbital_period_days']:.2f} days")
    print(f"   Io period: {resonance['io_orbital_period_days']:.2f} days")
    print(f"   Resonance ratio: {resonance['resonance_ratio']:.4f} (ideal: 2.0)")
    print(f"   Resonance quality: {resonance['resonance_quality']:.6f}")
    print(f"   Tidal frequency: {resonance['tidal_frequency_hz']:.6e} Hz")
    print(f"   NRCI: {resonance['nrci']:.10f}")
    print(f"   UBP Energy: {resonance['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Gravity is Coherence Curvature")
    print("Gravitational waves are coherence ripples")
    print("Orbital resonances are coherence harmonics")
    print("=" * 80)
