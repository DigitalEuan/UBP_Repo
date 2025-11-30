"""
TGIC Geometry Registry - Cross-Geometry Validation Extension
Based on concept by Qwen AI

Defines geometry-specific triads and constraint logic for multiple
geometric structures to validate TGIC's geometric relativity.

Author: UBP Development Team (concept by Qwen AI)
Date: November 30, 2025
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from enum import Enum
from typing import Dict, Tuple, Callable, List
from dataclasses import dataclass
import numpy as np
import math


# Import from actual TGIC module
from utils.tgic import TGICGeometry, TGICConstraint


@dataclass
class GeometrySpec:
    """Specification for a TGIC geometry."""
    triad: Tuple[int, int, int]  # (axis, face, interaction)
    constraint_initializer: Callable
    preferred_interactions: List[str]
    coherence_threshold: float
    description: str


def _init_cubic_constraints(system):
    """Initialize constraints for cubic geometry (3, 6, 8)."""
    # 3 axes: (±1,0,0), (0,±1,0), (0,0,±1)
    # 6 faces: ±x, ±y, ±z planes
    # 8 corners: full cube
    if system.graph and len(system.graph.nodes) >= 8:
        # 3-axis: nodes 0,1,2 (orthogonal corners)
        system.add_constraint(
            "cubic_3_axes", "geometric",
            [0, 1, 2], system._enforce_three_axis_constraint
        )
        # 6-face: use 6 face-center proxies
        system.add_constraint(
            "cubic_6_faces", "topological",
            list(range(6)), system._enforce_six_face_constraint
        )
        # 8-interaction neighborhood
        system.add_constraint(
            "cubic_8_interactions", "connectivity",
            list(range(8)), system._enforce_octal_interaction_constraint
        )


def _init_tetrahedral_constraints(system):
    """Initialize constraints for tetrahedral geometry (3, 4, 6)."""
    # 3 edges per vertex, 4 vertices, 6 edges total
    if system.graph and len(system.graph.nodes) >= 4:
        system.add_constraint(
            "tetra_3_edges", "geometric",
            [0, 1, 2], system._enforce_three_axis_constraint
        )
        system.add_constraint(
            "tetra_4_vertices", "topological",
            [0, 1, 2, 3], system._enforce_four_vertex_closure
        )
        system.add_constraint(
            "tetra_6_edge_pairs", "connectivity",
            [0, 1, 2, 3], system._enforce_six_edge_pair_constraint
        )


def _init_octahedral_constraints(system):
    """Initialize constraints for octahedral geometry (4, 6, 8)."""
    # 4 neighbors/vertex, 6 vertices, 8 faces
    if system.graph and len(system.graph.nodes) >= 6:
        system.add_constraint(
            "octa_4_degree", "geometric",
            list(range(4)), system._enforce_four_degree_constraint
        )
        system.add_constraint(
            "octa_6_vertices", "topological",
            list(range(6)), system._enforce_six_vertex_symmetry
        )
        system.add_constraint(
            "octa_8_faces", "connectivity",
            list(range(6)), system._enforce_eight_face_proxy
        )


def _init_icosahedral_constraints(system):
    """Initialize constraints for icosahedral geometry (5, 12, 30)."""
    # 5 triangles/vertex, 12 vertices, 30 edges
    if system.graph and len(system.graph.nodes) >= 12:
        system.add_constraint(
            "icosa_5_fold", "geometric",
            [0, 1, 2, 3, 4], system._enforce_five_fold_constraint
        )
        system.add_constraint(
            "icosa_12_vertices", "topological",
            list(range(12)), system._enforce_twelve_vertex_closure
        )
        system.add_constraint(
            "icosa_30_edges", "connectivity",
            list(range(12)), system._enforce_edge_density_constraint
        )


def _init_dodecahedral_constraints(system):
    """Initialize constraints for dodecahedral geometry (3, 6, 9) - UBP default."""
    # Use existing implementation
    system._initialize_constraints()


def _init_leech_constraints(system):
    """Initialize constraints for Leech 24D geometry (3, 8, 24)."""
    if not system.leech_projection:
        return
    # 3 E8 blocks, 8-dim coherence units, 24-bit alignment
    system.add_constraint(
        "leech_3_blocks", "geometric",
        ["E8_1", "E8_2", "E8_3"],
        system._enforce_leech_block_orthogonality
    )


# Geometry Registry
GEOMETRY_REGISTRY: Dict[TGICGeometry, GeometrySpec] = {
    TGICGeometry.CUBIC: GeometrySpec(
        triad=(3, 6, 8),
        constraint_initializer=_init_cubic_constraints,
        preferred_interactions=["AXIS_ALIGNED", "FACE_DIAGONAL", "SPACE_DIAGONAL"],
        coherence_threshold=0.93,
        description="Orthogonal, minimal nonlinearity — ideal for base-logic layer"
    ),
    TGICGeometry.TETRAHEDRAL: GeometrySpec(
        triad=(3, 4, 6),
        constraint_initializer=_init_tetrahedral_constraints,
        preferred_interactions=["EDGE_CONNECTED", "VERTEX_SHARED"],
        coherence_threshold=0.90,
        description="Simplex symmetry — minimal proof base cases"
    ),
    TGICGeometry.OCTAHEDRAL: GeometrySpec(
        triad=(4, 6, 8),
        constraint_initializer=_init_octahedral_constraints,
        preferred_interactions=["AXIS_ALIGNED", "VERTEX_SHARED", "HARMONIC"],
        coherence_threshold=0.94,
        description="Dual to cube — spin-1 analogues"
    ),
    TGICGeometry.ICOSAHEDRAL: GeometrySpec(
        triad=(5, 12, 30),
        constraint_initializer=_init_icosahedral_constraints,
        preferred_interactions=["HARMONIC", "NONLOCAL", "QUANTUM"],
        coherence_threshold=0.97,
        description="Pentavalent, high symmetry — candidate for consciousness layer"
    ),
    TGICGeometry.DODECAHEDRAL: GeometrySpec(
        triad=(3, 6, 9),
        constraint_initializer=_init_dodecahedral_constraints,
        preferred_interactions=["EDGE_CONNECTED", "HARMONIC", "TEMPORAL"],
        coherence_threshold=0.95,
        description="UBP default — balanced 3/6/9 resonance"
    ),
    TGICGeometry.LEECH_24D: GeometrySpec(
        triad=(3, 8, 24),
        constraint_initializer=_init_leech_constraints,
        preferred_interactions=["QUANTUM", "NONLOCAL", "HARMONIC"],
        coherence_threshold=0.98,
        description="24D optimal packing — cosmological & deep-coherence layer"
    )
}


def get_geometry_spec(geometry: TGICGeometry) -> GeometrySpec:
    """Get specification for a geometry."""
    return GEOMETRY_REGISTRY.get(geometry)


def list_geometries() -> List[str]:
    """List all available geometries."""
    return [geo.value for geo in GEOMETRY_REGISTRY.keys()]
