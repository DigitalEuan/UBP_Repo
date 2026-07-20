import json
import numpy as np
from core import BinaryLinearAlgebra, LEECH_ENGINE
from ubp_viz import save_scene_3d

def run_analog_chromatic_space():
    print("--- UBP v7.2: ANALOG CHROMATIC SPACE SIMULATION ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)

    spheres = []
    lines = []
    
    # 1. Define the "Origin of Stability" (The Noble Core)
    noble_z = [2, 10, 18, 36, 54, 86, 118]
    
    print(f"Projecting {len(elements)} elements into Analog Space...")

    for el in elements:
        # Map RGB to 3D Space (Centered at 128)
        # We scale down by 20 to keep the scene manageable
        x = (el['rgb']['r'] - 128) / 20.0
        y = (el['rgb']['g'] - 128) / 20.0
        z = (el['rgb']['b'] - 128) / 20.0
        
        # Calculate local NRCI for coloring
        tax = LEECH_ENGINE.calculate_symmetry_tax(el['vector'])
        nrci = 10.0 / (10.0 + float(tax))
        
        # Determine size: Nobles are "Anchors" (larger)
        radius = 0.6 if el['z'] in noble_z else 0.3
        
        # Color: Use the actual element hex color
        color = el['hex_color']
        
        spheres.append({
            "x": x, "y": y, "z": z,
            "r": radius,
            "color": color,
        })

    # 2. Draw the "Substrate Spine" (Connect elements by Hamming Distance < 8)
    # This visualizes the "Non-Local Links"
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            v1 = elements[i]['vector']
            v2 = elements[j]['vector']
            dist = BinaryLinearAlgebra.hamming_distance(v1, v2)
            
            if dist <= 8: # Only draw stable "Bonds"
                lines.append({
                    "start": [spheres[i]['x'], spheres[i]['y'], spheres[i]['z']],
                    "end": [spheres[j]['x'], spheres[j]['y'], spheres[j]['z']],
                    "color": "#444444",
                    "opacity": 0.2
                })

    # 3. Export to Visual Tab
    scene = {"spheres": spheres, "lines": lines}
    save_scene_3d(scene)
    
    print(f"✅ Analog Space Manifested.")
    print(f"   Nodes: {len(spheres)}")
    print(f"   Resonance Links: {len(lines)}")
    print("Check the 'Visual' tab to see the Chromatic Manifold.")

if __name__ == "__main__":
    run_analog_chromatic_space()