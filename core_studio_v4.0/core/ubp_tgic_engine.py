"""
UBP TGIC ENGINE v6.2 (Relational Master Edition)
================================================
The definitive TGIC implementation. 
Integrates all 9 internal interactions + Cross-Node Relational Gravity.

STANDARDS:
- Internal Harmony: 9 Pairwise Interactions (X, Y, Z blocks)
- External Harmony: Relational Pull (Hamming-weighted attraction)
- Hardware: Leech Tax + Coherence Pressure (d > 3 penalty)

Author: E R A Craig & UBP Research Cortex v4.2.7
Date: 03 March 2026
"""
import hashlib
from fractions import Fraction
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any

try:
    from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra, SUBSTRATE
    CORE_AVAILABLE = True
    CONST = SUBSTRATE.get_constants(50)
except ImportError:
    CORE_AVAILABLE = False
    CONST = {'Y': Fraction(2646, 10000), 'Y_INV': Fraction(10000, 2646)}

@dataclass(frozen=True)
class OffBit:
    v: Tuple[int, ...]
    phi: int
    def with_updates(self, new_v=None, delta_phi=0):
        return OffBit(v=tuple(new_v) if new_v is not None else self.v, phi=(self.phi + delta_phi) % 256)

class TGICInteractionEngine:
    def __init__(self):
        self.y_const = CONST['Y']
        self.interaction_weight = Fraction(5, 1) 

    def resonance_op(self, b_i, b_j):
        return Fraction(0) if b_i == b_j else self.y_const / 20

    def entanglement_op(self, b_i, b_j):
        return Fraction(-1, 200) if b_i == 1 and b_j == 1 else Fraction(0)

    def superposition_op(self, b_i, b_j):
        states = [Fraction(b_i), Fraction(b_j), Fraction((b_i + b_j) % 2)]
        return sum(s * Fraction(1, 3) for s in states)

    def mixed_op(self, x, y, z, mode):
        if mode == 'xyz': return Fraction(min(x, y)) * Fraction(z)
        if mode == 'yzx': return Fraction(abs(y - z)) * Fraction(x)
        if mode == 'zxy': return Fraction(max(z, x)) * Fraction(y)
        return Fraction(0)

    def calculate_internal_cost(self, v):
        """Sum of all 9 interactions within a single 24-bit vector."""
        total = Fraction(0)
        for i in range(8):
            x, y, z = v[i], v[i+8], v[i+16]
            # Pairwise
            total += self.resonance_op(x, y)
            total += self.resonance_op(y, x)
            total += self.entanglement_op(x, z)
            total += self.entanglement_op(z, x)
            total += self.superposition_op(y, z)
            total += self.superposition_op(z, y)
            # Mixed
            total += self.mixed_op(x, y, z, 'xyz')
            total += self.mixed_op(y, z, x, 'yzx')
            total += self.mixed_op(z, x, y, 'zxy')
        return total * self.interaction_weight

class TGICExactEngine:
    def __init__(self):
        self.interactions = TGICInteractionEngine()
        self.golay = GOLAY_ENGINE if CORE_AVAILABLE else None
        self.leech = LEECH_ENGINE if CORE_AVAILABLE else None
        self.y_const = CONST['Y']

    def get_relational_pull(self, coord_target, v_target, S):
        """Calculates the 'Gravity' exerted by all other nodes."""
        pull = Fraction(0)
        for coord, off in S.items():
            if coord == coord_target: continue
            dist = BinaryLinearAlgebra.hamming_distance(list(v_target), list(off.v))
            # Gravity: Pull increases as distance decreases (Convergence)
            # We subtract this from energy to reward proximity
            pull += Fraction(1, (dist + 1))
        return pull * (self.y_const / 2)

    def get_node_energy(self, coord, v, S):
        """Total Energy = Internal Cost + Leech Tax + Coherence Penalty - Relational Pull."""
        i_cost = self.interactions.calculate_internal_cost(v)
        l_tax = self.leech.calculate_symmetry_tax(v) if self.leech else Fraction(0)
        
        dist = 0
        if self.golay: _, _, dist = self.golay.decode(v)
        coherence_penalty = Fraction(dist**4, 1) if dist > 3 else Fraction(0)
        
        pull = self.get_relational_pull(coord, v, S)
        
        return i_cost + l_tax + coherence_penalty - pull

    def step(self, S):
        if not S: return S, {"status": "empty"}
        state_repr = str(sorted(S.items(), key=lambda x: x[0]))
        digest = hashlib.sha256(state_repr.encode()).digest()
        
        coord = list(S.keys())[digest[0] % len(S)]
        off_old = S[coord]
        
        flip_idx = digest[1] % 24
        new_v = list(off_old.v)
        new_v[flip_idx] ^= 1
        
        energy_old = self.get_node_energy(coord, list(off_old.v), S)
        energy_new = self.get_node_energy(coord, new_v, S)
        
        # Acceptance with Metabolic Drive (Y/4)
        if energy_new < (energy_old + self.y_const / 4):
            S_new = S.copy()
            S_new[coord] = off_old.with_updates(new_v=new_v)
            dist = 0
            if self.golay: _, _, dist = self.golay.decode(new_v)
            return S_new, {
                "status": "accepted", 
                "delta": float(energy_new - energy_old), 
                "dist": dist,
                "coord": coord,
                "bit": flip_idx
            }
        
        return S, {"status": "rejected"}

    def get_total_energy(self, S):
        return sum(self.get_node_energy(c, list(off.v), S) for c, off in S.items())