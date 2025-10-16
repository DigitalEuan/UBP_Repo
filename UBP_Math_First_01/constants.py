"""
UBP Constants Loader

Loads and provides access to all UBP constants from the spec/core.yaml file.
This module ensures a single source of truth for all numerical constants.
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


def load_constants(spec_path: str = None) -> Dict[str, Any]:
    """
    Load UBP constants from the core specification file.
    
    Args:
        spec_path: Optional path to the spec directory. If None, uses default location.
        
    Returns:
        Dictionary containing all UBP constants and parameters
    """
    if spec_path is None:
        # Default to spec directory relative to this file
        current_dir = Path(__file__).parent
        spec_path = current_dir.parent / "spec" / "core.yaml"
    
    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"UBP spec file not found: {spec_path}")
    
    with open(spec_path, 'r') as f:
        constants = yaml.safe_load(f)
    
    return constants


# Global constants instance - loaded once when module is imported
_CONSTANTS = None

def get_constants() -> Dict[str, Any]:
    """Get the global constants instance, loading if necessary."""
    global _CONSTANTS
    if _CONSTANTS is None:
        _CONSTANTS = load_constants()
    return _CONSTANTS


# Convenience functions for accessing specific constant categories
def get_fundamental_constants() -> Dict[str, float]:
    """Get fundamental mathematical constants (π, φ, e, c)."""
    return get_constants()["fundamental_constants"]


def get_system_constants() -> Dict[str, float]:
    """Get UBP system constants (bit_time, csc_time, etc.)."""
    return get_constants()["system_constants"]


def get_energy_constants() -> Dict[str, Any]:
    """Get energy equation parameters."""
    return get_constants()["energy_equation"]


def get_realm_constants(realm_name: str) -> Dict[str, Any]:
    """
    Get constants for a specific realm.
    
    Args:
        realm_name: Name of the realm (quantum, electromagnetic, etc.)
        
    Returns:
        Dictionary of realm-specific constants
        
    Raises:
        KeyError: If realm_name is not found
    """
    realms = get_constants()["realms"]
    if realm_name not in realms:
        available = list(realms.keys())
        raise KeyError(f"Realm '{realm_name}' not found. Available realms: {available}")
    
    return realms[realm_name]


def get_toggle_operations() -> Dict[str, Any]:
    """Get toggle algebra operation definitions."""
    return get_constants()["toggle_operations"]


def get_metrics_constants() -> Dict[str, Any]:
    """Get coherence and validation metric constants."""
    return get_constants()["metrics"]


def get_bitfield_config() -> Dict[str, Any]:
    """Get bitfield configuration parameters."""
    return get_constants()["bitfield"]


def get_hardware_profile(profile_name: str) -> Dict[str, Any]:
    """
    Get hardware-specific configuration.
    
    Args:
        profile_name: Hardware profile (desktop_8gb, mobile_4gb, raspberry_pi)
        
    Returns:
        Dictionary of hardware-specific parameters
    """
    profiles = get_constants()["hardware_profiles"]
    if profile_name not in profiles:
        available = list(profiles.keys())
        raise KeyError(f"Hardware profile '{profile_name}' not found. Available: {available}")
    
    return profiles[profile_name]


# Pre-computed derived constants for performance
class UBPConstants:
    """
    Convenience class providing direct access to commonly used constants.
    All values are loaded from the spec file to maintain single source of truth.
    """
    
    def __init__(self):
        fund = get_fundamental_constants()
        sys = get_system_constants()
        energy = get_energy_constants()
        
        # Fundamental constants
        self.PI = fund["pi"]
        self.PHI = fund["phi"]
        self.E = fund["e"]
        self.C = fund["c"]
        self.PLANCK_TIME = fund["planck_time"]
        
        # System constants
        self.BIT_TIME = sys["bit_time"]
        self.CSC_TIME = sys["csc_time"]
        self.CSC_FREQUENCY = sys["csc_frequency"]
        
        # Energy equation constants
        self.R_SPECIFIC = energy["R_specific"]
        self.S_OPT_DEFAULT = energy["S_opt_default"]
        self.P_GCI_SPECIFIC = energy["P_GCI_specific"]
        self.O_NEUTRAL = energy["O_neutral"]
        self.O_INTENTIONAL = energy["O_intentional"]
        self.C_INFINITY = energy["c_infinity"]
        self.I_SPIN_DEFAULT = energy["I_spin_default"]
        self.W_IJ_DEFAULT = energy["w_ij_default"]
        
        # Derived constants
        self.QUANTUM_CRV = fund["e"] / 12  # e/12 ≈ 0.2265234857
        self.COSMOLOGICAL_CRV = self.PI ** self.PHI  # π^φ ≈ 0.83203682


# Global constants instance
CONSTANTS = UBPConstants()


# Export commonly used constants at module level for convenience
PI = CONSTANTS.PI
PHI = CONSTANTS.PHI
E = CONSTANTS.E
EULER_E = CONSTANTS.E  # Alias for clarity
C = CONSTANTS.C
BIT_TIME = CONSTANTS.BIT_TIME
CSC_TIME = CONSTANTS.CSC_TIME
R_SPEC = CONSTANTS.R_SPECIFIC
S_OPT_SPEC = CONSTANTS.S_OPT_DEFAULT
P_GCI_SPEC = CONSTANTS.P_GCI_SPECIFIC
C_INFINITY = CONSTANTS.C_INFINITY




def get_frequency_weights() -> Dict[float, float]:
    """
    Get frequency weights for Global Coherence Invariant calculation.
    
    Returns:
        Dictionary mapping frequencies to weights
    """
    return {
        3.141593: 0.2,           # π (electromagnetic)
        1.618034: 0.2,           # φ (golden ratio)
        4.58e14: 0.3,            # Quantum frequency
        1e9: 0.05,               # GHz range
        1e15: 0.05,              # Optical range
        1e20: 0.05,              # Nuclear range
        58977069.609314: 0.05,   # Specific resonance
        1.86e41: 0.05            # Cosmological scale
    }

