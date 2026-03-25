"""
================================================================================
UBP NRCI CALCULATOR - v5.3 (FLOAT-FREE PATCHED)
================================================================================

Non-Random Coherence Index (NRCI) calculation module.
Integrates with metrics.py and provides coherence assessment.

Updates for v5.3:
- Imports from ubp_core_v5_3_merged.
- Implements Hyperbolic Stability Formula: 1 / (1 + Tax/10).
- Ensures strict Fraction arithmetic.

Author: Euan R A Craig, New Zealand
Date: 20 February 2026
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import json
from fractions import Fraction

# Import Core v5.3 Components
try:
    from ubp_core_v5_3_merged import LeechPointScaled
    from ubp_integration_adapter import UBP_INTEGRATION
    CORE_AVAILABLE = True
except ImportError:
    print("[WARNING] UBP Core v5.3 or Adapter not found.")
    CORE_AVAILABLE = False


@dataclass
class NRCIResult:
    """NRCI calculation result."""
    point_coords: Tuple[int, ...]
    global_nrci: Fraction      # Kept as Fraction for precision
    reality_health: Fraction
    info_health: Fraction
    activation_health: Fraction
    potential_health: Fraction
    coherence_regime: str
    stability_score: Fraction  # Kept as Fraction
    symmetry_tax: Fraction     # Kept as Fraction

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary (floats/strings)."""
        return {
            'point_coords': list(self.point_coords),
            'global_nrci': float(self.global_nrci),
            'reality_health': float(self.reality_health),
            'info_health': float(self.info_health),
            'activation_health': float(self.activation_health),
            'potential_health': float(self.potential_health),
            'coherence_regime': self.coherence_regime,
            'stability_score': float(self.stability_score),
            'symmetry_tax': float(self.symmetry_tax),
            'raw_fractions': {
                'nrci': str(self.global_nrci),
                'tax': str(self.symmetry_tax)
            }
        }


class NRCICalculator:
    """NRCI calculation engine."""
    
    def __init__(self):
        """Initialize NRCI calculator."""
        if CORE_AVAILABLE:
            self.metrics = UBP_INTEGRATION.metrics
            self.leech = UBP_INTEGRATION.leech
        self.history = []
    
    def calculate_nrci(self, coords: List[int]) -> NRCIResult:
        """Calculate NRCI for a point."""
        if not CORE_AVAILABLE:
            raise RuntimeError("Core not available.")
            
        if len(coords) != 24:
            raise ValueError("Point must have 24 coordinates")
        
        # 1. Create point (v5.3 Core Object)
        point = LeechPointScaled(coords=tuple(coords))
        
        # 2. Get ontological health (Returns Fractions)
        health = point.get_ontological_health()
        
        # 3. Get coherence regime
        regime = self.metrics.get_coherence_regime(health['Global_NRCI'])
        
        # 4. Calculate Symmetry Tax (Returns Fraction)
        tax = self.leech.calculate_symmetry_tax(coords)
        
        # 5. Calculate Stability Score (v5.3 Hyperbolic Standard)
        # Formula: Stability = 1 / (1 + (Tax / 10))
        # This prevents clamping to zero for high-complexity objects.
        one = Fraction(1, 1)
        ten = Fraction(10, 1)
        stability = one / (one + (tax / ten))
        
        result = NRCIResult(
            point_coords=tuple(coords),
            global_nrci=health['Global_NRCI'],
            reality_health=health['Reality'],
            info_health=health['Info'],
            activation_health=health['Activation'],
            potential_health=health['Potential'],
            coherence_regime=regime,
            stability_score=stability,
            symmetry_tax=tax,
        )
        
        self.history.append(result)
        return result
    
    def batch_calculate(self, point_list: List[List[int]]) -> List[NRCIResult]:
        """Calculate NRCI for multiple points."""
        results = []
        for coords in point_list:
            try:
                result = self.calculate_nrci(coords)
                results.append(result)
            except Exception as e:
                print(f"[WARNING] Failed to calculate NRCI for {coords}: {e}")
        return results
    
    def get_regime_distribution(self, results: List[NRCIResult]) -> Dict[str, int]:
        """Get distribution of coherence regimes."""
        distribution = {'high': 0, 'medium': 0, 'low': 0, 'unknown': 0}
        for result in results:
            reg = result.coherence_regime
            distribution[reg] = distribution.get(reg, 0) + 1
        return distribution
    
    def get_average_metrics(self, results: List[NRCIResult]) -> Dict[str, float]:
        """Get average metrics across results."""
        if not results:
            return {}
        
        count = len(results)
        return {
            'avg_nrci': float(sum(r.global_nrci for r in results) / count),
            'avg_stability': float(sum(r.stability_score for r in results) / count),
            'avg_tax': float(sum(r.symmetry_tax for r in results) / count),
        }
    
    def export_history(self, filename: str = None) -> str:
        """Export calculation history to JSON."""
        data = {
            'total_calculations': len(self.history),
            'results': [r.to_dict() for r in self.history],
        }
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return filename
        
        return json.dumps(data, indent=2)


# Global instance
NRCI_CALCULATOR = NRCICalculator()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("UBP NRCI CALCULATOR v5.3 - TEST")
    print("=" * 80)
    
    if CORE_AVAILABLE:
        # Test single point (Standard Leech Vector)
        print("\n[TEST 1] Single Point NRCI")
        test_coords = [2, 0, 1, -1, 0, 2, 0, 0, 1, -1, 0, 0, 1, 0, 0, 0, -1, 2, 0, 1, 0, 0, -1, 0]
        result = NRCI_CALCULATOR.calculate_nrci(test_coords)
        print(f"  NRCI: {float(result.global_nrci):.4f}")
        print(f"  Regime: {result.coherence_regime}")
        print(f"  Tax: {float(result.symmetry_tax):.4f}")
        print(f"  Stability: {float(result.stability_score):.4f}")
        
        # Test batch
        print("\n[TEST 2] Batch NRCI Calculation")
        batch_coords = [
            [2, 0, 1, -1, 0, 2, 0, 0, 1, -1, 0, 0, 1, 0, 0, 0, -1, 2, 0, 1, 0, 0, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Origin
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # Max Noise
        ]
        batch_results = NRCI_CALCULATOR.batch_calculate(batch_coords)
        print(f"  Processed: {len(batch_results)} points")
        
        # Get distribution
        distribution = NRCI_CALCULATOR.get_regime_distribution(batch_results)
        print(f"  Distribution: {distribution}")
        
        # Get averages
        averages = NRCI_CALCULATOR.get_average_metrics(batch_results)
        print(f"  Avg NRCI: {averages['avg_nrci']:.4f}")
        print(f"  Avg Stability: {averages['avg_stability']:.4f}")
        
        print("\n" + "=" * 80)
        print("✓ NRCI CALCULATOR READY (v5.3)")
        print("=" * 80)
    else:
        print("❌ Core not available. Cannot run tests.")