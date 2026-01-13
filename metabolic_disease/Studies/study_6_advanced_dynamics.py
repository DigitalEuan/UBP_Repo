"""
UBP STUDY 6: Multi-Pathway Metabolic Dynamics
==============================================
Advanced study of metabolic signal pathways using UBP principles.

Investigates:
1. Multiple signal pathways (Insulin, Glucagon, Leptin)
2. Cross-talk between pathways via Leech lattice
3. Hamming distance as a measure of metabolic dysregulation
4. Critical transitions and basin of attraction analysis

Author: Enhanced by AI Analysis System
Date: January 2026
"""

import random
import json
from fractions import Fraction
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra, LeechPointScaled
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition
from ubp_nrci_calculator import NRCI_CALCULATOR
import hashlib

random.seed(432)

def molecular_hash(data):
    """Generates a 24-bit geometric signature for a molecule."""
    s = f"{data['name']}-{data['formula']}"
    h = hashlib.sha256(s.encode()).hexdigest()
    val = int(h[:6], 16)
    return [(val >> i) & 1 for i in range(23, -1, -1)]

DEF_MOLECULE = PhenomenonDefinition(
    name="Molecular Identity",
    domain="Biochemistry",
    bit_generator=molecular_hash
)

def run_multi_pathway_analysis():
    """Analyze interactions between multiple metabolic pathways."""
    engine = PhenomenologyEngine()
    
    print("\n" + "="*80)
    print("UBP STUDY 6: MULTI-PATHWAY METABOLIC DYNAMICS")
    print("="*80)
    
    # Define key metabolic molecules
    molecules = {
        "Insulin": {"name": "Insulin", "formula": "C257H383N65O77S6"},
        "Glucagon": {"name": "Glucagon", "formula": "C153H225N43O49S"},
        "Leptin": {"name": "Leptin", "formula": "C714H1167N191O221S6"},
        "GLP1": {"name": "GLP-1", "formula": "C149H226N40O45"},
        "Cortisol": {"name": "Cortisol", "formula": "C21H30O5"}
    }
    
    # Process all molecules through UBP
    print("\n[PHASE 1] MAPPING MOLECULAR SIGNATURES TO SUBSTRATE")
    print("-" * 80)
    
    signatures = {}
    codewords = {}
    nrci_scores = {}
    
    for name, data in molecules.items():
        result = engine.process_phenomenon(DEF_MOLECULE, data)
        signatures[name] = result['substrate_identity']
        
        # Decode to nearest codeword
        ideal_signal, correctable, errors = GOLAY_DECODER.decode(result['substrate_identity'])
        codewords[name] = GOLAY_DECODER.encode(ideal_signal)
        
        # Get NRCI from result
        nrci_val = result.get('nrci', result.get('NRCI', 0.0))
        print(f"{name:12} | Substrate: {''.join(map(str, result['substrate_identity'][:8]))}... | "
              f"Errors: {errors} | NRCI: {nrci_val:.4f}")
    
    # Calculate pairwise Hamming distances
    print("\n[PHASE 2] PATHWAY INTERACTION MATRIX (Hamming Distances)")
    print("-" * 80)
    
    names = list(molecules.keys())
    print(f"{'':12}", end='')
    for n in names:
        print(f" {n:12}", end='')
    print()
    print("-" * (12 + 13 * len(names)))
    
    interaction_matrix = {}
    for n1 in names:
        print(f"{n1:12}", end='')
        interaction_matrix[n1] = {}
        for n2 in names:
            dist = BinaryLinearAlgebra.hamming_distance(codewords[n1], codewords[n2])
            interaction_matrix[n1][n2] = dist
            print(f" {dist:12}", end='')
        print()
    
    # Identify pathway clusters
    print("\n[PHASE 3] PATHWAY CLUSTERING ANALYSIS")
    print("-" * 80)
    
    # Find closely related pathways (distance <= 6)
    print("Closely Related Pathways (d <= 6):")
    for n1 in names:
        for n2 in names:
            if n1 < n2:  # Avoid duplicates
                dist = interaction_matrix[n1][n2]
                if dist <= 6:
                    print(f"  {n1} ↔ {n2}: Hamming distance = {dist} (STRONG COUPLING)")
    
    # Find antagonistic pathways (distance >= 18)
    print("\nAntagonistic Pathways (d >= 18):")
    for n1 in names:
        for n2 in names:
            if n1 < n2:
                dist = interaction_matrix[n1][n2]
                if dist >= 18:
                    print(f"  {n1} ⊗ {n2}: Hamming distance = {dist} (ANTAGONISTIC)")
    
    # Simulate metabolic state trajectory
    print("\n[PHASE 4] METABOLIC STATE TRAJECTORY SIMULATION")
    print("-" * 80)
    print("Simulating transition from diabetic state to healthy state...")
    print()
    
    # Start with corrupted insulin signaling (d=7, diabetic)
    insulin_codeword = codewords["Insulin"]
    current_state = list(insulin_codeword)
    
    # Introduce 7 errors
    for i in range(7):
        current_state[i] = 1 - current_state[i]
    
    # Multi-factor intervention simulation
    # Model: GLP-1 agonist therapy + stress reduction (cortisol management)
    
    glp1_codeword = codewords["GLP1"]
    cortisol_codeword = codewords["Cortisol"]
    
    print(f"{'Step':>4} | {'State':>6} | {'d(Insulin)':>12} | {'d(GLP-1)':>12} | {'d(Cortisol)':>12} | {'Status'}")
    print("-" * 80)
    
    max_steps = 15
    intervention_strength = 0.20  # 20% per step
    
    for step in range(max_steps):
        # Calculate distances to key pathways
        dist_insulin = BinaryLinearAlgebra.hamming_distance(current_state, insulin_codeword)
        dist_glp1 = BinaryLinearAlgebra.hamming_distance(current_state, glp1_codeword)
        dist_cortisol = BinaryLinearAlgebra.hamming_distance(current_state, cortisol_codeword)
        
        # Determine status
        _, _, errors = GOLAY_DECODER.decode(current_state)
        status = "DIABETIC" if errors > 3 else "HEALTHY"
        if errors == 3:
            status = "THRESHOLD"
        
        state_label = f"d={errors}"
        
        print(f"{step:4} | {state_label:>6} | {dist_insulin:>12} | {dist_glp1:>12} | {dist_cortisol:>12} | {status}")
        
        # Apply intervention: bias toward insulin codeword
        if errors > 0:
            for i in range(24):
                if current_state[i] != insulin_codeword[i]:
                    if random.random() < intervention_strength:
                        current_state[i] = insulin_codeword[i]
        
        if errors <= 1:
            print(f"\n✓ REMISSION ACHIEVED at step {step}")
            break
    
    # Calculate basin of attraction depth
    print("\n[PHASE 5] BASIN OF ATTRACTION ANALYSIS")
    print("-" * 80)
    
    print("Testing stability of different metabolic states...")
    
    test_states = [
        ("Healthy (d=0)", 0),
        ("Marginal (d=3)", 3),
        ("Pre-diabetic (d=4)", 4),
        ("Diabetic (d=7)", 7)
    ]
    
    noise_level = 0.08  # 8% perturbation
    trials = 50
    
    print(f"\n{'State':20} | {'Stability':>10} | {'Avg TTR':>10} | {'Max TTR':>10}")
    print("-" * 60)
    
    for state_name, initial_errors in test_states:
        # Create initial state
        state = list(insulin_codeword)
        for i in range(initial_errors):
            state[i] = 1 - state[i]
        
        # Run trials
        survival_times = []
        for trial in range(trials):
            test_state = list(state)
            ttr = 0  # Time to relapse
            
            for t in range(30):
                # Apply noise
                for i in range(24):
                    if test_state[i] == insulin_codeword[i]:
                        if random.random() < noise_level:
                            test_state[i] = 1 - test_state[i]
                
                # Check if relapsed
                _, _, errs = GOLAY_DECODER.decode(test_state)
                if errs > 3:
                    ttr = t
                    break
            else:
                ttr = 30  # Survived all steps
            
            survival_times.append(ttr)
        
        # Calculate statistics
        avg_ttr = sum(survival_times) / len(survival_times)
        max_ttr = max(survival_times)
        stability = (avg_ttr / 30.0) * 100  # As percentage
        
        print(f"{state_name:20} | {stability:>9.1f}% | {avg_ttr:>10.2f} | {max_ttr:>10}")
    
    print("\n" + "="*80)
    print("STUDY 6 COMPLETE")
    print("="*80)

if __name__ == "__main__":
    run_multi_pathway_analysis()
