#!/usr/bin/env python3
"""
Optimized Fertilizer Formulations
UBP 3.4 Chemical Coherence Optimization
"""

import sys
sys.path.append('/home/ubuntu/ubp_fertilizer_chemical_study/scripts')

from ubp_chemical_framework import UBPChemicalFramework, FertilizerComponent
import json


def design_optimized_formulations():
    """Design 3 optimized formulations with high NRCI"""
    
    framework = UBPChemicalFramework()
    
    formulations = {
        'UBP CoherencePro™': {
            'description': 'Ultra-pure crystalline NPK blend with controlled-release coating',
            'target_crops': 'High-value crops (horticulture, viticulture)',
            'components': [
                FertilizerComponent(
                    name="Ultra-pure urea (pharmaceutical grade)",
                    formula="CO(NH2)2",
                    npk_contribution=(46.0, 0.0, 0.0),
                    molecular_coherence=0.99,  # Pharmaceutical grade crystalline
                    chemical_purity=0.995,     # Ultra-pure
                    release_synchrony=0.95,    # Polymer-coated slow release
                    concentration=40.0
                ),
                FertilizerComponent(
                    name="Monoammonium phosphate (technical grade)",
                    formula="NH4H2PO4",
                    npk_contribution=(11.0, 52.0, 0.0),
                    molecular_coherence=0.96,
                    chemical_purity=0.98,
                    release_synchrony=0.93,
                    concentration=35.0
                ),
                FertilizerComponent(
                    name="Potassium sulfate (crystalline)",
                    formula="K2SO4",
                    npk_contribution=(0.0, 0.0, 50.0),
                    molecular_coherence=0.97,
                    chemical_purity=0.99,
                    release_synchrony=0.94,
                    concentration=25.0
                )
            ],
            'estimated_cost_per_tonne': 850,
            'application_rate_kg_ha': 200
        },
        'UBP SyncroBlend™': {
            'description': 'Synchronized-release NPK with micronutrient package',
            'target_crops': 'Pasture, broadacre crops',
            'components': [
                FertilizerComponent(
                    name="Polymer-coated urea",
                    formula="CO(NH2)2 + polymer",
                    npk_contribution=(44.0, 0.0, 0.0),
                    molecular_coherence=0.94,
                    chemical_purity=0.96,
                    release_synchrony=0.96,  # Excellent synchronization
                    concentration=45.0
                ),
                FertilizerComponent(
                    name="Triple superphosphate (granular)",
                    formula="Ca(H2PO4)2",
                    npk_contribution=(0.0, 46.0, 0.0),
                    molecular_coherence=0.90,
                    chemical_purity=0.94,
                    release_synchrony=0.88,
                    concentration=30.0
                ),
                FertilizerComponent(
                    name="Potassium chloride (fine crystalline)",
                    formula="KCl",
                    npk_contribution=(0.0, 0.0, 60.0),
                    molecular_coherence=0.98,
                    chemical_purity=0.99,
                    release_synchrony=0.90,
                    concentration=25.0
                )
            ],
            'estimated_cost_per_tonne': 650,
            'application_rate_kg_ha': 250
        },
        'UBP PureBalance™': {
            'description': 'High-purity balanced NPK for precision agriculture',
            'target_crops': 'Precision agriculture, controlled environments',
            'components': [
                FertilizerComponent(
                    name="Calcium nitrate (crystalline)",
                    formula="Ca(NO3)2",
                    npk_contribution=(15.5, 0.0, 0.0),
                    molecular_coherence=0.97,
                    chemical_purity=0.99,
                    release_synchrony=0.92,
                    concentration=40.0
                ),
                FertilizerComponent(
                    name="Monopotassium phosphate (reagent grade)",
                    formula="KH2PO4",
                    npk_contribution=(0.0, 52.0, 34.0),
                    molecular_coherence=0.98,
                    chemical_purity=0.995,
                    release_synchrony=0.94,
                    concentration=35.0
                ),
                FertilizerComponent(
                    name="Potassium nitrate (crystalline)",
                    formula="KNO3",
                    npk_contribution=(13.0, 0.0, 44.0),
                    molecular_coherence=0.97,
                    chemical_purity=0.99,
                    release_synchrony=0.93,
                    concentration=25.0
                )
            ],
            'estimated_cost_per_tonne': 950,
            'application_rate_kg_ha': 180
        }
    }
    
    results = {}
    
    print("="*80)
    print("OPTIMIZED FERTILIZER FORMULATIONS")
    print("UBP 3.4 Chemical Coherence Optimization")
    print("="*80)
    
    for formulation_name, formulation_data in formulations.items():
        print(f"\n{'='*80}")
        print(f"FORMULATION: {formulation_name}")
        print(f"Description: {formulation_data['description']}")
        print(f"Target crops: {formulation_data['target_crops']}")
        print(f"Estimated cost: ${formulation_data['estimated_cost_per_tonne']}/tonne")
        print(f"Application rate: {formulation_data['application_rate_kg_ha']} kg/ha")
        print(f"{'='*80}")
        
        result = framework.analyze_fertilizer_blend(formulation_data['components'])
        
        results[formulation_name] = {
            'description': formulation_data['description'],
            'target_crops': formulation_data['target_crops'],
            'system_nrci': result['system_nrci'],
            'coherence_capacity': result['coherence_capacity'],
            'synergy_factor': result['synergy_factor'],
            'cost_per_tonne': formulation_data['estimated_cost_per_tonne'],
            'application_rate_kg_ha': formulation_data['application_rate_kg_ha']
        }
    
    # Summary
    print("\n" + "="*80)
    print("COMPARATIVE SUMMARY")
    print("="*80)
    print(f"\n{'Formulation':<25} {'NRCI':<10} {'Synergy':<10} {'Cost ($/t)':<12}")
    print("-"*80)
    
    for formulation_name, data in results.items():
        print(f"{formulation_name:<25} {data['system_nrci']:<10.6f} "
              f"{data['synergy_factor']:<10.4f} ${data['cost_per_tonne']:<11}")
    
    # Comparison with Ballance products
    print("\n" + "="*80)
    print("IMPROVEMENT OVER CURRENT BALLANCE PRODUCTS")
    print("="*80)
    
    ballance_baseline = {
        'Superphosphate': 0.950426,
        'DAP': 0.972075,
        'Urea': 0.986215
    }
    
    print(f"\n{'Optimized Formulation':<25} {'NRCI':<10} {'vs Super':<12} {'vs DAP':<12} {'vs Urea':<12}")
    print("-"*80)
    
    for formulation_name, data in results.items():
        vs_super = (data['system_nrci'] - ballance_baseline['Superphosphate']) / ballance_baseline['Superphosphate'] * 100
        vs_dap = (data['system_nrci'] - ballance_baseline['DAP']) / ballance_baseline['DAP'] * 100
        vs_urea = (data['system_nrci'] - ballance_baseline['Urea']) / ballance_baseline['Urea'] * 100
        
        print(f"{formulation_name:<25} {data['system_nrci']:<10.6f} "
              f"+{vs_super:>6.2f}%    +{vs_dap:>6.2f}%    +{vs_urea:>6.2f}%")
    
    # Save
    output_file = '/home/ubuntu/ubp_fertilizer_chemical_study/outputs/optimized_formulations.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to: {output_file}")
    
    return results


if __name__ == '__main__':
    results = design_optimized_formulations()
