"""
UBP STUDY 3: GRAVITATIONAL REASONING (NRCI MASS)
================================================
Implements 'Ontological Mass' where NRCI determines the 
gravitational pull of an anchor on noisy concepts.

Features:
1. Weighted Anchors: Entries have mutable NRCI scores.
2. Gravitational Snapping: Snap to max(NRCI / Dist^2).
3. Dynamic Promotion: Adjusting NRCI changes reasoning outcomes.

Author: UBP Research Cortex v4.2.7
"""

import hashlib
from fractions import Fraction
from typing import List, Dict, Tuple, Optional
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra

class WeightedAnchor:
    def __init__(self, name: str, vector: List[int], nrci: float):
        self.name = name
        self.vector = vector
        self.nrci = nrci  # Ontological Mass (0.0 to Fraction(1, 1))

class GravitationalReasoning:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.memory: List[WeightedAnchor] = []
        self._hydrate_memory()

    def _hydrate_memory(self):
        # 1. Load a Fundamental Law (High Mass)
        # LAW_SQUEEZE_001 (from your Reflexive Memory)
        vec_squeeze = [0,0,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,0]
        self.memory.append(WeightedAnchor("LAW_SQUEEZE_001", vec_squeeze, Fraction(1, 1)))

        # 2. Load a Noise Artifact (Low Mass)
        # A random vector close to Squeeze but meaningless
        vec_noise = vec_squeeze.copy()
        vec_noise[0] = 1 - vec_noise[0] # Flip 1 bit
        self.memory.append(WeightedAnchor("ARTIFACT_NOISE_001", vec_noise, 0.1))

        # 3. Load Thermodynamics (Medium Mass)
        # From study_2 output (snapped)
        vec_thermo = [1,0,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,0,1,1,1,0,1] 
        self.memory.append(WeightedAnchor("THERMO_ANCHOR", vec_thermo, 0.8))

    def vectorize(self, text: str) -> List[int]:
        """Hashes text to 24-bit vector (Raw)."""
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        return [(val >> i) & 1 for i in range(23, -1, -1)]

    def observe(self, concept: str):
        print(f"\n[OBSERVER] Analyzing: '{concept}'")
        input_vec = self.vectorize(concept)
        
        best_anchor = None
        max_attraction = -Fraction(1, 1)
        
        print(f"  > Geometry: {''.join(map(str, input_vec))}")
        print(f"  > Scanning Gravitational Field...")

        for anchor in self.memory:
            dist = BinaryLinearAlgebra.hamming_distance(input_vec, anchor.vector)
            
            # Gravitational Formula: Mass / Distance^2
            # We use (Distance + 1) to avoid division by zero
            attraction = anchor.nrci / ((dist + 1) ** 2)
            
            print(f"    - {anchor.name:<20} | Dist: {dist:>2} | NRCI: {anchor.nrci:.1f} | Pull: {attraction:.4f}")
            
            if attraction > max_attraction:
                max_attraction = attraction
                best_anchor = anchor

        # Threshold for "Orbit" vs "Free Space"
        if max_attraction > 0.02: # Tunable Horizon
            print(f"  > RESULT: Captured by '{best_anchor.name}' (Pull: {max_attraction:.4f})")
            if best_anchor.nrci >= 0.9:
                print("  > STATUS: VERIFIED TRUTH. Snapped to High-Mass Anchor.")
            else:
                print("  > STATUS: HYPOTHESIS. Snapped to Low-Mass Anchor.")
        else:
            print("  > RESULT: Free Floating (No significant gravitational capture).")

# --- EXECUTION ---
if __name__ == "__main__":
    engine = GravitationalReasoning()
    
    # Test 1: "The Law of Informational Squeezing"
    # In study_2, this failed because it was distance 4 from a random keyword.
    # Here, we check if the High Mass of the true law pulls it in.
    engine.observe("The Law of Informational Squeezing")
    
    # Test 2: A concept close to the Noise Artifact
    # We simulate a typo of the law
    engine.observe("The Law of Informational Squeezin")