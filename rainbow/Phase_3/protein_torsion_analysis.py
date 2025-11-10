"""
Phase 3.2: Protein Folding Torsion Angle Analysis
Search for UBP geometric signatures (6φ, 10×6φ, 42°) in protein backbone torsion angles

This script demonstrates the methodology for analyzing real PDB data.
For production use, replace synthetic data with actual PDB torsion angles.
"""

import numpy as np
import matplotlib.pyplot as plt
import json

# Golden ratio and UBP constants
PHI_GR = 1.618033989  # Golden ratio
SIX_PHI = 6 * PHI_GR  # 9.708 (unitless)
TEN_SIX_PHI = 10 * SIX_PHI  # 97.08 (unitless)
SIX_PHI_DEG = SIX_PHI  # 9.708° (for torsion angles, already in degrees)
TEN_SIX_PHI_DEG = TEN_SIX_PHI  # 97.08°
DODEC_ANGLE = 42.0  # Dodecahedral signature

print("=" * 80)
print("Phase 3.2: Protein Torsion Angle Analysis")
print("=" * 80)
print(f"\nUBP Geometric Signatures:")
print(f"  6φ = {SIX_PHI_DEG:.3f}°")
print(f"  10×6φ = {TEN_SIX_PHI_DEG:.3f}°")
print(f"  Dodecahedral = {DODEC_ANGLE:.3f}°")
print()

# Known protein secondary structure torsion angles (from literature)
# These are well-established values from Ramachandran plot studies

KNOWN_STRUCTURES = {
    'alpha_helix': {
        'phi': -60.0,  # degrees
        'psi': -45.0,
        'description': 'Right-handed α-helix',
        'frequency': 0.32  # ~32% of residues
    },
    'beta_sheet': {
        'phi': -120.0,
        'psi': 120.0,
        'description': 'Extended β-sheet',
        'frequency': 0.23  # ~23% of residues
    },
    'left_alpha': {
        'phi': 60.0,
        'psi': 45.0,
        'description': 'Left-handed α-helix (rare)',
        'frequency': 0.01  # ~1% of residues
    },
    'collagen': {
        'phi': -60.0,
        'psi': 150.0,
        'description': 'Collagen helix',
        'frequency': 0.05  # ~5% of residues
    }
}

# Generate synthetic torsion angle distribution based on known structures
# In production, this would be replaced with actual PDB data
def generate_synthetic_protein_data(n_residues=100000):
    """
    Generate synthetic protein torsion angles based on known secondary structure distributions.
    
    In production, replace with:
    from Bio.PDB import PDBParser, PPBuilder
    parser = PDBParser()
    structure = parser.get_structure('protein', 'file.pdb')
    # Extract phi, psi angles using PPBuilder
    """
    phi_angles = []
    psi_angles = []
    structure_types = []
    
    for struct_name, struct_data in KNOWN_STRUCTURES.items():
        n = int(n_residues * struct_data['frequency'])
        phi_mean = struct_data['phi']
        psi_mean = struct_data['psi']
        
        # Add Gaussian noise to simulate natural variation
        phi_vals = np.random.normal(phi_mean, 15, n)  # 15° std dev
        psi_vals = np.random.normal(psi_mean, 15, n)
        
        phi_angles.extend(phi_vals)
        psi_angles.extend(psi_vals)
        structure_types.extend([struct_name] * n)
    
    # Add random coil (unstructured regions)
    n_coil = n_residues - len(phi_angles)
    phi_coil = np.random.uniform(-180, 180, n_coil)
    psi_coil = np.random.uniform(-180, 180, n_coil)
    phi_angles.extend(phi_coil)
    psi_angles.extend(psi_coil)
    structure_types.extend(['coil'] * n_coil)
    
    return np.array(phi_angles), np.array(psi_angles), structure_types

# Generate data
print("Generating synthetic protein torsion angle data...")
print("(In production, replace with actual PDB data extraction)")
phi_angles, psi_angles, structure_types = generate_synthetic_protein_data(100000)
print(f"Total residues analyzed: {len(phi_angles)}")
print()

# Create histograms
bins = np.arange(-180, 181, 1)  # 1° bins
hist_phi, bin_edges_phi = np.histogram(phi_angles, bins=bins)
hist_psi, bin_edges_psi = np.histogram(psi_angles, bins=bins)
bin_centers = (bin_edges_phi[:-1] + bin_edges_phi[1:]) / 2

# Search for peaks near UBP signatures
def find_peak_near(hist, bin_centers, target, tolerance=2):
    """Find histogram peak near target angle"""
    mask = np.abs(bin_centers - target) <= tolerance
    if np.any(mask):
        idx = np.argmax(hist[mask])
        actual_bins = bin_centers[mask]
        actual_counts = hist[mask]
        return actual_bins[idx], actual_counts[idx]
    return None, 0

# Test for UBP signatures
signatures_to_test = [
    ('6φ', SIX_PHI_DEG),
    ('10×6φ', TEN_SIX_PHI_DEG),
    ('42° (dodec)', DODEC_ANGLE),
    ('-6φ', -SIX_PHI_DEG),
    ('-10×6φ', -TEN_SIX_PHI_DEG),
    ('-42°', -DODEC_ANGLE),
]

print("=" * 80)
print("Searching for UBP Geometric Signatures")
print("=" * 80)

results = {}
for name, target in signatures_to_test:
    phi_angle, phi_count = find_peak_near(hist_phi, bin_centers, target)
    psi_angle, psi_count = find_peak_near(hist_psi, bin_centers, target)
    
    # Calculate statistical significance (compared to random baseline)
    mean_count = np.mean(hist_phi)
    std_count = np.std(hist_phi)
    
    phi_sigma = (phi_count - mean_count) / std_count if std_count > 0 else 0
    psi_sigma = (psi_count - mean_count) / std_count if std_count > 0 else 0
    
    results[name] = {
        'target': target,
        'phi': {'angle': phi_angle, 'count': int(phi_count), 'sigma': phi_sigma},
        'psi': {'angle': psi_angle, 'count': int(psi_count), 'sigma': psi_sigma}
    }
    
    print(f"\n{name} ({target:.2f}°):")
    phi_str = f"{phi_angle:.2f}" if phi_angle is not None else "N/A"
    psi_str = f"{psi_angle:.2f}" if psi_angle is not None else "N/A"
    print(f"  φ: {phi_str}° (count={phi_count}, σ={phi_sigma:.2f})")
    print(f"  ψ: {psi_str}° (count={psi_count}, σ={psi_sigma:.2f})")
    
    if phi_sigma > 2 or psi_sigma > 2:
        print(f"  *** SIGNIFICANT PEAK DETECTED (>2σ) ***")

# Save results
with open('/home/ubuntu/rainbow_phase3/protein_torsion_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print("Creating Visualizations")
print("=" * 80)

# Create comprehensive visualization
fig = plt.figure(figsize=(16, 12))

# 1. Ramachandran plot with UBP signature overlays
ax1 = plt.subplot(2, 3, 1)
plt.hexbin(phi_angles, psi_angles, gridsize=50, cmap='Blues', mincnt=1)
plt.colorbar(label='Count')
plt.xlabel('φ (degrees)', fontsize=12)
plt.ylabel('ψ (degrees)', fontsize=12)
plt.title('Ramachandran Plot with UBP Signatures', fontsize=14, fontweight='bold')

# Overlay UBP signature lines
plt.axvline(SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, label=f'6φ = {SIX_PHI_DEG:.2f}°', alpha=0.7)
plt.axhline(SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, alpha=0.7)
plt.axvline(-SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, alpha=0.7)
plt.axhline(-SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, alpha=0.7)

plt.axvline(DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, label=f'42° (dodec)', alpha=0.7)
plt.axhline(DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, alpha=0.7)
plt.axvline(-DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, alpha=0.7)
plt.axhline(-DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, alpha=0.7)

plt.legend(fontsize=10, loc='upper right')
plt.grid(True, alpha=0.3)
plt.xlim(-180, 180)
plt.ylim(-180, 180)

# 2. φ angle histogram
ax2 = plt.subplot(2, 3, 2)
plt.plot(bin_centers, hist_phi, 'b-', linewidth=1, alpha=0.7)
plt.xlabel('φ (degrees)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('φ Angle Distribution', fontsize=14, fontweight='bold')

# Mark UBP signatures
plt.axvline(SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, label=f'6φ = {SIX_PHI_DEG:.2f}°')
plt.axvline(-SIX_PHI_DEG, color='red', linestyle='--', linewidth=2)
plt.axvline(DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, label=f'42°')
plt.axvline(-DODEC_ANGLE, color='orange', linestyle=':', linewidth=2)
plt.axvline(TEN_SIX_PHI_DEG, color='purple', linestyle='-.', linewidth=2, label=f'10×6φ = {TEN_SIX_PHI_DEG:.2f}°')
plt.axvline(-TEN_SIX_PHI_DEG, color='purple', linestyle='-.', linewidth=2)

plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(-180, 180)

# 3. ψ angle histogram
ax3 = plt.subplot(2, 3, 3)
plt.plot(bin_centers, hist_psi, 'g-', linewidth=1, alpha=0.7)
plt.xlabel('ψ (degrees)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('ψ Angle Distribution', fontsize=14, fontweight='bold')

# Mark UBP signatures
plt.axvline(SIX_PHI_DEG, color='red', linestyle='--', linewidth=2, label=f'6φ = {SIX_PHI_DEG:.2f}°')
plt.axvline(-SIX_PHI_DEG, color='red', linestyle='--', linewidth=2)
plt.axvline(DODEC_ANGLE, color='orange', linestyle=':', linewidth=2, label=f'42°')
plt.axvline(-DODEC_ANGLE, color='orange', linestyle=':', linewidth=2)
plt.axvline(TEN_SIX_PHI_DEG, color='purple', linestyle='-.', linewidth=2, label=f'10×6φ = {TEN_SIX_PHI_DEG:.2f}°')
plt.axvline(-TEN_SIX_PHI_DEG, color='purple', linestyle='-.', linewidth=2)

plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(-180, 180)

# 4. Zoomed φ histogram (around 6φ)
ax4 = plt.subplot(2, 3, 4)
zoom_range = 30
mask = np.abs(bin_centers - SIX_PHI_DEG) < zoom_range
plt.bar(bin_centers[mask], hist_phi[mask], width=1, color='blue', alpha=0.6)
plt.axvline(SIX_PHI_DEG, color='red', linestyle='--', linewidth=3, label=f'6φ = {SIX_PHI_DEG:.2f}°')
plt.xlabel('φ (degrees)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title(f'φ Distribution Near 6φ (±{zoom_range}°)', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# 5. Zoomed φ histogram (around 42°)
ax5 = plt.subplot(2, 3, 5)
mask = np.abs(bin_centers - DODEC_ANGLE) < zoom_range
plt.bar(bin_centers[mask], hist_phi[mask], width=1, color='blue', alpha=0.6)
plt.axvline(DODEC_ANGLE, color='orange', linestyle=':', linewidth=3, label=f'42° (dodec)')
plt.xlabel('φ (degrees)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title(f'φ Distribution Near 42° (±{zoom_range}°)', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# 6. Statistical significance plot
ax6 = plt.subplot(2, 3, 6)
sig_names = [name for name in results.keys()]
phi_sigmas = [results[name]['phi']['sigma'] for name in sig_names]
psi_sigmas = [results[name]['psi']['sigma'] for name in sig_names]

x = np.arange(len(sig_names))
width = 0.35

plt.bar(x - width/2, phi_sigmas, width, label='φ', color='blue', alpha=0.7)
plt.bar(x + width/2, psi_sigmas, width, label='ψ', color='green', alpha=0.7)
plt.axhline(2, color='red', linestyle='--', linewidth=2, label='2σ threshold')
plt.axhline(-2, color='red', linestyle='--', linewidth=2)
plt.xlabel('UBP Signature', fontsize=12)
plt.ylabel('Statistical Significance (σ)', fontsize=12)
plt.title('Peak Significance at UBP Angles', fontsize=14, fontweight='bold')
plt.xticks(x, sig_names, rotation=45, ha='right')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/home/ubuntu/rainbow_phase3/protein_torsion_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print("Visualization saved: protein_torsion_analysis.png")

# Analysis summary
print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

print("\n**Key Findings:**")
print("\n1. **Methodology Validated:**")
print("   - Histogram binning at 1° resolution")
print("   - Peak detection within ±2° tolerance")
print("   - Statistical significance testing (σ)")

print("\n2. **Known Secondary Structures:**")
for name, data in KNOWN_STRUCTURES.items():
    print(f"   - {data['description']}: φ={data['phi']:.1f}°, ψ={data['psi']:.1f}° ({data['frequency']*100:.0f}%)")

print("\n3. **UBP Signature Search:**")
for name, data in results.items():
    phi_sig = data['phi']['sigma']
    psi_sig = data['psi']['sigma']
    if phi_sig > 2 or psi_sig > 2:
        print(f"   ✓ {name}: SIGNIFICANT (φ σ={phi_sig:.2f}, ψ σ={psi_sig:.2f})")
    else:
        print(f"   - {name}: Not significant (φ σ={phi_sig:.2f}, ψ σ={psi_sig:.2f})")

print("\n4. **Next Steps for Real PDB Data:**")
print("   a) Install BioPython: pip install biopython")
print("   b) Download PDB files from RCSB PDB (https://www.rcsb.org/)")
print("   c) Extract torsion angles using Bio.PDB.PPBuilder")
print("   d) Run this analysis on real data")
print("   e) Compare water-exposed vs buried residues")
print("   f) Test for spiral patterns in Ramachandran space")

print("\n5. **Hypothesis for Real Data:**")
print("   - Water-exposed loops: Expect 6φ and 10×6φ signatures")
print("   - α-helices: 100° pitch ≈ 3×6φ (29.1°) per residue?")
print("   - β-sheets: Twist angle ~30° ≈ 3×6φ?")
print("   - Buried regions: Weaker signatures (no transduction)")

print("\n" + "=" * 80)
print("Analysis complete!")
print("=" * 80)
