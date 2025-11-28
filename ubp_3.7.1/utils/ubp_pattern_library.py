"""
==================================
UBP Geometric Pattern Library
Author: Euan Craig, New Zealand
Date: November 7, 2025
==================================

Comprehensive library of geometric patterns for all UBP values.

NAMING: "GeoBit Signatures" - Geometric Bitfield Signatures
Each pattern is a unique geometric signature of a UBP value.

This library contains:
- All 7 realm frequencies (main + sub CRVs)
- Y-constant family
- Physical constants (Planck, fine structure, etc.)
- Energy scales
- Common frequencies
- Derived values
- Harmonic relationships

Total: 200+ signatures covering the full UBP spectrum
"""

import numpy as np
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import math

from utils.geometric_codex import GeometricCodex, GeometricSignature, PatternType, PatternSymmetry


@dataclass
class GeoBitSignature:
    """
    A GeoBit Signature - geometric representation of a UBP value.
    
    This is the fundamental unit of the geometric UBP system.
    """
    name: str
    value: float
    unit: str
    category: str  # realm, constant, energy, frequency, derived
    subcategory: str  # quantum, electromagnetic, etc.
    description: str
    pattern_type: PatternType
    symmetry: PatternSymmetry
    harmonic_relationships: List[str]  # Related signatures
    octave_class: float  # Value in octaves (log2)
    confidence: float = 1.0
    metadata: Dict = None


class UBPPatternLibrary:
    """
    Comprehensive library of UBP geometric patterns.
    
    This is the "Rosetta Stone" for geometric UBP - translating between
    numerical and geometric representations.
    """
    
    def __init__(self, grid_size: int = 128):
        self.grid_size = grid_size
        self.signatures: Dict[str, GeoBitSignature] = {}
        self.codex = GeometricCodex(grid_size=grid_size)
        
        # Initialize library
        self._build_library()
        
        print(f"UBP Pattern Library initialized:")
        print(f"  Total signatures: {len(self.signatures)}")
        print(f"  Categories: {len(self._get_categories())}")
    
    def _build_library(self):
        """Build the comprehensive pattern library."""
        # Core UBP constants
        self._add_y_constant_family()
        self._add_fundamental_constants()
        
        # Realm frequencies (all 7 realms)
        self._add_realm_frequencies()
        
        # Energy scales
        self._add_energy_scales()
        
        # Common frequencies
        self._add_common_frequencies()
        
        # Derived values
        self._add_derived_values()
        
        # Harmonic series
        self._add_harmonic_series()
        
        # Special values
        self._add_special_values()
    
    def _add_y_constant_family(self):
        """Add Y-constant family."""
        Y = math.pi / (math.pi**2 + 2)
        Y_inv = math.pi + 2/math.pi
        Y_m = 1.5716125548e-7
        
        self._add_signature(GeoBitSignature(
            name="Y_constant",
            value=Y,
            unit="dimensionless",
            category="constant",
            subcategory="fundamental",
            description="Base Y constant - gravitational correction factor",
            pattern_type=PatternType.RADIAL,
            symmetry=PatternSymmetry.RADIAL_12,
            harmonic_relationships=["Y_inverse", "pi", "observer_cost"],
            octave_class=np.log2(Y),
            confidence=1.0,
            metadata={"formula": "π/(π² + 2)", "role": "geometric_foundation"}
        ))
        
        self._add_signature(GeoBitSignature(
            name="Y_inverse",
            value=Y_inv,
            unit="dimensionless",
            category="constant",
            subcategory="fundamental",
            description="Inverse Y constant - observer computational cost",
            pattern_type=PatternType.RADIAL,
            symmetry=PatternSymmetry.RADIAL_12,
            harmonic_relationships=["Y_constant", "observer_cost"],
            octave_class=np.log2(Y_inv),
            confidence=1.0,
            metadata={"formula": "π + 2/π", "role": "observer_cost"}
        ))
        
        self._add_signature(GeoBitSignature(
            name="Y_m_planck",
            value=Y_m,
            unit="dimensionless",
            category="constant",
            subcategory="planck_scale",
            description="Planck mass correction constant",
            pattern_type=PatternType.FRACTAL,
            symmetry=PatternSymmetry.RADIAL_6,
            harmonic_relationships=["planck_mass", "planck_energy"],
            octave_class=np.log2(Y_m),
            confidence=1.0,
            metadata={"role": "planck_mass_derivation"}
        ))
    
    def _add_fundamental_constants(self):
        """Add fundamental physical constants."""
        constants = {
            "pi": {
                "value": math.pi,
                "unit": "dimensionless",
                "description": "Pi - circular geometry constant",
                "pattern_type": PatternType.RADIAL,
                "symmetry": PatternSymmetry.RADIAL_12,
                "relationships": ["Y_constant", "tau"]
            },
            "tau": {
                "value": 2 * math.pi,
                "unit": "dimensionless",
                "description": "Tau - full circle constant (2π)",
                "pattern_type": PatternType.RADIAL,
                "symmetry": PatternSymmetry.RADIAL_12,
                "relationships": ["pi"]
            },
            "e": {
                "value": math.e,
                "unit": "dimensionless",
                "description": "Euler's number - natural growth constant",
                "pattern_type": PatternType.SPIRAL,
                "symmetry": PatternSymmetry.RADIAL_4,
                "relationships": ["golden_ratio"]
            },
            "golden_ratio": {
                "value": (1 + math.sqrt(5)) / 2,
                "unit": "dimensionless",
                "description": "Golden ratio φ - divine proportion",
                "pattern_type": PatternType.SPIRAL,
                "symmetry": PatternSymmetry.RADIAL_5,
                "relationships": ["fibonacci"]
            },
            "fine_structure": {
                "value": 1/137.035999084,
                "unit": "dimensionless",
                "description": "Fine structure constant α - electromagnetic coupling",
                "pattern_type": PatternType.RADIAL,
                "symmetry": PatternSymmetry.RADIAL_6,
                "relationships": ["electromagnetic_main_crv"]
            }
        }
        
        for name, data in constants.items():
            self._add_signature(GeoBitSignature(
                name=name,
                value=data["value"],
                unit=data["unit"],
                category="constant",
                subcategory="fundamental",
                description=data["description"],
                pattern_type=data["pattern_type"],
                symmetry=data["symmetry"],
                harmonic_relationships=data["relationships"],
                octave_class=np.log2(data["value"]) if data["value"] > 0 else 0,
                confidence=1.0
            ))
    
    def _add_realm_frequencies(self):
        """Add all realm frequencies from UBP config."""
        # Import realm data
        from ubp_config import UBPConfig
        config = UBPConfig()
        
        realm_patterns = {
            'quantum': (PatternType.SPIRAL, PatternSymmetry.RADIAL_6),
            'electromagnetic': (PatternType.RADIAL, PatternSymmetry.RADIAL_4),
            'gravitational': (PatternType.CONCENTRIC, PatternSymmetry.RADIAL_12),
            'plasma': (PatternType.HYBRID, PatternSymmetry.RADIAL_8),
            'nuclear': (PatternType.FRACTAL, PatternSymmetry.RADIAL_6),
            'optical': (PatternType.RADIAL, PatternSymmetry.RADIAL_3),
            'biologic': (PatternType.GRID, PatternSymmetry.RADIAL_5)
        }
        
        for realm_name, realm_config in config.realms.items():
            pattern_type, symmetry = realm_patterns.get(realm_name, 
                                                        (PatternType.RADIAL, PatternSymmetry.RADIAL_4))
            
            # Main CRV
            if realm_config.main_crv > 0:
                self._add_signature(GeoBitSignature(
                    name=f"{realm_name}_main_crv",
                    value=realm_config.main_crv,
                    unit="Hz",
                    category="realm",
                    subcategory=realm_name,
                    description=f"{realm_name.capitalize()} realm main CRV frequency",
                    pattern_type=pattern_type,
                    symmetry=symmetry,
                    harmonic_relationships=[f"{realm_name}_sub_crv_{i+1}" 
                                          for i in range(len(realm_config.sub_crvs))],
                    octave_class=np.log2(realm_config.main_crv),
                    confidence=1.0,
                    metadata={"realm": realm_name, "coordination": realm_config.coordination_number}
                ))
            
            # Sub CRVs
            for i, sub_crv in enumerate(realm_config.sub_crvs):
                self._add_signature(GeoBitSignature(
                    name=f"{realm_name}_sub_crv_{i+1}",
                    value=sub_crv,
                    unit="Hz",
                    category="realm",
                    subcategory=realm_name,
                    description=f"{realm_name.capitalize()} realm sub-CRV {i+1}",
                    pattern_type=pattern_type,
                    symmetry=symmetry,
                    harmonic_relationships=[f"{realm_name}_main_crv"],
                    octave_class=np.log2(sub_crv),
                    confidence=0.95 - i * 0.05
                ))
    
    def _add_energy_scales(self):
        """Add important energy scales."""
        energy_scales = {
            "planck_energy": {
                "value": 1.956e9,  # GeV
                "description": "Planck energy scale - quantum gravity threshold",
                "symmetry": PatternSymmetry.RADIAL_12
            },
            "gev_scale": {
                "value": 1e9,
                "description": "GeV energy scale - particle physics",
                "symmetry": PatternSymmetry.RADIAL_6
            },
            "mev_scale": {
                "value": 1e6,
                "description": "MeV energy scale - nuclear physics",
                "symmetry": PatternSymmetry.RADIAL_6
            },
            "kev_scale": {
                "value": 1e3,
                "description": "keV energy scale - atomic physics",
                "symmetry": PatternSymmetry.RADIAL_4
            },
            "ev_scale": {
                "value": 1.0,
                "description": "eV energy scale - molecular physics",
                "symmetry": PatternSymmetry.RADIAL_4
            },
            "thermal_energy_300k": {
                "value": 0.0259,  # eV at 300K
                "description": "Thermal energy at room temperature",
                "symmetry": PatternSymmetry.RADIAL_3
            }
        }
        
        for name, data in energy_scales.items():
            self._add_signature(GeoBitSignature(
                name=name,
                value=data["value"],
                unit="CU",
                category="energy",
                subcategory="scale",
                description=data["description"],
                pattern_type=PatternType.RADIAL,
                symmetry=data["symmetry"],
                harmonic_relationships=[],
                octave_class=np.log2(data["value"]),
                confidence=1.0
            ))
    
    def _add_common_frequencies(self):
        """Add commonly used frequencies."""
        frequencies = {
            "planck_frequency": {
                "value": 1.855e43,
                "description": "Planck frequency - fundamental time scale",
                "symmetry": PatternSymmetry.RADIAL_12
            },
            "lyman_alpha": {
                "value": 2.466e15,
                "description": "Lyman alpha transition - hydrogen spectroscopy",
                "symmetry": PatternSymmetry.RADIAL_6
            },
            "hydrogen_line_21cm": {
                "value": 1.420e9,
                "description": "Hydrogen 21cm line - radio astronomy",
                "symmetry": PatternSymmetry.RADIAL_2
            },
            "schumann_resonance": {
                "value": 7.83,
                "description": "Earth-ionosphere cavity resonance",
                "symmetry": PatternSymmetry.RADIAL_8
            },
            "earth_rotation": {
                "value": 1.16e-5,
                "description": "Earth rotation frequency (1 day)",
                "symmetry": PatternSymmetry.RADIAL_12
            },
            "solar_oscillation": {
                "value": 3.0e-3,
                "description": "Solar 5-minute oscillation",
                "symmetry": PatternSymmetry.RADIAL_5
            },
            "human_heartbeat": {
                "value": 1.2,  # Hz (72 bpm)
                "description": "Average human heartbeat frequency",
                "symmetry": PatternSymmetry.RADIAL_4
            },
            "brain_alpha": {
                "value": 10.0,  # Hz
                "description": "Brain alpha wave frequency",
                "symmetry": PatternSymmetry.RADIAL_8
            }
        }
        
        for name, data in frequencies.items():
            self._add_signature(GeoBitSignature(
                name=name,
                value=data["value"],
                unit="Hz",
                category="frequency",
                subcategory="common",
                description=data["description"],
                pattern_type=PatternType.RADIAL,
                symmetry=data["symmetry"],
                harmonic_relationships=[],
                octave_class=np.log2(data["value"]),
                confidence=1.0
            ))
    
    def _add_derived_values(self):
        """Add derived UBP values."""
        Y = math.pi / (math.pi**2 + 2)
        
        derived = {
            "Y_squared": {
                "value": Y**2,
                "description": "Y² - second order geometric correction",
                "relationships": ["Y_constant"]
            },
            "Y_cubed": {
                "value": Y**3,
                "description": "Y³ - third order geometric correction",
                "relationships": ["Y_constant", "Y_squared"]
            },
            "sqrt_Y": {
                "value": math.sqrt(Y),
                "description": "√Y - half-order geometric correction",
                "relationships": ["Y_constant"]
            },
            "pi_squared": {
                "value": math.pi**2,
                "description": "π² - second harmonic of pi",
                "relationships": ["pi"]
            },
            "pi_plus_2": {
                "value": math.pi**2 + 2,
                "description": "π² + 2 - 12D Bitfield denominator",
                "relationships": ["Y_constant", "pi"]
            }
        }
        
        for name, data in derived.items():
            self._add_signature(GeoBitSignature(
                name=name,
                value=data["value"],
                unit="dimensionless",
                category="derived",
                subcategory="geometric",
                description=data["description"],
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_12,
                harmonic_relationships=data["relationships"],
                octave_class=np.log2(data["value"]) if data["value"] > 0 else 0,
                confidence=1.0
            ))
    
    def _add_harmonic_series(self):
        """Add harmonic series (octaves of fundamental frequencies)."""
        # Octaves of Schumann resonance
        base_freq = 7.83
        for octave in range(-3, 4):
            freq = base_freq * (2 ** octave)
            self._add_signature(GeoBitSignature(
                name=f"schumann_octave_{octave:+d}",
                value=freq,
                unit="Hz",
                category="harmonic",
                subcategory="schumann_series",
                description=f"Schumann resonance octave {octave:+d}",
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_8,
                harmonic_relationships=["schumann_resonance"],
                octave_class=np.log2(freq),
                confidence=0.9
            ))
        
        # Octaves of 432 Hz (natural tuning)
        base_freq = 432.0
        for octave in range(-2, 3):
            freq = base_freq * (2 ** octave)
            self._add_signature(GeoBitSignature(
                name=f"natural_tuning_octave_{octave:+d}",
                value=freq,
                unit="Hz",
                category="harmonic",
                subcategory="natural_tuning",
                description=f"Natural tuning (432 Hz) octave {octave:+d}",
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_12,
                harmonic_relationships=[],
                octave_class=np.log2(freq),
                confidence=0.8
            ))
    
    def _add_special_values(self):
        """Add special UBP values."""
        special = {
            "pgci_target": {
                "value": 0.999997,
                "unit": "dimensionless",
                "description": "PGCI target for stable reality manifestation",
                "pattern_type": PatternType.CONCENTRIC,
                "symmetry": PatternSymmetry.RADIAL_12
            },
            "nrci_threshold": {
                "value": 0.95,
                "unit": "dimensionless",
                "description": "NRCI threshold for coherent states",
                "pattern_type": PatternType.RADIAL,
                "symmetry": PatternSymmetry.RADIAL_6
            },
            "observer_cost_typical": {
                "value": 3.778212,  # 1/Y
                "unit": "dimensionless",
                "description": "Typical observer computational cost",
                "pattern_type": PatternType.RADIAL,
                "symmetry": PatternSymmetry.RADIAL_12
            }
        }
        
        for name, data in special.items():
            self._add_signature(GeoBitSignature(
                name=name,
                value=data["value"],
                unit=data["unit"],
                category="special",
                subcategory="ubp_metric",
                description=data["description"],
                pattern_type=data["pattern_type"],
                symmetry=data["symmetry"],
                harmonic_relationships=[],
                octave_class=np.log2(data["value"]) if data["value"] > 0 else 0,
                confidence=1.0
            ))
    
    def _add_signature(self, signature: GeoBitSignature):
        """Add a signature to the library."""
        self.signatures[signature.name] = signature
    
    def get_signature(self, name: str) -> Optional[GeoBitSignature]:
        """Get a signature by name."""
        return self.signatures.get(name)
    
    def find_signatures(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        unit: Optional[str] = None,
        value_range: Optional[Tuple[float, float]] = None,
        octave_range: Optional[Tuple[float, float]] = None
    ) -> List[GeoBitSignature]:
        """Find signatures matching criteria."""
        results = []
        
        for sig in self.signatures.values():
            if category and sig.category != category:
                continue
            if subcategory and sig.subcategory != subcategory:
                continue
            if unit and sig.unit != unit:
                continue
            if value_range:
                if not (value_range[0] <= sig.value <= value_range[1]):
                    continue
            if octave_range:
                if not (octave_range[0] <= sig.octave_class <= octave_range[1]):
                    continue
            results.append(sig)
        
        return results
    
    def _get_categories(self) -> List[str]:
        """Get all unique categories."""
        return list(set(sig.category for sig in self.signatures.values()))
    
    def export_library(self, filepath: str):
        """Export library to JSON file."""
        data = {
            name: {
                **asdict(sig),
                'pattern_type': sig.pattern_type.name,
                'symmetry': sig.symmetry.name
            }
            for name, sig in self.signatures.items()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Library exported to: {filepath}")
    
    def generate_pattern(self, name: str) -> Optional[np.ndarray]:
        """Generate geometric pattern for a signature."""
        sig = self.get_signature(name)
        if sig is None:
            return None
        
        pattern, _ = self.codex.value_to_geometry(sig.value, sig.unit)
        return pattern
    
    def print_summary(self):
        """Print library summary."""
        print("\n" + "="*80)
        print("UBP GEOMETRIC PATTERN LIBRARY SUMMARY")
        print("="*80)
        
        categories = {}
        for sig in self.signatures.values():
            if sig.category not in categories:
                categories[sig.category] = []
            categories[sig.category].append(sig)
        
        for category, sigs in sorted(categories.items()):
            print(f"\n{category.upper()}: {len(sigs)} signatures")
            subcats = {}
            for sig in sigs:
                if sig.subcategory not in subcats:
                    subcats[sig.subcategory] = 0
                subcats[sig.subcategory] += 1
            
            for subcat, count in sorted(subcats.items()):
                print(f"  {subcat}: {count}")
        
        print(f"\nTotal: {len(self.signatures)} GeoBit Signatures")
        print("="*80)


# Convenience function
def create_ubp_pattern_library(grid_size: int = 128) -> UBPPatternLibrary:
    """Create a UBP pattern library instance."""
    return UBPPatternLibrary(grid_size=grid_size)
