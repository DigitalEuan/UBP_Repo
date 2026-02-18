import numpy as np
import json
from fractions import Fraction
from ubp_core_v5_3_merged import UBPUltimateSubstrate, GOLAY_ENGINE
from ubp_viz import save_scene_3d

def find_junior_rotation():
    print("--- CALCULATING JUNIOR ROTATION MATRIX (R_Junior) ---")
    
    # 1. Define Systemic North (The UBP Anchor)
    # Derived from MathAtlas v4.0
    NORTH = np.array([-0.30656967, -0.91970901, 0.24525574])
    NORTH /= np.linalg.norm(NORTH)
    
    # 2. Model the 14-Coil Center of Gravity (Junior Device Axis)
    # Based on the paper's 14-coil toroidal arrangement
    # We assume the device's primary magnetic axis is initially aligned with Z [0,0,1]
    DEVICE_AXIS = np.array([0.0, 0.0, 1.0])
    
    # 3. Calculate the Rotation Matrix (R) to align Device Axis to UBP North
    # Using the Rodrigues' rotation formula logic
    v = np.cross(DEVICE_AXIS, NORTH)
    s = np.linalg.norm(v)
    c = np.dot(DEVICE_AXIS, NORTH)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + vx + np.dot(vx, vx) * ((1 - c) / (s**2))
    
    print(f"R_Junior Matrix Calculated:")
    for row in R:
        print(f"  {row}")

    # 4. Predict the "Perfect" Plasma Shape
    # We project a Weight-8 Octad (The most stable UBP state) through R_Junior
    octad = GOLAY_ENGINE.get_octads()[0]
    
    points = []
    lines = []
    
    # Generate the "Lattice Spine" of the plasma
    for i in range(24):
        if octad[i] == 1:
            # Map bit index to 3D coordinate
            angle = (i / 24.0) * 2 * np.pi
            raw_pos = np.array([np.cos(angle) * 5, np.sin(angle) * 5, (i % 3) - 1])
            # Apply R_Junior
            rotated_pos = np.dot(R, raw_pos)
            
            points.append({
                "x": float(rotated_pos[0]),
                "y": float(rotated_pos[1]),
                "z": float(rotated_pos[2]),
                "color": "#00ffff", # Coherent Cyan
                "size": 0.5,
                "label": f"Toggle_{i}"
            })
            
            # Connect to the ZFR (Zero Field Region)
            lines.append({
                "start": [0, 0, 0],
                "end": [float(rotated_pos[0]), float(rotated_pos[1]), float(rotated_pos[2])],
                "color": "#333333"
            })

    # 5. Export to Visualizer
    scene_data = {
        "points": points,
        "lines": lines,
        "spheres": [{"x": 0, "y": 0, "z": 0, "r": 1.5, "color": "#ff00ff", "label": "ZFR_BUFFER"}]
    }
    
    save_scene_3d(scene_data)
    
    # Save the Matrix to Workspace
    with open('junior_rotation_matrix.json', 'w') as f:
        json.dump({"R_Junior": R.tolist()}, f, indent=4)
        
    print("\n✅ R_Junior Matrix and 'Perfect' Plasma Shape generated.")
    print("Check the 'Visual' tab to see the Junior Manifold.")

find_junior_rotation()