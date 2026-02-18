import numpy as np
import json
from fractions import Fraction
from ubp_core_v5_3_merged import UBPUltimateSubstrate

def generate_control_table():
    print("--- GENERATING JUNIOR CONTROL TABLE (LNC-v1) ---")
    
    # 1. Load the R_Junior Matrix
    with open('junior_rotation_matrix.json', 'r') as f:
        R_data = json.load(f)
        R = np.array(R_data['R_Junior'])
    
    constants = UBPUltimateSubstrate.get_constants(precision=50)
    Y = float(constants['Y'])
    
    # 2. Define the 14 Coil Positions (Toroidal Angle theta)
    # Junior uses a 14-coil arrangement.
    coils = []
    for i in range(14):
        theta = (i / 14.0) * 2 * np.pi
        # Physical vector of the coil
        pos_vec = np.array([np.cos(theta), np.sin(theta), 0.0])
        
        # 3. Calculate "Lattice Alignment" (Dot product with Systemic North via R)
        # We rotate the coil vector into the Lattice Frame
        lattice_vec = np.dot(R, pos_vec)
        
        # Alignment Strength (How much this coil contributes to the 'Grip')
        alignment = np.abs(lattice_vec[0]) # X-axis alignment in Lattice Frame
        
        # 4. Calculate Phase Offset (Derived from Y)
        phase_offset = (theta / (2 * np.pi)) * Y
        
        coils.append({
            "coil_id": i + 1,
            "angle_deg": round(np.degrees(theta), 2),
            "base_weight": round(float(alignment), 4),
            "phase_offset_rad": round(float(phase_offset), 6),
            "recommended_ac_ripple": f"{round(alignment * 10, 2)}%"
        })

    # 5. Save to Workspace
    control_table = {
        "device": "Junior_Dipole",
        "protocol": "Lattice-Native Control v1.0",
        "modulation_frequency_factor": "0.264675 (Y)",
        "coils": coils
    }
    
    with open('junior_control_table.json', 'w') as f:
        json.dump(control_table, f, indent=4)
        
    print("✅ Control Table 'junior_control_table.json' generated.")
    print(f"   Calculated weights for 14 coils based on R_Junior alignment.")

generate_control_table()