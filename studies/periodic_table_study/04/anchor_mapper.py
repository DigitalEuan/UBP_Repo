"""
================================================================================
Anchor Mapper - UBP 3.5 Module for Detecting Coherence Anchors
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

A tool for detecting coherence anchors in biological and physical systems.

Coherence anchors are stable, high-NRCI, pre-biological invariants that serve
as reference frames for complex systems. They are characterized by:
- δ-deficit ≈ 0.001 (NRCI ≈ 0.999)
- Power-of-2 state count (2^k structure)
- Stability across perturbations

This module provides an Anchor Confidence Score (ACS) to quantify how likely
a given system represents a coherence anchor.
"""

import sys
import os
import json
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET


# ============================================================================
# ANCHOR SIGNATURE
# ============================================================================

@dataclass
class AnchorSignature:
    """
    Signature of a potential coherence anchor.
    """
    name: str
    num_states: int
    mean_delta: float
    mean_nrci: float
    delta_std: float
    binary_purity: float
    anchor_confidence_score: float
    is_anchor: bool
    domain: str


# ============================================================================
# ANCHOR MAPPER
# ============================================================================

class AnchorMapper:
    """
    Detect and characterize coherence anchors in biological systems.
    """
    
    # Weights for ACS calculation
    W_DELTA = 0.5      # Weight for δ-deficit proximity to 0.001
    W_BINARY = 0.3     # Weight for binary purity (2^k structure)
    W_STABILITY = 0.2  # Weight for δ stability (low std)
    
    # Thresholds
    DELTA_TARGET = 0.001
    DELTA_TOLERANCE = 0.01
    ACS_THRESHOLD = 0.7  # Minimum ACS to be considered an anchor
    
    def __init__(self):
        self.anchors = []
    
    def analyze_system(
        self,
        name: str,
        states: List[Dict[str, Any]],
        domain: str = "biological"
    ) -> AnchorSignature:
        """
        Analyze a system to determine if it's a coherence anchor.
        
        Args:
            name: Name of the system (e.g., "ABO/Rh")
            states: List of state dictionaries with 'nrci' or 'delta' keys
            domain: Domain of the system (biological, cosmological, etc.)
        
        Returns:
            AnchorSignature with analysis results
        """
        num_states = len(states)
        
        # Extract δ-deficits
        deltas = []
        for state in states:
            if 'delta' in state:
                deltas.append(state['delta'])
            elif 'nrci' in state:
                deltas.append(1.0 - state['nrci'])
            else:
                raise ValueError("States must have 'delta' or 'nrci' key")
        
        # Calculate statistics
        mean_delta = sum(deltas) / len(deltas)
        mean_nrci = 1.0 - mean_delta
        delta_std = math.sqrt(sum((d - mean_delta)**2 for d in deltas) / len(deltas))
        
        # Calculate binary purity
        binary_purity = self._calculate_binary_purity(num_states)
        
        # Calculate Anchor Confidence Score (ACS)
        acs = self._calculate_acs(mean_delta, binary_purity, delta_std)
        
        # Determine if this is an anchor
        is_anchor = (
            acs >= self.ACS_THRESHOLD and
            abs(mean_delta - self.DELTA_TARGET) < self.DELTA_TOLERANCE
        )
        
        signature = AnchorSignature(
            name=name,
            num_states=num_states,
            mean_delta=mean_delta,
            mean_nrci=mean_nrci,
            delta_std=delta_std,
            binary_purity=binary_purity,
            anchor_confidence_score=acs,
            is_anchor=is_anchor,
            domain=domain,
        )
        
        if is_anchor:
            self.anchors.append(signature)
        
        return signature
    
    def _calculate_binary_purity(self, num_states: int) -> float:
        """
        Calculate how close num_states is to a power of 2.
        
        Returns:
            1.0 if perfect power of 2, decreasing as it deviates
        """
        if num_states <= 0:
            return 0.0
        
        log2_n = math.log2(num_states)
        nearest_power = round(log2_n)
        deviation = abs(log2_n - nearest_power)
        
        # Binary purity: 1.0 for perfect 2^k, 0.0 for maximum deviation
        binary_purity = 1.0 - min(deviation, 1.0)
        
        return binary_purity
    
    def _calculate_acs(self, mean_delta: float, binary_purity: float, delta_std: float) -> float:
        """
        Calculate Anchor Confidence Score (ACS).
        
        ACS = w1 * (1 - |δ - 0.001|) + w2 * binary_purity + w3 * (1 - δ_std)
        """
        # δ-deficit proximity score
        delta_score = 1.0 - min(abs(mean_delta - self.DELTA_TARGET) / self.DELTA_TOLERANCE, 1.0)
        
        # Stability score (inverse of std)
        stability_score = 1.0 - min(delta_std / 0.01, 1.0)
        
        # Weighted sum
        acs = (
            self.W_DELTA * delta_score +
            self.W_BINARY * binary_purity +
            self.W_STABILITY * stability_score
        )
        
        return acs
    
    def get_anchor_registry(self) -> List[Dict[str, Any]]:
        """
        Get list of all detected anchors.
        """
        return [
            {
                "name": anchor.name,
                "num_states": anchor.num_states,
                "mean_delta": anchor.mean_delta,
                "mean_nrci": anchor.mean_nrci,
                "acs": anchor.anchor_confidence_score,
                "domain": anchor.domain,
            }
            for anchor in self.anchors
        ]
    
    def print_analysis(self, signature: AnchorSignature):
        """
        Print analysis results in a readable format.
        """
        print("=" * 80)
        print(f"Anchor Analysis: {signature.name}")
        print("=" * 80)
        print(f"Domain: {signature.domain}")
        print(f"Number of states: {signature.num_states}")
        print(f"Mean δ-deficit: {signature.mean_delta:.6f}")
        print(f"Mean NRCI: {signature.mean_nrci:.6f}")
        print(f"δ-deficit std: {signature.delta_std:.6f}")
        print(f"Binary purity: {signature.binary_purity:.3f}")
        print(f"Anchor Confidence Score (ACS): {signature.anchor_confidence_score:.3f}")
        print()
        if signature.is_anchor:
            print("✅ COHERENCE ANCHOR DETECTED")
        else:
            print("❌ Not a coherence anchor")
        print("=" * 80)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    mapper = AnchorMapper()
    
    # Test with ABO/Rh blood types (from our study)
    print("Testing Anchor Mapper with known systems...\n")
    
    # ABO/Rh system (8 states, δ ≈ 0.0009)
    abo_rh_states = [
        {"nrci": 0.9991} for _ in range(8)  # All 8 blood types have similar NRCI
    ]
    
    abo_signature = mapper.analyze_system(
        name="ABO/Rh Blood Types",
        states=abo_rh_states,
        domain="biological"
    )
    mapper.print_analysis(abo_signature)
    
    print()
    
    # Hypothetical tRNA codons (64 states, δ unknown - assume 0.002)
    trna_states = [
        {"delta": 0.002 + (i % 3) * 0.0001} for i in range(64)
    ]
    
    trna_signature = mapper.analyze_system(
        name="tRNA Codons",
        states=trna_states,
        domain="biological"
    )
    mapper.print_analysis(trna_signature)
    
    print()
    
    # Non-anchor example: Random biological system (37 states, δ ≈ 0.05)
    random_states = [
        {"delta": 0.05 + (i % 10) * 0.01} for i in range(37)
    ]
    
    random_signature = mapper.analyze_system(
        name="Random Biological System",
        states=random_states,
        domain="biological"
    )
    mapper.print_analysis(random_signature)
    
    # Print anchor registry
    print("\n" + "=" * 80)
    print("COHERENCE ANCHOR REGISTRY (CAR)")
    print("=" * 80)
    
    registry = mapper.get_anchor_registry()
    if registry:
        for anchor in registry:
            print(f"{anchor['name']:30s} | States: {anchor['num_states']:4d} | "
                  f"δ: {anchor['mean_delta']:.6f} | ACS: {anchor['acs']:.3f} | "
                  f"Domain: {anchor['domain']}")
    else:
        print("No coherence anchors detected.")
    
    # Save registry
    output_file = "/home/ubuntu/blood_type_ubp_study_v2/coherence_anchor_registry.json"
    with open(output_file, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"\nRegistry saved to: {output_file}")
