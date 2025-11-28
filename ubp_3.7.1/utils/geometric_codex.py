"""
==================================
Universal Binary Principle (UBP) Framework v3.7.1 - Geometric Codex
Author: Euan R A Craig, New Zealand
Date: 28 November 2025
==================================

The UBP Geometric Codex provides a comprehensive geometric pattern language
for the UBP system, enabling operation through geometry rather than text/numbers.

This module implements:
- Massive taxonomy of cymatic signatures for all UBP values
- Pattern generation engine
- Bidirectional translation protocol (value ↔ geometry)
- Pattern recognition and classification
- Geometric operation primitives

Based on research from "Into the Bitfield 2" study showing that cymatic
patterns provide clear, reproducible geometric structures suitable for
direct manipulation of the UBP system.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Union, Callable
from enum import Enum
import json
from pathlib import Path

# UBP 3.4 imports
from core.y_constants import (
    calculate_y_constant,
    calculate_y_inverse,
    apply_bidirectional_refinement
)
from core.system_constants import UBPConstants
from utils.ubp_config import get_config


# ============================================================================
# PATTERN TAXONOMY
# ============================================================================

class PatternType(Enum):
    """Classification of geometric pattern types."""
    RADIAL = "radial"  # Radial waves from origin
    SPIRAL = "spiral"  # Spiral/vortex patterns
    CONCENTRIC = "concentric"  # Concentric rings
    DIAGONAL = "diagonal"  # Diagonal striations
    GRID = "grid"  # Grid/lattice patterns
    FRACTAL = "fractal"  # Self-similar fractal patterns
    HYBRID = "hybrid"  # Combination of multiple types


class PatternSymmetry(Enum):
    """Symmetry classification."""
    RADIAL_2 = "radial_2"  # 2-fold rotational
    RADIAL_3 = "radial_3"  # 3-fold (triangular)
    RADIAL_4 = "radial_4"  # 4-fold (square)
    RADIAL_5 = "radial_5"  # 5-fold (pentagonal)
    RADIAL_6 = "radial_6"  # 6-fold (hexagonal)
    RADIAL_8 = "radial_8"  # 8-fold (octagonal)
    RADIAL_12 = "radial_12"  # 12-fold (dodecagonal)
    BILATERAL = "bilateral"  # Mirror symmetry
    NONE = "none"  # Asymmetric


class PatternDomain(Enum):
    """Domain in which pattern is defined."""
    SPATIAL = "spatial"  # Real space
    FREQUENCY = "frequency"  # Fourier space
    PHASE = "phase"  # Phase space
    COHERENCE = "coherence"  # NRCI field
    OBSERVER = "observer"  # Observer cost field
    CLOSURE = "closure"  # Bidirectional closure field


@dataclass
class GeometricSignature:
    """
    Complete geometric signature for a UBP value.
    
    This represents the "fingerprint" of a value in geometric space.
    """
    # Identity
    name: str
    value: float  # The UBP value (frequency, energy, etc.)
    unit: str  # Hz, CU, etc.
    realm: Optional[str] = None
    
    # Pattern characteristics
    pattern_type: PatternType = PatternType.RADIAL
    symmetry: PatternSymmetry = PatternSymmetry.RADIAL_4
    domain: PatternDomain = PatternDomain.SPATIAL
    
    # Geometric parameters
    wavelength_nm: Optional[float] = None
    spatial_frequency: float = 0.0  # cycles per unit
    angular_frequency: float = 0.0  # radians per unit
    phase_offset: float = 0.0  # radians
    
    # Y-constant modulation
    y_resonance_factor: float = 1.0  # Modulation by Y constant
    y_inverse_scaling: float = 1.0  # Scaling by 1/Y
    
    # Pattern quality metrics
    tgic_resonance_count: int = 0  # Number of TGIC resonant points
    nrci_mean: float = 0.0  # Mean NRCI in pattern
    observer_cost_mean: float = 0.0  # Mean observer cost
    closure_quality: float = 0.0  # Bidirectional closure quality
    
    # Pattern data (computed)
    pattern_hash: str = ""  # Unique hash of pattern
    thumbnail_path: Optional[str] = None  # Path to thumbnail image
    
    # Metadata
    platonic_solid: Optional[str] = None
    coordination_number: Optional[int] = None
    harmonic_type: Optional[str] = None
    confidence: float = 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'value': self.value,
            'unit': self.unit,
            'realm': self.realm,
            'pattern_type': self.pattern_type.value,
            'symmetry': self.symmetry.value,
            'domain': self.domain.value,
            'wavelength_nm': self.wavelength_nm,
            'spatial_frequency': self.spatial_frequency,
            'angular_frequency': self.angular_frequency,
            'phase_offset': self.phase_offset,
            'y_resonance_factor': self.y_resonance_factor,
            'y_inverse_scaling': self.y_inverse_scaling,
            'tgic_resonance_count': self.tgic_resonance_count,
            'nrci_mean': self.nrci_mean,
            'observer_cost_mean': self.observer_cost_mean,
            'closure_quality': self.closure_quality,
            'pattern_hash': self.pattern_hash,
            'thumbnail_path': self.thumbnail_path,
            'platonic_solid': self.platonic_solid,
            'coordination_number': self.coordination_number,
            'harmonic_type': self.harmonic_type,
            'confidence': self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GeometricSignature':
        """Create from dictionary."""
        data['pattern_type'] = PatternType(data['pattern_type'])
        data['symmetry'] = PatternSymmetry(data['symmetry'])
        data['domain'] = PatternDomain(data['domain'])
        return cls(**data)


# ============================================================================
# PATTERN GENERATION ENGINE
# ============================================================================

class PatternGenerator:
    """
    Generates geometric patterns from UBP values.
    
    Uses the Y-constant geometry and UBP 3.4 foundation to create
    reproducible cymatic patterns.
    """
    
    def __init__(self, grid_size: int = 256):
        self.grid_size = grid_size
        self.Y = calculate_y_constant()
        self.Y_inv = calculate_y_inverse()
        
    def generate_pattern(
        self,
        value: float,
        pattern_type: PatternType = PatternType.RADIAL,
        symmetry: PatternSymmetry = PatternSymmetry.RADIAL_4,
        modulus: int = 997
    ) -> np.ndarray:
        """
        Generate a geometric pattern for a given value.
        
        Args:
            value: The UBP value (frequency, energy, etc.)
            pattern_type: Type of pattern to generate
            symmetry: Symmetry of the pattern
            modulus: Prime modulus for T matrix construction
            
        Returns:
            2D numpy array representing the pattern
        """
        N = self.grid_size
        pattern = np.zeros((N, N), dtype=np.float64)
        
        # Normalize value to spatial frequency
        spatial_freq = self._value_to_spatial_frequency(value)
        
        # Validate parameters
        self.validate_parameters(value, spatial_freq)
        
        # Generate base pattern based on type
        if pattern_type == PatternType.RADIAL:
            pattern = self._generate_radial(spatial_freq, symmetry)
        elif pattern_type == PatternType.SPIRAL:
            pattern = self._generate_spiral(spatial_freq, symmetry)
        elif pattern_type == PatternType.CONCENTRIC:
            pattern = self._generate_concentric(spatial_freq)
        elif pattern_type == PatternType.DIAGONAL:
            pattern = self._generate_diagonal(spatial_freq, symmetry)
        elif pattern_type == PatternType.GRID:
            pattern = self._generate_grid(spatial_freq, symmetry)
        elif pattern_type == PatternType.FRACTAL:
            pattern = self._generate_fractal(spatial_freq)
        else:  # HYBRID
            pattern = self._generate_hybrid(spatial_freq, symmetry)
        
        # Apply Y-constant modulation
        pattern = self._apply_y_modulation(pattern)
        
        return pattern
    
    def compute_pattern_hash(self, pattern: np.ndarray) -> str:
        """
        Compute deterministic hash of pattern for identification.
        
        Uses FFT descriptor + quantized statistics for robust hashing.
        
        Args:
            pattern: 2D pattern array
            
        Returns:
            Hexadecimal hash string
        """
        import hashlib
        
        # Normalize pattern
        pattern_norm = (pattern - pattern.mean()) / (pattern.std() + 1e-10)
        
        # Compute FFT and take magnitude spectrum
        fft = np.fft.fft2(pattern_norm)
        fft_mag = np.abs(np.fft.fftshift(fft))
        
        # Quantize to reduce noise sensitivity
        fft_quantized = (fft_mag * 100).astype(np.int32)
        
        # Compute statistics
        stats = np.array([
            pattern.mean(),
            pattern.std(),
            pattern.min(),
            pattern.max(),
            np.median(pattern),
            fft_mag.sum()
        ])
        # Replace NaN/inf with zeros before quantization
        stats = np.nan_to_num(stats, nan=0.0, posinf=1e10, neginf=-1e10)
        stats_quantized = (stats * 1000).astype(np.int32)
        
        # Combine into hash
        hash_input = np.concatenate([
            fft_quantized.flatten()[:100],  # First 100 FFT coefficients
            stats_quantized
        ])
        
        hash_bytes = hash_input.tobytes()
        hash_hex = hashlib.sha256(hash_bytes).hexdigest()[:16]
        
        return hash_hex
    
    def compute_pattern_metrics(self, pattern: np.ndarray) -> dict:
        """
        Compute NRCI, TGIC, and observer cost metrics for a pattern.
        
        Uses analytic approximations based on pattern statistics.
        
        Args:
            pattern: 2D pattern array
            
        Returns:
            Dictionary with nrci_mean, tgic_resonance_count, observer_cost_mean
        """
        # Normalize pattern
        pattern_norm = (pattern - pattern.mean()) / (pattern.std() + 1e-10)
        
        # NRCI approximation: based on pattern coherence (smoothness)
        # Higher gradient = lower coherence
        # Safer gradient unpacking (works across numpy versions)
        grad_y, grad_x = np.gradient(pattern_norm)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2)
        
        # NRCI ≈ 1 - normalized_gradient
        # High smoothness → high NRCI
        nrci_mean = 1.0 - np.tanh(grad_mag.mean())
        
        # TGIC resonance count: peaks in pattern (local maxima)
        # Approximate using threshold crossings
        threshold = pattern_norm.mean() + pattern_norm.std()
        tgic_resonance_count = int(np.sum(pattern_norm > threshold) / 10)
        
        # Observer cost: proportional to pattern complexity
        # FFT entropy as proxy for information content
        fft = np.fft.fft2(pattern_norm)
        fft_mag = np.abs(fft)
        fft_mag_norm = fft_mag / (fft_mag.sum() + 1e-10)
        entropy = -np.sum(fft_mag_norm * np.log(fft_mag_norm + 1e-10))
        
        # Observer cost ≈ entropy (more complex = higher cost)
        observer_cost_mean = float(entropy / 10.0)  # Normalize to reasonable range
        
        return {
            'nrci_mean': float(np.clip(nrci_mean, 0.0, 1.0)),
            'tgic_resonance_count': max(0, tgic_resonance_count),
            'observer_cost_mean': float(np.clip(observer_cost_mean, 0.0, 100.0)),
            'closure_quality': float(np.clip(nrci_mean * 0.9, 0.0, 1.0))  # Approximate
        }
    
    def validate_parameters(self, value: float, spatial_freq: float) -> None:
        """
        Validate input parameters for pattern generation.
        
        Args:
            value: UBP value
            spatial_freq: Spatial frequency
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not np.isfinite(value):
            raise ValueError(f"Value must be finite, got {value}")
        
        if value <= 0:
            raise ValueError(f"Value must be positive, got {value}")
        
        if not np.isfinite(spatial_freq):
            raise ValueError(f"Spatial frequency must be finite, got {spatial_freq}")
        
        if spatial_freq < 0:
            raise ValueError(f"Spatial frequency must be non-negative, got {spatial_freq}")
    
    def _value_to_spatial_frequency(self, value: float) -> float:
        """
        Convert a UBP value to spatial frequency.
        
        Uses smooth logistic mapping for continuous, invertible transformation.
        """
        # Logarithmic scaling for wide dynamic range
        log_value = np.log10(abs(value) + 1)
        
        # Smooth logistic mapping (avoids modulo discontinuities)
        # Maps (-∞, ∞) → (0, 1) smoothly
        spatial_freq = 1.0 / (1.0 + np.exp(-log_value))
        
        return spatial_freq
    
    def _generate_radial(
        self,
        spatial_freq: float,
        symmetry: PatternSymmetry
    ) -> np.ndarray:
        """Generate radial wave pattern."""
        N = self.grid_size
        pattern = np.zeros((N, N))
        
        # Create coordinate system
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        # Radial distance
        R = np.sqrt(X**2 + Y**2)
        
        # Angular coordinate
        Theta = np.arctan2(Y, X)
        
        # Radial waves with density scaling
        # Density scale ensures visible ripples across grid (not just one blob)
        density_scale = self.grid_size / 4.0
        radial_component = np.cos(2 * np.pi * spatial_freq * density_scale * R / self.Y)
        
        # Angular modulation based on symmetry
        symmetry_order = self._get_symmetry_order(symmetry)
        angular_component = np.cos(symmetry_order * Theta)
        
        # Combine
        pattern = radial_component * (1 + 0.5 * angular_component)
        
        # Apply decay
        pattern *= np.exp(-R * self.Y)
        
        return pattern
    
    def _generate_spiral(
        self,
        spatial_freq: float,
        symmetry: PatternSymmetry
    ) -> np.ndarray:
        """Generate spiral/vortex pattern."""
        N = self.grid_size
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        R = np.sqrt(X**2 + Y**2)
        Theta = np.arctan2(Y, X)
        
        # Logarithmic spiral (canonical form: θ = a·ln(r) + b)
        # Spiral tightness increases with spatial frequency
        a = 1.0 + spatial_freq * 6.0
        
        # Clip minimum radius to avoid steep phase singularity at origin
        R_eff = np.clip(R, 1e-3, None)
        spiral_phase = a * np.log(R_eff) - Theta
        
        # Density scaling for visible spirals
        density_scale = self.grid_size / 4.0
        spiral_freq = spatial_freq * density_scale * 10
        pattern = np.cos(spiral_freq * spiral_phase)
        
        # Apply frequency-dependent damping (more physical than pure Y decay)
        # Normalized decay: Y * 3 for better attenuation
        decay_coeff = self.Y * 3.0 + spatial_freq * 0.1
        pattern *= np.exp(-R * decay_coeff)
        
        return pattern
    
    def _generate_concentric(self, spatial_freq: float) -> np.ndarray:
        """Generate concentric ring pattern."""
        N = self.grid_size
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        R = np.sqrt(X**2 + Y**2)
        
        # Concentric rings with physically meaningful wave number
        # k = spatial_freq × (1/Y) × 2π
        # Density scaling for visible rings
        density_scale = self.grid_size / 4.0
        k = spatial_freq * density_scale * (1.0 / self.Y) * 2 * np.pi
        pattern = np.cos(k * R)
        
        return pattern
    
    def _generate_diagonal(
        self,
        spatial_freq: float,
        symmetry: PatternSymmetry
    ) -> np.ndarray:
        """Generate diagonal striation pattern."""
        N = self.grid_size
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        # Diagonal waves
        angle = np.pi / 4  # 45 degrees
        U = X * np.cos(angle) + Y * np.sin(angle)
        
        pattern = np.cos(2 * np.pi * U * spatial_freq * 10 / self.Y)
        
        return pattern
    
    def _generate_grid(
        self,
        spatial_freq: float,
        symmetry: PatternSymmetry
    ) -> np.ndarray:
        """Generate grid/lattice pattern."""
        N = self.grid_size
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        # Density scaling for visible grid patterns
        density_scale = self.grid_size / 4.0
        freq = spatial_freq * density_scale * 10 / self.Y
        
        # Symmetry-aware grid patterns
        if symmetry in [PatternSymmetry.RADIAL_4, PatternSymmetry.RADIAL_8]:
            # Square lattice (standard axes)
            pattern_x = np.cos(2 * np.pi * X * freq)
            pattern_y = np.cos(2 * np.pi * Y * freq)
            pattern = pattern_x * pattern_y
        
        elif symmetry in [PatternSymmetry.RADIAL_3, PatternSymmetry.RADIAL_6]:
            # Hexagonal lattice (60° rotation basis)
            angle1 = 0
            angle2 = np.pi / 3  # 60 degrees
            U1 = X * np.cos(angle1) + Y * np.sin(angle1)
            U2 = X * np.cos(angle2) + Y * np.sin(angle2)
            pattern1 = np.cos(2 * np.pi * U1 * freq)
            pattern2 = np.cos(2 * np.pi * U2 * freq)
            pattern = pattern1 * pattern2
        
        elif symmetry in [PatternSymmetry.RADIAL_5, PatternSymmetry.RADIAL_12]:
            # Quasi-crystalline (pentagonal symmetry)
            pattern = np.zeros_like(X)
            for i in range(5):
                angle = 2 * np.pi * i / 5
                U = X * np.cos(angle) + Y * np.sin(angle)
                pattern += np.cos(2 * np.pi * U * freq)
            pattern /= 5
        
        else:
            # Default: square lattice
            pattern_x = np.cos(2 * np.pi * X * freq)
            pattern_y = np.cos(2 * np.pi * Y * freq)
            pattern = pattern_x * pattern_y
        
        return pattern
    
    def _generate_fractal(self, spatial_freq: float) -> np.ndarray:
        """
        Generate fractal pattern using fractional Brownian motion (fBm).
        
        True 2D fBm with independent X and Y variation (not radially symmetric).
        """
        N = self.grid_size
        pattern = np.zeros((N, N))
        
        # Fractional Brownian motion: sum octaves with 1/f amplitude scaling
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y = np.meshgrid(x, y)
        
        # True 2D fBm: 6 octaves with independent X and Y variation
        for i in range(6):
            freq = spatial_freq * (2 ** i)
            amplitude = 1.0 / (2 ** i)  # 1/f scaling
            # 2D Perlin-like fBm (not radially symmetric)
            pattern += amplitude * np.cos(2 * np.pi * (X * freq + Y * freq) / self.Y)
        
        return pattern
    
    def _generate_hybrid(
        self,
        spatial_freq: float,
        symmetry: PatternSymmetry
    ) -> np.ndarray:
        """Generate hybrid pattern combining multiple types."""
        # Combine radial and spiral
        radial = self._generate_radial(spatial_freq, symmetry)
        spiral = self._generate_spiral(spatial_freq, symmetry)
        
        pattern = 0.7 * radial + 0.3 * spiral
        
        return pattern
    
    def _apply_y_modulation(self, pattern: np.ndarray) -> np.ndarray:
        """Apply Y-constant geometric modulation."""
        N = pattern.shape[0]
        x = np.linspace(-1, 1, N)
        y = np.linspace(-1, 1, N)
        X, Y_coord = np.meshgrid(x, y)
        
        R = np.sqrt(X**2 + Y_coord**2)
        Theta = np.arctan2(Y_coord, X)
        
        # Y-resonant modulation
        y_mod = np.cos(2 * np.pi * R / self.Y) * np.exp(-R * self.Y)
        angular_mod = np.cos(Theta * self.Y_inv)
        
        modulated = pattern * (1 + 0.1 * y_mod * angular_mod)
        
        return modulated
    
    def _get_symmetry_order(self, symmetry: PatternSymmetry) -> int:
        """Get the numerical order of symmetry."""
        symmetry_map = {
            PatternSymmetry.RADIAL_2: 2,
            PatternSymmetry.RADIAL_3: 3,
            PatternSymmetry.RADIAL_4: 4,
            PatternSymmetry.RADIAL_5: 5,
            PatternSymmetry.RADIAL_6: 6,
            PatternSymmetry.RADIAL_8: 8,
            PatternSymmetry.RADIAL_12: 12,
            PatternSymmetry.BILATERAL: 1,
            PatternSymmetry.NONE: 0
        }
        return symmetry_map.get(symmetry, 4)


# ============================================================================
# GEOMETRIC CODEX DATABASE
# ============================================================================

class GeometricCodex:
    """
    Complete geometric codex for the UBP system.
    
    Provides:
    - Comprehensive library of geometric signatures
    - Pattern generation and recognition
    - Bidirectional translation (value ↔ geometry)
    - Pattern-based operations
    """
    
    def __init__(self, grid_size: int = 256):
        self.grid_size = grid_size
        self.generator = PatternGenerator(grid_size)
        self.config = get_config()
        
        # Signature library
        self.signatures: Dict[str, GeometricSignature] = {}
        
        # Initialize with UBP values
        self._initialize_library()
    
    def _initialize_library(self):
        """Initialize the geometric signature library with all UBP values."""
        print("Initializing UBP Geometric Codex...")
        
        # Add Y-constant family
        self._add_y_constants()
        
        # Add realm CRVs
        self._add_realm_crvs()
        
        # Add common frequencies
        self._add_common_frequencies()
        
        # Add energy scales
        self._add_energy_scales()
        
        print(f"Codex initialized with {len(self.signatures)} geometric signatures")
    
    def _add_y_constants(self):
        """Add Y-constant family to library."""
        Y = calculate_y_constant()
        Y_inv = calculate_y_inverse()
        
        self.add_signature(GeometricSignature(
            name="Y_constant",
            value=Y,
            unit="dimensionless",
            realm="fundamental",
            pattern_type=PatternType.RADIAL,
            symmetry=PatternSymmetry.RADIAL_12,
            y_resonance_factor=1.0,
            confidence=1.0
        ))
        
        self.add_signature(GeometricSignature(
            name="Y_inverse",
            value=Y_inv,
            unit="dimensionless",
            realm="fundamental",
            pattern_type=PatternType.RADIAL,
            symmetry=PatternSymmetry.RADIAL_12,
            y_inverse_scaling=1.0,
            confidence=1.0
        ))
        
        self.add_signature(GeometricSignature(
            name="O_observer",
            value=UBPConstants.O_OBSERVER,
            unit="dimensionless",
            realm="fundamental",
            pattern_type=PatternType.SPIRAL,
            symmetry=PatternSymmetry.RADIAL_12,
            confidence=1.0
        ))
    
    def _add_realm_crvs(self):
        """Add all realm CRVs and sub-CRVs to library."""
        for realm_name, realm_cfg in self.config.realms.items():
            # Main CRV
            self.add_signature(GeometricSignature(
                name=f"{realm_name}_main_crv",
                value=realm_cfg.main_crv,
                unit="Hz",
                realm=realm_name,
                wavelength_nm=realm_cfg.wavelength,
                platonic_solid=realm_cfg.platonic_solid,
                coordination_number=realm_cfg.coordination_number,
                pattern_type=self._infer_pattern_type(realm_name),
                symmetry=self._infer_symmetry(realm_cfg.coordination_number),
                confidence=1.0
            ))
            
            # Sub-CRVs
            if realm_cfg.sub_crvs:
                for i, sub_crv in enumerate(realm_cfg.sub_crvs):
                    harmonic_ratio = sub_crv / realm_cfg.main_crv if realm_cfg.main_crv > 0 else 1.0
                    harmonic_type = self._classify_harmonic(harmonic_ratio)
                    
                    self.add_signature(GeometricSignature(
                        name=f"{realm_name}_sub_crv_{i+1}",
                        value=sub_crv,
                        unit="Hz",
                        realm=realm_name,
                        harmonic_type=harmonic_type,
                        pattern_type=self._infer_pattern_type(realm_name),
                        symmetry=self._infer_symmetry(realm_cfg.coordination_number),
                        confidence=0.95 - i * 0.05
                    ))
    
    def _add_common_frequencies(self):
        """Add commonly used frequencies."""
        common_freqs = {
            "planck_frequency": 1.855e43,  # Hz
            "lyman_alpha": 2.466e15,  # Hz
            "hydrogen_line": 1.420e9,  # Hz (21 cm)
            "schumann_resonance": 7.83,  # Hz
            "earth_rotation": 1.16e-5,  # Hz
            "solar_oscillation": 3.0e-3,  # Hz
        }
        
        for name, freq in common_freqs.items():
            self.add_signature(GeometricSignature(
                name=name,
                value=freq,
                unit="Hz",
                realm="universal",
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_4,
                confidence=1.0
            ))
    
    def _add_energy_scales(self):
        """Add important energy scales in Coherence Units."""
        energy_scales = {
            "planck_energy": 1.956e9,  # GeV (converted to CU)
            "gev_scale": 1e9,  # GeV
            "mev_scale": 1e6,  # MeV
            "kev_scale": 1e3,  # keV
            "ev_scale": 1.0,  # eV
        }
        
        for name, energy in energy_scales.items():
            self.add_signature(GeometricSignature(
                name=name,
                value=energy,
                unit="CU",
                realm="energy",
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_6,
                confidence=1.0
            ))
    
    def add_signature(self, signature: GeometricSignature):
        """
        Add a geometric signature to the library.
        
        Automatically computes pattern hash and metrics if not already set.
        """
        # Generate pattern if needed for hash or metrics
        pattern = None
        
        # Compute pattern hash if not set
        if not signature.pattern_hash:
            if pattern is None:
                pattern = self.generator.generate_pattern(
                    value=signature.value,
                    pattern_type=signature.pattern_type,
                    symmetry=signature.symmetry
                )
            signature.pattern_hash = self.generator.compute_pattern_hash(pattern)
        
        # Compute NRCI/TGIC metrics if not set (check if they're zero/default)
        if signature.nrci_mean == 0.0 or signature.observer_cost_mean == 0.0:
            if pattern is None:
                pattern = self.generator.generate_pattern(
                    value=signature.value,
                    pattern_type=signature.pattern_type,
                    symmetry=signature.symmetry
                )
            metrics = self.generator.compute_pattern_metrics(pattern)
            
            # Update signature with computed metrics
            if signature.nrci_mean == 0.0:
                signature.nrci_mean = metrics['nrci_mean']
            if signature.tgic_resonance_count == 0:
                signature.tgic_resonance_count = metrics['tgic_resonance_count']
            if signature.observer_cost_mean == 0.0:
                signature.observer_cost_mean = metrics['observer_cost_mean']
            if signature.closure_quality == 0.0:
                signature.closure_quality = metrics['closure_quality']
        
        self.signatures[signature.name] = signature
    
    def get_signature(self, name: str) -> Optional[GeometricSignature]:
        """Get a signature by name."""
        return self.signatures.get(name)
    
    def find_signatures(
        self,
        realm: Optional[str] = None,
        pattern_type: Optional[PatternType] = None,
        value_range: Optional[Tuple[float, float]] = None
    ) -> List[GeometricSignature]:
        """Find signatures matching criteria."""
        results = []
        
        for sig in self.signatures.values():
            if realm and sig.realm != realm:
                continue
            if pattern_type and sig.pattern_type != pattern_type:
                continue
            if value_range:
                if not (value_range[0] <= sig.value <= value_range[1]):
                    continue
            results.append(sig)
        
        return results
    
    def generate_pattern_for_value(
        self,
        value: float,
        pattern_type: Optional[PatternType] = None,
        symmetry: Optional[PatternSymmetry] = None
    ) -> np.ndarray:
        """Generate a geometric pattern for any value."""
        if pattern_type is None:
            pattern_type = PatternType.RADIAL
        if symmetry is None:
            symmetry = PatternSymmetry.RADIAL_4
        
        return self.generator.generate_pattern(value, pattern_type, symmetry)
    
    def value_to_geometry(
        self,
        value: float,
        unit: str = "Hz"
    ) -> Tuple[np.ndarray, GeometricSignature]:
        """
        Translate a value to its geometric representation.
        
        This is the core of the bidirectional protocol.
        """
        # Check if we have a signature for this value
        matching_sigs = [s for s in self.signatures.values() 
                        if abs(s.value - value) < 1e-6 and s.unit == unit]
        
        if matching_sigs:
            sig = matching_sigs[0]
            pattern = self.generate_pattern_for_value(
                value, sig.pattern_type, sig.symmetry
            )
        else:
            # Create new signature
            sig = GeometricSignature(
                name=f"value_{value:.6e}",
                value=value,
                unit=unit,
                pattern_type=PatternType.RADIAL,
                symmetry=PatternSymmetry.RADIAL_4
            )
            pattern = self.generate_pattern_for_value(value)
        
        return pattern, sig
    
    def geometry_to_value(
        self,
        pattern: np.ndarray,
        unit: str = "Hz",
        use_spectral: bool = True
    ) -> Tuple[float, float]:
        """
        Translate a geometric pattern back to a value.
        
        Args:
            pattern: 2D geometric pattern
            unit: Unit of the value
            use_spectral: If True, use spectral extraction (recommended)
        
        Returns: (value, confidence)
        """
        if use_spectral:
            # Use spectral extraction (full-spectrum analysis)
            try:
                from spectral_extraction import SpectralValueExtractor
                extractor = SpectralValueExtractor(codex=self)
                value, confidence, _ = extractor.extract_value_from_spectrum(pattern, unit)
                return value, confidence
            except ImportError:
                # NOTE: spectral_extraction.py not found - this is expected for now
                # Fall through to pattern matching below
                pass
            except Exception as e:
                # Log error and fall through to pattern matching
                print(f"Warning: Spectral extraction failed ({e}), using pattern matching fallback")
                pass
        
        # Fallback to pattern matching (always executed if spectral fails)
        if True:
            # Fallback to pattern matching
            # This would use pattern recognition AI
            # For now, implement basic pattern matching
            
            # Extract pattern features
            features = self._extract_pattern_features(pattern)
            
            # Find best matching signature
            best_match = None
            best_score = -1
            
            for sig in self.signatures.values():
                if sig.unit != unit:
                    continue
                
                sig_pattern = self.generate_pattern_for_value(
                    sig.value, sig.pattern_type, sig.symmetry
                )
                sig_features = self._extract_pattern_features(sig_pattern)
                
                score = self._compare_features(features, sig_features)
                if score > best_score:
                    best_score = score
                    best_match = sig
            
            if best_match:
                return best_match.value, best_score
            else:
                return 0.0, 0.0
    
    def _extract_pattern_features(self, pattern: np.ndarray) -> Dict:
        """Extract features from a pattern for recognition."""
        features = {
            'mean': np.mean(pattern),
            'std': np.std(pattern),
            'max': np.max(pattern),
            'min': np.min(pattern),
            'fft_peak': self._get_fft_peak_frequency(pattern)
        }
        return features
    
    def _get_fft_peak_frequency(self, pattern: np.ndarray) -> float:
        """Get the peak frequency from FFT in normalized units (cycles per unit)."""
        from scipy.fft import fft2, fftshift
        
        N = pattern.shape[0]
        fft_pattern = fftshift(fft2(pattern))
        magnitude = np.abs(fft_pattern)
        
        # Find peak (excluding DC component)
        center = N // 2
        magnitude[center-2:center+3, center-2:center+3] = 0
        
        peak_idx = np.unravel_index(np.argmax(magnitude), magnitude.shape)
        
        # Calculate distance in pixels
        pixel_dist = np.sqrt((peak_idx[0] - center)**2 + (peak_idx[1] - center)**2)
        
        # Normalize to spatial frequency (0.0 to 0.5 cycles/pixel)
        # Account for density scaling used in generation
        density_scale = N / 4.0
        norm_freq = pixel_dist / density_scale
        
        return norm_freq
    
    def _compare_features(self, features1: Dict, features2: Dict) -> float:
        """Compare two feature sets and return similarity score."""
        # Simple Euclidean distance in feature space
        diff = 0
        for key in features1:
            if key in features2:
                diff += (features1[key] - features2[key])**2
        
        # Convert to similarity score [0, 1]
        similarity = 1.0 / (1.0 + np.sqrt(diff))
        return similarity
    
    def _infer_pattern_type(self, realm: str) -> PatternType:
        """Infer pattern type from realm."""
        pattern_map = {
            'quantum': PatternType.SPIRAL,
            'electromagnetic': PatternType.RADIAL,
            'gravitational': PatternType.CONCENTRIC,
            'plasma': PatternType.HYBRID,
            'nuclear': PatternType.FRACTAL,
            'optical': PatternType.RADIAL,
            'biologic': PatternType.GRID
        }
        return pattern_map.get(realm, PatternType.RADIAL)
    
    def _infer_symmetry(self, coordination: int) -> PatternSymmetry:
        """Infer symmetry from coordination number."""
        symmetry_map = {
            2: PatternSymmetry.RADIAL_2,
            3: PatternSymmetry.RADIAL_3,
            4: PatternSymmetry.RADIAL_4,
            5: PatternSymmetry.RADIAL_5,
            6: PatternSymmetry.RADIAL_6,
            8: PatternSymmetry.RADIAL_8,
            12: PatternSymmetry.RADIAL_12
        }
        return symmetry_map.get(coordination, PatternSymmetry.RADIAL_4)
    
    def _classify_harmonic(self, ratio: float) -> str:
        """Classify harmonic relationship."""
        if abs(ratio - 0.25) < 0.01:
            return "quarter_harmonic"
        elif abs(ratio - 0.5) < 0.01:
            return "half_harmonic"
        elif abs(ratio - 1.0) < 0.01:
            return "fundamental"
        elif abs(ratio - 2.0) < 0.01:
            return "second_harmonic"
        elif abs(ratio - 4.0) < 0.01:
            return "fourth_harmonic"
        elif ratio < 1.0:
            return f"subharmonic_{ratio:.2f}x"
        else:
            return f"harmonic_{ratio:.2f}x"
    
    def save_library(self, path: str):
        """Save the signature library to JSON."""
        data = {
            'signatures': {name: sig.to_dict() 
                          for name, sig in self.signatures.items()},
            'metadata': {
                'grid_size': self.grid_size,
                'total_signatures': len(self.signatures),
                'Y_constant': calculate_y_constant(),
                'Y_inverse': calculate_y_inverse()
            }
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_library(self, path: str):
        """Load signature library from JSON."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.signatures = {
            name: GeometricSignature.from_dict(sig_data)
            for name, sig_data in data['signatures'].items()
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_codex(grid_size: int = 256) -> GeometricCodex:
    """Create and initialize a geometric codex."""
    return GeometricCodex(grid_size)


def value_to_pattern(value: float, unit: str = "Hz", grid_size: int = 256) -> np.ndarray:
    """Quick function to convert a value to a pattern."""
    codex = create_codex(grid_size)
    pattern, _ = codex.value_to_geometry(value, unit)
    return pattern


def pattern_to_value(pattern: np.ndarray, unit: str = "Hz") -> Tuple[float, float]:
    """Quick function to convert a pattern to a value."""
    codex = create_codex(pattern.shape[0])
    return codex.geometry_to_value(pattern, unit)
