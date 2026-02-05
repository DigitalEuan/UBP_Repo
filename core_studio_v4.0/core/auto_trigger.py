"""
UBP Auto-Trigger v13.2 (V8 Bridge Aligned)
==========================================
Updates:
1. PAYLOAD FIX: Packs data as {"vector": [r,g,b]} to match JS item.vector.
2. CALL FIX: Unpacks arguments to compute(r, g, b) to match JS signature.
3. HYBRID CONTEXT: Merges Regex, Delta, and Geometric results.

Author: E R A Craig, New Zealand
UBP Research Cortex v4.2.7
Date: 5 Feb 2026
"""
import json
import sys
import re
import os
import hashlib
from fractions import Fraction
from typing import List, Dict, Any

# --- BRIDGE IMPORT ---
try:
    from js import window
    BRIDGE_ACTIVE = True
except ImportError:
    BRIDGE_ACTIVE = False
    print("[CORTEX] Warning: JS Bridge not found. Running in standalone mode.")

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
    
    if os.path.exists("ubp_lexicon_v2_defs.json"):
        lexicon_file = "ubp_lexicon_v2_defs.json"
    else:
        lexicon_file = "ubp_lexicon_v2.json"

    GLOBAL_DELTA_ENGINE.initialize(kb_files, lexicon_file)
else:
    pass

DELTA = globals().get("GLOBAL_DELTA_ENGINE", GLOBAL_DELTA_ENGINE)

# --- MODULE 1: THE REFLEXIVE BRIDGE ---
def initialize_gpu_bridge():
    """
    Serializes the HexDB into a Vector-packed JSON payload and 
    sends it to the Main Thread (App.tsx) for V8 acceleration.
    """
    if not BRIDGE_ACTIVE: return

    print("[BRIDGE] Serializing Substrate for V8 Accelerator...")
    payload = []
    
    for uid, entry in HEX_DB_EXACT.registry.items():
        vec = entry.get('vector')
        ubp_id = entry.get('ubp_id')
        
        if vec and len(vec) == 24 and ubp_id:
            # Pack 24 bits into 3 Integers (RGB)
            r = int("".join(map(str, vec[0:8])), 2)
            g = int("".join(map(str, vec[8:16])), 2)
            b = int("".join(map(str, vec[16:24])), 2)
            
            # FIX: Structure matches JS 'item.vector' expectation
            payload.append({
                "id": ubp_id,
                "vector": [r, g, b] 
            })
            
    try:
        # Send to Main Thread
        json_str = json.dumps(payload)
        if hasattr(window, 'ubp_gpu_load_data'):
            window.ubp_gpu_load_data(json_str)
            print(f"[BRIDGE] ✅ {len(payload)} vectors loaded into V8 Accelerator.")
        else:
            print("[BRIDGE] ⚠️ window.ubp_gpu_load_data not found.")
    except Exception as e:
        print(f"[BRIDGE] ❌ Handshake Failed: {e}")

def query_bridge(text_input: str):
    """
    Hashes input to a 24-bit vector and queries the Main Thread 
    for the nearest geometric neighbor.
    """
    if not BRIDGE_ACTIVE: return None

    # 1. Hash Input to 24-bit Vector (RGB)
    h = hashlib.sha256(text_input.encode('utf-8')).hexdigest()
    val = int(h[:6], 16)
    r = (val >> 16) & 0xFF
    g = (val >> 8) & 0xFF
    b = val & 0xFF

    # 2. Call Main Thread
    try:
        if hasattr(window, 'ubp_gpu_compute'):
            # FIX: Pass 3 separate arguments to match JS (r, g, b) signature
            best_id = window.ubp_gpu_compute(r, g, b)
            
            if best_id and best_id != "UNKNOWN" and best_id != "ERR:NoData":
                entry = HEX_DB_EXACT.find_by_id(str(best_id))
                if entry:
                    res = entry.copy()
                    res['match_type'] = "GEOMETRIC_RESONANCE (V8)"
                    res['nrci'] = "1/1" 
                    return res
    except Exception as e:
        print(f"[BRIDGE] Compute Error: {e}")
    
    return None

# --- MAIN REFLEXIVE LOOP ---
def reflexive_recall(text, ai_vectors=None):
    print(f"[Cortex v13.2] Processing Input via Hybrid Bridge...")
    
    memories = []

    # 1. Fast Path: Direct IDs (Regex)
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        entry = HEX_DB_EXACT.find_by_id(uid)
        if entry:
            e = entry.copy()
            e['match_type'] = "DIRECT_ID_REF"
            memories.append(e)

    # 2. Geometric Path: V8 Accelerator
    geo_match = query_bridge(text)
    if geo_match:
        memories.append(geo_match)

    # 3. Deep Path: Delta Engine
    delta_result = DELTA.reason(text, max_steps=4)
    
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
        if sig not in seen_sig:
             final_list.append(m)
             seen_sig.add(sig)
    
    # 5. Output
    print(f"--- REFLEXIVE MEMORY: {len(final_list)} ENTRIES ---")
    print(json.dumps(final_list, indent=2))
    
    stats = DELTA.stats()
    print(f"[System] Context: {stats['context']['turns']} turns | Feedback: {stats['feedback_count']}")

# --- INITIALIZATION ---
# Initialize the Bridge immediately upon script load
initialize_gpu_bridge()

if __name__ == "__main__":
    u_input = globals().get('USER_INPUT', "What is the definition of entropy?")
    s_vectors = globals().get('SEARCH_VECTORS', [])
    reflexive_recall(u_input, s_vectors)
