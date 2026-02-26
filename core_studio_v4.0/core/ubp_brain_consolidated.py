"""
================================================================================
UBP BRAIN CONSOLIDATED v3.0 — ENRICHED KB + LEXICON COMMUNICATION
================================================================================
Changes from v2:
  - Loads ubp_system_kb_enriched.json (670 entries: particles, elements, molecules,
    crystals, reactions, tools, algorithms, laws, beliefs)
  - Proper lexicon-based recall using [Name], [Description] format
  - Language field support for richer natural language responses
  - Hierarchy traversal: recursive decomposition to absolute primitives
  - FOM (Frame of Mind) context weighting for belief entries
  - Cross-domain primitive similarity detection
  - Improved _generate_response using language + lexicon fields

Author: Euan R A Craig, New Zealand (v3.0 updates: UBP Build System)
Date: February 2026
Version: 3.0
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
    print("[UBP Brain v3] UBP Core v5.3 FOUND - Full functionality enabled")
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
        """Extract 24-bit vector from KB entry."""
        for field_name in ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
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
        self._load_anchors()

    def _fallback_golay(self):
        class FallbackGolay:
            def encode(self, msg: List[int]) -> List[int]:
                return (msg + [0] * 24)[:24]
            def decode(self, vec: List[int]) -> Tuple[List[int], List[int], int]:
                return (vec, [0] * 24, 0)
        return FallbackGolay()

    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        for field_name in ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
        return None

    def _load_anchors(self):
        """Load anchor concepts from KB — LAW entries and hardened primitives."""
        for ubp_id, entry in self.kb.items():
            vector = self._extract_vector(entry)
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

    def validate_coherence(self, vector: List[int]) -> Tuple[bool, str]:
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
# SECTION 6: HIERARCHY TRAVERSAL ENGINE
# ==============================================================================

class HierarchyEngine:
    """
    Recursively decomposes KB entries to their absolute primitives.
    Primitives are entries with no sub-components in their math field
    (e.g. quarks, electrons, photons).
    """

    # Pattern to match "2×ELEM_H_001" or "2xELEM_H_001" or "1×PARTICLE_PROTON_001"
    COMPONENT_PATTERN = re.compile(
        r'(\d+)\s*[×xX]\s*([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]+)'
    )
    # Also match standalone IDs (count=1)
    STANDALONE_PATTERN = re.compile(
        r'(?<!\d[×xX]\s)(?<!\d[×xX])(?<!\d)\b([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]{3,})\b'
    )

    def __init__(self, kb: Dict[str, Dict]):
        self.kb = kb
        self._cache: Dict[str, Dict[str, int]] = {}

    def parse_math(self, math_str: str) -> Dict[str, int]:
        """Parse a math string into {component_id: count} dict."""
        # Strip the "Z=1 N=0 | " prefix if present
        if '|' in math_str:
            math_str = math_str.split('|', 1)[1].strip()

        components: Dict[str, int] = {}

        # Find "N×ID" patterns
        for mult_str, comp_id in self.COMPONENT_PATTERN.findall(math_str):
            components[comp_id] = components.get(comp_id, 0) + int(mult_str)

        # Find standalone IDs (no multiplier = count 1)
        # Remove already-found IDs from the string first
        remaining = math_str
        for comp_id in list(components.keys()):
            remaining = remaining.replace(comp_id, '')
        for comp_id in self.STANDALONE_PATTERN.findall(remaining):
            if comp_id not in components:
                components[comp_id] = 1

        # Filter junk
        junk = {'N', 'Z', 'Tax', 'Mean', 'Dist', 'Snap'}
        return {k: v for k, v in components.items()
                if k not in junk and not k.isdigit() and v > 0}

    def is_primitive(self, ubp_id: str) -> bool:
        """An entry is primitive if its math has no sub-component IDs."""
        entry = self.kb.get(ubp_id)
        if not entry:
            return True  # Unknown = treat as primitive
        math_str = entry.get('math', '')
        components = self.parse_math(math_str)
        return len(components) == 0

    def decompose_to_primitives(self, ubp_id: str,
                                 depth: int = 0,
                                 max_depth: int = 20) -> Dict[str, int]:
        """
        Recursively decompose ubp_id to its absolute primitive components.
        Returns {primitive_id: total_count}.
        """
        if ubp_id in self._cache:
            return dict(self._cache[ubp_id])

        if depth > max_depth:
            return {ubp_id: 1}

        entry = self.kb.get(ubp_id)
        if not entry:
            return {ubp_id: 1}

        math_str = entry.get('math', '')
        components = self.parse_math(math_str)

        if not components:
            # This IS a primitive
            result = {ubp_id: 1}
            self._cache[ubp_id] = result
            return result

        # Recurse into components
        total: Dict[str, int] = {}
        for comp_id, count in components.items():
            sub = self.decompose_to_primitives(comp_id, depth + 1, max_depth)
            for prim_id, prim_count in sub.items():
                total[prim_id] = total.get(prim_id, 0) + prim_count * count

        self._cache[ubp_id] = total
        return dict(total)

    def get_hierarchy_level(self, ubp_id: str) -> int:
        """
        Determine the hierarchy level of an entry:
        0 = absolute primitive (quark, electron, photon)
        1 = built from L0 (proton, neutron)
        2 = built from L1 (elements)
        3 = built from L2 (molecules)
        4 = built from L3 (crystals, polymers)
        """
        entry = self.kb.get(ubp_id)
        if not entry:
            return -1
        math_str = entry.get('math', '')
        components = self.parse_math(math_str)
        if not components:
            return 0
        max_child_level = 0
        for comp_id in components:
            child_level = self.get_hierarchy_level(comp_id)
            if child_level > max_child_level:
                max_child_level = child_level
        return max_child_level + 1

    def find_cross_domain_relatives(self, ubp_id: str,
                                     threshold: float = 0.3) -> List[Dict]:
        """
        Find entries that share significant primitive overlap with ubp_id.
        This is the cross-domain 'thinking' mechanism.
        """
        target_prims = self.decompose_to_primitives(ubp_id)
        if not target_prims:
            return []

        target_total = sum(target_prims.values())
        relatives = []

        for other_id, other_entry in self.kb.items():
            if other_id == ubp_id:
                continue
            other_prims = self.decompose_to_primitives(other_id)
            if not other_prims:
                continue

            # Jaccard-like similarity on primitive sets
            shared = sum(min(target_prims.get(p, 0), other_prims.get(p, 0))
                         for p in set(target_prims) | set(other_prims))
            union = sum(max(target_prims.get(p, 0), other_prims.get(p, 0))
                        for p in set(target_prims) | set(other_prims))

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
        self.name_index: Dict[str, str] = {}       # exact name → ubp_id
        self.short_name_index: Dict[str, str] = {} # short name → ubp_id
        self.context_window: List[Dict] = []
        self.context_max_size = 24
        self.kb_paths: List[str] = []
        self.pending_changes: List[Dict] = []
        self.stats = {
            'lexicon_terms': 0, 'kb_entries': 0,
            'lexicon_build_time': 0,
            'entries_with_vectors': 0, 'entries_without_vectors': 0
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
                if path.endswith('.json'):
                    entries_loaded = self._parse_kb_json(path)
                print(f"[INFO] Loaded KB from {path}: {entries_loaded} entries")
                total_entries += entries_loaded
            except Exception as e:
                print(f"[ERROR] Failed to load KB {path}: {e}")
                import traceback
                traceback.print_exc()
        self._build_lexicon_index()
        self.stats['kb_entries'] = len(self.kb)
        return total_entries

    def _parse_kb_json(self, path: str) -> int:
        """Parse JSON-format KB."""
        count = 0
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            for key in ('objects', 'kb', 'entries'):
                if key in data:
                    data = data[key]
                    break
            for key, entry in data.items():
                if isinstance(entry, dict):
                    ubp_id = entry.get('ubp_id', key)
                    if ubp_id:
                        self.kb[ubp_id] = entry
                        count += 1
        return count

    def _extract_vector(self, entry: Dict) -> Optional[List[int]]:
        for field_name in ['vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code']:
            if field_name in entry:
                vector = entry[field_name]
                if isinstance(vector, list) and len(vector) == 24:
                    return vector
        return None

    def _build_lexicon_index(self):
        """
        Build lexicon index from KB entries.
        Indexes: lexicon field, tags, name, category, language field.
        Also builds name_index (exact name → ubp_id) and
        short_name_index (simplified name → ubp_id).
        """
        import time
        start_time = time.time()

        self.lexicon_index = defaultdict(list)
        self.name_index = {}
        self.short_name_index = {}
        self.stats['entries_with_vectors'] = 0
        self.stats['entries_without_vectors'] = 0

        for ubp_id, entry in self.kb.items():
            vector = self._extract_vector(entry)
            if vector is None or len(vector) != 24:
                self.stats['entries_without_vectors'] += 1
                continue
            self.stats['entries_with_vectors'] += 1

            terms = []

            # 1. Lexicon field: "[Name], [Description]"
            lexicon_field = entry.get('lexicon', '')
            if isinstance(lexicon_field, str):
                # Extract both parts
                parts = re.findall(r'\[([^\]]+)\]', lexicon_field)
                for part in parts:
                    terms.append(part.strip())
                    # Also add individual words
                    for word in re.findall(r'\b\w{3,}\b', part.lower()):
                        terms.append(word)
            elif isinstance(lexicon_field, list):
                for t in lexicon_field:
                    terms.append(str(t).strip())

            # 2. Language field (plain English description)
            language = entry.get('language', '')
            if language:
                for word in re.findall(r'\b\w{3,}\b', language.lower()):
                    terms.append(word)

            # 3. Tags
            for tag in entry.get('tags', []):
                if isinstance(tag, str):
                    terms.append(tag.lower())

            # 4. Name field
            name = entry.get('name', '')
            if name:
                terms.append(name)
                terms.append(name.lower())
                # Build exact name index
                self.name_index[name.lower()] = ubp_id

                # Build short name index: extract the core name
                # e.g. "Element: Iron (Fe)" → "iron", "fe"
                # e.g. "Water (H₂O)" → "water"
                # e.g. "Quark: Up" → "up quark", "quark up"
                # Priority: PARTICLE > ELEM > MOLECULE > CRYSTAL > REACTION > others
                uid_prefix = ubp_id.split('_')[0]
                priority = {'PARTICLE': 100, 'ELEM': 90, 'MOLECULE': 80,
                            'CRYSTAL': 70, 'REACTION': 60, 'ALGO': 50,
                            'TOOL': 40, 'LAW': 30, 'BELIEF': 20}
                my_priority = priority.get(uid_prefix, 10)

                short = re.sub(r'^(Element:|Quark:|Particle:|Crystal:|Molecule:)\s*', '', name, flags=re.I)
                short = re.sub(r'\s*\([^)]+\)', '', short).strip().lower()
                if short:
                    # Only overwrite if we have higher priority
                    existing = self.short_name_index.get(short)
                    if existing is None:
                        self.short_name_index[short] = ubp_id
                    else:
                        ex_prefix = existing.split('_')[0]
                        ex_priority = priority.get(ex_prefix, 10)
                        if my_priority > ex_priority:
                            self.short_name_index[short] = ubp_id

                    for word in re.findall(r'\b\w{2,}\b', short):
                        if word not in ('the', 'and', 'for', 'with'):
                            existing_word = self.short_name_index.get(word)
                            if existing_word is None:
                                self.short_name_index[word] = ubp_id
                            else:
                                ex_prefix = existing_word.split('_')[0]
                                ex_priority = priority.get(ex_prefix, 10)
                                if my_priority > ex_priority:
                                    self.short_name_index[word] = ubp_id

                # Chemical symbols from parentheses: "(Fe)", "(H₂O)"
                symbols = re.findall(r'\(([A-Za-z0-9₀-₉⁰-⁹+\-]+)\)', name)
                for sym in symbols:
                    sym_clean = sym.lower()
                    existing_sym = self.short_name_index.get(sym_clean)
                    if existing_sym is None:
                        self.short_name_index[sym_clean] = ubp_id
                    else:
                        ex_prefix = existing_sym.split('_')[0]
                        ex_priority = priority.get(ex_prefix, 10)
                        if my_priority > ex_priority:
                            self.short_name_index[sym_clean] = ubp_id

            # 5. Category
            category = entry.get('category', '')
            if category:
                terms.append(category)
                for part in category.split('.'):
                    terms.append(part)

            # 6. Math field keywords
            math = entry.get('math', '')
            if math:
                for word in re.findall(r'\b[A-Za-z]{3,}\b', math):
                    terms.append(word.lower())

            # Map all terms to this ubp_id
            for term in terms:
                if isinstance(term, str) and term.strip():
                    term_clean = term.strip().lower().strip('[]')
                    if term_clean and len(term_clean) >= 2:
                        self.lexicon_index[term_clean].append(ubp_id)

        self.stats['lexicon_terms'] = len(self.lexicon_index)
        self.stats['lexicon_build_time'] = time.time() - start_time
        print(f"[INFO] Built lexicon index: {len(self.lexicon_index)} terms")
        print(f"[INFO] Entries with valid vectors: {self.stats['entries_with_vectors']}")
        print(f"[INFO] Short name index: {len(self.short_name_index)} entries")

    def add_to_context(self, entry: Dict):
        self.context_window.append(entry)
        if len(self.context_window) > self.context_max_size:
            self.context_window = self.context_window[-self.context_max_size:]

    def get_context(self) -> str:
        if not self.context_window:
            return ""
        parts = []
        for entry in self.context_window[-6:]:
            if 'concept' in entry and entry['concept'] and 'name' in entry['concept']:
                parts.append(entry['concept']['name'])
        return ", ".join(parts)

    def propose_change(self, new_entry: Dict) -> Dict:
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
        for i, delta in enumerate(self.pending_changes):
            if delta['ubp_id'] == ubp_id:
                self.kb[ubp_id] = delta['new_entry']
                self.pending_changes.pop(i)
                self._build_lexicon_index()
                return True
        return False

    def reject_change(self, ubp_id: str) -> bool:
        for i, delta in enumerate(self.pending_changes):
            if delta['ubp_id'] == ubp_id:
                self.pending_changes.pop(i)
                return True
        return False

    def save_kb(self, path: Optional[str] = None) -> bool:
        save_path = path or (self.kb_paths[0] if self.kb_paths else 'ubp_system_kb_saved.json')
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.kb, f, indent=2, ensure_ascii=False)
            print(f"[INFO] Saved KB to {save_path}: {len(self.kb)} entries")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save KB: {e}")
            return False

# ==============================================================================
# SECTION 8: CONSOLIDATED UBP BRAIN (Main Interface)
# ==============================================================================

class UBPBrain:
    """Consolidated UBP Reasoning System v3.0"""

    def __init__(self, config_path: str = 'rational_cortex.json'):
        self.config = self._load_config(config_path)
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.math = RationalMathEngine()
        self.architect = ConceptArchitect(self.golay)
        self.vector_engine = UBPVectorEngine(self.golay, self.math)
        self.dialogue = None
        self.memory = DeltaMemoryEngine()
        self.hierarchy = None  # Initialized after KB load
        self.initialized = False
        self.fom_context: str = "general"  # Frame of Mind
        self.stats = {
            'queries_processed': 0, 'concepts_minted': 0,
            'kb_entries': 0, 'coherence_snaps': 0, 'lexicon_terms': 0
        }

    def _load_config(self, path: str) -> Dict:
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

    def set_fom(self, context: str):
        """Set Frame of Mind context (e.g. 'physics', 'biology', 'general')."""
        self.fom_context = context.lower()
        print(f"[UBP Brain] FOM set to: {self.fom_context}")

    def initialize(self, kb_paths: List[str], lexicon_path: Optional[str] = None) -> bool:
        """Initialize the brain with KB and lexicon."""
        print("[UBP Brain v3] Initializing...")
        entries_loaded = self.memory.load_kb(kb_paths)
        if entries_loaded == 0:
            print("[WARNING] No KB entries loaded.")
        self.dialogue = UBPInnerDialogue(self.golay, self.memory.kb)
        self.hierarchy = HierarchyEngine(self.memory.kb)
        self.stats['kb_entries'] = len(self.memory.kb)
        self.stats['lexicon_terms'] = self.memory.stats['lexicon_terms']
        self.initialized = True
        print(f"[UBP Brain v3] Initialized: {self.stats['kb_entries']} KB entries, "
              f"{self.stats['lexicon_terms']} lexicon terms")
        return True

    def _score_candidate(self, ubp_id: str, entry: Dict, query_words: List[str],
                          query_lower: str) -> float:
        """
        Score a candidate entry for a query.
        Higher = better match.
        """
        score = 0.0
        name = entry.get('name', '').lower()
        category = entry.get('category', '').lower()
        lexicon = entry.get('lexicon', '').lower() if isinstance(entry.get('lexicon'), str) else ''
        language = entry.get('language', '').lower()
        tags = [t.lower() for t in entry.get('tags', [])]

        # 1. Exact name match in query (highest priority)
        if name and name in query_lower:
            score += 50.0

        # 2. Short name match
        for short, sid in self.memory.short_name_index.items():
            if sid == ubp_id and short in query_lower:
                score += 40.0
                break

        # 3. Each query word that appears in name
        for word in query_words:
            if len(word) >= 3:
                if word in name:
                    score += 15.0
                if word in lexicon:
                    score += 8.0
                if word in language:
                    score += 5.0
                if word in category:
                    score += 4.0
                if word in tags:
                    score += 3.0

        # 4. FOM context boost for beliefs/laws
        if self.fom_context != 'general':
            if self.fom_context in language or self.fom_context in lexicon:
                score += 10.0

        # 5. Hierarchy level bonus: prefer concrete objects over laws
        uid_prefix = ubp_id.split('_')[0]
        level_bonus = {
            'PARTICLE': 5.0, 'ELEM': 4.0, 'MOLECULE': 4.0,
            'CRYSTAL': 3.0, 'REACTION': 2.0, 'LAW': 1.0,
            'BELIEF': 1.5, 'ALGO': 2.0, 'TOOL': 1.5
        }
        score += level_bonus.get(uid_prefix, 1.0)

        return score

    def recall(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Recall the top-k most relevant KB entries for a query.
        Uses lexicon index + scoring.
        """
        query_lower = query.lower()
        query_words = re.findall(r'\b\w{2,}\b', query_lower)

        # Gather candidates
        candidate_ids: Set[str] = set()

        # From short name index (highest priority)
        for word in query_words:
            if word in self.memory.short_name_index:
                candidate_ids.add(self.memory.short_name_index[word])

        # From lexicon index
        for word in query_words:
            for uid in self.memory.lexicon_index.get(word, [])[:5]:
                candidate_ids.add(uid)

        # Score all candidates
        scored = []
        for uid in candidate_ids:
            entry = self.memory.kb.get(uid)
            if not entry:
                continue
            vec = self.vector_engine._extract_vector(entry)
            if vec is None:
                continue
            score = self._score_candidate(uid, entry, query_words, query_lower)
            scored.append((score, uid, entry, vec))

        scored.sort(key=lambda x: -x[0])
        return [
            {'ubp_id': uid, 'entry': entry, 'vector': vec, 'score': score}
            for score, uid, entry, vec in scored[:top_k]
        ]

    def process_query(self, query: str) -> ReasoningResult:
        """Process a natural language query."""
        self.stats['queries_processed'] += 1
        warnings = []
        reasoning_chain = []
        matched_terms = set()

        # Step 1: Recall top candidates
        candidates = self.recall(query, top_k=8)

        if not candidates:
            return ReasoningResult(
                query=query,
                response=f"No known concepts found for '{query}'. "
                         f"Try: 'electron', 'water', 'iron', 'glucose', 'photon'",
                primary_concept=None,
                reasoning_chain=[],
                final_vector=[0] * 24,
                final_nrci=Fraction(0, 1),
                final_tax=Fraction(1, 1),
                coherence_snap=False,
                warnings=["No lexicon matches"],
                matched_terms=[],
                primitive_decomposition={},
                related_concepts=[]
            )

        # Step 2: Build reasoning chain
        vectors = []
        for cand in candidates:
            entry = cand['entry']
            vec = cand['vector']
            vectors.append(vec)
            for word in re.findall(r'\b\w{2,}\b', query.lower()):
                if word in entry.get('name', '').lower():
                    matched_terms.add(word)

            concept = UBPConcept(
                ubp_id=cand['ubp_id'],
                name=entry.get('name', cand['ubp_id']),
                vector=vec,
                category=entry.get('category', 'unknown'),
                math=entry.get('math', ''),
                language=entry.get('language', ''),
                nrci=self.math.validate_fraction(entry.get('nrci', '1/1')),
                tax=self.math.validate_fraction(entry.get('tax', '0/1')),
                lexicon=entry.get('lexicon', ''),
                fingerprint=entry.get('fingerprint', ''),
                tags=entry.get('tags', [])
            )
            reasoning_chain.append(ThoughtStep(
                concept=concept,
                operation='recall',
                coherence=self.math.calculate_nrci(vec)
            ))

        # Step 3: Compose and snap
        if len(vectors) > 1:
            composed = self.vector_engine.majority_vote(vectors)
        else:
            composed = vectors[0]

        snapped_vector, was_corrected, syndrome_weight = self.vector_engine.coherence_snap(composed)
        if was_corrected:
            self.stats['coherence_snaps'] += 1
            warnings.append(f"Vector corrected (syndrome weight: {syndrome_weight})")

        # Step 4: Inner dialogue
        anchor_name, coherence_cost = self.dialogue.deliberate(
            snapped_vector, max_steps=self.config.get('max_reasoning_steps', 6)
        )

        # Step 5: Final metrics
        final_nrci = self.math.calculate_nrci(snapped_vector)
        final_tax = self.math.calculate_tax(len(matched_terms), len(reasoning_chain))

        # Step 6: Primary concept (top-scored candidate)
        primary_concept = None
        if candidates:
            top = candidates[0]
            entry = top['entry']
            vec = top['vector']
            primary_concept = UBPConcept(
                ubp_id=top['ubp_id'],
                name=entry.get('name', top['ubp_id']),
                vector=vec,
                category=entry.get('category', 'unknown'),
                math=entry.get('math', ''),
                language=entry.get('language', ''),
                nrci=self.math.validate_fraction(entry.get('nrci', '1/1')),
                tax=self.math.validate_fraction(entry.get('tax', '0/1')),
                lexicon=entry.get('lexicon', ''),
                fingerprint=entry.get('fingerprint', ''),
                tags=entry.get('tags', [])
            )

        # Step 7: Primitive decomposition
        primitive_decomp = {}
        if primary_concept and self.hierarchy:
            primitive_decomp = self.hierarchy.decompose_to_primitives(primary_concept.ubp_id)

        # Step 8: Related concepts (cross-domain)
        related = []
        if primary_concept and self.hierarchy:
            related = self.hierarchy.find_cross_domain_relatives(
                primary_concept.ubp_id, threshold=0.25
            )

        # Step 9: Context
        self.memory.add_to_context({
            'query': query,
            'concept': primary_concept.to_dict() if primary_concept else None,
            'vector': snapped_vector,
            'nrci': str(final_nrci)
        })

        # Step 10: Generate response
        response = self._generate_response(
            query, primary_concept, final_nrci, snapped_vector,
            primitive_decomp, related, candidates
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
            matched_terms=list(matched_terms),
            primitive_decomposition=primitive_decomp,
            related_concepts=related
        )

    def _generate_response(self, query: str, concept: Optional[UBPConcept],
                            nrci: Fraction, vector: List[int],
                            primitives: Dict[str, int],
                            related: List[Dict],
                            candidates: List[Dict]) -> str:
        """
        Generate a rich natural language response using the language and lexicon fields.
        This is the LLM-style communication layer.
        """
        if not concept:
            return f"Query '{query}' processed. No stable concept found. NRCI: {nrci}"

        lines = []

        # Primary identification
        lines.append(f"**{concept.name}**")

        # Language field (plain English description)
        if concept.language:
            lines.append(concept.language)

        # Category and hierarchy level
        level = self.hierarchy.get_hierarchy_level(concept.ubp_id) if self.hierarchy else -1
        level_names = {0: "Absolute Primitive", 1: "L1 Composite", 2: "L2 Element",
                       3: "L3 Molecule", 4: "L4 Structure", -1: "Unknown"}
        lines.append(f"Category: {concept.category} | Level: {level_names.get(level, f'L{level}')}")

        # Math (composition)
        if concept.math and concept.math not in ('atomic', ''):
            lines.append(f"Math: {concept.math}")

        # Primitive decomposition (if composite)
        if primitives and len(primitives) > 1:
            prim_parts = []
            for prim_id, count in sorted(primitives.items(), key=lambda x: -x[1])[:6]:
                prim_entry = self.memory.kb.get(prim_id, {})
                prim_name = prim_entry.get('name', prim_id)
                prim_parts.append(f"{count}×{prim_name}")
            lines.append(f"Primitives: {', '.join(prim_parts)}")

        # Vector metrics
        hw = sum(vector)
        lines.append(f"Vector weight: {hw}/24 | NRCI: {nrci}")

        # Related concepts (cross-domain thinking)
        if related:
            rel_parts = [f"{r['name']} ({r['similarity']:.0%})" for r in related[:3]]
            lines.append(f"Related: {', '.join(rel_parts)}")

        # Other candidates
        if len(candidates) > 1:
            alt_names = [c['entry'].get('name', c['ubp_id']) for c in candidates[1:4]]
            lines.append(f"Also relevant: {', '.join(alt_names)}")

        return "\n".join(lines)

    def explain(self, ubp_id: str) -> str:
        """
        Generate a full explanation of a KB entry using its language and lexicon fields,
        with complete primitive decomposition.
        """
        entry = self.memory.kb.get(ubp_id)
        if not entry:
            return f"Entry '{ubp_id}' not found in KB."

        lines = [f"=== {entry.get('name', ubp_id)} ==="]

        # Lexicon (SOP_002 format: [Name], [Description])
        lexicon = entry.get('lexicon', '')
        if lexicon:
            lines.append(f"Lexicon: {lexicon}")

        # Language
        language = entry.get('language', '')
        if language:
            lines.append(f"Language: {language}")

        # Math
        math = entry.get('math', '')
        if math:
            lines.append(f"Math: {math}")

        # Hierarchy level
        if self.hierarchy:
            level = self.hierarchy.get_hierarchy_level(ubp_id)
            lines.append(f"Hierarchy level: {level}")

            # Primitive decomposition
            primitives = self.hierarchy.decompose_to_primitives(ubp_id)
            if primitives and len(primitives) > 1:
                lines.append("Primitive decomposition:")
                for prim_id, count in sorted(primitives.items(), key=lambda x: -x[1]):
                    prim_entry = self.memory.kb.get(prim_id, {})
                    prim_name = prim_entry.get('name', prim_id)
                    lines.append(f"  {count}× {prim_name} ({prim_id})")
            elif primitives:
                lines.append("This IS an absolute primitive.")

            # Cross-domain relatives
            relatives = self.hierarchy.find_cross_domain_relatives(ubp_id, threshold=0.2)
            if relatives:
                lines.append("Cross-domain relatives (shared primitives):")
                for r in relatives[:5]:
                    lines.append(f"  {r['name']} [{r['category']}] — {r['similarity']:.1%} similarity")

        # Vector
        vec = self.vector_engine._extract_vector(entry)
        if vec:
            hw = sum(vec)
            lines.append(f"Vector: weight={hw}/24, fingerprint={entry.get('fingerprint','')[:16]}...")

        # NRCI
        nrci = entry.get('nrci', '?')
        lines.append(f"NRCI: {nrci}")

        # Tags
        tags = entry.get('tags', [])
        if tags:
            lines.append(f"Tags: {', '.join(tags[:8])}")

        return "\n".join(lines)

    def mint_concept(self, name: str, domain: str, p1: int, p2: int, p3: int = 0,
                     math: str = "", lexicon: str = None) -> Dict:
        """Mint a new concept."""
        vector = self.architect.mint(name, domain, p1, p2, p3)
        ubp_id = f"CONCEPT_{name.upper().replace(' ', '_')}"
        fingerprint = hashlib.sha256(math.encode() if math else name.encode()).hexdigest()
        entry = {
            'ubp_id': ubp_id, 'name': name,
            'category': f"custom.{domain}", 'vector': vector,
            'math': math, 'language': lexicon or name,
            'nrci': '1/1', 'tax': '0/1',
            'lexicon': f"[{name}], [{lexicon or name}]",
            'fingerprint': fingerprint, 'tags': ['MINTED']
        }
        delta = self.memory.propose_change(entry)
        self.stats['concepts_minted'] += 1
        return {'status': 'pending_acceptance', 'ubp_id': ubp_id, 'vector': vector, 'delta': delta}

    def accept_concept(self, ubp_id: str) -> bool:
        result = self.memory.accept_change(ubp_id)
        if result:
            self.stats['kb_entries'] = len(self.memory.kb)
            self.stats['lexicon_terms'] = self.memory.stats['lexicon_terms']
        return result

    def save_kb(self, path: Optional[str] = None) -> bool:
        return self.memory.save_kb(path)

    def get_stats(self) -> Dict:
        return {
            **self.stats,
            'vector_engine_metrics': self.vector_engine.metrics,
            'pending_changes': len(self.memory.pending_changes),
            'context_size': len(self.memory.context_window),
            'fom_context': self.fom_context
        }

    def debug_vector_lookup(self, word: str) -> Dict:
        """DEBUG: Trace vector lookup for a specific word."""
        result = {
            'word': word,
            'in_short_name_index': word.lower() in self.memory.short_name_index,
            'short_name_match': self.memory.short_name_index.get(word.lower()),
            'in_lexicon': word.lower() in self.memory.lexicon_index,
            'lexicon_candidates': self.memory.lexicon_index.get(word.lower(), [])[:5]
        }
        return result

    def export_session(self, path: str) -> bool:
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

# ==============================================================================
# SECTION 9: MAIN (Test & Demo)
# ==============================================================================

def main():
    """Test and demonstrate the consolidated UBP Brain v3.0."""
    print("=" * 80)
    print("UBP BRAIN CONSOLIDATED v3.0 — ENRICHED KB + LEXICON COMMUNICATION")
    print("=" * 80)

    brain = UBPBrain()

    # Try to find the enriched KB
    kb_candidates = [
        'ubp_system_kb_v2.json',
        '../ubp_system_kb_v2.json',
        '/home/ubuntu/ubp_build/ubp_system_kb_v2.json',
        'ubp_system_kb_enriched.json',
        '/home/ubuntu/ubp_build/ubp_system_kb_enriched.json',
        'ubp_system_kb.json',
        '../system_kb/ubp_system_kb.json',
    ]
    kb_path = None
    for p in kb_candidates:
        if os.path.exists(p):
            kb_path = p
            break

    if not kb_path:
        print("[ERROR] No KB file found. Tried:", kb_candidates)
        return

    brain.initialize([kb_path])

    print(f"\n[KB loaded] {brain.stats['kb_entries']} entries, "
          f"{brain.stats['lexicon_terms']} lexicon terms")

    # Test queries
    test_queries = [
        "What is a proton?",
        "Tell me about water",
        "What is iron?",
        "Explain glucose",
        "What is a photon?",
        "Tell me about diamond",
        "What is ATP?",
        "Explain the Higgs boson",
        "What is adenine?",
        "Tell me about quartz",
    ]

    print("\n" + "=" * 80)
    print("QUERY TESTS")
    print("=" * 80)

    for query in test_queries:
        print(f"\nQ: {query}")
        result = brain.process_query(query)
        print(result.response)
        if result.warnings:
            print(f"  [Warnings: {', '.join(result.warnings)}]")
        print("-" * 60)

    # Explain a specific entry
    print("\n" + "=" * 80)
    print("EXPLAIN: MOLECULE_H2O")
    print("=" * 80)
    print(brain.explain("MOLECULE_H2O"))

    print("\n" + "=" * 80)
    print("EXPLAIN: PARTICLE_ELECTRON_001")
    print("=" * 80)
    print(brain.explain("PARTICLE_ELECTRON_001"))

    # Stats
    print("\n" + "=" * 80)
    print("SYSTEM STATISTICS")
    print("=" * 80)
    stats = brain.get_stats()
    for key, value in stats.items():
        if key != 'vector_engine_metrics':
            print(f"  {key}: {value}")

    print("\n" + "=" * 80)
    print("UBP BRAIN v3.0 — TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
