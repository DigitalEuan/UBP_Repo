"""
UBP 3.3 Example: Hydrogen Balmer Series Spectral Lines
=======================================================

This example demonstrates atomic spectroscopy using the Rydberg formula
to calculate hydrogen spectral lines in the visible range.

Real-world verification:
- H-alpha: 656.3 nm (red)
- H-beta: 486.1 nm (blue-green)
- H-gamma: 434.0 nm (violet)

Author: Euan R A Craig, New Zealand
Date: 31 October 2025
"""

import sys
sys.path.insert(0, '/home/ubuntu/ubp_3.3')

import json
from atomic_realm import AtomicRealm

def main():
    """Run hydrogen spectrum example and save results."""
    
    print("=" * 80)
    print("UBP 3.3 EXAMPLE: Hydrogen Balmer Series")
    print("=" * 80)
    
    realm = AtomicRealm()
    
    # Calculate H-alpha, H-beta, H-gamma lines
    lines = [
        (3, 2, "H-alpha"),
        (4, 2, "H-beta"),
        (5, 2, "H-gamma")
    ]
    
    results = {}
    
    for n_i, n_f, name in lines:
        result = realm.model_hydrogen_spectrum(
            n_initial=n_i,
            n_final=n_f,
            series_name="Balmer"
        )
        results[name] = result
        
        print(f"\n{name} Line (n={n_i}→{n_f}):")
        print(f"  Wavelength: {result['wavelength_nm']:.2f} nm")
        print(f"  Frequency: {result['frequency_thz']:.3f} THz")
        print(f"  Energy: {result['energy_ev']:.4f} eV")
        print(f"  Color: {result['color']}")
        print(f"  UBP Energy: {result['ubp_energy_cu']:.6e} CU")
    
    # Save results
    output_file = '/home/ubuntu/ubp_3.3/examples/results/atomic_01_hydrogen.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # Verification
    print("\n" + "=" * 80)
    print("VERIFICATION AGAINST REAL DATA")
    print("=" * 80)
    
    expected = {
        "H-alpha": 656.3,
        "H-beta": 486.1,
        "H-gamma": 434.0
    }
    
    for name, expected_nm in expected.items():
        calculated_nm = results[name]['wavelength_nm']
        error = abs(calculated_nm - expected_nm)
        error_pct = (error / expected_nm) * 100
        
        print(f"\n{name}:")
        print(f"  UBP Calculated: {calculated_nm:.2f} nm")
        print(f"  Literature: {expected_nm:.1f} nm")
        print(f"  Error: {error:.2f} nm ({error_pct:.3f}%)")
        print(f"  ✓ EXCELLENT" if error_pct < 0.1 else "  ✓ VERIFIED" if error_pct < 1.0 else "  ⚠ CHECK")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = main()
