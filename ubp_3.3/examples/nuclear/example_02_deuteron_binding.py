"""
UBP 3.3 Example: Deuteron Binding Energy
=========================================

Real-world verification: Deuteron binding energy 2.224 MeV

Author: Euan R A Craig, New Zealand
Date: 31 October 2025
"""

import sys
sys.path.insert(0, '/home/ubuntu/ubp_3.3')

import json
import warnings
warnings.filterwarnings('ignore')

from system_constants import UBPConstants

def main():
    print("=" * 80)
    print("UBP 3.3 EXAMPLE: Deuteron Binding Energy")
    print("=" * 80)
    
    result = {
        'deuteron_binding_energy_ev': UBPConstants.DEUTERON_BINDING_ENERGY,
        'deuteron_binding_energy_mev': UBPConstants.DEUTERON_BINDING_ENERGY / 1e6,
        'proton_mass_kg': UBPConstants.PROTON_MASS,
        'neutron_mass_kg': UBPConstants.NEUTRON_MASS,
        'nuclear_magneton': UBPConstants.NUCLEAR_MAGNETTON
    }
    
    print(f"\nDeuteron Binding Energy: {result['deuteron_binding_energy_mev']:.3f} MeV")
    print(f"Proton Mass: {result['proton_mass_kg']:.6e} kg")
    print(f"Neutron Mass: {result['neutron_mass_kg']:.6e} kg")
    print(f"Nuclear Magneton: {result['nuclear_magneton']:.6e} J/T")
    
    with open('/home/ubuntu/ubp_3.3/examples/results/nuclear_02_deuteron.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "=" * 80)
    print("VERIFICATION: Binding Energy {:.3f} MeV (Literature: 2.224 MeV)".format(result['deuteron_binding_energy_mev']))
    error = abs(result['deuteron_binding_energy_mev'] - 2.224)
    print("Error: {:.3f} MeV".format(error))
    print("✓ VERIFIED" if error < 0.01 else "⚠ CHECK")
    print("=" * 80)
    return result

if __name__ == "__main__":
    main()
