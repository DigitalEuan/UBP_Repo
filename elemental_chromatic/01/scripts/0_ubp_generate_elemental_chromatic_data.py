import json
import os

def generate_elemental_chromatic_data():
    print("--- UBP ELEMENTAL CHROMATIC EXPORT ---")
    
    kb_path = 'ubp_system_kb.json'
    if not os.path.exists(kb_path):
        print(f"❌ Error: {kb_path} not found.")
        return

    with open(kb_path, 'r') as f:
        kb_data = json.load(f)

    fields = kb_data["_fields"]
    idx = {f: i for i, f in enumerate(fields)}
    entries = kb_data["entries"]

    element_data = []

    for key, entry in entries.items():
        uid = entry[idx["ubp_id"]]
        if uid.startswith("ELEM_"):
            vector = entry[idx["vector"]]
            nrci = float(entry[idx["nrci_val"]])
            lexicon = entry[idx["lexicon"]]
            
            # Convert vector to hex address
            val = 0
            for bit in vector:
                val = (val << 1) | bit
            hex_color = f"{val:06x}"
            
            # Extract RGB channels
            r = (val >> 16) & 0xFF
            g = (val >> 8) & 0xFF
            b = val & 0xFF
            
            # Extract Z (Atomic Number)
            try:
                z = int(uid.split('_')[-1])
            except:
                z = 999
                
            # Extract clean name
            try:
                name = lexicon.split(']')[0].strip('[').split(':')[-1].strip()
            except:
                name = uid
                
            element_data.append({
                "z": z,
                "ubp_id": uid,
                "name": name,
                "hex_color": f"#{hex_color}",
                "rgb": {"r": r, "g": g, "b": b},
                "nrci": nrci,
                "vector": vector
            })

    # Sort by Atomic Number
    element_data.sort(key=lambda x: x["z"])

    # Save to JSON
    output_file = 'elemental_chromatic_data.json'
    with open(output_file, 'w') as f:
        json.dump(element_data, f, indent=2)

    print(f"✅ Exported {len(element_data)} elements to {output_file}")
    
    # Print a sample of the first 10 elements
    print(f"\n{'Z':<4} | {'ID':<12} | {'Hex Color':<10} | {'R':<3} {'G':<3} {'B':<3} | {'NRCI'}")
    print("-" * 55)
    for el in element_data[:10]:
        print(f"{el['z']:<4} | {el['ubp_id']:<12} | {el['hex_color']:<10} | {el['rgb']['r']:<3} {el['rgb']['g']:<3} {el['rgb']['b']:<3} | {el['nrci']:.4f}")

if __name__ == "__main__":
    generate_elemental_chromatic_data()