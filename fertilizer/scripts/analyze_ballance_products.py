#!/usr/bin/env python3
"""
Ballance Agri-Nutrients Product Analysis
UBP 3.4 Chemical Coherence Assessment
"""

import sys
sys.path.append('/home/ubuntu/ubp_fertilizer_chemical_study/scripts')

from ubp_chemical_framework import UBPChemicalFramework, FertilizerComponent
import json


def analyze_ballance_products():
    """Analyze key Ballance products with realistic coherence parameters"""
    
    framework = UBPChemicalFramework()
    
    products = {
        'Superphosphate': {
            'description': 'Traditional P fertilizer - granulated, moderate quality',
            'components': [
                FertilizerComponent(
                    name="Monocalcium phosphate",
                    formula="Ca(H2PO4)2",
                    npk_contribution=(0.0, 9.0, 0.0),
                    molecular_coherence=0.75,  # Granulated, not crystalline
                    chemical_purity=0.82,      # Contains impurities
                    release_synchrony=0.70,    # Variable dissolution
                    concentration=60.0
                ),
                FertilizerComponent(
                    name="Gypsum",
                    formula="CaSO4·2H2O",
                    npk_contribution=(0.0, 0.0, 0.0),
                    molecular_coherence=0.78,
                    chemical_purity=0.85,
                    release_synchrony=0.65,
                    concentration=30.0
                ),
                FertilizerComponent(
                    name="Calcium carbonate",
                    formula="CaCO3",
                    npk_contribution=(0.0, 0.0, 0.0),
                    molecular_coherence=0.80,
                    chemical_purity=0.88,
                    release_synchrony=0.60,
                    concentration=10.0
                )
            ]
        },
        'DAP': {
            'description': 'Di-ammonium phosphate - high analysis, good quality',
            'components': [
                FertilizerComponent(
                    name="Diammonium phosphate",
                    formula="(NH4)2HPO4",
                    npk_contribution=(18.0, 46.0, 0.0),
                    molecular_coherence=0.88,  # Good crystalline
                    chemical_purity=0.94,      # High purity
                    release_synchrony=0.82,    # Good release
                    concentration=95.0
                ),
                FertilizerComponent(
                    name="Anti-caking agent",
                    formula="Various",
                    npk_contribution=(0.0, 0.0, 0.0),
                    molecular_coherence=0.60,
                    chemical_purity=0.70,
                    release_synchrony=0.50,
                    concentration=5.0
                )
            ]
        },
        'Urea': {
            'description': 'High-grade urea - excellent quality',
            'components': [
                FertilizerComponent(
                    name="Urea",
                    formula="CO(NH2)2",
                    npk_contribution=(46.0, 0.0, 0.0),
                    molecular_coherence=0.96,  # Excellent crystalline
                    chemical_purity=0.98,      # Very pure
                    release_synchrony=0.88,    # Consistent release
                    concentration=98.0
                ),
                FertilizerComponent(
                    name="Formaldehyde (coating)",
                    formula="CH2O",
                    npk_contribution=(0.0, 0.0, 0.0),
                    molecular_coherence=0.70,
                    chemical_purity=0.85,
                    release_synchrony=0.75,
                    concentration=2.0
                )
            ]
        }
    }
    
    results = {}
    
    print("="*80)
    print("BALLANCE AGRI-NUTRIENTS PRODUCT ANALYSIS")
    print("UBP 3.4 Chemical Coherence Assessment")
    print("="*80)
    
    for product_name, product_data in products.items():
        print(f"\n{'='*80}")
        print(f"PRODUCT: {product_name}")
        print(f"Description: {product_data['description']}")
        print(f"{'='*80}")
        
        result = framework.analyze_fertilizer_blend(product_data['components'])
        
        results[product_name] = {
            'description': product_data['description'],
            'system_nrci': result['system_nrci'],
            'coherence_capacity': result['coherence_capacity'],
            'synergy_factor': result['synergy_factor']
        }
    
    # Summary
    print("\n" + "="*80)
    print("COMPARATIVE SUMMARY")
    print("="*80)
    print(f"\n{'Product':<20} {'NRCI':<12} {'% of PGCI':<12} {'Synergy':<10}")
    print("-"*80)
    
    for product_name, data in results.items():
        pct_pgci = data['system_nrci'] / 0.999997 * 100
        print(f"{product_name:<20} {data['system_nrci']:<12.6f} "
              f"{pct_pgci:<12.2f}% {data['synergy_factor']:<10.4f}")
    
    # Save
    output_file = '/home/ubuntu/ubp_fertilizer_chemical_study/outputs/ballance_products.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to: {output_file}")
    
    return results


if __name__ == '__main__':
    results = analyze_ballance_products()
