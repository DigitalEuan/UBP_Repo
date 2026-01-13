#!/usr/bin/env python3
"""
UBP RGDL Engine v1.0 (Resonance Geometry Definition Language)
=============================================================
The Standard Visualization Engine for the UBP System.

"Geometry is the macroscopic manifestation of synchronized binary toggles."

FEATURES:
- Primitives: Sphere, Cube, Lattice.
- Physics: Coherence Pressure coloring (Core vs. Edge).
- Output: Direct injection to Visual Cortex via 'ubp_viz'.

Usage:
  import ubp_rgdl
  ubp_rgdl.manifest_sphere(radius=15)
  
  # Or run as demo:
  python ubp_rgdl.py

Author: UBP Research Cortex v4.2.6
"""
import math
import sys

# Try to import the visual bridge; mock it if running in pure terminal
try:
    import ubp_viz
    VIZ_ACTIVE = True
except ImportError:
    VIZ_ACTIVE = False
    print("[RGDL] Warning: 'ubp_viz' not found. Visual output disabled.")

class RGDLEngine:
    def __init__(self):
        self.palette = {
            "core": (0, 0, 136),   # Deep Blue (#000088)
            "edge": (0, 255, 255)  # Cyan (#00FFFF)
        }

    def _get_coherence_color(self, dist, max_dist):
        """Maps Coherence Pressure (Distance from Center) to Color."""
        if max_dist == 0: return "#00ffff"
        norm = dist / max_dist
        
        # Linear interpolation
        r = int(self.palette["core"][0] + (self.palette["edge"][0] - self.palette["core"][0]) * norm)
        g = int(self.palette["core"][1] + (self.palette["edge"][1] - self.palette["core"][1]) * norm)
        b = int(self.palette["core"][2] + (self.palette["edge"][2] - self.palette["core"][2]) * norm)
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def generate_sphere(self, radius: int) -> list:
        """Generates a Voxelized Sphere (The Monad)."""
        voxels = []
        r_sq = radius * radius
        
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                for z in range(-radius, radius + 1):
                    dist_sq = x*x + y*y + z*z
                    if dist_sq <= r_sq:
                        dist = math.sqrt(dist_sq)
                        voxels.append({
                            "x": x, "y": y, "z": z,
                            "r": 0.4, 
                            "color": self._get_coherence_color(dist, radius)
                        })
        return voxels

    def generate_cube(self, size: int) -> list:
        """Generates a Voxelized Cube (The Matrix)."""
        voxels = []
        half = size // 2
        max_dist = math.sqrt(3 * half**2)
        
        for x in range(-half, half + 1):
            for y in range(-half, half + 1):
                for z in range(-half, half + 1):
                    dist = math.sqrt(x*x + y*y + z*z)
                    voxels.append({
                        "x": x, "y": y, "z": z,
                        "r": 0.4,
                        "color": self._get_coherence_color(dist, max_dist)
                    })
        return voxels

    def render(self, voxels: list, label: str = "Geometry"):
        """Injects the geometry into the Visual Cortex."""
        count = len(voxels)
        print(f"--- MANIFESTING {label} ---")
        print(f"Active Toggles: {count}")
        
        if VIZ_ACTIVE:
            scene = {"spheres": voxels}
            ubp_viz.save_scene_3d(scene)
            print("✅ Scene sent to Visual Cortex.")
        else:
            print("❌ Visualization skipped (No Bridge).")

# --- CONVENIENCE FUNCTIONS ---

def manifest_sphere(radius=15):
    engine = RGDLEngine()
    voxels = engine.generate_sphere(radius)
    engine.render(voxels, f"RGDL SPHERE (r={radius})")

def manifest_cube(size=20):
    engine = RGDLEngine()
    voxels = engine.generate_cube(size)
    engine.render(voxels, f"RGDL CUBE (s={size})")

# --- DEMO MODE ---
if __name__ == "__main__":
    # Default behavior: Manifest a Sphere
    manifest_sphere(12)