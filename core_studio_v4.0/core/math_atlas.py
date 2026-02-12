"""
MathAtlas v1.3 - The Universal Compass Engine
=============================================
"Truth is Alignment. Error is Tilt."

Updates:
1. UNIVERSAL NORTH: Hardcoded the discovered systemic axis.
2. GEOMETRIC CHARGE: Automatic 'Tilt' calculation for all objects.
3. ROBUST PARSING: v1.2.2 parser fixes included.
"""

import json
import hashlib
import decimal
import math
import numpy as np
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any, Union

# --- UBP CORE INTEGRATION ---
try:
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

# --- THE UNIVERSAL CONSTANT ---
UNIVERSAL_NORTH = np.array([-0.30656966974248284, -0.9197090092274486, 0.2452557357939863])

decimal.getcontext().prec = 100

class MathAtlasConstants:
    _PI_CF = [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2, 2, 2, 
              1, 84, 2, 1, 1, 15, 3, 13, 1, 4, 2, 6, 6, 99, 1, 2, 2, 6, 3, 5, 
              1, 1, 6, 8, 1, 7, 1, 6, 1, 99, 7, 4, 1, 3, 3, 1, 4, 1]
    
    @classmethod
    def get_pi(cls) -> Fraction:
        x = Fraction(cls._PI_CF[-1], 1)
        for c in reversed(cls._PI_CF[:-1]): x = Fraction(c, 1) + Fraction(1, x)
        return x

PI_CONSTANT = MathAtlasConstants.get_pi()
Y_CONSTANT = Fraction(1, 1) / (PI_CONSTANT + Fraction(2, 1)/PI_CONSTANT)

@dataclass
class MathematicalObject:
    primitives: List[Tuple] = field(default_factory=list)
    description: str = ""
    tax: Fraction = field(init=False)
    voxels: List[Tuple[int, int, int, str]] = field(init=False)

    def __post_init__(self):
        self.voxels = []
        if not self.primitives:
            self.tax = PI_CONSTANT
            self.voxels.append((0, 0, 0, "#ffffff"))
        else:
            self._construct_manifold()

    def _construct_manifold(self, offset=(0,0,0)):
        total_tax = Fraction(0, 1)
        x, y, z = offset
        for op_tuple in self.primitives:
            op = op_tuple[0]
            if op == 'D':
                mag = op_tuple[1] if len(op_tuple) > 1 else 1
                for _ in range(mag):
                    x += 1
                    self.voxels.append((x, y, z, "#00ffff"))
                    total_tax += Y_CONSTANT
            elif op == 'X':
                mag = op_tuple[1] if len(op_tuple) > 1 else 1
                for _ in range(mag):
                    x -= 1
                    self.voxels.append((x, y, z, "#ff0000"))
                    total_tax += Y_CONSTANT
            elif op == 'N':
                child = op_tuple[1]
                child._construct_manifold(offset=(x, y + 1, z))
                self.voxels.extend(child.voxels)
                total_tax += child.tax + (Y_CONSTANT / 2)
            elif op == 'J':
                child = op_tuple[1]
                child._construct_manifold(offset=(x, y, z + 1))
                self.voxels.extend(child.voxels)
                total_tax += child.tax + (Y_CONSTANT / 4)
        self.tax = total_tax + Fraction(len(self.voxels)**2, 800)

    def get_vector(self) -> List[int]:
        if not CORE_AVAILABLE: return [0]*24
        geo_str = str(sorted(list(set(self.voxels))))
        h = hashlib.sha256(geo_str.encode()).digest()
        msg_int = ((h[0] << 8) | h[1]) & 0xFFF
        return GOLAY_DECODER.encode([(msg_int >> i) & 1 for i in range(11, -1, -1)])

    def get_charge(self) -> float:
        """Calculates the Tilt relative to Universal North."""
        vec = self.get_vector()
        o = np.array([float(sum(vec[0:8])-4), float(sum(vec[8:16])-4), float(sum(vec[16:24])-4)])
        mag = np.linalg.norm(o)
        if mag == 0: return 0.0
        unit_north = UNIVERSAL_NORTH / np.linalg.norm(UNIVERSAL_NORTH)
        cos_theta = np.dot(o, unit_north) / mag
        return math.degrees(math.acos(max(-1, min(1, cos_theta))))

def PositiveInteger(n: int) -> MathematicalObject:
    return MathematicalObject(primitives=[('D', n)], description=f"+{n}")

def Rational(p: int, q: int) -> MathematicalObject:
    return MathematicalObject(primitives=[('N', PositiveInteger(p)), ('J', PositiveInteger(q))], description=f"{p}/{q}")

def J_List(objs: List[MathematicalObject], label="") -> MathematicalObject:
    return MathematicalObject(primitives=[('J', obj) for obj in objs], description=label)

def construct_element_atlas(ubp_id, name, math_str):
    dims = []
    for p in math_str.split('|'):
        if '=' in p:
            k, v = p.split('=', 1)
            try:
                if '/' in v:
                    n, d = v.split('/')
                    dims.append(Rational(int(n), int(d)))
                else:
                    dims.append(PositiveInteger(int(float(v))))
            except: continue
    manifold = J_List(dims, label=name)
    tax = manifold.tax
    nrci = Fraction(1, 1) / (Fraction(1, 1) + (tax * Fraction(1, 10)))
    return {
        "ubp_id": ubp_id, "name": name, "math": math_str,
        "math_exact": {"tax": {"n": tax.numerator, "d": tax.denominator}, "nrci": {"n": nrci.numerator, "d": nrci.denominator}},
        "nrci_score": float(nrci), "vector": manifold.get_vector(),
        "geometric_charge": manifold.get_charge(),
        "atlas_metadata": {"voxel_count": len(manifold.voxels)}
    }

class ExactRationalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Fraction): return {"n": obj.numerator, "d": obj.denominator, "s": str(obj)}
        return super().default(obj)