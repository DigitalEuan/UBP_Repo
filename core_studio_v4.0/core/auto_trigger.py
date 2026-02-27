"""
UBP Auto-Trigger v17.2.2 (Patched)
==================================
FIX: Imports UBPBrain (not V3) from consolidated script.
Features:
1. PHRASE-LOCK SCANNING: Matches exact strings from Lexicon [Name] parts.
2. TRIADIC SCORING: Prioritizes Phrases > Math DNA > Keywords.
3. SOP_002 COMPLIANCE: Fully integrated with fingerprint-keyed KB.

Author: E R A Craig, New Zealand
Date: 27 Feb 2026
"""
import json
import sys
import re
import os
import hashlib
from typing import List, Dict, Any

# --- 1. SYSTEM INTEGRATION ---
try:
    # PATCH: Use UBPBrain, not UBPBrainV3
    from ubp_brain_consolidated import UBPBrain

    BRAIN = UBPBrain()
    # Load KB (try multiple paths)
    kb_paths = ['ubp_system_kb.json', 'ubp_system_kb_enriched.json']
    loaded = False
    for p in kb_paths:
        if os.path.exists(p):
            BRAIN.initialize([p])
            loaded = True
            break

    if not loaded:
        print("[Cortex] WARNING: No KB file found.")
        KB_DATA = {}
    else:
        # Access the KB dictionary directly
        KB_DATA = BRAIN.memory.kb

    # Build Reverse Map (ID -> Fingerprint/Key)
    ID_TO_KEY = {entry.get('ubp_id'): key for key, entry in KB_DATA.items() if entry.get('ubp_id')}

    # Build Phrase Map
    PHRASE_TO_KEY = {}
    for key, entry in KB_DATA.items():
        lex = entry.get('lexicon', '')
        if lex.startswith('['):
            name = lex.split('],')[0].strip('[')
            PHRASE_TO_KEY[name.lower()] = key

    print(f"[Cortex v17.2.2] Phrase-Lock Active. {len(PHRASE_TO_KEY)} Semantic Anchors.")

except Exception as e:
    print(f"[Cortex] CRITICAL ERROR: {e}")
    KB_DATA = {}
    PHRASE_TO_KEY = {}
    ID_TO_KEY = {}

# --- 2. HELPER FUNCTIONS ---

def parse_lexicon(lex_str: str) -> tuple:
    """Extracts [Name] and [Meaning] from SOP_002 Lexicon."""
    if not lex_str or not lex_str.startswith('['):
        return "Unknown", lex_str
    parts = lex_str.split('],')
    name = parts[0].strip('[') if len(parts) > 0 else "Unknown"
    meaning = parts[1].strip().strip('[') if len(parts) > 1 else lex_str
    if meaning.endswith(']'): meaning = meaning[:-1]
    return name, meaning

# --- 3. THE REFLEXIVE LOOP ---

def reflexive_recall(text: str):
    print(f"[Cortex] Scanning for Semantic Anchors...")
    memories = {} 
    input_lower = text.lower()

    # A. PHRASE-LOCK SCAN
    for phrase, key in PHRASE_TO_KEY.items():
        if phrase in input_lower:
            entry_obj = KB_DATA[key]
            memories[key] = {
                'data': entry_obj,
                'match_type': "PHRASE_LOCK",
                'score_boost': 2.0
            }

    # B. DIRECT ID SCAN
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        key = ID_TO_KEY.get(uid)
        if key and key not in memories:
            entry_obj = KB_DATA[key]
            memories[key] = {
                'data': entry_obj,
                'match_type': "DIRECT_ID",
                'score_boost': 1.5
            }

    # C. KEYWORD SCAN
    if len(memories) < 5:
        words = re.findall(r'\b\w{4,}\b', input_lower)
        for word in words:
            for key, entry_obj in KB_DATA.items():
                lex = entry_obj.get('lexicon', '').lower()
                uid = entry_obj.get('ubp_id', '').lower()
                if word in lex or word in uid:
                    if key not in memories:
                        memories[key] = {
                            'data': entry_obj,
                            'match_type': "KEYWORD",
                            'score_boost': 1.0
                        }
                if len(memories) > 15: break

    # --- 4. FORMAT FOR AI CONTEXT ---
    final_context = []
    sorted_memories = sorted(memories.values(), key=lambda x: x.get('score_boost', 0), reverse=True)

    for m in sorted_memories[:12]:
        entry = m['data']
        name, meaning = parse_lexicon(entry.get('lexicon', ''))

        # Handle nested atlas data
        atlas = entry.get('atlas', {})
        nrci = atlas.get('nrci', entry.get('nrci', '?'))

        ctx_entry = {
            "ubp_id": entry.get('ubp_id'),
            "name": name,
            "meaning": meaning,
            "math": entry.get('math'),
            "hierarchy": atlas.get('hierarchy', ''),
            "nrci": str(nrci),
            "match": m['match_type']
        }
        final_context.append(ctx_entry)

    print(f"--- CORTEX RECALL: {len(final_context)} ANCHORS INJECTED ---")
    return final_context

if __name__ == "__main__":
    q = "What is a Proton?"
    res = reflexive_recall(q)
    print(json.dumps(res, indent=2))
