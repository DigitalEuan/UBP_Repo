"""
================================================================================
UBP UNDERSTANDING ENGINE v3.0
================================================================================
Universal Binary Principal - Complete Traversal and Insight Engine

This engine provides comprehensive analysis of the UBP knowledge graph:
1. Bottom-up traversal (primitives → composites → molecules)
2. Top-down decomposition (any object → absolute primitives)
3. TAX pattern discovery and analysis
4. NRCI relationship verification
5. Path finding and dependency analysis
6. Insight generation from information dimensions

Author: Euan R A Craig, New Zealand
Version: 3.0 (Complete Rewrite)
Date: 2026-02-20
================================================================================
"""

import json
from fractions import Fraction
from collections import defaultdict
from typing import List, Dict, Any
from ubp_brain_v3 import UBPBrainV3


# ==============================================================================
# ENGINE CLASS
# ==============================================================================

class UBPUnderstandingEngine:
    """Main understanding and analysis engine"""
    
    def __init__(self, kb_file: str = 'ubp_system_kb.json'):
        print("[Understanding Engine v3] Initializing...")
        self.brain = UBPBrainV3()
        self.brain.load(kb_file)
        print("[Understanding Engine v3] Ready!\n")
    
    # ==========================================================================
    # SECTION 1: PRIMITIVE ANALYSIS
    # ==========================================================================
    
    def list_primitives(self) -> List[Dict[str, Any]]:
        """List all absolute primitives with their properties"""
        primitives = self.brain.kb.get_primitives()
        
        result = []
        for p in primitives:
            result.append({
                'ubp_id': p.ubp_id,
                'math': p.math,
                'weight': p.weight,
                'nrci': p.nrci_float,
                'tax': p.tax_float,
                'used_in_count': len(self.brain.kb.get_parents(p.ubp_id)),
                'tags': p.tags[:5]  # First 5 tags
            })
        
        return sorted(result, key=lambda x: x['ubp_id'])
    
    def analyze_primitive(self, ubp_id: str) -> Dict[str, Any]:
        """Deep analysis of a primitive"""
        return self.brain.analyze_object(ubp_id)
    
    # ==========================================================================
    # SECTION 2: BUILD UP FROM PRIMITIVES
    # ==========================================================================
    
    def build_up_from_quarks(self) -> Dict[str, Any]:
        """
        Build up from quark primitives.
        Shows what can be constructed at each level.
        """
        print("[Build Up] Starting from quark primitives...")
        
        # Get quark primitives
        quarks = [
            'PARTICLE_QUARK_UP_001',
            'PARTICLE_QUARK_DOWN_001',
            'PARTICLE_QUARK_STRANGE_001'
        ]
        
        # Build level 1 (nucleons)
        level_1 = self.brain.hierarchy.build_from_primitives(quarks)
        
        print(f"[Build Up] Level 1 (from quarks): {len(level_1)} objects")
        for entry in level_1[:5]:
            print(f"  - {entry.ubp_id}")
        
        # Add electron to build atoms
        primitives_with_electron = quarks + ['PARTICLE_ELECTRON_001']
        
        # Build level 1 again (includes proton, neutron)
        nucleons = [e.ubp_id for e in level_1]
        
        # Build level 2 (elements)
        level_2_primitives = primitives_with_electron + nucleons
        level_2 = self.brain.hierarchy.build_from_primitives(level_2_primitives)
        
        # Filter for actual level 2
        level_2_only = [e for e in level_2 if e not in level_1]
        
        print(f"[Build Up] Level 2 (from nucleons+electron): {len(level_2_only)} objects")
        for entry in level_2_only[:5]:
            print(f"  - {entry.ubp_id}")
        
        # Build level 3 (molecules)
        elements = [e.ubp_id for e in level_2_only if 'ELEM_' in e.ubp_id]
        level_3_primitives = primitives_with_electron + nucleons + elements
        level_3 = self.brain.hierarchy.build_from_primitives(level_3_primitives)
        
        level_3_only = [e for e in level_3 if e not in level_2]
        
        print(f"[Build Up] Level 3 (from elements): {len(level_3_only)} objects")
        for entry in level_3_only[:5]:
            print(f"  - {entry.ubp_id}")
        
        return {
            'level_0_primitives': quarks + ['PARTICLE_ELECTRON_001'],
            'level_1_nucleons': [e.ubp_id for e in level_1],
            'level_2_elements': [e.ubp_id for e in level_2_only if 'ELEM_' in e.ubp_id][:10],
            'level_3_molecules': [e.ubp_id for e in level_3_only if 'MOLECULE_' in e.ubp_id]
        }
    
    # ==========================================================================
    # SECTION 3: DECOMPOSE DOWN TO PRIMITIVES
    # ==========================================================================
    
    def decompose(self, ubp_id: str) -> Dict[str, Any]:
        """
        Decompose an object down to absolute primitives.
        Shows the complete breakdown.
        """
        entry = self.brain.kb.get(ubp_id)
        if not entry:
            return {'error': f'{ubp_id} not found'}
        
        print(f"\n[Decompose] Breaking down {ubp_id}...")
        
        # Get primitive composition
        primitives = self.brain.hierarchy.decompose_to_primitives(ubp_id)
        
        print(f"[Decompose] Primitive composition:")
        for prim_id, count in sorted(primitives.items()):
            print(f"  {count}× {prim_id}")
        
        # Get decomposition paths for each primitive
        paths = {}
        for prim_id in primitives.keys():
            path = self.brain.hierarchy.find_path_to_primitive(ubp_id, prim_id)
            paths[prim_id] = path
        
        return {
            'ubp_id': ubp_id,
            'primitive_composition': primitives,
            'paths_to_primitives': paths,
            'total_primitives': sum(primitives.values())
        }
    
    # ==========================================================================
    # SECTION 4: TAX ANALYSIS
    # ==========================================================================
    
    def analyze_tax_patterns(self) -> Dict[str, Any]:
        """
        Comprehensive TAX pattern analysis across all hierarchy levels.
        """
        print("\n[TAX Analysis] Discovering patterns...")
        
        patterns = self.brain.tax_analyzer.find_tax_patterns()
        
        report = {}
        
        for level, analyses in patterns.items():
            print(f"\n[TAX Analysis] {level}: {len(analyses)} objects")
            
            # Compute statistics
            ratios_simple = [a['ratio_simple'] for a in analyses if a['ratio_simple'] > 0]
            ratios_weighted = [a['ratio_weighted'] for a in analyses if a['ratio_weighted'] > 0]
            
            if ratios_simple:
                print(f"  Simple ratio (tax/sum_component_tax):")
                print(f"    Min: {min(ratios_simple):.6f}")
                print(f"    Max: {max(ratios_simple):.6f}")
                print(f"    Avg: {sum(ratios_simple)/len(ratios_simple):.6f}")
            
            if ratios_weighted:
                print(f"  Weighted ratio (tax/sum_weight*tax):")
                print(f"    Min: {min(ratios_weighted):.6f}")
                print(f"    Max: {max(ratios_weighted):.6f}")
                print(f"    Avg: {sum(ratios_weighted)/len(ratios_weighted):.6f}")
            
            # Show examples
            print(f"  Examples:")
            for a in analyses[:3]:
                print(f"    {a['ubp_id']}: tax={a['tax']:.4f}, components_sum={a['simple_sum_tax']:.4f}, ratio={a['ratio_simple']:.4f}")
            
            report[level] = {
                'count': len(analyses),
                'ratio_simple_avg': sum(ratios_simple)/len(ratios_simple) if ratios_simple else 0,
                'ratio_weighted_avg': sum(ratios_weighted)/len(ratios_weighted) if ratios_weighted else 0,
                'examples': analyses[:5]
            }
        
        return report
    
    # ==========================================================================
    # SECTION 5: COMPREHENSIVE OBJECT ANALYSIS
    # ==========================================================================
    
    def full_analysis(self, ubp_id: str) -> Dict[str, Any]:
        """
        Complete analysis of any object.
        Combines all analysis methods.
        """
        print(f"\n{'='*80}")
        print(f"FULL ANALYSIS: {ubp_id}")
        print(f"{'='*80}")
        
        analysis = self.brain.analyze_object(ubp_id)
        
        print(f"\nBasic Info:")
        print(f"  Level: {analysis['level']}")
        print(f"  Primitive: {analysis['is_primitive']}")
        print(f"  Math: {analysis['math'][:60]}...")
        print(f"  Hierarchy: {analysis['hierarchy']}")
        
        print(f"\nMetrics:")
        print(f"  Weight: {analysis['weight']}")
        print(f"  NRCI: {analysis['nrci']:.6f}")
        print(f"  TAX: {analysis['tax']:.6f}")
        
        if analysis['primitive_composition']:
            print(f"\nPrimitive Composition:")
            for prim, count in sorted(analysis['primitive_composition'].items()):
                print(f"  {count}× {prim}")
        
        if analysis['used_in']:
            print(f"\nUsed In ({len(analysis['used_in'])} objects):")
            for parent_id in analysis['used_in'][:5]:
                print(f"  - {parent_id}")
        
        if analysis['tax_analysis']:
            ta = analysis['tax_analysis']
            print(f"\nTAX Analysis:")
            print(f"  Component TAX sum: {ta.get('simple_sum_tax', 0):.6f}")
            print(f"  Ratio (tax/sum): {ta.get('ratio_simple', 0):.6f}")
        
        return analysis
    
    # ==========================================================================
    # SECTION 6: DISCOVERY AND INSIGHTS
    # ==========================================================================
    
    def find_similar_objects(self, ubp_id: str, metric: str = 'tax') -> List[Dict[str, Any]]:
        """
        Find objects with similar TAX, NRCI, or weight values.
        """
        entry = self.brain.kb.get(ubp_id)
        if not entry:
            return []
        
        target_value = getattr(entry, f'{metric}_float' if metric in ['tax', 'nrci'] else metric)
        
        similar = []
        for other_id, other_entry in self.brain.kb.entries.items():
            if other_id == ubp_id:
                continue
            
            other_value = getattr(other_entry, f'{metric}_float' if metric in ['tax', 'nrci'] else metric)
            diff = abs(target_value - other_value)
            
            if diff < target_value * 0.1:  # Within 10%
                similar.append({
                    'ubp_id': other_id,
                    'value': other_value,
                    'diff': diff,
                    'level': other_entry.classify_level()
                })
        
        return sorted(similar, key=lambda x: x['diff'])[:10]
    
    def compare_objects(self, id1: str, id2: str) -> Dict[str, Any]:
        """Compare two objects side by side"""
        entry1 = self.brain.kb.get(id1)
        entry2 = self.brain.kb.get(id2)
        
        if not entry1 or not entry2:
            return {'error': 'One or both objects not found'}
        
        # Decompose both
        prims1 = self.brain.hierarchy.decompose_to_primitives(id1)
        prims2 = self.brain.hierarchy.decompose_to_primitives(id2)
        
        # Find common primitives
        common_prims = set(prims1.keys()) & set(prims2.keys())
        
        return {
            'object_1': {
                'ubp_id': id1,
                'level': entry1.classify_level(),
                'weight': entry1.weight,
                'nrci': entry1.nrci_float,
                'tax': entry1.tax_float,
                'primitives': prims1
            },
            'object_2': {
                'ubp_id': id2,
                'level': entry2.classify_level(),
                'weight': entry2.weight,
                'nrci': entry2.nrci_float,
                'tax': entry2.tax_float,
                'primitives': prims2
            },
            'comparison': {
                'weight_diff': entry1.weight - entry2.weight,
                'nrci_diff': entry1.nrci_float - entry2.nrci_float,
                'tax_diff': entry1.tax_float - entry2.tax_float,
                'common_primitives': list(common_prims)
            }
        }


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':
    print("="*80)
    print("UBP UNDERSTANDING ENGINE v3.0")
    print("="*80)
    
    engine = UBPUnderstandingEngine()
    
    print("\n" + "="*80)
    print("EXPERIMENT 1: List Primitives")
    print("="*80)
    primitives = engine.list_primitives()
    print(f"\nFound {len(primitives)} primitives")
    print("\nParticle primitives:")
    for p in primitives:
        if 'PARTICLE_' in p['ubp_id'] and ('QUARK' in p['ubp_id'] or 'ELECTRON' in p['ubp_id'] or 'NEUTRIN' in p['ubp_id']):
            print(f"  {p['ubp_id']}: tax={p['tax']:.4f}, weight={p['weight']}, used_in={p['used_in_count']} objects")
    
    print("\n" + "="*80)
    print("EXPERIMENT 2: Build Up from Quarks")
    print("="*80)
    build_result = engine.build_up_from_quarks()
    
    print("\n" + "="*80)
    print("EXPERIMENT 3: Decompose Hydrogen")
    print("="*80)
    h_decomp = engine.decompose('ELEM_H_001')
    
    print("\n" + "="*80)
    print("EXPERIMENT 4: Decompose Water")
    print("="*80)
    water_decomp = engine.decompose('MOLECULE_H2O')
    
    print("\n" + "="*80)
    print("EXPERIMENT 5: TAX Pattern Analysis")
    print("="*80)
    tax_patterns = engine.analyze_tax_patterns()
    
    print("\n" + "="*80)
    print("EXPERIMENT 6: Full Analysis of Key Objects")
    print("="*80)
    
    for obj_id in ['PARTICLE_QUARK_UP_001', 'PARTICLE_PROTON_001', 'ELEM_H_001', 'MOLECULE_H2O']:
        analysis = engine.full_analysis(obj_id)
    
    print("\n" + "="*80)
    print("EXPERIMENT 7: Compare Proton and Neutron")
    print("="*80)
    comparison = engine.compare_objects('PARTICLE_PROTON_001', 'PARTICLE_NEUTRON_001')
    print(json.dumps(comparison, indent=2))
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETE")
    print("="*80)
