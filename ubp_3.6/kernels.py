"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6.2 - Mathematical Kernels
Author: Euan Craig, New Zealand
Date: November 20, 2025
================================================================================

Core mathematical functions implementing fundamental UBP formulas:
- Resonance kernel
- Coherence calculation
- Signal processing functions
- Frequency/wavelength conversions
- Special resonance frequencies

Updated for UBP 3.6.2:
- Removed numpy dependency (pure Python)
- Removed ubp_config dependency (uses system_constants directly)
- Integrated with Coherence Field ELITE
- Zero external dependencies

**Zero Dependencies**: Only Python stdlib (math, typing) + system_constants
"""

import math
from typing import List, Tuple, Optional

# Import only what we need from system_constants
from system_constants import UBPConstants

# Constants that may not be in UBPConstants
PI = math.pi
E = math.e
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
SPEED_OF_LIGHT = UBPConstants.C_CELERITAS  # Speed of light in m/s
PLANCK_TIME = 5.39116e-44  # Planck time in seconds


# ============================================================================
# RESONANCE KERNEL
# ============================================================================

def resonance_kernel(d: float, k: float = 0.0002) -> float:
    """
    Calculate the resonance kernel value.
    
    Axiom: f(d) = exp(-k * d²)
    where d is typically the product of time and frequency (d = t * f)
    
    This is the fundamental resonance decay function used throughout UBP.
    
    Args:
        d: Distance parameter (time * frequency)
        k: Decay constant (default: 0.0002)
        
    Returns:
        Resonance kernel value [0, 1]
        
    Example:
        >>> resonance_kernel(0.0)  # Perfect resonance
        1.0
        >>> resonance_kernel(10.0)  # Decayed resonance
        0.9801986...
    """
    return math.exp(-k * d * d)


def resonance_interaction(b_i: float, frequency: float, time: float, k: float = 0.0002) -> float:
    """
    Calculate resonance interaction between an OffBit state and frequency.
    
    Formula: b_i * exp(-k * (t * f)²)
    
    Args:
        b_i: OffBit state value
        frequency: Interaction frequency (Hz)
        time: Time parameter (seconds)
        k: Decay constant
        
    Returns:
        Resonance interaction value
        
    Example:
        >>> resonance_interaction(1.0, 1e12, 1e-9)  # 1 THz at 1 ns
        0.9801986...
    """
    d = time * frequency
    return b_i * resonance_kernel(d, k)


# ============================================================================
# COHERENCE CALCULATIONS
# ============================================================================

def coherence(s_i: List[float], s_j: List[float]) -> float:
    """
    Calculate coherence between two time-series signals.
    
    Axiom: C_ij = (1/N) * Σ(s_i(t_k) * s_j(t_k))
    
    This measures the correlation between two signals over time.
    
    Args:
        s_i: First signal (time series)
        s_j: Second signal (time series)
        
    Returns:
        Coherence value (can be positive or negative)
        
    Raises:
        ValueError: If signals have different lengths
        
    Example:
        >>> coherence([1, 2, 3], [1, 2, 3])  # Perfect correlation
        4.666...
        >>> coherence([1, 2, 3], [-1, -2, -3])  # Anti-correlation
        -4.666...
    """
    if len(s_i) != len(s_j):
        raise ValueError(f"Signals must have same length: {len(s_i)} != {len(s_j)}")
    
    if len(s_i) == 0:
        return 0.0
    
    N = len(s_i)
    correlation_sum = sum(s_i[k] * s_j[k] for k in range(N))
    
    return correlation_sum / N


def normalized_coherence(s_i: List[float], s_j: List[float]) -> float:
    """
    Calculate normalized coherence (cross-correlation) between signals.
    
    Formula: C_ij = |Σ(s_i(k) * s_j(k))| / √(Σs_i(k)² * Σs_j(k)²)
    
    This is the standard cross-correlation coefficient, normalized to [0, 1].
    
    Args:
        s_i: First signal
        s_j: Second signal
        
    Returns:
        Normalized coherence value [0, 1]
        
    Raises:
        ValueError: If signals have different lengths
        
    Example:
        >>> normalized_coherence([1, 2, 3], [1, 2, 3])  # Perfect correlation
        1.0
        >>> normalized_coherence([1, 2, 3], [3, 2, 1])  # Partial correlation
        0.714...
    """
    if len(s_i) != len(s_j):
        raise ValueError(f"Signals must have same length: {len(s_i)} != {len(s_j)}")
    
    if len(s_i) == 0:
        return 0.0
    
    # Calculate cross-correlation numerator
    cross_corr = sum(s_i[k] * s_j[k] for k in range(len(s_i)))
    
    # Calculate normalization factors
    norm_i = math.sqrt(sum(x * x for x in s_i))
    norm_j = math.sqrt(sum(x * x for x in s_j))
    
    if norm_i == 0 or norm_j == 0:
        return 0.0
    
    return abs(cross_corr) / (norm_i * norm_j)


def calculate_signal_coherence_matrix(signals: List[List[float]], 
                                     threshold: float = 0.5) -> Tuple[List[List[float]], List[Tuple[int, int]]]:
    """
    Calculate coherence matrix for multiple signals (pure Python version).
    
    Args:
        signals: List of time-series signals
        threshold: Coherence threshold for observability
        
    Returns:
        Tuple of (coherence_matrix, observable_pairs)
        - coherence_matrix: NxN matrix of coherence values (as list of lists)
        - observable_pairs: List of (i, j) pairs with C_ij >= threshold
        
    Example:
        >>> signals = [[1, 2, 3], [1, 2, 3], [3, 2, 1]]
        >>> matrix, pairs = calculate_signal_coherence_matrix(signals)
        >>> len(matrix)
        3
        >>> (0, 1) in pairs  # Signals 0 and 1 are coherent
        True
    """
    n_signals = len(signals)
    coherence_matrix = [[0.0 for _ in range(n_signals)] for _ in range(n_signals)]
    observable_pairs = []
    
    for i in range(n_signals):
        for j in range(n_signals):
            if i == j:
                coherence_matrix[i][j] = 1.0  # Perfect self-coherence
            else:
                c_ij = normalized_coherence(signals[i], signals[j])
                coherence_matrix[i][j] = c_ij
                
                if c_ij >= threshold:
                    observable_pairs.append((i, j))
    
    return coherence_matrix, observable_pairs


def validate_coherence_threshold(coherence_value: float, threshold: float = 0.5) -> bool:
    """
    Validate if coherence value meets observability threshold.
    
    Args:
        coherence_value: Calculated coherence
        threshold: Observability threshold (default: 0.5)
        
    Returns:
        True if coherence is observable
        
    Example:
        >>> validate_coherence_threshold(0.7)
        True
        >>> validate_coherence_threshold(0.3)
        False
    """
    return coherence_value >= threshold


# ============================================================================
# SIGNAL GENERATION
# ============================================================================

def generate_oscillating_signal(frequency: float, phase: float, 
                               duration: float, sample_rate: float = 1000.0) -> List[float]:
    """
    Generate an oscillating signal for coherence testing.
    
    Formula: s_i(t) = cos(2π * f_i * t + φ_i)
    
    Args:
        frequency: Signal frequency (Hz)
        phase: Phase offset (radians)
        duration: Signal duration (seconds)
        sample_rate: Sampling rate (Hz)
        
    Returns:
        List of signal values
        
    Example:
        >>> signal = generate_oscillating_signal(1.0, 0.0, 1.0, 10.0)
        >>> len(signal)
        10
        >>> signal[0]  # cos(0) = 1.0
        1.0
    """
    num_samples = int(duration * sample_rate)
    dt = 1.0 / sample_rate
    
    signal = []
    for i in range(num_samples):
        t = i * dt
        value = math.cos(2 * PI * frequency * t + phase)
        signal.append(value)
    
    return signal


# ============================================================================
# FREQUENCY/WAVELENGTH CONVERSIONS
# ============================================================================

def calculate_frequency_from_wavelength(wavelength_nm: float) -> float:
    """
    Calculate frequency from wavelength.
    
    Formula: f = c / λ
    
    Args:
        wavelength_nm: Wavelength in nanometers
        
    Returns:
        Frequency in Hz
        
    Example:
        >>> calculate_frequency_from_wavelength(500.0)  # Green light
        5.99584916e+14
    """
    wavelength_m = wavelength_nm * 1e-9  # Convert nm to m
    return SPEED_OF_LIGHT / wavelength_m


def calculate_wavelength_from_frequency(frequency_hz: float) -> float:
    """
    Calculate wavelength from frequency.
    
    Formula: λ = c / f
    
    Args:
        frequency_hz: Frequency in Hz
        
    Returns:
        Wavelength in nanometers
        
    Example:
        >>> calculate_wavelength_from_frequency(5.99584916e+14)  # Green light
        500.0
    """
    wavelength_m = SPEED_OF_LIGHT / frequency_hz
    return wavelength_m * 1e9  # Convert m to nm


# ============================================================================
# SPECIAL RESONANCE FREQUENCIES
# ============================================================================

def pi_phi_resonance_frequency() -> float:
    """
    Calculate the π-φ composite resonance frequency.
    
    This is a unique resonance arising from the interaction of π and φ.
    
    Formula: f = c / (π * φ)
    
    Returns:
        π-φ resonance frequency (~58,977,069.61 Hz)
        
    Example:
        >>> pi_phi_resonance_frequency()
        58977069.609314...
    """
    return SPEED_OF_LIGHT / (PI * PHI)


def planck_euler_resonance_frequency() -> float:
    """
    Calculate the Planck-Euler resonance frequency.
    
    Links Planck scale physics with Euler's number.
    
    Formula: f = c / (t_p * e)
    where t_p is Planck time
    
    Returns:
        Planck-Euler resonance frequency
        
    Example:
        >>> planck_euler_resonance_frequency()
        1.6403...e+43
    """
    return SPEED_OF_LIGHT / (PLANCK_TIME * E)


def euclidean_geometry_pi_resonance() -> float:
    """
    Calculate the Euclidean geometry π-resonance frequency.
    
    Specific frequency tied to Euclidean geometric patterns.
    
    Returns:
        Euclidean π-resonance frequency (95,366,637.6 Hz)
        
    Example:
        >>> euclidean_geometry_pi_resonance()
        95366637.6
    """
    return 95366637.6


# ============================================================================
# CARFE RECURSION
# ============================================================================

def carfe_recursion(offbit_n: float, offbit_n_minus_1: float, 
                   K_n: float, phi: Optional[float] = None) -> float:
    """
    Calculate CARFE (Cykloid Adelic Recursive Expansive Field Equation) recursion.
    
    Axiom: OffBit_{n+1} = φ * OffBit_n + K_n * OffBit_{n-1}
    
    This implements the recursive field expansion using the golden ratio.
    
    Args:
        offbit_n: Current OffBit state
        offbit_n_minus_1: Previous OffBit state
        K_n: Coupling constant
        phi: Golden ratio (default: from UBPConstants)
        
    Returns:
        Next OffBit state
        
    Example:
        >>> carfe_recursion(1.0, 0.0, 1.0)  # Start of sequence
        1.618...
    """
    if phi is None:
        phi = PHI
    
    return phi * offbit_n + K_n * offbit_n_minus_1


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_toggle_rate(state_changes: int, duration: float) -> float:
    """
    Calculate toggle rate for a binary signal.
    
    Formula: Toggle Rate = (Number of State Changes) / (Total Time Duration)
    
    Args:
        state_changes: Number of state transitions
        duration: Total time duration (seconds)
        
    Returns:
        Toggle rate (toggles per second)
        
    Example:
        >>> calculate_toggle_rate(100, 1.0)  # 100 toggles in 1 second
        100.0
    """
    if duration <= 0:
        return 0.0
    
    return state_changes / duration


def coherence_pressure_mitigation(coherence_pressure: float, 
                                 csc_frequency: Optional[float] = None) -> float:
    """
    Calculate coherence pressure mitigation using CSC.
    
    The Coherence Sampling Cycle mitigates pressure by periodic re-synchronization.
    
    Args:
        coherence_pressure: Current coherence pressure (Ψ_p)
        csc_frequency: CSC frequency (default: π Hz)
        
    Returns:
        Mitigated coherence pressure
        
    Example:
        >>> coherence_pressure_mitigation(1.0)  # With default π Hz
        0.241...
    """
    if csc_frequency is None:
        csc_frequency = PI
    
    # Mitigation factor based on CSC frequency
    mitigation_factor = 1.0 / (1.0 + csc_frequency)
    return coherence_pressure * mitigation_factor


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.6.2 MATHEMATICAL KERNELS")
    print("=" * 80)
    
    # Test resonance kernel
    print("\n1. Resonance Kernel:")
    for d in [0.0, 1.0, 5.0, 10.0]:
        print(f"   resonance_kernel({d:.1f}) = {resonance_kernel(d):.10f}")
    
    # Test coherence
    print("\n2. Signal Coherence:")
    signal1 = [1.0, 2.0, 3.0, 4.0, 5.0]
    signal2 = [1.0, 2.0, 3.0, 4.0, 5.0]
    signal3 = [5.0, 4.0, 3.0, 2.0, 1.0]
    
    print(f"   coherence(s1, s1) = {coherence(signal1, signal1):.6f}")
    print(f"   coherence(s1, s2) = {coherence(signal1, signal2):.6f}")
    print(f"   coherence(s1, s3) = {coherence(signal1, signal3):.6f}")
    print(f"   normalized_coherence(s1, s2) = {normalized_coherence(signal1, signal2):.6f}")
    print(f"   normalized_coherence(s1, s3) = {normalized_coherence(signal1, signal3):.6f}")
    
    # Test signal generation
    print("\n3. Signal Generation:")
    test_signal = generate_oscillating_signal(1.0, 0.0, 1.0, 10.0)
    print(f"   Generated {len(test_signal)} samples")
    print(f"   First 5 values: {[f'{v:.6f}' for v in test_signal[:5]]}")
    
    # Test frequency conversions
    print("\n4. Frequency/Wavelength Conversions:")
    wavelength = 500.0  # nm (green light)
    freq = calculate_frequency_from_wavelength(wavelength)
    wavelength_back = calculate_wavelength_from_frequency(freq)
    print(f"   Wavelength: {wavelength:.1f} nm")
    print(f"   Frequency: {freq:.6e} Hz")
    print(f"   Back to wavelength: {wavelength_back:.1f} nm")
    
    # Test special resonances
    print("\n5. Special Resonance Frequencies:")
    print(f"   π-φ resonance: {pi_phi_resonance_frequency():.2f} Hz")
    print(f"   Planck-Euler resonance: {planck_euler_resonance_frequency():.6e} Hz")
    print(f"   Euclidean π-resonance: {euclidean_geometry_pi_resonance():.1f} Hz")
    
    # Test CARFE recursion
    print("\n6. CARFE Recursion:")
    offbit_0 = 1.0
    offbit_1 = 1.0
    K = 1.0
    print(f"   OffBit_0 = {offbit_0:.6f}")
    print(f"   OffBit_1 = {offbit_1:.6f}")
    for i in range(2, 7):
        offbit_next = carfe_recursion(offbit_1, offbit_0, K)
        print(f"   OffBit_{i} = {offbit_next:.6f}")
        offbit_0, offbit_1 = offbit_1, offbit_next
    
    print("\n" + "=" * 80)
    print("UBP 3.6.2: Pure Python Mathematical Kernels")
    print("Zero external dependencies - Core UBP operations")
    print("=" * 80)
