#!/usr/bin/env python3
"""
================================================================================
UBP NRCI CALCULATOR - v4.2.6
================================================================================

Normalized Resonance Coherence Index (NRCI) calculation module.
Integrates with metrics.py and provides coherence assessment.

Version: 4.2.6 NRCI Calculator
Author: Euan R A Craig, New Zealand
Date: 2 January 2026

FEATURES:
✓ NRCI calculation from ontological health
✓ Coherence regime classification
✓ Stability prediction
✓ Multi-point analysis
✓ Historical tracking

================================================================================
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import json

try:
    from ubp_core_v4_2_6_COMBINED import LeechPointScaled
    from ubp_integration_adapter import UBP_INTEGRATION
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False


@dataclass
class NRCIResult:
    """NRCI calculation result."""
    point_coords: Tuple[int, ...]
    global_nrci: float
    reality_health: float
    info_health: float
    activation_health: float
    potential_health: float
    coherence_regime: str
    stability_score: float
    symmetry_tax: float


class NRCICalculator:
    """NRCI calculation engine."""
    
    def __init__(self):
        """Initialize NRCI calculator."""
        self.metrics = UBP_INTEGRATION.metrics
        self.leech = UBP_INTEGRATION.leech
        self.history = []
    
    def calculate_nrci(self, coords: List[int]) -> NRCIResult:
        """Calculate NRCI for a point."""
        if len(coords) != 24:
            raise ValueError("Point must have 24 coordinates")
        
        # Create point
        point = LeechPointScaled(coords=tuple(coords))
        
        # Get ontological health
        health = point.get_ontological_health()
        
        # Get coherence regime
        regime = self.metrics.get_coherence_regime(health['Global_NRCI'])
        
        # Calculate stability score (inverse of symmetry tax, normalized)
        tax = self.leech.calculate_symmetry_tax(coords)
        stability = max(0.0, 10.0 - tax) / 10.0  # Normalize to 0-1
        
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
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        for result in results:
            distribution[result.coherence_regime] += 1
        return distribution
    
    def get_average_metrics(self, results: List[NRCIResult]) -> Dict[str, float]:
        """Get average metrics across results."""
        if not results:
            return {}
        
        return {
            'avg_nrci': sum(r.global_nrci for r in results) / len(results),
            'avg_stability': sum(r.stability_score for r in results) / len(results),
            'avg_tax': sum(r.symmetry_tax for r in results) / len(results),
            'avg_reality': sum(r.reality_health for r in results) / len(results),
            'avg_info': sum(r.info_health for r in results) / len(results),
            'avg_activation': sum(r.activation_health for r in results) / len(results),
            'avg_potential': sum(r.potential_health for r in results) / len(results),
        }
    
    def result_to_dict(self, result: NRCIResult) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'point_coords': list(result.point_coords),
            'global_nrci': result.global_nrci,
            'reality_health': result.reality_health,
            'info_health': result.info_health,
            'activation_health': result.activation_health,
            'potential_health': result.potential_health,
            'coherence_regime': result.coherence_regime,
            'stability_score': result.stability_score,
            'symmetry_tax': result.symmetry_tax,
        }
    
    def export_history(self, filename: str = None) -> str:
        """Export calculation history to JSON."""
        data = {
            'total_calculations': len(self.history),
            'results': [self.result_to_dict(r) for r in self.history],
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
    print("UBP NRCI CALCULATOR v4.2.6 - TEST")
    print("=" * 80)
    
    # Test single point
    print("\n[TEST 1] Single Point NRCI")
    test_coords = [2, 0, 1, -1, 0, 2, 0, 0, 1, -1, 0, 0, 1, 0, 0, 0, -1, 2, 0, 1, 0, 0, -1, 0]
    result = NRCI_CALCULATOR.calculate_nrci(test_coords)
    print(f"  NRCI: {result.global_nrci:.4f}")
    print(f"  Regime: {result.coherence_regime}")
    print(f"  Stability: {result.stability_score:.4f}")
    
    # Test batch
    print("\n[TEST 2] Batch NRCI Calculation")
    batch_coords = [
        [2, 0, 1, -1, 0, 2, 0, 0, 1, -1, 0, 0, 1, 0, 0, 0, -1, 2, 0, 1, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
    print("✓ NRCI CALCULATOR READY")
    print("=" * 80)

