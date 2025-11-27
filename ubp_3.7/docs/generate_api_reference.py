"""
Generate Comprehensive API Reference for UBP 3.7
=================================================

This script inspects all modules and generates a Markdown document
with the real, working APIs.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.7')

import inspect
import os

# List of all modules to document
MODULES = [
    # Core
    ("core.coherence_substrate", "CoherenceState"),
    ("core.state", "OffBit"),
    ("core.y_constants", "YConstants"),
    ("core.system_constants", "UBPConstants"),
    
    # Error Correction
    ("error_correction.golay_code", "GolayG24"),
    ("error_correction.leech_lattice", "LeechLattice"),
    ("error_correction.vector_offbit", "VectorOffBit"),
    
    # Analysis
    ("analysis.resonance_detector_fft", "ResonanceDetectorFFT"),
    
    # Simulation
    ("simulation.simulation", "PhysicsSimulator"),
    
    # Reversible
    ("reversible.reversible_coherence_state", "ReversibleCoherenceState"),
    
    # Realms
    ("realms.atomic_realm", "AtomicRealm"),
    ("realms.electromagnetic_realm", "ElectromagneticRealm"),
    ("realms.optical_realm", "OpticalRealm"),
    ("realms.nuclear_realm", "NuclearRealm"),
    ("realms.gravitational_realm", "GravitationalRealm"),
    ("realms.biological_realm", "BiologicalRealm"),
    ("realms.plasma_realm", "PlasmaRealm"),
    ("realms.cosmological_realm", "CosmologicalRealm"),
]

def generate_api_reference():
    """Generate the API reference document."""
    
    with open("API_REFERENCE.md", "w") as f:
        f.write("# UBP 3.7 API Reference\n\n")
        f.write("This document provides the real, working API for all UBP 3.7 modules.\n\n")
        
        for module_name, class_name in MODULES:
            try:
                module = __import__(module_name, fromlist=[class_name])
                TargetClass = getattr(module, class_name)
                
                f.write(f"## {module_name}.{class_name}\n\n")
                f.write(f"{inspect.getdoc(TargetClass)}\n\n")
                
                # Constructor
                try:
                    sig = inspect.signature(TargetClass.__init__)
                    f.write(f"### Constructor\n`{class_name}{sig}`\n\n")
                except (TypeError, ValueError):
                    f.write("### Constructor\nNo explicit constructor.\n\n")
                
                # Methods
                f.write("### Methods\n")
                methods = inspect.getmembers(TargetClass, predicate=inspect.isfunction)
                if not methods:
                    f.write("No public methods.\n\n")
                else:
                    for name, func in methods:
                        if not name.startswith("_"):
                            try:
                                sig = inspect.signature(func)
                                f.write(f"- **`{name}{sig}`**\n")
                                doc = inspect.getdoc(func)
                                if doc:
                                    f.write(f"  - {doc.strip()}\n")
                            except ValueError:
                                f.write(f"- **`{name}`** (signature not available)\n")
                f.write("\n")
                
            except Exception as e:
                f.write(f"## {module_name}.{class_name}\n\n")
                f.write(f"**ERROR:** Could not inspect module: {e}\n\n")

if __name__ == "__main__":
    generate_api_reference()
    print("✅ API Reference generated successfully!")
