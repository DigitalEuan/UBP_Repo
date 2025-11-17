"""
Bitfield Spatial Analysis: 3D Information Geometry of Minerals
================================================================

Maps minerals and non-minerals into 3D information space (the "Bitfield")
to reveal spatial structure, clustering, boundaries, and voids.

Approach:
1. Extract information-theoretic features from minerals
2. Project to 3D using PCA on feature space
3. Add non-minerals (impossible structures) for contrast
4. Visualize in 3D scatter plot
5. Analyze spatial patterns

The Bitfield represents the INFORMATION SPACE where coherent structures can exist.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import math

# Load v3.1 results
with open('/home/ubuntu/ubp_mineral_study/results/mineral_coherence_v3_1_aggressive.json', 'r') as f:
    data = json.load(f)

results = data['results']

print("=" * 80)
print("BITFIELD SPATIAL ANALYSIS: 3D INFORMATION GEOMETRY")
print("=" * 80)
print()

# ============================================================================
# Step 1: Extract Information-Theoretic Features
# ============================================================================

print("Step 1: Extracting information-theoretic features...")
print()

# Define feature vector for each mineral
features = []
labels = []
pass_fail = []
crystal_systems = []

for r in results:
    # Feature vector (8 dimensions):
    # 1. Z (atomic number)
    # 2. Symmetry order
    # 3. I_cmplx (information complexity)
    # 4. Final NRCI
    # 5. Net refinements
    # 6. Total degradation
    # 7. Refinement/Degradation ratio
    # 8. Base NRCI
    
    I_cmplx = r['Z'] / r['metadata']['symmetry_order']
    ratio = r['net_refinements'] / r['total_degradation'] if r['total_degradation'] > 0 else 999
    
    feature_vec = [
        r['Z'],
        r['metadata']['symmetry_order'],
        I_cmplx,
        r['final_nrci'],
        r['net_refinements'],
        r['total_degradation'],
        ratio,
        r['base_nrci']
    ]
    
    features.append(feature_vec)
    labels.append(r['name'])
    pass_fail.append(1 if r['passes_natural'] else 0)
    crystal_systems.append(r['crystal_system'])

features = np.array(features)
print(f"Extracted {len(features)} mineral feature vectors (8D)")
print(f"  Passed: {sum(pass_fail)}")
print(f"  Failed: {len(pass_fail) - sum(pass_fail)}")
print()

# ============================================================================
# Step 2: Create Non-Minerals (Impossible Structures)
# ============================================================================

print("Step 2: Creating non-mineral structures for contrast...")
print()

non_minerals = []
non_mineral_labels = []

# Type 1: High Z + Low Symmetry (should be far outside coherent basin)
non_minerals.append({
    'name': 'NonMineral_1_U_triclinic',
    'Z': 92,  # Uranium
    'symmetry_order': 2,  # Triclinic (lowest)
    'crystal_system': 'triclinic',
    'I_cmplx': 92 / 2,
    'base_nrci': 0.998,
    'net_refinements': 2,
    'total_degradation': 5.0,
    'final_nrci': 0.95,
    'passes_natural': False
})

# Type 2: Extreme I_cmplx (Z=80, monoclinic)
non_minerals.append({
    'name': 'NonMineral_2_Hg_monoclinic',
    'Z': 80,  # Mercury
    'symmetry_order': 4,  # Monoclinic
    'crystal_system': 'monoclinic',
    'I_cmplx': 80 / 4,
    'base_nrci': 0.999,
    'net_refinements': 3,
    'total_degradation': 4.5,
    'final_nrci': 0.96,
    'passes_natural': False
})

# Type 3: Bottleneck + Low Symmetry
non_minerals.append({
    'name': 'NonMineral_3_Pb_triclinic',
    'Z': 82,  # Lead
    'symmetry_order': 2,  # Triclinic
    'crystal_system': 'triclinic',
    'I_cmplx': 82 / 2,
    'base_nrci': 0.998,
    'net_refinements': 2,
    'total_degradation': 4.8,
    'final_nrci': 0.94,
    'passes_natural': False
})

# Type 4: Very high Z (beyond bottleneck)
non_minerals.append({
    'name': 'NonMineral_4_Pu_orthorhombic',
    'Z': 94,  # Plutonium
    'symmetry_order': 8,  # Orthorhombic
    'crystal_system': 'orthorhombic',
    'I_cmplx': 94 / 8,
    'base_nrci': 0.9995,
    'net_refinements': 4,
    'total_degradation': 5.5,
    'final_nrci': 0.93,
    'passes_natural': False
})

# Type 5: Random invalid (high Z, low symmetry, extreme degradation)
non_minerals.append({
    'name': 'NonMineral_5_Ra_triclinic',
    'Z': 88,  # Radium
    'symmetry_order': 2,  # Triclinic
    'crystal_system': 'triclinic',
    'I_cmplx': 88 / 2,
    'base_nrci': 0.998,
    'net_refinements': 2,
    'total_degradation': 6.0,
    'final_nrci': 0.92,
    'passes_natural': False
})

# Type 6: Moderate Z but extreme low symmetry
non_minerals.append({
    'name': 'NonMineral_6_Fe_triclinic',
    'Z': 26,  # Iron
    'symmetry_order': 2,  # Triclinic (unusual for Fe)
    'crystal_system': 'triclinic',
    'I_cmplx': 26 / 2,
    'base_nrci': 0.998,
    'net_refinements': 2,
    'total_degradation': 2.0,
    'final_nrci': 0.97,
    'passes_natural': False
})

# Type 7: High Z with moderate symmetry (should be in bottleneck void)
non_minerals.append({
    'name': 'NonMineral_7_Bi_tetragonal',
    'Z': 83,  # Bismuth
    'symmetry_order': 16,  # Tetragonal
    'crystal_system': 'tetragonal',
    'I_cmplx': 83 / 16,
    'base_nrci': 0.9998,
    'net_refinements': 5,
    'total_degradation': 4.2,
    'final_nrci': 0.98,
    'passes_natural': False
})

# Type 8: Extreme complexity (high Z, low sym, high deg)
non_minerals.append({
    'name': 'NonMineral_8_Th_monoclinic',
    'Z': 90,  # Thorium
    'symmetry_order': 4,  # Monoclinic
    'crystal_system': 'monoclinic',
    'I_cmplx': 90 / 4,
    'base_nrci': 0.999,
    'net_refinements': 3,
    'total_degradation': 5.8,
    'final_nrci': 0.91,
    'passes_natural': False
})

# Add non-minerals to feature space
for nm in non_minerals:
    ratio = nm['net_refinements'] / nm['total_degradation'] if nm['total_degradation'] > 0 else 999
    
    feature_vec = [
        nm['Z'],
        nm['symmetry_order'],
        nm['I_cmplx'],
        nm['final_nrci'],
        nm['net_refinements'],
        nm['total_degradation'],
        ratio,
        nm['base_nrci']
    ]
    
    features = np.vstack([features, feature_vec])
    labels.append(nm['name'])
    pass_fail.append(-1)  # -1 for non-minerals
    crystal_systems.append(nm['crystal_system'])
    non_mineral_labels.append(nm['name'])

print(f"Added {len(non_minerals)} non-mineral structures")
print(f"Total structures: {len(features)}")
print()

# ============================================================================
# Step 3: Standardize and Project to 3D
# ============================================================================

print("Step 3: Projecting to 3D information space...")
print()

# Standardize features (zero mean, unit variance)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# PCA to 3D
pca = PCA(n_components=3)
coords_3d = pca.fit_transform(features_scaled)

print(f"PCA explained variance: {pca.explained_variance_ratio_}")
print(f"  PC1: {pca.explained_variance_ratio_[0]*100:.1f}%")
print(f"  PC2: {pca.explained_variance_ratio_[1]*100:.1f}%")
print(f"  PC3: {pca.explained_variance_ratio_[2]*100:.1f}%")
print(f"  Total: {sum(pca.explained_variance_ratio_)*100:.1f}%")
print()

# Analyze PCA components
print("PCA Component Loadings (what each axis represents):")
feature_names = ['Z', 'Symmetry', 'I_cmplx', 'NRCI', 'Refinements', 'Degradation', 'Ratio', 'Base_NRCI']
for i in range(3):
    print(f"\n  PC{i+1} (explains {pca.explained_variance_ratio_[i]*100:.1f}%):")
    loadings = pca.components_[i]
    sorted_idx = np.argsort(np.abs(loadings))[::-1]
    for idx in sorted_idx[:4]:  # Top 4 contributors
        print(f"    {feature_names[idx]:12s}: {loadings[idx]:+.3f}")

print()

# ============================================================================
# Step 4: Analyze Spatial Structure
# ============================================================================

print("=" * 80)
print("SPATIAL STRUCTURE ANALYSIS")
print("=" * 80)
print()

# Separate coordinates by category
passed_coords = coords_3d[np.array(pass_fail) == 1]
failed_coords = coords_3d[np.array(pass_fail) == 0]
nonmineral_coords = coords_3d[np.array(pass_fail) == -1]

print(f"Coordinate statistics:")
print(f"  Passed minerals:  {len(passed_coords)} points")
print(f"  Failed minerals:  {len(failed_coords)} points")
print(f"  Non-minerals:     {len(nonmineral_coords)} points")
print()

# Calculate centroids
passed_centroid = np.mean(passed_coords, axis=0) if len(passed_coords) > 0 else np.zeros(3)
failed_centroid = np.mean(failed_coords, axis=0) if len(failed_coords) > 0 else np.zeros(3)
nonmineral_centroid = np.mean(nonmineral_coords, axis=0) if len(nonmineral_coords) > 0 else np.zeros(3)
origin = np.zeros(3)

print("Centroids:")
print(f"  Passed:      [{passed_centroid[0]:+.3f}, {passed_centroid[1]:+.3f}, {passed_centroid[2]:+.3f}]")
print(f"  Failed:      [{failed_centroid[0]:+.3f}, {failed_centroid[1]:+.3f}, {failed_centroid[2]:+.3f}]")
print(f"  Non-mineral: [{nonmineral_centroid[0]:+.3f}, {nonmineral_centroid[1]:+.3f}, {nonmineral_centroid[2]:+.3f}]")
print()

# Calculate distances from origin
passed_dists = np.linalg.norm(passed_coords, axis=1)
failed_dists = np.linalg.norm(failed_coords, axis=1)
nonmineral_dists = np.linalg.norm(nonmineral_coords, axis=1)

print("Distance from origin statistics:")
print(f"  Passed:      mean={np.mean(passed_dists):.3f}, std={np.std(passed_dists):.3f}, range=[{np.min(passed_dists):.3f}, {np.max(passed_dists):.3f}]")
print(f"  Failed:      mean={np.mean(failed_dists):.3f}, std={np.std(failed_dists):.3f}, range=[{np.min(failed_dists):.3f}, {np.max(failed_dists):.3f}]")
print(f"  Non-mineral: mean={np.mean(nonmineral_dists):.3f}, std={np.std(nonmineral_dists):.3f}, range=[{np.min(nonmineral_dists):.3f}, {np.max(nonmineral_dists):.3f}]")
print()

# Calculate inter-centroid distances
dist_passed_failed = np.linalg.norm(passed_centroid - failed_centroid)
dist_passed_nonmineral = np.linalg.norm(passed_centroid - nonmineral_centroid)
dist_failed_nonmineral = np.linalg.norm(failed_centroid - nonmineral_centroid)

print("Inter-centroid distances:")
print(f"  Passed ↔ Failed:      {dist_passed_failed:.3f}")
print(f"  Passed ↔ Non-mineral: {dist_passed_nonmineral:.3f}")
print(f"  Failed ↔ Non-mineral: {dist_failed_nonmineral:.3f}")
print()

# Check for clustering
from scipy.spatial.distance import pdist, squareform

if len(passed_coords) > 1:
    passed_pairwise = pdist(passed_coords)
    print(f"Passed cluster tightness:  mean={np.mean(passed_pairwise):.3f}, std={np.std(passed_pairwise):.3f}")

if len(failed_coords) > 1:
    failed_pairwise = pdist(failed_coords)
    print(f"Failed cluster tightness:  mean={np.mean(failed_pairwise):.3f}, std={np.std(failed_pairwise):.3f}")

print()

# ============================================================================
# Step 5: Visualize in 3D
# ============================================================================

print("Step 5: Generating 3D visualization...")
print()

fig = plt.figure(figsize=(16, 12))

# Main 3D scatter plot
ax1 = fig.add_subplot(221, projection='3d')

# Plot passed minerals (green)
if len(passed_coords) > 0:
    ax1.scatter(passed_coords[:, 0], passed_coords[:, 1], passed_coords[:, 2],
                c='green', marker='o', s=100, alpha=0.7, label='Passed Minerals', edgecolors='darkgreen')

# Plot failed minerals (red)
if len(failed_coords) > 0:
    ax1.scatter(failed_coords[:, 0], failed_coords[:, 1], failed_coords[:, 2],
                c='red', marker='o', s=100, alpha=0.7, label='Failed Minerals', edgecolors='darkred')

# Plot non-minerals (black X)
if len(nonmineral_coords) > 0:
    ax1.scatter(nonmineral_coords[:, 0], nonmineral_coords[:, 1], nonmineral_coords[:, 2],
                c='black', marker='x', s=200, linewidths=3, label='Non-Minerals')

# Plot centroids
ax1.scatter(*passed_centroid, c='lime', marker='*', s=500, edgecolors='black', linewidths=2, label='Passed Centroid')
ax1.scatter(*failed_centroid, c='orange', marker='*', s=500, edgecolors='black', linewidths=2, label='Failed Centroid')
ax1.scatter(*nonmineral_centroid, c='gray', marker='*', s=500, edgecolors='black', linewidths=2, label='Non-Mineral Centroid')

# Plot origin
ax1.scatter(0, 0, 0, c='blue', marker='o', s=300, alpha=0.5, label='Origin')

ax1.set_xlabel('PC1 (Information Axis 1)', fontsize=10)
ax1.set_ylabel('PC2 (Information Axis 2)', fontsize=10)
ax1.set_zlabel('PC3 (Information Axis 3)', fontsize=10)
ax1.set_title('Bitfield: 3D Information Space of Minerals', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left', fontsize=8)
ax1.grid(True, alpha=0.3)

# 2D projections
# XY plane
ax2 = fig.add_subplot(222)
if len(passed_coords) > 0:
    ax2.scatter(passed_coords[:, 0], passed_coords[:, 1], c='green', marker='o', s=50, alpha=0.7, edgecolors='darkgreen')
if len(failed_coords) > 0:
    ax2.scatter(failed_coords[:, 0], failed_coords[:, 1], c='red', marker='o', s=50, alpha=0.7, edgecolors='darkred')
if len(nonmineral_coords) > 0:
    ax2.scatter(nonmineral_coords[:, 0], nonmineral_coords[:, 1], c='black', marker='x', s=100, linewidths=2)
ax2.scatter(0, 0, c='blue', marker='o', s=100, alpha=0.5)
ax2.set_xlabel('PC1')
ax2.set_ylabel('PC2')
ax2.set_title('XY Projection (PC1 vs PC2)')
ax2.grid(True, alpha=0.3)

# XZ plane
ax3 = fig.add_subplot(223)
if len(passed_coords) > 0:
    ax3.scatter(passed_coords[:, 0], passed_coords[:, 2], c='green', marker='o', s=50, alpha=0.7, edgecolors='darkgreen')
if len(failed_coords) > 0:
    ax3.scatter(failed_coords[:, 0], failed_coords[:, 2], c='red', marker='o', s=50, alpha=0.7, edgecolors='darkred')
if len(nonmineral_coords) > 0:
    ax3.scatter(nonmineral_coords[:, 0], nonmineral_coords[:, 2], c='black', marker='x', s=100, linewidths=2)
ax3.scatter(0, 0, c='blue', marker='o', s=100, alpha=0.5)
ax3.set_xlabel('PC1')
ax3.set_ylabel('PC3')
ax3.set_title('XZ Projection (PC1 vs PC3)')
ax3.grid(True, alpha=0.3)

# YZ plane
ax4 = fig.add_subplot(224)
if len(passed_coords) > 0:
    ax4.scatter(passed_coords[:, 1], passed_coords[:, 2], c='green', marker='o', s=50, alpha=0.7, edgecolors='darkgreen')
if len(failed_coords) > 0:
    ax4.scatter(failed_coords[:, 1], failed_coords[:, 2], c='red', marker='o', s=50, alpha=0.7, edgecolors='darkred')
if len(nonmineral_coords) > 0:
    ax4.scatter(nonmineral_coords[:, 1], nonmineral_coords[:, 2], c='black', marker='x', s=100, linewidths=2)
ax4.scatter(0, 0, c='blue', marker='o', s=100, alpha=0.5)
ax4.set_xlabel('PC2')
ax4.set_ylabel('PC3')
ax4.set_title('YZ Projection (PC2 vs PC3)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/ubuntu/ubp_mineral_study/results/bitfield_3d_visualization.png', dpi=300, bbox_inches='tight')
print("Saved 3D visualization to bitfield_3d_visualization.png")
print()

# ============================================================================
# Step 6: Save Results
# ============================================================================

# Save coordinates and analysis
bitfield_data = {
    'pca_explained_variance': pca.explained_variance_ratio_.tolist(),
    'pca_components': pca.components_.tolist(),
    'feature_names': feature_names,
    'coordinates': {
        'labels': labels,
        'coords_3d': coords_3d.tolist(),
        'pass_fail': pass_fail,
        'crystal_systems': crystal_systems
    },
    'centroids': {
        'passed': passed_centroid.tolist(),
        'failed': failed_centroid.tolist(),
        'nonmineral': nonmineral_centroid.tolist()
    },
    'distances_from_origin': {
        'passed': {'mean': float(np.mean(passed_dists)), 'std': float(np.std(passed_dists))},
        'failed': {'mean': float(np.mean(failed_dists)), 'std': float(np.std(failed_dists))},
        'nonmineral': {'mean': float(np.mean(nonmineral_dists)), 'std': float(np.std(nonmineral_dists))}
    },
    'inter_centroid_distances': {
        'passed_failed': float(dist_passed_failed),
        'passed_nonmineral': float(dist_passed_nonmineral),
        'failed_nonmineral': float(dist_failed_nonmineral)
    },
    'non_minerals': non_minerals
}

with open('/home/ubuntu/ubp_mineral_study/results/bitfield_spatial_analysis.json', 'w') as f:
    json.dump(bitfield_data, f, indent=2)

print("Saved Bitfield analysis to bitfield_spatial_analysis.json")
print()

print("=" * 80)
print("BITFIELD ANALYSIS COMPLETE")
print("=" * 80)
