"""
================================================================================
UBP BRAIN CONSOLIDATED v5.2 — N-GRAM NAME MATCHING
================================================================================
Author: E R A Craig, New Zealand
Date: 26 March 2026
Version: 5.2.1

ARCHITECTURE:
  The UBP Brain is a deterministic recall engine that maps natural language
  queries to entries in the UBP Knowledge Base (ubp_system_kb.json).

  The core mechanism is:
  1. **N-Gram Query Tokenization:** The query is first scanned for bigram and
     trigram matches against the KB's name index (e.g., "up quark", "W boson",
     "speed of light"). Matched n-grams are consumed as single tokens.
     Remaining unmatched words are processed as unigrams.
  2. **Token Vector Lookup:** Each token/n-gram is matched against the KB's
     `short_name_index` (primary match) or `lexicon_index` (secondary match).
  3. **Query Vector Generation:** The token vectors are averaged to produce
     a 24-bit query vector.
  4. **Memory Scoring:** The query vector is compared against all KB entry
     vectors using bipolar dot product similarity.
  5. **Confidence Calculation:** The confidence is based on how much the
     top candidate stands out from the rest, boosted by multi-token
     corroboration.

CHANGE LOG (v5.2 vs v5.1):
  - **[FEATURE] N-Gram Name Matching:** The query tokenizer now first scans
    for bigram and trigram matches in the short_name_index before falling back
    to unigram matching. This fixes failures for multi-word names like
    "up quark", "W boson", "speed of light", "fine structure constant",
    "nuclear fusion", "cellular respiration", "sodium hydroxide", etc.
  - **[FEATURE] Phrase-Level Direct Match Boost:** When an n-gram directly
    matches a KB entry, the corroboration count is boosted proportionally
    to the n-gram length (bigram=2, trigram=3), giving higher confidence.
  - **[FIX] Acid/Hydroxide Matching:** The lexicon index now correctly
    prioritises entries where the full compound name matches, not just
    individual words like "acid" or "hydroxide".
  - **[FIX] Null Resonance threshold:** Lowered to 0.08 to allow more
    results to be returned for lower-confidence matches.

================================================================================
"""

import json
import hashlib
import os
import re
import sys
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any, Set
from collections import defaultdict
from datetime import datetime
import math

# --- UBP Core Foundation ---
try:
    if os.path.exists('ubp_core_v5_3_merged.py'):
        sys.path.insert(0, 'core')
    from ubp_core_v5_3_merged import GOLAY_ENGINE
    CORE_AVAILABLE = True
    print('[UBP Brain v5.2] UBP Core v5.3 FOUND — Full Golay/Leech functionality enabled')
except ImportError as _e:
    CORE_AVAILABLE = False
    GOLAY_ENGINE = None
    print(f'[WARNING] UBP Core not found ({_e}). Running in fallback mode.')

# ==============================================================================
# SECTION 1: HELPERS
# ==============================================================================

def extract_vector(entry: Dict) -> Optional[List[int]]:
    """Extract the 24-bit vector from an entry's atlas field."""
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        v = atlas.get('vector')
        if isinstance(v, list) and len(v) == 24:
            return v
    return None

def extract_nrci(entry: Dict) -> Fraction:
    """Extract the NRCI score from an entry's atlas field."""
    atlas = entry.get('atlas', {})
    if isinstance(atlas, dict):
        nrci_str = atlas.get('nrci', '')
        if isinstance(nrci_str, str) and '/' in nrci_str:
            try:
                n, d = nrci_str.split('/')
                return Fraction(int(n), int(d))
            except: pass
        score = atlas.get('nrci_score')
        if score is not None:
            return Fraction(score).limit_denominator(1000000)
    return Fraction(1, 1)

def extract_name(entry: Dict) -> str:
    """
    Extract the primary name from an entry's lexicon field.
    Handles formats: '[Type: Name (Symbol)]', '[Type: Name]', '[Name]', 'Name'.
    Strips parenthetical symbols like '(H)', '(C)', etc.
    """
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        match = re.match(r'^\[\s*([^\]]+?)\s*\]', lexicon)
        if match:
            content = match.group(1).strip()
            if ':' in content:
                name = content.split(':', 1)[1].strip()
                name = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip()
                return name
            else:
                name = re.sub(r'\s*\([^)]*\)\s*$', '', content).strip()
                return name
    uid = entry.get('ubp_id', 'Unknown')
    return uid.replace('_', ' ').title()

def extract_description(entry: Dict) -> str:
    """Extract the description from an entry's lexicon field."""
    lexicon = entry.get('lexicon', '')
    if isinstance(lexicon, str):
        parts = re.findall(r'\[([^\]]+)\]', lexicon)
        if len(parts) >= 2:
            return parts[1].strip()
        match = re.match(r'^\s*\[([^\]]+)\],?\s*(.*)\s*$', lexicon, re.DOTALL)
        if match:
            return match.groups()[1].strip()
    return lexicon

def is_belief(entry: Dict) -> bool:
    """Check if an entry is a belief/law entry."""
    uid = entry.get('ubp_id', '')
    return uid.startswith(('LAW_', 'BELIEF_', 'AXIOM_', 'IMPERATIVE_'))

def is_understanding(entry: Dict) -> bool:
    """Check if an entry is an understanding entry (physical object)."""
    uid = entry.get('ubp_id', '')
    return uid.startswith(('ELEM_', 'MOLECULE_', 'PARTICLE_', 'CRYSTAL_', 'REACTION_', 'TOOL_', 'MATH_', 'ALGO_'))

def extract_tax(entry: Dict) -> Fraction:
    """Extract the TAX value from an entry."""
    tax = entry.get('tax', 0)
    if isinstance(tax, (int, float)):
        return Fraction(tax).limit_denominator(1000000)
    if isinstance(tax, str):
        try:
            return Fraction(tax).limit_denominator(1000000)
        except: pass
    return Fraction(0)

# ==============================================================================
# SECTION 2: KB MANAGER
# ==============================================================================

class KBManager:
    """Manages the UBP Knowledge Base."""

    def __init__(self):
        self.kb: Dict[str, Dict] = {}
        self.lexicon_index: Dict[str, List[str]] = defaultdict(list)
        self.short_name_index: Dict[str, str] = {}
        # N-gram indexes: bigram_index['up quark'] = uid, trigram_index['speed of light'] = uid
        self.bigram_index: Dict[str, str] = {}
        self.trigram_index: Dict[str, str] = {}
        self.stats: Dict[str, int] = {}

    def load(self, paths: List[str]) -> int:
        """Load KB from one or more JSON files."""
        for path in paths:
            if not os.path.exists(path):
                print(f'[WARNING] KB file not found: {path}')
                continue
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for key, entry in data.items():
                        if isinstance(entry, dict) and 'ubp_id' in entry:
                            self.kb[entry['ubp_id']] = entry
        self._build_indexes()
        return len(self.kb)

    UNDERSTANDING_PREFIXES_SET = ('ELEM_', 'MOLECULE_', 'PARTICLE_', 'CRYSTAL_', 'REACTION_', 'TOOL_', 'MATH_', 'ALGO_')

    def _build_indexes(self):
        """Build the short_name_index, bigram_index, trigram_index, and lexicon_index.

        N-gram indexes are ONLY built from UNDERSTANDING entries (not LAW/BELIEF entries)
        to prevent law names from polluting multi-word query matching.
        """
        for uid, entry in self.kb.items():
            is_understanding_uid = uid.startswith(self.UNDERSTANDING_PREFIXES_SET)

            # Primary name index
            name = extract_name(entry).lower()
            if name and name not in ('unknown', uid.lower()):
                self.short_name_index[name] = uid

                # Build n-gram indexes ONLY from understanding entries
                if is_understanding_uid:
                    words = name.split()
                    if len(words) >= 2:
                        for i in range(len(words) - 1):
                            bigram = f'{words[i]} {words[i+1]}'
                            if bigram not in self.bigram_index:
                                self.bigram_index[bigram] = uid
                    if len(words) >= 3:
                        for i in range(len(words) - 2):
                            trigram = f'{words[i]} {words[i+1]} {words[i+2]}'
                            if trigram not in self.trigram_index:
                                self.trigram_index[trigram] = uid

            # Also index chemical symbols from lexicon like '(H)', '(C)', '(O)'
            lexicon = entry.get('lexicon', '')
            if isinstance(lexicon, str):
                # Extract symbol from '[Type: Name (Symbol)]' format
                sym_match = re.search(r'\(([A-Z][a-z]?)\)', lexicon)
                if sym_match:
                    sym = sym_match.group(1).lower()
                    if sym not in self.short_name_index:
                        self.short_name_index[sym] = uid
                # Extract all words from the first bracket as aliases (UNDERSTANDING only)
                if is_understanding_uid:
                    first_bracket = re.match(r'^\[([^\]]+)\]', lexicon)
                    if first_bracket:
                        content = first_bracket.group(1)
                        for word in re.findall(r'\b[a-zA-Z]{3,}\b', content):
                            word_lower = word.lower()
                            if word_lower not in self.short_name_index and word_lower not in (
                                'element', 'molecule', 'particle', 'crystal', 'reaction',
                                'law', 'tool', 'math', 'algo', 'geo', 'belief', 'axiom'
                            ):
                                self.short_name_index[word_lower] = uid

        # Explicit aliases for entries with non-standard or abbreviated names
        if 'PARTICLE_W_BOSON_PLUS_001' in self.kb:
            self.bigram_index['w boson'] = 'PARTICLE_W_BOSON_PLUS_001'
            self.short_name_index['w+'] = 'PARTICLE_W_BOSON_PLUS_001'
        if 'PARTICLE_W_BOSON_MINUS_001' in self.kb:
            self.short_name_index['w-'] = 'PARTICLE_W_BOSON_MINUS_001'
        if 'REACTION_HABER_BOSCH_001' in self.kb:
            self.bigram_index['haber process'] = 'REACTION_HABER_BOSCH_001'
            self.bigram_index['haber bosch'] = 'REACTION_HABER_BOSCH_001'
        if 'MOLECULE_WATER_001' in self.kb:
            self.short_name_index['h2o'] = 'MOLECULE_WATER_001'
        if 'MOLECULE_GLUCOSE_001' in self.kb:
            self.short_name_index['c6h12o6'] = 'MOLECULE_GLUCOSE_001'
            self.short_name_index['dextrose'] = 'MOLECULE_GLUCOSE_001'
        if 'MOLECULE_AMMONIA_001' in self.kb:
            self.short_name_index['nh3'] = 'MOLECULE_AMMONIA_001'
        if 'MATH_PLANCK_CONSTANT_001' in self.kb:
            self.short_name_index['planck'] = 'MATH_PLANCK_CONSTANT_001'
            self.bigram_index['planck constant'] = 'MATH_PLANCK_CONSTANT_001'
        if 'MATH_FINE_STRUCTURE_CONSTANT_001' in self.kb:
            self.trigram_index['fine structure constant'] = 'MATH_FINE_STRUCTURE_CONSTANT_001'
            self.bigram_index['fine structure'] = 'MATH_FINE_STRUCTURE_CONSTANT_001'
            self.short_name_index['alpha'] = 'MATH_FINE_STRUCTURE_CONSTANT_001'
        if 'MATH_GRAVITATIONAL_CONSTANT_001' in self.kb:
            self.bigram_index['gravitational constant'] = 'MATH_GRAVITATIONAL_CONSTANT_001'
        if 'MATH_BOLTZMANN_CONSTANT_001' in self.kb:
            self.bigram_index['boltzmann constant'] = 'MATH_BOLTZMANN_CONSTANT_001'
        if 'MATH_AVOGADRO_CONSTANT_001' in self.kb:
            self.bigram_index['avogadro constant'] = 'MATH_AVOGADRO_CONSTANT_001'
        if 'MATH_SPEED_OF_LIGHT_001' in self.kb:
            self.trigram_index['speed of light'] = 'MATH_SPEED_OF_LIGHT_001'
            self.short_name_index['lightspeed'] = 'MATH_SPEED_OF_LIGHT_001'
        if 'PARTICLE_HIGGS_BOSON_001' in self.kb:
            self.bigram_index['higgs boson'] = 'PARTICLE_HIGGS_BOSON_001'
            self.short_name_index['higgs'] = 'PARTICLE_HIGGS_BOSON_001'
        if 'PARTICLE_ALPHA_001' in self.kb:
            self.bigram_index['alpha particle'] = 'PARTICLE_ALPHA_001'
        if 'REACTION_NUCLEAR_FUSION_DT_001' in self.kb:
            self.bigram_index['nuclear fusion'] = 'REACTION_NUCLEAR_FUSION_DT_001'
        if 'REACTION_NUCLEAR_FISSION_U235_001' in self.kb:
            self.bigram_index['nuclear fission'] = 'REACTION_NUCLEAR_FISSION_U235_001'
        # British/American spelling aliases
        if 'ELEM_Al_013' in self.kb:
            self.short_name_index['aluminium'] = 'ELEM_Al_013'
            self.short_name_index['aluminum'] = 'ELEM_Al_013'
        if 'ELEM_S_016' in self.kb:
            self.short_name_index['sulphur'] = 'ELEM_S_016'
            self.short_name_index['sulfur'] = 'ELEM_S_016'
        if 'MOLECULE_SULFURIC_ACID_001' in self.kb:
            self.bigram_index['sulphuric acid'] = 'MOLECULE_SULFURIC_ACID_001'
        # Additional common aliases
        if 'ELEM_Fe_026' in self.kb:
            self.short_name_index['fe'] = 'ELEM_Fe_026'
            self.short_name_index['ferrum'] = 'ELEM_Fe_026'
        if 'ELEM_Au_079' in self.kb:
            self.short_name_index['aurum'] = 'ELEM_Au_079'
        if 'ELEM_Na_011' in self.kb:
            self.short_name_index['natrium'] = 'ELEM_Na_011'
        if 'ELEM_K_019' in self.kb:
            self.short_name_index['kalium'] = 'ELEM_K_019'
        if 'ELEM_Ag_047' in self.kb:
            self.short_name_index['argentum'] = 'ELEM_Ag_047'
            self.short_name_index['silver'] = 'ELEM_Ag_047'
        if 'MOLECULE_CARBON_DIOXIDE_001' in self.kb:
            self.short_name_index['co2'] = 'MOLECULE_CARBON_DIOXIDE_001'
        if 'MOLECULE_METHANE_001' in self.kb:
            self.short_name_index['ch4'] = 'MOLECULE_METHANE_001'
        if 'MOLECULE_ETHANOL_001' in self.kb:
            self.short_name_index['ethyl'] = 'MOLECULE_ETHANOL_001'
        if 'PARTICLE_ELECTRON_001' in self.kb:
            self.short_name_index['electrons'] = 'PARTICLE_ELECTRON_001'
        if 'PARTICLE_PROTON_001' in self.kb:
            self.short_name_index['protons'] = 'PARTICLE_PROTON_001'
        if 'PARTICLE_NEUTRON_001' in self.kb:
            self.short_name_index['neutrons'] = 'PARTICLE_NEUTRON_001' 

            # Lexicon index (all words in name + description)
            desc = extract_description(entry).lower()
            full_text = name + ' ' + desc
            for word in re.findall(r'\b\w{3,}\b', full_text):
                if word not in self.lexicon_index or uid not in self.lexicon_index[word]:
                    self.lexicon_index[word].append(uid)

            self.polar_index = []
        for uid, entry in self.kb.items():
            vec = extract_vector(entry)
            if not vec: continue
            atlas = entry.get('atlas', {})
            # Convert rational tax string to float for fast filtering
            tax_str = atlas.get('tax', '0/1')
            tax_val = float(Fraction(tax_str))
            tilt_val = float(atlas.get('tilt', 0.0))
            self.polar_index.append({
                'uid': uid, 'vec': vec, 'tax': tax_val, 'tilt': tilt_val
            })

        self.stats = {
            'total_entries': len(self.kb),
            'indexed_names': len(self.short_name_index),
            'bigrams': len(self.bigram_index),
            'trigrams': len(self.trigram_index),
            'lexicon_terms': len(self.lexicon_index),
        }

# ==============================================================================
# SECTION 3: MAIN BRAIN & QUERY PROCESSOR
# ==============================================================================

@dataclass
class ReasoningResult:
    """Result of a brain query."""
    response: str
    ubp_id: Optional[str] = None
    confidence: float = 0.0
    layer: str = 'none'
    top_candidates: List[Tuple[str, float]] = field(default_factory=list)
    coherence_snap: bool = False

class UBPBrain:
    """The UBP Brain — a deterministic recall engine."""

    STOP_WORDS = {
        'what', 'is', 'the', 'a', 'an', 'of', 'to', 'in', 'and', 'for',
        'with', 'on', 'about', 'explain', 'tell', 'me', 'purpose', 'how',
        'does', 'work', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
        'it', 'its', 'at', 'by', 'from', 'out', 'or', 'but', 'not',
        # NOTE: 'w' and 'z' are NOT stop words — they are boson names
        'so', 'if', 'as', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'each', 'more', 'most', 'other',
        'some', 'such', 'no', 'only', 'same', 'than', 'too', 'very',
        'just', 'because', 'while', 'although', 'since', 'until', 'unless',
        'however', 'therefore', 'thus', 'hence', 'also', 'both', 'either',
        'neither', 'whether', 'which', 'who', 'whom', 'whose', 'when',
        'where', 'why', 'all', 'any', 'few', 'many', 'much', 'several',
        'every', 'own', 'same', 'then', 'there', 'their', 'they', 'them',
        'he', 'she', 'we', 'you', 'my', 'your', 'his', 'her', 'our', 'its',
    }

    # Note: 'up', 'down' removed from stop words — they are quark names
    UNDERSTANDING_PREFIXES = ('ELEM_', 'MOLECULE_', 'PARTICLE_', 'CRYSTAL_', 'REACTION_', 'TOOL_', 'MATH_', 'ALGO_')

    def __init__(self):
        self.kb_manager = KBManager()
        self.initialized = False

    def initialize(self, kb_paths: List[str]):
        """Initialize the brain with KB files."""
        count = self.kb_manager.load(kb_paths)
        if count > 0:
            self.initialized = True
            print(f'[UBP Brain v5.2] Initialized with {count} KB entries')
            print(f'  Indexed names: {self.kb_manager.stats.get("indexed_names", 0)}')
            print(f'  Bigrams: {self.kb_manager.stats.get("bigrams", 0)}')
            print(f'  Trigrams: {self.kb_manager.stats.get("trigrams", 0)}')
            print(f'  Lexicon terms: {self.kb_manager.stats.get("lexicon_terms", 0)}')

    def _get_token_vector(self, token: str) -> Tuple[Optional[List[float]], Optional[str]]:
        """
        Get the vector for a token.
        Priority: Primary name match > Lexicon match.
        Returns (vector, direct_uid) where direct_uid is set if the token
        directly matched a KB entry by name.
        """
        kb = self.kb_manager.kb

        # --- PRIMARY MATCH BOOST ---
        if token in self.kb_manager.short_name_index:
            uid = self.kb_manager.short_name_index[token]
            vec = extract_vector(kb[uid])
            if vec:
                return [float(b) for b in vec], uid

        # --- LEXICON SEARCH (Fallback) ---
        if token in self.kb_manager.lexicon_index:
            all_uids = self.kb_manager.lexicon_index[token]
            understanding_uids = [uid for uid in all_uids if uid.startswith(self.UNDERSTANDING_PREFIXES)]
            uids_to_use = understanding_uids if understanding_uids else all_uids

            weighted_vectors = []
            total_weight = 0.0
            for uid in uids_to_use[:5]:
                entry = kb.get(uid)
                if not entry:
                    continue
                vec = extract_vector(entry)
                if vec:
                    nrci = float(extract_nrci(entry))
                    weight = max(0.01, (nrci - 0.5) * 2)
                    weighted_vectors.append(([float(b) * weight for b in vec], weight))
                    total_weight += weight

            if not weighted_vectors:
                return None, None

            avg_vector = [0.0] * 24
            for vec, weight in weighted_vectors:
                for i in range(24):
                    avg_vector[i] += vec[i]

            return [v / total_weight for v in avg_vector] if total_weight > 0 else None, None

        return None, None

    def _tokenize_with_ngrams(self, query: str) -> List[Dict]:
        """
        Tokenize a query, first scanning for trigram and bigram matches,
        then falling back to unigrams.

        Returns a list of token dicts with 'word', 'vector', 'direct_uid', 'ngram_size'.
        """
        query_lower = query.lower()
        raw_words = re.sub(r'[^a-zA-Z0-9\s]', '', query_lower).split()

        tokens = []
        direct_matches: Dict[str, int] = defaultdict(int)
        i = 0

        while i < len(raw_words):
            word = raw_words[i]

            # --- Try trigram first (3 words) ---
            if i + 2 < len(raw_words):
                trigram = f'{raw_words[i]} {raw_words[i+1]} {raw_words[i+2]}'
                if trigram in self.kb_manager.trigram_index:
                    uid = self.kb_manager.trigram_index[trigram]
                    vec = extract_vector(self.kb_manager.kb[uid])
                    if vec:
                        tokens.append({'word': trigram, 'vector': [float(b) for b in vec],
                                       'direct_uid': uid, 'ngram_size': 3})
                        direct_matches[uid] += 3  # trigram = 3x corroboration
                        i += 3
                        continue

            # --- Try bigram (2 words) ---
            if i + 1 < len(raw_words):
                bigram = f'{raw_words[i]} {raw_words[i+1]}'
                if bigram in self.kb_manager.bigram_index:
                    uid = self.kb_manager.bigram_index[bigram]
                    vec = extract_vector(self.kb_manager.kb[uid])
                    if vec:
                        tokens.append({'word': bigram, 'vector': [float(b) for b in vec],
                                       'direct_uid': uid, 'ngram_size': 2})
                        direct_matches[uid] += 2  # bigram = 2x corroboration
                        i += 2
                        continue

            # --- Unigram ---
            if word not in self.STOP_WORDS and len(word) > 1:
                vector, direct_uid = self._get_token_vector(word)
                if vector:
                    tokens.append({'word': word, 'vector': vector,
                                   'direct_uid': direct_uid, 'ngram_size': 1})
                    if direct_uid:
                        direct_matches[direct_uid] += 1
            i += 1

        return tokens, direct_matches

    def process_query(self, query: str, debug: bool = False) -> ReasoningResult:
        if not self.initialized:
            return ReasoningResult('Brain not initialized.')

        # 1. Tokenize with n-gram support
        tokens, direct_matches = self._tokenize_with_ngrams(query)

        # Fallback: if no tokens found, try the last word
        if not tokens:
            query_lower = query.lower()
            raw_words = re.sub(r'[^a-zA-Z0-9\s]', '', query_lower).split()
            for word in reversed(raw_words):
                vector, direct_uid = self._get_token_vector(word)
                if vector:
                    tokens.append({'word': word, 'vector': vector,
                                   'direct_uid': direct_uid, 'ngram_size': 1})
                    if direct_uid:
                        direct_matches[direct_uid] += 1
                    break

        if not tokens:
            return ReasoningResult('**[Null Resonance]** Query could not be understood.', confidence=0.0)

        # 2. Generate Query Vector (Average)
        query_vector = [0.0] * 24
        for t in tokens:
            for i in range(24):
                query_vector[i] += t['vector'][i]
        query_vector = [v / len(tokens) for v in query_vector]

        # 3. FULL SCAN SCORING (Restored Original Logic)
        memory_scores = []
        for uid, entry in self.kb_manager.kb.items():
            mem_vec = extract_vector(entry)
            if mem_vec is None:
                continue

            # Bipolar dot product similarity
            qv_bipolar = [(v * 2) - 1 for v in query_vector]
            mv_bipolar = [(v * 2) - 1 for v in mem_vec]
            similarity = sum(q * m for q, m in zip(qv_bipolar, mv_bipolar)) / 24.0

            # Domain-aware scoring: understanding entries get a boost
            is_understanding_entry = uid.startswith(self.UNDERSTANDING_PREFIXES)
            domain_multiplier = 1.5 if is_understanding_entry else 0.75

            score = (similarity + 1.0) * domain_multiplier
            memory_scores.append((uid, score))

        if not memory_scores:
            return ReasoningResult('Lattice search failed.')

        sorted_scores = sorted(memory_scores, key=lambda x: x[1], reverse=True)
        top_candidate_uid, top_score = sorted_scores[0]

        # 4. DIRECT MATCH OVERRIDE
        if direct_matches and top_candidate_uid not in direct_matches:
            best_direct_uid = max(direct_matches, key=lambda uid: direct_matches[uid])
            direct_score = next((s for u, s in sorted_scores if u == best_direct_uid), 0)
            if direct_score >= top_score * 0.95:
                top_candidate_uid = best_direct_uid
                top_score = direct_score
                sorted_scores = [(u, s) for u, s in sorted_scores if u != best_direct_uid]
                sorted_scores.insert(0, (best_direct_uid, direct_score))

        # 5. CONFIDENCE CALCULATION
        confidence = 0.0
        if len(sorted_scores) > 1:
            avg_next_4 = sum(s[1] for s in sorted_scores[1:5]) / 4
            standout = 1.0 - (avg_next_4 / top_score) if top_score > 0 else 0
            top_nrci = float(extract_nrci(self.kb_manager.kb[top_candidate_uid]))
            
            corroboration_count = direct_matches.get(top_candidate_uid, 0)
            total_ngram_weight = sum(t.get('ngram_size', 1) for t in tokens)
            corroboration_boost = 1.0 + (corroboration_count / total_ngram_weight if total_ngram_weight > 0 else 0)
            
            confidence = min(1.0, standout * top_nrci * corroboration_boost)

        # 6. RESPONSE GENERATION
        top_entry = self.kb_manager.kb[top_candidate_uid]
        response_text = (
            f'**{extract_name(top_entry)}** ({top_candidate_uid})\n'
            f'{extract_description(top_entry)}\n'
            f'---\n'
            f'NRCI: {float(extract_nrci(top_entry)):.4f} | Confidence: {confidence:.2%}'
        )

        return ReasoningResult(response=response_text, ubp_id=top_candidate_uid, 
                               confidence=confidence, top_candidates=sorted_scores[:5])

        # --- STAGE 2: HAMMING RE-RANK ---
        memory_scores = []
        for cand in candidates:
            uid = cand['uid']
            mem_vec = cand['vec']
            
            # Bipolar dot product similarity
            qv_bipolar = [(v * 2) - 1 for v in query_vector]
            mv_bipolar = [(v * 2) - 1 for v in mem_vec]
            similarity = sum(q * m for q, m in zip(qv_bipolar, mv_bipolar)) / 24.0

            is_understanding_entry = uid.startswith(self.UNDERSTANDING_PREFIXES)
            domain_multiplier = 1.5 if is_understanding_entry else 0.75

            score = (similarity + 1.0) * domain_multiplier
            memory_scores.append((uid, score))

        if not memory_scores:
            return ReasoningResult('Lattice search failed.')

        sorted_scores = sorted(memory_scores, key=lambda x: x[1], reverse=True)
        top_candidate_uid, top_score = sorted_scores[0]

        # --- DIRECT MATCH OVERRIDE (Keep existing logic) ---
        if direct_matches and top_candidate_uid not in direct_matches:
            best_direct_uid = max(direct_matches, key=lambda uid: direct_matches[uid])
            direct_score = next((s for u, s in sorted_scores if u == best_direct_uid), 0)
            if direct_score >= top_score * 0.95:
                top_candidate_uid = best_direct_uid
                top_score = direct_score
                sorted_scores = [(u, s) for u, s in sorted_scores if u != best_direct_uid]
                sorted_scores.insert(0, (best_direct_uid, direct_score))

        # --- CONFIDENCE & RESPONSE (Keep existing logic) ---
        confidence = 0.0
        if len(sorted_scores) > 1:
            avg_next_4 = sum(s[1] for s in sorted_scores[1:5]) / 4
            standout = 1.0 - (avg_next_4 / top_score) if top_score > 0 else 0
            top_nrci = float(extract_nrci(self.kb_manager.kb[top_candidate_uid]))
            
            corroboration_count = direct_matches.get(top_candidate_uid, 0)
            total_ngram_weight = sum(t.get('ngram_size', 1) for t in tokens)
            corroboration_boost = 1.0 + (corroboration_count / total_ngram_weight if total_ngram_weight > 0 else 0)
            
            confidence = min(1.0, standout * top_nrci * corroboration_boost)

        top_entry = self.kb_manager.kb[top_candidate_uid]
        response_text = (
            f'**{extract_name(top_entry)}** ({top_candidate_uid})\n'
            f'{extract_description(top_entry)}\n'
            f'---\n'
            f'NRCI: {float(extract_nrci(top_entry)):.4f} | Confidence: {confidence:.2%}'
        )

        return ReasoningResult(response=response_text, ubp_id=top_candidate_uid, 
                               confidence=confidence, top_candidates=sorted_scores[:5])

        if debug:
            print(f'  [Debug] Tokens: {[t["word"] for t in tokens]}')
            if direct_matches:
                print(f'  [Debug] Direct matches: {dict(direct_matches)}')

        # Generate query vector (average of token vectors)
        query_vector = [0.0] * 24
        for t in tokens:
            for i in range(24):
                query_vector[i] += t['vector'][i]
        query_vector = [v / len(tokens) for v in query_vector]

        # --- NEW: STAGE 1 - POLAR FILTER (The Glance) ---
        # Estimate query tax/radius for filtering
        q_tax = (sum(query_vector) * 0.264675) + (sum(v*v for v in query_vector) / 8.0)
        
        def get_polar_dist(cand):
            # Law of Cosines distance in 2D Polar Space
            r1, t1 = q_tax, math.radians(90.0) # Assume median tilt for query
            r2, t2 = cand['tax'], math.radians(cand['tilt'])
            return math.sqrt(max(0, r1**2 + r2**2 - 2 * r1 * r2 * math.cos(t1 - t2)))

        # Narrow down to top 64 candidates based on Energy (Tax) and Orientation (Tilt)
        candidates = sorted(self.kb_manager.polar_index, key=get_polar_dist)[:64]

        # --- STAGE 2 - HAMMING RE-RANK (The Focus) ---
        memory_scores = []
        for cand in candidates:
            uid = cand['uid']
            mem_vec = cand['vec']
            # (The rest of your existing scoring logic continues here...)
            qv_bipolar = [(v * 2) - 1 for v in query_vector]
            mv_bipolar = [(v * 2) - 1 for v in mem_vec]
            similarity = sum(q * m for q, m in zip(qv_bipolar, mv_bipolar)) / 24.0

            is_understanding_entry = uid.startswith(self.UNDERSTANDING_PREFIXES)
            domain_multiplier = 1.5 if is_understanding_entry else 0.75

            score = (similarity + 1.0) * domain_multiplier
            memory_scores.append((uid, score))

            # Bipolar dot product similarity
            qv_bipolar = [(v * 2) - 1 for v in query_vector]
            mv_bipolar = [(v * 2) - 1 for v in mem_vec]
            similarity = sum(q * m for q, m in zip(qv_bipolar, mv_bipolar)) / 24.0

            # Domain-aware scoring: understanding entries get a boost
            is_understanding_entry = uid.startswith(self.UNDERSTANDING_PREFIXES)
            domain_multiplier = 1.5 if is_understanding_entry else 0.75

            score = (similarity + 1.0) * domain_multiplier
            memory_scores.append((uid, score))

        if not memory_scores:
            return ReasoningResult('KB is empty or has no vectors.')

        sorted_scores = sorted(memory_scores, key=lambda x: x[1], reverse=True)
        top_candidate_uid, top_score = sorted_scores[0]

        # --- DIRECT MATCH OVERRIDE ---
        # If the top candidate was NOT directly matched by any token, but there IS
        # a direct match candidate with the same or very similar score, prefer the
        # direct match. This handles vector collisions where two entries share the
        # same Golay codeword (e.g., glucose and ALGO_015).
        if direct_matches and top_candidate_uid not in direct_matches:
            best_direct_uid = max(direct_matches, key=lambda uid: direct_matches[uid])
            # Find the score of the best direct match
            direct_score = next((s for u, s in sorted_scores if u == best_direct_uid), 0)
            # If the direct match is within 5% of the top score, prefer it
            if direct_score >= top_score * 0.95:
                top_candidate_uid = best_direct_uid
                top_score = direct_score
                # Move the direct match to the front of sorted_scores for response building
                sorted_scores = [(u, s) for u, s in sorted_scores if u != best_direct_uid]
                sorted_scores.insert(0, (best_direct_uid, direct_score))

        if debug:
            print('  [Debug] Top 5 Scores:')
            for uid, score in sorted_scores[:5]:
                print(f'    - {uid}: {score:.4f}')

        # --- CONFIDENCE CALCULATION (v5.2 IMPROVED) ---
        confidence = 0.0
        coherence_snap = False

        if len(sorted_scores) > 1:
            next_4_scores = [s[1] for s in sorted_scores[1:5]]
            avg_next_4 = sum(next_4_scores) / len(next_4_scores) if next_4_scores else 0

            if top_score > 0.001:
                # Base standout factor
                standout_factor = 1.0 - (avg_next_4 / top_score)

                # NRCI of top candidate
                top_nrci = float(extract_nrci(self.kb_manager.kb[top_candidate_uid]))

                # Base confidence
                base_confidence = max(0.0, standout_factor) * top_nrci

                # --- MULTI-TOKEN CORROBORATION BOOST ---
                # If the top candidate was directly matched by multiple tokens (or n-grams),
                # boost the confidence proportionally.
                corroboration_count = direct_matches.get(top_candidate_uid, 0)
                total_tokens = len(tokens)
                # Weight total tokens by their ngram sizes for fair comparison
                total_ngram_weight = sum(t.get('ngram_size', 1) for t in tokens)

                if corroboration_count > 0 and total_ngram_weight > 0:
                    # Corroboration ratio: fraction of token weight that directly matched
                    corroboration_ratio = corroboration_count / total_ngram_weight
                    # Boost: up to 2x for full corroboration (all tokens match)
                    corroboration_boost = 1.0 + corroboration_ratio
                    confidence = min(1.0, base_confidence * corroboration_boost)
                else:
                    confidence = base_confidence

                # --- NRCI GAP BOOST ---
                next_4_nrci = []
                for uid, _ in sorted_scores[1:5]:
                    entry = self.kb_manager.kb.get(uid)
                    if entry:
                        next_4_nrci.append(float(extract_nrci(entry)))
                if next_4_nrci:
                    avg_next_4_nrci = sum(next_4_nrci) / len(next_4_nrci)
                    nrci_gap = top_nrci - avg_next_4_nrci
                    if nrci_gap > 0.05:
                        nrci_gap_boost = 1.0 + (nrci_gap * 0.5)
                        confidence = min(1.0, confidence * nrci_gap_boost)

                # Check if the result required a coherence snap
                if corroboration_count == 0:
                    coherence_snap = True

        # Null Resonance threshold
        if confidence < 0.08:
            return ReasoningResult(
                f'**[Null Resonance]** Query could not be resolved to a stable concept. '
                f'Best candidate: {top_candidate_uid} (Confidence: {confidence:.1%})',
                ubp_id=top_candidate_uid,
                confidence=confidence,
                top_candidates=sorted_scores[:5],
                coherence_snap=coherence_snap
            )

        # Build response
        top_entry = self.kb_manager.kb[top_candidate_uid]
        name = extract_name(top_entry)
        desc = extract_description(top_entry)
        layer = 'belief' if is_belief(top_entry) else 'understanding'
        nrci_val = float(extract_nrci(top_entry))

        response_text = (
            f'**{name}** ({top_candidate_uid})\n'
            f'{desc}\n'
            f'---\n'
            f'NRCI: {nrci_val:.4f} | Confidence: {confidence:.2%} | Layer: {layer}'
        )

        return ReasoningResult(
            response=response_text,
            ubp_id=top_candidate_uid,
            confidence=confidence,
            layer=layer,
            top_candidates=sorted_scores[:5],
            coherence_snap=coherence_snap
        )

    def recall(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Recall the top-k KB entries for a query.
        Returns a list of dicts with 'ubp_id', 'confidence', 'name', 'description'.
        """
        result = self.process_query(query)
        if not result.top_candidates:
            return []

        output = []
        for uid, score in result.top_candidates[:top_k]:
            entry = self.kb_manager.kb.get(uid, {})
            output.append({
                'ubp_id': uid,
                'score': score,
                'name': extract_name(entry),
                'description': extract_description(entry),
                'nrci': float(extract_nrci(entry)),
            })
        return output

# ==============================================================================
# SECTION 4: MAIN EXECUTION & DIAGNOSTICS
# ==============================================================================

if __name__ == '__main__':
    # --- Initialize Brain ---
    brain = UBPBrain()
    brain.initialize(['ubp_system_kb.json'])

    print('\n' + '='*70)
    print('UBP BRAIN v5.2 — N-GRAM MATCHING DIAGNOSTIC')
    print('='*70)

    test_queries = [
        "What is an up quark?",
        "What is a down quark?",
        "What is a strange quark?",
        "What is a charm quark?",
        "What is a top quark?",
        "What is a bottom quark?",
        "What is a W boson?",
        "What is a Z boson?",
        "What is the Higgs boson?",
        "What is a tau lepton?",
        "What is an electron neutrino?",
        "What is a muon neutrino?",
        "What is a tau neutrino?",
        "What is an alpha particle?",
        "What is a positron?",
        "What is water?",
        "What is carbon dioxide?",
        "What is ammonia?",
        "What is glucose?",
        "What is sulfuric acid?",
        "What is hydrochloric acid?",
        "What is sodium hydroxide?",
        "What is phosphoric acid?",
        "What is the speed of light?",
        "What is the Planck constant?",
        "What is the Boltzmann constant?",
        "What is the Avogadro constant?",
        "What is the fine structure constant?",
        "What is the gravitational constant?",
        "What is photosynthesis?",
        "What is cellular respiration?",
        "What is the Haber process?",
        "What is nuclear fission?",
        "What is nuclear fusion?",
    ]

    print(f'\n{"Query":<40} {"Result":<42} {"Conf":>6}')
    print('-' * 92)
    for q in test_queries:
        r = brain.process_query(q)
        uid = r.ubp_id or 'NULL'
        print(f'  {q:<38} {uid:<42} {r.confidence:>5.1%}')
