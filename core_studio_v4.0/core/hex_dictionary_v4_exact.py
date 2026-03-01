"""
UBP HexDictionary v4.8 (Spatial-Deterministic Edition)
=====================================================
Identity is derived from TOPOLOGY. 
The 'math' field is treated as a 3D Voxel Structure.
The Vector is a measurement of that structure's Volume and Compactness.

STANDARDS:
1. Domain: Bits 0-2 (Prefix)
2. Volume: Bits 3-7 (Voxel Count, Gray Coded)
3. Compactness: Bits 8-11 (Surface Area Proxy, Gray Coded)
4. Parity: Bits 12-23 (Golay [24,12,8])

Author: Euan R A Craig & UBP Research Cortex v4.2.7
Date: 28 Feb 2026
"""

import json
import os
import re
import math
from typing import Dict, List, Optional, Any, Tuple
from fractions import Fraction

# --- UBP CORE INTEGRATION ---
try:
    from ubp_core_v5_3_merged import GOLAY_ENGINE, BinaryLinearAlgebra
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

class HexDictionaryV4Exact:
    DOMAINS = {
        "QUANTITY": 0, "SUBSTANCE": 1, "MECHANISM": 2, "ALGORITHM": 3,
        "ORGANISM": 4, "IMPERATIVE": 5, "ENTROPY": 6, "MEANING": 7
    }

    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.id_map: Dict[str, str] = {}
        self.vector_cache: Dict[str, List[int]] = {}

    def _int_to_gray(self, n: int, bits: int) -> List[int]:
        """Gray code ensures that similar volumes have similar bit-patterns."""
        n = int(n) % (2**bits)
        gray = n ^ (n >> 1)
        return [(gray >> i) & 1 for i in range(bits - 1, -1, -1)]

    def _get_domain_for_id(self, ubp_id: str) -> int:
        uid = ubp_id.upper()
        if uid.startswith(("NUM_", "CONST_", "MATH_", "GEO_")): return 0
        if uid.startswith(("ELEM_", "CHEM_", "MAT_", "CRYSTAL_")): return 1
        if uid.startswith(("PHYS_", "MECH_", "PARTICLE_", "FORCE_")): return 2
        if uid.startswith(("PY_", "CODE_", "ALGO_", "DS_", "BITOP_")): return 3
        if uid.startswith(("BIO_", "CELL_", "PSYCH_", "MOLECULE_")): return 4
        if uid.startswith(("LAW_", "ACTION_", "STATE_", "IMPERATIVE_")): return 5
        if uid.startswith(("PATTERN_", "TRANSFORM_", "NOISE_")): return 6
        return 7

    def _measure_topology(self, math_dna: str) -> Tuple[int, int]:
        """
        SYMBOLIC HASHING:
        Turns the math string into a Voxel Count (Volume) 
        and a 'Complexity' score (Compactness).
        """
        if not math_dna or math_dna in ["atomic", "absolute_primitive"]:
            return 1, 0
            
        # 1. Volume (V): Total magnitude of all dimensions
        # Example: "Z=1|Valence=1" -> Volume 2
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", math_dna)
        volume = sum(abs(float(n)) for n in numbers)
        
        # 2. Compactness (C): Ratio of properties to volume
        # High property count per volume = 'Jagged' (High Surface Area)
        # Low property count per volume = 'Smooth' (Low Surface Area)
        prop_count = math_dna.count('|') + 1
        compactness = int((prop_count * 100) / (volume if volume > 0 else 1))
        
        return int(volume), int(compactness)

    def mint_rational_vector(self, ubp_id: str, math_dna: str) -> List[int]:
        """
        PROJECTS a vector from the SPATIAL properties of the math.
        """
        # 1. Domain Bits (3 bits)
        dom_val = self._get_domain_for_id(ubp_id)
        dom_bits = [(dom_val >> i) & 1 for i in range(2, -1, -1)]

        # 2. Measure Topology (Volume and Compactness)
        volume, compactness = self._measure_topology(math_dna)
        
        # Parameter A: Volume (5 bits, 0-31)
        p1_bits = self._int_to_gray(volume, 5)
        
        # Parameter B: Compactness (4 bits, 0-15)
        p2_bits = self._int_to_gray(compactness, 4)

        # 3. Construct 12-bit Noumenal Seed [Domain][Volume][Compactness]
        message = dom_bits + p1_bits + p2_bits
        
        # 4. Encode to 24-bit Phenomenal Codeword
        if CORE_AVAILABLE:
            return GOLAY_ENGINE.encode(message)
        return message + [0]*12

    def load_memory(self, filepath: str = "ubp_system_kb.json"):
        if not os.path.exists(filepath): return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            entries = data.get('objects', data)
            for fp, entry in entries.items():
                uid = entry.get('ubp_id')
                if uid:
                    self.registry[fp] = entry
                    self.id_map[uid] = fp
                    vec = entry.get('atlas', {}).get('vector')
                    if vec: self.vector_cache[uid] = vec
            print(f"[HEX_DB] Loaded {len(self.id_map)} spatial-deterministic entries.")
        except Exception as e:
            print(f"[HEX_DB] Load failed: {e}")

    def find_by_id(self, ubp_id: str) -> Optional[Dict[str, Any]]:
        fp = self.id_map.get(ubp_id)
        return self.registry.get(fp) if fp else None

    def get_vector(self, ubp_id: str) -> Optional[List[int]]:
        return self.vector_cache.get(ubp_id)

# Global Instance
HEX_DB_EXACT = HexDictionaryV4Exact()