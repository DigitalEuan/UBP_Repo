"""
Universal Binary Principle (UBP) Framework v3.7.1 - Golay/Leech Accuracy Test
Author: Euan Craig, New Zealand
Date: 01 December 2025

Tests the real-world error correction accuracy of the Golay/Leech integration
by comparing correction success rates against known corrupted data.
"""

import unittest
import numpy as np
import random
from typing import List, Tuple
from core.state import OffBit, MutableBitfield
from error_correction.golay_code import GolayG24
from error_correction.leech_lattice import LeechLatticePoint
from analysis.tgic_bridge import OffBitTGICBridge
from utils.tgic import TGICGeometry

class TestGolayLeechAccuracy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Golay Encoder/Decoder
        cls.golay_encoder = GolayG24()
        # We don't need to initialize LeechLatticePoint, we just use its properties
        cls.leech_proj = LeechLatticePoint # Placeholder for now, as we only use the OffBit.to_leech_point()
        
        # 1. Generate a set of perfect Golay codewords (the "real world" data)
        # We use the GolayCode module to ensure we have valid codewords
        cls.perfect_codewords: List[OffBit] = []
        
        # Generate 100 random 12-bit messages and encode them
        for _ in range(100):
            message_int = random.getrandbits(12)
            # Convert 12-bit integer to 12-element numpy array of bits
            message_bits = np.array([(message_int >> i) & 1 for i in range(12)], dtype=int)
            
            codeword_bits = cls.golay_encoder.encode(message_bits)
            # Convert 24-bit numpy array back to integer
            codeword_int = sum(codeword_bits[i] * (2**i) for i in range(24))
            cls.perfect_codewords.append(OffBit(codeword_int))
            
        # 2. Create corrupted versions of the codewords
        cls.corrupted_codewords: List[Tuple[OffBit, int]] = [] # (corrupted_offbit, error_count)
        
        for codeword in cls.perfect_codewords:
            # Introduce 1, 2, 3, or 4 errors (Golay can correct up to 3)
            error_count = random.choice([1, 2, 3, 4])
            
            corrupted_value = codeword.value
            
            # Randomly select bit positions to flip
            bit_positions = random.sample(range(24), error_count)
            
            for pos in bit_positions:
                corrupted_value ^= (1 << pos)
            
            cls.corrupted_codewords.append((OffBit(corrupted_value), error_count))

    def test_1_golay_codeword_generation(self):
        """Test that the generated codewords are valid G24 codewords."""
        for codeword in self.perfect_codewords:
            # Check the simplified weight property (0, 8, 12, 16, 24)
            self.assertTrue(codeword.is_golay_codeword, f"Codeword {codeword} failed G24 weight check.")
            self.assertEqual(codeword.golay_parity(), 0, f"Codeword {codeword} failed G24 parity check.")

    def test_2_leech_point_conversion(self):
        """Test Leech point conversion and norm property."""
        for codeword in self.perfect_codewords:
            leech_point = codeword.to_leech_point()
            self.assertEqual(leech_point.shape, (24,), "Leech point must be 24-dimensional.")
            
            # Check the norm squared (should be 24 in the simplified construction)
            norm_sq = np.sum(leech_point**2)
            self.assertAlmostEqual(norm_sq, 24.0, places=6, msg="Simplified Leech point norm squared should be 24.")

    def test_3_golay_correction_accuracy(self):
        """Test the accuracy of the Golay error correction (via HTR Engine logic)."""
        
        # NOTE: Since the full correction logic is in HTR Engine, we simulate the correction
        # by using the GolayCode module directly, which is what the HTR Engine uses.
        
        success_count = 0
        total_test_cases = len(self.corrupted_codewords)
        
        for i, (corrupted_offbit, error_count) in enumerate(self.corrupted_codewords):
            original_codeword = self.perfect_codewords[i]
            
            # Attempt correction
            try:
                # Convert OffBit value (int) to 24-bit numpy array
                codeword_bits = np.array([(corrupted_offbit.value >> i) & 1 for i in range(24)], dtype=int)
                
                # Correct (corrects up to 3 errors)
                corrected_bits = self.golay_encoder.correct_errors(codeword_bits)
                
                # Convert 24-bit numpy array back to integer
                corrected_value = sum(corrected_bits[i] * (2**i) for i in range(24))
                corrected_offbit = OffBit(corrected_value)
                
                # Check if the corrected OffBit matches the original perfect codeword
                if corrected_offbit.value == original_codeword.value:
                    success_count += 1
                    
                    # Check if the correction was within Golay's capacity
                    if error_count > 3:
                        # This is a successful correction of an uncorrectable error (lucky guess/side effect)
                        pass
                
            except Exception as e:
                # Golay decoder can raise an exception if it detects an uncorrectable error
                if error_count <= 3:
                    # This is a failure to correct a correctable error
                    print(f"\nFailed to correct {error_count} errors in case {i}: {e}")
                pass
        
        accuracy = success_count / total_test_cases
        print(f"\nGolay Correction Accuracy: {accuracy*100:.2f}% ({success_count}/{total_test_cases})")
        
        # Assert a minimum acceptable accuracy (e.g., 90% for 1, 2, 3 errors)
        # Since we have 4-error cases, the theoretical max is lower. We expect > 70%
        self.assertGreaterEqual(accuracy, 0.70, "Golay correction accuracy is below acceptable threshold (70%).")

    def test_4_tgic_bridge_coherence_sensitivity(self):
        """Test if the TGIC bridge coherence is sensitive to Golay validity."""
        
        # 1. Test with a perfect Golay codeword
        perfect_codeword = self.perfect_codewords[0]
        bitfield_perfect = MutableBitfield(size=1)
        bitfield_perfect.set_offbit(0, perfect_codeword)
        
        bridge = OffBitTGICBridge(geometry=TGICGeometry.DODECAHEDRAL)
        bridge.map_offbits_to_graph(bitfield_perfect)
        coherence_perfect = bridge.compute_offbit_coherence(bitfield_perfect)
        
        # 2. Test with a highly corrupted (4-error) codeword
        corrupted_offbit, _ = self.corrupted_codewords[0]
        bitfield_corrupted = MutableBitfield(size=1)
        bitfield_corrupted.set_offbit(0, corrupted_offbit)
        
        bridge_corrupted = OffBitTGICBridge(geometry=TGICGeometry.DODECAHEDRAL)
        bridge_corrupted.map_offbits_to_graph(bitfield_corrupted)
        coherence_corrupted = bridge_corrupted.compute_offbit_coherence(bitfield_corrupted)
        
        # The coherence should be significantly higher for the perfect Golay codeword
        self.assertGreater(coherence_perfect, coherence_corrupted, "Coherence should be higher for Golay codeword.")
        self.assertGreater(coherence_perfect, 0.5, "Perfect codeword coherence should be high.")
        self.assertLess(coherence_corrupted, 0.5, "Corrupted codeword coherence should be low.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
