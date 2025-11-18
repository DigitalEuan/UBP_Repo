#!/usr/bin/env python3.11
"""
Create Feature Distribution Visualizations
UBP Symbol Study Phase 2 (Refined)

Generates publication-quality visualizations of D5 and D6 distributions
across the baseline dataset.

Author: Manus AI
Date: Nov 18, 2025
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load baseline data
with open('/home/ubuntu/ubp_symbol_study_phase2_refined/data/baseline_normalized.json', 'r') as f:
    baseline = json.load(f)

# Extract D5 and D6
d5_values = [s['bitfield_d5'] for s in baseline]
d6_values = [s['bitfield_d6'] for s in baseline]
nrci_values = [s['nrci'] for s in baseline]

# Create figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Plot 1: D5 distribution
axes[0].hist(d5_values, bins=30, color='steelblue', alpha=0.7, edgecolor='black')
axes[0].set_xlabel('D5 (Meaning Count)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Distribution of D5 (Meaning Count)', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].axvline(np.mean(d5_values), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(d5_values):.3f}')
axes[0].legend()

# Plot 2: D6 distribution
axes[1].hist(d6_values, bins=30, color='darkorange', alpha=0.7, edgecolor='black')
axes[1].set_xlabel('D6 (Dependency Depth)', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('Distribution of D6 (Dependency Depth)', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].axvline(np.mean(d6_values), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(d6_values):.3f}')
axes[1].legend()

# Plot 3: D5 vs D6 scatter with NRCI color
scatter = axes[2].scatter(d5_values, d6_values, c=nrci_values, cmap='viridis', alpha=0.6, s=20)
axes[2].set_xlabel('D5 (Meaning Count)', fontsize=12)
axes[2].set_ylabel('D6 (Dependency Depth)', fontsize=12)
axes[2].set_title('D5 vs D6 (colored by NRCI)', fontsize=14, fontweight='bold')
axes[2].grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=axes[2])
cbar.set_label('NRCI', fontsize=12)

plt.tight_layout()
plt.savefig('/home/ubuntu/ubp_symbol_study_phase2_refined/results/feature_distributions.png', dpi=300, bbox_inches='tight')
print("Feature distribution plot saved to results/feature_distributions.png")
