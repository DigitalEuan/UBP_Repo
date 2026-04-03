"""
UBP Auto-Trigger v19.1 (Ultra-Compact Compatible)
=================================================
Fixed IndexError in synth_context by separating Metadata Fields 
from MOG Tensor Categories.

Author: UBP Research Cortex v4.2.7
Date: 03 April 2026
"""

import json
import re
import os
from ubp_kb_architect import MOG_CATEGORIES

# 1. CONFIGURATION
KB_FILE = 'ubp_system_kb_v9_ultra.json'
if not os.path.exists(KB_FILE):
    KB_FILE = 'ubp_system_kb.json'

def load_compact_kb(path):
    if not os.path.exists(path):
        return None, None, {}
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and "_fields" in data:
        fields = data["_fields"]
        entries = data["entries"]
        idx_map = {f: i for i, f in enumerate(fields)}
        return fields, idx_map, entries
    return None, None, data

# 2. INITIALIZE DATA
FIELDS, IDX, ENTRIES = load_compact_kb(KB_FILE)

# 3. BUILD RECALL INDEXES
ID_TO_KEY = {}
PHRASE_TO_KEY = {}
TAG_TO_KEYS = {}

if ENTRIES:
    print(f"[Cortex] Indexing {len(ENTRIES)} entries from {KB_FILE}...")
    for key, entry in ENTRIES.items():
        if IDX:
            uid = entry[IDX["ubp_id"]]
            lex = entry[IDX["lexicon"]]
            tags = entry[IDX["tags"]]
        else:
            uid = entry.get("ubp_id", "UNK")
            lex = entry.get("lexicon", "")
            tags = entry.get("tags", [])

        ID_TO_KEY[uid] = key
        
        # Index Name from Lexicon
        try:
            name_match = re.search(r'\[(.*?)\]', lex)
            if name_match:
                name = name_match.group(1).split(':')[-1].strip().lower()
                PHRASE_TO_KEY[name] = key
        except: pass

        # Index Tags
        for tag in tags:
            t = tag.upper()
            if t not in TAG_TO_KEYS: TAG_TO_KEYS[t] = []
            TAG_TO_KEYS[t].append(key)

# 4. RECALL LOGIC
def reflexive_recall(query: str):
    query_clean = query.lower()
    results = {}

    # A. Direct ID Match
    ids_found = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', query)
    for uid in ids_found:
        if uid in ID_TO_KEY:
            results[uid] = ENTRIES[ID_TO_KEY[uid]]

    # B. Phrase Match
    for phrase, key in PHRASE_TO_KEY.items():
        if phrase in query_clean:
            uid = ENTRIES[key][IDX["ubp_id"]] if IDX else ENTRIES[key]["ubp_id"]
            results[uid] = ENTRIES[key]

    # C. Linguistic Tag Match
    words = re.findall(r'\b[a-zA-Z]{5,}\b', query_clean)
    for word in words:
        w_up = word.upper()
        if w_up in TAG_TO_KEYS:
            for key in TAG_TO_KEYS[w_up]:
                uid = ENTRIES[key][IDX["ubp_id"]] if IDX else ENTRIES[key]["ubp_id"]
                if uid not in results:
                    results[uid] = ENTRIES[key]
    return results

# 5. CONTEXT SYNTHESIS
def synth_context(recall_dict: dict) -> str:
    if not recall_dict: return "[No relevant UBP context found]"
    
    lines = ["=== UBP Geometric Context ==="]
    for uid, entry in list(recall_dict.items())[:10]:
        if IDX:
            lex = entry[IDX["lexicon"]]
            mog = entry[IDX["mog_tensor"]]
            # FIX: Use MOG_CATEGORIES (length 24) to index the mog_tensor
            active_cats = []
            if isinstance(mog, list):
                for i, val in enumerate(mog):
                    if val != 0 and i < len(MOG_CATEGORIES):
                        active_cats.append(MOG_CATEGORIES[i])
            
            lines.append(f"• {uid}: {lex}")
            if active_cats:
                lines.append(f"  [MOG Active]: {', '.join(active_cats)}")
        else:
            lines.append(f"• {uid}: {entry.get('lexicon')}")
    
    lines.append("=== End Context ===")
    return "\n".join(lines)

# --- TEST ---
if __name__ == "__main__":
    test_query = "Tell me about the stability of Hydrogen and Ammonia"
    found = reflexive_recall(test_query)
    print(synth_context(found))