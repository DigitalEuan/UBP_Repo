import json
import numpy as np

def calculate_layer_resonance(v1, v2):
    layers1 = [v1[0:8], v1[8:16], v1[16:24]]
    layers2 = [v2[0:8], v2[8:16], v2[16:24]]
    resonances = []
    for i in range(3):
        b1 = np.array([(x * 2) - 1 for x in layers1[i]])
        b2 = np.array([(x * 2) - 1 for x in layers2[i]])
        dot = np.dot(b1, b2)
        norm = np.linalg.norm(b1) * np.linalg.norm(b2)
        resonances.append(dot / norm if norm != 0 else 0)
    return resonances

def run_full_resonance_scan():
    print("--- STUDY: CHROMATIC STRUCTURE OF MATTER (Phase 9 - Full Resonance Map) ---")
    
    with open('ubp_system_kb.json', 'r') as f:
        kb = json.load(f)
    
    idx = {f: i for i, f in enumerate(kb["_fields"])}
    entries = kb["entries"]

    # 1. Identify Reference (Water)
    water_v = next((e[idx["vector"]] for e in entries.values() if "MOLECULE_H2O_001" == e[idx["ubp_id"]]), None)
    if not water_v:
        print("❌ Error: Water vector not found.")
        return

    # 2. Scan all Hardened Molecules
    results = []
    for fp, e in entries.items():
        uid = e[idx["ubp_id"]]
        if uid.startswith("MOLECULE_") and "HARDENED" in e[idx["tags"]]:
            v_sub = e[idx["vector"]]
            r_res, g_res, b_res = calculate_layer_resonance(water_v, v_sub)
            
            # Composite Score: Weighted toward Green (Information/Interface)
            composite = (r_res * 0.2) + (g_res * 0.6) + (b_res * 0.2)
            
            results.append({
                "id": uid,
                "name": e[idx["lexicon"]].split(',')[0],
                "r": round(r_res, 3),
                "g": round(g_res, 3),
                "b": round(b_res, 3),
                "composite": round(composite, 3)
            })

    # 3. Sort by Composite Resonance
    results.sort(key=lambda x: x['composite'], reverse=True)

    print(f"{'Molecule':<25} | {'Red':<6} | {'Green':<6} | {'Blue':<6} | {'Composite'}")
    print("-" * 65)
    for r in results[:15]: # Show top 15
        print(f"{r['name'][:25]:<25} | {r['r']:>6.2f} | {r['g']:>6.2f} | {r['b']:>6.2f} | {r['composite']:>6.2f}")

    with open('full_chromatic_resonance_map.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Scan complete. {len(results)} molecules mapped to 'full_chromatic_resonance_map.json'.")

if __name__ == "__main__":
    run_full_resonance_scan()