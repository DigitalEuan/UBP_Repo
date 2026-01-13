"""
UBP STUDY: The Geometric Basis of Insulin Resistance
====================================================
Modeling metabolic signal transduction as a Golay Error-Correction event.

Objective: Determine the 'Diabetic Horizon' (Noise Threshold) where
insulin signaling fails to trigger the cellular state toggle.
"""

from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
import hashlib

# --- 1. DEFINITIONS ---

def molecular_hash(data):
    """Generates a 24-bit geometric signature for a molecule."""
    # Using SHA-256 to map molecular identity to the substrate
    s = f"{data['name']}-{data['formula']}"
    h = hashlib.sha256(s.encode()).hexdigest()
    val = int(h[:6], 16)
    return [(val >> i) & 1 for i in range(23, -1, -1)]

DEF_MOLECULE = PhenomenonDefinition(
    name="Molecular Identity",
    domain="Biochemistry",
    bit_generator=molecular_hash
)

# --- 2. SIMULATION ENGINE ---

def run_metabolic_simulation():
    engine = PhenomenologyEngine()
    
    print("\n--- [STEP 1] ESTABLISHING BASELINE IDENTITIES ---")
    
    # Define the Key (Insulin) and the Lock (Receptor)
    # In a healthy state, the Receptor is perfectly tuned to Insulin (or its complement).
    # Here we assume the Receptor expects the exact Insulin codeword.
    
    insulin_data = {"name": "Insulin", "formula": "C257H383N65O77S6"}
    insulin_result = engine.process_phenomenon(DEF_MOLECULE, insulin_data)
    insulin_vec = insulin_result['substrate_identity']
    
    # Snap Insulin to a perfect Golay Codeword to represent the "Ideal Signal"
    # Biology uses error-correcting codes; the hormone itself is a stable packet.
    ideal_signal, _, _ = GOLAY_DECODER.decode(insulin_vec)
    ideal_signal_vec = GOLAY_DECODER.encode(ideal_signal)
    
    print(f"Ideal Insulin Signal (Codeword): {ideal_signal_vec[:8]}...")

    print("\n--- [STEP 2] SIMULATING METABOLIC NOISE (RESISTANCE) ---")
    
    # We simulate the Receptor's state. 
    # Healthy = Matches Ideal Signal.
    # Resistant = Accumulated bit-flips (noise) in the receptor's recognition pattern.
    
    noise_levels = range(0, 8) # 0 to 7 bit flips
    
    print(f"{'NOISE':<6} | {'STATUS':<15} | {'SYNDROME':<10} | {'ACTION'}")
    print("-" * 60)
    
    for noise in noise_levels:
        # Create a noisy receptor state
        receptor_state = list(ideal_signal_vec)
        
        # Inject noise (flip bits)
        for i in range(noise):
            receptor_state[i] = 1 - receptor_state[i]
            
        # Attempt to "Decode" the signal (The Cell processing the Hormone)
        # If the cell can decode the noisy receptor state back to the Ideal Signal,
        # the "Key" fits the "Lock".
        
        decoded_msg, correctable, errors_corrected = GOLAY_DECODER.decode(receptor_state)
        
        # Check if the decoded message matches the original Insulin message
        # (This confirms the cell correctly identified the hormone)
        is_recognized = (decoded_msg == ideal_signal) and correctable
        
        status = "HEALTHY" if is_recognized else "DIABETIC"
        action = "GLUCOSE UPTAKE" if is_recognized else "SIGNAL REJECTED"
        
        if noise == 4:
            status += " (DEEP HOLE)"
            
        print(f"{noise:<6} | {status:<15} | {errors_corrected:<10} | {action}")

if __name__ == "__main__":
    run_metabolic_simulation()