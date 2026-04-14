import json

KB_PATH = '/home/ubuntu/UBP_Repo/core_studio_v4.0/system_kb/ubp_system_kb.json'

with open(KB_PATH) as f:
    kb = json.load(f)

fields = kb.get('_fields', [])
entries = kb.get('entries', {})
print(f"Fields: {fields}")
print(f"Total entries: {len(entries)}")

# Show first 3 entries raw to understand structure
print("\n--- First 3 entries raw ---")
for i, (k, v) in enumerate(list(entries.items())[:3]):
    print(f"\nEntry {i+1} hash={k[:16]}...")
    print(f"  type={type(v).__name__}")
    if isinstance(v, list):
        for j, field in enumerate(fields):
            if j < len(v):
                print(f"  [{j}] {field}: {str(v[j])[:120]}")
    elif isinstance(v, dict):
        print(f"  keys: {list(v.keys())}")

# Now find element entries - look for ELEMENT tag or ELEM in ubp_id field
print("\n--- Searching for ELEMENT entries ---")
elem_entries = []
for hash_key, raw in entries.items():
    if isinstance(raw, list) and len(raw) >= len(fields):
        ubp_id = raw[0] if len(raw) > 0 else ''
        tags = raw[2] if len(raw) > 2 else []
        lexicon = raw[1] if len(raw) > 1 else ''
        
        is_element = (
            'ELEMENT' in (tags if isinstance(tags, list) else []) or
            str(ubp_id).startswith('ELEM_') or
            '[Element:' in str(lexicon)
        )
        
        if is_element:
            vector = raw[3] if len(raw) > 3 else []
            hw = sum(vector) if isinstance(vector, list) else 0
            nrci_val = raw[5] if len(raw) > 5 else 0
            tax_str = raw[6] if len(raw) > 6 else ''
            elem_entries.append({
                'hash': hash_key,
                'ubp_id': ubp_id,
                'lexicon': str(lexicon)[:120],
                'tags': tags,
                'vector': vector,
                'hamming_weight': hw,
                'nrci_val': nrci_val,
                'tax_str': tax_str
            })

print(f"Found {len(elem_entries)} element entries")
print("\nAll element entries:")
for e in sorted(elem_entries, key=lambda x: x['ubp_id']):
    print(f"  {e['ubp_id']} | HW={e['hamming_weight']} | NRCI={e['nrci_val']:.4f} | {e['lexicon'][:80]}")

# Save for use in studies
with open('/home/ubuntu/ubp_thermo_study/kb_elements.json', 'w') as f:
    json.dump(elem_entries, f, indent=2)
print(f"\nSaved to kb_elements.json")
