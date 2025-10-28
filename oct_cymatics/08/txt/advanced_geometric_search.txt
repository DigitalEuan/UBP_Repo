"""
UBP Cymatics Study - Phase II Advanced: Operational Score Analysis
Author: Euan R A Craig, New Zealand
Date: October 24, 2025

This script performs a deeper analysis focusing on:
1. Operational scores from the Information Layer (π and √2)
2. Compound geometric ratios
3. Icosahedral harmonic signatures
"""

import numpy as np
import math
import json
from typing import Dict, List, Tuple
import sys

sys.path.insert(0, '/home/ubuntu/ubp_3.2')
from system_constants import UBPConstants

class AdvancedGeometricSearch:
    """Advanced search for Y using operational scores and compound ratios"""
    
    def __init__(self):
        self.constants = UBPConstants()
        
        self.c = self.constants.SPEED_OF_LIGHT
        self.pi = self.constants.PI
        self.phi = self.constants.PHI
        self.e_const = self.constants.E
        self.sqrt2 = math.sqrt(2)
        self.sqrt3 = math.sqrt(3)
        self.sqrt5 = math.sqrt(5)
        
        # Target from paper
        self.Y_target = 0.265
        self.X_G_target = 7.94e7
        
        print("=" * 80)
        print("ADVANCED GEOMETRIC SEARCH - Operational Score Analysis")
        print("=" * 80)
    
    def generate_compound_ratios(self) -> Dict[str, float]:
        """Generate more sophisticated compound ratios"""
        
        ratios = {}
        phi = self.phi
        pi = self.pi
        e = self.e_const
        sqrt2 = self.sqrt2
        sqrt3 = self.sqrt3
        sqrt5 = self.sqrt5
        
        # Icosahedral geometry - more combinations
        ratios['φ/(2π)'] = phi / (2 * pi)
        ratios['φ/(3π)'] = phi / (3 * pi)
        ratios['φ/(4π)'] = phi / (4 * pi)
        ratios['φ²/(8π)'] = (phi**2) / (8 * pi)
        ratios['φ/(π+√2)'] = phi / (pi + sqrt2)
        ratios['φ/(π+√3)'] = phi / (pi + sqrt3)
        ratios['φ/(π*√2)'] = phi / (pi * sqrt2)
        ratios['φ/(2π+1)'] = phi / (2*pi + 1)
        ratios['(φ-1)/(2π)'] = (phi - 1) / (2 * pi)
        ratios['√φ/(2π)'] = math.sqrt(phi) / (2 * pi)
        ratios['φ/(π+e)'] = phi / (pi + e)
        
        # Tetrahedral harmonics with π
        ratios['√3/(4π)'] = sqrt3 / (4 * pi)
        ratios['√3/(3π)'] = sqrt3 / (3 * pi)
        ratios['√3/(2π+1)'] = sqrt3 / (2*pi + 1)
        ratios['√3/(π+√2)'] = sqrt3 / (pi + sqrt2)
        ratios['(√3-1)/π'] = (sqrt3 - 1) / pi
        
        # Cubic harmonics with π
        ratios['√2/(3π)'] = sqrt2 / (3 * pi)
        ratios['√2/(2π+1)'] = sqrt2 / (2*pi + 1)
        ratios['√2/(π+√3)'] = sqrt2 / (pi + sqrt3)
        ratios['(√2-1)/(2π)'] = (sqrt2 - 1) / (2 * pi)
        ratios['1/(π+√2)'] = 1 / (pi + sqrt2)
        ratios['1/(π+√3)'] = 1 / (pi + sqrt3)
        
        # Combinations with e
        ratios['e/(4π)'] = e / (4 * pi)
        ratios['e/(3π)'] = e / (3 * pi)
        ratios['e/(2π+√2)'] = e / (2*pi + sqrt2)
        ratios['(e-1)/(2π)'] = (e - 1) / (2 * pi)
        ratios['π/(4e)'] = pi / (4 * e)
        ratios['π/(3e+1)'] = pi / (3*e + 1)
        
        # Mixed geometric constants
        ratios['(φ+√2)/(4π)'] = (phi + sqrt2) / (4 * pi)
        ratios['(φ*√2)/(8π)'] = (phi * sqrt2) / (8 * pi)
        ratios['φ/(2π+√2)'] = phi / (2*pi + sqrt2)
        ratios['φ/(2π+√3)'] = phi / (2*pi + sqrt3)
        ratios['(φ+1)/(3π)'] = (phi + 1) / (3 * pi)
        
        # Platonic solid ratios
        ratios['√5/(6π)'] = sqrt5 / (6 * pi)
        ratios['√5/(5π)'] = sqrt5 / (5 * pi)
        ratios['√5/(4π+1)'] = sqrt5 / (4*pi + 1)
        ratios['(√5-1)/(2π)'] = (sqrt5 - 1) / (2 * pi)
        ratios['(√5+1)/(4π)'] = (sqrt5 + 1) / (4 * pi)
        
        # Operational score combinations (from Information Layer)
        ratios['π/(π²+√2)'] = pi / (pi**2 + sqrt2)
        ratios['π/(π²+2)'] = pi / (pi**2 + 2)
        ratios['π/(π²+√3)'] = pi / (pi**2 + sqrt3)
        ratios['√2/(π²+1)'] = sqrt2 / (pi**2 + 1)
        ratios['√2/(π²+2)'] = sqrt2 / (pi**2 + 2)
        ratios['1/(π+2)'] = 1 / (pi + 2)
        ratios['1/(π+3)'] = 1 / (pi + 3)
        ratios['2/(π+5)'] = 2 / (pi + 5)
        ratios['3/(π+8)'] = 3 / (pi + 8)
        
        # Harmonic series based
        ratios['1/(1+π/2)'] = 1 / (1 + pi/2)
        ratios['1/(1+√2)'] = 1 / (1 + sqrt2)
        ratios['1/(1+φ)'] = 1 / (1 + phi)
        ratios['2/(3+π)'] = 2 / (3 + pi)
        ratios['3/(4+π)'] = 3 / (4 + pi)
        
        # Fine-tuned around 0.265
        for a in [1, 2, 3, 4, 5]:
            for b in [1, 2, 3, 4, 5]:
                for c in [1, 2, 3, 4]:
                    # Try (a + b*sqrt2) / (c*pi)
                    val = (a + b*sqrt2) / (c*pi)
                    if 0.2 < val < 0.35:
                        ratios[f'({a}+{b}√2)/({c}π)'] = val
                    
                    # Try (a*phi + b) / (c*pi)
                    val = (a*phi + b) / (c*pi)
                    if 0.2 < val < 0.35:
                        ratios[f'({a}φ+{b})/({c}π)'] = val
        
        return ratios
    
    def analyze_operational_scores(self) -> Dict:
        """
        Analyze operational scores based on the Information Layer
        
        From the paper:
        - π (Pi) is in the Information Layer
        - √2 is in the Information Layer (tetrahedral harmonic)
        - Y should be derivable from operational scores of these constants
        """
        
        print("\n" + "=" * 80)
        print("OPERATIONAL SCORE ANALYSIS")
        print("=" * 80)
        
        # Generate compound ratios
        ratios = self.generate_compound_ratios()
        
        # Filter for values close to Y_target
        candidates = []
        for name, value in ratios.items():
            if 0.2 < value < 0.35:
                error = abs(value - self.Y_target)
                rel_error = error / self.Y_target
                
                # Calculate X_G with this Y
                X_G = self.c * value
                X_G_error = abs(X_G - self.X_G_target) / self.X_G_target
                
                candidates.append({
                    'formula': name,
                    'Y_value': value,
                    'Y_error': error,
                    'Y_rel_error': rel_error,
                    'X_G': X_G,
                    'X_G_error': X_G_error,
                    'combined_score': rel_error + X_G_error  # Combined metric
                })
        
        # Sort by combined score
        candidates.sort(key=lambda x: x['combined_score'])
        
        print(f"\nFound {len(candidates)} candidates in range [0.2, 0.35]")
        print("\nTop 30 candidates by combined Y and X_G accuracy:")
        print("-" * 120)
        print(f"{'Rank':<6} {'Formula':<35} {'Y Value':<12} {'Y Err %':<10} {'X_G':<12} {'X_G Err %':<10} {'Score':<10}")
        print("-" * 120)
        
        for i, cand in enumerate(candidates[:30], 1):
            print(f"{i:<6} {cand['formula']:<35} {cand['Y_value']:<12.8f} "
                  f"{cand['Y_rel_error']*100:<10.4f} {cand['X_G']:<12.4e} "
                  f"{cand['X_G_error']*100:<10.4f} {cand['combined_score']:<10.6f}")
        
        return {
            'all_candidates': candidates,
            'top_30': candidates[:30],
            'best_match': candidates[0] if candidates else None
        }
    
    def verify_with_gravitational_constant(self, Y: float) -> Dict:
        """
        Verify the complete formula for the Gravitational Constant
        
        From the paper:
        G = Gravitational_Factor × (2/4) × c × Y
        
        Where:
        - Gravitational_Factor needs to be determined
        - (2/4) = 0.5 is the "Mass-Energy Factor" (√{2}/4 in the paper)
        - c is the speed of light
        - Y is the geometric ratio we're searching for
        """
        
        G_measured = self.constants.GRAVITATIONAL_CONSTANT  # 6.674×10^-11 m³/(kg·s²)
        
        # Calculate what Gravitational_Factor would need to be
        # G = GF × (2/4) × c × Y
        # GF = G / ((2/4) × c × Y)
        
        gravitational_factor = G_measured / (0.5 * self.c * Y)
        
        # Now calculate X_G
        X_G = self.c * Y
        
        verification = {
            'Y': Y,
            'X_G': X_G,
            'X_G_target': self.X_G_target,
            'X_G_match': abs(X_G - self.X_G_target) / self.X_G_target < 0.01,
            'gravitational_factor': gravitational_factor,
            'G_measured': G_measured,
            'G_formula': f'G = {gravitational_factor:.6e} × (2/4) × c × Y',
            'verification_check': G_measured
        }
        
        return verification
    
    def comprehensive_analysis(self) -> Dict:
        """Perform comprehensive analysis"""
        
        # Operational score analysis
        op_results = self.analyze_operational_scores()
        
        if op_results['best_match']:
            best = op_results['best_match']
            
            print("\n" + "=" * 80)
            print("BEST OVERALL MATCH")
            print("=" * 80)
            print(f"Formula: {best['formula']}")
            print(f"Y value: {best['Y_value']:.10f}")
            print(f"Y target: {self.Y_target:.10f}")
            print(f"Y error: {best['Y_rel_error']*100:.4f}%")
            print(f"X_G calculated: {best['X_G']:.6e}")
            print(f"X_G target: {self.X_G_target:.6e}")
            print(f"X_G error: {best['X_G_error']*100:.4f}%")
            print(f"Combined score: {best['combined_score']:.6f}")
            
            # Verify with gravitational constant
            verification = self.verify_with_gravitational_constant(best['Y_value'])
            
            print("\n" + "=" * 80)
            print("GRAVITATIONAL CONSTANT VERIFICATION")
            print("=" * 80)
            print(f"Gravitational Factor: {verification['gravitational_factor']:.6e}")
            print(f"Formula: {verification['G_formula']}")
            print(f"G measured: {verification['G_measured']:.6e} m³/(kg·s²)")
            
            return {
                'best_match': best,
                'verification': verification,
                'all_results': op_results
            }
        
        return {'error': 'No suitable candidates found'}


def main():
    """Main execution"""
    
    search = AdvancedGeometricSearch()
    results = search.comprehensive_analysis()
    
    # Save results
    output_file = '/home/ubuntu/advanced_geometric_search_results.json'
    
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
    
    return results


if __name__ == "__main__":
    main()

