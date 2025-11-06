#!/usr/bin/env python3.11
"""
Simple UBP-Augmented LLM Query Example

This example demonstrates basic usage of the UBP-LLM system.
"""

import sys
import os

# Add UBP paths
ubp_repo_path = os.path.expanduser("~/UBP_Repo/ubp_3.4")
ubp_llm_path = os.path.expanduser("~/UBP_Repo/ubp_llm_1/core")

sys.path.insert(0, ubp_repo_path)
sys.path.insert(0, ubp_llm_path)

from llm_ubp_pipeline import LLMUBPPipeline

def main():
    """Run a simple query through the UBP-LLM pipeline."""
    
    print("=" * 80)
    print("UBP-Augmented LLM System - Simple Example")
    print("=" * 80)
    print()
    
    # Initialize pipeline
    print("Initializing UBP-LLM pipeline...")
    pipeline = LLMUBPPipeline(
        model="gpt-4.1-nano",  # Fastest model
        ubp_repo_path=ubp_repo_path
    )
    print("✓ Pipeline initialized")
    print()
    
    # Example query
    query = "What are the eigenvalues of the matrix [[2,1],[1,2]]? Explain their geometric meaning."
    
    print(f"Query: {query}")
    print()
    print("Processing through 7-layer UBP pipeline...")
    print("  [1/7] Three Column Thinking (TCT)")
    print("  [2/7] NRCI Coherence Validation")
    print("  [3/7] HexDictionary Knowledge Verification")
    print("  [4/7] GLR Error Correction")
    print("  [5/7] Observer Framework Optimization")
    print("  [6/7] SOC Energy Management")
    print("  [7/7] Knowledge Persistence")
    print()
    
    # Process query
    result = pipeline.process(
        query=query,
        nrci_threshold=0.80  # Recommended threshold
    )
    
    # Display results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"NRCI Score:        {result.nrci:.6f}")
    print(f"Regime:            {get_regime(result.nrci)}")
    print(f"Action:            {result.action}")
    print(f"GLR Corrections:   {result.glr_corrections}")
    print(f"Observer Status:   {'Converged' if result.observer_converged else 'Not converged'}")
    print(f"SOC Closure:       {result.soc_closure:.2e}")
    print(f"HexDict Hash:      {result.hexdict_hash[:16]}...")
    print()
    print("Response:")
    print("-" * 80)
    print(result.final_response)
    print("-" * 80)
    print()
    
    # Interpretation
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    print()
    
    if result.nrci >= 0.85:
        print("✓ Excellent coherence - response is highly reliable")
    elif result.nrci >= 0.80:
        print("✓ Good coherence - response is reliable")
    elif result.nrci >= 0.65:
        print("⚠ Moderate coherence - response may need correction")
    else:
        print("✗ Low coherence - response should be regenerated or rejected")
    
    if result.glr_corrections > 0:
        print(f"✓ GLR detected and corrected {result.glr_corrections} error(s)")
    
    if result.observer_converged:
        print("✓ Observer framework converged to geometric fixed point")
    
    if result.soc_closure < 1e-12:
        print("✓ Perfect SOC bidirectional closure")
    
    print()
    print("=" * 80)
    print("Example complete!")
    print("=" * 80)

def get_regime(nrci):
    """Get NRCI regime classification."""
    if nrci >= 0.999997:
        return "Supercoherent"
    elif nrci >= 0.99:
        return "Coherent"
    elif nrci >= 0.9:
        return "Semicoherent"
    elif nrci >= 0.5:
        return "Subcoherent"
    else:
        return "Decoherent"

if __name__ == "__main__":
    main()
