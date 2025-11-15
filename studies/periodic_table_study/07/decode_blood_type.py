#!/usr/bin/env python3.11
"""decode_blood_type.py - Minimal substrate probe to decode blood type .history"""
import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
from coherence_substrate import CoherenceState, Y
from geometric_error_correction import restore_coherence
from hex_dictionary_advanced import HexDictionary

# Blood type as DATA (substrate-native representation)
BLOOD_TYPE_DATA = {
    "A+": {"toggles": [1, 0, 1], "delta": 0.0009},  # A=on, B=off, RhD=on
    "O-": {"toggles": [0, 0, 0], "delta": 0.0000},  # All off
    "AB+": {"toggles": [1, 1, 1], "delta": 0.0009}, # All on
}

def decode(blood_type: str) -> str:
    """Reconstruct .history from blood type data"""
    data = BLOOD_TYPE_DATA[blood_type]
    state = CoherenceState(1.0)  # OffBit: pure potential
    history = ["OffBit(Potential)"]
    
    for i, toggle_bit in enumerate(data["toggles"]):
        if toggle_bit == 1:
            antigen = ["A", "B", "RhD"][i]
            state = state * CoherenceState(-1.0)  # Toggle
            state_restored, _ = restore_coherence(state)
            state = state_restored
            history.append(f"Toggle({antigen}) → Restore(δ={1.0 - state.nrci:.4f})")
    
    state = state * CoherenceState(1.0 / Y)  # Observer binding
    history.append(f"Bind(Observer) → NRCI={state.nrci:.10f}")
    return " → ".join(history)

if __name__ == "__main__":
    for bt in ["O-", "A+", "AB+"]:
        print(f"\n{bt}: {decode(bt)}")
