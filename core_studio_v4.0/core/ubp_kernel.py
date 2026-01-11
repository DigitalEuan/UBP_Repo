"""
UBP KERNEL v2.2 (ACTIVE INFERENCE)
==================================
Integrates:
1. NativeCortex V2 (Recursive, Dimensional Integrity)
2. Hybrid Resonance (Jaccard + Hamming)
3. Active Inference (Geometric Truth Filter & Extrapolator)

Author: Euan R. A. Craig, New Zealand
Date: 11 January 2026
"""

import sys
import hashlib
import re
from fractions import Fraction
from typing import List, Dict, Any, Tuple, Optional

# --- CORE DEPENDENCIES ---
try:
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_tgic_engine import TGICExactEngine
    from ubp_horizon_monitor import HorizonMonitor
    IMPORTS_OK = True
except ImportError as e:
    print(f"[KERNEL PANIC] Critical Import Failed: {e}")
    IMPORTS_OK = False

# ... [Include OffBitMOG and NativeCortexV2 classes from previous kernel] ...
# (Assuming these classes are available or imported)

class ActiveInferenceModule:
    """The Geometric Immune System."""
    def __init__(self, db):
        self.golay = GOLAY_DECODER
        self.db = db

    def _vectorize(self, text: str) -> List[int]:
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        seed, _, _ = self.golay.decode(raw)
        return self.golay.encode(seed)

    def _find_nearest(self, vector: List[int]) -> Tuple[Dict, int]:
        best_match = None
        min_dist = 999
        for _, entry in self.db.registry.items():
            uid = entry.get('ubp_id', 'UNKNOWN')
            name = entry.get('name', 'Unknown Law')
            seed_text = f"{uid} {name}"
            v_entry = self._vectorize(seed_text)
            dist = BinaryLinearAlgebra.hamming_distance(vector, v_entry)
            if dist < min_dist:
                min_dist = dist
                best_match = entry
        return best_match, min_dist

    def check_truth(self, statement: str) -> str:
        vec_q = self._vectorize(statement)
        match, dist = self._find_nearest(vec_q)
        
        if not match: return "NO_DATA"
        
        if dist <= 3:
            return f"✅ VERIFIED (t={dist}): Aligns with '{match['name']}'"
        elif dist <= 6:
            return f"⚠️ PLAUSIBLE (t={dist}): Tension with '{match['name']}'"
        elif dist == 12:
            return f"📐 ORTHOGONAL (t=12): Stable Dodecad with '{match['name']}'"
        else:
            return f"⛔ DISSONANT (t={dist}): Violates '{match['name']}'"

class UBPKernelV2_2:
    def __init__(self):
        self.version = "2.2 (Active Inference)"
        self.memory = HEX_DB_EXACT
        self.inference = ActiveInferenceModule(self.memory)
        # ... [Initialize other modules] ...

    def boot(self):
        if not IMPORTS_OK: return
        self.memory.load_memory()
        print(f"[SYSTEM] UBP Kernel v{self.version} Online.")

    def query(self, user_input: str):
        print(f"\n>>> INPUT: '{user_input}'")
        
        # 1. TRUTH CHECK (The Guard Rail)
        truth_status = self.inference.check_truth(user_input)
        print(f"[GEOMETRIC TRUTH] {truth_status}")
        
        # 2. STANDARD PROCESSING (Resonance/Dialogue)
        # ... [Standard logic would go here] ...
        
        return truth_status

if __name__ == "__main__":
    KERNEL = UBPKernelV2_2()
    KERNEL.boot()
    KERNEL.query("The fine structure constant is 137")
