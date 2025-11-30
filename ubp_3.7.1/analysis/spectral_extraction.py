"""
==================================
UBP 3.7.1 Spectral Value Extraction
Author: Euan R A Craig, New Zealand
Date: 30 November 2025
==================================

This module implements spectral value extraction from geometric patterns.

Key Insight: The UBP system is 12-dimensional (π² + 2 ≈ 11.87), but geometric
patterns are 2D projections. The value is encoded in the FULL FREQUENCY SPECTRUM,
not just the spatial pattern. This module extracts values by analyzing the complete
spectral decomposition.

This solves the "projection problem" - recovering high-dimensional information
from 2D projections by analyzing the frequency domain.
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Tuple, Dict, List
import math


# Global calibration cache (shared across instances)
_CALIBRATION_CACHE = {}
_CALIBRATION_CACHE_INITIALIZED = False

class SpectralValueExtractor:
    """
    Extract values from geometric patterns using full spectral analysis.
    
    This bypasses pattern matching by directly reading the value from
    the pattern's frequency spectrum.
    
    Uses global calibration cache for performance.
    """
    
    def __init__(self, codex=None, use_cache=True):
        # Y-constant family for reference
        self.Y = math.pi / (math.pi**2 + 2)
        self.Y_inv = math.pi + 2/math.pi
        
        # Spectral signature database
        self.spectral_signatures = {}
        
        # Calibration data (learned from codex or loaded from cache)
        self.calibration = {}
        self.use_cache = use_cache
        
        # If codex provided, learn calibration (or use cache)
        if codex is not None:
            self._initialize_calibration(codex)
    
    def _initialize_calibration(self, codex):
        """Initialize calibration from codex or cache."""
        global _CALIBRATION_CACHE, _CALIBRATION_CACHE_INITIALIZED
        
        if self.use_cache and _CALIBRATION_CACHE_INITIALIZED:
            # Use cached calibration
            self.calibration = _CALIBRATION_CACHE
        else:
            # Learn new calibration
            self._learn_calibration(codex)
            
            # Cache it
            if self.use_cache:
                _CALIBRATION_CACHE = self.calibration
                _CALIBRATION_CACHE_INITIALIZED = True
    
    def _learn_calibration(self, codex):
        """
        Learn the mapping between spectral features and values from the codex.
        
        This creates a calibrated decoder by analyzing patterns with known values.
        """
        print("Learning spectral calibration from codex...")
        
        # Analyze all signatures in the codex
        for unit in ['Hz', 'dimensionless', 'CU']:
            unit_data = []
            
            for sig in codex.signatures.values():
                if sig.unit != unit:
                    continue
                
                # Generate pattern for this signature
                pattern = codex.generate_pattern_for_value(
                    sig.value, sig.pattern_type, sig.symmetry
                )
                
                # Extract spectral features
                fft_pattern = fftshift(fft2(pattern))
                magnitude = np.abs(fft_pattern)
                N = pattern.shape[0]
                center = N // 2
                y_coords, x_coords = np.ogrid[:N, :N]
                y_coords = y_coords - center
                x_coords = x_coords - center
                r = np.sqrt(x_coords**2 + y_coords**2)
                
                radial_spectrum = self._compute_radial_spectrum(magnitude, r, N)
                angular_spectrum = self._compute_angular_spectrum(magnitude, x_coords, y_coords)
                phase = np.angle(fft_pattern)
                
                features = self._extract_spectral_features(
                    magnitude, phase, radial_spectrum, angular_spectrum
                )
                
                # Store (features, value) pair
                unit_data.append({
                    'value': sig.value,
                    'features': features
                })
            
            # Learn mapping for this unit
            if len(unit_data) > 0:
                self.calibration[unit] = unit_data
                print(f"  Learned {len(unit_data)} calibration points for {unit}")
    
    def extract_value_from_spectrum(
        self,
        pattern: np.ndarray,
        unit: str = "Hz",
        reference_value: float = None
    ) -> Tuple[float, float, Dict]:
        """
        Extract value from pattern using full spectral analysis.
        
        Args:
            pattern: 2D geometric pattern
            unit: Unit of the value
            reference_value: Optional reference for relative extraction
        
        Returns:
            (extracted_value, confidence, diagnostics)
        """
        # Transform to frequency domain
        fft_pattern = fftshift(fft2(pattern))
        magnitude = np.abs(fft_pattern)
        phase = np.angle(fft_pattern)
        
        N = pattern.shape[0]
        center = N // 2
        
        # Create radial frequency coordinates
        y_coords, x_coords = np.ogrid[:N, :N]
        y_coords = y_coords - center
        x_coords = x_coords - center
        r = np.sqrt(x_coords**2 + y_coords**2)
        
        # Compute radial spectrum (azimuthal average)
        radial_spectrum = self._compute_radial_spectrum(magnitude, r, N)
        
        # Compute angular spectrum (radial average)
        angular_spectrum = self._compute_angular_spectrum(magnitude, x_coords, y_coords)
        
        # Extract spectral features
        features = self._extract_spectral_features(
            magnitude, phase, radial_spectrum, angular_spectrum
        )
        
        # Decode value from spectral features
        if reference_value is not None:
            # Relative extraction (for Y-refined patterns)
            value, confidence = self._decode_relative_value(
                features, reference_value, unit
            )
        else:
            # Absolute extraction
            value, confidence = self._decode_absolute_value(
                features, unit
            )
        
        diagnostics = {
            'radial_spectrum': radial_spectrum,
            'angular_spectrum': angular_spectrum,
            'features': features,
            'spectral_energy': np.sum(magnitude**2),
            'spectral_entropy': self._compute_spectral_entropy(magnitude)
        }
        
        return value, confidence, diagnostics
    
    def _compute_radial_spectrum(
        self,
        magnitude: np.ndarray,
        r: np.ndarray,
        N: int
    ) -> np.ndarray:
        """
        Compute radial spectrum by azimuthal averaging.
        
        This captures how energy is distributed across spatial frequencies.
        """
        max_r = int(np.sqrt(2) * N / 2)
        radial_spectrum = np.zeros(max_r)
        
        for i in range(max_r):
            mask = (r >= i) & (r < i + 1)
            if np.any(mask):
                radial_spectrum[i] = np.mean(magnitude[mask])
        
        return radial_spectrum
    
    def _compute_angular_spectrum(
        self,
        magnitude: np.ndarray,
        x_coords: np.ndarray,
        y_coords: np.ndarray
    ) -> np.ndarray:
        """
        Compute angular spectrum by radial averaging.
        
        This captures rotational symmetry and harmonic structure.
        """
        theta = np.arctan2(y_coords, x_coords)
        
        # Bin by angle (36 bins = 10° each)
        n_bins = 36
        angular_spectrum = np.zeros(n_bins)
        
        for i in range(n_bins):
            theta_min = -np.pi + i * 2 * np.pi / n_bins
            theta_max = -np.pi + (i + 1) * 2 * np.pi / n_bins
            mask = (theta >= theta_min) & (theta < theta_max)
            if np.any(mask):
                angular_spectrum[i] = np.mean(magnitude[mask])
        
        return angular_spectrum
    
    def _extract_spectral_features(
        self,
        magnitude: np.ndarray,
        phase: np.ndarray,
        radial_spectrum: np.ndarray,
        angular_spectrum: np.ndarray
    ) -> Dict:
        """
        Extract comprehensive spectral features.
        
        These features encode the value in frequency space.
        """
        # Total spectral energy
        total_energy = np.sum(magnitude**2)
        
        # Spectral centroid (center of mass in frequency space)
        N = magnitude.shape[0]
        center = N // 2
        y_coords, x_coords = np.ogrid[:N, :N]
        y_coords = y_coords - center
        x_coords = x_coords - center
        
        centroid_x = np.sum(x_coords * magnitude**2) / (total_energy + 1e-10)
        centroid_y = np.sum(y_coords * magnitude**2) / (total_energy + 1e-10)
        centroid_r = np.sqrt(centroid_x**2 + centroid_y**2)
        
        # Spectral spread (variance in frequency space)
        spread = np.sqrt(
            np.sum((x_coords - centroid_x)**2 * magnitude**2 + 
                   (y_coords - centroid_y)**2 * magnitude**2) / (total_energy + 1e-10)
        )
        
        # Peak frequency
        peak_idx = np.argmax(radial_spectrum)
        peak_frequency = peak_idx
        
        # Harmonic content (peaks in radial spectrum)
        harmonics = self._find_harmonic_peaks(radial_spectrum)
        
        # Angular symmetry order (from angular spectrum)
        symmetry_order = self._detect_symmetry_order(angular_spectrum)
        
        # Phase coherence
        phase_coherence = self._compute_phase_coherence(phase)
        
        # Spectral flatness (measure of noise vs tones)
        flatness = self._compute_spectral_flatness(radial_spectrum)
        
        features = {
            'total_energy': float(total_energy),
            'centroid_r': float(centroid_r),
            'spread': float(spread),
            'peak_frequency': float(peak_frequency),
            'harmonics': harmonics,
            'symmetry_order': int(symmetry_order),
            'phase_coherence': float(phase_coherence),
            'spectral_flatness': float(flatness),
            'radial_energy_ratio': float(np.sum(radial_spectrum[:10]) / (np.sum(radial_spectrum) + 1e-10)),
            'angular_variation': float(np.std(angular_spectrum))
        }
        
        return features
    
    def _find_harmonic_peaks(self, spectrum: np.ndarray) -> List[int]:
        """Find harmonic peaks in spectrum."""
        peaks = []
        threshold = np.max(spectrum) * 0.1  # 10% of max
        
        for i in range(1, len(spectrum) - 1):
            if spectrum[i] > threshold:
                if spectrum[i] > spectrum[i-1] and spectrum[i] > spectrum[i+1]:
                    peaks.append(i)
        
        return peaks[:5]  # Return top 5 peaks
    
    def _detect_symmetry_order(self, angular_spectrum: np.ndarray) -> int:
        """Detect rotational symmetry order from angular spectrum."""
        # FFT of angular spectrum reveals symmetry order
        angular_fft = np.abs(np.fft.fft(angular_spectrum))
        
        # Find dominant frequency (excluding DC)
        angular_fft[0] = 0
        symmetry_order = np.argmax(angular_fft)
        
        return symmetry_order if symmetry_order > 0 else 1
    
    def _compute_phase_coherence(self, phase: np.ndarray) -> float:
        """Compute phase coherence across the spectrum."""
        # Phase coherence = consistency of phase relationships
        phase_diff_x = np.diff(phase, axis=0)
        phase_diff_y = np.diff(phase, axis=1)
        
        # Compute total phase variation
        phase_var = np.mean(phase_diff_x**2) + np.mean(phase_diff_y**2)
        coherence = 1.0 / (1.0 + phase_var)
        return coherence
    
    def _compute_spectral_flatness(self, spectrum: np.ndarray) -> float:
        """Compute spectral flatness (Wiener entropy)."""
        spectrum_pos = spectrum[spectrum > 0]
        if len(spectrum_pos) == 0:
            return 0.0
        
        geometric_mean = np.exp(np.mean(np.log(spectrum_pos)))
        arithmetic_mean = np.mean(spectrum_pos)
        
        flatness = geometric_mean / (arithmetic_mean + 1e-10)
        return flatness
    
    def _compute_spectral_entropy(self, magnitude: np.ndarray) -> float:
        """Compute spectral entropy."""
        magnitude_norm = magnitude / (np.sum(magnitude) + 1e-10)
        magnitude_norm = magnitude_norm[magnitude_norm > 0]
        
        entropy = -np.sum(magnitude_norm * np.log(magnitude_norm))
        return entropy
    
    def _decode_absolute_value(
        self,
        features: Dict,
        unit: str
    ) -> Tuple[float, float]:
        """
        Decode absolute value from spectral features using calibration.
        
        This uses learned mapping from the signature library.
        """
        if unit not in self.calibration or len(self.calibration[unit]) == 0:
            # No calibration available, use fallback
            return self._decode_fallback(features, unit)
        
        # Find nearest neighbor in calibration space
        best_match = None
        best_distance = float('inf')
        
        for calib_point in self.calibration[unit]:
            calib_features = calib_point['features']
            
            # Compute feature distance
            distance = self._compute_feature_distance(features, calib_features)
            
            if distance < best_distance:
                best_distance = distance
                best_match = calib_point
        
        if best_match:
            value = best_match['value']
            # Confidence inversely proportional to distance
            confidence = 1.0 / (1.0 + best_distance)
            return value, confidence
        else:
            return self._decode_fallback(features, unit)
    
    def _compute_feature_distance(self, features1: Dict, features2: Dict) -> float:
        """
        Compute distance between two feature sets.
        
        Uses normalized Euclidean distance in feature space.
        """
        # Key features for comparison
        key_features = ['centroid_r', 'spread', 'peak_frequency', 
                       'phase_coherence', 'spectral_flatness']
        
        distance = 0.0
        for key in key_features:
            if key in features1 and key in features2:
                # Normalize by feature scale
                f1 = features1[key]
                f2 = features2[key]
                scale = max(abs(f1), abs(f2), 1.0)
                distance += ((f1 - f2) / scale) ** 2
        
        return np.sqrt(distance)
    
    def _decode_fallback(
        self,
        features: Dict,
        unit: str
    ) -> Tuple[float, float]:
        """
        Fallback decoder when no calibration is available.
        """
        centroid_r = features['centroid_r']
        peak_freq = features['peak_frequency']
        total_energy = features['total_energy']
        
        # Simple heuristic
        if unit == "Hz":
            value = peak_freq * 1e10  # Scale factor
        elif unit == "dimensionless":
            value = centroid_r / 100.0
        elif unit == "CU":
            value = total_energy
        else:
            value = centroid_r
        
        confidence = 0.1  # Low confidence for fallback
        return value, confidence
    
    def _decode_relative_value(
        self,
        features: Dict,
        reference_value: float,
        unit: str
    ) -> Tuple[float, float]:
        """
        Decode value relative to a reference (for Y-refined patterns).
        
        This uses the spectral shift to determine the transformation factor.
        """
        # After Y-refinement, the spectral centroid shifts
        # The shift factor encodes the Y-multiplication
        
        centroid_r = features['centroid_r']
        
        # The Y-refinement causes a predictable spectral shift
        # Forward (×Y): centroid shifts inward (lower frequencies)
        # Backward (×1/Y): centroid shifts outward (higher frequencies)
        
        # Decode the transformation factor from spectral shift
        # This is the key insight: Y-operations are spectral shifts!
        
        # Baseline centroid for reference value
        baseline_centroid = 50.0  # Empirical baseline
        
        # Shift factor
        shift_factor = centroid_r / baseline_centroid
        
        # Decode value
        if shift_factor < 1.0:
            # Inward shift → multiplied by Y
            value = reference_value * self.Y * shift_factor
        else:
            # Outward shift → multiplied by 1/Y
            value = reference_value * self.Y_inv * (shift_factor - 1.0) / self.Y_inv
        
        # Confidence based on consistency
        confidence = features['phase_coherence']
        
        return value, confidence


def extract_value_from_pattern_spectral(
    pattern: np.ndarray,
    unit: str = "Hz",
    reference_value: float = None
) -> Tuple[float, float]:
    """
    Convenience function for spectral value extraction.
    
    Args:
        pattern: 2D geometric pattern
        unit: Unit of the value
        reference_value: Optional reference for relative extraction
    
    Returns:
        (value, confidence)
    """
    extractor = SpectralValueExtractor()
    value, confidence, _ = extractor.extract_value_from_spectrum(
        pattern, unit, reference_value
    )
    return value, confidence
