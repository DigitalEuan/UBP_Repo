"""
================================================================================
UBP GRAMMATICAL DIFFUSION REASONER v1.0
================================================================================
Walks the zoned Grammar Lattice (glm_zoned_lattice_embedding) from a START
concept to a TARGET concept, producing a path that is simultaneously:

    1. a TOPOLOGICAL GEODESIC      — Hamming-distance / symmetry-tax descent
    2. a GRAMMATICAL DERIVATION    — accepted by the GrammarFSM
    3. a SEMANTIC TRACE            — every hop is a typed CRG edge OR a
                                     dominant-zone transition that has a
                                     verbal interpretation (e.g. "qN→qV"
                                     reads as "subject becomes predicate")

This replaces the original `TopologicalDiffusionReasoner` (which walked the
lattice ignoring grammar) with a unified semantic / geometric / grammatical
reasoner. The original 3-block schedule (high-noise → semantic → low-noise)
is retained, but each block now applies an ADDITIONAL filter: candidate
words must put the FSM into a legal state.

──────────────────────────────────────────────────────────────────────────────
WHY THIS WORKS
──────────────────────────────────────────────────────────────────────────────
In the Grammar Lattice, each role's words form a Hamming-tight cluster
(mean intra-role distance ≈ 2-3) while cross-role distances are large
(≈ 10). So a pure geodesic step naturally stays within a role — which is
GOOD for fluency (apposition / coordination of nouns) but BAD for
sentence-formation (need to cross to a verb at some point).

The FSM forces a role transition exactly when grammar demands it. The
walker temporarily allows a "large hop" (~8 flips) when, and only when,
the FSM state machine requires moving from S → O or O → M.

──────────────────────────────────────────────────────────────────────────────
OUTPUT
──────────────────────────────────────────────────────────────────────────────
DiffusionTrace(
    success          : bool                 # FSM ended in an accepting state
    target_reached   : bool                 # final word == target
    path             : List[Step]           # the trace itself
    sentence_skeleton: str                  # human-readable concatenation
    total_tax        : Fraction             # cumulative symmetry tax
    fsm_trace        : List[FSMStep]
    nrci_final       : Fraction
)

Step(
    word     : str                          # lemma at this position
    role     : str
    zone     : str                          # dominant zone of word's vector
    fsm_from : str
    fsm_to   : str
    h_dist   : int                          # Hamming dist from previous word
    h_to_tgt : int                          # Hamming dist remaining to target
    tax      : Fraction                     # symmetry tax of this vector
    crg_rel  : Optional[str]                # CRG label (if any) from prev word
)
================================================================================
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from fractions import Fraction

from ubp_unified_v5 import (
    GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra,
)
from glm_zoned_lattice_embedding import (
    ZonedVocabulary, ZonedWord,
    GrammarFSM, dominant_zone, zone_signature,
    ROLE_HOME_ZONE,
)
from glm_concept_relation_graph import (
    ConceptRelationGraph, build_default_crg,
)

BLA = BinaryLinearAlgebra
F   = Fraction


# ════════════════════════════════════════════════════════════════════════════════
# TRACE OBJECTS
# ════════════════════════════════════════════════════════════════════════════════

@dataclass
class Step:
    word:     str
    role:     str
    zone:     str
    fsm_from: str
    fsm_to:   str
    h_dist:   int
    h_to_tgt: int
    tax:      Fraction
    crg_rel:  Optional[str] = None


@dataclass
class DiffusionTrace:
    success:           bool
    target_reached:    bool
    path:              List[Step]
    sentence_skeleton: str
    total_tax:         Fraction
    fsm_trace:         List
    nrci_final:        Fraction


# ════════════════════════════════════════════════════════════════════════════════
# REASONER
# ════════════════════════════════════════════════════════════════════════════════

class GrammaticalDiffusionReasoner:
    """Three-block reverse-diffusion reasoner that respects the GrammarFSM.

    Each block is a different "noise level" on the lattice:
      Block 3  (high noise, d ≥ 12 to target) — big role-crossing hops
      Block 2  (mid noise,  6 ≤ d < 12)       — CRG-guided semantic moves
      Block 1  (low noise,  d < 6)            — fine adjustment by tax
    """

    # ── tuning knobs ─────────────────────────────────────────────────────
    MAX_STEPS_PER_BLOCK    = 5
    INTER_ROLE_HOP_LIMIT   = 12     # max Hamming hop allowed (an octad-XOR ≈ 8)
    INTRA_ROLE_HOP_LIMIT   = 4      # max within-role hop
    CRG_BIAS               = 3      # tax bonus for typed-edge moves
    FSM_BONUS              = 5      # tax bonus for FSM-legal moves

    def __init__(self,
                 vocab: ZonedVocabulary,
                 crg: Optional[ConceptRelationGraph] = None):
        self.vocab = vocab
        self.crg = crg or build_default_crg()
        # cache the word list for fast scanning
        self._words: List[ZonedWord] = list(vocab.words.values())

    # ── tax helpers ──────────────────────────────────────────────────────
    @staticmethod
    def _hd(a: List[int], b: List[int]) -> int:
        return BLA.hamming_distance(a, b)

    def _tax(self, v: List[int]) -> Fraction:
        return LEECH_ENGINE.calculate_symmetry_tax(v)

    # ── candidate enumeration ────────────────────────────────────────────
    def _block_filter(self, block_id: int, d_from: int, d_to: int,
                      d_current: int) -> bool:
        """Block-specific Hamming-distance gate."""
        if block_id == 3:
            return d_from <= self.INTER_ROLE_HOP_LIMIT \
                   and d_to < d_current
        if block_id == 2:
            return d_from <= 8 and d_to < d_current
        if block_id == 1:
            return d_from <= self.INTRA_ROLE_HOP_LIMIT
        return False

    def _propose(self,
                 current: ZonedWord,
                 target:  ZonedWord,
                 fsm:     GrammarFSM,
                 block_id: int,
                 visited: Set[str]) -> List[Tuple[ZonedWord, int, Optional[str]]]:
        """Return [(candidate_word, score, crg_label_or_None)] sorted by
        ascending score (lower = better). Only FSM-legal moves are
        returned; if no FSM-legal move exists we relax the FSM filter
        (recorded by the caller for diagnostics)."""
        v_curr = current.vector
        v_tgt  = target.vector
        d_current = self._hd(v_curr, v_tgt)

        candidates: List[Tuple[ZonedWord, int, Optional[str], bool]] = []
        for w in self._words:
            if w.lemma == current.lemma or w.lemma in visited:
                continue
            d_from = self._hd(v_curr, w.vector)
            d_to   = self._hd(w.vector, v_tgt)
            if not self._block_filter(block_id, d_from, d_to, d_current):
                continue

            zone = dominant_zone(w.vector)
            fsm_legal = fsm.peek(zone)
            crg_label = None
            crg_rels = self.crg.relate(current.lemma, w.lemma)
            if crg_rels:
                crg_label = crg_rels[0]

            # Base score: prefer closer to target
            score = d_to
            if crg_label:
                score -= self.CRG_BIAS
            if fsm_legal:
                score -= self.FSM_BONUS
            # Tax penalty (small, breaks ties geometrically)
            tax = self._tax(w.vector)
            score += int(tax * 2)  # int casting keeps the search float-free

            candidates.append((w, score, crg_label, fsm_legal))

        candidates.sort(key=lambda x: x[1])
        # Keep only FSM-legal ones if any exist; else relax
        legal = [c for c in candidates if c[3]]
        if legal:
            return [(c[0], c[1], c[2]) for c in legal]
        return [(c[0], c[1], c[2]) for c in candidates]

    # ── main runner ──────────────────────────────────────────────────────
    def reason(self, start_lemma: str, target_lemma: str
               ) -> DiffusionTrace:
        if start_lemma not in self.vocab.words or \
           target_lemma not in self.vocab.words:
            raise ValueError(f"missing vocabulary: {start_lemma!r} or {target_lemma!r}")

        start = self.vocab.words[start_lemma]
        target = self.vocab.words[target_lemma]

        fsm = GrammarFSM()
        # seed FSM with the start word's zone
        first_zone = dominant_zone(start.vector)
        first_step = fsm.step(start.lemma, first_zone)

        path: List[Step] = [Step(
            word=start.lemma, role=start.role, zone=first_zone,
            fsm_from=first_step.from_st, fsm_to=first_step.to_st,
            h_dist=0,
            h_to_tgt=self._hd(start.vector, target.vector),
            tax=self._tax(start.vector),
            crg_rel=None,
        )]

        current = start
        visited = {start.lemma}
        total_tax = path[0].tax

        for block_id in (3, 2, 1):
            for _ in range(self.MAX_STEPS_PER_BLOCK):
                if current.lemma == target.lemma:
                    break
                cands = self._propose(current, target, fsm, block_id, visited)
                if not cands:
                    break
                nxt, score, crg_label = cands[0]
                zone = dominant_zone(nxt.vector)
                fsm_step = fsm.step(nxt.lemma, zone)
                d_from = self._hd(current.vector, nxt.vector)
                d_to   = self._hd(nxt.vector, target.vector)
                tax    = self._tax(nxt.vector)
                path.append(Step(
                    word=nxt.lemma, role=nxt.role, zone=zone,
                    fsm_from=fsm_step.from_st, fsm_to=fsm_step.to_st,
                    h_dist=d_from, h_to_tgt=d_to, tax=tax,
                    crg_rel=crg_label,
                ))
                total_tax += tax
                visited.add(nxt.lemma)
                current = nxt
                if current.lemma == target.lemma:
                    break
            if current.lemma == target.lemma:
                break

        # If we never reached target, attempt one direct hop within the
        # final block (block 1, low noise) regardless of FSM legality.
        if current.lemma != target.lemma:
            d_final = self._hd(current.vector, target.vector)
            if d_final <= 8:                      # Golay correction radius
                zone = dominant_zone(target.vector)
                fsm_step = fsm.step(target.lemma, zone)
                path.append(Step(
                    word=target.lemma, role=target.role, zone=zone,
                    fsm_from=fsm_step.from_st, fsm_to=fsm_step.to_st,
                    h_dist=d_final, h_to_tgt=0,
                    tax=self._tax(target.vector),
                    crg_rel=None,
                ))
                total_tax += self._tax(target.vector)
                current = target

        sentence = " · ".join(s.word for s in path)
        nrci = LEECH_ENGINE.calculate_nrci(current.vector)
        return DiffusionTrace(
            success=fsm.is_accepting(),
            target_reached=(current.lemma == target.lemma),
            path=path,
            sentence_skeleton=sentence,
            total_tax=total_tax,
            fsm_trace=list(fsm.trace),
            nrci_final=nrci,
        )

    # ── sentence construction (multi-hop forced) ──────────────────────
    def build_sentence(self, subject: str, object_: str) -> DiffusionTrace:
        """Force a 3-hop NOUN -> VERB(/OPERATOR) -> NOUN sentence. Even when
        subject and object are Hamming-close, the FSM is required to pass
        through state qV (a verb/operator) before reaching the object."""
        if subject not in self.vocab.words or object_ not in self.vocab.words:
            raise ValueError("missing vocabulary entries")
        start = self.vocab.words[subject]
        target = self.vocab.words[object_]

        fsm = GrammarFSM()
        first_zone = dominant_zone(start.vector)
        first_step = fsm.step(start.lemma, first_zone)

        path: List[Step] = [Step(
            word=start.lemma, role=start.role, zone=first_zone,
            fsm_from=first_step.from_st, fsm_to=first_step.to_st,
            h_dist=0,
            h_to_tgt=self._hd(start.vector, target.vector),
            tax=self._tax(start.vector),
            crg_rel=None,
        )]
        visited = {start.lemma}
        total_tax = path[0].tax
        current = start

        # Step 1: force a transition into Operator zone
        verb_step = self._pick_zone(current, target, fsm, "O", visited)
        if verb_step is None:
            return self.reason(subject, object_)
        path.append(verb_step)
        visited.add(verb_step.word)
        total_tax += verb_step.tax
        current = self.vocab.words[verb_step.word]

        # Step 2: hop into the target
        final_zone = dominant_zone(target.vector)
        d_final = self._hd(current.vector, target.vector)
        fsm_step = fsm.step(target.lemma, final_zone)
        crg_rels = self.crg.relate(current.lemma, target.lemma)
        path.append(Step(
            word=target.lemma, role=target.role, zone=final_zone,
            fsm_from=fsm_step.from_st, fsm_to=fsm_step.to_st,
            h_dist=d_final, h_to_tgt=0,
            tax=self._tax(target.vector),
            crg_rel=crg_rels[0] if crg_rels else None,
        ))
        total_tax += self._tax(target.vector)

        sentence = " · ".join(s.word for s in path)
        return DiffusionTrace(
            success=fsm.is_accepting(),
            target_reached=True,
            path=path,
            sentence_skeleton=sentence,
            total_tax=total_tax,
            fsm_trace=list(fsm.trace),
            nrci_final=LEECH_ENGINE.calculate_nrci(target.vector),
        )

    def _pick_zone(self, current: ZonedWord, target: ZonedWord,
                   fsm: GrammarFSM, target_zone: str,
                   visited: Set[str]) -> Optional[Step]:
        """Pick the best candidate whose dominant zone == target_zone AND the
        FSM accepts that zone from its current state. Returns None if no
        such candidate exists."""
        if not fsm.peek(target_zone):
            return None
        best: Optional[Tuple[ZonedWord, int, Optional[str]]] = None
        for w in self._words:
            if w.lemma in visited or w.lemma == current.lemma:
                continue
            if dominant_zone(w.vector) != target_zone:
                continue
            d_from = self._hd(current.vector, w.vector)
            if d_from > self.INTER_ROLE_HOP_LIMIT:
                continue
            d_to = self._hd(w.vector, target.vector)
            crg_rels = self.crg.relate(current.lemma, w.lemma)
            crg_label = crg_rels[0] if crg_rels else None
            score = d_to - (self.CRG_BIAS if crg_label else 0)
            score += int(self._tax(w.vector) * 2)
            if best is None or score < best[1]:
                best = (w, score, crg_label)
        if best is None:
            return None
        w, score, crg_label = best
        zone = dominant_zone(w.vector)
        fsm_step = fsm.step(w.lemma, zone)
        return Step(
            word=w.lemma, role=w.role, zone=zone,
            fsm_from=fsm_step.from_st, fsm_to=fsm_step.to_st,
            h_dist=self._hd(current.vector, w.vector),
            h_to_tgt=self._hd(w.vector, target.vector),
            tax=self._tax(w.vector),
            crg_rel=crg_label,
        )

    # ── pretty printer ──────────────────────────────────────────────────
    def render(self, trace: DiffusionTrace) -> str:
        out: List[str] = []
        out.append("─" * 78)
        out.append(f" PATH: {trace.sentence_skeleton}")
        out.append(f" target_reached={trace.target_reached}  "
                   f"grammatical={trace.success}  "
                   f"total_tax={float(trace.total_tax):.2f}  "
                   f"final_NRCI={float(trace.nrci_final):.4f}")
        out.append("─" * 78)
        out.append(f" {'i':>2} {'word':14s} {'role':10s} {'zone':4s} "
                   f"{'fsm':18s} {'Δh':>4s} {'h→tgt':>5s} {'tax':>6s} "
                   f"{'CRG':>16s}")
        for i, s in enumerate(trace.path):
            fsm_arrow = f"{s.fsm_from}→{s.fsm_to}"
            out.append(f" {i:>2} {s.word:14s} {s.role:10s} {s.zone:4s} "
                       f"{fsm_arrow:18s} {s.h_dist:>4d} {s.h_to_tgt:>5d} "
                       f"{float(s.tax):>6.2f} {(s.crg_rel or '-'):>16s}")
        return "\n".join(out)


# ════════════════════════════════════════════════════════════════════════════════
# DEMO
# ════════════════════════════════════════════════════════════════════════════════

def _demo():
    print("─" * 78)
    print(" UBP GRAMMATICAL DIFFUSION REASONER — Demo")
    print("─" * 78)
    vocab = ZonedVocabulary()
    # Build a small physics vocabulary that includes all roles
    additions = [
        # NOUNs (Subject zone)
        ("electron",   "NOUN",      "M_Mass"),
        ("photon",     "NOUN",      "A_Energy"),
        ("hamiltonian","NOUN",      "A_Energy"),
        ("symmetry",   "NOUN",      "I_Symmetry"),
        ("momentum",   "NOUN",      "A_Velocity"),
        ("metric",     "NOUN",      "M_Space"),
        ("operator",   "NOUN",      "I_Connectivity"),
        ("anomaly",    "NOUN",      "I_Topology"),
        ("majorana",   "NOUN",      "M_Mass"),
        ("fermion",    "NOUN",      "M_Mass"),
        ("particle",   "NOUN",      "M_Mass"),
        # VERBs (Operator zone)
        ("commutes",   "VERB",      "I_Symmetry"),
        ("scales",     "VERB",      "P_Ratio"),
        ("generates",  "VERB",      "A_Energy"),
        ("measures",   "VERB",      "P_Tax"),
        ("depends",    "VERB",      "I_Connectivity"),
        # OPERATORs (Operator zone)
        ("between",    "OPERATOR",  "I_Connectivity"),
        ("with",       "OPERATOR",  "I_Connectivity"),
        # ADJ/PROP (Modifier zone)
        ("massless",   "ADJECTIVE", "M_Mass"),
        ("topological","ADJECTIVE", "I_Topology"),
        ("quantum",    "ADJECTIVE", "P_Phase"),
        ("strong",     "PROPERTY",  "A_Force"),
        ("weak",       "PROPERTY",  "A_Force"),
    ]
    for a in additions:
        vocab.add(*a)
    reasoner = GrammaticalDiffusionReasoner(vocab)

    # Run a few path queries
    queries = [
        ("electron", "photon"),
        ("majorana", "fermion"),
        ("hamiltonian", "symmetry"),
        ("electron", "topological"),
        ("symmetry", "anomaly"),
    ]
    print("\n## MODE 1: bare geodesic (no forced sentence structure) ##")
    for start, tgt in queries:
        print()
        trace = reasoner.reason(start, tgt)
        print(reasoner.render(trace))

    print("\n## MODE 2: forced NOUN – VERB – NOUN sentence construction ##")
    sentence_queries = [
        ("hamiltonian", "symmetry"),
        ("majorana",    "fermion"),
        ("electron",    "photon"),
        ("momentum",    "metric"),
        ("anomaly",     "metric"),
    ]
    for start, tgt in sentence_queries:
        print()
        trace = reasoner.build_sentence(start, tgt)
        print(reasoner.render(trace))


if __name__ == "__main__":
    _demo()
