#!/usr/bin/env python3.11
"""
Symbol Coherence Model - UBP Pipeline Implementation
Analogous to mineral_coherence_model_v3_recalibrated.py from minerals study

This module computes full UBP coherence features for mathematical symbols.
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase1/ubp_3.5')

import json
import numpy as np
from typing import Dict, List, Tuple
from coherence_substrate_v2 import CoherenceState, Y, Y_INVERSE, O_OBSERVER, NRCI_TARGET
import time

class SymbolCoherenceModel:
    """
    Compute UBP coherence features for mathematical symbols.
    
    Features computed:
    - Refinement operations (forward/backward Y-refinement)
    - Degradation (complexity penalty)
    - NRCI (Normalized Relative Coherence Index)
    - Net refinements
    - Bitfield features (8D property encoding)
    """
    
    def __init__(self, refinement_scale: float = 1.0, degradation_scale: float = 1.0):
        """
        Initialize the coherence model.
        
        Args:
            refinement_scale: Scaling factor for refinement operations
            degradation_scale: Scaling factor for degradation operations
        """
        self.refinement_scale = refinement_scale
        self.degradation_scale = degradation_scale
        
        print(f"Initialized SymbolCoherenceModel")
        print(f"  Refinement scale: {refinement_scale}")
        print(f"  Degradation scale: {degradation_scale}")
        print(f"  Y constant: {Y:.10f}")
        print(f"  Y_INVERSE: {Y_INVERSE:.10f}")
        print(f"  O_observer: {O_OBSERVER:.10f}")
        print(f"  NRCI target: {NRCI_TARGET:.10f}")
    
    def compute_refinement_score(self, symbol_data: Dict) -> float:
        """
        Compute refinement score based on symbol properties.
        
        Refinement drivers (order, structure, closure):
        - High closure degree → higher refinement
        - Full invertibility → higher refinement
        - High commutativity → higher refinement
        - Low dependency depth → higher refinement
        
        Args:
            symbol_data: Encoded symbol data
            
        Returns:
            Refinement score (higher = more ordered/structured)
        """
        props = symbol_data["properties"]
        bitfield = np.array(symbol_data["bitfield"])
        
        # Extract relevant dimensions
        invertibility = bitfield[2]  # D3: 0=none, 1=partial, 2=full
        commutativity = bitfield[3]  # D4: 0=no, 1=partial, 2=yes
        dependency_depth = bitfield[5]  # D6: compositional complexity
        closure_degree = bitfield[6]  # D7: 0=low, 1=medium, 2=high
        
        # Compute refinement score
        # Higher closure and invertibility increase refinement
        # Higher dependency depth decreases refinement
        refinement = 0.0
        
        # Closure contribution (0-2 scale)
        refinement += closure_degree * 0.4
        
        # Invertibility contribution (0-2 scale)
        refinement += invertibility * 0.3
        
        # Commutativity contribution (0-2 scale)
        refinement += commutativity * 0.2
        
        # Dependency depth penalty (1-3 scale, inverted)
        refinement += (4.0 - dependency_depth) * 0.1
        
        return refinement * self.refinement_scale
    
    def compute_degradation_score(self, symbol_data: Dict) -> float:
        """
        Compute degradation score based on symbol properties.
        
        Degradation drivers (ambiguity, complexity, overloading):
        - High meaning count → higher degradation
        - High overloading index → higher degradation
        - High dependency depth → higher degradation
        - Low closure → higher degradation
        
        Args:
            symbol_data: Encoded symbol data
            
        Returns:
            Degradation score (higher = more ambiguous/complex)
        """
        props = symbol_data["properties"]
        bitfield = np.array(symbol_data["bitfield"])
        
        # Extract relevant dimensions
        meaning_count_log = bitfield[4]  # D5: log(1 + meaning_count)
        dependency_depth = bitfield[5]  # D6: compositional complexity
        closure_degree = bitfield[6]  # D7: 0=low, 1=medium, 2=high
        overloading_log = bitfield[7]  # D8: log(1 + overloading_count)
        
        # Compute degradation score
        degradation = 0.0
        
        # Meaning count contribution (ambiguity)
        degradation += meaning_count_log * 0.3
        
        # Overloading contribution (semantic ambiguity)
        degradation += overloading_log * 0.4
        
        # Dependency depth contribution (compositional complexity)
        degradation += dependency_depth * 0.2
        
        # Closure penalty (inverted: low closure = high degradation)
        degradation += (2.0 - closure_degree) * 0.1
        
        return degradation * self.degradation_scale
    
    def apply_refinement_operations(
        self, 
        initial_state: CoherenceState,
        refinement_score: float
    ) -> CoherenceState:
        """
        Apply Y-refinement operations based on refinement score.
        
        Args:
            initial_state: Initial CoherenceState
            refinement_score: Refinement score (determines number of operations)
            
        Returns:
            Refined CoherenceState
        """
        # Number of refinement operations proportional to score
        num_refinements = int(refinement_score)
        
        state = initial_state
        for _ in range(num_refinements):
            state = state.refine_forward()
        
        return state
    
    def apply_degradation_operations(
        self,
        state: CoherenceState,
        degradation_score: float
    ) -> CoherenceState:
        """
        Apply degradation operations based on degradation score.
        
        Args:
            state: Current CoherenceState
            degradation_score: Degradation score (determines degradation amount)
            
        Returns:
            Degraded CoherenceState
        """
        # Degradation amount proportional to score
        # Use log-space degradation (correct way to accumulate error)
        delta_log_error = degradation_score * 0.01  # Scale factor
        
        degraded_state = state.degrade_by(delta_log_error)
        
        return degraded_state
    
    def compute_coherence_features(self, symbol_data: Dict) -> Dict:
        """
        Compute full UBP coherence features for a symbol.
        
        Args:
            symbol_data: Encoded symbol data
            
        Returns:
            Dictionary with coherence features
        """
        # Extract initial values
        initial_value = symbol_data["initial_value"]
        initial_nrci = symbol_data["initial_nrci"]
        bitfield = np.array(symbol_data["bitfield"])
        bitfield_magnitude = symbol_data["bitfield_magnitude"]
        
        # Initialize CoherenceState
        initial_state = CoherenceState(
            value=initial_value,
            metadata={'symbol_name': symbol_data["name"]}
        )
        
        # Compute refinement and degradation scores
        refinement_score = self.compute_refinement_score(symbol_data)
        degradation_score = self.compute_degradation_score(symbol_data)
        
        # Apply refinement operations
        refined_state = self.apply_refinement_operations(initial_state, refinement_score)
        
        # Apply degradation operations
        final_state = self.apply_degradation_operations(refined_state, degradation_score)
        
        # Compute final NRCI
        final_nrci = final_state.nrci
        
        # Compute net refinements
        net_refinements = final_state.net_refinements
        
        # Extract bitfield features
        bitfield_features = {
            f"bitfield_d{i+1}": float(bitfield[i]) for i in range(8)
        }
        
        # Compile features
        features = {
            # Core UBP features
            "nrci": float(final_nrci),
            "net_refinements": int(net_refinements),
            "refinement_score": float(refinement_score),
            "degradation_score": float(degradation_score),
            "final_value": float(final_state.value),
            
            # Bitfield features (8D)
            **bitfield_features,
            "bitfield_magnitude": float(bitfield_magnitude),
            
            # Initial state
            "initial_value": float(initial_value),
            "initial_nrci": float(initial_nrci),
            
            # Metadata
            "symbol": symbol_data["symbol"],
            "name": symbol_data["name"],
            "category": symbol_data["category"],
            "unicode": symbol_data["unicode"]
        }
        
        return features
    
    def process_dataset(self, encoded_dataset_path: str, output_path: str):
        """
        Process entire encoded dataset to compute coherence features.
        
        Args:
            encoded_dataset_path: Path to symbols_encoded.json
            output_path: Path to save processed dataset
        """
        # Load encoded dataset
        with open(encoded_dataset_path, 'r') as f:
            encoded_symbols = json.load(f)
        
        print(f"\nProcessing {len(encoded_symbols)} symbols...")
        start_time = time.time()
        
        # Process each symbol
        processed_symbols = []
        for i, symbol_data in enumerate(encoded_symbols):
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = (len(encoded_symbols) - i - 1) / rate
                print(f"  Processed {i + 1}/{len(encoded_symbols)} symbols "
                      f"({rate:.1f} sym/s, ETA: {remaining:.1f}s)")
            
            # Compute coherence features
            features = self.compute_coherence_features(symbol_data)
            processed_symbols.append(features)
        
        # Save processed dataset
        with open(output_path, 'w') as f:
            json.dump(processed_symbols, f, indent=2)
        
        elapsed = time.time() - start_time
        print(f"\nProcessed dataset saved to: {output_path}")
        print(f"Total time: {elapsed:.2f}s ({len(encoded_symbols)/elapsed:.1f} symbols/s)")
        
        # Print statistics
        self._print_coherence_statistics(processed_symbols)
    
    def _print_coherence_statistics(self, processed_symbols: List[Dict]):
        """Print statistics about computed coherence features."""
        nrcis = [s["nrci"] for s in processed_symbols]
        refinements = [s["refinement_score"] for s in processed_symbols]
        degradations = [s["degradation_score"] for s in processed_symbols]
        net_refs = [s["net_refinements"] for s in processed_symbols]
        
        print("\n" + "="*60)
        print("COHERENCE STATISTICS")
        print("="*60)
        
        print(f"\nNRCI:")
        print(f"  Range: [{min(nrcis):.10f}, {max(nrcis):.10f}]")
        print(f"  Mean:  {np.mean(nrcis):.10f}")
        print(f"  Std:   {np.std(nrcis):.10f}")
        
        print(f"\nRefinement Scores:")
        print(f"  Range: [{min(refinements):.6f}, {max(refinements):.6f}]")
        print(f"  Mean:  {np.mean(refinements):.6f}")
        print(f"  Std:   {np.std(refinements):.6f}")
        
        print(f"\nDegradation Scores:")
        print(f"  Range: [{min(degradations):.6f}, {max(degradations):.6f}]")
        print(f"  Mean:  {np.mean(degradations):.6f}")
        print(f"  Std:   {np.std(degradations):.6f}")
        
        print(f"\nNet Refinements:")
        print(f"  Range: [{min(net_refs)}, {max(net_refs)}]")
        print(f"  Mean:  {np.mean(net_refs):.2f}")
        print(f"  Std:   {np.std(net_refs):.2f}")
        
        # Category breakdown
        from collections import defaultdict
        category_nrcis = defaultdict(list)
        for s in processed_symbols:
            category_nrcis[s["category"]].append(s["nrci"])
        
        print(f"\nNRCI by Category:")
        for cat in sorted(category_nrcis.keys()):
            cat_nrcis = category_nrcis[cat]
            print(f"  {cat:20s}: {np.mean(cat_nrcis):.10f} ± {np.std(cat_nrcis):.10f} (n={len(cat_nrcis)})")
        
        print("\n" + "="*60)

def main():
    """Main execution function."""
    # Initialize model with calibrated scales
    model = SymbolCoherenceModel(
        refinement_scale=1.0,
        degradation_scale=500.0
    )
    
    encoded_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_encoded.json"
    output_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_processed.json"
    
    model.process_dataset(encoded_path, output_path)

if __name__ == "__main__":
    main()
