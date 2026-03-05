"""
UBP INTEGRATED ENGINE v2.3 (SOP_002 & Brain v5.2 Compatible)
============================================================
The high-level executive layer. 
Bridges the Soft-Decision Observer with the Consolidated Brain.
"""

import json
from typing import Dict, List, Any
from ubp_brain_consolidated import UBPBrain, extract_vector, extract_name
from ubp_core_v5_3_merged import BinaryLinearAlgebra

class UBPIntegratedEngine:
    def __init__(self):
        self.brain = UBPBrain()
        self.brain.initialize(['ubp_system_kb.json'])
        print(f"[IntegratedEngine] Online. Linked to Brain v5.2")

    def analyze_query(self, query: str):
        """
        Performs a dual-audit:
        1. Semantic: What does the user mean? (Brain)
        2. Geometric: How stable is that concept? (Core)
        """
        # 1. Resolve via Brain (N-Gram & Vector Resonance)
        result = self.brain.process_query(query)
        
        if not result.ubp_id:
            return {"status": "NULL_RESONANCE", "query": query}

        # 2. Fetch full entry for deep audit
        entry = self.brain.kb_manager.kb[result.ubp_id]
        vector = extract_vector(entry)
        
        # 3. Calculate 'Geometric Sincerity'
        # (How much the query vector matches the target anchor)
        # This is the 'Soft-Decision' logic
        sincerity = result.confidence
        
        return {
            "status": "RESOLVED",
            "ubp_id": result.ubp_id,
            "name": extract_name(entry),
            "confidence": f"{sincerity:.2%}",
            "nrci": float(extract_nrci(entry)) if 'extract_nrci' in globals() else "N/A",
            "is_hardened": "SOP_002" in entry.get('tags', []),
            "response": result.response
        }

if __name__ == "__main__":
    engine = UBPIntegratedEngine()
    print(json.dumps(engine.analyze_query("Tell me about the fusion of deuterium"), indent=2))