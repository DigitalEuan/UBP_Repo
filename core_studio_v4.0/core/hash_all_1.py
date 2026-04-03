"""
UBP HASH INDEXER v2.0
=====================
Generates a lightweight 'ubp_hash_memory_kb.json' index from the 
v9.9 Ultra-Compact Columnar database.

Author: UBP Research Cortex v4.2.7
Date: 03 April 2026
"""

import json
import os

def run_indexing():
    # 1. Identify the source (prefer the ultra-compact version)
    input_file = 'ubp_system_kb_v9_ultra.json'
    if not os.path.exists(input_file):
        input_file = 'ubp_system_kb.json'
        
    output_file = 'ubp_hash_memory_kb.json'
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Source file {input_file} not found.")
        return

    print(f"--- RE-INDEXING FROM {input_file} ---")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    hash_memory = {}
    collisions = 0
    
    # 2. Detect Format and Extract Entries
    if isinstance(data, dict) and "_fields" in data:
        # v9.9 Columnar Format
        fields = data["_fields"]
        idx_id = fields.index("ubp_id")
        entries = data["entries"]
        print(f"   Format: v9.9 Ultra-Compact Detected.")
    else:
        # Legacy Dictionary Format
        entries = data
        print(f"   Format: Legacy Dictionary Detected.")

    # 3. Build the Index
    for full_hash, entry in entries.items():
        # Get the ID based on format
        if isinstance(entry, list):
            uid = entry[idx_id]
        else:
            uid = entry.get("ubp_id", "UNK")
            
        short_key = full_hash[:8]
        
        # Handle potential collisions in the 8-char prefix
        if short_key in hash_memory and hash_memory[short_key]["ubp_id"] != uid:
            collisions += 1
            short_key = full_hash[:10] # Extend prefix to resolve
            
        hash_memory[short_key] = {
            "ubp_id": uid,
            "full_hash": full_hash
        }

    # 4. Save the Index
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hash_memory, f, indent=2)

    print(f"✅ Indexing Complete.")
    print(f"   Total Entries Indexed: {len(hash_memory)}")
    print(f"   Short-Hash Collisions: {collisions}")
    print(f"   Saved to: {output_file}")

if __name__ == "__main__":
    run_indexing()