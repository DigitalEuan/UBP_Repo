"""
UBP INTEGRATED ENGINE v2.2.1 (SOP_002 Compliant)
================================================
FIX: Corrected vector path to entry['atlas']['vector'].
"""

import hashlib
import re
import json
from typing import Dict, List, Any, Tuple
from fractions import Fraction

# UBP Core & Brain Imports
try:
    from ubp_core_v5_3_merged import GOLAY_ENGINE, BinaryLinearAlgebra, UBPUltimateSubstrate
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    # Import the helpers from the brain to ensure path consistency
    from ubp_brain_consolidated import SoftGolayDecoder, extract_vector, extract_name
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Core dependencies missing: {e}")
    CORE_AVAILABLE = False

# --- MODULE 1: THE SOFT OBSERVER ---
class UBPObserverSoft:
    def __init__(self, db):
        self.db = db
        self.soft_decoder = SoftGolayDecoder()
        constants = UBPUltimateSubstrate.get_constants(50)
        self.Y_inv = constants['Y_INV']
        self.OBSERVATION_COST = self.Y_inv
        print(f"[OBSERVER] Soft-Decision Observer Online.")

    def observe(self, analog_vector: List[float]) -> Dict[str, Any]:
        best_codeword, confidence, _ = self.soft_decoder.decode_soft(analog_vector)
        action = "MAINTAIN"
        if confidence < 0.99:
            action = "SOFT_CORRECT" if confidence >= 0.50 else "FORCED_SNAP"

        return {
            "action": action,
            "confidence": float(confidence),
            "snapped_vector": best_codeword,
            "energy_cost": float(self.OBSERVATION_COST * Fraction(int((1.0 - confidence)*1000), 1000))
        }

# --- MODULE 2: THE ANALOG CORTEX ---
class SemanticCortexSoft:
    def __init__(self):
        self.db = HEX_DB_EXACT
        if not self.db.registry: 
            self.db.load_memory()
            
        self.observer = UBPObserverSoft(self.db)
        self.anchors, self.vocab = self._load_anchors_and_vocab()

    def _load_anchors_and_vocab(self) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
        anchors = {}
        vocab = {}
        for _, entry in self.db.registry.items():
            # FIX: Use the helper to find the vector in entry['atlas']['vector']
            vec = extract_vector(entry)
            if vec and len(vec) == 24:
                name = extract_name(entry).upper()
                anchors[name] = vec
                
                # Index words for the vocabulary
                clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
                for word in clean_name.split():
                    if len(word) > 2:
                        vocab[word] = vec
        
        print(f"[CORTEX] Anchored {len(anchors)} memories into Euclidean space.")
        return anchors, vocab

    def word_to_bipolar(self, word: str) -> List[float]:
        if word in self.vocab:
            binary_vec = self.vocab[word]
            return [1.0 if b == 1 else -1.0 for b in binary_vec]
            
        h = hashlib.sha256(word.encode()).digest()
        val = int.from_bytes(h[:3], 'big') % 4096
        raw_binary = [(val >> i) & 1 for i in range(23, -1, -1)]
        return [0.3 if b == 1 else -0.3 for b in raw_binary]

    def process_query(self, query: str) -> Dict[str, Any]:
        words = re.sub(r'[^a-zA-Z0-9\s]', '', query.lower()).split()
        if not words: return {"status": "ERROR", "reason": "Empty query"}
            
        sum_vector = [0.0] * 24
        for w in words:
            bipolar_v = self.word_to_bipolar(w)
            sum_vector = [s + b for s, b in zip(sum_vector, bipolar_v)]
            
        analog_vector = [s / len(words) for s in sum_vector]
        observation = self.observer.observe(analog_vector)
        snapped_binary = observation["snapped_vector"]
        
        min_dist = 24 # Corrected max distance
        nearest = "UNKNOWN"
        for name, anchor in self.anchors.items():
            d = BinaryLinearAlgebra.hamming_distance(snapped_binary, anchor)
            if d < min_dist:
                min_dist = d
                nearest = name
                
        return {
            "status": "ACCEPTED",
            "query": query,
            "resonance": {
                "anchor": nearest,
                "distance": min_dist,
                "confidence": f"{observation['confidence']:.2%}"
            },
            "action": observation["action"]
        }

if __name__ == "__main__":
    if CORE_AVAILABLE:
        cortex = SemanticCortexSoft()
        # Test with the specific term you asked about
        print(json.dumps(cortex.process_query("What is the purpose of ubppy?"), indent=2))