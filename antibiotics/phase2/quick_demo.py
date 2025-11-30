"""
================================================================================
UBP Antibiotic Discovery - Quick Demo
Author: Euan R A Craig, New Zealand - # Powered by UBP 3.7.1
Date: 30 November 2025
================================================================================

Fast demonstration of antibiotic discovery (10,000 patterns in ~5 seconds).
"""

import sys
import time

sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study/ubp_core')
sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study')

from antibiotic_realm import AntibioticRealm, NRCI_SUPERCOHERENT, F_RIBOSOME_KEV, OMEGA_C
from bitfield_explorer import BitfieldExplorer, KNOWN_ANTIBIOTIC_SEEDS


def main():
    """Run quick demo."""
    print("=" * 80)
    print("UBP ANTIBIOTIC DISCOVERY - QUICK DEMO")
    print("=" * 80)
    print(f"\nSystem Parameters:")
    print(f"  F_ribosome: {F_RIBOSOME_KEV:.6f} keV")
    print(f"  Ω_c floor: {OMEGA_C:.15f}")
    print(f"  NRCI threshold: {NRCI_SUPERCOHERENT:.10f}")
    print("\n" + "=" * 80)
    
    # Create explorer
    explorer = BitfieldExplorer()
    
    # Phase 1: Seeds
    print("\nPhase 1: Known Antibiotic Seeds")
    print("-" * 80)
    seed_candidates = explorer.explore_seeds(KNOWN_ANTIBIOTIC_SEEDS)
    
    # Phase 2: Random exploration (10K patterns)
    print("\nPhase 2: Random Exploration (10,000 patterns)")
    print("-" * 80)
    start = time.time()
    random_candidates = explorer.explore_random(10000, seed=42, progress_interval=5000)
    elapsed = time.time() - start
    
    print(f"\n✓ Exploration complete in {elapsed:.2f} seconds")
    print(f"✓ Found {len(explorer.candidates)} total candidates")
    print(f"✓ SuperCoherent hits: {explorer.stats.supercoherent_hits}")
    
    # Show top 10
    print("\n" + "=" * 80)
    print("TOP 10 CANDIDATES (by NRCI)")
    print("=" * 80)
    top_10 = explorer.get_top_candidates(10, 'nrci')
    
    for i, candidate in enumerate(top_10, 1):
        print(f"\n{i}. {candidate.offbit_hex}")
        print(f"   NRCI: {candidate.nrci:.10f}")
        print(f"   Activity: {candidate.activity_class}")
        print(f"   Predicted MIC: {candidate.predicted_mic:.3f} μg/mL")
        print(f"   Selectivity: {candidate.selectivity_index:.2f}")
        print(f"   Scaffold: {candidate.scaffold_prediction}")
    
    print("\n" + "=" * 80)
    print("🐰 DEMO COMPLETE - The Bitfield Pharmacy is open!")
    print("=" * 80)
    print(f"\nTo run full study (1M patterns): python3.11 study_antibiotic_discovery.py")
    print(f"To run mega study (100M patterns): edit StudyConfig.NUM_RANDOM_PATTERNS = 100_000_000")


if __name__ == "__main__":
    main()
