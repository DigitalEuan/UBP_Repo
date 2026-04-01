"""
UBP Core Engine — Universal Binary Principal Computational Implementation
Implements the core UBP framework for the NZ Fuel Study V2
Based on: UBP Core Studio v4.0 / SOP_002 Hardened Protocol
Author context: E R A Craig, New Zealand
"""

import math
import json
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

# ============================================================
# UBP CORE CONSTANTS (from ubp_system_kb.json, SOP_002 Hardened)
# ============================================================

# Y-Constant: Y = 1 / (π + 2/π) ≈ 0.264675
PI = math.pi
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
E = math.e

Y_CONSTANT = 1 / (PI + 2 / PI)  # ≈ 0.264675

# NRCI Stability Windows (from ubp_files_and_usage.md)
NRCI_CAPTURE_ZONE = 0.98
NRCI_STABLE_MATTER = 0.60
NRCI_ANOMALY_THRESHOLD = 0.60
NRCI_NOISE_BASELINE = 0.42
NRCI_REDLINE = 0.005

# Golay Code parameters [24, 12, 8]
GOLAY_BLOCK_LENGTH = 24
GOLAY_MIN_HAMMING = 8
GOLAY_CORRECTION_RADIUS = 3  # t = floor((d_min - 1)/2) = 3
GOLAY_CODEWORDS = 4096  # 2^12

# Universal North reference manifold
UNIVERSAL_NORTH = (237, 83, 172)

# 13D Sink parameter
L_SINK = (PI * PHI * E % 1) / 13  # ≈ 0.06289

# Noumenal Volume
NOUMENAL_VOLUME = 204.801744

# ============================================================
# ELEMENT DATA (from ubp_system_kb.json, SOP_002 Hardened)
# ============================================================

ELEMENT_DATA = {
    'H': {
        'Z': 1, 'NRCI': 0.762346, 'Tax': 3.118, 'Tilt': 72.5198,
        'Valence': 1, 'Mass': 1.008,
        'vector': [0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1],
        'name': 'Hydrogen', 'symbol': 'H',
        'nrci_exact': Fraction(403444893430547524070884368918423718209681608902836667575630,
                               529214943424193212713164429654199740969412272217383116120321)
    },
    'He': {
        'Z': 2, 'NRCI': 0.681380, 'Tax': 4.676, 'Tilt': 134.4974,
        'Valence': 2, 'Mass': 4.003,
        'vector': [0,1,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1],
        'name': 'Helium', 'symbol': 'He'
    },
    'C': {
        'Z': 6, 'NRCI': 0.615961, 'Tax': 6.237, 'Tilt': 140.8900,
        'Valence': 4, 'Mass': 12.011,
        'name': 'Carbon', 'symbol': 'C'
    },
    'N': {
        'Z': 7, 'NRCI': 0.681380, 'Tax': 3.118, 'Tilt': 145.4624,
        'Valence': 5, 'Mass': 14.007,
        'name': 'Nitrogen', 'symbol': 'N'
    },
    'O': {
        'Z': 8, 'NRCI': 0.681380, 'Tax': 3.118, 'Tilt': 145.4624,
        'Valence': 6, 'Mass': 15.999,
        'name': 'Oxygen', 'symbol': 'O'
    },
    'K': {
        'Z': 19, 'NRCI': 0.412, 'Tax': 9.85, 'Tilt': 178.2,
        'Valence': 1, 'Mass': 39.098,
        'name': 'Potassium', 'symbol': 'K'
    }
}

# ============================================================
# UBP MATHEMATICAL CORE
# ============================================================

def compute_nrci(tax: float) -> float:
    """Compute NRCI from Symmetry Tax.
    NRCI = 10 / (10 + Tax)
    """
    return 10.0 / (10.0 + tax)

def compute_tax_from_vector(vector: List[int]) -> float:
    """Compute Symmetry Tax from 24-bit vector.
    Tax = Y * hamming_weight + ||psi(v)||^2 / 8
    where psi(v)_i = 1 - 2*v_i maps {0,1} -> {+1,-1}
    """
    hamming_w = sum(vector)
    # Stereoscopic lift: psi(v)_i = 1 - 2*v_i
    psi = [1 - 2 * bit for bit in vector]
    norm_sq = sum(x * x for x in psi)  # = sum((1-2v)^2) = sum(1 - 4v + 4v^2) = 24 - 4*sum(v) + 4*sum(v) = 24
    # Actually norm_sq = n for binary vectors (each component contributes 1)
    tax = Y_CONSTANT * hamming_w + norm_sq / 8.0
    return tax

def hamming_distance(v1: List[int], v2: List[int]) -> int:
    """Compute Hamming distance between two binary vectors."""
    return sum(b1 != b2 for b1, b2 in zip(v1, v2))

def vector_flow_addition(v1: List[int], v2: List[int]) -> List[int]:
    """UBP-Py Vector Flow Addition (Z^24).
    1. Stereoscopic Lift: psi(v)_i = 1 - 2*v_i
    2. Vector Flow: f = psi(v1) + psi(v2)
    3. Phenomenal Collapse: r_i = 0 if f_i >= 0, else 1
    """
    psi1 = [1 - 2 * b for b in v1]
    psi2 = [1 - 2 * b for b in v2]
    flow = [a + b for a, b in zip(psi1, psi2)]
    result = [0 if f >= 0 else 1 for f in flow]
    return result

def gap_score(vector: List[int], codeword: List[int]) -> int:
    """Gap = Hamming distance between raw vector and nearest codeword.
    0 = Noumenal Truth
    1-3 = Phenomenal Reality (stable matter)
    4-7 = High Tension (unstable)
    >= 8 = Deep Hole
    """
    return hamming_distance(vector, codeword)

def binding_energy(gap: int) -> float:
    """Symmetry Rebate = binding energy.
    Xi = Gap * Y
    """
    return gap * Y_CONSTANT

# ============================================================
# MOLECULAR NRCI CALCULATIONS
# ============================================================

@dataclass
class BondInfo:
    """Represents a chemical bond."""
    atom_a: str
    atom_b: str
    bond_order: int = 1  # 1=single, 2=double, 3=triple

@dataclass
class MoleculeUBP:
    """UBP representation of a molecule."""
    name: str
    formula: str
    composition: Dict[str, int]  # element -> count
    bonds: List[BondInfo] = field(default_factory=list)
    phase: str = 'liquid'  # 'liquid', 'vapor', 'gas'

    # Computed properties
    NRCI: float = 0.0
    Tax: float = 0.0
    Tax_v6: float = 0.0  # v6.0 topology-aware
    Tilt: float = 0.0
    Z_total: int = 0
    mass: float = 0.0
    hamming_drift: float = 0.0

    def compute_properties(self):
        """Compute all UBP properties for the molecule."""
        total_atoms = sum(self.composition.values())

        if total_atoms == 0:
            return

        # Z_total
        self.Z_total = sum(ELEMENT_DATA[el]['Z'] * count
                          for el, count in self.composition.items()
                          if el in ELEMENT_DATA)

        # Mass
        self.mass = sum(ELEMENT_DATA[el]['Mass'] * count
                       for el, count in self.composition.items()
                       if el in ELEMENT_DATA)

        # Simple weighted average NRCI (V1 approximation baseline)
        nrci_sum = sum(ELEMENT_DATA[el]['NRCI'] * count
                      for el, count in self.composition.items()
                      if el in ELEMENT_DATA)
        self.NRCI = nrci_sum / total_atoms

        # Weighted average Tax (V1 baseline)
        tax_sum = sum(ELEMENT_DATA[el]['Tax'] * count
                     for el, count in self.composition.items()
                     if el in ELEMENT_DATA)
        self.Tax = tax_sum / total_atoms

        # Apply bond corrections (LAW_CHEM_004)
        bond_correction = self._compute_bond_corrections()
        self.Tax += bond_correction

        # Recalculate NRCI with bond-corrected Tax
        self.NRCI = compute_nrci(self.Tax)

        # V6.0 Topology-Aware NRCI
        self.Tax_v6 = self._compute_v6_tax()

        # Weighted average Tilt
        tilt_sum = sum(ELEMENT_DATA[el]['Tilt'] * count
                      for el, count in self.composition.items()
                      if el in ELEMENT_DATA)
        self.Tilt = tilt_sum / total_atoms

        # Phase-dependent Hamming drift
        self.hamming_drift = self._compute_phase_drift()

    def _compute_bond_corrections(self) -> float:
        """Apply LAW_CHEM_004 bond order corrections.
        alpha_bond = ((alpha_A + alpha_B)/2) + 0.12*(BO-1)
        The bond correction to Tax is the sum of all bond corrections.
        """
        correction = 0.0
        for bond in self.bonds:
            if bond.atom_a in ELEMENT_DATA and bond.atom_b in ELEMENT_DATA:
                nrci_a = ELEMENT_DATA[bond.atom_a]['NRCI']
                nrci_b = ELEMENT_DATA[bond.atom_b]['NRCI']
                alpha_avg = (nrci_a + nrci_b) / 2
                # Bond correction: higher bond order lowers effective Tax
                # (stronger bonds = more geometric stability)
                bo_correction = 0.12 * (bond.bond_order - 1)
                # This reduces Tax (increases stability)
                correction -= bo_correction * 0.1  # Scale factor
        return correction

    def _compute_v6_tax(self) -> float:
        """V6.0 topology-aware NRCI calculation.
        1. Compactness: C = V^(2/3) / Surface (approximated by atom count ratio)
        2. Symmetry Rebate: R = 1 - C/13
        3. Adjusted Tax: T_adj = T_base * R
        """
        total_atoms = sum(self.composition.values())
        # Approximate compactness from molecular formula
        v = total_atoms  # Proxy for volume
        surface = 2 + total_atoms  # Approximate surface atoms
        compactness = (v ** (2.0/3)) / surface
        rebate = 1 - compactness / 13.0
        rebate = max(0.1, min(1.0, rebate))  # Clamp
        return self.Tax * rebate

    def _compute_phase_drift(self) -> float:
        """Compute Hamming drift from lattice based on phase state.
        LAW_CHEM_PHASE_001: Phase ~ d_H(State, Lattice)
        - Solid/near-solid: d_H <= 4 (near the d=4 solid boundary)
        - Liquid: d_H ~ 4-6
        - Vapor: d_H ~ 6-9
        - Gas: d_H > 9
        """
        if self.phase == 'solid':
            return 4.0
        elif self.phase == 'liquid':
            # Liquid phase: moderate drift
            # Heavier molecules sit closer to lattice (higher d_H needed to vaporize)
            base_drift = 5.0 + 0.02 * self.mass / len(self.composition)
            return min(base_drift, 7.0)
        elif self.phase == 'vapor':
            # Pre-vaporized but not fully gas
            return 7.5
        elif self.phase == 'gas':
            # Fully gaseous
            return 9.0
        return 5.0

    def get_nrci_v6(self) -> float:
        """Return V6.0 topology-aware NRCI."""
        return compute_nrci(self.Tax_v6)

    def activation_energy_estimate(self, phase_state: str = None) -> float:
        """Estimate activation energy for combustion.
        LAW_CHEM_KINETICS_001: E_act = max(Tax_path) - Tax_initial
        Pre-heating/vaporization raises Tax_initial, reducing E_act.
        """
        if phase_state is None:
            phase_state = self.phase

        # Activation peak Tax (estimated as fixed pathway cost)
        tax_peak = 15.0  # Representative activation barrier

        # Phase-dependent Tax_initial
        if phase_state == 'liquid':
            tax_initial = self.Tax
        elif phase_state == 'preheated_60c':
            # 60°C preheating: partial phase advancement
            # k = 0.00111 per °C from LAW_CHEM_FUEL_OPT_002
            advancement = 0.00111 * (60 - 20) * self.Tax
            tax_initial = self.Tax + advancement
        elif phase_state == 'preheated_90c':
            advancement = 0.00111 * (90 - 20) * self.Tax
            tax_initial = self.Tax + advancement
        elif phase_state == 'vapor':
            # Full vaporization: substantial phase advancement
            advancement = 0.00111 * 150 * self.Tax  # Equivalent temp advancement
            tax_initial = self.Tax + advancement
        else:
            tax_initial = self.Tax

        e_act = max(0, tax_peak - tax_initial)
        return e_act


def build_isooctane() -> MoleculeUBP:
    """Build isooctane (2,2,4-trimethylpentane, C8H18) UBP representation."""
    mol = MoleculeUBP(
        name='Isooctane (2,2,4-trimethylpentane)',
        formula='C8H18',
        composition={'C': 8, 'H': 18},
        bonds=[
            # 7 C-C single bonds
            BondInfo('C', 'C', 1), BondInfo('C', 'C', 1), BondInfo('C', 'C', 1),
            BondInfo('C', 'C', 1), BondInfo('C', 'C', 1), BondInfo('C', 'C', 1),
            BondInfo('C', 'C', 1),
            # 18 C-H single bonds
            *[BondInfo('C', 'H', 1) for _ in range(18)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_nheptane() -> MoleculeUBP:
    """Build n-heptane (C7H16) - zero octane reference fuel."""
    mol = MoleculeUBP(
        name='n-Heptane',
        formula='C7H16',
        composition={'C': 7, 'H': 16},
        bonds=[
            *[BondInfo('C', 'C', 1) for _ in range(6)],
            *[BondInfo('C', 'H', 1) for _ in range(16)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_acetone() -> MoleculeUBP:
    """Build acetone (C3H6O) UBP representation."""
    mol = MoleculeUBP(
        name='Acetone',
        formula='C3H6O',
        composition={'C': 3, 'H': 6, 'O': 1},
        bonds=[
            BondInfo('C', 'C', 1), BondInfo('C', 'C', 1),  # C-C single
            BondInfo('C', 'O', 2),  # C=O double bond (KETONE)
            *[BondInfo('C', 'H', 1) for _ in range(6)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_ethanol() -> MoleculeUBP:
    """Build ethanol (C2H6O) UBP representation."""
    mol = MoleculeUBP(
        name='Ethanol',
        formula='C2H6O',
        composition={'C': 2, 'H': 6, 'O': 1},
        bonds=[
            BondInfo('C', 'C', 1),
            BondInfo('C', 'O', 1),  # C-O single
            BondInfo('O', 'H', 1),  # O-H
            *[BondInfo('C', 'H', 1) for _ in range(5)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_methanol() -> MoleculeUBP:
    """Build methanol (CH4O) UBP representation."""
    mol = MoleculeUBP(
        name='Methanol',
        formula='CH4O',
        composition={'C': 1, 'H': 4, 'O': 1},
        bonds=[
            BondInfo('C', 'O', 1),
            BondInfo('O', 'H', 1),
            *[BondInfo('C', 'H', 1) for _ in range(3)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_water() -> MoleculeUBP:
    """Build water (H2O)."""
    mol = MoleculeUBP(
        name='Water',
        formula='H2O',
        composition={'H': 2, 'O': 1},
        bonds=[
            BondInfo('O', 'H', 1),
            BondInfo('O', 'H', 1)
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_hydrogen_gas() -> MoleculeUBP:
    """Build hydrogen gas (H2)."""
    mol = MoleculeUBP(
        name='Hydrogen Gas',
        formula='H2',
        composition={'H': 2},
        bonds=[BondInfo('H', 'H', 1)],
        phase='gas'
    )
    mol.compute_properties()
    return mol


def build_oxygen_gas() -> MoleculeUBP:
    """Build oxygen gas (O2)."""
    mol = MoleculeUBP(
        name='Oxygen Gas',
        formula='O2',
        composition={'O': 2},
        bonds=[BondInfo('O', 'O', 2)],  # O=O double bond
        phase='gas'
    )
    mol.compute_properties()
    return mol


def build_co2() -> MoleculeUBP:
    """Build carbon dioxide (CO2) - combustion product."""
    mol = MoleculeUBP(
        name='Carbon Dioxide',
        formula='CO2',
        composition={'C': 1, 'O': 2},
        bonds=[
            BondInfo('C', 'O', 2),
            BondInfo('C', 'O', 2)
        ],
        phase='gas'
    )
    mol.compute_properties()
    return mol


def build_methyl_oleate() -> MoleculeUBP:
    """Build methyl oleate (C19H36O2) - representative biodiesel."""
    mol = MoleculeUBP(
        name='Methyl Oleate (Biodiesel)',
        formula='C19H36O2',
        composition={'C': 19, 'H': 36, 'O': 2},
        bonds=[
            *[BondInfo('C', 'C', 1) for _ in range(17)],  # Mostly single
            BondInfo('C', 'C', 2),  # One double bond (oleic = monounsaturated)
            BondInfo('C', 'O', 2),  # Ester C=O
            BondInfo('C', 'O', 1),  # Ester C-O
            *[BondInfo('C', 'H', 1) for _ in range(36)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


def build_ft_diesel() -> MoleculeUBP:
    """Build Fischer-Tropsch synthetic diesel (approximated as C16H34)."""
    mol = MoleculeUBP(
        name='FT Synthetic Diesel (approx. C16H34)',
        formula='C16H34',
        composition={'C': 16, 'H': 34},
        bonds=[
            *[BondInfo('C', 'C', 1) for _ in range(15)],
            *[BondInfo('C', 'H', 1) for _ in range(34)]
        ],
        phase='liquid'
    )
    mol.compute_properties()
    return mol


# ============================================================
# BLEND CALCULATIONS (LAW_CHEM_FUEL_OPT_001)
# ============================================================

def compute_blend_nrci(components: List[Tuple[MoleculeUBP, float]]) -> Dict:
    """Compute NRCI of a fuel blend.
    LAW_CHEM_FUEL_OPT_001: NRCI_blend = Sum(x_i * NRCI_i) / Sum(x_i)

    components: list of (molecule, volume_fraction) tuples
    """
    total_fraction = sum(frac for _, frac in components)

    nrci_blend = sum(mol.NRCI * frac for mol, frac in components) / total_fraction
    tax_blend = sum(mol.Tax * frac for mol, frac in components) / total_fraction
    mass_blend = sum(mol.mass * frac for mol, frac in components) / total_fraction

    # Oxygen content of blend (mass fraction)
    o_content = sum(
        mol.composition.get('O', 0) * ELEMENT_DATA['O']['Mass'] / mol.mass * frac
        for mol, frac in components
    ) / total_fraction

    return {
        'NRCI_blend': nrci_blend,
        'Tax_blend': tax_blend,
        'Mass_blend': mass_blend,
        'Oxygen_mass_fraction': o_content,
        'NRCI_improvement': nrci_blend - components[0][0].NRCI,  # vs base fuel
    }


if __name__ == '__main__':
    print("=" * 60)
    print("UBP CORE ENGINE — INITIALIZATION TEST")
    print("=" * 60)
    print(f"Y-Constant: {Y_CONSTANT:.6f}")
    print(f"L-Sink (13D): {L_SINK:.6f}")
    print(f"Noumenal Volume: {NOUMENAL_VOLUME}")
    print(f"Golay Correction Radius: d={GOLAY_CORRECTION_RADIUS}")
    print()

    print("ELEMENT NRCI VERIFICATION:")
    for sym, data in ELEMENT_DATA.items():
        if 'NRCI' in data:
            print(f"  {sym:3s}: NRCI={data['NRCI']:.6f}, Tax={data['Tax']:.3f}, Z={data['Z']}")

    print()
    print("MOLECULAR CONSTRUCTION TEST:")

    isooctane = build_isooctane()
    print(f"\n  Isooctane (C8H18):")
    print(f"    NRCI = {isooctane.NRCI:.6f}")
    print(f"    Tax  = {isooctane.Tax:.4f}")
    print(f"    Z_total = {isooctane.Z_total}")
    print(f"    Mass = {isooctane.mass:.3f} g/mol")

    acetone = build_acetone()
    print(f"\n  Acetone (C3H6O):")
    print(f"    NRCI = {acetone.NRCI:.6f}")
    print(f"    Tax  = {acetone.Tax:.4f}")
    print(f"    Z_total = {acetone.Z_total}")

    ethanol = build_ethanol()
    print(f"\n  Ethanol (C2H6O):")
    print(f"    NRCI = {ethanol.NRCI:.6f}")
    print(f"    Tax  = {ethanol.Tax:.4f}")
    print(f"    Z_total = {ethanol.Z_total}")

    print("\nCore engine ready.")
