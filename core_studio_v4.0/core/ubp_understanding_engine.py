"""
================================================================================
UBP UNDERSTANDING ENGINE v3.3 (The Complete Suite)
================================================================================
The definitive research tool for the Universal Binary Principle.
Consolidates all functions from v1, v3.1, and vA into a single aligned class.

Author: Euan R A Craig & UBP Research Cortex
Date: 26 Feb 2026
================================================================================
"""

import json
import re
import os
import sys
import hashlib
from collections import defaultdict, Counter
from fractions import Fraction
from typing import Dict, List, Tuple, Optional, Any
import statistics

# --- CORE IMPORTS ---
try:
    from ubp_brain_consolidated import UBPBrain
    from ubp_core_v5_3_merged import GOLAY_ENGINE, BinaryLinearAlgebra, LEECH_ENGINE
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[CRITICAL] Import failed: {e}")
    sys.exit(1)

# --- HELPERS ---
def find_best_kb():
    candidates = ['ubp_system_kb_v2.json', 'ubp_system_kb_enriched.json', 'ubp_system_kb.json']
    for c in candidates:
        if os.path.exists(c): return c
    return None

def parse_math_dna(dna: str) -> Dict[str, int]:
    if not dna or not isinstance(dna, str): return {}
    if '|' in dna: dna = dna.split('|', 1)[1].strip()
    components = {}
    mult_pattern = re.compile(r'(\d+)\s*[×xX]\s*([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]+)')
    for mult_str, comp_id in mult_pattern.findall(dna):
        components[comp_id] = components.get(comp_id, 0) + int(mult_str)
    id_pattern = re.compile(r'\b([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]{3,})\b')
    for comp_id in id_pattern.findall(dna):
        if comp_id not in components: components[comp_id] = 1
    junk = {'N', 'Z', 'Tax', 'Mean', 'Dist', 'Snap', 'NRCI', 'TAX', 'Mass', 'Spin', 'Charge'}
    return {k: v for k, v in components.items() if k not in junk and not k.isdigit()}

# ==============================================================================
# THE UNIFIED ENGINE CLASS
# ==============================================================================

class UBPUnderstandingEngine:
    def __init__(self, kb_path: str = None):
        print(f"[Engine v3.3] Booting...")
        self.brain = UBPBrain()
        target_kb = kb_path or find_best_kb()
        if not target_kb: raise FileNotFoundError("No Knowledge Base found.")
        self.brain.initialize([target_kb])
        self.kb = self.brain.memory.kb # Direct access to dictionary
        print(f"[Engine v3.3] Online. {len(self.kb)} concepts indexed.")

    def _get_vec(self, entry):
        if 'vector' in entry: return entry['vector']
        return entry.get('atlas', {}).get('vector')

    def _get_tax(self, entry):
        tax_val = entry.get('tax') or entry.get('atlas', {}).get('tax', '0/1')
        try: return Fraction(tax_val)
        except: return Fraction(0)

    # --- SECTION 1: HIERARCHY & BINDING ---

    def audit_hierarchy(self, ubp_id: str) -> Dict[str, Any]:
        entry = self.kb.get(ubp_id)
        if not entry: return {"status": "MISSING"}
        target_vec = self._get_vec(entry)
        components = parse_math_dna(entry.get('math', ''))
        if not components: return {"status": "PRIMITIVE", "name": entry.get('name', ubp_id)}

        composed_coords = [0] * 24
        for comp_id, count in components.items():
            comp = self.kb.get(comp_id)
            c_vec = self._get_vec(comp) if comp else None
            if c_vec:
                vals = [1 if b else -1 for b in c_vec]
                for _ in range(count):
                    for i in range(24): composed_coords[i] += vals[i]

        raw_bits = [1 if c > 0 else 0 for c in composed_coords]
        snapped, _, _ = self.brain.vector_engine.coherence_snap(raw_bits)
        dist = BinaryLinearAlgebra.hamming_distance(target_vec, snapped)
        return {"status": "AUDITED", "name": entry.get('name', ubp_id), "gap": dist, "is_closed": dist == 0}

    def audit_binding_energy(self, ubp_id: str) -> Dict[str, Any]:
        entry = self.kb.get(ubp_id)
        if not entry: return {}
        assembly_tax = self._get_tax(entry)
        components = parse_math_dna(entry.get('math', ''))
        parts_tax_sum = Fraction(0)
        for comp_id, count in components.items():
            comp = self.kb.get(comp_id)
            if comp: parts_tax_sum += (self._get_tax(comp) * count)
        if parts_tax_sum == 0: return {"status": "PRIMITIVE"}
        rebate = parts_tax_sum - assembly_tax
        eff = (float(rebate) / float(parts_tax_sum)) * 100 if parts_tax_sum > 0 else 0
        return {"name": entry.get('name', ubp_id), "parts_tax": float(parts_tax_sum), 
                "assembly_tax": float(assembly_tax), "rebate": float(rebate), "efficiency_percent": eff}

    # --- SECTION 2: STRUCTURAL ANALYSIS ---

    def list_primitives(self):
        prims = [e for e in self.kb.values() if e.get('atlas', {}).get('hierarchy') == 'absolute_primitive']
        return sorted([{"id": p['ubp_id'], "tax": float(self._get_tax(p))} for p in prims], key=lambda x: x['tax'])

    def build_up_from_quarks(self):
        print("\n[Build Up] Evolutionary Ladder:")
        # Use fuzzy matching for quarks to handle different naming versions
        quarks = [uid for uid in self.kb if 'QUARK' in uid and ('UP' in uid or 'DOWN' in uid)]
        
        # Level 1: Nucleons (Protons/Neutrons)
        nucleons = [uid for uid, e in self.kb.items() 
                   if any(q in e.get('math', '') for q in quarks) and 'PARTICLE_' in uid and 'QUARK' not in uid]
        print(f"  L1 Nucleons: {', '.join(nucleons[:3]) if nucleons else 'None Found'}")
        
        # Level 2: Elements
        elements = [uid for uid, e in self.kb.items() 
                   if any(n in e.get('math', '') for n in nucleons) and 'ELEM_' in uid]
        print(f"  L2 Elements: {', '.join(elements[:3]) if elements else 'None Found'}")
        
        # Level 3: Molecules
        molecules = [uid for uid, e in self.kb.items() 
                    if any(el in e.get('math', '') for el in elements) and 'MOLECULE_' in uid]
        print(f"  L3 Molecules: {', '.join(molecules[:3]) if molecules else 'None Found'}")

    def ask(self, query: str):
        # Refinement: If the query contains biological or chemical terms, 
        # we temporarily boost the SUBSTANCE domain in the brain's reasoning.
        if any(word in query.upper() for word in ["ATP", "WATER", "GLUCOSE", "PROTON"]):
            # This is a conceptual 'nudge' to the brain
            return self.brain.process_query(query + " (Focus: Substance)").response
        return self.brain.process_query(query).response

    # --- SECTION 3: STATISTICAL LANDSCAPE ---

    def analyse_nrci_landscape(self):
        data = defaultdict(list)
        for e in self.kb.values():
            prefix = e['ubp_id'].split('_')[0]
            nrci = e.get('atlas', {}).get('nrci_score', 0)
            data[prefix].append(float(nrci))
        
        print("\n[Landscape] NRCI Distribution by Domain:")
        for prefix, vals in sorted(data.items()):
            print(f"  {prefix:12}: mean={statistics.mean(vals):.4f} (n={len(vals)})")

    def analyze_tax_patterns(self):
        print("\n[Patterns] TAX Efficiency Ratios:")
        for uid in ["PARTICLE_PROTON_001", "ELEM_H_001", "MOLECULE_H2O"]:
            res = self.audit_binding_energy(uid)
            if 'efficiency_percent' in res:
                print(f"  {uid:20}: {res['efficiency_percent']:.2f}% Efficiency")

    # --- SECTION 4: DISCOVERY & SCALING ---

    def run_scaling_experiment(self):
        print("\n[Experiment] Intelligence Scaling:")
        sizes = [100, 300, 500, len(self.kb)]
        for s in sizes:
            coverage = (s / len(self.kb)) * 100
            # Heuristic: Accuracy scales with log of KB size in UBP
            acc = 40 + (statistics.math.log(s) * 5)
            print(f"  KB Size: {s:4} | Coverage: {coverage:5.1f}% | Predicted Accuracy: {acc:.1f}%")

    def compare(self, id_a, id_b):
        e_a, e_b = self.kb.get(id_a), self.kb.get(id_b)
        if not e_a or not e_b: return "Missing ID"
        dist = BinaryLinearAlgebra.hamming_distance(self._get_vec(e_a), self._get_vec(e_b))
        return {"dist": dist, "tax_delta": float(abs(self._get_tax(e_a) - self._get_tax(e_b)))}

    # --- SECTION 5: COMMUNICATION ---

    def ask(self, query: str):
        return self.brain.process_query(query).response

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("="*80)
    print("UBP UNDERSTANDING ENGINE v3.3 (Consolidated)")
    print("="*80)
    
    engine = UBPUnderstandingEngine()

    # Run Suite
    engine.build_up_from_quarks()
    engine.analyse_nrci_landscape()
    engine.analyze_tax_patterns()
    engine.run_scaling_experiment()

    print("\n--- Sample Comparison: Proton vs Neutron ---")
    print(engine.compare("PARTICLE_PROTON_001", "PARTICLE_NEUTRON_001"))

    print("\n--- Sample Audit: Water ---")
    print(engine.audit_hierarchy("MOLECULE_H2O"))

    print("\n--- Cortex Query ---")
    q = "What is the composition of ATP?"
    print(f"Q: {q}\nA: {engine.ask(q)}")