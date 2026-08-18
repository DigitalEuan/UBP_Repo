"""
GLM Grammar FSM v1.0
====================
Deterministic automaton for dominant-zone sequences and GDR integration.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional, Set, Any
from fractions import Fraction
from glm_zoned_lattice_embedding import ZonedVocabulary, dominant_zone

_FSM_TRANSITIONS: Dict[str, Dict[str, str]] = {
    "start":   {"S": "qN"},
    "qN":      {"S": "qN", "M": "qN_mod", "O": "qV"},
    "qN_mod":  {"S": "qN", "M": "qN_mod", "O": "qV"},
    "qV":      {"S": "qN", "M": "qV_mod", "O": "qV"},
    "qV_mod":  {"S": "qN", "O": "qV"},
}
_ACCEPTING: Set[str] = {"qN", "qN_mod"}


@dataclass
class FSMStep:
    word:    str
    zone:    str
    from_st: str
    to_st:   str
    legal:   bool


class GrammarFSM:
    """Driver for the dominant-zone automaton."""

    def __init__(self):
        self.state = "start"
        self.trace: List[FSMStep] = []

    def reset(self):
        self.state = "start"
        self.trace.clear()

    def step(self, word: str, zone: str) -> FSMStep:
        legal_targets = _FSM_TRANSITIONS.get(self.state, {})
        if zone in legal_targets:
            new = legal_targets[zone]
            s = FSMStep(word, zone, self.state, new, True)
            self.state = new
        else:
            s = FSMStep(word, zone, self.state, self.state, False)
        self.trace.append(s)
        return s

    def peek(self, zone: str) -> bool:
        """Would `zone` be a legal next step? Does not mutate state."""
        return zone in _FSM_TRANSITIONS.get(self.state, {})

    def is_accepting(self) -> bool:
        return self.state in _ACCEPTING


class GDRWithFSM:
    def __init__(self, vocab: ZonedVocabulary):
        self.vocab  = vocab
        self.fsm    = GrammarFSM()

    def score_candidate(self, candidate_lemma: str,
                        current_anchors: list) -> dict:
        """
        Returns {"legal": bool, "nrci": Fraction, "zone": str}.
        Legal = FSM would accept this word as next token.
        """
        word = self.vocab.get(candidate_lemma)
        if word is None:
            return {
                "legal": False,
                "nrci": Fraction(0),
                "zone": "?",
                "displacement": 4,
                "confidence": "uncorrectable"
            }
        z = dominant_zone(word.vector)
        legal = self.fsm.peek(z)   # non-destructive check

        return {
            "legal":        legal,
            "nrci":         word.nrci,
            "zone":         z,
            "displacement": word.syndrome_w,          # Golay perturbation
            "confidence":  ["phase-locked", "substrate-adjacent",
                            "meaningful", "boundary", "uncorrectable"
                           ][min(word.syndrome_w, 4)]
        }

    def advance(self, chosen_lemma: str):
        """Call after committing to a candidate. Advances FSM state."""
        word = self.vocab.get(chosen_lemma)
        if word:
            z = dominant_zone(word.vector)
            self.fsm.step(chosen_lemma, z)

if __name__ == "__main__":
    from glm_lang_database import LANG_DB
    gdr = GDRWithFSM(LANG_DB)
    print("Testing FSM candidate scoring:")
    for lemma in ["zero", "is", "one"]:
        res = gdr.score_candidate(lemma, [])
        print(f"  {lemma:10s} legal={res['legal']} zone={res['zone']} "
              f"conf={res['confidence']}")
        if res['legal']:
            gdr.advance(lemma)
            print(f"  (Advanced to state: {gdr.fsm.state})")
