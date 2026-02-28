"""
================================================================================
UBP BRAIN CONSOLIDATED v4.0 — SOP_002 NATIVE + DUAL-LAYER ARCHITECTURE
================================================================================
Architecture:
  - UNDERSTANDING layer: deterministic entries (particles, elements, molecules)
    built from primitives. Verifiable, exact, composable.
  - BELIEF layer: LAW entries — learned memories with FOM-weighted meaning.

Key design principles (SOP_002):
  - Fingerprint key = SHA256(math_dna)
  - Vector stored in entry['atlas']['vector']
  - NRCI stored in entry['atlas']['nrci_score']
  - Name extracted from entry['lexicon'] first bracket [Name]

Author: Euan R A Craig, New Zealand
Date: 28 Feb 2026
Version: 4.0 (Production)
================================================================================
"""

import json
import hashlib
import os
import re
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any, Set
from collections import defaultdict
from datetime import datetime

# ── UBP Core Foundation ───────────────────────────────────────────────────────
try:
    from ubp_core_v5_3_merged import (
        GOLAY_ENGINE, 
        LEECH_ENGINE, 
        SUBSTRATE, 
        PARTICLE_PHYSICS,
        BinaryLinearAlgebra
    )
    CORE_AVAILABLE = True
    print("[UBP Brain v4] UBP Core v5.3 FOUND — Full Golay/Leech functionality enabled")
except ImportError as _e:
    CORE_AVAILABLE = False
    BinaryLinearAlgebra = None
    GOLAY_ENGINE = None
    print(f"[WARNING] UBP Core not found ({_e}). Running in fallback mode.")

# ==============================================================================
# SECTION 1: HELPERS — SOP_002 field extraction
# ==============================================================================

def extract_vector(entry: Dict) -> Optional[List[int]]:
    """Extract 24-bit Golay vector from an SOP_002 entry (atlas.vector)."""
    # 1. Check Atlas (Standard)
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        v = atlas.get('vector')
        if isinstance(v, list) and len(v) == 24:
            return v
    # 2. Legacy flat format fallback
    for field_name in ('vector', 'vectors', 'golay_vector', 'golay', 'vec', 'code'):
        v = entry.get(field_name)
        if isinstance(v, list) and len(v) == 24:
            return v
    return None

def extract_nrci(entry: Dict) -> Fraction:
    """Extract NRCI as Fraction from an SOP_002 entry."""
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        # Prefer exact rational form string "p/q"
        nrci_str = atlas.get('nrci', '')
        if isinstance(nrci_str, str) and '/' in nrci_str:
            try:
                n, d = nrci_str.split('/')
                return Fraction(int(n), int(d))
            except Exception:
                pass
        # Fallback to float score
        score = atlas.get('nrci_score')
        if score is not None:
            return Fraction(score).limit_denominator(1000000)
            
    # Legacy flat format
    nrci_str = entry.get('nrci', '1/1')
    if isinstance(nrci_str, str) and '/' in nrci_str:
        try:
            n, d = nrci_str.split('/')
            return Fraction(int(n), int(d))
        except Exception:
            pass
    return Fraction(1, 1)

def extract_tax(entry: Dict) -> Fraction:
    """Extract TAX as Fraction from an SOP_002 entry."""
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        tax_str = atlas.get('tax', '')
        if isinstance(tax_str, str) and '/' in tax_str:
            try:
                n, d = tax_str.split('/')
                return Fraction(int(n), int(d))
            except Exception:
                pass
    return Fraction(0, 1)

def extract_name(entry: Dict) -> str:
    """Extract the display name from an SOP_002 lexicon field: '[Name], [Description]'."""
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        # Match content inside first brackets
        m = re.match(r'\[([^\]]+)\]', lexicon)
        if m:
            return m.group(1).strip()
    # Fallback to ubp_id
    return entry.get('ubp_id', 'Unknown')

def extract_description(entry: Dict) -> str:
    """Extract the description from an SOP_002 lexicon field."""
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        # Split by '], [' or just find all bracketed groups
        parts = re.findall(r'\[([^\]]+)\]', lexicon)
        if len(parts) >= 2:
            return parts[1].strip()
        if len(parts) == 1:
            # Sometimes description is outside brackets or just one block
            return parts[0].strip()
        # Fallback: return everything after the first comma if no brackets
        if ',' in lexicon and not parts:
            return lexicon.split(',', 1)[1].strip()
    return lexicon

def is_belief(entry: Dict) -> bool:
    """Return True if this entry is a LAW/BELIEF (not a deterministic object)."""
    uid = entry.get('ubp_id', '')
    return uid.startswith(('LAW_', 'BELIEF_', 'AXIOM_', 'IMPERATIVE_'))

# ==============================================================================
# SECTION 2: DATA STRUCTURES
# ==============================================================================

@dataclass
class UBPConcept:
    """A single concept in the UBP ontology."""
    ubp_id: str
    name: str
    description: str
    vector: List[int]
    category: str
    math: str
    nrci: Fraction
    tax: Fraction
    lexicon: str
    fingerprint: str
    tags: List[str]
    is_belief: bool = False

    def to_dict(self) -> Dict:
        return {
            "ubp_id": self.ubp_id,
            "name": self.name,
            "description": self.description,
            "vector": self.vector,
            "category": self.category,
            "math": self.math,
            "nrci": str(self.nrci),
            "tax": str(self.tax),
            "lexicon": self.lexicon,
            "fingerprint": self.fingerprint,
            "tags": self.tags,
            "is_belief": self.is_belief
        }

@dataclass
class ReasoningResult:
    """Complete result of a reasoning operation."""
    query: str
    response: str
    primary_concept: Optional[UBPConcept]
    candidates: List[Dict]
    final_vector: List[int]
    final_nrci: Fraction
    coherence_snap: bool
    warnings: List[str]
    primitive_decomposition: Dict[str, int]
    related_concepts: List[Dict]
    layer: str  # 'understanding' or 'belief'

# ==============================================================================
# SECTION 3: VECTOR ENGINE
# ==============================================================================

class UBPVectorEngine:
    """Handles vector operations using real Golay engine when available."""

    def __init__(self):
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.metrics = {'error_corrections': 0, 'total_ops': 0}

    def hamming_distance(self, v1: List[int], v2: List[int]) -> int:
        return sum(a != b for a, b in zip(v1, v2))

    def majority_vote(self, vectors: List[List[int]]) -> List[int]:
        """Combine vectors by majority vote — noise-resistant composition."""
        if not vectors:
            return [0] * 24
        result = []
        for i in range(24):
            bits = [v[i] for v in vectors if len(v) == 24]
            result.append(1 if sum(bits) > len(bits) / 2 else 0)
        return result

    def coherence_snap(self, vector: List[int]) -> Tuple[List[int], bool, int]:
        """Snap vector to nearest valid Golay codeword."""
        self.metrics['total_ops'] += 1
        if not CORE_AVAILABLE or self.golay is None:
            return vector, False, 0
        try:
            decoded_msg, syndrome, weight = self.golay.decode(vector)
            was_corrected = weight > 0
            if was_corrected:
                self.metrics['error_corrections'] += 1
            snapped = self.golay.encode(decoded_msg)
            if len(snapped) != 24:
                snapped = (snapped + [0] * 24)[:24]
            return snapped, was_corrected, weight
        except Exception:
            return vector, False, 0

# ==============================================================================
# SECTION 4: HIERARCHY ENGINE
# ==============================================================================

class HierarchyEngine:
    """
    Recursively decomposes KB entries to their absolute primitives.
    """
    # Match "2×ELEM_H_001" or "2xELEM_H_001"
    MULT_PATTERN = re.compile(r'(\d+)\s*[×xX]\s*([A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+)')
    # Match standalone IDs like "ELEM_H_001"
    ID_PATTERN = re.compile(r'\b([A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,})\b')
    JUNK_IDS = {'N', 'Z', 'Tax', 'Mean', 'Dist', 'Snap', 'SOP', 'MATH', 'ALGO'}

    def __init__(self, kb: Dict):
        self.kb = kb
        self._decomp_cache: Dict[str, Dict[str, int]] = {}
        self._level_cache: Dict[str, int] = {}

    def parse_components(self, math_str: str) -> Dict[str, int]:
        """Parse a math/hierarchy string into {component_id: count}."""
        if not math_str or math_str in ('atomic', 'absolute_primitive', ''):
            return {}
        components: Dict[str, int] = {}
        # Find "N×ID" patterns
        for mult_str, comp_id in self.MULT_PATTERN.findall(math_str):
            if comp_id not in self.JUNK_IDS and comp_id in self.kb:
                components[comp_id] = components.get(comp_id, 0) + int(mult_str)
        # Find standalone IDs
        used = set(components.keys())
        for comp_id in self.ID_PATTERN.findall(math_str):
            if comp_id not in used and comp_id not in self.JUNK_IDS and comp_id in self.kb:
                components[comp_id] = components.get(comp_id, 0) + 1
        return components

    def decompose_to_primitives(self, ubp_id: str, depth: int = 0, max_depth: int = 20) -> Dict[str, int]:
        """Recursively decompose to absolute primitive counts."""
        if ubp_id in self._decomp_cache: return dict(self._decomp_cache[ubp_id])
        if depth > max_depth: return {ubp_id: 1}

        entry = self.kb.get(ubp_id)
        if not entry: return {ubp_id: 1}

        math_str = entry.get('math', '')
        atlas = entry.get('atlas', {})
        hier_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''

        components = self.parse_components(math_str)
        if not components: components = self.parse_components(hier_str)

        if not components:
            result = {ubp_id: 1}
            self._decomp_cache[ubp_id] = result
            return result

        total: Dict[str, int] = {}
        for comp_id, count in components.items():
            sub = self.decompose_to_primitives(comp_id, depth + 1, max_depth)
            for prim_id, prim_count in sub.items():
                total[prim_id] = total.get(prim_id, 0) + prim_count * count

        self._decomp_cache[ubp_id] = total
        return dict(total)

    def get_hierarchy_level(self, ubp_id: str, _visited: Optional[Set] = None) -> int:
        """0=Primitive, 1=Nucleon, 2=Element, 3=Molecule, 4=Structure"""
        if ubp_id in self._level_cache: return self._level_cache[ubp_id]
        if _visited is None: _visited = set()
        if ubp_id in _visited: return 0
        _visited.add(ubp_id)

        entry = self.kb.get(ubp_id)
        if not entry: return -1

        math_str = entry.get('math', '')
        atlas = entry.get('atlas', {})
        hier_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''

        components = self.parse_components(math_str)
        if not components: components = self.parse_components(hier_str)

        if not components:
            self._level_cache[ubp_id] = 0
            return 0

        max_child = max(self.get_hierarchy_level(cid, _visited) for cid in components)
        level = max_child + 1
        self._level_cache[ubp_id] = level
        return level

    def find_cross_domain_relatives(self, ubp_id: str, threshold: float = 0.25, limit: int = 8) -> List[Dict]:
        """Find entries sharing significant primitive overlap."""
        target_prims = self.decompose_to_primitives(ubp_id)
        if not target_prims or (len(target_prims) == 1 and ubp_id in target_prims):
            return []

        relatives = []
        for other_id, other_entry in self.kb.items():
            if other_id == ubp_id or is_belief(other_entry): continue
            other_prims = self.decompose_to_primitives(other_id)
            if not other_prims or (len(other_prims) == 1 and other_id in other_prims): continue

            all_prims = set(target_prims) | set(other_prims)
            shared = sum(min(target_prims.get(p, 0), other_prims.get(p, 0)) for p in all_prims)
            union = sum(max(target_prims.get(p, 0), other_prims.get(p, 0)) for p in all_prims)
            
            if union > 0:
                sim = shared / union
                if sim >= threshold:
                    relatives.append({
                        'ubp_id': other_id,
                        'name': extract_name(other_entry),
                        'category': other_entry.get('ubp_id', '').split('_')[0],
                        'similarity': round(sim, 3),
                        'shared_primitive_count': shared
                    })
        return sorted(relatives, key=lambda x: -x['similarity'])[:limit]

# ==============================================================================
# SECTION 5: KNOWLEDGE BASE MANAGER
# ==============================================================================

class KBManager:
    CATEGORY_PRIORITY = {
        'PARTICLE': 100, 'ELEM': 90, 'MOLECULE': 80, 'CRYSTAL': 70,
        'REACTION': 60, 'ALGO': 50, 'TOOL': 40, 'MATH': 35,
        'GEO': 30, 'LAW': 20, 'BELIEF': 15, 'DS': 10
    }

    def __init__(self):
        self.kb: Dict[str, Dict] = {}
        self.lexicon_index: Dict[str, List[str]] = defaultdict(list)
        self.short_name_index: Dict[str, str] = {}
        self.fingerprint_index: Dict[str, str] = {}
        self.stats = {'total_entries': 0, 'lexicon_terms': 0}

    def load(self, paths: List[str]) -> int:
        self.kb = {}
        for path in paths:
            if not os.path.exists(path): continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Unwrap nested formats
                if isinstance(data, dict):
                    for wrap_key in ('objects', 'kb', 'entries'):
                        if wrap_key in data and isinstance(data[wrap_key], dict):
                            data = data[wrap_key]
                            break
                    for key, entry in data.items():
                        if isinstance(entry, dict) and 'ubp_id' in entry:
                            self.kb[entry['ubp_id']] = entry
            except Exception as e:
                print(f"[ERROR] Failed to load {path}: {e}")
        self._build_indexes()
        return len(self.kb)

    def _build_indexes(self):
        self.lexicon_index = defaultdict(list)
        self.short_name_index = {}
        self.fingerprint_index = {}

        for uid, entry in self.kb.items():
            if 'fingerprint' in entry: self.fingerprint_index[entry['fingerprint']] = uid
            
            name = extract_name(entry)
            desc = extract_description(entry)
            
            # Lexicon Indexing
            terms = set()
            terms.add(name.lower())
            terms.update(re.findall(r'\b\w{2,}\b', name.lower()))
            terms.update(re.findall(r'\b\w{3,}\b', desc.lower()))
            for tag in entry.get('tags', []): terms.add(tag.lower())
            for part in uid.split('_'): 
                if len(part) >= 2: terms.add(part.lower())

            for term in terms: self.lexicon_index[term].append(uid)

            # Short Name Indexing (Priority)
            uid_prefix = uid.split('_')[0]
            my_priority = self.CATEGORY_PRIORITY.get(uid_prefix, 5)
            
            clean = re.sub(r'^(Element:|Quark:|Particle:|Molecule:|Law:|Belief:)\s*', '', name, flags=re.I)
            clean_no_paren = re.sub(r'\s*\([^)]+\)', '', clean).strip().lower()
            
            candidates = [clean_no_paren]
            for sym in re.findall(r'\(([A-Za-z0-9+\-]+)\)', name):
                candidates.append(sym.lower())

            for short in candidates:
                if not short or len(short) < 2: continue
                existing = self.short_name_index.get(short)
                if existing is None:
                    self.short_name_index[short] = uid
                else:
                    ex_prefix = existing.split('_')[0]
                    if my_priority > self.CATEGORY_PRIORITY.get(ex_prefix, 5):
                        self.short_name_index[short] = uid

        self.stats['total_entries'] = len(self.kb)
        self.stats['lexicon_terms'] = len(self.lexicon_index)

# ==============================================================================
# SECTION 6: INNER DIALOGUE
# ==============================================================================

class InnerDialogue:
    def __init__(self, kb: Dict, golay=None):
        self.golay = golay
        self.anchors: Dict[str, List[int]] = {}
        self.threshold = 3
        for uid, entry in kb.items():
            vec = extract_vector(entry)
            if vec and is_belief(entry):
                self.anchors[uid] = vec

    def deliberate(self, query_vector: List[int], max_steps: int = 6) -> Tuple[str, Fraction]:
        if len(query_vector) != 24: return "UNKNOWN", Fraction(1, 1)
        current = query_vector.copy()
        best_name, best_cost = "UNKNOWN", Fraction(1, 1)

        for _ in range(max_steps):
            closest_name, closest_dist = None, 25
            for name, anchor_vec in self.anchors.items():
                d = sum(a != b for a, b in zip(current, anchor_vec))
                if d < closest_dist: closest_dist, closest_name = d, name
            
            if closest_name is None: break
            cost = Fraction(closest_dist, 24)
            if cost < best_cost: best_cost, best_name = cost, closest_name
            if closest_dist <= self.threshold: break
            
            # Reflexive Step
            anchor_vec = self.anchors[closest_name]
            reflexive = [a ^ b for a, b in zip(current, anchor_vec)]
            if CORE_AVAILABLE and self.golay:
                try:
                    msg, _, _ = self.golay.decode(reflexive)
                    current = self.golay.encode(msg)
                except: current = reflexive
            else: current = reflexive

        return best_name, best_cost

# ==============================================================================
# SECTION 7: CONSOLIDATED UBP BRAIN
# ==============================================================================

class UBPBrain:
    def __init__(self):
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.vector_engine = UBPVectorEngine()
        self.kb_manager = KBManager()
        self.hierarchy: Optional[HierarchyEngine] = None
        self.dialogue: Optional[InnerDialogue] = None
        self.fom_context: str = "general"
        self.initialized = False
        self.memory = self.kb_manager # Alias for compatibility

    def initialize(self, kb_paths: List[str]) -> bool:
        print("[UBP Brain v4] Initializing...")
        n = self.kb_manager.load(kb_paths)
        if n == 0: return False
        self.hierarchy = HierarchyEngine(self.kb_manager.kb)
        self.dialogue = InnerDialogue(self.kb_manager.kb, self.golay)
        self.initialized = True
        return True

    def _score_candidate(self, uid: str, entry: Dict, query_words: List[str], query_lower: str) -> float:
        score = 0.0
        name = extract_name(entry).lower()
        desc = extract_description(entry).lower()
        
        # 1. Exact Short Name Match
        for short, sid in self.kb_manager.short_name_index.items():
            if sid == uid and short in query_lower: score += 50.0; break
        
        # 2. Full Name Match
        if name and name in query_lower: score += 40.0
        
        # 3. Keyword Match
        for word in query_words:
            if len(word) >= 3:
                if word in name: score += 15.0
                if word in desc: score += 6.0
                if word in entry.get('tags', []): score += 4.0

        # 4. Category Bonus
        uid_prefix = uid.split('_')[0]
        score += self.kb_manager.CATEGORY_PRIORITY.get(uid_prefix, 10) / 10.0
        return score

    def recall(self, query: str, top_k: int = 8) -> List[Dict]:
        query_lower = query.lower()
        query_words = re.findall(r'\b\w{2,}\b', query_lower)
        candidate_ids = set()

        for word in query_words:
            if word in self.kb_manager.short_name_index:
                candidate_ids.add(self.kb_manager.short_name_index[word])
            for uid in self.kb_manager.lexicon_index.get(word, [])[:8]:
                candidate_ids.add(uid)

        scored = []
        for uid in candidate_ids:
            entry = self.kb_manager.kb.get(uid)
            if not entry: continue
            vec = extract_vector(entry)
            if vec is None: continue
            score = self._score_candidate(uid, entry, query_words, query_lower)
            scored.append({'ubp_id': uid, 'entry': entry, 'vector': vec, 'score': score})

        scored.sort(key=lambda x: -x['score'])
        return scored[:top_k]

    def process_query(self, query: str) -> ReasoningResult:
        candidates = self.recall(query, top_k=8)
        if not candidates:
            return ReasoningResult(query, "No concepts found.", None, [], [0]*24, Fraction(0), False, [], {}, [], 'none')

        top = candidates[0]
        entry = top['entry']
        primary = UBPConcept(
            ubp_id=top['ubp_id'],
            name=extract_name(entry),
            description=extract_description(entry),
            vector=top['vector'],
            category=top['ubp_id'].split('_')[0],
            math=entry.get('math', ''),
            nrci=extract_nrci(entry),
            tax=extract_tax(entry),
            lexicon=entry.get('lexicon', ''),
            fingerprint=entry.get('fingerprint', ''),
            tags=entry.get('tags', []),
            is_belief=is_belief(entry)
        )

        # Vector Composition
        vectors = [c['vector'] for c in candidates[:4]]
        composed = self.vector_engine.majority_vote(vectors)
        snapped, corrected, _ = self.vector_engine.coherence_snap(composed)
        
        # Decomposition
        prims = {}
        if self.hierarchy and not primary.is_belief:
            prims = self.hierarchy.decompose_to_primitives(primary.ubp_id)

        # Response Generation
        response = f"**{primary.name}** ({primary.ubp_id})\n{primary.description}\n"
        if prims:
            p_str = ", ".join([f"{v}x {k}" for k,v in list(prims.items())[:5]])
            response += f"Primitives: {p_str}\n"
        response += f"NRCI: {float(primary.nrci):.4f} | Tax: {float(primary.tax):.4f}"

        return ReasoningResult(
            query=query, response=response, primary_concept=primary, candidates=candidates,
            final_vector=snapped, final_nrci=Fraction(sum(snapped), 24),
            coherence_snap=corrected, warnings=[], primitive_decomposition=prims,
            related_concepts=[], layer='belief' if primary.is_belief else 'understanding'
        )

if __name__ == "__main__":
    brain = UBPBrain()
    if os.path.exists('ubp_system_kb.json'):
        brain.initialize(['ubp_system_kb.json'])
        print(brain.process_query("What is water?").response)