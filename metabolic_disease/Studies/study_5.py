"""
UBP STUDY 5: The Resilience Titration
=====================================
Mapping the 'Stability Landscape' of Metabolic Health.
Determining the critical noise threshold where the Remission Buffer fails.
"""

import random
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
import hashlib

# --- 1. SETUP ---
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

def run_titration():
    engine = PhenomenologyEngine()
    
    # Baseline
    insulin_data = {"name": "Insulin", "formula": "C257H383N65O77S6"}
    insulin_result = engine.process_phenomenon(DEF_MOLECULE, insulin_data)
    ideal_signal, _, _ = GOLAY_DECODER.decode(insulin_result['substrate_identity'])
    ideal_vec = GOLAY_DECODER.encode(ideal_signal)
    
    # --- 2. TITRATION LOOP ---
    noise_levels = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06] # 1% to 6%
    max_steps = 50
    
    print(f"\n{'NOISE':<8} | {'COHORT A (Managed) SURVIVAL':<30} | {'COHORT B (Cured) SURVIVAL':<30}")
    print("-" * 80)
    
    for noise in noise_levels:
        # Reset Cohorts
        state_a = list(ideal_vec)
        # Set A to d=3
        for i in range(3): state_a[i] = 1 - state_a[i]
        
        state_b = list(ideal_vec) # B starts at d=0
        
        survival_a = 0
        survival_b = 0
        
        # Run Time Series
        for step in range(1, max_steps + 1):
            # Apply Noise to A
            if survival_a == step - 1:
                for i in range(24):
                    if state_a[i] == ideal_vec[i] and random.random() < noise:
                        state_a[i] = 1 - state_a[i]
                _, _, err_a = GOLAY_DECODER.decode(state_a)
                if err_a <= 3: survival_a = step
            
            # Apply Noise to B
            if survival_b == step - 1:
                for i in range(24):
                    if state_b[i] == ideal_vec[i] and random.random() < noise:
                        state_b[i] = 1 - state_b[i]
                _, _, err_b = GOLAY_DECODER.decode(state_b)
                if err_b <= 3: survival_b = step
                
        # Format Output
        res_a = f"{survival_a} steps" if survival_a < max_steps else "STABLE (>50)"
        res_b = f"{survival_b} steps" if survival_b < max_steps else "STABLE (>50)"
        
        print(f"{noise:.0%}      | {res_a:<30} | {res_b:<30}")

if __name__ == "__main__":
    run_titration()