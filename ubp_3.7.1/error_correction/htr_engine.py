"""
Universal Binary Principle (UBP) Framework v3.7.1 - Hierarchical Toggle Reversal (HTR) Engine
Author: Euan Craig, New Zealand
Date: 01 December 2025

Implements the HTR Engine for advanced error correction and state reversal.
Leverages the 24-bit OffBit structure for targeted layer reversal.
"""
import numpy as np
from typing import Dict, Any, List, Tuple
from core.state import OffBit
from error_correction.golay_code import GolayG24
from error_correction.leech_lattice import LeechLattice

class HTREngine:
    """
    Hierarchical Toggle Reversal Engine.
    Performs multi-layered error correction and state reversal using Golay and Leech structures.
    """
    def __init__(self):
        self.golay_corrector = GolayG24()
        self.leech_corrector = LeechLattice()

    def _get_layer_mask(self, layer_name: str) -> int:
        """
        Returns the 6-bit mask for the specified OffBit layer.
        
        Layers:
        - Reality Layer (bits 0-5)
        - Information Layer (bits 6-11)
        - Activation Layer (bits 12-17)
        - Unactivated Layer (bits 18-23)
        """
        masks = {
            "reality": 0x00003F,  # bits 0-5
            "information": 0x000FC0, # bits 6-11
            "activation": 0x03F000, # bits 12-17
            "unactivated": 0xFC0000  # bits 18-23
        }
        if layer_name.lower() not in masks:
            raise ValueError(f"Invalid layer name: {layer_name}. Must be one of {list(masks.keys())}")
        return masks[layer_name.lower()]

    def reverse_layer(self, offbit: OffBit, layer_name: str) -> OffBit:
        """
        Reverses (toggles) all bits within a specific layer of the OffBit.
        
        Args:
            offbit: The OffBit to modify.
            layer_name: The name of the layer to reverse.
            
        Returns:
            A new OffBit with the specified layer reversed.
        """
        mask = self._get_layer_mask(layer_name)
        new_value = offbit.value ^ mask
        return OffBit(new_value)

    def apply_error_correction(self, offbit: OffBit) -> OffBit:
        """
        Applies hierarchical error correction (Golay then Leech) to the OffBit.
        
        Args:
            offbit: The OffBit potentially containing errors.
            
        Returns:
            The corrected OffBit.
        """
        # 1. Golay Correction (24-bit data)
        data_to_correct = offbit.extract_data()
        corrected_data = self.golay_corrector.correct_data(data_to_correct)
        
        # 2. Leech Lattice Check (24D structure check)
        # The Leech check is typically a validation, not a direct correction on the 24-bit value
        # Here, we simulate a check that might adjust the Activation Layer based on Leech proximity
        is_valid_leech_point = self.leech_corrector.is_valid_point(corrected_data)
        
        # If not a valid Leech point, force a toggle in the Activation Layer (bits 12-17)
        if not is_valid_leech_point:
            # This is a heuristic correction based on the Leech structure
            activation_mask = self._get_layer_mask("activation")
            corrected_data ^= activation_mask # Toggle the activation layer
            
        return OffBit(corrected_data)

# Add to error_correction/__init__.py for easy import
# from .htr_engine import HTREngine
