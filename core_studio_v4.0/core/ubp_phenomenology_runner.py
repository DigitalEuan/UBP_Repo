"""
================================================================================
UBP PHENOMENOLOGY RUNNER - v4.1.1 (PRODUCTION)
================================================================================
Description: The Laboratory Controller. Orchestrates batch resolution of 
identities and generates 3D manifold visualizations.
================================================================================
"""
import json
import time
from typing import List, Dict, Any
from ubp_phenomenology_def import PhenomenonDefinition
from metrics import METRICS
import ubp_core_final_v4_1_1 as core
from ubp_core_final_v4_1_1 import save_scene_3d

class PhenomenologyRunner:
    """
    Orchestrates UBP studies by resolving batches of phenomena and 
    mapping them to the 24D Leech Substrate.
    """
    
    def __init__(self, study_name: str):
        self.study_name = study_name
        self.start_time = time.time()
        self.registry: List[PhenomenonDefinition] = []
        self.results_cache: List[Dict] = []

    def add_phenomenon(self, name: str, domain: str, raw_hex: str = None, tokens: List[str] = None):
        """Adds a new identity to the study batch."""
        phenom = PhenomenonDefinition(name, domain, raw_hex, tokens)
        self.registry.append(phenom)

    def run_study(self):
        """Resolves all registered phenomena and calculates aggregate metrics."""
        print(f"\n[RUNNER] Starting Study: {self.study_name}")
        print(f"[RUNNER] Substrate Version: 4.1.1 | Observer Cost: {METRICS.get_base_cost():.6f}")
        
        for phenom in self.registry:
            print(f"  > Resolving: {phenom.name}...", end="\r")
            res = phenom.resolve()
            self.results_cache.append({
                "name": phenom.name,
                "domain": phenom.domain,
                "nrci": res["nrci"],
                "tax": res["symmetry_tax"],
                "health": res["ontological_health"],
                "leech_point": phenom.leech_point,
                "stable": res["is_stable"]
            })
        
        print(f"\n[RUNNER] Study Complete. Processed {len(self.registry)} identities.")
        self._report_aggregates()

    def _report_aggregates(self):
        """Calculates the Global Coherence of the study batch."""
        avg_nrci = sum(r["nrci"] for r in self.results_cache) / len(self.results_cache)
        avg_tax = sum(r["tax"] for r in self.results_cache) / len(self.results_cache)
        
        print(f"\n--- AGGREGATE REPORT: {self.study_name} ---")
        print(f"Global NRCI: {avg_nrci:.6f}")
        print(f"Average Symmetry Tax: {avg_tax:.4f}")
        print(f"Coherence Regime: {'OPTIMIZED' if avg_nrci > 0.9 else 'STOCHASTIC'}")
        print("------------------------------------------")

    def generate_3d_manifold(self):
        """
        LAW_GPU_001: Maps the Leech Points to the 3D Visualizer.
        Uses the first 3 coordinates of the Leech Point for spatial mapping.
        """
        points = []
        for res in self.results_cache:
            lp = res["leech_point"]
            # Map Leech coordinates to 3D space
            points.append({
                "x": lp[0], 
                "y": lp[1], 
                "z": lp[2],
                "color": "#00ffcc" if res["stable"] else "#ff3366",
                "size": 0.5 + (res["nrci"] * 0.5),
                "label": res["name"]
            })
        
        save_scene_3d({"points": points, "study": self.study_name})
        print(f"[RUNNER] 3D Manifold generated for {self.study_name}.")

    def export_json(self, filename: str = "study_results.json"):
        """Exports the full triadic data to JSON."""
        with open(filename, 'w') as f:
            json.dump(self.results_cache, f, indent=2)
        print(f"[RUNNER] Results exported to {filename}.")

if __name__ == "__main__":
    # Example Study: Noble Gas Stability (Chemistry Domain)
    lab = PhenomenologyRunner("Noble_Gas_Resonance")
    
    # Adding identities
    lab.add_phenomenon("Helium", "Chemistry", raw_hex="He_2")
    lab.add_phenomenon("Neon", "Chemistry", raw_hex="Ne_10")
    lab.add_phenomenon("Argon", "Chemistry", raw_hex="Ar_18")
    lab.add_phenomenon("Krypton", "Chemistry", raw_hex="Kr_36")
    lab.add_phenomenon("Xenon", "Chemistry", raw_hex="Xe_54")
    lab.add_phenomenon("Radon", "Chemistry", raw_hex="Rn_86")
    
    # Execution
    lab.run_study()
    lab.generate_3d_manifold()
    lab.export_json()
