"""
================================================================================
UBP INTEGRATION ADAPTER - v4.2.6 (FLOAT-FREE PATCHED)
================================================================================

Bridges UBP Core v4.2.6 to existing UBP system components.
Ensures all metrics remain as exact Fractions.

Version: 4.2.6 Integration Adapter
Author: Euan R A Craig, New Zealand
Date: 10 January 2026
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json
import hashlib
from fractions import Fraction  # <--- CRITICAL FIX

# Import UBP Core v4.2.6
try:
    from ubp_core_v4_2_6_COMBINED import (
        GOLAY_DECODER,
        LEECH_ENHANCED,
        PARTICLE_VALIDATOR,
        LeechPointScaled,
        UBPUltimateSubstrate,
    )
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Could not import UBP Core v4.2.6: {e}")
    CORE_AVAILABLE = False


# ==============================================================================
# SECTION 1: METRICS BRIDGE (FLOAT-FREE PATCH)
# ==============================================================================

class MetricsBridge:
    """Bridge to metrics.py constants and functions (Exact)."""
    
    def __init__(self):
        """Initialize metrics bridge."""
        constants = UBPUltimateSubstrate.get_constants(precision=50)
        # KEEP AS FRACTIONS - DO NOT CAST TO FLOAT
        self.Y_inv = constants['Y_inv']
        self.Y = constants['Y']
        self.pi = constants['pi']
        
        # Observer constants
        self.OBSERVER_FIXED_POINT = self.Y_inv
        self.OBSERVER_COST = Fraction(1, 1) / self.Y_inv
        
        # Coherence regimes (Comparison values must be Fractions)
        self.COHERENCE_REGIMES = {
            'high': (Fraction(8, 10), Fraction(1, 1)),   # 0.8 - 1.0
            'medium': (Fraction(5, 10), Fraction(8, 10)), # 0.5 - 0.8
            'low': (Fraction(0, 1), Fraction(5, 10)),     # 0.0 - 0.5
        }
    
    def get_nrci(self, point: LeechPointScaled) -> Fraction:
        """Get NRCI (Normalized Resonance Coherence Index) for a point."""
        health = point.get_ontological_health()
        return health['Global_NRCI']
    
    def get_coherence_regime(self, nrci: Fraction) -> str:
        """Determine coherence regime from NRCI."""
        for regime, (low, high) in self.COHERENCE_REGIMES.items():
            if low <= nrci <= high:
                return regime
        return 'unknown'
    
    def get_all_constants(self) -> Dict[str, str]:
        """Get all fundamental constants (Returned as Strings to preserve precision in JSON)."""
        return {
            'Y_inv': str(self.Y_inv),
            'Y': str(self.Y),
            'pi': str(self.pi),
            'observer_fixed_point': str(self.OBSERVER_FIXED_POINT),
            'observer_cost': str(self.OBSERVER_COST),
        }


# ==============================================================================
# SECTION 2: HEX DICTIONARY INTERFACE
# ==============================================================================

class HexDictionaryInterface:
    """Interface to HexDictionary for memory storage/recall."""
    
    def __init__(self):
        """Initialize HexDictionary interface."""
        self.memory = {}
        self.index = {}
    
    def encode_point(self, point: LeechPointScaled) -> str:
        """Encode Leech point to hex string for storage."""
        coords_str = ','.join(str(c) for c in point.coords)
        hash_val = hashlib.sha256(coords_str.encode()).hexdigest()
        return hash_val[:32]
    
    def decode_point(self, hex_str: str) -> Optional[LeechPointScaled]:
        """Decode hex string back to Leech point (if stored)."""
        if hex_str in self.memory:
            return self.memory[hex_str]
        return None
    
    def store_point(self, point: LeechPointScaled, metadata: Dict[str, Any] = None) -> str:
        """Store point in memory with optional metadata."""
        hex_id = self.encode_point(point)
        self.memory[hex_id] = {
            'point': point,
            'metadata': metadata or {},
            'timestamp': None,
        }
        return hex_id
    
    def retrieve_point(self, hex_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored point and metadata."""
        return self.memory.get(hex_id)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            'total_stored': len(self.memory),
            'memory_keys': list(self.memory.keys())[:10],
        }

# ==============================================================================
# SECTION 3: POINT SERIALIZATION
# ==============================================================================

class PointSerializer:
    """Serialize/deserialize Leech points for storage and transmission."""
    
    @staticmethod
    def to_dict(point: LeechPointScaled) -> Dict[str, Any]:
        """Convert Leech point to dictionary."""
        return {
            'coords': list(point.coords),
            'norm_sq_scaled': point.norm_sq_scaled,
            'norm_sq_actual': float(point.norm_sq_actual), # Float ok for display/JSON
            'ontological_health': point.get_ontological_health(),
            'physical_space': point.to_physical_space(),
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> LeechPointScaled:
        """Reconstruct Leech point from dictionary."""
        return LeechPointScaled(coords=tuple(data['coords']))
    
    @staticmethod
    def to_json(point: LeechPointScaled) -> str:
        """Convert Leech point to JSON string."""
        return json.dumps(PointSerializer.to_dict(point), default=str)
    
    @staticmethod
    def from_json(json_str: str) -> LeechPointScaled:
        """Reconstruct Leech point from JSON string."""
        data = json.loads(json_str)
        return PointSerializer.from_dict(data)


# ==============================================================================
# SECTION 4: GOLAY CODE INTERFACE
# ==============================================================================

class GolayInterface:
    """Interface to Golay code operations."""
    
    def __init__(self):
        """Initialize Golay interface."""
        self.decoder = GOLAY_DECODER
    
    def encode_message(self, message: List[int]) -> List[int]:
        """Encode 12-bit message to 24-bit Golay codeword."""
        return self.decoder.encode(message)
    
    def decode_received(self, received: List[int]) -> Tuple[List[int], bool, int]:
        """Decode 24-bit received word with error correction."""
        return self.decoder.decode(received)
    
    def get_codeword_count(self) -> int:
        """Get total number of Golay codewords."""
        return len(self.decoder.get_all_codewords())
    
    def snap_to_codeword(self, noisy: List[int]) -> Tuple[List[int], Dict[str, Any]]:
        """Snap drifting state to nearest codeword."""
        return self.decoder.snap_to_codeword(noisy)
    
    def get_shadow_metrics(self) -> Dict[str, Any]:
        """Get shadow processor metrics."""
        return self.decoder.get_shadow_metrics()


# ==============================================================================
# SECTION 5: LEECH LATTICE INTERFACE
# ==============================================================================

class LeechInterface:
    """Interface to Leech lattice operations."""
    
    def __init__(self):
        """Initialize Leech interface."""
        self.engine = LEECH_ENHANCED
    
    def calculate_symmetry_tax(self, point: List[int]) -> Fraction:
        """Calculate symmetry tax for a point."""
        return self.engine.calculate_symmetry_tax(point)
    
    def rank_by_stability(self, points: List[List[int]]) -> List[Tuple[List[int], Fraction]]:
        """Rank points by stability."""
        return self.engine.rank_by_stability(points)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get Leech lattice statistics."""
        return self.engine.get_statistics()
    
    def create_point(self, coords: List[int]) -> LeechPointScaled:
        """Create a Leech point."""
        if len(coords) != 24:
            raise ValueError("Point must have 24 coordinates")
        return LeechPointScaled(coords=tuple(coords))


# ==============================================================================
# SECTION 6: PARTICLE PHYSICS INTERFACE
# ==============================================================================

class ParticlePhysicsInterface:
    """Interface to particle physics predictions."""
    
    def __init__(self):
        """Initialize particle physics interface."""
        self.validator = PARTICLE_VALIDATOR
    
    def get_predictions(self) -> Dict[str, Any]:
        """Get all particle physics predictions."""
        return self.validator.get_ultimate_predictions()
    
    def get_accuracy_metrics(self) -> Dict[str, float]:
        """Get accuracy metrics for predictions."""
        predictions = self.get_predictions()
        return {
            'muon_error_percent': predictions['muon_electron']['error_percent'],
            'proton_error_percent': predictions['proton_electron']['error_percent'],
            'alpha_error_percent': predictions['alpha_inv']['error_percent'],
            'average_error_percent': (
                predictions['muon_electron']['error_percent'] +
                predictions['proton_electron']['error_percent'] +
                predictions['alpha_inv']['error_percent']
            ) / 3.0
        }


# ==============================================================================
# SECTION 7: MASTER INTEGRATION INTERFACE
# ==============================================================================

class UBPCoreIntegration:
    """Master integration interface for UBP Core v4.2.6."""
    
    def __init__(self):
        """Initialize all integration components."""
        self.metrics = MetricsBridge()
        self.hex_dict = HexDictionaryInterface()
        self.serializer = PointSerializer()
        self.golay = GolayInterface()
        self.leech = LeechInterface()
        self.particle_physics = ParticlePhysicsInterface()
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize and validate all components."""
        if not CORE_AVAILABLE:
            return {'status': 'ERROR', 'message': 'UBP Core v4.2.6 not available'}
        
        return {
            'status': 'OK',
            'version': '4.2.6',
            'components': {
                'metrics': 'ready',
                'hex_dictionary': 'ready',
                'serializer': 'ready',
                'golay': 'ready',
                'leech': 'ready',
                'particle_physics': 'ready',
            },
            'constants': self.metrics.get_all_constants(),
            'leech_stats': self.leech.get_statistics(),
            'particle_accuracy': self.particle_physics.get_accuracy_metrics(),
        }
    
    def process_point(self, coords: List[int]) -> Dict[str, Any]:
        """Process a Leech point through all systems."""
        try:
            point = self.leech.create_point(coords)
            
            return {
                'status': 'OK',
                'point': self.serializer.to_dict(point),
                'nrci': self.metrics.get_nrci(point),
                'coherence_regime': self.metrics.get_coherence_regime(self.metrics.get_nrci(point)),
                'symmetry_tax': self.leech.calculate_symmetry_tax(coords),
                'hex_id': self.hex_dict.store_point(point),
            }
        except Exception as e:
            return {'status': 'ERROR', 'message': str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status."""
        return {
            'version': '4.2.6',
            'core_available': CORE_AVAILABLE,
            'components': {
                'metrics': 'operational',
                'hex_dictionary': 'operational',
                'golay': f"{self.golay.get_codeword_count()} codewords",
                'leech': self.leech.get_statistics(),
                'particle_physics': self.particle_physics.get_accuracy_metrics(),
            },
            'memory': self.hex_dict.get_memory_stats(),
        }


# ==============================================================================
# SECTION 8: GLOBAL INSTANCE
# ==============================================================================

UBP_INTEGRATION = UBPCoreIntegration()

if __name__ == "__main__":
    print("UBP Integration Adapter Loaded (Float-Free).")
