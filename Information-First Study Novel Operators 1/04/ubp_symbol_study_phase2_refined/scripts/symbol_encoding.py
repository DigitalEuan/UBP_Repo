#!/usr/bin/env python3.11
"""
Symbol Encoding Module for UBP Study
Implements three-layer encoding: Unicode seed → Property bitfield → CoherenceState
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase2/ubp_3.5')

import json
import numpy as np
from typing import Dict, Tuple
from coherence_substrate_v2 import CoherenceState

class SymbolEncoder:
    """
    Encodes mathematical symbols for UBP analysis.
    
    Three-layer encoding:
    1. Unicode Seed: Deterministic base from codepoint
    2. Property Bitfield (8D): Intrinsic properties
    3. CoherenceState: Full UBP substrate integration
    """
    
    def __init__(self):
        """Initialize the encoder with property mappings."""
        # Arity mapping (D1)
        self.arity_map = {
            "nullary": 0,
            "unary": 1,
            "binary": 2,
            "ternary": 3
        }
        
        # Formal role mapping (D2)
        self.role_map = {
            "operand": 0,
            "operator": 1,
            "relation": 2,
            "quantifier": 3
        }
        
        # Invertibility mapping (D3)
        self.invertibility_map = {
            "none": 0,
            "partial": 1,
            "full": 2
        }
        
        # Commutativity mapping (D4)
        self.commutativity_map = {
            "no": 0,
            "partial": 1,
            "yes": 2
        }
        
        # Closure degree mapping (D7)
        self.closure_map = {
            "low": 0,
            "medium": 1,
            "high": 2
        }
        
    def extract_unicode_seed(self, unicode_str: str) -> float:
        """
        Extract Unicode codepoint as normalized seed value.
        
        Args:
            unicode_str: Unicode string like "U+002B"
            
        Returns:
            Normalized seed value in [0, 1]
        """
        # Extract hex value from Unicode string
        hex_value = unicode_str.replace("U+", "")
        codepoint = int(hex_value, 16)
        
        # Normalize to [0, 1] range
        # Unicode range: 0x0000 to 0x10FFFF (1,114,111 possible values)
        max_unicode = 0x10FFFF
        normalized = codepoint / max_unicode
        
        return normalized
    
    def compute_property_bitfield(self, symbol_data: Dict) -> np.ndarray:
        """
        Compute 8-dimensional property bitfield from intrinsic properties.
        
        Dimensions:
        D1: Arity (nullary=0, unary=1, binary=2, ternary=3)
        D2: Formal Role (operand=0, operator=1, relation=2, quantifier=3)
        D3: Invertibility (none=0, partial=1, full=2)
        D4: Commutativity (no=0, partial=1, yes=2)
        D5: Meaning Count (log scale, ambiguity measure)
        D6: Dependency Depth (compositional complexity)
        D7: Closure Degree (low=0, medium=1, high=2)
        D8: Overloading Index (log scale, semantic ambiguity)
        
        Args:
            symbol_data: Dictionary containing symbol metadata
            
        Returns:
            8D numpy array (bitfield)
        """
        bitfield = np.zeros(8, dtype=np.float64)
        
        # D1: Arity
        bitfield[0] = self.arity_map.get(symbol_data["arity"], 0)
        
        # D2: Formal Role
        bitfield[1] = self.role_map.get(symbol_data["formal_role"], 0)
        
        # D3: Invertibility
        bitfield[2] = self.invertibility_map.get(symbol_data["invertibility"], 0)
        
        # D4: Commutativity
        bitfield[3] = self.commutativity_map.get(symbol_data["commutativity"], 0)
        
        # D5: Meaning Count (log scale for ambiguity)
        meaning_count = symbol_data.get("meaning_count", 1)
        bitfield[4] = np.log1p(meaning_count)  # log(1 + x) for numerical stability
        
        # D6: Dependency Depth (compositional complexity)
        bitfield[5] = symbol_data.get("dependency_depth", 1)
        
        # D7: Closure Degree
        bitfield[6] = self.closure_map.get(symbol_data["closure_degree"], 1)
        
        # D8: Overloading Index (log scale for semantic ambiguity)
        overloading_count = len(symbol_data.get("overloading_contexts", []))
        bitfield[7] = np.log1p(overloading_count)
        
        return bitfield
    
    def compute_bitfield_magnitude(self, bitfield: np.ndarray) -> float:
        """
        Compute magnitude of bitfield vector.
        
        Args:
            bitfield: 8D property bitfield
            
        Returns:
            Euclidean norm of bitfield
        """
        return np.linalg.norm(bitfield)
    
    def initialize_coherence_state(
        self, 
        unicode_seed: float, 
        bitfield_magnitude: float,
        symbol_name: str
    ) -> CoherenceState:
        """
        Initialize CoherenceState from Unicode seed and bitfield magnitude.
        
        Args:
            unicode_seed: Normalized Unicode codepoint [0, 1]
            bitfield_magnitude: Magnitude of property bitfield
            symbol_name: Name of symbol for tracking
            
        Returns:
            Initialized CoherenceState
        """
        # Combine unicode seed with bitfield magnitude
        # Use weighted combination to preserve both sources of information
        combined_value = (unicode_seed + bitfield_magnitude) / 2.0
        
        # Initialize CoherenceState with default NRCI target
        # Store symbol name in metadata
        state = CoherenceState(
            value=combined_value,
            metadata={'symbol_name': symbol_name, 'unicode_seed': unicode_seed, 'bitfield_magnitude': bitfield_magnitude}
        )
        
        return state
    
    def encode_symbol(self, symbol_data: Dict) -> Tuple[float, np.ndarray, float, CoherenceState]:
        """
        Full three-layer encoding of a symbol.
        
        Args:
            symbol_data: Dictionary containing symbol metadata
            
        Returns:
            Tuple of (unicode_seed, bitfield, bitfield_magnitude, coherence_state)
        """
        # Layer 1: Unicode Seed
        unicode_seed = self.extract_unicode_seed(symbol_data["unicode"])
        
        # Layer 2: Property Bitfield
        bitfield = self.compute_property_bitfield(symbol_data)
        bitfield_magnitude = self.compute_bitfield_magnitude(bitfield)
        
        # Layer 3: CoherenceState Initialization
        coherence_state = self.initialize_coherence_state(
            unicode_seed,
            bitfield_magnitude,
            symbol_data["name"]
        )
        
        return unicode_seed, bitfield, bitfield_magnitude, coherence_state
    
    def encode_dataset(self, dataset_path: str, output_path: str):
        """
        Encode entire symbol dataset.
        
        Args:
            dataset_path: Path to symbols_dataset.json
            output_path: Path to save encoded dataset
        """
        # Load dataset
        with open(dataset_path, 'r') as f:
            symbols = json.load(f)
        
        print(f"Encoding {len(symbols)} symbols...")
        
        # Encode each symbol
        encoded_symbols = []
        for i, symbol_data in enumerate(symbols):
            if (i + 1) % 50 == 0:
                print(f"  Encoded {i + 1}/{len(symbols)} symbols...")
            
            # Perform encoding
            unicode_seed, bitfield, bitfield_mag, coherence_state = self.encode_symbol(symbol_data)
            
            # Create encoded entry
            encoded_entry = {
                # Original metadata
                "symbol": symbol_data["symbol"],
                "unicode": symbol_data["unicode"],
                "name": symbol_data["name"],
                "category": symbol_data["category"],
                
                # Encoding layer 1: Unicode seed
                "unicode_seed": float(unicode_seed),
                
                # Encoding layer 2: Property bitfield
                "bitfield": bitfield.tolist(),
                "bitfield_magnitude": float(bitfield_mag),
                
                # Encoding layer 3: CoherenceState (initial values)
                "initial_nrci": float(coherence_state.nrci),
                "initial_value": float(coherence_state.value),
                
                # Store original properties for validation
                "properties": {
                    "arity": symbol_data["arity"],
                    "formal_role": symbol_data["formal_role"],
                    "invertibility": symbol_data["invertibility"],
                    "commutativity": symbol_data["commutativity"],
                    "meaning_count": symbol_data["meaning_count"],
                    "dependency_depth": symbol_data["dependency_depth"],
                    "closure_degree": symbol_data["closure_degree"],
                    "overloading_contexts": symbol_data["overloading_contexts"]
                }
            }
            
            encoded_symbols.append(encoded_entry)
        
        # Save encoded dataset
        with open(output_path, 'w') as f:
            json.dump(encoded_symbols, f, indent=2)
        
        print(f"\nEncoded dataset saved to: {output_path}")
        
        # Print encoding statistics
        self._print_encoding_statistics(encoded_symbols)
    
    def _print_encoding_statistics(self, encoded_symbols: list):
        """Print statistics about the encoding."""
        unicode_seeds = [s["unicode_seed"] for s in encoded_symbols]
        bitfield_mags = [s["bitfield_magnitude"] for s in encoded_symbols]
        initial_nrcis = [s["initial_nrci"] for s in encoded_symbols]
        
        print("\n" + "="*60)
        print("ENCODING STATISTICS")
        print("="*60)
        
        print(f"\nUnicode Seeds:")
        print(f"  Range: [{min(unicode_seeds):.6f}, {max(unicode_seeds):.6f}]")
        print(f"  Mean:  {np.mean(unicode_seeds):.6f}")
        print(f"  Std:   {np.std(unicode_seeds):.6f}")
        
        print(f"\nBitfield Magnitudes:")
        print(f"  Range: [{min(bitfield_mags):.6f}, {max(bitfield_mags):.6f}]")
        print(f"  Mean:  {np.mean(bitfield_mags):.6f}")
        print(f"  Std:   {np.std(bitfield_mags):.6f}")
        
        print(f"\nInitial NRCI:")
        print(f"  Range: [{min(initial_nrcis):.6f}, {max(initial_nrcis):.6f}]")
        print(f"  Mean:  {np.mean(initial_nrcis):.6f}")
        print(f"  Std:   {np.std(initial_nrcis):.6f}")
        
        print("\n" + "="*60)

def main():
    """Main execution function."""
    encoder = SymbolEncoder()
    
    dataset_path = "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_dataset_phase2.json"
    output_path = "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_encoded.json"
    
    encoder.encode_dataset(dataset_path, output_path)

if __name__ == "__main__":
    main()
