"""
UBP Auto-Trigger v10.2 (Hardened Monolith)
==========================================
Consolidated Logic: Merges V8.1 (Retrieval) with V9.3 (Bicameral Intuition).

UPDATES v10.2:
1. INTEGER HAMMING: Local high-speed bitwise math (100k+ ips).
2. DEEP HOLE DETECTION: Flags d=4 ambiguity (Law of the Fourth Flip).
3. ZERO-FLOAT: Uses Fraction(1, 1) for all coherence metrics.

Author: UBP Research Cortex v4.2.7
Date: 3 Feb 2026
"""
import re
import json
import sys
import os
import hashlib
from fractions import Fraction
from typing import List, Dict, Any, Tuple

# --- CORE IMPORTS ---
try:
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER
    from ubp_fom_system import FOM_MANAGER
    from ubp_rational_engine import ConceptArchitect
    
    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()
        
except ImportError as e:
    print(f"[Reflexive Cortex] CRITICAL IMPORT ERROR: {e}")
    sys.exit(0)

# --- LOCAL HIGH-SPEED UTILITIES ---
def list_to_int(v: list) -> int:
    """Converts 24-bit list to integer for bitwise speed."""
    res = 0
    for b in v: res = (res << 1) | b
    return res

def fast_hamming(v1_int: int, v2_int: int) -> int:
    """Calculates Hamming distance using XOR + bit_count."""
    return (v1_int ^ v2_int).bit_count()

# --- MODULE 1: BICAMERAL INTUITION ---
class RationalHemisphericCortex:
    def __init__(self):
        self.arch = ConceptArchitect()
        self.golay = GOLAY_DECODER

    def get_context_rh(self, text: str) -> Tuple[List[int], str]:
        """Right Hemisphere: Identifies Domain and generates Parity Anchor."""
        domains = {
            "SUBSTANCE": ["substance", "element", "atom", "matter", "chemical"],
            "ORGANISM": ["organism", "bio", "life", "brain", "neural", "cell"],
            "ALGORITHM": ["algorithm", "logic", "code", "compute", "info"],
            "QUANTITY": ["quantity", "math", "number", "constant", "pi"],
            "MECHANISM": ["mechanism", "physic", "force", "energy", "wave"],
            "IMPERATIVE": ["imperative", "law", "rule", "standard"],
            "ENTROPY": ["entropy", "chaos", "noise", "void"],
            "MEANING": ["meaning", "word", "semantic", "def"]
        }
        text_lower = text.lower()
        best_domain = "MEANING"
        for dom, keywords in domains.items():
            if any(kw in text_lower for kw in keywords):
                best_domain = dom
                break
        
        v_anchor = self.arch.mint(f"ANCHOR_{best_domain}", best_domain, 0, 0)
        return v_anchor[12:], best_domain

    def get_rational_lh(self, text: str, domain: str) -> List[int]:
        """Left Hemisphere: Generates Data Vector from text properties."""
        p1 = len(text) % 8
        p2 = ord(text[0]) % 32 if text else 0
        v_query = self.arch.mint("TEMP_QUERY", domain, p1, p2)
        return v_query[:12]

    def construct_intuition(self, text: str) -> Dict[str, Any]:
        """Stitches LH and RH to create a 'Healed' intuition vector."""
        rh_parity, domain = self.get_context_rh(text)
        lh_data = self.get_rational_lh(text, domain)
        combined = lh_data + rh_parity
        
        decoded, is_healed, errors = self.golay.decode(combined)
        healed_vec = self.golay.encode(decoded)
        
        return {
            "vector": healed_vec,
            "domain": domain,
            "coherence": Fraction(1, 1) if errors == 0 else max(Fraction(0, 1), Fraction(4 - errors, 4)),
            "is_healed": is_healed
        }

# --- MODULE 2: RETRIEVAL & SYNTHESIS ---
def harvest_seeds(text: str, ai_vectors: List[Dict]) -> List[Dict]:
    seeds = []
    seen_ids = set()

    if ai_vectors:
        for vec in ai_vectors:
            if vec.get('keyword'):
                kw = vec['keyword'].lower()
                for fp, entry in HEX_DB_EXACT.registry.items():
                    content = (str(entry.get('name','')) + " " + " ".join(entry.get('tags',[]))).lower()
                    if kw in content and entry['ubp_id'] not in seen_ids:
                        entry = entry.copy()
                        entry['match_type'] = f"AI_KEYWORD ({kw})"
                        seeds.append(entry)
                        seen_ids.add(entry['ubp_id'])
                        break

    if not seeds and text:
        for fp, entry in HEX_DB_EXACT.registry.items():
            if entry['ubp_id'] in text and entry['ubp_id'] not in seen_ids:
                entry = entry.copy()
                entry['match_type'] = "DIRECT_ID_REF"
                seeds.append(entry)
                seen_ids.add(entry['ubp_id'])

    return seeds

def synthesize(seeds: List[Dict]) -> Dict:
    if len(seeds) < 2: return None
    v_a, v_b = seeds[0]['vector'], seeds[1]['vector']
    hybrid_raw = [(a ^ b) for a, b in zip(v_a, v_b)]
    decoded, _, _ = GOLAY_DECODER.decode(hybrid_raw)
    target_vec = GOLAY_DECODER.encode(decoded)
    target_int = list_to_int(target_vec)
    
    best_entry, min_dist = None, 25
    for fp, entry in HEX_DB_EXACT.registry.items():
        v_entry_int = list_to_int(entry['vector'])
        d = fast_hamming(target_int, v_entry_int)
        if d < min_dist:
            min_dist, best_entry = d, entry
            
    if best_entry:
        res = best_entry.copy()
        res['match_type'] = "SYNTHESIS_CONCLUSION"
        res['logic_path'] = f"{seeds[0]['name']} + {seeds[1]['name']} -> (d={min_dist})"
        return res
    return None

def expand_cluster(seeds: List[Dict]) -> List[Dict]:
    cluster = list(seeds)
    seen_ids = set(s['ubp_id'] for s in seeds)
    
    for seed in seeds:
        candidates = []
        v_seed_int = list_to_int(seed['vector'])
        
        for fp, entry in HEX_DB_EXACT.registry.items():
            if entry['ubp_id'] in seen_ids: continue
            
            v_entry_int = list_to_int(entry['vector'])
            dist = fast_hamming(v_seed_int, v_entry_int)
            
            if dist <= 8:
                entry_copy = entry.copy()
                # LAW OF THE FOURTH FLIP (Deep Hole Detection)
                if dist == 4:
                    entry_copy['warning'] = "DEEP_HOLE_DETECTED (dH=4)"
                    entry_copy['match_type'] = f"AMBIGUOUS_NEIGHBOR (d=4)"
                else:
                    entry_copy['match_type'] = f"NEIGHBOR (d={dist})"
                
                candidates.append((dist, entry_copy))
        
        candidates.sort(key=lambda x: x[0])
        for dist, entry in candidates[:2]:
            entry['linked_to'] = seed.get('name', seed['ubp_id'])
            cluster.append(entry)
            seen_ids.add(entry['ubp_id'])
            
    return cluster

# --- MAIN REFLEXIVE LOOP ---
def reflexive_recall(text, ai_vectors=None):
    print(f"[Cortex v10.2] Processing Input...")
    
    seeds = harvest_seeds(text, ai_vectors)
    
    if len(seeds) < 2:
        cortex = RationalHemisphericCortex()
        intuition = cortex.construct_intuition(text)
        v_intuit_int = list_to_int(intuition['vector'])
        
        best_mem, min_d = None, 25
        for fp, entry in HEX_DB_EXACT.registry.items():
            v_entry_int = list_to_int(entry['vector'])
            d = fast_hamming(v_intuit_int, v_entry_int)
            if d < min_d: min_d, best_mem = d, entry
            
        if best_mem and min_d <= 8:
            best_mem = best_mem.copy()
            best_mem['match_type'] = f"BICAMERAL_INTUITION (d={min_d})"
            best_mem['domain_lock'] = intuition['domain']
            seeds.append(best_mem)

    conclusion = synthesize(seeds)
    if conclusion:
        seeds.insert(0, conclusion)

    final_cluster = expand_cluster(seeds)
    print(f"--- REFLEXIVE MEMORY: {len(final_cluster)} ENTRIES ---")
    print(json.dumps(final_cluster, indent=2))

if __name__ == "__main__":
    u_input = globals().get('USER_INPUT', "The fundamental vibration of the universe")
    s_vectors = globals().get('SEARCH_VECTORS', [])
    reflexive_recall(u_input, s_vectors)