#!/usr/bin/env python3.11
"""
information_layer_discovery.py - Use all study data to discover the pure information metric

Question: What IS information in the OffBit layer?
Method: Let the data tell us what it actually contains, not what we think it should contain
"""
import sys
import json
import os
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState

# Collect ALL data from the study
def collect_all_study_data():
    """Gather every piece of data we've generated"""
    data = {
        "blood_types": {},
        "measurements": [],
        "relationships": []
    }
    
    # Blood type toggle sequences (the ONLY real data we have)
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
    
    for bt, toggles in blood_types.items():
        data["blood_types"][bt] = {
            "toggle_sequence": toggles,
            "toggle_count": len(toggles),
            "toggle_bits": [1 if a in toggles else 0 for a in ["A", "B", "RhD"]],
            "binary_representation": "".join(str(1 if a in toggles else 0) for a in ["A", "B", "RhD"])
        }
    
    return data

def analyze_what_information_actually_is(data):
    """
    Stop assuming. Look at what the data actually contains.
    
    We have 8 blood types with 3-bit toggle patterns.
    What is the INFORMATION here?
    """
    print("\n" + "="*80)
    print("INFORMATION LAYER DISCOVERY")
    print("="*80 + "\n")
    
    print("What do we actually have?")
    print("-" * 40)
    
    # The raw data
    for bt, info in data["blood_types"].items():
        print(f"{bt:4s}: {info['binary_representation']} = {info['toggle_sequence']}")
    
    print("\n" + "="*80)
    print("QUESTION: What is the INFORMATION in this data?")
    print("="*80 + "\n")
    
    # Hypothesis 1: Information is the toggle sequence itself
    print("Hypothesis 1: Information = Toggle Sequence")
    print("-" * 40)
    print("  This is what we've been measuring (history-aware HexDictionary)")
    print("  Result: 8/8 perfect reconstructions")
    print("  But: This is TRIVIAL. We're just comparing lists.")
    print("  Insight: This is not information, this is DATA.\n")
    
    # Hypothesis 2: Information is the binary pattern
    print("Hypothesis 2: Information = Binary Pattern")
    print("-" * 40)
    print("  This is what Hamming distance measures")
    print("  Result: Can count bit differences")
    print("  But: Hamming(A+, B+) = Hamming(A-, B-) = 2")
    print("       Yet A+ and B+ both have RhD, A- and B- don't")
    print("  Insight: Hamming is blind to WHICH bits differ.\n")
    
    # Hypothesis 3: Information is the STRUCTURE of the pattern
    print("Hypothesis 3: Information = Pattern Structure")
    print("-" * 40)
    
    # Compute structural relationships
    for bt1, info1 in data["blood_types"].items():
        for bt2, info2 in data["blood_types"].items():
            if bt1 < bt2:  # Only compare each pair once
                # What do they SHARE?
                shared_toggles = set(info1["toggle_sequence"]) & set(info2["toggle_sequence"])
                # What is DIFFERENT?
                diff_toggles = set(info1["toggle_sequence"]) ^ set(info2["toggle_sequence"])
                
                # This is the INFORMATION
                print(f"  {bt1} ↔ {bt2}: Shared={shared_toggles}, Diff={diff_toggles}")
    
    print("\n" + "="*80)
    print("DISCOVERY: Information is RELATIONSHIP, not CONTENT")
    print("="*80 + "\n")
    
    print("The OffBit information layer is about:")
    print("  1. What is SHARED between states")
    print("  2. What is DIFFERENT between states")
    print("  3. The STRUCTURE of those relationships\n")
    
    print("This is not Hamming distance (counts bits)")
    print("This is not spectral distance (global structure)")
    print("This is not history comparison (sequence order)")
    print("\nThis is SET THEORY.\n")
    
    return discover_pure_metric(data)

def discover_pure_metric(data):
    """
    The pure information-first metric:
    Distance = |Shared| / |Union| (Jaccard index)
    
    This measures: How much information do two states have in common?
    """
    print("="*80)
    print("THE PURE INFORMATION METRIC: Jaccard Index")
    print("="*80 + "\n")
    
    print("Definition: J(A,B) = |A ∩ B| / |A ∪ B|")
    print("  - 1.0 = identical (maximum shared information)")
    print("  - 0.0 = disjoint (no shared information)\n")
    
    print("Distance: d(A,B) = 1 - J(A,B)")
    print("  - 0.0 = identical")
    print("  - 1.0 = completely different\n")
    
    results = {}
    
    print("Blood Type Information Distance Matrix:")
    print("-" * 80)
    
    blood_types = list(data["blood_types"].keys())
    
    # Header
    print(f"{'':6s}", end="")
    for bt in blood_types:
        print(f"{bt:8s}", end="")
    print()
    
    # Matrix
    for bt1 in blood_types:
        print(f"{bt1:6s}", end="")
        row = []
        for bt2 in blood_types:
            set1 = set(data["blood_types"][bt1]["toggle_sequence"])
            set2 = set(data["blood_types"][bt2]["toggle_sequence"])
            
            if len(set1) == 0 and len(set2) == 0:
                # Both empty = identical
                jaccard = 1.0
            elif len(set1 | set2) == 0:
                jaccard = 0.0
            else:
                jaccard = len(set1 & set2) / len(set1 | set2)
            
            distance = 1.0 - jaccard
            row.append(distance)
            print(f"{distance:8.4f}", end="")
        print()
        results[bt1] = row
    
    print("\n" + "="*80)
    print("INTERPRETATION")
    print("="*80 + "\n")
    
    # Find closest pairs
    print("Closest pairs (most shared information):")
    pairs = []
    for i, bt1 in enumerate(blood_types):
        for j, bt2 in enumerate(blood_types):
            if i < j:
                pairs.append((bt1, bt2, results[bt1][j]))
    
    pairs.sort(key=lambda x: x[2])
    for bt1, bt2, dist in pairs[:5]:
        shared = set(data["blood_types"][bt1]["toggle_sequence"]) & set(data["blood_types"][bt2]["toggle_sequence"])
        print(f"  {bt1} ↔ {bt2}: d={dist:.4f}, shared={shared}")
    
    print("\nFarthest pairs (least shared information):")
    for bt1, bt2, dist in pairs[-5:]:
        diff = set(data["blood_types"][bt1]["toggle_sequence"]) ^ set(data["blood_types"][bt2]["toggle_sequence"])
        print(f"  {bt1} ↔ {bt2}: d={dist:.4f}, diff={diff}")
    
    # Save
    with open("/home/ubuntu/blood_type_ubp_study_v4/information_metric_discovery.json", 'w') as f:
        json.dump({
            "metric": "Jaccard Distance",
            "formula": "d(A,B) = 1 - |A ∩ B| / |A ∪ B|",
            "distance_matrix": {bt: row for bt, row in zip(blood_types, [results[bt] for bt in blood_types])},
            "interpretation": "Information is relationship, not content"
        }, f, indent=2)
    
    return results

if __name__ == "__main__":
    data = collect_all_study_data()
    analyze_what_information_actually_is(data)
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80 + "\n")
    print("The HexDictionary doesn't need 8 methods.")
    print("It needs ONE method: Jaccard distance on toggle sets.")
    print("\nInformation in the OffBit layer = Set membership")
    print("Distance = How much do two states share?")
    print("\nThis is the pure, information-first metric.")
