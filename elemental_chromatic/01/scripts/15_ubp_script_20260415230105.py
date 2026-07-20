import json
import numpy as np
from core import BinaryLinearAlgebra

def run_hub_analysis():
    print("--- UBP v7.2: CHROMATIC RESONANCE HUB ANALYSIS ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)

    hub_data = []
    
    # 1. Calculate Connectivity (Degree) for each node
    for i, el_a in enumerate(elements):
        links = 0
        total_hamming_dist = 0
        
        for j, el_b in enumerate(elements):
            if i == j: continue
            dist = BinaryLinearAlgebra.hamming_distance(el_a['vector'], el_b['vector'])
            if dist <= 8:
                links += 1
                total_hamming_dist += dist
        
        # 2. Calculate "Topological Torque" 
        # Tension = (Physical RGB Distance from Origin) / (Substrate Stability)
        r, g, b = el_a['rgb']['r'], el_a['rgb']['g'], el_a['rgb']['b']
        phys_dist = np.sqrt((r-128)**2 + (g-128)**2 + (b-128)**2)
        torque = phys_dist * (1.0 - el_a['nrci'])
        
        hub_data.append({
            "name": el_a['name'],
            "z": el_a['z'],
            "links": links,
            "torque": float(torque),
            "nrci": el_a['nrci']
        })

    # 3. Sort by Connectivity (The Hubs)
    hubs = sorted(hub_data, key=lambda x: x['links'], reverse=True)
    
    print(f"{'Element':<15} | {'Links':<6} | {'Torque':<10} | {'NRCI'}")
    print("-" * 50)
    for h in hubs[:10]:
        print(f"{h['name']:<15} | {h['links']:<6} | {h['torque']:>10.2f} | {h['nrci']:.4f}")

    # 4. Identify the "Stability Anchor"
    anchor = hubs[0]
    print(f"\n[PRIMARY ANCHOR]: {anchor['name']} with {anchor['links']} resonance links.")
    
    # 5. Save Hub Map
    with open('chromatic_hub_map.json', 'w') as f:
        json.dump(hubs, f, indent=2)

if __name__ == "__main__":
    run_hub_analysis()