#!/usr/bin/env python3
"""
Coherence Pattern Analysis
Identify patterns that govern chemical coherence in fertilizer blends
"""

import sys
sys.path.append('/home/ubuntu/ubp_fertilizer_chemical_study/scripts')

from ubp_chemical_framework import UBPChemicalFramework, FertilizerComponent
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json


def explore_parameter_space():
    """Systematically explore the parameter space to identify patterns"""
    
    framework = UBPChemicalFramework()
    
    # Test ranges for each parameter
    mol_coh_range = np.linspace(0.70, 0.99, 15)
    chem_pur_range = np.linspace(0.80, 0.995, 15)
    rel_syn_range = np.linspace(0.65, 0.96, 15)
    
    results = []
    
    print("Exploring parameter space...")
    print(f"Testing {len(mol_coh_range) * len(chem_pur_range) * len(rel_syn_range)} combinations...")
    
    for mol_coh in mol_coh_range:
        for chem_pur in chem_pur_range:
            for rel_syn in rel_syn_range:
                # Create a single-component "blend" to test
                component = FertilizerComponent(
                    name="Test Component",
                    formula="Test",
                    npk_contribution=(20.0, 10.0, 10.0),
                    molecular_coherence=mol_coh,
                    chemical_purity=chem_pur,
                    release_synchrony=rel_syn,
                    concentration=100.0
                )
                
                result = framework.analyze_fertilizer_blend([component])
                
                results.append({
                    'molecular_coherence': mol_coh,
                    'chemical_purity': chem_pur,
                    'release_synchrony': rel_syn,
                    'nrci': result['system_nrci']
                })
    
    return results


def analyze_blend_composition_patterns():
    """Analyze how blend composition affects coherence"""
    
    framework = UBPChemicalFramework()
    
    # Test 2-component blends with varying quality differences
    results_2comp = []
    
    print("\nAnalyzing 2-component blend patterns...")
    
    for high_quality in np.linspace(0.90, 0.99, 10):
        for low_quality in np.linspace(0.70, 0.89, 10):
            for ratio in [0.25, 0.50, 0.75]:  # Concentration ratios
                comp1 = FertilizerComponent(
                    name="High Quality",
                    formula="HQ",
                    npk_contribution=(20.0, 10.0, 10.0),
                    molecular_coherence=high_quality,
                    chemical_purity=high_quality,
                    release_synchrony=high_quality,
                    concentration=ratio * 100
                )
                
                comp2 = FertilizerComponent(
                    name="Low Quality",
                    formula="LQ",
                    npk_contribution=(15.0, 15.0, 15.0),
                    molecular_coherence=low_quality,
                    chemical_purity=low_quality,
                    release_synchrony=low_quality,
                    concentration=(1 - ratio) * 100
                )
                
                result = framework.analyze_fertilizer_blend([comp1, comp2])
                
                results_2comp.append({
                    'high_quality': high_quality,
                    'low_quality': low_quality,
                    'ratio': ratio,
                    'quality_gap': high_quality - low_quality,
                    'nrci': result['system_nrci']
                })
    
    # Test 3-component blends
    results_3comp = []
    
    print("Analyzing 3-component blend patterns...")
    
    for avg_quality in np.linspace(0.85, 0.95, 10):
        for variance in np.linspace(0.01, 0.10, 10):
            comp1 = FertilizerComponent(
                name="Comp1",
                formula="C1",
                npk_contribution=(20.0, 10.0, 10.0),
                molecular_coherence=avg_quality + variance,
                chemical_purity=avg_quality + variance,
                release_synchrony=avg_quality + variance,
                concentration=33.3
            )
            
            comp2 = FertilizerComponent(
                name="Comp2",
                formula="C2",
                npk_contribution=(15.0, 15.0, 15.0),
                molecular_coherence=avg_quality,
                chemical_purity=avg_quality,
                release_synchrony=avg_quality,
                concentration=33.3
            )
            
            comp3 = FertilizerComponent(
                name="Comp3",
                formula="C3",
                npk_contribution=(10.0, 20.0, 10.0),
                molecular_coherence=avg_quality - variance,
                chemical_purity=avg_quality - variance,
                release_synchrony=avg_quality - variance,
                concentration=33.4
            )
            
            result = framework.analyze_fertilizer_blend([comp1, comp2, comp3])
            
            results_3comp.append({
                'avg_quality': avg_quality,
                'variance': variance,
                'nrci': result['system_nrci']
            })
    
    return results_2comp, results_3comp


def identify_patterns(param_results, blend_2comp, blend_3comp):
    """Identify key patterns from the data"""
    
    patterns = {}
    
    # Pattern 1: Which parameter matters most?
    param_data = np.array([[r['molecular_coherence'], r['chemical_purity'], 
                            r['release_synchrony'], r['nrci']] for r in param_results])
    
    # Calculate correlation with NRCI
    mol_coh_corr = np.corrcoef(param_data[:, 0], param_data[:, 3])[0, 1]
    chem_pur_corr = np.corrcoef(param_data[:, 1], param_data[:, 3])[0, 1]
    rel_syn_corr = np.corrcoef(param_data[:, 2], param_data[:, 3])[0, 1]
    
    patterns['parameter_importance'] = {
        'molecular_coherence': mol_coh_corr,
        'chemical_purity': chem_pur_corr,
        'release_synchrony': rel_syn_corr
    }
    
    # Pattern 2: Optimal parameter ranges
    high_nrci = [r for r in param_results if r['nrci'] > 0.990]
    
    if high_nrci:
        patterns['optimal_ranges'] = {
            'molecular_coherence': {
                'min': min(r['molecular_coherence'] for r in high_nrci),
                'max': max(r['molecular_coherence'] for r in high_nrci),
                'mean': np.mean([r['molecular_coherence'] for r in high_nrci])
            },
            'chemical_purity': {
                'min': min(r['chemical_purity'] for r in high_nrci),
                'max': max(r['chemical_purity'] for r in high_nrci),
                'mean': np.mean([r['chemical_purity'] for r in high_nrci])
            },
            'release_synchrony': {
                'min': min(r['release_synchrony'] for r in high_nrci),
                'max': max(r['release_synchrony'] for r in high_nrci),
                'mean': np.mean([r['release_synchrony'] for r in high_nrci])
            }
        }
    
    # Pattern 3: Blend composition effects
    blend_2_data = np.array([[r['quality_gap'], r['ratio'], r['nrci']] for r in blend_2comp])
    
    patterns['blend_composition'] = {
        'quality_gap_effect': np.corrcoef(blend_2_data[:, 0], blend_2_data[:, 2])[0, 1],
        'ratio_effect': np.corrcoef(blend_2_data[:, 1], blend_2_data[:, 2])[0, 1]
    }
    
    # Pattern 4: Variance effects in 3-component blends
    blend_3_data = np.array([[r['avg_quality'], r['variance'], r['nrci']] for r in blend_3comp])
    
    patterns['variance_effects'] = {
        'avg_quality_effect': np.corrcoef(blend_3_data[:, 0], blend_3_data[:, 2])[0, 1],
        'variance_penalty': np.corrcoef(blend_3_data[:, 1], blend_3_data[:, 2])[0, 1]
    }
    
    return patterns


def main():
    """Main analysis function"""
    
    print("="*80)
    print("COHERENCE PATTERN ANALYSIS")
    print("="*80)
    
    # Explore parameter space
    param_results = explore_parameter_space()
    
    # Analyze blend composition
    blend_2comp, blend_3comp = analyze_blend_composition_patterns()
    
    # Identify patterns
    patterns = identify_patterns(param_results, blend_2comp, blend_3comp)
    
    # Save results
    output_data = {
        'parameter_space': param_results,
        'blend_2component': blend_2comp,
        'blend_3component': blend_3comp,
        'patterns': patterns
    }
    
    with open('/home/ubuntu/ubp_fertilizer_chemical_study/outputs/coherence_patterns.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    # Print summary
    print("\n" + "="*80)
    print("PATTERN SUMMARY")
    print("="*80)
    
    print("\n1. PARAMETER IMPORTANCE (Correlation with NRCI):")
    for param, corr in patterns['parameter_importance'].items():
        print(f"   {param:25s}: {corr:+.4f}")
    
    if 'optimal_ranges' in patterns:
        print("\n2. OPTIMAL PARAMETER RANGES (for NRCI > 0.990):")
        for param, ranges in patterns['optimal_ranges'].items():
            print(f"   {param:25s}: {ranges['min']:.3f} - {ranges['max']:.3f} (mean: {ranges['mean']:.3f})")
    
    print("\n3. BLEND COMPOSITION EFFECTS:")
    print(f"   Quality gap effect:        {patterns['blend_composition']['quality_gap_effect']:+.4f}")
    print(f"   Ratio effect:              {patterns['blend_composition']['ratio_effect']:+.4f}")
    
    print("\n4. VARIANCE EFFECTS (3-component blends):")
    print(f"   Avg quality effect:        {patterns['variance_effects']['avg_quality_effect']:+.4f}")
    print(f"   Variance penalty:          {patterns['variance_effects']['variance_penalty']:+.4f}")
    
    print("\n" + "="*80)
    print("Data saved to: /home/ubuntu/ubp_fertilizer_chemical_study/outputs/coherence_patterns.json")
    print("="*80)
    
    return output_data


if __name__ == '__main__':
    data = main()
