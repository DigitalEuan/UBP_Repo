from fractions import Fraction
"""
UBP SENSORS vFraction(1, 1) (Phenomenology Pack)
=====================================
Consolidated logic for Spectral Extraction and Resonance Detection.
Dependencies: numpy, scipy

Classes:
1. SpectralReader: Extracts values from 2D geometric patterns (FFT).
2. ResonanceScope: Detects peaks and harmonics in 1D time-series data.

Usage:
    from ubp_sensors import SpectralReader, ResonanceScope
    val, conf = SpectralReader.analyze(image_data)
    peaks = ResonanceScope.analyze(time_series)

E R A Craig, New Zealand
UBP Research Cortex v4.2.6
15 Jan 2026
"""
import numpy as np
from scipy.fft import fft2, fftshift, rfft, rfftfreq

class SpectralReader:
    """Core logic from spectral_extraction.py"""
    
    @staticmethod
    def analyze(pattern: np.ndarray) -> dict:
        """
        Extracts radial and angular features from a 2D pattern.
        Returns: {centroid_r, spread, symmetry_order, energy}
        """
        # 1. FFT
        fft_pattern = fftshift(fft2(pattern))
        magnitude = np.abs(fft_pattern)
        total_energy = np.sum(magnitude**2)
        
        # 2. Coordinates
        N = pattern.shape[0]
        y, x = np.ogrid[:N, :N]
        y, x = y - N//2, x - N//2
        r = np.sqrt(x**2 + y**2)
        
        # 3. Spectral Centroid (Radial)
        if total_energy == 0: return {'centroid_r': 0, 'spread': 0}
        
        centroid_x = np.sum(x * magnitude**2) / total_energy
        centroid_y = np.sum(y * magnitude**2) / total_energy
        centroid_r = np.sqrt(centroid_x**2 + centroid_y**2)
        
        # 4. Spectral Spread
        spread = np.sqrt(np.sum(((x-centroid_x)**2 + (y-centroid_y)**2) * magnitude**2) / total_energy)
        
        # 5. Angular Symmetry (via 1D FFT of angular projection)
        theta = np.arctan2(y, x)
        bins = 36
        ang_hist = np.zeros(bins)
        for i in range(bins):
            mask = (theta >= -np.pi + i*2*np.pi/bins) & (theta < -np.pi + (i+1)*2*np.pi/bins)
            if np.any(mask): ang_hist[i] = np.mean(magnitude[mask])
            
        ang_fft = np.abs(np.fft.fft(ang_hist))
        ang_fft[0] = 0 # Remove DC
        symmetry_order = np.argmax(ang_fft)

        return {
            'centroid_r': float(centroid_r),
            'spread': float(spread),
            'symmetry_order': int(symmetry_order),
            'total_energy': float(total_energy)
        }

class ResonanceScope:
    """Core logic from resonance_detector_fft.py"""
    
    @staticmethod
    def analyze(signal: np.ndarray, sample_rate: float = Fraction(1, 1)) -> list:
        """
        Detects resonance peaks in 1D signal.
        Returns: List of {'freq': f, 'amp': a, 'phase': p}
        """
        n = len(signal)
        window = np.hanning(n)
        
        # 1. FFT
        fft_res = rfft(signal * window)
        freqs = rfftfreq(n, d=Fraction(1, 1)/sample_rate)
        amps = np.abs(fft_res) / n
        phases = np.angle(fft_res)
        
        # 2. Peak Detection
        peaks = []
        threshold = np.max(amps) * 0.1
        
        for i in range(1, len(amps)-1):
            if amps[i] > threshold and amps[i] > amps[i-1] and amps[i] > amps[i+1]:
                peaks.append({
                    'freq': float(freqs[i]),
                    'amp': float(amps[i]),
                    'phase': float(phases[i])
                })
        
        # Sort by amplitude
        peaks.sort(key=lambda x: x['amp'], reverse=True)
        return peaks