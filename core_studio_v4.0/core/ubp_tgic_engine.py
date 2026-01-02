"""
UBP TGIC Engine v4.3 (Triad Graph Interaction Constraints)
==========================================================
A standalone module for simulating dynamic interactions between
substrate states. Handles compatibility, flow, and triadic stability.

Dependencies: ubp_core_v4_2_6_COMBINED
"""
from ubp_core_v4_2_6_COMBINED import (
    BinaryLinearAlgebra,
    LEECH_ENHANCED,
    GOLAY_DECODER
)
from fractions import Fraction

class TGICEngine:
    """
    The Physics Engine for Inter-Identity Relations.
    """

    @staticmethod
    def calculate_interaction_cost(state_a: list[int], state_b: list[int]) -> float:
        """
        Calculates the 'Energy Cost' of interaction.
        Cost = Hamming_Distance + Delta_Symmetry_Tax
        """
        # 1. Hamming Distance (The raw bit-switching cost)
        dist = BinaryLinearAlgebra.hamming_distance(state_a, state_b)
        
        # 2. Symmetry Tax Delta (The ontological stress difference)
        tax_a = LEECH_ENHANCED.calculate_symmetry_tax(state_a)
        tax_b = LEECH_ENHANCED.calculate_symmetry_tax(state_b)
        delta_tax = abs(tax_a - tax_b)
        
        return float(dist) + delta_tax

    @staticmethod
    def validate_flow(source: list[int], target: list[int], mode: str = "subset") -> dict:
        """
        Determines if flow from Source -> Target is permissible.
        
        Modes:
        - 'subset': Source bits must be a subset of Target bits (e.g., Blood Donation).
                    Rule: (Source & NOT Target) == 0
        - 'resonance': Hamming Distance must be <= Threshold (e.g., Communication).
        """
        results = {"allowed": False, "reason": "Unknown mode"}
        
        if mode == "subset":
            # Check for 'Antigen' conflict: Source has a 1 where Target has a 0
            conflict_mask = [s & (1 - t) for s, t in zip(source, target)]
            conflicts = sum(conflict_mask)
            
            if conflicts == 0:
                results = {"allowed": True, "conflicts": 0, "type": "Universal Flow"}
            else:
                results = {"allowed": False, "conflicts": conflicts, "type": "Rejection"}
                
        elif mode == "resonance":
            # Law of Relation: d_H < 8 (Wall of Isolation)
            dist = BinaryLinearAlgebra.hamming_distance(source, target)
            if dist < 8:
                results = {"allowed": True, "distance": dist, "type": "Coherent"}
            else:
                results = {"allowed": False, "distance": dist, "type": "Decoherent"}
                
        return results

    @staticmethod
    def analyze_triad(a: list[int], b: list[int], c: list[int]) -> dict:
        """
        Analyzes a 3-body system for stability (Triadic Closure).
        Checks if A-B, B-C, and C-A interactions are all coherent.
        """
        d_ab = BinaryLinearAlgebra.hamming_distance(a, b)
        d_bc = BinaryLinearAlgebra.hamming_distance(b, c)
        d_ca = BinaryLinearAlgebra.hamming_distance(c, a)
        
        # Triangle Inequality Check (Metric Space validation)
        # d_ac <= d_ab + d_bc
        metric_valid = (d_ca <= d_ab + d_bc)
        
        # Stability: Are all links within the "Wall of Isolation" (d < 8)?
        stable_links = sum(1 for d in [d_ab, d_bc, d_ca] if d < 8)
        
        return {
            "distances": [d_ab, d_bc, d_ca],
            "metric_valid": metric_valid,
            "stability_score": stable_links / 3.0,
            "is_stable": stable_links == 3
        }

# Global Instance
TGIC = TGICEngine()