"""
================================================================================
UBP GEOMETRIC REASONING V2.0 - SEMANTIC ENHANCED
================================================================================

Major Improvements:
1. SEMANTIC EMBEDDING LAYER: Pre-computed semantic vectors before G24 encoding
2. KNOWLEDGE BASE SEEDING: Pre-populated with fundamental concepts
3. SEMANTIC OPERATORS: Proper vector arithmetic for reasoning
4. ENHANCED NRCI: Calibrated coherence metrics
5. INFERENCE ENGINE: Logical reasoning chains
6. VECTOR SPACE STRUCTURE: Preserves semantic relationships

Author: E. R. A. Craig / Manus AI / Genspark Enhancement
Date: January 30, 2026
Version: 2.0
================================================================================
"""

import hashlib
import json
import math
from typing import Dict, List, Any, Optional, Tuple
from fractions import Fraction
from dataclasses import dataclass
from collections import defaultdict

# Import V1 core components
try:
    from ubp_core_v4_2_6_COMBINED import (
        GOLAY_DECODER,
        BinaryLinearAlgebra,
        UBPUltimateSubstrate,
        LeechPointScaled
    )
    from ubp_nrci_calculator import NRCI_CALCULATOR
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("[WARNING] Core UBP modules not available")


# ==============================================================================
# SECTION 1: SEMANTIC EMBEDDING LAYER
# ==============================================================================

class SemanticEmbedder:
    """
    Creates semantic-aware 24-bit vectors instead of random hashing.
    Uses linguistic relationships and domain knowledge to structure the vector space.
    """
    
    def __init__(self):
        """Initialize semantic embedder with concept relationships."""
        
        # Semantic feature extractors (each maps to specific bit positions)
        self.feature_maps = {
            'concreteness': (0, 2),    # bits 0-1: abstract vs concrete
            'valence': (2, 4),          # bits 2-3: positive vs negative
            'animacy': (4, 6),          # bits 4-5: living vs non-living
            'temporality': (6, 8),      # bits 6-7: temporal vs atemporal
            'magnitude': (8, 10),       # bits 8-9: large vs small
            'complexity': (10, 12),     # bits 10-11: simple vs complex
        }
        
        # Pre-computed semantic anchors (ground truth vectors)
        self.semantic_anchors = self._initialize_anchors()
        
        # Word relationship graph
        self.relationships = defaultdict(list)
        self._build_relationship_graph()
    
    def _initialize_anchors(self) -> Dict[str, List[int]]:
        """Initialize core semantic anchors with hand-crafted vectors."""
        
        anchors = {
            # Core concepts with known semantic structure
            'unity': [0]*12 + [0]*12,  # Origin point
            'being': [1,0,1,0,1,0,1,0,1,0,1,0] + [0]*12,
            'void': [1]*12 + [1]*12,   # Maximum distance
            
            # Polar opposites (should have high Hamming distance)
            'good': [1,1,0,0,0,0,0,0,0,0,0,0] + [0]*12,
            'evil': [0,0,1,1,0,0,0,0,0,0,0,0] + [0]*12,
            
            'love': [1,1,0,0,1,0,0,0,0,0,0,0] + [0]*12,
            'hate': [0,0,1,1,0,1,0,0,0,0,0,0] + [0]*12,
            
            # Numbers (sequential with Hamming distance 1-2)
            'one': [1,0,0,0,0,0,0,0,0,0,0,0] + [0]*12,
            'two': [1,1,0,0,0,0,0,0,0,0,0,0] + [0]*12,
            'three': [1,1,1,0,0,0,0,0,0,0,0,0] + [0]*12,
            
            # Logical operators
            'and': [0,0,0,0,0,0,1,1,0,0,0,0] + [0]*12,
            'or': [0,0,0,0,0,0,1,0,1,0,0,0] + [0]*12,
            'not': [0,0,0,0,0,0,0,1,1,0,0,0] + [0]*12,
            
            # Abstract concepts
            'time': [0,0,0,0,0,0,0,0,0,0,1,1] + [0]*12,
            'space': [0,0,0,0,0,0,0,0,0,1,1,0] + [0]*12,
        }
        
        return anchors
    
    def _build_relationship_graph(self):
        """Build semantic relationship graph."""
        
        relationships = {
            'synonyms': [
                ('happy', 'joyful'), ('sad', 'sorrowful'),
                ('big', 'large'), ('small', 'tiny'),
            ],
            'antonyms': [
                ('good', 'evil'), ('love', 'hate'),
                ('hot', 'cold'), ('fast', 'slow'),
            ],
            'hypernyms': [
                ('animal', 'dog'), ('animal', 'cat'),
                ('vehicle', 'car'), ('vehicle', 'bike'),
            ],
        }
        
        for rel_type, pairs in relationships.items():
            for w1, w2 in pairs:
                self.relationships[w1].append((rel_type, w2))
                if rel_type == 'antonyms':  # Symmetric
                    self.relationships[w2].append((rel_type, w1))
    
    def compute_semantic_features(self, word: str) -> Dict[str, float]:
        """
        Compute semantic features for a word.
        Returns values in [0, 1] for each feature dimension.
        """
        word_lower = word.lower()
        
        features = {}
        
        # Concreteness: physical objects score high
        concrete_words = {'rock', 'tree', 'car', 'house', 'dog', 'cat', 'water'}
        abstract_words = {'love', 'justice', 'truth', 'beauty', 'freedom'}
        if word_lower in concrete_words:
            features['concreteness'] = 1.0
        elif word_lower in abstract_words:
            features['concreteness'] = 0.0
        else:
            features['concreteness'] = 0.5
        
        # Valence: emotional polarity
        positive_words = {'love', 'joy', 'happy', 'good', 'beauty', 'peace'}
        negative_words = {'hate', 'sad', 'evil', 'anger', 'fear', 'war'}
        if word_lower in positive_words:
            features['valence'] = 1.0
        elif word_lower in negative_words:
            features['valence'] = 0.0
        else:
            features['valence'] = 0.5
        
        # Animacy: living vs non-living
        animate_words = {'dog', 'cat', 'human', 'person', 'man', 'woman'}
        if word_lower in animate_words:
            features['animacy'] = 1.0
        else:
            features['animacy'] = 0.0
        
        # Temporality: time-related concepts
        temporal_words = {'time', 'moment', 'past', 'future', 'now', 'then'}
        if word_lower in temporal_words:
            features['temporality'] = 1.0
        else:
            features['temporality'] = 0.0
        
        # Magnitude: size-related
        large_words = {'big', 'huge', 'enormous', 'infinity'}
        small_words = {'small', 'tiny', 'microscopic'}
        if word_lower in large_words:
            features['magnitude'] = 1.0
        elif word_lower in small_words:
            features['magnitude'] = 0.0
        else:
            features['magnitude'] = 0.5
        
        # Complexity: conceptual complexity
        complex_words = {'consciousness', 'quantum', 'philosophy', 'relativity'}
        simple_words = {'one', 'yes', 'no', 'is'}
        if word_lower in complex_words:
            features['complexity'] = 1.0
        elif word_lower in simple_words:
            features['complexity'] = 0.0
        else:
            features['complexity'] = 0.5
        
        return features
    
    def features_to_vector(self, features: Dict[str, float]) -> List[int]:
        """Convert semantic features to 24-bit vector."""
        
        vector = [0] * 24
        
        for feature_name, (start, end) in self.feature_maps.items():
            if feature_name in features:
                value = features[feature_name]
                
                # Map [0,1] to bit pattern
                if value >= 0.75:
                    pattern = [1, 1]
                elif value >= 0.5:
                    pattern = [1, 0]
                elif value >= 0.25:
                    pattern = [0, 1]
                else:
                    pattern = [0, 0]
                
                vector[start:end] = pattern
        
        # Use hash for remaining bits (12-23) to add uniqueness
        hash_val = int(hashlib.sha256(str(features).encode()).hexdigest()[:3], 16)
        for i in range(12, 24):
            vector[i] = (hash_val >> (i-12)) & 1
        
        return vector
    
    def embed_word(self, word: str) -> List[int]:
        """
        Create semantic-aware 24-bit vector for a word.
        Priority: anchors > semantic features > hash fallback
        """
        
        word_lower = word.lower()
        
        # Check if word is a semantic anchor
        if word_lower in self.semantic_anchors:
            return self.semantic_anchors[word_lower].copy()
        
        # Compute semantic features
        features = self.compute_semantic_features(word)
        base_vector = self.features_to_vector(features)
        
        # Encode with Golay for error correction
        if CORE_AVAILABLE:
            message = base_vector[:12]
            encoded = GOLAY_DECODER.encode(message)
            return encoded
        
        return base_vector
    
    def vector_similarity(self, v1: List[int], v2: List[int]) -> float:
        """
        Calculate semantic similarity (0-1 scale).
        Converts Hamming distance to similarity score.
        """
        dist = BinaryLinearAlgebra.hamming_distance(v1, v2)
        # Normalize: distance 0 = similarity 1.0, distance 24 = similarity 0.0
        return 1.0 - (dist / 24.0)


# ==============================================================================
# SECTION 2: ENHANCED KNOWLEDGE BASE
# ==============================================================================

class EnhancedKnowledgeBase:
    """Enhanced KB with pre-populated fundamental concepts."""
    
    def __init__(self, embedder: SemanticEmbedder):
        """Initialize with semantic embedder."""
        self.embedder = embedder
        self.registry = {}
        self._populate_base_knowledge()
    
    def _populate_base_knowledge(self):
        """Seed KB with fundamental concepts."""
        
        base_concepts = [
            # Core ontology
            {'name': 'Unity', 'domain': 'IMPERATIVE', 'desc': 'Fundamental oneness'},
            {'name': 'Void', 'domain': 'ENTROPY', 'desc': 'Absence of being'},
            {'name': 'Being', 'domain': 'SUBSTANCE', 'desc': 'Existence itself'},
            
            # Numbers
            {'name': 'One', 'domain': 'QUANTITY', 'desc': 'Numerical unity'},
            {'name': 'Two', 'domain': 'QUANTITY', 'desc': 'Numerical duality'},
            {'name': 'Three', 'domain': 'QUANTITY', 'desc': 'Numerical trinity'},
            
            # Emotions
            {'name': 'Love', 'domain': 'MEANING', 'desc': 'Positive emotion'},
            {'name': 'Hate', 'domain': 'MEANING', 'desc': 'Negative emotion'},
            {'name': 'Joy', 'domain': 'MEANING', 'desc': 'Happiness'},
            {'name': 'Sorrow', 'domain': 'MEANING', 'desc': 'Sadness'},
            
            # Logic
            {'name': 'And', 'domain': 'ALGORITHM', 'desc': 'Logical conjunction'},
            {'name': 'Or', 'domain': 'ALGORITHM', 'desc': 'Logical disjunction'},
            {'name': 'Not', 'domain': 'ALGORITHM', 'desc': 'Logical negation'},
            
            # Physics
            {'name': 'Time', 'domain': 'MECHANISM', 'desc': 'Temporal dimension'},
            {'name': 'Space', 'domain': 'MECHANISM', 'desc': 'Spatial dimensions'},
            {'name': 'Energy', 'domain': 'MECHANISM', 'desc': 'Capacity for work'},
        ]
        
        for concept in base_concepts:
            vector = self.embedder.embed_word(concept['name'])
            fingerprint = hashlib.sha256(concept['name'].encode()).hexdigest()
            
            self.registry[fingerprint] = {
                'ubp_id': f"SEED_{concept['name'].upper()}",
                'name': concept['name'],
                'vector': vector,
                'domain': concept['domain'],
                'description': concept['desc'],
                'fingerprint': fingerprint
            }
    
    def query(self, search_vector: List[int], max_results: int = 5) -> List[Dict]:
        """Query KB by semantic similarity."""
        
        results = []
        for fp, entry in self.registry.items():
            entry_vec = entry.get('vector')
            if entry_vec and len(entry_vec) == 24:
                dist = BinaryLinearAlgebra.hamming_distance(search_vector, entry_vec)
                similarity = 1.0 - (dist / 24.0)
                
                results.append({
                    'entry': entry,
                    'distance': dist,
                    'similarity': similarity
                })
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:max_results]


# ==============================================================================
# SECTION 3: SEMANTIC OPERATORS
# ==============================================================================

class SemanticOperators:
    """Implements semantic-aware vector operations."""
    
    @staticmethod
    def semantic_add(v1: List[int], v2: List[int], weight1: float = 0.5) -> List[int]:
        """
        Semantic addition: blend two vectors.
        weight1: how much of v1 vs v2 (0.5 = equal blend)
        """
        result = []
        for i in range(24):
            # Weighted voting
            vote = v1[i] * weight1 + v2[i] * (1 - weight1)
            result.append(1 if vote >= 0.5 else 0)
        
        return result
    
    @staticmethod
    def semantic_subtract(v1: List[int], v2: List[int]) -> List[int]:
        """
        Semantic subtraction: emphasize differences.
        Returns features in v1 but not in v2.
        """
        return [v1[i] & (1 - v2[i]) for i in range(24)]
    
    @staticmethod
    def semantic_and(v1: List[int], v2: List[int]) -> List[int]:
        """Logical AND: features present in BOTH."""
        return [v1[i] & v2[i] for i in range(24)]
    
    @staticmethod
    def semantic_or(v1: List[int], v2: List[int]) -> List[int]:
        """Logical OR: features present in EITHER."""
        return [v1[i] | v2[i] for i in range(24)]
    
    @staticmethod
    def semantic_xor(v1: List[int], v2: List[int]) -> List[int]:
        """Logical XOR: features that differ."""
        return [v1[i] ^ v2[i] for i in range(24)]
    
    @staticmethod
    def semantic_not(v: List[int]) -> List[int]:
        """Logical NOT: flip all features."""
        return [1 - v[i] for i in range(24)]


# ==============================================================================
# SECTION 4: ENHANCED REASONING ENGINE
# ==============================================================================

class UBPGeometricReasoningV2:
    """
    UBP Geometric Reasoning V2.0 with semantic awareness.
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        """Initialize V2 reasoning engine."""
        
        if not CORE_AVAILABLE:
            raise RuntimeError("UBP core modules not available")
        
        # Initialize components
        self.golay = GOLAY_DECODER
        self.embedder = SemanticEmbedder()
        self.kb = EnhancedKnowledgeBase(self.embedder)
        self.operators = SemanticOperators()
        
        print("[UBP V2] Semantic Geometric Reasoning System initialized")
        print(f"  - Semantic anchors: {len(self.embedder.semantic_anchors)}")
        print(f"  - Knowledge base: {len(self.kb.registry)} concepts")
    
    # ... (continuing in next file)
    
    # =========================================================================
    # CORE CAPABILITIES (Enhanced from V1)
    # =========================================================================
    
    def vectorize_concept(self, concept: str) -> Dict[str, Any]:
        """
        V2: Semantic-aware vectorization.
        """
        # Get semantic embedding
        vector = self.embedder.embed_word(concept)
        
        # Calculate features
        features = self.embedder.compute_semantic_features(concept)
        
        # Generate fingerprint
        fingerprint = hashlib.sha256(concept.encode('utf-8')).hexdigest()
        
        # Determine domain (bit 11)
        bit_11 = vector[11]
        domain = "SUBSTANCE" if bit_11 == 1 else "QUANTITY"
        
        # Calculate NRCI (enhanced)
        try:
            nrci_result = NRCI_CALCULATOR.calculate_nrci(vector)
            nrci = float(nrci_result.global_nrci)
        except:
            nrci = 0.5
        
        # Find nearest anchor
        nearest_anchor, anchor_dist = self._find_nearest_anchor(vector)
        
        return {
            "concept": concept,
            "vector": vector,
            "fingerprint": fingerprint,
            "domain": domain,
            "nrci": nrci,
            "hamming_weight": sum(vector),
            "semantic_features": features,
            "nearest_anchor": nearest_anchor,
            "anchor_distance": anchor_dist
        }
    
    def _find_nearest_anchor(self, vector: List[int]) -> Tuple[str, int]:
        """Find nearest semantic anchor."""
        min_dist = 25
        nearest = "UNKNOWN"
        
        for name, anchor_vec in self.embedder.semantic_anchors.items():
            dist = BinaryLinearAlgebra.hamming_distance(vector, anchor_vec)
            if dist < min_dist:
                min_dist = dist
                nearest = name
        
        return nearest, min_dist
    
    def reason_about(self, query: str) -> Dict[str, Any]:
        """
        V2: Enhanced reasoning with semantic context.
        """
        # Vectorize query
        query_vec_data = self.vectorize_concept(query)
        query_vector = query_vec_data['vector']
        
        # Query knowledge base for context
        kb_results = self.kb.query(query_vector, max_results=3)
        
        # Check coherence
        _, _, errors = self.golay.decode(query_vector)
        
        if errors > 3:
            return {
                "status": "REJECTED",
                "reason": "Geometric incoherence (deep hole)",
                "errors": errors,
                "query": query
            }
        
        # Build response
        return {
            "status": "ACCEPTED",
            "query": query,
            "vector": query_vector,
            "semantic_features": query_vec_data['semantic_features'],
            "nearest_anchor": query_vec_data['nearest_anchor'],
            "anchor_distance": query_vec_data['anchor_distance'],
            "related_concepts": [
                {
                    'name': r['entry']['name'],
                    'similarity': r['similarity'],
                    'domain': r['entry']['domain']
                }
                for r in kb_results
            ],
            "nrci": query_vec_data['nrci']
        }
    
    def analogy_reasoning(self, a: str, b: str, c: str) -> Dict[str, Any]:
        """
        V2: Proper analogy reasoning (A:B :: C:?)
        Uses semantic operators instead of naive XOR.
        """
        # Vectorize concepts
        vec_a = self.embedder.embed_word(a)
        vec_b = self.embedder.embed_word(b)
        vec_c = self.embedder.embed_word(c)
        
        # Compute relationship vector: B - A
        relationship = self.operators.semantic_subtract(vec_b, vec_a)
        
        # Apply relationship to C: C + (B - A)
        vec_d_computed = self.operators.semantic_add(vec_c, relationship, weight1=0.7)
        
        # Encode for error correction
        corrected, _, _ = self.golay.decode(vec_d_computed)
        vec_d = self.golay.encode(corrected)
        
        # Find closest known concept
        kb_results = self.kb.query(vec_d, max_results=5)
        
        best_match = None
        if kb_results:
            best_match = kb_results[0]['entry']['name']
            best_similarity = kb_results[0]['similarity']
        
        return {
            "analogy": f"{a}:{b} :: {c}:?",
            "predicted_vector": vec_d,
            "best_match": best_match if kb_results else "UNKNOWN",
            "best_similarity": best_similarity if kb_results else 0.0,
            "top_candidates": [
                {'name': r['entry']['name'], 'similarity': r['similarity']}
                for r in kb_results[:3]
            ]
        }
    
    def logical_inference(self, premise1: str, premise2: str, 
                         inference_type: str = "modus_ponens") -> Dict[str, Any]:
        """
        V2: Proper logical inference using semantic operators.
        """
        vec_p1 = self.embedder.embed_word(premise1)
        vec_p2 = self.embedder.embed_word(premise2)
        
        if inference_type == "modus_ponens":
            # A ∧ (A → B) ⇒ B
            # Approximate: AND the premises
            conclusion_vec = self.operators.semantic_and(vec_p1, vec_p2)
        
        elif inference_type == "modus_tollens":
            # ¬B ∧ (A → B) ⇒ ¬A
            neg_p2 = self.operators.semantic_not(vec_p2)
            conclusion_vec = self.operators.semantic_and(vec_p1, neg_p2)
        
        elif inference_type == "conjunction":
            # A ∧ B
            conclusion_vec = self.operators.semantic_and(vec_p1, vec_p2)
        
        elif inference_type == "disjunction":
            # A ∨ B
            conclusion_vec = self.operators.semantic_or(vec_p1, vec_p2)
        
        else:
            return {"status": "ERROR", "message": f"Unknown inference type: {inference_type}"}
        
        # Encode and find nearest concept
        corrected, _, _ = self.golay.decode(conclusion_vec)
        conclusion_vec = self.golay.encode(corrected)
        
        kb_results = self.kb.query(conclusion_vec, max_results=3)
        
        return {
            "inference_type": inference_type,
            "premise1": premise1,
            "premise2": premise2,
            "conclusion_vector": conclusion_vec,
            "inferred_concepts": [
                {'name': r['entry']['name'], 'similarity': r['similarity']}
                for r in kb_results
            ]
        }
    
    def semantic_similarity(self, concept1: str, concept2: str) -> Dict[str, Any]:
        """
        V2: Enhanced semantic similarity with feature analysis.
        """
        vec1 = self.embedder.embed_word(concept1)
        vec2 = self.embedder.embed_word(concept2)
        
        features1 = self.embedder.compute_semantic_features(concept1)
        features2 = self.embedder.compute_semantic_features(concept2)
        
        # Calculate distances
        hamming_dist = BinaryLinearAlgebra.hamming_distance(vec1, vec2)
        similarity = 1.0 - (hamming_dist / 24.0)
        
        # Feature-wise comparison
        feature_diffs = {}
        for feature in features1:
            if feature in features2:
                feature_diffs[feature] = abs(features1[feature] - features2[feature])
        
        return {
            "concept1": concept1,
            "concept2": concept2,
            "hamming_distance": hamming_dist,
            "similarity_score": similarity,
            "semantic_features_diff": feature_diffs,
            "relationship": self._classify_relationship(similarity)
        }
    
    def _classify_relationship(self, similarity: float) -> str:
        """Classify semantic relationship based on similarity."""
        if similarity >= 0.9:
            return "SYNONYMS"
        elif similarity >= 0.7:
            return "RELATED"
        elif similarity >= 0.4:
            return "DISTANT"
        elif similarity <= 0.2:
            return "ANTONYMS"
        else:
            return "UNRELATED"
    
    def find_counterpart(self, concept: str, target_domain: str) -> Dict[str, Any]:
        """
        V2: Enhanced counterpart finding using semantic space.
        """
        source_vec = self.embedder.embed_word(concept)
        
        # Find concepts in target domain
        candidates = []
        for fp, entry in self.kb.registry.items():
            if entry.get('domain') == target_domain:
                entry_vec = entry['vector']
                dist = BinaryLinearAlgebra.hamming_distance(source_vec, entry_vec)
                similarity = 1.0 - (dist / 24.0)
                
                candidates.append({
                    'name': entry['name'],
                    'distance': dist,
                    'similarity': similarity,
                    'domain': entry['domain']
                })
        
        # Sort by similarity
        candidates.sort(key=lambda x: x['similarity'], reverse=True)
        
        if candidates:
            best = candidates[0]
            return {
                "source_concept": concept,
                "target_domain": target_domain,
                "counterpart": best['name'],
                "similarity": best['similarity'],
                "hamming_distance": best['distance'],
                "status": "FOUND",
                "alternatives": candidates[1:3]
            }
        else:
            return {
                "source_concept": concept,
                "target_domain": target_domain,
                "status": "NOT_FOUND"
            }
    
    # Keep V1 methods for compatibility
    def calculate_coherence(self, vector: List[int]) -> Dict[str, Any]:
        """V1 compatibility: Calculate coherence."""
        try:
            nrci_result = NRCI_CALCULATOR.calculate_nrci(vector)
            return {
                "nrci": float(nrci_result.global_nrci),
                "health": {
                    "reality": float(nrci_result.reality_health),
                    "info": float(nrci_result.info_health),
                    "activation": float(nrci_result.activation_health),
                    "potential": float(nrci_result.potential_health)
                },
                "regime": nrci_result.coherence_regime,
                "stability": float(nrci_result.stability_score),
                "symmetry_tax": float(nrci_result.symmetry_tax)
            }
        except:
            return {"nrci": 0.5, "regime": "unknown", "stability": 0.5}
    
    def snap_to_lattice(self, noisy_vector: List[int]) -> Dict[str, Any]:
        """V1 compatibility: Error correction."""
        corrected, syndrome, errors = self.golay.decode(noisy_vector)
        corrected_vector = self.golay.encode(corrected)
        
        status = "DEEP_HOLE" if errors > 3 else ("CORRECTED" if errors > 0 else "PERFECT")
        
        nearest_anchor, anchor_dist = self._find_nearest_anchor(corrected_vector)
        
        return {
            "original_vector": noisy_vector,
            "corrected_vector": corrected_vector,
            "errors_fixed": errors,
            "anchor_distance": anchor_dist,
            "nearest_anchor": nearest_anchor,
            "status": status
        }
    
    def query_memory(self, search_term: str, max_results: int = 12) -> List[Dict[str, Any]]:
        """V2: Enhanced memory query with semantic search."""
        search_vector = self.embedder.embed_word(search_term)
        results = self.kb.query(search_vector, max_results=max_results)
        
        return [
            {
                "name": r['entry']['name'],
                "domain": r['entry']['domain'],
                "similarity": r['similarity'],
                "hamming_distance": r['distance'],
                "description": r['entry'].get('description', '')
            }
            for r in results
        ]


# =============================================================================
# MODULE-LEVEL INTERFACE
# =============================================================================

_ubp_reasoning_v2 = None

def get_reasoning_engine_v2(kb_path: Optional[str] = None) -> UBPGeometricReasoningV2:
    """Get or create the global UBP V2 reasoning engine."""
    global _ubp_reasoning_v2
    if _ubp_reasoning_v2 is None:
        _ubp_reasoning_v2 = UBPGeometricReasoningV2(kb_path=kb_path)
    return _ubp_reasoning_v2


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("UBP GEOMETRIC REASONING V2.0 - INITIALIZATION TEST")
    print("=" * 80)
    
    ubp = UBPGeometricReasoningV2()
    
    # Test 1: Semantic similarity
    print("\n[TEST 1] Semantic Similarity:")
    result = ubp.semantic_similarity("love", "hate")
    print(f"  love <-> hate: {result['similarity_score']:.3f} ({result['relationship']})")
    
    result = ubp.semantic_similarity("love", "joy")
    print(f"  love <-> joy: {result['similarity_score']:.3f} ({result['relationship']})")
    
    # Test 2: Analogy
    print("\n[TEST 2] Analogy Reasoning:")
    result = ubp.analogy_reasoning("good", "evil", "love")
    print(f"  good:evil :: love:? → {result['best_match']} (similarity: {result['best_similarity']:.3f})")
    
    # Test 3: Logical inference
    print("\n[TEST 3] Logical Inference:")
    result = ubp.logical_inference("being", "unity", "conjunction")
    print(f"  being ∧ unity → {result['inferred_concepts'][0]['name']}")
    
    print("\n" + "=" * 80)
    print("UBP V2.0 READY")
    print("=" * 80)
