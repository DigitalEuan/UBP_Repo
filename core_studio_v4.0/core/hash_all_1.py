"""
UBP HASH INDEXER v3.1 (Universal Merged Edition + KB v4.0 migration)
=====================================================================
Generates a unified 'ubp_hash_memory_kb.json' index from all active
Knowledge Base files.

MIGRATION 2026-07-09 (v4.0):
- The legacy `ubp_system_kb.json` and `ubp_lang_kb_combined_v4.json` have
  been REPLACED by the four new system_kb files (elements/language_words/
  math/physics_law.json). `system_kb/legacy_adapter.py` materialises a
  merged v9.9 view of those four files at `ubp_system_kb_v4_merged.json`.
- This indexer now prefers the merged v9.9 file. If unavailable, it falls
  back to the legacy filenames.

Author: E R A Craig, New Zealand  and the UBP Research Cortex v4.2.7
Date: 07 April 2026 (original)  |  2026-07-09 (v4.0 migration)
"""

import json
import os
import sys

def _resolve_kb_files():
    """Return list of KB file paths to index. Prefer the merged v9.9 file
    produced by the legacy_adapter; fall back to legacy filenames."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, '..', 'system_kb', 'ubp_system_kb_v4_merged.json'),
        os.path.join('system_kb', 'ubp_system_kb_v4_merged.json'),
        'ubp_system_kb_v4_merged.json',
        'ubp_system_kb.json',                       # legacy fallback
        'ubp_lang_kb_combined_v4.json',             # legacy fallback
    ]
    env_dir = os.environ.get('UBP_SYSTEM_KB_DIR')
    if env_dir:
        candidates.insert(0, os.path.join(env_dir, 'ubp_system_kb_v4_merged.json'))
    found = [c for c in candidates if c and os.path.exists(c)]
    if not found:
        # Try to materialise via the adapter
        try:
            sys.path.insert(0, os.path.join(here, '..', 'system_kb'))
            from legacy_adapter import ensure_legacy_kb_on_disk as _ensure
            found = [str(_ensure())]
        except Exception:
            pass
    return found

def run_indexing():
    # 1. Configuration: Define all KB files to be indexed
    kb_files = _resolve_kb_files()
    output_file = 'ubp_hash_memory_kb_1.json'

    hash_memory = {}
    total_processed = 0
    collisions_resolved = 0

    print("--- UBP UNIVERSAL INDEXING START ---")
    if not kb_files:
        print("⚠️  No KB files found to index.")
        return

    for f_path in kb_files:
        if not os.path.exists(f_path):
            print(f"⚠️  Skipping: {f_path} (File not found)")
            continue

        print(f"🔍 Processing: {f_path}...")

        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {f_path}: {e}")
            continue

        # 2. Detect Format and Extract Entries
        entries_to_index = {}
        idx_id = None

        if isinstance(data, dict) and "_fields" in data:
            # v9.9 Ultra-Compact Columnar Format
            fields = data["_fields"]
            if "ubp_id" in fields:
                idx_id = fields.index("ubp_id")
                entries_to_index = data.get("entries", {})
                print(f"   Format: v9.9 Columnar detected ({len(entries_to_index)} entries)")
        elif isinstance(data, dict) and isinstance(data.get("entries"), list):
            # New schema: { _meta, entries: [entry_dict, ...] }
            entries_to_index = {e.get("fingerprint", str(i)): e for i, e in enumerate(data["entries"])}
            print(f"   Format: New-schema list detected ({len(entries_to_index)} entries)")
        elif isinstance(data, dict):
            # Legacy Dictionary Format
            entries_to_index = data
            print(f"   Format: Legacy Dictionary detected ({len(entries_to_index)} entries)")
        else:
            print(f"   Format: Unknown/Unsupported for {f_path}")
            continue

        # 3. Build the Index
        for full_hash, entry in entries_to_index.items():
            # Extract the UBP ID based on format
            if isinstance(entry, list) and idx_id is not None:
                uid = entry[idx_id]
            elif isinstance(entry, dict):
                uid = entry.get("ubp_id", "UNK")
            else:
                continue

            # Generate short key (8 chars)
            short_key = full_hash[:8]

            # 4. Collision Resolution Logic
            if short_key in hash_memory and hash_memory[short_key]["ubp_id"] != uid:
                collisions_resolved += 1
                short_key = full_hash[:12]

            hash_memory[short_key] = {
                "ubp_id": uid,
                "full_hash": full_hash
            }
            total_processed += 1

    # 5. Save the Unified Index
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(hash_memory, f, indent=2)

        print("\n" + "="*40)
        print(f"✅ INDEXING COMPLETE")
        print(f"   Total Entries Processed: {total_processed}")
        print(f"   Unique Index Keys:       {len(hash_memory)}")
        print(f"   Collisions Resolved:     {collisions_resolved}")
        print(f"   Saved to:                {output_file}")
        print("="*40)
    except Exception as e:
        print(f"❌ Failed to save index: {e}")

if __name__ == "__main__":
    run_indexing()