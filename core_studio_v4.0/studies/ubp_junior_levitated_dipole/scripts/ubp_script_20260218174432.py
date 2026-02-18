from fractions import Fraction
from ubp_core_v5_3_merged import UBPUltimateSubstrate

def calculate_junior_tuning():
    constants = UBPUltimateSubstrate.get_constants(precision=50)
    Y = constants['Y']
    PI = constants['PI']
    
    # The "Junior" Dipole has a specific geometric ratio
    # Let's assume a standard normalized radius of 1.0
    # The UBP Resonant Offset is derived from the waist of the Leech Lattice
    
    resonant_offset = Y / (2 * PI)
    
    print("--- UBP TUNING PARAMETERS FOR JUNIOR DIPOLE ---")
    print(f"Observer Constant (Y): {float(Y):.6f}")
    print(f"Resonant Phase Offset: {float(resonant_offset):.6f}")
    print(f"Coherence Multiplier:  {float(1/Y):.6f}x")
    
    print("\nRECOMMENDATION:")
    print(f"Apply an AC modulation to the levitation field at {float(Y)*100:.2f}% of the fundamental cyclotron frequency.")

calculate_junior_tuning()