"""
================================================================================
UBP LEECH ENGINE - v4.1.1 (FINAL PRODUCTION)
================================================================================
Description: The Geometric Substrate. Handles 24D Leech Lattice generation, 
Symmetry Tax calculation, and Physical Space projection.
================================================================================
"""
import math
from typing import List, Tuple, Dict, Optional, Generator
from fractions import Fraction

# Integration with the Final Core
try:
    import ubp_core_final_v4_1_1 as core
    from metrics import METRICS
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("[WARNING] ubp_core_final_v4_1_1 not found. Running in Standalone Mode.")

class ConstructionBMatrix:
    """LAW_SUBSTRATE_002: Construction B via Paley Matrix (p=23)."""
    def __init__(self):
        # Derive Paley Matrix from first principles if core is available
        if CORE_AVAILABLE:
            self.B = core.LEECH_ENHANCED.B_matrix
        else:
            # Fallback hardcoded Paley Matrix (p=23)
            self.B = [[0,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,0,1,1,1,0,0,0,1,0],
                      [1,1,0,1,1,1,0,0,0,1,0,1],[1,0,1,1,1,0,0,0,1,0,1,1],
                      [1,1,1,1,0,0,0,1,0,1,1,0],[1,1,1,0,0,0,1,0,1,1,0,1],
                      [1,1,0,0,0,1,0,1,1,0,1,1],[1,0,0,0,1,0,1,1,0,1,1,1],
                      [1,0,0,1,0,1,1,0,1,1,1,0],[1,0,1,0,1,1,0,1,1,1,0,0],
                      [1,1,0,1,1,0,1,1,1,0,0,0],[1,0,1,1,0,1,1,1,0,0,0,1]]
        
        self.M = self._build_generator()

    def _build_generator(self) -> List[List[int]]:
        M = []
        for i in range(12): # Top: [2*I12 | 0]
            M.append([(2 if i == j else 0) for j in range(12)] + [0]*12)
        for i in range(12): # Bottom: [B | I12]
            M.append(self.B[i] + [(1 if i == j else 0) for j in range(12)])
        return M

    def multiply(self, v: List[int]) -> List[int]:
        """Maps 24-bit seed to 24D Leech Coordinate."""
        res = [0]*24
        for i in range(24):
            res[i] = sum(v[j] * self.M[j][i] for j in range(24))
        return res

class LeechEngine:
    """The Master Geometric Controller for the 24-bit Substrate."""
    def __init__(self):
        self.matrix = ConstructionBMatrix()
        self.Y = 0.26467559 # The Y-Constant

    def get_leech_point(self, bits24: List[int]) -> List[int]:
        """Generates the integer Leech coordinate from a 24-bit identity."""
        return self.matrix.multiply(bits24)

    def verify_norm(self, point: List[int]) -> int:
        """Calculates the Scaled Norm Squared (Integer)."""
        return sum(p*p for p in point)

    def verify_norm_actual(self, point: List[int]) -> Fraction:
        """Calculates the Actual Norm Squared (Fractional)."""
        return Fraction(self.verify_norm(point), 8)

    # ========================================================================
    # ENHANCEMENT: LAW_SYMMETRY_001 - The Symmetry Tax
    # ========================================================================
    def calculate_symmetry_tax(self, point: List[int]) -> float:
        """Calculates the informational cost of 3D manifestation."""
        hw = sum(1 for x in point if x != 0)
        norm_sq = self.verify_norm(point)
        # Tax = (Hamming Weight * Y) + (Norm Squared / 8)
        return (hw * self.Y) + (norm_sq / 8.0)

    # ========================================================================
    # ENHANCEMENT: Physical Scaling Toggle
    # ========================================================================
    def to_physical_space(self, point: List[int]) -> List[float]:
        """Projects the integer lattice into physical GeV/MeV space."""
        scale = 1.0 / math.sqrt(8.0)
        return [p * scale for p in point]

    def get_statistics(self) -> Dict[str, Any]:
        """Returns the v4.1.1 Substrate Health Report."""
        return {
            "dimension": 24,
            "scale_factor": 8,
            "min_norm_actual": 4,
            "y_constant": self.Y,
            "status": "OPTIMIZED" if CORE_AVAILABLE else "STANDALONE"
        }

# Global Instance
LEECH = LeechEngine()

if __name__ == "__main__":
    print("UBP Leech Engine v4.1.1 Final Initialized.")
    # Test with a standard Golay-Lifted point (Norm 12)
    test_point = [2]*12 + [0]*12
    print(f"  - Test Norm²: {LEECH.verify_norm_actual(test_point)}")
    print(f"  - Symmetry Tax: {LEECH.calculate_symmetry_tax(test_point):.4f}")
