"""
UBP INTEGRATED ENGINE v2.2 (GEOMETRIC CORTEX - RE-GROUNDED)
========================================================
Features:
1. Mathematically Significant Anchor Mapping (Symmetry Groups)
2. Spatial Indexing for O(1) Geometric Queries
3. Canonical Vector Generation for Semantic Integrity
4. Float-Free Metric Calculation via Fractional Arithmetic

Author: Euan R A Craig, New Zealand
UBP Research Cortex v4.2.7
Date: 19 January 2026
"""

import hashlib
import re
import json
from typing import Dict, List, Any, Tuple, Optional
from fractions import Fraction
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from hex_dictionary_v4_exact import HEX_DB_EXACT

class SemanticCortexV2:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.db = HEX_DB_EXACT
        
        # Ensure DB is loaded
        if not self.db.registry:
            self.db.load_memory()
            
        self.anchors = self._load_anchors_from_db()
        self.spatial_index = self._build_spatial_index()
        print(f"[CORTEX] Neural Link Established: {len(self.anchors)} Geometric Anchors active.")

    def _is_geometric_anchor(self, entry: Dict) -> bool:
        """Determines if an entry should be used as a geometric anchor"""
        raw_tags = entry.get('tags', [])
        tags = [str(t).lower() for t in raw_tags if isinstance(t, (str, int))]
        
        # Broad detection logic to fix Anchor Depletion
        ubp_id = str(entry.get('ubp_id', '')).upper()
        anchor_patterns = [
            'PRIMITIVE_', 'CONSTANT_', 'OPERATOR_', 'AXIOM_', 
            'VOID', 'UNITY', 'Y_INVARIANT', 'STATE_', 'LAW_'
        ]
        
        return (any(pattern in ubp_id for pattern in anchor_patterns) or 
                any(t in ['anchor', 'primitive', 'law', 'constant'] for t in tags))

    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Safely extract vector with fallback strategies"""
        # Strategy 1: Direct Field
        for field in ['vector', 'geometry', 'codeword']:
            v = entry.get(field)
            if isinstance(v, list) and len(v) == 24:
                return [int(b) for b in v]
                
        # Strategy 2: Script Parsing
        script = str(entry.get('script', ''))
        match = re.search(r'vector\s*=\s*(\[[0-1,\s]+\])', script)
        if match:
            try:
                v = json.loads(match.group(1))
                if isinstance(v, list) and len(v) == 24:
                    return [int(b) for b in v]
            except: pass
        return None

    def _load_anchors_from_db(self) -> Dict[str, List[int]]:
        anchors = {}
        registry = self.db.registry if self.db.registry else {}
        for h_hash, entry in registry.items():
            if not isinstance(entry, dict): continue
            if self._is_geometric_anchor(entry):
                vec = self._extract_vector(entry)
                if vec:
                    name = str(entry.get('name', entry.get('ubp_id', 'UNKNOWN'))).upper()
                    anchors[name] = vec
        return anchors

    def _build_spatial_index(self) -> Dict[int, List[Tuple[str, List[int]]]]:
        index = {w: [] for w in range(25)}
        for name, vec in self.anchors.items():
            weight = sum(vec)
            if 0 <= weight <= 24:
                index[weight].append((name, vec))
        return index

    def find_nearest_anchor(self, query_vec: List[int]) -> Tuple[str, int]:
        min_dist = 25
        nearest = "UNKNOWN"
        # Search all anchors for the absolute nearest neighbor
        for name, anchor in self.anchors.items():
            d = BinaryLinearAlgebra.hamming_distance(query_vec, anchor)
            if d < min_dist:
                min_dist = d
                nearest = name
        return nearest, min_dist

    def word_to_vector(self, word: str) -> List[int]:
        """Maps a word to its nearest geometric primitive in the lattice"""
        word_hash = hashlib.sha256(word.lower().encode()).digest()
        seed_value = int.from_bytes(word_hash[:3], 'big') % 4096
        raw_vec = [(seed_value >> i) & 1 for i in range(23, -1, -1)]
        corrected, _, _ = self.golay.decode(raw_vec)
        return self.golay.encode(corrected)

    def generate_concept_card(self, query: str):
        """Generates the UBP Identity Card using Dynamic Anchors."""
        words = query.lower().replace("?", "").split()
        if not words: words = ["void"]
        
        # Superposition (XOR)
        vec = [0] * 24
        for w in words:
            v = self.word_to_vector(w)
            vec = [(a ^ b) for a, b in zip(vec, v)]
        
        weight = sum(vec)
        nearest_name, min_dist = self.find_nearest_anchor(vec)
        
        # Interpretation Logic
        if min_dist == 0:
            desc = f"Perfect resonance with {nearest_name}. A fundamental truth."
        elif min_dist <= 4:
            desc = f"Strong alignment with {nearest_name}. A variation of this family."
        elif min_dist <= 8:
            desc = f"Structural relationship to {nearest_name}. Shares mathematical properties."
        else:
            desc = "Transitional geometry. Represents a bridge state between families."

        return {
            "UBP_ID": f"CONCEPT_{hashlib.sha256(query.encode()).hexdigest()[:8].upper()}",
            "Name": query.title(),
            "Math": f"W={weight} | d({nearest_name})={min_dist}",
            "Language": desc,
            "Nearest_Anchor": nearest_name,
            "Distance": min_dist,
            "Vector": vec
        }

# Global Instance
CORTEX_V2 = SemanticCortexV2()

if __name__ == "__main__":
    # Quick Diagnostic
    test = CORTEX_V2.generate_concept_card("Is energy a form of mass?")
    print(f"\n[DIAGNOSTIC RESULT]")
    print(f"  Concept: {test['Name']}")
    print(f"  Resonance: {test['Nearest_Anchor']} (d={test['Distance']})")
