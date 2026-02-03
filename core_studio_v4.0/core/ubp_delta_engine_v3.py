"""
================================================================================
UBP DELTA REASONING ENGINE v3.0 - INTEGRATED LEXICON
================================================================================
Combines:
1. Delta Reasoning Engine v2.0 (attention field, feedback, context window)
2. Compact Lexicon v2.0 (Golay-encoded vocabulary, ~100KB)

Key improvements:
- Vocabulary is now integrated directly (no separate 94MB file)
- Words hash to Golay codewords for geometric consistency
- Cluster representatives provide semantic anchors
- Works in browser (via JS port) or Python

Target: Complete system under 1MB total

Author: E R A Craig, New Zealand
Date: 4 Feb 2026
================================================================================
"""

import hashlib
import json
import os
import sys
from fractions import Fraction
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import math

# Try to import UBP Core (optional - has fallback)
try:
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, LEECH_ENHANCED, UBPUltimateSubstrate
    HAS_UBP_CORE = True
except ImportError:
    HAS_UBP_CORE = False
    print("[Warning] UBP Core not found, using built-in Golay encoder")


# ==============================================================================
# SECTION 1: BUILT-IN GOLAY ENCODER (Fallback if UBP Core not available)
# ==============================================================================

class GolayEncoder:
    """Minimal Golay G24 encoder for standalone use."""
    
    # Parity matrix for G24
    P = [
        0b110111000101, 0b101110001011, 0b011100010111, 0b111000101101,
        0b110001011011, 0b100010110111, 0b000101101111, 0b001011011101,
        0b010110111001, 0b101101110001, 0b011011100011, 0b111111111110
    ]
    
    def encode(self, msg_bits: List[int]) -> List[int]:
        """Encode 12-bit message to 24-bit codeword."""
        if len(msg_bits) != 12:
            # Pad or truncate
            msg_bits = (msg_bits + [0] * 12)[:12]
        
        msg_int = int("".join(map(str, msg_bits)), 2)
        
        parity = 0
        for i in range(12):
            if (msg_int >> (11 - i)) & 1:
                parity ^= self.P[i]
        
        codeword_int = (msg_int << 12) | parity
        return [(codeword_int >> (23 - i)) & 1 for i in range(24)]
    
    def encode_int(self, msg_12bit: int) -> int:
        """Encode 12-bit integer to 24-bit codeword integer."""
        parity = 0
        for i in range(12):
            if (msg_12bit >> (11 - i)) & 1:
                parity ^= self.P[i]
        return (msg_12bit << 12) | parity


# Use UBP Core if available, otherwise use built-in
if HAS_UBP_CORE:
    GOLAY = GOLAY_DECODER
else:
    GOLAY = GolayEncoder()


# ==============================================================================
# SECTION 2: INTEGRATED LEXICON
# ==============================================================================

class IntegratedLexicon:
    """
    Compact lexicon with Golay-encoded vocabulary.
    
    Storage: ~100KB JSON with 4096 cluster representatives
    Lookup: Hash any word → Golay codeword → cluster info
    """
    
    DOMAINS = {
        0: "SUBSTANCE", 1: "MECHANISM", 2: "ORGANISM", 3: "ALGORITHM",
        4: "QUANTITY", 5: "IMPERATIVE", 6: "ENTROPY", 7: "MEANING"
    }
    
    DOMAIN_CHARS = {
        'S': "SUBSTANCE", 'M': "MECHANISM", 'O': "ORGANISM", 'A': "ALGORITHM",
        'Q': "QUANTITY", 'I': "IMPERATIVE", 'E': "ENTROPY", 'N': "MEANING"
    }
    
    def __init__(self):
        self.encoder = GolayEncoder()
        self.clusters: Dict[int, Dict] = {}  # vector_int → {rep, domain, size, def}
        self.loaded = False
    
    def load(self, filepath: str):
        """Load cluster data from JSON."""
        if not os.path.exists(filepath):
            print(f"[Lexicon] File not found: {filepath}")
            return False
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for hex_key, entry in data.get("c", {}).items():
            v_int = int(hex_key, 16)
            self.clusters[v_int] = {
                "rep": entry[0],
                "domain": self.DOMAIN_CHARS.get(entry[1], "MEANING"),
                "size": entry[2],
                "def": entry[3] if len(entry) > 3 else ""
            }
        
        self.loaded = True
        print(f"[Lexicon] Loaded {len(self.clusters)} clusters")
        return True
    
    def hash_word(self, word: str) -> int:
        """Hash word to 24-bit Golay codeword."""
        h = hashlib.sha256(word.lower().strip().encode()).digest()
        msg_12bit = ((h[0] << 8) | h[1]) & 0xFFF
        return self.encoder.encode_int(msg_12bit)
    
    def lookup(self, word: str) -> Dict:
        """Look up a word, return cluster info."""
        v_int = self.hash_word(word)
        cluster = self.clusters.get(v_int)
        
        if cluster:
            return {
                "word": word.lower().strip(),
                "vector": v_int,
                "vector_bits": self._int_to_bits(v_int),
                "domain": cluster["domain"],
                "representative": cluster["rep"],
                "cluster_size": cluster["size"],
                "definition": cluster.get("def", ""),
                "found": True
            }
        else:
            return {
                "word": word.lower().strip(),
                "vector": v_int,
                "vector_bits": self._int_to_bits(v_int),
                "domain": self._get_domain(v_int),
                "representative": word.lower().strip(),
                "cluster_size": 1,
                "definition": "",
                "found": False
            }
    
    def tokenize(self, text: str) -> List[Dict]:
        """Tokenize text into word lookups."""
        words = text.lower().split()
        return [self.lookup(w) for w in words if w]
    
    def _int_to_bits(self, v_int: int) -> List[int]:
        return [(v_int >> (23 - i)) & 1 for i in range(24)]
    
    def _get_domain(self, v_int: int) -> str:
        domain_bits = (v_int >> 21) & 7
        return self.DOMAINS.get(domain_bits, "MEANING")
    
    def nearest(self, v_int: int, threshold: int = 3) -> Optional[Dict]:
        """Find nearest cluster."""
        best = None
        min_dist = threshold + 1
        
        for cv_int, cluster in self.clusters.items():
            dist = (v_int ^ cv_int).bit_count()
            if dist < min_dist:
                min_dist = dist
                best = {
                    "vector": cv_int,
                    "distance": dist,
                    "representative": cluster["rep"],
                    "domain": cluster["domain"],
                    "cluster_size": cluster["size"]
                }
        
        return best


# ==============================================================================
# SECTION 3: MEMORY ENTRY
# ==============================================================================

@dataclass
class MemoryEntry:
    """Memory with context-specific NRCI weights."""
    codeword: List[int]
    codeword_int: int
    content: str
    domain: str
    base_nrci: Fraction
    context_nrci: Dict[str, Fraction] = field(default_factory=dict)
    associations: List[int] = field(default_factory=list)
    access_count: int = 0
    source: str = "kb"  # "kb", "vocab", "generated"
    
    def get_nrci(self, context: str = "default") -> Fraction:
        return self.context_nrci.get(context, self.base_nrci)
    
    def set_nrci(self, context: str, value: Fraction):
        self.context_nrci[context] = max(Fraction(1, 100), min(Fraction(1, 1), value))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "codeword_hex": f"{self.codeword_int:06x}",
            "content": self.content[:200],
            "domain": self.domain,
            "nrci": str(self.base_nrci),
            "source": self.source,
            "access_count": self.access_count
        }


# ==============================================================================
# SECTION 4: ATTENTION FIELD
# ==============================================================================

@dataclass
class AttentionSpike:
    """A spike in the attention field."""
    entry: MemoryEntry
    relevance: float
    distance: int
    domain_match: bool
    keyword_hits: int


class AttentionField:
    """Memory field with NRCI-weighted spikes."""
    
    def __init__(self, memories: Dict[int, MemoryEntry], context: str = "default"):
        self.memories = memories
        self.context = context
        self.focus_vector: Optional[int] = None
        self.focus_domain: Optional[str] = None
    
    def set_focus(self, vector_int: int, domain: str, keywords: List[str]):
        """Set the attention focus point."""
        self.focus_vector = vector_int
        self.focus_domain = domain
        self.keywords = [k.lower() for k in keywords if len(k) > 2]
    
    def scan(self, threshold: int = 12, limit: int = 20) -> List[AttentionSpike]:
        """Scan field for relevant spikes."""
        if self.focus_vector is None:
            return []
        
        spikes = []
        
        for cw_int, entry in self.memories.items():
            # Hamming distance
            dist = (self.focus_vector ^ cw_int).bit_count()
            if dist > threshold:
                continue
            
            # Domain match
            domain_match = entry.domain == self.focus_domain
            
            # Keyword hits
            content_lower = entry.content.lower()
            keyword_hits = sum(1 for kw in self.keywords if kw in content_lower)
            
            # Compute relevance
            nrci = float(entry.get_nrci(self.context))
            
            # Relevance formula:
            # - Base: inverse distance (closer = higher)
            # - Boost: domain match, keyword hits, NRCI
            # - KB entries get priority over vocab
            source_boost = 2.0 if entry.source == "kb" else 1.0
            
            relevance = (
                (1.0 / (1 + dist)) * 
                (2.0 if domain_match else 1.0) * 
                (1.0 + keyword_hits * 0.5) * 
                nrci * 
                source_boost
            )
            
            spikes.append(AttentionSpike(
                entry=entry,
                relevance=relevance,
                distance=dist,
                domain_match=domain_match,
                keyword_hits=keyword_hits
            ))
        
        # Sort by relevance
        spikes.sort(key=lambda s: -s.relevance)
        return spikes[:limit]


# ==============================================================================
# SECTION 5: CONTEXT WINDOW
# ==============================================================================

class ContextWindow:
    """Sliding window for multi-turn conversations."""
    
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turns: List[Dict] = []
        self.current_context: str = "default"
    
    def add_turn(self, query: str, response: str, vectors: List[int]):
        """Add a conversation turn."""
        self.turns.append({
            "query": query,
            "response": response[:500],
            "vectors": vectors[:5],
            "context": self.current_context
        })
        
        # Trim to max
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]
    
    def get_context_vectors(self) -> List[int]:
        """Get vectors from recent turns for context."""
        vectors = []
        for turn in self.turns[-3:]:  # Last 3 turns
            vectors.extend(turn.get("vectors", []))
        return vectors
    
    def set_context(self, context: str):
        """Switch context (e.g., 'physics', 'biology')."""
        self.current_context = context
    
    def to_dict(self) -> Dict:
        return {
            "turns": len(self.turns),
            "current_context": self.current_context,
            "recent_queries": [t["query"][:50] for t in self.turns[-3:]]
        }


# ==============================================================================
# SECTION 6: HEBBIAN TRAINER
# ==============================================================================

class HebbianTrainer:
    """Hebbian learning from feedback."""
    
    def __init__(self, memory_bank: 'DeltaMemoryBank'):
        self.memory = memory_bank
        self.learning_rate = Fraction(1, 10)
        self.feedback_log: List[Dict] = []
    
    def reinforce(self, chain: List[MemoryEntry], is_positive: bool, 
                  context: str = "default") -> int:
        """Reinforce or weaken chain based on feedback."""
        adjustments = 0
        
        for i, entry in enumerate(chain):
            position_weight = Fraction(len(chain) - i, len(chain))
            adjustment = self.learning_rate * position_weight
            
            old_nrci = entry.get_nrci(context)
            
            if is_positive:
                new_nrci = old_nrci + adjustment * (Fraction(1, 1) - old_nrci)
            else:
                new_nrci = old_nrci - adjustment
            
            entry.set_nrci(context, new_nrci)
            adjustments += 1
            
            # Update associations
            if i > 0 and is_positive:
                prev = chain[i - 1]
                if entry.codeword_int not in prev.associations:
                    prev.associations.append(entry.codeword_int)
        
        self.feedback_log.append({
            "context": context,
            "positive": is_positive,
            "adjustments": adjustments
        })
        
        return adjustments


# ==============================================================================
# SECTION 7: DELTA MEMORY BANK
# ==============================================================================

class DeltaMemoryBank:
    """Memory bank with integrated lexicon."""
    
    def __init__(self):
        self.memories: Dict[int, MemoryEntry] = {}
        self.domain_indices: Dict[str, List[int]] = defaultdict(list)
        self.lexicon = IntegratedLexicon()
    
    def store(self, codeword: List[int], content: str, domain: str,
              nrci: Fraction = Fraction(1, 2), source: str = "kb") -> MemoryEntry:
        """Store a memory."""
        cw_int = int("".join(map(str, codeword)), 2)
        
        # Check for existing entry at this codeword
        if cw_int in self.memories:
            # Append content if different
            existing = self.memories[cw_int]
            if content not in existing.content:
                existing.content = existing.content + " | " + content
            return existing
        
        entry = MemoryEntry(
            codeword=codeword,
            codeword_int=cw_int,
            content=content,
            domain=domain,
            base_nrci=nrci,
            source=source
        )
        
        self.memories[cw_int] = entry
        self.domain_indices[domain].append(cw_int)
        
        return entry
    
    def retrieve(self, query_cw: List[int], threshold: int = 8) -> Optional[MemoryEntry]:
        """Retrieve nearest memory."""
        q_int = int("".join(map(str, query_cw)), 2)
        best, min_d = None, threshold + 1
        
        for cw_int, entry in self.memories.items():
            d = (q_int ^ cw_int).bit_count()
            if d < min_d:
                min_d, best = d, entry
        
        if best:
            best.access_count += 1
        return best
    
    def keyword_search(self, keywords: List[str], limit: int = 10) -> List[MemoryEntry]:
        """Direct keyword search."""
        results = []
        kw_lower = [k.lower() for k in keywords if len(k) > 2]
        
        for entry in self.memories.values():
            content_lower = entry.content.lower()
            score = sum(1 for kw in kw_lower if kw in content_lower)
            if score > 0:
                results.append((score, entry))
        
        results.sort(key=lambda x: -x[0])
        return [e for _, e in results[:limit]]
    
    def load_kb(self, filepath: str):
        """Load system KB."""
        if not os.path.exists(filepath):
            print(f"[Memory] KB not found: {filepath}")
            return 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for k, v in data.items():
            if isinstance(v, dict) and ("ubp_id" in v or "vector" in v):
                vec = v.get("vector", [0] * 24)
                if len(vec) != 24:
                    continue
                
                nrci_str = v.get("nrci", "1/2")
                if isinstance(nrci_str, str) and "/" in nrci_str:
                    parts = nrci_str.split("/")
                    nrci = Fraction(int(parts[0]), int(parts[1]))
                else:
                    nrci = Fraction(1, 2)
                
                name = v.get("name", v.get("ubp_id", k))
                lang = v.get("language", "")
                content = f"{name}: {lang}" if lang else name
                
                domain = v.get("domain", self._infer_domain(v.get("ubp_id", k)))
                
                self.store(vec, content, domain, nrci, source="kb")
                count += 1
        
        print(f"[Memory] Loaded {count} KB entries")
        return count
    
    def load_lexicon(self, filepath: str):
        """Load compact lexicon."""
        return self.lexicon.load(filepath)
    
    def _infer_domain(self, ubp_id: str) -> str:
        uid = ubp_id.upper()
        if uid.startswith(("ELEM_", "CHEM_", "MAT_")): return "SUBSTANCE"
        if uid.startswith(("PHYS_", "MECH_", "QM_")): return "MECHANISM"
        if uid.startswith(("BIO", "CELL_", "PSYCH_")): return "ORGANISM"
        if uid.startswith(("PY_", "CODE_", "ALGO_")): return "ALGORITHM"
        if uid.startswith(("NUM_", "CONST_", "MATH_")): return "QUANTITY"
        if uid.startswith(("LAW_", "ACTION_")): return "IMPERATIVE"
        if uid.startswith(("PATTERN_", "TRANSFORM_")): return "ENTROPY"
        return "MEANING"
    
    def stats(self) -> Dict:
        domain_counts = {d: len(ids) for d, ids in self.domain_indices.items()}
        total_domain = sum(domain_counts.values())
        return {
            "total_memories": len(self.memories),
            "total_indexed": total_domain,
            "lexicon_clusters": len(self.lexicon.clusters),
            "domains": domain_counts
        }


# ==============================================================================
# SECTION 8: GEOMETRIC TOKENIZER
# ==============================================================================

class GeometricTokenizer:
    """Tokenizer with lexicon integration."""
    
    DOMAINS = {"SUBSTANCE": 0, "MECHANISM": 1, "ORGANISM": 2, "ALGORITHM": 3,
               "QUANTITY": 4, "IMPERATIVE": 5, "ENTROPY": 6, "MEANING": 7}
    
    def __init__(self, lexicon: IntegratedLexicon = None):
        self.encoder = GolayEncoder()
        self.lexicon = lexicon
    
    def infer_domain(self, text: str) -> str:
        t = text.upper()
        if any(x in t for x in ["ATOM", "CHEM", "ELEMENT", "MATERIAL"]): return "SUBSTANCE"
        if any(x in t for x in ["ENERGY", "FORCE", "QUANTUM", "PHYSICS"]): return "MECHANISM"
        if any(x in t for x in ["LAW", "MUST", "RULE", "SHOULD"]): return "IMPERATIVE"
        if any(x in t for x in ["PI", "MATH", "NUMBER", "CONSTANT"]): return "QUANTITY"
        if any(x in t for x in ["BIO", "LIFE", "CELL", "ORGANISM"]): return "ORGANISM"
        if any(x in t for x in ["CODE", "ALGO", "FUNCTION", "COMPUTE"]): return "ALGORITHM"
        if any(x in t for x in ["CHAOS", "RANDOM", "ENTROPY", "DECAY"]): return "ENTROPY"
        return "MEANING"
    
    def text_to_codeword(self, text: str, domain: str = None) -> List[int]:
        """Convert text to Golay codeword."""
        if not domain:
            domain = self.infer_domain(text)
        
        # Try lexicon lookup for single words
        words = text.lower().split()
        if len(words) == 1 and self.lexicon:
            lookup = self.lexicon.lookup(words[0])
            return lookup["vector_bits"]
        
        # Hash-based encoding
        h = hashlib.sha256(text.encode()).digest()
        combined = int.from_bytes(h[:4], 'big')
        
        dom_val = self.DOMAINS.get(domain, 7)
        msg = [(dom_val >> i) & 1 for i in range(2, -1, -1)]
        msg += [(combined >> i) & 1 for i in range(8, -1, -1)]
        
        return self.encoder.encode(msg)


# ==============================================================================
# SECTION 9: REASONING ENGINE
# ==============================================================================

@dataclass
class ThoughtStep:
    """A step in reasoning."""
    entry: MemoryEntry
    source: str
    coherence: float
    
    def to_dict(self) -> Dict:
        return {
            "content": self.entry.content[:200],
            "domain": self.entry.domain,
            "source": self.source,
            "coherence": self.coherence
        }


class DeltaReasoningEngine:
    """
    Complete reasoning engine with integrated lexicon.
    """
    
    def __init__(self):
        self.memory = DeltaMemoryBank()
        self.tokenizer = GeometricTokenizer()
        self.context_window = ContextWindow()
        self.trainer = HebbianTrainer(self.memory)
        
    def initialize(self, kb_paths: List[str] = None, lexicon_path: str = None):
        """Initialize with KB and lexicon."""
        # Load KBs
        if kb_paths:
            for path in kb_paths:
                if os.path.exists(path):
                    self.memory.load_kb(path)
        
        # Load lexicon
        if lexicon_path and os.path.exists(lexicon_path):
            self.memory.load_lexicon(lexicon_path)
            self.tokenizer.lexicon = self.memory.lexicon
        
        print(f"[Engine] Initialized: {self.memory.stats()}")
    
    def reason(self, query: str, max_steps: int = 6, context: str = None) -> Dict:
        """
        Perform reasoning on a query.
        
        Returns dict with:
        - query: original query
        - steps: reasoning chain
        - response: synthesized response
        - vectors: key vectors used
        """
        if context:
            self.context_window.set_context(context)
        
        ctx = self.context_window.current_context
        
        # Tokenize query
        domain = self.tokenizer.infer_domain(query)
        query_cw = self.tokenizer.text_to_codeword(query, domain)
        query_int = int("".join(map(str, query_cw)), 2)
        
        # Extract keywords
        keywords = [w for w in query.lower().split() if len(w) > 2]
        
        # Create attention field
        attention = AttentionField(self.memory.memories, ctx)
        attention.set_focus(query_int, domain, keywords)
        
        # Scan for spikes
        spikes = attention.scan(threshold=12, limit=max_steps * 2)
        
        # Also do keyword search
        kw_results = self.memory.keyword_search(keywords, limit=max_steps)
        
        # Build reasoning chain
        chain: List[ThoughtStep] = []
        seen_ints: Set[int] = set()
        
        # Add keyword results first (most relevant)
        for entry in kw_results:
            if entry.codeword_int not in seen_ints:
                chain.append(ThoughtStep(
                    entry=entry,
                    source="keyword",
                    coherence=1.0
                ))
                seen_ints.add(entry.codeword_int)
                if len(chain) >= max_steps:
                    break
        
        # Add attention spikes
        for spike in spikes:
            if spike.entry.codeword_int not in seen_ints:
                chain.append(ThoughtStep(
                    entry=spike.entry,
                    source="attention",
                    coherence=spike.relevance
                ))
                seen_ints.add(spike.entry.codeword_int)
                if len(chain) >= max_steps:
                    break
        
        # Synthesize response
        response_parts = []
        for step in chain[:3]:  # Top 3 for response
            content = step.entry.content
            if ":" in content:
                response_parts.append(content.split(":", 1)[1].strip()[:200])
            else:
                response_parts.append(content[:200])
        
        response = " | ".join(response_parts) if response_parts else "No relevant information found."
        
        # Update context window
        vectors = [step.entry.codeword_int for step in chain[:5]]
        self.context_window.add_turn(query, response, vectors)
        
        return {
            "query": query,
            "domain": domain,
            "context": ctx,
            "steps": [s.to_dict() for s in chain],
            "response": response,
            "vectors": vectors,
            "stats": {
                "spikes_found": len(spikes),
                "keyword_hits": len(kw_results),
                "chain_length": len(chain)
            }
        }
    
    def feedback(self, is_positive: bool) -> int:
        """Provide feedback on last response."""
        if not self.context_window.turns:
            return 0
        
        last_turn = self.context_window.turns[-1]
        vectors = last_turn.get("vectors", [])
        
        # Get entries for these vectors
        chain = [self.memory.memories[v] for v in vectors if v in self.memory.memories]
        
        return self.trainer.reinforce(
            chain, 
            is_positive, 
            self.context_window.current_context
        )
    
    def lookup_word(self, word: str) -> Dict:
        """Look up a word in the lexicon."""
        return self.memory.lexicon.lookup(word)
    
    def stats(self) -> Dict:
        """Get engine statistics."""
        return {
            "memory": self.memory.stats(),
            "context": self.context_window.to_dict(),
            "feedback_count": len(self.trainer.feedback_log)
        }


# ==============================================================================
# SECTION 10: MAIN / TESTING
# ==============================================================================

def main():
    """Test the integrated engine."""
    
    # Initialize engine
    engine = DeltaReasoningEngine()
    
    # KB paths (correct filenames)
    kb_paths = [
        "ubp_system_kb.json",
        "ubp_hash_memory_kb.json"
    ]
    
    # Lexicon path
    lexicon_path = "ubp_lexicon_v2.json"
    
    engine.initialize(kb_paths, lexicon_path)
    
    print("\n" + "="*60)
    print("UBP DELTA REASONING ENGINE v3.0 - TEST")
    print("="*60)
    
    # Test queries
    queries = [
        "What is the Golay code?",
        "Explain the observer fixed point",
        "Tell me about the Leech lattice",
        "How does error correction work?",
        "What is energy?"
    ]
    
    results = []
    for query in queries:
        print(f"\n[Query] {query}")
        result = engine.reason(query)
        print(f"[Domain] {result['domain']}")
        print(f"[Response] {result['response'][:200]}...")
        print(f"[Stats] {result['stats']}")
        results.append(result)
    
    # Test feedback
    print("\n[Testing feedback mechanism]")
    adj = engine.feedback(is_positive=True)
    print(f"Positive feedback: {adj} adjustments")
    
    # Test word lookup
    print("\n[Testing word lookup]")
    for word in ["quantum", "geometry", "the", "golay"]:
        lookup = engine.lookup_word(word)
        print(f"  '{word}' → rep='{lookup['representative']}', domain={lookup['domain']}")
    
    # Save results
    output = {
        "engine_stats": engine.stats(),
        "test_results": results
    }
    
    with open("delta_engine_v3_test.json", 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n[Results saved to delta_engine_v3_test.json]")
    
    return engine


if __name__ == "__main__":
    main()
