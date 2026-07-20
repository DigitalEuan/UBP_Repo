import json
import math
import numpy as np
from fractions import Fraction
from ubp_viz import save_scene_3d

def run_geometric_chromatic_study():
    print("--- UBP GEOMETRIC-CHROMATIC MANIFOLD STUDY ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)
    
    # 1. Define the Noble Equilibrium (The Center of the Funnel)
    noble_z = [2, 10, 18, 36, 54, 86, 118]
    nobles = [el for el in elements if el['z'] in noble_z]
    noble_coords = [np.array([el['rgb']['r'], el['rgb']['g'], el['rgb']['b']]) for el in nobles]
    noble_core = np.mean(noble_coords, axis=0)
    
    print(f"Noble Equilibrium Core: R={noble_core[0]:.2f} G={noble_core[1]:.2f} B={noble_core[2]:.2f}")

    # 2. Map the Funnel
    spheres = []
    lines = []
    funnel_data = []

    for el in elements:
        pos = np.array([el['rgb']['r'], el['rgb']['g'], el['rgb']['b']])
        
        # Vector relative to Noble Core
        rel_vec = pos - noble_core
        dist = np.linalg.norm(rel_vec)
        
        # Calculate "Geometric Tilt" (Angle relative to the R-axis)
        # This represents the 'Phase' of the element
        tilt = math.degrees(math.atan2(rel_vec[1], rel_vec[0]))
        
        # Map to 3D Space for Visualization
        # X = Atomic Number (The Flow of Time/Growth)
        # Y = Distance from Noble Core (Stability Tension)
        # Z = Tilt (Phase/Valence)
        vx = (el['z'] - 60) / 6.0
        vy = dist / 15.0
        vz = tilt / 18.0
        
        is_noble = el['z'] in noble_z
        
        spheres.append({
            "x": vx, "y": vy, "z": vz,
            "r": 0.6 if is_noble else 0.3,
            "color": el['hex_color'],
        })
        
        funnel_data.append({
            "z": el['z'],
            "dist": dist,
            "tilt": tilt
        })

    # 3. Connect the "Spine of Matter" (Z to Z+1)
    for i in range(len(spheres) - 1):
        lines.append({
            "start": [spheres[i]['x'], spheres[i]['y'], spheres[i]['z']],
            "end": [spheres[i+1]['x'], spheres[i+1]['y'], spheres[i+1]['z']],
            "color": "#444444"
        })

    # 4. Export to Visual Tab
    save_scene_3d({"spheres": spheres, "lines": lines})
    
    # 5. Statistical Correlation
    # Does Distance from Noble Core correlate with Periodicity?
    # We check if the 'Dist' oscillates with Z
    print("\n[GEOMETRIC INSIGHTS]")
    print(f"Total Nodes Projected: {len(spheres)}")
    
    # Find the "Tension Extremes"
    max_tension = max(funnel_data, key=lambda x: x['dist'])
    min_tension = min(funnel_data, key=lambda x: x['dist'])
    
    print(f"Highest Chromatic Tension: Z={max_tension['z']} (Dist: {max_tension['dist']:.2f})")
    print(f"Lowest Chromatic Tension:  Z={min_tension['z']} (Dist: {min_tension['dist']:.2f})")

    with open('geometric_chromatic_results.json', 'w') as f:
        json.dump(funnel_data, f, indent=2)

if __name__ == "__main__":
    run_geometric_chromatic_study()