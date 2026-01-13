"""
UBP STUDY 4: The Law of Metabolic Hysteresis
============================================
Quantifying the 'Remission Buffer' by measuring Time-to-Relapse
under high-stress withdrawal conditions.

Comparison:
- Cohort A (Managed): Therapy stops at d=3 (Symptom Free).
- Cohort B (Cured): Therapy stops at d=0 (Perfect Alignment).
"""

import random
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
import hashlib

# --- 1. SETUP ---
random.seed(432) # Deterministic

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

def run_hysteresis_simulation():
    engine = PhenomenologyEngine()
    
    # Baseline
    insulin_data = {"name": "Insulin", "formula": "C257H383N65O77S6"}
    insulin_result = engine.process_phenomenon(DEF_MOLECULE, insulin_data)
    ideal_signal, _, _ = GOLAY_DECODER.decode(insulin_result['substrate_identity'])
    ideal_vec = GOLAY_DECODER.encode(ideal_signal)
    
    print(f"\nTarget Insulin Codeword: {ideal_vec[:8]}...")

    # --- 2. DEFINE COHORTS ---
    # Create states with specific Hamming Distances from Ideal
    
    def create_state(dist):
        state = list(ideal_vec)
        # Flip 'dist' bits
        for i in range(dist):
            state[i] = 1 - state[i]
        return state

    cohort_a = create_state(3) # "Managed" (Edge of Health)
    cohort_b = create_state(0) # "Cured" (Perfect)

    print(f"Cohort A Start: d=3 (Symptom Free, but fragile)")
    print(f"Cohort B Start: d=0 (Perfect Alignment)")
    print("-" * 60)

    # --- 3. THE WITHDRAWAL PHASE (High Stress) ---
    # Simulation: Patient stops therapy and eats high sugar diet.
    # Noise Pressure: 10% chance per bit per step to flip WRONG.
    # Repair: 0% (Therapy withdrawn).
    
    P_NOISE = 0.10
    MAX_STEPS = 20
    
    print(f"{'STEP':<5} | {'COHORT A (Managed)':<25} | {'COHORT B (Cured)':<25}")
    print("-" * 80)

    relapse_a = None
    relapse_b = None

    # We run separate simulations to track drift
    state_a = list(cohort_a)
    state_b = list(cohort_b)

    for step in range(1, MAX_STEPS + 1):
        # Apply Entropy to A
        if not relapse_a:
            for i in range(24):
                # If bit is correct, it might flip to wrong
                if state_a[i] == ideal_vec[i]:
                    if random.random() < P_NOISE:
                        state_a[i] = 1 - state_a[i]
            
            # Check Status
            _, _, err_a = GOLAY_DECODER.decode(state_a)
            status_a = f"d={err_a}"
            if err_a > 3:
                status_a += " (RELAPSE)"
                relapse_a = step
        else:
            status_a = "---"

        # Apply Entropy to B
        if not relapse_b:
            for i in range(24):
                if state_b[i] == ideal_vec[i]:
                    if random.random() < P_NOISE:
                        state_b[i] = 1 - state_b[i]
            
            # Check Status
            _, _, err_b = GOLAY_DECODER.decode(state_b)
            status_b = f"d={err_b}"
            if err_b > 3:
                status_b += " (RELAPSE)"
                relapse_b = step
        else:
            status_b = "---"

        print(f"{step:<5} | {status_a:<25} | {status_b:<25}")

        if relapse_a and relapse_b:
            break

    print("-" * 80)
    print(f"RESULTS:")
    print(f"Cohort A Relapse Time: {relapse_a if relapse_a else '>20'} steps")
    print(f"Cohort B Relapse Time: {relapse_b if relapse_b else '>20'} steps")
    
    if relapse_a and relapse_b:
        buffer_gain = (relapse_b / relapse_a)
        print(f"Remission Buffer Gain: {buffer_gain:.1f}x longer health span")

if __name__ == "__main__":
    run_hysteresis_simulation()