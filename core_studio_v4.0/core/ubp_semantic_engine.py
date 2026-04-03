"""
================================================================================
UBP SEMANTIC QUERY ENGINE v8.0 — COSINE RESONANCE & THINKING TRACE
================================================================================
Author: E R A Craig & UBP Research Cortex v4.2.7
Date: 03 April 2026

THE PROPER LOGIC:
1.  TOKEN WEIGHTING: Matter (ELEM/MOLECULE) = 5.0, Actions (OP) = 2.0.
2.  INTENT SUPERPOSITION: Creates a weighted bipolar "Query Chord".
3.  COSINE RESONANCE: Measures the angular alignment between Query and Laws.
4.  SEMANTIC REFLECTION: Maps the physical result back to the Language KB.
5.  THINKING TRACE: Explicitly outputs the detected "Geometric Probes".
================================================================================
"""

import json
import re
import os
import math
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass

@dataclass
class SemanticResult:
    ubp_id: str
    lexicon: str
    resonance_score: float
    nrci: float
    reflection: str = "" 

    def summary(self) -> str:
        res = f"[Resonance: {self.resonance_score:.4f}] {self.ubp_id} (NRCI: {self.nrci:.4f})\n"
        res += f"    Lexicon: {self.lexicon[:110]}...\n"
        if self.reflection:
            res += f"    Reflection: This physical state resonates with the concept of '{self.reflection}'"
        return res

class UBPSemanticEngine:
    STOP_WORDS = {'what', 'is', 'the', 'of', 'to', 'in', 'and', 'for', 'with', 'on', 'about', 'does', 'why'}

    def __init__(self):
        self.system_kb: Dict[str, dict] = {}
        self.lang_kb: Dict[str, dict] = {}
        self.all_kb: Dict[str, dict] = {}
        self.name_index: Dict[str, str] = {}
        self.bigram_index: Dict[str, str] = {}
        self._system_vectors: Dict[str, List[float]] = {}
        self._lang_vectors: Dict[str, List[float]] = {}

    def load(self, system_path: str, lang_path: str):
        """Hydrates columnar data into rich internal dictionaries."""
        for path, target_dict in [(system_path, self.system_kb), (lang_path, self.lang_kb)]:
            if not os.path.exists(path): continue
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict) and "_fields" in data:
                fields = data["_fields"]
                f_idx = {name: i for i, name in enumerate(fields)}
                for fp, entry_list in data["entries"].items():
                    uid = entry_list[f_idx["ubp_id"]]
                    entry_dict = {
                        "ubp_id": uid,
                        "lexicon": entry_list[f_idx["lexicon"]],
                        "tags": entry_list[f_idx["tags"]],
                        "vector": entry_list[f_idx["vector"]],
                        "nrci_val": entry_list[f_idx["nrci_val"]]
                    }
                    target_dict[uid] = entry_dict
                    self.all_kb[uid] = entry_dict
            
        for uid, entry in self.system_kb.items():
            v = entry.get('vector')
            if v: self._system_vectors[uid] = [(b * 2) - 1 for b in v]
        for uid, entry in self.lang_kb.items():
            v = entry.get('vector')
            if v: self._lang_vectors[uid] = [(b * 2) - 1 for b in v]
            
        self._build_indexes()
        print(f"[SemanticEngine] Stack Online: {len(self.system_kb)} Physics + {len(self.lang_kb)} Language entries.")

    def _build_indexes(self):
        """Maps names, bigrams, and tags to IDs with Primary Priority."""
        for uid, entry in self.all_kb.items():
            lex = entry.get('lexicon', '').lower()
            try:
                name = lex.split(']')[0].strip('[]').split(':')[-1].strip()
                if name:
                    # PRIORITY: If it's a primary element (Z=1-20), it takes index precedence
                    if uid.startswith('ELEM_') and int(uid.split('_')[-1]) <= 20:
                        self.name_index[name] = uid
                    elif name not in self.name_index:
                        self.name_index[name] = uid
                    
                    words = name.split()
                    if len(words) >= 2:
                        self.bigram_index[' '.join(words[:2])] = uid
            except: pass
            for tag in entry.get('tags', []):
                if tag.lower() not in self.name_index:
                    self.name_index[tag.lower()] = uid

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = sum(a**2 for a in v1)**0.5
        mag2 = sum(b**2 for b in v2)**0.5
        if mag1 == 0 or mag2 == 0: return 0.0
        return dot / (mag1 * mag2)

    def _reflect_meaning(self, vector: List[float]) -> str:
        best_word, max_sim = "Unknown", -1.0
        for uid, v in self._lang_vectors.items():
            sim = self._cosine_similarity(vector, v)
            if sim > max_sim:
                max_sim = sim
                best_word = uid.replace('OP_', '').replace('_', ' ').title()
        return best_word

    def query(self, text: str, top_k: int = 5):
        q_clean = re.sub(r'[^a-z0-9 ]', '', text.lower()).split()
        
        weighted_probes = []
        trace_log = []
        i = 0
        while i < len(q_clean):
            word = q_clean[i]
            found = False
            # 1. Check Bigrams (High Weight)
            if i + 1 < len(q_clean):
                bi = f"{q_clean[i]} {q_clean[i+1]}"
                if bi in self.bigram_index:
                    uid = self.bigram_index[bi]
                    vec = self._system_vectors.get(uid) or self._lang_vectors.get(uid)
                    if vec:
                        w = 8.0 # Bigrams are very specific
                        weighted_probes.append((vec, w))
                        trace_log.append(f"'{bi}' ({uid}) [w={w}]")
                        i += 2; found = True
            
            # 2. Check Unigrams
            if not found and word in self.name_index:
                uid = self.name_index[word]
                vec = self._system_vectors.get(uid) or self._lang_vectors.get(uid)
                if vec:
                    # MATTER DOMINANCE
                    if uid.startswith(('ELEM_', 'MOLECULE_')): w = 10.0
                    elif uid.startswith('OP_'): 
                        # Context words are "Satellites"
                        w = 0.5 if word in ['why', 'does', 'with', 'is', 'the'] else 2.0
                    else: w = 1.0
                    
                    weighted_probes.append((vec, w))
                    trace_log.append(f"'{word}' ({uid}) [w={w}]")
                i += 1
            elif not found: i += 1
        
        if not weighted_probes: return []
        print(f"  [Thinking] Probes: {', '.join(trace_log)}")

        # 3. INTENT SUPERPOSITION
        intent_vec = [0.0] * 24
        for vec, weight in weighted_probes:
            for j in range(24):
                intent_vec[j] += vec[j] * weight

        # 4. LATTICE RESONANCE (Cosine)
        results = []
        # Extract IDs of subjects mentioned to avoid element-collisions
        subjects = [p[1].split('(')[1].split(')')[0] for p in [t.split() for t in trace_log] if 'ELEM_' in p[1]]

        for uid, sys_vec in self._system_vectors.items():
            # GATING: If we mentioned specific elements, don't show unrelated ones (like Antimony)
            if subjects and uid.startswith('ELEM_') and uid not in subjects:
                continue

            resonance = self._cosine_similarity(intent_vec, sys_vec)
            if resonance > 0.3: 
                entry = self.system_kb[uid]
                reflection = self._reflect_meaning(sys_vec)
                
                results.append(SemanticResult(
                    ubp_id=uid,
                    lexicon=entry['lexicon'],
                    resonance_score=resonance,
                    nrci=float(entry.get('nrci_val', 0.5)),
                    reflection=reflection
                ))
        
        return sorted(results, key=lambda x: x.resonance_score, reverse=True)[:top_k]

    def query_display(self, text: str):
        print(f"\n{'═'*70}\n  UBP SEMANTIC INFERENCE: {text}\n{'═'*70}")
        results = self.query(text)
        if not results:
            print("  [Null Resonance] — The query did not trigger any stable anchors.")
        for r in results:
            print(r.summary())

if __name__ == '__main__':
    engine = UBPSemanticEngine()
    engine.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
    engine.query_display("why does hydrogen bond with oxygen?")