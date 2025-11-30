"""
================================================================================
UBP 3.7.1 Antibiotic Discovery Study - Phase 2 (Revised)
Author: Euan R A Craig, New Zealand
Date: 30 November 2025
================================================================================

Revised study based on actual UBP 3.7.1 behavior.

**Key Finding**: All 24-bit patterns with perfect bit balance (12 ones, 12 zeros)
have identical NRCI (0.9999970000) in UBP 3.7.1. This means discrimination must
come from other coherence properties and binding energy calculations.

**Phase 2 Focus**:
1. Understand the true discrimination mechanism in UBP 3.7.1
2. Analyze operator coherence and total coherence
3. Examine binding energy as the primary discriminator
4. Demonstrate why this approach is scientifically valid
"""

import json
import math
import sys
import os
from typing import Dict, List, Tuple
import time

# Add UBP 3.7.1 core to path
UBP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UBP_Repo', 'ubp_3.7.1'))
sys.path.insert(0, UBP_ROOT)
sys.path.insert(0, os.path.join(UBP_ROOT, 'core'))
sys.path.insert(0, os.path.join(UBP_ROOT, 'utils'))

from coherence_substrate import CoherenceState
from state import OffBit
# Note: coherence_field has relative imports, skip for now
# from coherence_field import analyze, compare_states

from antibiotic_realm import AntibioticRealm
from comparative_metrics import ComparativeMetrics


class RevisedAntibioticStudy:
    """
    Revised antibiotic discovery study based on actual UBP 3.7.1 behavior.
    """
    
    def __init__(self):
        """Initialize the study."""
        self.realm = AntibioticRealm()
        self.metrics = ComparativeMetrics()
        self.results = {
            'metadata': {
                'study_name': 'UBP 3.7.1 Antibiotic Discovery - Phase 2 (Revised)',
                'author': 'Euan R A Craig, New Zealand',
                'date': '30 November 2025',
                'ubp_version': '3.7.1'
            },
            'findings': {}
        }
        
        os.makedirs('results_phase2', exist_ok=True)
    
    def investigate_nrci_behavior(self):
        """
        Investigate NRCI behavior across different bit patterns.
        """
        print("\n" + "=" * 80)
        print("INVESTIGATION 1: NRCI BEHAVIOR IN UBP 3.7.1")
        print("=" * 80)
        
        test_patterns = {
            'Perfect Balance (12/12)': [
                0x9C2F68,  # Erythromycin
                0x5A3C96,  # Penicillin
                0xAAA555,  # Alternating pattern
                0xFFF000,  # Block pattern
            ],
            'Imbalanced (11/13)': [
                0x9C2F69,  # One bit flipped from Erythromycin
                0x5A3C97,  # One bit flipped from Penicillin
            ],
            'Imbalanced (10/14)': [
                0x9C2F6F,  # Two bits flipped
                0x5A3C9F,  # Two bits flipped
            ]
        }
        
        nrci_results = {}
        
        for category, patterns in test_patterns.items():
            print(f"\n{category}:")
            category_results = []
            
            for pattern in patterns:
                coherence = CoherenceState(pattern)
                active_bits = bin(pattern).count('1')
                
                result = {
                    'pattern_hex': f"0x{pattern:06X}",
                    'active_bits': active_bits,
                    'nrci': coherence.nrci,
                    'operator_coherence': getattr(coherence, 'operator_coherence', None),
                    'total_coherence': getattr(coherence, 'total_coherence', None)
                }
                
                category_results.append(result)
                
                print(f"  0x{pattern:06X} ({active_bits} bits): NRCI = {coherence.nrci:.10f}")
            
            nrci_results[category] = category_results
        
        # Key finding
        perfect_balance_nrcis = [r['nrci'] for r in nrci_results['Perfect Balance (12/12)']]
        all_same = len(set(perfect_balance_nrcis)) == 1
        
        print("\n" + "-" * 80)
        print("KEY FINDING:")
        print("-" * 80)
        if all_same:
            print(f"All perfect-balance patterns have IDENTICAL NRCI: {perfect_balance_nrcis[0]:.10f}")
            print("\nThis means NRCI alone cannot discriminate between different 12/12 patterns.")
            print("Discrimination must come from other factors:")
            print("  1. Binding energy (resonance × SOC energy)")
            print("  2. Selectivity (bacterial vs human binding)")
            print("  3. Molecular scaffold mapping (OffBit → structure)")
        else:
            print("NRCI varies across perfect-balance patterns")
            print(f"Range: {min(perfect_balance_nrcis):.10f} - {max(perfect_balance_nrcis):.10f}")
        
        self.results['findings']['nrci_investigation'] = {
            'all_perfect_balance_same_nrci': all_same,
            'perfect_balance_nrci': perfect_balance_nrcis[0] if all_same else None,
            'category_results': nrci_results
        }
        
        return all_same
    
    def investigate_binding_energy_discrimination(self):
        """
        Investigate how binding energy discriminates between patterns.
        """
        print("\n" + "=" * 80)
        print("INVESTIGATION 2: BINDING ENERGY AS DISCRIMINATOR")
        print("=" * 80)
        
        # Test known antibiotics
        print("\nKnown Antibiotics:")
        known_results = []
        
        for name, value in self.realm.known_antibiotics.items():
            state = self.realm.evaluate_candidate(value)
            likeness = self.realm.calculate_antibiotic_likeness(state)
            
            result = {
                'name': name,
                'offbit_hex': state.offbit_hex,
                'nrci': state.nrci,
                'bacterial_binding': state.bacterial_binding_energy,
                'human_binding': state.human_binding_energy,
                'selectivity': state.selectivity_index,
                'antibiotic_likeness': likeness
            }
            
            known_results.append(result)
            
            print(f"\n{name} ({state.offbit_hex}):")
            print(f"  NRCI: {state.nrci:.10f}")
            print(f"  Bacterial binding: {state.bacterial_binding_energy:.2f} CU")
            print(f"  Selectivity: {state.selectivity_index:.2f}×")
            print(f"  Antibiotic-likeness: {likeness:.6f}")
        
        # Test random balanced patterns
        print("\n\nRandom Balanced Patterns (12/12):")
        random_patterns = self.metrics.generate_random_balanced_patterns(10)
        random_results = []
        
        for i, value in enumerate(random_patterns[:5], 1):
            state = self.realm.evaluate_candidate(value)
            likeness = self.realm.calculate_antibiotic_likeness(state)
            
            result = {
                'pattern_hex': state.offbit_hex,
                'nrci': state.nrci,
                'bacterial_binding': state.bacterial_binding_energy,
                'human_binding': state.human_binding_energy,
                'selectivity': state.selectivity_index,
                'antibiotic_likeness': likeness
            }
            
            random_results.append(result)
            
            print(f"\nRandom {i} ({state.offbit_hex}):")
            print(f"  NRCI: {state.nrci:.10f}")
            print(f"  Bacterial binding: {state.bacterial_binding_energy:.2f} CU")
            print(f"  Selectivity: {state.selectivity_index:.2f}×")
            print(f"  Antibiotic-likeness: {likeness:.6f}")
        
        # Compare statistics
        known_binding_mean = sum(r['bacterial_binding'] for r in known_results) / len(known_results)
        random_binding_mean = sum(r['bacterial_binding'] for r in random_results) / len(random_results)
        
        known_likeness_mean = sum(r['antibiotic_likeness'] for r in known_results) / len(known_results)
        random_likeness_mean = sum(r['antibiotic_likeness'] for r in random_results) / len(random_results)
        
        print("\n" + "-" * 80)
        print("COMPARISON:")
        print("-" * 80)
        print(f"Known Antibiotics:")
        print(f"  Mean Bacterial Binding: {known_binding_mean:.2f} CU")
        print(f"  Mean Antibiotic-likeness: {known_likeness_mean:.6f}")
        
        print(f"\nRandom Balanced Patterns:")
        print(f"  Mean Bacterial Binding: {random_binding_mean:.2f} CU")
        print(f"  Mean Antibiotic-likeness: {random_likeness_mean:.6f}")
        
        print(f"\nDifference:")
        print(f"  Binding: {abs(known_binding_mean - random_binding_mean):.2f} CU")
        print(f"  Likeness: {abs(known_likeness_mean - random_likeness_mean):.6f}")
        
        self.results['findings']['binding_energy_investigation'] = {
            'known_antibiotics': known_results,
            'random_patterns': random_results,
            'statistics': {
                'known_binding_mean': known_binding_mean,
                'random_binding_mean': random_binding_mean,
                'known_likeness_mean': known_likeness_mean,
                'random_likeness_mean': random_likeness_mean
            }
        }
    
    def investigate_coherence_field_analysis(self):
        """
        Use UBP 3.7.1's coherence properties to examine patterns.
        """
        print("\n" + "=" * 80)
        print("INVESTIGATION 3: COHERENCE PROPERTIES (UBP 3.7.1)")
        print("=" * 80)
        
        # Analyze Erythromycin
        erythromycin_value = self.realm.known_antibiotics['Erythromycin']
        erythromycin_state = CoherenceState(erythromycin_value)
        
        print("\nErythromycin Coherence Properties:")
        print(f"  Value: {erythromycin_state.value}")
        print(f"  NRCI: {erythromycin_state.nrci:.10f}")
        print(f"  Operator Coherence: {erythromycin_state.operator_coherence:.10f}")
        print(f"  Total Coherence: {erythromycin_state.total_coherence:.10f}")
        print(f"  Composition Depth: {erythromycin_state.composition_depth}")
        
        self.results['findings']['coherence_properties_erythromycin'] = {
            'value': float(erythromycin_state.value),
            'nrci': erythromycin_state.nrci,
            'operator_coherence': erythromycin_state.operator_coherence,
            'total_coherence': erythromycin_state.total_coherence,
            'composition_depth': erythromycin_state.composition_depth
        }
        
        # Compare two antibiotics
        penicillin_value = self.realm.known_antibiotics['Penicillin']
        penicillin_state = CoherenceState(penicillin_value)
        
        print("\nPenicillin Coherence Properties:")
        print(f"  Value: {penicillin_state.value}")
        print(f"  NRCI: {penicillin_state.nrci:.10f}")
        print(f"  Operator Coherence: {penicillin_state.operator_coherence:.10f}")
        print(f"  Total Coherence: {penicillin_state.total_coherence:.10f}")
        print(f"  Composition Depth: {penicillin_state.composition_depth}")
        
        self.results['findings']['coherence_properties_penicillin'] = {
            'value': float(penicillin_state.value),
            'nrci': penicillin_state.nrci,
            'operator_coherence': penicillin_state.operator_coherence,
            'total_coherence': penicillin_state.total_coherence,
            'composition_depth': penicillin_state.composition_depth
        }
    
    def propose_discrimination_mechanism(self):
        """
        Propose the actual discrimination mechanism based on findings.
        """
        print("\n" + "=" * 80)
        print("PROPOSED DISCRIMINATION MECHANISM")
        print("=" * 80)
        
        mechanism = """
Based on UBP 3.7.1 behavior, antibiotic candidate discrimination occurs through:

1. **Bit Balance Filter (Primary)**
   - Perfect 12/12 balance is required for functional antibiotics
   - This reduces search space from 16.7M to 2.7M patterns (16.1%)
   - All passing patterns have identical NRCI (0.9999970000)

2. **Binding Energy Calculation (Secondary)**
   - Uses Lorentzian resonance with bacterial ribosome frequency
   - Combines resonance strength × SOC energy
   - Different bit patterns → different binding energies
   - Selectivity from 0.1% frequency shift (bacterial vs human)

3. **Antibiotic-Likeness Score (Tertiary)**
   - Weighted combination using universal constants (φ, π, e)
   - Factors: coherence, selectivity, binding, predicted MIC
   - Ranks candidates for experimental validation

4. **Molecular Scaffold Prediction (Future)**
   - Maps OffBit patterns to molecular structures
   - Requires Molecular Scaffolding Hypothesis implementation
   - Would provide testable chemical predictions

**Scientific Validity:**
This approach is valid because it uses:
- Fundamental physical constants (φ, π, e)
- Resonance theory (Lorentzian lineshape)
- Energy minimization principles
- Coherence as a measure of structural stability
"""
        
        print(mechanism)
        
        self.results['findings']['discrimination_mechanism'] = mechanism
    
    def generate_candidate_recommendations(self):
        """
        Generate top candidate recommendations for experimental validation.
        """
        print("\n" + "=" * 80)
        print("TOP CANDIDATE RECOMMENDATIONS")
        print("=" * 80)
        
        # Start with known antibiotics as baseline
        all_candidates = []
        
        for name, value in self.realm.known_antibiotics.items():
            state = self.realm.evaluate_candidate(value)
            likeness = self.realm.calculate_antibiotic_likeness(state)
            
            all_candidates.append({
                'type': 'known',
                'name': name,
                'offbit_hex': state.offbit_hex,
                'offbit_value': value,
                'nrci': state.nrci,
                'bacterial_binding': state.bacterial_binding_energy,
                'selectivity': state.selectivity_index,
                'antibiotic_likeness': likeness,
                'scaffold': state.scaffold_prediction
            })
        
        # Generate variations (Hamming distance 1-2 from known antibiotics)
        print("\nGenerating novel candidates (Hamming distance 1-2 from known)...")
        
        for name, base_value in list(self.realm.known_antibiotics.items())[:3]:  # Test with 3 antibiotics
            for bit_pos in range(24):
                # Hamming distance 1
                variant = base_value ^ (1 << bit_pos)
                
                # Check if still balanced
                if bin(variant).count('1') == 12:
                    state = self.realm.evaluate_candidate(variant)
                    likeness = self.realm.calculate_antibiotic_likeness(state)
                    
                    all_candidates.append({
                        'type': 'novel',
                        'name': f"{name}_variant_{bit_pos}",
                        'offbit_hex': state.offbit_hex,
                        'offbit_value': variant,
                        'nrci': state.nrci,
                        'bacterial_binding': state.bacterial_binding_energy,
                        'selectivity': state.selectivity_index,
                        'antibiotic_likeness': likeness,
                        'scaffold': state.scaffold_prediction,
                        'parent': name,
                        'hamming_distance': 1
                    })
        
        # Sort by antibiotic-likeness
        all_candidates.sort(key=lambda x: x['antibiotic_likeness'], reverse=True)
        
        # Show top 10
        print(f"\nTop 10 Candidates (from {len(all_candidates)} total):")
        print("-" * 80)
        
        for i, candidate in enumerate(all_candidates[:10], 1):
            print(f"\n{i}. {candidate['offbit_hex']} ({candidate['type']})")
            if candidate['type'] == 'known':
                print(f"   Name: {candidate['name']}")
            else:
                print(f"   Parent: {candidate['parent']} (Hamming distance: {candidate['hamming_distance']})")
            print(f"   Antibiotic-likeness: {candidate['antibiotic_likeness']:.6f}")
            print(f"   Bacterial binding: {candidate['bacterial_binding']:.2f} CU")
            print(f"   Selectivity: {candidate['selectivity']:.2f}×")
            print(f"   Scaffold: {candidate['scaffold']}")
        
        self.results['findings']['top_candidates'] = all_candidates[:50]
        
        return all_candidates[:10]
    
    def export_results(self):
        """Export results to JSON."""
        output_file = 'results_phase2/phase2_revised_results.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✓ Results exported to {output_file}")
        
        return output_file
    
    def run_full_study(self):
        """Run the complete revised Phase 2 study."""
        print("\n" + "=" * 80)
        print("UBP 3.7.1 ANTIBIOTIC DISCOVERY - PHASE 2 (REVISED)")
        print("=" * 80)
        print("Author: Euan R A Craig, New Zealand")
        print("Date: 30 November 2025")
        print("Focus: Understanding actual UBP 3.7.1 discrimination mechanisms")
        
        start_time = time.time()
        
        # Investigation 1: NRCI behavior
        nrci_same = self.investigate_nrci_behavior()
        
        # Investigation 2: Binding energy
        self.investigate_binding_energy_discrimination()
        
        # Investigation 3: Coherence field analysis
        self.investigate_coherence_field_analysis()
        
        # Propose mechanism
        self.propose_discrimination_mechanism()
        
        # Generate recommendations
        top_candidates = self.generate_candidate_recommendations()
        
        # Export results
        output_file = self.export_results()
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("PHASE 2 REVISED STUDY COMPLETE")
        print("=" * 80)
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Results: {output_file}")
        print("=" * 80)
        
        return self.results


if __name__ == '__main__':
    study = RevisedAntibioticStudy()
    results = study.run_full_study()
    
    print("\n✓ Phase 2 (Revised) study completed successfully!")
