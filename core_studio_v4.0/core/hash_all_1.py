import json

# Load the current KB
with open('ubp_system_kb.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

hash_memory = {}
collisions = 0

print(f"--- RE-INDEXING {len(kb)} ENTRIES ---")

for key, entry in kb.items():
    # Priority 1: Use the internal fingerprint field
    # Priority 2: Fallback to the dictionary key if it looks like a hash
    full_hash = entry.get("fingerprint")
    if not full_hash or len(full_hash) < 32:
        full_hash = key if len(key) >= 32 else None
        
    if full_hash:
        short_key = full_hash[:8]
        if short_key in hash_memory:
            collisions += 1
            # If collision, use a slightly longer key
            short_key = full_hash[:10]
            
        hash_memory[short_key] = {
            "ubp_id": entry.get("ubp_id", "UNK"),
            "full_hash": full_hash
        }
    else:
        print(f"  [!] Warning: Entry {entry.get('ubp_id')} has no valid fingerprint.")

# Save the corrected index
with open('ubp_hash_memory_kb_1.json', 'w', encoding='utf-8') as f:
    json.dump(hash_memory, f, indent=2)

print(f"✅ Indexing Complete.")
print(f"   Total KB Entries: {len(kb)}")
print(f"   Total Indexed:    {len(hash_memory)}")
print(f"   Collisions:       {collisions}")