"""
================================================================================
UBP PHENOMENOLOGY ENGINE v5.4 (DUAL-MODE)
================================================================================
1. PHENOMENOLOGY (Scanner): Translates Real-World Data -> UBP Substrate.
2. NOUMENOLOGY (Projector): Translates Shadow Intent -> Required Matter.

Updates for v5.4:
- Integrated 'NoumenalProjector' for Shadow Inversion.
- Implements the 'Physics of Will' via the B-Matrix.
- Enforces Observer Threshold (Y) for manifestation.

Author: Euan R A Craig, New Zealand
Date: 24 February 2026
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Callable, Optional
from fractions import Fraction
import hashlib
import json

# Import Core v5.3 Components
try:
    from ubp_integration_adapter import UBP_INTEGRATION
    from ubp_core_v5_3_merged import (
        GOLAY_ENGINE, 
        LEECH_ENGINE, 
        BinaryLinearAlgebra, 
        UBPUltimateSubstrate
    )
    CORE_AVAILABLE = True
except ImportError:
    print("[WARNING] UBP Core not found. Functionality limited.")
    CORE_AVAILABLE = False

# ==============================================================================
# 1. PHENOMENOLOGY LAYER (The Scanner)
# ==============================================================================

@dataclass
class PhenomenonDefinition:
    """Defines how a real-world phenomenon maps to the 24-bit substrate."""
    name: str
    domain: str
    bit_generator: Callable[[Dict[str, Any]], List[int]]
    tags: List[str] = field(default_factory=list)

class PhenomenologyEngine:
    def __init__(self):
        self.adapter = UBP_INTEGRATION if CORE_AVAILABLE else None
        if self.adapter: self.adapter.initialize()

    def process_phenomenon(self, definition: PhenomenonDefinition, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates bits from data and maps to Leech Lattice."""
        print(f"\n[PHENOMENOLOGY] Scanning: {definition.name}")
        
        try:
            bits = definition.bit_generator(data)
            if len(bits) != 24: raise ValueError("Generator must return 24 bits.")
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

        if not self.adapter: return {"status": "ERROR", "message": "Core unavailable."}

        # Process via Core
        core_result = self.adapter.process_point(bits)
        
        # Calculate Stability (Hyperbolic)
        tax = core_result['symmetry_tax']
        stability = Fraction(1, 1) / (Fraction(1, 1) + (tax / Fraction(10, 1)))

        result = {
            "mode": "SCAN",
            "phenomenon": definition.name,
            "vector": bits,
            "metrics": {
                "nrci": float(core_result['nrci']),
                "tax": float(tax),
                "stability": float(stability)
            },
            "hex_id": core_result['hex_id']
        }
        self._print_summary(result)
        return result

    def _print_summary(self, res):
        m = res['metrics']
        print(f"  > Vector:      {''.join(map(str, res['vector']))}")
        print(f"  > Stability:   {m['stability']:.4f} (Tax: {m['tax']:.4f})")
        print(f"  > NRCI:        {m['nrci']:.4f}")
        print(f"  > ID:          {res['hex_id'][:8]}...")

# ==============================================================================
# 2. NOUMENOLOGY LAYER (The Projector)
# ==============================================================================

class NoumenalProjector:
    """
    The Engine of Will.
    Uses the Shadow Inversion Principle (Law of Shadow Inversion) to calculate
    the physical matter required to sustain a specific Noumenal Intent.
    """
    def __init__(self):
        if not CORE_AVAILABLE: raise RuntimeError("Core required for Noumenology.")
        self.golay = GOLAY_ENGINE
        self.leech = LEECH_ENGINE
        # Extract B-Matrix (The Shadow Inverter) from Generator Matrix [I | B]
        self.B = [row[12:] for row in self.golay.G]
        
        # Observer Constants
        c = UBPUltimateSubstrate.get_constants(50)
        self.Y = c['Y']
        self.THRESHOLD = Fraction(1, 2) # Coherence Limit

    def manifest_intent(self, name: str, shadow_bits: List[int]) -> Dict[str, Any]:
        """
        Attempts to manifest a Shadow Intent into Reality.
        Returns the required Matter configuration if stable.
        """
        print(f"\n[NOUMENOLOGY] Projecting: {name}")
        print(f"  > Intent (Shadow): {''.join(map(str, shadow_bits))}")

        if len(shadow_bits) != 12:
            print("  [ERROR] Intent must be exactly 12 bits.")
            return None

        # 1. INVERSION: Calculate Required Matter (Data = Intent * B)
        required_matter = BinaryLinearAlgebra.matrix_vector_multiply(self.B, shadow_bits)
        
        # 2. CONSTRUCTION: Full 24-bit Vector [Matter | Intent]
        full_vector = required_matter + shadow_bits
        
        # 3. AUDIT: Calculate Metrics
        tax = self.leech.calculate_symmetry_tax(full_vector)
        stability = Fraction(1, 1) / (Fraction(1, 1) + (tax / Fraction(10, 1)))
        
        print(f"  > Required Matter: {''.join(map(str, required_matter))}")
        print(f"  > Symmetry Tax:    {float(tax):.4f}")
        print(f"  > Stability:       {float(stability):.4f} (Threshold: {float(self.THRESHOLD)})")

        # 4. THE GATE
        success = stability >= self.THRESHOLD
        status = "MANIFESTED" if success else "REJECTED"
        
        if success:
            print(f"  [RESULT] SUCCESS. The lattice accepts this reality.")
        else:
            print(f"  [RESULT] REJECTED. Entropic Dissolution (Too expensive).")

        return {
            "mode": "PROJECT",
            "name": name,
            "intent": shadow_bits,
            "matter": required_matter,
            "full_vector": full_vector,
            "metrics": {"tax": float(tax), "stability": float(stability)},
            "status": status
        }

# ==============================================================================
# 3. UTILITIES & DEMO
# ==============================================================================

def text_to_12bits(text: str) -> List[int]:
    """Hashes text to 12 bits for Intent generation."""
    h = hashlib.sha256(text.encode()).hexdigest()
    val = int(h[:3], 16) # 12 bits
    return [(val >> i) & 1 for i in range(11, -1, -1)]

if __name__ == "__main__":
    # 1. Scanner Demo
    scanner = PhenomenologyEngine()
    def rgb_gen(d): 
        val = (d['r']<<16)|(d['g']<<8)|d['b']
        return [(val>>i)&1 for i in range(23,-1,-1)]
    
    scanner.process_phenomenon(
        PhenomenonDefinition("Pure Cyan", "Optics", rgb_gen), 
        {"r":0, "g":255, "b":255}
    )

    # 2. Projector Demo
    if CORE_AVAILABLE:
        projector = NoumenalProjector()
        
        # A. Manifest "Order" (Alternating)
        projector.manifest_intent("ORDER", [1,0,1,0,1,0,1,0,1,0,1,0])
        
        # B. Manifest a Concept (e.g., "Truth")
        intent_truth = text_to_12bits("Truth")
        projector.manifest_intent("CONCEPT: Truth", intent_truth)