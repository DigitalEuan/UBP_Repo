"""
UBP DISCOVERY ENGINE v1.1 (v5.3 Migration)
==========================================
An automated research laboratory for the Universal Binary Principle.
Generates, verifies, and documents emergent triadic laws.

Updated for UBP Core v5.3 Standards.
"""

import random
import json
import hashlib
from datetime import datetime
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v5_3_merged import BinaryLinearAlgebra, GOLAY_ENGINE, LEECH_ENGINE

class UBPDiscoveryEngine:
    def __init__(self):
        if not HEX_DB_EXACT.registry:
            HEX_DB_EXACT.load_memory()
        self.db = HEX_DB_EXACT
        self.all_ids = list(self.db.id_map.keys())
        
    def snap(self, vec):
        # v5.3 GOLAY_ENGINE uses the same decode/encode signature
        decoded, _, _ = GOLAY_ENGINE.decode(vec)
        return GOLAY_ENGINE.encode(decoded)

    def generate_hypothesis(self, id_a, id_b, id_out, dist):
        """Generates a semantic research prompt based on the reaction."""
        entry_a = self.db.find_by_id(id_a)
        entry_b = self.db.find_by_id(id_b)
        entry_out = self.db.find_by_id(id_out)
        
        dom_a = entry_a.get('tags', ['UNKNOWN'])[-1] if entry_a.get('tags') else 'UNKNOWN'
        dom_b = entry_b.get('tags', ['UNKNOWN'])[-1] if entry_b.get('tags') else 'UNKNOWN'
        
        hyp = f"How does the interaction of {id_a} ({dom_a}) and {id_b} ({dom_b}) "
        hyp += f"geometrically necessitate the emergence of {id_out}?"
        return hyp

    def run_session(self, trials=5000, output_file="ubp_discovery_report.json"):
        print(f"--- INITIATING DISCOVERY SESSION ({trials} TRIALS) [Core v5.3] ---")
        report = {
            "timestamp": datetime.now().isoformat(),
            "core_version": "5.3",
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

            # Interaction (XOR)
            interaction_vec = [(a ^ b) for a, b in zip(v_a, v_b)]
            
            # Snap to Grid (Golay Correction)
            v_prod = self.snap(interaction_vec)
            
            # Search for existing memories near this product
            best_match = None
            min_dist = 25
            
            # Optimization: Check exact match first
            # (In a full implementation, we might use a VP-Tree, but linear scan is fine for <5k items)
            for fp, entry in self.db.registry.items():
                target_vec = entry.get('vector', [])
                if not target_vec: continue
                
                d = BinaryLinearAlgebra.hamming_distance(v_prod, target_vec)
                if d < min_dist:
                    min_dist = d
                    best_match = entry
                if min_dist == 0: break 

            if min_dist <= 8:
                # Calculate Symmetry Tax using v5.3 Leech Engine
                tax_val = LEECH_ENGINE.calculate_symmetry_tax(v_prod)
                
                discovery = {
                    "input_a": id_a,
                    "input_b": id_b,
                    "output": best_match['ubp_id'],
                    "name": best_match.get('name'),
                    "distance": min_dist,
                    "tax": float(tax_val), # Convert Fraction to float for JSON
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
    engine.run_session(trials=1000)