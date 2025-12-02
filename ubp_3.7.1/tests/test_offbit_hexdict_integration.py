"""
Universal Binary Principle (UBP) Framework v3.7.1 - OffBit/HexDictionary Integration Test
Author: Euan Craig, New Zealand
Date: 01 December 2025

Comprehensive test suite for the core OffBit structure and its integration with
the HexDictionary and new advanced modules (HTR, RDGL, Pattern Integrator).
"""
import unittest
import numpy as np
import os
import shutil
from typing import Dict, Any

# Core Modules
from core.state import OffBit, MutableBitfield
from utils.hex_dictionary import HexDictionary
from utils.ubp_pattern_integrator import UBPPatternIntegrator
from utils.rdgl import RDGL
from analysis.dissident_horizon_oracle import DissidentHorizonOracle
from error_correction.htr_engine import HTREngine
from utils.tgic import TGICGeometry

# Configuration
STORAGE_DIR = os.path.abspath("./persistent_state/test_hex_dictionary_storage/")

class TestOffBitHexDictIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Clean up before all tests
        if os.path.exists(STORAGE_DIR):
            shutil.rmtree(STORAGE_DIR)
        os.makedirs(STORAGE_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests
        if os.path.exists(STORAGE_DIR):
            shutil.rmtree(STORAGE_DIR)

    def setUp(self):
        # Initialize HexDictionary for each test
        # HexDictionary needs the absolute path to correctly manage files
        self.hex_dict = HexDictionary(storage_dir=STORAGE_DIR)

    # --- OffBit Core Tests ---
    def test_offbit_initialization_and_layers(self):
        # Test 24-bit constraint
        with self.assertRaises(ValueError):
            OffBit(0x1000000) # 25th bit set
        
        offbit = OffBit(0xFC0001) # 1 in Reality, FC in Unactivated
        self.assertEqual(offbit.value, 0xFC0001)
        self.assertEqual(offbit.hamming_weight(), 1 + 6) # 1 + 6 bits in FC
        self.assertTrue(offbit.is_active)

    def test_offbit_bit_manipulation(self):
        offbit = OffBit(0x000000)
        
        # Set bit 5 (Reality Layer)
        offbit = offbit.set_bit(5, 1)
        self.assertEqual(offbit.value, 0x20)
        
        # Toggle bit 15 (Activation Layer)
        offbit = offbit.toggle_bit(15)
        self.assertEqual(offbit.value, 0x8020)
        
        # Set bit 5 to 0
        offbit = offbit.set_bit(5, 0)
        self.assertEqual(offbit.value, 0x8000)

    # --- HexDictionary Integration Tests ---
    def test_hexdict_offbit_storage(self):
        offbit_val = OffBit(0x123456)
        
        # Store the OffBit's value as an integer
        offbit_hash = self.hex_dict.store(offbit_val.value, 'int', metadata={'source': 'test_storage'})
        self.assertIsNotNone(offbit_hash)
        
        # Retrieve and verify
        retrieved_val, meta = self.hex_dict.retrieve(offbit_hash)
        self.assertEqual(retrieved_val, offbit_val.value)
        self.assertEqual(meta['source'], 'test_storage')

    def test_hexdict_bitfield_storage(self):
        bitfield = MutableBitfield(size=5)
        bitfield.set_offbit(0, OffBit(0xAAAAAA))
        bitfield.set_offbit(4, OffBit(0xBBBBBB))
        
        # Store the underlying numpy array
        bitfield_hash = self.hex_dict.store(bitfield.data, 'array', metadata={'type': 'bitfield_state'})
        
        # Retrieve and verify
        retrieved_data, meta = self.hex_dict.retrieve(bitfield_hash)
        self.assertTrue(np.array_equal(bitfield.data, retrieved_data))
        self.assertEqual(meta['type'], 'bitfield_state')

    # --- Advanced Module Integration Tests ---
    def test_ubp_pattern_integrator(self):
        # Use the test's HexDictionary instance for the integrator to ensure a single source of truth
        integrator = UBPPatternIntegrator(storage_dir=STORAGE_DIR)
        integrator.hex_dict = self.hex_dict # Force integrator to use the test's instance
        
        pattern = np.random.rand(10, 10)
        pattern_hash = integrator.integrate_pattern(pattern, 'geometric', 'quantum', 'Test Pattern')
        
        # Verify storage and metadata
        # Retrieval should now work as the HexDictionary instance is the same
        retrieved_pattern, meta = self.hex_dict.retrieve(pattern_hash)
        self.assertTrue(np.array_equal(pattern, retrieved_pattern))
        self.assertEqual(meta['data_type'], 'ubp_pattern')
        self.assertIn('geometric_signature', meta['pattern_details'])

    def test_htr_engine_layer_reversal(self):
        htr = HTREngine()
        offbit = OffBit(0x000001) # Bit 0 set (Reality Layer)
        
        # Reverse Reality Layer (0x00003F)
        reversed_reality = htr.reverse_layer(offbit, 'reality')
        self.assertEqual(reversed_reality.value, 0x00003E) # All 6 bits set except bit 0
        
        # Reverse Information Layer (0x000FC0)
        offbit = OffBit(0x000400) # Bit 10 set
        reversed_info = htr.reverse_layer(offbit, 'information')
        self.assertEqual(reversed_info.value, 0x000BC0) # 0x000FC0 ^ 0x000400 = 0x000BC0

    def test_rdgl_logic_application(self):
        # RDGL uses TGIC, so this tests the full stack
        rdgl = RDGL(geometry=TGICGeometry.CUBIC)
        bitfield = MutableBitfield(size=10)
        
        # Apply logic (should not raise error)
        new_bitfield = rdgl.apply_logic(bitfield)
        
        # Check if the bitfield was modified (simple check)
        self.assertIsInstance(new_bitfield, MutableBitfield)
        self.assertEqual(new_bitfield.size, 10)

    def test_dissident_horizon_oracle(self):
        oracle = DissidentHorizonOracle(geometry=TGICGeometry.DODECAHEDRAL)
        bitfield = MutableBitfield(size=10)
        
        # Set a high coherence state
        for i in range(10):
            bitfield.set_offbit(i, OffBit(0xFFFFFF))
            
        analysis = oracle.analyze_bitfield(bitfield)
        
        # Check for key metrics
        self.assertIn('dissidence_score', analysis)
        self.assertIn('bitfield_coherence', analysis)
        self.assertIn('enhanced_nrci_score', analysis)
        self.assertIsInstance(analysis['is_dissident_state'], bool)
        
        # Check if coherence is high
        self.assertGreater(analysis['bitfield_coherence'], 0.5)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
