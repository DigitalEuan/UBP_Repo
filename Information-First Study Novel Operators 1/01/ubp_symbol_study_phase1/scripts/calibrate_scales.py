#!/usr/bin/env python3.11
"""
Calibration Script for Refinement/Degradation Scales
Iteratively find scales that produce meaningful NRCI variance
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase1/ubp_3.5')

import json
import numpy as np
from symbol_coherence_model import SymbolCoherenceModel

def compute_nrci_statistics(model, encoded_path):
    """
    Compute NRCI statistics for given model parameters.
    
    Returns:
        (mean, std, min, max, range)
    """
    # Load encoded dataset
    with open(encoded_path, 'r') as f:
        encoded_symbols = json.load(f)
    
    # Compute NRCI for all symbols
    nrcis = []
    for symbol_data in encoded_symbols:
        features = model.compute_coherence_features(symbol_data)
        nrcis.append(features["nrci"])
    
    nrcis = np.array(nrcis)
    return {
        'mean': float(np.mean(nrcis)),
        'std': float(np.std(nrcis)),
        'min': float(np.min(nrcis)),
        'max': float(np.max(nrcis)),
        'range': float(np.max(nrcis) - np.min(nrcis))
    }

def calibrate_scales(encoded_path, target_std=0.01, target_range=0.05):
    """
    Calibrate refinement and degradation scales to achieve target variance.
    
    Args:
        encoded_path: Path to encoded symbols
        target_std: Target standard deviation for NRCI
        target_range: Target range (max - min) for NRCI
    """
    print("="*60)
    print("SCALE CALIBRATION")
    print("="*60)
    print(f"Target NRCI std: {target_std}")
    print(f"Target NRCI range: {target_range}")
    print()
    
    # Try different scale combinations
    refinement_scales = [0.5, 1.0, 2.0, 5.0, 10.0]
    degradation_scales = [1.0, 5.0, 10.0, 50.0, 100.0, 500.0, 1000.0]
    
    results = []
    
    print(f"Testing {len(refinement_scales)} × {len(degradation_scales)} = {len(refinement_scales) * len(degradation_scales)} combinations...")
    print()
    
    for ref_scale in refinement_scales:
        for deg_scale in degradation_scales:
            model = SymbolCoherenceModel(
                refinement_scale=ref_scale,
                degradation_scale=deg_scale
            )
            
            stats = compute_nrci_statistics(model, encoded_path)
            
            result = {
                'refinement_scale': ref_scale,
                'degradation_scale': deg_scale,
                **stats
            }
            results.append(result)
            
            print(f"ref={ref_scale:6.1f}, deg={deg_scale:7.1f} → "
                  f"NRCI: {stats['mean']:.8f} ± {stats['std']:.8f}, "
                  f"range: {stats['range']:.8f}")
    
    print()
    print("="*60)
    print("BEST CONFIGURATIONS")
    print("="*60)
    
    # Sort by how close to target std
    results_by_std = sorted(results, key=lambda x: abs(x['std'] - target_std))
    
    print("\nClosest to target std:")
    for i, r in enumerate(results_by_std[:5]):
        print(f"{i+1}. ref={r['refinement_scale']:6.1f}, deg={r['degradation_scale']:7.1f} → "
              f"std={r['std']:.8f}, range={r['range']:.8f}")
    
    # Sort by how close to target range
    results_by_range = sorted(results, key=lambda x: abs(x['range'] - target_range))
    
    print("\nClosest to target range:")
    for i, r in enumerate(results_by_range[:5]):
        print(f"{i+1}. ref={r['refinement_scale']:6.1f}, deg={r['degradation_scale']:7.1f} → "
              f"std={r['std']:.8f}, range={r['range']:.8f}")
    
    # Find best overall (balance std and range)
    def score(r):
        std_error = abs(r['std'] - target_std) / target_std
        range_error = abs(r['range'] - target_range) / target_range
        return std_error + range_error
    
    results_by_score = sorted(results, key=score)
    
    print("\nBest overall (balanced):")
    for i, r in enumerate(results_by_score[:5]):
        print(f"{i+1}. ref={r['refinement_scale']:6.1f}, deg={r['degradation_scale']:7.1f} → "
              f"std={r['std']:.8f}, range={r['range']:.8f}")
    
    print()
    print("="*60)
    print("RECOMMENDED CONFIGURATION")
    print("="*60)
    best = results_by_score[0]
    print(f"Refinement scale: {best['refinement_scale']}")
    print(f"Degradation scale: {best['degradation_scale']}")
    print(f"Expected NRCI std: {best['std']:.8f}")
    print(f"Expected NRCI range: {best['range']:.8f}")
    print("="*60)
    
    return best

def main():
    """Main execution function."""
    encoded_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_encoded.json"
    
    # Calibrate with target variance similar to minerals study
    # Minerals had NRCI range of ~0.3 (0.7 to 1.0)
    # For symbols, let's target smaller variance initially
    best_config = calibrate_scales(
        encoded_path,
        target_std=0.01,    # 1% standard deviation
        target_range=0.05   # 5% range
    )
    
    # Save recommended configuration
    config_path = "/home/ubuntu/ubp_symbol_study_phase1/data/calibration_config.json"
    with open(config_path, 'w') as f:
        json.dump(best_config, f, indent=2)
    
    print(f"\nConfiguration saved to: {config_path}")

if __name__ == "__main__":
    main()
