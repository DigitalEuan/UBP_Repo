"""
Generate all 84 individual GeoBit signature images with clear labeling.
Each image will be saved with a descriptive filename for easy cataloging.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
import matplotlib.pyplot as plt
from ubp_pattern_library import create_ubp_pattern_library
import os

# Create output directory
output_dir = '/home/ubuntu/geobit_images'
os.makedirs(output_dir, exist_ok=True)

# Initialize library
print("Initializing GeoBit library...")
library = create_ubp_pattern_library()

# Get all signatures
all_signatures = list(library.signatures.values())
print(f"Found {len(all_signatures)} signatures")

# Generate each image
for i, sig in enumerate(all_signatures, 1):
    print(f"[{i}/{len(all_signatures)}] Generating: {sig.name}")
    
    # Generate pattern
    pattern = library.generate_pattern(sig.name)
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=200)
    
    # Plot pattern
    im = ax.imshow(pattern, cmap='twilight', interpolation='bilinear')
    ax.set_title(f"{sig.name}\n{sig.description}", fontsize=12, fontweight='bold')
    ax.axis('off')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Amplitude', rotation=270, labelpad=20)
    
    # Add metadata text
    if sig.unit == 'dimensionless':
        value_str = f"Value: {sig.value:.15f}"
    elif sig.unit == 'Hz':
        value_str = f"Frequency: {sig.value:.6e} Hz"
    elif sig.unit == 'CU':
        value_str = f"Energy: {sig.value:.6e} CU"
    else:
        value_str = f"Value: {sig.value:.6e} {sig.unit}"
    
    metadata_text = f"{value_str}\nCategory: {sig.category}\nPattern: {sig.pattern_type}"
    ax.text(0.02, 0.02, metadata_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Create safe filename
    safe_name = sig.name.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '')
    category_prefix = sig.category[:4].upper()  # First 4 letters of category
    filename = f"{category_prefix}_{i:03d}_{safe_name}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Save
    plt.savefig(filepath, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved: {filename}")

print(f"\n✓ All {len(all_signatures)} images generated successfully!")
print(f"Output directory: {output_dir}")

# Create index file
print("\nCreating index file...")
index_path = os.path.join(output_dir, 'INDEX.txt')
with open(index_path, 'w') as f:
    f.write("GeoBit Signature Library - Image Index\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total Signatures: {len(all_signatures)}\n")
    f.write(f"Generated: {library.metadata['generated']}\n\n")
    
    # Group by category
    categories = {}
    for sig in all_signatures:
        if sig.category not in categories:
            categories[sig.category] = []
        categories[sig.category].append(sig)
    
    for category, sigs in sorted(categories.items()):
        f.write(f"\n{category.upper()} ({len(sigs)} signatures)\n")
        f.write("-" * 80 + "\n")
        for i, sig in enumerate(sigs, 1):
            safe_name = sig.name.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '')
            category_prefix = sig.category[:4].upper()
            idx = all_signatures.index(sig) + 1
            filename = f"{category_prefix}_{idx:03d}_{safe_name}.png"
            
            if sig.unit == 'dimensionless':
                value_str = f"{sig.value:.15f}"
            elif sig.unit == 'Hz':
                value_str = f"{sig.value:.6e} Hz"
            elif sig.unit == 'CU':
                value_str = f"{sig.value:.6e} CU"
            else:
                value_str = f"{sig.value:.6e} {sig.unit}"
            
            f.write(f"  {i:2d}. {filename}\n")
            f.write(f"      Name: {sig.name}\n")
            f.write(f"      Value: {value_str}\n")
            f.write(f"      Description: {sig.description}\n")
            f.write(f"      Symmetry: {sig.symmetry}, Pattern: {sig.pattern_type}\n")
            f.write("\n")

print(f"✓ Index file created: {index_path}")
print("\nDone!")
