"""Generate remaining Phase XIV figures (10, 11, 12)."""
import json, math, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['font.size'] = 9

C_BG = '#1a1a2e'; C_GRID = '#2d2d4a'; C_TEXT = '#e0e0e0'
C_PRIME = '#FF6B35'; C_BLUE = '#3498db'; C_GREEN = '#2ecc71'
C_PURPLE = '#9b59b6'; C_ORANGE = '#e67e22'; C_PINK = '#e91e63'
C_ACCENT = '#FFE66D'; C_RED = '#e74c3c'
OUTDIR = '/home/z/my-project/download/'


def fig10_3d_time_modes():
    """Fig 10: 3D RLS with different Time axis definitions (lightweight)."""
    # Load pre-computed grid sample
    with open('/home/z/my-project/scripts/phase14_rls_grid.json') as f:
        grid = json.load(f)

    fig = plt.figure(figsize=(16, 5))
    fig.patch.set_facecolor(C_BG)
    fig.suptitle('3D RLS: Comparing Time Dimension Definitions',
                 color=C_TEXT, fontsize=13, y=1.02)

    primes = [p for p in grid if p["is_prime"]][::2]
    comps = [p for p in grid if not p["is_prime"]][::15]

    # Time = Layer index
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.set_facecolor(C_BG)
    for c in comps[:1500]:
        ax1.scatter([c["i"]], [c["j"]], [c["layer_idx"]], c=C_BLUE, s=0.2, alpha=0.03)
    for c in primes:
        ax1.scatter([c["i"]], [c["j"]], [c["layer_idx"]], c=C_PRIME, s=2, alpha=0.5)
    ax1.set_title('Time = Layer Index\n(Natural RLS ordering)', color=C_TEXT, fontsize=9)
    ax1.tick_params(colors=C_TEXT, labelsize=5, pad=0)
    ax1.xaxis.pane.fill = False; ax1.yaxis.pane.fill = False; ax1.zaxis.pane.fill = False
    ax1.view_init(elev=20, azim=45)

    # Time = log(n)
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.set_facecolor(C_BG)
    for c in comps[:1500]:
        z = math.log(c["n"]) if c["n"] > 1 else 0
        ax2.scatter([c["i"]], [c["j"]], [z], c=C_BLUE, s=0.2, alpha=0.03)
    for c in primes:
        z = math.log(c["n"]) if c["n"] > 1 else 0
        ax2.scatter([c["i"]], [c["j"]], [z], c=C_PRIME, s=2, alpha=0.5)
    ax2.set_title('Time = log(n)\n(Logarithmic natural ordering)', color=C_TEXT, fontsize=9)
    ax2.tick_params(colors=C_TEXT, labelsize=5, pad=0)
    ax2.xaxis.pane.fill = False; ax2.yaxis.pane.fill = False; ax2.zaxis.pane.fill = False
    ax2.view_init(elev=20, azim=45)

    # Time = Radius (sqrt(m)) — continuous RLS distance
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.set_facecolor(C_BG)
    for c in comps[:1500]:
        ax3.scatter([c["i"]], [c["j"]], [c["radius"]], c=C_BLUE, s=0.2, alpha=0.03)
    for c in primes:
        ax3.scatter([c["i"]], [c["j"]], [c["radius"]], c=C_PRIME, s=2, alpha=0.5)
    ax3.set_title('Time = Radius = sqrt(m)\n(Continuous RLS distance)', color=C_TEXT, fontsize=9)
    ax3.tick_params(colors=C_TEXT, labelsize=5, pad=0)
    ax3.xaxis.pane.fill = False; ax3.yaxis.pane.fill = False; ax3.zaxis.pane.fill = False
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

    twin_obs = [0] * 36
    prime_cnt = [0] * 36
    for p in sorted(primes_in_grid):
        s = int(n_to_angle.get(p, 0) / 10) % 36
        prime_cnt[s] += 1
        if p + 2 in primes_in_grid:
            twin_obs[s] += 1

    total_twins = sum(twin_obs)
    total_primes = sum(prime_cnt)

    twin_exp_prop = [total_twins * pc / total_primes if total_primes > 0 else 0
                     for pc in prime_cnt]

    angles = [(i + 0.5) * 10 for i in range(36)]
    angles_rad = [math.radians(a) for a in angles]

    # Left: Observed
    ax.set_facecolor(C_BG)
    norm = plt.Normalize(min(twin_obs), max(twin_obs))
    cmap = plt.cm.hot
    ax.bar(angles_rad, twin_obs, width=math.radians(9),
           color=[cmap(norm(t)) for t in twin_obs], alpha=0.85, edgecolor='none')
    ax.set_title('Observed Twin Primes\nper 10\u00b0 Sector', color=C_TEXT, fontsize=10, pad=15)
    ax.tick_params(colors=C_TEXT, labelsize=6)
    ax.set_rticks([]); ax.grid(True, alpha=0.1, color=C_TEXT)

    # Right: Residual
    ax2.set_facecolor(C_BG)
    residuals = [o - e for o, e in zip(twin_obs, twin_exp_prop)]
    colors_r = [C_GREEN if r >= 0 else C_RED for r in residuals]
    ax2.bar(angles_rad, residuals, width=math.radians(9), color=colors_r,
            alpha=0.7, edgecolor='none')
    ax2.set_title('Twin Prime Residual\n(Observed \u2212 Proportional Expected)',
                  color=C_TEXT, fontsize=10, pad=15)
    ax2.tick_params(colors=C_TEXT, labelsize=6)
    ax2.set_rticks([]); ax2.grid(True, alpha=0.1, color=C_TEXT)

    plt.tight_layout()
    plt.savefig(f'{OUTDIR}phase14_fig11_hl_heatmap.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 11 saved: hl_heatmap")


def fig12_summary_dashboard(results):
    """Fig 12: Summary dashboard."""
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(C_BG)
    gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35)

    # (0,0): Correlation comparison
    ax = fig.add_subplot(gs[0, 0]); ax.set_facecolor(C_BG)
    metrics = ['Mean\nAngle', 'Anchor\nDist', 'Rot\nSC', 'NRCI\nGL', 'Net\nRot', 'HW']
    r_p13 = [0.9906, 0.9901, 0.9894, -0.9287, -0.9572, 0.9241]
    r_p14 = [0.9684, 0.9686, 0.9696, -0.7246, -0.9363, 0.7282]
    x = np.arange(len(metrics))
    ax.barh(x - 0.15, r_p13, 0.3, color=C_BLUE, alpha=0.8, label='P13 (10\u00b0)')
    ax.barh(x + 0.15, r_p14, 0.3, color=C_PRIME, alpha=0.8, label='P14 (1\u00b0)')
    ax.set_yticks(x); ax.set_yticklabels(metrics, fontsize=7, color=C_TEXT)
    ax.axvline(x=0, color=C_TEXT, alpha=0.3)
    ax.set_title('UBP-Prime Correlation\nP13 vs P14', color=C_TEXT, fontsize=9)
    ax.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=6)
    ax.tick_params(colors=C_TEXT, labelsize=6)
    for sp in ax.spines.values(): sp.set_color(C_GRID)

    # (0,1): 4-fold symmetry
    ax2 = fig.add_subplot(gs[0, 1]); ax2.set_facecolor(C_BG)
    sym_lags = [0, 45, 90, 135, 180]
    sym_rs = [1.0000, 0.1654, 0.9835, 0.1654, 0.9849]
    ax2.bar(sym_lags, sym_rs, width=15, color=[C_ACCENT if r > 0.9 else C_BLUE for r in sym_rs],
            alpha=0.8, edgecolor='none')
    ax2.set_xlabel('Lag (degrees)', color=C_TEXT, fontsize=7)
    ax2.set_ylabel('Autocorrelation r', color=C_TEXT, fontsize=7)
    ax2.set_title('4-Fold Symmetry\nr(90\u00b0)=0.984', color=C_TEXT, fontsize=9)
    ax2.tick_params(colors=C_TEXT, labelsize=6)
    for sp in ax2.spines.values(): sp.set_color(C_GRID)

    # (0,2): K-tuple counts
    ax3 = fig.add_subplot(gs[0, 2]); ax3.set_facecolor(C_BG)
    kt_names = ['Twins', 'Cousins', 'Sexy', 'Trip-1', 'Trip-2', 'Quads']
    kt_counts = [8169, 8144, 16386, 1393, 1444, 166]
    kt_colors = [C_PRIME, C_BLUE, C_GREEN, C_PURPLE, C_ORANGE, C_PINK]
    ax3.bar(kt_names, kt_counts, color=kt_colors, alpha=0.8, edgecolor='none')
    ax3.set_ylabel('Count (10\u2076 grid)', color=C_TEXT, fontsize=7)
    ax3.set_title('K-Tuple Counts\nin 10\u2076 RLS Grid', color=C_TEXT, fontsize=9)
    ax3.tick_params(colors=C_TEXT, labelsize=6, rotation=30)
    for sp in ax3.spines.values(): sp.set_color(C_GRID)

    # (1,0): HL observed vs expected
    ax4 = fig.add_subplot(gs[1, 0]); ax4.set_facecolor(C_BG)
    hl_names = ['Twins', 'Cousins', 'Sexy']
    hl_obs = [8169, 8144, 16386]; hl_exp = [6935, 6935, 13871]
    x4 = np.arange(3)
    ax4.bar(x4 - 0.15, hl_obs, 0.3, color=C_PRIME, alpha=0.8, label='Obs')
    ax4.bar(x4 + 0.15, hl_exp, 0.3, color=C_BLUE, alpha=0.8, label='Exp')
    ax4.set_xticks(x4); ax4.set_xticklabels(hl_names, fontsize=7, color=C_TEXT)
    ax4.set_title('Hardy-Littlewood\nObs/Exp \u2248 1.18', color=C_TEXT, fontsize=9)
    ax4.legend(facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=6)
    ax4.tick_params(colors=C_TEXT, labelsize=6)
    for sp in ax4.spines.values(): sp.set_color(C_GRID)

    # (1,1): 3D vs 2D variance
    ax5 = fig.add_subplot(gs[1, 1]); ax5.set_facecolor(C_BG)
    dims = ['2D\n(36 sec)', '3D Voxel\n(36x10)', '2D\n(360 sec)']
    var_vals = [0.002637, 0.003184, 0.001553]
    ax5.bar(dims, var_vals, color=[C_BLUE, C_PRIME, C_GREEN], alpha=0.8, edgecolor='none')
    ax5.set_title('3D Reveals 21%\nMore Structure', color=C_TEXT, fontsize=9)
    ax5.tick_params(colors=C_TEXT, labelsize=6)
    for sp in ax5.spines.values(): sp.set_color(C_GRID)

    # (1,2): Gaussian integer split
    ax6 = fig.add_subplot(gs[1, 2]); ax6.set_facecolor(C_BG)
    gi_cats = ['p=1(4)', 'p=3(4)']; gi_chi2 = [10478, 3527]
    ax6.bar(gi_cats, gi_chi2, color=[C_PRIME, C_BLUE], alpha=0.8, edgecolor='none')
    ax6.set_ylabel('\u03c7\u00b2 (angular)', color=C_TEXT, fontsize=7)
    ax6.set_title('Gaussian Integer Split\np=1(4) 3x more variable', color=C_TEXT, fontsize=9)
    ax6.tick_params(colors=C_TEXT, labelsize=7)
    for sp in ax6.spines.values(): sp.set_color(C_GRID)

    # (2, 0:2): Key findings
    ax7 = fig.add_subplot(gs[2, :]); ax7.set_facecolor(C_BG); ax7.axis('off')
    findings = [
        ("1\u00b0 Resolution", "r(RotSC)=+0.9696, r(Anchor)=+0.9686 \u2014 robust at fine scale; NRCI_GL drops from -0.93 to -0.72"),
        ("4-fold Symmetry", "Circular autocorrelation r(90\u00b0)=0.984 \u2014 RLS has inherent 4-fold angular structure from i\u00b2+j\u00b2=m"),
        ("K-tuple Alignment", "All k-tuple DENSITIES track prime density (r>0.99), but per-prime k-tuple rates are UNIFORM across all sectors"),
        ("Hardy-Littlewood", "Obs/Exp \u2248 1.18 for twins/cousins/sexy; sector distribution REJECTS uniformity (\u03c7\u00b2=1951, df=35)"),
        ("Short Intervals", "Primes in [x, x+\u221ax] cluster angularly at small x (R>0.3) but become uniform at x>10\u2074"),
        ("3D Structure", "Inner/outer angular r=+0.969 (consistent); 3D voxel variance 21% higher \u2014 Time dimension reveals hidden structure"),
        ("Gaussian Split", "p\u22611(4) and p\u22613(4) have DIFFERENT angular structures (cross-r=-0.40); p\u22611(4) 3x more angularly variable"),
    ]
    for i, (title, desc) in enumerate(findings):
        y = 0.92 - i * 0.125
        ax7.text(0.02, y, f"\u25cf {title}:", transform=ax7.transAxes,
                fontsize=9, color=C_PRIME, fontweight='bold', verticalalignment='top')
        ax7.text(0.22, y, desc, transform=ax7.transAxes,
                fontsize=8, color=C_TEXT, verticalalignment='top')

    fig.suptitle('Phase XIV \u2014 Summary Dashboard: Extended UBP \u00d7 RLS Fusion (10\u2076 cells)',
                 color=C_ACCENT, fontsize=14, y=0.99, fontweight='bold')
    plt.savefig(f'{OUTDIR}phase14_fig12_dashboard.png', facecolor=C_BG,
                bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print("  Fig 12 saved: dashboard")


if __name__ == "__main__":
    with open('/home/z/my-project/scripts/phase14_results.json') as f:
        results = json.load(f)

    print("Generating remaining figures (10, 11, 12)...")
    fig10_3d_time_modes()
    fig11_hl_sector_heatmap(results)
    fig12_summary_dashboard(results)
    print("\nAll remaining figures generated!")