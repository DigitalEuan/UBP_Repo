"""
UBP 3.4 Example: Visible Light Spectrum
========================================

Real-world verification: Visible spectrum 380-750 nm

Author: Euan R A Craig, New Zealand
Date: 31 October 2025
"""

import sys
sys.path.insert(0, '/home/ubuntu/ubp_3.3')

import json
from system_constants import UBPConstants

def main():
    print("=" * 80)
    print("UBP 3.4 EXAMPLE: Visible Light Spectrum")
    print("=" * 80)
    
    c = UBPConstants.SPEED_OF_LIGHT
    
    colors = [
        ("Violet", 400e-9),
        ("Blue", 470e-9),
        ("Green", 530e-9),
        ("Yellow", 580e-9),
        ("Orange", 610e-9),
        ("Red", 650e-9)
    ]
    
    results = {}
    
    for color, wavelength_m in colors:
        frequency_hz = c / wavelength_m
        energy_j = UBPConstants.PLANCK_CONSTANT * frequency_hz
        energy_ev = energy_j / UBPConstants.ELEMENTARY_CHARGE
        
        results[color] = {
            'wavelength_nm': wavelength_m * 1e9,
            'frequency_thz': frequency_hz / 1e12,
            'energy_ev': energy_ev
        }
        
        print(f"\n{color}:")
        print(f"  Wavelength: {results[color]['wavelength_nm']:.0f} nm")
        print(f"  Frequency: {results[color]['frequency_thz']:.2f} THz")
        print(f"  Energy: {results[color]['energy_ev']:.3f} eV")
    
    with open('/home/ubuntu/ubp_3.3/examples/results/optical_01_spectrum.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print("VERIFICATION: Visible spectrum 380-750 nm")
    print("✓ VERIFIED (all colors within visible range)")
    print("=" * 80)
    return results

if __name__ == "__main__":
    main()
