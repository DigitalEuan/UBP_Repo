import json

KB_PATH = '/home/ubuntu/UBP_Repo/core_studio_v4.0/system_kb/ubp_system_kb.json'

with open(KB_PATH) as f:
    kb = json.load(f)

# Each entry is a list: [id, description, tags, vector, ...]
entries = kb.get('entries', {})
fields = kb.get('_fields', [])
print(f"Fields: {fields}")
print(f"Total entries: {len(entries)}")

# Parse entries into structured dicts
def parse_entry(raw):
    """Parse a raw KB entry (list) into a structured dict using _fields."""
    if isinstance(raw, list) and len(raw) >= len(fields):
        d = {}
        for i, f in enumerate(fields):
            d[f] = raw[i]
        return d
    elif isinstance(raw, dict):
        return raw
    return {}

# Find all ELEM entries
elem_entries = []
for hash_key, raw in entries.items():
    parsed = parse_entry(raw)
    entry_id = parsed.get('id', '') if isinstance(parsed, dict) else (raw[0] if isinstance(raw, list) else '')
    if str(entry_id).startswith('ELEM_'):
        elem_entries.append({'hash': hash_key, 'id': entry_id, 'raw': raw, 'parsed': parsed})

print(f"\nTotal ELEM entries: {len(elem_entries)}")

# Show full schema of first ELEM entry
if elem_entries:
    e = elem_entries[0]
    print(f"\nFirst ELEM entry hash: {e['hash'][:16]}...")
    print(f"  ID: {e['id']}")
    print(f"  Raw (first 200 chars): {str(e['raw'])[:300]}")
    print(f"\nFields mapping:")
    for i, f in enumerate(fields):
        val = e['raw'][i] if isinstance(e['raw'], list) and i < len(e['raw']) else 'N/A'
        print(f"  [{i}] {f}: {str(val)[:100]}")

# List all elements
print(f"\nAll ELEM entries ({len(elem_entries)} total):")
for e in sorted(elem_entries, key=lambda x: x['id']):
    raw = e['raw']
    elem_id = raw[0] if isinstance(raw, list) else e['id']
    desc = raw[1][:80] if isinstance(raw, list) and len(raw) > 1 else ''
    vec = raw[3] if isinstance(raw, list) and len(raw) > 3 else []
    hw = sum(vec) if isinstance(vec, list) else '?'
    print(f"  {elem_id} | HW={hw} | {desc[:70]}")
