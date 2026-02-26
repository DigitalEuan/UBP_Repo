"""
UBP Auto-Trigger v17.2.1 (Phrase-Lock Edition)
==============================================
FIX: Aligned with UBPBrainV3 class naming.
Features:
1. PHRASE-LOCK SCANNING: Matches exact strings from Lexicon [Name] parts.
2. TRIADIC SCORING: Prioritizes Phrases > Math DNA > Keywords.
3. SOP_002 COMPLIANCE: Fully integrated with fingerprint-keyed KB.

Author: E R A Craig, New Zealand
Date: 25 Feb 2026
"""
import json
import sys
import re
import os
import hashlib
from typing import List, Dict, Any

# --- 1. SYSTEM INTEGRATION ---
try:
    # Import the correct class name from your consolidated brain
    from ubp_brain_consolidated import UBPBrainV3
    
    BRAIN = UBPBrainV3()
    BRAIN.load('ubp_system_kb.json')
    
    # Access the KB dictionary (keyed by fingerprint in SOP_002)
    KB_DATA = BRAIN.kb.by_fingerprint
    
    # Build Reverse Map (ID -> Fingerprint) for Direct ID lookups
    ID_TO_FP = {entry.ubp_id: fp for fp, entry in KB_DATA.items() if entry.ubp_id}
    
    # Build Phrase Map (Full Lexicon Name -> Fingerprint)
    # This allows us to find "Informational Materialism" as a single unit
    PHRASE_TO_FP = {}
    for fp, entry in KB_DATA.items():
        lex = entry.lexicon
        if lex.startswith('['):
            name = lex.split('],')[0].strip('[')
            PHRASE_TO_FP[name.lower()] = fp

    print(f"[Cortex v17.2.1] Phrase-Lock Active. {len(PHRASE_TO_FP)} Semantic Anchors.")

except ImportError as e:
    print(f"[Cortex] CRITICAL ERROR: {e}")
    # Fallback to prevent system crash, though recall will be limited
    KB_DATA = {}
    PHRASE_TO_FP = {}
    ID_TO_FP = {}

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
    for phrase, fp in PHRASE_TO_FP.items():
        if phrase in input_lower:
            entry_obj = KB_DATA[fp]
            memories[fp] = {
                'data': entry_obj,
                'match_type': "PHRASE_LOCK",
                'score_boost': 2.0
            }

    # B. DIRECT ID SCAN (Regex)
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        fp = ID_TO_FP.get(uid)
        if fp and fp not in memories:
            entry_obj = KB_DATA[fp]
            memories[fp] = {
                'data': entry_obj,
                'match_type': "DIRECT_ID",
                'score_boost': 1.5
            }

    # C. MATH DNA SCAN (Hashing)
    if "=" in text or "|" in text:
        # Attempt to see if the user provided raw Math DNA
        fp = hashlib.sha256(text.strip().encode()).hexdigest()
        if fp in KB_DATA and fp not in memories:
            entry_obj = KB_DATA[fp]
            memories[fp] = {
                'data': entry_obj,
                'match_type': "MATH_DNA",
                'score_boost': 1.8
            }

    # D. KEYWORD SCAN (Lexicon Search)
    # Only scan if we haven't found too many high-priority matches
    if len(memories) < 5:
        words = re.findall(r'\b\w{4,}\b', input_lower)
        for word in words:
            for fp, entry_obj in KB_DATA.items():
                if word in entry_obj.lexicon.lower() or word in entry_obj.ubp_id.lower():
                    if fp not in memories:
                        memories[fp] = {
                            'data': entry_obj,
                            'match_type': "KEYWORD",
                            'score_boost': 1.0
                        }
                if len(memories) > 15: break # Cap search

    # --- 4. FORMAT FOR AI CONTEXT ---
    final_context = []
    
    # Sort by boost (Phrases first)
    sorted_memories = sorted(memories.values(), key=lambda x: x.get('score_boost', 0), reverse=True)

    for m in sorted_memories[:12]: # Top 12
        entry = m['data']
        name, meaning = parse_lexicon(entry.lexicon)
        
        ctx_entry = {
            "ubp_id": entry.ubp_id,
            "name": name,
            "meaning": meaning,
            "math": entry.math,
            "hierarchy": entry.hierarchy,
            "nrci": str(entry.nrci),
            "match": m['match_type']
        }
        final_context.append(ctx_entry)

    print(f"--- CORTEX RECALL: {len(final_context)} ANCHORS INJECTED ---")
    return final_context

if __name__ == "__main__":
    # Test with a known concept
    q = "What is a Proton?"
    res = reflexive_recall(q)
    print(json.dumps(res, indent=2))