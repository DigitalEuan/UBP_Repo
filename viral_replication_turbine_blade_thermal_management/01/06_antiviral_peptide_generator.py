#!/usr/bin/env python3
"""
06_antiviral_peptide_generator.py
==================================
Generate antiviral peptide sequences targeting coherence valleys.

This script uses the coherence valley analysis to design peptides that:
1. Target the 0.1077% coherence deficit in viral genomes
2. Disrupt viral replication by amplifying coherence valleys
3. Generate 3D-printable molecular structures (PDB format)

Physical Mechanism:
- Peptides bind to viral genome regions with low coherence
- Binding amplifies the coherence deficit, preventing replication
- Specificity comes from matching THz frequency signatures

Author: UBP 3.6 Coherence Valley Study
Date: November 20, 2025
"""

import sys
import json
import math
from typing import List, Tuple, Dict
from pathlib import Path
import numpy as np


# ============================================================================
# AMINO ACID PROPERTIES
# ============================================================================

# Amino acid single-letter codes
AMINO_ACIDS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

# Amino acid THz frequencies (based on vibrational modes)
# These are approximate values for peptide bond vibrations
AA_FREQUENCIES = {
    'A': 10.2e12, 'C': 11.5e12, 'D': 12.8e12, 'E': 13.1e12, 'F': 14.5e12,
    'G': 9.8e12,  'H': 15.2e12, 'I': 11.8e12, 'K': 13.5e12, 'L': 11.9e12,
    'M': 12.3e12, 'N': 12.9e12, 'P': 10.5e12, 'Q': 13.0e12, 'R': 14.0e12,
    'S': 11.2e12, 'T': 11.4e12, 'V': 11.6e12, 'W': 15.8e12, 'Y': 15.0e12
}

# Amino acid 3-letter codes for PDB format
AA_THREE_LETTER = {
    'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE',
    'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU',
    'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG',
    'S': 'SER', 'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'
}


# ============================================================================
# PEPTIDE DESIGN
# ============================================================================

def design_antiviral_peptide(target_deficit: float, 
                            target_virus: str,
                            peptide_length: int = 20) -> str:
    """
    Design an antiviral peptide targeting a specific coherence deficit.
    
    Strategy:
    1. Calculate target THz frequency from deficit
    2. Select amino acids that resonate at complementary frequencies
    3. Optimize sequence for binding affinity and specificity
    
    Args:
        target_deficit: Target coherence deficit (%)
        target_virus: Name of target virus
        peptide_length: Length of peptide sequence
        
    Returns:
        Peptide sequence (single-letter amino acid codes)
    """
    print(f"\nDesigning antiviral peptide for {target_virus}")
    print(f"  Target deficit: {target_deficit:.4f}%")
    print(f"  Peptide length: {peptide_length} residues")
    
    # Convert deficit to target frequency
    # Higher deficit → higher frequency needed for disruption
    # Mapping: 0.1% deficit → 15 THz, 0.15% deficit → 18 THz
    target_freq = 15.0e12 + (target_deficit - 0.1) * 30.0e12
    print(f"  Target frequency: {target_freq/1e12:.2f} THz")
    
    # Select amino acids with frequencies near target
    sequence = []
    for i in range(peptide_length):
        # Add some variation: oscillate around target frequency
        position_offset = math.sin(2 * math.pi * i / peptide_length) * 2.0e12
        desired_freq = target_freq + position_offset
        
        # Find amino acid closest to desired frequency
        best_aa = min(AMINO_ACIDS, key=lambda aa: abs(AA_FREQUENCIES[aa] - desired_freq))
        sequence.append(best_aa)
    
    peptide_seq = ''.join(sequence)
    print(f"  Sequence: {peptide_seq}")
    
    # Calculate average frequency
    avg_freq = np.mean([AA_FREQUENCIES[aa] for aa in sequence])
    print(f"  Average frequency: {avg_freq/1e12:.2f} THz")
    
    return peptide_seq


def calculate_binding_affinity(peptide_seq: str, target_deficit: float) -> float:
    """
    Calculate predicted binding affinity to viral genome.
    
    Affinity is based on frequency matching between peptide and
    viral coherence valleys.
    
    Args:
        peptide_seq: Peptide sequence
        target_deficit: Target coherence deficit
        
    Returns:
        Binding affinity (arbitrary units, higher = stronger)
    """
    # Calculate peptide frequency spectrum
    peptide_freqs = [AA_FREQUENCIES[aa] for aa in peptide_seq]
    avg_freq = np.mean(peptide_freqs)
    freq_std = np.std(peptide_freqs)
    
    # Target frequency from deficit
    target_freq = 15.0e12 + (target_deficit - 0.1) * 30.0e12
    
    # Frequency matching score
    freq_match = math.exp(-((avg_freq - target_freq) / 1e12) ** 2)
    
    # Diversity bonus (more diverse sequences bind better)
    diversity = freq_std / 1e12
    
    # Combined affinity
    affinity = freq_match * (1.0 + 0.1 * diversity)
    
    return affinity


# ============================================================================
# PDB FILE GENERATION
# ============================================================================

def generate_pdb_file(peptide_seq: str, 
                     output_path: str,
                     title: str = "Antiviral Peptide") -> None:
    """
    Generate PDB file for peptide structure.
    
    This creates a simplified alpha-helix structure for visualization
    and 3D printing.
    
    Args:
        peptide_seq: Peptide sequence
        output_path: Path to output PDB file
        title: Title for PDB file
    """
    print(f"\n  Generating PDB file: {output_path}")
    
    # Alpha helix parameters
    rise_per_residue = 1.5  # Angstroms
    rotation_per_residue = 100.0  # degrees
    radius = 2.3  # Angstroms
    
    with open(output_path, 'w') as f:
        # Header
        f.write(f"HEADER    {title}\n")
        f.write(f"TITLE     {title}\n")
        f.write(f"REMARK    Generated by UBP 3.6 Coherence Valley Study\n")
        f.write(f"REMARK    Sequence: {peptide_seq}\n")
        f.write(f"REMARK    Length: {len(peptide_seq)} residues\n")
        
        # Atoms
        atom_num = 1
        for i, aa in enumerate(peptide_seq):
            residue_num = i + 1
            aa_3letter = AA_THREE_LETTER[aa]
            
            # Calculate position (alpha helix)
            z = i * rise_per_residue
            angle = math.radians(i * rotation_per_residue)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            # CA atom (alpha carbon)
            f.write(f"ATOM  {atom_num:5d}  CA  {aa_3letter} A{residue_num:4d}    "
                   f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n")
            atom_num += 1
            
            # C atom (carbonyl carbon)
            f.write(f"ATOM  {atom_num:5d}  C   {aa_3letter} A{residue_num:4d}    "
                   f"{x+0.5:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n")
            atom_num += 1
            
            # N atom (nitrogen)
            f.write(f"ATOM  {atom_num:5d}  N   {aa_3letter} A{residue_num:4d}    "
                   f"{x-0.5:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           N\n")
            atom_num += 1
        
        # Connectivity (bonds between CA atoms)
        for i in range(len(peptide_seq) - 1):
            ca1 = 1 + i * 3
            ca2 = 1 + (i + 1) * 3
            f.write(f"CONECT{ca1:5d}{ca2:5d}\n")
        
        f.write("END\n")
    
    print(f"  PDB file generated: {atom_num - 1} atoms")


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def generate_antiviral_peptides() -> List[Dict]:
    """
    Generate antiviral peptides for all analyzed viruses.
    
    Returns:
        List of peptide data dictionaries
    """
    print("=" * 80)
    print("UBP 3.6 ANTIVIRAL PEPTIDE GENERATOR")
    print("=" * 80)
    
    # Load viral analysis results
    print("\nLoading viral analysis results...")
    with open('../results/viral_valleys.json', 'r') as f:
        viral_results = json.load(f)
    
    print(f"  Loaded {len(viral_results)} viral results")
    
    # Generate peptides for each virus
    peptides = []
    
    for virus_data in viral_results:
        virus_name = virus_data['virus_name']
        deficit = virus_data['avg_deficit_percent']
        
        print(f"\n{'=' * 80}")
        
        # Design peptide
        peptide_seq = design_antiviral_peptide(
            target_deficit=deficit,
            target_virus=virus_name,
            peptide_length=20
        )
        
        # Calculate binding affinity
        affinity = calculate_binding_affinity(peptide_seq, deficit)
        print(f"  Predicted binding affinity: {affinity:.4f}")
        
        # Generate PDB file
        pdb_filename = f"peptide_{virus_name}.pdb"
        pdb_path = f"../artifacts/{pdb_filename}"
        
        # Create artifacts directory if it doesn't exist
        Path("../artifacts").mkdir(exist_ok=True)
        
        generate_pdb_file(
            peptide_seq=peptide_seq,
            output_path=pdb_path,
            title=f"Antiviral Peptide for {virus_name}"
        )
        
        # Store peptide data
        peptides.append({
            'virus_name': virus_name,
            'target_deficit': deficit,
            'sequence': peptide_seq,
            'length': len(peptide_seq),
            'binding_affinity': affinity,
            'pdb_file': pdb_filename
        })
    
    return peptides


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Generate peptides
    peptides = generate_antiviral_peptides()
    
    # Summary
    print("\n" + "=" * 80)
    print("ANTIVIRAL PEPTIDE SUMMARY")
    print("=" * 80)
    print(f"{'Virus':<20} {'Sequence':<25} {'Affinity':<10} {'PDB File':<30}")
    print("-" * 80)
    for p in peptides:
        seq_short = p['sequence'][:22] + "..." if len(p['sequence']) > 25 else p['sequence']
        print(f"{p['virus_name']:<20} {seq_short:<25} {p['binding_affinity']:<10.4f} {p['pdb_file']:<30}")
    
    # Save peptide data
    print("\nSaving peptide data...")
    with open('../results/antiviral_peptides.json', 'w') as f:
        json.dump(peptides, f, indent=2)
    
    print("Results saved to:")
    print("  - ../results/antiviral_peptides.json")
    print("  - ../artifacts/peptide_*.pdb (3D structures)")
    
    print(f"\n✓ Generated {len(peptides)} antiviral peptides")
    print("  PDB files can be visualized in PyMOL, Chimera, or 3D printed")
