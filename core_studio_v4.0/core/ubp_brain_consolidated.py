"""
================================================================================
UBP BRAIN CONSOLIDATED v5.2 — N-GRAM NAME MATCHING
================================================================================
Author: E R A Craig, New Zealand
Date: 27 March 2026
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
import math

# Link to the new modular core
from core import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra
CORE_AVAILABLE = True

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
        """v6.5.3 - Final Brute-Force N-Gram Extraction with Hyphen Support"""
        import re
        for uid, entry in self.kb.items():
            lex = entry.get('lexicon', '').lower()
            chunks = [c.split(']')[0] for c in lex.split('[') if ']' in c]
            for chunk in chunks:
                name = chunk.split(':')[-1].strip()
                name = name.split('(')[0].strip()
                if not name: continue
                
                # Index both 'Haber-Bosch' and 'Haber Bosch'
                variants = {name, name.replace('-', ' ')}
                for v in variants:
                    self.short_name_index[v] = uid
                    words = v.split()
                    if len(words) >= 3: self.trigram_index[' '.join(words[:3])] = uid
                    if len(words) >= 2: self.bigram_index[' '.join(words[:2])] = uid
                    for word in words:
                        if len(word) > 2 or word in ['w', 'z', 'h', 'e', 'p', 'n']:
                            self.lexicon_index[word].append(uid)
            for tag in entry.get('tags', []):
                self.short_name_index[tag.lower()] = uid
        self.stats = {
            'total_entries': len(self.kb),
            'indexed_names': len(self.short_name_index),
            'bigrams': len(self.bigram_index),
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

    def _pack_vector(self, vec):
        if isinstance(vec, int): return vec
        packed = 0
        for bit in vec: packed = (packed << 1) | bit
        return packed
    
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
            if (word in ['w', 'z', 'h'] or (word not in self.STOP_WORDS and len(word) > 2)):
                vector, direct_uid = self._get_token_vector(word)
                if vector:
                    tokens.append({'word': word, 'vector': vector,
                                   'direct_uid': direct_uid, 'ngram_size': 1})
                    if direct_uid:
                        direct_matches[direct_uid] += 1
            i += 1

        return tokens, direct_matches

    def process_query(self, query: str, debug: bool = False):
        if not self.initialized: return ReasoningResult('Brain not initialized.')
        from collections import defaultdict
        # Clean query for exact matching
        q_clean = query.lower().replace('?', '').replace('.', '').replace('what is an ', '').replace('what is a ', '').replace('what is ', '').strip()
        
        # --- 1. IDENTITY LOCK (v6.5.5) ---
        # Check for exact name matches first to resolve collisions (e.g., Ammonia vs Haber)
        if q_clean in self.kb_manager.short_name_index:
            uid = self.kb_manager.short_name_index[q_clean]
            return ReasoningResult(response='', ubp_id=uid, confidence=1.0)
        
        # --- 2. FUZZY RESONANCE (Fallback) ---
        q_lower = query.lower()
        is_particle = any(x in q_lower for x in ['quark', 'boson', 'lepton', 'neutrino', 'particle'])
        is_chem = any(x in q_lower for x in ['acid', 'hydroxide', 'molecule', 'water', 'glucose'])
        
        tokens, direct_matches = self._tokenize_with_ngrams(query)
        if not tokens: return ReasoningResult('**[Null Resonance]**', confidence=0.0)
        
        resonance_map = defaultdict(float)
        for token in tokens:
            t_word = token['word']
            t_vec = token['vector']
            t_weight = token.get('ngram_size', 1) ** 2
            
            for uid, entry in self.kb_manager.kb.items():
                # Domain Gating
                if is_particle and not uid.startswith('PARTICLE_'): continue
                if is_chem and not uid.startswith('MOLECULE_') and not (uid.startswith('REACTION_') and 'acid' in q_lower): continue
                
                m_vec = extract_vector(entry)
                if m_vec is None: continue
                
                # Bitwise Similarity
                dist = sum(1 for a, b in zip(t_vec, m_vec) if a != b)
                similarity = (24.0 - dist) / 24.0
                
                if similarity > 0.7:
                    score = similarity * t_weight * float(extract_nrci(entry))
                    # Exact Name Spike
                    if t_word == extract_name(entry).lower(): score *= 1000
                    # Tie-Breakers
                    if is_particle and uid.startswith('PARTICLE_'): score *= 2.0
                    
                    resonance_map[uid] += score
        
        for uid, count in direct_matches.items(): resonance_map[uid] *= (1.0 + count)
        
        if not resonance_map: return ReasoningResult('Lattice search failed.')
        sorted_res = sorted(resonance_map.items(), key=lambda x: x[1], reverse=True)
        top_uid, top_score = sorted_res[0]
        
        avg_others = sum(s[1] for s in sorted_res[1:4]) / 3 if len(sorted_res) > 1 else 0.1
        confidence = min(1.0, (top_score - avg_others) / top_score) if top_score > 0 else 0
        
        return ReasoningResult(response='', ubp_id=top_uid, confidence=confidence, top_candidates=sorted_res[:5])
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
