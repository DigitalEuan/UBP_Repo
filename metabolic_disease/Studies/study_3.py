"""
UBP STUDY 3: Resonance Tuning & The Diabetic Horizon
====================================================
Simulating the restoration of metabolic sensitivity via 
external informational biasing (Resonance Field).

Objective: Push a receptor from d=5 (Diabetic) to d<=3 (Healthy).
"""

import random
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
import hashlib

# --- 1. SETUP ---
# Ensure deterministic "randomness" for reproducible science
random.seed(432) 

def molecular_hash(data):
    s = f"{data['name']}-{data['formula']}"
    h = hashlib.sha256(s.encode()).hexdigest()
    val = int(h[:6], 16)
    return [(val >> i) & 1 for i in range(23, -1, -1)]

DEF_MOLECULE = PhenomenonDefinition(
    name="Molecular Identity",
    domain="Biochemistry",
    bit_generator=molecular_hash
)

def run_resonance_simulation():
    engine = PhenomenologyEngine()
    
    # 1. Establish Ideal Signal (Insulin)
    insulin_data = {"name": "Insulin", "formula": "C257H383N65O77S6"}
    insulin_result = engine.process_phenomenon(DEF_MOLECULE, insulin_data)
    ideal_signal, _, _ = GOLAY_DECODER.decode(insulin_result['substrate_identity'])
    ideal_vec = GOLAY_DECODER.encode(ideal_signal)
    
    print(f"\nTarget Insulin Codeword: {ideal_vec[:8]}...")

    # 2. Create Diabetic State (d=5)
    # We flip 5 specific bits to push it into the uncorrectable zone.
    diabetic_state = list(ideal_vec)
    flip_indices = [0, 1, 2, 3, 4] 
    for i in flip_indices:
        diabetic_state[i] = 1 - diabetic_state[i]
        
    initial_dist = BinaryLinearAlgebra.hamming_distance(diabetic_state, ideal_vec)
    print(f"Initial Receptor State: DIABETIC (Hamming Dist: {initial_dist})")
    print("-" * 60)

    # 3. Define Simulation Parameters
    # Probability that a wrong bit flips back to correct per time step
    P_NATURAL = 0.05   # 5% chance (Homeostasis fighting high entropy)
    P_RESONANT = 0.25  # 25% chance (Assisted by Resonance Field)
    
    MAX_STEPS = 10

    # 4. Run Simulation
    print(f"{'STEP':<5} | {'CONTROL (Natural)':<20} | {'EXPERIMENTAL (Resonant)':<25} | {'STATUS'}")
    print("-" * 80)

    # Initialize two separate timelines
    control_receptor = list(diabetic_state)
    resonant_receptor = list(diabetic_state)
    
    control_healed = False
    resonant_healed = False

    for step in range(1, MAX_STEPS + 1):
        # --- CONTROL LOGIC ---
        # Iterate through bits; if wrong, try to fix with low probability
        for i in range(24):
            if control_receptor[i] != ideal_vec[i]:
                if random.random() < P_NATURAL:
                    control_receptor[i] = ideal_vec[i] # Corrected
        
        # Check Control Status
        _, _, c_err = GOLAY_DECODER.decode(control_receptor)
        c_status = f"d={c_err} (DIABETIC)" if c_err > 3 else f"d={c_err} (HEALTHY)"
        if c_err <= 3 and not control_healed: control_healed = step

        # --- EXPERIMENTAL LOGIC ---
        # Iterate through bits; if wrong, try to fix with HIGH probability
        for i in range(24):
            if resonant_receptor[i] != ideal_vec[i]:
                if random.random() < P_RESONANT:
                    resonant_receptor[i] = ideal_vec[i] # Corrected
        
        # Check Experimental Status
        _, _, r_err = GOLAY_DECODER.decode(resonant_receptor)
        r_status = f"d={r_err} (DIABETIC)" if r_err > 3 else f"d={r_err} (HEALTHY)"
        if r_err <= 3 and not resonant_healed: resonant_healed = step

        # Output
        note = ""
        if resonant_healed == step: note = "✨ RESONANCE SNAP!"
        
        print(f"{step:<5} | {c_status:<20} | {r_status:<25} | {note}")
        
        # Stop if both healed (unlikely for control)
        if control_healed and resonant_healed: break

if __name__ == "__main__":
    run_resonance_simulation()