"""
Cluster Minerals in Hex Space via Jaccard Distance - v2
========================================================

Working directly with hex addresses from results.
Using HexDictionaryPure for distance calculations.
"""

import json
import ast
from collections import defaultdict
from typing import Set

# Import hex dictionary
import sys
sys.path.insert(0, '/home/ubuntu/ubp_mineral_study')
from hex_dictionary_pure import HexDictionaryPure

# Load v3.1 results
with open('/home/ubuntu/ubp_mineral_study/results/mineral_coherence_v3_1_aggressive.json', 'r') as f:
    data = json.load(f)

results = data['results']

print("=" * 80)
print("HEX SPACE CLUSTERING: MINERAL INFORMATION TOPOLOGY")
print("=" * 80)
print()

# ============================================================================
# Parse hex addresses
# ============================================================================

minerals_with_hex = []
for r in results:
    hex_addr = r.get('hex_address', '')
    if hex_addr and hex_addr != 'not_persisted':
        # Try to parse the hex address as a set
        try:
            # Hex address should be a string representation of a set
            # Try to evaluate it safely
            if hex_addr.startswith('{') and hex_addr.endswith('}'):
                # Parse as set literal
                hex_set = ast.literal_eval(hex_addr)
                if isinstance(hex_set, set):
                    r['hex_set'] = hex_set
                    minerals_with_hex.append(r)
            else:
                # Treat as single element set
                r['hex_set'] = {hex_addr}
                minerals_with_hex.append(r)
        except:
            # If parsing fails, use the string itself as a single-element set
            r['hex_set'] = {hex_addr}
            minerals_with_hex.append(r)

print(f"Minerals with hex addresses: {len(minerals_with_hex)}/{len(results)}")
print()

if len(minerals_with_hex) == 0:
    print("ERROR: No minerals have valid hex addresses!")
    sys.exit(1)

# Show a few examples
print("Sample hex addresses:")
for r in minerals_with_hex[:5]:
    print(f"  {r['name']:25s}: {str(r['hex_set'])[:60]}...")
print()

# ============================================================================
# Calculate distance matrix using HexDictionaryPure
# ============================================================================

print("Calculating Jaccard distance matrix...")
hex_dict = HexDictionaryPure()

mineral_names = [r['name'] for r in minerals_with_hex]
hex_sets = [r['hex_set'] for r in minerals_with_hex]

# Use the built-in distance matrix computation
distance_result = hex_dict.compute_distance_matrix(hex_sets, labels=mineral_names)

distances_dict = distance_result['distances']
print(f"Calculated {len(distances_dict)} pairwise distances")
print()

# ============================================================================
# Find closest pairs
# ============================================================================

print("=" * 80)
print("CLOSEST MINERAL PAIRS (Most informationally similar)")
print("=" * 80)
print()

# Convert to list and sort
distance_list = [(k, v) for k, v in distances_dict.items()]
sorted_pairs = sorted(distance_list, key=lambda x: x[1])

# Create name lookup
name_to_result = {r['name']: r for r in minerals_with_hex}

shown = 0
for (name1, name2), dist in sorted_pairs:
    if shown >= 20:
        break
    if dist < 1.0:  # Only show non-maximum distances
        r1 = name_to_result[name1]
        r2 = name_to_result[name2]
        
        print(f"Distance: {dist:.4f}")
        print(f"  {name1:30s} (Z={r1['Z']:2d}, {r1['crystal_system']:12s}, NRCI={r1['final_nrci']:.6f})")
        print(f"  {name2:30s} (Z={r2['Z']:2d}, {r2['crystal_system']:12s}, NRCI={r2['final_nrci']:.6f})")
        print()
        shown += 1

if shown == 0:
    print("All minerals are maximally distant (distance = 1.0)")
    print("This means all hex addresses are completely disjoint!")
    print()

# ============================================================================
# Analyze by pass/fail
# ============================================================================

print("=" * 80)
print("CLUSTERING BY PASS/FAIL STATUS")
print("=" * 80)
print()

passed_minerals = [r for r in minerals_with_hex if r['passes_natural']]
failed_minerals = [r for r in minerals_with_hex if not r['passes_natural']]

print(f"Passed minerals: {len(passed_minerals)}")
print(f"Failed minerals: {len(failed_minerals)}")
print()

# Calculate average intra-cluster distances
passed_names = [r['name'] for r in passed_minerals]
failed_names = [r['name'] for r in failed_minerals]

intra_passed_dists = []
for i, name1 in enumerate(passed_names):
    for name2 in passed_names[i+1:]:
        key = (name1, name2) if (name1, name2) in distances_dict else (name2, name1)
        if key in distances_dict:
            intra_passed_dists.append(distances_dict[key])

intra_failed_dists = []
for i, name1 in enumerate(failed_names):
    for name2 in failed_names[i+1:]:
        key = (name1, name2) if (name1, name2) in distances_dict else (name2, name1)
        if key in distances_dict:
            intra_failed_dists.append(distances_dict[key])

inter_dists = []
for name1 in passed_names:
    for name2 in failed_names:
        key = (name1, name2) if (name1, name2) in distances_dict else (name2, name1)
        if key in distances_dict:
            inter_dists.append(distances_dict[key])

if intra_passed_dists:
    avg_intra_passed = sum(intra_passed_dists) / len(intra_passed_dists)
    print(f"Average distance within PASSED cluster: {avg_intra_passed:.4f}")

if intra_failed_dists:
    avg_intra_failed = sum(intra_failed_dists) / len(intra_failed_dists)
    print(f"Average distance within FAILED cluster: {avg_intra_failed:.4f}")

if inter_dists:
    avg_inter = sum(inter_dists) / len(inter_dists)
    print(f"Average distance between PASSED and FAILED: {avg_inter:.4f}")

print()

# ============================================================================
# Find "orphan" minerals (most informationally unique)
# ============================================================================

print("=" * 80)
print("ORPHAN MINERALS (Most informationally unique)")
print("=" * 80)
print()

# For each mineral, calculate average distance to all others
avg_distances = {}
for name in mineral_names:
    dists = []
    for other_name in mineral_names:
        if name != other_name:
            key = (name, other_name) if (name, other_name) in distances_dict else (other_name, name)
            if key in distances_dict:
                dists.append(distances_dict[key])
    
    if dists:
        avg_distances[name] = sum(dists) / len(dists)

# Sort by average distance (highest = most unique)
sorted_by_uniqueness = sorted(avg_distances.items(), key=lambda x: -x[1])

print("Most unique minerals (highest average distance to all others):")
for name, avg_dist in sorted_by_uniqueness[:10]:
    r = name_to_result[name]
    status = "PASSED" if r['passes_natural'] else "FAILED"
    print(f"  {name:30s} (Z={r['Z']:2d}, {r['crystal_system']:12s}, avg_dist={avg_dist:.4f}) [{status}]")

print()

print("Least unique minerals (lowest average distance to all others):")
for name, avg_dist in sorted_by_uniqueness[-10:]:
    r = name_to_result[name]
    status = "PASSED" if r['passes_natural'] else "FAILED"
    print(f"  {name:30s} (Z={r['Z']:2d}, {r['crystal_system']:12s}, avg_dist={avg_dist:.4f}) [{status}]")

print()

# ============================================================================
# Analyze hex address patterns
# ============================================================================

print("=" * 80)
print("HEX ADDRESS ANALYSIS")
print("=" * 80)
print()

# Count unique hex addresses
unique_addresses = set(str(r['hex_set']) for r in minerals_with_hex)
print(f"Unique hex addresses: {len(unique_addresses)}")
print(f"Total minerals: {len(minerals_with_hex)}")

if len(unique_addresses) < len(minerals_with_hex):
    collision_rate = (1 - len(unique_addresses)/len(minerals_with_hex))*100
    print(f"Collision rate: {collision_rate:.1f}%")
else:
    print("No collisions - all minerals have unique hex addresses")

print()

# Analyze hex set sizes
hex_sizes = [len(r['hex_set']) for r in minerals_with_hex]
print(f"Hex set size statistics:")
print(f"  Min: {min(hex_sizes)}")
print(f"  Max: {max(hex_sizes)}")
print(f"  Average: {sum(hex_sizes)/len(hex_sizes):.2f}")
print()

# Group by hex set size
by_size = defaultdict(list)
for r in minerals_with_hex:
    by_size[len(r['hex_set'])].append(r)

print("Distribution by hex set size:")
for size in sorted(by_size.keys()):
    minerals = by_size[size]
    passed = sum(1 for m in minerals if m['passes_natural'])
    print(f"  Size {size:3d}: {len(minerals):2d} minerals ({passed:2d} passed, {len(minerals)-passed:2d} failed)")

print()

# ============================================================================
# Key insights
# ============================================================================

print("=" * 80)
print("KEY INSIGHTS FROM HEX SPACE CLUSTERING")
print("=" * 80)
print()

print("1. INFORMATION TOPOLOGY")
if len(unique_addresses) == len(minerals_with_hex):
    print("   ✓ Every mineral has a unique hex address")
    print("   ✓ No computational collisions - each lineage is distinct")
else:
    print(f"   ⚠ {len(minerals_with_hex) - len(unique_addresses)} collisions found")
print()

print("2. PASS/FAIL CLUSTERING")
if intra_passed_dists and intra_failed_dists and inter_dists:
    if avg_inter > max(avg_intra_passed, avg_intra_failed):
        print("   ✓ PASSED and FAILED minerals form SEPARATE clusters")
        print(f"   ✓ Inter-cluster distance ({avg_inter:.4f}) > intra-cluster ({max(avg_intra_passed, avg_intra_failed):.4f})")
    else:
        print("   ✓ PASSED and FAILED minerals are INTERMIXED")
        print(f"   ✓ Inter-cluster distance ({avg_inter:.4f}) ≤ intra-cluster")
print()

print("3. INFORMATION UNIQUENESS")
if avg_distances:
    max_avg_dist = max(avg_distances.values())
    min_avg_dist = min(avg_distances.values())
    print(f"   Average distance range: {min_avg_dist:.4f} to {max_avg_dist:.4f}")
    if max_avg_dist > 0.9:
        print("   ✓ Some minerals are highly unique (avg dist > 0.9)")
    if min_avg_dist < 0.5:
        print("   ✓ Some minerals cluster tightly (avg dist < 0.5)")
print()

print("4. HEX SET SIZE PATTERNS")
print(f"   Hex sets range from {min(hex_sizes)} to {max(hex_sizes)} elements")
print(f"   Average size: {sum(hex_sizes)/len(hex_sizes):.2f}")
if len(by_size) > 1:
    print("   Different minerals have different computational complexity")
print()

# Save clustering analysis
clustering_data = {
    'total_minerals': len(minerals_with_hex),
    'unique_hex_addresses': len(unique_addresses),
    'passed_count': len(passed_minerals),
    'failed_count': len(failed_minerals),
    'average_distances': {
        'intra_passed': avg_intra_passed if intra_passed_dists else None,
        'intra_failed': avg_intra_failed if intra_failed_dists else None,
        'inter_cluster': avg_inter if inter_dists else None
    },
    'hex_set_size_stats': {
        'min': min(hex_sizes),
        'max': max(hex_sizes),
        'average': sum(hex_sizes)/len(hex_sizes)
    },
    'most_unique': [
        {
            'name': name,
            'avg_distance': avg_dist,
            'Z': name_to_result[name]['Z'],
            'crystal_system': name_to_result[name]['crystal_system'],
            'passes': name_to_result[name]['passes_natural']
        }
        for name, avg_dist in sorted_by_uniqueness[:10]
    ]
}

with open('/home/ubuntu/ubp_mineral_study/results/hex_clustering_analysis.json', 'w') as f:
    json.dump(clustering_data, f, indent=2)

print("Clustering analysis saved to hex_clustering_analysis.json")
