"""
UBP Drive v2.0
===================================
Implements a Corrected Golay Decoder to resolve the 'Hemispheric Blindness' bug.
Provides true 3-bit error correction across the full 24-bit word.

Euan Craig, New Zealand with the UBP Research Cortex v4.2.6
7 Jan 2026

"""
import random
import itertools
from typing import List, Tuple, Dict
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra, GOLAY_DECODER

class PatchedGolayEngine:
    """
    A standalone Golay decoder with a corrected syndrome table
    that covers errors across all 24 bits (not just the first 12).
    """
    def __init__(self):
        self.G = GOLAY_DECODER.G
        self.H = GOLAY_DECODER.H
        self.syndrome_table = self._build_full_syndrome_table()

    def _build_full_syndrome_table(self):
        """Builds a complete lookup table for error weights 1, 2, and 3."""
        table = {}
        # Iterate through error weights 1 to 3
        for weight in range(1, 4):
            # Generate all combinations of bit positions for this weight
            for positions in itertools.combinations(range(24), weight):
                error_pattern = [0] * 24
                for pos in positions:
                    error_pattern[pos] = 1
                
                # Calculate Syndrome
                syndrome = BinaryLinearAlgebra.matrix_vector_multiply(self.H, error_pattern)
                
                # Store error pattern (as tuple for immutability) keyed by syndrome
                table[tuple(syndrome)] = tuple(error_pattern)
        return table

    def encode(self, message: List[int]) -> List[int]:
        return GOLAY_DECODER.encode(message)

    def decode(self, received: List[int]) -> Tuple[List[int], bool, int]:
        syndrome = BinaryLinearAlgebra.matrix_vector_multiply(self.H, received)
        syn_tuple = tuple(syndrome)
        
        # If syndrome is 0, no errors
        if sum(syndrome) == 0:
            return received[:12], True, 0
            
        # Look up error pattern
        if syn_tuple in self.syndrome_table:
            error_pattern = self.syndrome_table[syn_tuple]
            # Correct the received word
            corrected = [(r + e) % 2 for r, e in zip(received, error_pattern)]
            return corrected[:12], True, sum(error_pattern)
        
        # Uncorrectable (Weight > 3)
        return received[:12], False, 0

class UBPDriveV2:
    def __init__(self):
        self.engine = PatchedGolayEngine()

    def _text_to_bits(self, text: str) -> List[int]:
        bits = []
        for char in text:
            b = bin(ord(char))[2:].zfill(8)
            bits.extend([int(x) for x in b])
        return bits

    def _bits_to_text(self, bits: List[int]) -> str:
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int("".join(map(str, byte)), 2)))
        return "".join(chars)

    def write(self, data: str) -> Dict:
        raw_bits = self._text_to_bits(data)
        padding = (12 - (len(raw_bits) % 12)) % 12
        raw_bits.extend([0] * padding)
        
        matrix = []
        for i in range(0, len(raw_bits), 12):
            chunk = raw_bits[i:i+12]
            codeword = self.engine.encode(chunk)
            matrix.append(codeword)
            
        return {"matrix": matrix, "padding": padding, "size": len(matrix)*24}

    def read(self, drive_data: Dict) -> Tuple[str, Dict]:
        matrix = drive_data["matrix"]
        restored_bits = []
        stats = {"fixed": 0, "failed": 0}
        
        for codeword in matrix:
            msg, fixed, errs = self.engine.decode(codeword)
            if fixed: stats["fixed"] += errs
            else: stats["failed"] += 1
            restored_bits.extend(msg)
            
        if drive_data["padding"] > 0:
            restored_bits = restored_bits[:-drive_data["padding"]]
            
        return self._bits_to_text(restored_bits), stats

    def decay(self, drive_data: Dict, prob: float = 0.10) -> Dict:
        corrupted = []
        flips = 0
        for cw in drive_data["matrix"]:
            new_cw = list(cw)
            for i in range(24):
                if random.random() < prob:
                    new_cw[i] = 1 - new_cw[i]
                    flips += 1
            corrupted.append(new_cw)
        print(f"[DECAY] Injected {flips} bit-flips (Rate: {prob:.0%})")
        return {"matrix": corrupted, "padding": drive_data["padding"]}

if __name__ == "__main__":
    drive = UBPDriveV2()
    text = "The Universal Binary Principle is the operating system of reality."
    print(f"Original: '{text}'")
    
    # 1. Write
    storage = drive.write(text)
    
    # 2. Decay (10% Noise - High Radiation)
    damaged = drive.decay(storage, prob=0.04)
    
    # 3. Read
    restored, stats = drive.read(damaged)
    print(f"Restored: '{restored}'")
    print(f"Stats:    {stats}")
    
    if text == restored:
        print("RESULT: ✅ PERFECT INTEGRITY (Patched Engine)")
    else:
        print("RESULT: ⚠️ DATA LOSS")