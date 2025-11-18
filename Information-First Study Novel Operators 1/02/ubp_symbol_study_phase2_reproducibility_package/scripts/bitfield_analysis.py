#!/usr/bin/env python3.11
"""
Bitfield Analysis Module - Phase 2B
Comprehensive analysis of 8D property space and its relationship to coherence

This module performs:
1. Individual dimension analysis (distributions, correlations)
2. Multi-dimensional analysis (PCA, clustering in bitfield space)
3. Coherence-bitfield relationships (which properties drive coherence?)
4. Category-specific bitfield patterns
5. Predictive power of bitfield features
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import os

class BitfieldAnalyzer:
    """
    Analyze the 8D property bitfield and its relationship to coherence.
    
    Bitfield dimensions:
    D1: Arity (0=nullary, 1=unary, 2=binary, 3=ternary)
    D2: Formal role (0=operand, 1=operator, 2=relation, 3=quantifier)
    D3: Invertibility (0=none, 1=partial, 2=full)
    D4: Commutativity (0=no, 1=partial, 2=yes)
    D5: Meaning count (log scale)
    D6: Dependency depth (1=atomic, 2=simple, 3=complex)
    D7: Closure degree (0=low, 1=medium, 2=high)
    D8: Overloading index (log scale)
    """
    
    def __init__(self, processed_data_path: str):
        """
        Initialize analyzer with processed symbol data.
        
        Args:
            processed_data_path: Path to symbols_processed.json
        """
        with open(processed_data_path, 'r') as f:
            self.symbols = json.load(f)
        
        print(f"Loaded {len(self.symbols)} processed symbols")
        
        # Extract bitfield matrix (N x 8)
        self.bitfield_matrix = np.array([
            [s[f"bitfield_d{i}"] for i in range(1, 9)]
            for s in self.symbols
        ])
        
        # Extract NRCI values
        self.nrcis = np.array([s["nrci"] for s in self.symbols])
        
        # Extract categories
        self.categories = [s["category"] for s in self.symbols]
        
        # Dimension names
        self.dimension_names = [
            "D1: Arity",
            "D2: Formal Role",
            "D3: Invertibility",
            "D4: Commutativity",
            "D5: Meaning Count (log)",
            "D6: Dependency Depth",
            "D7: Closure Degree",
            "D8: Overloading Index (log)"
        ]
        
        print(f"Bitfield matrix shape: {self.bitfield_matrix.shape}")
        print(f"NRCI range: [{self.nrcis.min():.6f}, {self.nrcis.max():.6f}]")
    
    def analyze_dimension_distributions(self) -> Dict:
        """
        Analyze the distribution of each bitfield dimension.
        
        Returns:
            Dictionary with distribution statistics for each dimension
        """
        print("\n" + "="*60)
        print("BITFIELD DIMENSION DISTRIBUTIONS")
        print("="*60)
        
        distributions = {}
        
        for i in range(8):
            dim_values = self.bitfield_matrix[:, i]
            
            # Compute statistics
            stats = {
                "mean": float(np.mean(dim_values)),
                "std": float(np.std(dim_values)),
                "min": float(np.min(dim_values)),
                "max": float(np.max(dim_values)),
                "median": float(np.median(dim_values)),
                "unique_values": len(np.unique(dim_values)),
                "value_counts": dict(Counter(dim_values))
            }
            
            distributions[f"D{i+1}"] = stats
            
            print(f"\n{self.dimension_names[i]}:")
            print(f"  Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
            print(f"  Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}")
            print(f"  Std: {stats['std']:.2f}")
            print(f"  Unique values: {stats['unique_values']}")
            
            # Print value distribution for discrete dimensions
            if i < 7:  # D1-D7 are discrete
                print(f"  Value distribution:")
                for val, count in sorted(stats['value_counts'].items()):
                    pct = 100.0 * count / len(dim_values)
                    print(f"    {val:.0f}: {count:4d} ({pct:5.1f}%)")
        
        return distributions
    
    def analyze_dimension_correlations(self) -> np.ndarray:
        """
        Compute correlation matrix between bitfield dimensions.
        
        Returns:
            8x8 correlation matrix
        """
        print("\n" + "="*60)
        print("BITFIELD DIMENSION CORRELATIONS")
        print("="*60)
        
        # Compute correlation matrix
        corr_matrix = np.corrcoef(self.bitfield_matrix.T)
        
        print("\nCorrelation Matrix (8x8):")
        print("     ", end="")
        for i in range(8):
            print(f"  D{i+1}  ", end="")
        print()
        
        for i in range(8):
            print(f"D{i+1}  ", end="")
            for j in range(8):
                print(f"{corr_matrix[i, j]:6.3f} ", end="")
            print()
        
        # Find strong correlations (|r| > 0.5, excluding diagonal)
        print("\nStrong correlations (|r| > 0.5):")
        strong_corrs = []
        for i in range(8):
            for j in range(i+1, 8):
                if abs(corr_matrix[i, j]) > 0.5:
                    strong_corrs.append((i, j, corr_matrix[i, j]))
                    print(f"  {self.dimension_names[i]} <-> {self.dimension_names[j]}: r = {corr_matrix[i, j]:.3f}")
        
        if not strong_corrs:
            print("  None found (dimensions are relatively independent)")
        
        return corr_matrix
    
    def analyze_coherence_bitfield_relationship(self) -> Dict:
        """
        Analyze the relationship between bitfield dimensions and NRCI.
        
        Returns:
            Dictionary with correlation coefficients and significance
        """
        print("\n" + "="*60)
        print("COHERENCE-BITFIELD RELATIONSHIPS")
        print("="*60)
        
        relationships = {}
        
        print("\nCorrelation between each dimension and NRCI:")
        for i in range(8):
            dim_values = self.bitfield_matrix[:, i]
            
            # Pearson correlation
            corr = np.corrcoef(dim_values, self.nrcis)[0, 1]
            
            # Spearman rank correlation (for non-linear relationships)
            from scipy.stats import spearmanr
            spearman_corr, spearman_p = spearmanr(dim_values, self.nrcis)
            
            relationships[f"D{i+1}"] = {
                "pearson_r": float(corr),
                "spearman_r": float(spearman_corr),
                "spearman_p": float(spearman_p)
            }
            
            print(f"\n{self.dimension_names[i]}:")
            print(f"  Pearson r: {corr:7.4f}")
            print(f"  Spearman ρ: {spearman_corr:7.4f} (p={spearman_p:.4e})")
            
            # Interpretation
            if abs(corr) > 0.3:
                direction = "positive" if corr > 0 else "negative"
                strength = "strong" if abs(corr) > 0.5 else "moderate"
                print(f"  → {strength.capitalize()} {direction} relationship with NRCI")
        
        # Identify most predictive dimensions
        print("\n" + "-"*60)
        print("Most predictive dimensions (by |Pearson r|):")
        sorted_dims = sorted(relationships.items(), 
                           key=lambda x: abs(x[1]["pearson_r"]), 
                           reverse=True)
        for dim, stats in sorted_dims[:5]:
            print(f"  {dim}: r = {stats['pearson_r']:7.4f}")
        
        return relationships
    
    def analyze_category_bitfield_patterns(self) -> Dict:
        """
        Analyze bitfield patterns for each category.
        
        Returns:
            Dictionary with category-specific bitfield statistics
        """
        print("\n" + "="*60)
        print("CATEGORY-SPECIFIC BITFIELD PATTERNS")
        print("="*60)
        
        category_patterns = defaultdict(lambda: defaultdict(list))
        
        # Group by category
        for i, symbol in enumerate(self.symbols):
            cat = symbol["category"]
            for d in range(8):
                category_patterns[cat][f"D{d+1}"].append(self.bitfield_matrix[i, d])
            category_patterns[cat]["nrci"].append(symbol["nrci"])
        
        # Compute statistics for each category
        category_stats = {}
        
        for cat in sorted(category_patterns.keys()):
            cat_data = category_patterns[cat]
            n = len(cat_data["nrci"])
            
            # Compute mean bitfield vector
            mean_bitfield = np.array([
                np.mean(cat_data[f"D{d+1}"]) for d in range(8)
            ])
            
            # Compute std for each dimension
            std_bitfield = np.array([
                np.std(cat_data[f"D{d+1}"]) for d in range(8)
            ])
            
            category_stats[cat] = {
                "n": n,
                "mean_bitfield": mean_bitfield.tolist(),
                "std_bitfield": std_bitfield.tolist(),
                "mean_nrci": float(np.mean(cat_data["nrci"])),
                "std_nrci": float(np.std(cat_data["nrci"]))
            }
            
            print(f"\n{cat} (n={n}):")
            print(f"  Mean NRCI: {category_stats[cat]['mean_nrci']:.6f} ± {category_stats[cat]['std_nrci']:.6f}")
            print(f"  Mean bitfield:")
            for d in range(8):
                print(f"    {self.dimension_names[d]:30s}: {mean_bitfield[d]:.2f} ± {std_bitfield[d]:.2f}")
        
        return category_stats
    
    def compute_bitfield_pca(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform PCA on bitfield matrix to identify principal components.
        
        Returns:
            Tuple of (transformed_data, components, explained_variance_ratio)
        """
        print("\n" + "="*60)
        print("BITFIELD PCA ANALYSIS")
        print("="*60)
        
        from sklearn.decomposition import PCA
        
        # Filter out constant dimensions (zero variance)
        stds = self.bitfield_matrix.std(axis=0)
        varying_dims = stds > 0
        bitfield_varying = self.bitfield_matrix[:, varying_dims]
        varying_dim_indices = np.where(varying_dims)[0]
        
        print(f"\nFiltering dimensions:")
        print(f"  Total dimensions: 8")
        print(f"  Varying dimensions: {varying_dims.sum()}")
        print(f"  Constant dimensions: {(~varying_dims).sum()}")
        if (~varying_dims).any():
            const_dims = np.where(~varying_dims)[0]
            print(f"  Constant dimension indices: {const_dims.tolist()}")
        
        # Standardize bitfield matrix (only varying dimensions)
        bitfield_std = (bitfield_varying - bitfield_varying.mean(axis=0)) / bitfield_varying.std(axis=0)
        
        # Perform PCA
        pca = PCA()
        transformed = pca.fit_transform(bitfield_std)
        
        print(f"\nExplained variance ratio:")
        cumulative_var = 0.0
        for i, var_ratio in enumerate(pca.explained_variance_ratio_):
            cumulative_var += var_ratio
            print(f"  PC{i+1}: {var_ratio*100:5.2f}% (cumulative: {cumulative_var*100:5.2f}%)")
        
        print(f"\nPrincipal components (loadings):")
        print("     ", end="")
        for idx in varying_dim_indices:
            print(f"  D{idx+1}  ", end="")
        print()
        
        for i in range(min(4, len(pca.components_))):
            print(f"PC{i+1} ", end="")
            for j in range(len(varying_dim_indices)):
                print(f"{pca.components_[i, j]:6.3f} ", end="")
            print()
        
        # Interpret top PCs
        print(f"\nInterpretation of top principal components:")
        for i in range(min(3, len(pca.components_))):
            print(f"\nPC{i+1} (explains {pca.explained_variance_ratio_[i]*100:.1f}% of variance):")
            # Find dimensions with highest absolute loadings
            loadings = pca.components_[i]
            top_dims = np.argsort(np.abs(loadings))[::-1][:3]
            for dim_idx in top_dims:
                loading = loadings[dim_idx]
                direction = "positively" if loading > 0 else "negatively"
                actual_dim_idx = varying_dim_indices[dim_idx]
                print(f"  - {direction} loaded on {self.dimension_names[actual_dim_idx]} ({loading:+.3f})")
        
        return transformed, pca.components_, pca.explained_variance_ratio_
    
    def generate_visualizations(self, output_dir: str):
        """
        Generate comprehensive visualizations of bitfield analysis.
        
        Args:
            output_dir: Directory to save visualization files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*60)
        print("GENERATING BITFIELD VISUALIZATIONS")
        print("="*60)
        
        # 1. Dimension distributions
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.flatten()
        
        for i in range(8):
            dim_values = self.bitfield_matrix[:, i]
            axes[i].hist(dim_values, bins=20, edgecolor='black', alpha=0.7)
            axes[i].set_title(self.dimension_names[i])
            axes[i].set_xlabel("Value")
            axes[i].set_ylabel("Frequency")
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/bitfield_distributions.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: bitfield_distributions.png")
        
        # 2. Correlation heatmap
        corr_matrix = np.corrcoef(self.bitfield_matrix.T)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
        
        ax.set_xticks(range(8))
        ax.set_yticks(range(8))
        ax.set_xticklabels([f"D{i+1}" for i in range(8)])
        ax.set_yticklabels([f"D{i+1}" for i in range(8)])
        
        # Add correlation values
        for i in range(8):
            for j in range(8):
                text = ax.text(j, i, f"{corr_matrix[i, j]:.2f}",
                             ha="center", va="center", color="black", fontsize=9)
        
        plt.colorbar(im, ax=ax, label="Correlation coefficient")
        ax.set_title("Bitfield Dimension Correlation Matrix")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/bitfield_correlation_matrix.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: bitfield_correlation_matrix.png")
        
        # 3. Dimension-NRCI relationships
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.flatten()
        
        for i in range(8):
            dim_values = self.bitfield_matrix[:, i]
            axes[i].scatter(dim_values, self.nrcis, alpha=0.3, s=10)
            axes[i].set_title(self.dimension_names[i])
            axes[i].set_xlabel("Dimension value")
            axes[i].set_ylabel("NRCI")
            axes[i].grid(True, alpha=0.3)
            
            # Add correlation coefficient
            corr = np.corrcoef(dim_values, self.nrcis)[0, 1]
            axes[i].text(0.05, 0.95, f"r = {corr:.3f}", 
                        transform=axes[i].transAxes, 
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/dimension_nrci_relationships.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: dimension_nrci_relationships.png")
        
        # 4. Category-specific bitfield patterns
        category_means = defaultdict(lambda: np.zeros(8))
        category_counts = Counter()
        
        for i, symbol in enumerate(self.symbols):
            cat = symbol["category"]
            category_means[cat] += self.bitfield_matrix[i]
            category_counts[cat] += 1
        
        for cat in category_means:
            category_means[cat] /= category_counts[cat]
        
        # Select top 10 categories by count
        top_categories = [cat for cat, _ in category_counts.most_common(10)]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        x = np.arange(8)
        width = 0.08
        
        for i, cat in enumerate(top_categories):
            offset = (i - len(top_categories)/2) * width
            ax.bar(x + offset, category_means[cat], width, label=cat, alpha=0.8)
        
        ax.set_xlabel("Bitfield Dimension")
        ax.set_ylabel("Mean Value")
        ax.set_title("Category-Specific Bitfield Patterns (Top 10 Categories)")
        ax.set_xticks(x)
        ax.set_xticklabels([f"D{i+1}" for i in range(8)])
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/category_bitfield_patterns.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: category_bitfield_patterns.png")
        
        print(f"\nAll visualizations saved to: {output_dir}/")
    
    def save_analysis_results(self, output_path: str):
        """
        Save comprehensive analysis results to JSON.
        
        Args:
            output_path: Path to save results JSON
        """
        results = {
            "dataset_size": len(self.symbols),
            "dimension_distributions": self.analyze_dimension_distributions(),
            "dimension_correlations": self.analyze_dimension_correlations().tolist(),
            "coherence_relationships": self.analyze_coherence_bitfield_relationship(),
            "category_patterns": self.analyze_category_bitfield_patterns()
        }
        
        # Add PCA results
        transformed, components, var_ratio = self.compute_bitfield_pca()
        results["pca"] = {
            "explained_variance_ratio": var_ratio.tolist(),
            "components": components.tolist()
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nAnalysis results saved to: {output_path}")

def main():
    """Main execution function."""
    print("="*60)
    print("BITFIELD ANALYSIS - PHASE 2B")
    print("="*60)
    
    # Initialize analyzer
    analyzer = BitfieldAnalyzer(
        "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_processed.json"
    )
    
    # Perform analyses
    analyzer.analyze_dimension_distributions()
    analyzer.analyze_dimension_correlations()
    analyzer.analyze_coherence_bitfield_relationship()
    analyzer.analyze_category_bitfield_patterns()
    analyzer.compute_bitfield_pca()
    
    # Generate visualizations
    analyzer.generate_visualizations(
        "/home/ubuntu/ubp_symbol_study_phase2/results"
    )
    
    # Save results
    analyzer.save_analysis_results(
        "/home/ubuntu/ubp_symbol_study_phase2/results/bitfield_analysis.json"
    )
    
    print("\n" + "="*60)
    print("BITFIELD ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
