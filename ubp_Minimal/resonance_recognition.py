"""
Universal Binary Principle (UBP) - Resonance Recognition System
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements the Resonance Recognition system for identifying
and reacting to emergent resonant patterns within the UBP bitfield.
"""

import numpy as np
import math
import time
from typing import Dict, List, Tuple, Optional, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import scipy.signal as signal
import scipy.fft as fft

from .offbit import OffBit
from .bitfield import SparseBitfield


class ResonanceType(Enum):
    """Types of resonance patterns."""
    HARMONIC = "harmonic"              # Simple harmonic oscillation
    COHERENT = "coherent"              # Coherent phase alignment
    STANDING_WAVE = "standing_wave"    # Standing wave patterns
    INTERFERENCE = "interference"       # Constructive/destructive interference
    QUANTUM_BEAT = "quantum_beat"      # Quantum beating patterns
    FRACTAL = "fractal"                # Self-similar fractal patterns
    SPIRAL = "spiral"                  # Spiral/helical patterns
    CRYSTALLINE = "crystalline"        # Crystal-like ordered structures
    CHAOTIC = "chaotic"                # Chaotic attractors
    SOLITON = "soliton"                # Soliton wave packets


@dataclass
class ResonancePattern:
    """Represents a detected resonance pattern."""
    pattern_id: str
    resonance_type: ResonanceType
    frequency: float
    amplitude: float
    phase: float
    coherence: float
    spatial_extent: Tuple[int, int, int, int, int, int]  # 6D bounding box
    temporal_duration: float
    confidence: float
    coordinates: List[Tuple[int, int, int, int, int, int]]
    offbits: List[OffBit]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def energy(self) -> float:
        """Calculate pattern energy."""
        return self.amplitude ** 2 * len(self.offbits)
    
    @property
    def wavelength(self) -> float:
        """Calculate wavelength from frequency."""
        c = 299792458  # Speed of light
        return c / self.frequency if self.frequency > 0 else float('inf')


@dataclass
class ResonanceEvent:
    """Represents a resonance event trigger."""
    event_id: str
    pattern: ResonancePattern
    trigger_time: float
    action_taken: str
    result: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class ResonanceDetector:
    """Base class for resonance pattern detectors."""
    
    def __init__(self, resonance_type: ResonanceType, 
                 sensitivity: float = 0.1,
                 min_coherence: float = 0.5):
        """
        Initialize resonance detector.
        
        Args:
            resonance_type: Type of resonance to detect
            sensitivity: Detection sensitivity (0-1)
            min_coherence: Minimum coherence threshold
        """
        self.resonance_type = resonance_type
        self.sensitivity = sensitivity
        self.min_coherence = min_coherence
        self.detection_history = deque(maxlen=1000)
        self.stats = {
            'detections': 0,
            'false_positives': 0,
            'processing_time': 0.0
        }
    
    def detect(self, bitfield: SparseBitfield, 
               time_window: float = 1.0) -> List[ResonancePattern]:
        """
        Detect resonance patterns in bitfield.
        
        Args:
            bitfield: Bitfield to analyze
            time_window: Time window for analysis
        
        Returns:
            List of detected resonance patterns
        """
        start_time = time.time()
        patterns = self._detect_patterns(bitfield, time_window)
        
        # Filter by coherence threshold
        filtered_patterns = [p for p in patterns if p.coherence >= self.min_coherence]
        
        # Update statistics
        self.stats['detections'] += len(filtered_patterns)
        self.stats['processing_time'] += time.time() - start_time
        
        # Record detection history
        for pattern in filtered_patterns:
            self.detection_history.append({
                'timestamp': time.time(),
                'pattern_id': pattern.pattern_id,
                'frequency': pattern.frequency,
                'coherence': pattern.coherence
            })
        
        return filtered_patterns
    
    def _detect_patterns(self, bitfield: SparseBitfield, 
                        time_window: float) -> List[ResonancePattern]:
        """Override in subclasses to implement specific detection logic."""
        return []


class HarmonicResonanceDetector(ResonanceDetector):
    """Detector for harmonic resonance patterns."""
    
    def __init__(self, **kwargs):
        super().__init__(ResonanceType.HARMONIC, **kwargs)
        self.frequency_bins = np.logspace(0, 6, 100)  # 1 Hz to 1 MHz
    
    def _detect_patterns(self, bitfield: SparseBitfield, 
                        time_window: float) -> List[ResonancePattern]:
        """Detect harmonic resonance patterns using FFT analysis."""
        patterns = []
        
        active_offbits = bitfield.get_active_offbits()
        if len(active_offbits) < 3:
            return patterns
        
        # Extract time series data from OffBit values
        time_series = []
        coordinates = []
        
        for coord, offbit in active_offbits:
            time_series.append(offbit.active_bits)
            coordinates.append(coord)
        
        if len(time_series) < 8:  # Need minimum samples for FFT
            return patterns
        
        # Perform FFT analysis
        fft_result = fft.fft(time_series)
        frequencies = fft.fftfreq(len(time_series), d=time_window/len(time_series))
        
        # Find peaks in frequency domain
        magnitudes = np.abs(fft_result)
        peaks, properties = signal.find_peaks(
            magnitudes, 
            height=self.sensitivity * np.max(magnitudes),
            distance=2
        )
        
        # Create resonance patterns for significant peaks
        for peak_idx in peaks:
            if peak_idx < len(frequencies) // 2:  # Only positive frequencies
                freq = abs(frequencies[peak_idx])
                amplitude = magnitudes[peak_idx] / len(time_series)
                phase = np.angle(fft_result[peak_idx])
                
                # Calculate coherence based on peak sharpness
                coherence = self._calculate_harmonic_coherence(
                    magnitudes, peak_idx, len(frequencies)
                )
                
                if coherence >= self.min_coherence:
                    pattern = ResonancePattern(
                        pattern_id=f"harmonic_{int(time.time()*1000)}_{peak_idx}",
                        resonance_type=self.resonance_type,
                        frequency=freq,
                        amplitude=amplitude,
                        phase=phase,
                        coherence=coherence,
                        spatial_extent=self._calculate_spatial_extent(coordinates),
                        temporal_duration=time_window,
                        confidence=min(1.0, coherence * amplitude),
                        coordinates=coordinates,
                        offbits=[offbit for _, offbit in active_offbits],
                        metadata={
                            'peak_index': peak_idx,
                            'fft_magnitude': float(magnitudes[peak_idx]),
                            'samples_analyzed': len(time_series)
                        }
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _calculate_harmonic_coherence(self, magnitudes: np.ndarray, 
                                    peak_idx: int, total_bins: int) -> float:
        """Calculate coherence based on peak characteristics."""
        if peak_idx == 0 or peak_idx >= len(magnitudes) - 1:
            return 0.0
        
        peak_mag = magnitudes[peak_idx]
        left_mag = magnitudes[peak_idx - 1]
        right_mag = magnitudes[peak_idx + 1]
        
        # Coherence based on peak prominence
        prominence = peak_mag / (0.5 * (left_mag + right_mag) + 1e-10)
        coherence = min(1.0, prominence / 10.0)  # Normalize
        
        return coherence
    
    def _calculate_spatial_extent(self, coordinates: List[Tuple]) -> Tuple[int, int, int, int, int, int]:
        """Calculate 6D bounding box of coordinates."""
        if not coordinates:
            return (0, 0, 0, 0, 0, 0)
        
        coords_array = np.array(coordinates)
        min_coords = np.min(coords_array, axis=0)
        max_coords = np.max(coords_array, axis=0)
        
        extent = tuple(max_coords - min_coords)
        return extent if len(extent) == 6 else extent + (0,) * (6 - len(extent))


class CoherentResonanceDetector(ResonanceDetector):
    """Detector for coherent phase alignment patterns."""
    
    def __init__(self, **kwargs):
        super().__init__(ResonanceType.COHERENT, **kwargs)
        self.phase_bins = 32  # Number of phase bins for analysis
    
    def _detect_patterns(self, bitfield: SparseBitfield, 
                        time_window: float) -> List[ResonancePattern]:
        """Detect coherent phase alignment patterns."""
        patterns = []
        
        active_offbits = bitfield.get_active_offbits()
        if len(active_offbits) < 4:
            return patterns
        
        # Group OffBits by spatial proximity
        clusters = self._cluster_by_proximity(active_offbits)
        
        for cluster_id, cluster_offbits in clusters.items():
            if len(cluster_offbits) < 3:
                continue
            
            # Calculate phase coherence within cluster
            phases = []
            amplitudes = []
            coordinates = []
            offbits = []
            
            for coord, offbit in cluster_offbits:
                # Extract phase information from layer relationships
                phase = self._extract_phase(offbit)
                amplitude = offbit.active_bits / 24.0
                
                phases.append(phase)
                amplitudes.append(amplitude)
                coordinates.append(coord)
                offbits.append(offbit)
            
            # Calculate coherence using circular statistics
            coherence = self._calculate_phase_coherence(phases, amplitudes)
            
            if coherence >= self.min_coherence:
                # Calculate dominant frequency from phase variations
                frequency = self._estimate_frequency_from_phases(phases, coordinates)
                
                pattern = ResonancePattern(
                    pattern_id=f"coherent_{int(time.time()*1000)}_{cluster_id}",
                    resonance_type=self.resonance_type,
                    frequency=frequency,
                    amplitude=np.mean(amplitudes),
                    phase=np.mean(phases),
                    coherence=coherence,
                    spatial_extent=self._calculate_spatial_extent(coordinates),
                    temporal_duration=time_window,
                    confidence=coherence * np.mean(amplitudes),
                    coordinates=coordinates,
                    offbits=offbits,
                    metadata={
                        'cluster_id': cluster_id,
                        'cluster_size': len(cluster_offbits),
                        'phase_variance': np.var(phases)
                    }
                )
                patterns.append(pattern)
        
        return patterns
    
    def _cluster_by_proximity(self, active_offbits: List[Tuple], 
                            max_distance: float = 10.0) -> Dict[int, List[Tuple]]:
        """Cluster OffBits by spatial proximity."""
        clusters = defaultdict(list)
        cluster_id = 0
        processed = set()
        
        for i, (coord1, offbit1) in enumerate(active_offbits):
            if i in processed:
                continue
            
            current_cluster = [(coord1, offbit1)]
            processed.add(i)
            
            # Find nearby OffBits
            for j, (coord2, offbit2) in enumerate(active_offbits[i+1:], i+1):
                if j in processed:
                    continue
                
                distance = math.sqrt(sum((a - b)**2 for a, b in zip(coord1[:3], coord2[:3])))
                if distance <= max_distance:
                    current_cluster.append((coord2, offbit2))
                    processed.add(j)
            
            if len(current_cluster) >= 3:  # Minimum cluster size
                clusters[cluster_id] = current_cluster
                cluster_id += 1
        
        return clusters
    
    def _extract_phase(self, offbit: OffBit) -> float:
        """Extract phase information from OffBit layers."""
        # Use layer relationships to estimate phase
        reality, info, activation = offbit.layers
        
        # Phase based on layer balance and bit patterns
        if reality + info + activation == 0:
            return 0.0
        
        # Normalize and calculate phase angle
        total = reality + info + activation
        r_norm = reality / total
        i_norm = info / total
        
        # Convert to phase angle (0 to 2π)
        phase = math.atan2(i_norm - 0.5, r_norm - 0.5) + math.pi
        return phase
    
    def _calculate_phase_coherence(self, phases: List[float], 
                                 amplitudes: List[float]) -> float:
        """Calculate phase coherence using circular statistics."""
        if not phases:
            return 0.0
        
        # Convert to complex representation
        complex_sum = sum(amp * np.exp(1j * phase) 
                         for phase, amp in zip(phases, amplitudes))
        
        # Coherence is the magnitude of the normalized sum
        total_amplitude = sum(amplitudes)
        if total_amplitude == 0:
            return 0.0
        
        coherence = abs(complex_sum) / total_amplitude
        return min(1.0, coherence)
    
    def _estimate_frequency_from_phases(self, phases: List[float], 
                                      coordinates: List[Tuple]) -> float:
        """Estimate frequency from spatial phase variations."""
        if len(phases) < 2:
            return 1.0  # Default frequency
        
        # Calculate phase gradients in space
        phase_gradients = []
        
        for i in range(len(phases) - 1):
            phase_diff = phases[i+1] - phases[i]
            # Handle phase wrapping
            if phase_diff > math.pi:
                phase_diff -= 2 * math.pi
            elif phase_diff < -math.pi:
                phase_diff += 2 * math.pi
            
            spatial_diff = math.sqrt(sum(
                (a - b)**2 for a, b in zip(coordinates[i][:3], coordinates[i+1][:3])
            ))
            
            if spatial_diff > 0:
                gradient = abs(phase_diff) / spatial_diff
                phase_gradients.append(gradient)
        
        if not phase_gradients:
            return 1.0
        
        # Estimate frequency from average phase gradient
        avg_gradient = np.mean(phase_gradients)
        frequency = avg_gradient * 299792458 / (2 * math.pi)  # Convert to Hz
        
        return max(0.1, min(1e6, frequency))  # Clamp to reasonable range
    
    def _calculate_spatial_extent(self, coordinates: List[Tuple]) -> Tuple[int, int, int, int, int, int]:
        """Calculate 6D bounding box of coordinates."""
        if not coordinates:
            return (0, 0, 0, 0, 0, 0)
        
        coords_array = np.array(coordinates)
        min_coords = np.min(coords_array, axis=0)
        max_coords = np.max(coords_array, axis=0)
        
        extent = tuple(max_coords - min_coords)
        return extent if len(extent) == 6 else extent + (0,) * (6 - len(extent))


class ResonanceRecognitionSystem:
    """
    Main system for resonance recognition and pattern analysis.
    """
    
    def __init__(self):
        """Initialize the resonance recognition system."""
        self.detectors = {}
        self.patterns_detected = []
        self.events_triggered = []
        self.event_handlers = {}
        
        # Initialize default detectors
        self._initialize_detectors()
        
        # Statistics
        self.stats = {
            'total_detections': 0,
            'total_events': 0,
            'processing_time': 0.0,
            'detector_performance': {}
        }
    
    def _initialize_detectors(self):
        """Initialize default resonance detectors."""
        self.detectors[ResonanceType.HARMONIC] = HarmonicResonanceDetector(
            sensitivity=0.1, min_coherence=0.7
        )
        
        self.detectors[ResonanceType.COHERENT] = CoherentResonanceDetector(
            sensitivity=0.15, min_coherence=0.8
        )
    
    def add_detector(self, detector: ResonanceDetector):
        """Add a custom resonance detector."""
        self.detectors[detector.resonance_type] = detector
    
    def register_event_handler(self, resonance_type: ResonanceType, 
                             handler: Callable[[ResonancePattern], Any]):
        """
        Register an event handler for specific resonance types.
        
        Args:
            resonance_type: Type of resonance to handle
            handler: Function to call when pattern is detected
        """
        if resonance_type not in self.event_handlers:
            self.event_handlers[resonance_type] = []
        self.event_handlers[resonance_type].append(handler)
    
    def analyze_bitfield(self, bitfield: SparseBitfield, 
                        time_window: float = 1.0,
                        trigger_events: bool = True) -> List[ResonancePattern]:
        """
        Analyze bitfield for resonance patterns.
        
        Args:
            bitfield: Bitfield to analyze
            time_window: Time window for analysis
            trigger_events: Whether to trigger event handlers
        
        Returns:
            List of all detected resonance patterns
        """
        start_time = time.time()
        all_patterns = []
        
        # Run all detectors
        for resonance_type, detector in self.detectors.items():
            try:
                patterns = detector.detect(bitfield, time_window)
                all_patterns.extend(patterns)
                
                # Update detector performance stats
                self.stats['detector_performance'][resonance_type.value] = {
                    'patterns_found': len(patterns),
                    'processing_time': detector.stats['processing_time'],
                    'total_detections': detector.stats['detections']
                }
                
                # Trigger event handlers if enabled
                if trigger_events:
                    for pattern in patterns:
                        self._trigger_events(pattern)
                
            except Exception as e:
                print(f"Error in detector {resonance_type}: {e}")
                continue
        
        # Update global statistics
        self.stats['total_detections'] += len(all_patterns)
        self.stats['processing_time'] += time.time() - start_time
        
        # Store detected patterns
        self.patterns_detected.extend(all_patterns)
        
        # Keep only recent patterns (last 1000)
        if len(self.patterns_detected) > 1000:
            self.patterns_detected = self.patterns_detected[-1000:]
        
        return all_patterns
    
    def _trigger_events(self, pattern: ResonancePattern):
        """Trigger event handlers for a detected pattern."""
        handlers = self.event_handlers.get(pattern.resonance_type, [])
        
        for handler in handlers:
            try:
                result = handler(pattern)
                
                event = ResonanceEvent(
                    event_id=f"event_{int(time.time()*1000)}_{len(self.events_triggered)}",
                    pattern=pattern,
                    trigger_time=time.time(),
                    action_taken=handler.__name__,
                    result=result,
                    metadata={'handler_type': type(handler).__name__}
                )
                
                self.events_triggered.append(event)
                self.stats['total_events'] += 1
                
            except Exception as e:
                print(f"Error in event handler {handler.__name__}: {e}")
    
    def get_recent_patterns(self, count: int = 10, 
                          resonance_type: Optional[ResonanceType] = None) -> List[ResonancePattern]:
        """Get recent resonance patterns."""
        patterns = self.patterns_detected
        
        if resonance_type:
            patterns = [p for p in patterns if p.resonance_type == resonance_type]
        
        return patterns[-count:] if patterns else []
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pattern statistics."""
        if not self.patterns_detected:
            return {'total_patterns': 0}
        
        # Group by resonance type
        type_counts = defaultdict(int)
        type_coherences = defaultdict(list)
        type_frequencies = defaultdict(list)
        
        for pattern in self.patterns_detected:
            type_counts[pattern.resonance_type.value] += 1
            type_coherences[pattern.resonance_type.value].append(pattern.coherence)
            type_frequencies[pattern.resonance_type.value].append(pattern.frequency)
        
        # Calculate statistics
        stats = {
            'total_patterns': len(self.patterns_detected),
            'patterns_by_type': dict(type_counts),
            'average_coherence_by_type': {
                rtype: np.mean(coherences) 
                for rtype, coherences in type_coherences.items()
            },
            'frequency_ranges_by_type': {
                rtype: (min(freqs), max(freqs)) 
                for rtype, freqs in type_frequencies.items() if freqs
            },
            'system_stats': self.stats.copy()
        }
        
        return stats
    
    def clear_history(self):
        """Clear pattern and event history."""
        self.patterns_detected.clear()
        self.events_triggered.clear()
        
        # Reset detector statistics
        for detector in self.detectors.values():
            detector.stats = {
                'detections': 0,
                'false_positives': 0,
                'processing_time': 0.0
            }
            detector.detection_history.clear()


# Factory function
def create_resonance_system() -> ResonanceRecognitionSystem:
    """Create a complete resonance recognition system."""
    return ResonanceRecognitionSystem()


# Example event handlers
def harmonic_resonance_handler(pattern: ResonancePattern) -> str:
    """Example handler for harmonic resonance patterns."""
    return f"Detected harmonic at {pattern.frequency:.2f} Hz with coherence {pattern.coherence:.3f}"


def coherent_resonance_handler(pattern: ResonancePattern) -> str:
    """Example handler for coherent resonance patterns."""
    return f"Detected coherent pattern with {len(pattern.offbits)} OffBits, coherence {pattern.coherence:.3f}"


if __name__ == "__main__":
    # Test the resonance recognition system
    print("Testing Resonance Recognition System...")
    
    # Create resonance system
    resonance_system = create_resonance_system()
    
    # Register event handlers
    resonance_system.register_event_handler(ResonanceType.HARMONIC, harmonic_resonance_handler)
    resonance_system.register_event_handler(ResonanceType.COHERENT, coherent_resonance_handler)
    
    print(f"Created resonance system with {len(resonance_system.detectors)} detectors")
    
    # Create test bitfield with patterns
    from .bitfield import create_desktop_bitfield
    from .offbit import create_quantum_offbit, create_electromagnetic_offbit
    
    bitfield = create_desktop_bitfield()
    
    # Add OffBits in a pattern that should create resonance
    for i in range(20):
        # Create a harmonic pattern
        x = int(50 + 20 * math.sin(i * 0.5))
        y = int(50 + 20 * math.cos(i * 0.5))
        z = int(50 + 10 * math.sin(i * 0.3))
        coord = (x, y, z, 1, 0, 1)
        
        # Vary OffBit properties harmonically
        reality = int(128 + 64 * math.sin(i * 0.2))
        info = int(128 + 64 * math.cos(i * 0.2))
        activation = int(128 + 32 * math.sin(i * 0.4))
        
        offbit = create_quantum_offbit(reality, info, activation)
        bitfield.set_offbit(coord, offbit)
    
    print(f"Created test bitfield with {bitfield.active_count} OffBits in harmonic pattern")
    
    # Analyze for resonance patterns
    patterns = resonance_system.analyze_bitfield(bitfield, time_window=2.0)
    
    print(f"\nDetected {len(patterns)} resonance patterns:")
    for pattern in patterns:
        print(f"  {pattern.resonance_type.value}:")
        print(f"    Frequency: {pattern.frequency:.2f} Hz")
        print(f"    Coherence: {pattern.coherence:.3f}")
        print(f"    Confidence: {pattern.confidence:.3f}")
        print(f"    OffBits involved: {len(pattern.offbits)}")
    
    # Show events triggered
    print(f"\nEvents triggered: {len(resonance_system.events_triggered)}")
    for event in resonance_system.events_triggered:
        print(f"  {event.action_taken}: {event.result}")
    
    # Show statistics
    stats = resonance_system.get_pattern_statistics()
    print(f"\nResonance System Statistics:")
    print(f"  Total patterns detected: {stats['total_patterns']}")
    print(f"  Patterns by type: {stats['patterns_by_type']}")
    print(f"  System processing time: {stats['system_stats']['processing_time']:.4f}s")
    
    print("\nResonance Recognition System test completed successfully!")

