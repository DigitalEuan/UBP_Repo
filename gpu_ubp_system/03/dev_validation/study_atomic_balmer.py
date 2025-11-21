"""
Atomic Realm Study: Hydrogen Balmer Series
===========================================

Real-world validation of UBP atomic realm against experimental spectroscopy data.

The Balmer series consists of spectral lines from hydrogen atom electron transitions
from higher energy levels (n ≥ 3) to n=2. These are visible light wavelengths that
have been precisely measured since the 19th century.

Experimental Data:
- H-alpha (3→2): 656.3 nm
- H-beta (4→2): 486.1 nm
- H-gamma (5→2): 434.0 nm
- H-delta (6→2): 410.2 nm

Success Criterion: UBP predictions match within <1% error

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import Dict, List
import json
import time

from atomic_realm import AtomicRealm


class BalmerSeriesStudy:
    """Study of hydrogen Balmer series using UBP atomic realm."""
    
    # Experimental data (nm)
    EXPERIMENTAL_DATA = {
        'H-alpha': {'n_initial': 3, 'n_final': 2, 'wavelength_nm': 656.3},
        'H-beta': {'n_initial': 4, 'n_final': 2, 'wavelength_nm': 486.1},
        'H-gamma': {'n_initial': 5, 'n_final': 2, 'wavelength_nm': 434.0},
        'H-delta': {'n_initial': 6, 'n_final': 2, 'wavelength_nm': 410.2},
    }
    
    def __init__(self):
        """Initialize study."""
        self.realm = AtomicRealm()
        self.results = []
        
        print("=" * 70)
        print("ATOMIC REALM STUDY: HYDROGEN BALMER SERIES")
        print("=" * 70)
        print("Validating UBP atomic realm against experimental spectroscopy")
        print()
    
    def calculate_line(self, name: str, n_initial: int, n_final: int, 
                      experimental_nm: float) -> Dict:
        """Calculate a single Balmer line and compare to experiment."""
        
        print(f"Calculating {name} ({n_initial}→{n_final})...")
        
        # Use UBP atomic realm to calculate spectral line
        ubp_result = self.realm.model_hydrogen_spectrum(
            n_initial=n_initial,
            n_final=n_final,
            series_name="Balmer"
        )
        
        ubp_wavelength = ubp_result['wavelength_nm']
        ubp_energy_ev = ubp_result['energy_ev']
        ubp_frequency = ubp_result['frequency_hz']
        ubp_nrci = ubp_result['nrci']
        
        # Calculate error
        error_nm = ubp_wavelength - experimental_nm
        error_percent = (error_nm / experimental_nm) * 100
        
        # Determine if within tolerance
        within_tolerance = abs(error_percent) < 1.0
        
        result = {
            'line_name': name,
            'n_initial': n_initial,
            'n_final': n_final,
            'experimental_nm': experimental_nm,
            'ubp_wavelength_nm': ubp_wavelength,
            'ubp_energy_ev': ubp_energy_ev,
            'ubp_frequency_hz': ubp_frequency,
            'ubp_nrci': ubp_nrci,
            'error_nm': error_nm,
            'error_percent': error_percent,
            'within_tolerance': within_tolerance
        }
        
        # Print result
        status = "✅ PASS" if within_tolerance else "❌ FAIL"
        print(f"  Experimental: {experimental_nm:.1f} nm")
        print(f"  UBP: {ubp_wavelength:.1f} nm")
        print(f"  Error: {error_percent:+.3f}% ({error_nm:+.1f} nm)")
        print(f"  NRCI: {ubp_nrci:.6f}")
        print(f"  {status}")
        print()
        
        return result
    
    def run_study(self) -> Dict:
        """Run complete Balmer series study."""
        start_time = time.time()
        
        # Calculate all Balmer lines
        for name, data in self.EXPERIMENTAL_DATA.items():
            result = self.calculate_line(
                name=name,
                n_initial=data['n_initial'],
                n_final=data['n_final'],
                experimental_nm=data['wavelength_nm']
            )
            self.results.append(result)
        
        elapsed = time.time() - start_time
        
        # Calculate summary statistics
        errors = [abs(r['error_percent']) for r in self.results]
        mean_error = sum(errors) / len(errors)
        max_error = max(errors)
        passed = sum(1 for r in self.results if r['within_tolerance'])
        
        # Print summary
        print("=" * 70)
        print("BALMER SERIES STUDY RESULTS")
        print("=" * 70)
        print(f"Lines calculated: {len(self.results)}")
        print(f"Passed (<1% error): {passed}/{len(self.results)}")
        print(f"Mean absolute error: {mean_error:.3f}%")
        print(f"Max absolute error: {max_error:.3f}%")
        print(f"Elapsed time: {elapsed:.3f} seconds")
        print("=" * 70)
        
        # Overall assessment
        all_pass = (passed == len(self.results))
        if all_pass:
            print()
            print("✅ SUCCESS: UBP atomic realm accurately reproduces Balmer series!")
            print("   All wavelengths match experimental data within 1% tolerance.")
            print()
        else:
            print()
            print("⚠️  PARTIAL SUCCESS: Some lines exceed 1% tolerance.")
            print(f"   {passed}/{len(self.results)} lines pass validation.")
            print()
        
        return {
            'study': 'hydrogen_balmer_series',
            'realm': 'atomic',
            'summary': {
                'total_lines': len(self.results),
                'passed': passed,
                'mean_error_percent': mean_error,
                'max_error_percent': max_error,
                'all_pass': all_pass,
                'elapsed_time': elapsed
            },
            'results': self.results
        }


def main():
    """Main entry point."""
    study = BalmerSeriesStudy()
    results = study.run_study()
    
    # Export results
    with open('study_atomic_balmer_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results exported to study_atomic_balmer_results.json")
    
    # Exit with error if not all pass
    if not results['summary']['all_pass']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
