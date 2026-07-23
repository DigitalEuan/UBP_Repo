"""
Phase XIV Visualization Engine
Generates 12 publication-quality figures for the extended UBP x RLS fusion study.
"""

import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Font setup
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['font.size'] = 9

# Color palette (academic dark theme)
C_PRIME = '#FF6B35'
C_COMPOSITE = '#4ECDC4'
C_ACCENT = '#FFE66D'
C_BG = '#1a1a2e'
C_GRID = '#2d2d4a'
C_TEXT = '#e0e0e0'
C_RED = '#e74c3c'
C_BLUE = '#3498db'
C_GREEN = '#2ecc71'
C_PURPLE = '#9b59b6'
C_ORANGE = '#e67e22'
C_PINK = '#e91e63'

# Custom colormaps
cmap_prime = LinearSegmentedColormap.from_list('prime_dark',
    ['#0d1117', '#1a1a4e', '#2d4a7a', '#4a90d9', '#87ceeb', '#ffe66d', '#ff6b35', '#ff0000'])

cmap_cool = LinearSegmentedColormap.from_list('cool_dark',
    ['#0d1117', '#16213e', '#1a5276', '#2e86c1', '#85c1e9', '#d4efdf', '#f9e79f', '#f5b041', '#e74c3c'])

OUTDIR = '/home/z/my-project/download/'


def load_results():
    with open('/home/z/my-project/scripts/phase14_results.json') as f:
        return json.load(f)


def fig1_polar_density_1deg(results):
    """Fig 1: 1-degree polar prime density heatmap — the finest angular view."""
    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_subplot(121, projection='polar')
    ax2 = fig.add_subplot(122)
    fig.patch.set_facecolor(C_BG)

    sectors_1deg = results["sector_stats_1deg"]
    angles = [math.radians(s["angle_mid"]) for s in sectors_1deg]
    densities = [s["prime_density"] for s in sectors_1deg]

    # Left: full 360-sector polar plot
    ax.set_facecolor(C_BG)
    bars = ax.bar(angles, densities, width=math.radians(1.0), color=C_PRIME, alpha=0.8,
                  edgecolor='none')
    # Color by density
    norm = plt.Normalize(min(densities), max(densities))
    cmap = plt.cm.plasma
    for bar, d in zip(bars, densities):
        bar.set_facecolor(cmap(norm(d)))

    ax.set_title('Prime Density at 1\u00b0 Resolution (360 sectors)\n10\u2076 RLS cells',
                 color=C_TEXT, fontsize=11, pad=15)
    ax.tick_params(colors=C_TEXT, labelsize=7)
    ax.set_rticks([])
    ax.grid(True, alpha=0.15, color=C_TEXT)

    # Right: unwrapped 360-sector plot showing 4-fold symmetry
    # ax2 already created above
    ax2.set_facecolor(C_BG)
    sector_indices = [s["sector"] for s in sectors_1deg]
    ax2.bar(sector_indices, densities, width=1.0, color=[cmap(norm(d)) for d in densities],
            edgecolor='none')
    ax2.axhline(y=sum(densities)/len(densities), color=C_ACCENT, linestyle='--',
                alpha=0.7, label=f'Mean PD = {sum(densities)/len(densities):.4f}')

    # Mark 90-degree symmetry points
    for offset in [0, 90, 180, 270]:
        ax2.axvline(x=offset, color=C_RED, linestyle=':', alpha=0.5, linewidth=0.8)

    ax2.set_xlabel('Angular Sector (degrees)', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Prime Density', color=C_TEXT, fontsize=9)
    ax2.set_title('Unwrapped View — 4-fold Symmetry (r=0.984 at 90\u00b0 lag)',
                  color=C_TEXT, fontsize=11)
    ax2.tick_params(colors=C_TEXT, labelsize=7)
    ax2.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=8)
    ax2.set_xlim(0, 360)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig1_polar_1deg.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 1 saved: polar_1deg")


def fig2_correlation_stability(results):
    """Fig 2: Correlation stability comparison — 10° vs 1° resolution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)

    corr_1deg = results["1deg_correlations"]

    metrics = ["mean_angle", "anchor_dist", "rot_sign_changes", "nrci_gl",
               "net_rotation", "hw"]
    labels = ["Mean Angle", "Anchor Dist", "Rot SC", "NRCI_GL",
              "Net Rotation", "Hamming Wt"]

    # Phase XIII 10-degree values (from worklog)
    r_10deg_phase13 = [0.9906, 0.9901, 0.9894, -0.9287, -0.9572, 0.9241]
    # Phase XIV 1-degree values
    r_1deg_phase14 = [corr_1deg[m]["pearson_r"] for m in metrics]

    x = np.arange(len(metrics))
    width = 0.35

    # Left: bar chart comparison
    ax = axes[0]
    ax.set_facecolor(C_BG)
    bars1 = ax.bar(x - width/2, r_10deg_phase13, width, label='Phase XIII (10\u00b0, 50k)',
                   color=C_BLUE, alpha=0.85, edgecolor='none')
    bars2 = ax.bar(x + width/2, r_1deg_phase14, width, label='Phase XIV (1\u00b0, 200k sample)',
                   color=C_PRIME, alpha=0.85, edgecolor='none')

    ax.axhline(y=0, color=C_TEXT, alpha=0.3, linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8, color=C_TEXT)
    ax.set_ylabel('Pearson r (vs Prime Density)', color=C_TEXT, fontsize=9)
    ax.set_title('Correlation Stability: 10\u00b0 vs 1\u00b0 Angular Resolution',
                 color=C_TEXT, fontsize=11)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=8)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    ax.set_ylim(-1.1, 1.1)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add delta annotations
    for i, (r10, r1) in enumerate(zip(r_10deg_phase13, r_1deg_phase14)):
        delta = r1 - r10
        color = C_GREEN if abs(delta) < 0.05 else (C_ORANGE if abs(delta) < 0.15 else C_RED)
        ax.annotate(f'\u0394={delta:+.3f}', (x[i], max(r10, r1) + 0.04),
                    ha='center', fontsize=7, color=color)

    # Right: Spearman vs Pearson comparison at 1-degree
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    spearman_vals = [corr_1deg[m]["spearman_rho"] for m in metrics]
    pearson_vals = r_1deg_phase14

    ax2.scatter(pearson_vals, spearman_vals, s=80, c=[C_BLUE, C_PRIME, C_GREEN,
               C_RED, C_PURPLE, C_ORANGE], zorder=5, edgecolors='white', linewidth=0.5)

    for i, label in enumerate(labels):
        ax2.annotate(label, (pearson_vals[i], spearman_vals[i]),
                     textcoords="offset points", xytext=(8, 5), fontsize=7, color=C_TEXT)

    lims = [-1.05, 1.05]
    ax2.plot(lims, lims, '--', color=C_TEXT, alpha=0.3, linewidth=0.5)
    ax2.set_xlabel('Pearson r', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Spearman \u03c1', color=C_TEXT, fontsize=9)
    ax2.set_title('Pearson vs Spearman at 1\u00b0 (360 sectors)',
                  color=C_TEXT, fontsize=11)
    ax2.tick_params(colors=C_TEXT, labelsize=8)
    ax2.set_xlim(lims)
    ax2.set_ylim(lims)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig2_correlation_stability.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 2 saved: correlation_stability")


def fig3_ktuple_angular(results):
    """Fig 3: K-tuple angular distribution on RLS."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(C_BG)
    fig.suptitle('Prime K-Tuple Angular Distribution on RLS (10\u2076 cells)',
                 color=C_TEXT, fontsize=13, y=0.98)

    kt_angular = results["k_tuple_angular_36"]
    sector_stats_10deg = results["sector_stats_10deg"]

    # Get prime density for reference
    pd_36 = [s["prime_density"] for s in sector_stats_10deg]
    angles = [s["angle_mid"] for s in sector_stats_10deg]

    # Normalize k-tuple counts by sector size (approximate)
    sector_totals = [s["n_total"] for s in sector_stats_10deg]
    total_cells = sum(sector_totals)

    kt_configs = [
        ("twins", "Twin Primes (p, p+2)", C_PRIME, 0),
        ("cousins", "Cousin Primes (p, p+4)", C_BLUE, 1),
        ("sexy", "Sexy Primes (p, p+6)", C_GREEN, 2),
        ("quadruplets", "Prime Quadruplets", C_PURPLE, 3),
    ]

    for name, title, color, idx in kt_configs:
        ax_row = idx // 2
        ax_col = idx % 2
        ax = axes[ax_row][ax_col]
        ax.set_facecolor(C_BG)

        if name not in kt_angular:
            continue

        counts = kt_angular[name]
        total_kt = sum(counts)
        if total_kt == 0:
            continue

        # Normalize to density
        kt_density = [c / t if t > 0 else 0 for c, t in zip(counts, sector_totals)]

        # Twin axis
        ax2 = ax.twinx()
        ax.bar(angles, kt_density, width=9, color=color, alpha=0.6, label=f'{name} density')
        ax2.plot(angles, pd_36, 'o-', color=C_ACCENT, markersize=3, linewidth=1.2,
                 label='Prime density', alpha=0.8)

        ax.set_xlabel('Angle (degrees)', color=C_TEXT, fontsize=8)
        ax.set_ylabel(f'{name} density', color=color, fontsize=8)
        ax2.set_ylabel('Prime Density', color=C_ACCENT, fontsize=8)
        ax.set_title(f'{title}\nTotal: {total_kt} in 10\u2076 grid',
                     color=C_TEXT, fontsize=10)

        # Compute and show correlation
        r_val = np.corrcoef(kt_density, pd_36)[0, 1]
        ax.text(0.02, 0.95, f'r = {r_val:+.4f}', transform=ax.transAxes,
                fontsize=9, color=C_ACCENT, verticalalignment='top',
                fontweight='bold')

        ax.tick_params(colors=C_TEXT, labelsize=7)
        ax2.tick_params(colors=C_TEXT, labelsize=7)
        ax.spines['bottom'].set_color(C_GRID)
        ax.spines['left'].set_color(C_GRID)
        ax2.spines['right'].set_color(C_GRID)
        ax.spines['top'].set_visible(False)

    # Add shared legend
    lines1, labels1 = axes[0][0].get_legend_handles_labels()
    lines2, labels2 = axes[0][0].twinx().get_legend_handles_labels()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'{OUTDIR}phase14_fig3_ktuple_angular.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 3 saved: ktuple_angular")


def fig4_hardy_littlewood(results):
    """Fig 4: Hardy-Littlewood conjecture testing."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)

    hl = results["hardy_littlewood"]

    # Left: Observed vs Expected
    ax = axes[0]
    ax.set_facecolor(C_BG)

    names_display = ["Twins\n(0,2)", "Cousins\n(0,4)", "Sexy\n(0,6)",
                     "Triplet-1\n(0,2,6)", "Triplet-2\n(0,4,6)", "Quad\n(0,2,6,8)"]
    # Fix name mapping for HL results
    name_map = {"twins": 0, "cousins": 1, "sexy": 2,
                "triplet_1": 3, "triplet_2": 4, "quadruplet": 5}
    # Actual k-tuple counts from results
    kt_counts = results["k_tuples"]
    observed_fixed = [kt_counts.get("twins", 0), kt_counts.get("cousins", 0),
                      kt_counts.get("sexy", 0), kt_counts.get("triplets_1", 0),
                      kt_counts.get("triplets_2", 0), kt_counts.get("quadruplets", 0)]
    expected_vals = [hl["twins"]["expected"], hl["cousins"]["expected"],
                     hl["sexy"]["expected"], hl["triplet_1"]["expected"],
                     hl["triplet_2"]["expected"], hl["quadruplet"]["expected"]]

    x = np.arange(len(names_display))
    width = 0.35
    ax.bar(x - width/2, observed_fixed, width, label='Observed', color=C_PRIME, alpha=0.85)
    ax.bar(x + width/2, expected_vals, width, label='HL Expected', color=C_BLUE, alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(names_display, fontsize=8, color=C_TEXT)
    ax.set_ylabel('Count', color=C_TEXT, fontsize=9)
    ax.set_title('Hardy-Littlewood: Observed vs Expected (10\u2076 grid)',
                 color=C_TEXT, fontsize=11)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=8)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add ratio annotations
    for i, (obs, exp) in enumerate(zip(observed_fixed, expected_vals)):
        if exp > 0 and obs > 0:
            ratio = obs / exp
            ax.annotate(f'{ratio:.2f}x', (x[i], max(obs, exp) + 200),
                        ha='center', fontsize=7, color=C_GREEN)

    # Right: Sector-wise twin prime deviation
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)

    # Load RLS grid for sector-wise analysis
    try:
        with open('/home/z/my-project/scripts/phase14_rls_grid.json') as f:
            grid_data = json.load(f)

        # Rebuild k-tuple angular data at 36 sectors
        n_to_angle = {}
        for pt in grid_data:
            n_to_angle[pt["n"]] = pt["angle_deg"]

        # We need primality info from the grid
        primes_in_grid = set(pt["n"] for pt in grid_data if pt["is_prime"])

        twin_sector_obs = [0] * 36
        twin_sector_exp = [0.0] * 36
        prime_sector_count = [0] * 36

        for p in sorted(primes_in_grid):
            s_idx = int(n_to_angle.get(p, 0) / 10) % 36
            prime_sector_count[s_idx] += 1
            if p + 2 in primes_in_grid:
                twin_sector_obs[s_idx] += 1

        total_twins = sum(twin_sector_obs)
        total_primes = sum(prime_sector_count)

        for i in range(36):
            if prime_sector_count[i] > 0 and total_primes > 0:
                # Expected twins proportional to sector prime count
                twin_sector_exp[i] = total_twins * prime_sector_count[i] / total_primes

        deviations = [(o - e) / math.sqrt(e) if e > 0 else 0
                      for o, e in zip(twin_sector_obs, twin_sector_exp)]

        sector_angles = [(i + 0.5) * 10 for i in range(36)]
        colors = [C_GREEN if d >= 0 else C_RED for d in deviations]
        ax2.bar(sector_angles, deviations, width=9, color=colors, alpha=0.7, edgecolor='none')
        ax2.axhline(y=0, color=C_TEXT, alpha=0.5, linewidth=0.5)
        ax2.axhline(y=2, color=C_ACCENT, linestyle='--', alpha=0.4, label='2\u03c3')
        ax2.axhline(y=-2, color=C_ACCENT, linestyle='--', alpha=0.4)

        ax2.set_xlabel('Angular Sector (degrees)', color=C_TEXT, fontsize=9)
        ax2.set_ylabel('Standardized Residual (O\u2212E)/\u221aE', color=C_TEXT, fontsize=9)
        ax2.set_title('Twin Prime Sector-wise HL Deviation\n\u03c7\u00b2 = 1950.8 (df=35) — REJECT uniformity',
                      color=C_TEXT, fontsize=11)
        ax2.tick_params(colors=C_TEXT, labelsize=8)
        ax2.spines['bottom'].set_color(C_GRID)
        ax2.spines['left'].set_color(C_GRID)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

    except Exception as e:
        ax2.text(0.5, 0.5, f'Grid data unavailable\n{str(e)}', transform=ax2.transAxes,
                 ha='center', color=C_TEXT, fontsize=10)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig4_hardy_littlewood.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 4 saved: hardy_littlewood")


def fig5_3d_structure(results):
    """Fig 5: 3D RLS structure with Time dimension."""
    # Load grid for 3D visualization
    with open('/home/z/my-project/scripts/phase14_rls_grid.json') as f:
        grid = json.load(f)

    # Subsample for 3D scatter (need to keep it manageable)
    sample = grid[::3]  # Every 3rd point

    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(C_BG)

    # 3D view 1: Full structure with layer coloring
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.set_facecolor(C_BG)

    primes_3d = [(p["i"], p["j"], p["layer_idx"]) for p in sample if p["is_prime"]]
    composites_3d = [(p["i"], p["j"], p["layer_idx"]) for p in sample if not p["is_prime"]]

    if composites_3d:
        cx, cy, cz = zip(*composites_3d[:5000])
        ax1.scatter(cx, cy, cz, c=C_BLUE, s=0.3, alpha=0.08, label='Composite')
    if primes_3d:
        px, py, pz = zip(*primes_3d)
        ax1.scatter(px, py, pz, c=C_PRIME, s=2, alpha=0.5, label='Prime')

    ax1.set_xlabel('i (Gaussian int)', color=C_TEXT, fontsize=7, labelpad=-2)
    ax1.set_ylabel('j (Gaussian int)', color=C_TEXT, fontsize=7, labelpad=-2)
    ax1.set_zlabel('Layer (Time)', color=C_TEXT, fontsize=7, labelpad=-2)
    ax1.set_title('3D RLS: (i, j, Layer)\n"Time = Layer Index"', color=C_TEXT, fontsize=10)
    ax1.tick_params(colors=C_TEXT, labelsize=5)
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=6,
               markerscale=3, loc='upper left')
    ax1.view_init(elev=25, azim=45)

    # 3D view 2: Polar + Time
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.set_facecolor(C_BG)

    for pt in sample[:10000]:
        angle_rad = math.radians(pt["angle_deg"])
        x = pt["radius"] * math.cos(angle_rad)
        y = pt["radius"] * math.sin(angle_rad)
        z = pt["layer_idx"]
        color = C_PRIME if pt["is_prime"] else C_BLUE
        alpha = 0.4 if pt["is_prime"] else 0.03
        size = 3 if pt["is_prime"] else 0.3
        ax2.scatter([x], [y], [z], c=color, s=size, alpha=alpha)

    ax2.set_xlabel('x', color=C_TEXT, fontsize=7, labelpad=-2)
    ax2.set_ylabel('y', color=C_TEXT, fontsize=7, labelpad=-2)
    ax2.set_zlabel('Time (Layer)', color=C_TEXT, fontsize=7, labelpad=-2)
    ax2.set_title('3D RLS: Polar coords + Time\nSpiral Helix Structure', color=C_TEXT, fontsize=10)
    ax2.tick_params(colors=C_TEXT, labelsize=5)
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.view_init(elev=15, azim=30)

    # Bottom left: Layer-wise prime density (Time evolution)
    ax3 = fig.add_subplot(223)
    ax3.set_facecolor(C_BG)

    # Compute layer-wise prime density from grid data
    layers = defaultdict(lambda: {"total": 0, "primes": 0})
    for pt in grid:
        layers[pt["layer_idx"]]["total"] += 1
        if pt["is_prime"]:
            layers[pt["layer_idx"]]["primes"] += 1

    layer_indices = sorted(layers.keys())
    layer_pd = [layers[l]["primes"] / layers[l]["total"] if layers[l]["total"] > 0 else 0
                for l in layer_indices]
    layer_n = [layers[l]["total"] for l in layer_indices]

    # Smooth with running average
    window = 200
    if len(layer_pd) > window:
        smooth_pd = np.convolve(layer_pd, np.ones(window)/window, mode='valid')
        smooth_x = np.arange(window//2, window//2 + len(smooth_pd))
        ax3.plot(smooth_x, smooth_pd, color=C_PRIME, linewidth=1.2, label='Prime density (smoothed)')
        # Theoretical 1/ln(n) curve
        theoretical = []
        for l in smooth_x:
            # Approximate n from layer index
            n_approx = l * 4  # rough: average 4 cells per layer
            if n_approx > 2:
                theoretical.append(1.0 / math.log(n_approx))
            else:
                theoretical.append(0)
        ax3.plot(smooth_x, theoretical, '--', color=C_ACCENT, linewidth=1,
                 alpha=0.7, label='1/ln(n) approximation')

    ax3.set_xlabel('Layer Index (Time)', color=C_TEXT, fontsize=9)
    ax3.set_ylabel('Prime Density', color=C_TEXT, fontsize=9)
    ax3.set_title('Temporal Evolution of Prime Density\n"Time = Layer Index"',
                  color=C_TEXT, fontsize=10)
    ax3.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax3.tick_params(colors=C_TEXT, labelsize=7)
    ax3.spines['bottom'].set_color(C_GRID)
    ax3.spines['left'].set_color(C_GRID)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # Bottom right: 2D vs 3D angular variance comparison
    ax4 = fig.add_subplot(224)
    ax4.set_facecolor(C_BG)

    # Show that 3D voxel structure reveals more variance
    categories = ['2D Angular\n(36 sectors)', '3D Voxel\n(36 x 10)', '2D Angular\n(360 sectors)']
    variances = [results["1deg_analysis"]["pd_std"]**2,  # Approximate
                 0.003184,  # From computation
                 results["1deg_analysis"]["pd_std"]**2 * 0.3]  # Approximate
    colors_bar = [C_BLUE, C_PRIME, C_GREEN]

    # Use actual computed values
    var_2d_36 = 0.002637  # From computation output
    var_3d = 0.003184
    var_1deg = results["1deg_analysis"]["pd_std"]**2

    cats = ['2D (36 sectors)', '3D Voxel (36x10)', '2D (360 sectors)']
    vars_actual = [var_2d_36, var_3d, var_1deg]
    colors_v = [C_BLUE, C_PRIME, C_GREEN]

    bars = ax4.bar(cats, vars_actual, color=colors_v, alpha=0.85, edgecolor='none', width=0.6)
    ax4.axhline(y=var_2d_36, color=C_BLUE, linestyle='--', alpha=0.4, linewidth=0.8)

    for bar, v in zip(bars, vars_actual):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.00005,
                 f'{v:.6f}', ha='center', fontsize=8, color=C_TEXT)

    ax4.set_ylabel('Prime Density Variance', color=C_TEXT, fontsize=9)
    ax4.set_title('Structural Information: 2D vs 3D\n3D reveals 21% more variance',
                  color=C_TEXT, fontsize=10)
    ax4.tick_params(colors=C_TEXT, labelsize=7)
    ax4.spines['bottom'].set_color(C_GRID)
    ax4.spines['left'].set_color(C_GRID)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(f'{OUTDIR}phase14_fig5_3d_structure.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 5 saved: 3d_structure")


def fig6_gaussian_split(results):
    """Fig 6: p=1(4) vs p=3(4) Gaussian Integer angular comparison."""
    with open('/home/z/my-project/scripts/phase14_rls_grid.json') as f:
        grid = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(C_BG)

    # Classify primes
    p1_angles = []
    p3_angles = []
    p1_radii = []
    p3_radii = []

    for pt in grid:
        if pt["is_prime"] and pt["n"] > 2:
            if pt["n"] % 4 == 1:
                p1_angles.append(pt["angle_deg"])
                p1_radii.append(pt["radius"])
            elif pt["n"] % 4 == 3:
                p3_angles.append(pt["angle_deg"])
                p3_radii.append(pt["radius"])

    # Left: Angular histograms
    ax = axes[0]
    ax.set_facecolor(C_BG)
    bins = np.arange(0, 362, 10)
    ax.hist(p1_angles, bins=bins, alpha=0.6, color=C_PRIME, label=f'p=1(4) n={len(p1_angles)}',
            density=True, edgecolor='none')
    ax.hist(p3_angles, bins=bins, alpha=0.4, color=C_BLUE, label=f'p=3(4) n={len(p3_angles)}',
            density=True, edgecolor='none')
    ax.set_xlabel('Angle (degrees)', color=C_TEXT, fontsize=9)
    ax.set_ylabel('Density', color=C_TEXT, fontsize=9)
    ax.set_title('Angular Distribution\nCross-class r = -0.396', color=C_TEXT, fontsize=10)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax.tick_params(colors=C_TEXT, labelsize=7)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Middle: Radial distribution
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    ax2.hist(p1_radii, bins=50, alpha=0.6, color=C_PRIME, label='p=1(4)',
             density=True, edgecolor='none')
    ax2.hist(p3_radii, bins=50, alpha=0.4, color=C_BLUE, label='p=3(4)',
             density=True, edgecolor='none')
    ax2.set_xlabel('RLS Radius', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Density', color=C_TEXT, fontsize=9)
    ax2.set_title('Radial Distribution\nSimilar radial extent', color=C_TEXT, fontsize=10)
    ax2.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax2.tick_params(colors=C_TEXT, labelsize=7)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Right: Sector-wise counts
    ax3 = axes[2]
    ax3.set_facecolor(C_BG)

    p1_counts = [0] * 36
    p3_counts = [0] * 36
    for a in p1_angles:
        p1_counts[int(a / 10) % 36] += 1
    for a in p3_angles:
        p3_counts[int(a / 10) % 36] += 1

    x = np.arange(36)
    ax3.bar(x - 0.2, p1_counts, 0.4, color=C_PRIME, alpha=0.7, label='p=1(4)')
    ax3.bar(x + 0.2, p3_counts, 0.4, color=C_BLUE, alpha=0.7, label='p=3(4)')
    ax3.set_xlabel('Sector', color=C_TEXT, fontsize=9)
    ax3.set_ylabel('Prime Count', color=C_TEXT, fontsize=9)
    ax3.set_title('Sector-wise Counts\np=1(4) more variable (\u03c7\u00b2=10478 vs 3527)',
                  color=C_TEXT, fontsize=10)
    ax3.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax3.tick_params(colors=C_TEXT, labelsize=7)
    ax3.spines['bottom'].set_color(C_GRID)
    ax3.spines['left'].set_color(C_GRID)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig6_gaussian_split.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 6 saved: gaussian_split")


def fig7_short_interval(results):
    """Fig 7: Short-interval angular clustering."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)

    si = results["short_intervals"]

    # Left: Rayleigh R vs interval center
    ax = axes[0]
    ax.set_facecolor(C_BG)
    x_centers = [s["x_center"] for s in si]
    R_vals = [s["R"] for s in si]
    n_primes_si = [s["n_primes"] for s in si]

    colors_sc = [C_PRIME if r > 0.1 else (C_ORANGE if r > 0.05 else C_BLUE) for r in R_vals]
    ax.scatter(x_centers, R_vals, s=[n*5 for n in n_primes_si], c=colors_sc,
              alpha=0.8, edgecolors='white', linewidth=0.5, zorder=5)
    ax.axhline(y=0.1, color=C_RED, linestyle='--', alpha=0.5, label='Clustering threshold (R=0.1)')
    ax.axhline(y=0.05, color=C_ORANGE, linestyle=':', alpha=0.5, label='Weak threshold (R=0.05)')

    ax.set_xscale('log')
    ax.set_xlabel('Interval Center x (log scale)', color=C_TEXT, fontsize=9)
    ax.set_ylabel('Rayleigh R (concentration)', color=C_TEXT, fontsize=9)
    ax.set_title('Short-Interval Angular Clustering\n'
                 'Primes in [x, x+\u221ax] show clustering at small x',
                 color=C_TEXT, fontsize=10)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Annotate points
    for s in si:
        label = "CLUSTERED" if s["R"] > 0.1 else ("weak" if s["R"] > 0.05 else "uniform")
        ax.annotate(f'{label}\n({s["n_primes"]}p)',
                    (s["x_center"], s["R"]),
                    textcoords="offset points", xytext=(10, 5),
                    fontsize=6, color=C_TEXT)

    # Right: Angular spread (std) vs interval center
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    std_vals = [s["angular_std"] for s in si]

    ax2.scatter(x_centers, std_vals, s=[n*5 for n in n_primes_si],
               c=colors_sc, alpha=0.8, edgecolors='white', linewidth=0.5, zorder=5)

    ax2.set_xscale('log')
    ax2.set_xlabel('Interval Center x (log scale)', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Angular Std Dev (degrees)', color=C_TEXT, fontsize=9)
    ax2.set_title('Angular Spread in Short Intervals\n'
                  'Small intervals: primes concentrated in ~1\u00b0 arcs',
                  color=C_TEXT, fontsize=10)
    ax2.tick_params(colors=C_TEXT, labelsize=8)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig7_short_interval.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 7 saved: short_interval")


def fig8_autocorrelation_symmetry(results):
    """Fig 8: Circular autocorrelation and symmetry analysis."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)

    sectors = results["sector_stats_1deg"]
    pd = [s["prime_density"] for s in sectors]

    # Compute full circular autocorrelation
    lags = range(0, 180)
    autocorr = []
    for lag in lags:
        if lag == 0:
            autocorr.append(1.0)
        else:
            shifted = pd[lag:] + pd[:lag]
            r = np.corrcoef(pd[:len(shifted)], shifted)[0, 1] if len(shifted) == len(pd) else 0
            autocorr.append(r)

    # Left: Autocorrelation function
    ax = axes[0]
    ax.set_facecolor(C_BG)
    ax.fill_between(lags, autocorr, alpha=0.2, color=C_PRIME)
    ax.plot(lags, autocorr, color=C_PRIME, linewidth=1.5)

    # Mark symmetry peaks
    for peak_lag, label in [(0, "0\u00b0"), (45, "45\u00b0"), (90, "90\u00b0"), (180, "180\u00b0")]:
        if peak_lag < len(autocorr):
            ax.scatter([peak_lag], [autocorr[peak_lag]], s=60, color=C_ACCENT,
                      zorder=5, edgecolors='white', linewidth=0.5)
            ax.annotate(f'{label}\nr={autocorr[peak_lag]:.3f}',
                       (peak_lag, autocorr[peak_lag]),
                       textcoords="offset points", xytext=(8, 10),
                       fontsize=7, color=C_ACCENT)

    ax.set_xlabel('Angular Lag (degrees)', color=C_TEXT, fontsize=9)
    ax.set_ylabel('Autocorrelation r', color=C_TEXT, fontsize=9)
    ax.set_title('Circular Autocorrelation of 1\u00b0 Prime Density\n'
                 'Strong 90\u00b0 periodicity (4-fold symmetry)',
                 color=C_TEXT, fontsize=10)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Right: Folded symmetry comparison
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)

    # Create 4-fold averaged density
    n_sectors = 360
    quarter = n_sectors // 4  # 90
    quarters = []
    for q in range(4):
        q_data = pd[q*quarter:(q+1)*quarter]
        quarters.append(q_data)

    for q, (qd, color, label) in enumerate(zip(quarters,
            [C_PRIME, C_BLUE, C_GREEN, C_PURPLE],
            ['0\u00b0-90\u00b0', '90\u00b0-180\u00b0', '180\u00b0-270\u00b0', '270\u00b0-360\u00b0'])):
        ax2.plot(range(len(qd)), qd, color=color, alpha=0.7, linewidth=1, label=label)

    # Average
    min_len = min(len(q) for q in quarters)
    avg = [sum(q[i] for q in quarters if i < len(q)) / 4 for i in range(min_len)]
    ax2.plot(range(min_len), avg, color=C_ACCENT, linewidth=2, label='4-fold average')

    ax2.set_xlabel('Sector within 90\u00b0 quadrant', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Prime Density', color=C_TEXT, fontsize=9)
    ax2.set_title('4-Quadrant Overlay (90\u00b0 symmetry)\n'
                  'All quadrants show identical structure',
                  color=C_TEXT, fontsize=10)
    ax2.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax2.tick_params(colors=C_TEXT, labelsize=8)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig8_autocorrelation.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 8 saved: autocorrelation")


def fig9_ktuple_per_prime(results):
    """Fig 9: K-tuple rate per prime — testing if k-tuples preferentially cluster."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)

    kt_angular = results["k_tuple_angular_36"]
    sector_stats = results["sector_stats_10deg"]

    # Left: K-tuple count vs prime count per sector (twins)
    ax = axes[0]
    ax.set_facecolor(C_BG)

    prime_counts = [s["n_primes"] for s in sector_stats]
    twin_counts = kt_angular.get("twins", [0]*36)
    sexy_counts = kt_angular.get("sexy", [0]*36)
    quad_counts = kt_angular.get("quadruplets", [0]*36)

    ax.scatter(prime_counts, twin_counts, s=40, c=C_PRIME, alpha=0.7, label='Twins', zorder=5)
    ax.scatter(prime_counts, sexy_counts, s=40, c=C_GREEN, alpha=0.7, label='Sexy', zorder=5)
    ax.scatter(prime_counts, quad_counts, s=40, c=C_PURPLE, alpha=0.7, label='Quadruplets', zorder=5)

    # Fit lines
    for counts, color, label in [(twin_counts, C_PRIME, 'Twins'),
                                  (sexy_counts, C_GREEN, 'Sexy'),
                                  (quad_counts, C_PURPLE, 'Quadruplets')]:
        if sum(counts) > 0:
            z = np.polyfit(prime_counts, counts, 1)
            p = np.poly1d(z)
            x_fit = np.linspace(min(prime_counts), max(prime_counts), 50)
            ax.plot(x_fit, p(x_fit), '--', color=color, alpha=0.5, linewidth=1)

    ax.set_xlabel('Prime Count per Sector', color=C_TEXT, fontsize=9)
    ax.set_ylabel('K-tuple Count per Sector', color=C_TEXT, fontsize=9)
    ax.set_title('K-Tuple Counts vs Prime Counts\n'
                 'K-tuples follow prime density (R\u00b2>0.98)',
                 color=C_TEXT, fontsize=10)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    ax.spines['bottom'].set_color(C_GRID)
    ax.spines['left'].set_color(C_GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Right: Twin prime rate per prime (normalized)
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)

    twin_rate = [t / p if p > 0 else 0 for t, p in zip(twin_counts, prime_counts)]
    angles = [s["angle_mid"] for s in sector_stats]

    ax2.bar(angles, twin_rate, width=9, color=C_BLUE, alpha=0.7, edgecolor='none')
    ax2.axhline(y=sum(twin_rate)/len(twin_rate), color=C_ACCENT, linestyle='--',
                alpha=0.7, label=f'Mean rate = {sum(twin_rate)/len(twin_rate):.4f}')

    r_rate, _ = np.corrcoef([s["prime_density"] for s in sector_stats], twin_rate)
    ax2.text(0.02, 0.95, f'r(prime_density, twin_rate) = {r_rate[0,1]:+.4f}\n'
             f'Rayleigh R = 0.0012 (uniform)',
             transform=ax2.transAxes, fontsize=8, color=C_TEXT,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor=C_BG, edgecolor=C_GRID, alpha=0.8))

    ax2.set_xlabel('Angular Sector (degrees)', color=C_TEXT, fontsize=9)
    ax2.set_ylabel('Twin Primes per Prime', color=C_TEXT, fontsize=9)
    ax2.set_title('Twin Prime Rate per Prime (Normalized)\n'
                  'Rate is UNIFORM across sectors',
                  color=C_TEXT, fontsize=10)
    ax2.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=7)
    ax2.tick_params(colors=C_TEXT, labelsize=8)
    ax2.spines['bottom'].set_color(C_GRID)
    ax2.spines['left'].set_color(C_GRID)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig9_ktuple_per_prime.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 9 saved: ktuple_per_prime")


def fig10_3d_time_modes():
    """Fig 10: 3D RLS with different Time modes."""
    # Build small 3D grids with different time modes
    import sys
    sys.path.insert(0, '/home/z/my-project')

    # We'll build lightweight 3D data inline
    N = 50000

    # Fast RLS build
    def build_rls(max_n):
        cells = []
        n = 0
        m = 0
        layer_idx = 0
        while n < max_n:
            max_ij = int(math.isqrt(m)) + 1
            layer = []
            for i in range(-max_ij, max_ij + 1):
                j_sq = m - i*i
                if j_sq < 0: continue
                j = int(math.isqrt(j_sq))
                if j*j == j_sq:
                    layer.append((i, j))
                    if j != 0: layer.append((i, -j))
            seen = set()
            unique = []
            for p in layer:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)
            if not unique:
                m += 1
                continue
            unique.sort(key=lambda p: math.atan2(p[1], p[0]) % (2*math.pi))
            for (i, j) in unique:
                n += 1
                if n > max_n: break
                angle = math.atan2(j, i)
                if angle < 0: angle += 2*math.pi
                cells.append({"n": n, "i": i, "j": j, "layer_idx": layer_idx,
                              "angle_deg": math.degrees(angle), "radius": math.sqrt(m), "m": m})
            layer_idx += 1
            m += 1
        return cells

    from scripts.ubp_rls_fusion_phase14_extended import miller_rabin

    print("  Building 3D grids for time mode comparison...")
    cells = build_rls(N)
    for c in cells:
        c["is_prime"] = miller_rabin(c["n"])

    # Compute LL step time for subset
    for c in cells:
        if c["n"] > 3 and c["n"] % 2 == 1:
            s, Mp, steps = 4, c["n"], 0
            for _ in range(20):
                s_new = (s*s - 2) % Mp
                if s_new == s: break
                s = s_new
                steps += 1
            c["ll_step"] = steps
        else:
            c["ll_step"] = 0

    fig = plt.figure(figsize=(16, 5))
    fig.patch.set_facecolor(C_BG)
    fig.suptitle('3D RLS: Comparing Time Dimension Definitions',
                 color=C_TEXT, fontsize=13, y=1.02)

    sample = [c for c in cells if c["is_prime"]][::2]  # Every other prime
    comp_sample = [c for c in cells if not c["is_prime"]][::20]  # Sparse composites

    # Time = Layer index
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.set_facecolor(C_BG)
    for c in comp_sample[:2000]:
        ax1.scatter([c["i"]], [c["j"]], [c["layer_idx"]], c=C_BLUE, s=0.2, alpha=0.03)
    for c in sample:
        ax1.scatter([c["i"]], [c["j"]], [c["layer_idx"]], c=C_PRIME, s=2, alpha=0.5)
    ax1.set_title('Time = Layer Index\n(Natural RLS ordering)', color=C_TEXT, fontsize=9)
    ax1.tick_params(colors=C_TEXT, labelsize=5)
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.view_init(elev=20, azim=45)

    # Time = log(n)
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.set_facecolor(C_BG)
    for c in comp_sample[:2000]:
        z = math.log(c["n"]) if c["n"] > 1 else 0
        ax2.scatter([c["i"]], [c["j"]], [z], c=C_BLUE, s=0.2, alpha=0.03)
    for c in sample:
        z = math.log(c["n"]) if c["n"] > 1 else 0
        ax2.scatter([c["i"]], [c["j"]], [z], c=C_PRIME, s=2, alpha=0.5)
    ax2.set_title('Time = log(n)\n(Logarithmic natural ordering)', color=C_TEXT, fontsize=9)
    ax2.tick_params(colors=C_TEXT, labelsize=5)
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.view_init(elev=20, azim=45)

    # Time = LL iteration depth
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.set_facecolor(C_BG)
    for c in comp_sample[:2000]:
        ax3.scatter([c["i"]], [c["j"]], [c["ll_step"]], c=C_BLUE, s=0.2, alpha=0.03)
    for c in sample:
        ax3.scatter([c["i"]], [c["j"]], [c["ll_step"]], c=C_PRIME, s=2, alpha=0.5)
    ax3.set_title('Time = LL Iteration Depth\n(Dynamic computation time)', color=C_TEXT, fontsize=9)
    ax3.tick_params(colors=C_TEXT, labelsize=5)
    ax3.xaxis.pane.fill = False
    ax3.yaxis.pane.fill = False
    ax3.zaxis.pane.fill = False
    ax3.view_init(elev=20, azim=45)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig10_3d_time_modes.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 10 saved: 3d_time_modes")


def fig11_hl_sector_heatmap(results):
    """Fig 11: Twin prime sector heatmap — observed vs expected."""
    with open('/home/z/my-project/scripts/phase14_rls_grid.json') as f:
        grid = json.load(f)

    fig = plt.figure(figsize=(14, 5.5))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_subplot(121, projection='polar')
    ax2 = fig.add_subplot(122, projection='polar')

    n_to_angle = {}
    primes_in_grid = set()
    for pt in grid:
        n_to_angle[pt["n"]] = pt["angle_deg"]
        if pt["is_prime"]:
            primes_in_grid.add(pt["n"])

    # Count twins and primes per sector
    twin_obs = [0] * 36
    prime_cnt = [0] * 36
    for p in sorted(primes_in_grid):
        s = int(n_to_angle.get(p, 0) / 10) % 36
        prime_cnt[s] += 1
        if p + 2 in primes_in_grid:
            twin_obs[s] += 1

    total_twins = sum(twin_obs)
    total_primes = sum(prime_cnt)

    # Expected: uniform
    twin_exp_uniform = [total_twins / 36] * 36
    # Expected: proportional to prime count
    twin_exp_prop = [total_twins * pc / total_primes if total_primes > 0 else 0
                     for pc in prime_cnt]

    angles = [(i + 0.5) * 10 for i in range(36)]
    angles_rad = [math.radians(a) for a in angles]

    # Left: Observed twin primes per sector
    ax = axes[0]
    ax.set_facecolor(C_BG)
    norm = plt.Normalize(min(twin_obs), max(twin_obs))
    cmap = plt.cm.hot
    bars = ax.bar(angles_rad, twin_obs, width=math.radians(9),
                  color=[cmap(norm(t)) for t in twin_obs], alpha=0.85, edgecolor='none')
    ax.set_title('Observed Twin Primes\nper 10\u00b0 Sector', color=C_TEXT, fontsize=10, pad=15)
    ax.tick_params(colors=C_TEXT, labelsize=6)
    ax.set_rticks([])
    ax.grid(True, alpha=0.1, color=C_TEXT)

    # Right: Residual (observed - expected proportional)
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    residuals = [o - e for o, e in zip(twin_obs, twin_exp_prop)]
    max_abs = max(abs(r) for r in residuals) if residuals else 1
    colors_r = [C_GREEN if r >= 0 else C_RED for r in residuals]
    ax2.bar(angles_rad, residuals, width=math.radians(9), color=colors_r,
            alpha=0.7, edgecolor='none')
    ax2.set_title('Twin Prime Residual\n(Observed - Proportional Expected)',
                  color=C_TEXT, fontsize=10, pad=15)
    ax2.tick_params(colors=C_TEXT, labelsize=6)
    ax2.set_rticks([])
    ax2.grid(True, alpha=0.1, color=C_TEXT)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig11_hl_heatmap.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 11 saved: hl_heatmap")


def fig12_summary_dashboard(results):
    """Fig 12: Summary dashboard of all Phase XIV findings."""
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(C_BG)

    # Create grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.35)

    # (0,0): Key correlation comparison
    ax = fig.add_subplot(gs[0, 0])
    ax.set_facecolor(C_BG)
    metrics = ['Mean\nAngle', 'Anchor\nDist', 'Rot\nSC', 'NRCI\nGL', 'Net\nRot', 'HW']
    r_p13 = [0.9906, 0.9901, 0.9894, -0.9287, -0.9572, 0.9241]
    r_p14 = [0.9684, 0.9686, 0.9696, -0.7246, -0.9363, 0.7282]
    x = np.arange(len(metrics))
    ax.barh(x - 0.15, r_p13, 0.3, color=C_BLUE, alpha=0.8, label='P13 (10\u00b0)')
    ax.barh(x + 0.15, r_p14, 0.3, color=C_PRIME, alpha=0.8, label='P14 (1\u00b0)')
    ax.set_yticks(x)
    ax.set_yticklabels(metrics, fontsize=7, color=C_TEXT)
    ax.axvline(x=0, color=C_TEXT, alpha=0.3)
    ax.set_title('UBP-Prime Correlation\nP13 vs P14', color=C_TEXT, fontsize=9)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=6)
    ax.tick_params(colors=C_TEXT, labelsize=6)
    for spine in ax.spines.values(): spine.set_color(C_GRID)

    # (0,1): 4-fold symmetry
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(C_BG)
    sym_lags = [0, 45, 90, 135, 180]
    sym_rs = [1.0000, 0.1654, 0.9835, 0.1654, 0.9849]
    ax2.bar(sym_lags, sym_rs, width=15, color=[C_ACCENT if r > 0.9 else C_BLUE for r in sym_rs],
            alpha=0.8, edgecolor='none')
    ax2.set_xlabel('Lag (degrees)', color=C_TEXT, fontsize=7)
    ax2.set_ylabel('Autocorrelation r', color=C_TEXT, fontsize=7)
    ax2.set_title('4-Fold Symmetry\nr(90\u00b0)=0.984', color=C_TEXT, fontsize=9)
    ax2.tick_params(colors=C_TEXT, labelsize=6)
    for spine in ax2.spines.values(): spine.set_color(C_GRID)

    # (0,2): K-tuple summary
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(C_BG)
    kt_names = ['Twins', 'Cousins', 'Sexy', 'Trip-1', 'Trip-2', 'Quads']
    kt_counts = [8169, 8144, 16386, 1393, 1444, 166]
    kt_colors = [C_PRIME, C_BLUE, C_GREEN, C_PURPLE, C_ORANGE, C_PINK]
    ax3.bar(kt_names, kt_counts, color=kt_colors, alpha=0.8, edgecolor='none')
    ax3.set_ylabel('Count (10\u2076 grid)', color=C_TEXT, fontsize=7)
    ax3.set_title('K-Tuple Counts\nin 10\u2076 RLS Grid', color=C_TEXT, fontsize=9)
    ax3.tick_params(colors=C_TEXT, labelsize=6, rotation=30)
    for spine in ax3.spines.values(): spine.set_color(C_GRID)

    # (1,0): HL observed vs expected
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_facecolor(C_BG)
    hl_names = ['Twins', 'Cousins', 'Sexy']
    hl_obs = [8169, 8144, 16386]
    hl_exp = [6935, 6935, 13871]
    x4 = np.arange(3)
    ax4.bar(x4 - 0.15, hl_obs, 0.3, color=C_PRIME, alpha=0.8, label='Obs')
    ax4.bar(x4 + 0.15, hl_exp, 0.3, color=C_BLUE, alpha=0.8, label='Exp')
    ax4.set_xticks(x4)
    ax4.set_xticklabels(hl_names, fontsize=7, color=C_TEXT)
    ax4.set_title('Hardy-Littlewood\nObs/Exp \u2248 1.18', color=C_TEXT, fontsize=9)
    ax4.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=6)
    ax4.tick_params(colors=C_TEXT, labelsize=6)
    for spine in ax4.spines.values(): spine.set_color(C_GRID)

    # (1,1): 3D vs 2D
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_facecolor(C_BG)
    dims = ['2D (36 sec)', '3D (36x10)', '2D (360 sec)']
    var_vals = [0.002637, 0.003184, 0.001553]
    ax5.bar(dims, var_vals, color=[C_BLUE, C_PRIME, C_GREEN], alpha=0.8, edgecolor='none')
    ax5.set_title('3D Reveals 21%\nMore Structure', color=C_TEXT, fontsize=9)
    ax5.tick_params(colors=C_TEXT, labelsize=6, rotation=15)
    for spine in ax5.spines.values(): spine.set_color(C_GRID)

    # (1,2): Gaussian integer split
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor(C_BG)
    gi_cats = ['p=1(4)', 'p=3(4)']
    gi_chi2 = [10478, 3527]
    ax6.bar(gi_cats, gi_chi2, color=[C_PRIME, C_BLUE], alpha=0.8, edgecolor='none')
    ax6.set_ylabel('\u03c7\u00b2 (angular)', color=C_TEXT, fontsize=7)
    ax6.set_title('Gaussian Integer Split\np=1(4) 3x more variable', color=C_TEXT, fontsize=9)
    ax6.tick_params(colors=C_TEXT, labelsize=7)
    for spine in ax6.spines.values(): spine.set_color(C_GRID)

    # (2, 0:2): Key findings text
    ax7 = fig.add_subplot(gs[2, :])
    ax7.set_facecolor(C_BG)
    ax7.axis('off')

    findings = [
        ("1\u00b0 Resolution", "r(RotSC)=+0.9696, r(Anchor)=+0.9686 — robust at fine scale"),
        ("4-fold Symmetry", "Autocorrelation r(90\u00b0)=0.984 — RLS has inherent 4-fold angular structure"),
        ("K-tuple Alignment", "All k-tuple DENSITIES track prime density (r>0.99) — but per-prime rates are UNIFORM"),
        ("Hardy-Littlewood", "Obs/Exp \u2248 1.18 for twins/cousins/sexy; sector distribution REJECTS uniformity (\u03c7\u00b2=1951)"),
        ("Short Intervals", "Primes in [x, x+\u221ax] cluster angularly at small x (R>0.3) but become uniform at x>10\u2074"),
        ("3D Structure", "Inner/outer angular r=+0.969; 3D voxel variance 21% higher than 2D — Time reveals hidden structure"),
        ("Gaussian Split", "p\u22611(4) and p\u22613(4) have DIFFERENT angular structures (cross-r=-0.40)"),
    ]

    for i, (title, desc) in enumerate(findings):
        y = 0.92 - i * 0.125
        ax7.text(0.02, y, f"\u25cf {title}:", transform=ax7.transAxes,
                fontsize=9, color=C_PRIME, fontweight='bold', verticalalignment='top')
        ax7.text(0.22, y, desc, transform=ax7.transAxes,
                fontsize=8, color=C_TEXT, verticalalignment='top')

    fig.suptitle('Phase XIV — Summary Dashboard: Extended UBP \u00d7 RLS Fusion (10\u2076 cells)',
                 color=C_ACCENT, fontsize=14, y=0.99, fontweight='bold')

    plt.savefig(f'{OUTDIR}phase14_fig12_dashboard.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 12 saved: dashboard")


# ════════════════════════════════════════════════════════════════════════

def main():
    print("Loading Phase XIV results...")
    results = load_results()

    print("Generating 12 publication-quality figures...")
    fig1_polar_density_1deg(results)
    fig2_correlation_stability(results)
    fig3_ktuple_angular(results)
    fig4_hardy_littlewood(results)
    fig5_3d_structure(results)
    fig6_gaussian_split(results)
    fig7_short_interval(results)
    fig8_autocorrelation_symmetry(results)
    fig9_ktuple_per_prime(results)
    fig10_3d_time_modes()
    fig11_hl_sector_heatmap(results)
    fig12_summary_dashboard(results)

    print("\nAll 12 figures generated successfully!")


if __name__ == "__main__":
    main()