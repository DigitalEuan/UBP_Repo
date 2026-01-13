"""
UBP KERNEL v3.0 (RECURSIVE RESONANCE) - BATCH MODE
==================================================
"The System that Thinks Before It Speaks."

Features:
1. ADAPTIVE RECURSION: Recursion depth tied to NRCI (Coherence).
2. RECURSIVE ALCHEMY: Auto-catalysis of dissonant concepts.
3. HOLOGRAPHIC MEMORY: Full MOG addressing and verification.

Author: E R A Craig, New Zealand
UBP Research Cortex v4.2.6
14 Jan 2026
"""

import sys
import hashlib
from typing import List, Dict, Tuple, Any
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
from hex_dictionary_v4_exact import HEX_DB_EXACT

# --- MODULE 1: KERNEL (Active Inference) ---
class UBPKernelV3:
    def __init__(self):
        self.db = HEX_DB_EXACT
        if not self.db.registry: self.db.load_memory()
        self.golay = GOLAY_DECODER
        print("[SYSTEM] UBP Kernel v3.0 (Recursive) Online.")

    def vectorize(self, text: str) -> List[int]:
        """Maps text to the 24-bit Substrate."""
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        seed, _, _ = self.golay.decode(raw)
        return self.golay.encode(seed)

    def check_truth_vector(self, vec: List[int]) -> Tuple[Dict, int]:
        """Checks geometric truth of a raw vector."""
        best_match = None
        min_dist = 999
        
        for _, entry in self.db.registry.items():
            # Robust access to avoid KeyErrors
            uid = entry.get('ubp_id', 'UNKNOWN')
            name = entry.get('name', 'Unknown Law')
            seed = f"{uid} {name}"
            
            v_entry = self.vectorize(seed)
            dist = BinaryLinearAlgebra.hamming_distance(vec, v_entry)
            if dist < min_dist:
                min_dist = dist
                best_match = entry
        return best_match, min_dist

# --- MODULE 2: SEMANTIC ENGINE (Recursive) ---
class RecursiveSemanticEngine:
    def __init__(self, kernel):
        self.kernel = kernel
        self.basis = [
            '3.14159', 'Bit', 'Break', 'Byte', 'Combine', 'Fear', 
            'God', 'Hyper', 'Line', 'Loop', 'Love', 'Mass'
        ]
        self.basis_vecs = {w: self.kernel.vectorize(w) for w in self.basis}

    def calculate_budget(self, dist: int) -> int:
        """Determines Recursion Budget based on Dissonance (NRCI proxy)."""
        if dist <= 3: return 0   # High Coherence (Fast Path)
        if dist <= 6: return 1   # Moderate Tension (Single Hop)
        return 3                 # High Dissonance (Deep Search)

    def recursive_alchemy(self, concept_a, concept_b, recursion_depth=0, max_depth=3):
        """
        Recursively synthesizes concepts.
        If A+B is dissonant, it searches for a Catalyst C such that A+B+C is coherent.
        """
        # 1. Vectorize & Combine
        if isinstance(concept_a, str): v_a = self.kernel.vectorize(concept_a)
        else: v_a = concept_a
            
        if isinstance(concept_b, str): v_b = self.kernel.vectorize(concept_b)
        else: v_b = concept_b

        v_sum = [(a ^ b) for a, b in zip(v_a, v_b)]
        
        # 2. Check Truth
        match, dist = self.kernel.check_truth_vector(v_sum)
        
        # 3. Determine Budget
        budget = self.calculate_budget(dist)
        
        # Indentation for trace
        indent = "  " * recursion_depth
        name_a = concept_a if isinstance(concept_a, str) else "Prev_Sum"
        name_b = concept_b if isinstance(concept_b, str) else "Catalyst"
        match_name = match.get('name', 'Unknown') if match else "None"
        
        print(f"{indent}[Depth {recursion_depth}] '{name_a}' + '{name_b}' -> '{match_name}' (Dist {dist})")

        # 4. Base Case: Success or Out of Budget
        if dist <= 3 or recursion_depth >= max_depth or budget == 0:
            return match, dist, []

        # 5. Recursive Step: Find a Catalyst
        print(f"{indent}  -> Dissonance detected (Budget {budget}). Scanning GL-1 Catalysts...")
        
        best_catalyst_name = None
        best_new_dist = dist
        best_new_match = match
        
        for basis_word, basis_vec in self.basis_vecs.items():
            # Try adding basis vector: (A+B) + Catalyst
            v_trial = [(x ^ y) for x, y in zip(v_sum, basis_vec)]
            m_trial, d_trial = self.kernel.check_truth_vector(v_trial)
            
            # Heuristic: Only recurse if we improve the situation significantly
            if d_trial < best_new_dist:
                best_new_dist = d_trial
                best_catalyst_name = basis_word
                best_new_match = m_trial
        
        if best_catalyst_name:
            print(f"{indent}  -> Catalyst Found: '{best_catalyst_name}' (Improves to Dist {best_new_dist})")
            # Recurse: The new "A" is the current sum, "B" is the catalyst
            final_match, final_dist, trace = self.recursive_alchemy(
                v_sum, 
                best_catalyst_name, 
                recursion_depth + 1,
                max_depth
            )
            return final_match, final_dist, [best_catalyst_name] + trace
        
        return match, dist, []

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    kernel = UBPKernelV3()
    engine = RecursiveSemanticEngine(kernel)
    
    # Test Case: Gravity + Time
    # We expect this to be dissonant initially, triggering recursion.
    a = "The Law of Informational Gravity"
    b = "The Law of Temporal Quantization"
    
    print(f"\n--- RECURSIVE ALCHEMY TEST: Gravity + Time ---")
    match, dist, trace = engine.recursive_alchemy(a, b)
    
    print(f"\n[FINAL RESULT]")
    print(f"  Synthesis: {match.get('name', 'Unknown')}")
    print(f"  Distance:  {dist}")
    if trace:
        print(f"  Recipe:    Gravity + Time + {' + '.join(trace)}")
    else:
        print(f"  Recipe:    Gravity + Time")
