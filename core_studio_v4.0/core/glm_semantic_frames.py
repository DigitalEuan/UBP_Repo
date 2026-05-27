"""
================================================================================
GLM SEMANTIC FRAME GRAMMAR v1.0
================================================================================
Replaces the original linear ['NOUN', 'VERB', 'NOUN'] grammar rules with
parameterised TYPED FRAMES.  Each frame is a small template with named
slots, an explicit role-type per slot, and a fluent surface form.

A frame is filled deterministically:
  * Slots are filled in order.
  * Each slot's filler is the lattice-nearest word to a SLOT_VECTOR derived
    from the topic vector and the previous fillers (so consecutive slots
    have low symmetry tax).
  * If a slot is given a `seed_word`, that word is used verbatim provided it
    exists in the vocabulary.

The grammar is rich enough to express the semantic patterns CritPt actually
asks for:
  * DEFINITION:        "<topic> is a <category> that <verb>s the <object>."
  * RELATION:          "<lhs> scales as <rhs>^<exponent>."
  * COMPOSITION:       "<whole> is the <relation> of <part1> and <part2>."
  * EQUATION:          "the <quantity> equals the <operator> of <argument>."
  * CONSTRAINT:        "<lhs> commutes with <rhs>."
  * DUALITY:           "<lhs> is dual to <rhs>."

All slot fillers are still grounded in the Leech lattice — frames never
fabricate words, they only choose them.
================================================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable

from ubp_unified_v5 import BinaryLinearAlgebra
BLA = BinaryLinearAlgebra


@dataclass
class FrameSlot:
    name: str
    role: str                  # NOUN / VERB / ADJECTIVE / OPERATOR / PROPERTY / ANY
    seed_word: Optional[str] = None       # if set, prefer this word verbatim
    require_grounded: bool = True


@dataclass
class SemanticFrame:
    name: str
    template: str              # Python format string with slot names
    slots: List[FrameSlot]
    max_tax: float = 40.0

    def required_roles(self) -> List[str]:
        return [s.role for s in self.slots]


# ───────────────────────────────────────────────────────────────────────────────
# CANONICAL FRAME LIBRARY
# ───────────────────────────────────────────────────────────────────────────────

FRAMES: List[SemanticFrame] = [
    # ── definitions ───────────────────────────────────────────────────────────
    SemanticFrame(
        name="definition_isa",
        template="the {topic} is a {kind} that {verb}s the {object}",
        slots=[FrameSlot("topic", "NOUN"),
               FrameSlot("kind", "NOUN"),
               FrameSlot("verb", "VERB"),
               FrameSlot("object", "NOUN")],
    ),
    SemanticFrame(
        name="definition_property",
        template="the {topic} has the property of being {property}",
        slots=[FrameSlot("topic", "NOUN"),
               FrameSlot("property", "ADJECTIVE")],
    ),
    # ── relations ─────────────────────────────────────────────────────────────
    SemanticFrame(
        name="scales_as",
        template="{lhs} scales as {rhs} to a power",
        slots=[FrameSlot("lhs", "NOUN"),
               FrameSlot("rhs", "NOUN")],
    ),
    SemanticFrame(
        name="depends_on",
        template="{lhs} depends on {rhs}",
        slots=[FrameSlot("lhs", "NOUN"),
               FrameSlot("rhs", "NOUN")],
    ),
    SemanticFrame(
        name="commutes_with",
        template="{lhs} commutes with {rhs}",
        slots=[FrameSlot("lhs", "NOUN"),
               FrameSlot("rhs", "NOUN")],
    ),
    SemanticFrame(
        name="dual_to",
        template="{lhs} is dual to {rhs}",
        slots=[FrameSlot("lhs", "NOUN"),
               FrameSlot("rhs", "NOUN")],
    ),
    # ── composition ───────────────────────────────────────────────────────────
    SemanticFrame(
        name="composition",
        template="the {whole} is the {relation} of {part}",
        slots=[FrameSlot("whole", "NOUN"),
               FrameSlot("relation", "NOUN"),
               FrameSlot("part", "NOUN")],
    ),
    # ── equation / operator ──────────────────────────────────────────────────
    SemanticFrame(
        name="equation_op",
        template="the {quantity} equals the {operator} of the {argument}",
        slots=[FrameSlot("quantity", "NOUN"),
               FrameSlot("operator", "NOUN"),
               FrameSlot("argument", "NOUN")],
    ),
    # ── modifier ──────────────────────────────────────────────────────────────
    SemanticFrame(
        name="modified_subject",
        template="the {modifier} {topic} {verb}s",
        slots=[FrameSlot("modifier", "ADJECTIVE"),
               FrameSlot("topic", "NOUN"),
               FrameSlot("verb", "VERB")],
    ),
]


# ───────────────────────────────────────────────────────────────────────────────
# FRAME FILLER
# ───────────────────────────────────────────────────────────────────────────────

@dataclass
class FilledFrame:
    frame: SemanticFrame
    fillers: Dict[str, str]
    surface: str
    tax: float
    grounded_count: int
    total_slots: int

    @property
    def verification_rate(self) -> float:
        if self.total_slots == 0:
            return 100.0
        return self.grounded_count / self.total_slots * 100


def fill_frame(frame: SemanticFrame,
               topic_vec: List[int],
               vocab,                     # LeechLatticeVocabulary
               max_hamming_gap: int,
               seed_words: Optional[Dict[str, str]] = None,
               forbidden: Optional[List[str]] = None
               ) -> Optional[FilledFrame]:
    """
    Deterministically fill a frame.  Returns None if any required slot
    cannot be grounded.
    """
    seed_words = seed_words or {}
    forbidden = set(forbidden or [])
    fillers: Dict[str, str] = {}
    vectors: List[List[int]] = []
    grounded = 0
    used = set(forbidden)

    for slot in frame.slots:
        chosen_word, chosen_vec = None, None

        # honour seed_word
        if slot.name in seed_words and seed_words[slot.name] in vocab.words \
                and seed_words[slot.name] not in used:
            w = seed_words[slot.name]
            chosen_word = w
            chosen_vec = vocab.words[w].vector

        # honour the slot's own seed
        elif slot.seed_word and slot.seed_word in vocab.words \
                and slot.seed_word not in used:
            chosen_word = slot.seed_word
            chosen_vec = vocab.words[slot.seed_word].vector

        else:
            # pick from candidates of the desired role
            candidates = list(vocab.by_role.get(slot.role, []))
            if not candidates and slot.role != "ANY":
                # fall back to any noun (always plentiful)
                candidates = list(vocab.by_role.get("NOUN", []))

            best_word, best_d, best_vec = None, 99, None
            ref = vectors[-1] if vectors else topic_vec
            for w in candidates:
                if w in used:
                    continue
                e = vocab.words[w]
                d_topic = BLA.hamming_distance(topic_vec, e.vector)
                d_prev = BLA.hamming_distance(ref, e.vector)
                # Combined cost: closeness to topic + low tax to previous slot.
                score = d_topic + d_prev
                if score < best_d:
                    best_d, best_word, best_vec = score, w, e.vector
            chosen_word, chosen_vec = best_word, best_vec

        if chosen_word is None and slot.require_grounded:
            return None
        if chosen_word is None:
            # last-ditch property word
            chosen_word = "value"
            chosen_vec = topic_vec
        fillers[slot.name] = chosen_word
        vectors.append(chosen_vec)
        used.add(chosen_word)
        # Was the binding strictly grounded?
        if chosen_word in vocab.words:
            e = vocab.words[chosen_word]
            if e.hamming_to_system <= max_hamming_gap:
                grounded += 1

    # sentence tax = sum of consecutive Hamming distances
    tax = 0.0
    for i in range(1, len(vectors)):
        tax += BLA.hamming_distance(vectors[i - 1], vectors[i])

    if tax > frame.max_tax:
        return None

    surface = frame.template.format(**fillers)
    return FilledFrame(frame=frame, fillers=fillers, surface=surface,
                       tax=tax, grounded_count=grounded,
                       total_slots=len(frame.slots))


def select_frames_for_query(query_concepts: List[str],
                            available_frames: List[SemanticFrame] = None
                            ) -> List[SemanticFrame]:
    """
    Pick a sensible subset of frames based on the query.
    Deterministic: pure function of the input concepts.
    """
    if available_frames is None:
        available_frames = FRAMES
    qs = " ".join(query_concepts).lower()

    chosen = []
    # heuristic mapping from query verbs to frames
    if any(w in qs for w in ("define", "what", "is", "describe")):
        chosen.append(_get_frame("definition_isa"))
        chosen.append(_get_frame("definition_property"))
    if any(w in qs for w in ("scale", "scaling", "power", "exponent", "depends")):
        chosen.append(_get_frame("scales_as"))
        chosen.append(_get_frame("depends_on"))
    if any(w in qs for w in ("commute", "commutator", "anticommute")):
        chosen.append(_get_frame("commutes_with"))
    if any(w in qs for w in ("dual", "holographic", "ads", "bcft")):
        chosen.append(_get_frame("dual_to"))
    if any(w in qs for w in ("equation", "operator", "derivative", "integral", "gradient")):
        chosen.append(_get_frame("equation_op"))
    if any(w in qs for w in ("composed", "made", "consists", "composition")):
        chosen.append(_get_frame("composition"))

    if not chosen:
        # default mix that works for most queries
        chosen = [
            _get_frame("definition_isa"),
            _get_frame("modified_subject"),
            _get_frame("composition"),
        ]
    # de-dup preserving order
    seen, out = set(), []
    for f in chosen:
        if f and f.name not in seen:
            seen.add(f.name)
            out.append(f)
    return out


def _get_frame(name: str) -> Optional[SemanticFrame]:
    for f in FRAMES:
        if f.name == name:
            return f
    return None


if __name__ == "__main__":
    print("Frames defined:")
    for f in FRAMES:
        print(" ", f.name, "->", f.template)
    print()
    print("Selection demo:")
    for q in (["define", "weyl anomaly"],
              ["scales", "rayleigh", "number"],
              ["commute", "operators"]):
        print(" ", q, "=>", [f.name for f in select_frames_for_query(q)])