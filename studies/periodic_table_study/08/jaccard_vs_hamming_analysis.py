#!/usr/bin/env python3.11
"""
jaccard_vs_hamming_analysis.py - Compare Jaccard and Hamming distance on periodic table
Test: Does the information-first approach reveal different patterns?
"""
import json
from periodic_table_data import get_all_elements

def orbital_config_to_set(config_list):
    """Convert electron configuration to set of orbitals"""
    # Normalize: remove [Ubn] notation and expand
    orbitals = set()
    for orbital in config_list:
        if not orbital.startswith("["):
            orbitals.add(orbital)
    return orbitals

def orbital_config_to_binary(config_list, all_orbitals):
    """Convert electron configuration to binary vector"""
    orbitals = orbital_config_to_set(config_list)
    return [1 if orb in orbitals else 0 for orb in all_orbitals]

def jaccard_distance(set1, set2):
    """Jaccard distance: 1 - |A ∩ B| / |A ∪ B|"""
    if len(set1) == 0 and len(set2) == 0:
        return 0.0
    union = set1 | set2
    if len(union) == 0:
        return 0.0
    intersection = set1 & set2
    return 1.0 - (len(intersection) / len(union))

def hamming_distance(vec1, vec2):
    """Hamming distance: number of differing bits"""
    return sum(1 for a, b in zip(vec1, vec2) if a != b)

def analyze_periodic_table():
    """Run full comparison on all elements"""
    print("\n" + "="*80)
    print("JACCARD VS HAMMING: PERIODIC TABLE ANALYSIS")
    print("="*80 + "\n")
    
    elements = get_all_elements()
    
    # Build orbital vocabulary
    all_orbitals = set()
    for z, (symbol, name, config) in elements.items():
        all_orbitals.update(orbital_config_to_set(config))
    all_orbitals = sorted(all_orbitals)
    
    print(f"Total elements: {len(elements)}")
    print(f"Total unique orbitals: {len(all_orbitals)}\n")
    
    # Convert all elements to both representations
    element_sets = {}
    element_vectors = {}
    
    for z, (symbol, name, config) in elements.items():
        element_sets[z] = orbital_config_to_set(config)
        element_vectors[z] = orbital_config_to_binary(config, all_orbitals)
    
    # Compare distances for interesting pairs
    print("="*80)
    print("COMPARISON: Noble Gases (same group, different periods)")
    print("="*80 + "\n")
    
    noble_gases = [2, 10, 18, 36, 54, 86, 118]  # He, Ne, Ar, Kr, Xe, Rn, Og
    
    for i, z1 in enumerate(noble_gases):
        for z2 in noble_gases[i+1:]:
            sym1, name1, _ = elements[z1]
            sym2, name2, _ = elements[z2]
            
            jac_dist = jaccard_distance(element_sets[z1], element_sets[z2])
            ham_dist = hamming_distance(element_vectors[z1], element_vectors[z2])
            
            shared = element_sets[z1] & element_sets[z2]
            diff = element_sets[z1] ^ element_sets[z2]
            
            print(f"{sym1:3s} ↔ {sym2:3s}: Jaccard={jac_dist:.4f}, Hamming={ham_dist:3d}")
            print(f"         Shared: {len(shared)} orbitals, Diff: {len(diff)} orbitals\n")
    
    # Alkali metals
    print("="*80)
    print("COMPARISON: Alkali Metals (same group)")
    print("="*80 + "\n")
    
    alkali = [3, 11, 19, 37, 55, 87]  # Li, Na, K, Rb, Cs, Fr
    
    for i, z1 in enumerate(alkali):
        for z2 in alkali[i+1:]:
            sym1, name1, _ = elements[z1]
            sym2, name2, _ = elements[z2]
            
            jac_dist = jaccard_distance(element_sets[z1], element_sets[z2])
            ham_dist = hamming_distance(element_vectors[z1], element_vectors[z2])
            
            print(f"{sym1:3s} ↔ {sym2:3s}: Jaccard={jac_dist:.4f}, Hamming={ham_dist:3d}")
    
    # Find biggest discrepancies
    print("\n" + "="*80)
    print("BIGGEST DISCREPANCIES: Where Jaccard and Hamming disagree most")
    print("="*80 + "\n")
    
    discrepancies = []
    
    # Sample 100 random pairs to avoid O(n²) explosion
    import random
    random.seed(42)
    sample_pairs = []
    element_list = list(elements.keys())
    for _ in range(100):
        z1, z2 = random.sample(element_list, 2)
        if z1 > z2:
            z1, z2 = z2, z1
        sample_pairs.append((z1, z2))
    
    for z1, z2 in sample_pairs:
        sym1, name1, _ = elements[z1]
        sym2, name2, _ = elements[z2]
        
        jac_dist = jaccard_distance(element_sets[z1], element_sets[z2])
        ham_dist = hamming_distance(element_vectors[z1], element_vectors[z2])
        
        # Normalize Hamming to [0,1] for comparison
        ham_norm = ham_dist / len(all_orbitals)
        
        discrepancy = abs(jac_dist - ham_norm)
        discrepancies.append((z1, z2, jac_dist, ham_norm, discrepancy))
    
    discrepancies.sort(key=lambda x: x[4], reverse=True)
    
    print("Top 10 pairs where methods disagree:\n")
    for z1, z2, jac, ham, disc in discrepancies[:10]:
        sym1 = elements[z1][0]
        sym2 = elements[z2][0]
        print(f"{sym1:3s} ↔ {sym2:3s}: Jaccard={jac:.4f}, Hamming(norm)={ham:.4f}, Δ={disc:.4f}")
        
        shared = element_sets[z1] & element_sets[z2]
        diff = element_sets[z1] ^ element_sets[z2]
        print(f"         Shared: {shared}")
        print(f"         Diff: {diff}\n")
    
    # Save results
    results = {
        "total_elements": len(elements),
        "total_orbitals": len(all_orbitals),
        "noble_gas_comparison": [],
        "alkali_comparison": [],
        "biggest_discrepancies": []
    }
    
    for z1, z2, jac, ham, disc in discrepancies[:20]:
        results["biggest_discrepancies"].append({
            "element1": elements[z1][0],
            "element2": elements[z2][0],
            "jaccard_distance": jac,
            "hamming_normalized": ham,
            "discrepancy": disc
        })
    
    with open("/home/ubuntu/periodic_table_hexdictionary/jaccard_vs_hamming_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80 + "\n")
    print("Jaccard distance reveals STRUCTURAL relationships (shared orbitals)")
    print("Hamming distance counts BIT differences (presence/absence)")
    print("\nFor chemistry, Jaccard is more meaningful:")
    print("  - Elements with shared orbitals have similar chemistry")
    print("  - Hamming treats all orbital differences equally")
    print("  - Jaccard weights by overlap (information content)")

if __name__ == "__main__":
    analyze_periodic_table()
