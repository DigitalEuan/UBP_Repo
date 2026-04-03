"""
UBP KB ARCHITECT v4.4 (Ultra-Compact Columnar)
==============================================
- Implements v7.0 Gray Code Determinism.
- Supports Tokenized Nulls (0 = null).
- Optimized for index-based retrieval.
"""

import hashlib
import numpy as np
from fractions import Fraction
from typing import List, Dict, Any, Tuple
from core import LEECH_ENGINE, GOLAY_ENGINE

MOG_CATEGORIES = [
    "M_Mass", "M_Charge", "M_Space", "M_Time", "M_Thermal", "M_Count",
    "I_Topology", "I_Symmetry", "I_Density", "I_Connectivity", "I_Dimension", "I_Complexity",
    "A_Energy", "A_Force", "A_Velocity", "A_Flux", "A_Resonance", "A_Spin",
    "P_Probability", "P_Ratio", "P_Limit", "P_Tax", "P_Coherence", "P_Phase"
]

class KBArchitect:
    def __init__(self):
        self.leech = LEECH_ENGINE
        self.golay = GOLAY_ENGINE

    def build_math_dna(self, raw_props: Dict[str, Any]) -> str:
        parts = [f"{k}={raw_props[k]}" for k in sorted(raw_props.keys()) if raw_props[k] is not None]
        return "|".join(parts)

    def create_raw_metrics(self, ubp_id: str, raw_props: Dict[str, Any]):
        dna = self.build_math_dna(raw_props)
        fp = hashlib.sha256(dna.encode()).hexdigest()
        
        seed_int = int(fp[:3], 16)
        message = [(seed_int >> i) & 1 for i in range(11, -1, -1)]
        vector = self.golay.encode(message)
        
        tax = self.leech.calculate_symmetry_tax(vector)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
        
        # Return as a flat tuple for the mapper
        return fp, vector, f"{nrci.numerator}/{nrci.denominator}", round(float(nrci), 6), f"{tax.numerator}/{tax.denominator}"