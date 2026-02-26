"""
================================================================================
UBP UNDERSTANDING ENGINE v3.1 (Unified & Hardened)
================================================================================
Universal Binary Principal - Complete Traversal and Insight Engine

FIXES:
- Resolved 'UBPBrain' vs 'UBPBrainV3' naming conflict.
- Integrated v5.3 Core (Fractions & Leech Tax).

ADVANCED FEATURES:
1. Information Equivalence: Finds objects with identical geometric signatures.
2. Tilt Audit: Measures the 'Charge' of a hierarchy as it builds up.
3. Binding Energy Calculation: Measures the 'Symmetry Rebate' in composites.

Author: Euan R A Craig, New Zealand
Version: 3.1
Date: 23 Feb 2026
"""

import json
import hashlib
import re
from fractions import Fraction
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional, Any

# Import the Consolidated Brain and Core
from ubp_brain_v3 import UBPBrainV3
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra

class UBPUnderstandingEngineV3_1:
    def __init__(self, kb_file: str = 'ubp_system_kb.json'):
        print("[Understanding Engine v3.1] Initializing...")
        self.brain = UBPBrainV3()
        self.brain.load(kb_file)
        print("[Understanding Engine v3.1] Ready!\n")

    # --- SECTION 1: HIERARCHY & DECOMPOSITION ---

    def full_decomposition(self, ubp_id: str):
        """Tears an object down to its irreducible subatomic primitives."""
        print(f"\n[DECOMPOSE] Breaking down {ubp_id}...")
        analysis = self.brain.analyze_object(ubp_id)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return

        print(f"  Level: {analysis['level']}")
        print(f"  Composition:")
        for prim, count in sorted(analysis['primitive_composition'].items()):
            print(f"    - {count}× {prim}")
        
        return analysis

    # --- SECTION 2: GEOMETRIC INSIGHTS ---

    def find_information_equivalents(self):
        """
        DISCOVERY: Finds objects that share the same (Weight, NRCI, Tax).
        This reveals 'Geometric Synonyms' in the substrate.
        """
        print("\n[INSIGHT] Searching for Information Equivalence Classes...")
        classes = defaultdict(list)
        
        for entry in self.brain.kb.entries.values():
            # Create a signature from the metrics
            sig = (entry.weight, round(entry.nrci_float, 6), round(entry.tax_float, 6))
            classes[sig].append(entry.ubp_id)
            
        equivalents = {k: v for k, v in classes.items() if len(v) > 1}
        
        for sig, ids in equivalents.items():
            print(f"  Equivalence Found {sig}:")
            print(f"    > {', '.join(ids)}")
        
        return equivalents

    def audit_binding_efficiency(self, ubp_id: str):
        """
        Calculates the 'Symmetry Rebate' (Binding Energy).
        Compares the Tax of the whole vs the sum of the parts.
        """
        entry = self.brain.kb.get(ubp_id)
        if not entry or entry.is_primitive(): return

        analysis = self.brain.tax_analyzer.analyze_composition_tax(ubp_id)
        if not analysis: return

        actual_tax = analysis['tax']
        parts_tax = analysis['simple_sum_tax']
        rebate = parts_tax - actual_tax
        efficiency = (rebate / parts_tax) * 100 if parts_tax > 0 else 0

        print(f"\n[AUDIT] Binding Efficiency for {ubp_id}:")
        print(f"  Sum of Parts Tax: {parts_tax:.4f}")
        print(f"  Assembled Tax:    {actual_tax:.4f}")
        print(f"  Symmetry Rebate:  {rebate:.4f} ({efficiency:.2f}%)")
        
        return efficiency

    # --- SECTION 3: COMPARATIVE ANALYSIS ---

    def compare(self, id_a: str, id_b: str):
        """Side-by-side comparison of two geometric identities."""
        print(f"\n[COMPARE] {id_a} vs {id_b}")
        
        res = self.brain.hierarchy.find_path_to_primitive(id_a, id_b) # Check if related
        
        obj_a = self.brain.kb.get(id_a)
        obj_b = self.brain.kb.get(id_b)
        
        if not obj_a or not obj_b: return

        dist = BinaryLinearAlgebra.hamming_distance(obj_a.vector, obj_b.vector)
        
        print(f"  Hamming Distance: {dist} bits")
        print(f"  NRCI Delta:       {abs(obj_a.nrci_float - obj_b.nrci_float):.6f}")
        print(f"  Tax Delta:        {abs(obj_a.tax_float - obj_b.tax_float):.4f}")
        
        if dist <= 3:
            print("  Status: COHERENT PAIR (Geometric Variants)")
        elif dist == 24:
            print("  Status: PERFECT INVERSION (Antipodes)")
        else:
            print("  Status: DISSONANT (Distinct Identities)")

# --- EXECUTION ---
if __name__ == "__main__":
    engine = UBPUnderstandingEngineV3_1()
    
    # 1. Test Recursive Breakdown
    engine.full_decomposition("MOLECULE_H2O")
    
    # 2. Test Binding Efficiency (The 'Free Red' Logic)
    engine.audit_binding_efficiency("PARTICLE_PROTON_001")
    engine.audit_binding_efficiency("ELEM_H_001")
    
    # 3. Find Geometric Synonyms
    engine.find_information_equivalents()
    
    # 4. Compare Proton vs Neutron
    engine.compare("PARTICLE_PROTON_001", "PARTICLE_NEUTRON_001")