"""
UBP Auto-Trigger v7.2 (Reflexive Cortex + FOM Integrated)
1. Ingests AI-Identified 'SEARCH_VECTORS'.
2. Checks FOM (Frame of Mind) State.
3. Scans for Gravitational Core.
4. Performs adaptive Hamming Distance scan.
"""
import re
import json
import sys
import os
import hashlib

# --- CONTEXT DETECTION ---
active_context = []

# 1. Check Gravitational Reasoning
if os.path.exists("ubp_gravitational_reasoning.py"):
    active_context.append("GRAVITATIONAL REASONING: ONLINE (Available for import)")

# 2. Check Frame of Mind
try:
    from ubp_fom_system import FOM_MANAGER
    frame = FOM_MANAGER.get_active_frame()
    if frame:
        active_context.append(f"ACTIVE FOM: {frame.frame_id} (Bias: {frame.base_nrci})")
        if frame.description:
            active_context.append(f"FOM DESC: {frame.description}")
except ImportError:
    pass

if active_context:
    print("--- SYSTEM CONTEXT ---")
    for ctx in active_context: print(f">> {ctx}")
    print("----------------------")


def get_hamming_distance(h1, h2):
    try:
        n1 = int(h1, 16); n2 = int(h2, 16)
        return bin(n1 ^ n2).count('1')
    except: return 999

def generate_fingerprint(math, lang, script):
    raw = f"{math}|{lang}|{script}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

# --- HYDRATE KERNEL ---
try:
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    if not HEX_DB_EXACT.registry:
        print("[Reflexive Cortex] Loading 2MB HexDB...")
        HEX_DB_EXACT.load_memory()
except ImportError:
    print("[Reflexive Cortex] HexDB offline.")
    sys.exit(0)

def vector_scan(text):
    seeds = [] # (Fingerprint, SourceType, Label)

    # 1. PROCESS AI VECTORS (Priority 1)
    if 'SEARCH_VECTORS' in globals():
        for vec in SEARCH_VECTORS:
            if isinstance(vec, dict):
                # Type A: Structured Vector
                if vec.get('math') or vec.get('language'):
                    m = vec.get('math', '0')
                    l = vec.get('language', 'None')
                    s = vec.get('script', 'None')
                    fp = generate_fingerprint(m, l, s)
                    seeds.append((fp, "AI_VECTOR", f"{m}|{l}"))
                
                # Type B: Concept Keyword
                if vec.get('keyword'):
                    kw = vec['keyword'].lower()
                    # Scan for this keyword in DB
                    for fp, entry in HEX_DB_EXACT.registry.items():
                        entry_str = (str(entry.get('name','')) + " " + " ".join(entry.get('tags',[]))).lower()
                        if kw in entry_str:
                            seeds.append((fp, "AI_KEYWORD", kw))
                            break # Only one seed per keyword to avoid flooding

    # 2. FALLBACK: RAW TEXT SCAN (Priority 2)
    if not seeds and text:
        math_candidates = re.findall(r'(\d+/\d+|\d+\.\d+|0|1)', text)
        lang_candidates = [w for w in re.findall(r'[A-Z][a-z]+(?:-[A-Z][a-z]+)*', text) if len(w)>3]
        
        for m in (math_candidates + ["0"])[:2]:
            for l in (lang_candidates + ["None"])[:3]:
                fp = generate_fingerprint(m, l, "None")
                if fp in HEX_DB_EXACT.registry:
                    seeds.append((fp, "RAW_VECTOR", f"{m}|{l}"))
    
    # 3. GEOMETRIC CLUSTER (Hamming Expansion)
    final_cluster = []
    seen_ids = set()

    for seed_fp, source, label in seeds:
        # Add Seed
        if seed_fp in HEX_DB_EXACT.registry:
            seed_entry = HEX_DB_EXACT.registry[seed_fp]
            if seed_entry['ubp_id'] not in seen_ids:
                seed_entry['match_type'] = source
                final_cluster.append(seed_entry)
                seen_ids.add(seed_entry['ubp_id'])

        # Scan for Neighbors
        candidates = []
        for fp, entry in HEX_DB_EXACT.registry.items():
            if fp == seed_fp: continue
            dist = get_hamming_distance(seed_fp, fp)
            candidates.append((dist, entry))
        
        # Sort by distance, take Top 12 (Adaptive)
        candidates.sort(key=lambda x: x[0])
        for dist, entry in candidates[:12]:
            if entry['ubp_id'] not in seen_ids:
                entry['match_type'] = f"HAMMING_NEIGHBOR ({dist})"
                entry['linked_to'] = label
                final_cluster.append(entry)
                seen_ids.add(seed_entry['ubp_id'])

    # 4. OUTPUT
    if final_cluster:
        print(f"--- REFLEXIVE MEMORY: {len(final_cluster)} ENTRIES ---")
        print(json.dumps(final_cluster, indent=2))
    elif seeds:
        print(f"[Reflexive Cortex] Vectors identified but no neighbors found.")

if 'USER_INPUT' in globals():
    vector_scan(USER_INPUT)
