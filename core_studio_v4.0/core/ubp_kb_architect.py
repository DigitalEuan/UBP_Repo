"""
UBP KB ARCHITECT v2.1 (SOP_002 Standard)
========================================
The definitive factory for creating hardened UBP Knowledge Base entries.
Ensures 100% compatibility with the v5.3 Core and v5.2 Brain.

STANDARDS:
1. Key: SHA256(math_dna)
2. Vector: Deterministic Golay(24,12,8) derived from math_dna
3. NRCI: Hyperbolic Stability [10 / (10 + Tax)]
4. Tilt: Angular deviation from Universal North
5. Lexicon: Strict [Type: Name (Symbol)], [Definition] format.
"""

import hashlib
import json
import re
import numpy as np
import math
from fractions import Fraction
from typing import Tuple, List, Any
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate

# Universal Constants for Alignment
CONST = UBPUltimateSubstrate.get_constants(50)
Y_CONST = CONST['Y']
UNIVERSAL_NORTH = np.array([-0.30656966974248284, -0.9197090092274486, 0.2452557357939863])

class KBArchitect:
    @staticmethod
    def calculate_metrics(math_dna: str, vector: List[int]) -> Tuple[Fraction, Fraction]:
        """Calculates Symmetry Tax and Hyperbolic NRCI."""
        # Tax is derived from the Leech Lattice Engine
        tax = LEECH_ENGINE.calculate_symmetry_tax(vector)
        
        # Hyperbolic NRCI: 10 / (10 + Tax)
        # This ensures complex molecules don't hit 0 NRCI too quickly
        ten = Fraction(10, 1)
        nrci = ten / (ten + tax)
        return tax, nrci

    @staticmethod
    def calculate_tilt(vector: List[int]) -> float:
        """Calculates the 'Tilt' relative to Universal North."""
        # Map 24-bit vector to 3D orientation
        v = np.array([
            sum(vector[0:8]) - 4, 
            sum(vector[8:16]) - 4, 
            sum(vector[16:24]) - 4
        ], dtype=float)
        
        mag = np.linalg.norm(v)
        if mag == 0: return 0.0
        
        unit_v = v / mag
        unit_north = UNIVERSAL_NORTH / np.linalg.norm(UNIVERSAL_NORTH)
        dot = np.dot(unit_v, unit_north)
        # Return degrees
        return round(float(math.degrees(math.acos(max(-1, min(1, dot))))), 4)

    @staticmethod
    def generate_vector(math_dna: str) -> List[int]:
        """Generates a deterministic 24-bit vector from the math string."""
        h_bytes = hashlib.sha256(math_dna.encode()).digest()
        # Use first 12 bits of hash as the message
        combined = (h_bytes[0] << 4) | (h_bytes[1] >> 4)
        msg = [(combined >> i) & 1 for i in range(11, -1, -1)]
        return GOLAY_ENGINE.encode(msg)

    def create_entry(self, ubp_id, lexicon_name, definition, math_dna, hierarchy, tags):
        """Mints a complete SOP_002 compliant entry."""
        fingerprint = hashlib.sha256(math_dna.encode()).hexdigest()
        vector = self.generate_vector(math_dna)
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
            "tags": sorted(list(set(tags + ["SOP_002", "HARDENED"]))),
            "fingerprint": fingerprint
        }
        return fingerprint, entry

# --- Example Usage ---
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