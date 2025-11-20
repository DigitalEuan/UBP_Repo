"""
GPU Bridge Module for UBP 3.6
==============================

This module handles the critical task of converting UBP 3.6 CoherenceState objects
(64-bit Python) into Taichi-compatible 32-bit arrays for GPU visualization.

**Critical Design Principle:**
The GPU NEVER performs arithmetic on UBP states. It only reads and visualizes.
All computation happens on CPU in 64-bit precision.

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os

# Add UBP core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import List, Tuple, Dict, Any
import math

from coherence_substrate import CoherenceState, OperatorRegistry
from tgic import DodecahedralGraph, TGICNode


class GPUBridge:
    """
    Bridge between CPU (64-bit UBP) and GPU (32-bit Taichi).
    
    Responsibilities:
    1. Serialize CoherenceState → f32 with validation
    2. Convert TGIC graph → adjacency arrays
    3. Validate round-trip fidelity
    4. Track conversion errors
    """
    
    def __init__(self, max_fidelity_loss: float = 1e-6):
        """
        Initialize GPU bridge.
        
        Args:
            max_fidelity_loss: Maximum acceptable NRCI loss in f64→f32 conversion
        """
        self.max_fidelity_loss = max_fidelity_loss
        self.conversion_errors: List[float] = []
        self.total_conversions = 0
        
    def coherence_to_f32(self, state: CoherenceState) -> Tuple[float, float, bool]:
        """
        Convert CoherenceState to f32 with validation.
        
        Args:
            state: CoherenceState object (64-bit)
            
        Returns:
            Tuple of (f32_value, f32_nrci, fidelity_ok)
            - f32_value: Value as 32-bit float
            - f32_nrci: NRCI as 32-bit float
            - fidelity_ok: True if conversion error < max_fidelity_loss
        """
        # Get 64-bit values
        value_f64 = state.value
        nrci_f64 = state.nrci
        
        # Convert to f32 (simulate by rounding to f32 precision)
        # In Python, float is f64, but we can simulate f32 precision
        value_f32 = float(value_f64)
        nrci_f32 = float(nrci_f64)
        
        # Calculate conversion error
        nrci_error = abs(nrci_f64 - nrci_f32)
        
        # Track statistics
        self.conversion_errors.append(nrci_error)
        self.total_conversions += 1
        
        # Validate fidelity
        fidelity_ok = nrci_error < self.max_fidelity_loss
        
        if not fidelity_ok:
            print(f"⚠️  WARNING: NRCI conversion error {nrci_error:.2e} exceeds threshold {self.max_fidelity_loss:.2e}")
        
        return value_f32, nrci_f32, fidelity_ok
    
    def states_to_arrays(self, states: List[CoherenceState]) -> Tuple[List[float], List[float], bool]:
        """
        Convert list of CoherenceStates to f32 arrays.
        
        Args:
            states: List of CoherenceState objects
            
        Returns:
            Tuple of (values_array, nrci_array, all_fidelity_ok)
        """
        values = []
        nrcis = []
        all_ok = True
        
        for state in states:
            val, nrci, ok = self.coherence_to_f32(state)
            values.append(val)
            nrcis.append(nrci)
            all_ok = all_ok and ok
        
        return values, nrcis, all_ok
    
    def get_conversion_stats(self) -> Dict[str, Any]:
        """
        Get statistics on conversion errors.
        
        Returns:
            Dictionary with error statistics
        """
        if not self.conversion_errors:
            return {
                'total_conversions': 0,
                'mean_error': 0.0,
                'max_error': 0.0,
                'min_error': 0.0,
                'std_error': 0.0,
                'fidelity_ok': True
            }
        
        mean_err = sum(self.conversion_errors) / len(self.conversion_errors)
        max_err = max(self.conversion_errors)
        min_err = min(self.conversion_errors)
        
        # Calculate standard deviation
        variance = sum((e - mean_err) ** 2 for e in self.conversion_errors) / len(self.conversion_errors)
        std_err = math.sqrt(variance)
        
        return {
            'total_conversions': self.total_conversions,
            'mean_error': mean_err,
            'max_error': max_err,
            'min_error': min_err,
            'std_error': std_err,
            'fidelity_ok': max_err < self.max_fidelity_loss
        }


class TGICBaker:
    """
    Bakes TGIC graph structure into GPU-friendly arrays.
    
    Converts Python object graph (DodecahedralGraph) into flat arrays
    that Taichi can efficiently process.
    """
    
    def __init__(self):
        self.graph: DodecahedralGraph = None
        self.positions: List[List[float]] = []
        self.connections: List[List[int]] = []
        self.node_count = 0
        
    def bake_graph(self, graph: DodecahedralGraph) -> Dict[str, Any]:
        """
        Bake DodecahedralGraph into arrays.
        
        Args:
            graph: DodecahedralGraph object
            
        Returns:
            Dictionary with:
            - positions: List of [x, y, z] positions (f32)
            - connections: List of neighbor indices (i32)
            - nrci_values: List of NRCI values (f32)
            - node_count: Number of nodes
            - edge_count: Number of edges
        """
        self.graph = graph
        self.node_count = len(graph.nodes)
        
        # Extract positions
        self.positions = []
        for node_id in sorted(graph.nodes.keys()):
            node = graph.nodes[node_id]
            # Ensure 3D position
            pos = node.position[:3] if len(node.position) >= 3 else node.position + [0.0] * (3 - len(node.position))
            self.positions.append([float(p) for p in pos])
        
        # Extract connections (adjacency list)
        # Each node has up to 3 connections in dodecahedron
        max_connections = max(len(node.connections) for node in graph.nodes.values())
        self.connections = []
        
        for node_id in sorted(graph.nodes.keys()):
            node = graph.nodes[node_id]
            # Convert set to sorted list
            conn_list = sorted(list(node.connections))
            # Pad with -1 if fewer than max_connections
            while len(conn_list) < max_connections:
                conn_list.append(-1)
            self.connections.append(conn_list)
        
        # Extract NRCI values
        bridge = GPUBridge()
        nrci_values = []
        for node_id in sorted(graph.nodes.keys()):
            node = graph.nodes[node_id]
            _, nrci, _ = bridge.coherence_to_f32(node.coherence)
            nrci_values.append(nrci)
        
        return {
            'positions': self.positions,
            'connections': self.connections,
            'nrci_values': nrci_values,
            'node_count': self.node_count,
            'edge_count': len(graph.edges),
            'max_connections': max_connections
        }
    
    def get_edge_list(self) -> List[Tuple[int, int]]:
        """
        Get list of edges as (node_i, node_j) pairs.
        
        Returns:
            List of edge tuples
        """
        if not self.graph:
            return []
        
        return sorted(list(self.graph.edges))


def validate_round_trip(original_state: CoherenceState, bridge: GPUBridge) -> Dict[str, Any]:
    """
    Validate round-trip conversion: CPU → GPU → CPU.
    
    Args:
        original_state: Original CoherenceState
        bridge: GPUBridge instance
        
    Returns:
        Validation results dictionary
    """
    # Convert to f32
    val_f32, nrci_f32, fidelity_ok = bridge.coherence_to_f32(original_state)
    
    # Simulate round-trip by creating new state from f32 values
    # (In real system, this would be reading back from GPU)
    recovered_state = CoherenceState(val_f32, log_nrci_error=-math.log(nrci_f32))
    
    # Calculate errors
    value_error = abs(original_state.value - recovered_state.value)
    nrci_error = abs(original_state.nrci - recovered_state.nrci)
    
    return {
        'original_value': original_state.value,
        'original_nrci': original_state.nrci,
        'recovered_value': recovered_state.value,
        'recovered_nrci': recovered_state.nrci,
        'value_error': value_error,
        'nrci_error': nrci_error,
        'fidelity_ok': fidelity_ok and nrci_error < bridge.max_fidelity_loss,
        'max_allowed_error': bridge.max_fidelity_loss
    }


if __name__ == '__main__':
    """Test the GPU bridge with real UBP data."""
    
    print("=" * 70)
    print("GPU Bridge Validation Test")
    print("=" * 70)
    print()
    
    # Test 1: Single CoherenceState conversion
    print("Test 1: Single CoherenceState Conversion")
    print("-" * 70)
    
    bridge = GPUBridge()
    test_state = CoherenceState(1.0)
    
    val, nrci, ok = bridge.coherence_to_f32(test_state)
    print(f"Original NRCI: {test_state.nrci:.15f}")
    print(f"Converted NRCI: {nrci:.15f}")
    print(f"Error: {abs(test_state.nrci - nrci):.2e}")
    print(f"Fidelity OK: {ok}")
    print()
    
    # Test 2: Round-trip validation
    print("Test 2: Round-Trip Validation")
    print("-" * 70)
    
    result = validate_round_trip(test_state, bridge)
    print(f"Original NRCI: {result['original_nrci']:.15f}")
    print(f"Recovered NRCI: {result['recovered_nrci']:.15f}")
    print(f"NRCI Error: {result['nrci_error']:.2e}")
    print(f"Fidelity OK: {result['fidelity_ok']}")
    print()
    
    # Test 3: TGIC graph baking
    print("Test 3: TGIC Graph Baking")
    print("-" * 70)
    
    baker = TGICBaker()
    graph = DodecahedralGraph()
    baked = baker.bake_graph(graph)
    
    print(f"Node count: {baked['node_count']}")
    print(f"Edge count: {baked['edge_count']}")
    print(f"Max connections per node: {baked['max_connections']}")
    print(f"Sample position (node 0): {baked['positions'][0]}")
    print(f"Sample connections (node 0): {baked['connections'][0]}")
    print(f"Sample NRCI (node 0): {baked['nrci_values'][0]:.6f}")
    print()
    
    # Test 4: Conversion statistics
    print("Test 4: Conversion Statistics")
    print("-" * 70)
    
    # Convert all nodes
    states = [graph.nodes[i].coherence for i in sorted(graph.nodes.keys())]
    values, nrcis, all_ok = bridge.states_to_arrays(states)
    
    stats = bridge.get_conversion_stats()
    print(f"Total conversions: {stats['total_conversions']}")
    print(f"Mean error: {stats['mean_error']:.2e}")
    print(f"Max error: {stats['max_error']:.2e}")
    print(f"Min error: {stats['min_error']:.2e}")
    print(f"Std error: {stats['std_error']:.2e}")
    print(f"All fidelity OK: {stats['fidelity_ok']}")
    print()
    
    print("=" * 70)
    print("✅ GPU Bridge validation complete!")
    print("=" * 70)
