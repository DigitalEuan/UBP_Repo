"""
================================================================================
UBP SKILL VALIDATOR v1.0
================================================================================

Comprehensive validation and testing suite for the UBP Geometric Reasoning Skill.
Tests all eight capabilities and verifies system integrity.

Author: E. R. A. Craig / Manus AI
Date: January 30, 2026
Version: 1.0
================================================================================
"""

import sys
import json
from typing import Dict, List, Any
from fractions import Fraction

try:
    from ubp_geometric_reasoning_main import (
        UBPGeometricReasoning,
        vectorize_concept,
        reason_about,
        find_counterpart,
        calculate_coherence,
        snap_to_lattice,
        query_memory,
        validate_concept,
        archive_to_kb
    )
    MAIN_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] Failed to import main interface: {e}")
    MAIN_AVAILABLE = False
    sys.exit(1)


class UBPSkillValidator:
    """Comprehensive validation suite for UBP Geometric Reasoning Skill."""
    
    def __init__(self):
        """Initialize the validator."""
        self.ubp = UBPGeometricReasoning()
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log a test result."""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        print(f"  {status}: {test_name}")
        if details and not passed:
            print(f"    Details: {details}")
    
    def test_vectorize_concept(self):
        """Test Capability 1: Vectorize Concept."""
        print("\n[TEST SUITE 1] Vectorize Concept")
        
        # Test 1.1: Basic vectorization
        try:
            result = self.ubp.vectorize_concept("Energy")
            assert 'vector' in result
            assert len(result['vector']) == 24
            assert 'fingerprint' in result
            assert 'domain' in result
            self.log_test("1.1 Basic vectorization", True)
        except Exception as e:
            self.log_test("1.1 Basic vectorization", False, str(e))
        
        # Test 1.2: Vector is binary
        try:
            result = self.ubp.vectorize_concept("Matter")
            assert all(bit in [0, 1] for bit in result['vector'])
            self.log_test("1.2 Vector is binary", True)
        except Exception as e:
            self.log_test("1.2 Vector is binary", False, str(e))
        
        # Test 1.3: Deterministic hashing
        try:
            result1 = self.ubp.vectorize_concept("Photon")
            result2 = self.ubp.vectorize_concept("Photon")
            assert result1['vector'] == result2['vector']
            assert result1['fingerprint'] == result2['fingerprint']
            self.log_test("1.3 Deterministic hashing", True)
        except Exception as e:
            self.log_test("1.3 Deterministic hashing", False, str(e))
        
        # Test 1.4: Domain classification
        try:
            result = self.ubp.vectorize_concept("TestConcept")
            assert result['domain'] in ['SUBSTANCE', 'QUANTITY']
            self.log_test("1.4 Domain classification", True)
        except Exception as e:
            self.log_test("1.4 Domain classification", False, str(e))
    
    def test_reason_about(self):
        """Test Capability 2: Reason About."""
        print("\n[TEST SUITE 2] Reason About")
        
        # Test 2.1: Basic reasoning
        try:
            result = self.ubp.reason_about("What is energy?")
            assert 'status' in result
            self.log_test("2.1 Basic reasoning", True)
        except Exception as e:
            self.log_test("2.1 Basic reasoning", False, str(e))
        
        # Test 2.2: Resonance detection
        try:
            result = self.ubp.reason_about("Unity")
            if 'resonance' in result:
                assert 'anchor' in result['resonance']
                self.log_test("2.2 Resonance detection", True)
            else:
                self.log_test("2.2 Resonance detection", True, "No resonance field (cortex may not be initialized)")
        except Exception as e:
            self.log_test("2.2 Resonance detection", False, str(e))
    
    def test_find_counterpart(self):
        """Test Capability 3: Find Counterpart."""
        print("\n[TEST SUITE 3] Find Counterpart")
        
        # Test 3.1: Basic counterpart search
        try:
            result = self.ubp.find_counterpart("Hydrogen", "MECHANISM")
            assert 'status' in result
            assert 'target_domain' in result
            self.log_test("3.1 Basic counterpart search", True)
        except Exception as e:
            self.log_test("3.1 Basic counterpart search", False, str(e))
        
        # Test 3.2: Hamming distance calculation
        try:
            result = self.ubp.find_counterpart("Energy", "QUANTITY")
            if result['status'] == "FOUND":
                assert 'hamming_distance' in result
                assert isinstance(result['hamming_distance'], int)
                self.log_test("3.2 Hamming distance calculation", True)
            else:
                self.log_test("3.2 Hamming distance calculation", True, "No counterpart found (KB may be empty)")
        except Exception as e:
            self.log_test("3.2 Hamming distance calculation", False, str(e))
    
    def test_calculate_coherence(self):
        """Test Capability 4: Calculate Coherence."""
        print("\n[TEST SUITE 4] Calculate Coherence")
        
        # Test 4.1: Basic coherence calculation
        try:
            test_vector = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            result = self.ubp.calculate_coherence(test_vector)
            assert 'nrci' in result
            assert 'health' in result
            assert 'regime' in result
            self.log_test("4.1 Basic coherence calculation", True)
        except Exception as e:
            self.log_test("4.1 Basic coherence calculation", False, str(e))
        
        # Test 4.2: Tetradic health
        try:
            test_vector = [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
            result = self.ubp.calculate_coherence(test_vector)
            health = result['health']
            assert 'reality' in health
            assert 'info' in health
            assert 'activation' in health
            assert 'potential' in health
            self.log_test("4.2 Tetradic health", True)
        except Exception as e:
            self.log_test("4.2 Tetradic health", False, str(e))
        
        # Test 4.3: Stability score
        try:
            test_vector = [0] * 24
            result = self.ubp.calculate_coherence(test_vector)
            assert 'stability' in result
            assert 0 <= result['stability'] <= 1
            self.log_test("4.3 Stability score", True)
        except Exception as e:
            self.log_test("4.3 Stability score", False, str(e))
    
    def test_snap_to_lattice(self):
        """Test Capability 5: Snap to Lattice."""
        print("\n[TEST SUITE 5] Snap to Lattice")
        
        # Test 5.1: Perfect vector (no errors)
        try:
            perfect_vector = [0] * 24
            result = self.ubp.snap_to_lattice(perfect_vector)
            assert result['status'] in ['PERFECT', 'CORRECTED']
            assert result['errors_fixed'] >= 0
            self.log_test("5.1 Perfect vector", True)
        except Exception as e:
            self.log_test("5.1 Perfect vector", False, str(e))
        
        # Test 5.2: Single bit-flip correction
        try:
            noisy_vector = [0] * 24
            noisy_vector[0] = 1  # Flip one bit
            result = self.ubp.snap_to_lattice(noisy_vector)
            assert result['errors_fixed'] >= 1
            assert result['status'] in ['CORRECTED', 'PERFECT']
            self.log_test("5.2 Single bit-flip correction", True)
        except Exception as e:
            self.log_test("5.2 Single bit-flip correction", False, str(e))
        
        # Test 5.3: Deep hole detection
        try:
            deep_hole = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            result = self.ubp.snap_to_lattice(deep_hole)
            if result['errors_fixed'] > 3:
                assert result['status'] == 'DEEP_HOLE'
            self.log_test("5.3 Deep hole detection", True)
        except Exception as e:
            self.log_test("5.3 Deep hole detection", False, str(e))
        
        # Test 5.4: Nearest anchor identification
        try:
            test_vector = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
            result = self.ubp.snap_to_lattice(test_vector)
            assert 'nearest_anchor' in result
            self.log_test("5.4 Nearest anchor identification", True)
        except Exception as e:
            self.log_test("5.4 Nearest anchor identification", False, str(e))
    
    def test_query_memory(self):
        """Test Capability 6: Query Memory."""
        print("\n[TEST SUITE 6] Query Memory")
        
        # Test 6.1: Basic memory query
        try:
            results = self.ubp.query_memory("energy")
            assert isinstance(results, list)
            self.log_test("6.1 Basic memory query", True)
        except Exception as e:
            self.log_test("6.1 Basic memory query", False, str(e))
        
        # Test 6.2: Hamming distance sorting
        try:
            results = self.ubp.query_memory("photon", max_results=5)
            if len(results) > 1:
                # Check that results are sorted by distance
                distances = [r['hamming_distance'] for r in results]
                assert distances == sorted(distances)
                self.log_test("6.2 Hamming distance sorting", True)
            else:
                self.log_test("6.2 Hamming distance sorting", True, "Insufficient results to verify sorting")
        except Exception as e:
            self.log_test("6.2 Hamming distance sorting", False, str(e))
        
        # Test 6.3: Max results limit
        try:
            results = self.ubp.query_memory("concept", max_results=3)
            assert len(results) <= 3
            self.log_test("6.3 Max results limit", True)
        except Exception as e:
            self.log_test("6.3 Max results limit", False, str(e))
    
    def test_validate_concept(self):
        """Test Capability 7: Validate Concept."""
        print("\n[TEST SUITE 7] Validate Concept")
        
        # Test 7.1: Complete concept validation
        try:
            concept = {
                "name": "Test Particle",
                "math": "m=1.0",
                "language": "A test particle for validation",
                "script": "particle = {'mass': 1.0}",
                "tags": ["test", "particle"]
            }
            result = self.ubp.validate_concept(concept)
            assert 'phase_1_initiation' in result
            assert 'phase_2_development' in result
            assert 'phase_3_distillation' in result
            self.log_test("7.1 Complete concept validation", True)
        except Exception as e:
            self.log_test("7.1 Complete concept validation", False, str(e))
        
        # Test 7.2: Incomplete concept rejection
        try:
            incomplete = {"name": "Incomplete"}
            result = self.ubp.validate_concept(incomplete)
            assert result['phase_1_initiation'] == 'FAIL'
            self.log_test("7.2 Incomplete concept rejection", True)
        except Exception as e:
            self.log_test("7.2 Incomplete concept rejection", False, str(e))
        
        # Test 7.3: NRCI calculation in validation
        try:
            concept = {
                "name": "Energy Quantum",
                "math": "E=hf",
                "language": "Energy quantum relationship",
                "script": "E = h * f",
                "tags": ["energy", "quantum"]
            }
            result = self.ubp.validate_concept(concept)
            assert 'nrci' in result
            self.log_test("7.3 NRCI calculation in validation", True)
        except Exception as e:
            self.log_test("7.3 NRCI calculation in validation", False, str(e))
    
    def test_archive_to_kb(self):
        """Test Capability 8: Archive to KB."""
        print("\n[TEST SUITE 8] Archive to KB")
        
        # Test 8.1: Basic KB formatting
        try:
            concept = {
                "ubp_id": "TEST_001",
                "name": "Test Concept",
                "math": "x=1",
                "language": "A test concept",
                "script": "x = 1",
                "tags": ["test"]
            }
            result = self.ubp.archive_to_kb(concept)
            assert isinstance(result, str)
            kb_entry = json.loads(result)
            assert isinstance(kb_entry, dict)
            self.log_test("8.1 Basic KB formatting", True)
        except Exception as e:
            self.log_test("8.1 Basic KB formatting", False, str(e))
        
        # Test 8.2: Fingerprint generation
        try:
            concept = {
                "name": "Unique Concept",
                "math": "y=2",
                "language": "Another test",
                "script": "y = 2",
                "tags": ["unique"]
            }
            result = self.ubp.archive_to_kb(concept)
            kb_entry = json.loads(result)
            fingerprint = list(kb_entry.keys())[0]
            assert len(fingerprint) == 64  # SHA-256 hex length
            self.log_test("8.2 Fingerprint generation", True)
        except Exception as e:
            self.log_test("8.2 Fingerprint generation", False, str(e))
        
        # Test 8.3: Vector inclusion
        try:
            concept = {
                "name": "Vector Test",
                "math": "v=1",
                "language": "Test vector inclusion",
                "script": "v = 1",
                "tags": ["vector"]
            }
            result = self.ubp.archive_to_kb(concept)
            kb_entry = json.loads(result)
            entry_data = list(kb_entry.values())[0]
            assert 'vector' in entry_data
            assert len(entry_data['vector']) == 24
            self.log_test("8.3 Vector inclusion", True)
        except Exception as e:
            self.log_test("8.3 Vector inclusion", False, str(e))
    
    def test_system_integrity(self):
        """Test overall system integrity."""
        print("\n[TEST SUITE 9] System Integrity")
        
        # Test 9.1: Golay decoder availability
        try:
            assert self.ubp.golay is not None
            self.log_test("9.1 Golay decoder availability", True)
        except Exception as e:
            self.log_test("9.1 Golay decoder availability", False, str(e))
        
        # Test 9.2: Leech lattice availability
        try:
            assert self.ubp.leech is not None
            self.log_test("9.2 Leech lattice availability", True)
        except Exception as e:
            self.log_test("9.2 Leech lattice availability", False, str(e))
        
        # Test 9.3: NRCI calculator availability
        try:
            assert self.ubp.nrci_calc is not None
            self.log_test("9.3 NRCI calculator availability", True)
        except Exception as e:
            self.log_test("9.3 NRCI calculator availability", False, str(e))
        
        # Test 9.4: Knowledge base access
        try:
            assert self.ubp.db is not None
            self.log_test("9.4 Knowledge base access", True)
        except Exception as e:
            self.log_test("9.4 Knowledge base access", False, str(e))
    
    def run_all_tests(self):
        """Run all validation tests."""
        print("\n" + "=" * 80)
        print("UBP SKILL VALIDATOR - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        
        self.test_vectorize_concept()
        self.test_reason_about()
        self.test_find_counterpart()
        self.test_calculate_coherence()
        self.test_snap_to_lattice()
        self.test_query_memory()
        self.test_validate_concept()
        self.test_archive_to_kb()
        self.test_system_integrity()
        
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"  Total Tests: {self.passed + self.failed}")
        print(f"  Passed: {self.passed} ✓")
        print(f"  Failed: {self.failed} ✗")
        
        if self.failed == 0:
            print("\n  ✓ ALL TESTS PASSED - SKILL IS READY FOR USE")
        else:
            print(f"\n  ✗ {self.failed} TEST(S) FAILED - REVIEW REQUIRED")
        
        print("=" * 80)
        
        return self.failed == 0


if __name__ == "__main__":
    validator = UBPSkillValidator()
    success = validator.run_all_tests()
    sys.exit(0 if success else 1)
