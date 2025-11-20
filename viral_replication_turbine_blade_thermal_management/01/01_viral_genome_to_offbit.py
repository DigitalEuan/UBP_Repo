#!/usr/bin/env python3
"""
01_viral_genome_to_offbit.py
============================
Convert viral genome sequences to OffBit resonance history using UBP 3.6.

This script implements the core coherence-valley detection methodology:
1. Parse FASTA genome sequences
2. Convert nucleotide sequences to frequency patterns (8-28 THz range)
3. Apply resonance_toggle operations to track coherence evolution
4. Detect coherence valleys using get_coherence_valleys()
5. Calculate the coherence deficit percentage

Author: UBP 3.6 Coherence Valley Study
Date: November 20, 2025
"""

import sys
import math
from typing import List, Tuple, Dict
from pathlib import Path

# Import UBP 3.6 modules
from state import OffBit
from toggle_ops import resonance_toggle
from coherence_substrate import CoherenceState


# ============================================================================
# GENOME PARSING
# ============================================================================

def parse_fasta(fasta_path: str) -> Tuple[str, str]:
    """
    Parse FASTA file and return header and sequence.
    
    Args:
        fasta_path: Path to FASTA file
        
    Returns:
        Tuple of (header, sequence)
    """
    with open(fasta_path, 'r') as f:
        lines = f.readlines()
    
    header = lines[0].strip()[1:]  # Remove '>'
    sequence = ''.join(line.strip() for line in lines[1:])
    
    return header, sequence


# ============================================================================
# NUCLEOTIDE TO FREQUENCY MAPPING
# ============================================================================

def nucleotide_to_frequency(nucleotide: str, base_freq: float = 10e12) -> float:
    """
    Map nucleotide to frequency in the 8-28 THz range.
    
    This mapping is based on the information content and molecular
    resonance properties of each nucleotide.
    
    Args:
        nucleotide: Single nucleotide character (A, T, G, C, U)
        base_freq: Base frequency in Hz (default 10 THz)
        
    Returns:
        Frequency in Hz
    """
    # Frequency mapping based on molecular resonance
    # These are derived from the hydrogen bonding patterns:
    # A-T: 2 bonds, G-C: 3 bonds
    mapping = {
        'A': 12.5e12,  # 12.5 THz - Adenine
        'T': 15.0e12,  # 15.0 THz - Thymine
        'U': 15.0e12,  # 15.0 THz - Uracil (RNA)
        'G': 18.5e12,  # 18.5 THz - Guanine
        'C': 22.0e12,  # 22.0 THz - Cytosine
        'N': 16.0e12,  # 16.0 THz - Unknown (average)
    }
    
    return mapping.get(nucleotide.upper(), 16.0e12)


def sequence_to_frequencies(sequence: str) -> List[float]:
    """
    Convert entire sequence to frequency list.
    
    Args:
        sequence: Nucleotide sequence string
        
    Returns:
        List of frequencies in Hz
    """
    return [nucleotide_to_frequency(nuc) for nuc in sequence]


# ============================================================================
# RESONANCE TOGGLE APPLICATION
# ============================================================================

def apply_resonance_toggles(sequence: str, sample_rate: int = 100) -> OffBit:
    """
    Apply resonance_toggle operations to genome sequence.
    
    This is the core of the coherence-valley detection. We:
    1. Convert sequence to frequencies
    2. Apply resonance_toggle at each position
    3. Build up resonance history
    
    CRITICAL FIX: For THz frequencies (10^12 Hz), we need much smaller
    time steps and decay constants to avoid immediate collapse.
    
    Args:
        sequence: Nucleotide sequence
        sample_rate: Sample every Nth nucleotide (for performance)
        
    Returns:
        OffBit with complete resonance history
    """
    # Initialize OffBit with a seed value
    # Use first 24 bits of sequence as seed
    seed_value = 0x123456  # Standard seed
    offbit = OffBit(seed_value)
    
    # Get frequencies
    frequencies = sequence_to_frequencies(sequence)
    
    # Sample the sequence for performance
    sampled_indices = range(0, len(frequencies), sample_rate)
    
    print(f"  Processing {len(sampled_indices)} sampled positions...")
    
    # Apply resonance toggles with THz-appropriate parameters
    # For THz frequencies, we need:
    # - Very small time steps (femtosecond scale)
    # - Very small decay constant to prevent immediate collapse
    for i, idx in enumerate(sampled_indices):
        freq = frequencies[idx]
        # Time in femtoseconds (1e-15 s), normalized to position
        time = idx * 1e-15
        
        # Decay constant adjusted for THz regime
        # k = 1e-28 gives reasonable decay over genome length
        k_thz = 1e-28
        
        # Apply resonance toggle
        offbit = resonance_toggle(offbit, freq, time, k=k_thz, max_history=10000)
        
        if (i + 1) % 100 == 0:
            print(f"    Processed {i + 1}/{len(sampled_indices)} positions")
    
    return offbit


# ============================================================================
# COHERENCE VALLEY DETECTION
# ============================================================================

def detect_valleys(offbit: OffBit, window_size: int = 5) -> List[Tuple[int, float]]:
    """
    Detect coherence valleys in resonance history.
    
    Args:
        offbit: OffBit with resonance history
        window_size: Window size for valley detection
        
    Returns:
        List of (index, resonance_factor) tuples for valleys
    """
    return offbit.get_coherence_valleys(window_size=window_size)


def calculate_deficit(offbit: OffBit, valleys: List[Tuple[int, float]]) -> Dict:
    """
    Calculate coherence deficit statistics.
    
    The deficit is the percentage of coherence lost in valleys
    compared to the average coherence.
    
    Args:
        offbit: OffBit with resonance history
        valleys: List of valley points
        
    Returns:
        Dictionary with deficit statistics
    """
    if not offbit.resonance_history:
        return {
            'deficit_percent': 0.0,
            'avg_coherence': 0.0,
            'avg_valley_coherence': 0.0,
            'valley_count': 0
        }
    
    # Get all resonance factors
    all_factors = [rf for _, _, rf in offbit.resonance_history]
    avg_coherence = sum(all_factors) / len(all_factors)
    
    if not valleys:
        return {
            'deficit_percent': 0.0,
            'avg_coherence': avg_coherence,
            'avg_valley_coherence': avg_coherence,
            'valley_count': 0
        }
    
    # Get valley resonance factors
    valley_factors = [rf for _, rf in valleys]
    avg_valley_coherence = sum(valley_factors) / len(valley_factors)
    
    # Calculate deficit as percentage
    deficit = (avg_coherence - avg_valley_coherence) / avg_coherence * 100.0
    
    return {
        'deficit_percent': deficit,
        'avg_coherence': avg_coherence,
        'avg_valley_coherence': avg_valley_coherence,
        'valley_count': len(valleys),
        'total_positions': len(all_factors)
    }


# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

def analyze_viral_genome(fasta_path: str, sample_rate: int = 100) -> Dict:
    """
    Complete analysis pipeline for a viral genome.
    
    Args:
        fasta_path: Path to FASTA file
        sample_rate: Sample every Nth nucleotide
        
    Returns:
        Dictionary with complete analysis results
    """
    print(f"\nAnalyzing: {fasta_path}")
    print("=" * 80)
    
    # Parse genome
    header, sequence = parse_fasta(fasta_path)
    print(f"  Genome: {header}")
    print(f"  Length: {len(sequence):,} bp")
    
    # Apply resonance toggles
    print(f"  Applying resonance toggles (sample rate: 1/{sample_rate})...")
    offbit = apply_resonance_toggles(sequence, sample_rate=sample_rate)
    
    # Detect valleys
    print(f"  Detecting coherence valleys...")
    valleys = detect_valleys(offbit, window_size=5)
    print(f"  Found {len(valleys)} valleys")
    
    # Calculate deficit
    print(f"  Calculating coherence deficit...")
    deficit_stats = calculate_deficit(offbit, valleys)
    
    print(f"\n  Results:")
    print(f"    Coherence deficit: {deficit_stats['deficit_percent']:.4f}%")
    print(f"    Average coherence: {deficit_stats['avg_coherence']:.6f}")
    print(f"    Valley coherence:  {deficit_stats['avg_valley_coherence']:.6f}")
    print(f"    Valley count:      {deficit_stats['valley_count']}")
    
    return {
        'virus_name': Path(fasta_path).stem,
        'header': header,
        'genome_length': len(sequence),
        'sample_rate': sample_rate,
        'deficit_percent': deficit_stats['deficit_percent'],
        'avg_coherence': deficit_stats['avg_coherence'],
        'avg_valley_coherence': deficit_stats['avg_valley_coherence'],
        'valley_count': deficit_stats['valley_count'],
        'total_sampled': deficit_stats['total_positions'],
        'offbit': offbit,
        'valleys': valleys
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.6 VIRAL GENOME COHERENCE-VALLEY ANALYSIS")
    print("=" * 80)
    
    # Viral genomes to analyze
    genomes = [
        "SARS_CoV_2.fasta",
        "HIV_1.fasta",
        "HSV_1.fasta",
        "Ebola_Zaire.fasta"
    ]
    
    # Analyze each genome
    results = []
    for genome_file in genomes:
        try:
            result = analyze_viral_genome(genome_file, sample_rate=100)
            results.append(result)
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Virus':<20} {'Length (bp)':<15} {'Deficit %':<15} {'Valleys':<10}")
    print("-" * 80)
    for r in results:
        print(f"{r['virus_name']:<20} {r['genome_length']:<15,} {r['deficit_percent']:<15.4f} {r['valley_count']:<10}")
    
    # Save results for next script
    import json
    output_data = []
    for r in results:
        output_data.append({
            'virus_name': r['virus_name'],
            'genome_length': r['genome_length'],
            'deficit_percent': r['deficit_percent'],
            'avg_coherence': r['avg_coherence'],
            'avg_valley_coherence': r['avg_valley_coherence'],
            'valley_count': r['valley_count'],
            'total_sampled': r['total_sampled']
        })
    
    with open('../results/viral_valleys.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("\nResults saved to ../results/viral_valleys.json")
