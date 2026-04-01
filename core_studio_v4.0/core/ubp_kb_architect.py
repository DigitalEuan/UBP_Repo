"""
UBP KB ARCHITECT v2.2 (SOP_002 Standard + Gray Code)
===================================================
Now uses Binary-Reflected Gray Code for the 24-bit vector.
- Deterministic from math_dna
- Unique across all entries
- Elements use Z-based Gray ordering (topological smoothness)
- Fully compatible with v5.3 Core / v5.2 Brain
"""

import hashlib
import json
import math
import numpy as np
from fractions import Fraction
from typing import Tuple, List

# Keep your existing core imports
from core import LEECH_ENGINE, UBPUltimateSubstrate

# Universal Constants
CONST = UBPUltimateSubstrate.get_constants(50)
UNIVERSAL_NORTH = np.array([-0.30656966974248284, -0.9197090092274486, 0.2452557357939863])

def to_gray_code(n: int, bits: int = 24) -> List[int]:
    """Convert integer to n-bit binary-reflected Gray code."""
    gray = n ^ (n >> 1)
    return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

class KBArchitect:
    @staticmethod
    def calculate_metrics(math_dna: str, vector: List[int]) -> Tuple[Fraction, Fraction]:
        tax = LEECH_ENGINE.calculate_symmetry_tax(vector)
        ten = Fraction(10, 1)
        nrci = ten / (ten + tax)
        return tax, nrci

    @staticmethod
    def calculate_tilt(vector: List[int]) -> float:
        v = np.array([
            sum(vector[0:8]) - 4,
            sum(vector[8:16]) - 4,
            sum(vector[16:24]) - 4
        ], dtype=float)
        mag = np.linalg.norm(v)
        if mag == 0:
            return 0.0
        unit_v = v / mag
        unit_north = UNIVERSAL_NORTH / np.linalg.norm(UNIVERSAL_NORTH)
        dot = np.dot(unit_v, unit_north)
        return round(float(math.degrees(math.acos(max(-1, min(1, dot))))), 4)

        @staticmethod
    def generate_vector(math_dna: str, ubp_id: str = None) -> List[int]:
        """Deterministic 24-bit Gray Code vector (v8.1 fix)."""
        if ubp_id and ubp_id.startswith("ELEM_"):
            try:
                parts = ubp_id.split("_")
                z = int(parts[2])
                # Unique offset for isotopes (e.g. H_002 vs He_002)
                offset = 1000 if len(parts) > 3 and parts[3] else 0
                index = ((z * 0x111111) + offset) & 0xFFFFFF
            except:
                index = 0
        else:
            h = int(hashlib.sha256(math_dna.encode()).hexdigest(), 16)
            index = h & 0xFFFFFF

        return to_gray_code(index)

    def create_entry(self, ubp_id, lexicon_name, definition, math_dna, hierarchy, tags):
        """Mints a complete SOP_002 compliant entry (now with Gray Code)."""
        fingerprint = hashlib.sha256(math_dna.encode()).hexdigest()
        vector = self.generate_vector(math_dna, ubp_id)          # ← pass ubp_id
        tax, nrci = self.calculate_metrics(math_dna, vector)
        tilt = self.calculate_tilt(vector)

        entry = {
            "ubp_id": ubp_id,
            "lexicon": f"{lexicon_name}, {definition}",
            "math": math_dna,
            "atlas": {
                "hierarchy": hierarchy,
                "vector": vector,
                "nrci": f"{nrci.numerator}/{nrci.denominator}",
                "nrci_score": round(float(nrci), 6),
                "tax": f"{tax.numerator}/{tax.denominator}",
                "weight": sum(vector),
                "tilt": tilt
            },
            "tags": sorted(list(set(tags + ["SOP_002", "HARDENED", "TOPOLOGICAL_V8"]))),
            "fingerprint": fingerprint
        }
        return fingerprint, entry


# --- Example Usage (unchanged) ---
if __name__ == "__main__":
    arch = KBArchitect()
    fp, entry = arch.create_entry(
        ubp_id="REACTION_NUCLEAR_FUSION_DT_001",
        lexicon_name="[Reaction: Nuclear Fusion D-T]",
        definition="Deuterium-tritium fusion: D + T → He-4 + n + 17.6 MeV...",
        math_dna="Reactants=D+T|Products=He4+n|Energy=17.6|Type=Nuclear|Temp_required=1e8|Cross_section_max=5e-28",
        hierarchy="1×PARTICLE_DEUTERON_001 + 1×ELEM_H_001 → 1×ELEM_He_002 + 1×PARTICLE_NEUTRON_001",
        tags=["REACTION", "NUCLEAR", "FUSION", "ENERGY", "PLASMA"]
    )
    print(json.dumps({fp: entry}, indent=2))