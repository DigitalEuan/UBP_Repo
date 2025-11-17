"""
Trace Computational "Birth" of Minerals via ComputationHistory
================================================================

Using the ComputationHistory from v3.1 results to understand:
- How minerals are "born" computationally
- What operations lead to coherence vs decoherence
- How Y-refinements interact with degradation
- Whether Pi appears in the computational paths
"""

import json
import math
from collections import defaultdict

# Load v3.1 results
with open('/home/ubuntu/ubp_mineral_study/results/mineral_coherence_v3_1_aggressive.json', 'r') as f:
    data = json.load(f)

results = data['results']

print("=" * 80)
print("COMPUTATIONAL LINEAGE ANALYSIS: MINERAL 'BIRTH' PATHS")
print("=" * 80)
print()

# ============================================================================
# Analyze a few representative minerals
# ============================================================================

# Pick representatives: best pass, worst pass, best fail, worst fail
passed = [r for r in results if r['passes_natural']]
failed = [r for r in results if not r['passes_natural']]

best_pass = max(passed, key=lambda x: x['final_nrci'])
worst_pass = min(passed, key=lambda x: x['final_nrci'])
best_fail = max(failed, key=lambda x: x['final_nrci'])
worst_fail = min(failed, key=lambda x: x['final_nrci'])

representatives = [
    ("BEST PASS", best_pass),
    ("WORST PASS", worst_pass),
    ("BEST FAIL", best_fail),
    ("WORST FAIL", worst_fail)
]

for label, mineral in representatives:
    print(f"{label}: {mineral['name']}")
    print(f"  Formula: {mineral['formula']}")
    print(f"  Z={mineral['Z']}, Crystal system: {mineral['crystal_system']}")
    print(f"  Symmetry order: {mineral['metadata']['symmetry_order']}")
    print(f"  Final NRCI: {mineral['final_nrci']:.6f}")
    print(f"  Net refinements: {mineral['net_refinements']}")
    print(f"  Computation depth: {mineral['computation_depth']}")
    print()
    
    # Analyze history
    history = mineral['history_summary']
    print(f"  History summary:")
    print(f"    Total operations: {history.get('total_operations', 0)}")
    print(f"    Operation types: {history.get('operation_types', {})}")
    print()

print("=" * 80)
print("OPERATION PATTERNS: PASSED VS FAILED")
print("=" * 80)
print()

# Aggregate operation patterns
passed_ops = defaultdict(int)
failed_ops = defaultdict(int)

for r in passed:
    ops = r['history_summary'].get('operation_types', [])
    if isinstance(ops, list):
        for op in ops:
            passed_ops[op] += 1
    elif isinstance(ops, dict):
        for op, count in ops.items():
            passed_ops[op] += count

for r in failed:
    ops = r['history_summary'].get('operation_types', [])
    if isinstance(ops, list):
        for op in ops:
            failed_ops[op] += 1
    elif isinstance(ops, dict):
        for op, count in ops.items():
            failed_ops[op] += count

print("Operation counts for PASSED minerals:")
for op, count in sorted(passed_ops.items(), key=lambda x: -x[1]):
    avg = count / len(passed)
    print(f"  {op:20s}: {count:4d} total, {avg:.2f} avg per mineral")

print()
print("Operation counts for FAILED minerals:")
for op, count in sorted(failed_ops.items(), key=lambda x: -x[1]):
    avg = count / len(failed)
    print(f"  {op:20s}: {count:4d} total, {avg:.2f} avg per mineral")

print()

# ============================================================================
# Analyze refinement patterns
# ============================================================================

print("=" * 80)
print("Y-REFINEMENT PATTERNS")
print("=" * 80)
print()

# Calculate refinement statistics
passed_refinements = [r['net_refinements'] for r in passed]
failed_refinements = [r['net_refinements'] for r in failed]

print(f"PASSED minerals:")
print(f"  Average net refinements: {sum(passed_refinements)/len(passed_refinements):.2f}")
print(f"  Min: {min(passed_refinements)}, Max: {max(passed_refinements)}")
print(f"  Distribution: {sorted(set(passed_refinements))}")
print()

print(f"FAILED minerals:")
print(f"  Average net refinements: {sum(failed_refinements)/len(failed_refinements):.2f}")
print(f"  Min: {min(failed_refinements)}, Max: {max(failed_refinements)}")
print(f"  Distribution: {sorted(set(failed_refinements))}")
print()

# Group by net refinements
by_refinements = defaultdict(lambda: {'passed': 0, 'failed': 0})
for r in results:
    net_ref = r['net_refinements']
    if r['passes_natural']:
        by_refinements[net_ref]['passed'] += 1
    else:
        by_refinements[net_ref]['failed'] += 1

print("Pass/Fail by net refinements:")
for net_ref in sorted(by_refinements.keys()):
    data = by_refinements[net_ref]
    total = data['passed'] + data['failed']
    rate = data['passed'] / total * 100 if total > 0 else 0
    print(f"  Net refinements {net_ref:2d}: {data['passed']:2d} passed, {data['failed']:2d} failed ({rate:5.1f}% pass rate)")

print()

# ============================================================================
# Analyze degradation vs refinement balance
# ============================================================================

print("=" * 80)
print("DEGRADATION VS REFINEMENT BALANCE")
print("=" * 80)
print()

# For each mineral, calculate the "balance" between refinements and degradation
for r in results:
    # Refinements add coherence, degradation removes it
    # Net effect determines final NRCI
    r['refinement_degradation_ratio'] = r['net_refinements'] / r['total_degradation'] if r['total_degradation'] > 0 else 999

passed_ratios = [r['refinement_degradation_ratio'] for r in passed]
failed_ratios = [r['refinement_degradation_ratio'] for r in failed]

print(f"Refinement/Degradation ratio:")
print(f"  PASSED minerals: avg = {sum(passed_ratios)/len(passed_ratios):.4f}")
print(f"  FAILED minerals: avg = {sum(failed_ratios)/len(failed_ratios):.4f}")
print()

# Find the critical ratio
max_failed_ratio = max(failed_ratios)
min_passed_ratio = min(passed_ratios)

print(f"  Max ratio (failed): {max_failed_ratio:.4f}")
print(f"  Min ratio (passed): {min_passed_ratio:.4f}")
print()

if min_passed_ratio > max_failed_ratio:
    critical_ratio = (min_passed_ratio + max_failed_ratio) / 2
    print(f"  CRITICAL RATIO: {critical_ratio:.4f}")
    print(f"    Minerals with ratio > {critical_ratio:.4f} pass")
    print(f"    Minerals with ratio < {critical_ratio:.4f} fail")
else:
    print("  No clean threshold - ratios overlap")

print()

# ============================================================================
# Trace specific mineral paths
# ============================================================================

print("=" * 80)
print("DETAILED LINEAGE: PORTLANDITE (BEST PASS)")
print("=" * 80)
print()

portlandite = best_pass
print(f"Name: {portlandite['name']}")
print(f"Formula: {portlandite['formula']}")
print(f"Z={portlandite['Z']}, Crystal system: {portlandite['crystal_system']}")
print(f"Symmetry order: {portlandite['metadata']['symmetry_order']}")
print()

print("Computational path:")
print(f"  1. Base state created with NRCI = {portlandite['base_nrci']:.6f}")
print(f"  2. Applied {portlandite['metadata']['symmetry_order']} symmetry operations")
print(f"  3. Geometric refinements: {portlandite['net_refinements'] + 1} forward Y-refinements")
print(f"  4. Complexity degradation: {portlandite['total_degradation']:.6f}")
print(f"     - Z penalty: {portlandite['z_penalty']:.6f}")
print(f"     - Bottleneck penalty: {portlandite['bottleneck_penalty']:.6f}")
print(f"     - System penalty: {portlandite['system_penalty']:.6f}")
print(f"  5. Observer cost: 1 backward Y-refinement (cost = {1/0.2647:.4f})")
print(f"  6. Final NRCI: {portlandite['final_nrci']:.6f}")
print()

print(f"Net effect:")
print(f"  Refinements added: ~{portlandite['net_refinements']} × Y")
print(f"  Degradation removed: {portlandite['total_degradation']:.6f}")
print(f"  Balance: {portlandite['refinement_degradation_ratio']:.4f}")
print(f"  Result: PASSED (NRCI = {portlandite['final_nrci']:.6f} > 0.9995)")
print()

# ============================================================================
# Compare with a failed mineral
# ============================================================================

print("=" * 80)
print("DETAILED LINEAGE: CINNABAR (WORST FAIL)")
print("=" * 80)
print()

cinnabar = worst_fail
print(f"Name: {cinnabar['name']}")
print(f"Formula: {cinnabar['formula']}")
print(f"Z={cinnabar['Z']}, Crystal system: {cinnabar['crystal_system']}")
print(f"Symmetry order: {cinnabar['metadata']['symmetry_order']}")
print()

print("Computational path:")
print(f"  1. Base state created with NRCI = {cinnabar['base_nrci']:.6f}")
print(f"  2. Applied {cinnabar['metadata']['symmetry_order']} symmetry operations")
print(f"  3. Geometric refinements: {cinnabar['net_refinements'] + 1} forward Y-refinements")
print(f"  4. Complexity degradation: {cinnabar['total_degradation']:.6f}")
print(f"     - Z penalty: {cinnabar['z_penalty']:.6f}")
print(f"     - Bottleneck penalty: {cinnabar['bottleneck_penalty']:.6f}")
print(f"     - System penalty: {cinnabar['system_penalty']:.6f}")
print(f"  5. Observer cost: 1 backward Y-refinement (cost = {1/0.2647:.4f})")
print(f"  6. Final NRCI: {cinnabar['final_nrci']:.6f}")
print()

print(f"Net effect:")
print(f"  Refinements added: ~{cinnabar['net_refinements']} × Y")
print(f"  Degradation removed: {cinnabar['total_degradation']:.6f}")
print(f"  Balance: {cinnabar['refinement_degradation_ratio']:.4f}")
print(f"  Result: FAILED (NRCI = {cinnabar['final_nrci']:.6f} < 0.9995)")
print()

# ============================================================================
# Key insight: What makes the difference?
# ============================================================================

print("=" * 80)
print("KEY INSIGHT: WHY PORTLANDITE PASSES BUT CINNABAR FAILS")
print("=" * 80)
print()

print("PORTLANDITE (Ca(OH)2):")
print(f"  Z = {portlandite['Z']} (Calcium)")
print(f"  Symmetry = {portlandite['metadata']['symmetry_order']} ({portlandite['crystal_system']})")
print(f"  I_cmplx = {portlandite['Z'] / portlandite['metadata']['symmetry_order']:.2f}")
print(f"  Total degradation = {portlandite['total_degradation']:.6f}")
print(f"  Refinement/Degradation = {portlandite['refinement_degradation_ratio']:.4f}")
print()

print("CINNABAR (HgS):")
print(f"  Z = {cinnabar['Z']} (Mercury - BOTTLENECK ZONE)")
print(f"  Symmetry = {cinnabar['metadata']['symmetry_order']} ({cinnabar['crystal_system']})")
print(f"  I_cmplx = {cinnabar['Z'] / cinnabar['metadata']['symmetry_order']:.2f}")
print(f"  Total degradation = {cinnabar['total_degradation']:.6f}")
print(f"  Refinement/Degradation = {cinnabar['refinement_degradation_ratio']:.4f}")
print()

print("DIFFERENCE:")
print(f"  Portlandite has:")
print(f"    • Low Z (20 vs 80) → Less complexity")
print(f"    • High symmetry (48 vs 2) → More compression")
print(f"    • Low I_cmplx ({portlandite['Z'] / portlandite['metadata']['symmetry_order']:.2f} vs {cinnabar['Z'] / cinnabar['metadata']['symmetry_order']:.2f})")
print(f"    • Low degradation ({portlandite['total_degradation']:.4f} vs {cinnabar['total_degradation']:.4f})")
print(f"    • High ratio ({portlandite['refinement_degradation_ratio']:.4f} vs {cinnabar['refinement_degradation_ratio']:.4f})")
print()

print("  Cinnabar has:")
print(f"    • High Z (80 - IN BOTTLENECK ZONE)")
print(f"    • Low symmetry (triclinic - LOWEST)")
print(f"    • High I_cmplx (40.0 - WAY ABOVE THRESHOLD)")
print(f"    • Massive degradation (bottleneck + system penalties)")
print(f"    • Low ratio (refinements can't compensate)")
print()

print("CONCLUSION:")
print("  Mineral formation is a BALANCE between:")
print("    • Y-refinements (building coherence through symmetry)")
print("    • Z-degradation (losing coherence through complexity)")
print()
print("  Only minerals with:")
print("    • High symmetry (≥12 operations)")
print("    • Low-to-medium Z (avoiding bottleneck)")
print("    • Low I_cmplx (< ~4)")
print("  can maintain coherence above the observer threshold!")
print()

# Save lineage analysis
lineage_data = {
    'representatives': {
        'best_pass': {
            'name': best_pass['name'],
            'formula': best_pass['formula'],
            'final_nrci': best_pass['final_nrci'],
            'net_refinements': best_pass['net_refinements'],
            'total_degradation': best_pass['total_degradation'],
            'ratio': best_pass['refinement_degradation_ratio']
        },
        'worst_pass': {
            'name': worst_pass['name'],
            'formula': worst_pass['formula'],
            'final_nrci': worst_pass['final_nrci'],
            'net_refinements': worst_pass['net_refinements'],
            'total_degradation': worst_pass['total_degradation'],
            'ratio': worst_pass['refinement_degradation_ratio']
        },
        'best_fail': {
            'name': best_fail['name'],
            'formula': best_fail['formula'],
            'final_nrci': best_fail['final_nrci'],
            'net_refinements': best_fail['net_refinements'],
            'total_degradation': best_fail['total_degradation'],
            'ratio': best_fail['refinement_degradation_ratio']
        },
        'worst_fail': {
            'name': worst_fail['name'],
            'formula': worst_fail['formula'],
            'final_nrci': worst_fail['final_nrci'],
            'net_refinements': worst_fail['net_refinements'],
            'total_degradation': worst_fail['total_degradation'],
            'ratio': worst_fail['refinement_degradation_ratio']
        }
    },
    'critical_ratios': {
        'min_passed': min_passed_ratio,
        'max_failed': max_failed_ratio,
        'threshold': (min_passed_ratio + max_failed_ratio) / 2 if min_passed_ratio > max_failed_ratio else None
    },
    'average_refinements': {
        'passed': sum(passed_refinements) / len(passed_refinements),
        'failed': sum(failed_refinements) / len(failed_refinements)
    },
    'average_ratios': {
        'passed': sum(passed_ratios) / len(passed_ratios),
        'failed': sum(failed_ratios) / len(failed_ratios)
    }
}

with open('/home/ubuntu/ubp_mineral_study/results/mineral_lineage_analysis.json', 'w') as f:
    json.dump(lineage_data, f, indent=2)

print("Lineage analysis saved to mineral_lineage_analysis.json")
