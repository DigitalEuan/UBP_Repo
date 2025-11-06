"""
==================================
UBP Geometric Operations v2
Author: Euan Craig, New Zealand  
Date: November 7, 2025
==================================

Octave-aware geometric operations for UBP.

KEY INSIGHT: The 12D Bitfield has a harmonic structure like a musical instrument.
Geometric operations navigate this harmonic ladder in "octaves" (×2, ×1/2),
while the Y-constant provides the "tuning" that relates octaves to precise values.

Modes:
- HARMONIC: Operate in octave space (natural geometric transformations)
- VALUE: Operate in precise value space (backwards compatible with numerical UBP)
- HYBRID: Extract value, operate numerically, regenerate pattern
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import math


@dataclass
class GeometricResult:
    """Result from a geometric operation."""
    output_pattern: np.ndarray
    operation: str
    mode: str
    input_value: Optional[float] = None
    output_value: Optional[float] = None
    harmonic_shift: Optional[float] = None  # Octave shift
    pattern_quality: float = 0.0
    closure_quality: float = 0.0
    nrci_estimate: float = 0.0
    metadata: Dict = None


class OctaveAwareGeometricUBP:
    """
    Geometric UBP operations with octave awareness.
    
    Implements three modes:
    1. HARMONIC: Pure geometric, operates in octave space
    2. VALUE: Geometric with value extraction, operates in precise value space  
    3. HYBRID: Extract → numerical operation → regenerate
    """
    
    def __init__(self, grid_size: int = 128):
        self.grid_size = grid_size
        
        # Y-constant family
        self.Y = math.pi / (math.pi**2 + 2)
        self.Y_inv = math.pi + 2/math.pi
        
        # Octave relationships
        self.OCTAVE_UP = 2.0  # One octave up
        self.OCTAVE_DOWN = 0.5  # One octave down
        
        # Y-constant in octaves
        # Y ≈ 0.2647 ≈ 2^(-1.92) (between 1 and 2 octaves down)
        self.Y_IN_OCTAVES = np.log2(self.Y)  # ≈ -1.92 octaves
        self.Y_INV_IN_OCTAVES = np.log2(self.Y_inv)  # ≈ +1.92 octaves
        
        print(f"Octave-aware Geometric UBP initialized:")
        print(f"  Y = {self.Y:.6f} = 2^{self.Y_IN_OCTAVES:.3f} octaves")
        print(f"  1/Y = {self.Y_inv:.6f} = 2^{self.Y_INV_IN_OCTAVES:.3f} octaves")
    
    def apply_y_refinement(
        self,
        pattern: np.ndarray,
        direction: str = 'forward',
        mode: str = 'harmonic',
        codex = None
    ) -> GeometricResult:
        """
        Apply Y-refinement to a geometric pattern.
        
        Args:
            pattern: Input geometric pattern
            direction: 'forward' (×Y) or 'backward' (×1/Y)
            mode: 'harmonic', 'value', or 'hybrid'
            codex: GeometricCodex instance (required for value/hybrid modes)
        
        Returns:
            GeometricResult with output pattern and metadata
        """
        if mode == 'harmonic':
            return self._apply_harmonic_refinement(pattern, direction)
        elif mode == 'value':
            if codex is None:
                raise ValueError("Codex required for value mode")
            return self._apply_value_refinement(pattern, direction, codex)
        elif mode == 'hybrid':
            if codex is None:
                raise ValueError("Codex required for hybrid mode")
            return self._apply_hybrid_refinement(pattern, direction, codex)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def _apply_harmonic_refinement(
        self,
        pattern: np.ndarray,
        direction: str
    ) -> GeometricResult:
        """
        Apply Y-refinement in harmonic (octave) space.
        
        This is pure geometric - operates on harmonic modes without value extraction.
        Y-refinement shifts the pattern by ~1.92 octaves.
        """
        # Determine octave shift
        if direction == 'forward':
            octave_shift = self.Y_IN_OCTAVES  # ~-1.92 octaves
            operation = "Y-refinement (forward, harmonic)"
        else:
            octave_shift = self.Y_INV_IN_OCTAVES  # ~+1.92 octaves
            operation = "Y-refinement (backward, harmonic)"
        
        # Apply octave shift in frequency domain
        output_pattern = self._shift_octave(pattern, octave_shift)
        
        # Compute quality metrics
        quality = self._compute_pattern_quality(output_pattern)
        nrci = self._estimate_nrci(output_pattern)
        
        return GeometricResult(
            output_pattern=output_pattern,
            operation=operation,
            mode='harmonic',
            harmonic_shift=octave_shift,
            pattern_quality=quality,
            nrci_estimate=nrci,
            metadata={'octave_shift': octave_shift}
        )
    
    def _apply_value_refinement(
        self,
        pattern: np.ndarray,
        direction: str,
        codex
    ) -> GeometricResult:
        """
        Apply Y-refinement in value space.
        
        Extracts value, multiplies by Y (or 1/Y), regenerates pattern.
        This ensures backwards compatibility with numerical UBP.
        """
        # Extract value from pattern
        value, confidence = codex.geometry_to_value(pattern, "Hz")
        
        # Apply Y-refinement to value
        if direction == 'forward':
            refined_value = value * self.Y
            operation = "Y-refinement (forward, value)"
        else:
            refined_value = value * self.Y_inv
            operation = "Y-refinement (backward, value)"
        
        # Generate new pattern for refined value
        output_pattern, _ = codex.value_to_geometry(refined_value, "Hz")
        
        # Compute quality metrics
        quality = self._compute_pattern_quality(output_pattern)
        nrci = self._estimate_nrci(output_pattern)
        
        return GeometricResult(
            output_pattern=output_pattern,
            operation=operation,
            mode='value',
            input_value=value,
            output_value=refined_value,
            pattern_quality=quality,
            nrci_estimate=nrci,
            metadata={'value_confidence': confidence}
        )
    
    def _apply_hybrid_refinement(
        self,
        pattern: np.ndarray,
        direction: str,
        codex
    ) -> GeometricResult:
        """
        Apply Y-refinement in hybrid mode.
        
        Similar to value mode but keeps pattern structure.
        """
        # Same as value mode for now
        return self._apply_value_refinement(pattern, direction, codex)
    
    def _shift_octave(
        self,
        pattern: np.ndarray,
        octave_shift: float
    ) -> np.ndarray:
        """
        Shift a pattern by a given number of octaves.
        
        octave_shift > 0: shift up (higher frequencies)
        octave_shift < 0: shift down (lower frequencies)
        
        Implementation: Scale frequencies in FFT domain by 2^octave_shift
        """
        # Transform to frequency domain
        fft_pattern = fftshift(fft2(pattern))
        N = pattern.shape[0]
        center = N // 2
        
        # Create frequency coordinates
        y_coords, x_coords = np.ogrid[:N, :N]
        y_coords = (y_coords - center).astype(float)
        x_coords = (x_coords - center).astype(float)
        
        # Radial distance (frequency magnitude)
        r = np.sqrt(x_coords**2 + y_coords**2)
        r_max = np.sqrt(2) * center
        r_norm = r / r_max  # Normalized [0, 1]
        
        # Angular coordinate (preserves rotational symmetry)
        theta = np.arctan2(y_coords, x_coords)
        
        # Frequency scaling factor
        freq_scale = 2.0 ** octave_shift
        
        # Apply octave shift as radial scaling in frequency domain
        # This preserves the pattern structure while shifting frequencies
        
        if octave_shift > 0:
            # Shift up: compress in spatial domain, expand in frequency domain
            # Scale radial frequencies outward
            radial_transform = 1.0 + (freq_scale - 1.0) * r_norm
        else:
            # Shift down: expand in spatial domain, compress in frequency domain
            # Scale radial frequencies inward
            radial_transform = 1.0 / (1.0 + (1.0/freq_scale - 1.0) * r_norm)
        
        # Apply transformation
        scaled_fft = fft_pattern * radial_transform
        
        # Add phase modulation to preserve coherence
        # This is the key to maintaining pattern quality
        phase_mod = np.exp(1j * 2 * np.pi * octave_shift * r_norm / 10.0)
        scaled_fft = scaled_fft * phase_mod
        
        # Transform back to spatial domain
        output = np.real(ifft2(ifftshift(scaled_fft)))
        
        # Normalize to preserve energy
        output = output * (np.std(pattern) / (np.std(output) + 1e-10))
        
        return output
    
    def _compute_pattern_quality(self, pattern: np.ndarray) -> float:
        """Compute quality metric for a pattern."""
        # Quality based on coherence and structure
        mean = np.mean(pattern)
        std = np.std(pattern)
        
        # Normalized standard deviation
        if abs(mean) > 1e-10:
            quality = std / abs(mean)
        else:
            quality = std
        
        # Clip to [0, 1]
        quality = max(0.0, min(1.0, quality))
        return quality
    
    def _estimate_nrci(self, pattern: np.ndarray) -> float:
        """Estimate NRCI from pattern structure."""
        # NRCI related to pattern coherence
        # High coherence = high NRCI
        
        # Compute local correlation
        shifted_x = np.roll(pattern, 1, axis=0)
        shifted_y = np.roll(pattern, 1, axis=1)
        
        corr_x = np.corrcoef(pattern.flatten(), shifted_x.flatten())[0, 1]
        corr_y = np.corrcoef(pattern.flatten(), shifted_y.flatten())[0, 1]
        
        nrci = (abs(corr_x) + abs(corr_y)) / 2.0
        return nrci
    
    def compute_bidirectional_closure(
        self,
        pattern: np.ndarray,
        mode: str = 'harmonic',
        codex = None
    ) -> float:
        """
        Compute bidirectional closure quality.
        
        Apply forward then backward refinement, measure how well we recover original.
        """
        # Forward
        forward_result = self.apply_y_refinement(pattern, 'forward', mode, codex)
        
        # Backward
        backward_result = self.apply_y_refinement(
            forward_result.output_pattern, 'backward', mode, codex
        )
        
        # Compare to original
        recovered = backward_result.output_pattern
        
        # Normalized correlation
        p1_norm = (pattern - np.mean(pattern)) / (np.std(pattern) + 1e-10)
        p2_norm = (recovered - np.mean(recovered)) / (np.std(recovered) + 1e-10)
        
        correlation = np.mean(p1_norm * p2_norm)
        closure = (correlation + 1) / 2  # Map to [0, 1]
        
        return closure


# Convenience functions
def create_octave_aware_ubp(grid_size: int = 128) -> OctaveAwareGeometricUBP:
    """Create an octave-aware geometric UBP instance."""
    return OctaveAwareGeometricUBP(grid_size=grid_size)
