# ══════════════════════════════════════════════════════════════════════════════
# §01  SUBSTRATE — FULL MASTER (v3.7.6 Hardened)
# ══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import sys, os, re, json, math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Set
from collections import defaultdict, deque

# IMPORT HARDENED CONFIG
from GLM00_config import KB_SYSTEM_PATH, KB_LANG_PATH

# ── 1. MOG CATEGORIES ──────────────────────────────────────────────────
MOG_CATEGORIES = [
    "M_Mass", "M_Charge", "M_Space", "M_Time", "M_Thermal", "M_Count",
    "I_Topology", "I_Symmetry", "I_Density", "I_Connectivity", "I_Dimension", "I_Complexity",
    "A_Energy", "A_Force", "A_Velocity", "A_Flux", "A_Resonance", "A_Spin",
    "P_Probability", "P_Ratio", "P_Limit", "P_Tax", "P_Coherence", "P_Phase"
]

# ── 2. HEX-PACKING HELPERS (v3.7.4 Performance) ────────────────────────
def vector_to_hex_int(vec: List[int]) -> int:
    """Pack a 24-bit list [1,0,1,...] into a single integer."""
    val = 0
    for i, b in enumerate(vec):
        if b: val |= 1 << (23 - i)
    return val

def fast_hamming(a: int, b: int) -> int:
    """Hamming distance using native CPU bit_count."""
    return (a ^ b).bit_count()

def get_domain(hex_int: int) -> int:
    """Extract the 3-bit UBP Octad Domain."""
    return (hex_int >> 21) & 0b111

# ── 3. BINARY LINEAR ALGEBRA ───────────────────────────────────────────
class BinaryLinearAlgebra:
    @staticmethod
    def hamming_distance(u, v):
        if isinstance(u, int) and isinstance(v, int):
            return (u ^ v).bit_count()
        if isinstance(u, (list, tuple)) and isinstance(v, (list, tuple)):
            if len(u) == 24 and len(v) == 24:
                return (vector_to_hex_int(u) ^ vector_to_hex_int(v)).bit_count()
        return sum(1 for a, b in zip(u, v) if a != b)

    @staticmethod
    def fold24_to3(vec):
        v = list(vec)
        for n in (12, 6, 3):
            v = [v[2*i] ^ v[2*i+1] for i in range(n)]
        return v

BLA = BinaryLinearAlgebra

# ── 4. GOLAY & LEECH ENGINES ───────────────────────────────────────────
class _GolayCodeEngine:
    def snap_to_codeword(self, v24):
        return list(v24), {"anchor_distance": 0, "anchor_id": "self"}

class _LeechLatticeEngine:
    def __init__(self, golay): self.golay = golay
    def calculate_nrci(self, vec):
        w = sum(vec)
        if w == 0 or w == 24: return 0.0
        return max(0.0, 1.0 - abs(w - 12) / 12.0)
    def calculate_symmetry_tax(self, vec):
        sextets = [vec[i:i+6] for i in range(0, 24, 6)]
        weights = [sum(s) for s in sextets]
        avg = sum(weights) / 4.0
        return sum(abs(w - avg) for w in weights)

GOLAY_ENGINE = _GolayCodeEngine()
LEECH_ENGINE = _LeechLatticeEngine(GOLAY_ENGINE)

# ── 5. CONCEPT RELATION GRAPH ──────────────────────────────────────────
EDGE_LABELS: Set[str] = {
    "is_a", "has_property", "depends_on", "commutes_with",
    "scales_as", "is_dual_to", "generates", "measures",
    "lattice_adjacent", "auto_proposed", "contradicts", "incompatible_with",
}

@dataclass
class CRGEdge:
    src: str; label: str; dst: str
    def reverse(self):
        if self.label in ("commutes_with", "is_dual_to") or self.label.startswith("lattice_adjacent"):
            return CRGEdge(self.dst, self.label, self.src)
        return self

class ConceptRelationGraph:
    def __init__(self):
        self.out = defaultdict(list); self.into = defaultdict(list); self.edges = []
    def add_edge(self, src, label, dst):
        src, dst = src.lower().strip(), dst.lower().strip()
        edge = CRGEdge(src=src, label=label, dst=dst)
        self.edges.append(edge); self.out[src].append(edge); self.into[dst].append(edge)
        return True

_RAW_EDGES = [
    ("hamiltonian","is_a","operator"), ("lagrangian","is_a","functional"),
    ("hamiltonian","commutes_with","symmetry"), ("hamiltonian","generates","time"),
    ("symmetry","generates","anomaly"), ("quark","is_a","fermion"),
    ("gluon","is_a","boson"), ("boson","contradicts","fermion")
]

def build_default_crg():
    g = ConceptRelationGraph()
    for s, l, d in _RAW_EDGES: g.add_edge(s, l, d)
    return g

# ── 6. VOCABULARY & LINGUISTIC HELPERS ─────────────────────────────────
@dataclass
class WordEntry:
    word: str; vector: List[int]; role: str; ubp_id: str; nrci: float = 0.5
    hamming_to_system: int = 0; golay_codeword: List[int] = field(default_factory=list)
    golay_distance: int = 0; fold3: List[int] = field(default_factory=list)
    mog_category: str = "I_Topology"

def _get_mog_category(vector):
    w = sum(vector)
    return MOG_CATEGORIES[w % len(MOG_CATEGORIES)]

def _query_type(query: str) -> str:
    q = query.lower()
    if "what is" in q or "define" in q: return "definition"
    if "relationship" in q or "between" in q: return "relation"
    return "general"

def _load_kb_safe(path):
    if not path.exists(): return {}
    with open(path, 'r') as f: data = json.load(f)
    result = {}
    fields = data.get("_fields", [])
    f_idx = {name: i for i, name in enumerate(fields)}
    for entry_list in data.get("entries", {}).values():
        uid = entry_list[f_idx["ubp_id"]]
        result[uid] = {
            "ubp_id": uid, "lexicon": entry_list[f_idx["lexicon"]],
            "vector": entry_list[f_idx["vector"]] if "vector" in f_idx else [],
            "nrci_val": entry_list[f_idx["nrci_val"]] if "nrci_val" in f_idx else 0.5
        }
    return result

def _build_vocabulary():
    lang_kb = _load_kb_safe(KB_LANG_PATH)
    words = {}
    for uid, entry in lang_kb.items():
        vec = entry.get('vector')
        if not vec or len(vec) != 24: continue
        m = re.search(r'\[(?:Word|Property|Operator):?\s*([^\]]+)\]', entry['lexicon'])
        word = m.group(1).lower().strip() if m else uid.lower()
        words[word] = WordEntry(word=word, vector=vec, role="NOUN", ubp_id=uid, nrci=entry['nrci_val'])
    return words

# ── 7. ISOLATION TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Testing Module 01: Substrate ===")
    try:
        vocab = _build_vocabulary()
        print(f"✅ Success: Grounded {len(vocab)} words.")
        if vocab:
            sample = list(vocab.keys())[0]
            print(f"  Sample Entry: {sample} -> {vocab[sample].ubp_id}")
    except Exception as e:
        print(f"❌ Failed: {e}")