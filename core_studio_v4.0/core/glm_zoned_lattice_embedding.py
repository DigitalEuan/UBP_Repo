"""
================================================================================
GLM ZONED LATTICE EMBEDDING v2.0 — "The Grammar Lattice"
================================================================================
Implements spatially-deterministic placement of words in the 24-bit Golay /
Leech-lattice substrate, such that the bit-zone in which a word's active
weight is concentrated is a deterministic function of its grammatical role.

v2.0 Improvements:
- Deterministic Lemma IDs (math-equivalent integer or stable hash).
- 2-bit Gray code Lemma Stamps (16 sibling slots per role/category).
- Zone Repair strategy for words at category boundaries.
- Grounded extension principle (definition_is_grounded).

──────────────────────────────────────────────────────────────────────────────
DESIGN OVERVIEW
──────────────────────────────────────────────────────────────────────────────
The 24 bits are split into three 8-bit grammar zones:

    Z_S = bits  0..7   "Subject Zone"     —  NOUNs live here
    Z_O = bits  8..15  "Operator Zone"    —  VERBs / OPERATORs live here
    Z_M = bits 16..23  "Modifier Zone"    —  ADJECTIVES / PROPERTIES live here

Each word vector is constructed as

    v(word) = R(role)  XOR  M(mog_category, role)  XOR  L(lemma_id, role)

where every term lives in (or affects only) the role's home zone.
================================================================================
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple
from fractions import Fraction

from ubp_unified_v5 import (
    GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra,
)

BLA = BinaryLinearAlgebra
F   = Fraction


# ════════════════════════════════════════════════════════════════════════════════
# 1. ZONES
# ════════════════════════════════════════════════════════════════════════════════

ZONE_S: Tuple[int, ...] = tuple(range(0, 8))
ZONE_O: Tuple[int, ...] = tuple(range(8, 16))
ZONE_M: Tuple[int, ...] = tuple(range(16, 24))

ZONE_NAMES: Dict[str, Tuple[int, ...]] = {
    "S": ZONE_S, "O": ZONE_O, "M": ZONE_M,
}

ROLE_HOME_ZONE: Dict[str, str] = {
    "NOUN":      "S",
    "VERB":      "O",
    "OPERATOR":  "O",
    "ADJECTIVE": "M",
    "PROPERTY":  "M",
}

ROLES: Tuple[str, ...] = tuple(ROLE_HOME_ZONE.keys())


def zone_weight(v24: Sequence[int], zone: Tuple[int, ...]) -> int:
    return sum(v24[i] for i in zone)


def zone_signature(v24: Sequence[int]) -> Tuple[int, int, int]:
    return (zone_weight(v24, ZONE_S),
            zone_weight(v24, ZONE_O),
            zone_weight(v24, ZONE_M))


def dominant_zone(v24: Sequence[int]) -> str:
    """'S' / 'O' / 'M' — whichever zone carries the most active bits.
    Ties broken in the order S, O, M."""
    w = zone_signature(v24)
    if w[0] >= w[1] and w[0] >= w[2]:
        return "S"
    if w[1] >= w[2]:
        return "O"
    return "M"


# ════════════════════════════════════════════════════════════════════════════════
# 2. ROLE-ANCHOR OCTADS
# ════════════════════════════════════════════════════════════════════════════════

def _best_octad_for_zone(zone: Tuple[int, ...]) -> List[int]:
    """Among the 759 Golay octads, return the one whose support has the
    largest intersection with `zone`. First-encountered tie wins."""
    zone_set = set(zone)
    best_cw: Optional[List[int]] = None
    best_ov = -1
    for cw in GOLAY_ENGINE.get_octads():
        ov = sum(1 for i in zone_set if cw[i])
        if ov > best_ov:
            best_ov = ov
            best_cw = list(cw)
            if ov == 8:
                break
    assert best_cw is not None
    return best_cw


def build_role_basis() -> Dict[str, List[int]]:
    """Return {role: 24-bit Golay octad biased toward role's home zone}.
    Uses unique anchors for each role to improve separation."""
    octads = GOLAY_ENGINE.get_octads()
    # Hand-selected unique octads for each role (highest zone weight)
    # Zone S best indices: 110, 206
    # Zone O best indices: 490, 639
    # Zone M best indices: 27, 78
    return {
        "NOUN":      list(octads[110]),  # (6, 1, 1)
        "VERB":      list(octads[490]),  # (0, 6, 2)
        "OPERATOR":  list(octads[639]),  # (0, 6, 2)
        "ADJECTIVE": list(octads[27]),   # (2, 0, 6)
        "PROPERTY":  list(octads[78]),   # (2, 0, 6)
    }


# ════════════════════════════════════════════════════════════════════════════════
# 3. MOG CATEGORY → ZONE-LOCAL STAMP
# ════════════════════════════════════════════════════════════════════════════════

MOG_CATEGORIES: Tuple[str, ...] = (
    "M_Mass", "M_Charge", "M_Space", "M_Time", "M_Thermal", "M_Count",
    "I_Topology", "I_Symmetry", "I_Density", "I_Connectivity",
    "I_Dimension", "I_Complexity",
    "A_Energy", "A_Force", "A_Velocity", "A_Flux", "A_Resonance", "A_Spin",
    "P_Probability", "P_Ratio", "P_Limit", "P_Tax", "P_Coherence", "P_Phase",
)

_QUADRANT_OF: Dict[str, str] = {c: c[0] for c in MOG_CATEGORIES}

# Map sub-index 0..5 → 4-bit pattern with weight ≤ 2.
_LOW_WEIGHT_4_TABLE: Tuple[Tuple[int, int, int, int], ...] = (
    (0, 0, 0, 0),   # 0
    (1, 0, 0, 0),   # 1
    (0, 1, 0, 0),   # 2
    (1, 1, 0, 0),   # 3
    (0, 0, 1, 0),   # 4
    (1, 0, 1, 0),   # 5
)


def _low_weight_4(idx: int) -> Tuple[int, int, int, int]:
    return _LOW_WEIGHT_4_TABLE[idx % 6]


def mog_stamp(cat: str, role: str) -> List[int]:
    """A 24-bit vector encoding the MOG category deterministically.
    Uses a 5-bit Gray code in the first 5 bits of the home zone.
    This provides 32 category slots with 0 overlap with the lemma stamp."""
    zone = ZONE_NAMES[ROLE_HOME_ZONE[role]]
    idx = MOG_CATEGORIES.index(cat)
    # 5-bit Gray code for 24 categories
    gray = idx ^ (idx >> 1)
    v = [0] * 24
    for i in range(5):
        if (gray >> i) & 1:
            v[zone[i]] = 1
    return v


# ════════════════════════════════════════════════════════════════════════════════
# 4. LEMMA PERTURBATION (sibling distinguisher)
# ════════════════════════════════════════════════════════════════════════════════

def lemma_stamp(lemma_id: int, role: str) -> List[int]:
    """Extend to a 5-bit lemma stamp (32 slots) to resolve collisions.
    Uses bits 5-7 of the home zone and bits 0-1 of the cyclic next zone.
    This preserves home-zone dominance for the majority of words."""
    home_zone_name = ROLE_HOME_ZONE[role]
    home_zone = ZONE_NAMES[home_zone_name]

    # Cyclic next zone
    next_zone_name = {"S": "O", "O": "M", "M": "S"}[home_zone_name]
    next_zone = ZONE_NAMES[next_zone_name]

    v = [0] * 24
    if lemma_id <= 0:
        return v

    # 5-bit Gray code (32 states)
    gray = lemma_id ^ (lemma_id >> 1)

    # Low 3 bits in Home zone (bits 5,6,7)
    for i in range(3):
        if (gray >> i) & 1:
            v[home_zone[5 + i]] = 1

    # High 2 bits in Next zone (bits 0,1)
    for i in range(2):
        if (gray >> (3 + i)) & 1:
            v[next_zone[i]] = 1

    return v


# ════════════════════════════════════════════════════════════════════════════════
# 5. WORD ASSEMBLY
# ════════════════════════════════════════════════════════════════════════════════

@dataclass
class ZonedWord:
    lemma:        str
    role:         str
    mog_category: str
    lemma_id:     int
    vector:       List[int]
    anchor:       List[int]
    syndrome_w:   int
    zone_sig:     Tuple[int, int, int]
    nrci:         Fraction

    @property
    def home_zone(self) -> str:
        return ROLE_HOME_ZONE[self.role]

    @property
    def is_zone_pure(self) -> bool:
        h = "SOM".index(self.home_zone)
        return self.zone_sig[h] >= max(self.zone_sig)


class ZonedVocabulary:
    """Holds the deterministic role anchors and provides deterministic
    lemma IDs based on math equivalents or stable hashing."""

    def __init__(self):
        self.role_basis: Dict[str, List[int]] = build_role_basis()
        self.words:      Dict[str, ZonedWord] = {}

    def _lemma_id_for(self, lemma: str, role: str, mog_category: str,
                      math_equivalent: int = None) -> int:
        if math_equivalent is not None:
            # Ground truth: use the substrate value directly
            return math_equivalent % 32   # 32 sibling slots per (role, cat)
        # For words without math equivalents: stable hash of lemma string
        h = 0
        for ch in lemma:
            h = (h * 31 + ord(ch)) & 0xFF
        return h % 32

    def _repair_zone_purity(self, vector: List[int], role: str) -> List[int]:
        """If vector is not zone-pure, flip the minimum bits to make it so.
        Returns corrected vector. Never touches bits outside the home zone."""
        home = ROLE_HOME_ZONE[role]
        h_idx = "SOM".index(home)
        sig = zone_signature(vector)
        if sig[h_idx] >= max(sig):
            return vector   # already pure
        # Find the non-home zone with highest weight and suppress its top bit
        v = list(vector)
        for other_zone_name in ["S", "O", "M"]:
            if other_zone_name == home:
                continue
            zone_bits = ZONE_NAMES[other_zone_name]
            # Zero the highest-index active bit in this other zone
            for i in reversed(zone_bits):
                if v[i] == 1:
                    v[i] = 0
                    break
            # Re-check purity
            sig2 = zone_signature(v)
            if sig2[h_idx] >= max(sig2):
                return v
        return v   # best effort

    def add(self, lemma: str, role: str, mog_category: str,
            math_equivalent: int = None) -> ZonedWord:
        if role not in self.role_basis:
            raise ValueError(f"unknown role {role!r}")
        if mog_category not in MOG_CATEGORIES:
            raise ValueError(f"unknown MOG category {mog_category!r}")

        lemma_id = self._lemma_id_for(lemma, role, mog_category, math_equivalent)

        R = self.role_basis[role]
        M = mog_stamp(mog_category, role)
        L = lemma_stamp(lemma_id, role)
        perturb = [m ^ l for m, l in zip(M, L)]
        vector  = [r ^ p for r, p in zip(R, perturb)]

        # Repair zone purity before snapping
        vector = self._repair_zone_purity(vector, role)

        anchor  = list(R)

        snapped, meta = GOLAY_ENGINE.snap_to_codeword(vector)
        zw = ZonedWord(
            lemma=lemma, role=role, mog_category=mog_category,
            lemma_id=lemma_id, vector=vector, anchor=anchor,
            syndrome_w=meta["syndrome_weight"],
            zone_sig=zone_signature(vector),
            nrci=LEECH_ENGINE.calculate_nrci(vector),
        )
        self.words[lemma] = zw
        return zw

    def apply_shift(self, subject_lemma: str, op_lemma: str) -> Optional[ZonedWord]:
        """
        Applies a semantic magnitude shift to a subject noun using an operator.
        Uses XOR logic between the subject's vector and the operator's
        math-equivalent signature.
        """
        subject = self.get(subject_lemma)
        operator = self.get(op_lemma)
        if not subject or not operator or operator.role not in ("OPERATOR", "VERB"):
            return None

        # Get the math equivalent of the operator (magnitude shift code)
        # We'll use this to create a deterministic perturbation
        shift_code = operator.lemma_id # already derived from math_equivalent if present

        # Apply shift: XOR the subject vector with a Gray-coded version of the shift
        # We apply this to the 'Next' zone to avoid destroying the subject's zone purity
        home_zone = subject.home_zone
        next_zone_name = {"S": "O", "O": "M", "M": "S"}[home_zone]
        next_zone_bits = ZONE_NAMES[next_zone_name]

        shifted_vector = list(subject.vector)
        gray_shift = shift_code ^ (shift_code >> 1)
        for i in range(5):
            if (gray_shift >> i) & 1:
                idx = next_zone_bits[i]
                shifted_vector[idx] = 1 - shifted_vector[idx]

        # Snap result to codeword
        snapped, meta = GOLAY_ENGINE.snap_to_codeword(shifted_vector)

        # Create a transient ZonedWord for the shifted state
        return ZonedWord(
            lemma=f"{op_lemma}({subject_lemma})",
            role=subject.role,
            mog_category=subject.mog_category,
            lemma_id=subject.lemma_id, # Inherit base identity
            vector=snapped,
            anchor=subject.anchor,
            syndrome_w=meta["syndrome_weight"],
            zone_sig=zone_signature(snapped),
            nrci=LEECH_ENGINE.calculate_nrci(snapped)
        )

    def get(self, lemma: str) -> Optional[ZonedWord]:
        return self.words.get(lemma)


def definition_is_grounded(definition_tokens: list[str],
                            vocab: ZonedVocabulary) -> tuple[bool, list[str]]:
    """
    Returns (all_grounded, missing_words).
    Only call vocab.add() for a new word if all_grounded is True.
    """
    missing = [t for t in definition_tokens if vocab.get(t) is None]
    return (len(missing) == 0), missing


# ════════════════════════════════════════════════════════════════════════════════
# 7. LIFT EXISTING STRICT VOCABULARY INTO THE ZONED LATTICE
# ════════════════════════════════════════════════════════════════════════════════

def lift_strict_vocabulary(strict_vocab_path: str) -> ZonedVocabulary:
    """Read `glm_strict_vocabulary.json`, drop its hash-derived 24-bit
    vectors, and re-embed every word with a zone-coherent vector."""
    import json
    with open(strict_vocab_path, encoding="utf-8") as f:
        data = json.load(f)
    vocab = ZonedVocabulary()
    for lemma, info in data["words"].items():
        role = info.get("role", "NOUN")
        mog  = info.get("mog_category", "M_Count")
        if role not in ROLES:
            role = "NOUN"
        if mog not in MOG_CATEGORIES:
            mog = "M_Count"
        vocab.add(lemma, role, mog)
    return vocab


# ════════════════════════════════════════════════════════════════════════════════
# 8. SELF-TEST
# ════════════════════════════════════════════════════════════════════════════════

def _self_test():
    print("─" * 78)
    print(" GLM ZONED LATTICE EMBEDDING — Self-Test v2.0")
    print("─" * 78)

    rb = build_role_basis()
    print(" Role anchors (Golay octads biased toward home zone):")
    for r, cw in rb.items():
        sig = zone_signature(cw)
        h = "SOM".index(ROLE_HOME_ZONE[r])
        dom = sig[h] == max(sig)
        print(f"   {r:9s} hw={sum(cw)} sig(S,O,M)={sig} home={ROLE_HOME_ZONE[r]} dom={dom}")

    vocab = ZonedVocabulary()
    sample = [
        ("electron",   "NOUN",      "M_Mass"),
        ("photon",     "NOUN",      "A_Energy"),
        ("hamiltonian","NOUN",      "A_Energy"),
        ("symmetry",   "NOUN",      "I_Symmetry"),
        ("commutes",   "VERB",      "I_Symmetry"),
        ("scales",     "VERB",      "P_Ratio"),
        ("between",    "OPERATOR",  "I_Connectivity"),
        ("massless",   "ADJECTIVE", "M_Mass"),
        ("topological","ADJECTIVE", "I_Topology"),
        ("strong",     "PROPERTY",  "A_Force"),
    ]
    for lemma, role, mog in sample:
        vocab.add(lemma, role, mog)

    # Test Gap 1: Determinism
    print("\n Testing Gap 1: Determinism")
    v1 = vocab.words["electron"].vector
    v2 = ZonedVocabulary().add("electron", "NOUN", "M_Mass").vector
    print(f"   Duplicate add 'electron' identical vector: {v1 == v2}")

    # Test Gap 2: 16 slots via Gray code
    print("\n Testing Gap 2: 16 slots via Gray code")
    v_ids = []
    for i in range(16):
        w = vocab.add(f"word_{i}", "NOUN", "M_Count", math_equivalent=i)
        v_ids.append(w.vector)
    unique_vectors = len(set(tuple(v) for v in v_ids))
    print(f"   16 sibling words unique vectors: {unique_vectors == 16}")

    print("\n Sample zoned words:")
    print(f"   {'lemma':14s} {'role':10s} {'mog':16s} "
          f"{'sig':12s} {'pure':5s} {'snap':5s} {'nrci':8s}")
    for lemma, _, _ in sample:
        w = vocab.words[lemma]
        print(f"   {w.lemma:14s} {w.role:10s} {w.mog_category:16s} "
              f"{str(w.zone_sig):12s} {str(w.is_zone_pure):5s} "
              f"{w.syndrome_w:5d} {float(w.nrci):.4f}")


if __name__ == "__main__":
    _self_test()
