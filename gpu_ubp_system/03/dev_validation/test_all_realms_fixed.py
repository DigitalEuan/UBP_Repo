"""
Multi-Realm UBP System Validation (Fixed API)
==============================================

Systematically test the GPU UBP system across all 9 physical realms using
the correct API signatures from UBP 3.6.

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
    """Comprehensive validator for all 9 UBP realms."""
    
    def __init__(self):
        self.results = {}
        self.failures = []
        
        print("=" * 70)
        print("MULTI-REALM UBP SYSTEM VALIDATION")
        print("=" * 70)
        print("Testing all 9 physical realms with correct APIs...")
        print()
    
    def test_quantum_realm(self) -> Dict[str, Any]:
        """Test Quantum Realm."""
        print("Testing Quantum Realm...")
        print("-" * 70)
        
        try:
            realm = QuantumRealm()
            
            # Test 1: Quantum tunneling
            tunneling = realm.model_quantum_tunneling(
                barrier_height_eV=5.0,
                particle_energy_eV=4.2,
                barrier_width_nm=1.0
            )
            
            # Test 2: Entanglement
            state1 = QuantumState.create(amplitude=1.0+0j)
            state2 = QuantumState.create(amplitude=0.0+1.0j)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'quantum',
                'status': 'PASS',
                'tunneling_probability': tunneling['transmission_probability'],
                'tunneling_nrci': tunneling['transmitted_nrci'],
                'entanglement_degree': entangled.entanglement_degree,
                'entangled_nrci': entangled.nrci
            }
            
            print(f"✅ Quantum Realm: PASS")
            print(f"   Tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('quantum', e)
    
    def test_atomic_realm(self) -> Dict[str, Any]:
        """Test Atomic Realm."""
        print("Testing Atomic Realm...")
        print("-" * 70)
        
        try:
            realm = AtomicRealm()
            
            # Test 1: Hydrogen spectrum (Lyman alpha: n=2→1)
            lyman = realm.model_hydrogen_spectrum(n_initial=2, n_final=1, series_name="Lyman")
            
            # Test 2: Molecular vibration (CO2)
            vibration = realm.model_molecular_vibration(molecule='CO2', mode='symmetric_stretch')
            
            result = {
                'realm': 'atomic',
                'status': 'PASS',
                'lyman_wavelength_nm': lyman['wavelength_nm'],
                'lyman_energy_ev': lyman['energy_ev'],
                'vibration_frequency_hz': vibration['frequency_hz'],
                'vibration_energy_ev': vibration['energy_ev']
            }
            
            print(f"✅ Atomic Realm: PASS")
            print(f"   Lyman alpha: {lyman['wavelength_nm']:.2f} nm")
            print(f"   CO2 vibration: {vibration['frequency_hz']:.2e} Hz")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('atomic', e)
    
    def test_electromagnetic_realm(self) -> Dict[str, Any]:
        """Test Electromagnetic Realm."""
        print("Testing Electromagnetic Realm...")
        print("-" * 70)
        
        try:
            realm = ElectromagneticRealm()
            
            # Test 1: Tunneling (evanescent waves)
            tunneling = realm.model_electromagnetic_tunneling(
                barrier_width_m=1e-6,
                frequency_hz=1e9
            )
            
            # Test 2: Entanglement (photon pairs)
            from electromagnetic_realm import ElectromagneticState
            state1 = ElectromagneticState.create(frequency=1e9)
            state2 = ElectromagneticState.create(frequency=1e9)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'electromagnetic',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ Electromagnetic Realm: PASS")
            print(f"   EM tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('electromagnetic', e)
    
    def test_optical_realm(self) -> Dict[str, Any]:
        """Test Optical Realm."""
        print("Testing Optical Realm...")
        print("-" * 70)
        
        try:
            realm = OpticalRealm()
            
            # Test 1: Optical tunneling (frustrated total internal reflection)
            tunneling = realm.model_optical_tunneling(
                gap_distance_nm=100.0,
                wavelength_nm=550.0
            )
            
            # Test 2: Entanglement (entangled photons)
            from optical_realm import OpticalState
            state1 = OpticalState.create(wavelength_nm=550.0)
            state2 = OpticalState.create(wavelength_nm=550.0)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'optical',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ Optical Realm: PASS")
            print(f"   Optical tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('optical', e)
    
    def test_nuclear_realm(self) -> Dict[str, Any]:
        """Test Nuclear Realm."""
        print("Testing Nuclear Realm...")
        print("-" * 70)
        
        try:
            realm = NuclearRealm()
            
            # Test 1: Nuclear tunneling (alpha decay)
            tunneling = realm.model_nuclear_tunneling(
                barrier_height_MeV=25.0,
                particle_energy_MeV=4.2,
                barrier_width_fm=10.0
            )
            
            # Test 2: Entanglement (nuclear spin states)
            from nuclear_realm import NuclearState
            state1 = NuclearState.create(frequency=1e20)
            state2 = NuclearState.create(frequency=1e20)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'nuclear',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ Nuclear Realm: PASS")
            print(f"   Nuclear tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('nuclear', e)
    
    def test_gravitational_realm(self) -> Dict[str, Any]:
        """Test Gravitational Realm."""
        print("Testing Gravitational Realm...")
        print("-" * 70)
        
        try:
            realm = GravitationalRealm()
            
            # Test 1: LIGO gravitational wave
            ligo = realm.model_ligo_gravitational_wave(
                frequency_hz=250.0,
                strain_amplitude=1e-21
            )
            
            # Test 2: Jupiter-Europa resonance
            resonance = realm.model_jupiter_europa_resonance()
            
            result = {
                'realm': 'gravitational',
                'status': 'PASS',
                'ligo_energy_cu': ligo['energy_cu'],
                'ligo_nrci': ligo['nrci'],
                'resonance_period_days': resonance['europa_period_days'],
                'resonance_ratio': resonance['resonance_ratio']
            }
            
            print(f"✅ Gravitational Realm: PASS")
            print(f"   LIGO: {ligo['energy_cu']:.6e} CU")
            print(f"   Europa resonance: {resonance['resonance_ratio']:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('gravitational', e)
    
    def test_biological_realm(self) -> Dict[str, Any]:
        """Test Biological Realm."""
        print("Testing Biological Realm...")
        print("-" * 70)
        
        try:
            realm = BiologicalRealm()
            
            # Test 1: Biological tunneling (enzyme catalysis)
            tunneling = realm.model_biological_tunneling(
                barrier_height_eV=0.5,
                particle_energy_eV=0.3,
                barrier_width_nm=0.5
            )
            
            # Test 2: Entanglement (avian magnetoreception)
            from biological_realm import BiologicalState
            state1 = BiologicalState.create(frequency=40.0)  # Neural gamma
            state2 = BiologicalState.create(frequency=40.0)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'biological',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ Biological Realm: PASS")
            print(f"   Bio tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('biological', e)
    
    def test_plasma_realm(self) -> Dict[str, Any]:
        """Test Plasma Realm."""
        print("Testing Plasma Realm...")
        print("-" * 70)
        
        try:
            realm = PlasmaRealm()
            
            # Test 1: Plasma tunneling
            tunneling = realm.model_plasma_tunneling(
                barrier_height_eV=10.0,
                particle_energy_eV=8.0,
                barrier_width_m=1e-3
            )
            
            # Test 2: Entanglement (plasma oscillations)
            from plasma_realm import PlasmaState
            state1 = PlasmaState.create(frequency=1e7)  # 10 MHz
            state2 = PlasmaState.create(frequency=1e7)
            entangled = realm.model_entanglement(state1, state2)
            
            result = {
                'realm': 'plasma',
                'status': 'PASS',
                'tunneling_transmission': tunneling['transmission_probability'],
                'entanglement_degree': entangled.entanglement_degree
            }
            
            print(f"✅ Plasma Realm: PASS")
            print(f"   Plasma tunneling: {tunneling['transmission_probability']:.6e}")
            print(f"   Entanglement: {entangled.entanglement_degree:.6f}")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('plasma', e)
    
    def test_cosmological_realm(self) -> Dict[str, Any]:
        """Test Cosmological Realm."""
        print("Testing Cosmological Realm...")
        print("-" * 70)
        
        try:
            realm = CosmologicalRealm()
            
            # Test 1: CMB fluctuations
            cmb = realm.model_cmb_fluctuations(
                temperature_k=2.725,
                fluctuation_amplitude=1e-5
            )
            
            # Test 2: Hubble expansion
            hubble = realm.model_hubble_expansion(
                redshift=1.0
            )
            
            result = {
                'realm': 'cosmological',
                'status': 'PASS',
                'cmb_energy_cu': cmb['energy_cu'],
                'cmb_nrci': cmb['nrci'],
                'hubble_velocity_km_s': hubble['recession_velocity_km_s'],
                'hubble_distance_mpc': hubble['distance_mpc']
            }
            
            print(f"✅ Cosmological Realm: PASS")
            print(f"   CMB: {cmb['energy_cu']:.6e} CU")
            print(f"   Hubble: {hubble['recession_velocity_km_s']:.2f} km/s")
            print()
            
            return result
            
        except Exception as e:
            return self._handle_failure('cosmological', e)
    
    def _handle_failure(self, realm_name: str, exception: Exception) -> Dict[str, Any]:
        """Handle test failure."""
        print(f"❌ {realm_name.capitalize()} Realm: FAIL")
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
        
        # Test all realms
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
                print(f"  - {failure['realm']}: {failure['error'][:100]}")
        
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
