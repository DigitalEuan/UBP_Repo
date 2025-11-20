"""
GPU-Accelerated UBP 3.6 Simulation System
==========================================

This is the main simulation system that integrates:
1. CPU: UBP 3.6 core (64-bit authority)
2. GPU: Taichi visualization (32-bit worker)
3. TGIC: Dodecahedral coherence geometry
4. CSC: Coherence Sampling Cycle loop

**Architecture:**
- CPU maintains all UBP state with full 64-bit precision
- GPU reads snapshots for visualization only
- No GPU arithmetic on UBP states (fidelity preservation)
- Real-time visualization at 60+ FPS target

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

import taichi as ti
from typing import Dict, List, Tuple, Any, Optional
import time
import random
import math

from coherence_substrate import CoherenceState, OperatorRegistry
from tgic import DodecahedralGraph, TGICNode, TGICSystem, TGICGeometry
from kernels import resonance_kernel, normalized_coherence
from geometric_error_correction import CoherenceRegime, analyze_coherence
from gpu_bridge import GPUBridge, TGICBaker
from gpu_renderer import TaichiGPURenderer


class GPUUBPSimulation:
    """
    Main GPU-accelerated UBP simulation system.
    
    Implements the Master-Worker pattern:
    - Master (CPU): All UBP computation in 64-bit
    - Worker (GPU): Visualization in 32-bit
    """
    
    def __init__(self, backend: str = 'cpu', enable_visualization: bool = True):
        """
        Initialize GPU UBP simulation.
        
        Args:
            backend: 'metal' for iMac, 'cpu' for sandbox/testing
            enable_visualization: Enable real-time visualization
        """
        self.backend = backend
        self.enable_visualization = enable_visualization
        
        # CPU: UBP 3.6 Core (64-bit authority)
        print("Initializing CPU UBP core...")
        self.tgic_system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
        self.graph = self.tgic_system.graph
        self.operator_registry = OperatorRegistry()
        
        # GPU: Taichi renderer (32-bit worker)
        if enable_visualization:
            print(f"Initializing GPU renderer (backend: {backend})...")
            self.renderer = TaichiGPURenderer(backend=backend)
            self.renderer.load_graph(self.graph)
        else:
            self.renderer = None
        
        # Bridge for CPU-GPU communication
        self.bridge = GPUBridge()
        
        # Simulation state
        self.csc_count = 0  # Coherence Sampling Cycle count
        self.time_elapsed = 0.0  # Simulation time
        self.running = False
        self.paused = False
        
        # Statistics
        self.nrci_history: List[float] = []
        self.regime_history: List[str] = []
        self.interaction_count = 0
        
        print("✅ GPU UBP Simulation initialized")
        print(f"   Nodes: {len(self.graph.nodes)}")
        print(f"   Edges: {len(self.graph.edges)}")
        print(f"   Visualization: {'Enabled' if enable_visualization else 'Disabled'}")
    
    def run_csc(self) -> Dict[str, Any]:
        """
        Run one Coherence Sampling Cycle (CSC).
        
        This is where the CPU does all the UBP computation:
        1. Select interacting nodes (TGIC rules)
        2. Calculate resonance (64-bit)
        3. Apply operators (64-bit)
        4. Update coherence states (64-bit)
        5. Run error correction
        6. Transfer to GPU (f32 for visualization only)
        
        Returns:
            Dictionary with CSC results
        """
        # Step 1: Select two random nodes to interact (TGIC constraint)
        node_ids = list(self.graph.nodes.keys())
        node_a_id = random.choice(node_ids)
        node_b_id = random.choice(list(self.graph.nodes[node_a_id].connections))
        
        node_a = self.graph.nodes[node_a_id]
        node_b = self.graph.nodes[node_b_id]
        
        # Step 2: Calculate resonance coupling (64-bit)
        coupled_state = node_a.coherence_coupling(node_b)
        
        # Step 3: Apply random operator (for demonstration)
        # Use operator overloading (CoherenceState has __add__, __mul__, etc.)
        op_symbol = random.choice(['+', '×'])
        
        if op_symbol == '+':
            new_state = coupled_state + node_b.coherence
        elif op_symbol == '×':
            new_state = coupled_state * node_b.coherence
        elif op_symbol == '⊗Y':
            new_state = coupled_state.refine_forward()
        else:
            new_state = coupled_state
        
        # Step 4: Update node coherence (CPU maintains 64-bit state)
        node_a.coherence = new_state
        self.interaction_count += 1
        
        # Step 5: Determine coherence regime (simple threshold-based)
        nrci = new_state.nrci
        if nrci >= 0.999997:
            regime = 'SuperCoherent'
        elif nrci >= 0.99:
            regime = 'Coherent'
        elif nrci >= 0.9:
            regime = 'SemiCoherent'
        elif nrci >= 0.5:
            regime = 'SubCoherent'
        elif nrci >= 0.1:
            regime = 'Transitional'
        else:
            regime = 'Decoherent'
        
        # Step 6: Track statistics
        self.nrci_history.append(nrci)
        self.regime_history.append(regime)
        
        # Step 7: Transfer to GPU (f32 for visualization)
        if self.renderer:
            _, nrci_f32, fidelity_ok = self.bridge.coherence_to_f32(new_state)
            self.renderer.update_nrci(node_a_id, nrci_f32)
        
        # Increment CSC count
        self.csc_count += 1
        self.time_elapsed += 1.0  # 1 time unit per CSC
        
        return {
            'csc': self.csc_count,
            'node_a': node_a_id,
            'node_b': node_b_id,
            'operator': op_symbol,
            'nrci': nrci,
            'regime': regime,
            'fidelity_ok': fidelity_ok if self.renderer else True
        }
    
    def run_batch(self, num_cycles: int) -> Dict[str, Any]:
        """
        Run multiple CSCs in batch (no visualization).
        
        Args:
            num_cycles: Number of CSCs to run
            
        Returns:
            Batch statistics
        """
        print(f"Running {num_cycles} CSCs...")
        start_time = time.time()
        
        for i in range(num_cycles):
            self.run_csc()
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i+1}/{num_cycles} CSCs")
        
        elapsed = time.time() - start_time
        csc_per_sec = num_cycles / elapsed
        
        # Calculate statistics
        mean_nrci = sum(self.nrci_history[-num_cycles:]) / num_cycles
        min_nrci = min(self.nrci_history[-num_cycles:])
        max_nrci = max(self.nrci_history[-num_cycles:])
        
        return {
            'num_cycles': num_cycles,
            'elapsed_time': elapsed,
            'csc_per_second': csc_per_sec,
            'mean_nrci': mean_nrci,
            'min_nrci': min_nrci,
            'max_nrci': max_nrci,
            'total_interactions': self.interaction_count
        }
    
    def run_interactive(self):
        """
        Run interactive simulation with visualization.
        
        Controls:
        - SPACE: Pause/Resume
        - S: Step one CSC
        - R: Reset simulation
        - Q/ESC: Quit
        - Arrow keys: Rotate camera
        """
        if not self.renderer:
            print("❌ Visualization not enabled")
            return
        
        gui = ti.GUI('GPU UBP 3.6 Simulation', res=self.renderer.window_size)
        
        print()
        print("=" * 70)
        print("Interactive GPU UBP Simulation")
        print("=" * 70)
        print()
        print("Controls:")
        print("  SPACE: Pause/Resume")
        print("  S: Step one CSC")
        print("  R: Reset simulation")
        print("  Left/Right: Rotate Y")
        print("  Up/Down: Rotate X")
        print("  +/-: Zoom")
        print("  E: Toggle edges")
        print("  N: Toggle nodes")
        print("  Q/ESC: Quit")
        print()
        
        self.running = True
        self.paused = False
        frame_count = 0
        last_csc_time = time.time()
        csc_interval = 0.1  # Run CSC every 0.1 seconds
        
        while self.running and gui.running:
            # Handle input
            if gui.get_event(ti.GUI.PRESS):
                if gui.event.key == ti.GUI.ESCAPE or gui.event.key == 'q':
                    self.running = False
                elif gui.event.key == ti.GUI.SPACE:
                    self.paused = not self.paused
                    print(f"{'⏸️  Paused' if self.paused else '▶️  Resumed'}")
                elif gui.event.key == 's':
                    result = self.run_csc()
                    print(f"CSC {result['csc']}: Node {result['node_a']} {result['operator']} Node {result['node_b']} → NRCI={result['nrci']:.6f} ({result['regime']})")
                elif gui.event.key == 'r':
                    self.reset()
                    print("🔄 Simulation reset")
                elif gui.event.key == ti.GUI.LEFT:
                    self.renderer.camera_angle_y -= 0.1
                elif gui.event.key == ti.GUI.RIGHT:
                    self.renderer.camera_angle_y += 0.1
                elif gui.event.key == ti.GUI.UP:
                    self.renderer.camera_angle_x -= 0.1
                elif gui.event.key == ti.GUI.DOWN:
                    self.renderer.camera_angle_x += 0.1
                elif gui.event.key == '=':
                    self.renderer.camera_distance *= 0.9
                elif gui.event.key == '-':
                    self.renderer.camera_distance *= 1.1
                elif gui.event.key == 'e':
                    self.renderer.show_edges = not self.renderer.show_edges
                elif gui.event.key == 'n':
                    self.renderer.show_nodes = not self.renderer.show_nodes
            
            # Run CSC if not paused
            current_time = time.time()
            if not self.paused and (current_time - last_csc_time) >= csc_interval:
                result = self.run_csc()
                last_csc_time = current_time
                
                if self.csc_count % 10 == 0:
                    print(f"CSC {result['csc']}: NRCI={result['nrci']:.6f} ({result['regime']})")
            
            # Auto-rotate
            if not self.paused:
                self.renderer.camera_angle_y += 0.005
            
            # Render frame
            self.renderer.render_frame(gui)
            
            # Update title with stats
            stats = self.renderer.get_nrci_stats()
            gui.text(f"CSC: {self.csc_count} | Paused: {self.paused}",
                     pos=(0.02, 0.94), color=0xFFFFFF, font_size=16)
            
            frame_count += 1
        
        print()
        print("=" * 70)
        print("Simulation Summary")
        print("=" * 70)
        print(f"Total CSCs: {self.csc_count}")
        print(f"Total interactions: {self.interaction_count}")
        print(f"Final NRCI: {self.nrci_history[-1]:.6f}" if self.nrci_history else "N/A")
        print("=" * 70)
    
    def reset(self):
        """Reset simulation to initial state."""
        self.tgic_system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
        self.graph = self.tgic_system.graph
        
        if self.renderer:
            self.renderer.load_graph(self.graph)
        
        self.csc_count = 0
        self.time_elapsed = 0.0
        self.interaction_count = 0
        self.nrci_history.clear()
        self.regime_history.clear()
    
    def export_data(self, filename: str):
        """
        Export simulation data to JSON.
        
        Args:
            filename: Output filename
        """
        import json
        
        data = {
            'metadata': {
                'backend': self.backend,
                'total_csc': self.csc_count,
                'total_interactions': self.interaction_count,
                'node_count': len(self.graph.nodes),
                'edge_count': len(self.graph.edges)
            },
            'nrci_history': self.nrci_history,
            'regime_history': self.regime_history,
            'bridge_stats': self.bridge.get_conversion_stats()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Data exported to {filename}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='GPU-Accelerated UBP 3.6 Simulation')
    parser.add_argument('--backend', choices=['cpu', 'metal', 'vulkan', 'opengl'], default='cpu',
                        help='Taichi backend (use metal for iMac)')
    parser.add_argument('--mode', choices=['interactive', 'batch'], default='interactive',
                        help='Simulation mode')
    parser.add_argument('--cycles', type=int, default=1000,
                        help='Number of CSCs for batch mode')
    parser.add_argument('--export', type=str, default=None,
                        help='Export data to JSON file')
    
    args = parser.parse_args()
    
    # Create simulation
    sim = GPUUBPSimulation(backend=args.backend, enable_visualization=(args.mode == 'interactive'))
    
    if args.mode == 'interactive':
        # Run interactive mode
        sim.run_interactive()
    else:
        # Run batch mode
        results = sim.run_batch(args.cycles)
        print()
        print("=" * 70)
        print("Batch Results")
        print("=" * 70)
        print(f"CSCs run: {results['num_cycles']}")
        print(f"Elapsed time: {results['elapsed_time']:.2f} seconds")
        print(f"CSC/second: {results['csc_per_second']:.2f}")
        print(f"Mean NRCI: {results['mean_nrci']:.6f}")
        print(f"Min NRCI: {results['min_nrci']:.6f}")
        print(f"Max NRCI: {results['max_nrci']:.6f}")
        print("=" * 70)
    
    # Export data if requested
    if args.export:
        sim.export_data(args.export)


if __name__ == '__main__':
    main()
