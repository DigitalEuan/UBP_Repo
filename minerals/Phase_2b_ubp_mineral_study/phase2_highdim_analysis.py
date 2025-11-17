#!/usr/bin/env python3.11
"""
Phase 2 Module 4: Higher-Dimensional Analysis
Explore full 8D feature space using t-SNE, UMAP, and topological analysis
"""

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import umap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
import time

# Natural threshold from Phase 2 Module 2
NATURAL_THRESHOLD = 0.973243

def load_data():
    """Load Phase 2 results"""
    print("\n[1/7] Loading Phase 2 coherence analysis results...")
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    df = pd.DataFrame(results)
    
    # Features
    feature_cols = [
        'Z_max', 'symmetry_operations', 'element_count',
        'molar_mass', 'density', 'refinements',
        'degradation', 'final_coherence'
    ]
    
    df['mohs_hardness'] = df['mohs_hardness'].fillna(df['mohs_hardness'].median())
    
    X = df[feature_cols].values
    y = (df['nrci'] >= NATURAL_THRESHOLD).astype(int)
    
    print(f"   Loaded {len(df)} minerals")
    print(f"   Feature space: {X.shape[1]}D")
    
    return X, y, df, feature_cols

def analyze_8d_topology(X, y):
    """Analyze topology of full 8D space"""
    print("\n[2/7] Analyzing 8D topology...")
    
    # Compute pairwise distances
    print("   Computing pairwise distances...")
    distances = pdist(X, metric='euclidean')
    dist_matrix = squareform(distances)
    
    # Statistics
    print(f"   Mean distance: {np.mean(distances):.4f}")
    print(f"   Median distance: {np.median(distances):.4f}")
    print(f"   Std distance: {np.std(distances):.4f}")
    
    # Intra-class vs inter-class distances
    pass_idx = np.where(y == 1)[0]
    fail_idx = np.where(y == 0)[0]
    
    if len(pass_idx) > 1 and len(fail_idx) > 1:
        # Intra-class distances (pass)
        pass_dists = dist_matrix[np.ix_(pass_idx, pass_idx)]
        pass_dists = pass_dists[np.triu_indices_from(pass_dists, k=1)]
        
        # Intra-class distances (fail)
        fail_dists = dist_matrix[np.ix_(fail_idx, fail_idx)]
        fail_dists = fail_dists[np.triu_indices_from(fail_dists, k=1)]
        
        # Inter-class distances
        inter_dists = dist_matrix[np.ix_(pass_idx, fail_idx)].flatten()
        
        print(f"\n   Intra-class distances (PASS):")
        print(f"      Mean: {np.mean(pass_dists):.4f}")
        print(f"      Median: {np.median(pass_dists):.4f}")
        
        print(f"   Intra-class distances (FAIL):")
        print(f"      Mean: {np.mean(fail_dists):.4f}")
        print(f"      Median: {np.median(fail_dists):.4f}")
        
        print(f"   Inter-class distances:")
        print(f"      Mean: {np.mean(inter_dists):.4f}")
        print(f"      Median: {np.median(inter_dists):.4f}")
        
        # Separability metric
        separability = np.mean(inter_dists) / (np.mean(pass_dists) + np.mean(fail_dists)) * 2
        print(f"\n   Separability metric: {separability:.4f}")
        print(f"      (>1 = classes well-separated, <1 = overlapping)")
    
    separability = 0.0
    if len(pass_idx) > 1 and len(fail_idx) > 1:
        separability = np.mean(inter_dists) / (np.mean(pass_dists) + np.mean(fail_dists)) * 2
    return dist_matrix, separability

def run_pca(X, y):
    """Run PCA for comparison with Phase 1"""
    print("\n[3/7] Running PCA (for comparison with Phase 1)...")
    
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)
    
    print(f"   Explained variance ratio:")
    for i, var in enumerate(pca.explained_variance_ratio_):
        print(f"      PC{i+1}: {var:.4f} ({var*100:.2f}%)")
    print(f"   Cumulative: {np.sum(pca.explained_variance_ratio_):.4f} ({np.sum(pca.explained_variance_ratio_)*100:.2f}%)")
    
    return X_pca, pca

def run_tsne(X, y):
    """Run t-SNE in 2D and 3D"""
    print("\n[4/7] Running t-SNE...")
    
    # 2D t-SNE
    print("   Computing 2D t-SNE...")
    start = time.time()
    tsne_2d = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
    X_tsne_2d = tsne_2d.fit_transform(X)
    elapsed_2d = time.time() - start
    print(f"      Completed in {elapsed_2d:.2f}s")
    
    # 3D t-SNE
    print("   Computing 3D t-SNE...")
    start = time.time()
    tsne_3d = TSNE(n_components=3, random_state=42, perplexity=30, max_iter=1000)
    X_tsne_3d = tsne_3d.fit_transform(X)
    elapsed_3d = time.time() - start
    print(f"      Completed in {elapsed_3d:.2f}s")
    
    return X_tsne_2d, X_tsne_3d

def run_umap(X, y):
    """Run UMAP in 2D and 3D"""
    print("\n[5/7] Running UMAP...")
    
    # 2D UMAP
    print("   Computing 2D UMAP...")
    start = time.time()
    umap_2d = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
    X_umap_2d = umap_2d.fit_transform(X)
    elapsed_2d = time.time() - start
    print(f"      Completed in {elapsed_2d:.2f}s")
    
    # 3D UMAP
    print("   Computing 3D UMAP...")
    start = time.time()
    umap_3d = umap.UMAP(n_components=3, random_state=42, n_neighbors=15, min_dist=0.1)
    X_umap_3d = umap_3d.fit_transform(X)
    elapsed_3d = time.time() - start
    print(f"      Completed in {elapsed_3d:.2f}s")
    
    return X_umap_2d, X_umap_3d

def visualize_embeddings(X_pca, X_tsne_2d, X_tsne_3d, X_umap_2d, X_umap_3d, y):
    """Create comprehensive visualizations"""
    print("\n[6/7] Creating visualizations...")
    
    # Color scheme
    colors = ['red' if label == 0 else 'green' for label in y]
    
    # 1. 2D Comparison: PCA vs t-SNE vs UMAP
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # PCA 2D
    axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=colors, alpha=0.5, s=10)
    axes[0].set_xlabel('PC1')
    axes[0].set_ylabel('PC2')
    axes[0].set_title('PCA (2D)')
    axes[0].grid(True, alpha=0.3)
    
    # t-SNE 2D
    axes[1].scatter(X_tsne_2d[:, 0], X_tsne_2d[:, 1], c=colors, alpha=0.5, s=10)
    axes[1].set_xlabel('t-SNE 1')
    axes[1].set_ylabel('t-SNE 2')
    axes[1].set_title('t-SNE (2D)')
    axes[1].grid(True, alpha=0.3)
    
    # UMAP 2D
    axes[2].scatter(X_umap_2d[:, 0], X_umap_2d[:, 1], c=colors, alpha=0.5, s=10)
    axes[2].set_xlabel('UMAP 1')
    axes[2].set_ylabel('UMAP 2')
    axes[2].set_title('UMAP (2D)')
    axes[2].grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', label='Pass'),
                      Patch(facecolor='red', label='Fail')]
    axes[2].legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('results/phase2_highdim_2d_comparison.png', dpi=150)
    print("   ✓ Saved 2D comparison")
    
    # 2. 3D Visualizations
    fig = plt.figure(figsize=(18, 5))
    
    # PCA 3D
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=colors, alpha=0.5, s=10)
    ax1.set_xlabel('PC1')
    ax1.set_ylabel('PC2')
    ax1.set_zlabel('PC3')
    ax1.set_title('PCA (3D)')
    
    # t-SNE 3D
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(X_tsne_3d[:, 0], X_tsne_3d[:, 1], X_tsne_3d[:, 2], c=colors, alpha=0.5, s=10)
    ax2.set_xlabel('t-SNE 1')
    ax2.set_ylabel('t-SNE 2')
    ax2.set_zlabel('t-SNE 3')
    ax2.set_title('t-SNE (3D)')
    
    # UMAP 3D
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(X_umap_3d[:, 0], X_umap_3d[:, 1], X_umap_3d[:, 2], c=colors, alpha=0.5, s=10)
    ax3.set_xlabel('UMAP 1')
    ax3.set_ylabel('UMAP 2')
    ax3.set_zlabel('UMAP 3')
    ax3.set_title('UMAP (3D)')
    
    plt.tight_layout()
    plt.savefig('results/phase2_highdim_3d_comparison.png', dpi=150)
    print("   ✓ Saved 3D comparison")
    
    # 3. Distance preservation analysis
    # Compare distances in original space vs embeddings
    print("\n   Analyzing distance preservation...")
    
    # Sample 500 random points for efficiency
    np.random.seed(42)
    sample_idx = np.random.choice(len(X_pca), min(500, len(X_pca)), replace=False)
    
    from sklearn.preprocessing import StandardScaler
    X_sample = StandardScaler().fit_transform(X_pca[sample_idx])
    
    orig_dists = pdist(X_sample)
    pca_dists = pdist(X_pca[sample_idx])
    tsne_dists = pdist(X_tsne_2d[sample_idx])
    umap_dists = pdist(X_umap_2d[sample_idx])
    
    # Spearman correlation (rank preservation)
    corr_pca, _ = spearmanr(orig_dists, pca_dists)
    corr_tsne, _ = spearmanr(orig_dists, tsne_dists)
    corr_umap, _ = spearmanr(orig_dists, umap_dists)
    
    print(f"   Distance preservation (Spearman correlation):")
    print(f"      PCA:   {corr_pca:.4f}")
    print(f"      t-SNE: {corr_tsne:.4f}")
    print(f"      UMAP:  {corr_umap:.4f}")
    
    return {
        'distance_preservation': {
            'pca': float(corr_pca),
            'tsne': float(corr_tsne),
            'umap': float(corr_umap)
        }
    }

def save_results(topology_stats, embeddings_stats):
    """Save analysis results"""
    print("\n[7/7] Saving results...")
    
    summary = {
        'topology': topology_stats,
        'embeddings': embeddings_stats
    }
    
    with open('results/phase2_highdim_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved summary to results/phase2_highdim_summary.json")

def main():
    print("="*80)
    print("PHASE 2 MODULE 4: HIGHER-DIMENSIONAL ANALYSIS")
    print("="*80)
    print("Methods: PCA, t-SNE, UMAP")
    print("Dimensions: 2D and 3D embeddings")
    print("="*80)
    
    # Load data
    X, y, df, feature_cols = load_data()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Analyze 8D topology
    dist_matrix, separability = analyze_8d_topology(X_scaled, y)
    
    # Run dimensionality reduction
    X_pca, pca = run_pca(X_scaled, y)
    X_tsne_2d, X_tsne_3d = run_tsne(X_scaled, y)
    X_umap_2d, X_umap_3d = run_umap(X_scaled, y)
    
    # Visualize
    embeddings_stats = visualize_embeddings(X_pca, X_tsne_2d, X_tsne_3d, X_umap_2d, X_umap_3d, y)
    
    # Save
    topology_stats = {
        'mean_distance': float(np.mean(pdist(X_scaled))),
        'median_distance': float(np.median(pdist(X_scaled))),
        'pca_explained_variance': [float(v) for v in pca.explained_variance_ratio_],
        'separability_metric': float(separability)
    }
    save_results(topology_stats, embeddings_stats)
    
    print("\n" + "="*80)
    print("HIGHER-DIMENSIONAL ANALYSIS COMPLETE!")
    print("="*80)
    print("\nKey Findings:")
    print(f"   1. PCA preserves distances best: {embeddings_stats['distance_preservation']['pca']:.4f}")
    print(f"   2. UMAP preserves local structure: {embeddings_stats['distance_preservation']['umap']:.4f}")
    print(f"   3. t-SNE emphasizes clusters: {embeddings_stats['distance_preservation']['tsne']:.4f}")
    print(f"   4. First 3 PCs explain {sum(topology_stats['pca_explained_variance'])*100:.2f}% variance")

if __name__ == '__main__':
    main()
