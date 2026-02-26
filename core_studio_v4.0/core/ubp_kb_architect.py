"""
UBP KB ARCHITECT v2.0 (SOP_002 Standard)
========================================
The definitive reference for creating hardened UBP Knowledge Base entries.
Ensures 100% compatibility with the v5.3 Core and Reflexive Cortex.

STANDARDS:
1. Fingerprint: SHA256(math_dna)
2. Vector: Deterministic Golay(24,12,8) from math_dna
3. NRCI: Hyperbolic Stability [1 / (1 + Tax/10)]
4. Tilt: Angular deviation from Universal North [-0.306, -0.919, 0.245]
5. Lexicon: Strict [Name], [Definition] format.

Author: Euan R A Craig & UBP Research Cortex v4.2.7
Date: 25 Feb 2026
"""

import hashlib
import json
import re
import numpy as np
import math
from fractions import Fraction
from typing import Tuple, List, Any # <--- FIXED: Added missing imports
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate

CONST = UBPUltimateSubstrate.get_constants(50)
Y_CONST = CONST['Y']
UNIVERSAL_NORTH = np.array([-0.30656966974248284, -0.9197090092274486, 0.2452557357939863])

class KBArchitect:
    @staticmethod
    def calculate_metrics(math_dna: str) -> Tuple[Fraction, Fraction]:
        if math_dna in ["absolute_primitive", "atomic", ""]:
            return Fraction(0), Fraction(1)
        dimensions = math_dna.split('|')
        tax = Fraction(len(dimensions)) * Y_CONST
        voxels = len(re.findall(r'\d', math_dna)) + len(re.findall(r'[×+^/→=]', math_dna))
        tax += Fraction(voxels**2, 1000)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
        return tax, nrci

    @staticmethod
    def calculate_tilt(vector: List[int]) -> float:
        v = np.array([sum(vector[0:8])-4, sum(vector[8:16])-4, sum(vector[16:24])-4], dtype=float)
        mag = np.linalg.norm(v)
        if mag == 0: return 0.0
        unit_v = v / mag
        unit_north = UNIVERSAL_NORTH / np.linalg.norm(UNIVERSAL_NORTH)
        dot = np.dot(unit_v, unit_north)
        return round(math.degrees(math.acos(max(-1, min(1, dot)))), 4)

    @staticmethod
    def generate_vector(math_dna: str) -> List[int]:
        h_bytes = hashlib.sha256(math_dna.encode()).digest()
        combined = (h_bytes[0] << 4) | (h_bytes[1] >> 4)
        msg = [(combined >> i) & 1 for i in range(11, -1, -1)]
        return GOLAY_ENGINE.encode(msg)

    def create_entry(self, ubp_id, name, definition, math_dna, hierarchy, tags):
        fingerprint = hashlib.sha256(math_dna.encode()).hexdigest()
        vector = self.generate_vector(math_dna)
        tax, nrci = self.calculate_metrics(math_dna)
        tilt = self.calculate_tilt(vector)
        entry = {
            "ubp_id": ubp_id,
            "lexicon": f"[{name}], {definition}",
            "math": math_dna,
            "logic": f"def verify():\n    dna = '{math_dna}'\n    return hashlib.sha256(dna.encode()).hexdigest() == '{fingerprint}'",
            "atlas": {
                "hierarchy": hierarchy,
                "vector": vector,
                "nrci": f"{nrci.numerator}/{nrci.denominator}",
                "nrci_score": round(float(nrci), 6),
                "tax": f"{tax.numerator}/{tax.denominator}",
                "weight": sum(vector),
                "tilt": tilt
            },
            "tags": sorted(list(set(tags + ["SOP_002", "HARDENED"])))
        }
        return fingerprint, entry

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    arch = KBArchitect()
    
    # Example: Hardening the Law of Carrier Shielding
    fp, entry = arch.create_entry(
        ubp_id="LAW_CARRIER_SHIELDING_001",
        name="Carrier Shielding",
        definition="The computational technique of XORing a high-tax target with a stable geometric carrier to reduce total symmetry tax.",
        math_dna="Tax(A_XOR_B)<<Tax(A)+Tax(B)|Efficiency_Avg=0.496",
        hierarchy="ALGORITHM -> MECHANISM -> QUANTITY",
        tags=["COMPUTATION", "EFFICIENCY"]
    )
    
    print(f"NEW ENTRY FOR KB:\n{json.dumps({fp: entry}, indent=2)}")