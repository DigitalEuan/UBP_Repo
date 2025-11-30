#!/usr/bin/env python3
"""
TGIC Cross-Geometry Validator
Tests TGIC consistency across multiple geometric structures

Based on concept by Qwen AI
Author: UBP Development Team
Date: November 30, 2025
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import numpy as np
import json
import time
from typing import Dict, Any

from utils.tgic import TGICSystem, TGICGeometry
from studies.TGIC.geometry_registry import GEOMETRY_REGISTRY
from studies.TGIC.geometry_constraints_ext import inject_geometry_methods
from studies.TGIC.geometry_graphs import create_geometry_graph


def run_cross_geometry_test() -> Dict[str, Any]:
    """
    Run cross-geometry validation test.
    
    Tests TGIC across all geometric structures and measures:
    - Constraint satisfaction
    - Coherence levels
    - NRCI proxy (coherence-based metric)
    - Cross-consistency
    """
    print("=" * 70)
    print("🚀 TGIC CROSS-GEOMETRY VALIDATION")
    print("=" * 70)
    print("Based on concept by Qwen AI")
    print("Testing geometric relativity of truth in UBP 3.7.1")
    print("=" * 70)
    
    # Inject geometry-specific methods
    inject_geometry_methods(TGICSystem)
    
    results = {}
    baseline_nrci = None
    
    for geo in TGICGeometry:
        print(f"\n{'='*70}")
        print(f"🧪 Testing {geo.value.upper()}")
        print(f"{'='*70}")
        
        spec = GEOMETRY_REGISTRY.get(geo)
        if not spec:
            print(f"⚠️  No specification found for {geo.value}, skipping...")
            continue
        
        print(f"Triad: {spec.triad}")
        print(f"Description: {spec.description}")
        print(f"Coherence threshold: {spec.coherence_threshold}")
        
        try:
            # Create system
            print(f"\n→ Creating {geo.value} system...")
            system = TGICSystem(geometry=geo)
            
            # Replace graph with geometry-specific one
            if geo != TGICGeometry.LEECH_24D:
                print(f"→ Generating {geo.value} graph...")
                system.graph = create_geometry_graph(geo.value)
                print(f"   Nodes: {len(system.graph.nodes)}, Edges: {len(system.graph.edges)}")
            
            # Override constraints with geometry-specific ones
            print(f"→ Initializing geometry-specific constraints...")
            system.constraints.clear()
            spec.constraint_initializer(system)
            
            print(f"   Constraints initialized: {len(system.constraints)}")
            
            # Skip optimization if no constraints
            if len(system.constraints) == 0:
                print(f"⚠️  No constraints initialized, skipping optimization...")
                results[geo.value] = {
                    "error": "No constraints initialized",
                    "triad": spec.triad
                }
                continue
            
            # Optimize
            print(f"→ Optimizing node positions...")
            opt = system.optimize_node_positions(max_iterations=20, learning_rate=0.02)
            
            print(f"   Iterations: {opt['iterations']}")
            print(f"   Converged: {opt['converged']}")
            print(f"   Final violation: {opt['final_violation']:.6e}")
            print(f"   Improvement: {opt['improvement']:.6e}")
            
            # Analyze
            print(f"→ Analyzing interaction patterns...")
            analysis = system.analyze_interaction_patterns()
            
            # Compute metrics
            sat_rate = analysis['constraint_satisfaction']['satisfaction_rate']
            avg_coherence = analysis['average_coherence']
            
            # NRCI proxy: weighted combination of constraint satisfaction and coherence
            nrci_proxy = 0.6 * sat_rate + 0.4 * avg_coherence
            
            # Record results
            results[geo.value] = {
                "triad": spec.triad,
                "final_violation": float(opt['final_violation']),
                "improvement": float(opt['improvement']),
                "iterations": opt['iterations'],
                "constraint_satisfaction_rate": float(sat_rate),
                "avg_coherence": float(avg_coherence),
                "nrci_proxy": round(nrci_proxy, 6),
                "interactions_used": list(analysis['interaction_type_counts'].keys())[:3],
                "converged": opt['converged'],
                "coherence_threshold": spec.coherence_threshold,
                "description": spec.description
            }
            
            print(f"\n✅ Results:")
            print(f"   NRCI proxy: {nrci_proxy:.6f}")
            print(f"   Constraint satisfaction: {sat_rate:.3f}")
            print(f"   Average coherence: {avg_coherence:.3f}")
            
            # Save baseline (dodecahedral)
            if geo == TGICGeometry.DODECAHEDRAL:
                baseline_nrci = nrci_proxy
                print(f"   📌 Baseline set: {baseline_nrci:.6f}")
                
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            results[geo.value] = {
                "error": str(e),
                "triad": spec.triad if spec else None
            }
    
    # Cross-consistency check
    print(f"\n{'='*70}")
    print(f"🔍 CROSS-GEOMETRY CONSISTENCY CHECK")
    print(f"={'='*70}")
    
    if baseline_nrci:
        consistency_score = 0.0
        count = 0
        
        for geo_name, res in results.items():
            if 'nrci_proxy' in res:
                delta = abs(res['nrci_proxy'] - baseline_nrci)
                weight = 1.0 if geo_name == 'dodecahedral' else 0.8
                # Clamp delta at 5% for scoring
                consistency_score += weight * (1.0 - min(delta, 0.05)/0.05)
                count += weight
                
                print(f"{geo_name:15} | NRCI: {res['nrci_proxy']:.6f} | "
                      f"Δ from baseline: {delta:+.6f}")
        
        consistency = consistency_score / count if count else 0.0
        print(f"\nConsistency score (vs dodecahedral): {consistency:.6f}")
        
        results['_meta'] = {
            "baseline_nrci": round(baseline_nrci, 6),
            "cross_consistency": round(consistency, 6),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ubp_version": "3.7.1",
            "concept_by": "Qwen AI"
        }
    else:
        print("⚠️  No baseline NRCI available (dodecahedral failed)")
        results['_meta'] = {
            "error": "No baseline available",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ubp_version": "3.7.1"
        }
    
    # Save full report
    report_path = os.path.join(os.path.dirname(__file__), "cross_geometry_report.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Full report saved to: {report_path}")
    
    # Human-readable summary
    print(f"\n{'='*70}")
    print(f"📊 SUMMARY")
    print(f"{'='*70}")
    
    for geo_name, res in results.items():
        if geo_name.startswith('_'):
            continue
        
        if 'nrci_proxy' in res:
            nrci = res['nrci_proxy']
            status = "🟢" if nrci >= 0.95 else "🟡" if nrci >= 0.90 else "🔴"
            print(f"{status} {geo_name:15} | {nrci:.6f} | {res['triad']}")
        elif 'error' in res:
            print(f"❌ {geo_name:15} | ERROR: {res['error'][:40]}...")
    
    # Recommendations
    print(f"\n{'='*70}")
    print(f"🎯 RECOMMENDATIONS")
    print(f"{'='*70}")
    
    if baseline_nrci and results.get('dodecahedral', {}).get('nrci_proxy', 0) >= 0.95:
        print("→ Dodecahedral remains optimal for proof substrate.")
        
        tetra_nrci = results.get('tetrahedral', {}).get('nrci_proxy', 0)
        if tetra_nrci >= 0.90:
            print("→ Tetrahedral recommended for lemma induction.")
        
        leech_nrci = results.get('leech_24d', {}).get('nrci_proxy', 0)
        if leech_nrci >= 0.97:
            print("→ Leech_24D for cosmological deep-coherence embedding.")
        
        if results.get('_meta', {}).get('cross_consistency', 0) >= 0.99:
            print("\n✅ Cross-consistency ≥ 0.99: Geometric relativity validated!")
        else:
            print(f"\n⚠️  Cross-consistency < 0.99: Review constraint initializers")
    else:
        print("⚠️  Dodecahedral NRCI below 0.95 - review constraint implementation")
    
    print(f"\n{'='*70}")
    
    return results


if __name__ == "__main__":
    results = run_cross_geometry_test()
