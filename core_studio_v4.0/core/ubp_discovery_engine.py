"""
UBP DISCOVERY ENGINE v1.0 (Pro Edition)
=======================================
An automated research laboratory for the Universal Binary Principle.
Generates, verifies, and documents emergent triadic laws.

Author: UBP Research Cortex v4.2.7
"""

import random
import json
import hashlib
from datetime import datetime
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra, GOLAY_DECODER, LEECH_ENHANCED

class UBPDiscoveryEngine:
    def __init__(self):
        if not HEX_DB_EXACT.registry:
            HEX_DB_EXACT.load_memory()
        self.db = HEX_DB_EXACT
        self.all_ids = list(self.db.id_map.keys())
        
    def snap(self, vec):
        decoded, _, _ = GOLAY_DECODER.decode(vec)
        return GOLAY_DECODER.encode(decoded)

    def generate_hypothesis(self, id_a, id_b, id_out, dist):
        """Generates a semantic research prompt based on the reaction."""
        entry_a = self.db.find_by_id(id_a)
        entry_b = self.db.find_by_id(id_b)
        entry_out = self.db.find_by_id(id_out)
        
        dom_a = entry_a.get('tags', ['UNKNOWN'])[-1]
        dom_b = entry_b.get('tags', ['UNKNOWN'])[-1]
        
        hyp = f"How does the interaction of {id_a} ({dom_a}) and {id_b} ({dom_b}) "
        hyp += f"geometrically necessitate the emergence of {id_out}?"
        return hyp

    def run_session(self, trials=5000, output_file="ubp_discovery_report.json"):
        print(f"--- INITIATING DISCOVERY SESSION ({trials} TRIALS) ---")
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_trials": trials,
            "perfect_resonances": [],
            "harmonic_resonances": []
        }

        for i in range(trials):
            id_a = random.choice(self.all_ids)
            id_b = random.choice(self.all_ids)
            if id_a == id_b: continue

            v_a = self.db.get_vector(id_a)
            v_b = self.db.get_vector(id_b)
            if not v_a or not v_b: continue

            # Interaction
            v_prod = self.snap([(a ^ b) for a, b in zip(v_a, v_b)])
            
            # Search
            best_match = None
            min_dist = 25
            for fp, entry in self.db.registry.items():
                d = BinaryLinearAlgebra.hamming_distance(v_prod, entry.get('vector', []))
                if d < min_dist:
                    min_dist = d
                    best_match = entry
                if min_dist == 0: break # Optimization

            if min_dist <= 8:
                discovery = {
                    "input_a": id_a,
                    "input_b": id_b,
                    "output": best_match['ubp_id'],
                    "name": best_match.get('name'),
                    "distance": min_dist,
                    "tax": float(LEECH_ENHANCED.calculate_symmetry_tax(v_prod)),
                    "hypothesis": self.generate_hypothesis(id_a, id_b, best_match['ubp_id'], min_dist)
                }
                
                if min_dist == 0:
                    report["perfect_resonances"].append(discovery)
                else:
                    report["harmonic_resonances"].append(discovery)

        # Sort by Tax (Efficiency)
        report["perfect_resonances"].sort(key=lambda x: x['tax'])
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"✅ Session Complete. Found {len(report['perfect_resonances'])} Perfect and {len(report['harmonic_resonances'])} Harmonic resonances.")
        print(f"📂 Report saved to: {output_file}")

if __name__ == "__main__":
    engine = UBPDiscoveryEngine()
    engine.run_session(trials=1000) # Start with 1k for safety, user can increase