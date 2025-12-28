"""
================================================================================
UBP PHENOMENOLOGY DEFINITION - v4.1.1 (PRODUCTION)
================================================================================
Description: Defines the 'Phenomenon' object. Handles the transition from 
Noisy Observation (The Mask) to Substrate Truth (The Codeword).
================================================================================
"""
import hashlib
from typing import List, Dict, Any, Tuple
from fractions import Fraction

# Import the perfected v4.1.1 stack
from metrics import METRICS
import ubp_core_final_v4_1_1 as core
import leech_engine_v4_1_enhanced as engine

class PhenomenonDefinition:
    """
    The primary container for a UBP Identity.
    Implements LAW_MASK_001: Phenomenon = Codeword + Noise.
    """
    
    def __init__(self, name: str, domain: str, raw_hex: str = None, tokens: List[str] = None):
        self.name = name
        self.domain = domain
        self.raw_hex = raw_hex
        self.tokens = tokens or []
        self.version = "4.1.1"
        
        # Substrate State
        self.bits24 = []
        self.snapped_bits = []
        self.leech_point = None
        self.results = {}

    def _hex_to_bits24(self, hex_str: str) -> List[int]:
        """Converts a Hex string to a 24-bit list via SHA-256 truncation."""
        h = hashlib.sha256(hex_str.encode('utf-8')).digest()
        bits = []
        for i in range(3): # Take first 3 bytes (24 bits)
            byte = h[i]
            for j in range(8):
                bits.append((byte >> (7 - j)) & 1)
        return bits

    def resolve(self):
        """
        The Master Resolution Pipeline.
        1. Encode -> 2. Snap -> 3. Lift -> 4. Tax -> 5. Health
        """
        # 1. Encode Raw Identity
        if self.raw_hex:
            self.bits24 = self._hex_to_bits24(self.raw_hex)
        else:
            # Fallback to token-based hash if no hex provided
            self.bits24 = self._hex_to_bits24(":".join(self.tokens))

        # 2. Coherence Snap (LAW_APP_001)
        # Resets drifting states to the nearest stable Golay anchor
        self.snapped_bits, metadata = core.GOLAY_DECODER.snap_to_codeword(self.bits24)
        
        # 3. Lift to Leech Lattice (LAW_SUBSTRATE_002)
        self.leech_point = engine.LEECH.get_leech_point(self.snapped_bits)
        
        # 4. Calculate Symmetry Tax (LAW_SYMMETRY_001)
        tax = engine.LEECH.calculate_symmetry_tax(self.leech_point)
        
        # 5. Assess Ontological Health (LAW_SUBSTRATE_005)
        lp_obj = core.LeechPointScaled(coords=tuple(self.leech_point))
        health = lp_obj.get_ontological_health()
        
        # 6. Compile Results
        self.results = {
            "syndrome_weight": metadata["syndrome_weight"],
            "is_stable": metadata["snap_triggered"] == False,
            "symmetry_tax": tax,
            "ontological_health": health,
            "norm_sq_actual": engine.LEECH.verify_norm_actual(self.leech_point),
            "nrci": METRICS.calculate_nrci(metadata["syndrome_weight"])
        }
        return self.results

    def get_triadic_report(self) -> str:
        """Generates the UBP Triadic Identity Report."""
        if not self.results:
            self.resolve()
            
        res = self.results
        h = res["ontological_health"]
        
        report = [
            f"--- UBP IDENTITY REPORT: {self.name} ---",
            f"Domain: {self.domain} | Version: {self.version}",
            f"Substrate Status: {'STABLE' if res['is_stable'] else 'CORRECTED (SNAP)'}",
            f"NRCI: {res['nrci']:.6f} | Symmetry Tax: {res['symmetry_tax']:.4f}",
            f"Leech Norm²: {res['norm_sq_actual']}",
            "\n[ONTOLOGICAL HEALTH (MOG PARTITION)]",
            f"  Reality:    {h['Reality']:.4f}",
            f"  Info:       {h['Info']:.4f}",
            f"  Activation: {h['Activation']:.4f}",
            f"  Potential:  {h['Potential']:.4f}",
            f"  GLOBAL:     {h['Global_NRCI']:.4f}",
            "---------------------------------------"
        ]
        return "\n".join(report)

if __name__ == "__main__":
    # Test: Resolve the identity of 'Gold' (Au, Z=79)
    gold = PhenomenonDefinition("Gold", "Chemistry", raw_hex="Au_79")
    print(gold.get_triadic_report())
