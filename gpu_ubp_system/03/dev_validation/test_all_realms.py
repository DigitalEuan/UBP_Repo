"""
Multi-Realm UBP System Validation
==================================

Systematically test the GPU UBP system across all 9 physical realms to ensure
completeness and identify any issues.

The 9 UBP Realms (by scale):
1. Quantum Realm - Subatomic particles, quantum tunneling
2. Atomic Realm - Atoms, spectroscopy, molecular vibrations
3. Electromagnetic Realm - EM waves, antenna resonance
4. Optical Realm - Visible light, laser coherence
5. Nuclear Realm - Nuclear binding, E8-G2 lattice
6. Gravitational Realm - Gravitational waves, orbital mechanics
7. Biological Realm - Neural oscillations, DNA dynamics
8. Plasma Realm - Fusion, solar corona
9. Cosmological Realm - CMB, Hubble expansion

Each realm operates at different scales and will stress-test different aspects
of the UBP system.

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import Dict, List, Any
import json
import time
import traceback

from coherence_substrate import CoherenceState, NRCI_TARGET
from system_constants import PhysicalConstants

# Import all realm modules
from quantum_realm import QuantumRealm, QuantumState
from atomic_realm import AtomicRealm
from electromagnetic_realm import ElectromagneticRealm
from optical_realm import OpticalRealm
from nuclear_realm import NuclearRealm
from gravitational_realm import GravitationalRealm
from biological_realm import BiologicalRealm
from plasma_realm import PlasmaRealm
from cosmological_realm import CosmologicalRealm


class MultiRealmValidator:
    """
    Comprehensive validator for all 9 UBP realms.
    """
    
    def __init__(self):
        """Initialize validator with all realm instances."""
        self.results = {}
        self.failures = []
        
        print("=" * 70)
        print("MULTI-REALM UBP SYSTEM VALIDATION")
        print("=" * 70)
        print("Testing all 9 physical realms...")
        print()
    
    def test_quantum_realm(self) -> Dict[str, Any]:
        """Test Quantum Realm - Subatomic scale."""
        print("Testing Quantum Realm...")
        print("-" * 70)
        
        try:
            realm = QuantumRealm()
            
            # Test 1: Quantum tunneling (U-238 alpha decay)
            tunneling = realm.model_quantum_tunneling(
                barrier_height_eV=5.0,
                particle_energy_eV=4.2,
                barrier_width_nm=1.0
            )
            
            # Test 2: Quantum state energy
            state = QuantumState.create(amplitude=1.0+0j, coherence_level=NRCI_TARGET)
            energy = realm.calculate_quantum_energy(state, frequency=1e15)
            
            # Test 3: Entanglement
            state1 = QuantumState.create(amplitude=1.0+0j)
            state2 = QuantumState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'quantum',
                'status': 'PASS',
                'tunneling_probability': tunneling['transmission_probability'],
                'tunneling_nrci': tunneling['transmitted_nrci'],
                'energy_cu': energy['energy_cu'],
                'energy_nrci': energy['nrci'],
                'entanglement_degree': entangled.entanglement_degree,
                'entangled_nrci': entangled.nrci
            }
            
            print(f"✅ Quantum Realm: PASS")
            print(f"   Tunneling probability: {tunneling['transmission_probability']:.6e}")
            print(f"   Energy: {energy['energy_cu']:.6e} CU")
            print(f"   Entanglement degree: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Quantum Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'quantum',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'quantum',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_atomic_realm(self) -> Dict[str, Any]:
        """Test Atomic Realm - Atomic scale."""
        print("Testing Atomic Realm...")
        print("-" * 70)
        
        try:
            realm = AtomicRealm()
            
            # Test 1: Hydrogen spectroscopy (Lyman alpha)
            lyman_alpha = realm.calculate_spectral_line_energy(
                n_initial=2,
                n_final=1,
                element='H'
            )
            
            # Test 2: Molecular vibration (H2)
            vibration = realm.calculate_molecular_vibration_energy(
                reduced_mass_amu=0.5,
                force_constant=510.0,  # N/m for H2
                quantum_number=0
            )
            
            result = {
                'realm': 'atomic',
                'status': 'PASS',
                'lyman_alpha_energy_cu': lyman_alpha['energy_cu'],
                'lyman_alpha_nrci': lyman_alpha['nrci'],
                'vibration_energy_cu': vibration['energy_cu'],
                'vibration_nrci': vibration['nrci']
            }
            
            print(f"✅ Atomic Realm: PASS")
            print(f"   Lyman alpha: {lyman_alpha['energy_cu']:.6e} CU")
            print(f"   H2 vibration: {vibration['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Atomic Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'atomic',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'atomic',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_electromagnetic_realm(self) -> Dict[str, Any]:
        """Test Electromagnetic Realm - EM wave scale."""
        print("Testing Electromagnetic Realm...")
        print("-" * 70)
        
        try:
            realm = ElectromagneticRealm()
            
            # Test 1: Microwave (2.4 GHz WiFi)
            microwave = realm.calculate_electromagnetic_energy(
                frequency_hz=2.4e9,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: Radio wave (FM radio 100 MHz)
            radio = realm.calculate_electromagnetic_energy(
                frequency_hz=1e8,
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'electromagnetic',
                'status': 'PASS',
                'microwave_energy_cu': microwave['energy_cu'],
                'microwave_nrci': microwave['nrci'],
                'radio_energy_cu': radio['energy_cu'],
                'radio_nrci': radio['nrci']
            }
            
            print(f"✅ Electromagnetic Realm: PASS")
            print(f"   Microwave (2.4 GHz): {microwave['energy_cu']:.6e} CU")
            print(f"   Radio (100 MHz): {radio['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Electromagnetic Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'electromagnetic',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'electromagnetic',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_optical_realm(self) -> Dict[str, Any]:
        """Test Optical Realm - Visible light scale."""
        print("Testing Optical Realm...")
        print("-" * 70)
        
        try:
            realm = OpticalRealm()
            
            # Test 1: Green light (550 nm)
            green = realm.calculate_optical_energy(
                wavelength_nm=550.0,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: Red light (650 nm)
            red = realm.calculate_optical_energy(
                wavelength_nm=650.0,
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'optical',
                'status': 'PASS',
                'green_energy_cu': green['energy_cu'],
                'green_nrci': green['nrci'],
                'red_energy_cu': red['energy_cu'],
                'red_nrci': red['nrci']
            }
            
            print(f"✅ Optical Realm: PASS")
            print(f"   Green (550 nm): {green['energy_cu']:.6e} CU")
            print(f"   Red (650 nm): {red['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Optical Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'optical',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'optical',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_nuclear_realm(self) -> Dict[str, Any]:
        """Test Nuclear Realm - Nuclear scale."""
        print("Testing Nuclear Realm...")
        print("-" * 70)
        
        try:
            realm = NuclearRealm()
            
            # Test 1: Deuteron binding energy
            deuteron = realm.calculate_binding_energy(
                mass_number=2,
                atomic_number=1
            )
            
            # Test 2: Nuclear energy at characteristic frequency
            nuclear_energy = realm.calculate_nuclear_energy(
                frequency_hz=1e20,
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'nuclear',
                'status': 'PASS',
                'deuteron_binding_cu': deuteron['binding_energy_cu'],
                'deuteron_nrci': deuteron['nrci'],
                'nuclear_energy_cu': nuclear_energy['energy_cu'],
                'nuclear_nrci': nuclear_energy['nrci']
            }
            
            print(f"✅ Nuclear Realm: PASS")
            print(f"   Deuteron binding: {deuteron['binding_energy_cu']:.6e} CU")
            print(f"   Nuclear energy: {nuclear_energy['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Nuclear Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'nuclear',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'nuclear',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_gravitational_realm(self) -> Dict[str, Any]:
        """Test Gravitational Realm - Gravitational wave scale."""
        print("Testing Gravitational Realm...")
        print("-" * 70)
        
        try:
            realm = GravitationalRealm()
            
            # Test 1: LIGO GW150914 (250 Hz)
            ligo = realm.calculate_gravitational_energy(
                frequency_hz=250.0,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: Orbital resonance (Earth-Moon)
            orbital = realm.calculate_gravitational_energy(
                frequency_hz=1.0 / (27.3 * 86400),  # Moon orbital period
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'gravitational',
                'status': 'PASS',
                'ligo_energy_cu': ligo['energy_cu'],
                'ligo_nrci': ligo['nrci'],
                'orbital_energy_cu': orbital['energy_cu'],
                'orbital_nrci': orbital['nrci']
            }
            
            print(f"✅ Gravitational Realm: PASS")
            print(f"   LIGO (250 Hz): {ligo['energy_cu']:.6e} CU")
            print(f"   Orbital: {orbital['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Gravitational Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'gravitational',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'gravitational',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_biological_realm(self) -> Dict[str, Any]:
        """Test Biological Realm - Biological scale."""
        print("Testing Biological Realm...")
        print("-" * 70)
        
        try:
            realm = BiologicalRealm()
            
            # Test 1: Neural oscillation (40 Hz gamma)
            neural = realm.calculate_biological_energy(
                frequency_hz=40.0,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: DNA breathing mode (1 THz)
            dna = realm.calculate_biological_energy(
                frequency_hz=1e12,
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'biological',
                'status': 'PASS',
                'neural_energy_cu': neural['energy_cu'],
                'neural_nrci': neural['nrci'],
                'dna_energy_cu': dna['energy_cu'],
                'dna_nrci': dna['nrci']
            }
            
            print(f"✅ Biological Realm: PASS")
            print(f"   Neural (40 Hz): {neural['energy_cu']:.6e} CU")
            print(f"   DNA (1 THz): {dna['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Biological Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'biological',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'biological',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_plasma_realm(self) -> Dict[str, Any]:
        """Test Plasma Realm - Plasma scale."""
        print("Testing Plasma Realm...")
        print("-" * 70)
        
        try:
            realm = PlasmaRealm()
            
            # Test 1: Tokamak plasma (10 MHz)
            tokamak = realm.calculate_plasma_energy(
                frequency_hz=1e7,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: Solar corona (1 kHz)
            corona = realm.calculate_plasma_energy(
                frequency_hz=1e3,
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'plasma',
                'status': 'PASS',
                'tokamak_energy_cu': tokamak['energy_cu'],
                'tokamak_nrci': tokamak['nrci'],
                'corona_energy_cu': corona['energy_cu'],
                'corona_nrci': corona['nrci']
            }
            
            print(f"✅ Plasma Realm: PASS")
            print(f"   Tokamak (10 MHz): {tokamak['energy_cu']:.6e} CU")
            print(f"   Corona (1 kHz): {corona['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Plasma Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'plasma',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'plasma',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def test_cosmological_realm(self) -> Dict[str, Any]:
        """Test Cosmological Realm - Cosmological scale."""
        print("Testing Cosmological Realm...")
        print("-" * 70)
        
        try:
            realm = CosmologicalRealm()
            
            # Test 1: CMB fluctuations (160 GHz)
            cmb = realm.calculate_cosmological_energy(
                frequency_hz=1.6e11,
                target_nrci=NRCI_TARGET
            )
            
            # Test 2: Hubble expansion (very low frequency)
            hubble = realm.calculate_cosmological_energy(
                frequency_hz=1e-18,  # ~Hubble time scale
                target_nrci=NRCI_TARGET
            )
            
            result = {
                'realm': 'cosmological',
                'status': 'PASS',
                'cmb_energy_cu': cmb['energy_cu'],
                'cmb_nrci': cmb['nrci'],
                'hubble_energy_cu': hubble['energy_cu'],
                'hubble_nrci': hubble['nrci']
            }
            
            print(f"✅ Cosmological Realm: PASS")
            print(f"   CMB (160 GHz): {cmb['energy_cu']:.6e} CU")
            print(f"   Hubble: {hubble['energy_cu']:.6e} CU")
            print()
            
            return result
            
        except Exception as e:
            print(f"❌ Cosmological Realm: FAIL")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            print()
            
            self.failures.append({
                'realm': 'cosmological',
                'error': str(e),
                'traceback': traceback.format_exc()
            })
            
            return {
                'realm': 'cosmological',
                'status': 'FAIL',
                'error': str(e)
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all realm tests."""
        start_time = time.time()
        
        # Test all realms in order
        self.results['quantum'] = self.test_quantum_realm()
        self.results['atomic'] = self.test_atomic_realm()
        self.results['electromagnetic'] = self.test_electromagnetic_realm()
        self.results['optical'] = self.test_optical_realm()
        self.results['nuclear'] = self.test_nuclear_realm()
        self.results['gravitational'] = self.test_gravitational_realm()
        self.results['biological'] = self.test_biological_realm()
        self.results['plasma'] = self.test_plasma_realm()
        self.results['cosmological'] = self.test_cosmological_realm()
        
        elapsed = time.time() - start_time
        
        # Summary
        passed = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        failed = sum(1 for r in self.results.values() if r['status'] == 'FAIL')
        
        print("=" * 70)
        print("MULTI-REALM VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Total realms: 9")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Elapsed time: {elapsed:.2f} seconds")
        print("=" * 70)
        
        if failed > 0:
            print()
            print("FAILURES:")
            for failure in self.failures:
                print(f"  - {failure['realm']}: {failure['error']}")
        
        print()
        
        return {
            'summary': {
                'total': 9,
                'passed': passed,
                'failed': failed,
                'elapsed_time': elapsed
            },
            'results': self.results,
            'failures': self.failures
        }


def main():
    """Main entry point."""
    validator = MultiRealmValidator()
    results = validator.run_all_tests()
    
    # Export results
    with open('multi_realm_validation.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results exported to multi_realm_validation.json")
    
    # Exit with error code if any tests failed
    if results['summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
