#!/usr/bin/env python3.11
"""
Statistical Analysis Module for Symbol Study
Performs comprehensive analysis including:
- Information geometry
- Clustering analysis
- Classification boundary detection
- Statistical validation
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from collections import defaultdict
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SymbolStatisticalAnalysis:
    """
    Comprehensive statistical analysis of symbol coherence features.
    """
    
    def __init__(self, processed_data_path: str, output_dir: str):
        """
        Initialize analysis.
        
        Args:
            processed_data_path: Path to symbols_processed.json
            output_dir: Directory for output files
        """
        self.processed_data_path = processed_data_path
        self.output_dir = output_dir
        
        # Load processed data
        with open(processed_data_path, 'r') as f:
            self.data = json.load(f)
        
        print(f"Loaded {len(self.data)} processed symbols")
        
        # Extract feature matrix
        self.feature_matrix = self._extract_feature_matrix()
        self.categories = [s["category"] for s in self.data]
        self.symbols = [s["symbol"] for s in self.data]
        self.names = [s["name"] for s in self.data]
        
        print(f"Feature matrix shape: {self.feature_matrix.shape}")
    
    def _extract_feature_matrix(self) -> np.ndarray:
        """
        Extract feature matrix from processed data.
        
        Features:
        - NRCI
        - Net refinements
        - Refinement score
        - Degradation score
        - Bitfield dimensions (8D)
        - Bitfield magnitude
        """
        features = []
        for s in self.data:
            feature_vec = [
                s["nrci"],
                s["net_refinements"],
                s["refinement_score"],
                s["degradation_score"],
                s["bitfield_d1"],
                s["bitfield_d2"],
                s["bitfield_d3"],
                s["bitfield_d4"],
                s["bitfield_d5"],
                s["bitfield_d6"],
                s["bitfield_d7"],
                s["bitfield_d8"],
                s["bitfield_magnitude"]
            ]
            features.append(feature_vec)
        
        return np.array(features)
    
    def compute_information_geometry(self) -> Dict:
        """
        Compute information geometry metrics.
        
        Returns:
            Dictionary with geometry metrics
        """
        print("\n" + "="*60)
        print("INFORMATION GEOMETRY ANALYSIS")
        print("="*60)
        
        # Compute pairwise distances (Euclidean in feature space)
        distances = pdist(self.feature_matrix, metric='euclidean')
        distance_matrix = squareform(distances)
        
        # Compute Fisher information metric approximation
        # Use covariance of features as proxy for Fisher information
        cov_matrix = np.cov(self.feature_matrix.T)
        fisher_info = np.linalg.inv(cov_matrix + 1e-10 * np.eye(cov_matrix.shape[0]))
        
        # Compute geodesic distances (Mahalanobis distance)
        mahal_distances = pdist(self.feature_matrix, metric='mahalanobis', VI=fisher_info)
        mahal_matrix = squareform(mahal_distances)
        
        # Compute curvature (Ricci scalar approximation)
        # Use variance of distances as proxy for curvature
        curvature = np.var(distances)
        
        geometry = {
            'distance_matrix': distance_matrix,
            'mahalanobis_matrix': mahal_matrix,
            'fisher_information': fisher_info,
            'mean_distance': float(np.mean(distances)),
            'std_distance': float(np.std(distances)),
            'curvature': float(curvature),
            'dimensionality': self.feature_matrix.shape[1]
        }
        
        print(f"Mean pairwise distance: {geometry['mean_distance']:.6f}")
        print(f"Std pairwise distance: {geometry['std_distance']:.6f}")
        print(f"Curvature (variance): {geometry['curvature']:.6f}")
        print(f"Feature dimensionality: {geometry['dimensionality']}")
        
        return geometry
    
    def perform_clustering_analysis(self) -> Dict:
        """
        Perform clustering analysis using multiple algorithms.
        
        Returns:
            Dictionary with clustering results
        """
        print("\n" + "="*60)
        print("CLUSTERING ANALYSIS")
        print("="*60)
        
        results = {}
        
        # K-Means clustering (try different k values)
        print("\nK-Means Clustering:")
        kmeans_results = []
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.feature_matrix)
            silhouette = silhouette_score(self.feature_matrix, labels)
            davies_bouldin = davies_bouldin_score(self.feature_matrix, labels)
            
            kmeans_results.append({
                'k': k,
                'labels': labels.tolist(),
                'silhouette': float(silhouette),
                'davies_bouldin': float(davies_bouldin),
                'inertia': float(kmeans.inertia_)
            })
            
            print(f"  k={k}: silhouette={silhouette:.4f}, DB={davies_bouldin:.4f}")
        
        results['kmeans'] = kmeans_results
        
        # Find optimal k (highest silhouette score)
        optimal_kmeans = max(kmeans_results, key=lambda x: x['silhouette'])
        print(f"\nOptimal k={optimal_kmeans['k']} (silhouette={optimal_kmeans['silhouette']:.4f})")
        
        # DBSCAN clustering
        print("\nDBSCAN Clustering:")
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        dbscan_labels = dbscan.fit_predict(self.feature_matrix)
        n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
        n_noise = list(dbscan_labels).count(-1)
        
        print(f"  Clusters found: {n_clusters}")
        print(f"  Noise points: {n_noise}")
        
        if n_clusters > 1:
            # Compute silhouette only for non-noise points
            mask = dbscan_labels != -1
            if np.sum(mask) > 0:
                silhouette = silhouette_score(self.feature_matrix[mask], dbscan_labels[mask])
                print(f"  Silhouette: {silhouette:.4f}")
            else:
                silhouette = None
        else:
            silhouette = None
        
        results['dbscan'] = {
            'labels': dbscan_labels.tolist(),
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'silhouette': float(silhouette) if silhouette is not None else None
        }
        
        # Hierarchical clustering
        print("\nHierarchical Clustering:")
        linkage_matrix = linkage(self.feature_matrix, method='ward')
        
        results['hierarchical'] = {
            'linkage_matrix': linkage_matrix.tolist()
        }
        
        print("  Linkage matrix computed (ward method)")
        
        return results
    
    def perform_dimensionality_reduction(self) -> Dict:
        """
        Perform dimensionality reduction (PCA, t-SNE).
        
        Returns:
            Dictionary with reduced representations
        """
        print("\n" + "="*60)
        print("DIMENSIONALITY REDUCTION")
        print("="*60)
        
        results = {}
        
        # PCA
        print("\nPCA:")
        pca = PCA(n_components=min(10, self.feature_matrix.shape[1]))
        pca_features = pca.fit_transform(self.feature_matrix)
        
        explained_var = pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        print(f"  Explained variance (first 5 PCs): {explained_var[:5]}")
        print(f"  Cumulative variance (first 5 PCs): {cumulative_var[:5]}")
        
        results['pca'] = {
            'features': pca_features.tolist(),
            'explained_variance': explained_var.tolist(),
            'cumulative_variance': cumulative_var.tolist(),
            'components': pca.components_.tolist()
        }
        
        # t-SNE
        print("\nt-SNE:")
        tsne = TSNE(n_components=2, random_state=42, perplexity=30)
        tsne_features = tsne.fit_transform(self.feature_matrix)
        
        print(f"  t-SNE embedding computed (2D)")
        
        results['tsne'] = {
            'features': tsne_features.tolist()
        }
        
        return results
    
    def analyze_classification_boundaries(self) -> Dict:
        """
        Analyze classification boundaries between categories.
        
        Returns:
            Dictionary with boundary analysis
        """
        print("\n" + "="*60)
        print("CLASSIFICATION BOUNDARY ANALYSIS")
        print("="*60)
        
        # Compute category centroids
        category_centroids = {}
        category_samples = defaultdict(list)
        
        for i, cat in enumerate(self.categories):
            category_samples[cat].append(self.feature_matrix[i])
        
        for cat, samples in category_samples.items():
            category_centroids[cat] = np.mean(samples, axis=0)
        
        # Compute inter-category distances
        categories_list = sorted(category_centroids.keys())
        n_cats = len(categories_list)
        inter_cat_distances = np.zeros((n_cats, n_cats))
        
        for i, cat1 in enumerate(categories_list):
            for j, cat2 in enumerate(categories_list):
                dist = np.linalg.norm(category_centroids[cat1] - category_centroids[cat2])
                inter_cat_distances[i, j] = dist
        
        print("\nInter-category distances:")
        for i, cat1 in enumerate(categories_list):
            for j, cat2 in enumerate(categories_list):
                if i < j:
                    print(f"  {cat1:20s} <-> {cat2:20s}: {inter_cat_distances[i, j]:.6f}")
        
        # Compute intra-category variance
        intra_cat_variance = {}
        for cat, samples in category_samples.items():
            samples_array = np.array(samples)
            variance = np.mean(np.var(samples_array, axis=0))
            intra_cat_variance[cat] = float(variance)
        
        print("\nIntra-category variance:")
        for cat in sorted(intra_cat_variance.keys()):
            print(f"  {cat:20s}: {intra_cat_variance[cat]:.6f}")
        
        # Compute separability metric (Fisher discriminant ratio)
        # Between-class variance / Within-class variance
        overall_centroid = np.mean(self.feature_matrix, axis=0)
        between_var = 0.0
        within_var = 0.0
        
        for cat, samples in category_samples.items():
            n_samples = len(samples)
            cat_centroid = category_centroids[cat]
            
            # Between-class variance
            between_var += n_samples * np.sum((cat_centroid - overall_centroid) ** 2)
            
            # Within-class variance
            for sample in samples:
                within_var += np.sum((sample - cat_centroid) ** 2)
        
        separability = between_var / (within_var + 1e-10)
        
        print(f"\nSeparability (Fisher ratio): {separability:.6f}")
        
        results = {
            'category_centroids': {cat: centroid.tolist() for cat, centroid in category_centroids.items()},
            'inter_category_distances': inter_cat_distances.tolist(),
            'intra_category_variance': intra_cat_variance,
            'separability': float(separability),
            'between_class_variance': float(between_var),
            'within_class_variance': float(within_var)
        }
        
        return results
    
    def perform_statistical_tests(self) -> Dict:
        """
        Perform statistical hypothesis tests.
        
        Returns:
            Dictionary with test results
        """
        print("\n" + "="*60)
        print("STATISTICAL HYPOTHESIS TESTS")
        print("="*60)
        
        results = {}
        
        # Extract NRCI values by category
        category_nrcis = defaultdict(list)
        for i, cat in enumerate(self.categories):
            category_nrcis[cat].append(self.data[i]["nrci"])
        
        # ANOVA test (test if category means are different)
        print("\nANOVA Test (NRCI by category):")
        category_groups = [category_nrcis[cat] for cat in sorted(category_nrcis.keys())]
        f_stat, p_value = stats.f_oneway(*category_groups)
        
        print(f"  F-statistic: {f_stat:.6f}")
        print(f"  p-value: {p_value:.10f}")
        
        if p_value < 0.05:
            print("  Result: Categories have significantly different NRCI means (p < 0.05)")
        else:
            print("  Result: No significant difference in NRCI means (p >= 0.05)")
        
        results['anova'] = {
            'f_statistic': float(f_stat),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05)
        }
        
        # Pairwise t-tests (with Bonferroni correction)
        print("\nPairwise t-tests (Bonferroni corrected):")
        categories_list = sorted(category_nrcis.keys())
        n_comparisons = len(categories_list) * (len(categories_list) - 1) // 2
        bonferroni_alpha = 0.05 / n_comparisons
        
        pairwise_results = []
        for i, cat1 in enumerate(categories_list):
            for j, cat2 in enumerate(categories_list):
                if i < j:
                    t_stat, p_val = stats.ttest_ind(category_nrcis[cat1], category_nrcis[cat2])
                    significant = p_val < bonferroni_alpha
                    
                    pairwise_results.append({
                        'category1': cat1,
                        'category2': cat2,
                        't_statistic': float(t_stat),
                        'p_value': float(p_val),
                        'significant': bool(significant)
                    })
                    
                    if significant:
                        print(f"  {cat1:20s} vs {cat2:20s}: t={t_stat:.4f}, p={p_val:.6f} *")
        
        results['pairwise_ttests'] = pairwise_results
        print(f"\n  Bonferroni-corrected alpha: {bonferroni_alpha:.6f}")
        print(f"  Significant pairs: {sum(1 for r in pairwise_results if r['significant'])}/{n_comparisons}")
        
        # Kruskal-Wallis test (non-parametric alternative to ANOVA)
        print("\nKruskal-Wallis Test (non-parametric):")
        h_stat, kw_p_value = stats.kruskal(*category_groups)
        
        print(f"  H-statistic: {h_stat:.6f}")
        print(f"  p-value: {kw_p_value:.10f}")
        
        results['kruskal_wallis'] = {
            'h_statistic': float(h_stat),
            'p_value': float(kw_p_value),
            'significant': bool(kw_p_value < 0.05)
        }
        
        return results
    
    def run_full_analysis(self):
        """
        Run complete statistical analysis pipeline.
        """
        print("\n" + "="*70)
        print(" " * 15 + "SYMBOL STUDY: STATISTICAL ANALYSIS")
        print("="*70)
        
        # 1. Information geometry
        geometry = self.compute_information_geometry()
        
        # 2. Clustering analysis
        clustering = self.perform_clustering_analysis()
        
        # 3. Dimensionality reduction
        dim_reduction = self.perform_dimensionality_reduction()
        
        # 4. Classification boundaries
        boundaries = self.analyze_classification_boundaries()
        
        # 5. Statistical tests
        stat_tests = self.perform_statistical_tests()
        
        # Compile all results
        results = {
            'information_geometry': geometry,
            'clustering': clustering,
            'dimensionality_reduction': dim_reduction,
            'classification_boundaries': boundaries,
            'statistical_tests': stat_tests
        }
        
        # Save results
        output_path = f"{self.output_dir}/statistical_analysis_results.json"
        with open(output_path, 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            json.dump(results, f, indent=2, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
        
        print(f"\n{'='*70}")
        print(f"Analysis results saved to: {output_path}")
        print(f"{'='*70}\n")
        
        return results

def main():
    """Main execution function."""
    import os
    
    processed_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_processed.json"
    output_dir = "/home/ubuntu/ubp_symbol_study_phase1/results"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run analysis
    analysis = SymbolStatisticalAnalysis(processed_path, output_dir)
    results = analysis.run_full_analysis()

if __name__ == "__main__":
    main()
