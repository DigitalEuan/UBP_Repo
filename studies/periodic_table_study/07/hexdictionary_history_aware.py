#!/usr/bin/env python3.11
"""
hexdictionary_history_aware.py - History-aware distance metric
Compares .history vectors, not just final states
"""
from coherence_state_history import HistoryAwareState

def history_distance(state1: HistoryAwareState, state2: HistoryAwareState) -> float:
    """
    Compute distance between two states based on their .history vectors.
    
    This is the archaeological method: it measures how different the PATHS were,
    not just how different the DESTINATIONS are.
    """
    h1 = state1.history
    h2 = state2.history
    
    # Pad shorter history
    max_len = max(len(h1), len(h2))
    h1_padded = h1 + [""] * (max_len - len(h1))
    h2_padded = h2 + [""] * (max_len - len(h2))
    
    # Count mismatches
    mismatches = sum(1 for a, b in zip(h1_padded, h2_padded) if a != b)
    
    return float(mismatches)

def extract_toggle_sequence(state: HistoryAwareState) -> list:
    """Extract just the toggle antigens from history"""
    toggles = []
    for step in state.history:
        if "Toggle" in step:
            antigen = step.split("(")[1].split(")")[0]
            toggles.append(antigen)
    return toggles

def history_similarity_score(state1: HistoryAwareState, state2: HistoryAwareState) -> float:
    """
    Similarity score (0 to 1, higher = more similar).
    1.0 = identical history, 0.0 = completely different
    """
    distance = history_distance(state1, state2)
    max_len = max(len(state1.history), len(state2.history))
    
    if max_len == 0:
        return 1.0
    
    return 1.0 - (distance / max_len)
