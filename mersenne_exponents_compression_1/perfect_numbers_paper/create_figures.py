#!/usr/bin/env python3
"""
Create publication-quality figures for the Binary-Geometric Dualism paper
All data is extracted from actual computational results - no fabrication
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rcParams['text.usetex'] = False  # Avoid LaTeX rendering issues
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Load extracted data
data_path = Path('/home/ubuntu/perfect_numbers_paper/data/extracted_data.json')
with open(data_path, 'r') as f:
    data = json.load(f)

figures_dir = Path('/home/ubuntu/perfect_numbers_paper/figures')
figures_dir.mkdir(exist_ok=True)

# Extract key variables
mersenne_exponents = data['mersenne_exponents']
growth_ratios = data['growth_ratios']
avg_growth_ratio = data['avg_growth_ratio']
differences = data['differences']
Y = data['constants']['Y']
Y_inv = data['constants']['Y_inv']
Y_squared = data['constants']['Y_squared']
Y_inv_squared = data['constants']['Y_inv_squared']
binary_analysis = data['binary_analysis']

print("Creating Figure 1: Mersenne Exponent Growth and Scaling...")

# Figure 1: Mersenne Exponent Growth
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

# Subplot 1: Exponents vs Index (log scale)
n_indices = np.arange(len(mersenne_exponents))
ax1.semilogy(n_indices, mersenne_exponents, 'o-', color='#2E86AB', 
             markersize=6, linewidth=1.5, label='Mersenne exponents $p_n$')

# Add power law fit
coeffs = np.polyfit(n_indices, np.log10(mersenne_exponents), 1)
slope, intercept = coeffs
fit_line = 10**(slope * n_indices + intercept)
ax1.semilogy(n_indices, fit_line, '--', color='#A23B72', linewidth=2, 
             label=f'Power law fit: $\\log_{{10}}(p) \\approx {slope:.4f}n + {intercept:.4f}$')

ax1.set_xlabel('Index $n$')
ax1.set_ylabel('Mersenne exponent $p_n$')
ax1.set_title('(a) Exponential Growth of Mersenne Exponents')
ax1.legend(loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')

# Subplot 2: Growth ratios
ax2.plot(range(1, len(growth_ratios)+1), growth_ratios, 'o-', 
         color='#F18F01', markersize=6, linewidth=1.5, label='$p_n / p_{n-1}$')
ax2.axhline(y=avg_growth_ratio, color='#C73E1D', linestyle='--', 
            linewidth=2, label=f'Average: $r = {avg_growth_ratio:.4f}$')
ax2.axhline(y=Y_inv, color='#6A4C93', linestyle=':', 
            linewidth=2, label=f'$Y^{{-1}} = {Y_inv:.4f}$')
ax2.set_xlabel('Index $n$')
ax2.set_ylabel('Growth ratio $r_n$')
ax2.set_title('(b) Sequential Growth Ratios')
ax2.legend(loc='upper right', framealpha=0.9)
ax2.grid(True, alpha=0.3, linestyle='--')

# Subplot 3: Differences between consecutive exponents
ax3.plot(range(1, len(differences)+1), differences, 'o-', 
         color='#06A77D', markersize=6, linewidth=1.5)
ax3.set_xlabel('Index $n$')
ax3.set_ylabel('Difference $\\Delta p_n = p_n - p_{n-1}$')
ax3.set_title('(c) Gaps Between Consecutive Exponents')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_yscale('log')

# Subplot 4: Cumulative distribution
cumulative = np.cumsum([1] * len(mersenne_exponents))
ax4.plot(mersenne_exponents, cumulative, 'o-', 
         color='#8338EC', markersize=6, linewidth=1.5)
ax4.set_xlabel('Mersenne exponent $p$')
ax4.set_ylabel('Cumulative count')
ax4.set_title('(d) Cumulative Distribution of Exponents')
ax4.grid(True, alpha=0.3, linestyle='--')
ax4.set_xscale('log')

plt.tight_layout()
plt.savefig(figures_dir / 'fig1_mersenne_growth.pdf', bbox_inches='tight')
plt.savefig(figures_dir / 'fig1_mersenne_growth.png', bbox_inches='tight')
plt.close()

print("Creating Figure 2: Binary Compression Analysis...")

# Figure 2: Binary Compression
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

# Extract compression data
exponents = [b['exponent'] for b in binary_analysis]
binary_lengths = [b['binary_length'] for b in binary_analysis]
compressed_sizes = [b['compressed_size'] for b in binary_analysis]
compression_ratios = [b['compression_ratio'] for b in binary_analysis]
space_savings = [b['space_savings'] for b in binary_analysis]

# Subplot 1: Binary length vs compressed size
ax1.plot(exponents, binary_lengths, 'o-', color='#2E86AB', 
         markersize=7, linewidth=2, label='Binary length $(2p-1)$')
ax1.plot(exponents, compressed_sizes, 's-', color='#A23B72', 
         markersize=7, linewidth=2, label='Compressed size $\\lceil\\log_2(p)\\rceil$')
ax1.set_xlabel('Exponent $p$')
ax1.set_ylabel('Size (bits)')
ax1.set_title('(a) Raw vs Compressed Representation')
ax1.legend(loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')

# Subplot 2: Compression ratio
ax2.plot(exponents, compression_ratios, 'o-', color='#F18F01', 
         markersize=7, linewidth=2)
ax2.set_xlabel('Exponent $p$')
ax2.set_ylabel('Compression ratio')
ax2.set_title('(b) Compression Efficiency (compressed/raw)')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_ylim([0, 1])

# Subplot 3: Space savings percentage
ax3.plot(exponents, space_savings, 'o-', color='#06A77D', 
         markersize=7, linewidth=2)
ax3.set_xlabel('Exponent $p$')
ax3.set_ylabel('Space savings (\%)')
ax3.set_title('(c) Asymptotic Compression Approaching 100\%')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_ylim([0, 100])

# Subplot 4: Binary structure visualization (first few perfect numbers)
ax4.axis('off')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 5)
ax4.set_title('(d) Binary Structure of Perfect Numbers', pad=10)

y_pos = 4.5
for i in range(min(5, len(binary_analysis))):
    b = binary_analysis[i]
    p = b['exponent']
    n = b['perfect_number']
    binary = bin(n)[2:]
    
    # Show structure
    text = f"$p={p}$: " + '1'*p + '0'*(p-1)
    ax4.text(0.5, y_pos, text, fontsize=9, family='monospace', 
             verticalalignment='center')
    y_pos -= 0.8

plt.tight_layout()
plt.savefig(figures_dir / 'fig2_compression.pdf', bbox_inches='tight')
plt.savefig(figures_dir / 'fig2_compression.png', bbox_inches='tight')
plt.close()

print("Creating Figure 3: UBP Dimensional Coupling...")

# Figure 3: The Dimensional Link
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

# Subplot 1: Y constant relationships
constants_names = ['$Y$', '$Y^{-1}$', '$Y^2$', '$(Y^{-1})^2$']
constants_values = [Y, Y_inv, Y_squared, Y_inv_squared]
colors = ['#2E86AB', '#A23B72', '#F18F01', '#06A77D']

bars = ax1.bar(range(len(constants_names)), constants_values, color=colors, alpha=0.7, edgecolor='black')
ax1.set_xticks(range(len(constants_names)))
ax1.set_xticklabels(constants_names)
ax1.set_ylabel('Value')
ax1.set_title('(a) UBP Geometric Constants')
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, constants_values)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.4f}', ha='center', va='bottom', fontsize=8)

# Subplot 2: Dimensional coupling analysis
r_squared_Y_squared = (avg_growth_ratio**2) * Y_squared
log_slope = data['scaling']['log_slope']

coupling_data = {
    '$r^2 \\times Y^2$': r_squared_Y_squared,
    'Log slope': log_slope,
    'Error': abs(r_squared_Y_squared - log_slope)
}

bars = ax2.bar(range(len(coupling_data)), list(coupling_data.values()), 
               color=['#8338EC', '#C73E1D', '#FFB627'], alpha=0.7, edgecolor='black')
ax2.set_xticks(range(len(coupling_data)))
ax2.set_xticklabels(list(coupling_data.keys()))
ax2.set_ylabel('Value')
ax2.set_title('(b) Dimensional Coupling: $r^2 \\times Y^2$ vs Log Slope')
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# Add value labels
for bar, val in zip(bars, coupling_data.values()):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.4f}', ha='center', va='bottom', fontsize=8)

# Subplot 3: Tau/Mu ratio comparison
tau_mu_experimental = 16.8167
tau_mu_geometric = Y_inv_squared

ratio_data = {
    'Geometric\n$(Y^{-1})^2$': tau_mu_geometric,
    'Experimental\n$m_\\tau/m_\\mu$': tau_mu_experimental
}

bars = ax3.bar(range(len(ratio_data)), list(ratio_data.values()), 
               color=['#6A4C93', '#E63946'], alpha=0.7, edgecolor='black')
ax3.set_xticks(range(len(ratio_data)))
ax3.set_xticklabels(list(ratio_data.keys()))
ax3.set_ylabel('Mass ratio')
ax3.set_title('(c) $\\tau/\\mu$ Mass Ratio: Geometric vs Experimental')
ax3.grid(True, alpha=0.3, linestyle='--', axis='y')

# Add value labels
for bar, val in zip(bars, ratio_data.values()):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.4f}', ha='center', va='bottom', fontsize=8)

# Add error annotation
error_pct = abs(tau_mu_geometric - tau_mu_experimental) / tau_mu_experimental * 100
ax3.text(0.5, (tau_mu_geometric + tau_mu_experimental)/2, 
         f'Error: {error_pct:.2f}\%', 
         ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Subplot 4: Conceptual diagram
ax4.axis('off')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.set_title('(d) Binary-Geometric Dualism Framework', pad=10)

# Draw conceptual boxes
# Y constant at center
rect_y = mpatches.FancyBboxPatch((3.5, 4.5), 3, 1, boxstyle="round,pad=0.1", 
                                  edgecolor='black', facecolor='#FFD700', linewidth=2)
ax4.add_patch(rect_y)
ax4.text(5, 5, '$Y = \\pi/(\\pi^2+2)$', ha='center', va='center', fontsize=11, weight='bold')

# Lepton sector (top)
rect_lepton = mpatches.FancyBboxPatch((1, 7), 3, 1.5, boxstyle="round,pad=0.1",
                                       edgecolor='black', facecolor='#A8DADC', linewidth=1.5)
ax4.add_patch(rect_lepton)
ax4.text(2.5, 7.75, 'Lepton Masses\n$(Y^{-1})^k$', ha='center', va='center', fontsize=9)

# Perfect number sector (bottom)
rect_perfect = mpatches.FancyBboxPatch((6, 7), 3, 1.5, boxstyle="round,pad=0.1",
                                        edgecolor='black', facecolor='#F4A261', linewidth=1.5)
ax4.add_patch(rect_perfect)
ax4.text(7.5, 7.75, 'Perfect Numbers\n$r \\sim Y$', ha='center', va='center', fontsize=9)

# Arrows
ax4.annotate('', xy=(2.5, 7), xytext=(4, 5.5), 
             arrowprops=dict(arrowstyle='->', lw=2, color='#457B9D'))
ax4.annotate('', xy=(7.5, 7), xytext=(6, 5.5),
             arrowprops=dict(arrowstyle='->', lw=2, color='#457B9D'))

# Labels
ax4.text(2.8, 6.2, 'Leech\nlattice', ha='center', fontsize=8, style='italic')
ax4.text(7.2, 6.2, 'Prime\nlattice', ha='center', fontsize=8, style='italic')

# Bottom text
ax4.text(5, 2, 'Dual manifestations of universal\nbinary-geometric resonance', 
         ha='center', fontsize=9, style='italic',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig(figures_dir / 'fig3_dimensional_coupling.pdf', bbox_inches='tight')
plt.savefig(figures_dir / 'fig3_dimensional_coupling.png', bbox_inches='tight')
plt.close()

print("Creating Figure 4: Algorithmic Complexity...")

# Figure 4: Compression comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Subplot 1: Compression methods comparison
compression_methods = ['Raw\n(64-bit)', 'Delta\nencoding', 'Power law\n+ residuals']
compression_sizes = [
    data['compression']['raw_size'],
    data['compression']['delta_encoding_size'],
    464  # From the mersenne_exponents_compression_1.txt results
]
compression_colors = ['#E63946', '#06A77D', '#8338EC']

bars = ax1.bar(range(len(compression_methods)), compression_sizes, 
               color=compression_colors, alpha=0.7, edgecolor='black')
ax1.set_xticks(range(len(compression_methods)))
ax1.set_xticklabels(compression_methods)
ax1.set_ylabel('Storage size (bits)')
ax1.set_title('(a) Compression Methods for 20 Mersenne Exponents')
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')

# Add value labels and compression ratios
for i, (bar, size) in enumerate(zip(bars, compression_sizes)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{size} bits\n({size/compression_sizes[0]:.2%})', 
             ha='center', va='bottom', fontsize=8)

# Subplot 2: Kolmogorov complexity concept
ax2.axis('off')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_title('(b) Infinite Compression Theorem', pad=10)

# Text content
theorem_text = (
    "Perfect numbers can be compressed from\n"
    "infinitely many ~$2^p$ bit representations to:\n\n"
    "1. Sequence of exponents $\\{p_n\\}$\n"
    "2. Euclid-Euler formula: $N = 2^{p-1}(2^p-1)$\n\n"
    "Further compression via:\n"
    "• Power-law scaling: $p_n \\sim n^{4.32}$\n"
    "• Dimensional structure: $D \\approx 4.56$\n"
    "• Binary pattern: $p$ ones + $(p-1)$ zeros"
)

ax2.text(5, 5, theorem_text, ha='center', va='center', fontsize=9,
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF3B0', 
                   edgecolor='black', linewidth=1.5),
         linespacing=1.5)

plt.tight_layout()
plt.savefig(figures_dir / 'fig4_compression_methods.pdf', bbox_inches='tight')
plt.savefig(figures_dir / 'fig4_compression_methods.png', bbox_inches='tight')
plt.close()

print("\nAll figures created successfully!")
print(f"Figures saved to: {figures_dir}")
print("\nFigure summary:")
print("  - fig1_mersenne_growth.pdf/png: Mersenne exponent growth and scaling")
print("  - fig2_compression.pdf/png: Binary compression analysis")
print("  - fig3_dimensional_coupling.pdf/png: UBP dimensional coupling")
print("  - fig4_compression_methods.pdf/png: Algorithmic complexity comparison")
