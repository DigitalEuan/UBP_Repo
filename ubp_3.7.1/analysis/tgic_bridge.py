"""
Universal Binary Principle (UBP) Framework v3.7.1 - TGIC-OffBit Bridge Module
Author: Euan Craig, New Zealand
Date: 01 December 2025

Bridges the UBP OffBit state with the TGIC geometric constraint system,
enabling geometric analysis of the fundamental information unit.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from core.state import OffBit, MutableBitfield, UBPState
from utils.tgic import TGICSystem, TGICGeometry, create_tgic_system

class OffBitTGICBridge:
    """
    Bridges UBP OffBits with TGIC geometric constraints.
    
    Maps active OffBits to the geometric structure defined by TGIC.
    """
    
    def __init__(self, geometry: TGICGeometry = TGICGeometry.DODECAHEDRAL):
        self.tgic = create_tgic_system(geometry)
        self.offbit_states: Dict[int, Dict[str, Any]] = {}
        
    def map_offbits_to_graph(self, bitfield: MutableBitfield):
        """
        Map active OffBits to TGIC graph nodes.
        
        Each OffBit becomes a potential node in the geometric structure.
        """
        self.offbit_states = {}
        active_offbits = bitfield.get_active_offbits()
        
        # Create virtual nodes for each active OffBit
        for idx, offbit in active_offbits:
            # Convert OffBit to Leech lattice point
            leech_point = offbit.to_leech_point()
            
            # Map to 3D via projection
            if self.tgic.geometry == TGICGeometry.LEECH_24D:
                # Use Leech lattice projection (simplified for now)
                # The full projection is handled by the TGICSystem's internal LeechLatticeProjection
                proj_3d = self.tgic.leech_projection.project_to_3d(leech_point)
            else:
                # For other geometries, use simplified mapping
                proj_3d = self._map_offbit_to_3d(offbit)
            
            # Store mapping
            self.offbit_states[idx] = {
                'offbit': offbit,
                'leech_point': leech_point,
                'position_3d': proj_3d,
                'graph_node_id': None  # Will be mapped to graph node
            }
    
    def _map_offbit_to_3d(self, offbit: OffBit) -> np.ndarray:
        """
        Map OffBit to 3D position using bit patterns.
        
        Uses the 24 bits to generate 3 coordinates:
        - Bits 0-7 → x coordinate
        - Bits 8-15 → y coordinate  
        - Bits 16-23 → z coordinate
        
        This creates a natural mapping to TGIC's 3-axis structure.
        """
        bits = offbit.bits
        
        # Convert each 8-bit group to coordinate [-1, 1]
        x_bits = bits[0:8]
        y_bits = bits[8:16]
        z_bits = bits[16:24]
        
        def bits_to_coord(bit_group):
            # Convert 8 bits to value in [-1, 1]
            # Note: bits are LSB first in OffBit.bits, so we reverse for standard int conversion
            value = sum(b * (2**i) for i, b in enumerate(bit_group))
            normalized = (value / 255.0) * 2 - 1  # Map to [-1, 1]
            return normalized
        
        return np.array([
            bits_to_coord(x_bits),
            bits_to_coord(y_bits),
            bits_to_coord(z_bits)
        ])
    
    def compute_offbit_coherence(self, bitfield: MutableBitfield) -> float:
        """
        Compute geometric coherence of OffBits using TGIC constraints.
        
        Measures how well OffBits align with geometric structure.
        """
        if not self.offbit_states:
            self.map_offbits_to_graph(bitfield)
        
        # For each OffBit, check its geometric constraints
        coherence_scores = []
        
        for idx, state in self.offbit_states.items():
            pos = state['position_3d']
            offbit = state['offbit']
            
            # Check 3-axis alignment (TGIC constraint)
            axis_alignment = self._check_axis_alignment(pos)
            
            # Check Golay validity
            golay_valid = float(offbit.is_golay_codeword)
            
            # Combine scores
            # The weights (0.7, 0.3) are a heuristic from the DeepSeek suggestion
            coherence = 0.7 * axis_alignment + 0.3 * golay_valid
            coherence_scores.append(coherence)
        
        return np.mean(coherence_scores) if coherence_scores else 0.0
    
    def _check_axis_alignment(self, position: np.ndarray) -> float:
        """
        Check how well a position aligns with TGIC axes.
        """
        # Measure alignment with cardinal axes
        axis_alignment = max(np.abs(position))  # Closer to axes = higher value
        return min(1.0, axis_alignment)

class RealmSpecificTGIC:
    """
    TGIC system adapted for different UBP realms.
    
    Uses the OffBitTGICBridge to analyze UBPState based on realm-specific geometry.
    """
    
    # Map UBP realms to TGIC geometries (based on DeepSeek suggestion)
    REALM_GEOMETRY_MAP = {
        'quantum': TGICGeometry.LEECH_24D,
        'classical': TGICGeometry.CUBIC,
        'biological': TGICGeometry.DODECAHEDRAL,
        'consciousness': TGICGeometry.ICOSAHEDRAL,
        'temporal': TGICGeometry.OCTAHEDRAL,
        'spiritual': TGICGeometry.TETRAHEDRAL,
    }
    
    def __init__(self, realm: str = "quantum"):
        self.realm = realm
        geometry = self.REALM_GEOMETRY_MAP.get(realm, TGICGeometry.DODECAHEDRAL)
        self.tgic = create_tgic_system(geometry)
        self.offbit_bridge = OffBitTGICBridge(geometry)
        
    def analyze_ubp_state(self, ubp_state: UBPState) -> Dict[str, Any]:
        """
        Analyze UBP state through TGIC geometric constraints.
        """
        results = {
            'realm': self.realm,
            'geometry': self.tgic.geometry.value,
            'bitfield_coherence': ubp_state.get_coherence(),
            'tgic_constraints': {},
            'offbit_patterns': {},
            'geometric_alignment': 0.0
        }
        
        # 1. Evaluate TGIC constraints
        violations = self.tgic.evaluate_all_constraints()
        results['tgic_constraints']['violations'] = violations
        results['tgic_constraints']['total_violation'] = self.tgic.compute_total_violation()
        
        # 2. Analyze OffBit patterns geometrically
        self.offbit_bridge.map_offbits_to_graph(ubp_state.bitfield)
        geometric_coherence = self.offbit_bridge.compute_offbit_coherence(ubp_state.bitfield)
        results['geometric_alignment'] = geometric_coherence
        
        # 3. Check for Golay code patterns in OffBits
        active_offbits = ubp_state.bitfield.get_active_offbits()
        golay_stats = self._analyze_golay_patterns(active_offbits)
        results['offbit_patterns']['golay'] = golay_stats
        
        # 4. Compute combined alignment score
        # Weight geometric coherence with TGIC constraint satisfaction
        tgic_weight = 1.0 - results['tgic_constraints']['total_violation']
        combined_alignment = 0.6 * geometric_coherence + 0.4 * tgic_weight
        results['combined_alignment'] = combined_alignment
        
        return results
    
    def _analyze_golay_patterns(self, active_offbits: List[Tuple[int, OffBit]]) -> Dict[str, Any]:
        """
        Analyze Golay code patterns in active OffBits.
        """
        if not active_offbits:
            return {'golay_codeword_count': 0, 'total_offbits': 0, 'golay_ratio': 0.0}
        
        golay_count = sum(1 for _, offbit in active_offbits if offbit.is_golay_codeword)
        total_offbits = len(active_offbits)
        
        return {
            'golay_codeword_count': golay_count,
            'total_offbits': total_offbits,
            'golay_ratio': golay_count / total_offbits
        }

# Add to analysis/__init__.py for easy import
# from .tgic_bridge import OffBitTGICBridge, RealmSpecificTGIC
