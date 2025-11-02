"""
Crystal Database for UBP Study
Contains physical properties and structural parameters for 20 crystal systems
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class CrystalProperties:
    """Physical and structural properties of a crystal"""
    name: str
    formula: str
    structure_type: str
    space_group: str
    atoms_per_cell: int
    lattice_params: dict  # a, b, c (Angstroms), alpha, beta, gamma (degrees)
    atomic_masses: List[float]  # amu
    bonding_type: str
    is_piezoelectric: bool
    
    # Experimental data (where available)
    density: Optional[float] = None  # g/cm³
    bulk_modulus: Optional[float] = None  # GPa
    shear_modulus: Optional[float] = None  # GPa
    sound_velocity: Optional[float] = None  # m/s
    debye_temperature: Optional[float] = None  # K
    fundamental_frequency: Optional[float] = None  # Hz
    frequency_range: Optional[Tuple[float, float]] = None  # (min, max) Hz
    
    # Piezoelectric properties (if applicable)
    piezo_coefficient_d33: Optional[float] = None  # pC/N
    electromechanical_coupling: Optional[float] = None  # dimensionless
    
    # UBP-specific parameters (to be calculated)
    nrci_target: float = 0.999997
    expected_realm: str = "atomic"


# Crystal database
CRYSTAL_DATABASE = {
    # Group 1: Simple Cubic
    "Po": CrystalProperties(
        name="Polonium",
        formula="Po",
        structure_type="Simple Cubic (SC)",
        space_group="Pm-3m",
        atoms_per_cell=1,
        lattice_params={"a": 3.35, "b": 3.35, "c": 3.35, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[209.0],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=9.196,
        sound_velocity=2500,
        frequency_range=(1e9, 5e9),
        expected_realm="atomic"
    ),
    
    "CsCl": CrystalProperties(
        name="Cesium Chloride",
        formula="CsCl",
        structure_type="Primitive Cubic",
        space_group="Pm-3m",
        atoms_per_cell=2,
        lattice_params={"a": 4.123, "b": 4.123, "c": 4.123, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[132.9, 35.45],
        bonding_type="ionic",
        is_piezoelectric=False,
        density=3.988,
        bulk_modulus=17.5,
        sound_velocity=2000,
        frequency_range=(5e8, 2e9),
        expected_realm="atomic"
    ),
    
    # Group 2: Face-Centered Cubic
    "NaCl": CrystalProperties(
        name="Sodium Chloride",
        formula="NaCl",
        structure_type="FCC (Rock Salt)",
        space_group="Fm-3m",
        atoms_per_cell=2,
        lattice_params={"a": 5.64, "b": 5.64, "c": 5.64, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[22.99, 35.45],
        bonding_type="ionic",
        is_piezoelectric=False,
        density=2.165,
        bulk_modulus=24.0,
        shear_modulus=14.9,
        sound_velocity=3200,
        debye_temperature=321,
        frequency_range=(1e12, 8e12),
        expected_realm="atomic"
    ),
    
    "Au": CrystalProperties(
        name="Gold",
        formula="Au",
        structure_type="FCC",
        space_group="Fm-3m",
        atoms_per_cell=1,
        lattice_params={"a": 4.078, "b": 4.078, "c": 4.078, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[196.97],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=19.32,
        bulk_modulus=180,
        shear_modulus=27,
        sound_velocity=3240,
        debye_temperature=170,
        frequency_range=(1e12, 4e12),
        expected_realm="atomic"
    ),
    
    "Cu": CrystalProperties(
        name="Copper",
        formula="Cu",
        structure_type="FCC",
        space_group="Fm-3m",
        atoms_per_cell=1,
        lattice_params={"a": 3.615, "b": 3.615, "c": 3.615, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[63.55],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=8.96,
        bulk_modulus=140,
        shear_modulus=48,
        sound_velocity=4760,
        debye_temperature=343,
        frequency_range=(2e12, 8e12),
        expected_realm="atomic"
    ),
    
    # Group 3: Body-Centered Cubic
    "Fe": CrystalProperties(
        name="Iron",
        formula="Fe",
        structure_type="BCC",
        space_group="Im-3m",
        atoms_per_cell=1,
        lattice_params={"a": 2.866, "b": 2.866, "c": 2.866, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[55.845],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=7.874,
        bulk_modulus=170,
        shear_modulus=82,
        sound_velocity=5950,
        debye_temperature=470,
        frequency_range=(2e12, 8e12),
        expected_realm="atomic"
    ),
    
    "W": CrystalProperties(
        name="Tungsten",
        formula="W",
        structure_type="BCC",
        space_group="Im-3m",
        atoms_per_cell=1,
        lattice_params={"a": 3.165, "b": 3.165, "c": 3.165, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[183.84],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=19.25,
        bulk_modulus=310,
        shear_modulus=161,
        sound_velocity=5220,
        debye_temperature=400,
        frequency_range=(2e12, 8e12),
        expected_realm="atomic"
    ),
    
    # Group 4: Hexagonal Close-Packed
    "Mg": CrystalProperties(
        name="Magnesium",
        formula="Mg",
        structure_type="HCP",
        space_group="P63/mmc",
        atoms_per_cell=2,
        lattice_params={"a": 3.209, "b": 3.209, "c": 5.211, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[24.305],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=1.738,
        bulk_modulus=45,
        shear_modulus=17,
        sound_velocity=4940,
        debye_temperature=400,
        frequency_range=(2e12, 8e12),
        expected_realm="atomic"
    ),
    
    "Zn": CrystalProperties(
        name="Zinc",
        formula="Zn",
        structure_type="HCP",
        space_group="P63/mmc",
        atoms_per_cell=2,
        lattice_params={"a": 2.665, "b": 2.665, "c": 4.947, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[65.38],
        bonding_type="metallic",
        is_piezoelectric=False,
        density=7.14,
        bulk_modulus=70,
        shear_modulus=43,
        sound_velocity=4170,
        debye_temperature=327,
        frequency_range=(1e12, 6e12),
        expected_realm="atomic"
    ),
    
    # Group 5: Diamond/Zincblende
    "C": CrystalProperties(
        name="Diamond",
        formula="C",
        structure_type="Diamond Cubic",
        space_group="Fd-3m",
        atoms_per_cell=2,
        lattice_params={"a": 3.567, "b": 3.567, "c": 3.567, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[12.011],
        bonding_type="covalent",
        is_piezoelectric=False,
        density=3.515,
        bulk_modulus=442,
        shear_modulus=478,
        sound_velocity=18000,
        debye_temperature=2230,
        frequency_range=(1e13, 4e13),
        expected_realm="atomic"
    ),
    
    "Si": CrystalProperties(
        name="Silicon",
        formula="Si",
        structure_type="Diamond Cubic",
        space_group="Fd-3m",
        atoms_per_cell=2,
        lattice_params={"a": 5.431, "b": 5.431, "c": 5.431, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[28.085],
        bonding_type="covalent",
        is_piezoelectric=False,
        density=2.329,
        bulk_modulus=100,
        shear_modulus=80,
        sound_velocity=8433,
        debye_temperature=645,
        frequency_range=(4e12, 1.6e13),
        expected_realm="atomic"
    ),
    
    "GaAs": CrystalProperties(
        name="Gallium Arsenide",
        formula="GaAs",
        structure_type="Zincblende",
        space_group="F-43m",
        atoms_per_cell=2,
        lattice_params={"a": 5.653, "b": 5.653, "c": 5.653, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[69.723, 74.922],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=True,
        density=5.316,
        bulk_modulus=75.5,
        shear_modulus=33.3,
        sound_velocity=5150,
        debye_temperature=344,
        frequency_range=(2e12, 9e12),
        piezo_coefficient_d33=2.7,
        electromechanical_coupling=0.05,
        expected_realm="atomic"
    ),
    
    # Group 6: Piezoelectric Crystals
    "Quartz": CrystalProperties(
        name="Quartz",
        formula="SiO2",
        structure_type="Trigonal",
        space_group="P3221",
        atoms_per_cell=9,
        lattice_params={"a": 4.916, "b": 4.916, "c": 5.405, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[28.085, 15.999, 15.999],
        bonding_type="covalent",
        is_piezoelectric=True,
        density=2.648,
        bulk_modulus=37,
        shear_modulus=44,
        sound_velocity=5760,
        debye_temperature=470,
        fundamental_frequency=32768,  # 32.768 kHz watch crystal
        frequency_range=(3.2768e4, 1e8),  # 32 kHz to 100 MHz
        piezo_coefficient_d33=2.3,
        electromechanical_coupling=0.1,
        expected_realm="atomic"
    ),
    
    "LiNbO3": CrystalProperties(
        name="Lithium Niobate",
        formula="LiNbO3",
        structure_type="Trigonal",
        space_group="R3c",
        atoms_per_cell=10,
        lattice_params={"a": 5.148, "b": 5.148, "c": 13.863, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[6.941, 92.906, 15.999, 15.999, 15.999],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=True,
        density=4.64,
        bulk_modulus=150,
        sound_velocity=6570,
        frequency_range=(1e8, 5e9),  # 100 MHz to 5 GHz
        piezo_coefficient_d33=6.0,
        electromechanical_coupling=0.17,
        expected_realm="electromagnetic"
    ),
    
    "PZT": CrystalProperties(
        name="Lead Zirconate Titanate",
        formula="Pb(Zr,Ti)O3",
        structure_type="Perovskite",
        space_group="P4mm",
        atoms_per_cell=5,
        lattice_params={"a": 4.04, "b": 4.04, "c": 4.14, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[207.2, 91.224, 47.867, 15.999, 15.999, 15.999],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=True,
        density=7.5,
        bulk_modulus=100,
        sound_velocity=4000,
        frequency_range=(1e3, 1e6),  # kHz to MHz
        piezo_coefficient_d33=300,  # Very high!
        electromechanical_coupling=0.7,
        expected_realm="atomic"
    ),
    
    "AlN": CrystalProperties(
        name="Aluminum Nitride",
        formula="AlN",
        structure_type="Wurtzite (Hexagonal)",
        space_group="P63mc",
        atoms_per_cell=4,
        lattice_params={"a": 3.112, "b": 3.112, "c": 4.982, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[26.982, 14.007],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=True,
        density=3.26,
        bulk_modulus=210,
        sound_velocity=10400,
        frequency_range=(1e9, 1e10),  # 1-10 GHz
        piezo_coefficient_d33=5.5,
        electromechanical_coupling=0.24,
        expected_realm="electromagnetic"
    ),
    
    # Group 7: Complex Structures
    "CaCO3": CrystalProperties(
        name="Calcite",
        formula="CaCO3",
        structure_type="Trigonal",
        space_group="R-3c",
        atoms_per_cell=10,
        lattice_params={"a": 4.990, "b": 4.990, "c": 17.061, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[40.078, 12.011, 15.999, 15.999, 15.999],
        bonding_type="ionic",
        is_piezoelectric=False,
        density=2.71,
        bulk_modulus=73,
        sound_velocity=6530,
        frequency_range=(1e11, 3e12),
        expected_realm="atomic"
    ),
    
    "TiO2": CrystalProperties(
        name="Rutile",
        formula="TiO2",
        structure_type="Tetragonal",
        space_group="P42/mnm",
        atoms_per_cell=6,
        lattice_params={"a": 4.594, "b": 4.594, "c": 2.959, "alpha": 90, "beta": 90, "gamma": 90},
        atomic_masses=[47.867, 15.999, 15.999],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=False,
        density=4.23,
        bulk_modulus=211,
        sound_velocity=7900,
        frequency_range=(2e11, 3e12),
        expected_realm="atomic"
    ),
    
    "Al2O3": CrystalProperties(
        name="Sapphire",
        formula="Al2O3",
        structure_type="Trigonal (Corundum)",
        space_group="R-3c",
        atoms_per_cell=10,
        lattice_params={"a": 4.759, "b": 4.759, "c": 12.991, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[26.982, 26.982, 15.999, 15.999, 15.999],
        bonding_type="mixed_ionic_covalent",
        is_piezoelectric=False,
        density=3.98,
        bulk_modulus=240,
        shear_modulus=163,
        sound_velocity=11100,
        debye_temperature=1047,
        frequency_range=(2e12, 2.5e13),
        expected_realm="atomic"
    ),
    
    "H2O_ice": CrystalProperties(
        name="Ice Ih",
        formula="H2O",
        structure_type="Hexagonal",
        space_group="P63/mmc",
        atoms_per_cell=4,
        lattice_params={"a": 4.497, "b": 4.497, "c": 7.322, "alpha": 90, "beta": 90, "gamma": 120},
        atomic_masses=[1.008, 1.008, 15.999],
        bonding_type="hydrogen_bonding",
        is_piezoelectric=False,
        density=0.917,
        bulk_modulus=9,
        sound_velocity=3980,
        frequency_range=(1e12, 1e14),
        expected_realm="atomic"
    ),
}


def get_crystal(name: str) -> CrystalProperties:
    """Retrieve crystal properties by name"""
    if name not in CRYSTAL_DATABASE:
        raise ValueError(f"Crystal '{name}' not found in database. Available: {list(CRYSTAL_DATABASE.keys())}")
    return CRYSTAL_DATABASE[name]


def get_all_crystals() -> dict:
    """Get all crystals in database"""
    return CRYSTAL_DATABASE


def get_crystals_by_type(structure_type: str) -> dict:
    """Get all crystals of a specific structure type"""
    return {name: props for name, props in CRYSTAL_DATABASE.items() 
            if structure_type.lower() in props.structure_type.lower()}


def get_piezoelectric_crystals() -> dict:
    """Get all piezoelectric crystals"""
    return {name: props for name, props in CRYSTAL_DATABASE.items() 
            if props.is_piezoelectric}


def get_crystals_by_bonding(bonding_type: str) -> dict:
    """Get all crystals with specific bonding type"""
    return {name: props for name, props in CRYSTAL_DATABASE.items() 
            if bonding_type.lower() in props.bonding_type.lower()}


if __name__ == "__main__":
    # Test database
    print("Crystal Database Summary")
    print("=" * 80)
    print(f"Total crystals: {len(CRYSTAL_DATABASE)}")
    print(f"Piezoelectric crystals: {len(get_piezoelectric_crystals())}")
    print(f"\nCrystal list:")
    for i, (name, props) in enumerate(CRYSTAL_DATABASE.items(), 1):
        piezo_marker = "⚡" if props.is_piezoelectric else "  "
        print(f"{i:2d}. {piezo_marker} {name:10s} - {props.structure_type:20s} - {props.bonding_type}")
