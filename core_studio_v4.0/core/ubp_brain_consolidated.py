#!/usr/bin/env python3
"""
================================================================================
UBP BRAIN CONSOLIDATED v2 - FIXED VECTOR RETRIEVAL
================================================================================
FIX: Robust vector extraction from KB entries with multiple field name support
     Added debugging to trace vector retrieval issues

Author: Euan R A Craig, New Zealand
Date: 17 February 2026
Version: 2 (Grok X AI ubp V5 assisted)
================================================================================
"""

from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any, Set
from datetime import datetime
import json
import hashlib
import os
import re

# Import from UBP Core Foundation
try:
    from ubp_core_v5_3_merged import (
        GOLAY_ENGINE,
        LEECH_ENGINE,
        SUBSTRATE,
        PARTICLE_PHYSICS
    )
    CORE_AVAILABLE = True
    print("[UBP Brain] UBP Core v5.3 FOUND - Full functionality enabled")
except ImportError:
    CORE_AVAILABLE = False
    print("[WARNING] UBP Core v5.3 not found. Running in fallback mode.")

# ==============================================================================
# SECTION 1: DATA STRUCTURES
# ==============================================================================

@dataclass
class UBPConcept:
    """A single concept in the UBP ontology."""
    ubp_id: str
    name: str
    vector: List[int]
    category: str
    math: str
    nrci: Fraction
    tax: Fraction
    lexicon: List[str]
    fingerprint: str
    
    def to_dict(self) -> Dict:
        return {
            "ubp_id": self.ubp_id,
            "name": self.name,
            "vector": self.vector,
            "category": self.category,
            "math": self.math,
            "nrci": str(self.nrci),
            "tax": str(self.tax),
            "lexicon": self.lexicon,
            "fingerprint": self.fingerprint
        }

@dataclass
class ThoughtStep:
    """A single step in the reasoning chain."""
    concept: UBPConcept
    operation: str
    coherence: Fraction
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "concept": self.concept.to_dict(),
            "operation": self.operation,
            "coherence": str(self.coherence),
            "timestamp": self.timestamp
        }

@dataclass
class ReasoningResult:
    """Complete result of a reasoning operation."""
    query: str
    response: str
    primary_concept: Optional[UBPConcept]
    reasoning_chain: List[ThoughtStep]
    final_vector: List[int]
    final_nrci: Fraction
    final_tax: Fraction
    coherence_snap: bool
    warnings: List[str]
    matched_terms: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "response": self.response,
            "primary_concept": self.primary_concept.to_dict() if self.primary_concept else None,
            "reasoning_chain": [s.to_dict() for s in self.reasoning_chain],
            "final_vector": self.final_vector,
            "final_nrci": str(self.final_nrci),
            "final_tax": str(self.final_tax),
            "coherence_snap": self.coherence_snap,
            "warnings": self.warnings,
            "matched_terms": self.matched_terms
        }

# ==============================================================================
# SECTION 2: RATIONAL MATH ENGINE
# ==============================================================================

class RationalMathEngine:
    """Float-free mathematical operations for UBP."""
    
    def __init__(self):
        self.precision_threshold = Fraction(1, 1000000)
    
    def calculate_nrci(self, vector: List[int], reference_vector: Optional[List[int]] = None) -> Fraction:
        """Calculate Normalized Resonance Coherence Index."""
        if reference_vector is None:
            reference_vector = [0] * 24
        
        hamming = sum(1 for a, b in zip(vector, reference_vector) if a != b)
        nrci = Fraction(24 - hamming, 24)
        return nrci
    
    def calculate_tax(self, operations: int, depth: int) -> Fraction:
        """Calculate ontological tax (friction)."""
        base_tax = Fraction(1, 1000)
        op_tax = Fraction(operations, 10000)
        depth_tax = Fraction(depth, 5000)
        return base_tax + op_tax + depth_tax
    
    def validate_fraction(self, value: Any) -> Fraction:
        """Ensure a value is a Fraction."""
        if isinstance(value, Fraction):
            return value
        elif isinstance(value, (int, float)):
            return Fraction(value).limit_denominator(1000000)
        elif isinstance(value, str) and '/' in value:
            try:
                n, d = value.split('/')
                return Fraction(int(n), int(d))
            except:
                return Fraction(1, 1)
        elif isinstance(value, str):
            try:
                return Fraction(float(value)).limit_denominator(1000000)
            except:
                return Fraction(1, 1)
        else:
            return Fraction(1, 1)

# ==============================================================================
# SECTION 3: CONCEPT ARCHITECT
# ==============================================================================

class ConceptArchitect:
    """Mints new concepts with valid Golay vectors."""
    
    def __init__(self, golay_engine=None):
        self.golay = golay_engine if golay_engine else self._fallback_golay()
        self.registry = {}
        self.registry_file = 'ubp_rational_memory.json'
        self._load_registry()
    
    def _fallback_golay(self):
        """Minimal Golay encoder if core not available."""
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()
    
    def _load_registry(self):
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    self.registry = json.load(f)
            except:
                self.registry = {}
    
    def _save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def mint(self, name: str, domain: str, p1: int, p2: int, p3: int = 0) -> List[int]:
        """Mint a new concept with a valid Golay vector."""
        dom_bits = self._get_domain_bits(domain)
        p1_bits = self._gray_encode(p1, 3)
        p2_bits = self._gray_encode(p2, 5)
        p3_bits = [p3 & 1]
        
        msg = dom_bits + p1_bits + p2_bits + p3_bits
        msg = (msg + [0] * 12)[:12]
        
        vector = self.golay.encode(msg)
        
        self.registry[name] = {
            "name": name,
            "domain": domain,
            "params": [p1, p2, p3],
            "vector": vector,
            "created_at": datetime.now().isoformat()
        }
        self._save_registry()
        
        return vector
    
    def _get_domain_bits(self, domain: str) -> List[int]:
        domain_map = {
            "particle": [0, 0, 0, 1],
            "geometry": [0, 0, 1, 0],
            "physics": [0, 0, 1, 1],
            "biology": [0, 1, 0, 0],
            "logic": [0, 1, 0, 1],
            "math": [0, 1, 1, 0],
            "system": [0, 1, 1, 1],
            "law": [1, 0, 0, 0]
        }
        return domain_map.get(domain.lower(), [0, 0, 0, 0])
    
    def _gray_encode(self, value: int, bits: int) -> List[int]:
        gray = value ^ (value >> 1)
        return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

# ==============================================================================
# SECTION 4: VECTOR ENGINE (FIXED)
# ==============================================================================

class UBPVectorEngine:
    """Handles vector operations, concept composition, and geometric reasoning."""
    
    def __init__(self, golay_engine=None, math_engine=None):
        self.golay = golay_engine if golay_engine else self._fallback_golay()
        self.math = math_engine if math_engine else RationalMathEngine()
        self.vector_cache: Dict[str, List[int]] = {}
        self.concept_clusters: Dict[str, List[str]] = {}
        self.metrics = {
            'total_vectorizations': 0,
            'cache_hits': 0,
            'error_corrections': 0,
            'validation_passes': 0,
            'vector_not_found': 0,
            'invalid_vector_length': 0
        }
    
    def _fallback_golay(self):
        """Minimal Golay encoder if core not available."""
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()
    
    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Extract vector from KB entry with multiple field name support."""
        vector_field_names = ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']
        
        for field_name in vector_field_names:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
                elif isinstance(vector, list) and len(vector) != 24:
                    print(f"[DEBUG] Vector field '{field_name}' found but length={len(vector)} (expected 24)")
                    return None
        
        if 'data' in entry and isinstance(entry['data'], dict):
            return self._extract_vector(entry['data'])
        
        return None
    
    def word_to_vector(self, word: str, lexicon_index: Dict[str, str], kb: Dict[str, Dict]) -> Optional[List[int]]:
        """Map a word to its 24-bit vector with robust error handling."""
        self.metrics['total_vectorizations'] += 1
        word_lower = word.lower()
        
        if word_lower in self.vector_cache:
            self.metrics['cache_hits'] += 1
            return self.vector_cache[word_lower]
        
        if word_lower not in lexicon_index:
            self.metrics['vector_not_found'] += 1
            return None
        
        ubp_id = lexicon_index[word_lower]
        
        if ubp_id not in kb:
            print(f"[DEBUG] ubp_id '{ubp_id}' not found in KB for word '{word}'")
            self.metrics['vector_not_found'] += 1
            return None
        
        entry = kb[ubp_id]
        vector = self._extract_vector(entry)
        
        if vector is None:
            print(f"[DEBUG] No valid vector found in entry {ubp_id} for word '{word}'")
            print(f"[DEBUG] Entry keys: {list(entry.keys())[:10]}")
            self.metrics['invalid_vector_length'] += 1
            return None
        
        if len(vector) != 24:
            print(f"[DEBUG] Vector length={len(vector)} for {ubp_id} (expected 24)")
            self.metrics['invalid_vector_length'] += 1
            return None
        
        self.vector_cache[word_lower] = vector
        self.metrics['validation_passes'] += 1
        
        return vector
    
    def compose_vectors(self, vectors: List[List[int]], operation: str = 'xor') -> List[int]:
        """Compose multiple vectors into a single result."""
        if not vectors:
            return [0] * 24
        
        result = vectors[0].copy()
        
        for vec in vectors[1:]:
            if operation == 'xor':
                result = [(a ^ b) for a, b in zip(result, vec)]
            elif operation == 'and':
                result = [(a & b) for a, b in zip(result, vec)]
            elif operation == 'or':
                result = [(a | b) for a, b in zip(result, vec)]
            elif operation == 'add':
                result = [(a + b) % 2 for a, b in zip(result, vec)]
        
        return result
    
    def coherence_snap(self, vector: List[int]) -> Tuple[List[int], bool, int]:
        """
        FIXED v1.3: Snap a vector to the nearest valid Golay codeword.
        Returns 24-bit codeword (not 12-bit message).
        """
        if not CORE_AVAILABLE:
            return (vector, False, 0)
        
        # Decode returns (12-bit message, syndrome, weight)
        decoded_message, syndrome, weight = self.golay.decode(vector)
        was_corrected = weight > 0
        
        if was_corrected:
            self.metrics['error_corrections'] += 1
        
        # CRITICAL FIX: Re-encode the 12-bit message back to 24-bit codeword
        snapped_vector = self.golay.encode(decoded_message)
        
        # Ensure we return 24 bits
        if len(snapped_vector) != 24:
            snapped_vector = (snapped_vector + [0] * 24)[:24]
        
        return (snapped_vector, was_corrected, weight)
    
    def hamming_distance(self, v1: List[int], v2: List[int]) -> int:
        """Calculate Hamming distance between two vectors."""
        return sum(1 for a, b in zip(v1, v2) if a != b)
    
    def find_neighbors(self, target_vector: List[int], kb: Dict[str, Dict], max_distance: int = 3) -> List[Dict]:
        """Find all concepts within Hamming distance of target."""
        neighbors = []
        for ubp_id, entry in kb.items():
            entry_vector = self._extract_vector(entry)
            if entry_vector is None or len(entry_vector) != 24:
                continue
            dist = self.hamming_distance(target_vector, entry_vector)
            if dist <= max_distance:
                neighbors.append({
                    'ubp_id': ubp_id,
                    'name': entry.get('name', ''),
                    'distance': dist
                })
        return sorted(neighbors, key=lambda x: x['distance'])

# ==============================================================================
# SECTION 5: INNER DIALOGUE
# ==============================================================================

class UBPInnerDialogue:
    """Reflexive deliberation system."""
    
    def __init__(self, golay_engine=None, kb: Dict[str, Dict] = None):
        self.golay = golay_engine if golay_engine else self._fallback_golay()
        self.kb = kb if kb else {}
        self.anchors: Dict[str, List[int]] = {}
        self.threshold = 3
        self.max_iterations = 12
        self._load_anchors()
    
    def _fallback_golay(self):
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()
    
    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Extract vector from KB entry."""
        vector_field_names = ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']
        for field_name in vector_field_names:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
        return None
    
    def _load_anchors(self):
        """Load anchor concepts from KB."""
        for ubp_id, entry in self.kb.items():
            vector = self._extract_vector(entry)
            tags = entry.get('tags', [])
            
            if vector and len(vector) == 24:
                if ('LAW' in ubp_id or 'AXIOM' in ubp_id or 
                    'IMPERATIVE' in tags or 'KERNEL' in ubp_id):
                    self.anchors[ubp_id] = vector
        
        print(f"[Dialogue] Loaded {len(self.anchors)} anchor concepts")
    
    def deliberate(self, query_vector: List[int], max_steps: int = 6) -> Tuple[str, Fraction]:
        """Perform reflexive deliberation on a query vector."""
        if len(query_vector) != 24:
            return ("UNKNOWN", Fraction(24, 24))
        
        current_vec = query_vector.copy()
        best_name = "UNKNOWN"
        best_cost = Fraction(24, 24)
        
        for step in range(max_steps):
            closest_anchor = None
            closest_dist = 25
            
            for anchor_name, anchor_vec in self.anchors.items():
                dist = sum(1 for a, b in zip(current_vec, anchor_vec) if a != b)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_anchor = anchor_name
            
            if closest_anchor is None:
                break
            
            cost = Fraction(closest_dist, 24)
            
            if cost < best_cost:
                best_cost = cost
                best_name = closest_anchor
            
            if closest_dist <= self.threshold:
                break
            
            anchor_vec = self.anchors[closest_anchor]
            reflexive_vec = [(a ^ b) for a, b in zip(current_vec, anchor_vec)]
            
            if CORE_AVAILABLE:
                insight, _, _ = self.golay.decode(reflexive_vec)
                current_vec = self.golay.encode(insight)
            else:
                current_vec = reflexive_vec
        
        return best_name, best_cost
    
    def validate_coherence(self, vector: List[int]) -> Tuple[bool, str]:
        """Validate if a vector is coherent enough for output."""
        if len(vector) != 24:
            return (False, "Invalid vector length")
        
        for anchor_name, anchor_vec in self.anchors.items():
            dist = sum(1 for a, b in zip(vector, anchor_vec) if a != b)
            if dist <= self.threshold:
                return (True, f"Coherent with {anchor_name}")
        
        if CORE_AVAILABLE:
            _, syndrome, weight = self.golay.decode(vector)
            if weight <= self.threshold:
                return (True, f"Within correction radius (weight={weight})")
            else:
                return (False, f"Exceeds correction radius (weight={weight})")
        
        return (True, "Fallback validation")

# ==============================================================================
# SECTION 6: DELTA MEMORY ENGINE (FIXED)
# ==============================================================================

from collections import defaultdict  # ADDED for multi-valued lexicon

class DeltaMemoryEngine:
    """Memory management, context window, KB growth, AND LEXICON INDEXING."""
    
    def __init__(self):
        self.kb: Dict[str, Dict] = {}
        self.lexicon_index: defaultdict = defaultdict(list)  # FIXED: multi-valued
        self.context_window: List[Dict] = []
        self.context_max_size = 24
        self.kb_paths: List[str] = []
        self.pending_changes: List[Dict] = []
        self.stats = {
            'lexicon_terms': 0,
            'kb_entries': 0,
            'lexicon_build_time': 0,
            'entries_with_vectors': 0,
            'entries_without_vectors': 0
        }
    
    def load_kb(self, paths: List[str]) -> int:
        """Load knowledge base from one or more files."""
        self.kb_paths = paths
        self.kb = {}
        total_entries = 0
        
        for path in paths:
            if not os.path.exists(path):
                print(f"[WARNING] KB file not found: {path}")
                continue
            
            entries_loaded = 0
            try:
                if path.endswith('.txt'):
                    entries_loaded = self._parse_kb_text(path)
                elif path.endswith('.json'):
                    entries_loaded = self._parse_kb_json(path)
                
                print(f"[INFO] Loaded KB from {path}: {entries_loaded} entries")
                total_entries += entries_loaded
                
            except Exception as e:
                print(f"[ERROR] Failed to load KB {path}: {e}")
                import traceback
                traceback.print_exc()
        
        # BUILD LEXICON INDEX FROM KB ENTRIES
        self._build_lexicon_index()
        
        self.stats['kb_entries'] = len(self.kb)
        return total_entries
    
    def _parse_kb_text(self, path: str) -> int:
        """Parse text-format KB."""
        count = 0
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        pattern = r'"([a-f0-9]+)"\s*:\s*(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
        matches = re.findall(pattern, content)
        
        for fingerprint, entry_str in matches:
            try:
                entry = json.loads(entry_str)
                ubp_id = entry.get('ubp_id', fingerprint)
                if ubp_id:
                    self.kb[ubp_id] = entry
                    count += 1
            except json.JSONDecodeError:
                continue
        
        return count
    
    def _parse_kb_json(self, path: str) -> int:
        """Parse JSON-format KB."""
        count = 0
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle nested structure (e.g., {"objects": {...}})
        if isinstance(data, dict):
            if 'objects' in data:
                data = data['objects']
            elif 'kb' in data:
                data = data['kb']
            elif 'entries' in data:
                data = data['entries']
            
            for key, entry in data.items():
                if isinstance(entry, dict):
                    ubp_id = entry.get('ubp_id', key)
                    if ubp_id:
                        self.kb[ubp_id] = entry
                        count += 1
        
        return count
    
    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Extract vector from KB entry."""
        vector_field_names = ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']
        for field_name in vector_field_names:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
        return None
    
    def _build_lexicon_index(self):
        """
        FIXED: Build lexicon index FROM KB entries with vector validation.
        Only index entries that have valid 24-bit vectors.
        Uses defaultdict(list) for multi-valued mapping.
        """
        import time
        start_time = time.time()
        
        self.lexicon_index = defaultdict(list)
        self.stats['entries_with_vectors'] = 0
        self.stats['entries_without_vectors'] = 0
        
        for ubp_id, entry in self.kb.items():
            # CRITICAL FIX: Only index entries with valid vectors
            vector = self._extract_vector(entry)
            if vector is None or len(vector) != 24:
                self.stats['entries_without_vectors'] += 1
                continue  # Skip entries without valid vectors
            
            self.stats['entries_with_vectors'] += 1
            
            # Extract all searchable terms from this entry
            terms = []
            
            # 1. Get "lexicon" field
            lexicon_field = entry.get('lexicon', [])
            if isinstance(lexicon_field, list):
                terms.extend(lexicon_field)
            elif isinstance(lexicon_field, str):
                terms.extend([t.strip().strip('[]') for t in lexicon_field.split(',')])
            
            # 2. Get "tags" field
            tags_field = entry.get('tags', [])
            if isinstance(tags_field, list):
                terms.extend(tags_field)
            
            # 3. Get "name" field
            name = entry.get('name', '')
            if name:
                terms.append(name)
                terms.append(name.lower())
            
            # 4. Get "category" field
            category = entry.get('category', '')
            if category:
                terms.append(category)
                for part in category.split('.'):
                    terms.append(part)
            
            # Map all terms to this ubp_id (append to list)
            for term in terms:
                if isinstance(term, str) and term.strip():
                    term_clean = term.strip().lower()
                    term_clean = term_clean.strip('[]')
                    if term_clean:
                        self.lexicon_index[term_clean].append(ubp_id)  # FIXED: append instead of overwrite
        
        self.stats['lexicon_terms'] = len(self.lexicon_index)
        self.stats['lexicon_build_time'] = time.time() - start_time
        
        print(f"[INFO] Built lexicon index: {len(self.lexicon_index)} terms")
        print(f"[INFO] Entries with valid vectors: {self.stats['entries_with_vectors']}")
        print(f"[INFO] Entries without vectors: {self.stats['entries_without_vectors']}")
    
    def add_to_context(self, entry: Dict):
        """Add an entry to the context window."""
        self.context_window.append(entry)
        if len(self.context_window) > self.context_max_size:
            self.context_window = self.context_window[-self.context_max_size:]
    
    def get_context(self) -> str:
        """Get current context as a string."""
        if not self.context_window:
            return ""
        
        context_parts = []
        for entry in self.context_window[-6:]:
            if 'concept' in entry and entry['concept'] and 'name' in entry['concept']:
                context_parts.append(entry['concept']['name'])
        
        return ", ".join(context_parts)
    
    def propose_change(self, new_entry: Dict) -> Dict:
        """Propose a new KB entry."""
        ubp_id = new_entry.get('ubp_id', '')
        existing = self.kb.get(ubp_id, None)
        
        delta = {
            'ubp_id': ubp_id,
            'action': 'update' if existing else 'create',
            'new_entry': new_entry,
            'existing_entry': existing,
            'requires_acceptance': True,
            'timestamp': datetime.now().isoformat()
        }
        
        self.pending_changes.append(delta)
        return delta
    
    def accept_change(self, ubp_id: str) -> bool:
        """Accept a pending change and commit to KB."""
        for i, delta in enumerate(self.pending_changes):
            if delta['ubp_id'] == ubp_id:
                self.kb[ubp_id] = delta['new_entry']
                self.pending_changes.pop(i)
                self._build_lexicon_index()
                return True
        return False
    
    def reject_change(self, ubp_id: str) -> bool:
        """Reject a pending change."""
        for i, delta in enumerate(self.pending_changes):
            if delta['ubp_id'] == ubp_id:
                self.pending_changes.pop(i)
                return True
        return False
    
    def save_kb(self, path: Optional[str] = None) -> bool:
        """Save KB to disk."""
        save_path = path or self.kb_paths[0] if self.kb_paths else 'ubp_system_kb_hardened_complete.json'
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.kb, f, indent=2, ensure_ascii=False)
            print(f"[INFO] Saved KB to {save_path}: {len(self.kb)} entries")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save KB: {e}")
            return False
# ==============================================================================
# SECTION 7: CONSOLIDATED UBP BRAIN (Main Interface)
# ==============================================================================

class UBPBrain:
    """Consolidated UBP Reasoning System."""
    
    def __init__(self, config_path: str = 'rational_cortex.json'):
        self.config = self._load_config(config_path)
        
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.math = RationalMathEngine()
        self.architect = ConceptArchitect(self.golay)
        self.vector_engine = UBPVectorEngine(self.golay, self.math)
        self.dialogue = None
        self.memory = DeltaMemoryEngine()
        
        self.initialized = False
        self.stats = {
            'queries_processed': 0,
            'concepts_minted': 0,
            'kb_entries': 0,
            'coherence_snaps': 0,
            'lexicon_terms': 0
        }
    
    def _load_config(self, path: str) -> Dict:
        """Load system configuration."""
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    config = json.load(f)
                    if config:
                        return config
            except:
                pass
        
        return {
            'max_reasoning_steps': 6,
            'coherence_threshold': 3,
            'context_window_size': 24,
            'auto_snap': True
        }
    
    def initialize(self, kb_paths: List[str], lexicon_path: Optional[str] = None) -> bool:
        """Initialize the brain with KB and lexicon."""
        print("[UBP Brain] Initializing...")
        
        entries_loaded = self.memory.load_kb(kb_paths)
        
        if entries_loaded == 0:
            print("[WARNING] No KB entries loaded. System will operate in minimal mode.")
        
        self.dialogue = UBPInnerDialogue(self.golay, self.memory.kb)
        
        self.stats['kb_entries'] = len(self.memory.kb)
        self.stats['lexicon_terms'] = self.memory.stats['lexicon_terms']
        self.initialized = True
        
        print(f"[UBP Brain] Initialized with {self.stats['kb_entries']} KB entries")
        print(f"[UBP Brain] Lexicon index: {self.stats['lexicon_terms']} searchable terms")
        
        return True
    
    def debug_vector_lookup(self, word: str) -> Dict:
        """DEBUG: Trace vector lookup for a specific word."""
        result = {
            'word': word,
            'word_lower': word.lower(),
            'in_lexicon': word.lower() in self.memory.lexicon_index,
            'ubp_ids': None,
            'in_kb': False,
            'vectors': None,
            'vector_lengths': None,
            'entry_keys': []
        }
        
        candidates = self.memory.lexicon_index.get(word.lower(), [])
        result['ubp_ids'] = candidates
        
        vectors = []
        lengths = []
        entry_keys_set = set()  # Use set to avoid unhashable issues
        for ubp_id in candidates:
            if ubp_id in self.memory.kb:
                result['in_kb'] = True
                entry = self.memory.kb[ubp_id]
                entry_keys_set.update(list(entry.keys())[:15])
                
                vector = self.vector_engine._extract_vector(entry)
                if vector:
                    vectors.append(vector)
                    lengths.append(len(vector))
        
        result['vectors'] = vectors
        result['vector_lengths'] = lengths
        result['entry_keys'] = list(entry_keys_set)
        
        return result
    
    def process_query(self, query: str) -> ReasoningResult:
        """Process a natural language query - FIXED v1.7"""
        self.stats['queries_processed'] += 1
        warnings = []
        reasoning_chain = []
        matched_terms = set()  # Use set for unique terms
        
        # Step 1: Tokenize and lookup vectors
        words = re.findall(r'\b\w+\b', query.lower())
        vectors = []
        found_words = []
        found_concepts = []
        
        for word in words:
            candidates = self.memory.lexicon_index.get(word, [])
            top_candidates = candidates[:3]  # Limit to top 3 to avoid noise
            
            for ubp_id in top_candidates:
                if ubp_id in self.memory.kb:
                    entry = self.memory.kb[ubp_id]
                    vec = self.vector_engine._extract_vector(entry)
                    if vec:
                        vectors.append(vec)
                        found_words.append(word)
                        matched_terms.add(word)  # unique add
                        
                        # FIXED: Further enhanced scoring with atlas priority (assume atlas entries have ubp_id starting with 'PARTICLE_' or category 'particle.*')
                        category = entry.get('category', '').lower()
                        is_atlas = ubp_id.startswith('PARTICLE_') or ubp_id.startswith('PHYS_') or 'atlas' in ubp_id.lower()
                        score = 50 if is_atlas else \
                                30 if category.startswith('particle') or category.startswith('physics') else \
                                20 if word == entry.get('name', '').lower() else \
                                15 if 'particle' in category or 'physics' in category else \
                                10 if word in category else \
                                5 if word in entry.get('name', '').lower() else \
                                3 if any(word in str(t).lower() for t in entry.get('lexicon', [])) else 1
                        
                        found_concepts.append({
                            'ubp_id': ubp_id,
                            'entry': entry,
                            'vector': vec,
                            'score': score
                        })
        
        if not vectors:
            return ReasoningResult(
                query=query,
                response=f"No known concepts found in query. Try: 'electron', 'golay', 'prime', 'binary'",
                primary_concept=None,
                reasoning_chain=[],
                final_vector=[0] * 24,
                final_nrci=Fraction(0, 1),
                final_tax=Fraction(1, 1),
                coherence_snap=False,
                warnings=["No lexicon matches"],
                matched_terms=[]
            )
        
        # Step 2: Compose vectors (use majority vote for binary vectors to reduce noise)
        if len(vectors) > 1:
            composed_vector = []
            for i in range(24):
                bits = [v[i] for v in vectors]
                composed_vector.append(1 if sum(bits) >= len(bits)/2 else 0)  # >= for tie-breaking towards 1
            # Early snap to valid codeword
            composed_vector, _, _ = self.vector_engine.coherence_snap(composed_vector)
        else:
            composed_vector = vectors[0]
        
        # Step 3: Coherence snap
        snapped_vector, was_corrected, syndrome_weight = self.vector_engine.coherence_snap(composed_vector)
        
        if was_corrected:
            self.stats['coherence_snaps'] += 1
            self.vector_engine.metrics['error_corrections'] += 1  # Increment metric
            warnings.append(f"Vector corrected (syndrome weight: {syndrome_weight})")
        
        self.vector_engine.metrics['total_vectorizations'] += 1  # Increment
        self.vector_engine.metrics['validation_passes'] += 1 if not was_corrected else 0
        
        # Step 4: Inner dialogue
        anchor_name, coherence_cost = self.dialogue.deliberate(
            snapped_vector,
            max_steps=self.config.get('max_reasoning_steps', 6)
        )
        
        # Record reasoning steps
        for i, concept_data in enumerate(found_concepts):
            entry = concept_data['entry']
            vector = concept_data['vector']
            concept = UBPConcept(
                ubp_id=concept_data['ubp_id'],
                name=entry.get('name', found_words[i]),
                vector=vector,
                category=entry.get('category', 'unknown'),
                math=entry.get('math', ''),
                nrci=self.math.validate_fraction(entry.get('nrci', '1/1')),
                tax=self.math.validate_fraction(entry.get('tax', '0/1')),
                lexicon=entry.get('lexicon', []),
                fingerprint=entry.get('fingerprint', '')
            )
            reasoning_chain.append(ThoughtStep(
                concept=concept,
                operation='lookup',
                coherence=self.math.calculate_nrci(vector)
            ))
        
        # Step 5: Calculate final metrics
        # Domain-specific reference vector (average from matching categories)
        ref_vectors = [c['vector'] for c in found_concepts if 'particle' in c['entry'].get('category', '') or 'physics' in c['entry'].get('category', '')]
        ref_vector = [0] * 24 if not ref_vectors else [sum(bits) // len(ref_vectors) for bits in zip(*ref_vectors)]
        final_nrci = self.math.calculate_nrci(snapped_vector, ref_vector)
        final_tax = self.math.calculate_tax(len(matched_terms), len(reasoning_chain))  # Use unique terms for ops
        
        # Step 6: Validate coherence
        is_valid = True
        validation_msg = "Valid"
        
        # Check vector length BEFORE validation
        if len(snapped_vector) != 24:
            is_valid = False
            validation_msg = f"Invalid vector length: {len(snapped_vector)}"
            warnings.append(validation_msg)
            print(f"[DEBUG] snapped_vector length: {len(snapped_vector)}")
            print(f"[DEBUG] snapped_vector: {snapped_vector}")
        else:
            is_valid, validation_msg = self.dialogue.validate_coherence(snapped_vector)
            if not is_valid:
                warnings.append(validation_msg)
        
        # Step 7: Get primary concept - Prioritize by score
        primary_concept = None
        if found_concepts:
            found_concepts.sort(key=lambda x: x['score'], reverse=True)
            match = found_concepts[0]
            entry = match['entry']
            vector = match['vector']
            if vector and len(vector) == 24:
                primary_concept = UBPConcept(
                    ubp_id=match['ubp_id'],
                    name=entry.get('name', match['ubp_id']),
                    vector=vector,
                    category=entry.get('category', 'unknown'),
                    math=entry.get('math', ''),
                    nrci=self.math.validate_fraction(entry.get('nrci', '1/1')),
                    tax=self.math.validate_fraction(entry.get('tax', '0/1')),
                    lexicon=entry.get('lexicon', []),
                    fingerprint=entry.get('fingerprint', '')
                )
        
        # PRIORITY 2: Only use anchor if no direct match found
        if primary_concept is None:
            if anchor_name and anchor_name != "UNKNOWN" and anchor_name in self.memory.kb:
                entry = self.memory.kb[anchor_name]
                vector = self.vector_engine._extract_vector(entry)
                if vector and len(vector) == 24:
                    primary_concept = UBPConcept(
                        ubp_id=anchor_name,
                        name=entry.get('name', anchor_name),
                        vector=vector,
                        category=entry.get('category', 'unknown'),
                        math=entry.get('math', ''),
                        nrci=self.math.validate_fraction(entry.get('nrci', '1/1')),
                        tax=self.math.validate_fraction(entry.get('tax', '0/1')),
                        lexicon=entry.get('lexicon', []),
                        fingerprint=entry.get('fingerprint', '')
                    )
                    warnings.append(f"No direct match, using anchor '{anchor_name}'")
        
        # After getting primary_concept, validate against anchors
        if primary_concept:
            # Check if direct match is coherent with any anchor
            anchor_validated = False
            for anchor_name, anchor_vec in self.dialogue.anchors.items():
                dist = sum(1 for a, b in zip(primary_concept.vector, anchor_vec) if a != b)
                if dist <= 3:  # Within Golay correction radius
                    anchor_validated = True
                    warnings.append(f"Validated against anchor: {anchor_name}")
                    break
        
            if not anchor_validated:
                warnings.append("Direct match not anchored (may be novel concept)")
        # Step 8: Add to context
        self.memory.add_to_context({
            'query': query,
            'concept': primary_concept.to_dict() if primary_concept else None,
            'vector': snapped_vector,
            'nrci': str(final_nrci)
        })
        
        # Step 9: Generate response
        response = self._generate_response(
            query,
            primary_concept,
            final_nrci,
            is_valid,
            found_words
        )
        
        return ReasoningResult(
            query=query,
            response=response,
            primary_concept=primary_concept,
            reasoning_chain=reasoning_chain,
            final_vector=snapped_vector,
            final_nrci=final_nrci,
            final_tax=final_tax,
            coherence_snap=was_corrected,
            warnings=warnings,
            matched_terms=list(matched_terms)  # Convert back to list for output
        )
    
    def _generate_response(self, query: str, concept: Optional[UBPConcept],
                          nrci: Fraction, is_valid: bool, words: List[str]) -> str:
        """Generate natural language response."""
        
        if not concept:
            return f"Query processed. No stable concept anchor found. NRCI: {nrci}"
        
        validity_msg = "Coherent" if is_valid else "Unstable"
        
        response = f"[{validity_msg}] {concept.name}"
        
        if concept.math and concept.math != 'atomic':
            response += f" | {concept.math}"
        
        response += f" | NRCI: {nrci}"
        
        if concept.lexicon:
            lex_preview = concept.lexicon[:3] if isinstance(concept.lexicon, list) else []
            if lex_preview:
                response += f" | Also: {', '.join(lex_preview)}"
        
        return response
    
    def mint_concept(self, name: str, domain: str, p1: int, p2: int, p3: int = 0,
                    math: str = "", lexicon: List[str] = None) -> Dict:
        """Mint a new concept."""
        vector = self.architect.mint(name, domain, p1, p2, p3)
        
        ubp_id = f"CONCEPT_{name.upper().replace(' ', '_')}"
        fingerprint = hashlib.sha256(f"{name}{math}{vector}".encode()).hexdigest()
        
        entry = {
            'ubp_id': ubp_id,
            'name': name,
            'category': f"custom.{domain}",
            'vector': vector,
            'math': math,
            'nrci': '1/1',
            'tax': '0/1',
            'lexicon': lexicon or [name],
            'fingerprint': fingerprint
        }
        
        delta = self.memory.propose_change(entry)
        self.stats['concepts_minted'] += 1
        
        return {
            'status': 'pending_acceptance',
            'ubp_id': ubp_id,
            'vector': vector,
            'delta': delta
        }
    
    def accept_concept(self, ubp_id: str) -> bool:
        """Accept a minted concept."""
        result = self.memory.accept_change(ubp_id)
        if result:
            self.stats['kb_entries'] = len(self.memory.kb)
            self.stats['lexicon_terms'] = self.memory.stats['lexicon_terms']
        return result
    
    def save_kb(self, path: Optional[str] = None) -> bool:
        """Save current KB."""
        return self.memory.save_kb(path)
    
    def get_stats(self) -> Dict:
        """Get system statistics."""
        return {
            **self.stats,
            'vector_engine_metrics': self.vector_engine.metrics,
            'pending_changes': len(self.memory.pending_changes),
            'context_size': len(self.memory.context_window)
        }
    
    def export_session(self, path: str) -> bool:
        """Export current session state."""
        session = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.get_stats(),
            'context': self.memory.context_window,
            'pending_changes': self.memory.pending_changes
        }
        
        try:
            with open(path, 'w') as f:
                json.dump(session, f, indent=2)
            return True
        except:
            return False
    
    def import_session(self, path: str) -> bool:
        """Import a previous session state."""
        if not os.path.exists(path):
            return False
        
        try:
            with open(path, 'r') as f:
                session = json.load(f)
            
            self.memory.context_window = session.get('context', [])
            self.memory.pending_changes = session.get('pending_changes', [])
            return True
        except:
            return False

# ==============================================================================
# SECTION 8: MAIN (Test & Demo)
# ==============================================================================

def main():
    """Test and demonstrate the consolidated UBP Brain."""
    print("=" * 80)
    print("UBP BRAIN CONSOLIDATED v1.2 - TEST SUITE (FIXED VECTOR RETRIEVAL)")
    print("=" * 80)
    
    brain = UBPBrain()
    
    # Initialize with KB files
    kb_paths = ['ubp_system_kb_hardened_complete.json', 'ubp_atlas.json']
    brain.initialize(kb_paths)
    
    # DEBUG: Show vector lookup for 'electron'
    print("\n" + "=" * 80)
    print("DEBUG: Vector Lookup for 'electron'")
    print("=" * 80)
    debug_result = brain.debug_vector_lookup('electron')
    for key, value in debug_result.items():
        print(f"  {key}: {value}")
    
    # Show lexicon samples
    print("\n" + "=" * 80)
    print("LEXICON INDEX SAMPLE")
    print("=" * 80)
    sample_terms = list(brain.memory.lexicon_index.keys())[:20]
    print(f"First 20 indexed terms: {sample_terms}")
    
    # Test queries
    test_queries = [
        "electron",
        "golay",
        "prime",
        "binary",
        "particle",
        "logic"
    ]
    
    print("\n" + "=" * 80)
    print("PROCESSING TEST QUERIES")
    print("=" * 80 + "\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        result = brain.process_query(query)
        print(f"Response: {result.response}")
        print(f"NRCI: {result.final_nrci} | Tax: {result.final_tax}")
        print(f"Matched Terms: {result.matched_terms}")
        print(f"Coherence Snap: {result.coherence_snap}")
        if result.warnings:
            print(f"Warnings: {', '.join(result.warnings)}")
        print("-" * 80)
    
    # Show stats
    print("\n" + "=" * 80)
    print("SYSTEM STATISTICS")
    print("=" * 80)
    stats = brain.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)
    print("UBP BRAIN CONSOLIDATED v1.2 - TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()