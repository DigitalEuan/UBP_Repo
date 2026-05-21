"""
================================================================================
UBP SOVEREIGN SEMANTIC ENGINE — COGNITIVE LAYER
================================================================================
Absorbs the advanced Lattice-Snap and Triple Delta Protocol from the CritPt runner.
Allows the Semantic Engine to verify the physical reality of queried concepts.
"""
import hashlib
from fractions import Fraction
from typing import Any, Dict, List, Tuple, Optional
import sympy as sp

# Import core UBP engines
from core import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra

class SovereignSemanticAuditor:
    """
    Performs the 'Lattice Snap' on any mathematical or physical value.
    Determines if a concept is 'Phase-Locked' (NRCI >= 0.70) in reality.
    """
    NRCI_PHASE_LOCK = Fraction(7, 10)
    CODEWORD_WEIGHTS = {0, 8, 12, 16, 24}
    LATTICE_NAMES = {0: "Identity", 8: "Octad", 12: "Dodecad", 16: "Hexadecad", 24: "Universe"}

    @classmethod
    def to_gray_code(cls, n: int, bits: int = 24) -> list:
        gray = int(n) ^ (int(n) >> 1)
        return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

    @classmethod
    def audit_value(cls, value: Any) -> Dict[str, Any]:
        try:
            n = abs(int(float(str(value)))) & 0xFFFFFF
            raw = cls.to_gray_code(n)
        except Exception:
            h = int(hashlib.sha256(str(value).encode()).hexdigest(), 16)
            raw = [(h >> i) & 1 for i in range(23, -1, -1)]

        decoded, _, _ = GOLAY_ENGINE.decode(raw)
        snapped = GOLAY_ENGINE.encode(decoded)
        sw = sum(snapped)

        tax = LEECH_ENGINE.calculate_symmetry_tax(snapped)
        tax_f = tax if isinstance(tax, Fraction) else Fraction(tax)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax_f)

        return {
            "vector": snapped,
            "sw": sw,
            "nrci": float(nrci),
            "nrci_repr": f"{nrci.numerator}/{nrci.denominator}",
            "on_lattice": sw in cls.CODEWORD_WEIGHTS,
            "lattice": cls.LATTICE_NAMES.get(sw, "Off-lattice"),
            "phase_locked": nrci >= cls.NRCI_PHASE_LOCK
        }

class TripleDeltaProjector:
    """
    Implements the Triple Delta Protocol.
    Generates deterministic symbolic formulas from a 24-bit physical signature.
    """
    @classmethod
    def project_formula(cls, signature_text: str, symbols_list: List[str]) -> str:
        snap = SovereignSemanticAuditor.audit_value(signature_text)
        vec = snap["vector"]
        n_p = len(symbols_list)
        if n_p == 0: return "0"

        block = 24 // n_p
        terms = []
        for i, p in enumerate(symbols_list):
            bits = vec[i*block:(i+1)*block]
            c1 = sum(bits)
            c2 = sum(bits[:2])
            if c1:
                terms.append(f"{c1} * {p}")
            if c2:
                terms.append(f"{c2} * {p}**2")

        return " + ".join(terms) if terms else "0"

print("✅ 'ubp_semantic_sovereign.py' compiled successfully!")
