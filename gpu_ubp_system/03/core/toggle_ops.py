"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - Toggle Operations
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Toggle operations as coherence transformations.

**Paradigm Shift in 3.5**:
Toggle operations aren't bit manipulations - they're coherence transformations.
Every toggle operation maintains and transforms the coherence state.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + state
"""

import math
from typing import List, Union, Tuple
from state import OffBit
from coherence_substrate import CoherenceState, Y


# ============================================================================
# BASIC TOGGLE OPERATIONS (Coherence-Preserving)
# ============================================================================

def toggle_and(b_i: OffBit, b_j: OffBit) -> OffBit:
    """
    Perform AND toggle operation (coherence-preserving).
    
    Axiom: min(b_i, b_j)
    Coherence: Combined coherence of both inputs
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        
    Returns:
        Result OffBit with combined coherence
        
    Example:
        >>> b1 = OffBit(0x123456)
        >>> b2 = OffBit(0xABCDEF)
        >>> result = toggle_and(b1, b2)
    """
    result_value = min(b_i.value, b_j.value)
    
    # Combine coherence states (multiply for AND - both must be coherent)
    combined_coherence = CoherenceState(
        result_value,
        log_nrci_error=b_i.coherence.log_nrci_error + b_j.coherence.log_nrci_error
    )
    
    return OffBit(result_value, combined_coherence)


def toggle_xor(b_i: OffBit, b_j: OffBit) -> OffBit:
    """
    Perform XOR toggle operation (coherence-transforming).
    
    Axiom: |b_i - b_j|
    Coherence: Difference creates new coherence state
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        
    Returns:
        Result OffBit with transformed coherence
        
    Example:
        >>> b1 = OffBit(0x123456)
        >>> b2 = OffBit(0x123450)
        >>> result = toggle_xor(b1, b2)
    """
    result_value = abs(b_i.value - b_j.value)
    
    # XOR is a coherence transformation - apply Y-refinement
    avg_log_error = (b_i.coherence.log_nrci_error + b_j.coherence.log_nrci_error) / 2
    base_coherence = CoherenceState(result_value, log_nrci_error=avg_log_error)
    combined_coherence = base_coherence.refine_forward()
    
    return OffBit(result_value, combined_coherence)


def toggle_or(b_i: OffBit, b_j: OffBit) -> OffBit:
    """
    Perform OR toggle operation (coherence-selecting).
    
    Axiom: max(b_i, b_j)
    Coherence: Select coherence of dominant input
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        
    Returns:
        Result OffBit with selected coherence
        
    Example:
        >>> b1 = OffBit(0x123456)
        >>> b2 = OffBit(0xABCDEF)
        >>> result = toggle_or(b1, b2)
    """
    result_value = max(b_i.value, b_j.value)
    
    # OR selects the dominant coherence
    if b_i.value >= b_j.value:
        combined_coherence = b_i.coherence
    else:
        combined_coherence = b_j.coherence
    
    return OffBit(result_value, combined_coherence)


# ============================================================================
# RESONANCE OPERATIONS (Frequency-Based Coherence)
# ============================================================================

def resonance_kernel(distance: float, k: float = 0.0002) -> float:
    """
    Resonance decay kernel.
    
    Args:
        distance: Distance parameter (time × frequency)
        k: Decay constant
        
    Returns:
        Resonance factor (0 to 1)
    """
    return math.exp(-k * distance * distance)


def resonance_toggle(b_i: OffBit, frequency: float, time: float, 
                    k: float = 0.0002) -> OffBit:
    """
    Perform resonance toggle operation (frequency-based coherence decay).
    
    Axiom: b_i × exp(-k × (t × f)²)
    Coherence: Decays with distance from resonance
    
    Args:
        b_i: OffBit
        frequency: Resonance frequency (Hz)
        time: Time parameter (s)
        k: Decay constant
        
    Returns:
        Result OffBit with resonance-modulated coherence
        
    Example:
        >>> b = OffBit(0x123456)
        >>> result = resonance_toggle(b, frequency=1e9, time=1e-9)
    """
    distance = time * frequency
    resonance_factor = resonance_kernel(distance, k)
    result_value = int(b_i.value * resonance_factor)
    
    # Ensure result stays within 24-bit range
    result_value = max(0, min(result_value, 0xFFFFFF))
    
    # Resonance degrades coherence based on distance
    degradation = 1.0 - resonance_factor
    result_coherence = b_i.coherence.degrade_by(degradation)
    
    return OffBit(result_value, result_coherence)


# ============================================================================
# ENTANGLEMENT OPERATIONS (Cross-Layer Coherence)
# ============================================================================

def entanglement_toggle(b_i: OffBit, b_j: OffBit, 
                       coherence_threshold: float = 0.95) -> OffBit:
    """
    Perform entanglement toggle operation (cross-layer coupling).
    
    Axiom: b_i × b_j × C_ij (where C_ij ≥ 0.95)
    Coherence: Strong coupling only when both are coherent
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        coherence_threshold: Minimum coherence for strong entanglement
        
    Returns:
        Result OffBit with entangled coherence
        
    Example:
        >>> b1 = OffBit(0x100)
        >>> b2 = OffBit(0x200)
        >>> result = entanglement_toggle(b1, b2)
    """
    # Check if both OffBits meet coherence threshold
    both_coherent = (b_i.nrci >= coherence_threshold and 
                     b_j.nrci >= coherence_threshold)
    
    if both_coherent:
        # Strong entanglement
        coupling_factor = min(b_i.nrci, b_j.nrci)
        result_value = int(b_i.value * b_j.value * coupling_factor)
        
        # Entanglement creates new coherence state
        combined_log_error = (b_i.coherence.log_nrci_error + 
                             b_j.coherence.log_nrci_error) / 2
        result_coherence = CoherenceState(result_value, log_nrci_error=combined_log_error)
    else:
        # Weak entanglement
        coupling_factor = min(b_i.nrci, b_j.nrci) * 0.1
        result_value = int(b_i.value * b_j.value * coupling_factor)
        
        # Weak entanglement degrades coherence
        worse_coherence = b_i.coherence if b_i.nrci < b_j.nrci else b_j.coherence
        result_coherence = worse_coherence.degrade_by(0.1)
    
    # Ensure result stays within 24-bit range
    result_value = max(0, min(result_value, 0xFFFFFF))
    
    return OffBit(result_value, result_coherence)


# ============================================================================
# SUPERPOSITION OPERATIONS (Probabilistic Coherence)
# ============================================================================

def superposition_toggle(states: List[OffBit], 
                        weights: List[float]) -> OffBit:
    """
    Perform superposition toggle operation (probabilistic state).
    
    Axiom: Σ(states × weights) where Σ weights = 1
    Coherence: Weighted average of all coherence states
    
    Args:
        states: List of OffBit states
        weights: List of probability weights (must sum to 1)
        
    Returns:
        Result OffBit with superposed coherence
        
    Example:
        >>> states = [OffBit(0x100), OffBit(0x200), OffBit(0x300)]
        >>> weights = [0.5, 0.3, 0.2]
        >>> result = superposition_toggle(states, weights)
    """
    if len(states) != len(weights):
        raise ValueError("States and weights must have same length")
    
    if not states:
        return OffBit(0)
    
    # Normalize weights
    total_weight = sum(weights)
    if total_weight == 0:
        return OffBit(0)
    
    normalized_weights = [w / total_weight for w in weights]
    
    # Weighted sum of values
    result_value = sum(s.value * w for s, w in zip(states, normalized_weights))
    result_value = int(result_value)
    result_value = max(0, min(result_value, 0xFFFFFF))
    
    # Weighted average of coherence
    weighted_log_error = sum(s.coherence.log_nrci_error * w 
                             for s, w in zip(states, normalized_weights))
    
    result_coherence = CoherenceState(result_value, log_nrci_error=weighted_log_error)
    
    return OffBit(result_value, result_coherence)


# ============================================================================
# ADVANCED OPERATIONS
# ============================================================================

def hybrid_xor_resonance(b_i: OffBit, b_j: OffBit, 
                        frequency: float, time: float) -> OffBit:
    """
    Hybrid XOR with resonance modulation.
    
    Combines XOR transformation with frequency-based decay.
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        frequency: Resonance frequency
        time: Time parameter
        
    Returns:
        Result OffBit with hybrid coherence
    """
    # First apply XOR
    xor_result = toggle_xor(b_i, b_j)
    
    # Then apply resonance
    result = resonance_toggle(xor_result, frequency, time)
    
    return result


def spin_transition(b_i: OffBit, transition_probability: float) -> OffBit:
    """
    Spin transition operation (quantum-inspired).
    
    Models spin flip with given probability.
    
    Args:
        b_i: OffBit
        transition_probability: Probability of transition (0 to 1)
        
    Returns:
        Result OffBit with transitioned state
    """
    if transition_probability >= 1.0:
        # Certain transition - full toggle
        return b_i.toggle()
    elif transition_probability <= 0.0:
        # No transition
        return b_i
    else:
        # Partial transition - weighted superposition
        return superposition_toggle(
            [b_i, b_i.toggle()],
            [1.0 - transition_probability, transition_probability]
        )


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 TOGGLE OPERATIONS - Coherence Transformations")
    print("=" * 80)
    
    # Create test OffBits
    print("\n1. Creating Test OffBits:")
    b1 = OffBit(0x123456)
    b2 = OffBit(0xABCDEF)
    print(f"   b1: {b1}")
    print(f"   b2: {b2}")
    
    # Basic operations
    print("\n2. Basic Toggle Operations:")
    and_result = toggle_and(b1, b2)
    xor_result = toggle_xor(b1, b2)
    or_result = toggle_or(b1, b2)
    print(f"   AND: {and_result}")
    print(f"   XOR: {xor_result}")
    print(f"   OR:  {or_result}")
    
    # Resonance
    print("\n3. Resonance Toggle:")
    res_result = resonance_toggle(b1, frequency=1e9, time=1e-9)
    print(f"   Original: {b1}")
    print(f"   Resonant: {res_result}")
    print(f"   NRCI change: {res_result.nrci - b1.nrci:.10f}")
    
    # Entanglement
    print("\n4. Entanglement Toggle:")
    ent_result = entanglement_toggle(b1, b2)
    print(f"   Entangled: {ent_result}")
    print(f"   NRCI: {ent_result.nrci:.10f}")
    
    # Superposition
    print("\n5. Superposition Toggle:")
    states = [OffBit(0x100000), OffBit(0x200000), OffBit(0x300000)]
    weights = [0.5, 0.3, 0.2]
    sup_result = superposition_toggle(states, weights)
    print(f"   Superposed: {sup_result}")
    print(f"   NRCI: {sup_result.nrci:.10f}")
    
    # Hybrid
    print("\n6. Hybrid XOR-Resonance:")
    hyb_result = hybrid_xor_resonance(b1, b2, frequency=1e9, time=1e-9)
    print(f"   Hybrid: {hyb_result}")
    
    # Spin transition
    print("\n7. Spin Transition:")
    spin_result = spin_transition(b1, transition_probability=0.3)
    print(f"   Original: {b1}")
    print(f"   Transitioned: {spin_result}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Toggle Operations are Coherence Transformations")
    print("Zero external dependencies - Pure coherence geometry")
    print("=" * 80)
