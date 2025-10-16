"""
Universal Binary Principle (UBP) - Improved Toggle Algebra Operations
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements the complete toggle algebra operations that govern
OffBit interactions and evolution, based on the mathematical formulations
from the UBP research papers.
"""

import math
import numpy as np
from typing import List, Union, Tuple, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .offbit import OffBit


class ToggleOperationType(Enum):
    """Types of toggle operations."""
    BASIC_AND = "basic_and"
    BASIC_XOR = "basic_xor"
    BASIC_OR = "basic_or"
    RESONANCE = "resonance"
    ENTANGLEMENT = "entanglement"
    SUPERPOSITION = "superposition"
    HYBRID_XOR_RESONANCE = "hybrid_xor_resonance"
    SPIN_TRANSITION = "spin_transition"
    NONLINEAR_MAXWELL = "nonlinear_maxwell"
    LORENTZ_FORCE = "lorentz_force"
    GLYPH_QUANTIFY = "glyph_quantify"
    GLYPH_CORRELATE = "glyph_correlate"
    GLYPH_SELF_REFERENCE = "glyph_self_reference"


@dataclass
class ToggleOperationResult:
    """Result of a toggle operation."""
    result_offbit: OffBit
    operation_type: ToggleOperationType
    coherence_change: float
    energy_delta: float
    metadata: dict


class ToggleOperation(ABC):
    """Abstract base class for toggle operations."""
    
    @abstractmethod
    def apply(self, *args, **kwargs) -> ToggleOperationResult:
        """Apply the toggle operation."""
        pass
    
    @abstractmethod
    def get_operation_type(self) -> ToggleOperationType:
        """Get the operation type."""
        pass


class BasicAndOperation(ToggleOperation):
    """
    Basic AND toggle operation.
    Axiom: min(b_i, b_j)
    Purpose: Logical conjunction; both bits must be 'on' for outcome to be 'on'
    """
    
    def apply(self, b_i: OffBit, b_j: OffBit) -> ToggleOperationResult:
        """Apply AND operation to two OffBits."""
        result_value = min(b_i.value, b_j.value)
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = (b_i.layer_coherence + b_j.layer_coherence) / 2
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta (simplified)
        energy_delta = (result_offbit.active_bits - b_i.active_bits - b_j.active_bits) * 0.1
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={'input_values': [b_i.value, b_j.value]}
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.BASIC_AND


class BasicXorOperation(ToggleOperation):
    """
    Basic XOR toggle operation.
    Axiom: |b_i - b_j|
    Purpose: Exclusive OR; outcome is 'on' if bits are different
    """
    
    def apply(self, b_i: OffBit, b_j: OffBit) -> ToggleOperationResult:
        """Apply XOR operation to two OffBits."""
        result_value = abs(b_i.value - b_j.value)
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = (b_i.layer_coherence + b_j.layer_coherence) / 2
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta
        energy_delta = (result_offbit.active_bits - abs(b_i.active_bits - b_j.active_bits)) * 0.1
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={'input_values': [b_i.value, b_j.value], 'difference': abs(b_i.value - b_j.value)}
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.BASIC_XOR


class BasicOrOperation(ToggleOperation):
    """
    Basic OR toggle operation.
    Axiom: max(b_i, b_j)
    Purpose: Logical disjunction; at least one bit must be 'on'
    """
    
    def apply(self, b_i: OffBit, b_j: OffBit) -> ToggleOperationResult:
        """Apply OR operation to two OffBits."""
        result_value = max(b_i.value, b_j.value)
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = (b_i.layer_coherence + b_j.layer_coherence) / 2
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta
        energy_delta = (result_offbit.active_bits - max(b_i.active_bits, b_j.active_bits)) * 0.1
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={'input_values': [b_i.value, b_j.value]}
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.BASIC_OR


class ResonanceOperation(ToggleOperation):
    """
    Resonance toggle operation.
    Axiom: b_i × exp(-k × (t × f)²)
    Purpose: State transitions with distance-based decay
    """
    
    def __init__(self, k: float = 0.0002):
        """Initialize with decay constant."""
        self.k = k
    
    def apply(self, b_i: OffBit, frequency: float, time: float) -> ToggleOperationResult:
        """Apply resonance operation to an OffBit."""
        d = time * frequency
        resonance_factor = math.exp(-self.k * d * d)
        result_value = int(b_i.value * resonance_factor)
        
        # Ensure result stays within valid range
        result_value = max(0, min(result_value, 0xFFFFFF))
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = b_i.layer_coherence
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta based on resonance
        energy_delta = (result_offbit.active_bits - b_i.active_bits) * resonance_factor
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={
                'frequency': frequency,
                'time': time,
                'resonance_factor': resonance_factor,
                'decay_constant': self.k
            }
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.RESONANCE


class EntanglementOperation(ToggleOperation):
    """
    Entanglement toggle operation.
    Axiom: b_i × b_j × C_ij (where C_ij ≥ 0.95 for strong entanglement)
    Purpose: Cross-layer coupling between OffBits
    """
    
    def __init__(self, coherence_threshold: float = 0.95):
        """Initialize with coherence threshold."""
        self.coherence_threshold = coherence_threshold
    
    def apply(self, b_i: OffBit, b_j: OffBit, coherence: Optional[float] = None) -> ToggleOperationResult:
        """Apply entanglement operation to two OffBits."""
        if coherence is None:
            coherence = b_i.coherence_with(b_j)
        
        # Apply entanglement based on coherence level
        if coherence >= self.coherence_threshold:
            # Strong entanglement
            entanglement_factor = coherence
        else:
            # Weak entanglement - reduced coupling
            entanglement_factor = coherence * 0.1
        
        # Calculate entangled value
        base_value = (b_i.value * b_j.value) // 0xFFFFFF  # Normalize to prevent overflow
        result_value = int(base_value * entanglement_factor)
        result_value = max(0, min(result_value, 0xFFFFFF))
        
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = (b_i.layer_coherence + b_j.layer_coherence) / 2
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta based on entanglement strength
        energy_delta = result_offbit.active_bits * entanglement_factor * 0.1
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={
                'coherence': coherence,
                'entanglement_factor': entanglement_factor,
                'strong_entanglement': coherence >= self.coherence_threshold
            }
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.ENTANGLEMENT


class SuperpositionOperation(ToggleOperation):
    """
    Superposition toggle operation.
    Axiom: Σ(states × weights) where Σ weights = 1
    Purpose: Probabilistic state modeling
    """
    
    def apply(self, states: List[OffBit], weights: List[float]) -> ToggleOperationResult:
        """Apply superposition operation to multiple OffBits."""
        if len(states) != len(weights):
            raise ValueError("States and weights must have same length")
        
        # Normalize weights to sum to 1
        total_weight = sum(weights)
        if total_weight == 0:
            result_offbit = OffBit(0)
            coherence_change = 0.0
            energy_delta = 0.0
        else:
            normalized_weights = [w / total_weight for w in weights]
            
            # Calculate weighted sum
            weighted_sum = 0.0
            for state, weight in zip(states, normalized_weights):
                weighted_sum += state.value * weight
            
            result_value = int(weighted_sum)
            result_value = max(0, min(result_value, 0xFFFFFF))
            result_offbit = OffBit(result_value)
            
            # Calculate coherence change
            initial_coherence = sum(state.layer_coherence for state in states) / len(states)
            final_coherence = result_offbit.layer_coherence
            coherence_change = final_coherence - initial_coherence
            
            # Calculate energy delta
            initial_energy = sum(state.active_bits * weight for state, weight in zip(states, normalized_weights))
            energy_delta = result_offbit.active_bits - initial_energy
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={
                'num_states': len(states),
                'weights': weights,
                'normalized_weights': normalized_weights if total_weight > 0 else []
            }
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.SUPERPOSITION


class HybridXorResonanceOperation(ToggleOperation):
    """
    Hybrid XOR Resonance operation.
    Axiom: |b_i - b_j| × exp(-k × d²)
    Purpose: Combined XOR and resonance effects
    """
    
    def __init__(self, k: float = 0.0002):
        """Initialize with decay constant."""
        self.k = k
    
    def apply(self, b_i: OffBit, b_j: OffBit, frequency: float, time: float) -> ToggleOperationResult:
        """Apply hybrid XOR resonance operation."""
        # XOR component
        xor_value = abs(b_i.value - b_j.value)
        
        # Resonance component
        d = time * frequency
        resonance_factor = math.exp(-self.k * d * d)
        
        # Combine XOR and resonance
        result_value = int(xor_value * resonance_factor)
        result_value = max(0, min(result_value, 0xFFFFFF))
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = (b_i.layer_coherence + b_j.layer_coherence) / 2
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta
        energy_delta = result_offbit.active_bits * resonance_factor * 0.1
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={
                'xor_value': xor_value,
                'resonance_factor': resonance_factor,
                'frequency': frequency,
                'time': time
            }
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.HYBRID_XOR_RESONANCE


class SpinTransitionOperation(ToggleOperation):
    """
    Spin transition operation.
    Axiom: b_i × ln(1 / p_s)
    Purpose: Quantum spin state transitions
    """
    
    def apply(self, b_i: OffBit, p_s: float) -> ToggleOperationResult:
        """Apply spin transition operation."""
        if p_s <= 0 or p_s >= 1:
            raise ValueError("Spin probability p_s must be between 0 and 1")
        
        # Calculate spin transition factor
        spin_factor = math.log(1.0 / p_s)
        
        # Apply spin transition
        result_value = int(b_i.value * spin_factor)
        result_value = max(0, min(result_value, 0xFFFFFF))
        result_offbit = OffBit(result_value)
        
        # Calculate coherence change
        initial_coherence = b_i.layer_coherence
        final_coherence = result_offbit.layer_coherence
        coherence_change = final_coherence - initial_coherence
        
        # Calculate energy delta based on spin information
        spin_entropy = -p_s * math.log(p_s) - (1 - p_s) * math.log(1 - p_s)
        energy_delta = result_offbit.active_bits * spin_entropy
        
        return ToggleOperationResult(
            result_offbit=result_offbit,
            operation_type=self.get_operation_type(),
            coherence_change=coherence_change,
            energy_delta=energy_delta,
            metadata={
                'spin_probability': p_s,
                'spin_factor': spin_factor,
                'spin_entropy': spin_entropy
            }
        )
    
    def get_operation_type(self) -> ToggleOperationType:
        return ToggleOperationType.SPIN_TRANSITION


class ToggleAlgebraEngine:
    """
    Engine for managing and applying toggle operations.
    """
    
    def __init__(self):
        """Initialize the toggle algebra engine."""
        self.operations = {
            ToggleOperationType.BASIC_AND: BasicAndOperation(),
            ToggleOperationType.BASIC_XOR: BasicXorOperation(),
            ToggleOperationType.BASIC_OR: BasicOrOperation(),
            ToggleOperationType.RESONANCE: ResonanceOperation(),
            ToggleOperationType.ENTANGLEMENT: EntanglementOperation(),
            ToggleOperationType.SUPERPOSITION: SuperpositionOperation(),
            ToggleOperationType.HYBRID_XOR_RESONANCE: HybridXorResonanceOperation(),
            ToggleOperationType.SPIN_TRANSITION: SpinTransitionOperation(),
        }
        
        # Statistics
        self.operation_count = {op_type: 0 for op_type in ToggleOperationType}
        self.total_coherence_change = 0.0
        self.total_energy_change = 0.0
    
    def apply_operation(self, operation_type: ToggleOperationType, *args, **kwargs) -> ToggleOperationResult:
        """
        Apply a toggle operation.
        
        Args:
            operation_type: Type of operation to apply
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
        
        Returns:
            Result of the toggle operation
        """
        if operation_type not in self.operations:
            raise ValueError(f"Unknown operation type: {operation_type}")
        
        operation = self.operations[operation_type]
        result = operation.apply(*args, **kwargs)
        
        # Update statistics
        self.operation_count[operation_type] += 1
        self.total_coherence_change += result.coherence_change
        self.total_energy_change += result.energy_delta
        
        return result
    
    def register_operation(self, operation: ToggleOperation) -> None:
        """Register a custom toggle operation."""
        self.operations[operation.get_operation_type()] = operation
    
    def get_statistics(self) -> dict:
        """Get engine statistics."""
        total_operations = sum(self.operation_count.values())
        return {
            'total_operations': total_operations,
            'operation_counts': dict(self.operation_count),
            'total_coherence_change': self.total_coherence_change,
            'total_energy_change': self.total_energy_change,
            'average_coherence_change': self.total_coherence_change / max(1, total_operations),
            'average_energy_change': self.total_energy_change / max(1, total_operations)
        }
    
    def reset_statistics(self) -> None:
        """Reset engine statistics."""
        self.operation_count = {op_type: 0 for op_type in ToggleOperationType}
        self.total_coherence_change = 0.0
        self.total_energy_change = 0.0


# Convenience functions for common operations
def toggle_and(b_i: OffBit, b_j: OffBit) -> OffBit:
    """Convenience function for AND operation."""
    engine = ToggleAlgebraEngine()
    result = engine.apply_operation(ToggleOperationType.BASIC_AND, b_i, b_j)
    return result.result_offbit


def toggle_xor(b_i: OffBit, b_j: OffBit) -> OffBit:
    """Convenience function for XOR operation."""
    engine = ToggleAlgebraEngine()
    result = engine.apply_operation(ToggleOperationType.BASIC_XOR, b_i, b_j)
    return result.result_offbit


def toggle_or(b_i: OffBit, b_j: OffBit) -> OffBit:
    """Convenience function for OR operation."""
    engine = ToggleAlgebraEngine()
    result = engine.apply_operation(ToggleOperationType.BASIC_OR, b_i, b_j)
    return result.result_offbit


def resonance_toggle(b_i: OffBit, frequency: float, time: float, k: float = 0.0002) -> OffBit:
    """Convenience function for resonance operation."""
    engine = ToggleAlgebraEngine()
    operation = ResonanceOperation(k)
    engine.register_operation(operation)
    result = engine.apply_operation(ToggleOperationType.RESONANCE, b_i, frequency, time)
    return result.result_offbit


def entanglement_toggle(b_i: OffBit, b_j: OffBit, coherence: Optional[float] = None) -> OffBit:
    """Convenience function for entanglement operation."""
    engine = ToggleAlgebraEngine()
    result = engine.apply_operation(ToggleOperationType.ENTANGLEMENT, b_i, b_j, coherence)
    return result.result_offbit


if __name__ == "__main__":
    # Test the toggle algebra implementation
    print("Testing Toggle Algebra implementation...")
    
    # Create test OffBits
    from .offbit import create_quantum_offbit, create_electromagnetic_offbit
    
    offbit1 = create_quantum_offbit(100, 150, 200)
    offbit2 = create_electromagnetic_offbit(80, 120, 160)
    
    print(f"OffBit 1: {offbit1}")
    print(f"OffBit 2: {offbit2}")
    
    # Create engine
    engine = ToggleAlgebraEngine()
    
    # Test basic operations
    and_result = engine.apply_operation(ToggleOperationType.BASIC_AND, offbit1, offbit2)
    print(f"\nAND result: {and_result.result_offbit}")
    print(f"Coherence change: {and_result.coherence_change:.4f}")
    
    xor_result = engine.apply_operation(ToggleOperationType.BASIC_XOR, offbit1, offbit2)
    print(f"\nXOR result: {xor_result.result_offbit}")
    print(f"Energy delta: {xor_result.energy_delta:.4f}")
    
    # Test resonance operation
    resonance_result = engine.apply_operation(ToggleOperationType.RESONANCE, offbit1, 1000.0, 0.001)
    print(f"\nResonance result: {resonance_result.result_offbit}")
    print(f"Metadata: {resonance_result.metadata}")
    
    # Test entanglement operation
    entanglement_result = engine.apply_operation(ToggleOperationType.ENTANGLEMENT, offbit1, offbit2)
    print(f"\nEntanglement result: {entanglement_result.result_offbit}")
    print(f"Strong entanglement: {entanglement_result.metadata['strong_entanglement']}")
    
    # Test superposition operation
    states = [offbit1, offbit2, OffBit(0x123456)]
    weights = [0.5, 0.3, 0.2]
    superposition_result = engine.apply_operation(ToggleOperationType.SUPERPOSITION, states, weights)
    print(f"\nSuperposition result: {superposition_result.result_offbit}")
    
    # Test spin transition
    spin_result = engine.apply_operation(ToggleOperationType.SPIN_TRANSITION, offbit1, 0.2265234857)
    print(f"\nSpin transition result: {spin_result.result_offbit}")
    print(f"Spin entropy: {spin_result.metadata['spin_entropy']:.4f}")
    
    # Show statistics
    stats = engine.get_statistics()
    print(f"\nEngine statistics:")
    print(f"Total operations: {stats['total_operations']}")
    print(f"Average coherence change: {stats['average_coherence_change']:.4f}")
    print(f"Average energy change: {stats['average_energy_change']:.4f}")
    
    print("\nToggle Algebra implementation test completed successfully!")

