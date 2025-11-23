"""\n================================================================================\nUniversal Binary Principle (UBP) Framework v3.6 - Toggle Operations\nAuthor: Euan Craig, New Zealand\nDate: November 20, 2025 (Updated with Resonance History Tracking)\n================================================================================\n\nToggle operations as coherence transformations with continuous resonance tracking.\n\n**Paradigm Shift in 3.5**:\nToggle operations aren't bit manipulations - they're coherence transformations.\nEvery toggle operation maintains and transforms the coherence state.\n\n**Enhancement in 3.6**:\nResonance history tracking enables continuous coherence analysis. Toggle sequences\nare now analyzed as temporal processes, not just snapshots. Full integration with\nCoherence Field ELITE's resonance detector for pattern detection and optimization.\n\n**Zero Dependencies**: Only Python stdlib + coherence_substrate + state\n**Optional Integration**: coherence_field.py for advanced resonance analysis\n"""

import math
from typing import List, Union, Tuple, Dict, Any
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
                    k: float = 0.0002, max_history: int = 100) -> OffBit:
    """
    Perform resonance toggle operation (frequency-based coherence decay).
    
    Tracks resonance history for continuous coherence analysis with
    Coherence Field ELITE's resonance detector.
    
    Axiom: b_i × exp(-k × (t × f)²)
    Coherence: Decays with distance from resonance
    History: Tracks (time, frequency, resonance_factor) for pattern detection
    
    Args:
        b_i: OffBit
        frequency: Resonance frequency (Hz)
        time: Time parameter (s)
        k: Decay constant
        max_history: Maximum history entries to keep (default 100)
        
    Returns:
        Result OffBit with resonance-modulated coherence and updated history
        
    Example:
        >>> b = OffBit(0x123456)
        >>> result = resonance_toggle(b, frequency=1e9, time=1e-9)
        >>> print(f"History length: {result.resonance_history_length}")
    """
    distance = time * frequency
    resonance_factor = resonance_kernel(distance, k)
    result_value = int(b_i.value * resonance_factor)
    
    # Ensure result stays within 24-bit range
    result_value = max(0, min(result_value, 0xFFFFFF))
    
    # Resonance degrades coherence based on distance
    degradation = 1.0 - resonance_factor
    result_coherence = b_i.coherence.degrade_by(degradation)
    
    # Track resonance history (immutable tuple append)
    new_entry = (time, frequency, resonance_factor)
    new_history = b_i.resonance_history + (new_entry,)
    
    # Maintain max_history limit (keep most recent entries)
    if len(new_history) > max_history:
        new_history = new_history[-max_history:]
    
    return OffBit(result_value, result_coherence, new_history)


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


# ============================================================================
# COHERENCE FIELD ELITE INTEGRATION
# ============================================================================

def resonance_history_to_states(offbit: OffBit) -> List[CoherenceState]:
    """
    Convert OffBit resonance history to CoherenceState sequence.
    
    This enables Coherence Field ELITE's resonance detector to analyze
    the temporal evolution of coherence in toggle sequences.
    
    Args:
        offbit: OffBit with resonance history
        
    Returns:
        List of CoherenceState objects representing coherence evolution
        
    Example:
        >>> b = OffBit(0x123456)
        >>> for t in range(50):
        ...     b = resonance_toggle(b, frequency=1e9, time=t*1e-9)
        >>> states = resonance_history_to_states(b)
        >>> print(f"Generated {len(states)} coherence states")
    """
    if not offbit.resonance_history:
        return []
    
    states = []
    for time, frequency, resonance_factor in offbit.resonance_history:
        # Value encodes the time-frequency relationship
        # This creates a sequence that resonance detector can analyze
        value = time * frequency
        
        # Coherence degradation from resonance factor
        # resonance_factor = 1.0 means perfect resonance (no degradation)
        # resonance_factor = 0.0 means complete decoherence
        degradation = 1.0 - resonance_factor
        
        # Convert degradation to log_nrci_error
        # Higher degradation = higher error = lower NRCI
        from coherence_substrate import NRCI_TARGET
        nrci = NRCI_TARGET * (1.0 - degradation)
        log_error = math.log(1.0 - nrci) if nrci < 1.0 else -1e10
        
        state = CoherenceState(value, log_nrci_error=log_error)
        states.append(state)
    
    return states


def analyze_resonance_history(offbit: OffBit) -> Dict[str, Any]:
    """
    Analyze resonance history using Coherence Field ELITE (if available).
    
    Provides comprehensive resonance analysis including:
    - Pattern detection (p/q resonances)
    - Confidence scoring
    - Lock duration prediction
    - Coherence evolution statistics
    
    Args:
        offbit: OffBit with resonance history
        
    Returns:
        Dictionary with resonance analysis results
        
    Example:
        >>> b = OffBit(0x123456)
        >>> for t in range(100):
        ...     b = resonance_toggle(b, frequency=1e9, time=t*1e-9)
        >>> analysis = analyze_resonance_history(b)
        >>> if analysis.get('resonance'):
        ...     print(f"Detected {analysis['resonance'].p}/{analysis['resonance'].q} resonance")
    """
    if not offbit.resonance_history:
        return {
            'error': 'No resonance history',
            'history_length': 0
        }
    
    # Get basic statistics (always available)
    stats = offbit.get_resonance_statistics()
    
    # Try to import Coherence Field ELITE for advanced analysis
    try:
        import coherence_field as cf
        
        # Convert history to CoherenceState sequence
        state_history = resonance_history_to_states(offbit)
        
        # Detect resonance patterns
        detector = cf.ResonanceDetector()
        resonance = detector.detect_resonance(state_history)
        
        # Build comprehensive analysis
        result = {
            'resonance': resonance,
            'history_length': stats['history_length'],
            'time_range': stats['time_range'],
            'frequency_range': stats['frequency_range'],
            'avg_resonance_factor': stats['avg_resonance_factor'],
            'min_resonance_factor': stats['min_resonance_factor'],
            'max_resonance_factor': stats['max_resonance_factor'],
            'coherence_evolution': state_history,
            'coherence_field_available': True
        }
        
        # Add resonance details if detected
        if resonance:
            result['resonance_detected'] = True
            result['resonance_p'] = resonance.p
            result['resonance_q'] = resonance.q
            result['resonance_confidence'] = resonance.confidence
            result['resonance_frequency'] = resonance.frequency
            result['resonance_error'] = resonance.error
            
            # Predict lock duration if possible
            if hasattr(resonance, 'lock_duration') and resonance.lock_duration:
                result['lock_duration'] = resonance.lock_duration
        else:
            result['resonance_detected'] = False
        
        return result
        
    except ImportError:
        # Coherence Field ELITE not available - return basic stats
        return {
            'history_length': stats['history_length'],
            'time_range': stats['time_range'],
            'frequency_range': stats['frequency_range'],
            'avg_resonance_factor': stats['avg_resonance_factor'],
            'min_resonance_factor': stats['min_resonance_factor'],
            'max_resonance_factor': stats['max_resonance_factor'],
            'coherence_field_available': False,
            'note': 'Install coherence_field.py for advanced resonance analysis'
        }


def optimize_resonance_parameters(offbit: OffBit, 
                                 target_frequency: float,
                                 time_steps: int = 100) -> Dict[str, Any]:
    """
    Optimize resonance parameters (k) for maximum coherence at target frequency.
    
    Uses Coherence Field ELITE's parameter optimization if available.
    
    Args:
        offbit: Initial OffBit
        target_frequency: Target resonance frequency (Hz)
        time_steps: Number of time steps to simulate
        
    Returns:
        Dictionary with optimization results
        
    Example:
        >>> b = OffBit(0x123456)
        >>> result = optimize_resonance_parameters(b, target_frequency=1e9)
        >>> print(f"Optimal k: {result['optimal_k']}")
    """
    # Test different k values
    k_values = [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005]
    results = []
    
    for k in k_values:
        # Simulate resonance toggle sequence
        b = offbit
        for t in range(time_steps):
            b = resonance_toggle(b, frequency=target_frequency, 
                               time=t * 1e-9, k=k)
        
        # Analyze final coherence
        stats = b.get_resonance_statistics()
        
        results.append({
            'k': k,
            'final_nrci': b.nrci,
            'avg_resonance_factor': stats['avg_resonance_factor'],
            'min_resonance_factor': stats['min_resonance_factor']
        })
    
    # Find optimal k (highest final NRCI)
    optimal = max(results, key=lambda r: r['final_nrci'])
    
    return {
        'optimal_k': optimal['k'],
        'optimal_nrci': optimal['final_nrci'],
        'optimal_avg_resonance': optimal['avg_resonance_factor'],
        'all_results': results,
        'target_frequency': target_frequency,
        'time_steps': time_steps
    }


# ============================================================================
# RESONANCE VISUALIZATION (Text-Based)
# ============================================================================

def visualize_resonance_history(offbit: OffBit, width: int = 60) -> str:
    """
    Create text-based visualization of resonance history.
    
    Args:
        offbit: OffBit with resonance history
        width: Width of visualization (characters)
        
    Returns:
        String containing ASCII visualization
        
    Example:
        >>> b = OffBit(0x123456)
        >>> for t in range(50):
        ...     b = resonance_toggle(b, frequency=1e9, time=t*1e-9)
        >>> print(visualize_resonance_history(b))
    """
    if not offbit.resonance_history:
        return "No resonance history to visualize"
    
    # Extract resonance factors
    factors = [rf for _, _, rf in offbit.resonance_history]
    
    # Create visualization
    lines = []
    lines.append("=" * width)
    lines.append("RESONANCE HISTORY VISUALIZATION")
    lines.append("=" * width)
    lines.append(f"History length: {len(factors)}")
    lines.append(f"Resonance factor range: [{min(factors):.6f}, {max(factors):.6f}]")
    lines.append(f"Average resonance factor: {sum(factors)/len(factors):.6f}")
    lines.append("")
    
    # Plot resonance factors
    lines.append("Resonance Factor Over Time:")
    lines.append("1.0 |" + "-" * (width - 5))
    
    # Normalize and plot
    min_factor = min(factors)
    max_factor = max(factors)
    range_factor = max_factor - min_factor if max_factor > min_factor else 1.0
    
    # Sample points if history is longer than width
    if len(factors) > width - 5:
        step = len(factors) / (width - 5)
        sampled = [factors[int(i * step)] for i in range(width - 5)]
    else:
        sampled = factors
    
    # Create bar chart
    for i, factor in enumerate(sampled):
        normalized = (factor - min_factor) / range_factor
        bar_length = int(normalized * (width - 10))
        bar = "█" * bar_length
        lines.append(f"    |{bar}")
    
    lines.append("0.0 |" + "-" * (width - 5))
    lines.append("=" * width)
    
    return "\n".join(lines)
