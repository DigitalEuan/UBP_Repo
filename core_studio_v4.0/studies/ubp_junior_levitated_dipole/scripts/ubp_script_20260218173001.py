import math
from fractions import Fraction
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra

def analyze_levitation_gain():
    print("--- UBP TOPOLOGICAL ANALYSIS: JUNIOR DIPOLE ---")
    
    # 1. Define the Ideal Dipole (Levitated)
    # A pure, weight-8 Golay codeword represents the perfect magnetic loop.
    # We use a known octad from the Golay engine.
    ideal_dipole_vec = GOLAY_ENGINE.get_octads()[0] 
    
    # Calculate its stability (Tax)
    tax_levitated = LEECH_ENGINE.calculate_symmetry_tax(ideal_dipole_vec)
    nrci_levitated = Fraction(1, 1) / (Fraction(1, 1) + (tax_levitated * Fraction(1, 10)))
    
    print(f"State: LEVITATED (Ideal)")
    print(f"  > Vector: {ideal_dipole_vec}")
    print(f"  > Symmetry Tax: {float(tax_levitated):.4f}")
    print(f"  > NRCI (Coherence): {float(nrci_levitated):.4f}")
    
    # 2. Define the Supported Dipole (Noisy)
    # Supports introduce "Geometric Noise." We simulate this by flipping bits 
    # in the vector (representing the physical connection to the vessel).
    # 3 bit flips represents significant interference (limit of error correction).
    supported_vec = list(ideal_dipole_vec)
    # Flip 3 bits to simulate supports (mechanical bridges)
    for i in range(3):
        supported_vec[i] = 1 - supported_vec[i]
        
    # Calculate its stability
    tax_supported = LEECH_ENGINE.calculate_symmetry_tax(supported_vec)
    nrci_supported = Fraction(1, 1) / (Fraction(1, 1) + (tax_supported * Fraction(1, 10)))
    
    print(f"\nState: SUPPORTED (Interference)")
    print(f"  > Vector: {supported_vec}")
    print(f"  > Symmetry Tax: {float(tax_supported):.4f}")
    print(f"  > NRCI (Coherence): {float(nrci_supported):.4f}")
    
    # 3. Calculate the "Ontological Gain"
    gain = nrci_levitated - nrci_supported
    print(f"\n--- CONCLUSION ---")
    print(f"Ontological Gain from Levitation: +{float(gain):.4f}")
    
    if gain > 0.1:
        print("RESULT: Levitation provides a CRITICAL stability advantage.")
        print("The 'Pinch' effect is the system reclaiming this lost coherence.")
    else:
        print("RESULT: Marginal gain.")

analyze_levitation_gain()