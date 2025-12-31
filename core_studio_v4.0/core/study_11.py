import json
from ubp_core_v4_2_6_COMBINED import LEECH_ENHANCED, LeechPointScaled
from ubp_viz import save_scene_3d

def run_viz_calibration():
    print("[VIZ] Generating Leech Lattice Shell (Minimal Vectors)...")
    
    # 1. Generate Minimal Vectors (Norm^2 = 32 scaled / 4 actual)
    # In the standard Leech Lattice, minimal vectors have norm^2 = 4 (if scaled by 1/sqrt(8))
    # We will generate a subset for visualization.
    
    points_data = []
    lines_data = []
    
    # Origin
    points_data.append({
        "x": 0, "y": 0, "z": 0, 
        "color": "#ffffff", "size": 0.5, "label": "Origin"
    })
    
    # Generate a small sample of minimal vectors for calibration
    # (Generating all 196,560 is too heavy for a quick test, we'll do a slice)
    count = 0
    limit = 100  # Visual limit
    
    # We use the Golay code to drive the generation to ensure valid points
    codewords = LEECH_ENHANCED.golay.get_all_codewords()
    
    for cw in codewords:
        if count >= limit: break
        
        # Convert Golay codeword to Leech point (standard construction)
        # Simple mapping: 0 -> 0, 1 -> 2 (scaled)
        coords = [2 * x for x in cw]
        
        # Check if it's a minimal vector (Norm squared should be 32 in our scaling)
        # Note: This simple mapping might not hit minimal vectors directly without offset
        # So we'll just visualize the code structure for now.
        
        lp = LeechPointScaled(tuple(coords))
        phys = lp.to_physical_space()
        
        # Project 24D to 3D (using first 3 dims for simple projection)
        # In a real study, we use PCA or specific projection planes.
        x, y, z = phys[0], phys[1], phys[2]
        
        # Color based on Ontological Health
        health = lp.get_ontological_health()
        nrci = health['Global_NRCI']
        
        color = "#00ff00" # High coherence
        if nrci < 0.5: color = "#ffff00" # Medium
        if nrci < 0.2: color = "#ff0000" # Low
        
        points_data.append({
            "x": x, "y": y, "z": z,
            "color": color, "size": 0.2
        })
        
        # Draw line to origin
        lines_data.append({
            "start": [0, 0, 0],
            "end": [x, y, z],
            "color": "#333333"
        })
        
        count += 1

    scene = {
        "points": points_data,
        "lines": lines_data,
        "spheres": []
    }
    
    save_scene_3d(scene)
    print(f"[VIZ] Scene saved with {len(points_data)} points.")

if __name__ == "__main__":
    run_viz_calibration()