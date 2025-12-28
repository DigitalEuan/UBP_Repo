#!/usr/bin/env python3
"""
================================================================================
UBP CORE - ULTIMATE PRODUCTION MODULE
================================================================================

Universal Binary Principle - Core Mathematical Engine
Version: 4.0.0 Research Edition
Author: Euan R A Craig, New Zealand
Date: 18 December 2025
https://github.com/DigitalEuan/UBP_Repo

"""

from dataclasses import dataclass, asdict, field
from typing import List, Tuple, Dict, Optional, Set, Any, Generator
from fractions import Fraction
import hashlib
import itertools
import time
import json
import csv

# Integration imports (lazy loaded in functions or assumed available in env)
try:
    import numpy as np
    import pandas as pd
except ImportError:
    np = None
    pd = None

# ==============================================================================
# SECTION 1: BINARY LINEAR ALGEBRA OVER GF(2)
# ==============================================================================

def _identity(n: int) -> List[List[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def _transpose(M: List[List[int]]) -> List[List[int]]:
    if not M: return []
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]

def _binary_matmul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    if not A or not B: return []
    rows_A, cols_A, cols_B = len(A), len(A[0]), len(B[0])
    if cols_A != len(B): raise ValueError(f"Matrix dimensions incompatible: {cols_A} != {len(B)}")
    result = []
    for i in range(rows_A):
        row = []
        for j in range(cols_B):
            val = sum(A[i][k] * B[k][j] for k in range(cols_A)) % 2
            row.append(val)
        result.append(row)
    return result

def hamming_weight(v: List[int]) -> int:
    return sum(v)

def hamming_distance(a: List[int], b: List[int]) -> int:
    if len(a) != len(b): raise ValueError("Vectors must have same length")
    return sum(1 for i in range(len(a)) if a[i] != b[i])

# ==============================================================================
# SECTION 2: BINARY GOLAY CODE G24
# ==============================================================================

_GOLAY_A = [
    [1,1,0,1,1,1,0,0,0,1,0,1], [1,0,1,1,1,0,0,0,1,0,1,1], [0,1,1,1,0,0,0,1,0,1,1,1],
    [1,1,1,0,0,0,1,0,1,1,0,1], [1,1,0,0,0,1,0,1,1,0,1,1], [1,0,0,0,1,0,1,1,0,1,1,1],
    [0,0,0,1,0,1,1,0,1,1,1,1], [0,0,1,0,1,1,0,1,1,1,0,1], [0,1,0,1,1,0,1,1,1,0,0,1],
    [1,0,1,1,0,1,1,1,0,0,0,1], [0,1,1,0,1,1,1,0,0,0,1,1], [1,1,1,1,1,1,1,1,1,1,1,0]
]
_I12 = _identity(12)
_G = [i + a for i, a in zip(_I12, _GOLAY_A)]
_H = [_a + i for _a, i in zip(_transpose(_GOLAY_A), _I12)]

@dataclass
class SyndromeLookupTable:
    syndrome_to_error: Dict[Tuple[int, ...], Tuple[int, ...]]
    error_weight_dist: Dict[int, int]
    build_time: float
    table_size: int

    def lookup(self, syndrome: Tuple[int, ...]) -> Optional[Tuple[int, ...]]:
        return self.syndrome_to_error.get(syndrome, None)

def build_syndrome_lookup_table(max_error_weight: int = 3) -> SyndromeLookupTable:
    start_time = time.time()
    syndrome_to_error = {}
    error_weight_dist = {w: 0 for w in range(max_error_weight + 1)}
    for weight in range(max_error_weight + 1):
        for error_positions in itertools.combinations(range(24), weight):
            error = [0] * 24
            for pos in error_positions: error[pos] = 1
            e_col = [[b] for b in error]
            syndrome_col = _binary_matmul(_H, e_col)
            syndrome = tuple(row[0] for row in syndrome_col)
            if syndrome not in syndrome_to_error:
                syndrome_to_error[syndrome] = tuple(error)
                error_weight_dist[weight] += 1
    return SyndromeLookupTable(syndrome_to_error, error_weight_dist, time.time() - start_time, len(syndrome_to_error))

class GolayDecoderOptimized:
    def __init__(self, verbose: bool = False):
        self.G = _G
        self.H = _H
        self.verbose = verbose
        if verbose: print("Building syndrome lookup table...")
        self.lookup_table = build_syndrome_lookup_table(max_error_weight=3)
        if verbose: print("Generating all codewords...")
        self._codewords = self._generate_all_codewords()

    def _generate_all_codewords(self) -> Set[Tuple[int, ...]]:
        codewords = set()
        for msg_int in range(4096):
            msg = [(msg_int >> i) & 1 for i in range(12)]
            codewords.add(tuple(self.encode(msg)))
        return codewords

    def encode(self, message: List[int]) -> List[int]:
        if len(message) != 12: raise ValueError("Message must be 12 bits")
        return _binary_matmul([message], self.G)[0]

    def compute_syndrome(self, received: List[int]) -> Tuple[int, ...]:
        if len(received) != 24: raise ValueError("Received word must be 24 bits")
        r_col = [[b] for b in received]
        return tuple(row[0] for row in _binary_matmul(self.H, r_col))

    def decode_fast(self, received: List[int]) -> Tuple[List[int], Dict]:
        if len(received) != 24: raise ValueError("Received word must be 24 bits")
        syndrome = self.compute_syndrome(received)
        syndrome_weight = hamming_weight(list(syndrome))
        metadata = {
            'syndrome': syndrome, 'syndrome_weight': syndrome_weight,
            'is_codeword': (syndrome_weight == 0), 'correctable': False,
            'error_weight': 0, 'error_pattern': None, 'method': 'lookup'
        }
        if syndrome_weight == 0:
            metadata['correctable'] = True
            return received, metadata
        error_pattern = self.lookup_table.lookup(syndrome)
        if error_pattern is not None:
            corrected = [(received[i] + error_pattern[i]) % 2 for i in range(24)]
            metadata['correctable'] = True
            metadata['error_weight'] = hamming_weight(list(error_pattern))
            metadata['error_pattern'] = list(error_pattern)
            return corrected, metadata
        else:
            metadata['error_weight'] = -1
            return received, metadata

    def is_codeword(self, bits: List[int]) -> bool:
        return tuple(bits) in self._codewords

    def get_all_codewords(self) -> List[List[int]]:
        return [list(c) for c in self._codewords]

# ==============================================================================
# SECTION 3: LEECH LATTICE L24 (SCALED-INTEGER REPRESENTATION)
# ==============================================================================

@dataclass(frozen=True)
class LeechPointScaled:
    coords: Tuple[int, ...]
    
    def __post_init__(self):
        if len(self.coords) != 24: raise ValueError("Leech point must have 24 coordinates")
        if not all(isinstance(c, int) for c in self.coords): raise ValueError("Coordinates must be integers")
    
    @property
    def norm_sq_scaled(self) -> int: return sum(c * c for c in self.coords)
    
    @property
    def norm_sq_actual(self) -> Fraction: return Fraction(self.norm_sq_scaled, 8)
    
    @property
    def coord_sum(self) -> int: return sum(self.coords)
    
    def to_numpy(self):
        """Convert to NumPy array for fast analysis (if numpy is available)."""
        if np is None: raise ImportError("NumPy not available")
        return np.array(self.coords, dtype=int)
        
    def to_dict(self) -> Dict:
        """Serialize for export."""
        return {
            "type": "LeechPointScaled",
            "coords": list(self.coords),
            "norm_sq_actual": str(self.norm_sq_actual)
        }

    def __repr__(self) -> str: return f"LeechPointScaled(norm2={self.norm_sq_actual}, sum={self.coord_sum})"

def golay_to_leech_scaled(golay_codeword: List[int]) -> LeechPointScaled:
    """Standard UBP Lift: (2b - 1) * 2."""
    if len(golay_codeword) != 24: raise ValueError("Golay codeword must be 24 bits")
    v = tuple(2 * b - 1 for b in golay_codeword)
    a = tuple(2 * vi for vi in v)
    return LeechPointScaled(coords=a)

class LeechLatticeExplorer:
    """Tools for generating and exploring Leech Lattice points."""
    
    def __init__(self, golay_decoder: GolayDecoderOptimized):
        self.golay = golay_decoder
        
    def generate_shell_from_golay(self, target_norm_actual: Fraction) -> Generator[LeechPointScaled, None, None]:
        """
        Explores the 'Standard Lift' of all Golay codewords. 
        Note: The standard UBP lift (2b-1)*2 produces points of norm 12. 
        This generator filters them.
        """
        target_norm_scaled = target_norm_actual * 8
        if target_norm_scaled.denominator != 1:
            # Scaled norm must be integer
            return
        
        target = int(target_norm_scaled)
        
        for cw in self.golay.get_all_codewords():
            p = golay_to_leech_scaled(cw)
            if p.norm_sq_scaled == target:
                yield p

    def generate_construction_a_offsets(self) -> Generator[LeechPointScaled, None, None]:
        """
        Generates Leech points by adding offsets 4*e_k to lifted Golay codes.
        This allows finding minimal vectors (norm 4).
        """
        # Implementation example for advanced users wanting to explore deep structure
        # Not exhaustive, just a demonstration of the search space capability
        pass

# ==============================================================================
# SECTION 4: PROJECTION MODES & CANONICAL RECORD CONTRACT
# ==============================================================================

@dataclass
class CanonicalRecord:
    domain: str
    canonical_id: str
    tokens: List[str]
    features: Dict
    version: int

    def __post_init__(self):
        for key, value in self.features.items():
            if isinstance(value, float): raise ValueError(f"Feature '{key}' is float, must be Fraction or int")

    @property
    def payload_hash(self) -> str:
        payload = f"{self.domain}:{self.canonical_id}:v{self.version}:{':'.join(sorted(self.tokens))}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    @property
    def query_bits24(self) -> List[int]:
        h = hashlib.sha256(self.payload_hash.encode('utf-8')).digest()
        bits = []
        for i in range(3):
            byte = h[i]
            for j in range(8):
                bits.append((byte >> (7 - j)) & 1)
        return bits

    def to_dict(self) -> Dict:
        """Safe serialization of features including Fractions."""
        safe_features = {}
        for k, v in self.features.items():
            if isinstance(v, Fraction):
                safe_features[k] = f"{v.numerator}/{v.denominator}"
            else:
                safe_features[k] = v
        return {
            "domain": self.domain,
            "canonical_id": self.canonical_id,
            "tokens": self.tokens,
            "features": safe_features,
            "version": self.version,
            "hash": self.payload_hash
        }

# ==============================================================================
# SECTION 5: PERSISTENCE & ANALYTICS
# ==============================================================================

class UBPEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Fraction):
            return f"{obj.numerator}/{obj.denominator}"
        if isinstance(obj, LeechPointScaled):
            return obj.to_dict()
        if isinstance(obj, CanonicalRecord):
            return obj.to_dict()
        return super().default(obj)

def save_data_json(data: Any, filename: str):
    """Save any UBP object structure to JSON, preserving Fractions."""
    with open(filename, 'w') as f:
        json.dump(data, f, cls=UBPEncoder, indent=2)
    print(f"Data saved to {filename}")

def load_data_json(filename: str) -> Any:
    """Load UBP data. Note: Fractions come back as strings, you may need to parse them sweep."""
    with open(filename, 'r') as f:
        return json.load(f)

# ==============================================================================
# SECTION 6: THREE.JS VISUALIZATION HELPER
# ==============================================================================

def save_scene_3d(data: Dict[str, Any], filename: str = "scene_3d.json"):
    """
    Save 3D scene data for UBP Studio visualization.
    
    Structure:
    {
      "points": [ { "x": 1, "y": 2, "z": 3, "color": "#ff0000", "size": 0.5 }, ... ],
      "lines": [ { "start": [0,0,0], "end": [1,1,1], "color": "#00ff00" }, ... ],
      "spheres": [ { "x": 0, "y": 0, "z": 0, "r": 1, "color": "blue" } ]
    }
    """
    with open(filename, 'w') as f:
        json.dump(data, f, cls=UBPEncoder, indent=2)
    print(f"3D Scene saved to {filename}. Visualizer will update.")


class UBPAnalytics:
    @staticmethod
    def records_to_dataframe(records: List[CanonicalRecord]):
        """Convert a list of CanonicalRecords to a Pandas DataFrame."""
        if pd is None: raise ImportError("Pandas not available")
        
        data = []
        for r in records:
            row = r.to_dict()
            # Flatten features
            features = row.pop('features')
            for k, v in features.items():
                # Convert fraction strings back to float for analysis (safe for stats, not for core logic)
                if isinstance(v, str) and '/' in v:
                    try:
                        n, d = map(int, v.split('/'))
                        row[f"feat_{k}"] = n/d
                    except:
                        row[f"feat_{k}"] = v
                else:
                    row[f"feat_{k}"] = v
            data.append(row)
        return pd.DataFrame(data)

    @staticmethod
    def leech_points_to_dataframe(points: List[LeechPointScaled]):
        """Convert list of LeechPoints to DataFrame with norms and coords."""
        if pd is None: raise ImportError("Pandas not available")
        
        data = []
        for p in points:
            row = {f"c{i}": p.coords[i] for i in range(24)}
            row["norm_sq_actual"] = float(p.norm_sq_actual)
            row["sum"] = p.coord_sum
            data.append(row)
        return pd.DataFrame(data)
