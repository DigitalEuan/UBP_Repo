"""
Grammatical Diffusion Reasoner (GDR) — v2.1 (A* Edition)
========================================================
Implements a search through the zoned lattice, guided by the Grammar FSM,
using A* search to find valid grammatical paths between concepts.
"""
from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Set
from fractions import Fraction
from glm_grammar_fsm import GrammarFSM
from glm_zoned_lattice_embedding import dominant_zone
from ubp_unified_v5 import BinaryLinearAlgebra as BLA

@dataclass(frozen=True, order=True)
class ReasonerStep:
    word: str
    role: str
    nrci: Fraction
    zone: str
    displacement: int
    confidence: str
    tax: Fraction = Fraction(0)

@dataclass
class ReasonerTrace:
    path: List[ReasonerStep]
    target_reached: bool
    nrci_final: Fraction
    total_tax: Fraction

class GrammaticalDiffusionReasoner:
    def __init__(self, vocab, crg=None):
        self.vocab = vocab
        self.crg = crg
        # We'll create FSM instances as needed to avoid state pollution

    def reason(self, start_lemma: str, target_lemma: str, max_depth: int = 7) -> ReasonerTrace:
        start_word = self.vocab.get(start_lemma)
        target_word = self.vocab.get(target_lemma)

        if not start_word or not target_word:
            return ReasonerTrace([], False, Fraction(0), Fraction(0))

        # A* Search
        # State: (lemma, fsm_state)
        # Priority Queue: (f_score, g_score, lemma, fsm_state, path_indices)

        start_fsm = GrammarFSM()
        z_start = dominant_zone(start_word.vector)
        if not start_fsm.peek(z_start):
            if start_word.role != "NOUN":
                return ReasonerTrace([], False, Fraction(0), Fraction(0))

        start_fsm.step(start_lemma, z_start)

        # Initial tax is the starting word's NRCI penalty + displacement
        start_tax = Fraction(1) - start_word.nrci + Fraction(start_word.syndrome_w, 10)
        start_step = self._make_step(start_lemma, start_word, z_start, start_tax)

        # (f_score, g_score, current_lemma, fsm_state_name, path)
        open_set = []
        start_g = float(start_tax)
        start_h = BLA.hamming_distance(start_word.vector, target_word.vector) / 24.0
        heapq.heappush(open_set, (start_g + start_h, start_g, start_lemma, start_fsm.state, [start_step]))

        visited: Set[Tuple[str, str]] = set()

        while open_set:
            f, g, lemma, state_name, path = heapq.heappop(open_set)

            if (lemma, state_name) in visited:
                continue
            visited.add((lemma, state_name))

            if len(path) > max_depth:
                continue

            current_fsm = GrammarFSM()
            current_fsm.state = state_name
            if lemma == target_lemma and current_fsm.is_accepting():
                return ReasonerTrace(
                    path, True,
                    path[-1].nrci,
                    Fraction(sum(s.tax for s in path))
                )

            # Explore neighbors
            for next_lemma, next_word in self.vocab.words.items():
                z_next = dominant_zone(next_word.vector)

                if current_fsm.peek(z_next):
                    temp_fsm = GrammarFSM()
                    temp_fsm.state = state_name
                    temp_fsm.step(next_lemma, z_next)

                    # Cost: step penalty + NRCI penalty + displacement penalty
                    step_tax = Fraction(1) - next_word.nrci + Fraction(next_word.syndrome_w, 10)
                    next_step = self._make_step(next_lemma, next_word, z_next, step_tax)

                    new_path = path + [next_step]
                    new_g = g + float(step_tax) + 1.0 # 1.0 is the base step cost
                    new_h = BLA.hamming_distance(next_word.vector, target_word.vector) / 24.0

                    if (next_lemma, temp_fsm.state) not in visited:
                        heapq.heappush(open_set, (new_g + new_h, new_g, next_lemma, temp_fsm.state, new_path))

        return ReasonerTrace([], False, Fraction(0), Fraction(0))

    def build_sentence(self, n0: str, n1: str) -> ReasonerTrace:
        return self.reason(n0, n1)

    def _make_step(self, lemma: str, word: Any, zone: str, tax: Fraction) -> ReasonerStep:
        return ReasonerStep(
            word=lemma,
            role=word.role,
            nrci=word.nrci,
            zone=zone,
            displacement=word.syndrome_w,
            confidence=["phase-locked", "substrate-adjacent", "meaningful", "boundary", "uncorrectable"][min(word.syndrome_w, 4)],
            tax=tax
        )

if __name__ == "__main__":
    from glm_lang_database import LANG_DB
    gdr = GrammaticalDiffusionReasoner(LANG_DB)
    print("Testing A* Grammatical Diffusion (zero -> one):")
    trace = gdr.reason("zero", "one")
    print(f"  Target reached: {trace.target_reached}")
    if trace.path:
        print(f"  Path: {' -> '.join(s.word for s in trace.path)}")
        for s in trace.path:
            print(f"    {s.word:10s} zone={s.zone} disp={s.displacement} conf={s.confidence} tax={float(s.tax):.4f}")
        print(f"  Total Tax: {float(trace.total_tax):.4f}")
