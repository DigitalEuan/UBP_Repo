import json
from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate
from ubp_viz import save_scene_3d

def build_dimensional_compound_machine():
    # 1. Load the Dimensional Observer Study data
    try:
        with open('dimensional_observer_study.json', 'r') as f:
            study_data = json.load(f)
    except FileNotFoundError:
        print("Error: 'dimensional_observer_study.json' not found. Please run the study script first.")
        return

    # 2. Exact Constants
    consts = UBPUltimateSubstrate.get_v6_constants()
    PHI = consts['PHI']
    ONE = Fraction(1)
    ZERO = Fraction(0)
    SCALE = Fraction(27, 25)
    
    V_SCALE = 4.0   # Scale of the individual Icosa/Dodeca manifolds
    L_SCALE = 15.0  # Scale of the Macroscopic Leech Projection

    # 3. Base Icosahedron Vertices
    icosa_base = [
        (-ONE, PHI, ZERO), (ONE, PHI, ZERO), (-ONE, -PHI, ZERO), (ONE, -PHI, ZERO),
        (ZERO, -ONE, PHI), (ZERO, ONE, PHI), (ZERO, -ONE, -PHI), (ZERO, ONE, -PHI),
        (PHI, ZERO, -ONE), (-PHI, ZERO, -ONE), (PHI, ZERO, ONE), (-PHI, ZERO, ONE)
    ]
    dodeca_base = [(x * SCALE, y * SCALE, z * SCALE) for x, y, z in icosa_base]

    spheres = []
    lines = []
    
    prev_cw = None
    prev_m_coords = None
    prev_p_coords = None
    total_tax = Fraction(0)

    print("Building Dimensional Compound Machine...")

    for idx, row in enumerate(study_data):
        dim = row['raw_dimensions_active']
        
        # Reconstruct the raw vector and snap it
        raw_vec = [1] * dim + [0] * (24 - dim)
        cw, _ = GOLAY_ENGINE.snap_to_codeword(raw_vec)
        
        # 4. Actual Leech Coordinate Projection (24D -> 3D)
        # We use the canonical UBP block-sum projection
        ox = (sum(cw[0:8]) - 4) * L_SCALE
        oy = (sum(cw[8:16]) - 4) * L_SCALE
        oz = (sum(cw[16:24]) - 4) * L_SCALE
        
        # Add a micro-offset based on the raw dimension to prevent exact Z-fighting
        # This visually represents the "Ghost Tension" of the un-snapped state
        micro_offset = dim * 0.4
        ox += micro_offset
        oy += micro_offset
        oz += micro_offset

        msg12 = cw[:12]
        parity12 = cw[12:]
        
        tax = LEECH_ENGINE.calculate_symmetry_tax(cw)
        total_tax += tax

        curr_m_coords = []
        curr_p_coords = []

        for i in range(12):
            # Message Node
            mx = float(dodeca_base[i][0]) * V_SCALE + ox
            my = float(dodeca_base[i][1]) * V_SCALE + oy
            mz = float(dodeca_base[i][2]) * V_SCALE + oz
            curr_m_coords.append((mx, my, mz))
            
            m_bit = msg12[i]
            spheres.append({
                "x": mx, "y": my, "z": mz,
                "r": 0.55 if m_bit else 0.22,
                "color": "#00ffff" if m_bit else "#003366",
                "label": f"D{dim}_M{i}:{m_bit}"
            })

            # Parity Node
            px = float(icosa_base[i][0]) * V_SCALE + ox
            py = float(icosa_base[i][1]) * V_SCALE + oy
            pz = float(icosa_base[i][2]) * V_SCALE + oz
            curr_p_coords.append((px, py, pz))

            p_bit = parity12[i]
            spheres.append({
                "x": px, "y": py, "z": pz,
                "r": 0.55 if p_bit else 0.22,
                "color": "#ff00ff" if p_bit else "#660000",
                "label": f"D{dim}_P{i}:{p_bit}"
            })

            # Intra-unit bridge
            lines.append({
                "start": [mx, my, mz],
                "end": [px, py, pz],
                "color": "#aaffff" if (m_bit and p_bit) else "#444444"
            })

        # 5. Inter-unit bridges with Ternary Modulation
        if prev_cw is not None:
            for i in range(12):
                # Message to Message bridge
                t_val_m = (prev_cw[i] + cw[i]) % 3
                if t_val_m > 0:
                    pmx, pmy, pmz = prev_m_coords[i]
                    cmx, cmy, cmz = curr_m_coords[i]
                    mid_mx = (pmx + cmx) / 2
                    mid_my = (pmy + cmy) / 2
                    mid_mz = (pmz + cmz) / 2
                    
                    spheres.append({
                        "x": mid_mx, "y": mid_my, "z": mid_mz,
                        "r": 0.35,
                        "color": "#ffff00" if t_val_m == 1 else "#ff8800",
                        "label": f"T_M{i}:{t_val_m}"
                    })
                    lines.append({"start": [pmx, pmy, pmz], "end": [mid_mx, mid_my, mid_mz], "color": "#ffff00"})
                    lines.append({"start": [mid_mx, mid_my, mid_mz], "end": [cmx, cmy, cmz], "color": "#ffff00"})

                # Parity to Parity bridge
                t_val_p = (prev_cw[i+12] + cw[i+12]) % 3
                if t_val_p > 0:
                    ppx, ppy, ppz = prev_p_coords[i]
                    cpx, cpy, cpz = curr_p_coords[i]
                    mid_px = (ppx + cpx) / 2
                    mid_py = (ppy + cpy) / 2
                    mid_pz = (ppz + cpz) / 2
                    
                    spheres.append({
                        "x": mid_px, "y": mid_py, "z": mid_pz,
                        "r": 0.35,
                        "color": "#00ff00" if t_val_p == 1 else "#008800",
                        "label": f"T_P{i}:{t_val_p}"
                    })
                    lines.append({"start": [ppx, ppy, ppz], "end": [mid_px, mid_py, mid_pz], "color": "#00ff00"})
                    lines.append({"start": [mid_px, mid_py, mid_pz], "end": [cpx, cpy, cpz], "color": "#00ff00"})

        prev_cw = cw
        prev_m_coords = curr_m_coords
        prev_p_coords = curr_p_coords

    # 6. Export and Report
    scene = {"spheres": spheres, "lines": lines}
    
    # Write to file so the user can inspect the raw JSON if needed
    with open('compound_golay_scene.json', 'w') as f:
        json.dump(scene, f)
        
    save_scene_3d(scene)
    
    compound_nrci = Fraction(10) / (Fraction(10) + total_tax)
    print("\n=== COMPOUND GEOMETRIC-GOLAY MACHINE (DIMENSIONAL STUDY) ===")
    print(f"Units Processed: {len(study_data)}")
    print(f"Total Symmetry Tax: {float(total_tax):.4f}")
    print(f"Compound NRCI: {float(compound_nrci):.6f}")
    print("✅ 3D Manifold with Leech Projections and Ternary Bridges exported to Visual Cortex.")

if __name__ == "__main__":
    build_dimensional_compound_machine()