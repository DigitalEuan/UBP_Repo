import math
import json
import numpy as np
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_viz import save_scene_3d

def get_periodic_pos(z):
    if z == 1: return (1, 1)
    if z == 2: return (1, 18)
    if 3 <= z <= 10: return (2, (z - 2) if z <= 4 else (z - 2) + 10)
    if 11 <= z <= 18: return (3, (z - 10) if z <= 12 else (z - 10) + 10)
    if 19 <= z <= 36: return (4, z - 18)
    if 37 <= z <= 54: return (5, z - 36)
    if 55 <= z <= 86:
        if 57 <= z <= 71: return (6, 3)
        return (6, (z - 54) if z < 57 else (z - 54 - 14))
    if 87 <= z <= 118:
        if 89 <= z <= 103: return (7, 3)
        return (7, (z - 86) if z < 89 else (z - 86 - 14))
    return (8, 1)

def run_toroidal_manifold():
    print("--- UBP TOROIDAL MANIFOLD GENERATOR ---")
    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()

    points = []
    lines = []
    
    # Torus Constants
    R = 15.0  # Major Radius (The whole donut)
    
    elements = []
    for uid, entry in HEX_DB_EXACT.registry.items():
        ubp_id = entry.get('ubp_id', '')
        if not ubp_id.startswith('ELEM_'): continue
        
        z = int(ubp_id.split('_')[-1])
        period, group = get_periodic_pos(z)
        vec = entry.get('vector', [])
        tension = sum(vec)
        
        # 1. Toroidal Angle (Theta) - Based on Period/Z
        # We spread the 118 elements around the 360 degrees of the donut
        theta = (z / 118.0) * 2 * math.pi
        
        # 2. Poloidal Angle (Phi) - Based on Group
        # This rotates around the "tube" of the donut
        phi = (group / 18.0) * 2 * math.pi
        
        # 3. Minor Radius (r) - Based on Tension
        # High tension elements make the tube "thicker"
        r = (tension - 7) * 0.8
        
        # 4. Torus Cartesian Conversion
        x = (R + r * math.cos(phi)) * math.cos(theta)
        y = (R + r * math.cos(phi)) * math.sin(theta)
        z_pos = r * math.sin(phi)
        
        # Color by MRI (Magnetism)
        mri = entry.get('dimensional_projections', {}).get('substrate_metrics', {}).get('magnetic_resonance_index', 0)
        # Purple (Low) to Gold (High)
        color = f"#{int(255*min(1, mri/0.5)):02x}44{int(255*(1-min(1, mri/0.5))):02x}"
        
        elements.append({
            "z": z, "pos": [x, y, z_pos], "color": color, 
            "label": f"{entry.get('name', '').split(': ')[1]} (T={tension})"
        })

    # Sort for the Snake
    elements.sort(key=lambda x: x["z"])
    
    for i, el in enumerate(elements):
        points.append({
            "x": el["pos"][0], "y": el["pos"][1], "z": el["pos"][2],
            "color": el["color"], "size": 0.5, "label": el["label"]
        })
        
        if i < len(elements) - 1:
            lines.append({
                "start": el["pos"], "end": elements[i+1]["pos"], "color": "#444444"
            })

    # Add a central "Void" sphere
    spheres = [{"x": 0, "y": 0, "z": 0, "r": 2.0, "color": "#111111", "label": "SUBSTRATE_CORE"}]

    save_scene_3d({"points": points, "lines": lines, "spheres": spheres})
    print("\n[VISUALIZATION GENERATED]")
    print("The 'Periodic Torus' is now manifest.")
    print("  > Toroidal Loop: Atomic Evolution (Z)")
    print("  > Poloidal Loop: Chemical Groups (Valence)")
    print("  > Tube Thickness: Symmetry Tax (Tension)")

if __name__ == "__main__":
    run_toroidal_manifold()