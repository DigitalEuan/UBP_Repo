import json
import numpy as np
import hashlib
from fractions import Fraction
from core import BinaryLinearAlgebra

def hex_to_bw256(hex_str: str) -> list:
    """Converts a 256-bit hash directly into a 256D lattice coordinate."""
    b = bytes.fromhex(hex_str)
    bits = []
    for byte in b:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
    return bits

def run_bulk_drift_study():
    print("--- UBP v7.2: 256D ONTOLOGICAL DRIFT AUDIT ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)

    print(f"{'Element':<15} | {'Saturation':<10} | {'256D Drift':<12} | {'Ontology'}")
    print("-" * 60)

    drift_results = []

    for el in elements:
        # 1. Get the 24-bit Noumenal Core
        v24 = el['vector']
        
        # 2. Generate the 256-bit Phenomenal Bulk
        # We hash the vector to simulate the 'unfolding' into the bulk
        v_str = "".join(map(str, v24))
        fingerprint = hashlib.sha256(v_str.encode()).hexdigest()
        v256 = hex_to_bw256(fingerprint)
        
        # 3. Calculate Drift (Hamming distance between 24-bit core and the first 24 bits of the bulk)
        # This measures how much the 'Physical' manifestation deviates from the 'Ideal'
        drift = sum(1 for i in range(24) if v24[i] != v256[i])
        
        # 4. Chromatic Saturation
        r, g, b = el['rgb']['r'], el['rgb']['g'], el['rgb']['b']
        sat = np.sqrt((r-128)**2 + (g-128)**2 + (b-128)**2)
        
        ontology = "STABLE" if drift <= 8 else "TRANSITIONAL"
        if drift > 12: ontology = "GHOST/ZOMBIE"

        drift_results.append({
            "name": el['name'],
            "sat": float(sat),
            "drift": drift,
            "ontology": ontology
        })

        if el['z'] in [1, 2, 26, 118]:
            print(f"{el['name']:<15} | {sat:>10.2f} | {drift:>12} | {ontology}")

    # 5. Final Correlation
    sats = [d['sat'] for d in drift_results]
    drifts = [d['drift'] for d in drift_results]
    bulk_corr = np.corrcoef(sats, drifts)[0, 1]

    print("\n[BULK INFERENCE]")
    print(f"  Correlation (Saturation vs 256D Drift): {bulk_corr:.4f}")
    
    if abs(bulk_corr) > 0.4:
        print("✅ ANCHOR FOUND: Color is a function of 256D Ontological Drift.")
    else:
        print("❌ PERSISTENT DECOUPLING: The system is likely non-local (LAW_NONLOCAL_SURGERY_001).")

    with open('bulk_drift_results.json', 'w') as f:
        json.dump(drift_results, f, indent=2)

if __name__ == "__main__":
    run_bulk_drift_study()