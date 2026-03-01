import json
import hashlib
import re
from fractions import Fraction
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra, UBPUltimateSubstrate
from ubp_kb_architect import KBArchitect

# System Constants
CONST = UBPUltimateSubstrate.get_constants(50)
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
        print(f"[VM] Initializing v2.3.0 (Full Feature Set)")
        self.env = {}
        self.trace = []
        self.kb_path = kb_path
        self.lattice_path = lattice_path
        self.trace_path = trace_path
        self.fom_path = fom_index_path
        self.kb_cache = None
        self.id_map = {}

    def log(self, msg):
        print(f"[VM] {msg}")
        self.trace.append(msg)

    def let(self, label, val_str, tier=0, category="QUANTITY"):
        math_dna = f"Val={val_str}|Cat={category}"
        vec = KBArchitect.generate_vector(math_dna)
        tax, nrci = KBArchitect.calculate_metrics(math_dna)
        self.env[label] = CortexAtom(
            label=label, value=Fraction(val_str), vector=vec,
            nrci=nrci, tax=tax, tilt=KBArchitect.calculate_tilt(vec), 
            tier=tier, category=category, hierarchy="atomic"
        )
        self.log(f"LET {label} = {val_str}")

    def spiral(self, label, iterations, transform_name, label_prefix):
        if label not in self.env: return
        current = self.env[label]
        for i in range(1, iterations + 1):
            new_label = f"{label_prefix}_{i}"
            new_val = current.value + Fraction(1, 1)
            new_vec = [(b ^ 1) if idx % 2 == 0 else b for idx, b in enumerate(current.vector)]
            decoded, _, _ = GOLAY_ENGINE.decode(new_vec)
            snapped = GOLAY_ENGINE.encode(decoded)

            tax = LEECH_ENGINE.calculate_symmetry_tax(snapped)
            nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)

            self.env[new_label] = CortexAtom(
                label=new_label, value=new_val, vector=snapped,
                nrci=nrci, tax=tax, tilt=KBArchitect.calculate_tilt(snapped),
                tier=current.tier + i, category="SPIRAL", hierarchy=f"SPIRAL({label})"
            )
            current = self.env[new_label]
        self.log(f"SPIRAL complete: {iterations} iterations.")

    def reflex(self, threshold):
        to_remove = []
        for label, atom in self.env.items():
            if atom.nrci < threshold:
                decoded, _, _ = GOLAY_ENGINE.decode(atom.vector)
                corrected = GOLAY_ENGINE.encode(decoded)
                new_tax = LEECH_ENGINE.calculate_symmetry_tax(corrected)
                new_nrci = Fraction(10, 1) / (Fraction(10, 1) + new_tax)

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