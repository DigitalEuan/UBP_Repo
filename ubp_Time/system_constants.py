"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - System Constants
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

This module defines all fundamental constants used across the UBP Framework
as COHERENCE-NATIVE entities where appropriate.

**Paradigm Shift in 3.5**:
Physical constants remain as floats (they're measured, not computed).
UBP-derived constants become CoherenceStates (they emerge from computation).

This ensures a single, consistent source of truth with proper coherence tracking
for all computed values.

**Zero Dependencies**: Only Python stdlib (math module) + coherence_substrate
"""

import math
from typing import Tuple, Dict
from coherence_substrate import CoherenceState, NRCI_TARGET, Y as Y_RAW, Y_INVERSE as Y_INV_RAW, O_OBSERVER as O_OBS_RAW, PI, GOLDEN_RATIO


# ============================================================================
# UNIVERSAL PHYSICAL CONSTANTS (Measured - remain as floats)
# ============================================================================

class PhysicalConstants:
    """
    Universal physical constants from measurement.
    These are NOT computed, so they remain as floats.
    """
    
    # Fundamental constants
    SPEED_OF_LIGHT: float = 299792458  # m/s
    PLANCK_CONSTANT: float = 6.62607015e-34  # J⋅s
    PLANCK_REDUCED: float = 1.054571817e-34  # J⋅s (ℏ)
    BOLTZMANN_CONSTANT: float = 1.380649e-23  # J/K
    FINE_STRUCTURE_CONSTANT: float = 0.0072973525693  # Dimensionless
    GRAVITATIONAL_CONSTANT: float = 6.67430e-11  # m³⋅kg⁻¹⋅s⁻²
    AVOGADRO_NUMBER: float = 6.02214076e23  # mol⁻¹
    ELEMENTARY_CHARGE: float = 1.602176634e-19  # C
    VACUUM_PERMITTIVITY: float = 8.8541878128e-12  # F/m
    VACUUM_PERMEABILITY: float = 1.25663706212e-6  # H/m
    
    # Particle masses
    ELECTRON_MASS: float = 9.1093837015e-31  # kg
    PROTON_MASS: float = 1.67262192369e-27  # kg
    NEUTRON_MASS: float = 1.67492749804e-27  # kg
    
    # Nuclear constants
    NUCLEAR_MAGNETTON: float = 5.0507837461e-27  # J/T
    PROTON_GYROMAGNETIC: float = 2.6752218744e8  # rad/(s*T)
    NEUTRON_GYROMAGNETIC: float = -1.8324717e8  # rad/(s*T)
    DEUTERON_BINDING_ENERGY: float = 2.224573e6  # eV
    
    # Atomic constants
    RYDBERG_CONSTANT: float = 1.097373156853967e7  # m⁻¹
    
    # Temporal constants
    PLANCK_TIME_SECONDS: float = 5.391247e-44  # Smallest unit of time


# ============================================================================
# MATHEMATICAL CONSTANTS (Pure math - remain as floats)
# ============================================================================

class MathConstants:
    """
    Fundamental mathematical constants.
    These are mathematical truths, not computed values.
    """
    
    PI: float = math.pi  # π
    E: float = math.e  # e (Euler's number)
    PHI: float = (1 + math.sqrt(5)) / 2  # φ (Golden Ratio)
    EULER_MASCHERONI: float = 0.5772156649  # γ


# ============================================================================
# UBP CONSTANTS (Computed - become CoherenceStates)
# ============================================================================

class UBPConstants:
    """
    UBP-specific constants as CoherenceStates.
    
    These constants emerge from UBP computation and carry their own
    coherence quality. This is the foundation of information-first physics.
    """
    
    # --- Y Constant Family (from y_constants module) ---
    # Import from coherence_substrate for consistency
    Y_CONSTANT: CoherenceState = CoherenceState(Y_RAW, log_nrci_error=math.log(1 - NRCI_TARGET))
    Y_INVERSE: CoherenceState = CoherenceState(Y_INV_RAW, log_nrci_error=math.log(1 - NRCI_TARGET))
    Y_M_CONSTANT: CoherenceState = CoherenceState(1.5716125548e-7, log_nrci_error=math.log(1 - NRCI_TARGET))
    Y_FORMULA_N: int = 2  # Binary necessity parameter
    
    # --- Observer Framework (Coherence-Native) ---
    PGCI_TARGET: float = NRCI_TARGET  # 0.999997
    O_OBSERVER: CoherenceState = CoherenceState(O_OBS_RAW, log_nrci_error=math.log(1 - NRCI_TARGET))
    OBSERVER_CONVERGENCE_TOLERANCE: float = 1e-10
    
    # Y_Emergent as CoherenceState
    Y_EMERGENT_VALUE: float = NRCI_TARGET / Y_INV_RAW  # Use raw value from coherence_substrate
    Y_EMERGENT: CoherenceState = CoherenceState(Y_EMERGENT_VALUE, log_nrci_error=math.log(1 - NRCI_TARGET))
    
    # --- Wall of Reality ---
    WALL_OF_REALITY_FREQ: float = 1e12  # 1 THz - frequency limit
    WALL_APPROACH_WARNING: float = 0.9e12  # 90% of limit
    NRCI_COLLAPSE_THRESHOLD: float = 0.1
    
    # --- SOC Energy System ---
    M_META_TEMPORAL: float = math.pi  # Meta-Temporal Primitive
    C_CELERITAS: float = 299792458.0  # Master clock rate
    CU_TO_JOULES_CALIBRATION: float = 1.0  # Placeholder for Planck-scale calibration
    
    # --- Core Resonance Values (CRVs) as CoherenceStates ---
    # These are computed/derived, so they benefit from coherence tracking
    CRV_ELECTROMAGNETIC_BASE: CoherenceState = CoherenceState(
        math.pi, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_QUANTUM_BASE: CoherenceState = CoherenceState(
        math.e / 12, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_GRAVITATIONAL_BASE: CoherenceState = CoherenceState(
        160.19, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_BIOLOGICAL_BASE: CoherenceState = CoherenceState(
        10.0, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_COSMOLOGICAL_BASE: CoherenceState = CoherenceState(
        math.pi ** ((1 + math.sqrt(5)) / 2), log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_NUCLEAR_BASE: CoherenceState = CoherenceState(
        1.2356e20, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_OPTICAL_BASE: CoherenceState = CoherenceState(
        5.0e14, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    CRV_PLASMA_BASE: CoherenceState = CoherenceState(
        2 * math.pi, log_nrci_error=math.log(1 - NRCI_TARGET)
    )
    
    # --- Toggle Algebra & Bitfield Parameters ---
    OFFBIT_DEFAULT_SIZE_BYTES: int = 4
    BITFIELD_DEFAULT_SPARSITY: float = 0.01
    MAX_BITFIELD_DIMENSIONS: int = 6
    
    # --- UBP-specific operational constants ---
    C_INFINITY: float = 1.0e+308
    OFFBIT_ENERGY_UNIT: float = 1.0e-30
    EPSILON_UBP: float = 1e-18
    UBP_ZITTERBEWEGUNG_FREQ: float = 1.2356e20  # Hz
    MAX_PRIME_DEFAULT: int = 282281
    
    # --- OffBit counts for hardware profiles ---
    OFFBITS_4GB_MOBILE: int = 10000
    OFFBITS_RASPBERRY_PI5: int = 100000
    OFFBITS_8GB_IMAC: int = 1000000
    OFFBITS_GOOGLE_COLAB: int = 2500000
    OFFBITS_KAGGLE: int = 2000000
    OFFBITS_HPC: int = 10000000
    OFFBITS_DEVELOPMENT: int = 10000
    
    # --- Bitfield dimension configurations ---
    BITFIELD_6D_FULL: Tuple[int, ...] = (150, 150, 150, 5, 2, 2)
    BITFIELD_6D_MEDIUM: Tuple[int, ...] = (80, 80, 80, 5, 2, 2)
    BITFIELD_6D_SMALL: Tuple[int, ...] = (30, 30, 30, 5, 2, 2)
    
    # --- Harmonic Toggle Resonance (HTR) Parameters ---
    HTR_DEFAULT_THRESHOLD: float = 0.05
    HTR_MAX_ITERATIONS: int = 1000
    HTR_GENETIC_POPULATION_SIZE: int = 50
    HTR_GENETIC_GENERATIONS: int = 100
    
    # --- Error Correction Parameters ---
    NRCI_TARGET_HIGH_COHERENCE: float = 0.999997
    NRCI_TARGET_STANDARD: float = 0.9999
    COHERENCE_THRESHOLD: float = 0.95
    GOLAY_CODE_PARAMS: Tuple[int, int] = (23, 12)
    HAMMING_CODE_PARAMS: Tuple[int, int] = (7, 4)
    BCH_CODE_PARAMS: Tuple[int, int] = (31, 21)
    REED_SOLOMON_DEFAULT_COMPRESSION_RATIO: float = 0.30
    
    # --- Temporal Mechanics (BitTime) ---
    BIT_TIME_UNIT_SECONDS: float = 1e-12  # picoseconds
    COHERENT_SYNCHRONIZATION_CYCLE_SECONDS: float = 1 / math.pi
    TAUTFLUENCE_TIME_SECONDS: float = 2.117e-15
    
    # --- Realm Specific Frequencies ---
    UBP_REALM_FREQUENCIES: Dict[str, float] = {
        'nuclear': 1.2356e20,
        'optical': 5.0e14,
        'quantum': 4.58e14,
        'electromagnetic': math.pi,
        'gravitational': 100.0,
        'biological': 10.0,
        'cosmological': 1e-11,
        'atomic': 4.58e14,
        'plasma': 2 * math.pi,
    }
    
    # --- Performance targets ---
    DEFAULT_TARGET_OPS_PER_SECOND: int = 5000
    DEFAULT_MAX_OPERATION_TIME_SECONDS: float = 1.0
    DEFAULT_VALIDATION_ITERATIONS: int = 1000
    
    # --- Directory naming ---
    DATA_DIR_NAME: str = "data"
    OUTPUT_DIR_NAME: str = "output"
    TEMP_DIR_NAME: str = "temp"
    CACHE_DIR_NAME: str = "cache"
    LOGS_DIR_NAME: str = "logs"
    
    # --- Configuration defaults ---
    UBP_CONFIG_DEFAULT_MEMORY_LIMIT_MB: int = 1000
    UBP_CONFIG_DEFAULT_PARALLEL_PROCESSING: bool = True
    UBP_CONFIG_DEFAULT_GPU_ACCELERATION: bool = False
    UBP_CONFIG_DEFAULT_CACHE_ENABLED: bool = True
    
    # --- UBP frequency weights for global coherence ---
    UBP_FREQUENCY_WEIGHTS: Dict[float, float] = {
        math.pi: 0.2,      # π (electromagnetic)
        (1 + math.sqrt(5)) / 2: 0.2,  # φ (golden ratio)
        4.58e14: 0.35,     # Quantum entanglement frequency
        1e9: 0.1,          # GHz range
        1e15: 0.1,         # Optical range
        1e20: 0.05,        # Zitterbewegung / nuclear frequencies
        58977069.609314: 0.05,  # Composite resonance frequency
    }
    
    # --- UBP toggle probabilities by realm ---
    UBP_TOGGLE_PROBABILITIES: Dict[str, float] = {
        'quantum': math.e / 12,
        'cosmological': math.pi ** ((1 + math.sqrt(5)) / 2),
        'electromagnetic': math.pi / 4,
        'gravitational': 1.0 / math.pi,
        'biological': 1.0 / math.e,
        'nuclear': 1.0 / ((1 + math.sqrt(5)) / 2),
        'optical': 1.0 / math.sqrt(2),
        'atomic': math.e / 12,
        'plasma': math.pi / 4,
    }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_crv_for_realm(realm_name: str) -> CoherenceState:
    """
    Get the Core Resonance Value for a specific realm as a CoherenceState.
    
    Args:
        realm_name: Name of the realm (e.g., 'quantum', 'gravitational')
        
    Returns:
        CRV as CoherenceState
        
    Example:
        >>> crv = get_crv_for_realm('quantum')
        >>> print(f"Quantum CRV: {crv.value:.6e}, NRCI: {crv.nrci:.6f}")
    """
    realm_name = realm_name.lower()
    
    crv_map = {
        'electromagnetic': UBPConstants.CRV_ELECTROMAGNETIC_BASE,
        'quantum': UBPConstants.CRV_QUANTUM_BASE,
        'gravitational': UBPConstants.CRV_GRAVITATIONAL_BASE,
        'biological': UBPConstants.CRV_BIOLOGICAL_BASE,
        'cosmological': UBPConstants.CRV_COSMOLOGICAL_BASE,
        'nuclear': UBPConstants.CRV_NUCLEAR_BASE,
        'optical': UBPConstants.CRV_OPTICAL_BASE,
        'plasma': UBPConstants.CRV_PLASMA_BASE,
        'atomic': UBPConstants.CRV_QUANTUM_BASE,  # Atomic uses quantum CRV
    }
    
    if realm_name not in crv_map:
        # Default to electromagnetic
        return UBPConstants.CRV_ELECTROMAGNETIC_BASE
    
    return crv_map[realm_name]


def get_realm_frequency(realm_name: str) -> float:
    """
    Get the characteristic frequency for a specific realm.
    
    Args:
        realm_name: Name of the realm
        
    Returns:
        Characteristic frequency in Hz
        
    Example:
        >>> freq = get_realm_frequency('optical')
        >>> print(f"Optical frequency: {freq:.2e} Hz")
    """
    realm_name = realm_name.lower()
    return UBPConstants.UBP_REALM_FREQUENCIES.get(realm_name, math.pi)


def get_toggle_probability(realm_name: str) -> float:
    """
    Get the toggle probability for a specific realm.
    
    Args:
        realm_name: Name of the realm
        
    Returns:
        Toggle probability (0 to 1)
        
    Example:
        >>> prob = get_toggle_probability('quantum')
        >>> print(f"Quantum toggle probability: {prob:.6f}")
    """
    realm_name = realm_name.lower()
    return UBPConstants.UBP_TOGGLE_PROBABILITIES.get(realm_name, 0.5)


def validate_system_constants() -> Dict[str, bool]:
    """
    Validate that all UBP constants are properly initialized.
    
    Returns:
        Dictionary of validation results
        
    Example:
        >>> results = validate_system_constants()
        >>> print(f"All validations passed: {all(results.values())}")
    """
    results = {}
    
    # Validate Y constants are CoherenceStates
    results['Y_CONSTANT_IS_COHERENCE'] = isinstance(UBPConstants.Y_CONSTANT, CoherenceState)
    results['Y_INVERSE_IS_COHERENCE'] = isinstance(UBPConstants.Y_INVERSE, CoherenceState)
    results['O_OBSERVER_IS_COHERENCE'] = isinstance(UBPConstants.O_OBSERVER, CoherenceState)
    
    # Validate Y constants have high NRCI
    results['Y_CONSTANT_COHERENT'] = UBPConstants.Y_CONSTANT.nrci > 0.999
    results['Y_INVERSE_COHERENT'] = UBPConstants.Y_INVERSE.nrci > 0.999
    results['O_OBSERVER_COHERENT'] = UBPConstants.O_OBSERVER.nrci > 0.999
    
    # Validate CRVs are CoherenceStates
    results['CRV_QUANTUM_IS_COHERENCE'] = isinstance(UBPConstants.CRV_QUANTUM_BASE, CoherenceState)
    results['CRV_GRAVITATIONAL_IS_COHERENCE'] = isinstance(UBPConstants.CRV_GRAVITATIONAL_BASE, CoherenceState)
    
    # Validate inverse relationship
    y_times_y_inv = UBPConstants.Y_CONSTANT.value * UBPConstants.Y_INVERSE.value
    results['Y_INVERSE_RELATIONSHIP'] = abs(y_times_y_inv - 1.0) < 1e-10
    
    # Validate O_observer equals Y_INVERSE
    results['O_OBSERVER_EQUALS_Y_INVERSE'] = abs(
        UBPConstants.O_OBSERVER.value - UBPConstants.Y_INVERSE.value
    ) < 1e-10
    
    return results


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 SYSTEM CONSTANTS - Coherence-Native Implementation")
    print("=" * 80)
    
    print("\n1. Physical Constants (measured - remain as floats):")
    print(f"   Speed of Light: {PhysicalConstants.SPEED_OF_LIGHT:.0f} m/s")
    print(f"   Planck Constant: {PhysicalConstants.PLANCK_CONSTANT:.6e} J⋅s")
    print(f"   Gravitational Constant: {PhysicalConstants.GRAVITATIONAL_CONSTANT:.6e} m³⋅kg⁻¹⋅s⁻²")
    
    print("\n2. Mathematical Constants (pure math - remain as floats):")
    print(f"   π: {MathConstants.PI:.15f}")
    print(f"   e: {MathConstants.E:.15f}")
    print(f"   φ: {MathConstants.PHI:.15f}")
    
    print("\n3. UBP Constants (computed - become CoherenceStates):")
    print(f"   Y: {UBPConstants.Y_CONSTANT.value:.15f}, NRCI: {UBPConstants.Y_CONSTANT.nrci:.10f}")
    print(f"   1/Y: {UBPConstants.Y_INVERSE.value:.15f}, NRCI: {UBPConstants.Y_INVERSE.nrci:.10f}")
    print(f"   O_observer: {UBPConstants.O_OBSERVER.value:.15f}, NRCI: {UBPConstants.O_OBSERVER.nrci:.10f}")
    print(f"   Y_Emergent: {UBPConstants.Y_EMERGENT.value:.15f}, NRCI: {UBPConstants.Y_EMERGENT.nrci:.10f}")
    
    print("\n4. Core Resonance Values (as CoherenceStates):")
    print(f"   Quantum CRV: {UBPConstants.CRV_QUANTUM_BASE.value:.6e}, NRCI: {UBPConstants.CRV_QUANTUM_BASE.nrci:.6f}")
    print(f"   Gravitational CRV: {UBPConstants.CRV_GRAVITATIONAL_BASE.value:.6e}, NRCI: {UBPConstants.CRV_GRAVITATIONAL_BASE.nrci:.6f}")
    print(f"   Optical CRV: {UBPConstants.CRV_OPTICAL_BASE.value:.6e}, NRCI: {UBPConstants.CRV_OPTICAL_BASE.nrci:.6f}")
    
    print("\n5. System Validation:")
    validations = validate_system_constants()
    all_passed = all(validations.values())
    for key, passed in validations.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"   {key}: {status}")
    
    print(f"\n{'='*80}")
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("UBP 3.5 System Constants: Coherence-Native, Zero Dependencies")
    else:
        print("✗ SOME VALIDATIONS FAILED - Check configuration")
    print(f"{'='*80}")
