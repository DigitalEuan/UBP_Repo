"""
================================================================================
GLM ENGINE v3.1 — SEMANTIC EDITION (Stewardship v3.2)
================================================================================
Upgrades GLM Engine v3.0 with the four extensions that targeted the gaps
revealed by CritPt-style probes:

  1. PHYSICS VOCABULARY EXTENSION PACK   (glm_physics_vocab_pack)
  2. MULTI-TOKEN LEXER                   (glm_multi_token_lexer)
  3. SEMANTIC FRAME GRAMMAR              (glm_semantic_frames)
  4. CONCEPT RELATION GRAPH              (glm_concept_relation_graph)

v3.2 Improvements:
- Stateful Manifold Memory: Contextual centroid tracking.
- Ontological Health Feedback: Automatic query self-correction.
- GDR v3.3 Integration: Recursive A* reasoning.
================================================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Set
from fractions import Fraction

from ubp_unified_v5 import (
    BinaryLinearAlgebra, GOLAY_ENGINE, LEECH_ENGINE, MOG_CATEGORIES,
)
from glm_strict_lang_builder import (
    LeechLatticeVocabulary, WordEntry, GrammarRule, LearnedPath,
    LexicalGap, MAX_HAMMING_GAP, ADJACENCY_RADIUS, SENTENCE_MAX_TAX,
    build_vocabulary,
)
from glm_physics_vocab_pack import (
    PHYSICS_LEXICON, build_pack, PackEntry, derive_term_vector,
    get_pack_summary,
)
from glm_multi_token_lexer import MultiTokenLexer
from glm_semantic_frames import (
    SemanticFrame, FrameSlot, FilledFrame, FRAMES,
    fill_frame, select_frames_for_query,
)
from glm_concept_relation_graph import (
    ConceptRelationGraph, CRGEdge, build_default_crg,
)
from glm_lang_database import LANG_DB
from glm_zoned_lattice_embedding import ZonedVocabulary
from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner

BLA = BinaryLinearAlgebra

@dataclass
class PhysicalRoot:
    ubp_id: str
    vector: List[int]
    lexicon: str
    resonance: float
    nrci: float

@dataclass
class LexicalBinding:
    word: str
    is_grounded: bool
    role: str

@dataclass
class DialogueTurn:
    query: str
    response: str
    physical_roots: List[PhysicalRoot]
    lexical_bindings: List[LexicalBinding]

@dataclass
class DialogueContext:
    turns: List[DialogueTurn]
    context_centroid: List[int] = field(default_factory=lambda: [0]*24)

class GLMDialogueEngine:
    def __init__(self, vocab: LeechLatticeVocabulary):
        self.vocab = vocab
        self.turn_history: List[DialogueTurn] = []

    def _ground_physically(self, concepts: List[str], max_depth: int) -> Tuple[List[PhysicalRoot], List[str]]:
        return [], []

    def _compute_centroid(self, vectors: List[List[int]]) -> List[int]:
        if not vectors: return [0]*24
        res = [0]*24
        for v in vectors:
            for i in range(24): res[i] += v[i]
        return [1 if x > len(vectors)//2 else 0 for x in res]

    def respond(self, query: str, max_depth: int = 3) -> DialogueTurn:
        return DialogueTurn(query, "", [], [])


def merge_pack_into_vocab(vocab: LeechLatticeVocabulary,
                          system_vectors: Dict[str, List[int]]
                          ) -> Dict[str, Any]:
    grounded, gaps = build_pack(system_vectors, MAX_HAMMING_GAP)
    added, skipped_dup = 0, 0
    for pe in grounded:
        if pe.term in vocab.words:
            skipped_dup += 1
            continue
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(pe.vector)
        fold3 = BLA.fold24_to3(pe.vector)
        nrci = float(LEECH_ENGINE.calculate_nrci(pe.vector))
        from glm_strict_lang_builder import _get_mog_category
        mog_cat = _get_mog_category(pe.vector)
        entry = WordEntry(pe.term, pe.vector, pe.role, pe.ubp_id, pe.hamming_to_system, nrci, snapped, snap_info["anchor_distance"], fold3, mog_cat)
        vocab.words[pe.term] = entry
        vocab.by_role.setdefault(pe.role, []).append(pe.term)
        added += 1
    for pe in gaps:
        vocab.lexical_gaps.append(LexicalGap("PVE_GAP", pe.term, pe.vector, pe.term, pe.hamming_to_system))
    new_words = [pe.term for pe in grounded if pe.term in vocab.words]
    existing = list(vocab.words.keys())
    for w in new_words:
        v = vocab.words[w].vector
        for w2 in existing:
            if w2 == w: continue
            d = BLA.hamming_distance(v, vocab.words[w2].vector)
            if d <= ADJACENCY_RADIUS:
                vocab.adjacency.setdefault(w, []).append(w2)
                vocab.adjacency.setdefault(w2, []).append(w)
    return {"pack_total": len(PHYSICS_LEXICON), "pack_grounded": len(grounded), "added_to_vocab": added, "skipped_duplicates": skipped_dup}


class GLMSemanticEngine(GLMDialogueEngine):
    def __init__(self, vocab: LeechLatticeVocabulary,
                 crg: Optional[ConceptRelationGraph] = None,
                 frames: Optional[List[SemanticFrame]] = None,
                 lexer: Optional[MultiTokenLexer] = None):
        super().__init__(vocab)
        self.crg = crg or build_default_crg()
        self.frames = frames or list(FRAMES)
        self.lexer = lexer or MultiTokenLexer(set(vocab.words.keys()))
        self.semantic_turns: List[SemanticTurn] = []
        self.context = DialogueContext(turns=[])
        kept, missing = self.crg.vocab_check(set(vocab.words.keys()))
        self._crg_kept, self._crg_missing = kept, missing

    def _parse_query(self, query: str) -> List[str]:
        ctx_vec = self.context.context_centroid if hasattr(self, "context") else None
        return self.lexer.tokenise(query, context_centroid=ctx_vec)

    def respond_semantic(self, query: str, max_depth: int = 2) -> SemanticTurn:
        tokens = self._parse_query(query)
        known = [t for t in tokens if t in self.vocab.words]
        unknown = [t for t in tokens if t not in self.vocab.words]
        roots, _ = self._ground_physically(known, max_depth)

        # Health Feedback (v3.2)
        health_feedback = []
        for t in list(known):
            w = self.vocab.words[t]
            if w.nrci < 0.7:
                 best_neighbor, best_nrci = None, 0.0
                 if t in self.vocab.adjacency:
                     for neighbor in self.vocab.adjacency[t]:
                         nw = self.vocab.words[neighbor]
                         if nw.nrci > best_nrci: best_nrci, best_neighbor = nw.nrci, neighbor
                 if best_neighbor and best_nrci > w.nrci + 0.1:
                     health_feedback.append(f"[Correction] Concept '{t}' (NRCI {w.nrci:.2f}) is unstable; using '{best_neighbor}' (NRCI {best_nrci:.2f}) as stable anchor.")
                     known = [best_neighbor if x == t else x for x in known]

        topic_vec = self._compute_centroid([self.vocab.words[t].vector for t in known]) if known else self._compute_centroid([r.vector for r in roots]) if roots else [0]*24
        from glm_grammar_patch import synthesize_path, _query_type
        qtype = _query_type(query)
        reasoner = GrammaticalDiffusionReasoner(self.vocab, self.crg)
        reasoner.attraction_potential = self.context.context_centroid
        gdr_sentences = []
        if len(known) >= 2:
            for i in range(len(known) - 1):
                try:
                    trace = reasoner.reason(known[i], known[i+1])
                    if trace.target_reached: gdr_sentences.append(synthesize_path(trace.path, qtype, self.crg))
                except Exception: continue

        chosen_frames = select_frames_for_query(tokens, self.frames)
        forbidden, filled = [], []
        seed_word = next((t for t in known if self.vocab.words[t].role == "NOUN"), None)
        for fr in chosen_frames:
            seeds = {s.name: seed_word for s in fr.slots if s.name in ("topic", "lhs", "whole", "quantity") and s.role == "NOUN"} if seed_word else {}
            ff = fill_frame(fr, topic_vec, self.vocab, MAX_HAMMING_GAP, seed_words=seeds, forbidden=forbidden)
            if ff:
                filled.append(ff)
                forbidden.extend(ff.fillers.values())
        crg_paths = []
        for i, a in enumerate(known):
            for b in known[i + 1:]:
                p = self.crg.shortest_path(a, b, max_hops=2)
                if p: crg_paths.append(p)

        parts = [self._compose_overview(known, tokens)] if known else ["[NULL RESONANCE] No grounded concept in query."]
        for ff in filled: parts.append(self._sentence(ff.surface))
        for p in crg_paths[:4]: parts.append(self._verbalise_path(p))
        if unknown: parts.append("[GAP] No verified vector for: " + ", ".join(unknown[:6]) + ".")
        response = " ".join(health_feedback + gdr_sentences + parts)
        if known:
            current_centroid = self._compute_centroid([self.vocab.words[t].vector for t in known])
            self.context.context_centroid = current_centroid
        grounded = sum(ff.grounded_count for ff in filled)
        total = sum(ff.total_slots for ff in filled)
        turn = SemanticTurn(query, tokens, known, unknown, roots, filled, crg_paths, response, grounded, total-grounded, (grounded/total*100.0) if total else 100.0, sum(ff.tax for ff in filled))
        self.semantic_turns.append(turn)
        return turn

    @staticmethod
    def _sentence(s: str) -> str:
        s = s.strip()
        return s[0].upper() + s[1:] + ("." if not s.endswith(".") else "") if s else s
    def _compose_overview(self, known: List[str], all_tokens: List[str]) -> str:
        head = known[0]; cat = self.vocab.words[head].mog_category
        return self._sentence(f"the {head} is a concept in the {cat.replace('_',' ')} category")
    def _verbalise_path(self, path: List[CRGEdge]) -> str:
        if not path: return ""
        words, rels = [path[0].src], [e.label.replace("_", " ") for e in path]
        for e in path: words.append(e.dst)
        if len(path) == 1: return self._sentence(f"{path[0].src} {rels[0]} {path[0].dst}")
        return self._sentence(" ".join(f"{words[i]} {rels[i]} {words[i+1]}" + (" which" if i < len(path)-1 else "") for i in range(len(path))))
    def explain_relation(self, a: str, b: str) -> str:
        a, b = a.lower(), b.lower()
        if a not in self.vocab.words or b not in self.vocab.words: return f"[GAP] one of {{{a}, {b}}} is not in the vocabulary."
        labels = self.crg.relate(a, b)
        if labels: return self._sentence(f"{a} {', '.join(l.replace('_',' ') for l in labels)} {b}")
        path = self.crg.shortest_path(a, b, max_hops=3)
        if path: return self._verbalise_path(path)
        d = BLA.hamming_distance(self.vocab.words[a].vector, self.vocab.words[b].vector)
        if d <= ADJACENCY_RADIUS: return self._sentence(f"{a} and {b} are geometric neighbours in the lattice with hamming distance {d}")
        return self._sentence(f"no relation found between {a} and {b}; lattice distance {d}")
    def extension_stats(self) -> Dict[str, Any]:
        return {"vocab_words": len(self.vocab.words), "vocab_by_role": {k: len(v) for k, v in self.vocab.by_role.items()}, "frames": len(self.frames), "crg_edges_kept": self._crg_kept, "crg_missing_concepts": len(self._crg_missing), "lexical_gaps": len(self.vocab.lexical_gaps)}

def merge_zoned_vocab(vocab: LeechLatticeVocabulary, zoned_db: ZonedVocabulary) -> Dict[str, Any]:
    added, updated = 0, 0
    for lemma, zw in zoned_db.words.items():
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(zw.vector)
        fold3 = BLA.fold24_to3(zw.vector)
        entry = WordEntry(lemma, zw.vector, zw.role, f"GDB_{lemma}", 0, float(zw.nrci), snapped, zw.syndrome_w, fold3, zw.mog_category)
        if lemma in vocab.words:
            old_role = vocab.words[lemma].role
            if old_role in vocab.by_role and lemma in vocab.by_role[old_role]: vocab.by_role[old_role].remove(lemma)
            updated += 1
        else: added += 1
        vocab.words[lemma] = entry
        vocab.by_role.setdefault(zw.role, []).append(lemma)
    return {"zoned_added": added, "zoned_updated": updated}

def create_semantic_engine(system_kb_path: str,
                           lang_kb_path: str) -> Tuple[GLMSemanticEngine, Dict[str, Any]]:
    vocab = build_vocabulary(system_kb_path, lang_kb_path)
    zoned_report = merge_zoned_vocab(vocab, LANG_DB)
    merge_report = merge_pack_into_vocab(vocab, vocab.system_vectors)
    engine = GLMSemanticEngine(vocab)
    full_report = merge_report.copy()
    full_report.update(zoned_report)
    return engine, full_report
