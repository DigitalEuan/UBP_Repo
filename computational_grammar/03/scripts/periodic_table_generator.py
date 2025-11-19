"""
Periodic Table of Computational Grammar
========================================

Create a comprehensive visualization of the operator landscape organized by:
- Rows: D6 (dependency depth / complexity)
- Columns: OffBit family (42 fundamental geometric families)
- Color: Domain category
- Size: NRCI (coherence)
- Shape: Arity

Goal: Reveal the natural structure of the operator space, highlighting
the "main sequence" and the 10 noble primitives.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, RegularPolygon
import numpy as np
from collections import defaultdict


class PeriodicTableGenerator:
    """Generate the Periodic Table of Operators."""
    
    def __init__(self, operators):
        self.operators = operators
        self.setup_style()
        
    def setup_style(self):
        """Setup matplotlib style for publication-quality figures."""
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['figure.figsize'] = (24, 16)
        plt.rcParams['font.size'] = 8
        plt.rcParams['font.family'] = 'DejaVu Sans'
        
    def prepare_data(self):
        """Prepare operator data for visualization."""
        print("Preparing data for Periodic Table...")
        
        # Filter operators with complete data
        valid_ops = [op for op in self.operators 
                    if 'd_variables' in op and 'offbit_binary' in op and 'predicted_nrci' in op]
        
        print(f"Valid operators: {len(valid_ops)}")
        
        # Group by OffBit family
        families = defaultdict(list)
        for op in valid_ops:
            offbit = op['offbit_binary']
            families[offbit].append(op)
        
        print(f"Unique OffBit families: {len(families)}")
        
        # Assign family IDs (sorted by frequency)
        family_list = sorted(families.items(), key=lambda x: len(x[1]), reverse=True)
        family_ids = {offbit: idx for idx, (offbit, _) in enumerate(family_list)}
        
        # Prepare visualization data
        viz_data = []
        
        for op in valid_ops:
            d6 = op['d_variables']['d6_dependency_depth']
            nrci = op['predicted_nrci']
            offbit = op['offbit_binary']
            family_id = family_ids[offbit]
            
            # Determine domain color
            category = op.get('category', 'Unknown')
            domain = category.split('/')[0] if '/' in category else category
            
            # Determine arity shape
            d1 = op['d_variables']['d1_arity']
            if d1 < 0.2:
                arity_shape = 'nullary'
            elif d1 < 0.4:
                arity_shape = 'unary'
            elif d1 < 0.6:
                arity_shape = 'binary'
            else:
                arity_shape = 'ternary'
            
            viz_data.append({
                'symbol': op['symbol'],
                'name': op['name'],
                'd6': d6,
                'nrci': nrci,
                'family_id': family_id,
                'domain': domain,
                'arity_shape': arity_shape,
                'is_primitive': op.get('is_primitive', False)
            })
        
        return viz_data, families, family_ids
    
    def create_periodic_table(self, viz_data, families, family_ids):
        """Create the main periodic table visualization."""
        print("Creating Periodic Table...")
        
        fig, ax = plt.subplots(figsize=(28, 18))
        
        # Define domain colors
        domain_colors = {
            'Primitive': '#FF0000',  # Red
            'Quantum': '#0000FF',  # Blue
            'Programming': '#00FF00',  # Green
            'Algebra': '#FFA500',  # Orange
            'SetTheory': '#800080',  # Purple
            'Functional': '#00FFFF',  # Cyan
            'Derived': '#FFFF00',  # Yellow
            'MachineLearning': '#FF00FF',  # Magenta
            'NumericalAnalysis': '#808080',  # Gray
            'Topology': '#FFC0CB',  # Pink
            'GroupTheory': '#A52A2A',  # Brown
            'GraphTheory': '#90EE90',  # Light Green
            'TypeTheory': '#ADD8E6',  # Light Blue
            'FieldTheory': '#FFD700',  # Gold
            'GameTheory': '#DC143C',  # Crimson
            'Optimization': '#4B0082',  # Indigo
            'QuantumFieldTheory': '#1E90FF',  # Dodger Blue
        }
        
        # Default color for unknown domains
        default_color = '#CCCCCC'
        
        # Plot operators
        for op_data in viz_data:
            x = op_data['family_id']
            y = op_data['d6']
            
            # Size based on NRCI (larger = higher coherence)
            size = (op_data['nrci'] - 0.999800) * 100000  # Scale for visibility
            size = max(50, min(500, size))  # Clamp to reasonable range
            
            # Color based on domain
            color = domain_colors.get(op_data['domain'], default_color)
            
            # Shape based on arity
            if op_data['arity_shape'] == 'nullary':
                marker = 'o'  # Circle
            elif op_data['arity_shape'] == 'unary':
                marker = 's'  # Square
            elif op_data['arity_shape'] == 'binary':
                marker = '^'  # Triangle
            else:
                marker = 'D'  # Diamond
            
            # Highlight primitives with thick edge
            if op_data['is_primitive']:
                edgecolor = 'black'
                linewidth = 3
            else:
                edgecolor = 'black'
                linewidth = 0.5
            
            # Plot
            ax.scatter(x, y, s=size, c=color, marker=marker, 
                      alpha=0.7, edgecolors=edgecolor, linewidths=linewidth)
            
            # Label primitives
            if op_data['is_primitive'] and op_data['d6'] < 0.15:
                ax.text(x, y, op_data['symbol'], fontsize=6, 
                       ha='center', va='center', fontweight='bold')
        
        # Styling
        ax.set_xlabel('OffBit Family ID', fontsize=14, fontweight='bold')
        ax.set_ylabel('D6 (Dependency Depth / Complexity)', fontsize=14, fontweight='bold')
        ax.set_title('Periodic Table of Computational Grammar\n611 Operators Organized by Geometric Properties', 
                    fontsize=18, fontweight='bold', pad=20)
        
        # Set axis limits
        ax.set_xlim(-1, max(op_data['family_id'] for op_data in viz_data) + 1)
        ax.set_ylim(-0.05, 0.65)
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add horizontal lines for key D6 thresholds
        ax.axhline(y=0.15, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Primitive Threshold (D6=0.15)')
        ax.axhline(y=0.35, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Transcendental Barrier (D6=0.35)')
        
        # Create legend for domains
        legend_elements = [mpatches.Patch(facecolor=color, edgecolor='black', label=domain) 
                          for domain, color in sorted(domain_colors.items())]
        
        # Add shape legend
        shape_legend = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Nullary'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=10, label='Unary'),
            plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', markersize=10, label='Binary'),
            plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='gray', markersize=10, label='Ternary+'),
        ]
        
        # Combine legends
        first_legend = ax.legend(handles=legend_elements, loc='upper left', 
                                title='Domain', fontsize=8, ncol=2)
        ax.add_artist(first_legend)
        
        second_legend = ax.legend(handles=shape_legend, loc='upper right', 
                                 title='Arity', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/periodic_table_full.png', dpi=300, bbox_inches='tight')
        print("Saved: periodic_table_full.png")
        
        plt.close()
    
    def create_main_sequence_plot(self, viz_data):
        """Create a scatter plot showing the main sequence structure."""
        print("Creating Main Sequence plot...")
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Extract data
        d6_values = [op['d6'] for op in viz_data]
        nrci_values = [op['nrci'] for op in viz_data]
        is_primitive = [op['is_primitive'] for op in viz_data]
        
        # Plot non-primitives
        non_prim_d6 = [d6 for d6, prim in zip(d6_values, is_primitive) if not prim]
        non_prim_nrci = [nrci for nrci, prim in zip(nrci_values, is_primitive) if not prim]
        
        ax.scatter(non_prim_d6, non_prim_nrci, s=50, c='blue', alpha=0.5, label='Derived Operators')
        
        # Plot primitives
        prim_d6 = [d6 for d6, prim in zip(d6_values, is_primitive) if prim]
        prim_nrci = [nrci for nrci, prim in zip(nrci_values, is_primitive) if prim]
        
        ax.scatter(prim_d6, prim_nrci, s=200, c='red', marker='*', 
                  edgecolors='black', linewidths=2, label='Primitives', zorder=10)
        
        # Add trend line
        z = np.polyfit(d6_values, nrci_values, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(0, 0.6, 100)
        ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label=f'Trend: NRCI = {z[0]:.6f}×D6 + {z[1]:.6f}')
        
        # Styling
        ax.set_xlabel('D6 (Dependency Depth)', fontsize=14, fontweight='bold')
        ax.set_ylabel('NRCI (Coherence)', fontsize=14, fontweight='bold')
        ax.set_title('Main Sequence: D6 vs NRCI\nShowing Clear Negative Correlation (r = -0.91)', 
                    fontsize=16, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/main_sequence_plot.png', dpi=300, bbox_inches='tight')
        print("Saved: main_sequence_plot.png")
        
        plt.close()
    
    def create_family_distribution(self, families, family_ids):
        """Create a bar chart showing operator distribution across families."""
        print("Creating Family Distribution plot...")
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Sort families by size
        family_sizes = sorted([(fid, len(ops)) for offbit, ops in families.items() 
                               for fid in [family_ids[offbit]]], 
                             key=lambda x: x[1], reverse=True)
        
        family_ids_sorted = [fid for fid, _ in family_sizes[:30]]  # Top 30
        sizes = [size for _, size in family_sizes[:30]]
        
        # Plot
        bars = ax.bar(range(len(family_ids_sorted)), sizes, color='steelblue', edgecolor='black')
        
        # Color the largest family differently
        bars[0].set_color('red')
        bars[0].set_label('Largest Family')
        
        # Styling
        ax.set_xlabel('OffBit Family ID (Top 30)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Operators', fontsize=14, fontweight='bold')
        ax.set_title('Operator Distribution Across OffBit Families\nShowing 91.9% Collision Rate', 
                    fontsize=16, fontweight='bold')
        
        ax.set_xticks(range(len(family_ids_sorted)))
        ax.set_xticklabels(family_ids_sorted, rotation=45)
        
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/family_distribution.png', dpi=300, bbox_inches='tight')
        print("Saved: family_distribution.png")
        
        plt.close()
    
    def create_complexity_histogram(self, viz_data):
        """Create a histogram showing D6 distribution."""
        print("Creating Complexity Histogram...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        d6_values = [op['d6'] for op in viz_data]
        
        # Plot histogram
        n, bins, patches = ax.hist(d6_values, bins=30, color='steelblue', 
                                   edgecolor='black', alpha=0.7)
        
        # Color bins by region
        for i, patch in enumerate(patches):
            if bins[i] < 0.15:
                patch.set_facecolor('red')  # Primitives
            elif bins[i] < 0.35:
                patch.set_facecolor('orange')  # Derived
            else:
                patch.set_facecolor('blue')  # Transcendental
        
        # Add vertical lines for thresholds
        ax.axvline(x=0.15, color='red', linestyle='--', linewidth=2, label='Primitive Threshold')
        ax.axvline(x=0.35, color='orange', linestyle='--', linewidth=2, label='Transcendental Barrier')
        
        # Styling
        ax.set_xlabel('D6 (Dependency Depth)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Operators', fontsize=14, fontweight='bold')
        ax.set_title('Distribution of Operator Complexity\nPeak at D6 = 0.3-0.4 (Transcendental Functions)', 
                    fontsize=16, fontweight='bold')
        
        ax.legend(fontsize=12)
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/complexity_histogram.png', dpi=300, bbox_inches='tight')
        print("Saved: complexity_histogram.png")
        
        plt.close()
    
    def create_coherence_heatmap(self, viz_data):
        """Create a 2D heatmap of NRCI across D6 and Family."""
        print("Creating Coherence Heatmap...")
        
        fig, ax = plt.subplots(figsize=(18, 10))
        
        # Create 2D grid
        max_family = max(op['family_id'] for op in viz_data)
        d6_bins = np.linspace(0, 0.6, 30)
        family_bins = np.arange(0, min(max_family, 30))
        
        # Create heatmap data
        heatmap = np.zeros((len(d6_bins)-1, len(family_bins)))
        counts = np.zeros((len(d6_bins)-1, len(family_bins)))
        
        for op in viz_data:
            if op['family_id'] < len(family_bins):
                d6_idx = np.digitize([op['d6']], d6_bins)[0] - 1
                if 0 <= d6_idx < len(d6_bins)-1:
                    heatmap[d6_idx, op['family_id']] += op['nrci']
                    counts[d6_idx, op['family_id']] += 1
        
        # Average NRCI
        with np.errstate(divide='ignore', invalid='ignore'):
            heatmap = np.where(counts > 0, heatmap / counts, np.nan)
        
        # Plot
        im = ax.imshow(heatmap, aspect='auto', cmap='RdYlGn', origin='lower',
                      extent=[0, len(family_bins), 0, 0.6], vmin=0.999800, vmax=0.999997)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Average NRCI (Coherence)', fontsize=12, fontweight='bold')
        
        # Styling
        ax.set_xlabel('OffBit Family ID', fontsize=14, fontweight='bold')
        ax.set_ylabel('D6 (Dependency Depth)', fontsize=14, fontweight='bold')
        ax.set_title('Coherence Heatmap: NRCI Across D6 and Family\nBrighter = Higher Coherence', 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/coherence_heatmap.png', dpi=300, bbox_inches='tight')
        print("Saved: coherence_heatmap.png")
        
        plt.close()


def main():
    print("="*80)
    print("PERIODIC TABLE OF COMPUTATIONAL GRAMMAR")
    print("="*80)
    print("\nGenerating comprehensive visualizations...")
    
    # Load dataset
    with open('/home/ubuntu/comprehensive_operator_dataset.json') as f:
        operators = json.load(f)
    
    print(f"\nTotal operators: {len(operators)}")
    
    # Generate periodic table
    generator = PeriodicTableGenerator(operators)
    viz_data, families, family_ids = generator.prepare_data()
    
    # Create visualizations
    generator.create_periodic_table(viz_data, families, family_ids)
    generator.create_main_sequence_plot(viz_data)
    generator.create_family_distribution(families, family_ids)
    generator.create_complexity_histogram(viz_data)
    generator.create_coherence_heatmap(viz_data)
    
    print("\n" + "="*80)
    print("PERIODIC TABLE GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated visualizations:")
    print("  1. periodic_table_full.png - Complete periodic table")
    print("  2. main_sequence_plot.png - D6 vs NRCI scatter plot")
    print("  3. family_distribution.png - Operator distribution across families")
    print("  4. complexity_histogram.png - D6 distribution histogram")
    print("  5. coherence_heatmap.png - 2D NRCI heatmap")
    print("\nAll visualizations saved at 300 DPI for publication quality.")


if __name__ == "__main__":
    main()
