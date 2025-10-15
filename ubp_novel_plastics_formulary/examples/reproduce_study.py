#!/usr/bin/env python3
"""
Reproduce the UBP Novel Plastics Study
Complete reproduction script for all seven plastic categories

Author: Euan R A Craig, New Zealand
Date: October 14, 2025
"""
import sys
import os
import time

# Add parent directory to path to import code modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ubp_3.2'))

def main():
    """
    Main reproduction routine
    """
    print("\n" + "="*80)
    print("UBP NOVEL PLASTICS STUDY - FULL REPRODUCTION")
    print("="*80)
    print("This script will reproduce the entire study from scratch.")
    print("Estimated time: 2-4 hours")
    print("="*80 + "\n")
    
    # Confirm with user
    response = input("Do you want to proceed? This will overwrite existing results. (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Reproduction cancelled.")
        return
    
    start_time = time.time()
    
    # Step 1: Validate system
    print("\n" + "="*80)
    print("STEP 1: VALIDATING UBP FRAMEWORK")
    print("="*80 + "\n")
    
    from validate_system import main as validate
    validate()
    
    # Step 2: Run pilot optimization for PP
    print("\n" + "="*80)
    print("STEP 2: PILOT OPTIMIZATION (POLYPROPYLENE)")
    print("="*80 + "\n")
    
    from chemical_carousel_pilot import main as pilot
    pilot()
    
    # Step 3: Analyze best PP candidate
    print("\n" + "="*80)
    print("STEP 3: ANALYZING BEST CANDIDATE")
    print("="*80 + "\n")
    
    from analyze_best_candidate import main as analyze
    analyze()
    
    # Step 4: Run full-scale optimization
    print("\n" + "="*80)
    print("STEP 4: FULL-SCALE OPTIMIZATION (ALL CATEGORIES)")
    print("="*80 + "\n")
    
    from full_scale_carousel import main as full_scale
    full_scale()
    
    # Step 5: Compile formulary
    print("\n" + "="*80)
    print("STEP 5: COMPILING FORMULARY")
    print("="*80 + "\n")
    
    from compile_formulary import main as compile_formulary
    compile_formulary()
    
    # Done
    elapsed_time = time.time() - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    
    print("\n" + "="*80)
    print("REPRODUCTION COMPLETE")
    print("="*80)
    print(f"Total time: {hours}h {minutes}m")
    print(f"Results saved to: ../data/")
    print(f"Formulary saved to: ../docs/UBP_Novel_Plastics_Formulary.md")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

