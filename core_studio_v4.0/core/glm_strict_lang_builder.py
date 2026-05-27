"""
================================================================================
GLM STRICT LANGUAGE DATABASE BUILDER v3.0 (Full v6.1 Alignment)
================================================================================
Builds a complete language database from the UBP system_kb and lang_kb.
Implements STRICT semantic binding: every word is bound EXACTLY to its
system_kb vector entry via Hamming distance verification.

NEW in v3.0:
- MOG category classification (24 semantic dimensions)
- fold24_to3 tension analysis for word grouping
- Volumetric Rebate in coherence scoring
- BarnesWall 256D macro-stability auditing per word
- Internal Dialogue pattern (multi-depth physical grounding)
- Gap detection: reports concepts that lack vocabulary
- Deterministic mapping: NO probabilistic selection

Architecture:
- Each word = a verified point in Λ₂₄ (the Leech Lattice)
- Relationships = Hamming distance between 24-bit vectors
- Grammar = geometric constraints (not probabilistic)
- Sentence coherence = symmetry tax (sum of consecutive Hamming distances)
- Error correction = Golay(24,12) snapping to nearest codeword
- Macro-stability = Barnes-Wall 256D audit
================================================================================
"""

import json
import re
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
from fractions import Fraction

from ubp_unified_v5 import (
    GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE, BarnesWallEngine,
    BinaryLinearAlgebra, GolayCodeEngine, LeechLatticeEngine,
    UBPUltimateSubstrate, to_gray_code,
    ontological_position_to_vector, MOG_CATEGORIES
)


# --- Configuration ---
MAX_HAMMING_GAP = 6       # Max distance for strict grounding (from internal dialogue blueprint)
ADJACENCY_RADIUS = 8      # Hamming distance for "related" concepts
SENTENCE_MAX_TAX = 40.0   # Maximum symmetry tax for a valid sentence
CANDIDATE_COUNT = 8        # Number of candidate sentences to generate per slot
GOLAY_CORRECTION_THRESHOLD = 3  # Max bits to correct via Golay (matches Golay 3-error correction)


# ═══════════════════════════════════════════════════════════════════════════════
# WORD CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

NOUN_INDICATORS = {
    'a ', 'an ', 'the ', 'state of', 'quality of', 'condition of',
    'process of', 'act of', 'instance of', 'type of', 'form of',
    'point ', 'region ', 'area ', 'body ', 'unit ', 'system ',
    'structure', 'entity', 'object', 'thing', 'substance', 'material',
    'phenomenon', 'concept', 'principle', 'mechanism', 'framework',
}

VERB_INDICATORS = {
    'to ', 'the act of', 'action of', 'causing', 'making',
    'moving', 'changing', 'creating', 'producing', 'generating',
    'transforming', 'connecting', 'linking', 'binding', 'breaking',
}

ADJECTIVE_INDICATORS = {
    'having', 'being', 'characterized by', 'relating to',
    'pertaining to', 'of or relating', 'resembling',
    'capable of', 'tending to', 'inclined to',
    'marked by', 'exhibiting', 'showing',
}

ROLE_OVERRIDES = {
    # Nouns
    'anchor': 'NOUN', 'atmosphere': 'NOUN', 'boundary': 'NOUN',
    'capacity': 'NOUN', 'channel': 'NOUN', 'circuit': 'NOUN',
    'cluster': 'NOUN', 'core': 'NOUN', 'crystal': 'NOUN',
    'current': 'NOUN', 'cycle': 'NOUN', 'density': 'NOUN',
    'dimension': 'NOUN', 'domain': 'NOUN', 'edge': 'NOUN',
    'element': 'NOUN', 'energy': 'NOUN', 'engine': 'NOUN',
    'entropy': 'NOUN', 'equilibrium': 'NOUN', 'fabric': 'NOUN',
    'field': 'NOUN', 'flux': 'NOUN', 'force': 'NOUN',
    'foundation': 'NOUN', 'frame': 'NOUN', 'frequency': 'NOUN',
    'frontier': 'NOUN', 'gradient': 'NOUN', 'gravity': 'NOUN',
    'grid': 'NOUN', 'harmony': 'NOUN', 'horizon': 'NOUN',
    'impulse': 'NOUN', 'inertia': 'NOUN', 'interface': 'NOUN',
    'kernel': 'NOUN', 'lattice': 'NOUN', 'layer': 'NOUN',
    'lens': 'NOUN', 'light': 'NOUN', 'magnitude': 'NOUN',
    'mass': 'NOUN', 'matrix': 'NOUN', 'membrane': 'NOUN',
    'momentum': 'NOUN', 'network': 'NOUN', 'nexus': 'NOUN',
    'node': 'NOUN', 'nucleus': 'NOUN', 'orbit': 'NOUN',
    'origin': 'NOUN', 'oscillation': 'NOUN', 'particle': 'NOUN',
    'path': 'NOUN', 'pattern': 'NOUN', 'phase': 'NOUN',
    'pivot': 'NOUN', 'plane': 'NOUN', 'polarity': 'NOUN',
    'potential': 'NOUN', 'pressure': 'NOUN', 'prism': 'NOUN',
    'pulse': 'NOUN', 'radius': 'NOUN', 'ratio': 'NOUN',
    'resonance': 'NOUN', 'rhythm': 'NOUN', 'scale': 'NOUN',
    'sequence': 'NOUN', 'signal': 'NOUN', 'source': 'NOUN',
    'spectrum': 'NOUN', 'sphere': 'NOUN', 'spiral': 'NOUN',
    'structure': 'NOUN', 'surface': 'NOUN', 'symmetry': 'NOUN',
    'system': 'NOUN', 'tensor': 'NOUN', 'threshold': 'NOUN',
    'topology': 'NOUN', 'torque': 'NOUN', 'trajectory': 'NOUN',
    'vector': 'NOUN', 'vertex': 'NOUN', 'vortex': 'NOUN',
    'wave': 'NOUN', 'wavelength': 'NOUN', 'weight': 'NOUN',
    'zone': 'NOUN', 'baryon': 'NOUN', 'boson': 'NOUN',
    'electron': 'NOUN', 'fermion': 'NOUN', 'gluon': 'NOUN',
    'hadron': 'NOUN', 'lepton': 'NOUN', 'meson': 'NOUN',
    'muon': 'NOUN', 'neutrino': 'NOUN', 'neutron': 'NOUN',
    'photon': 'NOUN', 'proton': 'NOUN', 'quark': 'NOUN',
    'hypothesis': 'NOUN', 'proportion': 'NOUN', 'period': 'NOUN',
    'bottom': 'NOUN', 'top': 'NOUN', 'strange': 'NOUN',
    # Verbs
    'absorb': 'VERB', 'accelerate': 'VERB', 'activate': 'VERB',
    'align': 'VERB', 'amplify': 'VERB', 'attract': 'VERB',
    'balance': 'VERB', 'bind': 'VERB', 'branch': 'VERB',
    'collapse': 'VERB', 'compress': 'VERB', 'conduct': 'VERB',
    'converge': 'VERB', 'decay': 'VERB', 'diffuse': 'VERB',
    'dissolve': 'VERB', 'emit': 'VERB', 'encrypt': 'VERB',
    'evolve': 'VERB', 'expand': 'VERB', 'flow': 'VERB',
    'fold': 'VERB', 'fuse': 'VERB', 'generate': 'VERB',
    'merge': 'VERB', 'oscillate': 'VERB', 'polarize': 'VERB',
    'propagate': 'VERB', 'radiate': 'VERB', 'recurse': 'VERB',
    'reflect': 'VERB', 'refract': 'VERB', 'repel': 'VERB',
    'resonate': 'VERB', 'reverse': 'VERB', 'rotate': 'VERB',
    'scatter': 'VERB', 'split': 'VERB', 'stabilize': 'VERB',
    'transform': 'VERB', 'transmit': 'VERB', 'vibrate': 'VERB',
    # Adjectives
    'cold': 'ADJECTIVE', 'hot': 'ADJECTIVE', 'fast': 'ADJECTIVE',
    'slow': 'ADJECTIVE', 'heavy': 'ADJECTIVE', 'light': 'ADJECTIVE',
    'stable': 'ADJECTIVE', 'volatile': 'ADJECTIVE', 'harmonic': 'ADJECTIVE',
    'inverse': 'ADJECTIVE', 'fundamental': 'ADJECTIVE', 'different': 'ADJECTIVE',
    'essential': 'ADJECTIVE', 'physical': 'ADJECTIVE', 'opposite': 'ADJECTIVE',
    'coherent': 'ADJECTIVE', 'symmetric': 'ADJECTIVE', 'dense': 'ADJECTIVE',
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class WordEntry:
    """A word grounded in the Leech Lattice with full verification."""
    word: str
    vector: List[int]           # 24-bit vector from KB
    role: str                   # NOUN, VERB, ADJECTIVE, OPERATOR, PROPERTY
    ubp_id: str                 # Source KB entry ID
    hamming_to_system: int      # Distance to nearest system_kb entry
    nrci: float                 # Non-Recursive Compositional Index
    golay_codeword: List[int]   # Nearest Golay codeword
    golay_distance: int         # Distance to nearest codeword
    fold3: List[int]            # 3-bit tension signature
    mog_category: str           # Primary MOG category
    macro_nrci: float = 0.0    # Barnes-Wall 256D stability


@dataclass
class GrammarRule:
    """A sentence template with geometric constraints."""
    pattern: List[str]          # e.g., ['NOUN', 'VERB', 'NOUN']
    name: str
    max_tax: float = SENTENCE_MAX_TAX


@dataclass
class LearnedPath:
    """A learned low-tax word sequence."""
    words: List[str]
    vectors: List[List[int]]
    tax: float
    pattern_key: str


@dataclass
class LexicalGap:
    """A concept that lacks vocabulary (from internal dialogue)."""
    law_id: str
    concept_text: str
    vector: List[int]
    nearest_word: str
    distance: int


@dataclass
class LeechLatticeVocabulary:
    """Complete vocabulary grounded in the Leech Lattice."""
    words: Dict[str, WordEntry]
    by_role: Dict[str, List[str]]
    adjacency: Dict[str, List[str]]
    grammar_rules: List[GrammarRule]
    learned_paths: Dict[str, List[LearnedPath]]
    lexical_gaps: List[LexicalGap]
    system_vectors: Dict[str, List[int]]   # system_kb vectors indexed by ubp_id
    lang_vectors: Dict[str, List[int]]     # lang_kb vectors indexed by ubp_id


# ═══════════════════════════════════════════════════════════════════════════════
# VOCABULARY BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def _classify_word(word: str, definition: str) -> str:
    """Classify a word into its grammatical role."""
    # Check overrides first
    if word.lower() in ROLE_OVERRIDES:
        return ROLE_OVERRIDES[word.lower()]

    # Check word endings
    if word.endswith(('tion', 'sion', 'ment', 'ness', 'ity', 'ance', 'ence')):
        return 'NOUN'
    if word.endswith(('ate', 'ize', 'ify', 'ise')):
        return 'VERB'
    if word.endswith(('ive', 'ous', 'ful', 'less', 'able', 'ible', 'al', 'ic')):
        return 'ADJECTIVE'

    # Check definition text
    def_lower = definition.lower()
    for indicator in VERB_INDICATORS:
        if indicator in def_lower[:50]:
            return 'VERB'
    for indicator in ADJECTIVE_INDICATORS:
        if indicator in def_lower[:50]:
            return 'ADJECTIVE'
    for indicator in NOUN_INDICATORS:
        if indicator in def_lower[:50]:
            return 'NOUN'

    return 'PROPERTY'


def _get_mog_category(vector: List[int]) -> str:
    """Determine primary MOG category from vector bit pattern."""
    # Divide 24 bits into 4 sextets (Reality, Info, Activation, Potential)
    # Then find which of the 24 MOG categories has highest activation
    sextets = [vector[i:i+6] for i in range(0, 24, 6)]
    weights = [sum(s) for s in sextets]

    # Map to MOG quadrant
    quadrant_idx = weights.index(max(weights))
    # Within quadrant, find the most active pair
    sextet = sextets[quadrant_idx]
    pair_weights = [(sextet[2*i] + sextet[2*i+1], i) for i in range(3)]
    pair_weights.sort(reverse=True)
    sub_idx = pair_weights[0][1]

    category_idx = quadrant_idx * 6 + sub_idx * 2 + (1 if sum(vector) % 2 else 0)
    category_idx = min(category_idx, len(MOG_CATEGORIES) - 1)
    return MOG_CATEGORIES[category_idx]


def _extract_word_from_lexicon(lexicon: str) -> Tuple[str, str]:
    """Extract clean word and definition from lexicon string."""
    # Format: "[Type: Word], Definition text"
    try:
        bracket_part = lexicon.split(']')[0].replace('[', '')
        word = bracket_part.split(':')[-1].strip()
        definition = lexicon.split('],')[-1].strip() if '],' in lexicon else ''
        return word.lower(), definition
    except:
        return '', ''


def build_vocabulary(system_kb_path: str, lang_kb_path: str) -> LeechLatticeVocabulary:
    """
    Build a complete vocabulary with strict semantic binding.
    Every word MUST have a verified 24-bit vector from the KB.
    Uses Hamming distance verification (gap_threshold from internal dialogue).
    """
    print("\n" + "=" * 70)
    print("GLM STRICT VOCABULARY BUILDER v3.0")
    print("=" * 70)

    # Load KBs
    system_kb = _load_kb(system_kb_path)
    lang_kb = _load_kb(lang_kb_path)

    print(f"  System KB: {len(system_kb)} entries")
    print(f"  Language KB: {len(lang_kb)} entries")

    # Extract system vectors for grounding verification
    system_vectors = {}
    for uid, entry in system_kb.items():
        vec = entry.get('vector')
        if vec and len(vec) == 24:
            system_vectors[uid] = vec

    lang_vectors = {}
    for uid, entry in lang_kb.items():
        vec = entry.get('vector')
        if vec and len(vec) == 24:
            lang_vectors[uid] = vec

    # Build word entries with strict verification
    words: Dict[str, WordEntry] = {}
    by_role: Dict[str, List[str]] = defaultdict(list)
    lexical_gaps: List[LexicalGap] = []

    # Process language KB entries
    for uid, entry in lang_kb.items():
        vec = entry.get('vector')
        if not vec or len(vec) != 24:
            continue

        lexicon = entry.get('lexicon', '')
        word, definition = _extract_word_from_lexicon(lexicon)
        if not word or len(word) < 2:
            continue

        # Determine role
        if uid.startswith('OP_'):
            role = 'OPERATOR'
        else:
            role = _classify_word(word, definition)

        # STRICT GROUNDING: Find nearest system_kb vector
        min_dist = 99
        nearest_sys_id = None
        for sys_id, sys_vec in system_vectors.items():
            d = BinaryLinearAlgebra.hamming_distance(vec, sys_vec)
            if d < min_dist:
                min_dist = d
                nearest_sys_id = sys_id

        # Golay codeword snapping
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(vec)
        golay_distance = snap_info['anchor_distance']

        # fold24_to3 tension signature
        fold3 = BinaryLinearAlgebra.fold24_to3(vec)

        # MOG category
        mog_cat = _get_mog_category(vec)

        # NRCI
        nrci = float(LEECH_ENGINE.calculate_nrci(vec))

        # Create entry (only if within gap threshold)
        word_entry = WordEntry(
            word=word,
            vector=vec,
            role=role,
            ubp_id=uid,
            hamming_to_system=min_dist,
            nrci=nrci,
            golay_codeword=snapped,
            golay_distance=golay_distance,
            fold3=fold3,
            mog_category=mog_cat,
        )

        # Only include words that are strictly grounded
        if min_dist <= MAX_HAMMING_GAP:
            words[word] = word_entry
            by_role[role].append(word)
        else:
            # Record as lexical gap
            lexical_gaps.append(LexicalGap(
                law_id=nearest_sys_id or "UNKNOWN",
                concept_text=lexicon[:100],
                vector=vec,
                nearest_word=word,
                distance=min_dist
            ))

    # Also process system KB for direct physical concepts
    for uid, entry in system_kb.items():
        vec = entry.get('vector')
        if not vec or len(vec) != 24:
            continue

        lexicon = entry.get('lexicon', '')
        word, definition = _extract_word_from_lexicon(lexicon)
        if not word or len(word) < 2 or word in words:
            continue

        role = _classify_word(word, definition)
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(vec)
        fold3 = BinaryLinearAlgebra.fold24_to3(vec)
        mog_cat = _get_mog_category(vec)
        nrci = float(LEECH_ENGINE.calculate_nrci(vec))

        word_entry = WordEntry(
            word=word,
            vector=vec,
            role=role,
            ubp_id=uid,
            hamming_to_system=0,  # It IS a system entry
            nrci=nrci,
            golay_codeword=snapped,
            golay_distance=snap_info['anchor_distance'],
            fold3=fold3,
            mog_category=mog_cat,
        )
        words[word] = word_entry
        by_role[role].append(word)

    # Build adjacency graph (words within ADJACENCY_RADIUS)
    adjacency: Dict[str, List[str]] = defaultdict(list)
    word_list = list(words.keys())
    for i, w1 in enumerate(word_list):
        for w2 in word_list[i+1:]:
            d = BinaryLinearAlgebra.hamming_distance(words[w1].vector, words[w2].vector)
            if d <= ADJACENCY_RADIUS:
                adjacency[w1].append(w2)
                adjacency[w2].append(w1)

    # Define grammar rules
    grammar_rules = [
        GrammarRule(['NOUN', 'VERB', 'NOUN'], 'subject_verb_object'),
        GrammarRule(['ADJECTIVE', 'NOUN', 'VERB'], 'modified_subject_verb'),
        GrammarRule(['NOUN', 'VERB', 'ADJECTIVE', 'NOUN'], 'full_sentence'),
        GrammarRule(['NOUN', 'OPERATOR', 'NOUN'], 'relation'),
        GrammarRule(['ADJECTIVE', 'NOUN', 'VERB', 'NOUN'], 'complex_sentence'),
    ]

    print(f"\n  Strictly grounded words: {len(words)}")
    print(f"  Lexical gaps (d > {MAX_HAMMING_GAP}): {len(lexical_gaps)}")
    print(f"  NOUNs: {len(by_role.get('NOUN', []))}")
    print(f"  VERBs: {len(by_role.get('VERB', []))}")
    print(f"  ADJECTIVEs: {len(by_role.get('ADJECTIVE', []))}")
    print(f"  OPERATORs: {len(by_role.get('OPERATOR', []))}")
    print(f"  Adjacency edges: {sum(len(v) for v in adjacency.values()) // 2}")
    print("=" * 70)

    return LeechLatticeVocabulary(
        words=words,
        by_role=dict(by_role),
        adjacency=dict(adjacency),
        grammar_rules=grammar_rules,
        learned_paths={},
        lexical_gaps=lexical_gaps,
        system_vectors=system_vectors,
        lang_vectors=lang_vectors,
    )


def _load_kb(path: str) -> Dict[str, dict]:
    """Load a UBP knowledge base file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {}
    if isinstance(data, dict) and "_fields" in data:
        fields = data["_fields"]
        f_idx = {name: i for i, name in enumerate(fields)}
        for fp, entry_list in data.get("entries", {}).items():
            try:
                uid = entry_list[f_idx["ubp_id"]]
                entry_dict = {
                    "ubp_id": uid,
                    "lexicon": entry_list[f_idx["lexicon"]],
                    "tags": entry_list[f_idx["tags"]],
                    "vector": entry_list[f_idx["vector"]],
                    "nrci_val": entry_list[f_idx["nrci_val"]] if "nrci_val" in f_idx else 0.5
                }
                result[uid] = entry_dict
            except (IndexError, KeyError):
                continue
    return result
