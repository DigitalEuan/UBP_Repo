"""
UBP Auto-Trigger v19.2 (Ultra-Compact Compatible + KB v4.0 migration)
=====================================================================
Fixed IndexError in synth_context by separating Metadata Fields
from MOG Tensor Categories.

MIGRATION 2026-07-09 (v4.0):
- The legacy `ubp_system_kb.json` has been replaced by the four new
  system_kb files (elements/language_words/math/physics_law.json).
- `system_kb/legacy_adapter.py` provides a drop-in v9.9 view of those four
  files. We use it to materialise a v9.9-shaped `ubp_system_kb_v4_merged.json`
  on disk and load that — keeps the existing positional-list code path intact.

Author: UBP Research Cortex v4.2.7
Date: 03 April 2026 (original)  |  2026-07-09 (v4.0 migration)
"""

import json
import re
import os
import sys
from ubp_kb_architect import MOG_CATEGORIES

# 1. CONFIGURATION
# MIGRATION v4.0: locate the merged v9.9 KB produced by the legacy_adapter.
# Resolution order:
#   (a) $UBP_SYSTEM_KB_DIR/ubp_system_kb_v4_merged.json
#   (b) ./system_kb/ubp_system_kb_v4_merged.json  (CWD fallback)
#   (c) <this file's parent>/../system_kb/ubp_system_kb_v4_merged.json
#   (d) ./ubp_system_kb.json  (last-resort legacy filename for old deployments)
def _resolve_kb_file():
    env_dir = os.environ.get('UBP_SYSTEM_KB_DIR')
    candidates = []
    if env_dir:
        candidates.append(os.path.join(env_dir, 'ubp_system_kb_v4_merged.json'))
    candidates.append(os.path.join('system_kb', 'ubp_system_kb_v4_merged.json'))
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(here, '..', 'system_kb', 'ubp_system_kb_v4_merged.json'))
    candidates.append('ubp_system_kb.json')  # legacy filename fallback
    for c in candidates:
        if c and os.path.exists(c):
            return c
    # If none exist, try to materialise via the adapter
    try:
        sys.path.insert(0, os.path.join(here, '..', 'system_kb'))
        from legacy_adapter import ensure_legacy_kb_on_disk as _ensure
        return str(_ensure())
    except Exception:
        return candidates[0]  # will report missing

KB_FILE = _resolve_kb_file()

def load_compact_kb(path):
    if not path or not os.path.exists(path):
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