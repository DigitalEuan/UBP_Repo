import json
import numpy as np

def calculate_layer_resonance(v1, v2):
    # Split into R, G, B layers (8 bits each)
    layers1 = [v1[0:8], v1[8:16], v1[16:24]]
    layers2 = [v2[0:8], v2[8:16], v2[16:24]]
    
    resonances = []
    for i in range(3):
        # Convert to bipolar (-1, 1)
        b1 = np.array([(x * 2) - 1 for x in layers1[i]])
        b2 = np.array([(x * 2) - 1 for x in layers2[i]])
        
        dot = np.dot(b1, b2)
        norm = np.linalg.norm(b1) * np.linalg.norm(b2)
        res = dot / norm if norm != 0 else 0
        resonances.append(res)
        
    return resonances

def run_layered_solubility_test():
    print("--- STUDY: CHROMATIC STRUCTURE OF MATTER (Phase 8.1 - Layered Resonance) ---")
    
    with open('ubp_system_kb.json', 'r') as f:
        kb = json.load(f)
    
    idx = {f: i for i, f in enumerate(kb["_fields"])}
    entries = kb["entries"]

    def get_vec(name_query):
        for e in entries.values():
            if name_query in e[idx['lexicon']]: return e[idx["vector"]]
        return None

    water_v = get_vec("Water")
    test_subjects = [
        {"name": "Ethanol", "expected": "Miscible"},
        {"name": "Ammonia", "expected": "Miscible"},
        {"name": "Methane", "expected": "Immiscible"}
    ]

    if water_v is None:
        print("❌ Error: Water vector not found.")
        return

    print(f"{'Subject':<12} | {'Red (Mass)':<10} | {'Green (Info)':<10} | {'Blue (Pot)':<10} | {'Result'}")
    print("-" * 65)

    results = []
    for sub in test_subjects:
        v_sub = get_vec(sub['name'])
        if v_sub is None: continue
        
        r_res, g_res, b_res = calculate_layer_resonance(water_v, v_sub)
        
        # Prediction Logic: If Green Resonance is high, they mix.
        prediction = "MISCIBLE" if g_res > 0.1 else "IMMISCIBLE"
        
        print(f"{sub['name']:<12} | {r_res:>10.2f} | {g_res:>10.2f} | {b_res:>10.2f} | {prediction}")
        
        results.append({
            "name": sub['name'],
            "green_resonance": g_res,
            "prediction": prediction,
            "accurate": prediction.upper() == sub['expected'].upper()
        })

    with open('layered_solubility_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_layered_solubility_test()