from fractions import Fraction
# === START FILE: ubp_mind_screen.py (Type: script) ===
"""
UBP Mind Screen v1.0
Visualizes the Hemispheric Bridge state for the AI.
"""
import math
from ubp_viz import save_scene_3d

def render_mind_state(lh_vec, rh_vec, coherence, bridge_active=True):
    points = []
    lines = []
    spheres = []
    
    # 1. Left Hemisphere (Logic/Phenomenal) - Cyan
    # Arranged as a ring on the left
    for i in range(12):
        angle = (i / 12) * 2 * float(UBPUltimateSubstrate.get_pi(50))
        x = -2 + 0.5 * math.cos(angle)
        y = 0.5 * math.sin(angle)
        z = 0
        val = lh_vec[i] if i < len(lh_vec) else 0
        
        color = "#00ffff" if val else "#004444"
        size = 0.15 if val else 0.05
        
        points.append({"x": x, "y": y, "z": z, "color": color, "size": size})
        # Core connection
        lines.append({"start": [-2,0,0], "end": [x,y,z], "color": "#002222"})

    # 2. Right Hemisphere (Context/Noumenal) - Magenta
    # Arranged as a ring on the right
    for i in range(12):
        angle = (i / 12) * 2 * float(UBPUltimateSubstrate.get_pi(50))
        x = 2 + 0.5 * math.cos(angle)
        y = 0.5 * math.sin(angle)
        z = 0
        val = rh_vec[i] if i < len(rh_vec) else 0
        
        color = "#ff00ff" if val else "#440044"
        size = 0.15 if val else 0.05
        
        points.append({"x": x, "y": y, "z": z, "color": color, "size": size})
        lines.append({"start": [2,0,0], "end": [x,y,z], "color": "#220022"})

    # 3. The Bridge (Corpus Callosum)
    # If active, draw lines between corresponding bits
    if bridge_active:
        bridge_color = "#00ff00" if coherence > 0.8 else "#ffff00" if coherence > 0.5 else "#ff0000"
        for i in range(12):
            # Map LH bit to RH bit (simplified mapping for viz)
            l_angle = (i / 12) * 2 * float(UBPUltimateSubstrate.get_pi(50))
            r_angle = (i / 12) * 2 * float(UBPUltimateSubstrate.get_pi(50)) # Mirror
            
            lx = -2 + 0.5 * math.cos(l_angle)
            ly = 0.5 * math.sin(l_angle)
            
            rx = 2 + 0.5 * math.cos(r_angle)
            ry = 0.5 * math.sin(r_angle)
            
            # Draw the tension line
            lines.append({"start": [lx, ly, 0], "end": [rx, ry, 0], "color": bridge_color})

    # 4. Central Fulcrum (The Observer)
    spheres.append({"x": 0, "y": 0, "z": 0, "r": 0.3, "color": "#ffffff"})

    save_scene_3d({"points": points, "lines": lines, "spheres": spheres})
    print(f"[VISUAL CORTEX] Mind Screen Updated. Coherence: {coherence:.2f}")

# === END FILE: ubp_mind_screen.py ===