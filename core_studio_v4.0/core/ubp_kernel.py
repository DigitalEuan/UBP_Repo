#!/usr/bin/env python3
"""
UBP KERNEL v1.2.6 (SCAVENGER SYNC)
==================================

Author: Euan R A Craig, New Zealand
Date: 06 January 2026

"""
import sys
import keyword
import importlib
from typing import List, Any, Tuple

# --- 1. SYSTEM RELOAD PROTOCOL ---
try:
    import hex_dictionary_v4_exact
    importlib.reload(hex_dictionary_v4_exact)
    from hex_dictionary_v4_exact import HEX_DB_EXACT

    import auto_trigger
    importlib.reload(auto_trigger)
    from auto_trigger import HM_KB

    import ubp_tgic_engine
    importlib.reload(ubp_tgic_engine)
    from ubp_tgic_engine import TGICExactEngine

    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, LEECH_ENHANCED
    from ubp_integration_adapter import UBP_INTEGRATION
    from ubp_horizon_monitor import HorizonMonitor
    
    IMPORTS_OK = True
except ImportError as e:
    print(f"[KERNEL PANIC] Critical Import Failed: {e}")
    IMPORTS_OK = False

# --- 2. SUB-COMPONENTS ---
class NativeCortex:
    def __init__(self): self.golay = GOLAY_DECODER
    def _hash_to_vector(self, tag: str) -> List[int]:
        import hashlib
        h = hashlib.sha256(tag.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        corrected, _, _ = self.golay.decode(raw)
        return corrected
    def process_concept(self, concept: Any) -> dict:
        tags, context = ["VOID"], "GENERAL"
        if isinstance(concept, int): 
            tags = ["NUMBER", "EVEN" if concept % 2 == 0 else "ODD"]
            context = "MATH"
        elif isinstance(concept, str):
            if concept in keyword.kwlist: tags, context = ["CODE", "KEYWORD"], "PYTHON"
            else: tags, context = ["WORD", "NOUN" if concept and concept[0].isupper() else "LOWER"], "LANGUAGE"
        return {"SYN": self._hash_to_vector(tags[0]), "SEM": self._hash_to_vector(tags[-1]), "TAGS": tags}

# --- 3. THE KERNEL ---
class UBPKernel:
    def __init__(self):
        self.version = "1.2.6"
        self.status = "INIT"
        self.memory = HEX_DB_EXACT
        self.scanner = HM_KB
        self.cortex = NativeCortex()
        self.monitor = HorizonMonitor()
        self.physics = TGICExactEngine()

    def boot(self):
        print("\n" + "="*60 + f"\n   UBP KERNEL v{self.version} - INITIALIZING\n" + "="*60)
        if not IMPORTS_OK: return
        
        # Load Memory (Scavenger Mode)
        self.memory.load_memory()
        
        count = len(self.memory.registry)
        if count > 0: 
            print(f"   ✅ Memory Online: {count} Laws Mounted.")
        else: 
            print("   ⚠️  Memory Empty. Check 'ubp_system_kb.md' content.")

        UBP_INTEGRATION.initialize()
        self.status = "READY"
        print(f"\n[SYSTEM] {self.status}.\n")

    def query(self, user_input: str):
        print(f">>> INPUT: '{user_input}'")
        
        # Memory Recall Check
        match = self.scanner.scan_and_trigger(user_input)
        if match:
            print(f"[RECALL: {match['ubp_id']}]")
            return

        concept = self.cortex.process_concept(user_input)
        print(f"   Tags: {concept['TAGS']}")
        cost = self.physics.calculate_interaction_cost(concept['SYN'], concept['SEM'])
        print(f"   [REASONER] Syn/Sem Distance: {cost}")

if __name__ == "__main__":
    KERNEL = UBPKernel()
    KERNEL.boot()
    if KERNEL.status == "READY":
        KERNEL.query("Tell me about the law of fractal packing")