"""
Generate visual catalog of GeoBit signatures.

This creates a comprehensive visual reference showing all geometric patterns
in the UBP library.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ubp_pattern_library import create_ubp_pattern_library

print("Generating GeoBit Visual Catalog...")

# Create library
lib = create_ubp_pattern_library()

# Categories to visualize
categories = {
    'constant': "Fundamental Constants",
    'realm': "Realm Frequencies",
    'harmonic': "Harmonic Series",
    'frequency': "Common Frequencies",
    'energy': "Energy Scales",
    'derived': "Derived Values",
    'special': "Special UBP Values"
}

for category, title in categories.items():
    print(f"\nGenerating {title}...")
    
    # Get signatures for this category
    sigs = lib.find_signatures(category=category)
    
    if len(sigs) == 0:
        continue
    
    # Limit to first 20 for visualization
    sigs = sigs[:20]
    
    # Calculate grid size
    n_sigs = len(sigs)
    n_cols = min(5, n_sigs)
    n_rows = (n_sigs + n_cols - 1) // n_cols
    
    # Create figure
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*3, n_rows*3))
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)
    
    fig.suptitle(f"GeoBit Catalog: {title}", fontsize=16, fontweight='bold')
    
    for idx, sig in enumerate(sigs):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        
        # Generate pattern
        pattern = lib.generate_pattern(sig.name)
        
        if pattern is not None:
            # Display pattern
            im = ax.imshow(pattern, cmap='RdBu_r', interpolation='bilinear')
            
            # Title with name and value
            if sig.value >= 1e6 or sig.value <= 1e-6:
                value_str = f"{sig.value:.2e}"
            else:
                value_str = f"{sig.value:.6f}"
            
            title_str = f"{sig.name}\n{value_str} {sig.unit}"
            ax.set_title(title_str, fontsize=8)
        else:
            ax.text(0.5, 0.5, 'Pattern\nGeneration\nFailed', 
                   ha='center', va='center', transform=ax.transAxes)
        
        ax.axis('off')
    
    # Hide empty subplots
    for idx in range(n_sigs, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    
    # Save
    filename = f"/home/ubuntu/UBP_Repo/Studies/geobit_catalog_{category}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved: {filename} ({n_sigs} patterns)")

# Create a master catalog with key signatures
print("\nGenerating Master Catalog (key signatures)...")

key_signatures = [
    'Y_constant',
    'Y_inverse',
    'pi',
    'golden_ratio',
    'fine_structure',
    'quantum_main_crv',
    'electromagnetic_main_crv',
    'gravitational_main_crv',
    'plasma_main_crv',
    'nuclear_main_crv',
    'optical_main_crv',
    'biologic_main_crv',
    'schumann_resonance',
    'hydrogen_line_21cm',
    'planck_energy',
    'pgci_target'
]

fig, axes = plt.subplots(4, 4, figsize=(16, 16))
fig.suptitle("GeoBit Master Catalog: Key UBP Signatures", fontsize=20, fontweight='bold')

for idx, name in enumerate(key_signatures):
    row = idx // 4
    col = idx % 4
    ax = axes[row, col]
    
    sig = lib.get_signature(name)
    if sig:
        pattern = lib.generate_pattern(name)
        
        if pattern is not None:
            im = ax.imshow(pattern, cmap='RdBu_r', interpolation='bilinear')
            
            # Format value
            if sig.value >= 1e6 or sig.value <= 1e-6:
                value_str = f"{sig.value:.2e}"
            else:
                value_str = f"{sig.value:.6f}"
            
            # Title with description
            title_str = f"{sig.name}\n{value_str} {sig.unit}\n{sig.description[:40]}"
            ax.set_title(title_str, fontsize=9, fontweight='bold')
            
            # Add colorbar
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    ax.axis('off')

plt.tight_layout()
plt.savefig("/home/ubuntu/UBP_Repo/Studies/geobit_master_catalog.png", dpi=200, bbox_inches='tight')
plt.close()

print("  Saved: geobit_master_catalog.png")

# Generate comparison chart showing octave relationships
print("\nGenerating Octave Relationship Chart...")

fig, ax = plt.subplots(figsize=(16, 10))

# Get all signatures with positive values
all_sigs = [sig for sig in lib.signatures.values() if sig.value > 0]

# Sort by octave class
all_sigs.sort(key=lambda s: s.octave_class)

# Plot octave classes
categories_color = {
    'constant': 'red',
    'realm': 'blue',
    'harmonic': 'green',
    'frequency': 'orange',
    'energy': 'purple',
    'derived': 'brown',
    'special': 'pink'
}

for sig in all_sigs:
    color = categories_color.get(sig.category, 'gray')
    ax.scatter(sig.octave_class, 1, c=color, s=100, alpha=0.6, edgecolors='black')
    
    # Label key signatures
    if sig.name in key_signatures[:8]:
        ax.annotate(sig.name, (sig.octave_class, 1), 
                   xytext=(0, 20), textcoords='offset points',
                   ha='center', fontsize=8, rotation=45,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))

ax.set_xlabel('Octave Class (log₂ of value)', fontsize=14, fontweight='bold')
ax.set_ylabel('', fontsize=14)
ax.set_title('UBP GeoBit Signatures: Octave Distribution', fontsize=16, fontweight='bold')
ax.set_yticks([])
ax.grid(True, alpha=0.3)

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=cat.capitalize()) 
                  for cat, color in categories_color.items()]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Add Y-constant markers
Y_octave = np.log2(lib.get_signature('Y_constant').value)
ax.axvline(Y_octave, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Y constant')
ax.axvline(-Y_octave, color='red', linestyle='--', linewidth=2, alpha=0.5, label='1/Y')

plt.tight_layout()
plt.savefig("/home/ubuntu/UBP_Repo/Studies/geobit_octave_chart.png", dpi=150, bbox_inches='tight')
plt.close()

print("  Saved: geobit_octave_chart.png")

print("\n" + "="*80)
print("GEOBIT VISUAL CATALOG COMPLETE")
print("="*80)
print(f"Total patterns generated: {len(lib.signatures)}")
print(f"Files created:")
print(f"  - geobit_master_catalog.png (16 key signatures)")
print(f"  - geobit_octave_chart.png (octave distribution)")
for category in categories.keys():
    print(f"  - geobit_catalog_{category}.png")
print("="*80)
