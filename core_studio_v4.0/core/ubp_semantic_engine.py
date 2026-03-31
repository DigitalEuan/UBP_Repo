"""
================================================================================
UBP SEMANTIC QUERY ENGINE v1.0
================================================================================
Author: E R A Craig & Claude (Anthropic)
Date: 30 March 2026

PURPOSE:
    Bridges the lang KB (semantic operators) and the system KB (physical laws,
    elements, particles, molecules) into a unified semantic retrieval system.

    This is the "auto_trigger upgrade" — instead of keyword matching alone, the
    engine decomposes natural language into:
        1. Semantic OPERATORS  (OP_*)  — what action/relation is involved
        2. Physical ENTITIES   (ELEM_, MOLECULE_, PARTICLE_, etc.) — what objects
    
    These are combined via mod-2 SYNTH addition into a single 24-bit query vector.
    The nearest system KB entries to that vector are the most contextually relevant
    laws and facts — retrieved geometrically, not by keyword.

ARCHITECTURE:
    query("why does hydrogen bond with oxygen?")
         │
         ├─ operator extraction → [OP_WHY, OP_BOND]
         ├─ entity extraction   → [ELEM_H_001, ELEM_O_008]
         ├─ SYNTH vector        → mod-2 sum of all 4 vectors
         └─ nearest neighbours  → top system KB laws (Hamming proximity)

KEY RESULT (verified):
    SYNTH(OP_WHY + PARTICLE_ELECTRON_001) → LAW_META_GENESIS_001 (d=0, exact)
    LAW_META_GENESIS_001: "The Law of Recursive Genesis"

================================================================================
"""

import json
import re
import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass, field


# ============================================================
# DATA TYPES
# ============================================================

@dataclass
class ParsedQuery:
    original: str
    operators: List[str]        # OP_ ubp_ids found
    entities: List[str]         # ELEM_/PARTICLE_/etc ubp_ids found
    unmatched_tokens: List[str] # words not resolved to any KB entry
    synth_vector: Optional[List[int]] = None

@dataclass
class SemanticResult:
    ubp_id: str
    name: str
    lexicon: str
    hamming_distance: int
    nrci_score: float
    tilt: float
    category: str               # LAW / ELEM / MOLECULE / PARTICLE / etc.
    activated_by: List[str]     # which operators/entities triggered this

    def summary(self) -> str:
        desc = self.lexicon[:120].rstrip() + ("..." if len(self.lexicon) > 120 else "")
        return (f"[d={self.hamming_distance}] {self.ubp_id} (nrci={self.nrci_score:.4f})\n"
                f"  {desc}\n"
                f"  Activated by: {', '.join(self.activated_by)}")


# ============================================================
# UTILITY
# ============================================================

def _get_vector(entry: dict) -> Optional[np.ndarray]:
    v = entry.get('atlas', {}).get('vector')
    if isinstance(v, list) and len(v) == 24:
        return np.array(v, dtype=np.int8)
    return None

def _hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.sum(a != b))

def _category(ubp_id: str) -> str:
    prefix = ubp_id.split('_')[0]
    return prefix  # LAW, ELEM, MOLECULE, PARTICLE, REACTION, OP, etc.


# ============================================================
# MAIN ENGINE
# ============================================================

class UBPSemanticEngine:
    """
    Unified semantic retrieval over the system KB, guided by lang KB operators.

    Usage:
        engine = UBPSemanticEngine()
        engine.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')

        result = engine.query("why does hydrogen bond with oxygen?")
        for r in result:
            print(r.summary())
    """

    def __init__(self):
        self.system_kb: Dict[str, dict] = {}   # ubp_id → entry (physical)
        self.lang_kb:   Dict[str, dict] = {}   # ubp_id → entry (operators)
        self.all_kb:    Dict[str, dict] = {}   # combined

        # Lookup indexes
        self._entity_name_index: Dict[str, str] = {}   # normalized name → ubp_id
        self._entity_word_index: Dict[str, List[str]] = defaultdict(list)  # word → [ubp_ids]
        self._operator_word_index: Dict[str, str] = {}  # word/stem → op ubp_id
        self._op_law_map: Optional[Dict] = None   # lazy computed

        # Precomputed vectors for fast search
        self._system_vectors: Dict[str, np.ndarray] = {}  # ubp_id → vector

    # ----------------------------------------------------------
    # LOADING
    # ----------------------------------------------------------

    def load(self, system_kb_path: str, lang_kb_path: str):
        """Load both KBs and build all indexes."""
        with open(system_kb_path, encoding='utf-8') as f:
            raw = json.load(f)
            for entry in raw.values():
                uid = entry.get('ubp_id')
                if uid:
                    self.system_kb[uid] = entry

        with open(lang_kb_path, encoding='utf-8') as f:
            raw = json.load(f)
            for entry in raw.values():
                uid = entry.get('ubp_id')
                if uid:
                    self.lang_kb[uid] = entry

        self.all_kb = {**self.system_kb, **self.lang_kb}

        # Precompute system KB vectors (these are the search targets)
        for uid, entry in self.system_kb.items():
            v = _get_vector(entry)
            if v is not None:
                self._system_vectors[uid] = v

        self._build_entity_index()
        self._build_operator_index()

        print(f"[SemanticEngine] Loaded {len(self.system_kb)} system KB + "
              f"{len(self.lang_kb)} lang KB = {len(self.all_kb)} total entries")
        print(f"  Entity index: {len(self._entity_name_index)} names, "
              f"{len(self._entity_word_index)} word buckets")
        print(f"  Operator index: {len(self._operator_word_index)} trigger words")

    # ----------------------------------------------------------
    # INDEX BUILDING
    # ----------------------------------------------------------

    def _extract_name(self, entry: dict) -> str:
        """Extract the primary name from lexicon field."""
        lex = entry.get('lexicon', '')
        m = re.match(r'^\[([^\]]+)\]', lex)
        if m:
            content = m.group(1)
            if ':' in content:
                name = content.split(':', 1)[1].strip()
                name = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip()
                return name
            return content.strip()
        return entry.get('ubp_id', '').replace('_', ' ')

    # Entity type priority for resolution disambiguation (lower = higher priority)
    ENTITY_PRIORITY = {
        'PARTICLE': 1, 'ELEM': 2, 'MOLECULE': 3,
        'REACTION': 4, 'CRYSTAL': 5, 'MATH': 6,
        'ALGO': 7, 'TOOL': 8, 'GEO': 9,
        'LAW': 10, 'BELIEF': 11, 'DS': 12, 'BIN': 13,
    }

    # Words that are operators — never resolve these as entity names
    OP_WORDS = {
        'bond', 'bonds', 'emit', 'emits', 'absorb', 'absorbs',
        'orbit', 'orbits', 'spin', 'spins', 'decay', 'decays',
        'react', 'reacts', 'grow', 'grows', 'combine', 'combines',
        'move', 'moves', 'stop', 'stops', 'push', 'pull',
        'compress', 'expand', 'store', 'retrieve', 'signal',
        'filter', 'sort', 'merge', 'split', 'bind', 'release',
        'create', 'destroy', 'change', 'stay', 'measure',
        'remember', 'forget', 'focus', 'ignore', 'know',
        'attract', 'repel', 'vibrate', 'oscillate', 'propagate',
        'scatter', 'diffract', 'refract', 'tunnel', 'entangle',
        'encode', 'decode', 'transmit', 'receive', 'encrypt',
        'compare', 'classify', 'predict', 'transform', 'invert',
        'integrate', 'derive', 'converge', 'diverge', 'recurse',
        'permute', 'project', 'amplify', 'dampen', 'accelerate',
        'decelerate', 'reverse', 'repeat', 'iterate',
        'evolve', 'mutate', 'metabolize', 'replicate', 'transcribe',
        'inhibit', 'differentiate', 'collide', 'resonate',
        'catalyze', 'polymerize', 'ionize', 'oxidize', 'reduce',
        'dissolve', 'precipitate', 'unbond',
    }

    def _build_entity_index(self):
        """
        Index all non-operator system KB entries by name and individual words.
        LAW entries are indexed by full name only (not word-level) to prevent
        spurious matches when operator words appear in law names.
        """
        # Only word-index concrete physical entries
        WORD_INDEX_PREFIXES = ('ELEM_', 'MOLECULE_', 'PARTICLE_', 'REACTION_',
                               'CRYSTAL_', 'MATH_')
        ALL_PREFIXES = WORD_INDEX_PREFIXES + ('ALGO_', 'TOOL_', 'LAW_',
                                               'BELIEF_', 'GEO_', 'DS_', 'BIN_')

        for uid, entry in self.system_kb.items():
            if not any(uid.startswith(p) for p in ALL_PREFIXES):
                continue

            name = self._extract_name(entry).lower()

            # Full-name index (all types)
            self._entity_name_index[name] = uid

            # Symbol index (e.g. 'H', 'He', 'Fe')
            lex = entry.get('lexicon', '')
            sym_m = re.search(r'\(([A-Za-z][a-z0-9]?)\)', lex[:80])
            if sym_m:
                sym = sym_m.group(1).lower()
                if 1 <= len(sym) <= 3 and sym not in self.OP_WORDS:
                    self._entity_name_index[sym] = uid

            # ubp_id stem index (e.g. 'h2o', 'nacl' from MOLECULE_H2O_001)
            id_parts = uid.lower().split('_')
            for s in id_parts[1:]:
                if len(s) >= 2 and not s.isdigit() and s not in self.OP_WORDS:
                    # Only overwrite if this type has higher priority
                    if s not in self._entity_name_index:
                        self._entity_name_index[s] = uid
                    else:
                        existing = self._entity_name_index[s]
                        ex_type = existing.split('_')[0]
                        cur_type = uid.split('_')[0]
                        if (self.ENTITY_PRIORITY.get(cur_type, 99) <
                                self.ENTITY_PRIORITY.get(ex_type, 99)):
                            self._entity_name_index[s] = uid

            # Word-level index — only for concrete physical entries, skip op words
            if any(uid.startswith(p) for p in WORD_INDEX_PREFIXES):
                words = re.sub(r'[^a-z0-9 ]', '', name).split()
                for w in words:
                    if len(w) >= 3 and w not in self.OP_WORDS and w not in self.STOP_WORDS:
                        self._entity_word_index[w].append(uid)

    def _build_operator_index(self):
        """
        Index all lang KB operators by their name and common trigger words.
        Includes stemmed forms so 'bonding' → OP_BOND, 'emitting' → OP_EMIT.
        """
        SUFFIXES_TO_STRIP = ['ing', 'tion', 'sion', 'ness', 'ment', 'ive',
                             'ise', 'ize', 'ed', 'er', 'ly', 'al', 'ent', 'ate']

        def stem(word: str) -> str:
            for suf in SUFFIXES_TO_STRIP:
                if word.endswith(suf) and len(word) - len(suf) >= 3:
                    return word[:-len(suf)]
            return word

        for uid, entry in self.lang_kb.items():
            if not uid.startswith('OP_'):
                continue
            # Primary trigger: the operator word itself (e.g. 'bond' from OP_BOND)
            op_word = uid[3:].lower().replace('_', ' ')  # 'bond', 'accelerate field'
            self._operator_word_index[op_word] = uid

            # Each component word
            for w in op_word.split():
                self._operator_word_index[w] = uid
                self._operator_word_index[stem(w)] = uid

            # Synonyms / alternate triggers from lexicon
            lex = entry.get('lexicon', '').lower()
            # Pull words from the definition that are distinctive (length > 5)
            def_words = re.findall(r'\b([a-z]{5,})\b', lex)
            for w in def_words[:6]:  # take first 6 distinctive words
                s = stem(w)
                if s not in self._operator_word_index:
                    self._operator_word_index[s] = uid

        # Manual high-value synonyms
        SYNONYMS = {
            'join': 'OP_BOND', 'link': 'OP_BOND', 'attach': 'OP_BOND',
            'break': 'OP_UNBOND', 'split': 'OP_SPLIT', 'cleave': 'OP_UNBOND',
            'why': 'OP_WHY', 'because': 'OP_WHY', 'cause': 'OP_WHY', 'reason': 'OP_WHY',
            'how': 'OP_HOW', 'mechanism': 'OP_HOW', 'process': 'OP_HOW',
            'what': 'OP_WHAT', 'define': 'OP_WHAT', 'meaning': 'OP_WHAT',
            'where': 'OP_WHERE', 'location': 'OP_WHERE', 'position': 'OP_WHERE',
            'when': 'OP_WHEN', 'time': 'OP_WHEN', 'sequence': 'OP_WHEN',
            'who': 'OP_WHO', 'which': 'OP_WHAT',
            'speed': 'OP_FAST', 'slow': 'OP_SLOW', 'fast': 'OP_FAST',
            'combine': 'OP_COMBINE', 'merge': 'OP_MERGE', 'fuse': 'OP_BOND',
            'release': 'OP_RELEASE', 'emit': 'OP_EMIT', 'absorb': 'OP_ABSORB',
            'stable': 'OP_STABLE', 'decay': 'OP_DECAY', 'grow': 'OP_GROW',
            'orbit': 'OP_ORBIT', 'rotate': 'OP_SPIN', 'spin': 'OP_SPIN',
            'quantum': 'OP_QUANTUM', 'entangled': 'OP_ENTANGLE',
            'tunnel': 'OP_TUNNEL', 'tunnelling': 'OP_TUNNEL',
            'oscillat': 'OP_OSCILLATE', 'vibrat': 'OP_VIBRATE',
            'scatter': 'OP_SCATTER', 'diffract': 'OP_DIFFRACT', 'refract': 'OP_REFRACT',
            'react': 'OP_REACT', 'reaction': 'OP_REACT', 'catalys': 'OP_CATALYZE',
            'oxidis': 'OP_OXIDIZE', 'oxidiz': 'OP_OXIDIZE', 'reduc': 'OP_REDUCE',
            'dissolv': 'OP_DISSOLVE', 'soluble': 'OP_DISSOLVE',
            'evolv': 'OP_EVOLVE', 'evolut': 'OP_EVOLVE', 'mutat': 'OP_MUTATE',
            'replac': 'OP_REPLICATE', 'copy': 'OP_REPLICATE', 'duplicat': 'OP_REPLICATE',
            'encod': 'OP_ENCODE', 'decod': 'OP_DECODE', 'encrypt': 'OP_ENCRYPT',
            'stor': 'OP_STORE', 'retriev': 'OP_RETRIEVE', 'memoris': 'OP_REMEMBER',
            'predict': 'OP_PREDICT', 'classif': 'OP_CLASSIFY', 'sort': 'OP_SORT',
            'compress': 'OP_COMPRESS', 'expand': 'OP_EXPAND',
            'accelerat': 'OP_ACCELERATE', 'decalerat': 'OP_DECELERATE',
            'integrat': 'OP_INTEGRATE', 'differentiat': 'OP_DIFFERENTIATE',
            'transform': 'OP_TRANSFORM', 'invert': 'OP_INVERT',
            'converg': 'OP_CONVERGE', 'diverg': 'OP_DIVERGE',
            'propagat': 'OP_PROPAGATE', 'transmit': 'OP_TRANSMIT',
            'signal': 'OP_SIGNAL', 'inhibit': 'OP_INHIBIT',
            'bind': 'OP_BIND', 'unbind': 'OP_RELEASE',
        }
        for word, uid in SYNONYMS.items():
            if uid in self.lang_kb:
                self._operator_word_index[word] = uid

    # ----------------------------------------------------------
    # QUERY PARSING
    # ----------------------------------------------------------

    STOP_WORDS = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'of', 'to', 'in', 'and', 'for',
        'with', 'on', 'at', 'by', 'from', 'or', 'but', 'not', 'so', 'if',
        'as', 'into', 'this', 'that', 'these', 'those', 'it', 'its',
        'about', 'explain', 'tell', 'me', 'give', 'show', 'describe',
        'between', 'more', 'most', 'also', 'just', 'very', 'then',
    }

    def parse_query(self, query: str) -> ParsedQuery:
        """
        Decompose a natural language query into operators and physical entities.
        
        Strategy:
          1. Tokenize to words, strip punctuation
          2. Try bigram entity matches (e.g. 'carbon dioxide', 'sulfuric acid')  
          3. Try unigram entity matches (element names, symbols, particle names)
          4. Try operator matches (with stemming)
          5. Remaining words → unmatched_tokens
        """
        query_clean = re.sub(r'[^a-zA-Z0-9 ]', ' ', query.lower())
        words = query_clean.split()

        operators: List[str] = []
        entities: List[str] = []
        used_positions: Set[int] = set()

        op_set = set()
        entity_set = set()

        # --- Pass 1: Bigram entity matching ---
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if bigram in self._entity_name_index:
                uid = self._entity_name_index[bigram]
                if uid not in entity_set:
                    entity_set.add(uid)
                    entities.append(uid)
                used_positions.add(i)
                used_positions.add(i + 1)

        # --- Pass 2: Unigram entity matching ---
        for i, w in enumerate(words):
            if i in used_positions or w in self.STOP_WORDS or len(w) < 2:
                continue
            if w in self._entity_name_index:
                uid = self._entity_name_index[w]
                if uid not in entity_set:
                    entity_set.add(uid)
                    entities.append(uid)
                used_positions.add(i)
            elif w in self._entity_word_index:
                # Multiple candidates — pick highest NRCI
                candidates = self._entity_word_index[w]
                best = min(candidates, key=lambda u: (self.ENTITY_PRIORITY.get(u.split("_")[0], 99), -self.system_kb.get(u, {}).get("atlas", {}).get("nrci_score", 0)))
                if best not in entity_set:
                    entity_set.add(best)
                    entities.append(best)
                used_positions.add(i)

        # --- Pass 3: Operator matching (with stem fallback) ---
        SUFFIXES = ['ing', 'tion', 'sion', 'ness', 'ment', 'ive',
                    'ise', 'ize', 'ed', 'er', 'al', 'ent', 'ate', 'ly']

        def find_op(word: str) -> Optional[str]:
            if word in self._operator_word_index:
                return self._operator_word_index[word]
            for suf in SUFFIXES:
                if word.endswith(suf) and len(word) - len(suf) >= 3:
                    stem = word[:-len(suf)]
                    if stem in self._operator_word_index:
                        return self._operator_word_index[stem]
            return None

        # Bigram operators (e.g. "accelerate field")
        for i in range(len(words) - 1):
            if i in used_positions:
                continue
            bigram = f"{words[i]} {words[i+1]}"
            op = find_op(bigram)
            if op and op not in op_set:
                op_set.add(op)
                operators.append(op)
                used_positions.add(i)
                used_positions.add(i + 1)

        for i, w in enumerate(words):
            if i in used_positions or w in self.STOP_WORDS or len(w) < 2:
                continue
            op = find_op(w)
            if op and op not in op_set:
                op_set.add(op)
                operators.append(op)
                used_positions.add(i)

        unmatched = [w for i, w in enumerate(words)
                     if i not in used_positions
                     and w not in self.STOP_WORDS
                     and len(w) >= 3]

        return ParsedQuery(
            original=query,
            operators=operators,
            entities=entities,
            unmatched_tokens=unmatched,
        )

    # ----------------------------------------------------------
    # SYNTH
    # ----------------------------------------------------------

    def synth(self, ubp_ids: List[str]) -> Optional[np.ndarray]:
        """
        Mod-2 (XOR) sum of vectors for the given ubp_ids.
        Looks in both system_kb and lang_kb.
        """
        result = None
        for uid in ubp_ids:
            entry = self.all_kb.get(uid)
            if entry is None:
                print(f"  [SYNTH] Warning: '{uid}' not found in KB")
                continue
            v = _get_vector(entry)
            if v is None:
                continue
            result = v.copy() if result is None else (result + v) % 2
        return result

    # ----------------------------------------------------------
    # SEMANTIC QUERY (the main API)
    # ----------------------------------------------------------

    def query(self, text: str, top_k: int = 8,
              include_lang: bool = False,
              max_hamming: int = 16) -> Tuple[ParsedQuery, List[SemanticResult]]:
        """
        Full semantic query pipeline:
          1. Parse text → operators + entities
          2. SYNTH all found vectors
          3. Find nearest system KB entries (by Hamming distance)
          4. Return ParsedQuery + ranked SemanticResult list

        Args:
            text:         Natural language query
            top_k:        Number of results to return
            include_lang: If True, also search lang KB (useful for debugging)
            max_hamming:  Discard results beyond this distance
        """
        parsed = self.parse_query(text)

        all_ids = parsed.operators + parsed.entities
        if not all_ids:
            parsed.synth_vector = None
            return parsed, []

        synth_vec = self.synth(all_ids)
        if synth_vec is None:
            return parsed, []
        parsed.synth_vector = synth_vec.tolist()

        # Score all system KB entries
        search_pool = self._system_vectors
        if include_lang:
            for uid, entry in self.lang_kb.items():
                v = _get_vector(entry)
                if v is not None:
                    search_pool = dict(search_pool)
                    search_pool[uid] = v

        scored = []
        for uid, v in search_pool.items():
            d = _hamming(synth_vec, v)
            if d <= max_hamming:
                scored.append((uid, d))
        scored.sort(key=lambda x: (x[1], -self.all_kb.get(x[0], {}).get('atlas', {}).get('nrci_score', 0)))

        results = []
        for uid, d in scored[:top_k]:
            entry = self.all_kb[uid]
            results.append(SemanticResult(
                ubp_id=uid,
                name=self._extract_name(entry),
                lexicon=entry.get('lexicon', ''),
                hamming_distance=d,
                nrci_score=entry.get('atlas', {}).get('nrci_score', 0.0),
                tilt=entry.get('atlas', {}).get('tilt', 0.0),
                category=_category(uid),
                activated_by=all_ids,
            ))

        return parsed, results

    def query_display(self, text: str, top_k: int = 8, max_hamming: int = 16):
        """Convenience: query + print formatted results."""
        parsed, results = self.query(text, top_k=top_k, max_hamming=max_hamming)

        print(f"\n{'═'*70}")
        print(f"  QUERY: {parsed.original}")
        print(f"{'═'*70}")
        print(f"  Operators: {parsed.operators or '(none)'}")
        print(f"  Entities:  {parsed.entities or '(none)'}")
        if parsed.unmatched_tokens:
            print(f"  Unmatched: {parsed.unmatched_tokens}")
        if parsed.synth_vector:
            weight = sum(parsed.synth_vector)
            print(f"  SYNTH vector weight: {weight}/24")
        print(f"  Results: {len(results)}")
        print()

        if not results:
            print("  [Null Resonance] — no system KB entries within Hamming threshold.")
        for i, r in enumerate(results):
            # Truncate lexicon for display
            lex_short = r.lexicon[:100].rstrip() + ("…" if len(r.lexicon) > 100 else "")
            print(f"  [{i+1}] d={r.hamming_distance:2d}  {r.ubp_id:<40s}  nrci={r.nrci_score:.4f}")
            print(f"       {lex_short}")
        return parsed, results

    # ----------------------------------------------------------
    # OPERATOR-LAW PROXIMITY MAP
    # ----------------------------------------------------------

    def build_op_law_map(self, max_hamming: int = 8) -> Dict:
        """
        Precompute: for every operator in the lang KB, which system KB entries
        sit within max_hamming Hamming distance?
        
        This is the 'activation map': applying OP_BOND activates these laws.
        Returns a dict suitable for JSON export.
        """
        result = {}
        ops = [(uid, e) for uid, e in self.lang_kb.items() if uid.startswith('OP_')]

        for op_uid, op_entry in ops:
            op_vec = _get_vector(op_entry)
            if op_vec is None:
                continue
            matches = []
            for sys_uid, sys_vec in self._system_vectors.items():
                d = _hamming(op_vec, sys_vec)
                if d <= max_hamming:
                    sys_entry = self.system_kb[sys_uid]
                    matches.append({
                        'ubp_id': sys_uid,
                        'hamming': d,
                        'nrci': sys_entry.get('atlas', {}).get('nrci_score', 0),
                        'name': self._extract_name(sys_entry),
                        'category': _category(sys_uid),
                    })
            matches.sort(key=lambda x: (x['hamming'], -x['nrci']))
            result[op_uid] = {
                'tilt': op_entry.get('atlas', {}).get('tilt', 0.0),
                'nrci': op_entry.get('atlas', {}).get('nrci_score', 0.0),
                'activated_laws': matches,
            }

        self._op_law_map = result
        return result


# ============================================================
# MODULE SELF-TEST  (run directly: python3 ubp_semantic_engine.py)
# ============================================================

if __name__ == '__main__':


    engine = UBPSemanticEngine()
    engine.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')

    print("\n" + "═"*70)
    print("  SEMANTIC ENGINE SELF-TEST")
    print("═"*70)

    TESTS = [
        "why does hydrogen bond with oxygen?",
        "how does the electron emit a photon?",
        "what is the process of nuclear fusion?",
        "how does carbon bond to form a molecule?",
        "why does water dissolve sodium chloride?",
        "how does DNA replicate and transcribe?",
        "what happens when particles collide at high speed?",
        "why do quantum systems entangle?",
        "how does a catalyst accelerate a reaction?",
        "what is the orbit of an electron?",
    ]

    for q in TESTS:
        engine.query_display(q, top_k=5, max_hamming=12)
