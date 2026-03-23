"""
UBP INTEGRATED ENGINE v3.2 (Composite Scene Edition)
====================================================
The high-level executive layer of the UBP Studio. 
Bridges the Semantic Brain, the 24D Micro-Core, and the 256D Macro-Bulk.

REFINEMENT:
Added 'Composite Query Detection'. If multiple entities are detected in the 
prompt, the engine bypasses the single-vector confidence threshold and 
automatically constructs a multi-object scene for the ViT Eyes.

Author: UBP Research Cortex v4.2.7
Date: 24 March 2026
"""

import json
import hashlib
from fractions import Fraction
from typing import Dict, List, Any
from ubp_brain_consolidated import UBPBrain, extract_vector, extract_name, extract_nrci
from ubp_core_v5_3_merged import BinaryLinearAlgebra, GOLAY_ENGINE
from ubp_barnes_wall import BarnesWallEngine

def hex_to_bw256(hex_str: str) -> list:
    """Converts a 256-bit SHA-256 hash directly into a 256D lattice coordinate."""
    b = bytes.fromhex(hex_str)
    bits = []
    for byte in b:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
    return [x * 2 for x in bits]

class VitEyesEngine:
    """The Visual Cortex of the UBP."""
    def __init__(self):
        self.bw = BarnesWallEngine(dimension=256)
        self.golay = GOLAY_ENGINE

    def _visual_hash(self, vec_24d: List[int]) -> str:
        """Hashes the 'Light' (Vector) rather than the 'DNA' (Math)."""
        vec_str = "".join(map(str, vec_24d))
        return hashlib.sha256(vec_str.encode()).hexdigest()

    def observe_scene(self, objects: List[Dict]) -> Dict[str, Any]:
        if not objects: return {"status": "BLIND"}

        embedded_patches = []
        for obj in objects:
            # Visual Projection
            v_hash = self._visual_hash(obj["vector"])
            macro_point = self.bw.generate(v_hash)
            snapped_macro = self.bw.snap(macro_point)
            macro_nrci = self.bw.calculate_nrci(snapped_macro)
            
            embedded_patches.append({
                "name": obj["name"],
                "visual_nrci": float(macro_nrci)
            })

        # The eye darts to the lowest NRCI (Highest Visual Tension)
        embedded_patches.sort(key=lambda e: e["visual_nrci"])
        
        return {
            "status": "SCENE_OBSERVED",
            "primary_focus": embedded_patches[0],
            "peripheral": embedded_patches[1:]
        }

class UBPIntegratedEngine:
    def __init__(self):
        self.brain = UBPBrain()
        self.brain.initialize(['ubp_system_kb.json'])
        self.bw_engine = BarnesWallEngine(dimension=256)
        self.eyes = VitEyesEngine()
        self.COMPLEXITY_THRESHOLD = 0.80 
        print(f"[IntegratedEngine v3.2] Online. Composite Scene Detection Active.")

    def analyze_query(self, query: str):
        """Performs a Penta-Audit on the query."""
        
        # 1. Detect Explicit Entities (Composite Query Check)
        query_lower = query.lower()
        explicit_uids = set()
        
        # Sort by length to catch "carbon dioxide" before "carbon"
        for name in sorted(self.brain.kb_manager.short_name_index.keys(), key=len, reverse=True):
            if name in query_lower:
                explicit_uids.add(self.brain.kb_manager.short_name_index[name])
                query_lower = query_lower.replace(name, "") # Consume the word
                
        is_composite = len(explicit_uids) > 1

        # 2. Semantic Resolution
        result = self.brain.process_query(query)
        
        # Bailout ONLY if confidence is low AND it's not a composite scene
        if not result.ubp_id or (result.confidence < 0.10 and not is_composite):
            return {"status": "NULL_RESONANCE", "query": query, "response": result.response}

        # 3. Fetch Primary Entry
        primary_uid = result.ubp_id
        # If it's a composite query and the averaged vector missed the explicit targets, force the first target
        if is_composite and primary_uid not in explicit_uids and result.confidence < 0.10:
            primary_uid = list(explicit_uids)[0]

        entry = self.brain.kb_manager.kb[primary_uid]
        true_v24 = extract_vector(entry)
        fingerprint = entry.get('fingerprint', '')
        micro_nrci_frac = extract_nrci(entry)
        
        response_data = {
            "status": "RESOLVED",
            "query": query,
            "primary_subject": extract_name(entry),
            "confidence": f"{result.confidence:.2%}" if not is_composite else "COMPOSITE_SCENE",
            "micro_nrci": float(micro_nrci_frac),
        }

        # 4. Ontological Drift Lens
        if fingerprint and true_v24:
            hash_vec_256 = hex_to_bw256(fingerprint)
            snapped_256 = self.bw_engine.snap(hash_vec_256)
            hash_core_24 = [abs(x)//2 for x in snapped_256[:24]]
            drift = BinaryLinearAlgebra.hamming_distance(true_v24, hash_core_24)
            
            if drift <= 3: ontology = "PHENOMENAL (Physical Matter)"
            elif 11 <= drift <= 13: ontology = "NOUMENAL (Abstract Concept / Math)"
            else: ontology = "TRANSITIONAL (Anomalous State)"
            
            response_data["ontology"] = f"{ontology} [{drift} bits drift]"

        # 5. Macro-Coherence Lens
        if float(micro_nrci_frac) < self.COMPLEXITY_THRESHOLD and fingerprint:
            macro_audit = self.bw_engine.audit(primary_uid, micro_nrci_frac, fingerprint)
            response_data["macro_audit"] = {
                "macro_nrci": macro_audit["macro_nrci"],
                "relative_coherence": f"{macro_audit['relative_coherence']:.2%}",
                "clarity_status": macro_audit["clarity_status"]
            }
        else:
            response_data["macro_audit"] = "Not required (High 24D Stability)"

        # 6. Imagination Sandbox (ViT Eyes)
        scene_objects = []
        if is_composite:
            # Load the explicitly mentioned objects
            for uid in explicit_uids:
                e = self.brain.kb_manager.kb.get(uid)
                if e and extract_vector(e):
                    scene_objects.append({"name": extract_name(e), "vector": extract_vector(e)})
        elif len(result.top_candidates) > 1:
            # Fallback: Load the top semantic associations
            for uid, score in result.top_candidates[:3]:
                e = self.brain.kb_manager.kb.get(uid)
                if e and extract_vector(e):
                    scene_objects.append({"name": extract_name(e), "vector": extract_vector(e)})
        
        if len(scene_objects) > 1:
            vision_report = self.eyes.observe_scene(scene_objects)
            response_data["imagination_sandbox"] = vision_report

        return response_data

if __name__ == "__main__":
    engine = UBPIntegratedEngine()
    
    print("\n" + "="*80)
    print("PENTA-AUDIT TEST (COMPOSITE SCENE EDITION)")
    print("="*80)
    
    query = "Compare the stability of Glucose, ATP, and Water."
    print(f"\nQ: {query}")
    res = engine.analyze_query(query)
    print(json.dumps(res, indent=2))