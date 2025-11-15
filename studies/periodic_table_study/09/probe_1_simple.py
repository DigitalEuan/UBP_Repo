#!/usr/bin/env python3.11
"""
Probe 1 (Simplified): All 8 Blood Types as Toggle Sequences
Just track the toggle history and compute Jaccard distances
No complex error correction - focus on WHAT WE LEARN
"""
import sys
import json
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState

def main():
    print("\n" + "="*80)
    print("PROBE 1: ALL 8 BLOOD TYPES AS TOGGLE SEQUENCES (SIMPLIFIED)")
    print("="*80 + "\n")
    
    # Define all 8 blood types as toggle sets
    blood_types = {
        "O-": [],
        "O+": ["RhD"],
        "A-": ["A"],
        "A+": ["A", "RhD"],
        "B-": ["B"],
        "B+": ["B", "RhD"],
        "AB-": ["A", "B"],
        "AB+": ["A", "B", "RhD"]
    }
    
    print("Blood types as toggle sets:")
    for name, toggles in blood_types.items():
        print(f"  {name:4s}: {toggles if toggles else '(empty set)'}")
    
    # Compute Jaccard distance matrix
    print("\n" + "="*80)
    print("JACCARD DISTANCE MATRIX")
    print("="*80 + "\n")
    
    blood_type_names = list(blood_types.keys())
    
    # Header
    print(f"{'':6s}", end="")
    for name in blood_type_names:
        print(f"{name:8s}", end="")
    print()
    
    # Matrix
    jaccard_matrix = {}
    for name1 in blood_type_names:
        print(f"{name1:6s}", end="")
        jaccard_matrix[name1] = {}
        for name2 in blood_type_names:
            set1 = set(blood_types[name1])
            set2 = set(blood_types[name2])
            
            intersection = set1 & set2
            union = set1 | set2
            
            if len(union) == 0:
                jaccard_sim = 1.0  # Both empty = identical
            else:
                jaccard_sim = len(intersection) / len(union)
            
            dist = 1.0 - jaccard_sim
            jaccard_matrix[name1][name2] = dist
            print(f"{dist:8.4f}", end="")
        print()
    
    # Analysis
    print("\n" + "="*80)
    print("ANALYSIS: What Did We Learn?")
    print("="*80 + "\n")
    
    print("1. STRUCTURE:")
    print("   - 2^3 = 8 possible toggle combinations")
    print("   - 3 independent toggles: A, B, RhD")
    print("   - Each blood type = a unique subset of {A, B, RhD}")
    print()
    
    print("2. JACCARD PATTERNS:")
    pairs = []
    for i, name1 in enumerate(blood_type_names):
        for name2 in blood_type_names[i+1:]:
            dist = jaccard_matrix[name1][name2]
            set1 = set(blood_types[name1])
            set2 = set(blood_types[name2])
            shared = set1 & set2
            different = set1 ^ set2
            pairs.append((name1, name2, dist, shared, different))
    
    pairs.sort(key=lambda x: x[2])
    
    print("\n   CLOSEST PAIRS (most shared toggles):")
    for name1, name2, dist, shared, diff in pairs[:5]:
        print(f"   {name1} ↔ {name2}: d={dist:.4f}, shared={sorted(shared) if shared else '∅'}, diff={sorted(diff) if diff else '∅'}")
    
    print("\n   FARTHEST PAIRS (no shared toggles):")
    for name1, name2, dist, shared, diff in pairs[-5:]:
        print(f"   {name1} ↔ {name2}: d={dist:.4f}, shared={sorted(shared) if shared else '∅'}, diff={sorted(diff) if diff else '∅'}")
    
    print("\n3. KEY INSIGHT:")
    print("   Jaccard distance reveals INFORMATION STRUCTURE:")
    print("   - O- ↔ AB+: d=1.00 (disjoint sets, maximally different)")
    print("   - AB- ↔ AB+: d=0.33 (share {A,B}, differ only in RhD)")
    print("   - A+ ↔ B+: d=0.67 (share RhD, differ in A vs B)")
    print()
    print("   This is NOT about antigen chemistry - it's about SET OVERLAP.")
    print("   Two blood types are 'similar' if they share toggle history,")
    print("   regardless of what those toggles biochemically mean.")
    
    # Save
    output = {
        "blood_types": {name: toggles for name, toggles in blood_types.items()},
        "jaccard_matrix": jaccard_matrix,
        "pairs": [
            {
                "pair": f"{name1}↔{name2}",
                "distance": dist,
                "shared": sorted(shared) if shared else [],
                "different": sorted(diff) if diff else []
            }
            for name1, name2, dist, shared, diff in pairs
        ]
    }
    
    with open("/home/ubuntu/ubp_probes/probe_1_results.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*80)
    print("✅ Results saved to: probe_1_results.json")
    print("="*80)
    
    print("\n" + "="*80)
    print("WHAT WE LEARNED:")
    print("="*80)
    print("""
1. Blood types ARE toggle sets - nothing more, nothing less
2. Jaccard distance measures information overlap perfectly
3. The 2^3 = 8 structure emerges naturally from 3 independent toggles
4. "Similarity" = shared toggle history, not biochemical properties
5. This validates the information-first perspective

NEXT: Test what happens when we try a FORBIDDEN 4th toggle
""")

if __name__ == "__main__":
    main()
