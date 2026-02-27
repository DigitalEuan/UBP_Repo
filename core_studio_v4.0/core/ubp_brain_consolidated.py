"""
================================================================================
UBP BRAIN CONSOLIDATED v3.1 — ENRICHED KB + LEXICON COMMUNICATION
================================================================================
Changes from v3.0:
  - Fixed Vector Extraction: Now searches entry['atlas']['vector'].
  - Fixed NRCI/Tax Extraction: Now searches entry['atlas']['nrci'].
  - Class Name: UBPBrain (Standardized).

Author: Euan R A Craig, New Zealand
Date: February 2026
Version: 3.1
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
from collections import defaultdict, Counter

# Import from UBP Core Foundation
try:
    from ubp_core_v5_3_merged import (
        GOLAY_ENGINE,
        LEECH_ENGINE,
        SUBSTRATE,
        PARTICLE_PHYSICS,
        BinaryLinearAlgebra
    )
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    BinaryLinearAlgebra = None
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
    language: str
    nrci: Fraction
    tax: Fraction
    lexicon: str
    fingerprint: str
    tags: List[str]

    def to_dict(self) -> Dict:
        return {
            "ubp_id": self.ubp_id,
            "name": self.name,
            "vector": self.vector,
            "category": self.category,
            "math": self.math,
            "language": self.language,
            "nrci": str(self.nrci),
            "tax": str(self.tax),
            "lexicon": self.lexicon,
            "fingerprint": self.fingerprint,
            "tags": self.tags
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
    primitive_decomposition: Dict[str, int]
    related_concepts: List[Dict]

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
            "matched_terms": self.matched_terms,
            "primitive_decomposition": self.primitive_decomposition,
            "related_concepts": self.related_concepts
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
        return Fraction(24 - hamming, 24)

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
            "name": name, "domain": domain,
            "params": [p1, p2, p3], "vector": vector,
            "created_at": datetime.now().isoformat()
        }
        self._save_registry()
        return vector

    def _get_domain_bits(self, domain: str) -> List[int]:
        domain_map = {
            "particle": [0, 0, 0, 1], "geometry": [0, 0, 1, 0],
            "physics": [0, 0, 1, 1], "biology": [0, 1, 0, 0],
            "logic": [0, 1, 0, 1], "math": [0, 1, 1, 0],
            "system": [0, 1, 1, 1], "law": [1, 0, 0, 0]
        }
        return domain_map.get(domain.lower(), [0, 0, 0, 0])

    def _gray_encode(self, value: int, bits: int) -> List[int]:
        gray = value ^ (value >> 1)
        return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

# ==============================================================================
# SECTION 4: VECTOR ENGINE
# ==============================================================================

class UBPVectorEngine:
    """Handles vector operations, concept composition, and geometric reasoning."""

    def __init__(self, golay_engine=None, math_engine=None):
        self.golay = golay_engine if golay_engine else self._fallback_golay()
        self.math = math_engine if math_engine else RationalMathEngine()
        self.vector_cache: Dict[str, List[int]] = {}
        self.metrics = {
            'total_vectorizations': 0, 'cache_hits': 0,
            'error_corrections': 0, 'validation_passes': 0,
            'vector_not_found': 0, 'invalid_vector_length': 0
        }

    def _fallback_golay(self):
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()

    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        """Extract 24-bit vector from KB entry, checking 'atlas' first."""
        # 1. Check Atlas (SOP_002 Standard)
        if 'atlas' in entry and isinstance(entry['atlas'], dict):
            vec = entry['atlas'].get('vector')
            if isinstance(vec, list) and len(vec) == 24:
                return vec

        # 2. Check Top Level
        for field_name in ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector

        # 3. Check Nested Data
        if 'data' in entry and isinstance(entry['data'], dict):
            return self._extract_vector(entry['data'])

        return None

    def compose_vectors(self, vectors: List[List[int]], operation: str = 'xor') -> List[int]:
        """Compose multiple vectors."""
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

    def majority_vote(self, vectors: List[List[int]]) -> List[int]:
        """Combine vectors by majority vote — reduces noise."""
        if not vectors:
            return [0] * 24
        result = []
        for i in range(24):
            bits = [v[i] for v in vectors]
            result.append(1 if sum(bits) >= len(bits) / 2 else 0)
        return result

    def coherence_snap(self, vector: List[int]) -> Tuple[List[int], bool, int]:
        """Snap a vector to the nearest valid Golay codeword."""
        if not CORE_AVAILABLE:
            return (vector, False, 0)
        decoded_message, syndrome, weight = self.golay.decode(vector)
        was_corrected = weight > 0
        if was_corrected:
            self.metrics['error_corrections'] += 1
        snapped_vector = self.golay.encode(decoded_message)
        if len(snapped_vector) != 24:
            snapped_vector = (snapped_vector + [0] * 24)[:24]
        return (snapped_vector, was_corrected, weight)

    def hamming_distance(self, v1: List[int], v2: List[int]) -> int:
        return sum(1 for a, b in zip(v1, v2) if a != b)

    def find_neighbors(self, target_vector: List[int], kb: Dict[str, Dict],
                       max_distance: int = 4, limit: int = 10) -> List[Dict]:
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
                    'category': entry.get('category', ''),
                    'distance': dist
                })
        return sorted(neighbors, key=lambda x: x['distance'])[:limit]

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
        self.vector_engine = UBPVectorEngine() # Helper for extraction
        self._load_anchors()

    def _fallback_golay(self):
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()

    def _load_anchors(self):
        """Load anchor concepts from KB — LAW entries and hardened primitives."""
        for ubp_id, entry in self.kb.items():
            vector = self.vector_engine._extract_vector(entry)
            tags = entry.get('tags', [])
            if vector and len(vector) == 24:
                if ('LAW' in ubp_id or 'AXIOM' in ubp_id or
                        'IMPERATIVE' in tags or 'KERNEL' in ubp_id or
                        'HARDENED' in ' '.join(tags)):
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

# ==============================================================================
# SECTION 6: HIERARCHY TRAVERSAL ENGINE
# ==============================================================================

class HierarchyEngine:
    """
    Recursively decomposes KB entries to their absolute primitives.
    """
    COMPONENT_PATTERN = re.compile(r'(\d+)\s*[×xX]\s*([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]+)')
    STANDALONE_PATTERN = re.compile(r'(?<!\d[×xX]\s)(?<!\d[×xX])(?<!\d)\b([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]{3,})\b')

    def __init__(self, kb: Dict[str, Dict]):
        self.kb = kb
        self._cache: Dict[str, Dict[str, int]] = {}

    def parse_math(self, math_str: str) -> Dict[str, int]:
        if not math_str: return {}
        if '|' in math_str:
            math_str = math_str.split('|', 1)[1].strip()
        components: Dict[str, int] = {}
        for mult_str, comp_id in self.COMPONENT_PATTERN.findall(math_str):
            components[comp_id] = components.get(comp_id, 0) + int(mult_str)
        remaining = math_str
        for comp_id in list(components.keys()):
            remaining = remaining.replace(comp_id, '')
        for comp_id in self.STANDALONE_PATTERN.findall(remaining):
            if comp_id not in components:
                components[comp_id] = 1
        junk = {'N', 'Z', 'Tax', 'Mean', 'Dist', 'Snap'}
        return {k: v for k, v in components.items()
                if k not in junk and not k.isdigit() and v > 0}

    def decompose_to_primitives(self, ubp_id: str, depth: int = 0, max_depth: int = 20) -> Dict[str, int]:
        if ubp_id in self._cache: return dict(self._cache[ubp_id])
        if depth > max_depth: return {ubp_id: 1}
        entry = self.kb.get(ubp_id)
        if not entry: return {ubp_id: 1}

        # Check hierarchy field first, then math
        hier = entry.get('atlas', {}).get('hierarchy', '')
        math_str = entry.get('math', '')

        components = self.parse_math(hier) if hier else self.parse_math(math_str)

        if not components or hier == 'absolute_primitive':
            result = {ubp_id: 1}
            self._cache[ubp_id] = result
            return result

        total: Dict[str, int] = {}
        for comp_id, count in components.items():
            sub = self.decompose_to_primitives(comp_id, depth + 1, max_depth)
            for prim_id, prim_count in sub.items():
                total[prim_id] = total.get(prim_id, 0) + prim_count * count
        self._cache[ubp_id] = total
        return dict(total)

    def get_hierarchy_level(self, ubp_id: str) -> int:
        entry = self.kb.get(ubp_id)
        if not entry: return -1
        hier = entry.get('atlas', {}).get('hierarchy', '')
        if hier == 'absolute_primitive': return 0

        components = self.parse_math(entry.get('math', ''))
        if not components: return 0

        max_child = 0
        for comp_id in components:
            child_level = self.get_hierarchy_level(comp_id)
            if child_level > max_child: max_child = child_level
        return max_child + 1

    def find_cross_domain_relatives(self, ubp_id: str, threshold: float = 0.3) -> List[Dict]:
        target_prims = self.decompose_to_primitives(ubp_id)
        if not target_prims: return []
        relatives = []
        for other_id, other_entry in self.kb.items():
            if other_id == ubp_id: continue
            other_prims = self.decompose_to_primitives(other_id)
            if not other_prims: continue
            shared = sum(min(target_prims.get(p, 0), other_prims.get(p, 0)) for p in set(target_prims) | set(other_prims))
            union = sum(max(target_prims.get(p, 0), other_prims.get(p, 0)) for p in set(target_prims) | set(other_prims))
            if union > 0:
                similarity = shared / union
                if similarity >= threshold:
                    relatives.append({
                        'ubp_id': other_id,
                        'name': other_entry.get('name', other_id),
                        'category': other_entry.get('category', ''),
                        'similarity': round(similarity, 3),
                        'shared_primitives': shared
                    })
        return sorted(relatives, key=lambda x: -x['similarity'])[:8]

# ==============================================================================
# SECTION 7: DELTA MEMORY ENGINE
# ==============================================================================

class DeltaMemoryEngine:
    """Memory management, context window, KB growth, and lexicon indexing."""

    def __init__(self):
        self.kb: Dict[str, Dict] = {}
        self.lexicon_index: defaultdict = defaultdict(list)
        self.name_index: Dict[str, str] = {}
        self.short_name_index: Dict[str, str] = {}
        self.context_window: List[Dict] = []
        self.context_max_size = 24
        self.vector_engine = UBPVectorEngine()
        self.stats = {'lexicon_terms': 0, 'kb_entries': 0, 'entries_with_vectors': 0}

    def load_kb(self, paths: List[str]) -> int:
        self.kb = {}
        total_entries = 0
        for path in paths:
            if not os.path.exists(path): continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, dict):
                    # Check if it's a wrapper like {"entries": ...}
                    if 'entries' in data: data = data['entries']
                    elif 'kb' in data: data = data['kb']

                    if isinstance(data, dict):
                        for key, entry in data.items():
                            ubp_id = entry.get('ubp_id', key)
                            if ubp_id: self.kb[ubp_id] = entry
                    elif isinstance(data, list):
                        for entry in data:
                            ubp_id = entry.get('ubp_id')
                            if ubp_id: self.kb[ubp_id] = entry
                elif isinstance(data, list):
                    for entry in data:
                        ubp_id = entry.get('ubp_id')
                        if ubp_id: self.kb[ubp_id] = entry

                total_entries = len(self.kb)
            except Exception as e:
                print(f"[ERROR] Failed to load KB {path}: {e}")

        self._build_lexicon_index()
        self.stats['kb_entries'] = len(self.kb)
        return total_entries

    def _build_lexicon_index(self):
        self.lexicon_index = defaultdict(list)
        self.name_index = {}
        self.short_name_index = {}
        self.stats['entries_with_vectors'] = 0

        for ubp_id, entry in self.kb.items():
            vector = self.vector_engine._extract_vector(entry)
            if vector is None or len(vector) != 24:
                continue
            self.stats['entries_with_vectors'] += 1

            terms = []
            # 1. Lexicon field
            lexicon_field = entry.get('lexicon', '')
            if isinstance(lexicon_field, str):
                parts = re.findall(r'\[([^\]]+)\]', lexicon_field)
                for part in parts:
                    terms.append(part.strip())
                    for word in re.findall(r'\b\w{3,}\b', part.lower()):
                        terms.append(word)

            # 2. Name field (if exists)
            name = entry.get('name', '')
            if name:
                terms.append(name)
                self.name_index[name.lower()] = ubp_id

            # 3. ID parts
            if '_' in ubp_id:
                parts = ubp_id.split('_')
                for p in parts:
                    if len(p) > 2 and not p.isdigit(): terms.append(p)

            # Map terms
            for term in terms:
                if isinstance(term, str) and term.strip():
                    term_clean = term.strip().lower()
                    if term_clean:
                        self.lexicon_index[term_clean].append(ubp_id)

        self.stats['lexicon_terms'] = len(self.lexicon_index)

    def add_to_context(self, entry: Dict):
        self.context_window.append(entry)
        if len(self.context_window) > self.context_max_size:
            self.context_window = self.context_window[-self.context_max_size:]

# ==============================================================================
# SECTION 8: CONSOLIDATED UBP BRAIN (Main Interface)
# ==============================================================================

class UBPBrain:
    """Consolidated UBP Reasoning System v3.1"""

    def __init__(self):
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.math = RationalMathEngine()
        self.architect = ConceptArchitect(self.golay)
        self.vector_engine = UBPVectorEngine(self.golay, self.math)
        self.memory = DeltaMemoryEngine()
        self.dialogue = None
        self.hierarchy = None
        self.initialized = False

    def initialize(self, kb_paths: List[str]):
        print("[UBP Brain v3.1] Initializing...")
        self.memory.load_kb(kb_paths)
        self.dialogue = UBPInnerDialogue(self.golay, self.memory.kb)
        self.hierarchy = HierarchyEngine(self.memory.kb)
        self.initialized = True
        print(f"[UBP Brain v3.1] Initialized: {self.memory.stats['kb_entries']} entries, {self.memory.stats['entries_with_vectors']} vectors.")

    def process_query(self, query: str) -> ReasoningResult:
        # Simple recall for now
        candidates = self.recall(query)

        primary = None
        if candidates:
            top = candidates[0]
            entry = top['entry']
            vec = top['vector']

            # Get NRCI/Tax from Atlas if available
            nrci_val = entry.get('atlas', {}).get('nrci', '1/1')
            tax_val = entry.get('atlas', {}).get('tax', '0/1')

            primary = UBPConcept(
                ubp_id=top['ubp_id'],
                name=entry.get('name', top['ubp_id']),
                vector=vec,
                category=entry.get('category', 'unknown'),
                math=entry.get('math', ''),
                language=entry.get('lexicon', ''),
                nrci=self.math.validate_fraction(nrci_val),
                tax=self.math.validate_fraction(tax_val),
                lexicon=entry.get('lexicon', ''),
                fingerprint=entry.get('fingerprint', ''),
                tags=entry.get('tags', [])
            )

        # Generate response
        response = self._generate_response(query, primary, candidates)

        return ReasoningResult(
            query=query,
            response=response,
            primary_concept=primary,
            reasoning_chain=[],
            final_vector=primary.vector if primary else [0]*24,
            final_nrci=primary.nrci if primary else Fraction(0),
            final_tax=primary.tax if primary else Fraction(0),
            coherence_snap=False,
            warnings=[],
            matched_terms=[],
            primitive_decomposition={},
            related_concepts=[]
        )

    def recall(self, query: str, top_k: int = 5) -> List[Dict]:
        query_lower = query.lower()
        words = re.findall(r'\b\w{3,}\b', query_lower)
        candidates = set()

        for word in words:
            if word in self.memory.lexicon_index:
                candidates.update(self.memory.lexicon_index[word])

        results = []
        for uid in candidates:
            entry = self.memory.kb[uid]
            vec = self.vector_engine._extract_vector(entry)
            if vec:
                score = 0
                if uid.lower() in query_lower: score += 10
                if entry.get('name', '').lower() in query_lower: score += 5
                results.append({'ubp_id': uid, 'entry': entry, 'vector': vec, 'score': score})

        return sorted(results, key=lambda x: -x['score'])[:top_k]

    def _generate_response(self, query, concept, candidates):
        if not concept:
            return f"No concept found for '{query}'."

        lines = [f"**{concept.ubp_id}**"]
        if concept.lexicon: lines.append(f"Lexicon: {concept.lexicon}")
        if concept.math: lines.append(f"Math: {concept.math}")

        if self.hierarchy:
            prims = self.hierarchy.decompose_to_primitives(concept.ubp_id)
            if prims:
                lines.append("Primitives: " + ", ".join([f"{v}x {k}" for k,v in prims.items()]))

        return "\n".join(lines)

if __name__ == "__main__":
    brain = UBPBrain()
    if os.path.exists('ubp_system_kb.json'):
        brain.initialize(['ubp_system_kb.json'])
        print(brain.process_query("hydrogen").response)
