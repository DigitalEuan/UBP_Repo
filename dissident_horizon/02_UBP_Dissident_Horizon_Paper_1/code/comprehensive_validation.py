#!/usr/bin/env python3.11
"""
Comprehensive Dissident Horizon Validation Study
Runs 100+ test cases across all realms with full statistical analysis
Author: Euan Craig, New Zealand
Date: November 14, 2025
Framework: UBP 3.5
"""

import sys
import json
import math
from pathlib import Path

# Add UBP path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState
from dissident_horizon_oracle import DissidentHorizonOracle
from hex_dictionary_advanced import AdvancedHexDictionaryAnalyzer
import numpy as np

def generate_test_scenarios(num_tests=100):
    """Generate comprehensive test scenarios across all realms"""
    scenarios = []
    
    # Quantum realm scenarios (25 tests)
    for i in range(25):
        nrci_base = 0.999997
        deficit = 0.0015 + (np.random.randn() * 0.0002)  # 0.15% ± noise
        nrci = nrci_base * (1 - deficit)
        
        scenarios.append({
            'realm': 'quantum',
            'type': 'dissident' if abs(deficit - 0.0015) < 0.0005 else 'normal',
            'expected_type': 'harmful' if deficit > 0.002 else 'beneficial' if deficit < 0.001 else 'neutral',
            'nrci': nrci,
            'frequency': 1e15 * (1 + np.random.randn() * 0.1),
            'description': f'Quantum state {i+1}: NRCI={nrci:.6f}'
        })
    
    # Biological realm scenarios (25 tests)
    for i in range(25):
        nrci_base = 0.999997
        deficit = 0.0015 + (np.random.randn() * 0.0002)
        nrci = nrci_base * (1 - deficit)
        
        scenarios.append({
            'realm': 'biological',
            'type': 'dissident' if abs(deficit - 0.0015) < 0.0005 else 'normal',
            'expected_type': 'harmful' if deficit > 0.002 else 'beneficial' if deficit < 0.001 else 'neutral',
            'nrci': nrci,
            'frequency': 1e3 * (1 + np.random.randn() * 0.1),
            'description': f'Biological state {i+1}: NRCI={nrci:.6f}'
        })
    
    # Cosmological realm scenarios (25 tests)
    for i in range(25):
        nrci_base = 0.999997
        deficit = 0.0015 + (np.random.randn() * 0.0002)
        nrci = nrci_base * (1 - deficit)
        
        scenarios.append({
            'realm': 'cosmological',
            'type': 'dissident' if abs(deficit - 0.0015) < 0.0005 else 'normal',
            'expected_type': 'neutral',  # Dark matter is neutral
            'nrci': nrci,
            'frequency': 1e-18 * (1 + np.random.randn() * 0.1),
            'description': f'Cosmological state {i+1}: NRCI={nrci:.6f}'
        })
    
    # Electromagnetic realm scenarios (25 tests)
    for i in range(25):
        nrci_base = 0.999997
        deficit = 0.0015 + (np.random.randn() * 0.0002)
        nrci = nrci_base * (1 - deficit)
        
        scenarios.append({
            'realm': 'electromagnetic',
            'type': 'dissident' if abs(deficit - 0.0015) < 0.0005 else 'normal',
            'expected_type': 'beneficial' if deficit < 0.0018 else 'harmful',
            'nrci': nrci,
            'frequency': 5e14 * (1 + np.random.randn() * 0.1),
            'description': f'EM state {i+1}: NRCI={nrci:.6f}'
        })
    
    return scenarios

def create_synthetic_data(scenario):
    """Create synthetic data matrix and coherence states for a scenario"""
    # Create data matrix with characteristics matching the scenario
    size = 50
    data = np.random.randn(size, size)
    
    # Add structure based on NRCI
    if scenario['nrci'] < 0.999:
        # Add dissident-like structure: low connectivity, stable attractor
        for i in range(size):
            for j in range(i+1, min(i+5, size)):
                data[i, j] = data[i, j] * 0.3  # Reduce connectivity
                data[j, i] = data[i, j]
    
    # Create coherence states with history
    states = []
    for i in range(20):
        # Simulate temporal decay for dissidents
        if scenario['type'] == 'dissident':
            nrci_current = scenario['nrci'] * (1 - 0.01 * i)  # Memory decay
        else:
            nrci_current = scenario['nrci'] * (1 - 0.001 * i)  # Slow decay
        
        # Convert NRCI to log_nrci_error
        log_error = math.log(1 - max(0.95, nrci_current))
        state = CoherenceState(
            value=scenario['frequency'] * (1 + 0.01 * i),
            log_nrci_error=log_error,
            net_refinements=0
        )
        states.append(state)
    
    return data, states

def run_comprehensive_validation():
    """Run comprehensive validation with 100+ test cases"""
    print("=" * 80)
    print("COMPREHENSIVE DISSIDENT HORIZON VALIDATION STUDY")
    print("=" * 80)
    print()
    
    # Generate test scenarios
    print("Generating 100 test scenarios across all realms...")
    scenarios = generate_test_scenarios(100)
    print(f"✓ Generated {len(scenarios)} scenarios")
    print()
    
    # Initialize oracle
    oracle = DissidentHorizonOracle(delta_deficit_threshold=0.0015)
    
    # Run validation
    results = []
    detection_correct = 0
    classification_correct = 0
    
    print("Running validation tests...")
    for idx, scenario in enumerate(scenarios):
        if (idx + 1) % 10 == 0:
            print(f"  Progress: {idx+1}/100 tests completed")
        
        # Create synthetic data
        data, states = create_synthetic_data(scenario)
        
        # Analyze with oracle
        analysis = oracle.analyze_system(data, states, states)
        
        # Check detection accuracy
        detected_as_dissident = analysis.signature.dissident_score > 0.5
        is_dissident = scenario['type'] == 'dissident'
        detection_match = detected_as_dissident == is_dissident
        if detection_match:
            detection_correct += 1
        
        # Check classification accuracy
        classification_match = analysis.signature.dissident_type == scenario['expected_type']
        if classification_match:
            classification_correct += 1
        
        # Store result
        results.append({
            'scenario_id': idx + 1,
            'realm': scenario['realm'],
            'description': scenario['description'],
            'true_type': scenario['type'],
            'expected_classification': scenario['expected_type'],
            'true_nrci': scenario['nrci'],
            'true_deficit': 1.0 - (scenario['nrci'] / 0.999997),
            'detected_dissident': detected_as_dissident,
            'dissident_score': analysis.signature.dissident_score,
            'classified_type': analysis.signature.dissident_type,
            'delta_deficit': analysis.signature.delta_deficit,
            'spectral_eigenvalue': analysis.signature.laplacian_eigenvalue,
            'pca_variance': analysis.signature.pca_variance_ratio,
            'temporal_memory': analysis.signature.memory_persistence,
            'confidence': analysis.confidence,
            'detection_correct': detection_match,
            'classification_correct': classification_match
        })
    
    print(f"✓ Completed all 100 tests")
    print()
    
    # Calculate statistics
    detection_rate = (detection_correct / len(scenarios)) * 100
    classification_rate = (classification_correct / len(scenarios)) * 100
    
    # Calculate per-realm statistics
    realm_stats = {}
    for realm in ['quantum', 'biological', 'cosmological', 'electromagnetic']:
        realm_results = [r for r in results if r['realm'] == realm]
        
        dissident_scores = [r['dissident_score'] for r in realm_results if r['true_type'] == 'dissident']
        deficits = [r['delta_deficit'] for r in realm_results if r['true_type'] == 'dissident']
        
        realm_stats[realm] = {
            'n_tests': len(realm_results),
            'n_dissidents': len(dissident_scores),
            'avg_dissident_score': np.mean(dissident_scores) if dissident_scores else 0,
            'std_dissident_score': np.std(dissident_scores) if dissident_scores else 0,
            'avg_deficit': np.mean(deficits) if deficits else 0,
            'std_deficit': np.std(deficits) if deficits else 0,
            'detection_rate': sum(r['detection_correct'] for r in realm_results) / len(realm_results) * 100,
            'classification_rate': sum(r['classification_correct'] for r in realm_results) / len(realm_results) * 100
        }
    
    # Overall statistics
    all_dissident_scores = [r['dissident_score'] for r in results if r['true_type'] == 'dissident']
    all_deficits = [r['delta_deficit'] for r in results if r['true_type'] == 'dissident']
    
    summary = {
        'total_tests': len(scenarios),
        'detection_accuracy': detection_rate,
        'classification_accuracy': classification_rate,
        'overall_stats': {
            'avg_dissident_score': np.mean(all_dissident_scores),
            'std_dissident_score': np.std(all_dissident_scores),
            'avg_deficit': np.mean(all_deficits),
            'std_deficit': np.std(all_deficits),
            'min_deficit': np.min(all_deficits),
            'max_deficit': np.max(all_deficits)
        },
        'realm_stats': realm_stats
    }
    
    # Print summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Detection Accuracy: {summary['detection_accuracy']:.1f}%")
    print(f"Classification Accuracy: {summary['classification_accuracy']:.1f}%")
    print()
    print("Overall Dissident Statistics:")
    print(f"  Average Dissident Score: {summary['overall_stats']['avg_dissident_score']:.3f} ± {summary['overall_stats']['std_dissident_score']:.3f}")
    print(f"  Average δ-Deficit: {summary['overall_stats']['avg_deficit']:.6f} ± {summary['overall_stats']['std_deficit']:.6f}")
    print(f"  Deficit Range: [{summary['overall_stats']['min_deficit']:.6f}, {summary['overall_stats']['max_deficit']:.6f}]")
    print()
    print("Per-Realm Statistics:")
    for realm, stats in realm_stats.items():
        print(f"  {realm.capitalize()}:")
        print(f"    Tests: {stats['n_tests']}, Dissidents: {stats['n_dissidents']}")
        print(f"    Dissident Score: {stats['avg_dissident_score']:.3f} ± {stats['std_dissident_score']:.3f}")
        print(f"    δ-Deficit: {stats['avg_deficit']:.6f} ± {stats['std_deficit']:.6f}")
        print(f"    Detection: {stats['detection_rate']:.1f}%, Classification: {stats['classification_rate']:.1f}%")
        print()
    
    return {
        'summary': summary,
        'detailed_results': results
    }

def run_hex_dictionary_validation():
    """Run comprehensive HexDictionary validation with real patterns"""
    print("=" * 80)
    print("COMPREHENSIVE HEXDICTIONARY VALIDATION STUDY")
    print("=" * 80)
    print()
    
    analyzer = AdvancedHexDictionaryAnalyzer()
    
    # Generate 50 pattern pairs with known relationships
    print("Generating 50 pattern pairs for validation...")
    
    test_cases = []
    
    # Similar patterns (15 pairs)
    for i in range(15):
        base_pattern = np.random.randn(100)
        similar_pattern = base_pattern + np.random.randn(100) * 0.1  # 10% noise
        
        test_cases.append({
            'type': 'similar',
            'expected_similarity': 'high',
            'pattern1': base_pattern,
            'pattern2': similar_pattern,
            'description': f'Similar pair {i+1}: 10% noise'
        })
    
    # Structurally related patterns (15 pairs)
    for i in range(15):
        base_pattern = np.sin(np.linspace(0, 4*np.pi, 100))
        related_pattern = np.sin(np.linspace(0, 4*np.pi, 100) + np.pi/4)  # Phase shift
        
        test_cases.append({
            'type': 'related',
            'expected_similarity': 'medium',
            'pattern1': base_pattern,
            'pattern2': related_pattern,
            'description': f'Related pair {i+1}: phase shift'
        })
    
    # Unrelated patterns (20 pairs)
    for i in range(20):
        pattern1 = np.random.randn(100)
        pattern2 = np.random.randn(100)
        
        test_cases.append({
            'type': 'unrelated',
            'expected_similarity': 'low',
            'pattern1': pattern1,
            'pattern2': pattern2,
            'description': f'Unrelated pair {i+1}: random'
        })
    
    print(f"✓ Generated {len(test_cases)} pattern pairs")
    print()
    
    # Run analysis
    print("Running advanced similarity analysis...")
    results = []
    
    for idx, test in enumerate(test_cases):
        if (idx + 1) % 10 == 0:
            print(f"  Progress: {idx+1}/50 pairs analyzed")
        
        # Create hashes and states
        hash1 = ''.join([f'{int(abs(x)*255):02x}' for x in test['pattern1'][:32]])
        hash2 = ''.join([f'{int(abs(x)*255):02x}' for x in test['pattern2'][:32]])
        
        # Create states with log_nrci_error
        log_error = math.log(1 - 0.999)
        states1 = [CoherenceState(x, log_error, 0) for x in test['pattern1'][:10]]
        states2 = [CoherenceState(x, log_error, 0) for x in test['pattern2'][:10]]
        
        # Analyze
        analysis = analyzer.analyze_similarity(
            hash1, hash2,
            test['pattern1'], test['pattern2'],
            states1, states2
        )
        
        # Hamming for comparison
        hamming_dist = sum(c1 != c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)
        hamming_sim = 1.0 - hamming_dist
        
        results.append({
            'test_id': idx + 1,
            'type': test['type'],
            'expected_similarity': test['expected_similarity'],
            'description': test['description'],
            'hamming_similarity': hamming_sim,
            'overall_similarity': analysis.overall_similarity,
            'spectral_similarity': analysis.spectral_similarity,
            'kl_similarity': analysis.kl_similarity,
            'topological_similarity': analysis.topological_similarity,
            'coherence_similarity': analysis.coherence_similarity,
            'frequency_similarity': analysis.frequency_similarity,
            'wavelet_similarity': analysis.wavelet_similarity,
            'graph_similarity': analysis.graph_similarity,
            'confidence': analysis.confidence
        })
    
    print(f"✓ Completed all 50 analyses")
    print()
    
    # Calculate discriminative power
    similar_advanced = [r['overall_similarity'] for r in results if r['type'] == 'similar']
    similar_hamming = [r['hamming_similarity'] for r in results if r['type'] == 'similar']
    
    unrelated_advanced = [r['overall_similarity'] for r in results if r['type'] == 'unrelated']
    unrelated_hamming = [r['hamming_similarity'] for r in results if r['type'] == 'unrelated']
    
    # Separation (higher is better)
    advanced_separation = np.mean(similar_advanced) - np.mean(unrelated_advanced)
    hamming_separation = np.mean(similar_hamming) - np.mean(unrelated_hamming)
    
    discriminative_power = advanced_separation / hamming_separation if hamming_separation > 0 else float('inf')
    
    # Per-method discriminative power
    method_power = {}
    for method in ['spectral', 'kl', 'topological', 'coherence', 'frequency', 'wavelet', 'graph']:
        similar_method = [r[f'{method}_similarity'] for r in results if r['type'] == 'similar']
        unrelated_method = [r[f'{method}_similarity'] for r in results if r['type'] == 'unrelated']
        
        method_separation = np.mean(similar_method) - np.mean(unrelated_method)
        method_power[method] = method_separation / hamming_separation if hamming_separation > 0 else 0
    
    summary = {
        'total_tests': len(test_cases),
        'discriminative_power': discriminative_power,
        'method_discriminative_power': method_power,
        'similar_patterns': {
            'n': len(similar_advanced),
            'advanced_similarity': np.mean(similar_advanced),
            'hamming_similarity': np.mean(similar_hamming)
        },
        'unrelated_patterns': {
            'n': len(unrelated_advanced),
            'advanced_similarity': np.mean(unrelated_advanced),
            'hamming_similarity': np.mean(unrelated_hamming)
        }
    }
    
    # Print summary
    print("=" * 80)
    print("HEXDICTIONARY VALIDATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Pattern Pairs Tested: {summary['total_tests']}")
    print()
    print(f"Overall Discriminative Power: {summary['discriminative_power']:.1f}x vs Hamming")
    print()
    print("Per-Method Discriminative Power:")
    for method, power in sorted(method_power.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method.capitalize():15s}: {power:6.1f}x")
    print()
    print("Similar Patterns:")
    print(f"  Advanced Similarity: {summary['similar_patterns']['advanced_similarity']:.3f}")
    print(f"  Hamming Similarity:  {summary['similar_patterns']['hamming_similarity']:.3f}")
    print()
    print("Unrelated Patterns:")
    print(f"  Advanced Similarity: {summary['unrelated_patterns']['advanced_similarity']:.3f}")
    print(f"  Hamming Similarity:  {summary['unrelated_patterns']['hamming_similarity']:.3f}")
    print()
    
    return {
        'summary': summary,
        'detailed_results': results
    }

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("COMPREHENSIVE UBP DISSIDENT HORIZON VALIDATION")
    print("Framework: UBP 3.5 | Author: Euan Craig, New Zealand")
    print("=" * 80 + "\n")
    
    # Run dissident validation
    dissident_results = run_comprehensive_validation()
    
    print("\n")
    
    # Run HexDictionary validation
    hex_results = run_hex_dictionary_validation()
    
    # Save results
    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80 + "\n")
    
    with open('comprehensive_dissident_validation.json', 'w') as f:
        json.dump(dissident_results, f, indent=2)
    print("✓ Saved: comprehensive_dissident_validation.json")
    
    with open('comprehensive_hex_validation.json', 'w') as f:
        json.dump(hex_results, f, indent=2)
    print("✓ Saved: comprehensive_hex_validation.json")
    
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80 + "\n")
