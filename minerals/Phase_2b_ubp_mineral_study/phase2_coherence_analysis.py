#!/usr/bin/env python3.11
"""
Phase 2: UBP Coherence Analysis on 3,112 Minerals
Uses the aggressive v3.1 calibration from Phase 1
"""

import json
import sys
from pathlib import Path
from coherence_substrate_v2 import CoherenceState, Y
import time

# Import hex dictionary for persistence
from hex_dictionary import HexDictionary

# Calibration parameters (from v3.1 aggressive)
BASE_DEGRADATION_PER_Z = 0.001  # 10x stronger than v2
TGIC_PENALTY_MULTIPLIER = 0.01  # 10x stronger than v2
NRCI_THRESHOLD = 0.9995

def calculate_tgic(element_count):
    """Calculate Topological-Geometric Information Complexity"""
    if element_count <= 1:
        return 0.0
    # Logarithmic scaling: more elements = exponentially harder to organize
    import math
    return math.log(element_count)

def calculate_nrci(mineral):
    """
    Calculate Net Refined Coherence Index (NRCI) for a mineral
    
    NRCI = base_coherence - degradation + refinements
    
    where:
    - base_coherence = 1.0 (perfect initial state)
    - degradation = f(Z, symmetry, complexity)
    - refinements = g(symmetry)
    """
    name = mineral['name']
    Z = mineral['Z_max']
    symmetry = mineral['symmetry_operations']
    element_count = mineral['element_count']
    
    # Calculate degradation
    z_degradation = Z * BASE_DEGRADATION_PER_Z
    tgic = calculate_tgic(element_count)
    tgic_penalty = (1 - (symmetry / 48)) * tgic * TGIC_PENALTY_MULTIPLIER
    total_degradation = z_degradation + tgic_penalty
    
    # Calculate refinements (Y-operations)
    # Higher symmetry = more refinement opportunities
    refinement_factor = symmetry / 48  # Normalize to [0, 1]
    num_refinements = int(refinement_factor * 10)  # 0-10 refinements
    
    # Create CoherenceState and perform refinements
    state = CoherenceState(1.0)
    
    for _ in range(num_refinements):
        state = state.refine_forward()
    
    # Calculate NRCI
    nrci = float(state.value) - total_degradation
    
    # Store operation count (simplified history)
    operation_count = len(state.history.operations) if hasattr(state, 'history') and hasattr(state.history, 'operations') else num_refinements
    
    return {
        'nrci': nrci,
        'degradation': total_degradation,
        'z_degradation': z_degradation,
        'tgic_penalty': tgic_penalty,
        'tgic': tgic,
        'refinements': num_refinements,
        'operation_count': operation_count,
        'final_coherence': float(state.value),
        'passes': nrci >= NRCI_THRESHOLD
    }

def main():
    print("="*80)
    print("PHASE 2: UBP COHERENCE ANALYSIS - 3,112 MINERALS")
    print("="*80)
    print(f"Model: v3.1 Aggressive")
    print(f"Base degradation: {BASE_DEGRADATION_PER_Z} per Z")
    print(f"TGIC multiplier: {TGIC_PENALTY_MULTIPLIER}")
    print(f"NRCI threshold: {NRCI_THRESHOLD}")
    print("="*80)
    
    # Load processed minerals
    print("\n[1/4] Loading processed mineral dataset...")
    with open('data/minerals_processed_3112.json', 'r') as f:
        minerals = json.load(f)
    print(f"   Loaded {len(minerals)} minerals")
    
    # Analyze each mineral
    print("\n[2/4] Running coherence analysis...")
    results = []
    start_time = time.time()
    
    for i, mineral in enumerate(minerals):
        if (i + 1) % 500 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(minerals) - i - 1) / rate
            print(f"   Progress: {i+1}/{len(minerals)} ({(i+1)/len(minerals)*100:.1f}%) - {rate:.1f} minerals/sec - ETA: {remaining:.0f}s")
        
        analysis = calculate_nrci(mineral)
        result = {
            **mineral,
            **analysis
        }
        results.append(result)
    
    elapsed = time.time() - start_time
    print(f"   ✓ Completed in {elapsed:.2f}s ({len(minerals)/elapsed:.1f} minerals/sec)")
    
    # Calculate statistics
    print("\n[3/4] Calculating statistics...")
    passed = [r for r in results if r['passes']]
    failed = [r for r in results if not r['passes']]
    
    print(f"\n   OVERALL RESULTS:")
    print(f"   ================")
    print(f"   Total minerals: {len(results)}")
    print(f"   Passed: {len(passed)} ({len(passed)/len(results)*100:.2f}%)")
    print(f"   Failed: {len(failed)} ({len(failed)/len(results)*100:.2f}%)")
    
    # By crystal system
    print(f"\n   BY CRYSTAL SYSTEM:")
    print(f"   ==================")
    crystal_systems = set(r['crystal_system'] for r in results)
    for system in sorted(crystal_systems):
        system_results = [r for r in results if r['crystal_system'] == system]
        system_passed = [r for r in system_results if r['passes']]
        print(f"   {system:15s}: {len(system_passed):4d}/{len(system_results):4d} passed ({len(system_passed)/len(system_results)*100:5.2f}%)")
    
    # By symmetry
    print(f"\n   BY SYMMETRY OPERATIONS:")
    print(f"   =======================")
    symmetries = sorted(set(r['symmetry_operations'] for r in results))
    for sym in symmetries:
        sym_results = [r for r in results if r['symmetry_operations'] == sym]
        sym_passed = [r for r in sym_results if r['passes']]
        print(f"   {sym:2d} operations: {len(sym_passed):4d}/{len(sym_results):4d} passed ({len(sym_passed)/len(sym_results)*100:5.2f}%)")
    
    # By Z range
    print(f"\n   BY Z RANGE:")
    print(f"   ===========")
    z_ranges = [(1, 30), (30, 50), (50, 80), (80, 92)]
    for z_min, z_max in z_ranges:
        z_results = [r for r in results if z_min <= r['Z_max'] < z_max]
        z_passed = [r for r in z_results if r['passes']]
        if z_results:
            print(f"   Z={z_min:2d}-{z_max:2d}: {len(z_passed):4d}/{len(z_results):4d} passed ({len(z_passed)/len(z_results)*100:5.2f}%)")
    
    # Top 10 best and worst
    print(f"\n   TOP 10 HIGHEST NRCI (BEST):")
    print(f"   ===========================")
    sorted_results = sorted(results, key=lambda r: r['nrci'], reverse=True)
    for i, r in enumerate(sorted_results[:10]):
        print(f"   {i+1:2d}. {r['name']:30s} NRCI={r['nrci']:.6f} Z={r['Z_max']:2d} sym={r['symmetry_operations']:2d} {'✓' if r['passes'] else '✗'}")
    
    print(f"\n   TOP 10 LOWEST NRCI (WORST):")
    print(f"   ===========================")
    for i, r in enumerate(sorted_results[-10:]):
        print(f"   {i+1:2d}. {r['name']:30s} NRCI={r['nrci']:.6f} Z={r['Z_max']:2d} sym={r['symmetry_operations']:2d} {'✓' if r['passes'] else '✗'}")
    
    # Save results
    print("\n[4/4] Saving results...")
    output_file = 'results/phase2_coherence_analysis_3112.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"   ✓ Saved to {output_file}")
    
    # Save summary
    summary = {
        'total_minerals': len(results),
        'passed': len(passed),
        'failed': len(failed),
        'pass_rate': len(passed) / len(results),
        'by_crystal_system': {},
        'by_symmetry': {},
        'by_z_range': {},
        'calibration': {
            'base_degradation_per_z': BASE_DEGRADATION_PER_Z,
            'tgic_multiplier': TGIC_PENALTY_MULTIPLIER,
            'nrci_threshold': NRCI_THRESHOLD
        }
    }
    
    for system in sorted(crystal_systems):
        system_results = [r for r in results if r['crystal_system'] == system]
        system_passed = [r for r in system_results if r['passes']]
        summary['by_crystal_system'][system] = {
            'total': len(system_results),
            'passed': len(system_passed),
            'pass_rate': len(system_passed) / len(system_results) if system_results else 0
        }
    
    for sym in symmetries:
        sym_results = [r for r in results if r['symmetry_operations'] == sym]
        sym_passed = [r for r in sym_results if r['passes']]
        summary['by_symmetry'][sym] = {
            'total': len(sym_results),
            'passed': len(sym_passed),
            'pass_rate': len(sym_passed) / len(sym_results) if sym_results else 0
        }
    
    for z_min, z_max in z_ranges:
        z_results = [r for r in results if z_min <= r['Z_max'] < z_max]
        z_passed = [r for r in z_results if r['passes']]
        summary['by_z_range'][f'{z_min}-{z_max}'] = {
            'total': len(z_results),
            'passed': len(z_passed),
            'pass_rate': len(z_passed) / len(z_results) if z_results else 0
        }
    
    summary_file = 'results/phase2_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"   ✓ Saved summary to {summary_file}")
    
    print("\n" + "="*80)
    print("PHASE 2 COHERENCE ANALYSIS COMPLETE!")
    print("="*80)

if __name__ == '__main__':
    main()
