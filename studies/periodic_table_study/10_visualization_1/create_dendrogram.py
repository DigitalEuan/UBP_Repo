#!/usr/bin/env python3.11
"""
Hierarchical Clustering Dendrogram from Jaccard Distances

Creates a visual dendrogram showing how elements cluster based on
Jaccard distance of their orbital toggle sets.

This visualization makes the paper's core insight instantly graspable.
"""

import sys
import json
sys.path.insert(0, '/home/ubuntu/periodic_table_hexdictionary')
sys.path.insert(0, '/home/ubuntu/FINAL_DELIVERABLES')

from periodic_table_data import get_all_elements
from hex_dictionary_pure import HexDictionaryPure
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def orbital_to_set(config_list):
    """Convert orbital configuration list to set."""
    orbitals = set()
    for orbital in config_list:
        if not orbital.startswith("["):
            orbitals.add(orbital)
    return orbitals

def simple_hierarchical_clustering(distance_matrix, labels, max_clusters=20):
    """
    Simple hierarchical clustering using complete linkage.
    Returns merge history and final clusters.
    """
    n = len(distance_matrix)
    clusters = [[i] for i in range(n)]
    cluster_labels = [[labels[i]] for i in range(n)]
    
    merge_history = []
    
    while len(clusters) > max_clusters:
        # Find closest pair
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                # Complete linkage
                max_dist = 0
                for idx_i in clusters[i]:
                    for idx_j in clusters[j]:
                        dist = distance_matrix[idx_i][idx_j]
                        if dist > max_dist:
                            max_dist = dist
                
                if max_dist < min_dist:
                    min_dist = max_dist
                    merge_i, merge_j = i, j
        
        # Merge
        new_cluster = clusters[merge_i] + clusters[merge_j]
        new_labels = cluster_labels[merge_i] + cluster_labels[merge_j]
        
        merge_history.append({
            'cluster_1': cluster_labels[merge_i],
            'cluster_2': cluster_labels[merge_j],
            'distance': min_dist,
            'size': len(new_cluster)
        })
        
        clusters = [c for i, c in enumerate(clusters) if i not in [merge_i, merge_j]]
        cluster_labels = [c for i, c in enumerate(cluster_labels) if i not in [merge_i, merge_j]]
        
        clusters.append(new_cluster)
        cluster_labels.append(new_labels)
    
    return merge_history, cluster_labels

def create_dendrogram_visualization():
    """
    Create a simplified dendrogram visualization for key element groups.
    """
    print("\nCreating hierarchical clustering dendrogram...")
    
    elements = get_all_elements()
    hex_dict = HexDictionaryPure()
    
    # Focus on first 36 elements for clarity
    focus_z = list(range(1, 37))
    
    # Convert to orbital sets
    element_sets = {}
    labels = []
    for z in focus_z:
        if z in elements:
            symbol, name, config = elements[z]
            element_sets[z] = orbital_to_set(config)
            labels.append(symbol)
    
    # Compute distance matrix
    z_list = sorted(element_sets.keys())
    n = len(z_list)
    distance_matrix = []
    
    for i, z_i in enumerate(z_list):
        row = []
        for j, z_j in enumerate(z_list):
            dist = hex_dict.distance(element_sets[z_i], element_sets[z_j])
            row.append(dist)
        distance_matrix.append(row)
    
    # Perform clustering
    merge_history, final_clusters = simple_hierarchical_clustering(
        distance_matrix, labels, max_clusters=8
    )
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Left panel: Cluster visualization
    ax1.set_title('Element Clustering by Jaccard Distance\n(First 36 Elements)', 
                  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Cluster', fontsize=12)
    ax1.set_ylabel('Elements', fontsize=12)
    
    colors = plt.cm.tab10(range(len(final_clusters)))
    
    y_offset = 0
    for i, cluster in enumerate(final_clusters):
        cluster_str = ', '.join(cluster[:10])
        if len(cluster) > 10:
            cluster_str += f' ... ({len(cluster)} total)'
        
        ax1.add_patch(Rectangle((i, y_offset), 0.8, 0.8, 
                                 facecolor=colors[i], alpha=0.6, edgecolor='black'))
        ax1.text(i + 0.4, y_offset + 0.4, f'Cluster {i+1}\n{len(cluster)} elements',
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax1.text(i + 0.4, y_offset - 0.3, cluster_str,
                ha='center', va='top', fontsize=7, wrap=True)
    
    ax1.set_xlim(-0.5, len(final_clusters))
    ax1.set_ylim(-2, 2)
    ax1.set_xticks(range(len(final_clusters)))
    ax1.set_xticklabels([f'C{i+1}' for i in range(len(final_clusters))])
    ax1.set_yticks([])
    ax1.grid(axis='x', alpha=0.3)
    
    # Right panel: Distance heatmap for selected elements
    ax2.set_title('Jaccard Distance Heatmap\n(Selected Elements)', 
                  fontsize=14, fontweight='bold')
    
    # Select representative elements
    selected_z = [1, 2, 3, 6, 8, 10, 11, 17, 18, 26]  # H, He, Li, C, O, Ne, Na, Cl, Ar, Fe
    selected_indices = [z_list.index(z) for z in selected_z if z in z_list]
    selected_labels = [labels[i] for i in selected_indices]
    
    # Extract submatrix
    submatrix = []
    for i in selected_indices:
        row = [distance_matrix[i][j] for j in selected_indices]
        submatrix.append(row)
    
    im = ax2.imshow(submatrix, cmap='RdYlGn_r', vmin=0, vmax=1, aspect='auto')
    ax2.set_xticks(range(len(selected_labels)))
    ax2.set_yticks(range(len(selected_labels)))
    ax2.set_xticklabels(selected_labels, rotation=45, ha='right')
    ax2.set_yticklabels(selected_labels)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Jaccard Distance', rotation=270, labelpad=20, fontsize=12)
    
    # Add text annotations
    for i in range(len(selected_labels)):
        for j in range(len(selected_labels)):
            text = ax2.text(j, i, f'{submatrix[i][j]:.2f}',
                           ha="center", va="center", color="black", fontsize=8)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/dendrogram_visualization.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Dendrogram saved to: dendrogram_visualization.png")
    
    # Create a second, more detailed dendrogram for noble gases and alkali metals
    fig2, ax3 = plt.subplots(figsize=(12, 8))
    
    # Noble gases and alkali metals
    noble_z = [2, 10, 18, 36]  # He, Ne, Ar, Kr
    alkali_z = [3, 11, 19, 37]  # Li, Na, K, Rb
    
    combined_z = noble_z + alkali_z
    combined_labels = [elements[z][0] for z in combined_z]
    combined_sets = [orbital_to_set(elements[z][2]) for z in combined_z]
    
    # Compute distance matrix
    n_combined = len(combined_z)
    combined_matrix = []
    for i in range(n_combined):
        row = []
        for j in range(n_combined):
            dist = hex_dict.distance(combined_sets[i], combined_sets[j])
            row.append(dist)
        combined_matrix.append(row)
    
    # Visualize
    im2 = ax3.imshow(combined_matrix, cmap='RdYlGn_r', vmin=0, vmax=1, aspect='auto')
    ax3.set_xticks(range(len(combined_labels)))
    ax3.set_yticks(range(len(combined_labels)))
    ax3.set_xticklabels(combined_labels, fontsize=12)
    ax3.set_yticklabels(combined_labels, fontsize=12)
    ax3.set_title('Jaccard Distance: Noble Gases vs Alkali Metals', 
                  fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar2 = plt.colorbar(im2, ax=ax3)
    cbar2.set_label('Jaccard Distance', rotation=270, labelpad=20, fontsize=12)
    
    # Add text annotations
    for i in range(len(combined_labels)):
        for j in range(len(combined_labels)):
            text = ax3.text(j, i, f'{combined_matrix[i][j]:.2f}',
                           ha="center", va="center", 
                           color="white" if combined_matrix[i][j] > 0.5 else "black", 
                           fontsize=10, fontweight='bold')
    
    # Add group labels
    ax3.axhline(y=3.5, color='blue', linewidth=2, linestyle='--')
    ax3.axvline(x=3.5, color='blue', linewidth=2, linestyle='--')
    ax3.text(-0.5, 1.5, 'Noble\nGases', fontsize=12, fontweight='bold', 
             rotation=90, va='center', ha='right', color='blue')
    ax3.text(-0.5, 5.5, 'Alkali\nMetals', fontsize=12, fontweight='bold', 
             rotation=90, va='center', ha='right', color='red')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/noble_alkali_comparison.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Noble/Alkali comparison saved to: noble_alkali_comparison.png")
    
    return final_clusters

def main():
    print("\n" + "="*80)
    print("HIERARCHICAL CLUSTERING DENDROGRAM GENERATOR")
    print("="*80)
    
    final_clusters = create_dendrogram_visualization()
    
    print("\n" + "="*80)
    print("FINAL CLUSTERS (First 36 Elements)")
    print("="*80)
    for i, cluster in enumerate(final_clusters, 1):
        print(f"\nCluster {i} ({len(cluster)} elements):")
        print(f"  {', '.join(cluster)}")
    
    print("\n" + "="*80)
    print("✓ Visualizations complete!")
    print("="*80)
    print("\nGenerated files:")
    print("  1. dendrogram_visualization.png")
    print("  2. noble_alkali_comparison.png")
    print("\nThese visualizations make the paper's core insight instantly graspable.")

if __name__ == "__main__":
    main()
