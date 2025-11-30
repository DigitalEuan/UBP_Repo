"""
TGIC Geometry Graph Generators
Implements graph structures for all TGIC geometries

Author: UBP Development Team
Date: November 30, 2025
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import numpy as np
from utils.tgic import TGICNode, InteractionType


class CubicGraph:
    """8-node cubic graph structure."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._generate_cubic_graph()
    
    def get_interaction_type(self, node1: int, node2: int):
        """Get interaction type between two nodes."""
        if node1 in self.nodes and node2 in self.nodes[node1].interaction_types:
            return self.nodes[node1].interaction_types[node2]
        return None
    
    def compute_graph_properties(self):
        """Compute properties of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.edges)
        degrees = [len(node.connections) for node in self.nodes.values()]
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'avg_degree': np.mean(degrees) if degrees else 0,
            'avg_clustering': 0.0,
            'degree_distribution': degrees,
            'is_regular': len(set(degrees)) == 1 if degrees else True,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0
        }
    
    def _generate_cubic_graph(self):
        """Generate 8 vertices of a cube."""
        # Cube vertices: all combinations of (±1, ±1, ±1)
        positions = [
            np.array([x, y, z], dtype=np.float64) 
            for x in [-1, 1] 
            for y in [-1, 1] 
            for z in [-1, 1]
        ]
        
        # Create nodes
        for i, pos in enumerate(positions):
            self.nodes[i] = TGICNode(
                node_id=i,
                position=pos,
                coherence_level=0.5  # Initialize with some coherence
            )
        
        # Create edges (connect vertices that differ in exactly one coordinate)
        for i in range(8):
            for j in range(i+1, 8):
                pos_i = self.nodes[i].position
                pos_j = self.nodes[j].position
                diff = np.abs(pos_i - pos_j)
                # Edge exists if exactly one coordinate differs
                if np.sum(diff > 0.1) == 1:
                    self.edges.append((i, j))
                    self.nodes[i].connections.add(j)
                    self.nodes[j].connections.add(i)
                    self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                    self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED


class TetrahedralGraph:
    """4-node tetrahedral graph structure."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._generate_tetrahedral_graph()
    
    def get_interaction_type(self, node1: int, node2: int):
        """Get interaction type between two nodes."""
        if node1 in self.nodes and node2 in self.nodes[node1].interaction_types:
            return self.nodes[node1].interaction_types[node2]
        return None
    
    def compute_graph_properties(self):
        """Compute properties of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.edges)
        degrees = [len(node.connections) for node in self.nodes.values()]
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'avg_degree': np.mean(degrees) if degrees else 0,
            'avg_clustering': 0.0,
            'degree_distribution': degrees,
            'is_regular': len(set(degrees)) == 1 if degrees else True,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0
        }
    
    def _generate_tetrahedral_graph(self):
        """Generate 4 vertices of a regular tetrahedron."""
        # Regular tetrahedron vertices
        positions = [
            np.array([1, 1, 1]),
            np.array([1, -1, -1]),
            np.array([-1, 1, -1]),
            np.array([-1, -1, 1])
        ]
        
        # Normalize to unit distance from origin
        positions = [p / np.linalg.norm(p) for p in positions]
        
        # Create nodes
        for i, pos in enumerate(positions):
            self.nodes[i] = TGICNode(
                node_id=i,
                position=pos,
                coherence_level=0.6
            )
        
        # Create edges (complete graph - all vertices connected)
        for i in range(4):
            for j in range(i+1, 4):
                self.edges.append((i, j))
                self.nodes[i].connections.add(j)
                self.nodes[j].connections.add(i)
                self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED


class OctahedralGraph:
    """6-node octahedral graph structure."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._generate_octahedral_graph()
    
    def get_interaction_type(self, node1: int, node2: int):
        """Get interaction type between two nodes."""
        if node1 in self.nodes and node2 in self.nodes[node1].interaction_types:
            return self.nodes[node1].interaction_types[node2]
        return None
    
    def compute_graph_properties(self):
        """Compute properties of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.edges)
        degrees = [len(node.connections) for node in self.nodes.values()]
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'avg_degree': np.mean(degrees) if degrees else 0,
            'avg_clustering': 0.0,
            'degree_distribution': degrees,
            'is_regular': len(set(degrees)) == 1 if degrees else True,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0
        }
    
    def _generate_octahedral_graph(self):
        """Generate 6 vertices of a regular octahedron."""
        # Octahedron vertices: ±1 on each axis
        positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([-1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, -1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
            np.array([0.0, 0.0, -1.0])
        ]
        
        # Create nodes
        for i, pos in enumerate(positions):
            self.nodes[i] = TGICNode(
                node_id=i,
                position=pos,
                coherence_level=0.55
            )
        
        # Create edges (each vertex connects to 4 others - not opposite)
        for i in range(6):
            for j in range(i+1, 6):
                pos_i = self.nodes[i].position
                pos_j = self.nodes[j].position
                # Don't connect opposite vertices (dot product = -1)
                if np.dot(pos_i, pos_j) > -0.9:
                    self.edges.append((i, j))
                    self.nodes[i].connections.add(j)
                    self.nodes[j].connections.add(i)
                    self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                    self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED


class IcosahedralGraph:
    """12-node icosahedral graph structure."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._generate_icosahedral_graph()
    
    def get_interaction_type(self, node1: int, node2: int):
        """Get interaction type between two nodes."""
        if node1 in self.nodes and node2 in self.nodes[node1].interaction_types:
            return self.nodes[node1].interaction_types[node2]
        return None
    
    def compute_graph_properties(self):
        """Compute properties of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.edges)
        degrees = [len(node.connections) for node in self.nodes.values()]
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'avg_degree': np.mean(degrees) if degrees else 0,
            'avg_clustering': 0.0,
            'degree_distribution': degrees,
            'is_regular': len(set(degrees)) == 1 if degrees else True,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0
        }
    
    def _generate_icosahedral_graph(self):
        """Generate 12 vertices of a regular icosahedron."""
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # Icosahedron vertices using golden rectangles
        positions = [
            # Rectangle in xy plane
            np.array([0, 1, phi]),
            np.array([0, 1, -phi]),
            np.array([0, -1, phi]),
            np.array([0, -1, -phi]),
            # Rectangle in yz plane
            np.array([1, phi, 0]),
            np.array([1, -phi, 0]),
            np.array([-1, phi, 0]),
            np.array([-1, -phi, 0]),
            # Rectangle in zx plane
            np.array([phi, 0, 1]),
            np.array([phi, 0, -1]),
            np.array([-phi, 0, 1]),
            np.array([-phi, 0, -1])
        ]
        
        # Normalize
        positions = [p / np.linalg.norm(p) for p in positions]
        
        # Create nodes
        for i, pos in enumerate(positions):
            self.nodes[i] = TGICNode(
                node_id=i,
                position=pos,
                coherence_level=0.7
            )
        
        # Create edges (connect vertices within edge length distance)
        edge_length = 2.0 / phi  # Theoretical edge length of unit icosahedron
        tolerance = 0.2
        
        for i in range(12):
            for j in range(i+1, 12):
                dist = np.linalg.norm(self.nodes[i].position - self.nodes[j].position)
                if abs(dist - edge_length) < tolerance:
                    self.edges.append((i, j))
                    self.nodes[i].connections.add(j)
                    self.nodes[j].connections.add(i)
                    self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                    self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED


def create_geometry_graph(geometry_type: str):
    """
    Factory function to create appropriate graph for geometry type.
    
    Args:
        geometry_type: One of 'cubic', 'tetrahedral', 'octahedral', 'icosahedral', 'dodecahedral'
    
    Returns:
        Graph object with nodes and edges
    """
    if geometry_type == 'cubic':
        return CubicGraph()
    elif geometry_type == 'tetrahedral':
        return TetrahedralGraph()
    elif geometry_type == 'octahedral':
        return OctahedralGraph()
    elif geometry_type == 'icosahedral':
        return IcosahedralGraph()
    else:
        # Import dodecahedral from main module
        from utils.tgic import DodecahedralGraph
        return DodecahedralGraph()
