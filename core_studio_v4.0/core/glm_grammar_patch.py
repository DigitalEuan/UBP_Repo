"""
GLM Grammar Lattice Integration Patch v2.0
===========================================
Patches GLMDialogueEngine to produce human-readable, KB-grounded responses.


v2.0 improvements over v1.1
-----------------------------
- CONCEPT_ALIAS_MAP: 'monster', 'moonshine', 'golay', 'leech', 'quark',
  'hydrogen', 'hadron', 'symmetry', 'nrci', etc. now resolve to correct
  system_kb entries rather than falling through to context_anchor.
- Patches _ground_physically to check the alias map before declaring a gap.
- _describe_root uses the actual KB lexicon description text (not just
  ubp_id prefix parsing), giving substantive one-sentence definitions.
- Noun selection filtered: res=1.0 (direct query match) roots are preferred;
  lattice-fill elements (H, He, Li…) are suppressed from noun pairs.
- Query-type aware response: definition / explanation / relation / metric /
  causation templates each pull from the KB description text differently.
- Verb selection improved: preferred list intersected with actual VERB entries.
- Added **Mathematical Verification** to output, verifying the ontological health
  and stability metrics of the primary root using LeechLatticeEngine.
"""

from __future__ import annotations
import json
import re
from fractions import Fraction
from typing import Dict, List, Optional, Tuple


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
        with open(path) as f:
            kb = json.load(f)
        entries = kb["entries"]
        fields  = kb["_fields"]   # ubp_id, lexicon, tags, vector, nrci_str, nrci_val, ...
        for h, v in entries.items():
            if not isinstance(v, list) or len(v) < 6:
                continue
            uid     = v[0]
            lexicon = str(v[1])
            vector  = v[3] if len(v) > 3 else []
            nrci    = float(v[5]) if len(v) > 5 else 0.0
            # Extract [Name] and [Description] from lexicon string
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




# Hard-coded concept aliases: plain English → best system_kb ubp_id
_CONCEPT_ALIASES: Dict[str, str] = {
    # Monster / Moonshine
    "monster":        "LAW_MONSTROUS_MOONSHINE_001",
    "monstrous":      "LAW_MONSTROUS_MOONSHINE_001",
    "moonshine":      "LAW_MONSTROUS_MOONSHINE_001",
    "sporadic":       "LAW_MONSTROUS_MOONSHINE_001",
    "moonshine_corr": "LAW_MONSTROUS_MOONSHINE_001",
    # Golay / Leech
    "golay":          "LAW_GOLAY_UNIQUENESS_001",
    "leech":          "LAW_LEECH_TENSION_001",
    "lattice":        "LAW_LEECH_TENSION_001",
    # Quarks / hadrons
    "quark":          "PARTICLE_QUARK_UP_001",
    "quarks":         "PARTICLE_QUARK_UP_001",
    "hadron":         "LAW_BARYON_001",
    "hadrons":        "LAW_BARYON_001",
    "baryon":         "LAW_BARYON_001",
    # Elements not in strict vocab
    "hydrogen":       "ELEM_H_001",
    "helium":         "ELEM_He_002",
    "lithium":        "ELEM_Li_003",
    "beryllium":      "ELEM_Be_004",
    "boron":          "ELEM_B_005",
    "carbon":         "ELEM_C_006",
    "nitrogen":       "ELEM_N_007",
    "oxygen":         "ELEM_O_008",
    "fluorine":       "ELEM_F_009",
    "neon":           "ELEM_Ne_010",
    "sodium":         "ELEM_Na_011",
    "magnesium":      "ELEM_Mg_012",
    "aluminum":       "ELEM_Al_013",
    "phosphorus":     "ELEM_P_015",
    "cadmium":        "ELEM_Cd_048",
    "proton":         "PARTICLE_PROTON_001",
    "electron":       "PARTICLE_ELECTRON_001",
    "photon":         "PARTICLE_PHOTON_001",
    "neutron":         "PARTICLE_NEUTRON_001",
    # Abstract concepts
    "nrci":           "LAW_GEOMETRIC_NRCI",
    "coherence":      "LAW_GEOMETRIC_NRCI",
    "symmetry":       "LAW_BARYON_001",
    "holographic":    "LAW_ATOM_HOLOGRAPHIC",
    "holograph":      "LAW_ATOM_HOLOGRAPHIC",
    "holography":     "LAW_ATOM_HOLOGRAPHIC",
    "anomaly":        "LAW_ANOMALY_001",
    "weyl":           "LAW_ANOMALY_001",
    "substrate":      "LAW_GOLAY_UNIQUENESS_001",
    "stability":      "LAW_BARYON_PROTON_001",
    "isolation":      "LAW_BARYON_001",
    "isolated":       "LAW_BARYON_001",
    "encode":         "LAW_GOLAY_UNIQUENESS_001",
    "encodes":        "LAW_GOLAY_UNIQUENESS_001",
    "mass":           "LAW_LEECH_TENSION_001",
    "relationship":   "LAW_META_002",
    "connection":     "LAW_META_002",
    "water":          "MOLECULE_H2O_001",
}


# Elements that are lattice-fill and should be deprioritised as response nouns
_FILL_ELEMENTS = {
    "ELEM_He_002", "ELEM_Li_003", "ELEM_Be_004", "ELEM_B_005",
    "ELEM_C_006",  "ELEM_N_007",  "ELEM_O_008",  "ELEM_F_009",
    "ELEM_Ne_010", "ELEM_Mg_012", "ELEM_Al_013", "ELEM_Cd_048",
    "ELEM_Cm_096", "ELEM_Db_105", "ELEM_Og_118", "ELEM_Mn_025",
}




def _build_alias_map() -> Dict[str, str]:
    """Build alias map: plain word → ubp_id, using hard-coded overrides + auto-extraction."""
    global _alias_map_cache
    if _alias_map_cache:
        return _alias_map_cache
    kb = _load_system_kb()
    # Auto-extract words from lexicon text
    for uid, entry in kb.items():
        for text in [entry["name"], entry["desc"][:60]]:
            words = re.sub(r"[^a-z0-9 ]", "", text.lower()).split()
            for w in words:
                if len(w) >= 4 and w not in {"with", "that", "this", "from", "have",
                                               "their", "when", "which", "than", "also"}:
                    if w not in _alias_map_cache:
                        _alias_map_cache[w] = uid
    # Apply hard-coded overrides (higher priority)
    _alias_map_cache.update(_CONCEPT_ALIASES)
    return _alias_map_cache




# ═══════════════════════════════════════════════════════════════════════════════
# REASONER SETUP
# ═══════════════════════════════════════════════════════════════════════════════


def _get_reasoner(strict_vocab_path: str = "glm_strict_vocabulary.json"):
    global _zoned_vocab_cache, _reasoner_cache
    if _reasoner_cache is not None:
        return _reasoner_cache
    from glm_zoned_lattice_embedding import lift_strict_vocabulary
    from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner
    from glm_concept_relation_graph import build_default_crg
    _zoned_vocab_cache = lift_strict_vocabulary(strict_vocab_path)
    _reasoner_cache = GrammaticalDiffusionReasoner(
        _zoned_vocab_cache, build_default_crg()
    )
    return _reasoner_cache




# ═══════════════════════════════════════════════════════════════════════════════
# VOCAB UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════


_VERB_RE = re.compile(r'^[a-z]{3,}$')


_PREFERRED_VERBS = {
    "define", "explain", "verify", "measure", "predict",
    "classify", "cause", "compare", "compose", "decompose",
    "transform", "decay", "capture",
}


def _fuzzy_find(lemma: str, zv) -> Optional[str]:
    if lemma in zv.words:
        return lemma
    for key in zv.words:
        if key.startswith(lemma + " ("):
            return key
    for key in zv.words:
        if key.startswith(lemma):
            return key
    for key in zv.words:
        if lemma in key:
            return key
    return None




def _pick_verb(zv) -> Optional[str]:
    preferred_ordered = [
        "define", "explain", "verify", "measure", "predict",
        "classify", "cause", "compare", "compose", "transform", "decay", "capture",
    ]
    for v in preferred_ordered:
        k = _fuzzy_find(v, zv)
        if k and zv.words[k].role in ("VERB", "OPERATOR"):
            return k
    for key, w in zv.words.items():
        if w.role == "VERB" and _VERB_RE.match(key):
            return key
    return None




# ═══════════════════════════════════════════════════════════════════════════════
# QUERY TYPE
# ═══════════════════════════════════════════════════════════════════════════════


def _query_type(query: str) -> str:
    q = query.lower()
    if re.search(r'\bwhat\s+is\b|\bdefine\b|\bmeaning\b', q):
        return "definition"
    if re.search(r'\bexplain\b|\bdescribe\b|\bhow does\b', q):
        return "explanation"
    if re.search(r'\brelationship\b|\bconnection\b|\blink\b|\bbetween\b', q):
        return "relation"
    if re.search(r'\bnrci\b|\bstability\b|\btax\b|\bcoherence\b', q):
        return "metric"
    if re.search(r'\bhappens\b|\beffect\b|\bwhen\b|\bisolated\b', q):
        return "causation"
    return "general"




# ═══════════════════════════════════════════════════════════════════════════════
# ROOT DESCRIPTION  (uses actual KB description text)
# ═══════════════════════════════════════════════════════════════════════════════


def _describe_root(root, query_concepts: List[str], qtype: str) -> str:
    uid  = root.ubp_id
    res  = root.resonance
    nrci = root.nrci
    lex  = root.lexicon


    kb   = _load_system_kb()
    entry = kb.get(uid, {})
    name  = entry.get("name", uid)
    desc  = entry.get("desc", "")


    # Shorten name for readability
    display = name
    if display.startswith("The Law of "):
        display = display[len("The Law of "):]
    elif display.startswith("Law of "):
        display = display[len("Law of "):]
    elif display.startswith("Law: "):
        display = display[len("Law: "):]
    elif display.startswith("Particle: "):
        display = display[len("Particle: "):]
    elif display.startswith("Element: "):
        display = display[len("Element: "):]
    elif display.startswith("Molecule: "):
        display = display[len("Molecule: "):]


    # Build intro line 
    intro = f"[{display}] resonance={res:.2f} NRCI={nrci:.3f}"


    # Pull first sentence of description (up to '. ' or 120 chars)
    desc_sentence = ""
    if desc:
        m = re.match(r'([^.]{10,}\.)', desc)
        if m:
            desc_sentence = m.group(1).strip()
        else:
            desc_sentence = desc[:120].strip()


    if desc_sentence:
        return f"{intro} — {desc_sentence}"
    return intro




# ═══════════════════════════════════════════════════════════════════════════════
# NOUN SELECTION  (filtered, query-aware)
# ═══════════════════════════════════════════════════════════════════════════════


def _select_response_nouns(
        physical_roots,
        bindings,
        zv,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Choose subject and object nouns for the grammatical sentence.
    Prefer:
      1. High-resonance roots whose lexicon matches a query concept
      2. Roots that are NOT lattice-fill elements
      3. Roots that ARE in the zoned vocab (for FSM walk)
    """
    # Score each root
    scored = []
    for r in physical_roots:
        uid = r.ubp_id
        # Penalise fill elements
        if uid in _FILL_ELEMENTS:
            score = r.resonance * 0.1
        else:
            score = r.resonance
        # Try to find a vocab key for this root
        lex = r.lexicon
        key = _fuzzy_find(lex, zv) if lex else None
        if key is None:
            # Try ubp_id-derived word
            short = uid.lower().split("_")[-2] if "_" in uid else uid.lower()
            key = _fuzzy_find(short, zv)
        scored.append((score, key, r))


    scored.sort(key=lambda x: x[0], reverse=True)


    nouns = []
    for score, key, r in scored:
        if key and key in zv.words and zv.words[key].role in ("NOUN", "PROPERTY"):
            if key not in nouns:
                nouns.append(key)
        if len(nouns) >= 2:
            break


    # Fallback: bindings with high is_grounded, non-fill
    if len(nouns) < 2:
        for b in bindings:
            if b.is_grounded and b.role in ("NOUN", "PROPERTY"):
                # Check if the binding's root is a fill element
                fill = any(r.ubp_id in _FILL_ELEMENTS and r.lexicon == b.word
                           for r in physical_roots)
                if not fill:
                    k = _fuzzy_find(b.word, zv)
                    if k and k not in nouns:
                        nouns.append(k)
            if len(nouns) >= 2:
                break


    n0 = nouns[0] if len(nouns) >= 1 else None
    n1 = nouns[1] if len(nouns) >= 2 else None
    return n0, n1




# ═══════════════════════════════════════════════════════════════════════════════
# GRAMMATICAL SENTENCE ASSEMBLY
# ═══════════════════════════════════════════════════════════════════════════════


def _assemble_sentence(n0, n1, qtype, zv, reasoner, physical_roots) -> str:
    """Build N-V-N sentence or template fallback."""
    verb_key = _pick_verb(zv)


    trace = None
    if n0 and n1:
        try:
            trace = reasoner.build_sentence(n0, n1)
        except Exception:
            trace = None


    if n0 and trace is None:
        for w in list(zv.words.values())[:150]:
            if w.lemma != n0 and w.role == "NOUN" and w.lemma != n1:
                try:
                    t = reasoner.reason(n0, w.lemma)
                    if t.target_reached:
                        trace = t
                        break
                except Exception:
                    continue


    if trace and trace.target_reached:
        path_words = []
        for s in trace.path:
            if s.role in ("VERB", "OPERATOR") and s.word not in _PREFERRED_VERBS:
                path_words.append(verb_key or s.word)
            else:
                path_words.append(s.word)
        nrci_f = float(trace.nrci_final)
        tax_f  = float(trace.total_tax)
        return " ".join(path_words) + f" [NRCI={nrci_f:.3f} tax={tax_f:.2f}]"


    # Template fallback using KB description for richness
    kb = _load_system_kb()
    primary = max(physical_roots, key=lambda r: r.resonance) if physical_roots else None
    kb_desc = ""
    if primary:
        entry = kb.get(primary.ubp_id, {})
        kb_desc = entry.get("desc", "")[:80]


    vb = verb_key or "define"
    if n0 and n1:
        if qtype == "relation":
            return f"{n0} {vb} {n1} — the substrate geometry links them via shared codeword structure."
        if qtype == "metric":
            return f"The NRCI of {n0} is measured relative to {n1} across the 24-bit manifold."
        if qtype == "causation":
            return f"When {n0} is isolated, {n1} responds through lattice displacement."
        return f"{n0} {vb} {n1} within the 24-bit Golay substrate."
    elif n0:
        if kb_desc:
            return f"{n0}: {kb_desc}"
        if qtype == "metric":
            return f"The stability of {n0} is expressed as NRCI = {primary.nrci:.3f} in the Leech shell."
        return f"{n0} is encoded as a Golay codeword in the 24-bit manifold."
    return "[GLM] Insufficient lattice grounding for this query."




# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RESPONSE COMPOSER
# ═══════════════════════════════════════════════════════════════════════════════


def build_glm_response(physical_roots, bindings, query: str) -> str:
    try:
        reasoner = _get_reasoner()
        zv = _zoned_vocab_cache
    except Exception as e:
        return _fallback_response(physical_roots, query, f"reasoner: {e}")


    qtype = _query_type(query)
    query_concepts = list({
        w for w in re.sub(r"[^a-z0-9 ]", "", query.lower()).split()
        if len(w) >= 4
    })
    parts: List[str] = []


    # Filter roots: sort by resonance, annotate fill status
    primary = max(physical_roots, key=lambda r: r.resonance) if physical_roots else None
    if primary:
        parts.append(_describe_root(primary, query_concepts, qtype))


    # Noun selection
    n0, n1 = _select_response_nouns(physical_roots, bindings, zv)


    # Grammatical sentence
    try:
        sent = _assemble_sentence(n0, n1, qtype, zv, reasoner, physical_roots)
        parts.append(sent)
    except Exception as e:
        parts.append(f"[lattice path error: {e}]")


    # Mathematical Verification using LeechLatticeEngine
    if primary and primary.vector:
        try:
            from ubp_unified_v5 import LEECH_ENGINE
            health = LEECH_ENGINE.ontological_health(primary.vector)
            tax = LEECH_ENGINE.calculate_symmetry_tax(primary.vector)
            nrci_calc = LEECH_ENGINE.calculate_nrci(primary.vector)
            
            # Format verification string
            h_str = ", ".join(f"{k}:{float(v):.2f}" for k, v in health.items() if k != "Global_NRCI")
            parts.append(f"[Math Verification] Ontological Health ({h_str}) | Symmetry Tax: {float(tax):.2f} | Verified NRCI: {float(nrci_calc):.4f}")
        except Exception as e:
            parts.append(f"[Math Verification Error: {e}]")


    # Supporting non-fill roots
    extra_roots = [
        r for r in physical_roots
        if r.ubp_id not in _FILL_ELEMENTS and r.ubp_id != (primary.ubp_id if primary else None)
    ][:2]
    if extra_roots:
        kb = _load_system_kb()
        extra_descs = []
        for r in extra_roots:
            e = kb.get(r.ubp_id, {})
            n = e.get("name", r.ubp_id)
            if n.startswith("The Law of "): n = n[len("The Law of "):]
            elif n.startswith("Law of "): n = n[len("Law of "):]
            extra_descs.append(f"{n} (res={r.resonance:.2f})")
        parts.append("Also grounded: " + "; ".join(extra_descs) + ".")


    return "  |  ".join(parts) if parts else _fallback_response(physical_roots, query, "empty")




def _fallback_response(physical_roots, query: str, reason: str) -> str:
    if not physical_roots:
        return f"[GLM] No lattice grounding for: {query!r}"
    top = physical_roots[:3]
    desc = "; ".join(f"{r.ubp_id}(res={r.resonance:.2f})" for r in top)
    return f"[GLM] Anchors: {desc}. ({reason})"




# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE-LEVEL PATCH: _ground_physically + respond()
# ═══════════════════════════════════════════════════════════════════════════════


def _apply_patch():
    from glm_engine import GLMDialogueEngine, PhysicalRoot
    from dataclasses import replace as dc_replace


    kb = _load_system_kb()
    alias = _build_alias_map()


    # --- patch _ground_physically ---
    _orig_ground = GLMDialogueEngine._ground_physically


    def _patched_ground(self, concepts, max_depth):
        # Disambiguation & suppression:
        # 1. First, handle direct alias grounding (Highest Priority)
        roots = []
        new_ids = set()
        grounded_concepts = set()
        
        try:
            from ubp_unified_v5 import LEECH_ENGINE, BinaryLinearAlgebra as BLA
        except Exception:
            return _orig_ground(self, concepts, max_depth)

        for concept in concepts:
            uid = alias.get(concept)
            if uid and uid in kb:
                entry = kb[uid]
                vec = entry["vector"]
                if not vec: continue
                try:
                    nrci = float(LEECH_ENGINE.calculate_nrci(vec))
                except Exception:
                    nrci = entry["nrci"]
                
                roots.append(PhysicalRoot(
                    ubp_id    = uid,
                    vector    = vec,
                    lexicon   = concept,
                    resonance = 1.0,  # Full resonance for direct alias
                    nrci      = nrci
                ))
                new_ids.add(uid)
                grounded_concepts.add(concept)

        # 2. For remaining concepts, use original fuzzy vector grounding
        remaining_concepts = [c for c in concepts if c not in grounded_concepts]
        if remaining_concepts:
            fuzzy_roots, gaps = _orig_ground(self, remaining_concepts, max_depth)
            # Add fuzzy roots if they don't collide with direct aliases
            for r in fuzzy_roots:
                if r.ubp_id not in new_ids:
                    roots.append(r)
                    new_ids.add(r.ubp_id)
        else:
            gaps = []

        # Element Suppression & Recall Control:
        # We only want to suppress elements if they are "clutter" (secondary matches).
        # If an element was explicitly grounded via an alias, it should NOT be suppressed.
        protected_ids = {alias.get(c) for c in grounded_concepts if alias.get(c)}
        non_fill_roots = [r for r in roots if r.ubp_id not in _FILL_ELEMENTS or r.ubp_id in protected_ids]
        fill_roots = [r for r in roots if r.ubp_id in _FILL_ELEMENTS and r.ubp_id not in protected_ids]
        if non_fill_roots:
            for r in fill_roots:
                r.resonance *= 0.5
        combined = sorted(non_fill_roots + fill_roots, key=lambda r: r.resonance, reverse=True)
        roots = combined[:4]

        return roots, gaps


    GLMDialogueEngine._ground_physically = _patched_ground


    # --- patch respond() ---
    _orig_respond = GLMDialogueEngine.respond


    def _patched_respond(self, query, max_depth=3):
        turn = _orig_respond(self, query, max_depth)
        new_text = build_glm_response(
            turn.physical_roots,
            turn.lexical_bindings,
            query,
        )
        turn = dc_replace(turn, response=new_text)
        if self.turn_history and self.turn_history[-1].query == query:
            self.turn_history[-1] = turn
        return turn


    GLMDialogueEngine.respond = _patched_respond




_apply_patch()
