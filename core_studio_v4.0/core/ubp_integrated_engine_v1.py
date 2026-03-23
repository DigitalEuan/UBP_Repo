"""
UBP INTEGRATED ENGINE v2.4 (Holographic Feedback Edition)
=========================================================
The high-level executive layer. 
Bridges the Semantic Brain, the 24D Micro-Core, and the 256D Macro-Bulk.
Automatically triggers high-dimensional unfolding for complex behaviors.
"""

import json
from fractions import Fraction
from typing import Dict, List, Any
from ubp_brain_consolidated import UBPBrain, extract_vector, extract_name, extract_nrci
from ubp_core_v5_3_merged import BinaryLinearAlgebra
from ubp_barnes_wall import BarnesWallEngine

class UBPIntegratedEngine:
    def __init__(self):
        self.brain = UBPBrain()
        self.brain.initialize(['ubp_system_kb.json'])
        self.bw_engine = BarnesWallEngine(dimension=256)
        
        # The Trigger: If 24D NRCI is below this, the object is under tension
        # and requires 256D unfolding to understand its true structure.
        self.COMPLEXITY_THRESHOLD = 0.80 
        
        print(f"[IntegratedEngine] Online. Linked to Brain v5.2 & BW-256 Macro-Auditor.")

    def analyze_query(self, query: str):
        """
        Performs a tri-audit:
        1. Semantic: What does the user mean? (Brain)
        2. Micro-Geometric: How stable is it in 24D? (Core)
        3. Macro-Geometric: How does it fold in 256D? (BW-256, if complex)
        """
        # 1. Resolve via Brain
        result = self.brain.process_query(query)
        
        if not result.ubp_id:
            return {"status": "NULL_RESONANCE", "query": query}

        # 2. Fetch full entry for deep audit
        entry = self.brain.kb_manager.kb[result.ubp_id]
        vector = extract_vector(entry)
        fingerprint = entry.get('fingerprint', '')
        
        micro_nrci_frac = extract_nrci(entry)
        micro_nrci = float(micro_nrci_frac)
        sincerity = result.confidence
        
        response_data = {
            "status": "RESOLVED",
            "ubp_id": result.ubp_id,
            "name": extract_name(entry),
            "confidence": f"{sincerity:.2%}",
            "micro_nrci": micro_nrci,
            "is_hardened": "SOP_002" in entry.get('tags', []),
            "response": result.response
        }

        # 3. The Macro-Trigger (Complex Behavior Detection)
        if micro_nrci < self.COMPLEXITY_THRESHOLD and fingerprint:
            print(f"\n[IntegratedEngine] Complex behavior detected (NRCI {micro_nrci:.4f} < {self.COMPLEXITY_THRESHOLD}). Triggering BW-256 Macro-Audit...")
            
            # Unfold into 256D
            macro_audit = self.bw_engine.audit(result.ubp_id, micro_nrci_frac, fingerprint)
            
            response_data["macro_audit"] = {
                "macro_nrci": macro_audit["macro_nrci"],
                "relative_coherence": f"{macro_audit['relative_coherence']:.2%}",
                "clarity_status": macro_audit["clarity_status"]
            }
        else:
            response_data["macro_audit"] = "Not required (High 24D Stability)"

        return response_data

if __name__ == "__main__":
    engine = UBPIntegratedEngine()
    
    # Test 1: A simple element (High NRCI, no macro-audit needed)
    print("\n--- TEST 1: Simple Element ---")
    print(json.dumps(engine.analyze_query("Tell me about Hydrogen"), indent=2))
    
    # Test 2: A complex behavior (Low NRCI, triggers macro-audit)
    print("\n--- TEST 2: Complex Behavior ---")
    print(json.dumps(engine.analyze_query("What is ATP?"), indent=2))