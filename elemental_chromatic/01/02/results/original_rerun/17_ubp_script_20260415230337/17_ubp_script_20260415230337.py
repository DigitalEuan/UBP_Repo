import json
import numpy as np
from fractions import Fraction
from core import BinaryLinearAlgebra, LEECH_ENGINE

def run_full_manifold_audit():
    print("--- UBP v7.2: FULL CHROMATIC MANIFOLD AUDIT ---")
    
    # 1. Load System KB (Columnar)
    with open('ubp_system_kb.json', 'r') as f:
        kb_data = json.load(f)
    
    fields = kb_data["_fields"]
    idx = {f: i for i, f in enumerate(fields)}
    entries = kb_data["entries"]
    
    # 2. Load Chromatic Data
    with open('elemental_chromatic_data.json', 'r') as f:
        chromatic_list = json.load(f)
    chromatic_map = {c['ubp_id']: c for c in chromatic_list}

    print(f"Auditing {len(chromatic_list)} elements against Hardened KB...")
    print(f"{'ID':<15} | {'Z':<3} | {'NRCI':<8} | {'RGB Tension':<12} | {'Status'}")
    print("-" * 65)

    full_audit_results = []

    for fp, e in entries.items():
        uid = e[idx["ubp_id"]]
        if not uid.startswith("ELEM_"): continue
        
        # Get Noumenal Data (from KB)
        v_noumenal = e[idx["vector"]]
        nrci = float(e[idx["nrci_val"]])
        
        # Get Phenomenal Data (from Chromatic Study)
        c_data = chromatic_map.get(uid)
        if not c_data: continue
        
        v_phenomenal = c_data['vector']
        
        # Calculate Tension (Hamming distance between the two representations)
        tension = BinaryLinearAlgebra.hamming_distance(v_noumenal, v_phenomenal)
        
        # Determine Manifestation Status
        if tension <= 4: status = "LOCKED"
        elif tension <= 8: status = "STABLE"
        elif tension <= 12: status = "TRANSITIONAL"
        else: status = "GHOST"

        full_audit_results.append({
            "uid": uid,
            "z": c_data['z'],
            "nrci": nrci,
            "tension": tension,
            "status": status
        })

        if c_data['z'] in [1, 22, 50, 98, 118]: # Key milestones
            print(f"{uid:<15} | {c_data['z']:<3} | {nrci:.4f} | {tension:<12} | {status}")

    # 3. Global Statistics
    tensions = [r['tension'] for r in full_audit_results]
    avg_tension = np.mean(tensions)
    ghost_count = sum(1 for r in full_audit_results if r['status'] == "GHOST")

    print("\n[MANIFOLD STATISTICS]")
    print(f"  Average Systemic Tension: {avg_tension:.2f} bits")
    print(f"  Ghost/Zombie Elements:    {ghost_count} / {len(full_audit_results)}")
    
    if avg_tension < 8:
        print("✅ MANIFOLD COHERENCE: The Chromatic and Noumenal layers are phase-locked.")
    else:
        print("⚠️ MANIFOLD SHEAR: High tension detected. The system is undergoing 'Relational Decay'.")

    with open('full_manifold_audit.json', 'w') as f:
        json.dump(full_audit_results, f, indent=2)

if __name__ == "__main__":
    run_full_manifold_audit()