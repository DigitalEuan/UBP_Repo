"""
UBP Auto-Trigger v17.2.3 (SOP_002 Compliant)
============================================
FIX: Aligns with fingerprint-keyed Knowledge Base.
1. REVERSE MAPPING: Maps ubp_id -> SHA256 Fingerprint.
2. PHRASE-LOCK: Maps Lexicon [Names] -> Fingerprint.
3. ATLAS-AWARE: Correctly extracts nested metrics from entry['atlas'].

Author: E R A Craig & UBP Research Cortex v4.2.7
Date: 01 March 2026
"""
import json
import re
import os
from typing import List, Dict, Any

# --- 1. SYSTEM INTEGRATION ---
try:
    # We use the helper functions from the consolidated brain to ensure consistency
    from ubp_brain_consolidated import UBPBrain, extract_name, extract_nrci, is_belief

    BRAIN = UBPBrain()
    kb_path = 'ubp_system_kb.json'
    
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            KB_DATA = json.load(f)
        print(f"[Cortex] SOP_002 KB Loaded: {len(KB_DATA)} entries.")
    else:
        print("[Cortex] WARNING: ubp_system_kb.json not found.")
        KB_DATA = {}

    # BUILD REVERSE MAPS
    # We need to know which Fingerprint Key belongs to which UBP-ID
    ID_TO_KEY = {}
    PHRASE_TO_KEY = {}

    for key, entry in KB_DATA.items():
        uid = entry.get('ubp_id')
        if uid:
            ID_TO_KEY[uid] = key
        
        # Map the name in brackets [Water] to the key
        name = extract_name(entry)
        if name and name != "Unknown":
            PHRASE_TO_KEY[name.lower()] = key

    print(f"[Cortex] Reverse Maps Built. {len(ID_TO_KEY)} IDs, {len(PHRASE_TO_KEY)} Phrases.")

except Exception as e:
    print(f"[Cortex] CRITICAL INITIALIZATION ERROR: {e}")
    KB_DATA = {}
    ID_TO_KEY = {}
    PHRASE_TO_KEY = {}

# --- 2. THE REFLEXIVE LOOP ---

def reflexive_recall(text: str):
    """Scans input and returns relevant context for the AI."""
    memories = {} 
    input_lower = text.lower()

    # A. PHRASE-LOCK SCAN (Highest Priority)
    # Matches "Water", "Glucose", etc.
    for phrase, key in PHRASE_TO_KEY.items():
        if phrase in input_lower:
            memories[key] = {"data": KB_DATA[key], "match": "PHRASE", "boost": 2.0}

    # B. DIRECT ID SCAN (High Priority)
    # Matches "MOLECULE_H2O_001"
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        key = ID_TO_KEY.get(uid)
        if key and key not in memories:
            memories[key] = {"data": KB_DATA[key], "match": "ID", "boost": 1.5}

    # C. KEYWORD SCAN (Fallback)
    if len(memories) < 5:
        words = re.findall(r'\b\w{4,}\b', input_lower)
        for word in words:
            for key, entry in KB_DATA.items():
                if word in entry.get('lexicon', '').lower() or word in entry.get('ubp_id', '').lower():
                    if key not in memories:
                        memories[key] = {"data": entry, "match": "KEYWORD", "boost": 1.0}
                if len(memories) > 12: break

    # --- 3. FORMAT FOR AI CONTEXT ---
    final_context = []
    # Sort by boost score
    sorted_memories = sorted(memories.values(), key=lambda x: x['boost'], reverse=True)

    for m in sorted_memories[:12]:
        entry = m['data']
        atlas = entry.get('atlas', {})
        
        ctx_entry = {
            "ubp_id": entry.get('ubp_id'),
            "name": extract_name(entry),
            "math": entry.get('math'),
            "hierarchy": atlas.get('hierarchy', 'atomic'),
            "nrci": str(extract_nrci(entry)),
            "match_type": m['match']
        }
        final_context.append(ctx_entry)

    return final_context

if __name__ == "__main__":
    # Test the recall
    test_query = "Tell me about Water and ELEM_H_001"
    results = reflexive_recall(test_query)
    print(json.dumps(results, indent=2))