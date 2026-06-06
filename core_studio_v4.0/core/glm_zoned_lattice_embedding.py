"""
================================================================================
GLM ZONED LATTICE EMBEDDING v3.2 — "The Transformation Manifold"
================================================================================
Implements spatially-deterministic placement of words in the 24-bit Golay /
Leech-lattice substrate, partitioned into S/O/M grammatical zones.

v3.2 Improvements:
- Calculus of Transformations: Gray code sub-signatures for operator types.
- Tensor Composition: Multi-variable field XOR composition.
- Corrected Syndrome Metrics: Records anchor distance (0-4) as syndrome_w.
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
    """'S' / 'O' / 'M' — whichever zone carries the most active bits."""
    w = zone_signature(v24)
    if w[0] >= w[1] and w[0] >= w[2]:
        return "S"
    if w[1] >= w[2]:
        return "O"
    return "M"


# ════════════════════════════════════════════════════════════════════════════════
# 2. ROLE-ANCHOR OCTADS
# ════════════════════════════════════════════════════════════════════════════════

def build_role_basis() -> Dict[str, List[int]]:
    """Return {role: 24-bit Golay octad biased toward role's home zone}."""
    octads = GOLAY_ENGINE.get_octads()
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

# Calculus of Transformations — v3.2 Gray code sub-signatures
_TRANSFORMATION_TYPES = {
    "LINEAR":      (1, 0, 0),
    "QUADRATIC":   (0, 1, 0),
    "EXPONENTIAL": (1, 1, 1),
    "LOGARITHMIC": (0, 0, 1),
}

def get_transformation_signature(math_equivalent: Optional[int]) -> List[int]:
    """Return a 3-bit Gray code signature for the transformation type."""
    v = [0, 0, 0]
    if math_equivalent is None: return v
    if math_equivalent in (401,): t = "EXPONENTIAL"
    elif math_equivalent in (402,): t = "LOGARITHMIC"
    elif math_equivalent in (404,): t = "QUADRATIC"
    else: t = "LINEAR"
    sig = _TRANSFORMATION_TYPES.get(t, (1, 0, 0))
    return list(sig)


def mog_stamp(cat: str, role: str) -> List[int]:
    zone = ZONE_NAMES[ROLE_HOME_ZONE[role]]
    idx = MOG_CATEGORIES.index(cat)
    gray = idx ^ (idx >> 1)
    v = [0] * 24
    for i in range(5):
        if (gray >> i) & 1:
            v[zone[i]] = 1
    return v


# ════════════════════════════════════════════════════════════════════════════════
# 4. LEMMA PERTURBATION
# ════════════════════════════════════════════════════════════════════════════════

def lemma_stamp(lemma_id: int, role: str) -> List[int]:
    home_zone_name = ROLE_HOME_ZONE[role]
    home_zone = ZONE_NAMES[home_zone_name]
    next_zone_name = {"S": "O", "O": "M", "M": "S"}[home_zone_name]
    next_zone = ZONE_NAMES[next_zone_name]
    v = [0] * 24
    if lemma_id <= 0: return v
    gray = lemma_id ^ (lemma_id >> 1)
    for i in range(3):
        if (gray >> i) & 1: v[home_zone[5 + i]] = 1
    for i in range(2):
        if (gray >> (3 + i)) & 1: v[next_zone[i]] = 1
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
    def __init__(self):
        self.role_basis: Dict[str, List[int]] = build_role_basis()
        self.words:      Dict[str, ZonedWord] = {}

    def _lemma_id_for(self, lemma: str, role: str, mog_category: str,
                      math_equivalent: int = None) -> int:
        if math_equivalent is not None:
            return math_equivalent % 32
        h = 0
        for ch in lemma: h = (h * 31 + ord(ch)) & 0xFF
        return h % 32

    def _repair_zone_purity(self, vector: List[int], role: str) -> List[int]:
        home = ROLE_HOME_ZONE[role]
        h_idx = "SOM".index(home)
        sig = zone_signature(vector)
        if sig[h_idx] >= max(sig): return vector
        v = list(vector)
        for other_zone_name in ["S", "O", "M"]:
            if other_zone_name == home: continue
            zone_bits = ZONE_NAMES[other_zone_name]
            for i in reversed(zone_bits):
                if v[i] == 1:
                    v[i] = 0
                    break
            if zone_signature(v)[h_idx] >= max(zone_signature(v)): return v
        return v

    def add(self, lemma: str, role: str, mog_category: str,
            math_equivalent: int = None) -> ZonedWord:
        lemma_id = self._lemma_id_for(lemma, role, mog_category, math_equivalent)
        R = self.role_basis[role]
        M = mog_stamp(mog_category, role)
        L = lemma_stamp(lemma_id, role)
        perturb = [m ^ l for m, l in zip(M, L)]
        vector  = self._repair_zone_purity([r ^ p for r, p in zip(R, perturb)], role)
        snapped, meta = GOLAY_ENGINE.snap_to_codeword(vector)
        dist = meta["anchor_distance"] if meta["correctable"] else 4
        zw = ZonedWord(lemma, role, mog_category, lemma_id, vector, list(R), dist, zone_signature(vector), LEECH_ENGINE.calculate_nrci(vector))
        self.words[lemma] = zw
        return zw

    def apply_shift(self, subject_lemmas: List[str] | str, op_lemma: str) -> Optional[ZonedWord]:
        if isinstance(subject_lemmas, str): subject_lemmas = [subject_lemmas]
        subjects = [self.get(s) for s in subject_lemmas if self.get(s)]
        operator = self.get(op_lemma)
        if not subjects or not operator or operator.role not in ("OPERATOR", "VERB"): return None
        composite_vector = [0] * 24
        for s in subjects:
            for i in range(24): composite_vector[i] ^= s.vector[i]
        shift_code = operator.lemma_id
        type_sig = get_transformation_signature(shift_code)
        home_zone = subjects[0].home_zone
        next_zone_bits = ZONE_NAMES[{"S": "O", "O": "M", "M": "S"}[home_zone]]
        shifted_vector = list(composite_vector)
        gray_shift = shift_code ^ (shift_code >> 1)
        for i in range(5):
            if (gray_shift >> i) & 1: shifted_vector[next_zone_bits[i]] = 1 - shifted_vector[next_zone_bits[i]]
        for i in range(3):
            if type_sig[i]: shifted_vector[next_zone_bits[5 + i]] = 1 - shifted_vector[next_zone_bits[5 + i]]
        snapped, meta = GOLAY_ENGINE.snap_to_codeword(shifted_vector)
        dist = meta["anchor_distance"] if meta["correctable"] else 4
        return ZonedWord(f"{op_lemma}({','.join(subject_lemmas)})", subjects[0].role, subjects[0].mog_category, subjects[0].lemma_id, snapped, subjects[0].anchor, dist, zone_signature(snapped), LEECH_ENGINE.calculate_nrci(snapped))

    def get(self, lemma: str) -> Optional[ZonedWord]:
        return self.words.get(lemma)

def lift_strict_vocabulary(strict_vocab_path: str) -> ZonedVocabulary:
    import json
    with open(strict_vocab_path, encoding="utf-8") as f: data = json.load(f)
    vocab = ZonedVocabulary()
    for lemma, info in data["words"].items():
        vocab.add(lemma, info.get("role", "NOUN"), info.get("mog_category", "M_Count"))
    return vocab
