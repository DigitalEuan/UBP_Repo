"""
UBP Auto-Trigger v17.2 (Phrase-Lock Edition)
==============================================
Features:
1. PHRASE-LOCK SCANNING: Matches exact strings from Lexicon [Name] parts.
2. TRIADIC SCORING: Prioritizes Phrases > Math DNA > Keywords.
3. SOP_002 COMPLIANCE: Fully integrated with fingerprint-keyed KB.

Author: E R A Craig, New Zealand
Date: 20 Feb 2026
"""
import json
import sys
import re
import os
import hashlib
from typing import List, Dict, Any

# --- 1. SYSTEM INTEGRATION ---
try:
    from ubp_brain_consolidated import UBPBrain
    
    BRAIN = UBPBrain()
    BRAIN.initialize(['ubp_system_kb.json'])
    
    # Build Reverse Map (ID -> Fingerprint)
    ID_TO_FP = {v.get('ubp_id'): k for k, v in BRAIN.memory.kb.items() if v.get('ubp_id')}
    
    # Build Phrase Map (Full Lexicon Name -> Fingerprint)
    # This allows us to find "Informational Materialism" as a single unit
    PHRASE_TO_FP = {}
    for fp, entry in BRAIN.memory.kb.items():
        lex = entry.get('lexicon', '')
        if lex.startswith('['):
            name = lex.split('],')[0].strip('[')
            PHRASE_TO_FP[name.lower()] = fp

    print(f"[Cortex v17.2] Phrase-Lock Active. {len(PHRASE_TO_FP)} Semantic Anchors.")

except ImportError as e:
    print(f"[Cortex] CRITICAL ERROR: {e}")
    sys.exit(0)

# --- 2. HELPER FUNCTIONS ---

def parse_lexicon(lex_str: str) -> tuple:
    """Extracts [Name] and [Meaning] from SOP_002 Lexicon."""
    if not lex_str or not lex_str.startswith('['):
        return "Unknown", lex_str
    # Split by the first occurrence of '],'
    parts = lex_str.split('],')
    name = parts[0].strip('[') if len(parts) > 0 else "Unknown"
    meaning = parts[1].strip().strip('[') if len(parts) > 1 else lex_str
    # Remove trailing bracket if present
    if meaning.endswith(']'): meaning = meaning[:-1]
    return name, meaning

# --- 3. THE REFLEXIVE LOOP ---

def reflexive_recall(text: str):
    print(f"[Cortex] Scanning for Semantic Anchors...")
    memories = {} # Key = Fingerprint
    input_lower = text.lower()

    # A. PHRASE-LOCK SCAN (High Priority)
    # Checks if any full Lexicon Name exists in the user's query
    for phrase, fp in PHRASE_TO_FP.items():
        if phrase in input_lower:
            entry = BRAIN.memory.kb[fp].copy()
            entry['match_type'] = "PHRASE_LOCK"
            entry['score_boost'] = 2.0
            memories[fp] = entry

    # B. DIRECT ID SCAN (Regex)
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        fp = ID_TO_FP.get(uid)
        if fp and fp not in memories:
            entry = BRAIN.memory.kb[fp].copy()
            entry['match_type'] = "DIRECT_ID"
            entry['score_boost'] = 1.5
            memories[fp] = entry

    # C. MATH DNA SCAN (Hashing)
    if "=" in text or "|" in text:
        fp = hashlib.sha256(text.strip().encode()).hexdigest()
        if fp in BRAIN.memory.kb and fp not in memories:
            entry = BRAIN.memory.kb[fp].copy()
            entry['match_type'] = "MATH_DNA"
            entry['score_boost'] = 1.8
            memories[fp] = entry

    # D. KEYWORD SCAN (Lexicon Index)
    words = re.findall(r'\b\w{4,}\b', input_lower)
    for word in words:
        fps = BRAIN.memory.lexicon_index.get(word, [])
        for fp in fps:
            if fp not in memories:
                entry = BRAIN.memory.kb[fp].copy()
                entry['match_type'] = "KEYWORD"
                entry['score_boost'] = 1.0
                memories[fp] = entry

    # --- 4. FORMAT FOR AI CONTEXT ---
    final_context = []
    
    # Sort by boost (Phrases first)
    sorted_memories = sorted(memories.values(), key=lambda x: x.get('score_boost', 0), reverse=True)

    for m in sorted_memories[:12]: # Top 12
        name, meaning = parse_lexicon(m.get('lexicon', ''))
        atlas = m.get('atlas', {})
        
        ctx_entry = {
            "ubp_id": m.get('ubp_id'),
            "name": name,
            "meaning": meaning,
            "math": m.get('math'),
            "hierarchy": atlas.get('hierarchy'),
            "nrci": atlas.get('nrci'),
            "match": m.get('match_type')
        }
        final_context.append(ctx_entry)

    print(f"--- CORTEX RECALL: {len(final_context)} ANCHORS INJECTED ---")
    return final_context

if __name__ == "__main__":
    # Test with the specific phrase
    q = "What is Informational Materialism?"
    res = reflexive_recall(q)
    print(json.dumps(res, indent=2))