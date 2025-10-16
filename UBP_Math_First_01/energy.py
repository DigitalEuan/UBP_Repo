"""
UBP Energy Equation Implementation

Implements the complete UBP energy equation and related calculations:
E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × Σ(w_ij M_ij)
"""

import math
from typing import List, Optional
from .constants import (
    C, PI, PHI, E as EULER_E, 
    R_SPEC, S_OPT_SPEC, P_GCI_SPEC, C_INFINITY,
    get_energy_constants
)


def energy(M: int, C_speed: float = C, R: float = R_SPEC, S_opt: float = S_OPT_SPEC,
          P_GCI: float = P_GCI_SPEC, O_observer: float = 1.0, 
          c_infinity: float = C_INFINITY, I_spin: float = 1.0, 
          w_sum: float = 0.1) -> float:
    """
    Calculate the total UBP energy.
    
    Axiom: E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × Σ(w_ij M_ij)
    
    Args:
        M: Active OffBits count
        C_speed: Speed of light (m/s)
        R: Resonance strength
        S_opt: Structural optimality factor
        P_GCI: Global Coherence Invariant
        O_observer: Observer effect factor (1.0 neutral, 1.5 intentional)
        c_infinity: Cosmic constant
        I_spin: Spin information factor
        w_sum: Weighted toggle matrix sum
        
    Returns:
        Total energy value
    """
    return (M * C_speed * (R * S_opt) * P_GCI * O_observer * 
            c_infinity * I_spin * w_sum)


def resonance_strength(R_0: float = 0.95, H_t: float = 0.05) -> float:
    """
    Calculate resonance strength.
    
    Axiom: R = R_0 × (1 - H_t / ln(4))
    
    Args:
        R_0: Base resonance strength
        H_t: Tonal entropy
        
    Returns:
        Resonance strength value
    """
    return R_0 * (1 - H_t / math.log(4))


def structural_optimality(distances: List[float], max_distance: float, 
                         active_bits: List[int]) -> float:
    """
    Calculate structural optimization factor.
    
    Axiom: S_opt = 0.7 × (1 - Σd_i / √Σd_max²) + 0.3 × (Σb_j / 12)
    
    Args:
        distances: List of distances to Glyph center
        max_distance: Maximum possible distance (Bitfield diagonal)
        active_bits: List of active bits in Information layer (0-11)
        
    Returns:
        Structural optimality factor
    """
    if not distances or max_distance == 0:
        spatial_term = 0.0
    else:
        sum_distances = sum(distances)
        sqrt_sum_max_squared = math.sqrt(len(distances) * max_distance * max_distance)
        spatial_term = 1 - (sum_distances / sqrt_sum_max_squared)
    
    if not active_bits:
        bit_term = 0.0
    else:
        sum_active_bits = sum(active_bits)
        bit_term = sum_active_bits / 12  # 12 bits in Information layer
    
    return 0.7 * spatial_term + 0.3 * bit_term


def observer_effect_factor(observation_type: str = "neutral", 
                          purpose_tensor: float = 1.0) -> float:
    """
    Calculate observer effect factor.
    
    Formula: O_observer = 1 + (1/4π) * log(s/s_0) * F_μν(ψ)
    Simplified: 1.0 (neutral) or 1.5 (intentional)
    
    Args:
        observation_type: "neutral" or "intentional"
        purpose_tensor: Purpose tensor value
        
    Returns:
        Observer effect factor
    """
    if observation_type == "neutral":
        return 1.0
    elif observation_type == "intentional":
        return 1.5
    else:
        # General formula (simplified)
        k = 1.0 / (4 * PI)
        return 1.0 + k * math.log(purpose_tensor)


def cosmic_constant(phi: float = PHI, alpha: float = 0.0072973525693) -> float:
    """
    Calculate the cosmic constant c_∞.
    
    Formula: c_∞ = 24 × φ × (1 + α)
    
    Args:
        phi: Golden ratio
        alpha: Fine-structure constant
        
    Returns:
        Cosmic constant value
    """
    return 24 * phi * (1 + alpha)


def spin_information_factor(spin_probabilities: List[float]) -> float:
    """
    Calculate spin information factor using Shannon entropy.
    
    Formula: I_spin = Σ p_s × ln(1/p_s)
    
    Args:
        spin_probabilities: List of spin state probabilities
        
    Returns:
        Spin information factor
    """
    if not spin_probabilities:
        return 1.0
    
    entropy = 0.0
    for p_s in spin_probabilities:
        if p_s > 0:
            entropy += p_s * math.log(1.0 / p_s)
    
    return entropy


def quantum_spin_entropy(p_s: float = None) -> float:
    """
    Calculate spin entropy for quantum realm.
    
    Args:
        p_s: Spin probability (default: e/12 ≈ 0.2265234857)
        
    Returns:
        Quantum spin entropy
    """
    if p_s is None:
        p_s = EULER_E / 12  # e/12 ≈ 0.2265234857
    
    if p_s <= 0 or p_s >= 1:
        return 0.0
    
    return p_s * math.log(1.0 / p_s) + (1 - p_s) * math.log(1.0 / (1 - p_s))


def cosmological_spin_entropy(p_s: float = None) -> float:
    """
    Calculate spin entropy for cosmological realm.
    
    Args:
        p_s: Spin probability (default: π^φ ≈ 0.83203682)
        
    Returns:
        Cosmological spin entropy
    """
    if p_s is None:
        p_s = PI ** PHI  # π^φ ≈ 0.83203682
    
    if p_s <= 0 or p_s >= 1:
        return 0.0
    
    return p_s * math.log(1.0 / p_s) + (1 - p_s) * math.log(1.0 / (1 - p_s))


def weighted_toggle_matrix_sum(weights: List[float], toggle_operations: List[float]) -> float:
    """
    Calculate weighted sum of toggle operations.
    
    Formula: Σ(w_ij × M_ij)
    
    Args:
        weights: Interaction weights (must sum to 1)
        toggle_operations: Toggle operation results
        
    Returns:
        Weighted sum
    """
    if len(weights) != len(toggle_operations):
        raise ValueError("Weights and operations must have same length")
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    
    normalized_weights = [w / total_weight for w in weights]
    
    return sum(w * op for w, op in zip(normalized_weights, toggle_operations))


def calculate_energy_for_realm(realm_name: str, active_offbits: int, 
                              distances: Optional[List[float]] = None,
                              max_distance: Optional[float] = None,
                              active_bits: Optional[List[int]] = None) -> float:
    """
    Calculate energy for a specific realm using realm-specific parameters.
    
    Args:
        realm_name: Name of the realm
        active_offbits: Number of active OffBits
        distances: Optional distances for S_opt calculation
        max_distance: Optional max distance for S_opt calculation
        active_bits: Optional active bits for S_opt calculation
        
    Returns:
        Energy value for the realm
    """
    from .constants import get_realm_constants
    
    try:
        realm = get_realm_constants(realm_name)
    except KeyError:
        # Use default values if realm not found
        realm = {}
    
    # Use realm-specific or default values
    R = resonance_strength()  # Use calculated value
    
    if distances and max_distance and active_bits:
        S_opt = structural_optimality(distances, max_distance, active_bits)
    else:
        S_opt = S_OPT_SPEC  # Use default
    
    # Calculate energy with realm-specific parameters
    return energy(
        M=active_offbits,
        R=R,
        S_opt=S_opt
    )


def energy_conservation_check(initial_energy: float, final_energy: float, 
                            tolerance: float = 1e-10) -> bool:
    """
    Check if energy is conserved within tolerance.
    
    Args:
        initial_energy: Energy before operation
        final_energy: Energy after operation
        tolerance: Acceptable difference
        
    Returns:
        True if energy is conserved
    """
    return abs(final_energy - initial_energy) <= tolerance


def calculate_energy_density(energy: float, volume: float) -> float:
    """
    Calculate energy density.
    
    Args:
        energy: Total energy
        volume: Volume of the region
        
    Returns:
        Energy density (energy per unit volume)
    """
    if volume <= 0:
        return 0.0
    
    return energy / volume


def energy_from_frequency(frequency: float, num_quanta: int = 1) -> float:
    """
    Calculate energy from frequency using Planck relation.
    
    Formula: E = n × h × f
    
    Args:
        frequency: Frequency in Hz
        num_quanta: Number of energy quanta
        
    Returns:
        Energy value
    """
    from .constants import PLANCK_TIME
    
    # Planck constant from Planck time: h = t_P × c²
    h = PLANCK_TIME * C * C
    
    return num_quanta * h * frequency


def energy_efficiency_ratio(actual_energy: float, theoretical_max: float) -> float:
    """
    Calculate energy efficiency ratio.
    
    Args:
        actual_energy: Actual measured energy
        theoretical_max: Theoretical maximum energy
        
    Returns:
        Efficiency ratio [0, 1]
    """
    if theoretical_max <= 0:
        return 0.0
    
    return min(1.0, actual_energy / theoretical_max)


def validate_energy_bounds(energy_value: float, min_energy: float = 0.0, 
                          max_energy: Optional[float] = None) -> bool:
    """
    Validate that energy value is within acceptable bounds.
    
    Args:
        energy_value: Energy to validate
        min_energy: Minimum acceptable energy
        max_energy: Maximum acceptable energy (None for no limit)
        
    Returns:
        True if energy is within bounds
    """
    if energy_value < min_energy:
        return False
    
    if max_energy is not None and energy_value > max_energy:
        return False
    
    return True

