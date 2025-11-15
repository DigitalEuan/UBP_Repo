#!/usr/bin/env python3.11
"""
coherence_state_history.py - History-aware CoherenceState wrapper
Extends CoherenceState to track .history for archaeological decoding
"""
import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
from coherence_substrate import CoherenceState, Y, Y_INVERSE
from geometric_error_correction import restore_coherence

class HistoryAwareState:
    """CoherenceState with .history tracking"""
    
    def __init__(self, state: CoherenceState, history: list = None):
        self.state = state
        self.history = history if history is not None else ["OffBit(Potential)"]
    
    @property
    def value(self):
        return self.state.value
    
    @property
    def nrci(self):
        return self.state.nrci
    
    @property
    def log_nrci_error(self):
        return self.state.log_nrci_error
    
    def toggle(self, antigen: str) -> 'HistoryAwareState':
        """Apply toggle and record in history"""
        new_state = self.state * CoherenceState(-1.0)
        new_history = self.history + [f"Toggle({antigen})"]
        return HistoryAwareState(new_state, new_history)
    
    def restore(self) -> 'HistoryAwareState':
        """Restore coherence and record in history"""
        restored_state, _ = restore_coherence(self.state)
        delta = 1.0 - restored_state.nrci
        new_history = self.history + [f"Restore(δ={delta:.4f})"]
        return HistoryAwareState(restored_state, new_history)
    
    def bind_observer(self) -> 'HistoryAwareState':
        """Bind observer and record in history"""
        new_state = self.state * CoherenceState(Y_INVERSE)
        new_history = self.history + [f"Bind(Observer)→NRCI={new_state.nrci:.10f}"]
        return HistoryAwareState(new_state, new_history)
    
    def confess(self) -> str:
        """Return first-person confession of history"""
        confession = []
        for step in self.history:
            if "OffBit" in step:
                confession.append("I am M. I am potential.")
            elif "Toggle" in step:
                antigen = step.split("(")[1].split(")")[0]
                confession.append(f"I toggled {antigen}.")
            elif "Restore" in step:
                delta = step.split("δ=")[1].split(")")[0]
                confession.append(f"I remained (δ={delta}).")
            elif "Bind" in step:
                confession.append("I am referenced. I am here.")
        return " ".join(confession)
    
    def __repr__(self):
        return f"HistoryAwareState(value={self.value:.6f}, nrci={self.nrci:.10f}, history={len(self.history)} steps)"
