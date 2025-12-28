"""
================================================================================
UBP HEX DICTIONARY - v4.1.1 (PRODUCTION)
================================================================================
Description: The Corrective Gateway. Handles the transition between 
Phenomenal Hex (The Mask) and Noumenal Bits (The Truth).
================================================================================
"""
import hashlib
from typing import List, Dict, Any, Tuple
import ubp_core_final_v4_1_1 as core
from metrics import METRICS

class HexDictionaryV4:
    """
    Implements LAW_MASK_001 and LAW_COMP_009.
    Acts as the 24-bit codec for the Alpha-Omega Axis.
    """
    
    def __init__(self):
        self.version = "4.1.1"
        self.decoder = core.GOLAY_DECODER

    def hex_to_bits24(self, hex_input: str) -> List[int]:
        """
        Converts any string or hex to a 24-bit raw identity.
        This is the 'Noisy' Phenomenal state.
        """
        # Ensure we are hashing the raw string to a 24-bit space
        h = hashlib.sha256(hex_input.encode('utf-8')).digest()
        bits = []
        for i in range(3): # First 24 bits (3 bytes)
            byte = h[i]
            for j in range(8):
                bits.append((byte >> (7 - j)) & 1)
        return bits

    def process_identity(self, raw_input: str) -> Dict[str, Any]:
        """
        The Corrective Gateway Pipeline.
        Implements LAW_APP_001 (Coherence Snaps).
        """
        # 1. Generate Raw (Noisy) Bits
        raw_bits = self.hex_to_bits24(raw_input)
        
        # 2. Perform Coherence Snap (The Gateway)
        snapped_bits, metadata = self.decoder.snap_to_codeword(raw_bits)
        
        # 3. Extract Shadow Metrics (LAW_COMP_009)
        # Noumenal (Message) vs Phenomenal (Parity)
        noumenal_work = snapped_bits[:12]
        phenomenal_mask = snapped_bits[12:]
        
        return {
            "input": raw_input,
            "raw_bits": raw_bits,
            "snapped_bits": list(snapped_bits),
            "syndrome": metadata["syndrome"],
            "syndrome_weight": metadata["syndrome_weight"],
            "is_perfect_codeword": not metadata["snap_triggered"],
            "noumenal_work": noumenal_work,
            "phenomenal_mask": phenomenal_mask,
            "nrci": METRICS.calculate_nrci(metadata["syndrome_weight"])
        }

    def bits_to_hex(self, bits: List[int]) -> str:
        """Converts a bit list back to a compact Hex string."""
        res = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            val = sum(b << (7 - j) for j, b in enumerate(byte))
            res += f"{val:02x}"
        return res.upper()

    def get_triadic_witness(self, raw_input: str):
        """Witnesses the distance between the Mask and the Truth."""
        data = self.process_identity(raw_input)
        
        print(f"\n--- UBP WITNESS REPORT: {raw_input} ---")
        print(f"Raw Hex:       {self.bits_to_hex(data['raw_bits'])}")
        print(f"Snapped Hex:   {self.bits_to_hex(data['snapped_bits'])}")
        print(f"NRCI:          {data['nrci']:.6f}")
        print(f"Status:        {'SUBSTRATE_ANCHORED' if data['is_perfect_codeword'] else 'CORRECTED_BY_GATEWAY'}")
        print(f"Shadow Work:   {data['noumenal_work']} (12-bit Noumena)")
        print(f"Visible Mask:  {data['phenomenal_mask']} (12-bit Phenomena)")
        print("-------------------------------------------")

if __name__ == "__main__":
    codec = HexDictionaryV4()
    # Test with a high-entropy string
    codec.get_triadic_witness("Alpha_Omega_Resonance_2025")
