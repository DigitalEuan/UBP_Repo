"""
Batch Simulation Script
Run UBP simulations for all 20 crystal systems
"""

import sys
import time
import json
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/ubp_crystal_study/simulations')
sys.path.insert(0, '/home/ubuntu/ubp_crystal_study/data')

from ubp_crystal_simulator import UBPCrystalSimulator
from crystal_database import get_all_crystals


def run_all_simulations(verbose: bool = False):
    """Run simulations for all crystals in database"""
    
    print("="*80)
    print("UBP CRYSTAL STUDY - BATCH SIMULATION")
    print("="*80)
    print()
    
    # Initialize simulator
    simulator = UBPCrystalSimulator()
    
    # Get all crystals
    crystals = get_all_crystals()
    total_crystals = len(crystals)
    
    print(f"Total crystals to simulate: {total_crystals}")
    print()
    
    # Results storage
    all_results = []
    successful = 0
    failed = 0
    
    # Run simulations
    start_time = time.time()
    
    for i, (crystal_name, crystal_props) in enumerate(crystals.items(), 1):
        print(f"\n[{i}/{total_crystals}] Processing: {crystal_name} ({crystal_props.formula})")
        print(f"  Structure: {crystal_props.structure_type}")
        print(f"  Bonding: {crystal_props.bonding_type}")
        if crystal_props.is_piezoelectric:
            print(f"  ⚡ Piezoelectric")
        
        try:
            # Run simulation
            result = simulator.simulate_crystal(crystal_name, verbose=verbose)
            all_results.append(result)
            successful += 1
            
            # Print summary
            print(f"  ✓ NRCI: {result.nrci_baseline:.6f} ({result.nrci_regime})")
            print(f"  ✓ Fundamental Frequency: {result.fundamental_frequency:.3e} Hz")
            if result.frequency_error is not None:
                print(f"  ✓ Frequency Error: {result.frequency_error:.2f}%")
            print(f"  ✓ Quality Score: {result.nrci_quality_score:.1f}/100")
            
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
            failed += 1
            continue
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Print summary
    print("\n" + "="*80)
    print("SIMULATION SUMMARY")
    print("="*80)
    print(f"Total crystals:     {total_crystals}")
    print(f"Successful:         {successful}")
    print(f"Failed:             {failed}")
    print(f"Success rate:       {100*successful/total_crystals:.1f}%")
    print(f"Total time:         {elapsed:.2f} seconds")
    print(f"Average time/crystal: {elapsed/total_crystals:.2f} seconds")
    print()
    
    # Generate summary statistics
    if all_results:
        print("="*80)
        print("STATISTICAL SUMMARY")
        print("="*80)
        
        # NRCI statistics
        nrci_values = [r.nrci_baseline for r in all_results]
        print(f"\nNRCI Statistics:")
        print(f"  Mean:    {sum(nrci_values)/len(nrci_values):.9f}")
        print(f"  Min:     {min(nrci_values):.9f}")
        print(f"  Max:     {max(nrci_values):.9f}")
        
        # Frequency statistics
        freq_values = [r.fundamental_frequency for r in all_results]
        print(f"\nFundamental Frequency Statistics:")
        print(f"  Mean:    {sum(freq_values)/len(freq_values):.3e} Hz")
        print(f"  Min:     {min(freq_values):.3e} Hz")
        print(f"  Max:     {max(freq_values):.3e} Hz")
        
        # Quality score statistics
        quality_scores = [r.nrci_quality_score for r in all_results]
        print(f"\nQuality Score Statistics:")
        print(f"  Mean:    {sum(quality_scores)/len(quality_scores):.2f}/100")
        print(f"  Min:     {min(quality_scores):.2f}/100")
        print(f"  Max:     {max(quality_scores):.2f}/100")
        
        # Piezoelectric crystals
        piezo_results = [r for r in all_results if r.piezo_coefficient_ubp is not None]
        if piezo_results:
            print(f"\nPiezoelectric Crystals: {len(piezo_results)}")
            for r in piezo_results:
                print(f"  {r.crystal_name:10s}: d33 = {r.piezo_coefficient_ubp:.2f} pC/N, "
                      f"k = {r.electromechanical_coupling_ubp:.4f}")
        
        # Frequency error statistics (where experimental data available)
        freq_errors = [r.frequency_error for r in all_results if r.frequency_error is not None]
        if freq_errors:
            print(f"\nFrequency Prediction Errors (vs. experimental):")
            print(f"  Mean error:  {sum(freq_errors)/len(freq_errors):.2f}%")
            print(f"  Min error:   {min(freq_errors):.2f}%")
            print(f"  Max error:   {max(freq_errors):.2f}%")
            print(f"  Crystals with data: {len(freq_errors)}")
    
    # Save consolidated results
    output_file = Path("/home/ubuntu/ubp_crystal_study/results/all_crystals_summary.json")
    summary_data = {
        'total_crystals': total_crystals,
        'successful': successful,
        'failed': failed,
        'elapsed_time': elapsed,
        'crystals': [
            {
                'name': r.crystal_name,
                'nrci': r.nrci_baseline,
                'fundamental_frequency': r.fundamental_frequency,
                'quality_score': r.nrci_quality_score,
                'frequency_error': r.frequency_error,
                'is_piezoelectric': r.piezo_coefficient_ubp is not None
            }
            for r in all_results
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"\nConsolidated results saved to: {output_file}")
    print("="*80)
    
    return all_results


if __name__ == "__main__":
    # Run with minimal verbosity for batch processing
    results = run_all_simulations(verbose=False)
    
    print("\n✓ All simulations complete!")
    print(f"✓ Individual results saved in: /home/ubuntu/ubp_crystal_study/results/")
    print(f"✓ Summary saved in: /home/ubuntu/ubp_crystal_study/results/all_crystals_summary.json")
