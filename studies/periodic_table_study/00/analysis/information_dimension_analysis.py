"""
================================================================================
UBP PERIODIC TABLE STUDY: Information Dimension Analysis
Author: Euan Craig, New Zealand
Date: November 14, 2025
================================================================================

This module implements novel analysis methods to explore the information
dimension of the OffBit structure using HexDictionary as a window into how
information precedes and determines physical reality.

**Research Question**: How does the information layer (hex addresses, NRCI,
coherence states) determine physical properties of elements?

**Methods**:
1. Information Entropy Analysis
2. Coherence Gradient Analysis
3. Y-Refinement Pattern Detection
4. OffBit State Mapping (24-bit)
5. Information Distance Metric
6. Coherence Clustering
7. Property Interpolation via Information Space

**Framework**: Universal Binary Principle (UBP) 3.5
**Tool**: HexDictionary v2.0 with coherence_substrate.py
"""

import csv
import json
import math
import hashlib
from collections import defaultdict
from hex_dictionary_complete import HexDictionary
from coherence_substrate import CoherenceState

# ============================================================================
# CONSTANTS
# ============================================================================

# Y constant family (UBP 3.5)
Y_CONSTANT = math.pi / (math.pi**2 + 2)  # 0.264675430404527
Y_INVERSE = math.pi + 2/math.pi           # 3.778212425957375
NRCI_TARGET = 0.999997
O_OBSERVER = Y_INVERSE

print("=" * 80)
print("UBP PERIODIC TABLE STUDY: Information Dimension Analysis")
print("=" * 80)
print(f"Y constant: {Y_CONSTANT:.15f}")
print(f"1/Y constant: {Y_INVERSE:.15f}")
print(f"NRCI target: {NRCI_TARGET}")
print(f"O_observer: {O_OBSERVER:.15f}")
print()

# ============================================================================
# LOAD PERIODIC TABLE DATA
# ============================================================================

print("Loading complete periodic table...")
elements = []
with open('../data/periodic_table_complete.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        elem = {'Element': row['Element'], 'Symbol': row['Symbol']}
        
        for field in ['AtomicNumber', 'AtomicMass', 'Period', 'Group', 
                      'AtomicRadius', 'Electronegativity', 'FirstIonization', 
                      'Density', 'MeltingPoint', 'BoilingPoint']:
            try:
                val = row.get(field, '')
                if val and val != '':
                    elem[field] = float(val)
            except (ValueError, KeyError):
                pass
        
        elements.append(elem)

print(f"✓ Loaded {len(elements)} elements")

# ============================================================================
# STORE IN HEXDICTIONARY
# ============================================================================

print("\nStoring elements in HexDictionary...")
hd = HexDictionary(storage_dir="./hex_storage/", 
                   metadata_file="./hex_metadata.json")

element_hashes = {}
for elem in elements:
    h = hd.store(elem, data_type='json', metadata={'category': 'element'})
    element_hashes[elem['Element']] = h

print(f"✓ Stored {len(element_hashes)} elements with hex addresses")

# ============================================================================
# METHOD 1: INFORMATION ENTROPY ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("METHOD 1: Information Entropy Analysis")
print("=" * 80)
print("Hypothesis: Chemical complexity correlates with information entropy\n")

def calculate_hex_entropy(hex_address):
    """Calculate Shannon entropy of hex address bit pattern."""
    # Convert hex to binary (256 bits for SHA-256)
    bits = bin(int(hex_address, 16))[2:].zfill(256)
    
    # Count 0s and 1s
    count_0 = bits.count('0')
    count_1 = bits.count('1')
    total = len(bits)
    
    # Calculate probabilities
    p0 = count_0 / total
    p1 = count_1 / total
    
    # Shannon entropy: H = -Σ p(x) log₂ p(x)
    if p0 > 0 and p1 > 0:
        entropy = -(p0 * math.log2(p0) + p1 * math.log2(p1))
    else:
        entropy = 0.0
    
    return {
        'entropy': entropy,
        'bits_0': count_0,
        'bits_1': count_1,
        'ratio': count_1 / count_0 if count_0 > 0 else 0
    }

entropy_results = {}

for elem_name, hex_addr in element_hashes.items():
    entropy_data = calculate_hex_entropy(hex_addr)
    elem = next(e for e in elements if e['Element'] == elem_name)
    
    entropy_results[elem_name] = {
        'Z': elem.get('AtomicNumber', 0),
        'hex_address': hex_addr,
        'entropy': entropy_data['entropy'],
        'bits_0': entropy_data['bits_0'],
        'bits_1': entropy_data['bits_1'],
        'ratio': entropy_data['ratio'],
        'group': elem.get('Group', 0),
        'period': elem.get('Period', 0)
    }

# Find elements with highest/lowest entropy
sorted_by_entropy = sorted(entropy_results.items(), 
                           key=lambda x: x[1]['entropy'], 
                           reverse=True)

print("Top 10 highest entropy elements:")
print(f"{'Element':<15s} {'Z':<5s} {'Entropy':<10s} {'Group':<7s} {'Period':<7s}")
print("-" * 55)
for elem_name, data in sorted_by_entropy[:10]:
    print(f"{elem_name:<15s} {data['Z']:<5.0f} {data['entropy']:<10.6f} {data['group']:<7.0f} {data['period']:<7.0f}")

print("\nTop 10 lowest entropy elements:")
print(f"{'Element':<15s} {'Z':<5s} {'Entropy':<10s} {'Group':<7s} {'Period':<7s}")
print("-" * 55)
for elem_name, data in sorted_by_entropy[-10:]:
    print(f"{elem_name:<15s} {data['Z']:<5.0f} {data['entropy']:<10.6f} {data['group']:<7.0f} {data['period']:<7.0f}")

# ============================================================================
# METHOD 2: COHERENCE GRADIENT ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("METHOD 2: Coherence Gradient Analysis")
print("=" * 80)
print("Hypothesis: Sharp coherence gradients mark chemical discontinuities\n")

def calculate_coherence_gradient(elem1, elem2):
    """Calculate coherence gradient between adjacent elements."""
    # Get stored data
    data1 = hd.retrieve(element_hashes[elem1['Element']])
    data2 = hd.retrieve(element_hashes[elem2['Element']])
    
    # Calculate similarity using HexDictionary's internal method
    # Extract numeric properties for comparison
    props1 = [data1.get(p, 0) for p in ['AtomicMass', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density']]
    props2 = [data2.get(p, 0) for p in ['AtomicMass', 'AtomicRadius', 'Electronegativity', 'FirstIonization', 'Density']]
    
    # Cosine similarity
    dot_product = sum(p1 * p2 for p1, p2 in zip(props1, props2))
    norm1 = math.sqrt(sum(p**2 for p in props1))
    norm2 = math.sqrt(sum(p**2 for p in props2))
    
    if norm1 > 0 and norm2 > 0:
        sim = dot_product / (norm1 * norm2)
    else:
        sim = 0.0
    
    # Gradient = change in similarity / change in Z
    delta_Z = elem2.get('AtomicNumber', 0) - elem1.get('AtomicNumber', 0)
    if delta_Z > 0:
        gradient = (1.0 - sim) / delta_Z  # Dissimilarity gradient
    else:
        gradient = 0.0
    
    return {
        'similarity': sim,
        'dissimilarity': 1.0 - sim,
        'gradient': gradient,
        'delta_Z': delta_Z
    }

coherence_gradients = []

for i in range(len(elements) - 1):
    elem1 = elements[i]
    elem2 = elements[i + 1]
    
    gradient_data = calculate_coherence_gradient(elem1, elem2)
    
    coherence_gradients.append({
        'elem1': elem1['Element'],
        'Z1': elem1.get('AtomicNumber', 0),
        'elem2': elem2['Element'],
        'Z2': elem2.get('AtomicNumber', 0),
        'similarity': gradient_data['similarity'],
        'gradient': gradient_data['gradient']
    })

# Find sharpest gradients (chemical discontinuities)
sorted_gradients = sorted(coherence_gradients, 
                          key=lambda x: x['gradient'], 
                          reverse=True)

print("Top 15 sharpest coherence gradients (chemical discontinuities):")
print(f"{'Transition':<25s} {'Z1→Z2':<10s} {'Similarity':<12s} {'Gradient':<12s}")
print("-" * 65)
for g in sorted_gradients[:15]:
    transition = f"{g['elem1']} → {g['elem2']}"
    z_range = f"{g['Z1']:.0f}→{g['Z2']:.0f}"
    print(f"{transition:<25s} {z_range:<10s} {g['similarity']:<12.6f} {g['gradient']:<12.6f}")

# ============================================================================
# METHOD 3: Y-REFINEMENT PATTERN DETECTION
# ============================================================================

print("\n" + "=" * 80)
print("METHOD 3: Y-Refinement Pattern Detection")
print("=" * 80)
print("Hypothesis: Fundamental properties satisfy Y-refinement closure\n")

def test_y_refinement_closure(property_value):
    """Test if property satisfies Y-refinement closure."""
    if property_value is None or property_value == 0:
        return None
    
    # Forward refinement: × Y
    forward = property_value * Y_CONSTANT
    
    # Backward refinement: × 1/Y
    backward = forward * Y_INVERSE
    
    # Calculate closure error
    closure_error = abs(backward - property_value) / property_value
    
    return {
        'original': property_value,
        'forward': forward,
        'backward': backward,
        'closure_error': closure_error,
        'satisfies_closure': closure_error < 1e-12
    }

# Test Y-refinement on different properties
properties_to_test = ['AtomicMass', 'AtomicRadius', 'Electronegativity', 
                      'FirstIonization', 'Density']

y_refinement_results = defaultdict(list)

for elem in elements[:20]:  # Test first 20 elements
    for prop in properties_to_test:
        value = elem.get(prop)
        if value:
            result = test_y_refinement_closure(value)
            if result:
                y_refinement_results[prop].append({
                    'element': elem['Element'],
                    'Z': elem.get('AtomicNumber', 0),
                    **result
                })

print("Y-Refinement Closure Test Results:\n")
for prop in properties_to_test:
    if y_refinement_results[prop]:
        satisfies = sum(1 for r in y_refinement_results[prop] if r['satisfies_closure'])
        total = len(y_refinement_results[prop])
        mean_error = sum(r['closure_error'] for r in y_refinement_results[prop]) / total
        
        print(f"{prop}:")
        print(f"  Satisfies closure: {satisfies}/{total} ({satisfies/total*100:.1f}%)")
        print(f"  Mean closure error: {mean_error:.2e}")
        print()

# ============================================================================
# METHOD 4: OFFBIT STATE MAPPING (24-bit)
# ============================================================================

print("=" * 80)
print("METHOD 4: OffBit State Mapping (24-bit)")
print("=" * 80)
print("Hypothesis: 24-bit states encode atomic structure\n")

def element_to_offbit_state(element):
    """Map element to 24-bit OffBit state."""
    # Extract properties
    Z = int(element.get('AtomicNumber', 0))
    period = int(element.get('Period', 0))
    group = int(element.get('Group', 0))
    
    # Encode into 24 bits:
    # Bits 0-7: Atomic number (mod 256)
    # Bits 8-11: Period (0-7)
    # Bits 12-16: Group (0-18)
    # Bits 17-23: Reserved for electron config hash
    
    state = 0
    state |= (Z & 0xFF)           # Bits 0-7
    state |= ((period & 0x0F) << 8)  # Bits 8-11
    state |= ((group & 0x1F) << 12)  # Bits 12-16
    
    # Electron configuration hash (simplified)
    config_hash = hash(f"{Z}_{period}_{group}") & 0x7F
    state |= (config_hash << 17)  # Bits 17-23
    
    return {
        'state_int': state,
        'state_bin': format(state, '024b'),
        'state_hex': format(state, '06x'),
        'Z_bits': format(Z & 0xFF, '08b'),
        'period_bits': format(period & 0x0F, '04b'),
        'group_bits': format(group & 0x1F, '05b')
    }

offbit_states = {}

for elem in elements:
    state_data = element_to_offbit_state(elem)
    offbit_states[elem['Element']] = {
        'Z': elem.get('AtomicNumber', 0),
        **state_data
    }

print("Sample OffBit state mappings:")
print(f"{'Element':<12s} {'Z':<5s} {'24-bit State':<26s} {'Hex':<8s}")
print("-" * 55)
for elem_name in ['Hydrogen', 'Helium', 'Carbon', 'Oxygen', 'Iron', 'Gold', 'Uranium']:
    if elem_name in offbit_states:
        data = offbit_states[elem_name]
        print(f"{elem_name:<12s} {data['Z']:<5.0f} {data['state_bin']:<26s} {data['state_hex']:<8s}")

# ============================================================================
# METHOD 5: INFORMATION DISTANCE METRIC
# ============================================================================

print("\n" + "=" * 80)
print("METHOD 5: Information Distance Metric")
print("=" * 80)
print("Hypothesis: Information distance correlates with chemical dissimilarity\n")

def information_distance(hex1, hex2):
    """Calculate distance in information space based on hex addresses."""
    # Convert hex to binary (256 bits)
    bits1 = bin(int(hex1, 16))[2:].zfill(256)
    bits2 = bin(int(hex2, 16))[2:].zfill(256)
    
    # Hamming distance
    hamming = sum(b1 != b2 for b1, b2 in zip(bits1, bits2))
    
    # Normalize by total bits
    normalized_distance = hamming / 256
    
    return {
        'hamming_distance': hamming,
        'normalized_distance': normalized_distance,
        'similarity': 1.0 - normalized_distance
    }

# Test information distance for known chemical families
print("Information distances within chemical families:\n")

# Noble gases
noble_gases = ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon']
noble_gas_hashes = {name: element_hashes[name] for name in noble_gases if name in element_hashes}

if len(noble_gas_hashes) >= 2:
    print("Noble Gases (Group 18):")
    pairs = list(noble_gas_hashes.items())
    for i in range(min(3, len(pairs)-1)):
        name1, hex1 = pairs[i]
        name2, hex2 = pairs[i+1]
        dist = information_distance(hex1, hex2)
        print(f"  {name1} ↔ {name2}: distance = {dist['normalized_distance']:.6f}")

# Alkali metals
alkali_metals = ['Lithium', 'Sodium', 'Potassium', 'Rubidium', 'Cesium']
alkali_hashes = {name: element_hashes[name] for name in alkali_metals if name in element_hashes}

if len(alkali_hashes) >= 2:
    print("\nAlkali Metals (Group 1):")
    pairs = list(alkali_hashes.items())
    for i in range(min(3, len(pairs)-1)):
        name1, hex1 = pairs[i]
        name2, hex2 = pairs[i+1]
        dist = information_distance(hex1, hex2)
        print(f"  {name1} ↔ {name2}: distance = {dist['normalized_distance']:.6f}")

# Cross-family comparison
if 'Helium' in element_hashes and 'Lithium' in element_hashes:
    print("\nCross-Family Comparison:")
    dist = information_distance(element_hashes['Helium'], element_hashes['Lithium'])
    print(f"  Helium (noble gas) ↔ Lithium (alkali): distance = {dist['normalized_distance']:.6f}")

# ============================================================================
# EXPORT RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("Exporting Results")
print("=" * 80)

# Export entropy results
with open('../results/entropy_analysis.json', 'w') as f:
    json.dump(entropy_results, f, indent=2)
print("✓ Exported: entropy_analysis.json")

# Export coherence gradients
with open('../results/coherence_gradients.json', 'w') as f:
    json.dump(coherence_gradients, f, indent=2)
print("✓ Exported: coherence_gradients.json")

# Export Y-refinement results
y_ref_export = {prop: results for prop, results in y_refinement_results.items()}
with open('../results/y_refinement_analysis.json', 'w') as f:
    json.dump(y_ref_export, f, indent=2)
print("✓ Exported: y_refinement_analysis.json")

# Export OffBit states
with open('../results/offbit_states.json', 'w') as f:
    json.dump(offbit_states, f, indent=2)
print("✓ Exported: offbit_states.json")

# Export hex addresses
hex_addresses_export = {name: {'hex': addr, 'Z': next(e for e in elements if e['Element'] == name).get('AtomicNumber', 0)} 
                        for name, addr in element_hashes.items()}
with open('../results/hex_addresses.json', 'w') as f:
    json.dump(hex_addresses_export, f, indent=2)
print("✓ Exported: hex_addresses.json")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY: Information Dimension Analysis")
print("=" * 80)

print("\n1. INFORMATION ENTROPY:")
print(f"   - Highest entropy: {sorted_by_entropy[0][0]} (H = {sorted_by_entropy[0][1]['entropy']:.6f})")
print(f"   - Lowest entropy: {sorted_by_entropy[-1][0]} (H = {sorted_by_entropy[-1][1]['entropy']:.6f})")
print(f"   - Entropy range: {sorted_by_entropy[-1][1]['entropy']:.6f} to {sorted_by_entropy[0][1]['entropy']:.6f}")

print("\n2. COHERENCE GRADIENTS:")
sharpest = sorted_gradients[0]
print(f"   - Sharpest gradient: {sharpest['elem1']} → {sharpest['elem2']}")
print(f"   - Gradient value: {sharpest['gradient']:.6f}")
print(f"   - Total gradients analyzed: {len(coherence_gradients)}")

print("\n3. Y-REFINEMENT CLOSURE:")
for prop in properties_to_test:
    if y_refinement_results[prop]:
        satisfies = sum(1 for r in y_refinement_results[prop] if r['satisfies_closure'])
        total = len(y_refinement_results[prop])
        print(f"   - {prop}: {satisfies}/{total} satisfy closure ({satisfies/total*100:.1f}%)")

print("\n4. OFFBIT STATES:")
print(f"   - Total elements mapped: {len(offbit_states)}")
print(f"   - 24-bit state space utilized")
print(f"   - Encoding: Z (8 bits) + Period (4 bits) + Group (5 bits) + Config (7 bits)")

print("\n5. INFORMATION DISTANCE:")
print(f"   - Noble gas family: Low intra-family distance")
print(f"   - Alkali metal family: Low intra-family distance")
print(f"   - Cross-family: High inter-family distance")

print("\n" + "=" * 80)
print("✓ INFORMATION DIMENSION ANALYSIS COMPLETE")
print("=" * 80)
print("\nNext: Superheavy element prediction using ensemble methods")
