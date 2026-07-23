"""
Generate 4 academic paper charts for computational musicology study.
All saved to /home/z/my-project/download/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.ticker import MaxNLocator

# ─── Global style settings ───────────────────────────────────────────
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.dpi'] = 200

# Academic palette: blues/grays + one accent (warm orange)
C_BLUE_DARK   = '#1B3A5C'   # primary blue
C_BLUE_MED    = '#3A7CA5'   # medium blue
C_BLUE_LIGHT  = '#81B4D8'   # light blue
C_GRAY_DARK   = '#4A4A4A'   # dark gray
C_GRAY_MED    = '#8C8C8C'   # medium gray
C_GRAY_LIGHT  = '#C8C8C8'   # light gray
C_ACCENT      = '#D4763C'   # warm orange accent
C_HIGHLIGHT   = '#1B6B93'   # highlight blue for best result

OUTDIR = '/home/z/my-project/download/'

# ═══════════════════════════════════════════════════════════════════════
# CHART 1: Encoding Comparison (horizontal bar chart)
# ═══════════════════════════════════════════════════════════════════════
def make_fig1():
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)

    labels = [
        'Circle-of-Fifths Gray',
        'Direct Interval',
        'Chromatic Gray',
        'Raw Binary CoF',
        'One-Hot',
    ]
    r_values = [0.8674, 0.5200, 0.2947, 0.1800, 0.0000]
    r_squared = 0.7522  # only for CoF Gray

    # Colors: highlight the best, rest in gray-blue gradient
    colors = [C_HIGHLIGHT, C_GRAY_MED, C_GRAY_MED, C_GRAY_MED, C_GRAY_LIGHT]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, r_values, height=0.55, color=colors,
                   edgecolor='white', linewidth=0.5, zorder=3)

    # Add r-value labels on bars
    for i, (bar, r) in enumerate(zip(bars, r_values)):
        label_text = f'r = {r:.4f}'
        if i == 0:
            label_text += f'  (R² = {r_squared:.4f})'
        # Position label outside bar end
        ax.text(bar.get_width() + 0.015, bar.get_y() + bar.get_height()/2,
                label_text, va='center', ha='left',
                fontsize=9.5, color=C_GRAY_DARK, fontstyle='italic')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel('Pearson Correlation (r)', fontsize=11)
    ax.set_title('Interval Consonance Correlation by Encoding Strategy',
                 fontsize=14, pad=12, color=C_BLUE_DARK)

    ax.set_xlim(0, 1.08)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(axis='x', alpha=0.3, linestyle='--', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add a subtle bracket / annotation for the best
    ax.annotate('Best encoding', xy=(0.8674, 0), xytext=(0.72, -0.7),
                fontsize=9, color=C_HIGHLIGHT, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_HIGHLIGHT, lw=1.2),
                ha='center')

    fig.savefig(OUTDIR + 'fig1_encoding_comparison.png',
                dpi=200, bbox_inches='tight')
    plt.close(fig)
    print('✓ fig1_encoding_comparison.png saved')


# ═══════════════════════════════════════════════════════════════════════
# CHART 2: Golay Ceiling (dual panel)
# ═══════════════════════════════════════════════════════════════════════
def make_fig2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)

    fig.suptitle('The Golay [24,12,8] Three-Distance Ceiling',
                 fontsize=14, color=C_BLUE_DARK, y=1.02)

    # ── Left panel: histogram of distances ──
    distances = [8, 12, 16]
    counts = [759, 2576, 759]
    total = 4096
    proportions = [c / total for c in counts]

    bar_colors = [C_BLUE_DARK, C_BLUE_MED, C_BLUE_DARK]
    bars = ax1.bar(distances, proportions, width=2.8, color=bar_colors,
                   edgecolor='white', linewidth=0.5, zorder=3)

    for bar, d, p in zip(bars, distances, proportions):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                 f'{p:.3f}\n({counts[distances.index(d)]}/{total})',
                 ha='center', va='bottom', fontsize=8.5, color=C_GRAY_DARK)

    ax1.set_xticks(distances)
    ax1.set_xticklabels(['d = 8', 'd = 12', 'd = 16'], fontsize=10)
    ax1.set_xlabel('Hamming Distance', fontsize=11)
    ax1.set_ylabel('Proportion of Pairs', fontsize=11)
    ax1.set_title('Theoretical Distance Distribution', fontsize=12,
                  color=C_BLUE_DARK, pad=8)
    ax1.set_ylim(0, 0.72)
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax1.tick_params(axis='both', labelsize=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # ── Right panel: mapping diagram ──
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-1, 9)
    ax2.axis('off')
    ax2.set_title('Consonance Rank → Distance Mapping', fontsize=12,
                  color=C_BLUE_DARK, pad=8)

    # Rank labels (left column)
    rank_labels = ['Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5', 'Rank 6']
    rank_y = [7.5, 6.3, 4.5, 3.3, 2.1, 0.9]

    for lbl, y in zip(rank_labels, rank_y):
        ax2.text(0.5, y, lbl, fontsize=10, va='center', ha='center',
                 color=C_GRAY_DARK, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=C_GRAY_LIGHT,
                           edgecolor=C_GRAY_MED, linewidth=0.8))

    # Distance target boxes (right column)
    # d=8 box
    rect_d8 = mpatches.FancyBboxPatch((7, 5.8), 3, 2.2,
                                       boxstyle='round,pad=0.3',
                                       facecolor=C_BLUE_LIGHT,
                                       edgecolor=C_BLUE_DARK, linewidth=1.2)
    ax2.add_patch(rect_d8)
    ax2.text(8.5, 6.9, 'd = 8', fontsize=12, va='center', ha='center',
             color=C_BLUE_DARK, fontweight='bold')
    ax2.text(8.5, 6.1, 'Consonant', fontsize=9, va='center', ha='center',
             color=C_GRAY_DARK, fontstyle='italic')

    # d=12 box
    rect_d12 = mpatches.FancyBboxPatch((7, 0.3), 3, 4.2,
                                        boxstyle='round,pad=0.3',
                                        facecolor='#F5E6D3',
                                        edgecolor=C_ACCENT, linewidth=1.2)
    ax2.add_patch(rect_d12)
    ax2.text(8.5, 3.5, 'd = 12', fontsize=12, va='center', ha='center',
             color=C_ACCENT, fontweight='bold')
    ax2.text(8.5, 2.7, 'Dissonant', fontsize=9, va='center', ha='center',
             color=C_GRAY_DARK, fontstyle='italic')

    # Arrows: Rank 1,2 → d=8
    for y in [7.5, 6.3]:
        ax2.annotate('', xy=(7, 6.9), xytext=(2.2, y),
                     arrowprops=dict(arrowstyle='->', color=C_BLUE_DARK,
                                     lw=1.5, connectionstyle='arc3,rad=0.0'))

    # Arrows: Rank 3,4,5,6 → d=12
    for y in [4.5, 3.3, 2.1, 0.9]:
        ax2.annotate('', xy=(7, 2.4), xytext=(2.2, y),
                     arrowprops=dict(arrowstyle='->', color=C_ACCENT,
                                     lw=1.3, connectionstyle='arc3,rad=0.0'))

    # Annotation about information loss
    ax2.text(5.0, -0.6, '6 ranks → 2 distances: information loss',
             fontsize=8.5, va='center', ha='center',
             color=C_ACCENT, fontstyle='italic',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFF3E6',
                       edgecolor=C_ACCENT, linewidth=0.6, alpha=0.9))

    fig.savefig(OUTDIR + 'fig2_golay_ceiling.png',
                dpi=200, bbox_inches='tight')
    plt.close(fig)
    print('✓ fig2_golay_ceiling.png saved')


# ═══════════════════════════════════════════════════════════════════════
# CHART 3: Dimensional Hierarchy (dual y-axis line chart)
# ═══════════════════════════════════════════════════════════════════════
def make_fig3():
    fig, ax1 = plt.subplots(figsize=(8, 5), constrained_layout=True)

    dims = [24, 256, 512, 1024]
    dim_labels = ['Golay\n(24)', 'BW\n(256)', 'BW\n(512)', 'BW\n(1024)']
    interval_r = [0.8674, 0.8674, 0.8674, 0.8674]
    chord_r = [-0.0894, -0.0894, -0.0894, -0.0894]
    dist_ranges = ['[8, 12]', '[16.0, 19.6]', '[22.6, 27.7]', '[32.0, 39.2]']

    x = np.arange(len(dims))

    # Left axis: Interval correlation
    line1, = ax1.plot(x, interval_r, 'o-', color=C_BLUE_DARK, linewidth=2.2,
                      markersize=8, markerfacecolor=C_BLUE_DARK,
                      markeredgecolor='white', markeredgewidth=1.5,
                      label='Interval r', zorder=5)
    ax1.set_ylabel('Interval Consonance r', fontsize=11, color=C_BLUE_DARK)
    ax1.tick_params(axis='y', labelcolor=C_BLUE_DARK, labelsize=10)
    ax1.set_ylim(0.7, 1.0)
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))

    # Right axis: Chord correlation
    ax2 = ax1.twinx()
    line2, = ax2.plot(x, chord_r, 's--', color=C_ACCENT, linewidth=2.2,
                      markersize=8, markerfacecolor=C_ACCENT,
                      markeredgecolor='white', markeredgewidth=1.5,
                      label='Chord r', zorder=5)
    ax2.set_ylabel('Chord Quality Correlation r', fontsize=11, color=C_ACCENT)
    ax2.tick_params(axis='y', labelcolor=C_ACCENT, labelsize=10)
    ax2.set_ylim(-0.25, 0.10)
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))

    # X-axis
    ax1.set_xticks(x)
    ax1.set_xticklabels(dim_labels, fontsize=10)
    ax1.set_xlabel('Embedding Dimension', fontsize=11)

    # Distance range annotations below x-axis
    for i, (d, dr) in enumerate(zip(dims, dist_ranges)):
        ax1.annotate(f'Dist: {dr}', xy=(i, 0.705), fontsize=7.5,
                     ha='center', va='top', color=C_GRAY_MED,
                     fontstyle='italic')

    ax1.tick_params(axis='x', labelsize=10)

    # Title
    ax1.set_title('Correlation Preservation Across Dimensional Expansion',
                  fontsize=14, pad=12, color=C_BLUE_DARK)

    # Grid
    ax1.grid(axis='y', alpha=0.2, linestyle='--', zorder=0)
    ax1.spines['top'].set_visible(False)

    # Legend
    lines = [line1, line2]
    labels_leg = [l.get_label() for l in lines]
    ax1.legend(lines, labels_leg, loc='lower right', fontsize=9,
               framealpha=0.9, edgecolor=C_GRAY_LIGHT)

    # Annotation
    ax1.annotate('Signal preserved but never enriched',
                 xy=(1.5, 0.8674), xytext=(1.5, 0.93),
                 fontsize=9, ha='center', va='bottom',
                 color=C_BLUE_DARK, fontstyle='italic', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0F8',
                           edgecolor=C_BLUE_MED, linewidth=0.8, alpha=0.9),
                 arrowprops=dict(arrowstyle='->', color=C_BLUE_DARK, lw=1.0))

    # Value annotations on points
    for i, (ir, cr) in enumerate(zip(interval_r, chord_r)):
        ax1.annotate(f'{ir:.4f}', xy=(i, ir), xytext=(i, ir + 0.015),
                     fontsize=8, ha='center', va='bottom', color=C_BLUE_DARK)
        ax2.annotate(f'{cr:.4f}', xy=(i, cr), xytext=(i, cr - 0.025),
                     fontsize=8, ha='center', va='top', color=C_ACCENT)

    fig.savefig(OUTDIR + 'fig3_dimensional_hierarchy.png',
                dpi=200, bbox_inches='tight')
    plt.close(fig)
    print('✓ fig3_dimensional_hierarchy.png saved')


# ═══════════════════════════════════════════════════════════════════════
# CHART 4: Mersenne/Fermat Duality in mod-144 Space (polar/circular)
# ═══════════════════════════════════════════════════════════════════════
def make_fig4():
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True,
                           subplot_kw={'projection': 'polar'})

    ax.set_title('Mersenne/Fermat Duality in mod-144 Space',
                 fontsize=14, pad=20, color=C_BLUE_DARK)

    # Positions on mod-144 circle (angles in radians)
    residues = [17, 31, 113, 127]
    angles = [2 * np.pi * r / 144 for r in residues]

    # Fermat residues: 17, 113 (3^2+2^3=17, 3^2·2^4+2^3·3^2+1 ... conceptually)
    # Mersenne residues: 31, 127 (2^5-1=31, 2^7-1=127)
    fermat_idx = [0, 2]   # 17, 113
    mersenne_idx = [1, 3]  # 31, 127

    # Draw the mod-144 circle
    theta_circle = np.linspace(0, 2 * np.pi, 200)
    ax.plot(theta_circle, np.ones_like(theta_circle), '-',
            color=C_GRAY_LIGHT, linewidth=1.5, zorder=1)

    # Tick marks every 24 units (like clock hours) with labels
    for tick_val in range(0, 144, 24):
        tick_angle = 2 * np.pi * tick_val / 144
        ax.plot([tick_angle, tick_angle], [0.92, 1.05], '-',
                color=C_GRAY_MED, linewidth=0.7, zorder=2)
        ax.text(tick_angle, 1.13, str(tick_val), fontsize=7.5,
                ha='center', va='center', color=C_GRAY_MED)

    # Minor tick marks every 12 units
    for tick_val in range(0, 144, 12):
        if tick_val % 24 != 0:
            tick_angle = 2 * np.pi * tick_val / 144
            ax.plot([tick_angle, tick_angle], [0.96, 1.02], '-',
                    color=C_GRAY_LIGHT, linewidth=0.5, zorder=2)

    # Plot points
    for i in fermat_idx:
        ax.plot(angles[i], 1.0, 'o', color=C_BLUE_DARK, markersize=14,
                markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        ax.text(angles[i], 1.22, str(residues[i]), fontsize=11,
                ha='center', va='center', color=C_BLUE_DARK, fontweight='bold')

    for i in mersenne_idx:
        ax.plot(angles[i], 1.0, 's', color=C_ACCENT, markersize=13,
                markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        ax.text(angles[i], 1.22, str(residues[i]), fontsize=11,
                ha='center', va='center', color=C_ACCENT, fontweight='bold')

    # XOR identity lines: 31⊕127 = 96, 17⊕113 = 96
    # 31↔127 (Mersenne pair)
    ax.plot([angles[1], angles[3]], [1.0, 1.0], '--',
            color=C_ACCENT, linewidth=1.8, alpha=0.8, zorder=4)
    mid_angle_m = (angles[1] + angles[3]) / 2
    if abs(angles[3] - angles[1]) > np.pi:
        mid_angle_m += np.pi
    ax.text(mid_angle_m, 0.78, '31 ⊕ 127 = 96', fontsize=8.5,
            ha='center', va='center', color=C_ACCENT, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3E6',
                      edgecolor=C_ACCENT, linewidth=0.6, alpha=0.9))

    # 17↔113 (Fermat pair)
    ax.plot([angles[0], angles[2]], [1.0, 1.0], '--',
            color=C_BLUE_DARK, linewidth=1.8, alpha=0.8, zorder=4)
    mid_angle_f = (angles[0] + angles[2]) / 2
    if abs(angles[2] - angles[0]) > np.pi:
        mid_angle_f += np.pi
    ax.text(mid_angle_f, 0.78, '17 ⊕ 113 = 96', fontsize=8.5,
            ha='center', va='center', color=C_BLUE_DARK, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F0F8',
                      edgecolor=C_BLUE_DARK, linewidth=0.6, alpha=0.9))

    # Music theory annotations
    # 17 ≡ 5 (mod 12) = Fourth
    ax.text(angles[0], 0.55, '17 ≡ 5 (mod 12)\n= Fourth',
            fontsize=7.5, ha='center', va='center', color=C_BLUE_DARK,
            fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=C_BLUE_LIGHT, linewidth=0.5, alpha=0.85))

    # 31 ≡ 7 (mod 12) = Fifth
    ax.text(angles[1], 0.55, '31 ≡ 7 (mod 12)\n= Fifth',
            fontsize=7.5, ha='center', va='center', color=C_ACCENT,
            fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=C_ACCENT, linewidth=0.5, alpha=0.85))

    # 113 ≡ 5 (mod 12) = Fourth
    ax.text(angles[2], 0.55, '113 ≡ 5 (mod 12)\n= Fourth',
            fontsize=7.5, ha='center', va='center', color=C_BLUE_DARK,
            fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=C_BLUE_LIGHT, linewidth=0.5, alpha=0.85))

    # 127 ≡ 7 (mod 12) = Fifth
    ax.text(angles[3], 0.55, '127 ≡ 7 (mod 12)\n= Fifth',
            fontsize=7.5, ha='center', va='center', color=C_ACCENT,
            fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=C_ACCENT, linewidth=0.5, alpha=0.85))

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C_BLUE_DARK,
               markersize=10, label='Fermat residues (17, 113)'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=C_ACCENT,
               markersize=10, label='Mersenne residues (31, 127)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8.5,
              bbox_to_anchor=(1.25, -0.08), framealpha=0.9,
              edgecolor=C_GRAY_LIGHT)

    # Configure polar axes
    ax.set_ylim(0, 1.4)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    fig.savefig(OUTDIR + 'fig4_mersenne_fermat_duality.png',
                dpi=200, bbox_inches='tight')
    plt.close(fig)
    print('✓ fig4_mersenne_fermat_duality.png saved')


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    print('\nAll 4 figures generated successfully.')