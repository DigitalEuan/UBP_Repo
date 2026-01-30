"""
TGIC-Capable Engine (Exact, Float-Free, Deterministic) v4.4
===========================================================
Updates:
- REMOVED: 'random' library (Non-deterministic).
- ADDED: 'hashlib' for content-addressable determinism.
- The 'step' function now behaves identically for identical inputs.

Triad-Graph Interaction Constraint (TGIC)
Author: Euan R A Craig, New Zealand
Date: 10 January 2026
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
import hashlib
from ubp_core_v4_2_6_COMBINED import (
    GOLAY_DECODER,
    LEECH_ENHANCED,
    BinaryLinearAlgebra
)

# --- Constants ---
PHASE_MOD = 256  # 8-bit phase

# --- Helper Functions ---
def mod_phase(x: int) -> int:
    return x % PHASE_MOD

def phase_dist(a: int, b: int) -> int:
    d = abs(a - b)
    if d > 128:
        d = 256 - d
    return d

# --- Deterministic RNG ---
class DeterministicFlux:
    """Generates pseudo-random numbers derived from the system state hash."""
    def __init__(self, seed_obj):
        # Create a seed from the string representation of the input object
        seed_str = str(seed_obj)
        self.digest = hashlib.sha256(seed_str.encode()).digest()
        self.idx = 0

    def _next_byte(self) -> int:
        if self.idx >= len(self.digest):
            # Reseed with own digest to continue stream
            self.digest = hashlib.sha256(self.digest).digest()
            self.idx = 0
        val = self.digest[self.idx]
        self.idx += 1
        return val

    def randint(self, a, b):
        """Deterministic randint(a, b)."""
        span = b - a + 1
        val = self._next_byte()
        return a + (val % span)

    def choice(self, seq):
        """Deterministic choice."""
        if not seq: return None
        idx = self.randint(0, len(seq) - 1)
        return list(seq)[idx]

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

# --- 1. SEMANTIC REACTION LAYER (The Beaker) ---
class SemanticBeaker:
    @staticmethod
    def react(id_a: str, id_b: str):
        if not HEX_DB_EXACT.registry: HEX_DB_EXACT.load_memory()
        
        e_a = HEX_DB_EXACT.find_by_id(id_a)
        e_b = HEX_DB_EXACT.find_by_id(id_b)
        
        if not e_a or not e_b: return None

        # Interaction (XOR) + Reflexive Snap
        raw_v = [(a ^ b) for a, b in zip(e_a['vector'], e_b['vector'])]
        decoded, _, _ = GOLAY_DECODER.decode(raw_v)
        product_v = GOLAY_DECODER.encode(decoded)
        
        # Find Resonance
        best_match = None
        min_dist = 25
        for fp, entry in HEX_DB_EXACT.registry.items():
            dist = BinaryLinearAlgebra.hamming_distance(product_v, entry.get('vector', []))
            if dist < min_dist:
                min_dist = dist
                best_match = entry
        
        return {
            "product_vector": product_v,
            "match": best_match['ubp_id'] if best_match else "UNKNOWN",
            "stability": min_dist
        }

# --- 2. LOW-LEVEL LATTICE LAYER (TGIC) ---
class TGICExactEngine:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.leech = LEECH_ENHANCED
        self.SHELL_TARGET = 12
        self.ANGLE_TOLERANCE = 16

    def calculate_interaction_cost(self, v1: List[int], v2: List[int]) -> int:
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
        
        # Initialize Deterministic Flux based on current state S
        # This ensures that if S is the same, the 'random' choice is the same.
        # We sort keys to ensure consistent ordering for the hash.
        state_repr = str(sorted(S.items(), key=lambda x: x[0]))
        flux = DeterministicFlux(state_repr)

        coord = flux.choice(list(S.keys()))
        off_old = S[coord]
        
        flip_idx = flux.randint(0, 23)
        fulcrum = (flip_idx + 12) % 24
        mask = [0]*24
        mask[flip_idx] = 1
        toggle = Toggle(load_bits=(flip_idx,), fulcrum_bit=fulcrum, effort=10)
        
        d_phi = flux.randint(-5, 5)
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
