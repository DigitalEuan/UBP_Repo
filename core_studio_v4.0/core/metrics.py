"""
================================================================================
UBP METRICS SYSTEM - v4.1.1 (PRODUCTION)
================================================================================
Description: The central 'Witness' module. Provides universal constants, 
ontological health metrics, and symmetry tax calculations.
================================================================================
"""
import math
from fractions import Fraction
from typing import List, Dict, Any, Tuple

class UBPConstants:
    """The Alpha-Omega Source of Truth."""
    # LAW_METRIC_001: The Observer Fixed Point
    Y_INV = math.pi + (2.0 / math.pi)  # 3.77820187...
    Y = 1.0 / Y_INV                   # 0.26467559...
    
    # LAW_AXIS_001: Primary Anchors
    ALPHA = 237
    OMEGA = 83
    RESONANCE = 172
    
    # LAW_SUBSTRATE_005: MOG Partition
    LAYER_NAMES = ["Reality", "Info", "Activation", "Potential"]
    BITS_PER_LAYER = 6

class MetricsEngine:
    def __init__(self):
        self.constants = UBPConstants()

    def get_base_cost(self) -> float:
        """Returns the fixed Observer Cost (Y_inv)."""
        return self.constants.Y_INV

    def calculate_nrci(self, syndrome_weight: int) -> float:
        """
        Normalized Resonance Coherence Index.
        NRCI = 1.0 - (Syndrome_Weight / 24.0)
        """
        return 1.0 - (syndrome_weight / 24.0)

    def calculate_ontological_health(self, bits24: List[int]) -> Dict[str, float]:
        """
        LAW_SUBSTRATE_005: Tetradic MOG Partition.
        Calculates the health of the four 6-bit ontological layers.
        """
        if len(bits24) != 24:
            raise ValueError("Input must be exactly 24 bits.")
            
        health = {}
        for i, name in enumerate(self.constants.LAYER_NAMES):
            start = i * self.constants.BITS_PER_LAYER
            end = start + self.constants.BITS_PER_LAYER
            layer_bits = bits24[start:end]
            # Health is the inverse of the local syndrome weight (on-bits)
            on_bits = sum(layer_bits)
            health[name] = 1.0 - (on_bits / 6.0)
            
        health["Global_NRCI"] = sum(health.values()) / 4.0
        return health

    def calculate_symmetry_tax(self, hamming_weight: int, norm_sq_scaled: int) -> float:
        """
        LAW_SYMMETRY_001: The informational cost of 3D manifestation.
        Tax = (HW * Y) + (Norm_Sq / 8)
        """
        return (hamming_weight * self.constants.Y) + (norm_sq_scaled / 8.0)

    def verify_lepton_ratio(self, predicted: float, experimental: float) -> bool:
        """Validates if a ratio falls within the 0.01% Coherence Basin."""
        error = abs(predicted - experimental) / experimental
        return error < 0.0001

# Global Instance for system-wide access
METRICS = MetricsEngine()

if __name__ == "__main__":
    print(f"UBP Metrics v4.1.1 Initialized.")
    print(f"  - Observer Fixed Point: {METRICS.get_base_cost():.8f}")
    print(f"  - Y-Constant: {METRICS.constants.Y:.8f}")
