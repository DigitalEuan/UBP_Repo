#!/usr/bin/env python3.11
"""
π-Helix GeoBit STL Generator
Generate 3D printable STL file for UBP sanitation study

Specifications:
- Radius: 0.15 m (150 mm)
- Height: 0.50 m (500 mm)
- Pitch: π/10 rad
- Turns: 5 full rotations
- Wall thickness: 3 mm
- Material: HDPE (3D printable)

Author: Euan Craig, New Zealand
Date: November 2025
Framework: UBP v3.4
"""

import numpy as np
from math import pi, cos, sin
from stl import mesh

# UBP Constants
Y = pi / (pi**2 + 2)
Y_INV = pi + 2 / pi

# Helix Parameters (from paper specification)
RADIUS = 150.0  # mm (0.15 m)
HEIGHT = 500.0  # mm (0.50 m)
PITCH = pi / 10  # rad
TURNS = 5
WALL_THICKNESS = 3.0  # mm
TUBE_RADIUS = 8.0  # mm (radius of helix tube cross-section)

# Resolution parameters
THETA_STEPS = 200  # Points per turn
CIRCLE_STEPS = 16  # Points around tube cross-section

def generate_helix_path(radius, height, turns, steps_per_turn):
    """
    Generate the centerline path of the helix.
    
    Returns:
    --------
    points : ndarray (N, 3)
        Array of (x, y, z) coordinates along helix centerline
    """
    total_steps = steps_per_turn * turns
    theta = np.linspace(0, 2 * pi * turns, total_steps)
    
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.linspace(0, height, total_steps)
    
    return np.column_stack([x, y, z])

def generate_tube_mesh(centerline, tube_radius, circle_steps):
    """
    Generate a tube mesh following the centerline path.
    
    Parameters:
    -----------
    centerline : ndarray (N, 3)
        Centerline points
    tube_radius : float
        Radius of tube cross-section
    circle_steps : int
        Number of points around tube circumference
    
    Returns:
    --------
    vertices : ndarray
        Vertex coordinates
    faces : ndarray
        Triangle face indices
    """
    n_points = len(centerline)
    
    # Generate circle points around tube
    angles = np.linspace(0, 2 * pi, circle_steps, endpoint=False)
    circle = np.column_stack([
        tube_radius * np.cos(angles),
        tube_radius * np.sin(angles),
        np.zeros(circle_steps)
    ])
    
    # Calculate tangent vectors along centerline
    tangents = np.zeros_like(centerline)
    tangents[:-1] = centerline[1:] - centerline[:-1]
    tangents[-1] = tangents[-2]  # Duplicate last tangent
    
    # Normalize tangents
    tangent_norms = np.linalg.norm(tangents, axis=1, keepdims=True)
    tangents = tangents / (tangent_norms + 1e-10)
    
    # Generate vertices by sweeping circle along centerline
    vertices = []
    for i, (center, tangent) in enumerate(zip(centerline, tangents)):
        # Create rotation matrix to align circle with tangent
        # Use Rodrigues' rotation formula
        z_axis = np.array([0, 0, 1])
        
        # Rotation axis
        if np.allclose(tangent, z_axis):
            rot_axis = np.array([1, 0, 0])
            angle = 0
        elif np.allclose(tangent, -z_axis):
            rot_axis = np.array([1, 0, 0])
            angle = pi
        else:
            rot_axis = np.cross(z_axis, tangent)
            rot_axis = rot_axis / np.linalg.norm(rot_axis)
            angle = np.arccos(np.dot(z_axis, tangent))
        
        # Rodrigues rotation matrix
        K = np.array([
            [0, -rot_axis[2], rot_axis[1]],
            [rot_axis[2], 0, -rot_axis[0]],
            [-rot_axis[1], rot_axis[0], 0]
        ])
        
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        
        # Rotate and translate circle
        rotated_circle = (R @ circle.T).T + center
        vertices.extend(rotated_circle)
    
    vertices = np.array(vertices)
    
    # Generate faces (triangles)
    faces = []
    for i in range(n_points - 1):
        for j in range(circle_steps):
            # Current ring
            v1 = i * circle_steps + j
            v2 = i * circle_steps + (j + 1) % circle_steps
            
            # Next ring
            v3 = (i + 1) * circle_steps + j
            v4 = (i + 1) * circle_steps + (j + 1) % circle_steps
            
            # Two triangles per quad
            faces.append([v1, v2, v4])
            faces.append([v1, v4, v3])
    
    faces = np.array(faces)
    
    return vertices, faces

def add_base_plate(vertices, faces, radius, thickness):
    """
    Add a circular base plate at z=0.
    
    Returns:
    --------
    vertices : ndarray
        Updated vertices including base
    faces : ndarray
        Updated faces including base
    """
    # Generate base circle
    n_base_points = 32
    angles = np.linspace(0, 2 * pi, n_base_points, endpoint=False)
    
    base_outer = np.column_stack([
        radius * np.cos(angles),
        radius * np.sin(angles),
        np.zeros(n_base_points)
    ])
    
    base_inner = np.column_stack([
        (radius - 20) * np.cos(angles),
        (radius - 20) * np.sin(angles),
        np.zeros(n_base_points)
    ])
    
    # Center point
    center = np.array([[0, 0, 0]])
    
    # Add vertices
    base_offset = len(vertices)
    vertices = np.vstack([vertices, base_outer, base_inner, center])
    
    # Add faces
    base_faces = []
    center_idx = base_offset + 2 * n_base_points
    
    for i in range(n_base_points):
        # Outer ring triangles
        v1 = base_offset + i
        v2 = base_offset + (i + 1) % n_base_points
        base_faces.append([v1, v2, center_idx])
        
        # Inner ring triangles
        v3 = base_offset + n_base_points + i
        v4 = base_offset + n_base_points + (i + 1) % n_base_points
        base_faces.append([v3, center_idx, v4])
        
        # Connect outer and inner rings
        base_faces.append([v1, v3, v4])
        base_faces.append([v1, v4, v2])
    
    faces = np.vstack([faces, np.array(base_faces)])
    
    return vertices, faces

def main():
    """Generate and save STL file."""
    
    print("=" * 70)
    print("π-HELIX GEOBIT STL GENERATOR")
    print("=" * 70)
    print()
    print("UBP v3.4 Constants:")
    print(f"  Y (Base Resonance):      {Y:.15f}")
    print(f"  Y_INV (Observer):        {Y_INV:.15f}")
    print()
    print("Helix Specifications:")
    print(f"  Radius:                  {RADIUS:.1f} mm")
    print(f"  Height:                  {HEIGHT:.1f} mm")
    print(f"  Pitch:                   π/{10:.0f} rad")
    print(f"  Turns:                   {TURNS}")
    print(f"  Tube Radius:             {TUBE_RADIUS:.1f} mm")
    print(f"  Wall Thickness:          {WALL_THICKNESS:.1f} mm")
    print()
    
    print("Generating helix centerline...")
    centerline = generate_helix_path(RADIUS, HEIGHT, TURNS, THETA_STEPS)
    print(f"  Generated {len(centerline)} centerline points")
    
    print("Generating tube mesh...")
    vertices, faces = generate_tube_mesh(centerline, TUBE_RADIUS, CIRCLE_STEPS)
    print(f"  Generated {len(vertices)} vertices, {len(faces)} faces")
    
    print("Adding base plate...")
    vertices, faces = add_base_plate(vertices, faces, RADIUS, WALL_THICKNESS)
    print(f"  Total: {len(vertices)} vertices, {len(faces)} faces")
    
    print("Creating STL mesh...")
    # Create mesh
    helix_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            helix_mesh.vectors[i][j] = vertices[face[j]]
    
    # Save STL file
    output_file = 'pi_helix_geobit.stl'
    helix_mesh.save(output_file)
    
    print()
    print(f"✓ STL file saved: {output_file}")
    
    # Calculate statistics
    volume = helix_mesh.get_mass_properties()[0]
    surface_area = helix_mesh.areas.sum()
    
    print()
    print("Mesh Statistics:")
    print(f"  Volume:                  {volume/1000:.2f} cm³")
    print(f"  Surface Area:            {surface_area/100:.2f} cm²")
    print(f"  Estimated Print Time:    ~4 hours (0.2mm layers)")
    print(f"  Estimated Filament:      ~{volume/1000 * 1.25 * 0.0012:.0f}g HDPE")
    print(f"  Estimated Cost:          ~${volume/1000 * 1.25 * 0.0012 * 0.025:.2f} NZD")
    print()
    print("=" * 70)
    print("Ready for 3D printing!")
    print("Recommended settings: 0.2mm layer height, 20% infill, HDPE filament")
    print("=" * 70)

if __name__ == "__main__":
    main()
