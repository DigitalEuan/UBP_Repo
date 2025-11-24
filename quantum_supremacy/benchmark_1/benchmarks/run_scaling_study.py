#!/usr/bin/env python3.11
"""
UBP CHSH Scaling Study
======================

Systematically test UBP performance at different scales to understand:
1. How performance scales with problem size
2. Where bottlenecks appear
3. Computational complexity (O(n), O(n²), etc.)

Author: Manus AI
Date: November 25, 2025
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPT_PATH = "/home/ubuntu/UBP_Repo/gpu_ubp_system/03/dev_validation/study_chsh_quantum.py"
RESULTS_DIR = Path("/home/ubuntu/UBP_Repo/bulk/gpu_ubp_study_rigorous/results/06_scaling_study")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Scaling test configurations
# Format: (trials, measurements_per_trial, total_measurements)
SCALES = [
    (10, 100, 1_000),
    (10, 500, 5_000),
    (10, 1000, 10_000),
    (10, 2000, 20_000),
    (5, 10000, 50_000),
]

def run_chsh_at_scale(trials, measurements):
    """Run CHSH study at specified scale and collect timing data."""
    print(f"\n{'='*70}")
    print(f"Scale: {trials} trials × {measurements:,} measurements = {trials*measurements:,} total")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    # Run the study
    cmd = [
        "python3.11",
        SCRIPT_PATH,
        "--backend", "cpu",
        "--trials", str(trials),
        "--measurements", str(measurements)
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="/home/ubuntu/UBP_Repo/gpu_ubp_system/03",
        env={
            "PYTHONPATH": "/home/ubuntu/UBP_Repo/gpu_ubp_system/03:/home/ubuntu/UBP_Repo/gpu_ubp_system/03/core",
            **subprocess.os.environ
        }
    )
    
    elapsed = time.time() - start_time
    
    # Parse results
    results_file = Path("/home/ubuntu/UBP_Repo/gpu_ubp_system/03/chsh_quantum_results.json")
    if results_file.exists():
        with open(results_file, 'r') as f:
            chsh_results = json.load(f)
    else:
        chsh_results = None
    
    # Extract key metrics
    if chsh_results:
        mean_S = chsh_results['mean_S']
        mean_nrci = sum(r['mean_nrci'] for r in chsh_results['all_results']) / len(chsh_results['all_results'])
        mean_time_per_trial = sum(r['elapsed_time'] for r in chsh_results['all_results']) / len(chsh_results['all_results'])
    else:
        mean_S = None
        mean_nrci = None
        mean_time_per_trial = None
    
    # Calculate throughput
    total_measurements = trials * measurements * 4  # 4 correlations per trial
    measurements_per_second = total_measurements / elapsed if elapsed > 0 else 0
    
    print(f"\n  Mean S: {mean_S:.6f}" if mean_S else "  Mean S: N/A")
    print(f"  Mean NRCI: {mean_nrci:.10f}" if mean_nrci else "  Mean NRCI: N/A")
    print(f"  Total elapsed: {elapsed:.2f} seconds")
    print(f"  Mean time per trial: {mean_time_per_trial:.4f} seconds" if mean_time_per_trial else "  Mean time per trial: N/A")
    print(f"  Throughput: {measurements_per_second:,.1f} measurements/second")
    
    return {
        'trials': trials,
        'measurements_per_trial': measurements,
        'total_measurements': total_measurements,
        'elapsed_seconds': elapsed,
        'mean_time_per_trial': mean_time_per_trial,
        'measurements_per_second': measurements_per_second,
        'mean_S': mean_S,
        'mean_nrci': mean_nrci,
        'chsh_results': chsh_results
    }


def analyze_scaling(results):
    """Analyze scaling behavior from collected results."""
    print(f"\n{'='*70}")
    print("SCALING ANALYSIS")
    print(f"{'='*70}")
    
    print("\n| Scale | Total Meas | Time (s) | Meas/sec | Time/Trial (s) |")
    print("|-------|------------|----------|----------|----------------|")
    
    for r in results:
        print(f"| {r['trials']}×{r['measurements_per_trial']:,} | "
              f"{r['total_measurements']:,} | "
              f"{r['elapsed_seconds']:.2f} | "
              f"{r['measurements_per_second']:,.0f} | "
              f"{r['mean_time_per_trial']:.4f} |")
    
    # Calculate scaling factor
    print(f"\n{'='*70}")
    print("SCALING FACTOR ANALYSIS")
    print(f"{'='*70}")
    
    for i in range(1, len(results)):
        prev = results[i-1]
        curr = results[i]
        
        size_ratio = curr['total_measurements'] / prev['total_measurements']
        time_ratio = curr['elapsed_seconds'] / prev['elapsed_seconds']
        throughput_ratio = curr['measurements_per_second'] / prev['measurements_per_second']
        
        print(f"\nScale {i} → {i+1}:")
        print(f"  Size increase: {size_ratio:.2f}×")
        print(f"  Time increase: {time_ratio:.2f}×")
        print(f"  Throughput ratio: {throughput_ratio:.2f}× {'(improving)' if throughput_ratio > 1 else '(degrading)'}")
        
        if time_ratio < size_ratio:
            scaling = "sub-linear (good!)"
        elif time_ratio == size_ratio:
            scaling = "linear (O(n))"
        else:
            scaling = "super-linear (bottleneck)"
        
        print(f"  Scaling behavior: {scaling}")


def main():
    """Run complete scaling study."""
    print("="*70)
    print("UBP CHSH SCALING STUDY")
    print("="*70)
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Testing {len(SCALES)} different scales")
    
    all_results = []
    
    for trials, measurements, total in SCALES:
        try:
            result = run_chsh_at_scale(trials, measurements)
            all_results.append(result)
            
            # Save intermediate results
            output_file = RESULTS_DIR / f"scale_{trials}trials_{measurements}meas.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error at scale {trials}×{measurements}: {e}")
            continue
    
    # Analyze scaling behavior
    if len(all_results) > 1:
        analyze_scaling(all_results)
    
    # Save complete results
    summary_file = RESULTS_DIR / "scaling_study_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'date': datetime.now().isoformat(),
            'scales_tested': len(all_results),
            'results': all_results
        }, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Scaling study complete!")
    print(f"Results saved to: {RESULTS_DIR}")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
