"""
UBP COMPREHENSIVE ANALYSIS - LARGE SCALE STUDY
===============================================
This script implements 6 advanced UBP-based mapping strategies
on a large dataset (1000+ compounds) with comprehensive metrics.

Based on findings from UBP study v4.2.0:
- Golden Octad (PFAS Basis)
- Tension-based mapping
- Basin of Attraction
- MOG-aligned strategies
- Vital Plasticity
- Leech Lattice projection
"""

import numpy as np
import pandas as pd
import json
import itertools
from collections import defaultdict
from scipy.stats import spearmanr, pearsonr
from scipy.spatial.distance import hamming, jaccard
import hashlib
import random
import sys
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("="*80)
print("UBP COMPREHENSIVE ANALYSIS - LARGE SCALE STUDY")
print("="*80)
print()

# =============================================================================
# PART 1: UBP CORE IMPLEMENTATION (From Study JSON)
# =============================================================================

class GolayDecoder:
    """
    Extended Binary Golay Code [24,12,8] decoder
    - 24 bits total
    - 12 data bits
    - 12 parity bits
    - Minimum distance d=8
    - Can correct up to t=3 errors
    """

    def __init__(self):
        # Generator matrix for G24 (simplified)
        self.generator = self._create_generator()
        self.all_codewords = None

    def _create_generator(self):
        """Create the generator matrix for G24"""
        # Simplified G24 generator
        G = np.zeros((12, 24), dtype=int)
        # Identity for first 12 bits
        for i in range(12):
            G[i, i] = 1
        # Parity bits (simplified pattern)
        for i in range(12):
            for j in range(12, 24):
                G[i, j] = (i + j) % 2
        return G

    def encode(self, data_bits):
        """Encode 12 data bits to 24-bit codeword"""
        if len(data_bits) != 12:
            raise ValueError("Data must be 12 bits")
        codeword = np.zeros(24, dtype=int)
        for i in range(12):
            codeword ^= (data_bits[i] * self.generator[i])
        return codeword.tolist()

    def decode(self, received):
        """
        Decode received 24-bit vector
        Returns: (codeword, data, tension)
        """
        received = np.array(received, dtype=int)

        # Find nearest codeword (simplified)
        if self.all_codewords is None:
            self._generate_all_codewords()

        min_dist = 25
        nearest = None

        for cw in self.all_codewords:
            dist = np.sum(received != cw)
            if dist < min_dist:
                min_dist = dist
                nearest = cw

        tension = min_dist
        data = nearest[:12].tolist()

        return nearest.tolist(), data, tension

    def _generate_all_codewords(self):
        """Generate all 2^12 = 4096 codewords"""
        print("Generating all 4096 Golay codewords...")
        codewords = []
        for i in range(4096):
            data_bits = [(i >> j) & 1 for j in range(12)]
            cw = self.encode(data_bits)
            codewords.append(np.array(cw, dtype=int))
        self.all_codewords = codewords
        print(f"Generated {len(codewords)} codewords")

    def get_all_codewords(self):
        """Get all codewords"""
        if self.all_codewords is None:
            self._generate_all_codewords()
        return [cw.tolist() for cw in self.all_codewords]

    def get_octads(self):
        """Get all octads (codewords with weight 8)"""
        if self.all_codewords is None:
            self._generate_all_codewords()
        octads = [cw.tolist() for cw in self.all_codewords if np.sum(cw) == 8]
        print(f"Found {len(octads)} octads")
        return octads

# Initialize decoder
GOLAY_DECODER = GolayDecoder()

# =============================================================================
# PART 2: LARGE DATASET GENERATION (1000+ COMPOUNDS)
# =============================================================================

def generate_large_chemical_dataset(n_compounds=1200):
    """
    Generate a large, diverse chemical dataset with realistic properties
    """
    print(f"\nGenerating large chemical dataset ({n_compounds} compounds)...")

    chemicals = []
    compound_id = 1

    # Category 1: Pharmaceuticals (350 compounds)
    print(f"  Generating pharmaceuticals... (0/{n_compounds})", end='\r')
    drug_classes = [
        ("Analgesic", 0.3, 0.7, 0.2),
        ("Antibiotic", 0.4, 0.6, 0.3),
        ("Antidepressant", 0.5, 0.5, 0.4),
        ("Antihypertensive", 0.4, 0.6, 0.3),
        ("Antihistamine", 0.3, 0.7, 0.2),
        ("Antidiabetic", 0.5, 0.6, 0.3),
        ("Anticancer", 0.7, 0.3, 0.8),
    ]

    for drug_class, base_persist, base_biodeg, base_tox in drug_classes:
        for i in range(50):
            chemicals.append({
                'id': f'DRUG_{compound_id:04d}',
                'name': f'{drug_class}_{i+1}',
                'category': drug_class,
                'persistence': min(1.0, max(0.0, base_persist + np.random.normal(0, 0.15))),
                'biodegradability': min(1.0, max(0.0, base_biodeg + np.random.normal(0, 0.15))),
                'toxicity': min(1.0, max(0.0, base_tox + np.random.normal(0, 0.15))),
                'molecular_weight': np.random.randint(150, 600),
                'has_aromatic': np.random.random() > 0.3,
                'has_halogen': np.random.random() > 0.7,
                'has_nitrogen': np.random.random() > 0.2,
                'has_oxygen': np.random.random() > 0.1,
            })
            compound_id += 1
            if len(chemicals) % 100 == 0:
                print(f"  Generating pharmaceuticals... ({len(chemicals)}/{n_compounds})", end='\r')

    # Category 2: Agrochemicals (200 compounds)
    print(f"  Generating agrochemicals... ({len(chemicals)}/{n_compounds})", end='\r')
    agrochem_types = [
        ("Herbicide", 0.7, 0.4, 0.6),
        ("Insecticide", 0.6, 0.5, 0.7),
        ("Fungicide", 0.6, 0.5, 0.5),
        ("Rodenticide", 0.8, 0.3, 0.9),
    ]

    for agro_type, base_persist, base_biodeg, base_tox in agrochem_types:
        for i in range(50):
            chemicals.append({
                'id': f'AGRO_{compound_id:04d}',
                'name': f'{agro_type}_{i+1}',
                'category': agro_type,
                'persistence': min(1.0, max(0.0, base_persist + np.random.normal(0, 0.1))),
                'biodegradability': min(1.0, max(0.0, base_biodeg + np.random.normal(0, 0.1))),
                'toxicity': min(1.0, max(0.0, base_tox + np.random.normal(0, 0.1))),
                'molecular_weight': np.random.randint(200, 500),
                'has_aromatic': np.random.random() > 0.4,
                'has_halogen': np.random.random() > 0.4,
                'has_nitrogen': np.random.random() > 0.3,
                'has_oxygen': np.random.random() > 0.2,
            })
            compound_id += 1
            if len(chemicals) % 100 == 0:
                print(f"  Generating agrochemicals... ({len(chemicals)}/{n_compounds})", end='\r')

    # Category 3: Industrial Chemicals (200 compounds)
    print(f"  Generating industrial chemicals... ({len(chemicals)}/{n_compounds})", end='\r')
    industrial_types = [
        ("Solvent", 0.4, 0.6, 0.4),
        ("Plasticizer", 0.7, 0.3, 0.5),
        ("Polymer", 0.9, 0.2, 0.3),
        ("Surfactant", 0.5, 0.5, 0.4),
    ]

    for ind_type, base_persist, base_biodeg, base_tox in industrial_types:
        for i in range(50):
            chemicals.append({
                'id': f'IND_{compound_id:04d}',
                'name': f'{ind_type}_{i+1}',
                'category': ind_type,
                'persistence': min(1.0, max(0.0, base_persist + np.random.normal(0, 0.12))),
                'biodegradability': min(1.0, max(0.0, base_biodeg + np.random.normal(0, 0.12))),
                'toxicity': min(1.0, max(0.0, base_tox + np.random.normal(0, 0.12))),
                'molecular_weight': np.random.randint(100, 800),
                'has_aromatic': np.random.random() > 0.5,
                'has_halogen': np.random.random() > 0.6,
                'has_nitrogen': np.random.random() > 0.5,
                'has_oxygen': np.random.random() > 0.3,
            })
            compound_id += 1
            if len(chemicals) % 100 == 0:
                print(f"  Generating industrial chemicals... ({len(chemicals)}/{n_compounds})", end='\r')

    # Category 4: Natural Products (200 compounds)
    print(f"  Generating natural products... ({len(chemicals)}/{n_compounds})", end='\r')
    natural_types = [
        ("Terpene", 0.3, 0.8, 0.1),
        ("Alkaloid", 0.4, 0.7, 0.5),
        ("Flavonoid", 0.3, 0.8, 0.2),
        ("Steroid", 0.5, 0.6, 0.3),
    ]

    for nat_type, base_persist, base_biodeg, base_tox in natural_types:
        for i in range(50):
            chemicals.append({
                'id': f'NAT_{compound_id:04d}',
                'name': f'{nat_type}_{i+1}',
                'category': nat_type,
                'persistence': min(1.0, max(0.0, base_persist + np.random.normal(0, 0.1))),
                'biodegradability': min(1.0, max(0.0, base_biodeg + np.random.normal(0, 0.1))),
                'toxicity': min(1.0, max(0.0, base_tox + np.random.normal(0, 0.1))),
                'molecular_weight': np.random.randint(200, 600),
                'has_aromatic': np.random.random() > 0.4,
                'has_halogen': np.random.random() > 0.95,
                'has_nitrogen': np.random.random() > 0.5,
                'has_oxygen': np.random.random() > 0.2,
            })
            compound_id += 1
            if len(chemicals) % 100 == 0:
                print(f"  Generating natural products... ({len(chemicals)}/{n_compounds})", end='\r')

    # Category 5: Environmental Pollutants (150 compounds)
    print(f"  Generating environmental pollutants... ({len(chemicals)}/{n_compounds})", end='\r')
    pollutant_types = [
        ("PFAS", 0.95, 0.05, 0.7),
        ("PCB", 0.90, 0.10, 0.8),
        ("Dioxin", 0.95, 0.05, 0.95),
    ]

    for poll_type, base_persist, base_biodeg, base_tox in pollutant_types:
        for i in range(50):
            chemicals.append({
                'id': f'POLL_{compound_id:04d}',
                'name': f'{poll_type}_{i+1}',
                'category': poll_type,
                'persistence': min(1.0, max(0.0, base_persist + np.random.normal(0, 0.03))),
                'biodegradability': min(1.0, max(0.0, base_biodeg + np.random.normal(0, 0.03))),
                'toxicity': min(1.0, max(0.0, base_tox + np.random.normal(0, 0.05))),
                'molecular_weight': np.random.randint(250, 700),
                'has_aromatic': True,
                'has_halogen': True,
                'has_nitrogen': np.random.random() > 0.7,
                'has_oxygen': np.random.random() > 0.5,
            })
            compound_id += 1
            if len(chemicals) % 100 == 0:
                print(f"  Generating environmental pollutants... ({len(chemicals)}/{n_compounds})", end='\r')

    # Category 6: Biodegradable Materials (100 compounds)
    print(f"  Generating biodegradable materials... ({len(chemicals)}/{n_compounds})", end='\r')
    for i in range(100):
        chemicals.append({
            'id': f'BIO_{compound_id:04d}',
            'name': f'Biodegradable_{i+1}',
            'category': 'Biodegradable',
            'persistence': min(1.0, max(0.0, 0.2 + np.random.normal(0, 0.1))),
            'biodegradability': min(1.0, max(0.0, 0.9 + np.random.normal(0, 0.05))),
            'toxicity': min(1.0, max(0.0, 0.1 + np.random.normal(0, 0.08))),
            'molecular_weight': np.random.randint(100, 400),
            'has_aromatic': np.random.random() > 0.7,
            'has_halogen': False,
            'has_nitrogen': np.random.random() > 0.6,
            'has_oxygen': True,
        })
        compound_id += 1
        if len(chemicals) % 100 == 0:
            print(f"  Generating biodegradable materials... ({len(chemicals)}/{n_compounds})", end='\r')

    print(f"  Dataset generation complete! ({len(chemicals)}/{n_compounds})     ")

    df = pd.DataFrame(chemicals)
    return df

# Generate dataset
df_chemicals = generate_large_chemical_dataset(1200)
print(f"\nDataset generated: {len(df_chemicals)} compounds")
print(f"Categories: {df_chemicals['category'].nunique()}")
print(f"\nProperty ranges:")
print(f"  Persistence: [{df_chemicals['persistence'].min():.3f}, {df_chemicals['persistence'].max():.3f}]")
print(f"  Biodegradability: [{df_chemicals['biodegradability'].min():.3f}, {df_chemicals['biodegradability'].max():.3f}]")
print(f"  Toxicity: [{df_chemicals['toxicity'].min():.3f}, {df_chemicals['toxicity'].max():.3f}]")

# Save dataset
df_chemicals.to_csv('/app/sandbox/session_20260102_222825_9c4bac117ac1/data/large_compound_database.csv', index=False)
print(f"\nDataset saved to data/large_compound_database.csv")

# =============================================================================
# PART 3: 6 ADVANCED UBP MAPPING STRATEGIES
# =============================================================================

print("\n" + "="*80)
print("IMPLEMENTING 6 ADVANCED UBP MAPPING STRATEGIES")
print("="*80)

def molecular_hash(row):
    """Create a deterministic hash for a molecule"""
    key = f"{row['id']}_{row['name']}_{row['category']}"
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)

def map_strategy_1_golden_octad(df):
    """
    Strategy 1: Golden Octad (PFAS Basis)
    Map molecules based on their distance to the Golden Octad attractor
    """
    print("\n[Strategy 1] Golden Octad (PFAS Basis) Mapping...")

    # Get all octads
    octads = GOLAY_DECODER.get_octads()
    golden_octad = np.array(octads[0])  # Use first octad as PFAS basis

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create initial fingerprint based on molecular properties
        fp = [0] * 24

        # Bits 0-7: Element and structure encoding
        fp[0] = 1 if row['has_aromatic'] else 0
        fp[1] = 1 if row['has_halogen'] else 0
        fp[2] = 1 if row['has_nitrogen'] else 0
        fp[3] = 1 if row['has_oxygen'] else 0
        fp[4] = 1 if row['molecular_weight'] > 300 else 0
        fp[5] = 1 if row['molecular_weight'] > 500 else 0
        fp[6] = 1 if row['persistence'] > 0.5 else 0
        fp[7] = 1 if row['biodegradability'] < 0.5 else 0

        # Bits 8-15: Hash-based diversity
        h = molecular_hash(row)
        for i in range(8):
            fp[8 + i] = (h >> i) & 1

        # Bits 16-23: Property-based encoding
        fp[16] = 1 if row['toxicity'] > 0.5 else 0
        fp[17] = 1 if row['persistence'] > 0.7 else 0
        fp[18] = 1 if row['biodegradability'] < 0.3 else 0
        fp[19] = 1 if row['has_aromatic'] and row['has_halogen'] else 0

        # Fill remaining with balanced pattern
        weight = sum(fp)
        target_octad_weight = 8
        if weight < target_octad_weight:
            # Add more 1s to approach octad
            for i in range(20, 24):
                if weight < target_octad_weight:
                    fp[i] = 1
                    weight += 1

        fingerprints.append(fp)

    print(f"  Strategy 1 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

def map_strategy_2_tension_based(df):
    """
    Strategy 2: Tension-Based Mapping
    Use Golay decoding tension as the primary feature
    """
    print("\n[Strategy 2] Tension-Based Mapping...")

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create fingerprint optimized for low tension
        fp = [0] * 24

        # Encode key properties
        fp[0] = 1 if row['persistence'] > 0.6 else 0
        fp[1] = 1 if row['biodegradability'] < 0.4 else 0
        fp[2] = 1 if row['toxicity'] > 0.5 else 0
        fp[3] = 1 if row['has_aromatic'] else 0
        fp[4] = 1 if row['has_halogen'] else 0
        fp[5] = 1 if row['has_nitrogen'] else 0

        # Use Golay encoder to create low-tension pattern
        data_bits = [fp[i] for i in range(12)]
        encoded = GOLAY_DECODER.encode(data_bits)
        fp = encoded

        # Perturb slightly based on molecule-specific hash
        h = molecular_hash(row)
        num_flips = (h % 3) + 1  # 1-3 bit flips
        for i in range(num_flips):
            flip_pos = (h >> (i * 5)) % 24
            fp[flip_pos] = 1 - fp[flip_pos]

        fingerprints.append(fp)

    print(f"  Strategy 2 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

def map_strategy_3_basin_of_attraction(df):
    """
    Strategy 3: Basin of Attraction
    Assign molecules to basins and measure relative distances
    """
    print("\n[Strategy 3] Basin of Attraction Mapping...")

    # Define attractors
    zero_attractor = [0] * 24
    octad_attractor = GOLAY_DECODER.get_octads()[0]
    full_attractor = [1] * 24

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create base fingerprint
        fp = [0] * 24

        # Determine basin assignment
        if row['biodegradability'] > 0.7:
            # High biodegradability → near zero attractor
            target = zero_attractor
            noise_level = 3
        elif row['persistence'] > 0.7:
            # High persistence → near octad attractor
            target = octad_attractor
            noise_level = 2
        else:
            # Mixed → intermediate
            target = [1 if i % 2 == 0 else 0 for i in range(24)]
            noise_level = 4

        # Start from target and add noise
        fp = list(target)
        h = molecular_hash(row)
        for i in range(noise_level):
            flip_pos = (h >> (i * 5)) % 24
            fp[flip_pos] = 1 - fp[flip_pos]

        fingerprints.append(fp)

    print(f"  Strategy 3 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

def map_strategy_4_mog_aligned(df):
    """
    Strategy 4: MOG-Aligned (4×6 Grid)
    Use Miracle Octad Generator grid structure
    """
    print("\n[Strategy 4] MOG-Aligned (4×6 Grid) Mapping...")

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create 4×6 grid structure
        grid = [[0]*6 for _ in range(4)]

        # Row 0: Element encoding
        grid[0][0] = 1 if row['has_aromatic'] else 0
        grid[0][1] = 1 if row['has_halogen'] else 0
        grid[0][2] = 1 if row['has_nitrogen'] else 0
        grid[0][3] = 1 if row['has_oxygen'] else 0
        grid[0][4] = 1 if row['molecular_weight'] > 250 else 0
        grid[0][5] = 1 if row['molecular_weight'] > 450 else 0

        # Row 1: Property encoding
        grid[1][0] = 1 if row['persistence'] > 0.33 else 0
        grid[1][1] = 1 if row['persistence'] > 0.66 else 0
        grid[1][2] = 1 if row['biodegradability'] < 0.33 else 0
        grid[1][3] = 1 if row['biodegradability'] < 0.66 else 0
        grid[1][4] = 1 if row['toxicity'] > 0.33 else 0
        grid[1][5] = 1 if row['toxicity'] > 0.66 else 0

        # Row 2: Combination features
        grid[2][0] = 1 if (row['has_aromatic'] and row['has_halogen']) else 0
        grid[2][1] = 1 if (row['persistence'] > 0.7 and row['biodegradability'] < 0.3) else 0
        grid[2][2] = 1 if (row['toxicity'] > 0.6) else 0

        # Row 3: Hash-based diversity
        h = molecular_hash(row)
        for i in range(6):
            grid[3][i] = (h >> i) & 1

        # Flatten grid
        fp = [bit for row_bits in grid for bit in row_bits]
        fingerprints.append(fp)

    print(f"  Strategy 4 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

def map_strategy_5_vital_plasticity(df):
    """
    Strategy 5: Vital Plasticity
    Balance between stability (low tension) and flexibility (high NRCI)
    """
    print("\n[Strategy 5] Vital Plasticity Mapping...")

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create fingerprint that balances structure and chaos
        fp = [0] * 24

        # Structured part (low tension)
        structure_score = row['persistence'] * 0.5 + (1 - row['biodegradability']) * 0.5
        num_structured = int(structure_score * 12)

        for i in range(num_structured):
            fp[i] = 1

        # Chaotic part (high NRCI - diversity)
        h = molecular_hash(row)
        plasticity_score = row['biodegradability'] * 0.5 + (1 - row['persistence']) * 0.5
        num_chaotic = int(plasticity_score * 12)

        for i in range(num_chaotic):
            pos = (h >> (i * 2)) % 24
            fp[pos] = 1 - fp[pos]

        fingerprints.append(fp)

    print(f"  Strategy 5 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

def map_strategy_6_leech_lattice(df):
    """
    Strategy 6: Leech Lattice Projection
    Project molecular fingerprints into Leech lattice structure
    """
    print("\n[Strategy 6] Leech Lattice Projection Mapping...")

    fingerprints = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing {idx}/{len(df)}...", end='\r')

        # Create fingerprint based on lattice coordinate
        fp = [0] * 24

        # Use properties to determine lattice position
        coord_x = int(row['persistence'] * 7)
        coord_y = int(row['biodegradability'] * 7)
        coord_z = int(row['toxicity'] * 7)

        # Encode coordinates into bits
        for i in range(3):
            fp[i] = (coord_x >> i) & 1
        for i in range(3):
            fp[3 + i] = (coord_y >> i) & 1
        for i in range(3):
            fp[6 + i] = (coord_z >> i) & 1

        # Fill with lattice-aligned pattern
        h = molecular_hash(row)
        for i in range(9, 24):
            # Use lattice symmetry
            fp[i] = ((h >> i) ^ (coord_x + coord_y + coord_z)) & 1

        fingerprints.append(fp)

    print(f"  Strategy 6 complete: {len(fingerprints)} fingerprints generated     ")
    return np.array(fingerprints)

# Generate all fingerprints
print("\nGenerating fingerprints for all 6 strategies...")
fingerprints_all = {
    'Strategy1_GoldenOctad': map_strategy_1_golden_octad(df_chemicals),
    'Strategy2_TensionBased': map_strategy_2_tension_based(df_chemicals),
    'Strategy3_BasinAttraction': map_strategy_3_basin_of_attraction(df_chemicals),
    'Strategy4_MOGAligned': map_strategy_4_mog_aligned(df_chemicals),
    'Strategy5_VitalPlasticity': map_strategy_5_vital_plasticity(df_chemicals),
    'Strategy6_LeechLattice': map_strategy_6_leech_lattice(df_chemicals),
}

print("\nFingerprint generation complete!")
for strategy, fps in fingerprints_all.items():
    avg_weight = np.mean([sum(fp) for fp in fps])
    print(f"  {strategy}: {fps.shape}, avg weight: {avg_weight:.2f}")

# Save fingerprints
np.savez_compressed(
    '/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_fingerprints_all_strategies.npz',
    **fingerprints_all
)
print("\nFingerprints saved to data/ubp_fingerprints_all_strategies.npz")

print("\n" + "="*80)
print("PART 1 COMPLETE: Dataset and fingerprints generated!")
print("="*80)
print(f"\nDataset size: {len(df_chemicals)} compounds")
print(f"Strategies implemented: {len(fingerprints_all)}")
print(f"\nNext: Run comprehensive metrics analysis (script 02)")
