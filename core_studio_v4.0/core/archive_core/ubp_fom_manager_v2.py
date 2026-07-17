"""
UBP FRAME OF MIND (FOM) ENGINE v4.2.7 (v5.3 Core Compatible)
============================================================
Implements dynamic NRCI weighting and Contextual Gravity.
Updated to use UBP Core v5.3 Merged standards.

Author: E R A Craig, New Zealand and the UBP Research Cortex v4.2.7
Date: 20 Feb 2026
"""

import json
import hashlib
from fractions import Fraction
from typing import Dict, List, Any, Optional
# v5.3 Migration: Use GOLAY_ENGINE
from ubp_unified_v5 import GOLAY_ENGINE as GOLAY_DECODER, BinaryLinearAlgebra

# --- 1. THE FRAME CONTAINER ---
class FrameOfMind:
    def __init__(self, frame_id: str, description: str = ""):
        self.frame_id = frame_id
        self.description = description
        self.weights: Dict[str, Fraction] = {} 
        self.category_weights: Dict[str, Fraction] = {}
        self.base_nrci = Fraction(1, 2)

    def set_weight(self, ubp_id: str, nrci: Fraction):
        self.weights[ubp_id] = nrci

    def set_category_weight(self, category: str, nrci: Fraction):
        self.category_weights[category] = nrci

    def get_weight(self, ubp_id: str, category: str = None) -> Fraction:
        # 1. Specific ID Weight
        if ubp_id in self.weights:
            return self.weights[ubp_id]
        # 2. Category Weight
        if category and category in self.category_weights:
            return self.category_weights[category]
        # 3. Base Weight
        return self.base_nrci

    def export_frame(self) -> str:
        def ubp_json_serializer(obj):
            if isinstance(obj, Fraction):
                return f"{obj.numerator}/{obj.denominator}"
            raise TypeError(f"Type {type(obj)} not serializable")

        data = {
            "frame_id": self.frame_id,
            "description": self.description,
            "base_nrci": self.base_nrci,
            "weights": self.weights,
            "category_weights": self.category_weights
        }
        return json.dumps(data, indent=2, default=ubp_json_serializer)

# --- 2. THE GRAVITATIONAL CORTEX ---
class GravitationalCortex:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.anchors: Dict[str, List[int]] = {}
        self.active_frame = FrameOfMind("DEFAULT")
        self.EVENT_HORIZON = Fraction(1, 200) 

    def load_anchor(self, ubp_id: str, vector: List[int]):
        self.anchors[ubp_id] = vector

    def set_frame(self, frame):
        # Support both local FrameOfMind and System FrameOfMind objects
        fid = getattr(frame, 'frame_id', getattr(frame, 'name', 'UNKNOWN'))
        print(f"\n[CORTEX] Shifting Frame of Mind to: {fid}")
        self.active_frame = frame

    def vectorize(self, text: str) -> List[int]:
        h = hashlib.sha256(text.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        # Map to 24 bits
        return [(val >> i) & 1 for i in range(23, -1, -1)]

    def observe(self, concept: str, category: str = None):
        fid = getattr(self.active_frame, 'frame_id', 'DEFAULT')
        print(f"\n[OBSERVER] Analyzing: '{concept}' (Frame: {fid})")
        
        input_vec = self.vectorize(concept)
        
        best_anchor = None
        max_pull = Fraction(-1, 1)
        
        for uid, vec in self.anchors.items():
            dist = BinaryLinearAlgebra.hamming_distance(input_vec, vec)
            
            # Use the system-standard get_weight method
            # Note: In a full implementation, we'd look up the category of 'uid'
            mass = self.active_frame.get_weight(uid, category)
            
            # Gravity Formula: Mass / Distance^2
            pull = mass / ((dist + 1) ** 2)
            
            if pull > max_pull:
                max_pull = pull
                best_anchor = uid

        if max_pull >= self.EVENT_HORIZON:
            print(f"  [!] CAPTURE: Snapped to '{best_anchor}' (Pull {float(max_pull):.4f})")
            return best_anchor
        else:
            print(f"  [?] FREE FLOATING: No anchor had sufficient gravity.")
            return None