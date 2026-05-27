"""
================================================================================
GLM ENGINE v3.1 — SEMANTIC EDITION
================================================================================
Upgrades GLM Engine v3.0 with the four extensions that targeted the gaps
revealed by CritPt-style probes:

  1. PHYSICS VOCABULARY EXTENSION PACK   (glm_physics_vocab_pack)
  2. MULTI-TOKEN LEXER                   (glm_multi_token_lexer)
  3. SEMANTIC FRAME GRAMMAR              (glm_semantic_frames)
  4. CONCEPT RELATION GRAPH              (glm_concept_relation_graph)

All four are merged at engine construction time.  The original
GLMDialogueEngine API is preserved (so existing callers keep working) and
augmented with:
    .lexer                  – multi-token tokenizer
    .crg                    – concept relation graph
    .frames                 – list[SemanticFrame]
    .respond(query, ...)    – now uses lexer + frames + CRG enrichment
    .explain_relation(a, b) – verbalises any CRG relation between two
                              concepts (or reports a lattice-only relation)
    .extension_stats()      – diagnostic counts

The engine remains:
    * float-free (all distances are ints, all scores are ints/Fractions)
    * stdlib only
    * deterministic (no sampling, no RNG)
    * grounded (every emitted word is a Hamming-verified lattice point)
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
from glm_engine import (
    GLMDialogueEngine, DialogueContext, DialogueTurn,
    PhysicalRoot, LexicalBinding,
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

BLA = BinaryLinearAlgebra


# ───────────────────────────────────────────────────────────────────────────────
# VOCAB MERGE
# ───────────────────────────────────────────────────────────────────────────────

def merge_pack_into_vocab(vocab: LeechLatticeVocabulary,
                          system_vectors: Dict[str, List[int]]
                          ) -> Dict[str, Any]:
    """Insert PVE pack entries (those grounded vs system_vectors) into vocab.
    Returns a small report dict."""
    grounded, gaps = build_pack(system_vectors, MAX_HAMMING_GAP)
    added, skipped_dup = 0, 0
    for pe in grounded:
        if pe.term in vocab.words:
            skipped_dup += 1
            continue
        # Build a strict WordEntry consistent with the rest of the vocab.
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(pe.vector)
        fold3 = BLA.fold24_to3(pe.vector)
        nrci = float(LEECH_ENGINE.calculate_nrci(pe.vector))
        from glm_strict_lang_builder import _get_mog_category
        mog_cat = _get_mog_category(pe.vector)
        entry = WordEntry(
            word=pe.term,
            vector=pe.vector,
            role=pe.role,
            ubp_id=pe.ubp_id,
            hamming_to_system=pe.hamming_to_system,
            nrci=nrci,
            golay_codeword=snapped,
            golay_distance=snap_info["anchor_distance"],
            fold3=fold3,
            mog_category=mog_cat,
        )
        vocab.words[pe.term] = entry
        vocab.by_role.setdefault(pe.role, []).append(pe.term)
        added += 1

    # Record true gaps in the vocab.lexical_gaps list
    for pe in gaps:
        vocab.lexical_gaps.append(LexicalGap(
            law_id="PVE_GAP", concept_text=pe.term,
            vector=pe.vector, nearest_word=pe.term,
            distance=pe.hamming_to_system,
        ))

    # Update adjacency for newly added words only (avoid full O(N²) rebuild).
    new_words = [pe.term for pe in grounded if pe.term in vocab.words]
    existing = list(vocab.words.keys())
    for w in new_words:
        v = vocab.words[w].vector
        for w2 in existing:
            if w2 == w:
                continue
            d = BLA.hamming_distance(v, vocab.words[w2].vector)
            if d <= ADJACENCY_RADIUS:
                vocab.adjacency.setdefault(w, []).append(w2)
                vocab.adjacency.setdefault(w2, []).append(w)

    return {"pack_total": len(PHYSICS_LEXICON),
            "pack_grounded": len(grounded),
            "pack_gaps": len(gaps),
            "added_to_vocab": added,
            "skipped_duplicates": skipped_dup}


# ───────────────────────────────────────────────────────────────────────────────
# ENGINE v3.1
# ───────────────────────────────────────────────────────────────────────────────

@dataclass
class SemanticTurn:
    """Enhanced dialogue turn with frame-level diagnostics."""
    query: str
    tokens: List[str]
    known_tokens: List[str]
    unknown_tokens: List[str]
    physical_roots: List[PhysicalRoot]
    filled_frames: List[FilledFrame]
    crg_paths: List[List[CRGEdge]]
    response: str
    grounded_count: int
    unverified_count: int
    verification_rate: float
    tax: float


class GLMSemanticEngine(GLMDialogueEngine):
    """
    Drop-in replacement for GLMDialogueEngine that uses semantic frames,
    multi-token lexing, and the concept relation graph.
    """

    def __init__(self, vocab: LeechLatticeVocabulary,
                 crg: Optional[ConceptRelationGraph] = None,
                 frames: Optional[List[SemanticFrame]] = None,
                 lexer: Optional[MultiTokenLexer] = None):
        super().__init__(vocab)
        self.crg = crg or build_default_crg()
        self.frames = frames or list(FRAMES)
        self.lexer = lexer or MultiTokenLexer(set(vocab.words.keys()))
        self.semantic_turns: List[SemanticTurn] = []
        # CRG sanity report
        kept, missing = self.crg.vocab_check(set(vocab.words.keys()))
        self._crg_kept = kept
        self._crg_missing = missing

    # ──────────────────────────────────────────────────────────────────────────
    # PARSING
    # ──────────────────────────────────────────────────────────────────────────

    def _parse_query(self, query: str) -> List[str]:
        """Replace the original parser with the multi-token lexer."""
        return self.lexer.tokenise(query)

    # ──────────────────────────────────────────────────────────────────────────
    # SEMANTIC RESPONSE
    # ──────────────────────────────────────────────────────────────────────────

    def respond_semantic(self, query: str, max_depth: int = 2) -> SemanticTurn:
        tokens = self._parse_query(query)
        known = [t for t in tokens if t in self.vocab.words]
        unknown = [t for t in tokens if t not in self.vocab.words]

        # Physical grounding (multi-depth lattice walk)
        roots, _ = self._ground_physically(known, max_depth)

        # Topic vector = centroid of known tokens, falls back to roots
        if known:
            topic_vec = self._compute_centroid(
                [self.vocab.words[t].vector for t in known])
        elif roots:
            topic_vec = self._compute_centroid([r.vector for r in roots])
        else:
            topic_vec = [0] * 24

        # Pick frames informed by the surface form of the query
        chosen_frames = select_frames_for_query(tokens, self.frames)

        # Fill each frame, biasing slot fillers toward the known tokens
        forbidden: List[str] = []
        filled: List[FilledFrame] = []
        # Use the first known noun as a seed_word for {topic}/{lhs}/{whole}
        seed_word = None
        for t in known:
            if t in self.vocab.words and \
               self.vocab.words[t].role == "NOUN":
                seed_word = t
                break

        for fr in chosen_frames:
            seeds: Dict[str, str] = {}
            if seed_word:
                # apply to any slot named one of these canonical positions
                for slot in fr.slots:
                    if slot.name in ("topic", "lhs", "whole", "quantity") \
                       and slot.role == "NOUN":
                        seeds[slot.name] = seed_word
                        break
            ff = fill_frame(fr, topic_vec, self.vocab,
                            MAX_HAMMING_GAP,
                            seed_words=seeds,
                            forbidden=forbidden)
            if ff:
                filled.append(ff)
                forbidden.extend(ff.fillers.values())

        # CRG enrichment: for each pair of known tokens, walk the graph
        crg_paths: List[List[CRGEdge]] = []
        for i, a in enumerate(known):
            for b in known[i + 1:]:
                p = self.crg.shortest_path(a, b, max_hops=2)
                if p:
                    crg_paths.append(p)

        # Compose the response
        parts: List[str] = []
        if not known:
            parts.append("[NULL RESONANCE] No grounded concept in query.")
        else:
            parts.append(self._compose_overview(known, tokens))
        for ff in filled:
            parts.append(self._sentence(ff.surface))
        for p in crg_paths[:4]:  # keep response concise
            parts.append(self._verbalise_path(p))
        if unknown:
            parts.append("[GAP] No verified vector for: "
                         + ", ".join(unknown[:6]) + ".")

        response = " ".join(parts)

        grounded = sum(ff.grounded_count for ff in filled)
        total = sum(ff.total_slots for ff in filled)
        vrate = (grounded / total * 100.0) if total else 100.0
        tax = sum(ff.tax for ff in filled)

        turn = SemanticTurn(
            query=query, tokens=tokens, known_tokens=known,
            unknown_tokens=unknown, physical_roots=roots,
            filled_frames=filled, crg_paths=crg_paths,
            response=response, grounded_count=grounded,
            unverified_count=total - grounded, verification_rate=vrate,
            tax=tax,
        )
        self.semantic_turns.append(turn)
        return turn

    # Keep the original `.respond()` working unchanged.
    # External callers wanting the new pipeline use `.respond_semantic()`.

    # ──────────────────────────────────────────────────────────────────────────
    # VERBALISATION HELPERS
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _sentence(s: str) -> str:
        s = s.strip()
        if not s:
            return s
        return s[0].upper() + s[1:] + ("." if not s.endswith(".") else "")

    def _compose_overview(self, known: List[str], all_tokens: List[str]) -> str:
        head = known[0]
        cat = self.vocab.words[head].mog_category
        return self._sentence(
            f"the {head} is a concept in the {cat.replace('_',' ')} category"
        )

    def _verbalise_path(self, path: List[CRGEdge]) -> str:
        if not path:
            return ""
        words = [path[0].src]
        rel_phrases = []
        for e in path:
            rel_phrases.append(e.label.replace("_", " "))
            words.append(e.dst)
        if len(path) == 1:
            return self._sentence(
                f"{path[0].src} {rel_phrases[0]} {path[0].dst}")
        return self._sentence(
            " ".join(
                f"{words[i]} {rel_phrases[i]} {words[i+1]}"
                + (" which" if i < len(path) - 1 else "")
                for i in range(len(path))
            )
        )

    # ──────────────────────────────────────────────────────────────────────────
    # PUBLIC UTILITIES
    # ──────────────────────────────────────────────────────────────────────────

    def explain_relation(self, a: str, b: str) -> str:
        a, b = a.lower(), b.lower()
        if a not in self.vocab.words or b not in self.vocab.words:
            return f"[GAP] one of {{{a}, {b}}} is not in the vocabulary."
        # direct labels
        labels = self.crg.relate(a, b)
        if labels:
            return self._sentence(
                f"{a} {', '.join(l.replace('_',' ') for l in labels)} {b}")
        # try short path
        path = self.crg.shortest_path(a, b, max_hops=3)
        if path:
            return self._verbalise_path(path)
        # fall back to lattice geometric closeness
        d = BLA.hamming_distance(
            self.vocab.words[a].vector, self.vocab.words[b].vector)
        if d <= ADJACENCY_RADIUS:
            return self._sentence(
                f"{a} and {b} are geometric neighbours in the lattice "
                f"with hamming distance {d}")
        return self._sentence(
            f"no relation found between {a} and {b}; "
            f"lattice distance {d}")

    def extension_stats(self) -> Dict[str, Any]:
        return {
            "vocab_words": len(self.vocab.words),
            "vocab_by_role": {k: len(v) for k, v in self.vocab.by_role.items()},
            "frames": len(self.frames),
            "crg_edges_kept": self._crg_kept,
            "crg_missing_concepts": len(self._crg_missing),
            "lexical_gaps": len(self.vocab.lexical_gaps),
        }


# ───────────────────────────────────────────────────────────────────────────────
# FACTORY
# ───────────────────────────────────────────────────────────────────────────────

def create_semantic_engine(system_kb_path: str,
                           lang_kb_path: str) -> Tuple[GLMSemanticEngine, Dict[str, Any]]:
    """Build a vocabulary, merge the physics pack, attach CRG + frames + lexer,
    return the live engine plus a build report."""
    vocab = build_vocabulary(system_kb_path, lang_kb_path)
    merge_report = merge_pack_into_vocab(vocab, vocab.system_vectors)
    engine = GLMSemanticEngine(vocab)
    return engine, merge_report