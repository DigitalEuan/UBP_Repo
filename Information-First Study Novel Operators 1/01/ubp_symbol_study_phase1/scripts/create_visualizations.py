#!/usr/bin/env python3.11
"""
Visualization Module for Symbol Study
Creates publication-quality figures for analysis results
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as mpatches
from scipy.cluster.hierarchy import dendrogram, linkage
from collections import defaultdict

class SymbolVisualization:
    """Create visualizations for symbol study results."""
    
    def __init__(self, processed_path: str, analysis_path: str, output_dir: str):
        """Initialize visualization."""
        self.output_dir = output_dir
        
        # Load data
        with open(processed_path, 'r') as f:
            self.processed_data = json.load(f)
        
        with open(analysis_path, 'r') as f:
            self.analysis_results = json.load(f)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Category colors
        self.category_colors = {
            'algebra': '#e74c3c',
            'arithmetic': '#3498db',
            'calculus': '#2ecc71',
            'information': '#f39c12',
            'logic': '#9b59b6',
            'miscellaneous': '#95a5a6',
            'probability': '#e67e22',
            'quantum': '#1abc9c',
            'set_theory': '#34495e'
        }
    
    def plot_nrci_distribution(self):
        """Plot NRCI distribution by category."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Extract NRCI by category
        category_nrcis = defaultdict(list)
        for s in self.processed_data:
            category_nrcis[s['category']].append(s['nrci'])
        
        # Box plot
        categories = sorted(category_nrcis.keys())
        data = [category_nrcis[cat] for cat in categories]
        colors = [self.category_colors[cat] for cat in categories]
        
        bp = ax1.boxplot(data, labels=categories, patch_artist=True, vert=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax1.set_ylabel('NRCI', fontsize=12)
        ax1.set_title('NRCI Distribution by Category', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Violin plot
        parts = ax2.violinplot(data, positions=range(1, len(categories)+1), 
                               showmeans=True, showmedians=True)
        
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colors[i])
            pc.set_alpha(0.7)
        
        ax2.set_xticks(range(1, len(categories)+1))
        ax2.set_xticklabels(categories, rotation=45, ha='right')
        ax2.set_ylabel('NRCI', fontsize=12)
        ax2.set_title('NRCI Violin Plot by Category', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/nrci_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: nrci_distribution.png")
    
    def plot_pca_projection(self):
        """Plot PCA projection (2D)."""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Get PCA features (first 2 components)
        pca_features = np.array(self.analysis_results['dimensionality_reduction']['pca']['features'])
        pc1 = pca_features[:, 0]
        pc2 = pca_features[:, 1]
        
        # Plot by category
        categories = [s['category'] for s in self.processed_data]
        for cat in sorted(set(categories)):
            mask = np.array([c == cat for c in categories])
            ax.scatter(pc1[mask], pc2[mask], 
                      c=self.category_colors[cat], 
                      label=cat, 
                      alpha=0.6, 
                      s=100,
                      edgecolors='black',
                      linewidths=0.5)
        
        ax.set_xlabel('PC1 (99.98% variance)', fontsize=12)
        ax.set_ylabel('PC2 (0.01% variance)', fontsize=12)
        ax.set_title('PCA Projection of Symbol Feature Space', fontsize=14, fontweight='bold')
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/pca_projection.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: pca_projection.png")
    
    def plot_tsne_embedding(self):
        """Plot t-SNE embedding (2D)."""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Get t-SNE features
        tsne_features = np.array(self.analysis_results['dimensionality_reduction']['tsne']['features'])
        tsne1 = tsne_features[:, 0]
        tsne2 = tsne_features[:, 1]
        
        # Plot by category
        categories = [s['category'] for s in self.processed_data]
        for cat in sorted(set(categories)):
            mask = np.array([c == cat for c in categories])
            ax.scatter(tsne1[mask], tsne2[mask], 
                      c=self.category_colors[cat], 
                      label=cat, 
                      alpha=0.6, 
                      s=100,
                      edgecolors='black',
                      linewidths=0.5)
        
        ax.set_xlabel('t-SNE Dimension 1', fontsize=12)
        ax.set_ylabel('t-SNE Dimension 2', fontsize=12)
        ax.set_title('t-SNE Embedding of Symbol Feature Space', fontsize=14, fontweight='bold')
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/tsne_embedding.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: tsne_embedding.png")
    
    def plot_clustering_results(self):
        """Plot clustering results."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # K-Means elbow plot
        kmeans_results = self.analysis_results['clustering']['kmeans']
        k_values = [r['k'] for r in kmeans_results]
        silhouettes = [r['silhouette'] for r in kmeans_results]
        davies_bouldins = [r['davies_bouldin'] for r in kmeans_results]
        
        ax1.plot(k_values, silhouettes, 'o-', linewidth=2, markersize=8, label='Silhouette Score')
        ax1.set_xlabel('Number of Clusters (k)', fontsize=12)
        ax1.set_ylabel('Silhouette Score', fontsize=12)
        ax1.set_title('K-Means Clustering: Silhouette Score', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Mark optimal k
        optimal_idx = np.argmax(silhouettes)
        ax1.axvline(k_values[optimal_idx], color='red', linestyle='--', alpha=0.5, label=f'Optimal k={k_values[optimal_idx]}')
        
        # Davies-Bouldin plot
        ax2.plot(k_values, davies_bouldins, 's-', linewidth=2, markersize=8, color='orange', label='Davies-Bouldin Index')
        ax2.set_xlabel('Number of Clusters (k)', fontsize=12)
        ax2.set_ylabel('Davies-Bouldin Index', fontsize=12)
        ax2.set_title('K-Means Clustering: Davies-Bouldin Index', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/clustering_metrics.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: clustering_metrics.png")
    
    def plot_hierarchical_dendrogram(self):
        """Plot hierarchical clustering dendrogram."""
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Get linkage matrix
        linkage_matrix = np.array(self.analysis_results['clustering']['hierarchical']['linkage_matrix'])
        
        # Create dendrogram
        dendrogram(linkage_matrix, ax=ax, color_threshold=100, above_threshold_color='gray')
        
        ax.set_xlabel('Symbol Index', fontsize=12)
        ax.set_ylabel('Distance', fontsize=12)
        ax.set_title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/hierarchical_dendrogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: hierarchical_dendrogram.png")
    
    def plot_category_heatmap(self):
        """Plot inter-category distance heatmap."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get inter-category distances
        distance_matrix = np.array(self.analysis_results['classification_boundaries']['inter_category_distances'])
        categories = sorted(self.category_colors.keys())
        
        # Create heatmap
        im = ax.imshow(distance_matrix, cmap='viridis', aspect='auto')
        
        # Set ticks
        ax.set_xticks(range(len(categories)))
        ax.set_yticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.set_yticklabels(categories)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Euclidean Distance', fontsize=12)
        
        # Add text annotations
        for i in range(len(categories)):
            for j in range(len(categories)):
                text = ax.text(j, i, f'{distance_matrix[i, j]:.1f}',
                             ha="center", va="center", color="white" if distance_matrix[i, j] > 60 else "black",
                             fontsize=8)
        
        ax.set_title('Inter-Category Distance Matrix', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/category_distance_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: category_distance_heatmap.png")
    
    def plot_feature_importance(self):
        """Plot feature importance from PCA."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get explained variance
        explained_var = np.array(self.analysis_results['dimensionality_reduction']['pca']['explained_variance'])
        
        # Plot first 10 components
        n_components = min(10, len(explained_var))
        x = range(1, n_components + 1)
        
        ax.bar(x, explained_var[:n_components], alpha=0.7, color='steelblue', edgecolor='black')
        ax.plot(x, np.cumsum(explained_var[:n_components]), 'ro-', linewidth=2, markersize=8, label='Cumulative')
        
        ax.set_xlabel('Principal Component', fontsize=12)
        ax.set_ylabel('Explained Variance Ratio', fontsize=12)
        ax.set_title('PCA Feature Importance', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Created: feature_importance.png")
    
    def create_all_visualizations(self):
        """Create all visualizations."""
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60 + "\n")
        
        self.plot_nrci_distribution()
        self.plot_pca_projection()
        self.plot_tsne_embedding()
        self.plot_clustering_results()
        self.plot_hierarchical_dendrogram()
        self.plot_category_heatmap()
        self.plot_feature_importance()
        
        print("\n" + "="*60)
        print(f"All visualizations saved to: {self.output_dir}")
        print("="*60 + "\n")

def main():
    """Main execution function."""
    processed_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_processed.json"
    analysis_path = "/home/ubuntu/ubp_symbol_study_phase1/results/statistical_analysis_results.json"
    output_dir = "/home/ubuntu/ubp_symbol_study_phase1/results"
    
    viz = SymbolVisualization(processed_path, analysis_path, output_dir)
    viz.create_all_visualizations()

if __name__ == "__main__":
    main()
