import json
import numpy as np
from core import BinaryLinearAlgebra, LEECH_ENGINE
from ubp_viz import save_scene_3d

def generate_full_chromatic_map():
    print("--- UBP v7.2: GENERATING FULL ELEMENTAL CHROMATIC MAP ---")
    
    # 1. Load the phase-locked chromatic data
    try:
        with open('elemental_chromatic_data.json', 'r') as f:
            elements = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'elemental_chromatic_data.json' not found.")
        return

    spheres = []
    lines = []
    map_data = []

    print(f"Mapping {len(elements)} elements into Chromatic Space...")

    for el in elements:
        # Position = RGB Coordinates (Centered at 128, scaled for visibility)
        x = (el['rgb']['r'] - 128) / 15.0
        y = (el['rgb']['g'] - 128) / 15.0
        z = (el['rgb']['b'] - 128) / 15.0
        
        # Size = NRCI Stability (Scaled)
        # Elements with higher NRCI appear as larger "Stability Anchors"
        radius = (el['nrci'] * 2.0) - 0.5 
        
        # Color = Actual Element Hex
        color = el['hex_color']
        
        spheres.append({
            "x": x, "y": y, "z": z,
            "r": radius,
            "color": color,
            "label": f"{el['name']} (Z={el['z']}, NRCI={el['nrci']:.4f})"
        })
        
        map_data.append({
            "z": el['z'],
            "symbol": el['name'],
            "rgb": el['rgb'],
            "hex": color,
            "nrci": el['nrci'],
            "pos": [x, y, z]
        })

    # 2. Draw the "Resonance Spine" (Hamming Distance <= 8)
    # This connects the elements into their natural "Growth Spiral"
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            v1 = elements[i]['vector']
            v2 = elements[j]['vector']
            if BinaryLinearAlgebra.hamming_distance(v1, v2) <= 8:
                lines.append({
                    "start": [spheres[i]['x'], spheres[i]['y'], spheres[i]['z']],
                    "end": [spheres[j]['x'], spheres[j]['y'], spheres[j]['z']],
                    "color": "#ffffff",
                    "opacity": 0.1
                })

    # 3. Export to Visual Tab
    save_scene_3d({"spheres": spheres, "lines": lines})
    
    # 4. Save the Master Map Data
    with open('full_elemental_chromatic_map.json', 'w') as f:
        json.dump(map_data, f, indent=2)
    
    print(f"✅ Master Map Generated.")
    print(f"   Nodes: {len(spheres)}")
    print(f"   Resonance Edges: {len(lines)}")
    print("Check the 'Visual' tab to see the Chromatic Periodic Table.")

if __name__ == "__main__":
    generate_full_chromatic_map()