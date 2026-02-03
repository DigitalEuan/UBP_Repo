"""
UBP INTEGRATED ENGINE v2.0 (SELF-AWARE CORTEX)
==============================================
Features:
1. EMBEDDED OBSERVER: Recursive state evaluation via UBPObserver.
2. SELF-STABILIZATION: Rejects queries that violate geometric integrity.
3. METABOLIC COSTING: Calculates energy tax for every operation.

Author: E R A Craig, New Zealand
UBP Research Cortex v4.2.7
Date: 20 January 2026
"""

import hashlib
import re
import json
from typing import Dict, List, Any, Tuple, Optional
from fractions import Fraction
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra, UBPUltimateSubstrate
from hex_dictionary_v4_exact import HEX_DB_EXACT

# --- MODULE 1: THE OBSERVER ---
class UBPObserver:
    def __init__(self, db):
        self.golay = GOLAY_DECODER
        self.db = db
        
        # Constants
        self.Y_inv = UBPUltimateSubstrate.get_constants()['Y_inv']
        self.COHERENCE_THRESHOLD = 0.95
        self.OBSERVATION_COST = UBPUltimateSubstrate.get_constants(50)['Y_inv'] # Fixed tax
        
        # The "Self"
        self.integrity_vector = self._initialize_self_vector()
        print(f"[OBSERVER] Online. Self-Vector Weight: {sum(self.integrity_vector)}")

    def _initialize_self_vector(self) -> List[int]:
        """Generates the System Identity by XORing all known Truths."""
        identity = [0] * 24
        count = 0
        for _, entry in self.db.registry.items():
            vec = entry.get('vector')
            if vec and len(vec) == 24:
                identity = [(a ^ b) for a, b in zip(identity, vec)]
                count += 1
        
        # Ensure Identity is a valid codeword
        corrected, _, _ = self.golay.decode(identity)
        return self.golay.encode(corrected)

    def observe(self, state_vector: List[int]) -> Dict[str, Any]:
        """Measures geometric tension between Input and System Identity."""
        _, _, errors = self.golay.decode(state_vector)
        
        # Local Coherence (Internal Consistency)
        local_coherence = Fraction(4 - min(4, errors), 4)
        
        # Global Alignment (Distance to Self)
        dist_to_self = BinaryLinearAlgebra.hamming_distance(state_vector, self.integrity_vector)
        
        action = "MAINTAIN"
        if local_coherence < 1:
            if errors <= 3:
                action = "CORRECT"
            else:
                action = "RECALIBRATE"

        return {
            "action": action,
            "coherence": float(local_coherence),
            "dist_to_self": dist_to_self,
            "energy_cost": self.OBSERVATION_COST * (Fraction(1, 1) - float(local_coherence))
        }

# --- MODULE 2: THE CORTEX ---
class SemanticCortexV3:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.db = HEX_DB_EXACT
        if not self.db.registry: self.db.load_memory()
        
        # Initialize Observer
        self.observer = UBPObserver(self.db)
        self.anchors = self._load_anchors()

    def _load_anchors(self) -> Dict[str, List[int]]:
        anchors = {}
        for _, entry in self.db.registry.items():
            vec = entry.get('vector')
            if vec:
                name = str(entry.get('name', entry.get('ubp_id', 'UNKNOWN'))).upper()
                anchors[name] = vec
        return anchors

    def word_to_vector(self, word: str) -> List[int]:
        h = hashlib.sha256(word.lower().encode()).digest()
        val = int.from_bytes(h[:3], 'big') % 4096
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        cw, _, _ = self.golay.decode(raw)
        return self.golay.encode(cw)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        The Main Loop:
        1. Vectorize Input
        2. OBSERVE (Check Coherence)
        3. ACT (Generate or Reject)
        """
        print(f"\n[CORTEX] Processing: '{query}'")
        
        # 1. Vectorize
        words = query.lower().replace("?", "").split()
        vec = [0] * 24
        for w in words:
            v = self.word_to_vector(w)
            vec = [(a ^ b) for a, b in zip(vec, v)]
            
        # 2. Observe
        observation = self.observer.observe(vec)
        print(f"  [OBSERVER] Action: {observation['action']} | Coherence: {observation['coherence']:.2f}")
        
        # 3. Act
        if observation['action'] == "RECALIBRATE":
            return {
                "status": "REJECTED",
                "reason": "Geometric Hallucination Detected (Deep Hole)",
                "metrics": observation
            }
            
        if observation['action'] == "CORRECT":
            print("  [CORTEX] Applying Geometric Correction...")
            corrected, _, _ = self.golay.decode(vec)
            vec = self.golay.encode(corrected)
            # Re-observe to confirm fix
            observation = self.observer.observe(vec)
            
        # Find Nearest Anchor
        min_dist = 25
        nearest = "UNKNOWN"
        for name, anchor in self.anchors.items():
            d = BinaryLinearAlgebra.hamming_distance(vec, anchor)
            if d < min_dist:
                min_dist = d
                nearest = name
                
        return {
            "status": "ACCEPTED",
            "concept": query.upper(),
            "vector_hex": hex(int("".join(map(str, vec)), 2)),
            "resonance": {
                "anchor": nearest,
                "distance": min_dist,
                "type": "PERFECT" if min_dist == 0 else "VARIANT"
            },
            "observer_metrics": observation
        }

# --- EXECUTION ---
if __name__ == "__main__":
    cortex = SemanticCortexV3()
    
    # Test 1: Valid Concept
    result = cortex.process_query("Energy Time")
    print(json.dumps(result, indent=2))
    
    # Test 2: Forced Hallucination (Random Noise)
    # We simulate a vector that we know is a Deep Hole (Weight 4, e.g., 111100...)
    print("\n[TEST] Injecting Deep Hole Vector...")
    bad_vec = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    obs = cortex.observer.observe(bad_vec)
    print(f"  Result: {obs['action']} (Coherence {obs['coherence']})")
