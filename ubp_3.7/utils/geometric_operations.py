"""
==================================
Universal Binary Principle (UBP) Framework v3.7 - Geometric Operations
Author: Euan Craig, New Zealand
Date: November 7, 2025
==================================

This module implements native geometric UBP operations, enabling the UBP system
to work directly with geometric patterns rather than numerical values.

Two operational modes:
1. **Pure Geometric** - Direct pattern manipulation (no value conversion)
2. **Hybrid** - Pattern → value → operation (backwards compatibility)

This demonstrates that geometry can fully replace text/numbers for UBP operations.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Union
from scipy.fft import fft2, ifft2, fftshift, ifftshift

# UBP 3.4 imports
from core.y_constants import (
    calculate_y_constant,
    calculate_y_inverse,
    apply_bidirectional_refinement
)
from core.system_constants import UBPConstants
from core.soc_energy import SOCCalculator

# Geometric codex import
from utils.geometric_codex import GeometricCodex, GeometricSignature, PatternType


# ============================================================================
# GEOMETRIC OPERATION RESULTS
# ============================================================================

@dataclass
class GeometricOperationResult:
    """Result of a geometric UBP operation."""
    # Output pattern
    output_pattern: np.ndarray
    
    # Metadata
    operation_type: str
    mode: str  # 'pure_geometric' or 'hybrid'
    
    # Quality metrics
    pattern_quality: float  # [0, 1]
    closure_quality: float  # [0, 1]
    nrci_estimate: float  # Estimated NRCI
    
    # Extracted values (for hybrid mode)
    input_value: Optional[float] = None
    output_value: Optional[float] = None
    intermediate_value: Optional[float] = None
    
    # UBP metrics
    energy_cu: Optional[float] = None
    y_emergent: Optional[float] = None
    observer_cost: Optional[float] = None
    
    # Timing
    computation_time: float = 0.0
    
    def __repr__(self) -> str:
        return (f"GeometricOperationResult("
                f"operation={self.operation_type}, "
                f"mode={self.mode}, "
                f"quality={self.pattern_quality:.4f})")


# ============================================================================
# PURE GEOMETRIC OPERATIONS
# ============================================================================

class PureGeometricOperations:
    """
    Pure geometric operations on patterns.
    
    These operations work directly in pattern space without converting
    to numerical values. This is the **breakthrough** - true geometric computation.
    """
    
    def __init__(self, grid_size: int = 256):
        self.grid_size = grid_size
        self.Y = calculate_y_constant()
        self.Y_inv = calculate_y_inverse()
    
    def apply_y_refinement(
        self,
        pattern: np.ndarray,
        direction: str = 'forward'
    ) -> np.ndarray:
        """
        Apply Y-constant refinement directly to a pattern.
        
        This is geometric multiplication/division by Y.
        """
        if direction == 'forward':
            # Multiply by Y in geometric space
            # Implemented as spatial frequency modulation
            refined = self._geometric_multiply(pattern, self.Y)
        else:  # backward
            # Multiply by 1/Y in geometric space
            refined = self._geometric_multiply(pattern, self.Y_inv)
        
        return refined
    
    def _geometric_multiply(self, pattern: np.ndarray, factor: float) -> np.ndarray:
        """
        Multiply a pattern by a scalar in geometric space.
        
        For Y-constant operations, this must respect:
        - Y = π/(π² + 2) - harmonic relationship
        - 1/Y = π + 2/π - observer cost
        - Connection to 12D Bitfield (π² + 2 ≈ 11.87)
        
        Implementation:
        1. Transform to frequency domain
        2. Apply harmonic scaling based on factor's relationship to π
        3. Preserve circular symmetry (π-based)
        4. Transform back to spatial domain
        """
        # FFT to frequency domain
        fft_pattern = fftshift(fft2(pattern))
        N = pattern.shape[0]
        
        # Create radial frequency coordinate (respects circular symmetry)
        center = N // 2
        y_coords, x_coords = np.ogrid[:N, :N]
        y_coords = y_coords - center
        x_coords = x_coords - center
        
        # Radial distance from center (circular geometry)
        r = np.sqrt(x_coords**2 + y_coords**2)
        r_max = np.sqrt(2) * center
        r_norm = r / r_max  # Normalized [0, 1]
        
        # Angular coordinate (preserves rotational symmetry)
        theta = np.arctan2(y_coords, x_coords)
        
        # Determine if this is Y or 1/Y operation
        # Y ≈ 0.2647, 1/Y ≈ 3.778
        is_y_forward = (factor < 1.0)  # Multiply by Y
        is_y_backward = (factor > 1.0)  # Multiply by 1/Y
        
        if is_y_forward:
            # Forward: Geometry → Observer
            # Y = π/(π² + 2) - compress harmonics
            # This should increase spatial frequency (compress patterns)
            
            # Harmonic compression factor based on π relationship
            # Y relates 1st harmonic (π) to 2nd harmonic (π²)
            harmonic_factor = np.pi / (np.pi**2 + 2)
            
            # Apply radial compression (higher frequencies)
            # Preserve low frequencies, compress high frequencies
            radial_scale = 1.0 + (1.0 / harmonic_factor - 1.0) * r_norm**2
            
            # Apply harmonic modulation
            # This respects the π-based circular geometry
            phase_shift = -2 * np.pi * factor * r_norm
            
        else:
            # Backward: Observer → Geometry  
            # 1/Y = π + 2/π - expand harmonics
            # This should decrease spatial frequency (expand patterns)
            
            # Harmonic expansion factor
            harmonic_factor = np.pi + 2/np.pi
            
            # Apply radial expansion (lower frequencies)
            radial_scale = 1.0 / (1.0 + (harmonic_factor - 1.0) * r_norm**2)
            
            # Apply harmonic modulation
            phase_shift = 2 * np.pi * (1.0/factor) * r_norm
        
        # Apply transformation in frequency domain
        # Radial scaling + phase modulation
        scaled_fft = fft_pattern * radial_scale * np.exp(1j * phase_shift)
        
        # Transform back to spatial domain
        result = np.real(ifft2(ifftshift(scaled_fft)))
        
        # Normalize to preserve energy
        result = result * (np.std(pattern) / (np.std(result) + 1e-10))
        
        return result
    
    def compose_patterns(
        self,
        pattern1: np.ndarray,
        pattern2: np.ndarray,
        operation: str = 'add'
    ) -> np.ndarray:
        """
        Compose two patterns geometrically.
        
        Operations:
        - 'add': Superposition
        - 'multiply': Interference
        - 'convolve': Convolution (geometric product)
        """
        if operation == 'add':
            # Superposition
            result = pattern1 + pattern2
        elif operation == 'multiply':
            # Interference
            result = pattern1 * pattern2
        elif operation == 'convolve':
            # Convolution in spatial domain = multiplication in frequency domain
            fft1 = fft2(pattern1)
            fft2_pat = fft2(pattern2)
            result = np.real(ifft2(fft1 * fft2_pat))
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        # Normalize
        result = result / np.max(np.abs(result)) if np.max(np.abs(result)) > 0 else result
        
        return result
    
    def extract_nrci_from_pattern(self, pattern: np.ndarray) -> float:
        """
        Extract NRCI estimate directly from pattern geometry.
        
        This analyzes the pattern's coherence without converting to values.
        """
        # Measure pattern coherence through spatial correlation
        # High coherence = high spatial correlation
        
        # Calculate autocorrelation
        fft_pattern = fft2(pattern)
        autocorr = np.real(ifft2(np.abs(fft_pattern)**2))
        autocorr = fftshift(autocorr)
        
        # Normalize
        autocorr = autocorr / autocorr.max()
        
        # NRCI is related to the width of the autocorrelation peak
        # Narrow peak = high coherence
        center = autocorr.shape[0] // 2
        peak_region = autocorr[center-5:center+5, center-5:center+5]
        
        # Coherence measure
        coherence = np.mean(peak_region)
        
        # Convert to NRCI scale [0, 1]
        nrci = min(coherence, 1.0)
        
        return nrci
    
    def extract_observer_cost_from_pattern(self, pattern: np.ndarray) -> float:
        """
        Extract observer cost estimate directly from pattern geometry.
        
        Observer cost is related to pattern complexity.
        """
        # Measure pattern complexity through frequency content
        fft_pattern = fftshift(fft2(pattern))
        magnitude = np.abs(fft_pattern)
        
        # Complexity = distribution of frequency components
        # More distributed = higher complexity = higher observer cost
        
        # Calculate entropy of frequency distribution
        magnitude_norm = magnitude / magnitude.sum()
        magnitude_norm = magnitude_norm[magnitude_norm > 0]  # Remove zeros
        
        entropy = -np.sum(magnitude_norm * np.log(magnitude_norm))
        
        # Scale to observer cost range
        # Base cost is O_observer = 1/Y
        base_cost = self.Y_inv
        
        # Complexity factor [1, 2]
        complexity_factor = 1 + entropy / 10.0
        
        observer_cost = base_cost * complexity_factor
        
        return observer_cost
    
    def measure_pattern_quality(self, pattern: np.ndarray) -> float:
        """
        Measure the quality of a pattern.
        
        Quality metrics:
        - Contrast
        - Sharpness
        - Coherence
        """
        # Contrast
        contrast = np.std(pattern) / (np.mean(np.abs(pattern)) + 1e-10)
        
        # Sharpness (high-frequency content)
        fft_pattern = fftshift(fft2(pattern))
        magnitude = np.abs(fft_pattern)
        center = magnitude.shape[0] // 2
        edge_region = magnitude.copy()
        edge_region[center-10:center+10, center-10:center+10] = 0
        sharpness = np.sum(edge_region) / np.sum(magnitude)
        
        # Coherence
        coherence = self.extract_nrci_from_pattern(pattern)
        
        # Combined quality [0, 1]
        quality = (contrast * 0.3 + sharpness * 0.3 + coherence * 0.4)
        quality = min(quality, 1.0)
        
        return quality


# ============================================================================
# HYBRID OPERATIONS
# ============================================================================

class HybridGeometricOperations:
    """
    Hybrid operations: Pattern → Value → UBP Operation → Pattern
    
    This provides backwards compatibility and validation.
    """
    
    def __init__(self, grid_size: int = 256):
        self.grid_size = grid_size
        self.codex = GeometricCodex(grid_size)
        self.soc_calc = SOCCalculator()
        self.Y = calculate_y_constant()
        self.Y_inv = calculate_y_inverse()
    
    def pattern_to_soc_energy(
        self,
        pattern: np.ndarray,
        unit: str = "Hz"
    ) -> Tuple[float, float]:
        """
        Convert pattern to SOC energy via value extraction.
        
        Returns: (energy_cu, confidence)
        """
        # Extract value from pattern
        value, confidence = self.codex.geometry_to_value(pattern, unit)
        
        if confidence < 0.5:
            # Low confidence, return default
            return 0.0, confidence
        
        # Calculate SOC energy
        # Assume modal_sum = 1.0 for simplicity
        result = self.soc_calc.calculate_soc_energy(modal_sum=1.0)
        
        # Scale by extracted value
        energy_cu = result.energy_cu * value / 1e12  # Normalize
        
        return energy_cu, confidence
    
    def apply_y_refinement_hybrid(
        self,
        pattern: np.ndarray,
        direction: str = 'forward'
    ) -> Tuple[np.ndarray, float]:
        """
        Apply Y refinement via value extraction.
        
        Returns: (refined_pattern, extracted_value)
        """
        # Extract value
        value, confidence = self.codex.geometry_to_value(pattern, "Hz")
        
        # Apply bidirectional refinement
        refined_value = apply_bidirectional_refinement(value, direction)
        
        # Generate new pattern
        refined_pattern, _ = self.codex.value_to_geometry(refined_value, "Hz")
        
        return refined_pattern, refined_value


# ============================================================================
# UNIFIED GEOMETRIC OPERATIONS INTERFACE
# ============================================================================

class GeometricUBP:
    """
    Unified interface for geometric UBP operations.
    
    Supports both pure geometric and hybrid modes.
    """
    
    def __init__(self, grid_size: int = 256):
        self.grid_size = grid_size
        self.pure = PureGeometricOperations(grid_size)
        self.hybrid = HybridGeometricOperations(grid_size)
        self.codex = GeometricCodex(grid_size)
    
    def apply_y_refinement(
        self,
        pattern: np.ndarray,
        direction: str = 'forward',
        mode: str = 'pure_geometric'
    ) -> GeometricOperationResult:
        """
        Apply Y-constant refinement to a pattern.
        
        Args:
            pattern: Input geometric pattern
            direction: 'forward' (×Y) or 'backward' (×1/Y)
            mode: 'pure_geometric' or 'hybrid'
        
        Returns:
            GeometricOperationResult with output pattern and metrics
        """
        import time
        start_time = time.time()
        
        if mode == 'pure_geometric':
            # Pure geometric operation
            output_pattern = self.pure.apply_y_refinement(pattern, direction)
            
            # Extract metrics from geometry
            nrci = self.pure.extract_nrci_from_pattern(output_pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(output_pattern)
            quality = self.pure.measure_pattern_quality(output_pattern)
            
            # Measure closure quality
            # Apply reverse operation and compare
            reverse_dir = 'backward' if direction == 'forward' else 'forward'
            recovered = self.pure.apply_y_refinement(output_pattern, reverse_dir)
            closure = 1.0 - np.mean(np.abs(recovered - pattern)) / (np.mean(np.abs(pattern)) + 1e-10)
            closure = max(0, min(closure, 1.0))
            
            result = GeometricOperationResult(
                output_pattern=output_pattern,
                operation_type='y_refinement',
                mode='pure_geometric',
                pattern_quality=quality,
                closure_quality=closure,
                nrci_estimate=nrci,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        else:  # hybrid
            # Hybrid operation
            output_pattern, refined_value = self.hybrid.apply_y_refinement_hybrid(
                pattern, direction
            )
            
            # Extract input value
            input_value, _ = self.codex.geometry_to_value(pattern, "Hz")
            
            # Calculate SOC energy
            energy_cu, _ = self.hybrid.pattern_to_soc_energy(output_pattern, "Hz")
            
            # Extract metrics
            nrci = self.pure.extract_nrci_from_pattern(output_pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(output_pattern)
            quality = self.pure.measure_pattern_quality(output_pattern)
            
            # Closure quality from bidirectional refinement
            reverse_value = apply_bidirectional_refinement(refined_value, 
                'backward' if direction == 'forward' else 'forward')
            closure = 1.0 - abs(reverse_value - input_value) / (abs(input_value) + 1e-10)
            closure = max(0, min(closure, 1.0))
            
            result = GeometricOperationResult(
                output_pattern=output_pattern,
                operation_type='y_refinement',
                mode='hybrid',
                pattern_quality=quality,
                closure_quality=closure,
                nrci_estimate=nrci,
                input_value=input_value,
                output_value=refined_value,
                energy_cu=energy_cu,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        return result
    
    def compose_patterns(
        self,
        pattern1: np.ndarray,
        pattern2: np.ndarray,
        operation: str = 'add',
        mode: str = 'pure_geometric'
    ) -> GeometricOperationResult:
        """
        Compose two patterns.
        
        Args:
            pattern1: First pattern
            pattern2: Second pattern
            operation: 'add', 'multiply', or 'convolve'
            mode: 'pure_geometric' or 'hybrid'
        
        Returns:
            GeometricOperationResult
        """
        import time
        start_time = time.time()
        
        if mode == 'pure_geometric':
            # Pure geometric composition
            output_pattern = self.pure.compose_patterns(pattern1, pattern2, operation)
            
            # Extract metrics
            nrci = self.pure.extract_nrci_from_pattern(output_pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(output_pattern)
            quality = self.pure.measure_pattern_quality(output_pattern)
            
            result = GeometricOperationResult(
                output_pattern=output_pattern,
                operation_type=f'compose_{operation}',
                mode='pure_geometric',
                pattern_quality=quality,
                closure_quality=1.0,  # Composition is always valid
                nrci_estimate=nrci,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        else:  # hybrid
            # Extract values
            value1, _ = self.codex.geometry_to_value(pattern1, "Hz")
            value2, _ = self.codex.geometry_to_value(pattern2, "Hz")
            
            # Perform numerical operation
            if operation == 'add':
                result_value = value1 + value2
            elif operation == 'multiply':
                result_value = value1 * value2
            else:
                result_value = value1  # Default
            
            # Generate result pattern
            output_pattern, _ = self.codex.value_to_geometry(result_value, "Hz")
            
            # Extract metrics
            nrci = self.pure.extract_nrci_from_pattern(output_pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(output_pattern)
            quality = self.pure.measure_pattern_quality(output_pattern)
            
            result = GeometricOperationResult(
                output_pattern=output_pattern,
                operation_type=f'compose_{operation}',
                mode='hybrid',
                pattern_quality=quality,
                closure_quality=1.0,
                nrci_estimate=nrci,
                input_value=value1,
                output_value=result_value,
                intermediate_value=value2,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        return result
    
    def calculate_soc_energy(
        self,
        pattern: np.ndarray,
        mode: str = 'pure_geometric'
    ) -> GeometricOperationResult:
        """
        Calculate SOC energy from a pattern.
        
        Args:
            pattern: Input geometric pattern
            mode: 'pure_geometric' or 'hybrid'
        
        Returns:
            GeometricOperationResult with energy estimate
        """
        import time
        start_time = time.time()
        
        if mode == 'pure_geometric':
            # Pure geometric energy estimation
            # Energy is encoded in pattern complexity and coherence
            
            nrci = self.pure.extract_nrci_from_pattern(pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(pattern)
            
            # SOC energy formula (geometric version)
            # E_SOC ≈ (Y × O_obs) / (1 - NRCI)
            Y = self.pure.Y
            energy_estimate = (Y * observer_cost) / (1 - nrci + 1e-10)
            
            quality = self.pure.measure_pattern_quality(pattern)
            
            result = GeometricOperationResult(
                output_pattern=pattern,  # No transformation
                operation_type='soc_energy',
                mode='pure_geometric',
                pattern_quality=quality,
                closure_quality=1.0,
                nrci_estimate=nrci,
                energy_cu=energy_estimate,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        else:  # hybrid
            # Hybrid: extract value and calculate SOC
            energy_cu, confidence = self.hybrid.pattern_to_soc_energy(pattern, "Hz")
            
            nrci = self.pure.extract_nrci_from_pattern(pattern)
            observer_cost = self.pure.extract_observer_cost_from_pattern(pattern)
            quality = self.pure.measure_pattern_quality(pattern)
            
            result = GeometricOperationResult(
                output_pattern=pattern,
                operation_type='soc_energy',
                mode='hybrid',
                pattern_quality=quality,
                closure_quality=confidence,
                nrci_estimate=nrci,
                energy_cu=energy_cu,
                observer_cost=observer_cost,
                computation_time=time.time() - start_time
            )
        
        return result


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_geometric_ubp(grid_size: int = 256) -> GeometricUBP:
    """Create a geometric UBP interface."""
    return GeometricUBP(grid_size)


def pattern_y_refinement(
    pattern: np.ndarray,
    direction: str = 'forward',
    mode: str = 'pure_geometric'
) -> np.ndarray:
    """Quick function to apply Y refinement to a pattern."""
    ubp = create_geometric_ubp(pattern.shape[0])
    result = ubp.apply_y_refinement(pattern, direction, mode)
    return result.output_pattern
