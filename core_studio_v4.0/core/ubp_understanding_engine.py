import re
import json
import hashlib
from collections import defaultdict
from ubp_brain_consolidated import UBPBrain
from ubp_core_v5_3_merged import GOLAY_ENGINE, BinaryLinearAlgebra

# 1. Initialize the Brain
brain = UBPBrain()
brain.initialize(['ubp_system_kb.json'])

# ==============================================================================
# STRICT PARSER
# ==============================================================================
def parse_math_dna(dna: str):
    if '|' in dna:
        dna = dna.split('|', 1)[1].strip()
    components = defaultdict(int)
    id_pattern = r'([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]{3,})'
    # Look for "2xID" or "2×ID"
    mult_pattern = r'(\d+)\s*[\u00d7xX]?\s*' + id_pattern
    for mult_str, name in re.findall(mult_pattern, dna):
        components[name] += int(mult_str)
    # Look for standalone IDs
    for name in re.findall(r'\b' + id_pattern + r'\b', dna):
        if name not in components:
            components[name] += 1
    
    # Filter out non-ID noise
    junk = {'N', 'Z', 'Tax', 'Mean_Dist', 'Snap'}
    for name in list(components.keys()):
        if name in junk or components[name] == 0 or name.isdigit():
            del components[name]
    return dict(components)

# ==============================================================================
# LATTICE GAP SOLVER (FIXED COMPARISON LOGIC)
# ==============================================================================
def solve_for_missing_logic(subject_id, auto_mint=True):
    entry = brain.memory.kb.get(subject_id)
    if not entry:
        return print(f"ID {subject_id} not found.")

    # 1. Get the Current Vector in the KB
    target_vec = brain.vector_engine._extract_vector(entry)
    if not target_vec or len(target_vec) != 24:
        return print(f"[{subject_id}] Skipped: No valid 24-bit vector.")

    math_dna = entry.get('math', '').strip()
    parsed = parse_math_dna(math_dna)

    # If no components found (e.g. Proton primitive), skip
    if not parsed:
        print(f"[{subject_id}] Primitive/Atomic (No sub-components in math). Status: OK.")
        return

    print(f"\n--- AUDITING: '{entry.get('name', subject_id)}' ---")
    
    # 2. Calculate the Sum of Parts (Leech Space)
    composed_coords = [0] * 24
    resolved = []
    missing = []

    for name, mult in parsed.items():
        # Resolve ID
        candidates = brain.memory.lexicon_index.get(name.lower(), [])
        if not candidates and name in brain.memory.kb:
            candidates = [name]
        
        found = False
        for comp_id in candidates[:3]:
            comp_entry = brain.memory.kb.get(comp_id)
            if comp_entry:
                comp_vec = brain.vector_engine._extract_vector(comp_entry)
                if comp_vec and len(comp_vec) == 24:
                    # Convert 0/1 to -1/1 for summation
                    comp_coords = [1 if b == 1 else -1 for b in comp_vec]
                    for _ in range(mult):
                        for i in range(24):
                            composed_coords[i] += comp_coords[i]
                    resolved.append((mult, name))
                    found = True
                    break
        if not found:
            missing.append((mult, name))

    if missing:
        print(f"  [!] Cannot verify: Missing components {missing}")
        return

    # 3. Snap the Sum to a Codeword (The "Calculated Truth")
    # Convert back to bits: Positive sum -> 1, Negative/Zero -> 0
    raw_bits = [1 if c > 0 else 0 for c in composed_coords]
    snapped_calculated, _, _ = brain.vector_engine.coherence_snap(raw_bits)

    # 4. Compare Calculated vs Stored
    # This is the fix: Compare Vector to Vector, not Vector to Integer Sum
    dist = BinaryLinearAlgebra.hamming_distance(target_vec, snapped_calculated)

    if dist == 0:
        print(f"  ✅ HIERARCHY CLOSED. The math perfectly generates the vector.")
    else:
        print(f"  ❌ GAP DETECTED (Dist={dist}).")
        print(f"     Stored Vector does not match Math Sum.")
        
        if auto_mint:
            # If we are here, it means the KB entry has the WRONG vector for its math.
            # We don't need a new composite; we need to update the entry or mint a patch.
            # But per your workflow, we mint a composite to show the "True" sum.
            fingerprint = hashlib.sha256(math_dna.encode()).hexdigest()
            new_id = f"COMPOSITE_{subject_id}_FIX"
            
            new_entry = {
                "ubp_id": new_id,
                "name": f"Corrected Sum: {entry.get('name')}",
                "category": "composite.correction",
                "math": math_dna,
                "vector": snapped_calculated,
                "hamming_weight": sum(snapped_calculated),
                "tags": ["CORRECTION", "GENERATED"],
                "nrci": "1/1"
            }
            
            brain.memory.kb[new_id] = new_entry
            print(f"     → Generated Correction: {new_id} (Vector updated)")

# ==============================================================================
# RUN AUDIT
# ==============================================================================
targets = ["ELEM_H_001", "MOLECULE_H2O", "MOLECULE_H2", "PARTICLE_PROTON_001"]

for t in targets:
    solve_for_missing_logic(t)

# Save if needed (optional, mostly for debugging the loop)
# with open("system_kb_audit.json", "w") as f:
#    json.dump(brain.memory.kb, f, indent=2)