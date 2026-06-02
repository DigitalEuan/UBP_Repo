"""
GLM Grammar Lattice Integration Patch v2.2
===========================================
Patches the GLM response system to produce human-readable, KB-grounded responses
using the A* Reasoner and the expanded Priority Vocabulary.

Improvements:
- Restored engine-level monkey-patching for GLMDialogueEngine.
- Uses A* Reasoner (ubp_grammatical_diffusion) for optimal paths.
- Provides ontological health verification and word-level confidence.
"""

from __future__ import annotations
import json
import re
from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Any


# ── caches ────────────────────────────────────────────────────────────────────
_zoned_vocab_cache   = None   # ZonedVocabulary
_reasoner_cache      = None   # GrammaticalDiffusionReasoner
_system_kb_cache: Dict[str, dict] = {}   # ubp_id → {ubp_id, name, desc, vector, nrci}
_alias_map_cache: Dict[str, str]  = {}   # plain word → ubp_id


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM KB INDEX
# ═══════════════════════════════════════════════════════════════════════════════

def _load_system_kb(path: str = "ubp_system_kb.json") -> Dict[str, dict]:
    global _system_kb_cache
    if _system_kb_cache:
        return _system_kb_cache
    try:
        import os
        actual_path = path
        if not os.path.exists(actual_path):
            potential = os.path.join("..", "system_kb", path)
            if os.path.exists(potential):
                actual_path = potential

        with open(actual_path) as f:
            kb = json.load(f)
        entries = kb["entries"]
        for h, v in entries.items():
            if not isinstance(v, list) or len(v) < 6:
                continue
            uid     = v[0]
            lexicon = str(v[1])
            vector  = v[3] if len(v) > 3 else []
            nrci    = float(v[5]) if len(v) > 5 else 0.0
            m = re.search(r'\[([^\]]{3,})\].*?\[([^\]]{10,})\]', lexicon)
            name = m.group(1).strip() if m else uid
            desc = m.group(2).strip() if m else ""
            _system_kb_cache[uid] = {
                "ubp_id": uid, "name": name, "desc": desc,
                "vector": vector, "nrci": nrci,
            }
    except Exception:
        pass
    return _system_kb_cache

_CONCEPT_ALIASES: Dict[str, str] = {
    "monster":        "LAW_MONSTROUS_MOONSHINE_001",
    "golay":          "LAW_GOLAY_UNIQUENESS_001",
    "leech":          "LAW_LEECH_TENSION_001",
    "lattice":        "LAW_LEECH_TENSION_001",
    "proton":         "PARTICLE_PROTON_001",
    "electron":       "PARTICLE_ELECTRON_001",
    "photon":         "PARTICLE_PHOTON_001",
    "neutron":        "PARTICLE_NEUTRON_001",
    "nrci":           "LAW_GEOMETRIC_NRCI",
    "coherence":      "LAW_GEOMETRIC_NRCI",
    "water":          "MOLECULE_H2O_001",
}

_FILL_ELEMENTS = {
    "ELEM_He_002", "ELEM_Li_003", "ELEM_Be_004", "ELEM_B_005",
}

def _build_alias_map() -> Dict[str, str]:
    global _alias_map_cache
    if _alias_map_cache:
        return _alias_map_cache
    kb = _load_system_kb()
    for uid, entry in kb.items():
        for text in [entry["name"], entry["desc"][:60]]:
            words = re.sub(r"[^a-z0-9 ]", "", text.lower()).split()
            for w in words:
                if len(w) >= 4 and w not in {"with", "that", "this", "from", "have"}:
                    if w not in _alias_map_cache:
                        _alias_map_cache[w] = uid
    _alias_map_cache.update(_CONCEPT_ALIASES)
    return _alias_map_cache

# ═══════════════════════════════════════════════════════════════════════════════
# REASONER SETUP
# ═══════════════════════════════════════════════════════════════════════════════

def _get_reasoner(strict_vocab_path: str = "glm_strict_vocabulary.json"):
    global _zoned_vocab_cache, _reasoner_cache
    if _reasoner_cache is not None:
        return _reasoner_cache

    from glm_lang_database import LANG_DB
    from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner

    _zoned_vocab_cache = LANG_DB
    try:
        from glm_zoned_lattice_embedding import lift_strict_vocabulary
        import os
        if os.path.exists(strict_vocab_path):
            strict = lift_strict_vocabulary(strict_vocab_path)
            for k, v in strict.words.items():
                if k not in _zoned_vocab_cache.words:
                    _zoned_vocab_cache.words[k] = v
    except:
        pass

    _reasoner_cache = GrammaticalDiffusionReasoner(_zoned_vocab_cache)
    return _reasoner_cache

# ═══════════════════════════════════════════════════════════════════════════════
# NOUN SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

def _select_response_nouns(physical_roots, bindings, zv) -> Tuple[Optional[str], Optional[str]]:
    scored = []
    for r in physical_roots:
        uid = r.ubp_id
        score = r.resonance * (0.1 if uid in _FILL_ELEMENTS else 1.0)
        lex = getattr(r, "lexicon", uid)
        key = None
        if lex in zv.words: key = lex
        else:
            short = uid.lower().split("_")[-2] if "_" in uid else uid.lower()
            if short in zv.words: key = short
        scored.append((score, key))

    scored.sort(key=lambda x: x[0], reverse=True)
    nouns = []
    for s, k in scored:
        if k and k in zv.words and zv.words[k].role in ("NOUN", "PROPERTY"):
            if k not in nouns: nouns.append(k)
        if len(nouns) >= 2: break

    n0 = nouns[0] if len(nouns) >= 1 else None
    n1 = nouns[1] if len(nouns) >= 2 else None
    return n0, n1

# ═══════════════════════════════════════════════════════════════════════════════
# SENTENCE ASSEMBLY
# ═══════════════════════════════════════════════════════════════════════════════

def _assemble_sentence(n0, n1, zv, reasoner) -> str:
    if not n0: return "[GLM] Insufficient grounding."

    target = n1 if n1 else n0
    if n0 == target:
        for lemma in ["stable", "correct", "valid", "nrci"]:
            if lemma in zv.words:
                target = lemma
                break

    trace = reasoner.reason(n0, target)

    if trace.path:
        path_strs = []
        for s in trace.path:
            tag = f"[{s.confidence}]" if s.displacement > 0 else ""
            path_strs.append(f"{s.word}{tag}")

        sent = " ".join(path_strs)
        if trace.target_reached:
            sent += f". (NRCI={float(trace.nrci_final):.3f})"
        else:
            sent += "... [partial path]"
        return sent

    return f"{n0} is grounded in the lattice."

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN COMPOSER
# ═══════════════════════════════════════════════════════════════════════════════

def build_glm_response(physical_roots, bindings, query: str) -> str:
    try:
        reasoner = _get_reasoner()
        zv = _zoned_vocab_cache
    except Exception as e:
        return f"[GLM Error] {e}"

    parts = []

    # 1. Describe primary root
    primary = max(physical_roots, key=lambda r: r.resonance) if physical_roots else None
    if primary:
        kb = _load_system_kb()
        entry = kb.get(primary.ubp_id, {})
        name = entry.get("name", primary.ubp_id)
        desc = entry.get("desc", "")
        intro = f"[{name}] (res={primary.resonance:.2f}, NRCI={primary.nrci:.3f})"
        desc_sentence = ""
        if desc:
            m = re.match(r'([^.]{10,}\.)', desc)
            desc_sentence = m.group(1).strip() if m else desc[:120].strip()
        parts.append(f"{intro} — {desc_sentence}" if desc_sentence else intro)

    # 2. Build grammatical sentence
    n0, n1 = _select_response_nouns(physical_roots, bindings, zv)
    sent = _assemble_sentence(n0, n1, zv, reasoner)
    parts.append(sent)

    # 3. Math Verification
    if primary and hasattr(primary, "vector"):
        try:
            from ubp_unified_v5 import LEECH_ENGINE
            health = LEECH_ENGINE.ontological_health(primary.vector)
            h_str = ", ".join(f"{k}:{float(v):.2f}" for k, v in health.items() if k != "Global_NRCI")
            parts.append(f"[Math Verification] Ontological Health ({h_str})")
        except: pass

    return "  |  ".join(parts)

# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE-LEVEL PATCH
# ═══════════════════════════════════════════════════════════════════════════════

def _apply_patch():
    try:
        from glm_engine import GLMDialogueEngine, PhysicalRoot
        from dataclasses import replace as dc_replace
    except ImportError:
        return

    kb = _load_system_kb()
    alias = _build_alias_map()
    _orig_ground = GLMDialogueEngine._ground_physically

    def _patched_ground(self, concepts, max_depth):
        roots = []
        new_ids = set()
        grounded_concepts = set()
        
        try:
            from ubp_unified_v5 import LEECH_ENGINE
        except ImportError:
            return _orig_ground(self, concepts, max_depth)

        for concept in concepts:
            uid = alias.get(concept)
            if uid and uid in kb:
                entry = kb[uid]
                vec = entry["vector"]
                if not vec: continue
                nrci = float(LEECH_ENGINE.calculate_nrci(vec))
                roots.append(PhysicalRoot(
                    ubp_id=uid, vector=vec, lexicon=concept,
                    resonance=1.0, nrci=nrci
                ))
                new_ids.add(uid)
                grounded_concepts.add(concept)

        remaining = [c for c in concepts if c not in grounded_concepts]
        if remaining:
            fuzzy_roots, gaps = _orig_ground(self, remaining, max_depth)
            for r in fuzzy_roots:
                if r.ubp_id not in new_ids:
                    roots.append(r)
                    new_ids.add(r.ubp_id)
        else: gaps = []

        protected_ids = {alias.get(c) for c in grounded_concepts if alias.get(c)}
        non_fill = [r for r in roots if r.ubp_id not in _FILL_ELEMENTS or r.ubp_id in protected_ids]
        fill = [r for r in roots if r.ubp_id in _FILL_ELEMENTS and r.ubp_id not in protected_ids]
        for r in fill: r.resonance *= 0.5

        combined = sorted(non_fill + fill, key=lambda r: r.resonance, reverse=True)
        return combined[:4], gaps

    GLMDialogueEngine._ground_physically = _patched_ground
    _orig_respond = GLMDialogueEngine.respond

    def _patched_respond(self, query, max_depth=3):
        turn = _orig_respond(self, query, max_depth)
        new_text = build_glm_response(turn.physical_roots, turn.lexical_bindings, query)
        turn = dc_replace(turn, response=new_text)
        if self.turn_history and self.turn_history[-1].query == query:
            self.turn_history[-1] = turn
        return turn

    GLMDialogueEngine.respond = _patched_respond

# Execute patch on import
_apply_patch()

if __name__ == "__main__":
    print("GLM Grammar Patch v2.2 active.")
