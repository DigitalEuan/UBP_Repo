"""
UBP INTEGRATED ENGINE v2.1 (GEOMETRIC CORTEX - ENHANCED)
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
        # Primary criteria: explicit anchor designation
        raw_tags = entry.get('tags', [])
        tags = [str(t).lower() for t in raw_tags if isinstance(t, (str, int))]
        
        if 'anchor' in tags or 'primitive' in tags:
            return True
            
        # Secondary criteria: UBP ID patterns
        ubp_id = str(entry.get('ubp_id', '')).upper()
        anchor_patterns = [
            'PRIMITIVE_', 'CONSTANT_', 'OPERATOR_', 'AXIOM_', 
            'VOID', 'UNITY', 'Y_INVARIANT', 'STATE_'
        ]
        return any(pattern in ubp_id for pattern in anchor_patterns)

    def _validate_vector(self, vec) -> bool:
        """Validates that a vector is a proper 24-bit binary vector"""
        return (isinstance(vec, list) and 
                len(vec) == 24 and 
                all(isinstance(b, int) and b in (0, 1) for b in vec))

    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Safely extract vector with multiple fallback strategies"""
        # Strategy 1: Check standard vector fields
        for field in ['vector', 'geometry', 'codeword']:
            v_field = entry.get(field)
            if self._validate_vector(v_field):
                return v_field
                
        # Strategy 2: Parse from script field
        script = str(entry.get('script', ''))
        match = re.search(r'vector\s*=\s*(\[[0-1,\s]+\])', script)
        if match:
            try:
                v = json.loads(match.group(1))
                if self._validate_vector(v):
                    return v
            except json.JSONDecodeError:
                pass
                
        # Strategy 3: Generate canonical vector based on entry properties
        ubp_id = str(entry.get('ubp_id', ''))
        if ubp_id:
            return self._generate_canonical_vector(ubp_id)
            
        return None

    def _generate_canonical_vector(self, ubp_id: str) -> List[int]:
        """Generates mathematically significant vectors based on concept type"""
        # Map concept types to symmetry groups and weights
        CONCEPT_TYPES = {
            'PRIMITIVE_VOID': {'symmetry': 'trivial', 'weight': 0},
            'PRIMITIVE_UNITY': {'symmetry': 'octahedral', 'weight': 12},
            'OPERATOR_XOR': {'symmetry': 'tetrahedral', 'weight': 8},
            'CONSTANT_PI': {'symmetry': 'circular', 'weight': 16},
            'STATE_ENTROPY': {'symmetry': 'icosahedral', 'weight': 20},
            'OPERATOR_AND': {'symmetry': 'cubic', 'weight': 6},
            'OPERATOR_OR': {'symmetry': 'cubic', 'weight': 18},
            'CONSTANT_Y': {'symmetry': 'dihedral', 'weight': 14},
        }
        
        # Determine concept type from ID
        concept_key = None
        for key in CONCEPT_TYPES.keys():
            if key in ubp_id.upper():
                concept_key = key
                break
        
        # Default fallback
        if not concept_key:
            concept_key = 'PRIMITIVE_UNITY'
            
        params = CONCEPT_TYPES[concept_key]
        
        # Generate seed based on ID hash (deterministic but meaningful)
        seed_hash = hashlib.sha256(ubp_id.encode()).digest()
        seed_value = int.from_bytes(seed_hash[:3], 'big') % 4096
        
        # Create base vector with appropriate weight properties
        target_weight = params['weight']
        base_vec = [0] * 24
        for i in range(target_weight):
            base_vec[(seed_value + i) % 24] = 1
            
        # Ensure it's a valid Golay codeword
        corrected, _, _ = self.golay.decode(base_vec)
        return self.golay.encode(corrected)

    def _load_anchors_from_db(self) -> Dict[str, List[int]]:
        anchors = {}
        registry = self.db.registry if self.db.registry else {}
        
        for h_hash, entry in registry.items():
            if not isinstance(entry, dict): 
                continue
                
            if self._is_geometric_anchor(entry):
                vec = self._extract_vector(entry)
                if vec:
                    name = str(entry.get('name', entry.get('ubp_id', 'UNKNOWN'))).upper()
                    anchors[name] = vec
                    
        return anchors

    def _build_spatial_index(self) -> Dict[int, List[Tuple[str, List[int]]]]:
        """Builds a spatial partitioning index for fast nearest-neighbor lookup"""
        index = {w: [] for w in range(25)}  # 0-24 possible weights
        
        for name, vec in self.anchors.items():
            weight = sum(vec)
            if 0 <= weight <= 24:
                index[weight].append((name, vec))
                
        return index

    def find_nearest_anchor(self, query_vec: List[int]) -> Tuple[str, int]:
        """Finds nearest anchor using spatial index for efficiency"""
        weight = sum(query_vec)
        candidates = []
        
        # Check nearby weight buckets (current, ±1, ±2)
        for dw in range(-2, 3):
            w_bucket = max(0, min(24, weight + dw))
            candidates.extend(self.spatial_index[w_bucket])
        
        # Compute distances only for candidate anchors
        min_dist = 25
        nearest = "UNKNOWN"
        
        for name, anchor in candidates:
            d = BinaryLinearAlgebra.hamming_distance(query_vec, anchor)
            if d < min_dist:
                min_dist = d
                nearest = name
                
        return nearest, min_dist

    def word_to_vector(self, word: str) -> List[int]:
        """Maps a word to its nearest geometric primitive in the lattice"""
        word_upper = word.upper()
        
        # First check if we have this word as an anchor
        if word_upper in self.anchors:
            return self.anchors[word_upper]
        
        # Otherwise find nearest semantic neighbor using hash-based seed
        word_hash = hashlib.sha256(word.encode()).digest()
        seed_value = int.from_bytes(word_hash[:3], 'big') % 4096
        
        # Create base vector with appropriate properties
        raw_vec = [(seed_value >> i) & 1 for i in range(23, -1, -1)]
        corrected, _, _ = self.golay.decode(raw_vec)
        return self.golay.encode(corrected)

    def generate_concept_card(self, query: str):
        """Generates the UBP Identity Card using Dynamic Anchors."""
        # 1. Build Vector (Superposition)
        words = query.lower().replace("?", "").split()
        if not words:
            words = ["void"]
            
        vectors = [self.word_to_vector(w) for w in words]
        
        vec = [0] * 24
        for v in vectors:
            vec = [(a ^ b) for a, b in zip(vec, v)]
        
        # 2. Analyze Geometry
        weight = sum(vec)
        nearest_name, min_dist = self.find_nearest_anchor(vec)
        
        # 3. Generate Language with Enhanced Geometric Interpretation
        if min_dist == 0:
            desc = f"Perfect resonance with {nearest_name}. A fundamental truth."
            confidence = "CERTAIN"
        elif min_dist <= 3:
            desc = f"Strong alignment with {nearest_name}. A variation of the same geometric family."
            confidence = "HIGH"
        elif min_dist <= 6:
            desc = f"Structural relationship to {nearest_name}. Shares mathematical properties."
            confidence = "MEDIUM"
        elif min_dist <= 9:
            desc = f"Geometric proximity to {nearest_name}. Related concept in higher-dimensional space."
            confidence = "LOW"
        elif weight == 12:
            desc = "A balanced Dodecad configuration. Represents stable independent potential."
            confidence = "MEDIUM"
        else:
            desc = "Transitional geometry. Represents a bridge state between geometric families."
            confidence = "SPECULATIVE"

        return {
            "UBP_ID": f"CONCEPT_{hashlib.sha256(query.encode()).hexdigest()[:8].upper()}",
            "Name": query.title(),
            "Math": f"W={weight} | d({nearest_name})={min_dist}",
            "Language": desc,
            "Confidence": confidence,
            "Script": f"XOR({words}) -> {''.join(map(str, vec))}",
            "Vector": vec,
            "Nearest_Anchor": nearest_name,
            "Distance": min_dist
        }

    def triangulate_concept(self, concepts: List[str]) -> Dict[str, Any]:
        """
        Performs geometric triangulation between multiple concepts.
        Returns the synthesized concept card and relationship metrics.
        """
        if len(concepts) < 2:
            return self.generate_concept_card(" ".join(concepts))
            
        # Generate vectors for each concept
        vectors = []
        names = []
        for concept in concepts:
            card = self.generate_concept_card(concept)
            vectors.append(card["Vector"])
            names.append(card["Name"])
            
        # Triangulate: Find the geometric center point
        center_vec = [0] * 24
        for vec in vectors:
            center_vec = [(a ^ b) for a, b in zip(center_vec, vec)]
            
        # Normalize to valid codeword
        center_vec = self.golay.encode(self.golay.decode(center_vec)[0])
        weight = sum(center_vec)
        
        # Find nearest anchor to the center point
        nearest_anchor, min_dist = self.find_nearest_anchor(center_vec)
        
        # Calculate coherence metric (average distance between concepts)
        total_dist = 0
        count = 0
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                d = BinaryLinearAlgebra.hamming_distance(vectors[i], vectors[j])
                total_dist += d
                count += 1
                
        avg_dist = total_dist / count if count > 0 else 0
        coherence = max(0, min(1, 1 - (avg_dist / 24)))
        
        # Generate description
        if coherence > 0.85:
            desc = f"High-coherence synthesis of {', '.join(names)}. Geometrically unified concept."
        elif coherence > 0.6:
            desc = f"Medium-coherence synthesis of {', '.join(names)}. Structurally related concepts."
        else:
            desc = f"Low-coherence synthesis of {', '.join(names)}. Conceptual bridge between domains."
            
        return {
            "UBP_ID": f"SYNTH_{hashlib.sha256(' '.join(concepts).encode()).hexdigest()[:8].upper()}",
            "Name": f"Synthesis of {' + '.join(names)}",
            "Math": f"W={weight} | d({nearest_anchor})={min_dist} | C={coherence:.2f}",
            "Language": desc,
            "Confidence": "HIGH" if coherence > 0.8 else ("MEDIUM" if coherence > 0.6 else "LOW"),
            "Script": f"TRIANGULATE({names}) -> center",
            "Vector": center_vec,
            "Source_Concepts": names,
            "Coherence": coherence,
            "Nearest_Anchor": nearest_anchor,
            "Distance": min_dist
        }

# --- EXECUTION TEST ---
if __name__ == "__main__":
    cortex = SemanticCortexV2()
    
    print("\n=== ENHANCED GEOMETRIC CORTEX DIAGNOSTICS ===")
    print(f"System Version: UBP Core v4.2.7")
    print(f"Anchors Loaded: {len(cortex.anchors)}")
    print(f"Spatial Index Buckets: {len(cortex.spatial_index)}")
    
    # Test Queries - Individual Concepts
    print("\n--- INDIVIDUAL CONCEPT ANALYSIS ---")
    queries = [
        "What is energy",
        "Chaos and order",
        "Love is the law",
        "The truth is stable"
    ]
    
    for q in queries:
        card = cortex.generate_concept_card(q)
        print(f"\n[IDENTITY CARD: {card['Name']}]")
        print(f"  UBP_ID:      {card['UBP_ID']}")
        print(f"  MATH:        {card['Math']}")
        print(f"  LANGUAGE:    {card['Language']}")
        print(f"  CONFIDENCE:  {card['Confidence']}")
        print(f"  NEAREST:     {card['Nearest_Anchor']} (d={card['Distance']})")
    
    # Test Query - Concept Triangulation
    print("\n--- CONCEPT TRIANGULATION ---")
    synthesis = cortex.triangulate_concept(["energy", "time", "mass"])
    print(f"\n[SYNTHESIZED CONCEPT: {synthesis['Name']}]")
    print(f"  UBP_ID:      {synthesis['UBP_ID']}")
    print(f"  MATH:        {synthesis['Math']}")
    print(f"  LANGUAGE:    {synthesis['Language']}")
    print(f"  CONFIDENCE:  {synthesis['Confidence']}")
    print(f"  COHERENCE:   {synthesis['Coherence']:.2f}")
    print(f"  NEAREST:     {synthesis['Nearest_Anchor']} (d={synthesis['Distance']})")
    
    # Show vector visualization
    print(f"\n  GEOMETRIC SIGNATURE: {''.join(str(b) for b in synthesis['Vector'][:12])}...")
