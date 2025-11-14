"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Atomic Realm
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Atomic realm as coherence dynamics.

**Paradigm Shift in 3.5**:
Atomic spectra are coherence resonances. Electron orbitals are coherence
configurations. Chemical bonds are coherence couplings.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.5
"""

import math
from typing import Dict
from dataclasses import dataclass

from coherence_substrate import CoherenceState, NRCI_TARGET
from system_constants import PhysicalConstants, get_crv_for_realm
from energy_dual import EnergyCalculator


# ============================================================================
# ATOMIC STATE
# ============================================================================

@dataclass
class AtomicState:
    """
    Atomic system state in UBP 3.5.
    """
    coherence: CoherenceState
    frequency: float
    wavelength: float
    energy_ev: float
    quantum_numbers: Dict[str, int]
    
    @property
    def nrci(self) -> float:
        """NRCI of this atomic state."""
        return self.coherence.nrci


# ============================================================================
# ATOMIC REALM CALCULATOR
# ============================================================================

class AtomicRealm:
    """
    Atomic realm calculator for UBP 3.5.
    
    Atomic spectra are coherence resonances.
    """
    
    # Realm constants
    REALM_NAME = "atomic"
    
    # Physical constants
    RYDBERG_CONSTANT = 1.0973731568160e7  # m^-1
    PLANCK_CONSTANT = PhysicalConstants.PLANCK_CONSTANT
    SPEED_OF_LIGHT = PhysicalConstants.SPEED_OF_LIGHT
    BOHR_RADIUS = 5.29177210903e-11  # m
    
    def __init__(self):
        """Initialize atomic realm calculator."""
        self.energy_calc = EnergyCalculator()
        self.crv = get_crv_for_realm(self.REALM_NAME)
    
    def calculate_atomic_energy(
        self,
        atomic_state: AtomicState
    ) -> Dict[str, any]:
        """
        Calculate atomic energy.
        
        Args:
            atomic_state: AtomicState to calculate
            
        Returns:
            Dictionary with energy results
        """
        # Modal sum from atomic properties
        modal_sum = self._calculate_modal_sum(atomic_state)
        
        # Calculate energy
        energy_result = self.energy_calc.calculate(
            modal_sum=modal_sum,
            realm=self.REALM_NAME,
            frequency=atomic_state.frequency
        )
        
        return {
            'energy_cu': energy_result.energy_cu,
            'energy_joules': energy_result.energy_joules,
            'nrci': energy_result.nrci,
            'atomic_nrci': atomic_state.nrci,
            'frequency': atomic_state.frequency,
            'wavelength': atomic_state.wavelength,
            'energy_ev': atomic_state.energy_ev
        }
    
    def _calculate_modal_sum(self, state: AtomicState) -> float:
        """
        Calculate modal sum from atomic state.
        """
        # Energy contribution (log scale for eV range)
        energy_contrib = math.log10(state.energy_ev + 1) / 3.0
        
        # Frequency contribution
        freq_contrib = math.log10(state.frequency + 1) / 18.0
        
        # Quantum number contribution
        n_sum = sum(state.quantum_numbers.values())
        quantum_contrib = math.log10(n_sum + 1) / 2.0
        
        # Coherence contribution
        coherence_contrib = state.coherence.nrci
        
        modal_sum = (
            energy_contrib * 
            freq_contrib * 
            (1.0 + quantum_contrib) *
            coherence_contrib
        )
        
        return max(modal_sum, 1e-10)
    
    def model_hydrogen_spectrum(
        self,
        n_initial: int = 3,
        n_final: int = 2,
        series_name: str = "Balmer"
    ) -> Dict[str, float]:
        """
        Model hydrogen spectral lines (Rydberg formula).
        
        Real data: Balmer series (visible light from hydrogen)
        
        Args:
            n_initial: Initial quantum number
            n_final: Final quantum number
            series_name: Series name (Lyman, Balmer, Paschen, etc.)
            
        Returns:
            Dictionary with spectral line analysis
            
        Example:
            >>> realm = AtomicRealm()
            >>> balmer_alpha = realm.model_hydrogen_spectrum(3, 2, "Balmer")
            >>> print(f"Wavelength: {balmer_alpha['wavelength_nm']:.1f} nm")
        """
        if n_initial <= n_final:
            raise ValueError("n_initial must be > n_final")
        
        # Rydberg formula: 1/λ = R_H * (1/n_f² - 1/n_i²)
        inv_wavelength = self.RYDBERG_CONSTANT * (
            1.0 / (n_final ** 2) - 1.0 / (n_initial ** 2)
        )
        
        wavelength = 1.0 / inv_wavelength  # meters
        frequency = self.SPEED_OF_LIGHT / wavelength  # Hz
        
        # Energy in eV
        energy_j = self.PLANCK_CONSTANT * frequency
        energy_ev = energy_j / PhysicalConstants.ELEMENTARY_CHARGE
        
        # Coherence (spectral lines are highly coherent)
        coherence_level = 0.999
        
        # Create atomic state
        coherence = CoherenceState(
            energy_ev,
            log_nrci_error=math.log(1 - coherence_level * NRCI_TARGET)
        )
        
        atomic_state = AtomicState(
            coherence=coherence,
            frequency=frequency,
            wavelength=wavelength,
            energy_ev=energy_ev,
            quantum_numbers={'n_initial': n_initial, 'n_final': n_final}
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_atomic_energy(atomic_state)
        
        # Determine color (for visible spectrum)
        color = self._wavelength_to_color(wavelength * 1e9)  # nm
        
        return {
            'series_name': series_name,
            'n_initial': n_initial,
            'n_final': n_final,
            'wavelength_m': wavelength,
            'wavelength_nm': wavelength * 1e9,
            'frequency_hz': frequency,
            'frequency_thz': frequency / 1e12,
            'energy_ev': energy_ev,
            'energy_joules': energy_j,
            'color': color,
            'coherence': coherence_level,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
        }
    
    def _wavelength_to_color(self, wavelength_nm: float) -> str:
        """Determine color from wavelength."""
        if wavelength_nm < 380:
            return "Ultraviolet"
        elif wavelength_nm < 450:
            return "Violet"
        elif wavelength_nm < 495:
            return "Blue"
        elif wavelength_nm < 570:
            return "Green"
        elif wavelength_nm < 590:
            return "Yellow"
        elif wavelength_nm < 620:
            return "Orange"
        elif wavelength_nm < 750:
            return "Red"
        else:
            return "Infrared"
    
    def model_molecular_vibration(
        self,
        molecule: str = "CO2",
        mode: str = "symmetric_stretch",
        temperature_k: float = 300.0
    ) -> Dict[str, float]:
        """
        Model molecular vibrational modes.
        
        Real data: CO₂ IR spectroscopy
        
        Args:
            molecule: Molecule name
            mode: Vibrational mode
            temperature_k: Temperature (K)
            
        Returns:
            Dictionary with vibrational analysis
            
        Example:
            >>> realm = AtomicRealm()
            >>> co2_vib = realm.model_molecular_vibration("CO2", "symmetric_stretch")
            >>> print(f"Frequency: {co2_vib['frequency_thz']:.2f} THz")
        """
        # CO₂ vibrational frequencies (experimental values)
        co2_modes = {
            'symmetric_stretch': 1388.0e9,  # Hz (1388 cm^-1)
            'bending': 667.0e9,              # Hz (667 cm^-1)
            'asymmetric_stretch': 2349.0e9   # Hz (2349 cm^-1)
        }
        
        if molecule != "CO2":
            # Default to CO2 for now
            frequency = co2_modes.get(mode, 1388.0e9)
        else:
            frequency = co2_modes.get(mode, 1388.0e9)
        
        # Wavelength
        wavelength = self.SPEED_OF_LIGHT / frequency
        
        # Energy
        energy_j = self.PLANCK_CONSTANT * frequency
        energy_ev = energy_j / PhysicalConstants.ELEMENTARY_CHARGE
        
        # Thermal population (Boltzmann factor)
        k_B = PhysicalConstants.BOLTZMANN_CONSTANT
        thermal_factor = math.exp(-energy_j / (k_B * temperature_k))
        
        # Coherence (molecular vibrations are moderately coherent)
        coherence_level = 0.8 * thermal_factor
        
        # Create atomic state
        coherence = CoherenceState(
            energy_ev,
            log_nrci_error=math.log(1 - coherence_level * NRCI_TARGET)
        )
        
        atomic_state = AtomicState(
            coherence=coherence,
            frequency=frequency,
            wavelength=wavelength,
            energy_ev=energy_ev,
            quantum_numbers={'v': 1}  # First excited state
        )
        
        # Calculate UBP energy
        energy_result = self.calculate_atomic_energy(atomic_state)
        
        return {
            'molecule': molecule,
            'mode': mode,
            'temperature_k': temperature_k,
            'frequency_hz': frequency,
            'frequency_thz': frequency / 1e12,
            'wavelength_um': wavelength * 1e6,
            'energy_ev': energy_ev,
            'thermal_population': thermal_factor,
            'coherence': coherence_level,
            'nrci': energy_result['nrci'],
            'ubp_energy_cu': energy_result['energy_cu']
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 ATOMIC REALM - Atomic Spectra as Coherence Resonances")
    print("=" * 80)
    
    # Create realm
    print("\n1. Creating Atomic Realm:")
    realm = AtomicRealm()
    print(f"   Realm: {realm.REALM_NAME}")
    print(f"   CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
    
    # Hydrogen Balmer series
    print("\n2. Hydrogen Balmer Series (Visible Spectral Lines):")
    transitions = [(3, 2, "H-alpha"), (4, 2, "H-beta"), (5, 2, "H-gamma")]
    
    for n_i, n_f, name in transitions:
        result = realm.model_hydrogen_spectrum(n_i, n_f, "Balmer")
        print(f"\n   {name} (n={n_i}→{n_f}):")
        print(f"     Wavelength: {result['wavelength_nm']:.1f} nm")
        print(f"     Color: {result['color']}")
        print(f"     Energy: {result['energy_ev']:.3f} eV")
        print(f"     Frequency: {result['frequency_thz']:.2f} THz")
        print(f"     NRCI: {result['nrci']:.10f}")
        print(f"     UBP Energy: {result['ubp_energy_cu']:.6e} CU")
    
    # CO₂ molecular vibrations
    print("\n3. CO₂ Molecular Vibrations (IR Spectroscopy):")
    modes = ['symmetric_stretch', 'bending', 'asymmetric_stretch']
    
    for mode in modes:
        result = realm.model_molecular_vibration("CO2", mode, temperature_k=300.0)
        print(f"\n   {mode}:")
        print(f"     Frequency: {result['frequency_thz']:.2f} THz")
        print(f"     Wavelength: {result['wavelength_um']:.2f} μm")
        print(f"     Energy: {result['energy_ev']:.4f} eV")
        print(f"     Thermal population: {result['thermal_population']:.4f}")
        print(f"     NRCI: {result['nrci']:.10f}")
        print(f"     UBP Energy: {result['ubp_energy_cu']:.6e} CU")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Atomic Spectra are Coherence Resonances")
    print("Electron orbitals are coherence configurations")
    print("Chemical bonds are coherence couplings")
    print("=" * 80)
