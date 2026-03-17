import json
import hashlib
import re
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra, SUBSTRATE
from ubp_kb_architect import KBArchitect

# System Constants
CONST = SUBSTRATE.get_constants(50)
Y_CONST = CONST['Y']

@dataclass
class CortexAtom:
    label: str
    value: Fraction
    vector: List[int]
    nrci: Fraction
    tax: Fraction
    tilt: float
    tier: int
    category: str
    hierarchy: str
    parents: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "label": self.label,
            "value": str(self.value),
            "vector": self.vector,
            "nrci": str(self.nrci),
            "tax": str(self.tax),
            "tilt": self.tilt,
            "tier": self.tier,
            "category": self.category,
            "hierarchy": self.hierarchy
        }

class UBPPyVM:
    def __init__(self, kb_path='ubp_system_kb.json', lattice_path='ubp_py_lattice.json', trace_path='ubp_py_trace.json', fom_index_path='ubp_fom_index.json'):
        print(f"[VM] Initializing v2.3.4 (SOP_002 Final Patch)")
        self.env = {}
        self.trace = []
        self.kb_path = kb_path
        self.lattice_path = lattice_path
        self.trace_path = trace_path
        self.fom_path = fom_index_path
        self.kb_cache = {}
        self._load_kb()

    def _load_kb(self):
        try:
            with open(self.kb_path, 'r') as f:
                self.kb_cache = json.load(f)
        except:
            self.kb_cache = {}

    def log(self, msg):
        print(f"[VM] {msg}")
        self.trace.append(msg)

    def let(self, label, val_str, tier=0, category="QUANTITY"):
        math_dna = f"Val={val_str}|Cat={category}"
        vec = KBArchitect.generate_vector(math_dna)
        # FIXED: Pass both math_dna and vec
        tax, nrci = KBArchitect.calculate_metrics(math_dna, vec)

        self.env[label] = CortexAtom(
            label=label, value=Fraction(val_str), vector=vec,
            nrci=nrci, tax=tax, tilt=KBArchitect.calculate_tilt(vec), 
            tier=tier, category=category, hierarchy="atomic"
        )
        self.log(f"LET {label} = {val_str}")

    def import_atom(self, ubp_id, alias=None):
        target_label = alias if alias else ubp_id
        entry = None
        for key, val in self.kb_cache.items():
            if val.get('ubp_id') == ubp_id:
                entry = val
                break

        if entry:
            atlas = entry.get('atlas', {})
            self.env[target_label] = CortexAtom(
                label=target_label,
                value=Fraction(1, 1),
                vector=atlas.get('vector'),
                nrci=Fraction(atlas.get('nrci', '1/1')),
                tax=Fraction(atlas.get('tax', '0/1')),
                tilt=atlas.get('tilt', 0.0),
                tier=0,
                category=entry.get('tags', ['IMPORTED'])[0],
                hierarchy=atlas.get('hierarchy', 'atomic')
            )
            self.log(f"IMPORT {ubp_id} as {target_label}")
        else:
            self.log(f"ERROR: {ubp_id} not found in KB.")

    def synth(self, label, recipe_str):
        self.log(f"SYNTH {label} FROM {recipe_str}")
        components = re.findall(r'(\d+)x([A-Za-z0-9_]+)', recipe_str)
        composite_vec = [0] * 24
        total_val = Fraction(0)
        for count_str, comp_label in components:
            count = int(count_str)
            if comp_label in self.env:
                atom = self.env[comp_label]
                for _ in range(count):
                    composite_vec = [(a + b) % 2 for a, b in zip(composite_vec, atom.vector)]
                    total_val += atom.value

        decoded, _, _ = GOLAY_ENGINE.decode(composite_vec)
        snapped = GOLAY_ENGINE.encode(decoded)

        math_dna = f"Synth={label}|Recipe={recipe_str}"
        # FIXED: Pass both math_dna and snapped vector
        tax, nrci = KBArchitect.calculate_metrics(math_dna, snapped)

        self.env[label] = CortexAtom(
            label=label, value=total_val, vector=snapped,
            nrci=nrci, tax=tax, tilt=KBArchitect.calculate_tilt(snapped),
            tier=1, category="SYNTHESIS", hierarchy=recipe_str
        )

    def spiral(self, label, iterations, transform_name, label_prefix):
        if label not in self.env: return
        current = self.env[label]
        
        # MATH_CONST_PHI_001 Vector (The Growth Primitive)
        PHI_VEC = [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]
        
        for i in range(1, iterations + 1):
            new_label = f"{label_prefix}_{i}"
            new_val = current.value + Fraction(1, 1)
            
            # V5.8 SPIRAL DYNAMICS: 1-Bit Shift + Phi XOR
            shifted = current.vector[-1:] + current.vector[:-1]
            new_vec = [(b ^ p) for b, p in zip(shifted, PHI_VEC)]
            
            decoded, _, _ = GOLAY_ENGINE.decode(new_vec)
            snapped = GOLAY_ENGINE.encode(decoded)

            math_dna = f"Spiral={new_label}|Parent={label}"
            tax, nrci = KBArchitect.calculate_metrics(math_dna, snapped)

            self.env[new_label] = CortexAtom(
                label=new_label, value=new_val, vector=snapped,
                nrci=nrci, tax=tax, tilt=KBArchitect.calculate_tilt(snapped),
                tier=current.tier + i, category="SPIRAL", hierarchy=f"SPIRAL({label})"
            )
            current = self.env[new_label]
        self.log(f"SPIRAL complete: {iterations} iterations (Phi-Shift Dynamics).")

    def reflex(self, threshold):
        to_remove = []
        for label, atom in self.env.items():
            if atom.nrci < threshold:
                decoded, _, _ = GOLAY_ENGINE.decode(atom.vector)
                corrected = GOLAY_ENGINE.encode(decoded)

                math_dna = f"Reflex={label}|Original={atom.hierarchy}"
                # FIXED: Pass both math_dna and corrected vector
                new_tax, new_nrci = KBArchitect.calculate_metrics(math_dna, corrected)

                if new_nrci >= threshold:
                    atom.vector = corrected
                    atom.nrci = new_nrci
                    atom.tax = new_tax
                    self.log(f"REFLEX: Corrected {label}")
                else:
                    to_remove.append(label)
                    self.log(f"REFLEX: Pruned {label} (NRCI {float(atom.nrci):.4f} < {float(threshold)})")
        for label in to_remove:
            del self.env[label]

    def commit(self):
        data = {k: v.to_dict() for k, v in self.env.items()}
        with open(self.lattice_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.log(f"Lattice committed to {self.lattice_path}")

    def export_env(self, path):
        data = {k: v.to_dict() for k, v in self.env.items()}
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        self.log(f"Environment exported to {path}")

    def export_trace(self, path):
        with open(path, 'w') as f:
            json.dump(self.trace, f, indent=2)

    def to_scene_3d(self):
        spheres = []
        for a in self.env.values():
            import math
            rad = math.radians(a.tilt)
            dist = float(a.tax) * 2
            spheres.append({
                "x": math.cos(rad) * dist, "y": a.tier * 2, "z": math.sin(rad) * dist, 
                "r": 0.5, "color": "#00ff00" if float(a.nrci) > 0.8 else "#ffff00", "label": a.label
            })
        return {"spheres": spheres, "lines": []}
