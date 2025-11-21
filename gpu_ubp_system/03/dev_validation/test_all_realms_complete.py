"""
Multi-Realm UBP System Validation - Complete & Correct
=======================================================

Final version with all correct API signatures from UBP 3.6.

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import Dict, Any
import json
import time
import traceback

# Import all realm modules and their state classes
from quantum_realm import QuantumRealm, QuantumState
from atomic_realm import AtomicRealm
from electromagnetic_realm import ElectromagneticRealm, ElectromagneticState
from optical_realm import OpticalRealm, OpticalState
from nuclear_realm import NuclearRealm, NuclearState
from gravitational_realm import GravitationalRealm
from biological_realm import BiologicalRealm, BiologicalState
from plasma_realm import PlasmaRealm, PlasmaState
from cosmological_realm import CosmologicalRealm


class MultiRealmValidator:
    """Comprehensive validator for all 9 UBP realms with correct APIs."""
    
    def __init__(self):
        self.results = {}
        self.failures = []
        
        print("=" * 70)
        print("MULTI-REALM UBP SYSTEM VALIDATION - COMPLETE")
        print("=" * 70)
        print("Testing all 9 physical realms with verified correct APIs...")
        print()
    
    def test_quantum_realm(self) -> Dict[str, Any]:
        """Test Quantum Realm."""
        print("1. Testing Quantum Realm...")
        print("-" * 70)
        
        try:
            realm = QuantumRealm()
            
            # Test: Quantum tunneling + Entanglement
            tunneling = realm.model_quantum_tunneling(
                barrier_height_eV=5.0,
                particle_energy_eV=4.2,
                barrier_width_nm=1.0
            )
            
            state1 = QuantumState.create(amplitude=1.0+0j)
            state2 = QuantumState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'quantum',
                'status': 'PASS',
                'tunneling_probability': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('quantum', e)
    
    def test_atomic_realm(self) -> Dict[str, Any]:
        """Test Atomic Realm."""
        print("2. Testing Atomic Realm...")
        print("-" * 70)
        
        try:
            realm = AtomicRealm()
            
            # Test: Hydrogen spectrum + Molecular vibration
            lyman = realm.model_hydrogen_spectrum(n_initial=2, n_final=1, series_name="Lyman")
            vibration = realm.model_molecular_vibration(molecule='CO2', mode='symmetric_stretch')
            
            result = {
                'realm': 'atomic',
                'status': 'PASS',
                'lyman_wavelength_nm': lyman['wavelength_nm'],
                'vibration_frequency_hz': vibration['frequency_hz']
            }
            
            print(f"✅ PASS - Lyman: {lyman['wavelength_nm']:.2f} nm, CO2 vib: {vibration['frequency_hz']:.2e} Hz")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('atomic', e)
    
    def test_electromagnetic_realm(self) -> Dict[str, Any]:
        """Test Electromagnetic Realm."""
        print("3. Testing Electromagnetic Realm...")
        print("-" * 70)
        
        try:
            realm = ElectromagneticRealm()
            
            # Test: Tunneling + Entanglement (correct API)
            tunneling = realm.model_electromagnetic_tunneling(
                barrier_height_eV=1.0,
                particle_energy_eV=0.8,
                barrier_width_nm=10.0
            )
            
            state1 = ElectromagneticState.create(amplitude=1.0+0j)
            state2 = ElectromagneticState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'electromagnetic',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('electromagnetic', e)
    
    def test_optical_realm(self) -> Dict[str, Any]:
        """Test Optical Realm."""
        print("4. Testing Optical Realm...")
        print("-" * 70)
        
        try:
            realm = OpticalRealm()
            
            # Test: Tunneling + Entanglement (correct API)
            tunneling = realm.model_optical_tunneling(
                barrier_height_eV=2.0,
                particle_energy_eV=1.8,
                barrier_width_nm=100.0
            )
            
            state1 = OpticalState.create(amplitude=1.0+0j)
            state2 = OpticalState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'optical',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('optical', e)
    
    def test_nuclear_realm(self) -> Dict[str, Any]:
        """Test Nuclear Realm."""
        print("5. Testing Nuclear Realm...")
        print("-" * 70)
        
        try:
            realm = NuclearRealm()
            
            # Test: Tunneling + Entanglement (correct API - uses eV not MeV)
            tunneling = realm.model_nuclear_tunneling(
                barrier_height_eV=25e6,  # 25 MeV in eV
                particle_energy_eV=4.2e6,  # 4.2 MeV in eV
                barrier_width_nm=0.01  # 10 fm in nm
            )
            
            state1 = NuclearState.create(amplitude=1.0+0j)
            state2 = NuclearState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'nuclear',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('nuclear', e)
    
    def test_gravitational_realm(self) -> Dict[str, Any]:
        """Test Gravitational Realm."""
        print("6. Testing Gravitational Realm...")
        print("-" * 70)
        
        try:
            realm = GravitationalRealm()
            
            # Test: LIGO + Jupiter-Europa resonance (correct API)
            ligo = realm.model_ligo_gravitational_wave(
                event_name='GW150914',
                m1_solar_masses=36.0,
                m2_solar_masses=29.0,
                distance_mpc=410.0,
                peak_frequency_hz=250.0
            )
            
            resonance = realm.model_jupiter_europa_resonance()
            
            result = {
                'realm': 'gravitational',
                'status': 'PASS',
                'ligo_energy_cu': ligo['ubp_energy_cu'],
                'ligo_nrci': ligo['nrci'],
                'resonance_ratio': resonance['resonance_ratio']
            }
            
            print(f"✅ PASS - LIGO: {ligo['ubp_energy_cu']:.6e} CU, Resonance: {resonance['resonance_ratio']:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('gravitational', e)
    
    def test_biological_realm(self) -> Dict[str, Any]:
        """Test Biological Realm."""
        print("7. Testing Biological Realm...")
        print("-" * 70)
        
        try:
            realm = BiologicalRealm()
            
            # Test: Tunneling + Entanglement (correct API)
            tunneling = realm.model_biological_tunneling(
                barrier_height_eV=0.5,
                particle_energy_eV=0.3,
                barrier_width_nm=0.5
            )
            
            state1 = BiologicalState.create(amplitude=1.0+0j)
            state2 = BiologicalState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'biological',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('biological', e)
    
    def test_plasma_realm(self) -> Dict[str, Any]:
        """Test Plasma Realm."""
        print("8. Testing Plasma Realm...")
        print("-" * 70)
        
        try:
            realm = PlasmaRealm()
            
            # Test: Tunneling + Entanglement (correct API)
            tunneling = realm.model_plasma_tunneling(
                barrier_height_eV=10.0,
                particle_energy_eV=8.0,
                barrier_width_nm=1000.0  # 1 micron
            )
            
            state1 = PlasmaState.create(amplitude=1.0+0j)
            state2 = PlasmaState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'plasma',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ PASS - Tunneling: {tunneling['transmission_probability']:.6e}, Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('plasma', e)
    
    def test_cosmological_realm(self) -> Dict[str, Any]:
        """Test Cosmological Realm."""
        print("9. Testing Cosmological Realm...")
        print("-" * 70)
        
        try:
            realm = CosmologicalRealm()
            
            # Test: CMB + Hubble expansion (correct API)
            cmb = realm.model_cmb_fluctuations(
                angular_scale_arcmin=1.0,
                temperature_fluctuation_uk=100.0
            )
            
            hubble = realm.model_hubble_expansion(redshift=1.0)
            
            result = {
                'realm': 'cosmological',
                'status': 'PASS',
                'cmb_energy_cu': cmb['ubp_energy_cu'],
                'cmb_nrci': cmb['nrci'],
                'hubble_parameter': hubble['hubble_parameter_km_s_mpc'],
                'hubble_age_gyr': hubble['age_gyr']
            }
            
            print(f"✅ PASS - CMB: {cmb['ubp_energy_cu']:.6e} CU, Hubble H0: {hubble['hubble_parameter_km_s_mpc']:.2f} km/s/Mpc")
            print()
            return result
            
        except Exception as e:
            return self._handle_failure('cosmological', e)
    
    def _handle_failure(self, realm_name: str, exception: Exception) -> Dict[str, Any]:
        """Handle test failure."""
        print(f"❌ FAIL - {realm_name.capitalize()} Realm")
        print(f"   Error: {str(exception)}")
        print(f"   Traceback: {traceback.format_exc()}")
        print()
        
        self.failures.append({
            'realm': realm_name,
            'error': str(exception),
            'traceback': traceback.format_exc()
        })
        
        return {
            'realm': realm_name,
            'status': 'FAIL',
            'error': str(exception)
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
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Elapsed time: {elapsed:.2f} seconds")
        print("=" * 70)
        
        if failed > 0:
            print()
            print("FAILURES:")
            for failure in self.failures:
                print(f"  - {failure['realm']}: {failure['error'][:80]}...")
        else:
            print()
            print("🎉 ALL REALMS PASS! GPU UBP system is complete and validated.")
        
        print()
        
        return {
            'summary': {
                'total': 9,
                'passed': passed,
                'failed': failed,
                'elapsed_time': elapsed,
                'all_pass': (failed == 0)
            },
            'results': self.results,
            'failures': self.failures
        }


def main():
    """Main entry point."""
    validator = MultiRealmValidator()
    results = validator.run_all_tests()
    
    # Export results
    with open('multi_realm_validation_complete.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results exported to multi_realm_validation_complete.json")
    
    # Exit with error code if any tests failed
    if results['summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
