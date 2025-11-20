        >>> refined_back = apply_bidirectional_refinement(refined_fwd, 'backward')
        >>> print(f"Round-trip: {state.value} → {refined_fwd.value:.2f} → {refined_back.value:.2f}")
        Round-trip: 1000.0 → 264.68 → 1000.00
    """
    direction = direction.lower()
    
    if direction not in ['forward', 'backward']:
        raise ValueError(f"Direction must be 'forward' or 'backward', got '{direction}'")
    
    result = state
    for _ in range(iterations):
        if direction == 'forward':
            result = result.refine_forward()
        else:  # backward
            result = result.refine_backward()
    
    return result


def propagate_refinement_through_chain(
    initial_state: CoherenceState,
    chain_length: int = 5
) -> Dict[str, any]:
    """
    Propagate refinement through a forward-backward chain using CoherenceStates.
    
    This demonstrates the lossless nature of Y ↔ 1/Y refinement with
    full coherence tracking.
    
    Args: