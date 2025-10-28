"""
UBP Cymatics Study - Phase II: Geometric Constant Search
Author: Euan R A Craig, New Zealand
Date: October 24, 2025

This script searches for the geometric ratio Y ≈ 0.265 that resolves the 
dimensional scaling factor X_G ≈ 7.94 × 10^7 when combined with the speed of light.

Based on the Level_Up_1.pdf blueprint, we investigate:
1. Icosahedral geometric ratios
2. Tetrahedral and cubic harmonic signatures
3. Elementary charge relationships
"""

import numpy as np
import math
import json
from typing import Dict, List, Tuple
import sys

# Add the ubp_3.2 directory to the path
sys.path.insert(0, '/home/ubuntu/ubp_3.2')

from system_constants import UBPConstants

class GeometricConstantSearch:
    """Search for the geometric constant Y that resolves the scaling factor"""
    
    def __init__(self):
        self.constants = UBPConstants()
        
        # Physical constants from UBP framework
        self.c = self.constants.SPEED_OF_LIGHT  # Speed of light
        self.pi = self.constants.PI
        self.phi = self.constants.PHI  # Golden ratio
        self.e_const = self.constants.E  # Euler's number
        self.alpha = self.constants.FINE_STRUCTURE_CONSTANT
        self.G = self.constants.GRAVITATIONAL_CONSTANT
        self.elementary_charge = self.constants.ELEMENTARY_CHARGE
        
        # Target values from the paper
        self.X_G_target = 7.94 * 10**7  # Scaling factor for G
        self.X_m_p_target = 5.81 * 10**7  # Scaling factor for Planck mass
        self.Y_target = 0.265  # Target geometric ratio
        
        # Tolerance for matching
        self.tolerance = 0.01  # 1% tolerance
        
        print("=" * 80)
        print("UBP Cymatics Study - Geometric Constant Search")
        print("=" * 80)
        print(f"Speed of light (c): {self.c:.4e} m/s")
        print(f"Golden ratio (φ): {self.phi:.10f}")
        print(f"Pi (π): {self.pi:.10f}")
        print(f"Euler's number (e): {self.e_const:.10f}")
        print(f"Fine structure constant (α): {self.alpha:.10f}")
        print(f"Elementary charge (e): {self.elementary_charge:.4e} C")
        print(f"\nTarget X_G: {self.X_G_target:.4e}")
        print(f"Target Y: {self.Y_target:.6f}")
        print("=" * 80)
    
    def generate_geometric_ratios(self) -> Dict[str, float]:
        """Generate candidate geometric ratios from various geometric systems"""
        
        ratios = {}
        
        # Golden ratio based (Icosahedral geometry)
        ratios['phi'] = self.phi
        ratios['1/phi'] = 1 / self.phi
        ratios['phi^2'] = self.phi ** 2
        ratios['1/phi^2'] = 1 / (self.phi ** 2)
        ratios['phi^3'] = self.phi ** 3
        ratios['1/phi^3'] = 1 / (self.phi ** 3)
        ratios['sqrt(phi)'] = math.sqrt(self.phi)
        ratios['1/sqrt(phi)'] = 1 / math.sqrt(self.phi)
        ratios['phi/2'] = self.phi / 2
        ratios['phi/3'] = self.phi / 3
        ratios['phi/4'] = self.phi / 4
        ratios['phi/pi'] = self.phi / self.pi
        ratios['pi/phi'] = self.pi / self.phi
        
        # Tetrahedral harmonics (sqrt(3) based)
        ratios['sqrt(3)/2'] = math.sqrt(3) / 2
        ratios['1/sqrt(3)'] = 1 / math.sqrt(3)
        ratios['sqrt(3)/3'] = math.sqrt(3) / 3
        ratios['sqrt(3)/4'] = math.sqrt(3) / 4
        ratios['sqrt(3)/6'] = math.sqrt(3) / 6
        
        # Cubic harmonics (sqrt(2) based)
        ratios['sqrt(2)/2'] = math.sqrt(2) / 2
        ratios['1/sqrt(2)'] = 1 / math.sqrt(2)
        ratios['sqrt(2)/3'] = math.sqrt(2) / 3
        ratios['sqrt(2)/4'] = math.sqrt(2) / 4
        
        # Octahedral (combinations)
        ratios['sqrt(2/3)'] = math.sqrt(2/3)
        ratios['sqrt(3/2)'] = math.sqrt(3/2)
        
        # Simple fractions
        for i in range(1, 13):
            for j in range(1, 13):
                if i != j:
                    key = f'{i}/{j}'
                    ratios[key] = i / j
        
        # Pi-based ratios
        ratios['1/pi'] = 1 / self.pi
        ratios['pi/2'] = self.pi / 2
        ratios['pi/3'] = self.pi / 3
        ratios['pi/4'] = self.pi / 4
        ratios['pi/6'] = self.pi / 6
        ratios['2/pi'] = 2 / self.pi
        ratios['3/pi'] = 3 / self.pi
        ratios['4/pi'] = 4 / self.pi
        
        # e-based ratios
        ratios['1/e'] = 1 / self.e_const
        ratios['e/2'] = self.e_const / 2
        ratios['e/3'] = self.e_const / 3
        ratios['e/4'] = self.e_const / 4
        ratios['e/pi'] = self.e_const / self.pi
        ratios['pi/e'] = self.pi / self.e_const
        
        # Combined geometric ratios
        ratios['phi*sqrt(2)/2'] = self.phi * math.sqrt(2) / 2
        ratios['phi*sqrt(3)/3'] = self.phi * math.sqrt(3) / 3
        ratios['phi/(2*pi)'] = self.phi / (2 * self.pi)
        ratios['sqrt(phi)/2'] = math.sqrt(self.phi) / 2
        
        # Platonic solid ratios
        ratios['1/(2*phi)'] = 1 / (2 * self.phi)
        ratios['sqrt(5)/5'] = math.sqrt(5) / 5
        ratios['sqrt(5)/3'] = math.sqrt(5) / 3
        ratios['2/sqrt(5)'] = 2 / math.sqrt(5)
        
        return ratios
    
    def check_scaling_factor_match(self, Y: float, ratio_name: str) -> Dict:
        """Check if a given Y produces the target X_G when combined with c"""
        
        # Calculate X_G = c * Y
        X_G_calculated = self.c * Y
        
        # Calculate relative error
        rel_error_G = abs(X_G_calculated - self.X_G_target) / self.X_G_target
        
        # Check if within tolerance
        match = rel_error_G < self.tolerance
        
        result = {
            'ratio_name': ratio_name,
            'Y_value': Y,
            'X_G_calculated': X_G_calculated,
            'X_G_target': self.X_G_target,
            'relative_error': rel_error_G,
            'match': match,
            'error_percentage': rel_error_G * 100
        }
        
        return result
    
    def search_for_Y(self) -> List[Dict]:
        """Search through all geometric ratios to find Y ≈ 0.265"""
        
        print("\n" + "=" * 80)
        print("SEARCHING FOR GEOMETRIC CONSTANT Y ≈ 0.265")
        print("=" * 80)
        
        ratios = self.generate_geometric_ratios()
        results = []
        
        print(f"\nGenerated {len(ratios)} candidate geometric ratios")
        print(f"Searching for ratios close to Y_target = {self.Y_target:.6f}\n")
        
        # Filter ratios close to Y_target
        candidates = []
        for name, value in ratios.items():
            if 0.1 < value < 0.5:  # Reasonable range around 0.265
                error = abs(value - self.Y_target)
                rel_error = error / self.Y_target
                candidates.append({
                    'name': name,
                    'value': value,
                    'error': error,
                    'rel_error': rel_error
                })
        
        # Sort by error
        candidates.sort(key=lambda x: x['error'])
        
        print(f"Found {len(candidates)} candidates in range [0.1, 0.5]")
        print("\nTop 20 candidates closest to Y = 0.265:")
        print("-" * 80)
        print(f"{'Rank':<6} {'Ratio Name':<25} {'Value':<15} {'Error':<15} {'Rel Error %':<15}")
        print("-" * 80)
        
        for i, candidate in enumerate(candidates[:20], 1):
            print(f"{i:<6} {candidate['name']:<25} {candidate['value']:<15.10f} "
                  f"{candidate['error']:<15.10f} {candidate['rel_error']*100:<15.6f}")
            
            # Check if this Y produces the correct X_G
            result = self.check_scaling_factor_match(candidate['value'], candidate['name'])
            results.append(result)
        
        return results
    
    def verify_X_G_formula(self, Y: float) -> Dict:
        """Verify the complete formula: X_G = c * Y"""
        
        X_G = self.c * Y
        
        # Now check if this X_G correctly scales G
        # From the paper: G = Gravitational_Factor * (2/4) * c * Y
        # We need to find what Gravitational_Factor should be
        
        # The paper states: X_G ≈ 7.94 × 10^7
        # And: X_G * c/π ≈ 9.54 × 10^7 (close to c/π)
        
        verification = {
            'Y': Y,
            'X_G': X_G,
            'c': self.c,
            'formula': 'X_G = c × Y',
            'X_G_target': self.X_G_target,
            'match': abs(X_G - self.X_G_target) / self.X_G_target < 0.01
        }
        
        return verification
    
    def investigate_elementary_charge_connection(self) -> Dict:
        """
        Investigate the Elementary Charge connection to Y
        
        From the paper:
        e ≈ 1.602 × 10^(-19) C (dimensionless in natural units, but has dimensions in SI)
        
        The paper suggests:
        e ≈ 10 * Operational_Score_of_π * Operational_Score_of_2 * Scaling_Factor_1
        
        And that Y might be derived from operational scores related to π and √2
        """
        
        print("\n" + "=" * 80)
        print("INVESTIGATING ELEMENTARY CHARGE CONNECTION")
        print("=" * 80)
        
        e = self.elementary_charge
        
        # Operational scores are dimensionless ratios
        # Let's explore combinations that might give us Y ≈ 0.265
        
        # From the paper's hint: Y is related to Information Layer (π and √2)
        operational_pi = self.pi
        operational_sqrt2 = math.sqrt(2)
        
        # Try various combinations
        candidates = {
            '1/π': 1 / self.pi,
            '1/(π*√2)': 1 / (self.pi * math.sqrt(2)),
            'π/(π²+√2)': self.pi / (self.pi**2 + math.sqrt(2)),
            '√2/(2π)': math.sqrt(2) / (2 * self.pi),
            '1/(2*√2)': 1 / (2 * math.sqrt(2)),
            '√2/π²': math.sqrt(2) / (self.pi ** 2),
            'φ/(4π)': self.phi / (4 * self.pi),
            '1/(φ*π)': 1 / (self.phi * self.pi),
            '(√2-1)/π': (math.sqrt(2) - 1) / self.pi,
            'π/(4*e)': self.pi / (4 * self.e_const),
            '1/(π+√2)': 1 / (self.pi + math.sqrt(2)),
            '(π-2)/π²': (self.pi - 2) / (self.pi ** 2),
        }
        
        results = []
        print(f"\nTesting operational score combinations:")
        print("-" * 80)
        print(f"{'Formula':<30} {'Value':<15} {'Error from 0.265':<20}")
        print("-" * 80)
        
        for formula, value in candidates.items():
            error = abs(value - self.Y_target)
            results.append({
                'formula': formula,
                'value': value,
                'error': error,
                'rel_error': error / self.Y_target
            })
            print(f"{formula:<30} {value:<15.10f} {error:<20.10f}")
        
        # Sort by error
        results.sort(key=lambda x: x['error'])
        
        print("\n" + "=" * 80)
        print("BEST MATCH FROM OPERATIONAL SCORES:")
        best = results[0]
        print(f"Formula: {best['formula']}")
        print(f"Value: {best['value']:.10f}")
        print(f"Target: {self.Y_target:.10f}")
        print(f"Error: {best['error']:.10f} ({best['rel_error']*100:.4f}%)")
        print("=" * 80)
        
        return {
            'elementary_charge': e,
            'candidates': results,
            'best_match': results[0]
        }
    
    def comprehensive_search(self) -> Dict:
        """Perform comprehensive search for Y"""
        
        # Search through geometric ratios
        geometric_results = self.search_for_Y()
        
        # Investigate elementary charge connection
        charge_results = self.investigate_elementary_charge_connection()
        
        # Find best matches
        best_geometric = min(geometric_results, key=lambda x: x['relative_error'])
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE SEARCH RESULTS")
        print("=" * 80)
        
        print("\nBest Geometric Ratio Match:")
        print(f"  Ratio: {best_geometric['ratio_name']}")
        print(f"  Y value: {best_geometric['Y_value']:.10f}")
        print(f"  X_G calculated: {best_geometric['X_G_calculated']:.4e}")
        print(f"  X_G target: {best_geometric['X_G_target']:.4e}")
        print(f"  Error: {best_geometric['error_percentage']:.6f}%")
        
        print("\nBest Operational Score Match:")
        best_op = charge_results['best_match']
        print(f"  Formula: {best_op['formula']}")
        print(f"  Y value: {best_op['value']:.10f}")
        print(f"  Error from target: {best_op['error']:.10f} ({best_op['rel_error']*100:.4f}%)")
        
        # Verify the formula with the best match
        verification = self.verify_X_G_formula(best_geometric['Y_value'])
        
        summary = {
            'target_Y': self.Y_target,
            'target_X_G': self.X_G_target,
            'best_geometric_match': best_geometric,
            'best_operational_match': best_op,
            'verification': verification,
            'all_geometric_results': geometric_results,
            'all_operational_results': charge_results['candidates']
        }
        
        return summary


def main():
    """Main execution function"""
    
    search = GeometricConstantSearch()
    results = search.comprehensive_search()
    
    # Save results to JSON
    output_file = '/home/ubuntu/geometric_constant_search_results.json'
    
    # Convert numpy types to Python types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=convert_to_serializable)
    
    print(f"\n✓ Results saved to: {output_file}")
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review the best geometric ratio matches")
    print("2. Verify the formula G = Gravitational_Factor × (2/4) × c × Y")
    print("3. Complete the dimensional constant derivation")
    print("4. Update the cymatics study with the resolved scaling factor")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    main()

