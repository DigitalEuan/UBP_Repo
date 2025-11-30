"""
================================================================================
UBP 3.7.1 Antibiotic Study - Comparative Metrics Analysis
Author: Euan R A Craig, New Zealand
Date: 30 November 2025
================================================================================

Comparative analysis of NRCI vs traditional complexity/information metrics.

**Purpose**:
Demonstrate why NRCI is superior to standard metrics for antibiotic discovery:
- Shannon Entropy measures randomness/unpredictability
- NRCI measures functional coherence and self-similar order

**Key Defense**:
High entropy ≠ functional coherence. Many random patterns have maximum entropy
but zero biological function. NRCI provides the directional filter needed to
identify patterns with specific, non-random internal structure.
"""

import math
import sys
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
import random

# Add UBP 3.7.1 core to path
UBP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UBP_Repo', 'ubp_3.7.1'))
sys.path.insert(0, UBP_ROOT)
sys.path.insert(0, os.path.join(UBP_ROOT, 'core'))
sys.path.insert(0, os.path.join(UBP_ROOT, 'utils'))

from coherence_substrate import CoherenceState
from state import OffBit


@dataclass
class MetricComparison:
    """Comparison of different complexity metrics for a pattern."""
    offbit_hex: str
    offbit_value: int
    active_bits: int
    
    # NRCI (UBP metric)
    nrci: float
    
    # Shannon Entropy
    shannon_entropy: float
    
    # Lempel-Ziv Complexity
    lz_complexity: float
    
    # Bit balance (perfect = 0.0)
    bit_balance: float
    
    # Pattern type classification
    pattern_type: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for export."""
        return {
            'offbit_hex': self.offbit_hex,
            'offbit_value': self.offbit_value,
            'active_bits': self.active_bits,
            'nrci': self.nrci,
            'shannon_entropy': self.shannon_entropy,
            'lz_complexity': self.lz_complexity,
            'bit_balance': self.bit_balance,
            'pattern_type': self.pattern_type
        }


class ComparativeMetrics:
    """
    Calculate and compare different complexity/information metrics.
    """
    
    def __init__(self):
        """Initialize the comparative metrics calculator."""
        pass
    
    def calculate_shannon_entropy(self, offbit_value: int, num_bits: int = 24) -> float:
        """
        Calculate Shannon Entropy of a bit pattern.
        
        Shannon Entropy measures the average information content or unpredictability.
        For a binary string:
            H = -p₀ log₂(p₀) - p₁ log₂(p₁)
        
        Where p₀ = proportion of 0s, p₁ = proportion of 1s.
        
        Maximum entropy (H = 1.0) occurs when p₀ = p₁ = 0.5 (perfect balance).
        This means the pattern is maximally unpredictable/random.
        
        Args:
            offbit_value: Integer value of the bit pattern
            num_bits: Number of bits to consider (default 24)
        
        Returns:
            Shannon entropy [0, 1]
        """
        # Convert to binary string
        bit_string = format(offbit_value, f'0{num_bits}b')
        
        # Count 0s and 1s
        num_ones = bit_string.count('1')
        num_zeros = num_bits - num_ones
        
        # Calculate proportions
        p0 = num_zeros / num_bits
        p1 = num_ones / num_bits
        
        # Calculate entropy
        entropy = 0.0
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        if p1 > 0:
            entropy -= p1 * math.log2(p1)
        
        return entropy
    
    def calculate_lempel_ziv_complexity(self, offbit_value: int, num_bits: int = 24) -> float:
        """
        Calculate Lempel-Ziv Complexity (normalized).
        
        LZ complexity measures the number of distinct patterns in a sequence.
        Higher complexity indicates more diverse patterns (less repetition).
        
        This is a simplified implementation of LZ76 compression complexity.
        
        Args:
            offbit_value: Integer value of the bit pattern
            num_bits: Number of bits to consider (default 24)
        
        Returns:
            Normalized LZ complexity [0, 1]
        """
        # Convert to binary string
        bit_string = format(offbit_value, f'0{num_bits}b')
        
        # LZ76 algorithm
        i = 0
        complexity = 0
        n = len(bit_string)
        
        while i < n:
            # Find longest match in history
            max_len = 0
            for j in range(i):
                k = 0
                while (i + k < n) and (bit_string[j + k] == bit_string[i + k]):
                    k += 1
                max_len = max(max_len, k)
            
            # Move forward by match length + 1
            i += max(1, max_len)
            complexity += 1
        
        # Normalize by theoretical maximum
        # Maximum complexity for n bits is approximately n / log₂(n)
        if num_bits > 1:
            max_complexity = num_bits / math.log2(num_bits)
            normalized = complexity / max_complexity
        else:
            normalized = 0.0
        
        return min(1.0, normalized)
    
    def calculate_bit_balance(self, offbit_value: int, num_bits: int = 24) -> float:
        """
        Calculate bit balance deviation from perfect 50/50.
        
        Perfect balance = 0.0 (exactly 12 ones and 12 zeros for 24 bits)
        Maximum imbalance = 1.0 (all ones or all zeros)
        
        Args:
            offbit_value: Integer value of the bit pattern
            num_bits: Number of bits to consider (default 24)
        
        Returns:
            Bit balance deviation [0, 1]
        """
        num_ones = bin(offbit_value).count('1')
        ideal_ones = num_bits / 2
        deviation = abs(num_ones - ideal_ones) / ideal_ones
        
        return deviation
    
    def classify_pattern(self, offbit_value: int, nrci: float, 
                        shannon_entropy: float, num_bits: int = 24) -> str:
        """
        Classify pattern type based on metrics.
        
        Args:
            offbit_value: Integer value
            nrci: Non-Random Coherence Index
            shannon_entropy: Shannon entropy
            num_bits: Number of bits
        
        Returns:
            Pattern classification string
        """
        num_ones = bin(offbit_value).count('1')
        
        # Check for super-coherent (NRCI > 0.9999992)
        if nrci > 0.9999992:
            return "SuperCoherent (Antibiotic Candidate)"
        
        # Check for high coherence (NRCI > 0.999997)
        elif nrci > 0.999997:
            return "HighCoherent (Known Antibiotic)"
        
        # Check for perfect balance + high entropy (random-like)
        elif num_ones == num_bits // 2 and shannon_entropy > 0.99:
            return "MaxEntropy (Random Balanced)"
        
        # Check for high entropy but not balanced
        elif shannon_entropy > 0.99:
            return "HighEntropy (Random Unbalanced)"
        
        # Low entropy patterns
        elif shannon_entropy < 0.5:
            return "LowEntropy (Highly Ordered)"
        
        # Everything else
        else:
            return "Moderate (Mixed)"
    
    def analyze_pattern(self, offbit_value: int, num_bits: int = 24) -> MetricComparison:
        """
        Perform comprehensive metric analysis on a pattern.
        
        Args:
            offbit_value: Integer value of the pattern
            num_bits: Number of bits to consider
        
        Returns:
            MetricComparison with all metrics calculated
        """
        # Calculate NRCI using UBP 3.7.1
        coherence = CoherenceState(offbit_value)
        nrci = coherence.nrci
        
        # Calculate traditional metrics
        shannon = self.calculate_shannon_entropy(offbit_value, num_bits)
        lz = self.calculate_lempel_ziv_complexity(offbit_value, num_bits)
        balance = self.calculate_bit_balance(offbit_value, num_bits)
        
        # Classify pattern
        pattern_type = self.classify_pattern(offbit_value, nrci, shannon, num_bits)
        
        # Count active bits
        active_bits = bin(offbit_value).count('1')
        
        return MetricComparison(
            offbit_hex=f"0x{offbit_value:06X}",
            offbit_value=offbit_value,
            active_bits=active_bits,
            nrci=nrci,
            shannon_entropy=shannon,
            lz_complexity=lz,
            bit_balance=balance,
            pattern_type=pattern_type
        )
    
    def generate_random_balanced_patterns(self, count: int, num_bits: int = 24) -> List[int]:
        """
        Generate random patterns with perfect bit balance (12 ones, 12 zeros).
        
        These patterns will have maximum Shannon Entropy but random NRCI values.
        This demonstrates that high entropy ≠ functional coherence.
        
        Args:
            count: Number of patterns to generate
            num_bits: Number of bits (default 24)
        
        Returns:
            List of integer values with perfect bit balance
        """
        patterns = []
        target_ones = num_bits // 2
        
        for _ in range(count):
            # Create list with exactly target_ones 1s and rest 0s
            bits = [1] * target_ones + [0] * (num_bits - target_ones)
            
            # Shuffle randomly
            random.shuffle(bits)
            
            # Convert to integer
            value = int(''.join(map(str, bits)), 2)
            patterns.append(value)
        
        return patterns
    
    def compare_metric_effectiveness(self, 
                                    supercoherent_patterns: List[int],
                                    random_balanced_patterns: List[int]) -> Dict:
        """
        Compare NRCI vs Shannon Entropy for discriminating functional patterns.
        
        Args:
            supercoherent_patterns: List of high-NRCI antibiotic candidates
            random_balanced_patterns: List of random patterns with perfect balance
        
        Returns:
            Dictionary with comparison statistics
        """
        # Analyze both groups
        super_analyses = [self.analyze_pattern(p) for p in supercoherent_patterns]
        random_analyses = [self.analyze_pattern(p) for p in random_balanced_patterns]
        
        # Calculate statistics
        super_nrci_mean = sum(a.nrci for a in super_analyses) / len(super_analyses)
        super_entropy_mean = sum(a.shannon_entropy for a in super_analyses) / len(super_analyses)
        
        random_nrci_mean = sum(a.nrci for a in random_analyses) / len(random_analyses)
        random_entropy_mean = sum(a.shannon_entropy for a in random_analyses) / len(random_analyses)
        
        return {
            'supercoherent_group': {
                'count': len(supercoherent_patterns),
                'nrci_mean': super_nrci_mean,
                'nrci_min': min(a.nrci for a in super_analyses),
                'nrci_max': max(a.nrci for a in super_analyses),
                'shannon_entropy_mean': super_entropy_mean,
                'shannon_entropy_min': min(a.shannon_entropy for a in super_analyses),
                'shannon_entropy_max': max(a.shannon_entropy for a in super_analyses),
            },
            'random_balanced_group': {
                'count': len(random_balanced_patterns),
                'nrci_mean': random_nrci_mean,
                'nrci_min': min(a.nrci for a in random_analyses),
                'nrci_max': max(a.nrci for a in random_analyses),
                'shannon_entropy_mean': random_entropy_mean,
                'shannon_entropy_min': min(a.shannon_entropy for a in random_analyses),
                'shannon_entropy_max': max(a.shannon_entropy for a in random_analyses),
            },
            'discrimination_power': {
                'nrci_separation': super_nrci_mean - random_nrci_mean,
                'entropy_separation': super_entropy_mean - random_entropy_mean,
                'nrci_discriminates': super_nrci_mean > random_nrci_mean + 0.0000001,
                'entropy_discriminates': abs(super_entropy_mean - random_entropy_mean) > 0.01,
            },
            'conclusion': self._generate_conclusion(super_nrci_mean, random_nrci_mean,
                                                   super_entropy_mean, random_entropy_mean)
        }
    
    def _generate_conclusion(self, super_nrci: float, random_nrci: float,
                            super_entropy: float, random_entropy: float) -> str:
        """Generate conclusion text for the comparison."""
        nrci_diff = super_nrci - random_nrci
        entropy_diff = abs(super_entropy - random_entropy)
        
        if nrci_diff > 0.0000001 and entropy_diff < 0.01:
            return (
                "NRCI successfully discriminates between functional (supercoherent) "
                "and random patterns, while Shannon Entropy fails to distinguish them. "
                "This demonstrates that NRCI measures functional coherence, not mere "
                "randomness or bit balance. High entropy indicates unpredictability; "
                "high NRCI indicates specific, non-random internal structure required "
                "for biological function."
            )
        else:
            return (
                "Both metrics show some discrimination capability. Further analysis "
                "required to determine optimal metric for antibiotic discovery."
            )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("UBP 3.7.1 Comparative Metrics Analysis - Test Suite")
    print("=" * 80)
    
    metrics = ComparativeMetrics()
    
    # Test with Erythromycin signature
    print("\nAnalyzing Erythromycin (0x9C2F68):")
    analysis = metrics.analyze_pattern(0x9C2F68)
    print(f"  NRCI: {analysis.nrci:.10f}")
    print(f"  Shannon Entropy: {analysis.shannon_entropy:.10f}")
    print(f"  LZ Complexity: {analysis.lz_complexity:.10f}")
    print(f"  Bit Balance: {analysis.bit_balance:.10f}")
    print(f"  Pattern Type: {analysis.pattern_type}")
    
    # Generate and test random balanced patterns
    print("\nGenerating 10 random balanced patterns (12 ones, 12 zeros):")
    random_patterns = metrics.generate_random_balanced_patterns(10)
    
    for i, pattern in enumerate(random_patterns[:3], 1):
        analysis = metrics.analyze_pattern(pattern)
        print(f"\n  Pattern {i} (0x{pattern:06X}):")
        print(f"    NRCI: {analysis.nrci:.10f}")
        print(f"    Shannon Entropy: {analysis.shannon_entropy:.10f}")
        print(f"    Pattern Type: {analysis.pattern_type}")
    
    print("\n" + "=" * 80)
    print("Comparative Metrics module initialized successfully!")
    print("=" * 80)
