#!/usr/bin/env python3
"""
ChEMBL Data Processing: SMILES → UBP Signatures
================================================

This script processes the ChEMBL dataset by converting chemical structures (SMILES)
into UBP Signatures using the UBP Core library.

Pipeline:
1. SMILES → RDKit Molecule
2. RDKit Molecule → Morgan Fingerprint (radius=2, 24 bits)
3. Fingerprint → 24-bit Seed (integer)
4. Seed → OffBit → UBP Signature

Author: K-Dense System
Date: December 11, 2025
"""

import csv
import json
import sys
from pathlib import Path

# RDKit imports for "sensory" transduction
from rdkit import Chem
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

# UBP Core imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from ubp_core import OffBit, observe_offbit


def smiles_to_24bit(smiles: str, morgan_gen) -> int:
    """
    Convert SMILES string to 24-bit seed using Morgan fingerprint.

    This is the "sensory transduction" step - converting external chemical
    information into a UBP-compatible 24-bit seed.

    Args:
        smiles: SMILES string representation of molecule
        morgan_gen: Pre-initialized Morgan fingerprint generator

    Returns:
        24-bit integer seed (0 if conversion fails)
    """
    try:
        # Validate input
        if not smiles or not isinstance(smiles, str) or smiles.strip() == "":
            return 0

        # Convert SMILES to RDKit molecule
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return 0

        # Generate 24-bit Morgan fingerprint
        fp = morgan_gen.GetFingerprint(mol)

        # Convert to integer
        seed = int(fp.ToBitString(), 2)
        return seed

    except Exception as e:
        # Gracefully handle any conversion errors
        print(f"Warning: Failed to convert SMILES '{smiles[:50]}...': {e}", file=sys.stderr)
        return 0


def process_chembl_to_ubp_signatures(
    input_csv: Path,
    output_json: Path,
    progress_interval: int = 100
):
    """
    Process ChEMBL CSV and generate UBP signatures for all molecules.

    Args:
        input_csv: Path to chembl_sample.csv
        output_json: Path to output JSON file
        progress_interval: Print progress every N molecules
    """
    print("=" * 70)
    print("ChEMBL → UBP Signature Processing")
    print("=" * 70)
    print(f"Input:  {input_csv}")
    print(f"Output: {output_json}")
    print()

    # Initialize Morgan fingerprint generator (radius=2, 24 bits)
    # This matches the original Information Frigate v1.3 notebook
    print("Initializing Morgan fingerprint generator (radius=2, fpSize=24)...")
    morgan_generator = GetMorganGenerator(radius=2, fpSize=24)
    print("✓ Generator ready")
    print()

    # Process molecules
    results = []
    processed = 0
    failed = 0
    zero_seeds = 0

    print("Processing molecules...")
    print("-" * 70)

    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, 1):
            chembl_id = row.get('chembl_id', '')
            smiles = row.get('canonical_smiles', '')

            # Step 1: SMILES → 24-bit Seed (Sensory Transduction)
            seed = smiles_to_24bit(smiles, morgan_generator)

            if seed == 0:
                zero_seeds += 1

            # Step 2: Seed → OffBit → Signature (UBP Engine)
            try:
                offbit = OffBit.from_int(width=24, value=seed)
                signature = observe_offbit(offbit, block_size=6, rotate_by=5)

                # Store results
                results.append({
                    'chembl_id': chembl_id,
                    'smiles': smiles,
                    'seed': seed,
                    'signature': {
                        'block_counts': list(signature.block_counts),
                        'rotated_hash': signature.rotated_hash,
                        'parity_vector': list(signature.parity_vector)
                    }
                })

                processed += 1

            except Exception as e:
                print(f"Error processing {chembl_id}: {e}", file=sys.stderr)
                failed += 1

            # Progress indicator
            if i % progress_interval == 0:
                print(f"Progress: {i:>6,} molecules processed "
                      f"({processed:>6,} successful, {zero_seeds:>5,} zero seeds, {failed:>3,} failed)")

    print("-" * 70)
    print(f"✓ Processing complete!")
    print()

    # Summary statistics
    print("Summary:")
    print(f"  Total molecules:    {processed + failed:>6,}")
    print(f"  Successful:         {processed:>6,}")
    print(f"  Failed:             {failed:>6,}")
    print(f"  Zero seeds:         {zero_seeds:>6,} (invalid SMILES)")
    print()

    # Save results
    print(f"Saving results to {output_json}...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'source': str(input_csv),
                'total_molecules': processed + failed,
                'successful': processed,
                'failed': failed,
                'zero_seeds': zero_seeds,
                'morgan_radius': 2,
                'morgan_fpsize': 24,
                'ubp_block_size': 6,
                'ubp_rotate_by': 5
            },
            'results': results
        }, f, indent=2)

    print(f"✓ Saved {len(results):,} signatures to {output_json}")
    print()
    print("=" * 70)
    print("Processing complete!")
    print("=" * 70)


def main():
    """Main execution function."""
    # Define paths
    base_dir = Path(__file__).parent.parent
    input_csv = base_dir / "user_data" / "chembl_sample.csv"
    output_json = base_dir / "workflow" / "chembl_processed.json"

    # Validate input exists
    if not input_csv.exists():
        print(f"ERROR: Input file not found: {input_csv}", file=sys.stderr)
        sys.exit(1)

    # Process
    process_chembl_to_ubp_signatures(
        input_csv=input_csv,
        output_json=output_json,
        progress_interval=100
    )


if __name__ == "__main__":
    main()
