    """
    Restore coherence using a coherence pattern.
    
    This is the 3.5 equivalent of "decode with error correction" - but
    understood as restoring natural coherence, not correcting errors.
    
    Args:
        state: CoherenceState to restore
        pattern: Optional CoherencePattern to use (default: Golay)
        
    Returns:
        Tuple of (restored_state, restoration_info)
        
    Example:
        >>> state = CoherenceState(1000.0, log_nrci_error=-5.0)
        >>> restored, info = restore_coherence(state)
        >>> print(f"Restored NRCI: {restored.nrci:.6f}")
    """
    if pattern is None:
        pattern = GolayPattern()
    
    # Decode using pattern
    restored, deviations = pattern.decode_state(state)
    
    # Analyze restoration
    original_nrci = state.nrci
    restored_nrci = restored.nrci
    improvement = restored_nrci - original_nrci
    
    info = {
        'pattern': pattern.name,
        'original_nrci': original_nrci,
        'restored_nrci': restored_nrci,
        'improvement': improvement,
        'deviations': deviations,
        'success': improvement > 0
    }
    
    return restored, info


# ============================================================================
# GLOBAL COHERENCE MANAGEMENT
# ============================================================================

class GlobalCoherenceManager:
    """
    Manage coherence across multiple states/systems.