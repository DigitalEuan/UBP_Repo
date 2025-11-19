"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - Cosmological Realm
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Cosmological realm as coherence evolution.

**Paradigm Shift in 3.5**:
The universe is coherence evolution. CMB fluctuations are coherence patterns.
Dark energy is coherence pressure. Cosmic expansion is coherence dynamics.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.5
"""

import math
from typing import Dict
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET
from system_constants import PhysicalConstants, get_crv_for_realm
from energy_dual import EnergyCalculator


# ============================================================================
# COSMOLOGICAL STATE
# ============================================================================

@dataclass
class CosmologicalState:
    """
    Cosmological system state in UBP 3.5.
    """
    coherence: CoherenceState
    frequency: float
    scale_mpc: float  # Megaparsecs
    temperature_k: float
    density_kg_m3: float
    
    @property
    def nrci(self) -> float:
        """NRCI of this cosmological state."""
        return self.coherence.nrci


# ============================================================================
# COSMOLOGICAL REALM CALCULATOR
# ============================================================================

class CosmologicalRealm:
    """
    Cosmological realm calculator for UBP 3.5.
    
    The universe is coherence evolution.
    """
    
    # Realm constants
    REALM_NAME = "cosmological"
    
    # Cosmological constants
    SPEED_OF_LIGHT = PhysicalConstants.SPEED_OF_LIGHT
    HUBBLE_CONSTANT = 67.4  # km/s/Mpc (Planck 2018)
    CMB_TEMPERATURE = 2.725  # K
    CRITICAL_DENSITY = 8.5e-27  # kg/m³
    DARK_ENERGY_FRACTION = 0.685  # Ω_Λ
    DARK_MATTER_FRACTION = 0.265  # Ω_DM
    BARYON_FRACTION = 0.05  # Ω_b
    
    # Unit conversions
    MPC_TO_METERS = 3.086e22  # Megaparsec to meters
    GYR_TO_SECONDS = 3.154e16  # Gigayear to seconds
    
    def __init__(self):
        """Initialize cosmological realm calculator."""
        self.energy_calc = EnergyCalculator()
        self.crv = get_crv_for_realm(self.REALM_NAME)
    
    def calculate_cosmological_energy(
        self,
        cosmo_state: CosmologicalState
    ) -> Dict[str, any]:
        """
        Calculate cosmological energy.
        
        Args:
            cosmo_state: CosmologicalState to calculate
            
        Returns:
            Dictionary with energy results
        """
        # Modal sum from cosmological properties
        modal_sum = self._calculate_modal_sum(cosmo_state)
        
        # Calculate energy
        energy_result = self.energy_calc.calculate(
            modal_sum=modal_sum,
            realm=self.REALM_NAME,
            frequency=cosmo_state.frequency
        )
        
        return {
            'energy_cu': energy_result.energy_cu,
            'energy_joules': energy_result.energy_joules,
            'nrci': energy_result.nrci,
            'cosmo_nrci': cosmo_state.nrci,
            'frequency': cosmo_state.frequency,
            'scale_mpc': cosmo_state.scale_mpc,
            'temperature_k': cosmo_state.temperature_k
        }
    
    def _calculate_modal_sum(self, state: CosmologicalState) -> float:
        """
        Calculate modal sum from cosmological state.
        """
        # Scale contribution (log scale for vast distances)
        scale_contrib = math.log10(state.scale_mpc + 1) / 5.0
        
        # Density contribution
        density_contrib = math.log10(state.density_kg_m3 * 1e30 + 1) / 10.0
        
        # Temperature contribution
        temp_contrib = math.log10(state.temperature_k + 1) / 3.0
        
        # Frequency contribution (very low frequencies)
        freq_contrib = math.log10(state.frequency + 1e-20) / 20.0
        
        # Coherence contribution
        coherence_contrib = state.coherence.nrci
        
        modal_sum = (
            scale_contrib * 
            density_contrib * 
            temp_contrib * 
            coherence_contrib *
            (1.0 + freq_contrib)
        )
        
        return max(modal_sum, 1e-10)
    
    def model_cmb_fluctuations(
        self,
        angular_scale_arcmin: float = 1.0,
        temperature_fluctuation_uk: float = 100.0
    ) -> Dict[str, float]:
        """
        Model CMB temperature fluctuations.
        
        Real data: WMAP/Planck observations
        
        Args:
            angular_scale_arcmin: Angular scale (arcminutes)
            temperature_fluctuation_uk: Temperature fluctuation (microKelvin)
            
        Returns:
            Dictionary with CMB analysis
            
        Example:
            >>> realm = CosmologicalRealm()
            >>> cmb = realm.model_cmb_fluctuations(angular_scale_arcmin=1.0)
            >>> print(f"ΔT/T: {cmb['relative_fluctuation']:.2e}")
        """
        # Convert angular scale to multipole moment
        # ℓ ≈ 180° / θ (for small angles)
        angular_scale_deg = angular_scale_arcmin / 60.0
        multipole = 180.0 / angular_scale_deg
        
        # Physical scale at last scattering surface
        # Distance to last scattering ~ 14 Gpc
        distance_to_ls_mpc = 14000.0  # Mpc
        physical_scale_mpc = distance_to_ls_mpc * angular_scale_deg * (math.pi / 180.0)
        
        # Characteristic frequency (sound waves in early universe)
        # f ~ c_s / λ, where c_s ~ c/√3 for radiation-dominated plasma
        sound_speed = self.SPEED_OF_LIGHT / math.sqrt(3)
        wavelength_m = physical_scale_mpc * self.MPC_TO_METERS
        frequency = sound_speed / wavelength_m
        
        # Temperature fluctuation
        delta_T = temperature_fluctuation_uk * 1e-6  # K
        relative_fluctuation = delta_T / self.CMB_TEMPERATURE
        
        # Coherence (CMB is highly coherent)
        coherence_level = 1.0 - relative_fluctuation
        
        # Energy density of CMB
        stefan_boltzmann = 5.670374419e-8  # W m^-2 K^-4
        energy_density = 4 * stefan_boltzmann * self.CMB_TEMPERATURE ** 4 / self.SPEED_OF_LIGHT
        
        # Create cosmological state
        coherence = CoherenceState(
            energy_density,
            log_nrci_error=math.log(1 - coherence_level * NRCI_TARGET)
        )
        
        cosmo_state = CosmologicalState(
            coherence=coherence,
            frequency=frequency,
            scale_mpc=physical_scale_mpc,
            temperature_k=self.CMB_TEMPERATURE,
            density_kg_m3=energy_density / (self.SPEED_OF_LIGHT ** 2)
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_cosmological_energy(cosmo_state)
        
        return {
            'angular_scale_arcmin': angular_scale_arcmin,
            'angular_scale_deg': angular_scale_deg,
            'multipole_moment': multipole,
            'physical_scale_mpc': physical_scale_mpc,
            'frequency_hz': frequency,
            'temperature_fluctuation_uk': temperature_fluctuation_uk,
            'relative_fluctuation': relative_fluctuation,
            'cmb_temperature_k': self.CMB_TEMPERATURE,
            'energy_density_j_m3': energy_density,
            'coherence': coherence_level,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
        }
    
    def model_hubble_expansion(
        self,
        redshift: float = 0.0
    ) -> Dict[str, float]:
        """
        Model Hubble expansion and dark energy.
        
        Real data: Hubble constant measurements
        
        Args:
            redshift: Cosmological redshift z
            
        Returns:
            Dictionary with expansion analysis
            
        Example:
            >>> realm = CosmologicalRealm()
            >>> expansion = realm.model_hubble_expansion(redshift=1.0)
            >>> print(f"H(z): {expansion['hubble_parameter_km_s_mpc']:.1f} km/s/Mpc")
        """
        # Hubble parameter as function of redshift
        # H(z) = H₀ * sqrt(Ω_m(1+z)³ + Ω_Λ)
        matter_term = (self.DARK_MATTER_FRACTION + self.BARYON_FRACTION) * (1 + redshift) ** 3
        dark_energy_term = self.DARK_ENERGY_FRACTION
        
        hubble_z = self.HUBBLE_CONSTANT * math.sqrt(matter_term + dark_energy_term)
        
        # Age of universe at redshift z (approximate)
        # t(z) ≈ (2/3H₀) * (1+z)^(-3/2) for matter-dominated
        age_gyr = (2.0 / 3.0) * (1.0 / self.HUBBLE_CONSTANT) * (1 + redshift) ** (-1.5) * 100.0 / 3.086e19 * 3.154e16 / 1e9
        
        # Dark energy density
        dark_energy_density = self.DARK_ENERGY_FRACTION * self.CRITICAL_DENSITY
        
        # Characteristic frequency (Hubble frequency)
        hubble_frequency = hubble_z * 1000.0 / self.MPC_TO_METERS  # Hz
        
        # Coherence (universe is coherent on large scales)
        coherence_level = 0.999
        
        # Create cosmological state
        coherence = CoherenceState(
            dark_energy_density,
            log_nrci_error=math.log(1 - coherence_level * NRCI_TARGET)
        )
        
        cosmo_state = CosmologicalState(
            coherence=coherence,
            frequency=hubble_frequency,
            scale_mpc=self.SPEED_OF_LIGHT / (hubble_z * 1000.0),  # Hubble length
            temperature_k=self.CMB_TEMPERATURE * (1 + redshift),
            density_kg_m3=dark_energy_density
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_cosmological_energy(cosmo_state)
        
        return {
            'redshift': redshift,
            'hubble_parameter_km_s_mpc': hubble_z,
            'age_gyr': age_gyr,
            'hubble_frequency_hz': hubble_frequency,
            'hubble_length_mpc': self.SPEED_OF_LIGHT / (hubble_z * 1000.0),
            'dark_energy_density_kg_m3': dark_energy_density,
            'dark_energy_fraction': self.DARK_ENERGY_FRACTION,
            'matter_fraction': self.DARK_MATTER_FRACTION + self.BARYON_FRACTION,
            'coherence': coherence_level,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 COSMOLOGICAL REALM - Universe as Coherence Evolution")
    print("=" * 80)
    
    # Create realm
    print("\n1. Creating Cosmological Realm:")
    realm = CosmologicalRealm()
    print(f"   Realm: {realm.REALM_NAME}")
    print(f"   CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
    
    # CMB fluctuations
    print("\n2. CMB Temperature Fluctuations (WMAP/Planck):")
    angular_scales = [0.5, 1.0, 5.0]  # arcminutes
    
    for scale in angular_scales:
        cmb = realm.model_cmb_fluctuations(angular_scale_arcmin=scale)
        print(f"\n   Angular scale: {scale:.1f} arcmin (ℓ ≈ {cmb['multipole_moment']:.0f}):")
        print(f"     Physical scale: {cmb['physical_scale_mpc']:.2f} Mpc")
        print(f"     ΔT/T: {cmb['relative_fluctuation']:.2e}")
        print(f"     Frequency: {cmb['frequency_hz']:.2e} Hz")
        print(f"     NRCI: {cmb['nrci']:.10f}")
        print(f"     UBP Energy: {cmb['ubp_energy_cu']:.6e} CU")
    
    # Hubble expansion
    print("\n3. Hubble Expansion and Dark Energy:")
    redshifts = [0.0, 0.5, 1.0, 2.0]
    
    for z in redshifts:
        expansion = realm.model_hubble_expansion(redshift=z)
        print(f"\n   Redshift z = {z:.1f}:")
        print(f"     H(z): {expansion['hubble_parameter_km_s_mpc']:.1f} km/s/Mpc")
        print(f"     Age: {expansion['age_gyr']:.2f} Gyr")
        print(f"     Hubble length: {expansion['hubble_length_mpc']:.0f} Mpc")
        print(f"     Dark energy density: {expansion['dark_energy_density_kg_m3']:.2e} kg/m³")
        print(f"     NRCI: {expansion['nrci']:.10f}")
        print(f"     UBP Energy: {expansion['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: The Universe is Coherence Evolution")
    print("CMB fluctuations are coherence patterns")
    print("Dark energy is coherence pressure")
    print("=" * 80)
