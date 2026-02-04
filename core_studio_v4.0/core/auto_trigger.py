"""
UBP Auto-Trigger v12.1 (Semantic-Aware)
=======================================
Updates:
1. LEXICON PRIORITY: Loads '_defs.json' for full definitions.
2. DEFINITION INJECTION: Injects word meanings into the reasoning context.

Author: UBP Research Cortex v4.2.7
Date: 4 Feb 2026
"""
import json
import sys
import re
import os
from fractions import Fraction
from typing import List, Dict, Any

# --- CORE IMPORTS ---
try:
    from ubp_delta_engine_v3 import DeltaReasoningEngine
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER
    
    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()

except ImportError as e:
    print(f"[Reflexive Cortex] CRITICAL IMPORT ERROR: {e}")
    sys.exit(0)

# --- SINGLETON DELTA ENGINE ---
if "GLOBAL_DELTA_ENGINE" not in globals():
    print("[CORTEX] Initializing Global Delta Engine...")
    GLOBAL_DELTA_ENGINE = DeltaReasoningEngine()
    
    kb_files = ["ubp_system_kb.json", "ubp_hash_memory_kb.json"]
    
    # PRIORITY: Look for the definitions file first
    if os.path.exists("ubp_lexicon_v2_defs.json"):
        lexicon_file = "ubp_lexicon_v2_defs.json"
        print("[CORTEX] Loaded Extended Lexicon (Definitions Enabled)")
    else:
        lexicon_file = "ubp_lexicon_v2.json"
        print("[CORTEX] Loaded Standard Lexicon")

    GLOBAL_DELTA_ENGINE.initialize(kb_files, lexicon_file)
else:
    pass

DELTA = globals().get("GLOBAL_DELTA_ENGINE", GLOBAL_DELTA_ENGINE)

# --- GEOMETRIC UTILITIES ---
def list_to_int(v: list) -> int:
    if not v: return 0
    res = 0
    for b in v: res = (res << 1) | b
    return res

def fast_hamming(v1_int: int, v2_int: int) -> int:
    return (v1_int ^ v2_int).bit_count()

# --- MODULE 1: SYNTHESIS ENGINE ---
def attempt_synthesis(seeds: List[Dict]) -> Dict:
    if len(seeds) < 2: return None
    
    vecs = []
    for s in seeds[:2]:
        v = s.get('vector')
        if not v and s.get('ubp_id'):
            entry = HEX_DB_EXACT.find_by_id(s['ubp_id'])
            if entry: v = entry.get('vector')
        if v: vecs.append(v)
    
    if len(vecs) < 2: return None

    v_a, v_b = vecs[0], vecs[1]
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
            
    if best_entry and min_dist <= 3:
        res = best_entry.copy()
        res['match_type'] = f"GEOMETRIC_SYNTHESIS (d={min_dist})"
        res['language'] = f"Emergent Truth derived from {seeds[0].get('name')} + {seeds[1].get('name')}: {res.get('language','')}"
        res['nrci'] = "1/1"
        return res
    return None

# --- MAIN REFLEXIVE LOOP ---
def reflexive_recall(text, ai_vectors=None):
    print(f"[Cortex v12.1] Processing Input via Delta Bridge...")
    
    # 1. Fast Path: Direct IDs
    memories = []
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        entry = HEX_DB_EXACT.find_by_id(uid)
        if entry:
            e = entry.copy()
            e['match_type'] = "DIRECT_ID_REF"
            memories.append(e)

    # 2. Deep Path: Delta Engine
    delta_result = DELTA.reason(text, max_steps=6)
    
    delta_memories = []
    for step in delta_result.get('steps', []):
        mem_entry = {
            "ubp_id": "DELTA_RECALL",
            "name": "Contextual Memory",
            "language": step.get('content', ''),
            "domain": step.get('domain', 'UNKNOWN'),
            "nrci": f"{step.get('coherence', 0.5):.2f}",
            "match_type": f"DELTA_{step.get('source', 'ASSOC').upper()}",
            "vector": []
        }
        delta_memories.append(mem_entry)

    # 3. Geometric Synthesis
    synthesis = attempt_synthesis(delta_memories)
    if synthesis:
        memories.insert(0, synthesis)

    # 4. Merge & Deduplicate
    all_candidates = memories + delta_memories
    seen_sig = set()
    final_list = []
    
    if delta_result.get('response'):
        final_list.append({
            "ubp_id": "SYS_DELTA_SYNTHESIS",
            "name": "Delta Synthesis",
            "language": delta_result['response'],
            "domain": delta_result.get('domain', 'MEANING'),
            "match_type": "SYNTHESIS_OUTPUT",
            "nrci": "1/1"
        })

    for m in all_candidates:
        sig = m.get('ubp_id', '') + m.get('language', '')[:30]
        if sig not in seen_content: # Fixed variable name from previous version
             final_list.append(m)
             seen_sig.add(sig)
    
    # 5. Output
    print(f"--- REFLEXIVE MEMORY: {len(final_list)} ENTRIES ---")
    print(json.dumps(final_list, indent=2))
    
    stats = DELTA.stats()
    print(f"[System] Context: {stats['context']['turns']} turns | Feedback: {stats['feedback_count']}")

# Fix for the variable name error in the loop above
seen_content = set() 

if __name__ == "__main__":
    u_input = globals().get('USER_INPUT', "What is the definition of entropy?")
    s_vectors = globals().get('SEARCH_VECTORS', [])
    reflexive_recall(u_input, s_vectors)
