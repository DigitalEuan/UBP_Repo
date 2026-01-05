"""
TGIC-Capable Engine (Exact, Float-Free) v4.3.1 (FIXED)
======================================================

Version: 4.3.1
Author: Euan R A Craig, New Zealand
Date: 06 January 2026

Fixes:
- Method name mismatch (neighbors vs get_neighbors)
- Invalid dataclass arithmetic in energy calculation
- Undefined S_temp variable
- Implements proper local energy delta calculation

Dependencies: ubp_core_v4_2_6_COMBINED
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
Coord = Tuple[int, int, int]  # 3D coordinate representation

@dataclass(frozen=True)
class OffBit:
    v: Tuple[int, ...]  # 24 bits
    phi: int            # 0..255

    def with_updates(self, new_v: Optional[List[int]] = None, delta_phi: int = 0) -> "OffBit":
        v2 = tuple(new_v) if new_v is not None else self.v
        return OffBit(v=v2, phi=mod_phase(self.phi + delta_phi))

@dataclass(frozen=True)
class Toggle:
    load_bits: Tuple[int, ...]  # Indices allowed to flip
    fulcrum_bit: int            # Index FORBIDDEN to flip
    effort: int                 # Energy barrier

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
        
        # Physics Constants
        self.SHELL_TARGET = 12  # Norm^2 = 12 (Hemic Shell)
        self.ANGLE_TOLERANCE = 16 # approx pi/8 in 256-bin space

    def neighbors(self, c: Coord) -> List[Coord]:
        x, y, z = c
        # 6-neighborhood
        return [
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z),
            (x, y, z+1), (x, y, z-1)
        ]

    def _site_energy(self, coord: Coord, off: OffBit, S: Dict[Coord, OffBit]) -> int:
        """Calculates the interaction energy of a single site with its current neighbors."""
        E = 0
        for n in self.neighbors(coord):
            if n in S:
                off2 = S[n]
                # Hamming Distance (Spatial)
                h_dist = BinaryLinearAlgebra.hamming_distance(list(off.v), list(off2.v))
                # Phase Distance (Temporal/Resonant)
                p_dist = phase_dist(off.phi, off2.phi)
                
                # Coupling: E += Hamming * Phase
                E += h_dist * p_dist
        return E

    def energy(self, S: Dict[Coord, OffBit]) -> int:
        """
        Global Integer Energy:
        E = Sum(HammingDist(neighbors) * PhaseDist(neighbors))
        """
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

    # --- Gamma Gates (The Laws of Physics) ---
    
    def gamma_sphere(self, off: OffBit) -> bool:
        """Gate 1: Must stay on the Leech Shell (Correctable Golay Code)."""
        # "Existence" requires Syndrome <= 3 (Correctable)
        _, _, synd = self.golay.decode(list(off.v))
        return synd <= 3

    def gamma_angle(self, S: Dict[Coord, OffBit], prop: Proposal, off_new: OffBit) -> bool:
        """Gate 2: Phase Coherence with neighbors."""
        neigh_phis = [S[n].phi for n in self.neighbors(prop.coord) if n in S]
        if not neigh_phis: return True # Isolated is free
        
        # Simple consensus: Must be within tolerance of average neighbor phase
        avg_phi = sum(neigh_phis) // len(neigh_phis)
        return phase_dist(off_new.phi, avg_phi) < self.ANGLE_TOLERANCE

    def gamma_conservation(self, prop: Proposal, off_old: OffBit, off_new: OffBit) -> bool:
        """Gate 3: Fulcrum Bit must not flip."""
        f = prop.toggle.fulcrum_bit
        return off_old.v[f] == off_new.v[f]

    # --- Dynamics ---

    def step(self, S: Dict[Coord, OffBit]) -> Tuple[Dict[Coord, OffBit], dict]:
        if not S: return S, {"status": "empty"}
        
        # 1. Pick random site
        coord = random.choice(list(S.keys()))
        off_old = S[coord]
        
        # 2. Generate Toggle (Phenomenology)
        flip_idx = random.randint(0, 23)
        fulcrum = (flip_idx + 12) % 24 # Arbitrary fulcrum
        
        mask = [0]*24
        mask[flip_idx] = 1
        
        toggle = Toggle(load_bits=(flip_idx,), fulcrum_bit=fulcrum, effort=10)
        
        # 3. Propose Phase Shift
        d_phi = random.randint(-5, 5)
        
        prop = Proposal(coord, tuple(mask), d_phi, toggle)
        
        # 4. Apply Candidate
        new_v = [b ^ m for b, m in zip(off_old.v, mask)]
        off_new = off_old.with_updates(new_v=new_v, delta_phi=d_phi)
        
        # 5. Check Gates
        if not self.gamma_conservation(prop, off_old, off_new):
            return S, {"status": "rejected", "reason": "conservation"}
            
        if not self.gamma_sphere(off_new):
            return S, {"status": "rejected", "reason": "sphere_collapse"}
            
        if not self.gamma_angle(S, prop, off_new):
            return S, {"status": "rejected", "reason": "phase_decoherence"}
            
        # 6. Energy Check (Metropolis-like)
        # Calculate local energy difference only (Optimization)
        E_local_old = self._site_energy(coord, off_old, S)
        E_local_new = self._site_energy(coord, off_new, S)
        
        dE = E_local_new - E_local_old
        
        # Simple threshold acceptance
        if dE <= toggle.effort:
            S_new = S.copy()
            S_new[coord] = off_new
            return S_new, {"status": "accepted", "dE": dE}
        else:
            return S, {"status": "rejected", "reason": "energy_barrier", "dE": dE}

# --- Initialization Helper ---
def make_initial_state(n=5) -> Dict[Coord, OffBit]:
    S = {}
    # Create a small line of atoms
    for i in range(n):
        # Start with perfect codewords (Zero vector)
        v = tuple([0]*24)
        phi = 128 # Neutral phase
        S[(i,0,0)] = OffBit(v, phi)
    return S

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    print("========================================")
    print("   TGIC EXACT ENGINE v4.3.1 (FIXED)     ")
    print("========================================")
    
    engine = TGICExactEngine()
    state = make_initial_state(n=5)
    
    print(f"[INIT] System Size: {len(state)} atoms")
    print(f"[INIT] Initial Energy: {engine.energy(state)}")
    
    accepted = 0
    steps = 1000
    
    print(f"\n[RUN] Simulating {steps} steps...")
    for i in range(steps):
        state, meta = engine.step(state)
        if meta['status'] == 'accepted':
            accepted += 1
            
    print(f"\n[DONE] Simulation Complete.")
    print(f"   Accepted Moves: {accepted}/{steps}")
    print(f"   Final Energy:   {engine.energy(state)}")
    
    # Check final stability
    stable_atoms = sum(1 for off in state.values() if engine.gamma_sphere(off))
    print(f"   Stable Atoms:   {stable_atoms}/{len(state)}")
