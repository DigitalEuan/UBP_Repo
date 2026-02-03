# UBP Frame of Mind System v4.3.1 (Fraction-Aware)
import json
import os
from fractions import Fraction

class FrameOfMind:
    def __init__(self, frame_id, description="", base_nrci=0.5):
        self.frame_id = frame_id
        self.description = description
        # Convert incoming base_nrci to Fraction
        self.base_nrci = Fraction(base_nrci).limit_denominator()
        self.weights = {}
        self.category_weights = {} 

    def set_weight(self, ubp_id, nrci): 
        self.weights[ubp_id] = Fraction(nrci).limit_denominator()
        
    def set_category_weight(self, category, nrci): 
        self.category_weights[category] = Fraction(nrci).limit_denominator()

    def get_weight(self, ubp_id, category=None):
        if ubp_id in self.weights: return self.weights[ubp_id]
        if category and category in self.category_weights: return self.category_weights[category]
        return self.base_nrci

    def to_dict(self): 
        # Export as p/q strings for Bridge Compatibility
        return {
            'frame_id': self.frame_id, 
            'description': self.description, 
            'base_nrci': f"{self.base_nrci.numerator}/{self.base_nrci.denominator}", 
            'weights': {k: f"{v.numerator}/{v.denominator}" for k, v in self.weights.items()},
            'category_weights': {k: f"{v.numerator}/{v.denominator}" for k, v in self.category_weights.items()}
        }

class FOMManager:
    def __init__(self, index_file='ubp_fom_index.json'):
        self.frames = {}; self.active_frame = None; self.index_file = index_file; self.load_index()

    def load_index(self):
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                    # Handle both List and Dict formats
                    frames_data = data if isinstance(data, list) else data.values()
                    for f_data in frames_data:
                        fid = f_data.get('frame_id')
                        if fid:
                            frame = FrameOfMind(fid, f_data.get('description', ''), f_data.get('base_nrci', 0.5))
                            # Load weights and convert to Fractions
                            for k, v in f_data.get('weights', {}).items():
                                frame.set_weight(k, v)
                            for k, v in f_data.get('category_weights', {}).items():
                                frame.set_category_weight(k, v)
                            self.frames[fid] = frame
                    if self.frames: self.active_frame = list(self.frames.keys())[0]
            else:
                 self.frames["FOM_DEFAULT"] = FrameOfMind("FOM_DEFAULT", "Balanced Standard Bias", 0.5)
                 self.active_frame = "FOM_DEFAULT"
        except Exception as e: print(f"[FOM] Error loading index: {e}")

    def save_index(self):
        try:
             data = [f.to_dict() for f in self.frames.values()]
             with open(self.index_file, 'w') as f: json.dump(data, f, indent=4)
        except Exception as e: print(f"[FOM] Error saving: {e}")

    def switch_frame(self, frame_id):
        if frame_id in self.frames: self.active_frame = frame_id; return True
        return False

    def get_active_frame(self): return self.frames[self.active_frame] if (self.active_frame and self.active_frame in self.frames) else None
    def get_mass(self, ubp_id, category=None): return self.get_active_frame().get_weight(ubp_id, category) if self.get_active_frame() else Fraction(1, 2)

FOM_MANAGER = FOMManager()