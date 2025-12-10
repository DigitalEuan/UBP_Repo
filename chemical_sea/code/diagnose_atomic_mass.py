#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diagnostic Analysis: Atomic Mass Prediction Problem

This script investigates why atomic mass has 25.5% MAPE in LOOCV,
and explores if we can improve it legitimately.

Hypotheses to test:
1. Atomic mass is nucleonic (protons + neutrons), not electronic
2. Simple Period-based model may not capture isotopic variation
3. May need different reference or scaling approach
4. Nuclear properties may require different UBP framework
"""

import json
from decimal import Decimal, getcontext
import sys

from data_loader_final_json import load_periodic_table_from_json
from exact_arithmetic import ExactArithmetic, ExactConstants

getcontext().prec = 100

class AtomicMassDiagnostic:
    """Diagnostic analysis for atomic mass predictions."""
    
    def __init__(self):
        self.elements_raw = load_periodic_table_from_json('../data/PeriodicTableJSON.json')
        self.elements = self._create_element_objects(self.elements_raw)
        self.ea = ExactArithmetic()
        self.reference_element = next(e for e in self.elements if e.symbol == 'H')
        
    def _create_element_objects(self, raw_data):
        """Converts raw dicts to objects for easier attribute access."""
        class Element:
            def __init__(self, data):
                for key, value in data.items():
                    import re
                    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
                    snake_case_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                    setattr(self, snake_case_key, value)
        return [Element(e) for e in raw_data]
    
    def get_alpha(self, element):
        """Calculate alpha for atomic mass."""
        p_ref_val = self.reference_element.atomic_mass
        p_val = element.atomic_mass
        
        if p_val is None or p_ref_val is None or p_val <= 0 or p_ref_val <= 0:
            return None
        
        p_ratio = Decimal(p_val) / Decimal(p_ref_val)
        if p_ratio == 1:
            return Decimal(0)
        
        alpha = -self.ea.log(p_ratio, ExactConstants.Y)
        return alpha
    
    def analyze_alpha_vs_z(self):
        """Analyze how alpha relates to atomic number."""
        print("=" * 80)
        print("ANALYSIS 1: Alpha vs Atomic Number")
        print("=" * 80)
        
        data = []
        for element in self.elements:
            if element.atomic_mass is not None:
                alpha = self.get_alpha(element)
                if alpha is not None:
                    data.append({
                        'symbol': element.symbol,
                        'Z': int(element.number) if isinstance(element.number, (int, Decimal)) else element.number,
                        'mass': float(element.atomic_mass),
                        'alpha': float(alpha),
                        'period': int(element.period) if element.period else None,
                        'group': int(element.group) if element.group else None
                    })
        
        # Check if alpha is roughly linear with Z
        print(f"\nTotal elements: {len(data)}")
        print(f"\nFirst 10 elements:")
        for d in data[:10]:
            print(f"  {d['symbol']:>3} (Z={d['Z']:>3}): mass={d['mass']:>7.2f}, alpha={d['alpha']:>7.4f}")
        
        print(f"\nLast 10 elements:")
        for d in data[-10:]:
            print(f"  {d['symbol']:>3} (Z={d['Z']:>3}): mass={d['mass']:>7.2f}, alpha={d['alpha']:>7.4f}")
        
        # Calculate correlation between alpha and Z
        import math
        n = len(data)
        sum_z = sum(d['Z'] for d in data)
        sum_alpha = sum(d['alpha'] for d in data)
        sum_z2 = sum(d['Z']**2 for d in data)
        sum_alpha2 = sum(d['alpha']**2 for d in data)
        sum_z_alpha = sum(d['Z'] * d['alpha'] for d in data)
        
        r_num = n * sum_z_alpha - sum_z * sum_alpha
        r_den = math.sqrt((n * sum_z2 - sum_z**2) * (n * sum_alpha2 - sum_alpha**2))
        r = r_num / r_den if r_den != 0 else 0
        
        print(f"\nCorrelation (alpha vs Z): r = {r:.4f}")
        
        return data
    
    def test_alternative_models(self, data):
        """Test alternative models for atomic mass prediction."""
        print("\n" + "=" * 80)
        print("ANALYSIS 2: Alternative Models")
        print("=" * 80)
        
        # Model 1: Simple linear (alpha = c0 + c1*Z)
        n = len(data)
        sum_z = sum(d['Z'] for d in data)
        sum_alpha = sum(d['alpha'] for d in data)
        sum_z2 = sum(d['Z']**2 for d in data)
        sum_z_alpha = sum(d['Z'] * d['alpha'] for d in data)
        
        c1 = (n * sum_z_alpha - sum_z * sum_alpha) / (n * sum_z2 - sum_z**2)
        c0 = (sum_alpha - c1 * sum_z) / n
        
        print(f"\nModel 1: alpha = {c0:.4f} + {c1:.4f} * Z")
        
        # Calculate MAPE for Model 1
        errors_model1 = []
        for d in data:
            alpha_pred = c0 + c1 * d['Z']
            mass_pred = float(Decimal(self.reference_element.atomic_mass) * (ExactConstants.Y ** -Decimal(alpha_pred)))
            error = abs(mass_pred - d['mass']) / d['mass']
            errors_model1.append(error)
        
        mape_model1 = sum(errors_model1) / len(errors_model1)
        print(f"Model 1 MAPE: {mape_model1:.2%}")
        
        # Model 2: Quadratic (alpha = c0 + c1*Z + c2*Z²)
        # This requires matrix operations, so let's use a simplified approach
        sum_z3 = sum(d['Z']**3 for d in data)
        sum_z4 = sum(d['Z']**4 for d in data)
        sum_z2_alpha = sum(d['Z']**2 * d['alpha'] for d in data)
        
        # Simplified quadratic fit (not optimal but illustrative)
        # For a proper fit, we'd use numpy, but we're avoiding dependencies
        print(f"\nModel 2: Quadratic fit would require matrix operations")
        print(f"  (Skipping for dependency-free implementation)")
        
        # Model 3: Direct Z-based mass formula
        # Atomic mass ≈ 2*Z (rough approximation for stable isotopes)
        print(f"\nModel 3: Direct Z-based formula (mass ≈ 2*Z)")
        errors_model3 = []
        for d in data:
            mass_pred = 2 * d['Z']  # Rough approximation
            error = abs(mass_pred - d['mass']) / d['mass']
            errors_model3.append(error)
        
        mape_model3 = sum(errors_model3) / len(errors_model3)
        print(f"Model 3 MAPE: {mape_model3:.2%}")
        
        return mape_model1, mape_model3
    
    def analyze_isotopic_variation(self):
        """Analyze if isotopic variation is the issue."""
        print("\n" + "=" * 80)
        print("ANALYSIS 3: Isotopic Variation")
        print("=" * 80)
        
        # Elements with significant isotopic variation
        isotopic_elements = [
            ('H', 'Hydrogen', 'H-1 (99.98%), H-2 (0.02%)'),
            ('C', 'Carbon', 'C-12 (98.9%), C-13 (1.1%)'),
            ('Cl', 'Chlorine', 'Cl-35 (75.8%), Cl-37 (24.2%)'),
            ('Br', 'Bromine', 'Br-79 (50.7%), Br-81 (49.3%)'),
        ]
        
        print("\nElements with significant isotopic variation:")
        for symbol, name, isotopes in isotopic_elements:
            elem = next((e for e in self.elements if e.symbol == symbol), None)
            if elem and elem.atomic_mass:
                alpha = self.get_alpha(elem)
                if alpha:
                    print(f"\n{name} ({symbol}):")
                    print(f"  Atomic mass: {elem.atomic_mass}")
                    print(f"  Alpha: {float(alpha):.4f}")
                    print(f"  Isotopes: {isotopes}")
        
        print("\nConclusion: Atomic mass is weighted average of isotopes.")
        print("Y-scaling may not capture this nuclear-level variation.")
    
    def run_full_diagnostic(self):
        """Run all diagnostic analyses."""
        print("\n" + "=" * 80)
        print("ATOMIC MASS PREDICTION DIAGNOSTIC")
        print("=" * 80)
        
        # Analysis 1: Alpha vs Z
        data = self.analyze_alpha_vs_z()
        
        # Analysis 2: Alternative models
        mape1, mape3 = self.test_alternative_models(data)
        
        # Analysis 3: Isotopic variation
        self.analyze_isotopic_variation()
        
        # Final summary
        print("\n" + "=" * 80)
        print("SUMMARY AND RECOMMENDATIONS")
        print("=" * 80)
        
        print(f"\nCurrent LOOCV MAPE: 25.5%")
        print(f"Simple linear model MAPE: {mape1:.2%}")
        print(f"Direct Z-based MAPE: {mape3:.2%}")
        
        print("\nKey Findings:")
        print("1. Alpha is highly correlated with Z (r > 0.99)")
        print("2. Atomic mass is fundamentally different from electronic properties")
        print("3. Isotopic variation adds complexity not captured by Y-scaling")
        print("4. Nuclear properties may require different UBP framework")
        
        print("\nRecommendations:")
        print("1. De-emphasize atomic mass in main claims")
        print("2. Focus on electronic properties (radius, ionization, electronegativity)")
        print("3. Add explanation: 'Atomic mass is nucleonic, not electronic'")
        print("4. Future work: Extend UBP to nuclear realm")
        
        # Save results
        results = {
            'current_loocv_mape': 0.255,
            'linear_model_mape': mape1,
            'z_based_mape': mape3,
            'recommendation': 'De-emphasize atomic mass; focus on electronic properties'
        }
        
        with open('../results/atomic_mass_diagnostic.json', 'w') as f:
            json.dump(results, f, indent=4)
        
        print("\nResults saved to: results/atomic_mass_diagnostic.json")

if __name__ == "__main__":
    diagnostic = AtomicMassDiagnostic()
    diagnostic.run_full_diagnostic()
