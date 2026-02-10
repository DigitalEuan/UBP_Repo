"""
UBP Auto-Trigger v14.0 (Acoustic-Integrated)
============================================
Updates:
1. ACOUSTIC PATH: Triggers AcousticCortex logic on vibrational keywords.
2. RESONANCE PULL: Automatically resolves dissonant queries toward harmony.
3. HYBRID CONTEXT: Merges Regex, Delta, Geometric, and Acoustic results.

Author: E R A Craig, New Zealand
UBP Research Cortex v4.2.7
Date: 11 Feb 2026
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
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
    
    # New Acoustic Integration
    try:
        from ubp_acoustic_cortex import AcousticCortex
        HAS_ACOUSTIC = True
    except ImportError:
        HAS_ACOUSTIC = False

    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()

except ImportError as e:
    print(f"[Reflexive Cortex] CRITICAL IMPORT ERROR: {e}")
    sys.exit(0)

# --- SINGLETON DELTA ENGINE ---
if "GLOBAL_DELTA_ENGINE" not in globals():
    GLOBAL_DELTA_ENGINE = DeltaReasoningEngine()
    kb_files = ["ubp_system_kb.json", "ubp_hash_memory_kb.json"]
    lexicon_file = "ubp_lexicon_v2_defs.json" if os.path.exists("ubp_lexicon_v2_defs.json") else "ubp_lexicon_v2.json"
    GLOBAL_DELTA_ENGINE.initialize(kb_files, lexicon_file)

DELTA = globals().get("GLOBAL_DELTA_ENGINE", GLOBAL_DELTA_ENGINE)

# --- MODULE 1: THE REFLEXIVE BRIDGE ---
def initialize_gpu_bridge():
    if not BRIDGE_ACTIVE: return
    payload = []
    for uid, entry in HEX_DB_EXACT.registry.items():
        vec = entry.get('vector')
        ubp_id = entry.get('ubp_id')
        if vec and len(vec) == 24 and ubp_id:
            r = int("".join(map(str, vec[0:8])), 2)
            g = int("".join(map(str, vec[8:16])), 2)
            b = int("".join(map(str, vec[16:24])), 2)
            payload.append({"id": ubp_id, "vector": [r, g, b]})
    try:
        json_str = json.dumps(payload)
        if hasattr(window, 'ubp_gpu_load_data'):
            window.ubp_gpu_load_data(json_str)
    except Exception: pass

def query_bridge_by_vector(vector: List[int]):
    """Queries V8 Accelerator using a raw 24-bit vector."""
    if not BRIDGE_ACTIVE: return None
    r = int("".join(map(str, vector[0:8])), 2)
    g = int("".join(map(str, vector[8:16])), 2)
    b = int("".join(map(str, vector[16:24])), 2)
    try:
        best_id = window.ubp_gpu_compute(r, g, b)
        if best_id and best_id not in ["UNKNOWN", "ERR:NoData"]:
            return HEX_DB_EXACT.find_by_id(str(best_id))
    except Exception: pass
    return None

# --- MAIN REFLEXIVE LOOP ---
def reflexive_recall(text, ai_vectors=None):
    print(f"[Cortex v14.0] Processing Input via Acoustic-Hybrid Bridge...")
    memories = []

    # 1. Fast Path: Direct IDs (Regex)
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        entry = HEX_DB_EXACT.find_by_id(uid)
        if entry:
            e = entry.copy()
            e['match_type'] = "DIRECT_ID_REF"
            memories.append(e)

    # 2. Acoustic Path: Vibrational Context
    acoustic_keywords = ['frequency', 'sound', 'vibration', 'harmony', 'pitch', 'acoustic', 'resonance', 'chord', 'tone']
    if HAS_ACOUSTIC and any(kw in text.lower() for kw in acoustic_keywords):
        print("  [!] Acoustic Context Detected. Initializing Resonance Pull...")
        ac = AcousticCortex()
        # Extract potential pitch (default to C/0 if not found)
        pitch_match = re.search(r'pitch\s*(\d+)', text.lower())
        p = int(pitch_match.group(1)) if pitch_match else 0
        
        # Encode and Resolve
        raw_v = ac.encode_vibration(pitch=p)
        resolved_v, pull = ac.resonance_pull(raw_v)
        
        # Query resolved vector
        geo_match = query_bridge_by_vector(resolved_v)
        if geo_match:
            e = geo_match.copy()
            e['match_type'] = f"ACOUSTIC_RESONANCE (Pull: {pull})"
            memories.append(e)

    # 3. Geometric Path: Standard V8 Accelerator
    h = hashlib.sha256(text.encode('utf-8')).hexdigest()
    val = int(h[:6], 16)
    std_v = [(val >> i) & 1 for i in range(23, -1, -1)]
    geo_match = query_bridge_by_vector(std_v)
    if geo_match:
        e = geo_match.copy()
        e['match_type'] = "GEOMETRIC_RESONANCE (V8)"
        memories.append(e)

    # 4. Deep Path: Delta Engine
    delta_result = DELTA.reason(text, max_steps=4)
    for step in delta_result.get('steps', []):
        mem_entry = {
            "ubp_id": "DELTA_RECALL",
            "name": "Contextual Memory",
            "language": step.get('content', ''),
            "domain": step.get('domain', 'UNKNOWN'),
            "nrci": f"{step.get('coherence', 0.5):.2f}",
            "match_type": f"DELTA_{step.get('source', 'ASSOC').upper()}"
        }
        memories.append(mem_entry)

    # 5. Merge & Deduplicate
    seen_sig = set()
    final_list = []
    if delta_result.get('response'):
        final_list.append({
            "ubp_id": "SYS_DELTA_SYNTHESIS",
            "name": "Delta Synthesis",
            "language": delta_result['response'],
            "match_type": "SYNTHESIS_OUTPUT",
            "nrci": "1/1"
        })

    for m in memories:
        sig = m.get('ubp_id', '') + m.get('language', '')[:30]
        if sig not in seen_sig:
             final_list.append(m)
             seen_sig.add(sig)
    
    print(f"--- REFLEXIVE MEMORY: {len(final_list)} ENTRIES ---")
    print(json.dumps(final_list, indent=2))

# --- INITIALIZATION ---
initialize_gpu_bridge()

if __name__ == "__main__":
    u_input = globals().get('USER_INPUT', "What is the frequency of harmony?")
    reflexive_recall(u_input)
