"""
UBP STUDY 2: The Zinc Anchor Effect
===================================
Verifying the 'Law of Parity Anchoring' in metabolic health.
Simulating the protective effect of structural constraints (Zinc)
against informational entropy (Inflammation).
"""

from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
import hashlib

# --- 1. SETUP ---

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

def run_zinc_simulation():
    engine = PhenomenologyEngine()
    
    # 1. Establish Ideal Signal (Insulin)
    insulin_data = {"name": "Insulin", "formula": "C257H383N65O77S6"}
    insulin_result = engine.process_phenomenon(DEF_MOLECULE, insulin_data)
    ideal_signal, _, _ = GOLAY_DECODER.decode(insulin_result['substrate_identity'])
    ideal_vec = GOLAY_DECODER.encode(ideal_signal)
    
    print(f"\nBaseline Insulin Codeword: {ideal_vec[:8]}...")

    # 2. Define The Zinc Anchor (Locking Bits)
    # We assume Zinc coordinates structurally, locking the first 2 bits of the sequence.
    # In a real protein, these would be the Histidine residues.
    ZINC_MASK = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 1 = Locked, 0 = Vulnerable
    
    print(f"Zinc Anchor Active: Locking {sum(ZINC_MASK)} bits against entropy.")

    # 3. Stress Test
    print(f"\n{'ENV NOISE':<10} | {'CONTROL (No Zinc)':<20} | {'EXPERIMENTAL (Zinc)':<20} | {'GAIN'}")
    print("-" * 80)
    
    for noise_pressure in range(0, 9):
        # --- CONTROL GROUP (Naked Receptor) ---
        control_state = list(ideal_vec)
        # Apply noise sequentially (deterministic entropy)
        for i in range(noise_pressure):
            control_state[i] = 1 - control_state[i] # Flip bit
            
        # Decode Control
        _, _, ctrl_errors = GOLAY_DECODER.decode(control_state)
        ctrl_status = "HEALTHY" if ctrl_errors <= 3 else "DIABETIC"
        
        # --- EXPERIMENTAL GROUP (Zinc Anchored) ---
        exp_state = list(ideal_vec)
        actual_flips = 0
        
        for i in range(noise_pressure):
            # The Anchor Check: Can this bit be flipped?
            if ZINC_MASK[i] == 1:
                # Zinc prevents the flip (Energy barrier too high)
                pass 
            else:
                # Vulnerable bit flips
                exp_state[i] = 1 - exp_state[i]
                actual_flips += 1
                
        # Decode Experimental
        _, _, exp_errors = GOLAY_DECODER.decode(exp_state)
        exp_status = "HEALTHY" if exp_errors <= 3 else "DIABETIC"
        
        # --- RESULT ---
        gain = "---"
        if ctrl_status == "DIABETIC" and exp_status == "HEALTHY":
            gain = "PROTECTED"
            
        print(f"{noise_pressure:<10} | {ctrl_status:<20} (d={ctrl_errors}) | {exp_status:<20} (d={exp_errors}) | {gain}")

if __name__ == "__main__":
    run_zinc_simulation()