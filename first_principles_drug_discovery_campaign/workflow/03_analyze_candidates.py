#!/usr/bin/env python3
"""
Step 3: Docking/QSAR Layer - First Principles Analysis
=======================================================

This script implements the three-layer analysis:
1. Syndrome Clustering (Activity): Golay error correction analysis
2. Bit-Mask Filters (ADMET): Toxicity screening using bit masks
3. Informational Docking: Information complementarity scoring

Author: K-Dense System
Date: December 11, 2025
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path to import ubp_core
sys.path.insert(0, str(Path(__file__).parent.parent))

import ubp_core


def hamming_weight(x: int) -> int:
    """Calculate Hamming weight (number of 1s in binary representation)."""
    return bin(x).count('1')


def load_processed_data(filepath: str) -> Dict:
    """Load processed ChEMBL data."""
    print(f"Loading data from {filepath}...")
    with open(filepath, 'r') as f:
        data = json.load(f)
    print(f"  Loaded {data['metadata']['total_molecules']} molecules")
    return data


def analyze_molecule(molecule: Dict, target_seed: int, toxic_mask: int) -> Dict:
    """
    Analyze a single molecule through the three-layer system.

    Args:
        molecule: Dictionary containing chembl_id, smiles, seed, signature
        target_seed: Virtual target seed (24-bit)
        toxic_mask: Toxicity mask for ADMET filtering

    Returns:
        Dictionary with analysis results
    """
    seed = molecule['seed']

    # Layer 1: Syndrome Analysis (Activity via Golay decoding)
    # Convert seed to 24-bit representation
    bits_24 = ubp_core.int_to_bits(seed, 24)

    # Decode using Golay G₂₄ to determine syndrome
    decoded_message, num_errors, success = ubp_core.golay_decode(bits_24)

    # Syndrome weight: number of errors detected (0-3 correctable, -1 = uncorrectable)
    syndrome_weight = num_errors if success else 4  # Treat uncorrectable as worse than 3 errors

    # Layer 2: ADMET Filter (Toxicity Mask)
    # Check if molecule matches any toxic bits
    is_toxic = (seed & toxic_mask) != 0

    # Layer 3: Informational Docking (Complementarity)
    # Calculate information distance: hamming_weight(molecule_seed XOR target_seed)
    xor_result = seed ^ target_seed
    docking_distance = hamming_weight(xor_result)

    return {
        'chembl_id': molecule['chembl_id'],
        'smiles': molecule['smiles'],
        'seed': seed,
        'seed_hex': f"0x{seed:06X}",
        'syndrome_weight': syndrome_weight,
        'syndrome_correctable': success,
        'is_toxic': is_toxic,
        'docking_distance': docking_distance,
        'signature': molecule['signature']
    }


def rank_candidates(analyzed_molecules: List[Dict]) -> List[Dict]:
    """
    Rank candidates by multiple criteria.

    Ranking priority:
    1. Filter out toxic molecules
    2. Sort by docking_distance (ascending - lower is better)
    3. Then by syndrome_weight (ascending - fewer errors is better)

    Args:
        analyzed_molecules: List of analyzed molecule dictionaries

    Returns:
        Sorted list of non-toxic candidates
    """
    # Filter out toxic molecules
    non_toxic = [m for m in analyzed_molecules if not m['is_toxic']]

    print(f"\nFiltering Results:")
    print(f"  Total molecules analyzed: {len(analyzed_molecules)}")
    print(f"  Toxic molecules filtered out: {len(analyzed_molecules) - len(non_toxic)}")
    print(f"  Non-toxic candidates: {len(non_toxic)}")

    # Sort by docking_distance (primary), then syndrome_weight (secondary)
    ranked = sorted(non_toxic, key=lambda x: (x['docking_distance'], x['syndrome_weight']))

    return ranked


def main():
    """Main execution function."""
    print("=" * 70)
    print("Step 3: Docking/QSAR Layer - First Principles Analysis")
    print("=" * 70)

    # Define paths
    session_dir = Path("/app/sandbox/session_20251211_141515_ba86f641fd8f")
    input_file = session_dir / "workflow" / "chembl_processed.json"
    output_file = session_dir / "workflow" / "analysis_results.json"

    # Load processed data
    data = load_processed_data(str(input_file))
    molecules = data['results']

    # Step 1: Define Analysis Parameters
    print("\n" + "=" * 70)
    print("Analysis Parameters")
    print("=" * 70)

    # Find a perfect candidate from Step 2 to use as target
    # Look for a molecule with all block_counts = 6 (perfect Golay codeword)
    perfect_candidates = [
        m for m in molecules
        if all(count == 6 for count in m['signature']['block_counts'])
    ]

    if perfect_candidates:
        # Use the first perfect candidate as the virtual target
        target_seed = perfect_candidates[0]['seed']
        print(f"  Virtual Target: Using perfect candidate seed = 0x{target_seed:06X}")
        print(f"    ChEMBL ID: {perfect_candidates[0]['chembl_id']}")
        print(f"    Found {len(perfect_candidates)} perfect candidates in dataset")
    else:
        # Fallback: use a specific pattern
        target_seed = 0xAAAAAA  # Alternating bit pattern
        print(f"  Virtual Target: Using fallback pattern = 0x{target_seed:06X}")

    # Define toxicity mask (hypothetical)
    toxic_mask = 0x800001  # First and last bits set
    print(f"  Toxicity Mask: 0x{toxic_mask:06X}")
    print(f"    (Molecules matching this mask will be flagged as toxic)")

    # Step 2: Analyze all molecules
    print("\n" + "=" * 70)
    print("Analyzing Molecules")
    print("=" * 70)

    analyzed_molecules = []
    total = len(molecules)

    for i, molecule in enumerate(molecules):
        if i % 1000 == 0:
            print(f"  Progress: {i}/{total} molecules analyzed ({100*i/total:.1f}%)")

        analysis = analyze_molecule(molecule, target_seed, toxic_mask)
        analyzed_molecules.append(analysis)

    print(f"  Progress: {total}/{total} molecules analyzed (100.0%)")
    print(f"  Analysis complete!")

    # Step 3: Rank and select top candidates
    print("\n" + "=" * 70)
    print("Ranking and Selection")
    print("=" * 70)

    ranked_candidates = rank_candidates(analyzed_molecules)

    # Select Top 20
    top_n = 20
    top_candidates = ranked_candidates[:top_n]

    # Step 4: Save full results
    print("\n" + "=" * 70)
    print("Saving Results")
    print("=" * 70)

    output_data = {
        'metadata': {
            'source': str(input_file),
            'target_seed': target_seed,
            'target_seed_hex': f"0x{target_seed:06X}",
            'toxic_mask': toxic_mask,
            'toxic_mask_hex': f"0x{toxic_mask:06X}",
            'total_analyzed': len(analyzed_molecules),
            'total_toxic': len(analyzed_molecules) - len(ranked_candidates),
            'total_non_toxic': len(ranked_candidates),
            'top_n_selected': top_n
        },
        'all_results': analyzed_molecules,
        'ranked_non_toxic': ranked_candidates,
        'top_candidates': top_candidates
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"  Full analysis saved to: {output_file}")

    # Step 5: Print Top 20 Candidates
    print("\n" + "=" * 70)
    print(f"TOP {top_n} CANDIDATES (Ranked by Information Complementarity)")
    print("=" * 70)
    print()
    print(f"{'Rank':<6} {'ChEMBL ID':<15} {'Docking Dist':<13} {'Syndrome':<10} {'Seed (hex)':<12} {'SMILES':<50}")
    print("-" * 140)

    for i, candidate in enumerate(top_candidates, 1):
        smiles_truncated = candidate['smiles'][:47] + "..." if len(candidate['smiles']) > 50 else candidate['smiles']
        print(f"{i:<6} {candidate['chembl_id']:<15} {candidate['docking_distance']:<13} "
              f"{candidate['syndrome_weight']:<10} {candidate['seed_hex']:<12} {smiles_truncated:<50}")

    # Summary statistics
    print("\n" + "=" * 70)
    print("Summary Statistics for Top 20")
    print("=" * 70)

    docking_distances = [c['docking_distance'] for c in top_candidates]
    syndrome_weights = [c['syndrome_weight'] for c in top_candidates]

    print(f"  Docking Distance Range: {min(docking_distances)} - {max(docking_distances)}")
    print(f"  Average Docking Distance: {sum(docking_distances)/len(docking_distances):.2f}")
    print(f"  Syndrome Weight Range: {min(syndrome_weights)} - {max(syndrome_weights)}")
    print(f"  Perfect Codewords (syndrome=0): {sum(1 for s in syndrome_weights if s == 0)}")
    print(f"  1-Error Correctable (syndrome=1): {sum(1 for s in syndrome_weights if s == 1)}")
    print(f"  2-Error Correctable (syndrome=2): {sum(1 for s in syndrome_weights if s == 2)}")
    print(f"  3-Error Correctable (syndrome=3): {sum(1 for s in syndrome_weights if s == 3)}")

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print(f"\nOutput files:")
    print(f"  - {output_file}")
    print(f"\nNext steps:")
    print(f"  - Review top candidates for further validation")
    print(f"  - Perform detailed structural analysis")
    print(f"  - Validate predictions with experimental data")


if __name__ == "__main__":
    main()
