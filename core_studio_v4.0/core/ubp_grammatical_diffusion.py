"""
Grammatical Diffusion Reasoner (GDR) — v3.2 (Stateful A* Edition)
===============================================================
Implements a search through the zoned lattice, guided by the Grammar FSM,
using A* search with stateful attraction potentials.
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
        self.attraction_potential: Optional[List[int]] = None

    def _get_word(self, lemma: str):
        if hasattr(self.vocab, "get"): return self.vocab.get(lemma)
        return self.vocab.words.get(lemma)

    def _get_lemma(self, word: Any) -> str:
        if hasattr(word, "lemma"): return word.lemma
        if hasattr(word, "word"): return word.word
        return "?"

    def _get_dist(self, word: Any) -> int:
        if hasattr(word, "syndrome_w"): return word.syndrome_w
        if hasattr(word, "golay_distance"): return word.golay_distance
        return 0

    def reason(self, start_lemma: str, target_lemma: str, max_depth: int = 7) -> ReasonerTrace:
        start_word, target_word = self._get_word(start_lemma), self._get_word(target_lemma)
        if not start_word or not target_word: return ReasonerTrace([], False, Fraction(0), Fraction(0))
        start_fsm = GrammarFSM()
        z_start = dominant_zone(start_word.vector)
        if not start_fsm.peek(z_start) and start_word.role != "NOUN": return ReasonerTrace([], False, Fraction(0), Fraction(0))
        start_fsm.step(self._get_lemma(start_word), z_start)
        start_tax = Fraction(1) - start_word.nrci + Fraction(self._get_dist(start_word), 10)
        start_step = self._make_step(self._get_lemma(start_word), start_word, z_start, start_tax)
        open_set = []
        dist_to_target = BLA.hamming_distance(start_word.vector, target_word.vector) / 24.0
        attraction = BLA.hamming_distance(start_word.vector, self.attraction_potential) / 48.0 if self.attraction_potential and any(self.attraction_potential) else 0.0
        heapq.heappush(open_set, (float(start_tax) + dist_to_target + attraction, float(start_tax), start_lemma, start_fsm.state, [start_step]))
        visited: Set[Tuple[str, str]] = set()
        while open_set:
            f, g, lemma, state_name, path = heapq.heappop(open_set)
            if (lemma, state_name) in visited: continue
            visited.add((lemma, state_name))
            if len(path) > max_depth: continue
            current_fsm = GrammarFSM(); current_fsm.state = state_name
            if lemma == target_lemma and current_fsm.is_accepting(): return ReasonerTrace(path, True, path[-1].nrci, Fraction(sum(s.tax for s in path)))
            if hasattr(self.vocab, "adjacency") and lemma in self.vocab.adjacency:
                neighbors = [(n, self._get_word(n)) for n in self.vocab.adjacency[lemma]]
            else:
                vocab_items = list(self.vocab.words.items() if hasattr(self.vocab, "words") else self.vocab.words)
                neighbors = vocab_items[:200]
            for next_lemma, next_word in neighbors:
                z_next = dominant_zone(next_word.vector)
                if current_fsm.peek(z_next):
                    temp_fsm = GrammarFSM(); temp_fsm.state = state_name; temp_fsm.step(self._get_lemma(next_word), z_next)
                    step_tax = Fraction(1) - next_word.nrci + Fraction(self._get_dist(next_word), 10)
                    new_g = g + float(step_tax) + 1.0
                    h = (BLA.hamming_distance(next_word.vector, target_word.vector) / 24.0) + (BLA.hamming_distance(next_word.vector, self.attraction_potential) / 48.0 if self.attraction_potential and any(self.attraction_potential) else 0.0)
                    if (next_lemma, temp_fsm.state) not in visited: heapq.heappush(open_set, (new_g + h, new_g, next_lemma, temp_fsm.state, path + [self._make_step(self._get_lemma(next_word), next_word, z_next, step_tax)]))
            if current_fsm.peek("O") and len(path) < max_depth - 1 and hasattr(self.vocab, "apply_shift"):
                vocab_items = list(self.vocab.words.items() if hasattr(self.vocab, "words") else self.vocab.words)
                for op_lemma, op_word in vocab_items[:100]:
                    if op_word.role in ("OPERATOR", "VERB"):
                        for subjects in [[path[0].word, target_lemma], target_lemma]:
                            shifted = self.vocab.apply_shift(subjects, op_lemma)
                            if shifted:
                                z_op, z_sh = dominant_zone(op_word.vector), dominant_zone(shifted.vector)
                                temp_fsm = GrammarFSM(); temp_fsm.state = state_name; temp_fsm.step(self._get_lemma(op_word), z_op)
                                if temp_fsm.peek(z_sh):
                                    temp_fsm.step(self._get_lemma(shifted), z_sh)
                                    op_tax, sh_tax = Fraction(1)-op_word.nrci+Fraction(self._get_dist(op_word),10), Fraction(1)-shifted.nrci+Fraction(self._get_dist(shifted),10)
                                    new_g = g + float(op_tax) + float(sh_tax) + 2.0
                                    h = (BLA.hamming_distance(shifted.vector, target_word.vector)/24.0) + (BLA.hamming_distance(shifted.vector, self.attraction_potential)/48.0 if self.attraction_potential and any(self.attraction_potential) else 0.0)
                                    if (self._get_lemma(shifted), temp_fsm.state) not in visited: heapq.heappush(open_set, (new_g+h, new_g, self._get_lemma(shifted), temp_fsm.state, path + [self._make_step(self._get_lemma(op_word), op_word, z_op, op_tax), self._make_step(self._get_lemma(shifted), shifted, z_sh, sh_tax)]))
        return ReasonerTrace([], False, Fraction(0), Fraction(0))

    def build_sentence(self, n0: str, n1: str) -> ReasonerTrace: return self.reason(n0, n1)
    def _make_step(self, lemma: str, word: Any, zone: str, tax: Fraction) -> ReasonerStep:
        dist = self._get_dist(word)
        return ReasonerStep(lemma, word.role, word.nrci, zone, dist, ["phase-locked", "substrate-adjacent", "meaningful", "boundary", "uncorrectable"][min(dist, 4)], tax)
