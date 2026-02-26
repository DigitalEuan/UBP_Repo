"""
UBP PHYSICS BRIDGE v2.0 (Geometric Topology Edition)
====================================================
Integrates MathAtlas Voxel Logic into Physical Simulation.

CHANGELOG:
- Replaced SHA256 hashing with Spatial Voxel Hashing.
- Implemented 'Topological Folding' for frequencies.
- Light is now treated as a geometric structure, not a string.

SCALING:
- 1 Voxel = 10 THz (Terahertz).
- Example: Green Light (545nm) ~550 THz -> 55 Voxels.

Author: Euan R A Craig & UBP Cortex
Date: 23 Feb 2026
"""

import hashlib
import math
from fractions import Fraction
from typing import Dict, List, Any, Tuple

# Import v5.3 Core
try:
    from ubp_core_v5_3_merged import (
        GOLAY_ENGINE, 
        LEECH_ENGINE, 
        UBPUltimateSubstrate, 
        BinaryLinearAlgebra
    )
    CORE_AVAILABLE = True
except ImportError:
    print("[WARNING] Core not found. Running in standalone mode.")
    CORE_AVAILABLE = False

# --- 1. CONSTANTS ---
CONSTANTS = UBPUltimateSubstrate.get_constants(50) if CORE_AVAILABLE else {'Y_INV': Fraction(34,9)}
C_SPEED = 299792458 # m/s
VOXEL_SCALE_THZ = 10 # 1 Voxel = 10 THz

# --- 2. GEOMETRIC ENGINE ---
class TopologyEngine:
    """
    The 'Figurate Auditor'. Folds scalar counts into optimal 3D shapes.
    """
    @staticmethod
    def get_optimal_shape(n: int) -> List[Dict[str, int]]:
        """
        Folds 'n' voxels into the most compact shape possible (Cube > Square > Line).
        Returns a list of voxel coordinates.
        """
        if n <= 0: return []
        
        best_dims = [n, 1, 1]
        min_surface = 2 * n + 2 # Initial linear surface area
        
        # 1. Try 3D (Cube-like)
        limit_i = int(n**(1/3)) + 1
        for i in range(limit_i, 1, -1):
            if n % i == 0:
                rem = n // i
                limit_j = int(math.sqrt(rem)) + 1
                for j in range(limit_j, 1, -1):
                    if rem % j == 0:
                        k = rem // j
                        # Found a 3D factor set (i, j, k)
                        dims = [i, j, k]
                        surface = 2*(i*j + j*k + i*k)
                        if surface < min_surface:
                            min_surface = surface
                            best_dims = dims
                        break
        
        # 2. Try 2D (Square-like) if 3D didn't find a perfect block
        if best_dims == [n, 1, 1]:
            limit_i = int(math.sqrt(n)) + 1
            for i in range(limit_i, 1, -1):
                if n % i == 0:
                    j = n // i
                    dims = [i, j, 1]
                    surface = 2*(i*j + i + j) # Simplified perimeter proxy
                    if surface < min_surface:
                        min_surface = surface
                        best_dims = dims
                    break
        
        # 3. Generate Coordinates
        voxels = []
        dx, dy, dz = best_dims
        for x in range(dx):
            for y in range(dy):
                for z in range(dz):
                    voxels.append({"x": x, "y": y, "z": z})
        
        return voxels, best_dims

    @staticmethod
    def get_spatial_vector(voxels: List[Dict[str, int]]) -> List[int]:
        """
        SOP_002 Standard: Deterministic Spatial Hash.
        """
        if not voxels: return [0]*24
        # Sort to ensure order independence
        geo_str = str(sorted([(v['x'], v['y'], v['z']) for v in voxels]))
        h = hashlib.sha256(geo_str.encode()).digest()
        
        # Extract 12 bits
        seed_int = int.from_bytes(h[:2], 'big') & 0xFFF
        if seed_int == 0: seed_int = 137 # Prevent void collapse
        
        msg_bits = [(seed_int >> i) & 1 for i in range(11, -1, -1)]
        
        if CORE_AVAILABLE:
            return GOLAY_ENGINE.encode(msg_bits)
        return msg_bits + [0]*12

# --- 3. GEOMETRIC LUMINESCENCE MAPPER ---
class GeometricLuminescence:
    @staticmethod
    def process_light(nm: int):
        """
        Converts Wavelength -> Frequency -> Voxels -> Vector.
        """
        # A. Physics: Wavelength to Frequency (THz)
        # f = c / lambda
        freq_hz = C_SPEED / (nm * 1e-9)
        freq_thz = freq_hz / 1e12
        
        # B. Quantization: Frequency to Voxel Count
        n_voxels = int(round(freq_thz / VOXEL_SCALE_THZ))
        if n_voxels < 1: n_voxels = 1
        
        # C. Topology: Fold the Voxels
        voxels, dims = TopologyEngine.get_optimal_shape(n_voxels)
        
        # D. Vectorization
        vector = TopologyEngine.get_spatial_vector(voxels)
        
        # E. Metrics
        tax = Fraction(0)
        if CORE_AVAILABLE:
            tax = LEECH_ENGINE.calculate_symmetry_tax(vector)
        
        shape_type = "Linear (Prime Tension)"
        if dims[1] > 1 and dims[2] == 1: shape_type = f"Planar {dims[0]}x{dims[1]}"
        if dims[2] > 1: shape_type = f"Volumetric {dims[0]}x{dims[1]}x{dims[2]}"
        
        return {
            "nm": nm,
            "thz": round(freq_thz, 2),
            "voxels": n_voxels,
            "shape": shape_type,
            "vector": vector,
            "tax": tax
        }

# --- 4. UBP-LANG PARSER (Updated) ---
class UBPLangParserV2:
    def __init__(self):
        self.lattice = {}
        self.logs = []

    def execute(self, script: str):
        lines = script.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'): continue
            
            parts = line.split()
            cmd = parts[0].upper()
            
            if cmd == "DEFINE":
                # DEFINE [ID] [NM]
                uid, nm = parts[1], int(parts[2])
                data = GeometricLuminescence.process_light(nm)
                self.lattice[uid] = data
                self.logs.append(f"DEFINE {uid}: {data['thz']}THz -> {data['voxels']} Voxels [{data['shape']}] | Tax: {float(data['tax']):.4f}")
                
            elif cmd == "INTERACT":
                # INTERACT [A] [B] -> [OUT]
                id_a, id_b, _, id_out = parts[1], parts[2], parts[3], parts[4]
                if id_a in self.lattice and id_b in self.lattice:
                    v_a = self.lattice[id_a]['vector']
                    v_b = self.lattice[id_b]['vector']
                    
                    # XOR Interaction
                    raw = [(a ^ b) for a, b in zip(v_a, v_b)]
                    
                    # Snap
                    if CORE_AVAILABLE:
                        decoded, _, _ = GOLAY_ENGINE.decode(raw)
                        snapped = GOLAY_ENGINE.encode(decoded)
                        tax = LEECH_ENGINE.calculate_symmetry_tax(snapped)
                    else:
                        snapped = raw
                        tax = 0
                    
                    self.lattice[id_out] = {"vector": snapped, "tax": tax}
                    self.logs.append(f"INTERACT {id_a} + {id_b} -> {id_out} | Result Tax: {float(tax):.4f}")

            elif cmd == "MEASURE":
                uid = parts[1]
                if uid in self.lattice:
                    d = self.lattice[uid]
                    # Energy = Tax * NRCI * Y_inv
                    tax = d['tax']
                    nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
                    y_inv = CONSTANTS['Y_INV']
                    energy = tax * nrci * y_inv
                    self.logs.append(f"MEASURE {uid}: Stability={float(nrci):.4f}, Metabolic Cost={float(energy):.4f}")

    def get_report(self):
        return "\n".join(self.logs)

# --- MAIN ---
if __name__ == "__main__":
    print("--- UBP PHYSICS BRIDGE v2.0 (Geometric) ---")
    
    script = """
    # Lanthanide Geometry Test
    # Terbium (545nm) ~ 550 THz ~ 55 Voxels
    # Europium (611nm) ~ 490 THz ~ 49 Voxels
    DEFINE TERBIUM_GREEN 545
    DEFINE EUROPIUM_RED 611
    INTERACT TERBIUM_GREEN EUROPIUM_RED -> HYBRID_LIGHT
    MEASURE HYBRID_STATE
    """
    
    parser = UBPLangParserV2()
    parser.execute(script)
    print(parser.get_report())