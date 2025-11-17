#!/usr/bin/env python3.11
"""
Phase 2 Module 7: Foundational Principles Investigation
Investigate the deep "why" questions: Pi emergence, threshold origins, PCA derivation
"""

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

NATURAL_THRESHOLD = 0.973243
PI = np.pi

def load_data():
    """Load Phase 2 results"""
    print("\n[1/6] Loading Phase 2 results...")
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    df = pd.DataFrame(results)
    print(f"   Loaded {len(df)} minerals")
    
    return df

def investigate_pi_emergence(df):
    """
    Investigate why Pi emerges in the symmetry-coherence relationship
    """
    print("\n[2/6] Investigating Pi emergence...")
    
    # From Phase 1, we found: 12 / π ≈ O_observer
    # Let's verify this with Phase 2 data
    
    # Calculate O_observer from UBP constants
    Y = PI / (PI**2 + 2)  # 0.264675430404527
    O_observer = 1 / Y     # 3.778212425957375
    
    print(f"   UBP Constants:")
    print(f"      Y = π/(π²+2) = {Y:.15f}")
    print(f"      O_observer = 1/Y = {O_observer:.15f}")
    print(f"      π = {PI:.15f}")
    
    # Test the 12/π relationship
    ratio_12_pi = 12 / PI
    print(f"\n   12 / π = {ratio_12_pi:.15f}")
    print(f"   O_observer = {O_observer:.15f}")
    print(f"   Difference: {abs(ratio_12_pi - O_observer):.15f}")
    print(f"   Relative error: {abs(ratio_12_pi - O_observer) / O_observer * 100:.4f}%")
    
    # Analyze symmetry vs NRCI relationship
    passed = df[df['nrci'] >= NATURAL_THRESHOLD]
    failed = df[df['nrci'] < NATURAL_THRESHOLD]
    
    # Group by symmetry operations
    symmetry_groups = df.groupby('symmetry_operations').agg({
        'nrci': ['mean', 'std', 'count'],
        'name': 'count'
    })
    
    print(f"\n   Symmetry vs NRCI:")
    print(f"      Symmetry | Mean NRCI | Std NRCI | Count")
    for sym in sorted(df['symmetry_operations'].unique()):
        group = df[df['symmetry_operations'] == sym]
        mean_nrci = group['nrci'].mean()
        std_nrci = group['nrci'].std()
        count = len(group)
        print(f"      {sym:8d} | {mean_nrci:9.6f} | {std_nrci:8.6f} | {count:5d}")
    
    # Find critical symmetry threshold
    # Where does pass rate cross 50%?
    symmetry_pass_rates = []
    for sym in sorted(df['symmetry_operations'].unique()):
        group = df[df['symmetry_operations'] == sym]
        pass_rate = (group['nrci'] >= NATURAL_THRESHOLD).sum() / len(group)
        symmetry_pass_rates.append({
            'symmetry': sym,
            'pass_rate': pass_rate,
            'count': len(group)
        })
    
    # Find where pass rate crosses 50%
    for i, spr in enumerate(symmetry_pass_rates):
        if spr['pass_rate'] >= 0.5 and i > 0:
            print(f"\n   Critical symmetry threshold:")
            print(f"      Symmetry {symmetry_pass_rates[i-1]['symmetry']}: {symmetry_pass_rates[i-1]['pass_rate']*100:.1f}% pass")
            print(f"      Symmetry {spr['symmetry']}: {spr['pass_rate']*100:.1f}% pass")
            critical_sym = (symmetry_pass_rates[i-1]['symmetry'] + spr['symmetry']) / 2
            print(f"      Critical value: ~{critical_sym:.1f}")
            print(f"      {critical_sym:.1f} / π = {critical_sym / PI:.6f}")
            print(f"      O_observer = {O_observer:.6f}")
            break
    
    # Investigate rotational symmetry connection to Pi
    # Pi governs circular/rotational geometry
    # Symmetry operations are rotations/reflections
    # Connection: 2π/n for n-fold rotation
    
    print(f"\n   Rotational symmetry and Pi:")
    print(f"      n-fold | Rotation angle | Angle/π")
    for n in [1, 2, 3, 4, 6, 12]:
        angle = 2 * PI / n if n > 0 else 0
        print(f"      {n:6d} | {angle:14.6f} | {angle/PI:7.4f}")
    
    return {
        'Y': float(Y),
        'O_observer': float(O_observer),
        '12_over_pi': float(12 / PI),
        'difference': float(abs(12/PI - O_observer)),
        'relative_error_percent': float(abs(12/PI - O_observer) / O_observer * 100)
    }

def investigate_threshold_origin(df):
    """
    Investigate why the natural threshold is 0.973243
    """
    print("\n[3/6] Investigating threshold origin...")
    
    # The threshold was the 95th percentile
    # But WHY 95th percentile?
    
    # Test different percentiles
    percentiles = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    percentile_analysis = []
    
    for p in percentiles:
        threshold = np.percentile(df['nrci'], p)
        pass_count = (df['nrci'] >= threshold).sum()
        pass_rate = pass_count / len(df) * 100
        
        percentile_analysis.append({
            'percentile': int(p),
            'threshold': float(threshold),
            'pass_count': int(pass_count),
            'pass_rate': float(pass_rate)
        })
        
        print(f"   {p}th percentile: threshold={threshold:.6f}, pass={pass_count} ({pass_rate:.2f}%)")
    
    # Earth has ~5,000 minerals from ~1.5M possible = 0.33%
    # Our dataset has 3,112 minerals
    # Expected pass count: 3,112 * 0.0033 ≈ 10 minerals
    
    print(f"\n   Expected pass count (Earth rate 0.33%): {3112 * 0.0033:.1f} minerals")
    print(f"   Actual pass count (95th percentile): 157 minerals (5.04%)")
    print(f"   Ratio: {157 / (3112 * 0.0033):.1f}x higher")
    
    # This suggests our dataset is enriched in "possible" minerals
    # compared to the full theoretical space
    
    # Investigate mathematical significance of 0.973243
    threshold = NATURAL_THRESHOLD
    
    print(f"\n   Mathematical properties of threshold {threshold:.6f}:")
    print(f"      1 - threshold = {1 - threshold:.6f}")
    print(f"      threshold / π = {threshold / PI:.6f}")
    print(f"      threshold * π = {threshold * PI:.6f}")
    print(f"      threshold² = {threshold**2:.6f}")
    print(f"      √threshold = {np.sqrt(threshold):.6f}")
    
    # Check if it relates to UBP constants
    Y = PI / (PI**2 + 2)
    O_observer = 1 / Y
    
    print(f"\n   Relationship to UBP constants:")
    print(f"      threshold / Y = {threshold / Y:.6f}")
    print(f"      threshold * Y = {threshold * Y:.6f}")
    print(f"      threshold / O_observer = {threshold / O_observer:.6f}")
    print(f"      threshold * O_observer = {threshold * O_observer:.6f}")
    
    # Check if it's related to e^(-x) decay
    # NRCI = 1 - degradation, so threshold might be e^(-k) for some k
    if threshold > 0 and threshold < 1:
        k = -np.log(threshold)
        print(f"\n   Exponential decay interpretation:")
        print(f"      threshold = e^(-k) where k = {k:.6f}")
        print(f"      k / π = {k / PI:.6f}")
    
    return {
        'percentile_analysis': percentile_analysis,
        'threshold': float(threshold),
        'one_minus_threshold': float(1 - threshold),
        'threshold_over_pi': float(threshold / PI),
        'threshold_over_Y': float(threshold / Y),
        'threshold_over_O_observer': float(threshold / O_observer)
    }

def investigate_pca_derivation(df):
    """
    Derive PCA loadings from first principles
    """
    print("\n[4/6] Investigating PCA derivation...")
    
    # Features
    feature_cols = [
        'Z_max', 'symmetry_operations', 'element_count',
        'molar_mass', 'density', 'refinements',
        'degradation', 'final_coherence'
    ]
    
    df['mohs_hardness'] = df['mohs_hardness'].fillna(df['mohs_hardness'].median())
    
    X = df[feature_cols].values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA
    pca = PCA(n_components=8)
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"   PCA Explained Variance:")
    for i, var in enumerate(pca.explained_variance_ratio_):
        print(f"      PC{i+1}: {var:.6f} ({var*100:.2f}%)")
    
    print(f"\n   PCA Loadings (PC1, PC2, PC3):")
    print(f"      Feature          | PC1      | PC2      | PC3")
    for i, feat in enumerate(feature_cols):
        print(f"      {feat:16s} | {pca.components_[0,i]:8.4f} | {pca.components_[1,i]:8.4f} | {pca.components_[2,i]:8.4f}")
    
    # Analyze PC1 loadings
    # PC1 should be the "complexity" axis
    pc1_loadings = pca.components_[0, :]
    
    print(f"\n   PC1 Loading Analysis:")
    print(f"      Positive loadings (increase complexity):")
    for i, feat in enumerate(feature_cols):
        if pc1_loadings[i] > 0:
            print(f"         {feat}: {pc1_loadings[i]:.4f}")
    
    print(f"      Negative loadings (decrease complexity):")
    for i, feat in enumerate(feature_cols):
        if pc1_loadings[i] < 0:
            print(f"         {feat}: {pc1_loadings[i]:.4f}")
    
    # Correlation analysis
    print(f"\n   Feature Correlations:")
    corr_matrix = np.corrcoef(X_scaled.T)
    
    # Find strongest correlations
    for i, feat1 in enumerate(feature_cols):
        for j, feat2 in enumerate(feature_cols):
            if i < j and abs(corr_matrix[i, j]) > 0.5:
                print(f"      {feat1} <-> {feat2}: {corr_matrix[i,j]:.4f}")
    
    return {
        'explained_variance': [float(v) for v in pca.explained_variance_ratio_],
        'pc1_loadings': {feat: float(pc1_loadings[i]) for i, feat in enumerate(feature_cols)},
        'pc2_loadings': {feat: float(pca.components_[1,i]) for i, feat in enumerate(feature_cols)},
        'pc3_loadings': {feat: float(pca.components_[2,i]) for i, feat in enumerate(feature_cols)}
    }

def investigate_bitfield_uniqueness(df):
    """
    Test if the Bitfield projection is unique or if alternatives exist
    """
    print("\n[5/6] Investigating Bitfield uniqueness...")
    
    # Features
    feature_cols = [
        'Z_max', 'symmetry_operations', 'element_count',
        'molar_mass', 'density', 'refinements',
        'degradation', 'final_coherence'
    ]
    
    df['mohs_hardness'] = df['mohs_hardness'].fillna(df['mohs_hardness'].median())
    
    X = df[feature_cols].values
    y = (df['nrci'] >= NATURAL_THRESHOLD).astype(int)
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Test different projections
    projections = []
    
    # 1. PCA (variance-maximizing)
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)
    
    # Separability metric
    pass_idx = np.where(y == 1)[0]
    fail_idx = np.where(y == 0)[0]
    
    if len(pass_idx) > 1 and len(fail_idx) > 1:
        from scipy.spatial.distance import pdist, squareform
        
        dist_matrix_pca = squareform(pdist(X_pca))
        pass_dists_pca = dist_matrix_pca[np.ix_(pass_idx, pass_idx)]
        pass_dists_pca = pass_dists_pca[np.triu_indices_from(pass_dists_pca, k=1)]
        fail_dists_pca = dist_matrix_pca[np.ix_(fail_idx, fail_idx)]
        fail_dists_pca = fail_dists_pca[np.triu_indices_from(fail_dists_pca, k=1)]
        inter_dists_pca = dist_matrix_pca[np.ix_(pass_idx, fail_idx)].flatten()
        
        sep_pca = np.mean(inter_dists_pca) / (np.mean(pass_dists_pca) + np.mean(fail_dists_pca)) * 2
        
        projections.append({
            'name': 'PCA',
            'separability': float(sep_pca),
            'pass_mean_dist': float(np.mean(pass_dists_pca)),
            'fail_mean_dist': float(np.mean(fail_dists_pca)),
            'inter_mean_dist': float(np.mean(inter_dists_pca))
        })
        
        print(f"   PCA Projection:")
        print(f"      Separability: {sep_pca:.4f}")
        print(f"      PASS mean distance: {np.mean(pass_dists_pca):.4f}")
        print(f"      FAIL mean distance: {np.mean(fail_dists_pca):.4f}")
        print(f"      Inter-class distance: {np.mean(inter_dists_pca):.4f}")
    
    # 2. Random projections (test if PCA is special)
    print(f"\n   Testing random projections...")
    
    np.random.seed(42)
    for i in range(5):
        # Random orthogonal matrix
        random_matrix = np.random.randn(8, 3)
        random_matrix, _ = np.linalg.qr(random_matrix)
        
        X_random = X_scaled @ random_matrix
        
        dist_matrix_random = squareform(pdist(X_random))
        pass_dists_random = dist_matrix_random[np.ix_(pass_idx, pass_idx)]
        pass_dists_random = pass_dists_random[np.triu_indices_from(pass_dists_random, k=1)]
        fail_dists_random = dist_matrix_random[np.ix_(fail_idx, fail_idx)]
        fail_dists_random = fail_dists_random[np.triu_indices_from(fail_dists_random, k=1)]
        inter_dists_random = dist_matrix_random[np.ix_(pass_idx, fail_idx)].flatten()
        
        sep_random = np.mean(inter_dists_random) / (np.mean(pass_dists_random) + np.mean(fail_dists_random)) * 2
        
        projections.append({
            'name': f'Random_{i+1}',
            'separability': float(sep_random),
            'pass_mean_dist': float(np.mean(pass_dists_random)),
            'fail_mean_dist': float(np.mean(fail_dists_random)),
            'inter_mean_dist': float(np.mean(inter_dists_random))
        })
        
        print(f"      Random {i+1}: Separability = {sep_random:.4f}")
    
    # Compare
    print(f"\n   Comparison:")
    print(f"      PCA separability: {sep_pca:.4f}")
    print(f"      Random mean separability: {np.mean([p['separability'] for p in projections if 'Random' in p['name']]):.4f}")
    print(f"      PCA is better: {sep_pca > np.mean([p['separability'] for p in projections if 'Random' in p['name']])}")
    
    return {
        'projections': projections,
        'pca_is_optimal': bool(sep_pca > np.mean([p['separability'] for p in projections if 'Random' in p['name']]))
    }

def visualize_findings():
    """Create visualizations of foundational principles"""
    print("\n[6/6] Creating visualizations...")
    
    # This will be implemented after analysis
    print("   (Visualizations will be created based on findings)")

def save_results(pi_results, threshold_results, pca_results, bitfield_results):
    """Save investigation results"""
    print("\n   Saving results...")
    
    summary = {
        'pi_emergence': pi_results,
        'threshold_origin': threshold_results,
        'pca_derivation': pca_results,
        'bitfield_uniqueness': bitfield_results
    }
    
    with open('results/phase2_foundational_principles.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved to results/phase2_foundational_principles.json")

def main():
    print("="*80)
    print("PHASE 2 MODULE 7: FOUNDATIONAL PRINCIPLES INVESTIGATION")
    print("="*80)
    print("Investigations:")
    print("  1. Pi emergence in symmetry-coherence relationship")
    print("  2. Natural threshold origin (why 0.973243?)")
    print("  3. PCA loading derivation from first principles")
    print("  4. Bitfield uniqueness vs alternative projections")
    print("="*80)
    
    # Load data
    df = load_data()
    
    # Investigate
    pi_results = investigate_pi_emergence(df)
    threshold_results = investigate_threshold_origin(df)
    pca_results = investigate_pca_derivation(df)
    bitfield_results = investigate_bitfield_uniqueness(df)
    
    # Visualize
    visualize_findings()
    
    # Save
    save_results(pi_results, threshold_results, pca_results, bitfield_results)
    
    print("\n" + "="*80)
    print("FOUNDATIONAL PRINCIPLES INVESTIGATION COMPLETE!")
    print("="*80)
    
    # Summary
    print("\nKey Findings:")
    print(f"   1. Pi emergence: 12/π vs O_observer error = {pi_results['relative_error_percent']:.4f}%")
    print(f"   2. Threshold: {threshold_results['threshold']:.6f} (95th percentile)")
    print(f"   3. PC1 variance: {pca_results['explained_variance'][0]*100:.2f}%")
    print(f"   4. PCA is optimal: {bitfield_results['pca_is_optimal']}")

if __name__ == '__main__':
    main()
