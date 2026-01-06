"""
TGIC-Capable Engine (Exact, Float-Free) v4.3.2 (KERNEL COMPATIBLE)
==================================================================
Updates:
- Added calculate_interaction_cost for Kernel geometric reasoning.

Tria-Graph Interaction Constraint (TGIC)
Author: Euan R A Craig, New Zealand
Date: 06 January 2026

"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
import random
from ubp_core_v4_2_6_COMBINED import (
    GOLAY_DECODER,
    LEECH_ENHANCED,
    BinaryLinearAlgebra,
    LeechPointScaled
)

# --- Constants ---
PHASE_MOD = 256  # 8-bit phase

# --- Helper Functions ---
def mod_phase(x: int) -> int:
    return x % PHASE_MOD

def phase_dist(a: int, b: int) -> int:
    """Circular distance in 8-bit space."""
    d = abs(a - b)
    if d > 128:
        d = 256 - d
    return d

# --- Data Structures ---
Coord = Tuple[int, int, int]

@dataclass(frozen=True)
class OffBit:
    v: Tuple[int, ...]
    phi: int

    def with_updates(self, new_v: Optional[List[int]] = None, delta_phi: int = 0) -> "OffBit":
        v2 = tuple(new_v) if new_v is not None else self.v
        return OffBit(v=v2, phi=mod_phase(self.phi + delta_phi))

@dataclass(frozen=True)
class Toggle:
    load_bits: Tuple[int, ...]
    fulcrum_bit: int
    effort: int

@dataclass(frozen=True)
class Proposal:
    coord: Coord
    flip_mask: Tuple[int, ...]
    delta_phi: int
    toggle: Toggle

# --- The Engine ---
class TGICExactEngine:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.leech = LEECH_ENHANCED
        self.SHELL_TARGET = 12
        self.ANGLE_TOLERANCE = 16

    def calculate_interaction_cost(self, v1: List[int], v2: List[int]) -> int:
        """
        Geometric Cost for Kernel Reasoner.
        Returns Hamming Distance (Spatial Cost).
        """
        # Ensure inputs are lists for the algebra module
        l1 = list(v1) if isinstance(v1, (tuple, list)) else [0]*24
        l2 = list(v2) if isinstance(v2, (tuple, list)) else [0]*24
        return BinaryLinearAlgebra.hamming_distance(l1, l2)

    def neighbors(self, c: Coord) -> List[Coord]:
        x, y, z = c
        return [
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z),
            (x, y, z+1), (x, y, z-1)
        ]

    def _site_energy(self, coord: Coord, off: OffBit, S: Dict[Coord, OffBit]) -> int:
        E = 0
        for n in self.neighbors(coord):
            if n in S:
                off2 = S[n]
                h_dist = BinaryLinearAlgebra.hamming_distance(list(off.v), list(off2.v))
                p_dist = phase_dist(off.phi, off2.phi)
                E += h_dist * p_dist
        return E

    def energy(self, S: Dict[Coord, OffBit]) -> int:
        E = 0
        seen_edges = set()
        for c, off in S.items():
            for n in self.neighbors(c):
                if n in S:
                    edge = tuple(sorted((c, n)))
                    if edge in seen_edges: continue
                    seen_edges.add(edge)
                    off2 = S[n]
                    h_dist = BinaryLinearAlgebra.hamming_distance(list(off.v), list(off2.v))
                    p_dist = phase_dist(off.phi, off2.phi)
                    E += h_dist * p_dist
        return E

    def gamma_sphere(self, off: OffBit) -> bool:
        _, _, synd = self.golay.decode(list(off.v))
        return synd <= 3

    def gamma_angle(self, S: Dict[Coord, OffBit], prop: Proposal, off_new: OffBit) -> bool:
        neigh_phis = [S[n].phi for n in self.neighbors(prop.coord) if n in S]
        if not neigh_phis: return True
        avg_phi = sum(neigh_phis) // len(neigh_phis)
        return phase_dist(off_new.phi, avg_phi) < self.ANGLE_TOLERANCE

    def gamma_conservation(self, prop: Proposal, off_old: OffBit, off_new: OffBit) -> bool:
        f = prop.toggle.fulcrum_bit
        return off_old.v[f] == off_new.v[f]

    def step(self, S: Dict[Coord, OffBit]) -> Tuple[Dict[Coord, OffBit], dict]:
        if not S: return S, {"status": "empty"}
        coord = random.choice(list(S.keys()))
        off_old = S[coord]
        flip_idx = random.randint(0, 23)
        fulcrum = (flip_idx + 12) % 24
        mask = [0]*24
        mask[flip_idx] = 1
        toggle = Toggle(load_bits=(flip_idx,), fulcrum_bit=fulcrum, effort=10)
        d_phi = random.randint(-5, 5)
        prop = Proposal(coord, tuple(mask), d_phi, toggle)
        new_v = [b ^ m for b, m in zip(off_old.v, mask)]
        off_new = off_old.with_updates(new_v=new_v, delta_phi=d_phi)
        
        if not self.gamma_conservation(prop, off_old, off_new):
            return S, {"status": "rejected", "reason": "conservation"}
        if not self.gamma_sphere(off_new):
            return S, {"status": "rejected", "reason": "sphere_collapse"}
        if not self.gamma_angle(S, prop, off_new):
            return S, {"status": "rejected", "reason": "phase_decoherence"}
            
        E_local_old = self._site_energy(coord, off_old, S)
        E_local_new = self._site_energy(coord, off_new, S)
        dE = E_local_new - E_local_old
        
        if dE <= toggle.effort:
            S_new = S.copy()
            S_new[coord] = off_new
            return S_new, {"status": "accepted", "dE": dE}
        else:
            return S, {"status": "rejected", "reason": "energy_barrier", "dE": dE}
