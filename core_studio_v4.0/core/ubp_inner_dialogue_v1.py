"""
UBP INNER DIALOGUE MODULE v1.1
==============================
"The System that Thinks Before It Speaks."

Fixed: Robust anchor loading and iterative convergence logic.
Author: E R A Craig, New Zealand
UBP Research Cortex v4.2.7
19 Jan 2026
"""
import hashlib
import json
import re
import os
from fractions import Fraction
from typing import Dict, List, Tuple
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra

class UBPInnerDialogue:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.filename = "ubp_system_kb.md"
        self.anchors = self._load_cortex()
        self.threshold = 3 # The Error-Correction Radius (t=3)

    def _derive_vector(self, seed: str) -> List[int]:
        """Derives a stable 24-bit Golay codeword from any string."""
        h = hashlib.sha256(seed.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        insight, _, _ = self.golay.decode(raw)
        return self.golay.encode(insight)

    def _load_cortex(self) -> Dict[str, List[int]]:
        print(f"[CORTEX] Initializing Semantic Substrate...")
        if not os.path.exists(self.filename):
            print("  ❌ KB File not found.")
            return {}
            
        with open(self.filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fixed Regex for JSON Extraction
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        raw_json = match.group(1) if match else content
        
        try:
            # Clean up trailing commas and parse
            clean_json = re.sub(r',\s*\}', '}', raw_json)
            data = json.loads(clean_json)
            
            anchors = {}
            for k, v in data.items():
                if not isinstance(v, dict): continue
                
                # Check for existing vector or derive from fingerprint
                vec = v.get('vector')
                if not isinstance(vec, list):
                    # Check the script field for a vector definition
                    v_match = re.search(r'vector\s*=\s*(\[[0-1,\s]+\])', str(v.get('script', '')))
                    if v_match:
                        try: vec = json.loads(v_match.group(1))
                        except: pass
                
                # If still no vector, derive it (ensures 100% coverage)
                if not isinstance(vec, list) or len(vec) != 24:
                    seed = v.get('fingerprint', v.get('ubp_id', k))
                    vec = self._derive_vector(seed)
                
                name = str(v.get('name', v.get('ubp_id', k))).upper()
                anchors[name] = [int(x) for x in vec]
            
            print(f"  ✅ {len(anchors)} Anchors synchronized.")
            return anchors
        except Exception as e:
            print(f"  ❌ Initialization Error: {e}")
            return {}

    def vectorize(self, text: str) -> List[int]:
        return self._derive_vector(text)

    def deliberate(self, query: str, max_turns: int = 5) -> Tuple[str, Fraction]:
        print(f"\n[INNER DIALOGUE] Inquiry: '{query}'")
        current_vec = self.vectorize(query)
        
        last_name = "NONE"
        last_cost = Fraction(1)

        for turn in range(1, max_turns + 1):
            # 1. Find Nearest Anchor (The "First Impression")
            best_name, min_dist = "NONE", 25
            for name, anchor_vec in self.anchors.items():
                d = BinaryLinearAlgebra.hamming_distance(current_vec, anchor_vec)
                if d < min_dist:
                    min_dist, best_name = d, name
            
            # 2. Calculate Interaction Cost (Hamming Weight / Substrate Width)
            cost = Fraction(min_dist, 24)
            print(f"  Turn {turn}: Closest resonance '{best_name}' | Distance: {min_dist} | Cost: {cost}")

            # 3. Convergence Check (t=3 Error-Correction Radius)
            if min_dist <= self.threshold:
                print(f"  [!] COHERENCE REACHED: Signal snapped to {best_name}")
                return best_name, cost

            # 4. Reflexive Adjustment (The "Pivot")
            # We XOR the current thought with the anchor to find the 'Residue' 
            # and then re-center the thought on that discrepancy.
            anchor_vec = self.anchors[best_name]
            # Bitwise XOR
            reflexive_vec = [(a ^ b) for a, b in zip(current_vec, anchor_vec)]
            
            # Re-snap to the closest valid codeword to maintain geometric stability
            insight, _, _ = self.golay.decode(reflexive_vec)
            current_vec = self.golay.encode(insight)
            
            last_name, last_cost = best_name, cost

        print("  [?] DIALOGUE TERMINATED: Maximum complexity reached without full snap.")
        return last_name, last_cost

if __name__ == "__main__":
    dialogue = UBPInnerDialogue()
    
    # Test a complex, non-obvious query
    concept, final_cost = dialogue.deliberate("Do you have any original ideas?")
    
    print(f"\n[FINAL VERDICT]")
    print(f"  Primary Anchor: {concept}")
    print(f"  Linguistic Entropy (Final Cost): {final_cost}")
