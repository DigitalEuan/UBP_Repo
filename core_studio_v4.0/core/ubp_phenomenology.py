"""
================================================================================
UBP PHENOMENOLOGY ENGINE v5.3 (CORE COMPATIBLE)
================================================================================
The "Top-Down" Bridge: Translates Real-World Phenomena -> UBP Substrate.

Updates for v5.3:
- Implements Hyperbolic Stability Formula (1 / (1 + Tax/10)) to handle 
  v5.3 Symmetry Tax values (which can be > 1.0).
- Aligned with new Integration Adapter.

Author: Euan R A Craig, New Zealand
Date: 20 February 2026
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Callable, Optional
from fractions import Fraction
import hashlib
import json

# Import the Integration Adapter (Bridges to v5.3 Core)
try:
    from ubp_integration_adapter import UBP_INTEGRATION
    ADAPTER_AVAILABLE = True
except ImportError:
    print("[WARNING] UBP Integration Adapter not found. Core functions disabled.")
    ADAPTER_AVAILABLE = False

# ==============================================================================
# 1. DEFINITION LAYER (The Contract)
# ==============================================================================

@dataclass
class PhenomenonDefinition:
    """
    Defines how a real-world phenomenon maps to the 24-bit substrate.
    """
    name: str
    domain: str  # e.g., "Physics", "Biology", "Color"
    
    # The Logic: How do we turn data into 24 bits?
    # This function takes a data dict and returns a list of 24 ints (0 or 1)
    bit_generator: Callable[[Dict[str, Any]], List[int]]
    
    # Metadata for the Knowledge Base
    tags: List[str] = field(default_factory=list)
    version: str = "5.3"

# ==============================================================================
# 2. EXECUTION LAYER (The Runner)
# ==============================================================================

class PhenomenologyEngine:
    def __init__(self):
        self.adapter = UBP_INTEGRATION if ADAPTER_AVAILABLE else None
        if self.adapter:
            self.adapter.initialize()

    def process_phenomenon(self, definition: PhenomenonDefinition, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        1. Generates bits from the definition.
        2. Maps bits to the Leech Lattice (via Core).
        3. Calculates Metrics (NRCI, Tax).
        4. Returns a full Study Result.
        """
        print(f"\n[PHENOMENOLOGY v5.3] Processing: {definition.name}")
        
        # A. Generate the Substrate Identity (The Bits)
        try:
            bits = definition.bit_generator(data)
            if len(bits) != 24:
                raise ValueError(f"Bit generator produced {len(bits)} bits; expected 24.")
        except Exception as e:
            return {"status": "ERROR", "stage": "Bit Generation", "message": str(e)}

        print(f"  > Substrate Identity: {''.join(map(str, bits))}")

        # B. Process via UBP Core v5.3 (via Adapter)
        if not self.adapter:
            return {"status": "ERROR", "message": "Core Adapter unavailable."}

        # This step calculates NRCI, Coherence, and Symmetry Tax
        core_result = self.adapter.process_point(bits)
        
        if core_result['status'] != 'OK':
            return {"status": "ERROR", "stage": "Core Processing", "message": core_result.get('message')}

        # C. Synthesize the Result (v5.3 Logic)
        tax = core_result['symmetry_tax']
        
        # v5.3 Hyperbolic Stability Formula: 1 / (1 + Tax/10)
        # This handles Tax > 1.0 without clamping to zero.
        one = Fraction(1, 1)
        ten = Fraction(10, 1)
        stability = one / (one + (tax / ten))

        result = {
            "phenomenon": definition.name,
            "domain": definition.domain,
            "input_data": data,
            "substrate_identity": bits,
            "metrics": {
                "nrci": core_result['nrci'], # Ontological Health (MOG Partition)
                "coherence": core_result['coherence_regime'],
                "symmetry_tax": tax,
                "stability_score": stability # Calculated Stability
            },
            "memory": {
                "hex_id": core_result['hex_id'],
                "stored": True
            }
        }
        
        self._print_summary(result)
        return result

    def _print_summary(self, res):
        m = res['metrics']
        print(f"  > NRCI (Health): {m['nrci']:.4f} ({m['coherence']})")
        print(f"  > Symmetry Tax:  {m['symmetry_tax']:.4f}")
        print(f"  > Stability:     {m['stability_score']:.4f}")
        print(f"  > ID:            {res['memory']['hex_id'][:8]}...")
        print(f"[COMPLETE] Phenomenon mapped to Substrate.\n")

# ==============================================================================
# 3. EXAMPLE DEFINITIONS (Standard Library)
# ==============================================================================

def _simple_text_hasher(data: Dict[str, Any]) -> List[int]:
    """Simple utility to turn a string into 24 bits via SHA-256."""
    s = str(data.get('value', ''))
    h = hashlib.sha256(s.encode()).hexdigest()
    # Take first 6 hex chars = 24 bits
    val = int(h[:6], 16)
    return [(val >> i) & 1 for i in range(23, -1, -1)]

# Standard "Text-to-Substrate" Definition
DEF_SEMANTIC_HASH = PhenomenonDefinition(
    name="Semantic Resonance",
    domain="Information",
    bit_generator=_simple_text_hasher,
    tags=["hashing", "text", "semantic"]
)

# ==============================================================================
# 4. MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    engine = PhenomenologyEngine()
    
    # Test 1: Information-First (Semantic Mapping)
    # "What is the geometric shape of the word 'Truth'?"
    engine.process_phenomenon(DEF_SEMANTIC_HASH, {"value": "Truth"})
    
    # Test 2: Custom Definition (e.g., RGB Color Mapping)
    def rgb_to_bits(data):
        # Map R, G, B (0-255) to 8 bits each -> 24 bits
        r, g, b = data['r'], data['g'], data['b']
        combined = (r << 16) | (g << 8) | b
        return [(combined >> i) & 1 for i in range(23, -1, -1)]

    DEF_COLOR = PhenomenonDefinition(
        name="Color Qualia",
        domain="Optics",
        bit_generator=rgb_to_bits,
        tags=["color", "light", "perception"]
    )
    
    # "What is the stability of Pure Cyan?"
    engine.process_phenomenon(DEF_COLOR, {"r": 0, "g": 255, "b": 255})