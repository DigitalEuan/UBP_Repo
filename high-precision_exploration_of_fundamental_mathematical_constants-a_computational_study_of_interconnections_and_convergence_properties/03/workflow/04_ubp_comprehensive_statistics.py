#!/usr/bin/env python3
"""
UBP COMPREHENSIVE STATISTICAL ANALYSIS & VISUALIZATION
=======================================================

Comprehensive analysis of all UBP predictions:
1. Compile all results (notebook + new analyses)
2. Statistical validation and error analysis
3. Publication-quality figures
4. Comprehensive results tables

Author: Euan Craig, New Zealand
"""

import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

# Set publication style
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.linewidth'] = 1.0
matplotlib.rcParams['figure.dpi'] = 150

# Paths
RESULTS_DIR = Path('/app/sandbox/session_20251215_122025_664f88889fdc/results')
FIGURES_DIR = Path('/app/sandbox/session_20251215_122025_664f88889fdc/figures')
FIGURES_DIR.mkdir(exist_ok=True)


class UBPStatisticalAnalysis:
    """Comprehensive statistical analysis of UBP predictions."""

    def __init__(self):
        """Initialize with all results."""
        # Load previous results
        with open(RESULTS_DIR / 'ubp_extended_results.json', 'r') as f:
            self.extended_results = json.load(f)

        with open(RESULTS_DIR / 'ubp_mesons_couplings.json', 'r') as f:
            self.meson_coupling_results = json.load(f)

        # Compile all predictions
        self.all_predictions = self._compile_predictions()

    def _compile_predictions(self):
        """Compile all predictions into unified structure."""
        predictions = []

        # Leptons
        for name, data in self.extended_results.get('leptons', {}).items():
            predictions.append({
                'particle': name.capitalize(),
                'category': 'Lepton',
                'error_percent': data.get('error_percent', None),
                'formula': data.get('formula', ''),
                'success': data.get('error_percent', 100) < 5.0
            })

        # Quarks
        for name, data in self.extended_results.get('quarks', {}).items():
            predictions.append({
                'particle': name.replace('_', '/').title(),
                'category': 'Quark Ratio',
                'error_percent': data.get('error_percent', None),
                'N': data.get('N', None),
                'delta': data.get('delta', None),
                'success': data.get('error_percent', 100) < 5.0
            })

        # Baryons
        for name, data in self.extended_results.get('baryons', {}).items():
            predictions.append({
                'particle': name.capitalize(),
                'category': 'Baryon',
                'error_percent': data.get('error_percent', None),
                'formula': data.get('formula', ''),
                'success': data.get('error_percent', 100) < 1.0  # Stricter for baryons
            })

        # Hyperons
        for name, data in self.meson_coupling_results.get('hyperons', {}).items():
            predictions.append({
                'particle': name.capitalize(),
                'category': 'Hyperon',
                'error_percent': data.get('error_percent', None),
                'success': data.get('error_percent', 100) < 1.0
            })

        # Coupling constants
        for name, data in [
            ('alpha_em', self.meson_coupling_results.get('fine_structure', {})),
            ('alpha_s', self.meson_coupling_results.get('strong_coupling', {})),
            ('weinberg', self.meson_coupling_results.get('weak_coupling', {}))
        ]:
            if data:
                predictions.append({
                    'particle': name,
                    'category': 'Coupling',
                    'error_percent': data.get('error_percent', None),
                    'success': data.get('error_percent', 100) < 5.0
                })

        return predictions

    def generate_summary_statistics(self):
        """Generate summary statistics across all categories."""
        print("=" * 80)
        print("UBP COMPREHENSIVE STATISTICAL SUMMARY")
        print("=" * 80)

        # Group by category
        categories = {}
        for pred in self.all_predictions:
            cat = pred['category']
            if cat not in categories:
                categories[cat] = []
            if pred['error_percent'] is not None:
                categories[cat].append(pred['error_percent'])

        print("\nCategory-wise Error Statistics:")
        print("-" * 80)
        print(f"{'Category':<20} {'Count':<8} {'Mean Error %':<15} {'Median %':<12} {'Best %':<12}")
        print("-" * 80)

        summary_stats = {}
        for cat, errors in sorted(categories.items()):
            if errors:
                mean_err = np.mean(errors)
                median_err = np.median(errors)
                best_err = np.min(errors)
                count = len(errors)

                print(f"{cat:<20} {count:<8} {mean_err:<15.3f} {median_err:<12.3f} {best_err:<12.3f}")

                summary_stats[cat] = {
                    'count': count,
                    'mean': mean_err,
                    'median': median_err,
                    'min': best_err,
                    'max': np.max(errors),
                    'std': np.std(errors)
                }

        # Overall statistics
        all_errors = [p['error_percent'] for p in self.all_predictions if p['error_percent'] is not None]
        print("-" * 80)
        print(f"{'OVERALL':<20} {len(all_errors):<8} {np.mean(all_errors):<15.3f} {np.median(all_errors):<12.3f} {np.min(all_errors):<12.3f}")
        print("-" * 80)

        # Success rate
        successes = sum(1 for p in self.all_predictions if p.get('success', False))
        total = len([p for p in self.all_predictions if p['error_percent'] is not None])
        success_rate = 100 * successes / total if total > 0 else 0

        print(f"\n  Success Rate (< 5% error): {successes}/{total} ({success_rate:.1f}%)")

        # Highlight exceptional predictions
        print("\n" + "=" * 80)
        print("EXCEPTIONAL PREDICTIONS (< 1% error):")
        print("=" * 80)

        exceptional = [p for p in self.all_predictions
                      if p['error_percent'] is not None and p['error_percent'] < 1.0]
        exceptional.sort(key=lambda x: x['error_percent'])

        for pred in exceptional:
            print(f"  • {pred['particle']:<20} ({pred['category']:<12}): {pred['error_percent']:.4f}%")

        return summary_stats

    def plot_error_distribution(self):
        """Create error distribution plots."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('UBP Prediction Error Analysis', fontsize=14, fontweight='bold')

        # 1. Error by category (bar plot)
        ax = axes[0, 0]
        categories = {}
        for pred in self.all_predictions:
            cat = pred['category']
            if pred['error_percent'] is not None:
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(pred['error_percent'])

        cat_names = list(categories.keys())
        cat_means = [np.mean(categories[cat]) for cat in cat_names]
        cat_medians = [np.median(categories[cat]) for cat in cat_names]

        x = np.arange(len(cat_names))
        width = 0.35

        ax.bar(x - width/2, cat_means, width, label='Mean', alpha=0.8, color='steelblue')
        ax.bar(x + width/2, cat_medians, width, label='Median', alpha=0.8, color='coral')
        ax.set_ylabel('Error (%)', fontsize=10)
        ax.set_title('Mean & Median Error by Category', fontsize=11, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(cat_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        ax.set_yscale('log')

        # 2. Individual prediction errors (sorted)
        ax = axes[0, 1]
        errors_sorted = sorted([p['error_percent'] for p in self.all_predictions
                               if p['error_percent'] is not None])

        ax.plot(range(len(errors_sorted)), errors_sorted, 'o-', linewidth=2, markersize=6, color='darkgreen')
        ax.axhline(y=1.0, color='r', linestyle='--', linewidth=1.5, label='1% threshold')
        ax.axhline(y=5.0, color='orange', linestyle='--', linewidth=1.5, label='5% threshold')
        ax.set_xlabel('Prediction Index (sorted)', fontsize=10)
        ax.set_ylabel('Error (%)', fontsize=10)
        ax.set_title('Individual Predictions (Sorted by Error)', fontsize=11, fontweight='bold')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(alpha=0.3)

        # 3. Error distribution histogram
        ax = axes[1, 0]
        all_errors = [p['error_percent'] for p in self.all_predictions if p['error_percent'] is not None]

        # Use log bins for better visualization
        bins = np.logspace(-2, 2, 30)
        ax.hist(all_errors, bins=bins, alpha=0.7, color='purple', edgecolor='black')
        ax.set_xlabel('Error (%)', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.set_title('Error Distribution (All Predictions)', fontsize=11, fontweight='bold')
        ax.set_xscale('log')
        ax.grid(alpha=0.3)

        # 4. Success rate by category
        ax = axes[1, 1]
        success_counts = {}
        total_counts = {}
        for pred in self.all_predictions:
            cat = pred['category']
            if pred['error_percent'] is not None:
                if cat not in success_counts:
                    success_counts[cat] = 0
                    total_counts[cat] = 0
                if pred.get('success', False):
                    success_counts[cat] += 1
                total_counts[cat] += 1

        cat_names = list(total_counts.keys())
        success_rates = [100 * success_counts[cat] / total_counts[cat] for cat in cat_names]

        colors = ['green' if sr > 50 else 'orange' if sr > 25 else 'red' for sr in success_rates]
        ax.barh(cat_names, success_rates, color=colors, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Success Rate (%)', fontsize=10)
        ax.set_title('Success Rate by Category (< 5% error)', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        output_file = FIGURES_DIR / 'ubp_error_analysis.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nSaved figure: {output_file}")
        plt.close()

    def plot_particle_predictions(self):
        """Create particle-specific prediction plots."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('UBP Particle Mass Predictions', fontsize=14, fontweight='bold')

        # 1. Leptons
        ax = axes[0, 0]
        lepton_data = self.extended_results.get('leptons', {})
        particles = list(lepton_data.keys())
        errors = [lepton_data[p]['error_percent'] for p in particles]

        colors_lepton = ['green' if e < 1 else 'orange' if e < 10 else 'red' for e in errors]
        ax.bar(particles, errors, color=colors_lepton, alpha=0.7, edgecolor='black')
        ax.set_ylabel('Error (%)', fontsize=10)
        ax.set_title('Lepton Mass Ratios', fontsize=11, fontweight='bold')
        ax.set_yscale('log')
        ax.grid(axis='y', alpha=0.3)
        for i, (p, e) in enumerate(zip(particles, errors)):
            ax.text(i, e * 1.2, f'{e:.3f}%', ha='center', va='bottom', fontsize=8)

        # 2. Quarks
        ax = axes[0, 1]
        quark_data = self.extended_results.get('quarks', {})
        ratios = [r.replace('_', '/') for r in quark_data.keys()]
        errors = [quark_data[r]['error_percent'] for r in quark_data.keys()]

        colors_quark = ['green' if e < 1 else 'orange' if e < 5 else 'red' for e in errors]
        ax.bar(ratios, errors, color=colors_quark, alpha=0.7, edgecolor='black')
        ax.set_ylabel('Error (%)', fontsize=10)
        ax.set_title('Quark Mass Ratios', fontsize=11, fontweight='bold')
        ax.set_xticklabels(ratios, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        for i, (r, e) in enumerate(zip(ratios, errors)):
            ax.text(i, e * 1.1, f'{e:.2f}%', ha='center', va='bottom', fontsize=8)

        # 3. Baryons + Hyperons
        ax = axes[1, 0]
        baryon_data = self.extended_results.get('baryons', {})
        hyperon_data = self.meson_coupling_results.get('hyperons', {})

        all_baryons = {**baryon_data, **hyperon_data}
        names = list(all_baryons.keys())
        errors = [all_baryons[n]['error_percent'] for n in names]

        colors_baryon = ['green' if e < 0.5 else 'orange' for e in errors]
        ax.bar(names, errors, color=colors_baryon, alpha=0.7, edgecolor='black')
        ax.set_ylabel('Error (%)', fontsize=10)
        ax.set_title('Baryon & Hyperon Masses', fontsize=11, fontweight='bold')
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, max(errors) * 1.3)
        for i, (n, e) in enumerate(zip(names, errors)):
            ax.text(i, e * 1.05, f'{e:.3f}%', ha='center', va='bottom', fontsize=8)

        # 4. Coupling Constants
        ax = axes[1, 1]
        coupling_names = ['α_em', 'α_s(MZ)', 'sin²θ_W']
        coupling_errors = [
            self.meson_coupling_results.get('fine_structure', {}).get('error_percent', None),
            self.meson_coupling_results.get('strong_coupling', {}).get('error_percent', None),
            self.meson_coupling_results.get('weak_coupling', {}).get('error_percent', None)
        ]

        # Filter None values
        valid_couplings = [(n, e) for n, e in zip(coupling_names, coupling_errors) if e is not None]
        names, errors = zip(*valid_couplings) if valid_couplings else ([], [])

        if names:
            colors_coupling = ['green' if e < 1 else 'orange' if e < 10 else 'red' for e in errors]
            ax.bar(names, errors, color=colors_coupling, alpha=0.7, edgecolor='black')
            ax.set_ylabel('Error (%)', fontsize=10)
            ax.set_title('Coupling Constants', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            for i, (n, e) in enumerate(zip(names, errors)):
                ax.text(i, e * 1.1, f'{e:.2f}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        output_file = FIGURES_DIR / 'ubp_particle_predictions.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved figure: {output_file}")
        plt.close()

    def plot_geometric_scaling(self):
        """Visualize the geometric scaling law."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        # Calculate Y and 1/Y
        Y = 0.264675430404527
        Y_inv = 3.778212425957375

        # Powers of 1/Y
        powers = np.arange(-16, 5)
        scaling_factors = [Y_inv ** p for p in powers]

        # Mark particle positions
        particles = {
            'Neutrinos\n(ν_e, ν_μ, ν_τ)': [-8, -12, -16],
            'Electron': [0],
            'Muon': [4],
            'Quarks\n(s/d, c/s)': [2],
            'Bottom/Charm': [1],
            'Proton': [4],  # With OffBits multiplier
        }

        ax.semilogy(powers, scaling_factors, 'o-', linewidth=2.5, markersize=10,
                   color='darkblue', label='(1/Y)^N scaling', alpha=0.7)

        colors_particle = ['red', 'green', 'orange', 'purple', 'brown', 'cyan']
        for i, (name, exponents) in enumerate(particles.items()):
            for exp in exponents:
                scale = Y_inv ** exp
                ax.plot(exp, scale, 's', markersize=12, color=colors_particle[i % len(colors_particle)],
                       label=name if exp == exponents[0] else '', alpha=0.8, markeredgecolor='black', markeredgewidth=1.5)

        ax.set_xlabel('Exponent N in (1/Y)^N', fontsize=12, fontweight='bold')
        ax.set_ylabel('Scaling Factor', fontsize=12, fontweight='bold')
        ax.set_title('UBP Geometric Scaling Law: (1/Y)^N\nY = π/(π²+2) ≈ 0.2647, 1/Y ≈ 3.778',
                    fontsize=13, fontweight='bold')
        ax.grid(alpha=0.4, which='both')
        ax.legend(loc='best', fontsize=10)

        # Add annotations
        ax.annotate('Dimensional\nSuppression\n(Neutrinos)', xy=(-12, Y_inv**(-12)), xytext=(-12, 1e-4),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='red'), fontsize=9, ha='center',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.annotate('Lepton\nGeneration\nJumps', xy=(4, Y_inv**4), xytext=(6, Y_inv**4 * 3),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='green'), fontsize=9, ha='left',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

        ax.annotate('Quark\nScaling', xy=(2, Y_inv**2), xytext=(2, Y_inv**2 / 3),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='orange'), fontsize=9, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

        plt.tight_layout()
        output_file = FIGURES_DIR / 'ubp_geometric_scaling.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved figure: {output_file}")
        plt.close()

    def generate_results_table(self):
        """Generate comprehensive results table."""
        print("\n" + "=" * 100)
        print("UBP COMPREHENSIVE PREDICTION TABLE")
        print("=" * 100)

        print(f"\n{'Particle':<20} {'Category':<15} {'Error %':<12} {'Formula/N':<30} {'Success':<10}")
        print("-" * 100)

        # Sort by category then error
        sorted_preds = sorted(self.all_predictions,
                            key=lambda x: (x['category'], x['error_percent'] if x['error_percent'] else 999))

        for pred in sorted_preds:
            if pred['error_percent'] is not None:
                success_mark = '✓' if pred.get('success', False) else '✗'
                formula_or_n = pred.get('formula', f"N={pred.get('N', '?')}" if pred.get('N') else '')
                if len(formula_or_n) > 28:
                    formula_or_n = formula_or_n[:25] + '...'

                print(f"{pred['particle']:<20} {pred['category']:<15} {pred['error_percent']:<12.4f} "
                     f"{formula_or_n:<30} {success_mark:<10}")

        print("-" * 100)

        # Save as JSON
        output_file = RESULTS_DIR / 'ubp_comprehensive_table.json'
        with open(output_file, 'w') as f:
            json.dump(self.all_predictions, f, indent=2)

        print(f"\nTable saved to: {output_file}")


def main():
    """Main execution."""
    print("\n" + "=" * 80)
    print("UBP COMPREHENSIVE STATISTICAL ANALYSIS")
    print("=" * 80)
    print()

    analyzer = UBPStatisticalAnalysis()

    # Generate statistics
    summary = analyzer.generate_summary_statistics()

    # Create plots
    print("\n" + "=" * 80)
    print("GENERATING PUBLICATION-QUALITY FIGURES")
    print("=" * 80)

    analyzer.plot_error_distribution()
    analyzer.plot_particle_predictions()
    analyzer.plot_geometric_scaling()

    # Generate tables
    analyzer.generate_results_table()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nAll figures saved to: {FIGURES_DIR}")
    print(f"All results saved to: {RESULTS_DIR}")


if __name__ == '__main__':
    main()
