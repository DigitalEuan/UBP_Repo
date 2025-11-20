#!/usr/bin/env python3.11
"""
================================================================================
UBP 3.6 Comprehensive Viral Genome Coherence Valley Analysis
Author: Euan Craig, New Zealand
Date: November 20, 2025
================================================================================

Analyzes 20+ viral genomes using proper OffBit resonance_toggle methodology:
- 24-bit quantization of genome sequences
- 1000-step resonance_toggle simulation
- k = 0.0002 ± 0.00006 sinusoidal fluctuation
- 14-28 THz frequency range
- Target NRCI > 99.99%

This provides statistical power to detect the coherence valley isomorphism.
"""

import os
import json
import subprocess
from typing import List, Dict, Any, Tuple
import sys
sys.path.insert(0, '.')
import importlib
resonance_sim = importlib.import_module('01_proper_resonance_toggle_simulation')

# Import functions
quantize_to_24bit = resonance_sim.quantize_to_24bit
run_resonance_simulation = resonance_sim.run_resonance_simulation
detect_coherence_valleys = resonance_sim.detect_coherence_valleys
FREQ_MIN_THZ = resonance_sim.FREQ_MIN_THZ
FREQ_MAX_THZ = resonance_sim.FREQ_MAX_THZ

# Old import line (commented out):
# from 01_proper_resonance_toggle_simulation import (...)

# ============================================================================
# VIRAL GENOME DATABASE (20+ Major Human Pathogens)
# ============================================================================

VIRAL_GENOMES = [
    # RNA viruses - Coronaviridae
    {"name": "SARS-CoV-2", "accession": "NC_045512.2", "description": "COVID-19 virus"},
    {"name": "SARS-CoV", "accession": "NC_004718.3", "description": "SARS coronavirus"},
    {"name": "MERS-CoV", "accession": "NC_019843.3", "description": "MERS coronavirus"},
    
    # RNA viruses - Orthomyxoviridae (Influenza)
    {"name": "Influenza_A_H1N1", "accession": "NC_026433.1", "description": "Influenza A H1N1 segment 1"},
    {"name": "Influenza_A_H3N2", "accession": "NC_007366.1", "description": "Influenza A H3N2 segment 1"},
    {"name": "Influenza_B", "accession": "NC_002204.1", "description": "Influenza B segment 1"},
    
    # RNA viruses - Retroviridae
    {"name": "HIV-1", "accession": "NC_001802.1", "description": "Human immunodeficiency virus 1"},
    {"name": "HIV-2", "accession": "NC_001722.1", "description": "Human immunodeficiency virus 2"},
    
    # RNA viruses - Flaviviridae
    {"name": "Dengue_virus_1", "accession": "NC_001477.1", "description": "Dengue virus type 1"},
    {"name": "Zika_virus", "accession": "NC_012532.1", "description": "Zika virus"},
    {"name": "West_Nile_virus", "accession": "NC_001563.2", "description": "West Nile virus"},
    {"name": "Hepatitis_C", "accession": "NC_004102.1", "description": "Hepatitis C virus"},
    
    # RNA viruses - Filoviridae
    {"name": "Ebola_Zaire", "accession": "NC_002549.1", "description": "Ebola virus Zaire"},
    {"name": "Marburg_virus", "accession": "NC_001608.3", "description": "Marburg virus"},
    
    # RNA viruses - Paramyxoviridae
    {"name": "Measles_virus", "accession": "NC_001498.1", "description": "Measles virus"},
    {"name": "Mumps_virus", "accession": "NC_002200.1", "description": "Mumps virus"},
    
    # DNA viruses - Herpesviridae
    {"name": "HSV-1", "accession": "NC_001806.2", "description": "Herpes simplex virus 1"},
    {"name": "HSV-2", "accession": "NC_001798.2", "description": "Herpes simplex virus 2"},
    {"name": "Varicella_zoster", "accession": "NC_001348.1", "description": "Varicella-zoster virus"},
    {"name": "Epstein_Barr", "accession": "NC_007605.1", "description": "Epstein-Barr virus"},
    
    # DNA viruses - Poxviridae
    {"name": "Vaccinia_virus", "accession": "NC_006998.1", "description": "Vaccinia virus"},
    {"name": "Monkeypox_virus", "accession": "NC_063383.1", "description": "Monkeypox virus"},
    
    # DNA viruses - Hepadnaviridae
    {"name": "Hepatitis_B", "accession": "NC_003977.2", "description": "Hepatitis B virus"},
    
    # DNA viruses - Papillomaviridae
    {"name": "HPV-16", "accession": "NC_001526.4", "description": "Human papillomavirus 16"},
    {"name": "HPV-18", "accession": "NC_001357.1", "description": "Human papillomavirus 18"},
]

# ============================================================================
# GENOME DOWNLOAD
# ============================================================================

def download_viral_genome(accession: str, output_dir: str) -> str:
    """
    Download viral genome from NCBI using efetch.
    
    Args:
        accession: NCBI accession number
        output_dir: Directory to save FASTA file
        
    Returns:
        Path to downloaded FASTA file
    """
    output_file = os.path.join(output_dir, f"{accession}.fasta")
    
    if os.path.exists(output_file):
        print(f"  Already downloaded: {accession}")
        return output_file
    
    print(f"  Downloading: {accession}")
    
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text"
    
    try:
        subprocess.run(
            ["curl", "-s", url, "-o", output_file],
            check=True,
            timeout=30
        )
        print(f"  Downloaded: {output_file}")
        return output_file
    except Exception as e:
        print(f"  ERROR downloading {accession}: {e}")
        return None


def download_all_genomes(output_dir: str) -> Dict[str, str]:
    """
    Download all viral genomes.
    
    Returns:
        Dictionary mapping virus names to FASTA file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    genome_files = {}
    
    print("=" * 80)
    print(f"Downloading {len(VIRAL_GENOMES)} viral genomes from NCBI")
    print("=" * 80)
    
    for virus in VIRAL_GENOMES:
        name = virus['name']
        accession = virus['accession']
        
        file_path = download_viral_genome(accession, output_dir)
        if file_path:
            genome_files[name] = file_path
    
    print()
    print(f"Successfully downloaded {len(genome_files)}/{len(VIRAL_GENOMES)} genomes")
    print()
    
    return genome_files


# ============================================================================
# GENOME SEQUENCE PROCESSING
# ============================================================================

def read_fasta_sequence(fasta_file: str) -> str:
    """
    Read genome sequence from FASTA file.
    
    Args:
        fasta_file: Path to FASTA file
        
    Returns:
        Genome sequence (uppercase, no whitespace)
    """
    with open(fasta_file, 'r') as f:
        lines = f.readlines()
    
    # Skip header lines (starting with >)
    sequence_lines = [line.strip() for line in lines if not line.startswith('>')]
    sequence = ''.join(sequence_lines).upper()
    
    return sequence


def sequence_to_frequency_pattern(sequence: str, min_freq_thz: float = FREQ_MIN_THZ, 
                                 max_freq_thz: float = FREQ_MAX_THZ) -> List[float]:
    """
    Convert genome sequence to frequency pattern in THz range.
    
    Maps nucleotides to frequencies:
    - A (Adenine): 14 THz (minimum)
    - T/U (Thymine/Uracil): 18 THz
    - G (Guanine): 22 THz
    - C (Cytosine): 28 THz (maximum)
    
    Args:
        sequence: Genome sequence
        min_freq_thz: Minimum frequency (THz)
        max_freq_thz: Maximum frequency (THz)
        
    Returns:
        List of frequencies (THz)
    """
    # Nucleotide to frequency mapping
    nucleotide_freqs = {
        'A': min_freq_thz,
        'T': min_freq_thz + (max_freq_thz - min_freq_thz) * 0.286,  # 18 THz
        'U': min_freq_thz + (max_freq_thz - min_freq_thz) * 0.286,  # 18 THz (RNA)
        'G': min_freq_thz + (max_freq_thz - min_freq_thz) * 0.571,  # 22 THz
        'C': max_freq_thz,
    }
    
    frequencies = []
    for nucleotide in sequence:
        if nucleotide in nucleotide_freqs:
            frequencies.append(nucleotide_freqs[nucleotide])
        else:
            # Unknown nucleotide - use middle frequency
            frequencies.append((min_freq_thz + max_freq_thz) / 2.0)
    
    return frequencies


# ============================================================================
# VIRAL GENOME COHERENCE ANALYSIS
# ============================================================================

def analyze_viral_genome(virus_name: str, fasta_file: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Analyze a single viral genome for coherence valleys.
    
    Args:
        virus_name: Name of virus
        fasta_file: Path to FASTA file
        verbose: Print progress
        
    Returns:
        Dictionary with analysis results
    """
    if verbose:
        print(f"\nAnalyzing: {virus_name}")
        print(f"  FASTA: {fasta_file}")
    
    # Read sequence
    sequence = read_fasta_sequence(fasta_file)
    genome_length = len(sequence)
    
    if verbose:
        print(f"  Genome length: {genome_length:,} bp")
    
    # Convert to frequency pattern
    frequencies = sequence_to_frequency_pattern(sequence)
    avg_frequency = sum(frequencies) / len(frequencies)
    
    if verbose:
        print(f"  Average frequency: {avg_frequency:.2f} THz")
    
    # Sample genome at regular intervals (use 100 samples for analysis)
    sample_size = min(100, genome_length)
    step = max(1, genome_length // sample_size)
    sampled_frequencies = frequencies[::step][:sample_size]
    
    # Run resonance simulation for each sampled frequency
    results = []
    for i, freq_thz in enumerate(sampled_frequencies):
        # Quantize frequency to 24-bit
        quantized = quantize_to_24bit(freq_thz, FREQ_MIN_THZ, FREQ_MAX_THZ)
        
        # Run simulation
        offbit, stats = run_resonance_simulation(quantized, freq_thz, verbose=False)
        
        results.append(stats)
        
        if verbose and (i + 1) % 20 == 0:
            print(f"    Processed {i+1}/{len(sampled_frequencies)} samples")
    
    # Aggregate results
    avg_deficit = sum(r['coherence_valley_deficit_percent'] for r in results) / len(results)
    min_deficit = min(r['coherence_valley_deficit_percent'] for r in results)
    max_deficit = max(r['coherence_valley_deficit_percent'] for r in results)
    avg_nrci = sum(r['final_nrci'] for r in results) / len(results)
    
    analysis = {
        'virus_name': virus_name,
        'genome_length': genome_length,
        'average_frequency_thz': avg_frequency,
        'samples_analyzed': len(results),
        'coherence_valley_deficit_percent': avg_deficit,
        'deficit_min': min_deficit,
        'deficit_max': max_deficit,
        'average_final_nrci': avg_nrci,
        'nrci_target_met': avg_nrci >= 0.9999,
        'detailed_results': results
    }
    
    if verbose:
        print(f"  Coherence valley deficit: {avg_deficit:.6f}%")
        print(f"  Average final NRCI: {avg_nrci:.10f}")
        print(f"  Target met: {analysis['nrci_target_met']}")
    
    return analysis


# ============================================================================
# BATCH ANALYSIS
# ============================================================================

def analyze_all_viral_genomes(genome_files: Dict[str, str], output_file: str) -> List[Dict[str, Any]]:
    """
    Analyze all viral genomes.
    
    Args:
        genome_files: Dictionary mapping virus names to FASTA files
        output_file: Path to save results JSON
        
    Returns:
        List of analysis results
    """
    print("=" * 80)
    print(f"Analyzing {len(genome_files)} viral genomes")
    print("=" * 80)
    
    all_results = []
    
    for i, (virus_name, fasta_file) in enumerate(genome_files.items(), 1):
        print(f"\n[{i}/{len(genome_files)}] {virus_name}")
        
        try:
            result = analyze_viral_genome(virus_name, fasta_file, verbose=True)
            all_results.append(result)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    # Save results
    print()
    print("=" * 80)
    print("Saving results")
    print("=" * 80)
    
    # Remove detailed_results for summary (too large)
    summary_results = []
    for result in all_results:
        summary = {k: v for k, v in result.items() if k != 'detailed_results'}
        summary_results.append(summary)
    
    with open(output_file, 'w') as f:
        json.dump(summary_results, f, indent=2)
    
    print(f"Saved: {output_file}")
    
    # Print summary statistics
    print()
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    deficits = [r['coherence_valley_deficit_percent'] for r in all_results]
    nrcis = [r['average_final_nrci'] for r in all_results]
    
    print(f"Total viruses analyzed: {len(all_results)}")
    print()
    print(f"Coherence valley deficit:")
    print(f"  Mean: {sum(deficits)/len(deficits):.6f}%")
    print(f"  Min: {min(deficits):.6f}%")
    print(f"  Max: {max(deficits):.6f}%")
    print(f"  Std dev: {(sum((d - sum(deficits)/len(deficits))**2 for d in deficits) / len(deficits))**0.5:.6f}%")
    print()
    print(f"Average final NRCI:")
    print(f"  Mean: {sum(nrcis)/len(nrcis):.10f}")
    print(f"  Min: {min(nrcis):.10f}")
    print(f"  Max: {max(nrcis):.10f}")
    print()
    print(f"NRCI > 99.99% target met: {sum(1 for r in all_results if r['nrci_target_met'])}/{len(all_results)}")
    
    return all_results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Main execution function.
    """
    # Setup directories
    data_dir = "../data"
    results_dir = "../results"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Download genomes
    genome_files = download_all_genomes(data_dir)
    
    if not genome_files:
        print("ERROR: No genomes downloaded")
        return
    
    # Analyze genomes
    results = analyze_all_viral_genomes(
        genome_files,
        os.path.join(results_dir, "viral_coherence_valleys_20plus.json")
    )
    
    print()
    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
