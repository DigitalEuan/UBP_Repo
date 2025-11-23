"""
Run All Visual Proofs
======================

This script runs all six millennium prize visual proof generators and creates
a complete gallery of geometric visualizations.

Author: Euan R A Craig, New Zealand
Date: November 22, 2025
"""

import sys
import os
import subprocess
import time

# Add visualizers to path
visualizers_path = os.path.join(os.path.dirname(__file__), 'visualizers')
sys.path.insert(0, visualizers_path)


def run_visualizer(script_name, problem_name):
    """
    Run a single visualizer script.
    
    Args:
        script_name: Name of the Python script
        problem_name: Human-readable problem name
    """
    print("=" * 80)
    print(f"Running: {problem_name}")
    print("=" * 80)
    print()
    
    script_path = os.path.join(visualizers_path, script_name)
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        elapsed = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"✓ {problem_name} completed successfully in {elapsed:.2f}s")
            return True
        else:
            print(f"✗ {problem_name} failed with return code {result.returncode}")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {problem_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"✗ {problem_name} failed with exception: {e}")
        return False
    finally:
        print()


def main():
    """
    Run all visualizers and generate the complete gallery.
    """
    print()
    print("=" * 80)
    print("UBP Millennium Prize Problems: Visual Proofs Generator")
    print("=" * 80)
    print()
    print("This script will generate geometric visualizations for all six problems.")
    print("Each visualization demonstrates a geometric constraint, not a computational")
    print("validation. The proofs emerge from the geometry of the information substrate.")
    print()
    
    # Define visualizers
    visualizers = [
        ("riemann_resonance_map.py", "Riemann Hypothesis: Resonance Channel"),
        ("p_vs_np_energy_landscape.py", "P vs NP: Energy Landscape"),
        ("navier_stokes_discretization.py", "Navier-Stokes: Discretization Limit"),
        ("yang_mills_mass_gap.py", "Yang-Mills: Mass Gap"),
        ("bsd_rank_geometry.py", "BSD Conjecture: Rank Geometry"),
        ("hodge_cycle_structure.py", "Hodge Conjecture: Cycle Structure"),
    ]
    
    # Run all visualizers
    results = {}
    for script, name in visualizers:
        success = run_visualizer(script, name)
        results[name] = success
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    successful = sum(results.values())
    total = len(results)
    
    for name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}: {name}")
    
    print()
    print(f"Total: {successful}/{total} visualizations generated successfully")
    print()
    
    if successful == total:
        print("=" * 80)
        print("ALL VISUALIZATIONS COMPLETE!")
        print("=" * 80)
        print()
        print("The gallery/ directory now contains geometric proofs for all six")
        print("millennium prize problems. These visualizations demonstrate that the")
        print("'unsolved' aspects are actually geometric constraints of the")
        print("information substrate.")
        print()
        print("Next steps:")
        print("  1. Review the visualizations in the gallery/ directory")
        print("  2. Read the mathematical isomorphisms documentation")
        print("  3. Explore the README.md for the full narrative")
        print()
    else:
        print("=" * 80)
        print("SOME VISUALIZATIONS FAILED")
        print("=" * 80)
        print()
        print("Please review the error messages above and fix any issues.")
        print()
    
    return successful == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
