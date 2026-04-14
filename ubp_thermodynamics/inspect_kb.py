import json

KB_PATH = '/home/ubuntu/UBP_Repo/core_studio_v4.0/system_kb/ubp_system_kb.json'

with open(KB_PATH) as f:
    kb = json.load(f)

print("Top-level keys:", list(kb.keys()))

# Inspect entries
entries = kb.get('entries', {})
print(f"'entries' type: {type(entries).__name__}")
if isinstance(entries, dict):
    print(f"  Number of entries: {len(entries)}")
    # Show first few keys
    keys = list(entries.keys())[:5]
    print(f"  First 5 keys: {keys}")
    # Show structure of first entry
    first_key = list(entries.keys())[0]
    print(f"\nFirst entry ({first_key}):")
    print(json.dumps(entries[first_key], indent=2)[:500])
elif isinstance(entries, list):
    print(f"  Number of entries: {len(entries)}")
    print(f"\nFirst entry:")
    print(json.dumps(entries[0], indent=2)[:500])

# Find ELEM entries
def find_elem_entries(obj):
    results = []
    if isinstance(obj, dict):
        if str(obj.get('id', '')).startswith('ELEM_'):
            results.append(obj)
        for v in obj.values():
            results.extend(find_elem_entries(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_elem_entries(item))
    return results

elems = find_elem_entries(kb)
print(f"\nTotal ELEM entries found: {len(elems)}")
for e in sorted(elems, key=lambda x: x.get('id','')):
    data = e.get('data', {})
    print(f"  {e.get('id','?')} | {e.get('title','?')} | HW={data.get('hamming_weight','?')} | Z={data.get('atomic_number','?')}")
