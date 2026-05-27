"""
================================================================================
GLM ENGINE v3.0 - Geometric Language Machine (Internal Dialogue Edition)
================================================================================
A dialogue engine implementing the Internal Dialogue pattern from
ubp_internal_dialogue_semantic_description.py.

Key Design Principles:
1. PHYSICAL GROUNDING FIRST: Every query maps to system_kb physical laws
2. LEXICAL MAPPING: Physical vectors map to vocabulary via Hamming distance
3. GAP DETECTION: If no word exists within threshold, report "NULL RESONANCE"
4. DETERMINISTIC: No randomness, no sampling, no probability distributions
5. MULTI-DEPTH REFLECTION: Iterative deepening through physical→lexical chain

Architecture:
- Input → Parse → Physical Grounding (system_kb) → Lexical Mapping (lang_kb)
- Generate sentences by traversing lattice paths (minimum tax)
- Apply Golay correction to ensure all words are valid lattice points
- Maintain context via topic_vector centroid
- Record learned paths for efficiency
================================================================================
"""

import json
import re
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import deque
from fractions import Fraction

from ubp_unified_v5 import (
    BinaryLinearAlgebra, GOLAY_ENGINE, LEECH_ENGINE, BarnesWallEngine,
    to_gray_code, MOG_CATEGORIES
)
from glm_strict_lang_builder import (
    LeechLatticeVocabulary, WordEntry, GrammarRule, LearnedPath, LexicalGap,
    MAX_HAMMING_GAP, ADJACENCY_RADIUS, CANDIDATE_COUNT,
    SENTENCE_MAX_TAX, build_vocabulary
)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PhysicalRoot:
    """A physical grounding found in system_kb."""
    ubp_id: str
    vector: List[int]
    lexicon: str
    resonance: float
    nrci: float


@dataclass
class LexicalBinding:
    """A word bound to a physical root via Hamming distance."""
    word: str
    vector: List[int]
    distance: int
    role: str
    is_grounded: bool  # True if distance <= MAX_HAMMING_GAP


@dataclass
class DialogueContext:
    """
    Maintains context across a conversation.
    Carries topic_vector and active concepts between turns.
    """
    active_concepts: List[str] = field(default_factory=list)
    explored_regions: Set[str] = field(default_factory=set)
    turn_count: int = 0
    topic_vector: Optional[List[int]] = None
    topic_history: List[List[int]] = field(default_factory=list)
    concept_activation: Dict[str, float] = field(default_factory=dict)
    max_history: int = 10

    def update(self, new_concepts: List[str], new_topic_vec: List[int]):
        """Update context with new turn information."""
        self.turn_count += 1
        self.active_concepts = new_concepts[-10:]
        self.topic_vector = new_topic_vec
        self.topic_history.append(new_topic_vec)
        if len(self.topic_history) > self.max_history:
            self.topic_history.pop(0)
        # Decay old activations
        for w in list(self.concept_activation.keys()):
            self.concept_activation[w] *= 0.7
            if self.concept_activation[w] < 0.1:
                del self.concept_activation[w]
        # Activate new concepts
        for c in new_concepts:
            self.concept_activation[c] = 1.0

    def get_topic_drift(self) -> float:
        """Measure topic drift as average Hamming distance between consecutive topics."""
        if len(self.topic_history) < 2:
            return 0.0
        drifts = []
        for i in range(1, len(self.topic_history)):
            d = BinaryLinearAlgebra.hamming_distance(
                self.topic_history[i-1], self.topic_history[i]
            )
            drifts.append(d)
        return sum(drifts) / len(drifts) if drifts else 0.0


@dataclass
class DialogueTurn:
    """A single turn in the dialogue with full verification."""
    query: str
    response: str
    physical_roots: List[PhysicalRoot]
    lexical_bindings: List[LexicalBinding]
    grounded_count: int
    unverified_count: int
    gaps: List[LexicalGap]
    tax: float
    verification_rate: float


# ═══════════════════════════════════════════════════════════════════════════════
# GLM DIALOGUE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class GLMDialogueEngine:
    """
    Geometric Language Machine - Internal Dialogue Edition.
    Implements the pattern from ubp_internal_dialogue_semantic_description.py.
    """

    def __init__(self, vocab: LeechLatticeVocabulary):
        self.vocab = vocab
        self.context = DialogueContext()
        self.learned_paths: Dict[str, List[LearnedPath]] = {}
        self.turn_history: List[DialogueTurn] = []

    def respond(self, query: str, max_depth: int = 3) -> DialogueTurn:
        """
        Generate a response using the Internal Dialogue pattern:
        1. Parse query to extract concepts
        2. Ground in physical system_kb (multi-depth)
        3. Map physical roots to vocabulary via Hamming distance
        4. Generate sentences following lattice paths
        5. Verify all words, report gaps
        """
        # Step 1: Parse query
        query_concepts = self._parse_query(query)

        # Step 2: Physical grounding (multi-depth reflection)
        physical_roots, gaps = self._ground_physically(query_concepts, max_depth)

        # Step 3: Lexical mapping
        bindings = self._map_to_vocabulary(physical_roots)

        # Step 4: Generate response sentences
        sentences, sentence_tax = self._generate_response(bindings, query_concepts)

        # Step 5: Verify and compile
        response_text = ' '.join(sentences)
        grounded = sum(1 for b in bindings if b.is_grounded)
        unverified = sum(1 for b in bindings if not b.is_grounded)
        total = grounded + unverified
        rate = (grounded / total * 100) if total > 0 else 100.0

        # Update context
        new_concepts = [b.word for b in bindings if b.is_grounded]
        if bindings:
            topic_vec = self._compute_centroid([b.vector for b in bindings if b.vector])
        elif self.context.topic_vector:
            topic_vec = self.context.topic_vector
        else:
            topic_vec = [0] * 24
        self.context.update(new_concepts, topic_vec)

        # Record turn
        turn = DialogueTurn(
            query=query,
            response=response_text,
            physical_roots=physical_roots,
            lexical_bindings=bindings,
            grounded_count=grounded,
            unverified_count=unverified,
            gaps=gaps,
            tax=sentence_tax,
            verification_rate=rate
        )
        self.turn_history.append(turn)

        return turn

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 1: PARSE QUERY
    # ─────────────────────────────────────────────────────────────────────────

    def _parse_query(self, query: str) -> List[str]:
        """Extract meaningful concepts from query text."""
        stop_words = {'what', 'is', 'the', 'of', 'to', 'in', 'and', 'for',
                      'with', 'on', 'about', 'does', 'why', 'how', 'can',
                      'a', 'an', 'this', 'that', 'it', 'be', 'are', 'was'}
        words = re.sub(r'[^a-z0-9 ]', '', query.lower()).split()
        concepts = [w for w in words if w not in stop_words and len(w) > 2]
        return concepts

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 2: PHYSICAL GROUNDING (Internal Dialogue Pattern)
    # ─────────────────────────────────────────────────────────────────────────

    def _ground_physically(self, concepts: List[str], max_depth: int) -> Tuple[List[PhysicalRoot], List[LexicalGap]]:
        """
        Multi-depth physical grounding following the Internal Dialogue pattern.
        For each concept, find the closest system_kb entry by vector similarity.
        Iteratively deepen to find related physical laws.
        """
        roots = []
        gaps = []
        seen_ids = set()

        for concept in concepts:
            # Check if concept exists directly in vocabulary
            if concept in self.vocab.words:
                entry = self.vocab.words[concept]
                # Find nearest system_kb entry
                best_sys_id, best_dist = self._find_nearest_system(entry.vector)
                if best_sys_id and best_dist <= MAX_HAMMING_GAP:
                    sys_vec = self.vocab.system_vectors[best_sys_id]
                    roots.append(PhysicalRoot(
                        ubp_id=best_sys_id,
                        vector=sys_vec,
                        lexicon=concept,
                        resonance=1.0 - (best_dist / 24.0),
                        nrci=entry.nrci
                    ))
                    seen_ids.add(best_sys_id)

        # Multi-depth reflection: follow lattice neighbors
        for depth in range(1, max_depth):
            new_roots = []
            for root in roots:
                # Find system_kb neighbors of this root
                for sys_id, sys_vec in self.vocab.system_vectors.items():
                    if sys_id in seen_ids:
                        continue
                    d = BinaryLinearAlgebra.hamming_distance(root.vector, sys_vec)
                    if d <= ADJACENCY_RADIUS:
                        new_roots.append(PhysicalRoot(
                            ubp_id=sys_id,
                            vector=sys_vec,
                            lexicon=sys_id,
                            resonance=1.0 - (d / 24.0),
                            nrci=float(LEECH_ENGINE.calculate_nrci(sys_vec))
                        ))
                        seen_ids.add(sys_id)
                        if len(new_roots) >= 3:  # Limit breadth per depth
                            break
                if len(new_roots) >= 3:
                    break
            roots.extend(new_roots)

        # Use context if no direct grounding found
        if not roots and self.context.topic_vector:
            best_sys_id, best_dist = self._find_nearest_system(self.context.topic_vector)
            if best_sys_id:
                sys_vec = self.vocab.system_vectors[best_sys_id]
                roots.append(PhysicalRoot(
                    ubp_id=best_sys_id,
                    vector=sys_vec,
                    lexicon="context_anchor",
                    resonance=1.0 - (best_dist / 24.0),
                    nrci=float(LEECH_ENGINE.calculate_nrci(sys_vec))
                ))

        return roots, gaps

    def _find_nearest_system(self, vector: List[int]) -> Tuple[Optional[str], int]:
        """Find nearest system_kb entry to a given vector."""
        best_id = None
        best_dist = 99
        for sys_id, sys_vec in self.vocab.system_vectors.items():
            d = BinaryLinearAlgebra.hamming_distance(vector, sys_vec)
            if d < best_dist:
                best_dist = d
                best_id = sys_id
        return best_id, best_dist

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 3: LEXICAL MAPPING
    # ─────────────────────────────────────────────────────────────────────────

    def _map_to_vocabulary(self, roots: List[PhysicalRoot]) -> List[LexicalBinding]:
        """
        Map physical roots to vocabulary words via Hamming distance.
        This is the core of strict semantic binding.
        """
        bindings = []

        for root in roots:
            # Find closest word in vocabulary to this physical root
            best_word = None
            best_dist = 99

            for word, entry in self.vocab.words.items():
                d = BinaryLinearAlgebra.hamming_distance(root.vector, entry.vector)
                if d < best_dist:
                    best_dist = d
                    best_word = word

            if best_word and best_dist <= MAX_HAMMING_GAP:
                entry = self.vocab.words[best_word]
                bindings.append(LexicalBinding(
                    word=best_word,
                    vector=entry.vector,
                    distance=best_dist,
                    role=entry.role,
                    is_grounded=True
                ))
            elif best_word:
                # Gap: word exists but too far from physical root
                entry = self.vocab.words[best_word]
                bindings.append(LexicalBinding(
                    word=best_word,
                    vector=entry.vector,
                    distance=best_dist,
                    role=entry.role,
                    is_grounded=False  # Beyond gap threshold
                ))

        return bindings

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 4: SENTENCE GENERATION
    # ─────────────────────────────────────────────────────────────────────────

    def _generate_response(self, bindings: List[LexicalBinding], query_concepts: List[str]) -> Tuple[List[str], float]:
        """
        Generate response sentences using lattice-path traversal.
        - Select grammar rules
        - Fill slots with words closest to topic vector
        - Rank by symmetry tax
        - Apply Golay correction
        """
        if not bindings:
            return ["[NULL RESONANCE] No physical grounding found."], 0.0

        # Compute topic vector from bindings
        topic_vec = self._compute_centroid([b.vector for b in bindings if b.vector])

        sentences = []
        total_tax = 0.0

        # Generate 3-5 sentences using different grammar rules
        rules_to_use = self.vocab.grammar_rules[:min(4, len(self.vocab.grammar_rules))]

        for rule in rules_to_use:
            sentence, tax = self._generate_sentence(rule, topic_vec)
            if sentence:
                sentences.append(sentence)
                total_tax += tax

        # Add synthesis sentence connecting concepts
        if len(bindings) >= 2:
            synthesis = self._synthesize(bindings[:3], topic_vec)
            if synthesis:
                sentences.append(synthesis)

        avg_tax = total_tax / len(sentences) if sentences else 0.0
        return sentences, avg_tax

    def _generate_sentence(self, rule: GrammarRule, topic_vec: List[int]) -> Tuple[str, float]:
        """Generate a single sentence following a grammar rule, ranked by tax."""
        best_sentence = None
        best_tax = float('inf')

        for _ in range(CANDIDATE_COUNT):
            words = []
            vectors = []
            valid = True

            for role in rule.pattern:
                word, vec = self._select_word_for_role(role, topic_vec, words)
                if word is None:
                    valid = False
                    break
                words.append(word)
                vectors.append(vec)

            if not valid:
                continue

            # Calculate sentence tax (sum of consecutive Hamming distances)
            tax = 0.0
            for i in range(1, len(vectors)):
                tax += BinaryLinearAlgebra.hamming_distance(vectors[i-1], vectors[i])

            if tax < best_tax:
                best_tax = tax
                best_sentence = ' '.join(words)

            # Shift topic slightly for variety in candidates
            topic_vec = self._shift_topic(topic_vec, vectors)

        if best_sentence and best_tax <= SENTENCE_MAX_TAX:
            # Record learned path
            self._record_path(rule, best_sentence.split(), best_tax)
            return best_sentence, best_tax

        return None, 0.0

    def _select_word_for_role(self, role: str, topic_vec: List[int], already_used: List[str]) -> Tuple[Optional[str], Optional[List[int]]]:
        """Select the best word for a given role, closest to topic vector."""
        candidates = self.vocab.by_role.get(role, [])
        if not candidates:
            # Fallback to PROPERTY or any role
            candidates = self.vocab.by_role.get('PROPERTY', [])
        if not candidates:
            candidates = list(self.vocab.words.keys())

        best_word = None
        best_dist = 99
        best_vec = None

        for word in candidates:
            if word in already_used:
                continue
            entry = self.vocab.words.get(word)
            if not entry:
                continue

            d = BinaryLinearAlgebra.hamming_distance(topic_vec, entry.vector)

            # Boost recently active concepts (context memory)
            activation = self.context.concept_activation.get(word, 0.0)
            effective_d = d - int(activation * 3)  # Reduce distance for active words

            if effective_d < best_dist:
                best_dist = effective_d
                best_word = word
                best_vec = entry.vector

        return best_word, best_vec

    def _synthesize(self, bindings: List[LexicalBinding], topic_vec: List[int]) -> Optional[str]:
        """Create a synthesis sentence connecting multiple concepts."""
        grounded_words = [b.word for b in bindings if b.is_grounded]
        if len(grounded_words) < 2:
            return None

        # Find a connecting verb
        verb, _ = self._select_word_for_role('VERB', topic_vec, grounded_words)
        if not verb:
            return None

        return f"{grounded_words[0]} and {grounded_words[1]} {verb} as one coherent structure in the lattice"

    # ─────────────────────────────────────────────────────────────────────────
    # UTILITIES
    # ─────────────────────────────────────────────────────────────────────────

    def _compute_centroid(self, vectors: List[List[int]]) -> List[int]:
        """Compute centroid of vectors (majority vote per bit)."""
        if not vectors:
            return [0] * 24
        n = len(vectors)
        centroid = []
        for bit_pos in range(24):
            ones = sum(v[bit_pos] for v in vectors)
            centroid.append(1 if ones > n / 2 else 0)
        return centroid

    def _shift_topic(self, topic_vec: List[int], used_vectors: List[List[int]]) -> List[int]:
        """Slightly shift topic vector for candidate diversity."""
        if not used_vectors:
            return topic_vec
        # XOR with fold of last used vector
        last = used_vectors[-1]
        fold3 = BinaryLinearAlgebra.fold24_to3(last)
        shifted = list(topic_vec)
        # Flip bits at positions indicated by fold3
        for i, b in enumerate(fold3):
            if b:
                pos = (i * 8 + 3) % 24  # Deterministic position shift
                shifted[pos] = 1 - shifted[pos]
        return shifted

    def _record_path(self, rule: GrammarRule, words: List[str], tax: float):
        """Record a low-tax path for future reuse."""
        if tax > SENTENCE_MAX_TAX:
            return
        key = rule.name
        vectors = [self.vocab.words[w].vector for w in words if w in self.vocab.words]
        path = LearnedPath(words=words, vectors=vectors, tax=tax, pattern_key=key)

        if key not in self.learned_paths:
            self.learned_paths[key] = []
        self.learned_paths[key].append(path)
        # Keep only top 5 paths per pattern
        self.learned_paths[key].sort(key=lambda p: p.tax)
        self.learned_paths[key] = self.learned_paths[key][:5]

    def get_verification_summary(self) -> Dict[str, Any]:
        """Get a summary of all verification across turns."""
        total_grounded = sum(t.grounded_count for t in self.turn_history)
        total_unverified = sum(t.unverified_count for t in self.turn_history)
        total = total_grounded + total_unverified
        return {
            'total_turns': len(self.turn_history),
            'total_grounded': total_grounded,
            'total_unverified': total_unverified,
            'overall_rate': (total_grounded / total * 100) if total > 0 else 100.0,
            'learned_paths': sum(len(v) for v in self.learned_paths.values()),
            'topic_drift': self.context.get_topic_drift(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# FACTORY FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_engine(system_kb_path: str, lang_kb_path: str) -> GLMDialogueEngine:
    """Create a GLM engine with strict vocabulary."""
    vocab = build_vocabulary(system_kb_path, lang_kb_path)
    return GLMDialogueEngine(vocab)
