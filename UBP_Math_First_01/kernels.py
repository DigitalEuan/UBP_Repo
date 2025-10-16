"""
UBP Mathematical Kernels

Core mathematical functions implementing the fundamental UBP formulas:
- Resonance kernel
- Coherence calculation
- Global Coherence Invariant
- Signal processing functions
"""

import math
import numpy as np
from typing import List, Union, Tuple
from .constants import PI, CSC_TIME, get_frequency_weights


def resonance_kernel(d: float, k: float = 0.0002) -> float:
    """
    Calculate the resonance kernel value.
    
    Axiom: f(d) = exp(-k * d²)
    where d is typically the product of time and frequency (d = t * f)
    
    Args:
        d: Distance parameter (time * frequency)
        k: Decay constant (default: 0.0002)
        
    Returns:
        Resonance kernel value
    """
    return math.exp(-k * d * d)


def coherence(s_i: List[float], s_j: List[float]) -> float:
    """
    Calculate coherence between two time-series signals.
    
    Axiom: C_ij = (1/N) * Σ(s_i(t_k) * s_j(t_k))
    
    Args:
        s_i: First signal (time series)
        s_j: Second signal (time series)
        
    Returns:
        Coherence value between signals
        
    Raises:
        ValueError: If signals have different lengths
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
    
    Args:
        s_i: First signal
        s_j: Second signal
        
    Returns:
        Normalized coherence value [0, 1]
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


def global_coherence_invariant(f_avg: float, delta_t: float = CSC_TIME) -> float:
    """
    Calculate the Global Coherence Invariant.
    
    Axiom: P_GCI = cos(2π * f_avg * Δt)
    
    Args:
        f_avg: Average frequency (weighted mean of CRVs)
        delta_t: Time delta (default: CSC time = 1/π ≈ 0.318309886 s)
        
    Returns:
        Global Coherence Invariant value
    """
    return math.cos(2 * PI * f_avg * delta_t)


def calculate_weighted_frequency_average() -> float:
    """
    Calculate the weighted average frequency from the frequency spectrum.
    
    Uses the frequency weights defined in the spec for P_GCI calculation.
    
    Returns:
        Weighted average frequency
    """
    freq_weights = get_frequency_weights()
    
    total_weight = sum(freq_weights.values())
    if total_weight == 0:
        return 0.0
    
    weighted_sum = sum(freq * weight for freq, weight in freq_weights.items())
    return weighted_sum / total_weight


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
    """
    num_samples = int(duration * sample_rate)
    dt = 1.0 / sample_rate
    
    signal = []
    for i in range(num_samples):
        t = i * dt
        value = math.cos(2 * PI * frequency * t + phase)
        signal.append(value)
    
    return signal


def calculate_signal_coherence_matrix(signals: List[List[float]], 
                                    threshold: float = 0.5) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    """
    Calculate coherence matrix for multiple signals.
    
    Args:
        signals: List of time-series signals
        threshold: Coherence threshold for observability
        
    Returns:
        Tuple of (coherence_matrix, observable_pairs)
        - coherence_matrix: NxN matrix of coherence values
        - observable_pairs: List of (i, j) pairs with C_ij >= threshold
    """
    n_signals = len(signals)
    coherence_matrix = np.zeros((n_signals, n_signals))
    observable_pairs = []
    
    for i in range(n_signals):
        for j in range(n_signals):
            if i == j:
                coherence_matrix[i, j] = 1.0  # Perfect self-coherence
            else:
                c_ij = normalized_coherence(signals[i], signals[j])
                coherence_matrix[i, j] = c_ij
                
                if c_ij >= threshold:
                    observable_pairs.append((i, j))
    
    return coherence_matrix, observable_pairs


def resonance_interaction(b_i: float, frequency: float, time: float, k: float = 0.0002) -> float:
    """
    Calculate resonance interaction between an OffBit state and frequency.
    
    Formula: b_i * exp(-k * (t * f)²)
    
    Args:
        b_i: OffBit state value
        frequency: Interaction frequency
        time: Time parameter
        k: Decay constant
        
    Returns:
        Resonance interaction value
    """
    d = time * frequency
    return b_i * resonance_kernel(d, k)


def coherence_pressure_mitigation(coherence_pressure: float, 
                                csc_frequency: float = PI) -> float:
    """
    Calculate coherence pressure mitigation using CSC.
    
    The Coherence Sampling Cycle mitigates pressure by periodic re-synchronization.
    
    Args:
        coherence_pressure: Current coherence pressure (Ψ_p)
        csc_frequency: CSC frequency (default: π Hz)
        
    Returns:
        Mitigated coherence pressure
    """
    # Mitigation factor based on CSC frequency
    mitigation_factor = 1.0 / (1.0 + csc_frequency)
    return coherence_pressure * mitigation_factor


def calculate_frequency_from_wavelength(wavelength_nm: float) -> float:
    """
    Calculate frequency from wavelength.
    
    Formula: f = c / λ
    
    Args:
        wavelength_nm: Wavelength in nanometers
        
    Returns:
        Frequency in Hz
    """
    from .constants import C  # Speed of light
    
    wavelength_m = wavelength_nm * 1e-9  # Convert nm to m
    return C / wavelength_m


def calculate_wavelength_from_frequency(frequency_hz: float) -> float:
    """
    Calculate wavelength from frequency.
    
    Formula: λ = c / f
    
    Args:
        frequency_hz: Frequency in Hz
        
    Returns:
        Wavelength in nanometers
    """
    from .constants import C  # Speed of light
    
    wavelength_m = C / frequency_hz
    return wavelength_m * 1e9  # Convert m to nm


def carfe_recursion(offbit_n: float, offbit_n_minus_1: float, 
                   K_n: float, phi: float = None) -> float:
    """
    Calculate CARFE (Cykloid Adelic Recursive Expansive Field Equation) recursion.
    
    Axiom: OffBit_{n+1} = φ * OffBit_n + K_n * OffBit_{n-1}
    
    Args:
        offbit_n: Current OffBit state
        offbit_n_minus_1: Previous OffBit state
        K_n: Coupling constant
        phi: Golden ratio (default: loaded from constants)
        
    Returns:
        Next OffBit state
    """
    if phi is None:
        from .constants import PHI
        phi = PHI
    
    return phi * offbit_n + K_n * offbit_n_minus_1


def pi_phi_resonance_frequency() -> float:
    """
    Calculate the π-φ composite resonance frequency.
    
    This is a unique resonance arising from the interaction of π and φ.
    
    Returns:
        π-φ resonance frequency (58,977,069.609314 Hz)
    """
    from .constants import C, PI, PHI
    
    # Formula: f = C / (π * φ)
    return C / (PI * PHI)


def planck_euler_resonance_frequency() -> float:
    """
    Calculate the Planck-Euler resonance frequency.
    
    Links Planck scale physics with Euler's number.
    
    Returns:
        Planck-Euler resonance frequency
    """
    from .constants import C, PLANCK_TIME, E
    
    # Formula: f = C / (h * e^t) where h is Planck time
    return C / (PLANCK_TIME * math.exp(1))


def euclidean_geometry_pi_resonance() -> float:
    """
    Calculate the Euclidean geometry π-resonance frequency.
    
    Specific frequency tied to Euclidean geometric patterns.
    
    Returns:
        Euclidean π-resonance frequency (95,366,637.6 Hz)
    """
    # This is a specific value from the documentation
    return 95366637.6


def validate_coherence_threshold(coherence_value: float, threshold: float = 0.5) -> bool:
    """
    Validate if coherence value meets observability threshold.
    
    Args:
        coherence_value: Calculated coherence
        threshold: Observability threshold (default: 0.5)
        
    Returns:
        True if coherence is observable
    """
    return coherence_value >= threshold


def calculate_toggle_rate(state_changes: int, duration: float) -> float:
    """
    Calculate toggle rate for a binary signal.
    
    Formula: Toggle Rate = (Number of State Changes) / (Total Time Duration)
    
    Args:
        state_changes: Number of state transitions
        duration: Total time duration
        
    Returns:
        Toggle rate (toggles per second)
    """
    if duration <= 0:
        return 0.0
    
    return state_changes / duration

