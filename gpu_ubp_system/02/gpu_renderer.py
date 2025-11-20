"""
Taichi GPU Renderer for UBP 3.6
================================

This module implements the GPU visualization layer using Taichi.
It follows the Master-Worker pattern where CPU maintains 64-bit authority
and GPU provides 32-bit visualization.

**Key Design:**
- CPU: All UBP arithmetic (64-bit)
- GPU: Read-only visualization (32-bit)
- Taichi backend: Metal (iMac) or CPU (sandbox/testing)

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

import taichi as ti
from typing import Dict, List, Tuple, Any
import math

from coherence_substrate import CoherenceState
from tgic import DodecahedralGraph
from gpu_bridge import GPUBridge, TGICBaker


@ti.data_oriented
class TaichiGPURenderer:
    """
    GPU renderer using Taichi for UBP visualization.
    
    Manages Taichi fields, kernels, and rendering pipeline.
    """
    
    def __init__(self, backend: str = 'cpu', window_size: Tuple[int, int] = (1024, 768)):
        """
        Initialize Taichi GPU renderer.
        
        Args:
            backend: 'metal' for iMac, 'cpu' for sandbox/testing
            window_size: (width, height) for visualization window
        """
        self.backend = backend
        self.window_size = window_size
        
        # Initialize Taichi
        if backend == 'metal':
            ti.init(arch=ti.metal, device_memory_GB=1.0)
        elif backend == 'vulkan':
            ti.init(arch=ti.vulkan)
        elif backend == 'opengl':
            ti.init(arch=ti.opengl)
        else:
            ti.init(arch=ti.cpu)
        
        print(f"[TaichiGPU] Initialized with backend: {self.backend}")
        
        # Taichi fields (GPU arrays)
        self.node_count = 0
        self.max_connections = 0
        self.positions = None
        self.connections = None
        self.nrci_values = None
        self.colors = None
        
        # Bridge for CPU-GPU communication
        self.bridge = GPUBridge()
        self.baker = TGICBaker()
        
        # Visualization state
        self.camera_distance = 5.0
        self.camera_angle_x = 0.0
        self.camera_angle_y = 0.0
        self.show_edges = True
        self.show_nodes = True
        
    def initialize_fields(self, node_count: int, max_connections: int):
        """
        Initialize Taichi fields for given graph size.
        
        Args:
            node_count: Number of nodes in graph
            max_connections: Maximum connections per node
        """
        self.node_count = node_count
        self.max_connections = max_connections
        
        # Node positions (3D vectors)
        self.positions = ti.Vector.field(3, dtype=ti.f32, shape=node_count)
        
        # Node connections (adjacency list, -1 for no connection)
        self.connections = ti.field(dtype=ti.i32, shape=(node_count, max_connections))
        
        # NRCI values (read-only from CPU)
        self.nrci_values = ti.field(dtype=ti.f32, shape=node_count)
        
        # Colors (computed from NRCI)
        self.colors = ti.Vector.field(3, dtype=ti.f32, shape=node_count)
        
        print(f"[TaichiGPU] Fields initialized: {node_count} nodes, {max_connections} max connections")
    
    def load_graph(self, graph: DodecahedralGraph):
        """
        Load TGIC graph into GPU fields.
        
        Args:
            graph: DodecahedralGraph to visualize
        """
        # Bake graph into arrays
        baked = self.baker.bake_graph(graph)
        
        # Initialize fields if not done
        if self.positions is None:
            self.initialize_fields(baked['node_count'], baked['max_connections'])
        
        # Transfer data to GPU
        self.positions.from_numpy(self._to_numpy_array(baked['positions']))
        self.connections.from_numpy(self._to_numpy_array(baked['connections']))
        self.nrci_values.from_numpy(self._to_numpy_array(baked['nrci_values']))
        
        # Compute colors
        self.compute_colors()
        
        print(f"[TaichiGPU] Graph loaded: {baked['node_count']} nodes, {baked['edge_count']} edges")
    
    def _to_numpy_array(self, data: List) -> Any:
        """Convert Python list to numpy array (Taichi requires numpy)."""
        import numpy as np
        if isinstance(data[0], list):
            return np.array(data, dtype=np.float32)
        elif isinstance(data[0], float):
            return np.array(data, dtype=np.float32)
        else:
            return np.array(data, dtype=np.int32)
    
    @ti.kernel
    def compute_colors(self):
        """
        Compute node colors from NRCI values.
        
        Color mapping:
        - NRCI ≥ 0.999997: Green (SuperCoherent)
        - NRCI ≥ 0.99: Yellow (Coherent)
        - NRCI ≥ 0.9: Orange (SemiCoherent)
        - NRCI < 0.9: Red (SubCoherent/Decoherent)
        """
        for i in range(self.node_count):
            nrci = self.nrci_values[i]
            
            if nrci >= 0.999997:
                # SuperCoherent: Green
                self.colors[i] = ti.Vector([0.0, 1.0, 0.0])
            elif nrci >= 0.99:
                # Coherent: Yellow-Green
                t = (nrci - 0.99) / (0.999997 - 0.99)
                self.colors[i] = ti.Vector([1.0 - t, 1.0, 0.0])
            elif nrci >= 0.9:
                # SemiCoherent: Orange-Yellow
                t = (nrci - 0.9) / (0.99 - 0.9)
                self.colors[i] = ti.Vector([1.0, t, 0.0])
            else:
                # SubCoherent/Decoherent: Red
                self.colors[i] = ti.Vector([1.0, 0.0, 0.0])
    
    def update_nrci(self, node_id: int, new_nrci: float):
        """
        Update NRCI value for a single node.
        
        Args:
            node_id: Node index
            new_nrci: New NRCI value (f32)
        """
        self.nrci_values[node_id] = new_nrci
        self.compute_colors()
    
    def update_all_nrci(self, nrci_list: List[float]):
        """
        Update all NRCI values at once.
        
        Args:
            nrci_list: List of NRCI values (f32)
        """
        import numpy as np
        self.nrci_values.from_numpy(np.array(nrci_list, dtype=np.float32))
        self.compute_colors()
    
    def get_nrci_stats(self) -> Dict[str, float]:
        """
        Get statistics on current NRCI values.
        
        Returns:
            Dictionary with min, max, mean, std of NRCI
        """
        import numpy as np
        nrci_array = self.nrci_values.to_numpy()
        
        return {
            'min': float(np.min(nrci_array)),
            'max': float(np.max(nrci_array)),
            'mean': float(np.mean(nrci_array)),
            'std': float(np.std(nrci_array))
        }
    
    def render_frame(self, gui: ti.GUI):
        """
        Render a single frame to GUI.
        
        Args:
            gui: Taichi GUI instance
        """
        # Clear canvas
        gui.clear(0x112F41)
        
        # Render edges if enabled
        if self.show_edges:
            self._render_edges(gui)
        
        # Render nodes if enabled
        if self.show_nodes:
            self._render_nodes(gui)
        
        # Show stats
        stats = self.get_nrci_stats()
        gui.text(f"NRCI: min={stats['min']:.6f} max={stats['max']:.6f} mean={stats['mean']:.6f}",
                 pos=(0.02, 0.98), color=0xFFFFFF, font_size=16)
        
        gui.show()
    
    def _render_nodes(self, gui: ti.GUI):
        """Render nodes as circles."""
        import numpy as np
        
        # Get positions and colors
        pos_np = self.positions.to_numpy()
        col_np = self.colors.to_numpy()
        
        # Project 3D to 2D (simple orthographic projection)
        for i in range(self.node_count):
            x, y, z = pos_np[i]
            
            # Simple rotation
            cos_x = math.cos(self.camera_angle_x)
            sin_x = math.sin(self.camera_angle_x)
            cos_y = math.cos(self.camera_angle_y)
            sin_y = math.sin(self.camera_angle_y)
            
            # Rotate around Y axis
            x_rot = x * cos_y - z * sin_y
            z_rot = x * sin_y + z * cos_y
            
            # Rotate around X axis
            y_rot = y * cos_x - z_rot * sin_x
            z_final = y * sin_x + z_rot * cos_x
            
            # Project to screen (orthographic)
            screen_x = (x_rot / self.camera_distance + 1.0) / 2.0
            screen_y = (y_rot / self.camera_distance + 1.0) / 2.0
            
            # Draw circle
            color = int(col_np[i][0] * 255) * 65536 + int(col_np[i][1] * 255) * 256 + int(col_np[i][2] * 255)
            gui.circle((screen_x, screen_y), radius=10, color=color)
    
    def _render_edges(self, gui: ti.GUI):
        """Render edges as lines."""
        import numpy as np
        
        # Get positions and connections
        pos_np = self.positions.to_numpy()
        conn_np = self.connections.to_numpy()
        
        # Project and draw edges
        for i in range(self.node_count):
            for j in range(self.max_connections):
                neighbor = conn_np[i][j]
                if neighbor == -1:
                    break
                
                # Only draw each edge once (i < neighbor)
                if i >= neighbor:
                    continue
                
                # Get positions
                x1, y1, z1 = pos_np[i]
                x2, y2, z2 = pos_np[neighbor]
                
                # Rotate and project
                cos_x = math.cos(self.camera_angle_x)
                sin_x = math.sin(self.camera_angle_x)
                cos_y = math.cos(self.camera_angle_y)
                sin_y = math.sin(self.camera_angle_y)
                
                # Point 1
                x1_rot = x1 * cos_y - z1 * sin_y
                z1_rot = x1 * sin_y + z1 * cos_y
                y1_rot = y1 * cos_x - z1_rot * sin_x
                screen_x1 = (x1_rot / self.camera_distance + 1.0) / 2.0
                screen_y1 = (y1_rot / self.camera_distance + 1.0) / 2.0
                
                # Point 2
                x2_rot = x2 * cos_y - z2 * sin_y
                z2_rot = x2 * sin_y + z2 * cos_y
                y2_rot = y2 * cos_x - z2_rot * sin_x
                screen_x2 = (x2_rot / self.camera_distance + 1.0) / 2.0
                screen_y2 = (y2_rot / self.camera_distance + 1.0) / 2.0
                
                # Draw line
                gui.line((screen_x1, screen_y1), (screen_x2, screen_y2), color=0x444444, radius=1)


def run_interactive_demo():
    """Run interactive demo of GPU renderer."""
    print("=" * 70)
    print("Taichi GPU Renderer Demo")
    print("=" * 70)
    print()
    
    # Create renderer (use CPU backend in sandbox)
    renderer = TaichiGPURenderer(backend='cpu', window_size=(1024, 768))
    
    # Load TGIC graph
    print("Loading dodecahedral graph...")
    graph = DodecahedralGraph()
    renderer.load_graph(graph)
    
    # Create GUI
    gui = ti.GUI('UBP 3.6 GPU Visualization', res=renderer.window_size)
    
    print()
    print("Controls:")
    print("  Left/Right arrow: Rotate around Y axis")
    print("  Up/Down arrow: Rotate around X axis")
    print("  +/-: Zoom in/out")
    print("  E: Toggle edges")
    print("  N: Toggle nodes")
    print("  Q/ESC: Quit")
    print()
    
    # Main loop
    frame_count = 0
    while gui.running:
        # Handle input
        if gui.get_event(ti.GUI.PRESS):
            if gui.event.key == ti.GUI.ESCAPE or gui.event.key == 'q':
                break
            elif gui.event.key == ti.GUI.LEFT:
                renderer.camera_angle_y -= 0.1
            elif gui.event.key == ti.GUI.RIGHT:
                renderer.camera_angle_y += 0.1
            elif gui.event.key == ti.GUI.UP:
                renderer.camera_angle_x -= 0.1
            elif gui.event.key == ti.GUI.DOWN:
                renderer.camera_angle_x += 0.1
            elif gui.event.key == '=':  # + key
                renderer.camera_distance *= 0.9
            elif gui.event.key == '-':
                renderer.camera_distance *= 1.1
            elif gui.event.key == 'e':
                renderer.show_edges = not renderer.show_edges
            elif gui.event.key == 'n':
                renderer.show_nodes = not renderer.show_nodes
        
        # Auto-rotate
        renderer.camera_angle_y += 0.01
        
        # Render frame
        renderer.render_frame(gui)
        
        frame_count += 1
        if frame_count % 60 == 0:
            stats = renderer.get_nrci_stats()
            print(f"Frame {frame_count}: NRCI mean={stats['mean']:.6f}, std={stats['std']:.2e}")
    
    print()
    print("=" * 70)
    print("✅ Demo complete!")
    print("=" * 70)


if __name__ == '__main__':
    run_interactive_demo()
