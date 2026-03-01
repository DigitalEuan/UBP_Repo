"""
UBP-Py Runtime v2.1 (v5.3 Core)
===============================
The execution engine for UBP-Lang. Manages the "Environment" of 
geometric objects (Atoms) and their interactions.

UPDATES:
- SOP_002 Compliance: Atoms now have Tilt, Vector, and Hierarchy.
- Geometric Synthesis: Uses XOR for interaction, not just addition.
- Binding Audit: Calculates Symmetry Rebate on synthesis.

Author: Euan R A Craig & UBP Cortex
Date: 25 Feb 2026
"""

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
            "nrci": float(self.nrci),
            "tax": float(self.tax),
            "tilt": self.tilt,
            "tier": self.tier,
            "category": self.category,
            "hierarchy": self.hierarchy
        }

class UBPPyVM:
    def __init__(self, kb_path='ubp_system_kb.json'):
        self.env = {}
        self.trace = []
        self.energy_spent = Fraction(0)
        self.kb_path = kb_path
        self.kb_cache = None

    def _load_kb(self):
        if not self.kb_cache:
            try:
                with open(self.kb_path, 'r') as f:
                    self.kb_cache = json.load(f)
                # Create lookup map
                self.id_map = {v['ubp_id']: v for v in self.kb_cache.values()}
            except Exception as e:
                print(f"[VM] Error loading KB: {e}")
                self.kb_cache = {}
                self.id_map = {}

    def log(self, msg):
        print(f"[VM] {msg}")
        self.trace.append(msg)

    def let(self, label, val_str, tier=0, category="QUANTITY"):
        """Creates a new Atom from raw values."""
        # Use KBArchitect logic to generate vector/metrics
        math_dna = f"Val={val_str}|Cat={category}"
        vec = KBArchitect.generate_vector(math_dna)
        tax, nrci = KBArchitect.calculate_metrics(math_dna)
        tilt = KBArchitect.calculate_tilt(vec)
        
        self.env[label] = CortexAtom(
            label=label,
            value=Fraction(val_str),
            vector=vec,
            nrci=nrci,
            tax=tax,
            tilt=tilt,
            tier=tier,
            category=category,
            hierarchy="atomic"
        )
        self.log(f"LET {label} = {val_str} (Tax: {float(tax):.4f})")

    def import_atom(self, ubp_id, alias=None):
        """Imports an existing entry from the System KB."""
        self._load_kb()
        if ubp_id not in self.id_map:
            self.log(f"ERROR: {ubp_id} not found in KB.")
            return

        entry = self.id_map[ubp_id]
        label = alias if alias else ubp_id
        
        # Parse metrics
        atlas = entry.get('atlas', {})
        try:
            nrci = Fraction(atlas.get('nrci', '1/2'))
            tax = Fraction(atlas.get('tax', '1/1'))
        except:
            nrci, tax = Fraction(1, 2), Fraction(1, 1)

        self.env[label] = CortexAtom(
            label=label,
            value=Fraction(0), # Placeholder for KB items
            vector=atlas.get('vector', [0]*24),
            nrci=nrci,
            tax=tax,
            tilt=atlas.get('tilt', 0.0),
            tier=1, # Imported items are usually established
            category=entry.get('tags', ['UNKNOWN'])[0],
            hierarchy=atlas.get('hierarchy', 'imported')
        )
        self.log(f"IMPORT {ubp_id} as {label}")

    def synth(self, out_label, recipe_str):
        """
        Synthesizes a new Atom by reacting existing ones.
        Recipe format: "1xH + 2xO" (labels must exist in env)
        """
        parts = re.findall(r'(\d+)x([A-Za-z0-9_]+)', recipe_str)
        if not parts:
            self.log(f"ERROR: Invalid recipe '{recipe_str}'")
            return

        # 1. Noumenal Sum (XOR)
        result_vec = [0] * 24
        parents = []
        sum_tax = Fraction(0)

        for count_str, label in parts:
            count = int(count_str)
            if label not in self.env:
                self.log(f"ERROR: Atom '{label}' not defined.")
                return
            
            atom = self.env[label]
            parents.append(label)
            sum_tax += (atom.tax * count)
            
            # XOR logic: If count is odd, flip bits. If even, no net change.
            if count % 2 == 1:
                result_vec = [(a ^ b) for a, b in zip(result_vec, atom.vector)]

        # 2. Coherence Snap
        decoded, _, _ = GOLAY_ENGINE.decode(result_vec)
        snapped_vec = GOLAY_ENGINE.encode(decoded)
        
        # 3. Calculate New Metrics
        new_tax = LEECH_ENGINE.calculate_symmetry_tax(snapped_vec)
        new_nrci = Fraction(10, 1) / (Fraction(10, 1) + new_tax)
        new_tilt = KBArchitect.calculate_tilt(snapped_vec)
        
        # 4. Binding Efficiency
        rebate = sum_tax - new_tax
        
        self.env[out_label] = CortexAtom(
            label=out_label,
            value=Fraction(0),
            vector=snapped_vec,
            nrci=new_nrci,
            tax=new_tax,
            tilt=new_tilt,
            tier=max(self.env[p].tier for p in parents) + 1,
            category="COMPOSITE",
            hierarchy=recipe_str,
            parents=parents
        )
        
        self.log(f"SYNTH {out_label}: Tax={float(new_tax):.4f} (Rebate: {float(rebate):.4f})")

    def to_scene_3d(self):
        spheres = []
        lines = []
        for a in self.env.values():
            # Map Tilt/Tax to 3D position for visualization
            # X/Z = Tilt direction, Y = Tier/Complexity
            import math
            rad = math.radians(a.tilt)
            dist = float(a.tax) * 2
            x = math.cos(rad) * dist
            z = math.sin(rad) * dist
            y = a.tier * 5
            
            color = "#00ff00" if float(a.nrci) > 0.9 else "#ffff00"
            if a.category == "ENTROPY": color = "#ff0000"
            
            spheres.append({
                "x": x, "y": y, "z": z, 
                "r": 0.5, "color": color, "label": a.label
            })
            
            for p in a.parents:
                if p in self.env:
                    # Find parent pos (recalc needed or store in atom)
                    # For simplicity, we just skip lines in this basic export
                    pass
                    
        return {"spheres": spheres, "lines": lines}