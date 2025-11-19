"""\n================================================================================\nUniversal Binary Principle (UBP) Framework v3.6 - State Management\nAuthor: Euan Craig, New Zealand\nDate: November 20, 2025 (Updated with Resonance History Tracking)\n================================================================================\n\nUBP State management with coherence-native OffBits and resonance history.\n\n**Paradigm Shift in 3.5**:\nOffBits now carry their own coherence state. Every bit operation maintains\ncoherence tracking, making state management inherently coherence-aware.\n\n**Enhancement in 3.6**:\nOffBits now track resonance history - a temporal record of (time, frequency,\nresonance_factor) tuples. This enables continuous coherence analysis and\nintegration with Coherence Field ELITE's resonance detector for pattern\ndetection, optimization, and prediction.\n\n**Zero Dependencies**: Only Python stdlib + coherence_substrate\n"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from coherence_substrate import CoherenceState, NRCI_TARGET


# ============================================================================
# OFFBIT - Coherence-Native 24-bit State
# ============================================================================

@dataclass(frozen=True)
class OffBit:
    """
    Immutable 24-bit UBP OffBit with intrinsic coherence and resonance history.
    
    In 3.6, OffBits aren't just bit patterns - they're coherence states
    that happen to have a 24-bit representation, with full temporal tracking
    of resonance evolution for continuous coherence analysis.
    
    Resonance history enables integration with Coherence Field ELITE's
    resonance detector for pattern detection and optimization.
    """
    value: int  # 24-bit value (0 to 0xFFFFFF)
    coherence: CoherenceState = None
    resonance_history: Tuple[Tuple[float, float, float], ...] = ()  # (time, frequency, resonance_factor)
    
    def __post_init__(self):
        # Ensure value is within 24-bit range
        if not (0 <= self.value <= 0xFFFFFF):
            object.__setattr__(self, 'value', self.value & 0xFFFFFF)
        
        # Initialize coherence if not provided
        if self.coherence is None:
            object.__setattr__(self, 'coherence', CoherenceState(
                float(self.value),
                log_nrci_error=math.log(1 - NRCI_TARGET)
            ))
    
    @property
    def layer(self) -> int:
        """Get the 24-bit layer value."""
        return self.value & 0xFFFFFF
    
    @property
    def bits(self) -> List[int]:
        """Get individual bits as a list."""
        return [(self.value >> i) & 1 for i in range(24)]
    
    @property
    def active_bits(self) -> int:
        """Count of active (1) bits."""
        return bin(self.value).count('1')
    
    @property
    def is_active(self) -> bool:
        """Check if OffBit has any active bits."""
        return self.value > 0
    
    @property
    def nrci(self) -> float:
        """Get NRCI of this OffBit."""
        return self.coherence.nrci
    
    @property
    def has_resonance_history(self) -> bool:
        """Check if this OffBit has resonance history."""
        return len(self.resonance_history) > 0
    
    @property
    def resonance_history_length(self) -> int:
        """Get length of resonance history."""
        return len(self.resonance_history)
    
    def get_resonance_statistics(self) -> Dict[str, Any]:
        """
        Get basic statistics from resonance history.
        
        Returns:
            Dictionary with resonance statistics
        """
        if not self.resonance_history:
            return {
                'history_length': 0,
                'time_range': (0, 0),
                'frequency_range': (0, 0),
                'avg_resonance_factor': 0,
                'min_resonance_factor': 0,
                'max_resonance_factor': 0
            }
        
        times = [t for t, _, _ in self.resonance_history]
        frequencies = [f for _, f, _ in self.resonance_history]
        factors = [rf for _, _, rf in self.resonance_history]
        
        return {
            'history_length': len(self.resonance_history),
            'time_range': (min(times), max(times)),
            'frequency_range': (min(frequencies), max(frequencies)),
            'avg_resonance_factor': sum(factors) / len(factors),
            'min_resonance_factor': min(factors),
            'max_resonance_factor': max(factors)
        }
    
    def add_resonance_record(self, time: float, frequency: float, 
                           resonance_factor: float, 
                           max_history: int = 1000) -> 'OffBit':
        """
        Add a resonance record to history with size management.
        
        Creates a new OffBit with the resonance record appended to history.
        Automatically maintains history size limit by keeping most recent entries.
        
        Args:
            time: Time parameter
            frequency: Resonance frequency
            resonance_factor: Resonance factor (0 to 1)
            max_history: Maximum history entries to keep (default 1000)
            
        Returns:
            New OffBit with updated resonance history
            
        Example:
            >>> b = OffBit(0x123456)
            >>> b = b.add_resonance_record(1e-9, 1e9, 0.999)
            >>> print(b.resonance_history_length)  # 1
        """
        # Create new entry
        new_entry = (time, frequency, resonance_factor)
        
        # Append to history
        new_history = self.resonance_history + (new_entry,)
        
        # Maintain size limit (keep most recent)
        if len(new_history) > max_history:
            new_history = new_history[-max_history:]
        
        # Return new OffBit with updated history
        return OffBit(self.value, self.coherence, new_history)
    
    def detect_perception_reset_points(self, threshold: float = 0.95) -> List[int]:
        """
        Identify points where resonance factor dropped below threshold.
        
        These points represent potential perception resets - moments where
        coherence degraded significantly and may have triggered a reset.
        In the 4π/3 resonance simulations, these correspond to coherence
        valleys that mark natural perception reset boundaries.
        
        Args:
            threshold: Resonance factor threshold (default 0.95)
                      Points below this are considered reset candidates
            
        Returns:
            List of indices in resonance_history where factor < threshold
            
        Example:
            >>> b = OffBit(0x123456)
            >>> # ... apply resonance toggles ...
            >>> reset_points = b.detect_perception_reset_points(threshold=0.95)
            >>> print(f"Found {len(reset_points)} potential reset points")
            >>> for idx in reset_points:
            ...     time, freq, factor = b.resonance_history[idx]
            ...     print(f"  Reset at t={time:.9f}s, factor={factor:.6f}")
        """
        if not self.resonance_history:
            return []
        
        reset_points = []
        for i, (time, frequency, resonance_factor) in enumerate(self.resonance_history):
            if resonance_factor < threshold:
                reset_points.append(i)
        
        return reset_points
    
    def get_coherence_valleys(self, window_size: int = 5) -> List[Tuple[int, float]]:
        """
        Identify coherence valleys in resonance history.
        
        A valley is a local minimum in resonance factors - a point where
        coherence dipped below surrounding values. These often correspond
        to perception reset points or decoherence events.
        
        Args:
            window_size: Size of window for local minimum detection (default 5)
            
        Returns:
            List of (index, resonance_factor) tuples for valley points
            
        Example:
            >>> b = OffBit(0x123456)
            >>> # ... apply resonance toggles ...
            >>> valleys = b.get_coherence_valleys(window_size=5)
            >>> print(f"Found {len(valleys)} coherence valleys")
            >>> for idx, factor in valleys:
            ...     time, freq, _ = b.resonance_history[idx]
            ...     print(f"  Valley at t={time:.9f}s, factor={factor:.6f}")
        """
        if len(self.resonance_history) < window_size:
            return []
        
        factors = [rf for _, _, rf in self.resonance_history]
        valleys = []
        
        half_window = window_size // 2
        
        for i in range(half_window, len(factors) - half_window):
            # Check if this is a local minimum
            current = factors[i]
            window = factors[i - half_window:i + half_window + 1]
            
            if current == min(window):
                valleys.append((i, current))
        
        return valleys
    
    def to_coherence_states(self) -> List[CoherenceState]:
        """
        Convert resonance history to CoherenceState sequence.
        
        This is the primary integration point with Coherence Field ELITE.
        Each history entry is converted to a CoherenceState that encodes
        the time-frequency relationship and resonance factor.
        
        Returns:
            List of CoherenceState objects representing coherence evolution
            
        Example:
            >>> b = OffBit(0x123456)
            >>> # ... apply resonance toggles ...
            >>> states = b.to_coherence_states()
            >>> # Now use with Coherence Field ELITE
            >>> import coherence_field as cf
            >>> detector = cf.ResonanceDetector()
            >>> resonance = detector.detect_resonance(states)
        """
        if not self.resonance_history:
            return []
        
        states = []
        for time, frequency, resonance_factor in self.resonance_history:
            # Encode time-frequency relationship as state value
            value = time * frequency
            
            # Map resonance_factor to NRCI degradation
            # resonance_factor = 1.0 means perfect resonance (no degradation)
            # resonance_factor = 0.0 means complete decoherence
            degradation = 1.0 - resonance_factor
            
            # Convert to log_nrci_error
            nrci = NRCI_TARGET * (1.0 - degradation)
            log_error = math.log(1.0 - nrci) if nrci < 1.0 else -1e10
            
            state = CoherenceState(value, log_nrci_error=log_error)
            states.append(state)
        
        return states
    
    def analyze_with_coherence_field(self) -> Optional[Dict[str, Any]]:
        """
        Analyze resonance history using Coherence Field ELITE.
        
        This is a convenience method that automatically converts history
        to CoherenceState sequence and runs resonance detection.
        
        Returns:
            Dictionary with analysis results, or None if Coherence Field unavailable
            
        Example:
            >>> b = OffBit(0x123456)
            >>> # ... apply resonance toggles ...
            >>> analysis = b.analyze_with_coherence_field()
            >>> if analysis and analysis.get('resonance'):
            ...     res = analysis['resonance']
            ...     print(f"Detected {res.p}/{res.q} resonance")
        """
        if not self.resonance_history:
            return {'error': 'No resonance history'}
        
        try:
            import coherence_field as cf
            
            # Convert to states
            states = self.to_coherence_states()
            
            # Detect resonance
            detector = cf.ResonanceDetector()
            resonance = detector.detect_resonance(states)
            
            # Get statistics
            stats = self.get_resonance_statistics()
            
            # Build result
            result = {
                'resonance': resonance,
                'history_length': stats['history_length'],
                'time_range': stats['time_range'],
                'frequency_range': stats['frequency_range'],
                'avg_resonance_factor': stats['avg_resonance_factor'],
                'min_resonance_factor': stats['min_resonance_factor'],
                'max_resonance_factor': stats['max_resonance_factor'],
                'coherence_states': states
            }
            
            # Add resonance details if detected
            if resonance:
                result['resonance_detected'] = True
                result['resonance_p'] = resonance.p
                result['resonance_q'] = resonance.q
                result['resonance_confidence'] = resonance.confidence
            else:
                result['resonance_detected'] = False
            
            return result
            
        except ImportError:
            return None
    
    def toggle(self) -> 'OffBit':
        """
        Create a new OffBit with toggled state.
        
        Toggling is a coherence transformation - it applies Y-refinement.
        Preserves resonance history.
        
        Returns:
            New OffBit with inverted bits and refined coherence
        """
        new_value = self.value ^ 0xFFFFFF
        new_coherence = self.coherence.refine_forward()
        return OffBit(new_value, new_coherence, self.resonance_history)
    
    def toggle_bit(self, position: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit toggled.
        
        Args:
            position: Bit position to toggle (0-23)
        
        Returns:
            New OffBit with specified bit toggled
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        new_value = self.value ^ (1 << position)
        # Small toggle = small coherence change
        new_coherence = self.coherence.degrade_by(1e-8)
        return OffBit(new_value, new_coherence, self.resonance_history)
    
    def get_bit(self, position: int) -> int:
        """
        Get the value of a specific bit.
        
        Args:
            position: Bit position (0-23)
        
        Returns:
            Bit value (0 or 1)
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        return (self.value >> position) & 1
    
    def set_bit(self, position: int, bit_value: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit set.
        
        Args:
            position: Bit position (0-23)
            bit_value: Bit value (0 or 1)
        
        Returns:
            New OffBit with specified bit set
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        if bit_value not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1, got {bit_value}")
        
        if bit_value == 1:
            new_value = self.value | (1 << position)
        else:
            new_value = self.value & ~(1 << position)
        
        new_coherence = self.coherence.degrade_by(1e-8)
        return OffBit(new_value, new_coherence, self.resonance_history)
    
    def extract_data(self) -> int:
        """
        Extract 24-bit data.
        
        Returns:
            24-bit data value
        """
        return self.layer
    
    def __str__(self) -> str:
        return f"OffBit(0x{self.value:06X}, NRCI={self.nrci:.6f})"
    
    def __repr__(self) -> str:
        return f"OffBit(value={self.value}, layer=0x{self.layer:06X}, active_bits={self.active_bits}, nrci={self.nrci:.10f})"


# ============================================================================
# BITFIELD - Collection of Coherent OffBits
# ============================================================================

class MutableBitfield:
    """
    Mutable bitfield for UBP operations with coherence tracking.
    
    In 3.5, a bitfield isn't just a collection of bits - it's a
    coherence ensemble where collective coherence emerges.
    """
    
    def __init__(self, size: int = 1000):
        """
        Initialize mutable bitfield.
        
        Args:
            size: Number of OffBits to store
        """
        self.size = size
        self.offbits: List[OffBit] = [OffBit(0) for _ in range(size)]
        self._modification_count = 0
    
    def get(self, index: int) -> OffBit:
        """Get OffBit at index."""
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        return self.offbits[index]
    
    def set(self, index: int, offbit: OffBit):
        """Set OffBit at index."""
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        self.offbits[index] = offbit
        self._modification_count += 1
    
    def toggle(self, index: int):
        """Toggle OffBit at index."""
        self.offbits[index] = self.offbits[index].toggle()
        self._modification_count += 1
    
    def get_collective_coherence(self) -> CoherenceState:
        """
        Get collective coherence of the entire bitfield.
        
        Returns:
            CoherenceState representing ensemble coherence
        """
        if not self.offbits:
            return CoherenceState(0.0)
        
        # Average coherence across all OffBits
        total_value = sum(ob.coherence.value for ob in self.offbits)
        avg_value = total_value / len(self.offbits)
        
        total_log_error = sum(ob.coherence.log_nrci_error for ob in self.offbits)
        avg_log_error = total_log_error / len(self.offbits)
        
        return CoherenceState(avg_value, log_nrci_error=avg_log_error)
    
    def get_active_count(self) -> int:
        """Count of active OffBits."""
        return sum(1 for ob in self.offbits if ob.is_active)
    
    def get_total_active_bits(self) -> int:
        """Total count of active bits across all OffBits."""
        return sum(ob.active_bits for ob in self.offbits)
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        collective = self.get_collective_coherence()
        return f"MutableBitfield(size={self.size}, active={self.get_active_count()}, nrci={collective.nrci:.6f})"


# ============================================================================
# UBP STATE - Complete System State
# ============================================================================

@dataclass
class UBPState:
    """
    Complete UBP system state with coherence tracking.
    
    In 3.5, system state is fundamentally a coherence configuration.
    """
    bitfield: MutableBitfield
    timestamp: float
    metadata: Dict[str, Any]
    
    @classmethod
    def create(cls, size: int = 1000, **metadata) -> 'UBPState':
        """
        Create a new UBPState.
        
        Args:
            size: Bitfield size
            **metadata: Additional metadata
        
        Returns:
            New UBPState
        """
        import time
        return cls(
            bitfield=MutableBitfield(size),
            timestamp=time.time(),
            metadata=metadata
        )
    
    def get_system_coherence(self) -> CoherenceState:
        """Get overall system coherence."""
        return self.bitfield.get_collective_coherence()
    
    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get summary of system state.
        
        Returns:
            Dictionary with state statistics
        """
        coherence = self.get_system_coherence()
        
        return {
            'bitfield_size': self.bitfield.size,
            'active_offbits': self.bitfield.get_active_count(),
            'total_active_bits': self.bitfield.get_total_active_bits(),
            'system_nrci': coherence.nrci,
            'system_value': coherence.value,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    def __str__(self) -> str:
        coherence = self.get_system_coherence()
        return f"UBPState(size={self.bitfield.size}, nrci={coherence.nrci:.6f})"


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 STATE MANAGEMENT - Coherence-Native OffBits")
    print("=" * 80)
    
    # Create OffBit
    print("\n1. Creating OffBit:")
    offbit = OffBit(0x123456)
    print(f"   {offbit}")
    print(f"   Active bits: {offbit.active_bits}")
    print(f"   NRCI: {offbit.nrci:.10f}")
    
    # Toggle operations
    print("\n2. Toggle Operations:")
    toggled = offbit.toggle()
    print(f"   Original: {offbit}")
    print(f"   Toggled:  {toggled}")
    print(f"   NRCI change: {toggled.nrci - offbit.nrci:.10f}")
    
    # Bit operations
    print("\n3. Bit Operations:")
    bit_toggled = offbit.toggle_bit(5)
    print(f"   Bit 5 toggled: {bit_toggled}")
    print(f"   Bit 5 value: {bit_toggled.get_bit(5)}")
    
    # Bitfield
    print("\n4. Mutable Bitfield:")
    bitfield = MutableBitfield(size=100)
    for i in range(10):
        bitfield.set(i, OffBit(i * 0x1000))
    
    collective = bitfield.get_collective_coherence()
    print(f"   {bitfield}")
    print(f"   Collective NRCI: {collective.nrci:.10f}")
    print(f"   Active OffBits: {bitfield.get_active_count()}")
    
    # UBP State
    print("\n5. UBP System State:")
    state = UBPState.create(size=1000, realm='quantum', experiment='test')
    summary = state.get_state_summary()
    print(f"   {state}")
    print(f"   Summary: {summary}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: OffBits are Coherence States")
    print("Zero external dependencies - Pure coherence")
    print("=" * 80)
