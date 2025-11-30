"""
================================================================================
UBP Antibiotic Super-Rabbit Analyzer
Author: Euan R A Craig, New Zealand - # Powered by UBP 3.7.1
Date: 30 November 2025
================================================================================

Analyze super-rabbits from the discovery study and rank them by
antibiotic-likeness based on known antibiotic signatures.
"""

import sys
import json
import re
from typing import List, Dict, Tuple
from collections import defaultdict

sys.path.insert(0, '/home/ubuntu/UBP_Repo/gpu_ubp_system/03/core')
from state import OffBit

# Known antibiotics (from reverse engineering study)
KNOWN_ANTIBIOTICS = {
    "Penicillin": 0x1A4F3C,
    "Tetracycline": 0x6C9E2A,
    "Ciprofloxacin": 0xA3D5B1,
    "Vancomycin": 0xE8F142,
    "Streptomycin": 0x4B7D91,
    "Erythromycin": 0x9C2F68,
    "Chloramphenicol": 0x5E8A3D,
    "Linezolid": 0xA77F3C
}


def parse_superrabbits_from_log(log_path: str, max_count: int = None) -> List[Tuple[int, float]]:
    """
    Parse super-rabbits from study log.
    
    Args:
        log_path: Path to study output log
        max_count: Maximum number to parse (None = all)
        
    Returns:
        List of (offbit_value, nrci) tuples
    """
    pattern = r"Super-rabbit found! (0x[0-9A-F]+) \(NRCI: ([0-9.]+)\)"
    
    superrabbits = []
    with open(log_path, 'r') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                hex_val = match.group(1)
                nrci = float(match.group(2))
                offbit_value = int(hex_val, 16)
                superrabbits.append((offbit_value, nrci))
                
                if max_count and len(superrabbits) >= max_count:
                    break
    
    return superrabbits


def calculate_pattern_signature(offbit_value: int) -> Dict:
    """Calculate pattern signature metrics."""
    high_bits = (offbit_value >> 16) & 0xFF
    mid_bits = (offbit_value >> 8) & 0xFF
    low_bits = offbit_value & 0xFF
    
    active_bits = bin(offbit_value).count('1')
    bit_balance = abs(active_bits - 12) / 12.0
    
    # Bit distribution
    bit_string = f"{offbit_value:024b}"
    runs = []
    current_run = 1
    for i in range(1, len(bit_string)):
        if bit_string[i] == bit_string[i-1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    runs.append(current_run)
    avg_run_length = sum(runs) / len(runs) if runs else 0
    
    return {
        "high_byte": high_bits,
        "mid_byte": mid_bits,
        "low_byte": low_bits,
        "active_bits": active_bits,
        "bit_balance": bit_balance,
        "avg_run_length": avg_run_length,
        "symmetry": abs(high_bits - low_bits) / 255.0
    }


def calculate_antibiotic_likeness(
    candidate_value: int,
    candidate_nrci: float,
    known_antibiotics: Dict[str, int]
) -> Tuple[float, Dict]:
    """
    Calculate how similar a candidate is to known antibiotics.
    
    Args:
        candidate_value: Candidate OffBit value
        candidate_nrci: Candidate NRCI
        known_antibiotics: Dict of known antibiotic OffBit values
        
    Returns:
        (overall_score, similarity_details)
    """
    candidate_sig = calculate_pattern_signature(candidate_value)
    
    similarities = {}
    for name, known_value in known_antibiotics.items():
        known_offbit = OffBit(known_value)
        known_sig = calculate_pattern_signature(known_value)
        
        # NRCI similarity (40% weight)
        nrci_sim = 1.0 - abs(candidate_nrci - known_offbit.nrci)
        
        # Bit balance similarity (20% weight)
        balance_sim = 1.0 - abs(candidate_sig["bit_balance"] - known_sig["bit_balance"])
        
        # Run length similarity (20% weight)
        run_sim = 1.0 - abs(candidate_sig["avg_run_length"] - known_sig["avg_run_length"]) / 24.0
        
        # Symmetry similarity (20% weight)
        sym_sim = 1.0 - abs(candidate_sig["symmetry"] - known_sig["symmetry"])
        
        # Combined similarity
        similarity = (
            nrci_sim * 0.4 +
            balance_sim * 0.2 +
            run_sim * 0.2 +
            sym_sim * 0.2
        )
        
        similarities[name] = similarity
    
    # Overall score is average of top 3 similarities
    top_3_scores = sorted(similarities.values(), reverse=True)[:3]
    overall_score = sum(top_3_scores) / len(top_3_scores)
    
    # Find best match
    best_match = max(similarities.items(), key=lambda x: x[1])
    
    return overall_score, {
        "best_match": best_match[0],
        "best_similarity": best_match[1],
        "all_similarities": similarities,
        "signature": candidate_sig
    }


def main():
    """Main analysis routine."""
    print("=" * 80)
    print("UBP ANTIBIOTIC SUPER-RABBIT ANALYZER")
    print("=" * 80)
    print()
    
    # Parse super-rabbits from log
    print("Phase 1: Parsing Super-Rabbits from Study Log")
    print("-" * 80)
    
    log_path = "/home/ubuntu/ubp_antibiotics_study/study_output.log"
    print(f"Reading from: {log_path}")
    
    # Parse all super-rabbits
    superrabbits = parse_superrabbits_from_log(log_path)
    print(f"✓ Found {len(superrabbits):,} super-rabbits")
    
    # Analyze antibiotic-likeness
    print("\n\nPhase 2: Calculating Antibiotic-Likeness Scores")
    print("-" * 80)
    print("Comparing against 8 known antibiotics...")
    
    candidates = []
    for i, (offbit_value, nrci) in enumerate(superrabbits):
        score, details = calculate_antibiotic_likeness(
            offbit_value,
            nrci,
            KNOWN_ANTIBIOTICS
        )
        
        candidates.append({
            "offbit_hex": f"0x{offbit_value:06X}",
            "offbit_value": offbit_value,
            "nrci": nrci,
            "antibiotic_likeness": score,
            "best_match": details["best_match"],
            "best_similarity": details["best_similarity"],
            "active_bits": details["signature"]["active_bits"],
            "bit_balance": details["signature"]["bit_balance"]
        })
        
        if (i + 1) % 10000 == 0:
            print(f"  Processed {i+1:,}/{len(superrabbits):,} candidates...")
    
    print(f"✓ Analysis complete")
    
    # Sort by antibiotic-likeness
    candidates.sort(key=lambda x: x["antibiotic_likeness"], reverse=True)
    
    # Display top 50
    print("\n\n" + "=" * 80)
    print("TOP 50 NOVEL ANTIBIOTIC CANDIDATES")
    print("=" * 80)
    print()
    
    for i, candidate in enumerate(candidates[:50], 1):
        print(f"{i}. {candidate['offbit_hex']}")
        print(f"   Antibiotic-Likeness: {candidate['antibiotic_likeness']:.4f}")
        print(f"   NRCI: {candidate['nrci']:.10f}")
        print(f"   Most Similar To: {candidate['best_match']} ({candidate['best_similarity']:.4f})")
        print(f"   Active Bits: {candidate['active_bits']}/24")
        print()
    
    # Save results
    print("=" * 80)
    print("Phase 3: Saving Results")
    print("-" * 80)
    
    results = {
        "study_date": "2025-11-22",
        "total_superrabbits": len(superrabbits),
        "top_50_candidates": candidates[:50],
        "top_100_candidates": candidates[:100],
        "statistics": {
            "mean_antibiotic_likeness": sum(c["antibiotic_likeness"] for c in candidates) / len(candidates),
            "max_antibiotic_likeness": candidates[0]["antibiotic_likeness"],
            "min_antibiotic_likeness": candidates[-1]["antibiotic_likeness"]
        }
    }
    
    output_path = "/home/ubuntu/ubp_antibiotics_study/top_antibiotic_candidates.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Results saved to: {output_path}")
    
    # Summary
    print("\n" + "=" * 80)
    print("🐰 ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nAnalyzed: {len(superrabbits):,} super-rabbits")
    print(f"Top Candidate: {candidates[0]['offbit_hex']}")
    print(f"  Antibiotic-Likeness: {candidates[0]['antibiotic_likeness']:.4f}")
    print(f"  Most Similar To: {candidates[0]['best_match']}")
    print(f"  NRCI: {candidates[0]['nrci']:.10f}")
    
    print("\n\nNext Steps:")
    print("  1. Review top 50 candidates for synthesis")
    print("  2. Generate structural predictions")
    print("  3. Run in vitro antibacterial assays")
    print("  4. Test selectivity against human cells")


if __name__ == "__main__":
    main()
