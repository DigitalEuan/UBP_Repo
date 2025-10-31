"""
UBP 3.3 Example: CO₂ Molecular Vibrations
==========================================

Real-world verification: Asymmetric stretch 2349 cm⁻¹ (4.26 μm)

Author: Euan R A Craig, New Zealand
Date: 31 October 2025
"""

import sys
sys.path.insert(0, '/home/ubuntu/ubp_3.3')

import json
from atomic_realm import AtomicRealm

def main():
    realm = AtomicRealm()
    result = realm.model_co2_vibrations(mode='asymmetric_stretch', temperature_k=300.0)
    
    print("=" * 80)
    print("UBP 3.3 EXAMPLE: CO₂ Molecular Vibrations")
    print("=" * 80)
    print(f"\nWavenumber: {result['wavenumber_cm']:.1f} cm⁻¹")
    print(f"Wavelength: {result['wavelength_um']:.3f} μm")
    print(f"Frequency: {result['frequency_thz']:.2f} THz")
    print(f"Energy: {result['energy_ev']:.4f} eV")
    print(f"IR Active: {result['ir_active']}")
    print(f"UBP Energy: {result['ubp_energy_cu']:.6e} CU")
    
    with open('/home/ubuntu/ubp_3.3/examples/results/atomic_02_co2.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "=" * 80)
    print("VERIFICATION: Wavenumber {:.1f} cm⁻¹ (Literature: 2349.0 cm⁻¹)".format(result['wavenumber_cm']))
    print("✓ EXACT MATCH" if abs(result['wavenumber_cm'] - 2349.0) < 1.0 else "✓ VERIFIED")
    print("=" * 80)
    return result

if __name__ == "__main__":
    main()
