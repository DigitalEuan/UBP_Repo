"""
================================================================================
UBP BRAIN CONSOLIDATED v4.0.1 — SOFT-DECISION INTEGRATED
================================================================================
Author: Euan R A Craig, New Zealand
Date: 04 March 2026
Version: 4.0.1 (Soft-Decision Enabled)
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
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        v = atlas.get('vector')
        if isinstance(v, list) and len(v) == 24:
            return v
    return None

def extract_nrci(entry: Dict) -> Fraction:
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        nrci_str = atlas.get('nrci', '')
        if isinstance(nrci_str, str) and '/' in nrci_str:
            try:
                n, d = nrci_str.split('/')
                return Fraction(int(n), int(d))
            except: pass
        score = atlas.get('nrci_score')
        if score is not None:
            return Fraction(score).limit_denominator(1000000)
    return Fraction(1, 1)

def extract_tax(entry: Dict) -> Fraction:
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        tax_str = atlas.get('tax', '')
        if isinstance(tax_str, str) and '/' in tax_str:
            try:
                n, d = tax_str.split('/')
                return Fraction(int(n), int(d))
            except: pass
    return Fraction(0, 1)

def extract_name(entry: Dict) -> str:
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        m = re.match(r'\[([^\]]+)\]', lexicon)
        if m: return m.group(1).strip()
    return entry.get('ubp_id', 'Unknown')

def extract_description(entry: Dict) -> str:
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        parts = re.findall(r'\[([^\]]+)\]', lexicon)
        if len(parts) >= 2: return parts[1].strip()
    return lexicon

def is_belief(entry: Dict) -> bool:
    uid = entry.get('ubp_id', '')
    return uid.startswith(('LAW_', 'BELIEF_', 'AXIOM_', 'IMPERATIVE_'))

# ==============================================================================
# SECTION 2: SOFT DECODER (Conway & Sloane)
# ==============================================================================

class SoftGolayDecoder:
    """
    Conway & Sloane Soft-Decision Decoding.
    Maps 4096 codewords to 24D Euclidean space for high-noise recovery.
    """
    def __init__(self):
        if not CORE_AVAILABLE or GOLAY_ENGINE is None:
            self.binary_codewords = []
            self.bipolar_codewords = []
            return
        
        print("[Soft Decoder] Initializing 24D Euclidean Space...")
        self.binary_codewords = GOLAY_ENGINE.get_all_codewords()
        self.bipolar_codewords = [[1.0 if b == 1 else -1.0 for b in cw] for cw in self.binary_codewords]

    def decode_soft(self, analog_vector: List[float]) -> Tuple[List[int], float, int]:
        if not self.bipolar_codewords:
            return [1 if v > 0 else 0 for v in analog_vector], 0.0, -1

        search_vector = [(v * 2.0) - 1.0 for v in analog_vector] if min(analog_vector) >= 0 else analog_vector
        best_score = -float('inf')
        best_index = -1

        for i, bp_cw in enumerate(self.bipolar_codewords):
            score = sum(s * c for s, c in zip(search_vector, bp_cw))
            if score > best_score:
                best_score, best_index = score, i

        return self.binary_codewords[best_index], max(0.0, best_score / 24.0), best_index

# ==============================================================================
# SECTION 3: VECTOR ENGINE
# ==============================================================================

class UBPVectorEngine:
    def __init__(self):
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.soft_decoder = SoftGolayDecoder()
        self.metrics = {'error_corrections': 0, 'total_ops': 0, 'soft_snaps': 0}

    def hamming_distance(self, v1: List[int], v2: List[int]) -> int:
        return sum(a != b for a, b in zip(v1, v2))

    def majority_vote(self, vectors: List[List[int]]) -> List[int]:
        if not vectors: return [0] * 24
        result = []
        for i in range(24):
            bits = [v[i] for v in vectors if len(v) == 24]
            result.append(1 if sum(bits) > len(bits) / 2 else 0)
        return result

    def coherence_snap(self, vector: List[int]) -> Tuple[List[int], bool, int]:
        self.metrics['total_ops'] += 1
        if not CORE_AVAILABLE or self.golay is None: return vector, False, 0
        try:
            decoded_msg, syndrome, weight = self.golay.decode(vector)
            snapped = self.golay.encode(decoded_msg)
            return snapped, weight > 0, weight
        except: return vector, False, 0

    def coherence_snap_soft(self, analog_vector: List[float]) -> Tuple[List[int], float, int]:
        self.metrics['total_ops'] += 1
        self.metrics['soft_snaps'] += 1
        return self.soft_decoder.decode_soft(analog_vector)

# ==============================================================================
# SECTION 4: HIERARCHY ENGINE
# ==============================================================================

class HierarchyEngine:
    MULT_PATTERN = re.compile(r'(\d+)\s*[×xX]\s*([A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+)')
    ID_PATTERN = re.compile(r'\b([A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,})\b')
    JUNK_IDS = {'N', 'Z', 'Tax', 'Mean', 'Dist', 'Snap', 'SOP', 'MATH', 'ALGO'}

    def __init__(self, kb: Dict):
        self.kb = kb
        self._decomp_cache: Dict[str, Dict[str, int]] = {}
        self._level_cache: Dict[str, int] = {}

    def parse_components(self, math_str: str) -> Dict[str, int]:
        if not math_str or math_str in ('atomic', 'absolute_primitive', ''): return {}
        components: Dict[str, int] = {}
        for mult_str, comp_id in self.MULT_PATTERN.findall(math_str):
            if comp_id in self.kb: components[comp_id] = components.get(comp_id, 0) + int(mult_str)
        used = set(components.keys())
        for comp_id in self.ID_PATTERN.findall(math_str):
            if comp_id not in used and comp_id not in self.JUNK_IDS and comp_id in self.kb:
                components[comp_id] = components.get(comp_id, 0) + 1
        return components

    def decompose_to_primitives(self, ubp_id: str, depth: int = 0, max_depth: int = 20) -> Dict[str, int]:
        if ubp_id in self._decomp_cache: return dict(self._decomp_cache[ubp_id])
        if depth > max_depth: return {ubp_id: 1}
        entry = self.kb.get(ubp_id)
        if not entry: return {ubp_id: 1}
        components = self.parse_components(entry.get('math', ''))
        if not components: components = self.parse_components(entry.get('atlas', {}).get('hierarchy', ''))
        if not components:
            res = {ubp_id: 1}; self._decomp_cache[ubp_id] = res; return res
        total: Dict[str, int] = {}
        for comp_id, count in components.items():
            sub = self.decompose_to_primitives(comp_id, depth + 1, max_depth)
            for prim_id, prim_count in sub.items():
                total[prim_id] = total.get(prim_id, 0) + prim_count * count
        self._decomp_cache[ubp_id] = total
        return dict(total)

    def get_hierarchy_level(self, ubp_id: str, _visited: Optional[Set] = None) -> int:
        if ubp_id in self._level_cache: return self._level_cache[ubp_id]
        if _visited is None: _visited = set()
        if ubp_id in _visited: return 0
        _visited.add(ubp_id)
        entry = self.kb.get(ubp_id)
        if not entry: return -1
        components = self.parse_components(entry.get('math', ''))
        if not components: components = self.parse_components(entry.get('atlas', {}).get('hierarchy', ''))
        if not components:
            self._level_cache[ubp_id] = 0; return 0
        max_child = max(self.get_hierarchy_level(cid, _visited) for cid in components)
        self._level_cache[ubp_id] = max_child + 1
        return max_child + 1

# ==============================================================================
# SECTION 5: KB MANAGER
# ==============================================================================

class KBManager:
    CATEGORY_PRIORITY = {'PARTICLE': 100, 'ELEM': 90, 'MOLECULE': 80, 'LAW': 20}
    def __init__(self):
        self.kb: Dict[str, Dict] = {}
        self.lexicon_index = defaultdict(list)
        self.short_name_index = {}
        self.stats = {'total_entries': 0, 'lexicon_terms': 0}

    def load(self, paths: List[str]) -> int:
        for path in paths:
            if not os.path.exists(path): continue
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'objects' in data: data = data['objects']
                for key, entry in data.items():
                    if isinstance(entry, dict) and 'ubp_id' in entry:
                        self.kb[entry['ubp_id']] = entry
        self._build_indexes()
        return len(self.kb)

    def _build_indexes(self):
        for uid, entry in self.kb.items():
            name = extract_name(entry).lower()
            self.short_name_index[name] = uid
            for word in re.findall(r'\b\w{3,}\b', name + " " + extract_description(entry).lower()):
                self.lexicon_index[word].append(uid)
        self.stats['total_entries'] = len(self.kb)
        self.stats['lexicon_terms'] = len(self.lexicon_index)

# ==============================================================================
# SECTION 6: UBP BRAIN
# ==============================================================================

@dataclass
class ReasoningResult:
    query: str
    response: str
    primary_concept: Any
    final_vector: List[int]
    final_nrci: Fraction
    coherence_snap: bool
    primitive_decomposition: Dict[str, int]
    layer: str

class UBPBrain:
    def __init__(self):
        self.vector_engine = UBPVectorEngine()
        self.kb_manager = KBManager()
        self.hierarchy = None
        self.initialized = False

    def initialize(self, kb_paths: List[str]) -> bool:
        n = self.kb_manager.load(kb_paths)
        if n > 0:
            self.hierarchy = HierarchyEngine(self.kb_manager.kb)
            self.initialized = True
            return True
        return False

    def recall(self, query: str, top_k: int = 8) -> List[Dict]:
        query_lower = query.lower()
        words = re.findall(r'\b\w{3,}\b', query_lower)
        candidates = set()
        for w in words:
            if w in self.kb_manager.short_name_index: candidates.add(self.kb_manager.short_name_index[w])
            candidates.update(self.kb_manager.lexicon_index.get(w, [])[:5])
        
        scored = []
        for uid in candidates:
            entry = self.kb_manager.kb[uid]
            vec = extract_vector(entry)
            if vec:
                score = 40.0 if extract_name(entry).lower() in query_lower else 10.0
                scored.append({'ubp_id': uid, 'entry': entry, 'vector': vec, 'score': score})
        return sorted(scored, key=lambda x: -x['score'])[:top_k]

    def process_query(self, query: str) -> ReasoningResult:
        candidates = self.recall(query)
        if not candidates: return ReasoningResult(query, "No resonance.", None, [0]*24, Fraction(0), False, {}, 'none')
        
        # Analog Center of Mass
        analog_vec = [0.0] * 24
        weight_sum = sum(c['score'] for c in candidates[:4])
        for c in candidates[:4]:
            for i, bit in enumerate(c['vector']):
                analog_vec[i] += (1.0 if bit == 1 else -1.0) * (c['score'] / weight_sum)
        
        snapped, confidence, _ = self.vector_engine.coherence_snap_soft(analog_vec)
        top = candidates[0]['entry']
        prims = self.hierarchy.decompose_to_primitives(top['ubp_id'])
        
        resp = f"**{extract_name(top)}** ({top['ubp_id']})\n{extract_description(top)}\n"
        resp += f"NRCI: {float(extract_nrci(top)):.4f} | Recall Confidence: {confidence:.2%}"

        return ReasoningResult(
            query=query, response=resp, primary_concept=top,
            final_vector=snapped, final_nrci=extract_nrci(top),
            coherence_snap=confidence < 0.99, primitive_decomposition=prims,
            layer='belief' if is_belief(top) else 'understanding'
        )

if __name__ == "__main__":
    brain = UBPBrain()
    if os.path.exists('ubp_system_kb.json'):
        brain.initialize(['ubp_system_kb.json'])
        print(brain.process_query("What is water?").response)