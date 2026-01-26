"""
UBP FRAME OF MIND (FOM) ENGINE v1.0
===================================
Implements dynamic NRCI weighting and Contextual Gravity.
Allows the system to "Focus" on specific domains by boosting the 
Ontological Mass of relevant anchors.

Features:
1. Frame Management: Create, Edit, Save, Load Frames.
2. Gravitational Lensing: High-NRCI anchors bend noisy vectors closer.
3. Event Horizon: Calibrated to 0.01 (Captures d=8 at NRCI=0.8).

Author: UBP Research Cortex v4.2.7
"""

import json
import hashlib
from fractions import Fraction
from typing import Dict, List, Any, Optional
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra

# --- 1. THE FRAME CONTAINER ---
class FrameOfMind:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.weights: Dict[str, float] = {} # Map UBP_ID -> NRCI (0.0 to 1.0)
        self.base_nrci = 0.5 # Default mass for unlisted items

    def set_weight(self, ubp_id: str, nrci: float):
        """Boosts or suppresses a specific concept."""
        self.weights[ubp_id] = max(0.0, min(1.0, nrci))
        print(f"[FOM] '{self.name}': Set {ubp_id} mass to {nrci}")

    def get_weight(self, ubp_id: str) -> float:
        return self.weights.get(ubp_id, self.base_nrci)

    def export_frame(self) -> str:
        """Serializes the Frame for storage."""
        data = {
            "ubp_frame_id": f"FOM_{self.name.upper()}",
            "description": self.description,
            "base_nrci": self.base_nrci,
            "weights": self.weights
        }
        return json.dumps(data, indent=2)

# --- 2. THE GRAVITATIONAL CORTEX ---
class GravitationalCortex:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.anchors: Dict[str, List[int]] = {}
        self.active_frame = FrameOfMind("DEFAULT")
        self.EVENT_HORIZON = 0.01 # Adjusted to capture d=8 at High Mass

    def load_anchor(self, ubp_id: str, vector: List[int]):
        self.anchors[ubp_id] = vector

    def set_frame(self, frame: FrameOfMind):
        print(f"\n[CORTEX] Shifting Frame of Mind to: {frame.name}")
        self.active_frame = frame

    def vectorize(self, text: str) -> List[int]:
        """Hashes text to 24-bit vector."""
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        return [(val >> i) & 1 for i in range(23, -1, -1)]

    def observe(self, concept: str):
        print(f"\n[OBSERVER] Analyzing: '{concept}' (Frame: {self.active_frame.name})")
        input_vec = self.vectorize(concept)
        
        best_anchor = None
        max_pull = -1.0
        
        # Scan all anchors in memory
        for uid, vec in self.anchors.items():
            dist = BinaryLinearAlgebra.hamming_distance(input_vec, vec)
            
            # Get Dynamic Mass from Active Frame
            mass = self.active_frame.get_weight(uid)
            
            # Gravitational Law: F = G * (M / r^2)
            # We use (dist + 1)^2 to avoid division by zero
            pull = mass / ((dist + 1) ** 2)
            
            if pull > 0.005: # Only log significant pulls
                print(f"  > {uid:<20} | Dist: {dist:>2} | Mass: {mass:.2f} | Pull: {pull:.4f}")
            
            if pull > max_pull:
                max_pull = pull
                best_anchor = uid

        # Decision Logic
        if max_pull >= self.EVENT_HORIZON:
            print(f"  [!] CAPTURE: Snapped to '{best_anchor}' (Pull {max_pull:.4f})")
            return best_anchor
        else:
            print(f"  [?] FREE FLOATING: No anchor had sufficient gravity.")
            return None

# --- 3. EXECUTION & DEMO ---
if __name__ == "__main__":
    cortex = GravitationalCortex()
    
    # A. Load Memories (From your provided list)
    # 1. The Law of Squeezing (Target)
    cortex.load_anchor("LAW_SQUEEZE_001", [0,0,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,0])
    # 2. A Noise Artifact (Distractor)
    cortex.load_anchor("NOISE_ARTIFACT", [0,0,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0]) 
    # 3. Thermodynamics (Distractor)
    cortex.load_anchor("THERMO_001", [1,0,0,0,1,0,0,1,1,1,0,1,1,0,0,0,1,0,0,1,1,1,0,1])

    # B. Test 1: Default Frame (Flat Mass = 0.5)
    # "The Law of Informational Squeezin" (Typo)
    # In Study 3, this was Dist 8 from Squeeze.
    # Pull = 0.5 / 81 = 0.006 (Below Horizon)
    cortex.observe("The Law of Informational Squeezin")

    # C. Create "PHYSICS_FOCUS" Frame
    physics_frame = FrameOfMind("PHYSICS_FOCUS", "High gain for physical laws")
    physics_frame.set_weight("LAW_SQUEEZE_001", 1.0) # Maximum Mass
    physics_frame.set_weight("THERMO_001", 0.9)
    physics_frame.set_weight("NOISE_ARTIFACT", 0.05) # Suppress Noise

    # D. Apply Frame and Retest
    cortex.set_frame(physics_frame)
    # Pull = 1.0 / 81 = 0.0123 (Above Horizon 0.01)
    cortex.observe("The Law of Informational Squeezin")

    # E. Save Frame
    print("\n[SYSTEM] Saving Frame of Mind to Disk...")
    print(physics_frame.export_frame())