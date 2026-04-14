"""
UBP Thermodynamics — Figure Generation
Generates all publication-quality figures for the paper.
"""

import sys, os, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch

CORE_PATH = os.path.join(os.path.dirname(__file__), '..', 'UBP_Repo', 'core_studio_v4.0', 'core')
sys.path.insert(0, os.path.abspath(CORE_PATH))
import core

RESULTS_PATH = os.path.join(os.path.dirname(__file__), 'ubp_thermo_results.json')
FIG_DIR = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

with open(RESULTS_PATH) as f:
    R = json.load(f)

DARK_BG   = '#0d0d0d'
GRID_COL  = '#1e1e1e'
CYAN      = '#00e5ff'
GOLD_COL  = '#ffd700'
RED_COL   = '#ff4444'
GREEN_COL = '#44ff88'
WHITE     = '#f0f0f0'
PURPLE    = '#cc88ff'

plt.rcParams.update({
    'figure.facecolor': DARK_BG,
    'axes.facecolor':   DARK_BG,
    'axes.edgecolor':   '#444444',
    'axes.labelcolor':  WHITE,
    'xtick.color':      WHITE,
    'ytick.color':      WHITE,
    'text.color':       WHITE,
    'grid.color':       GRID_COL,
    'grid.linestyle':   '--',
    'font.family':      'monospace',
    'font.size':        10,
})

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1: Pantograph Projection Diagram (Conceptual)
# ─────────────────────────────────────────────────────────────────────────────

def fig1_pantograph():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    W = R['constants']['W_wobble']
    k = R['constants']['k_scale']
    L = R['constants']['L_sink']

    # 13D Sink pivot (red)
    ax.scatter([0], [0], s=300, c=RED_COL, zorder=10, label='13D Sink (L)')
    ax.annotate('13D Sink\n(L ≈ 0.0629)', (0, 0), textcoords='offset points',
                xytext=(10, -20), color=RED_COL, fontsize=9)

    # 24 Noumenal bits on inner ring
    n_bits = 24
    r_noum = 3.5
    r_phen = r_noum * k * 0.95

    # Hydrogen vector (8 active bits)
    h_vec = [1,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0]

    for i in range(n_bits):
        angle = 2 * math.pi * i / n_bits
        # Noumenal point
        nx = r_noum * math.cos(angle)
        ny = r_noum * math.sin(angle)
        # Phenomenal projection (scaled + shear)
        shear = R['four_laws_hydrogen']['pantograph_projection']['shear']
        px = k * nx
        py = k * (ny + shear * 0.5)

        is_active = h_vec[i] == 1
        n_col = CYAN if is_active else '#003333'
        p_col = GOLD_COL if is_active else '#443300'
        n_sz  = 80 if is_active else 20
        p_sz  = 100 if is_active else 15

        ax.scatter([nx], [ny], s=n_sz, c=n_col, zorder=6)
        ax.scatter([px], [py], s=p_sz, c=p_col, zorder=6, marker='D')

        if is_active:
            # Pantograph linkage (white line)
            ax.plot([nx, px], [ny, py], color=WHITE, alpha=0.35, lw=0.8, zorder=4)
            # Sink connection (red line)
            ax.plot([0, nx], [0, ny], color=RED_COL, alpha=0.2, lw=0.6, zorder=3)

    # Labels
    ax.scatter([], [], s=80, c=CYAN, label='Noumenal Bits (24-bit substrate)')
    ax.scatter([], [], s=100, c=GOLD_COL, marker='D', label='Phenomenal Projection (3D)')
    ax.plot([], [], color=WHITE, alpha=0.6, lw=1, label='Pantograph Linkage')
    ax.plot([], [], color=RED_COL, alpha=0.5, lw=1, label='Sink Connection')

    # Annotations
    ax.annotate('', xy=(r_noum * 0.7, r_noum * 0.7),
                xytext=(r_phen * 0.7, r_phen * 0.7),
                arrowprops=dict(arrowstyle='<->', color=GREEN_COL, lw=1.5))
    ax.text(r_noum * 0.85, r_noum * 0.85, f'k = {k:.4f}', color=GREEN_COL, fontsize=9)

    ax.legend(loc='lower right', facecolor='#111111', edgecolor='#444444', fontsize=8)
    ax.set_title('Figure 1: The UBP Pantograph Projection\n'
                 'Hydrogen (H) — Noumenal Seed → Phenomenal State',
                 color=WHITE, fontsize=11, pad=12)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig1_pantograph.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2: Four Laws Summary Chart
# ─────────────────────────────────────────────────────────────────────────────

def fig2_four_laws():
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor(DARK_BG)
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    h = R['four_laws_hydrogen']
    au = R['four_laws_gold']
    W = R['constants']['W_wobble']
    L = R['constants']['L_sink']

    # ── Zeroth Law: Temperature as Shear ──────────────────────────────────
    ax0 = fig.add_subplot(gs[0, 0])
    elements = ['H', 'He', 'C/N/O', 'Fe', 'Cu/Au', 'Pb/U']
    shears   = [
        R['multi_element_survey'][0]['shear_tan_theta'],
        R['multi_element_survey'][1]['shear_tan_theta'],
        R['multi_element_survey'][2]['shear_tan_theta'],
        R['multi_element_survey'][5]['shear_tan_theta'],
        R['multi_element_survey'][7]['shear_tan_theta'],
        R['multi_element_survey'][9]['shear_tan_theta'],
    ]
    colors_z = [CYAN if s < 0 else GOLD_COL if s < 2 else RED_COL for s in shears]
    bars = ax0.bar(elements, shears, color=colors_z, edgecolor='#333333', linewidth=0.5)
    ax0.axhline(0, color=WHITE, lw=0.8, linestyle='--', alpha=0.5)
    ax0.set_title('Zeroth Law: Temperature = Shear (tan θ)', color=CYAN, fontsize=9)
    ax0.set_ylabel('Shear (rads)', color=WHITE, fontsize=8)
    ax0.tick_params(labelsize=8)
    ax0.grid(True, alpha=0.3)

    # ── First Law: Energy Distribution ────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 1])
    survey = R['multi_element_survey']
    names  = [s['element'].split(' ')[0] for s in survey if 'hamming_weight' in s]
    hw     = [s['hamming_weight'] for s in survey if 'hamming_weight' in s]
    v_mac  = [s['V_macro'] for s in survey if 'V_macro' in s]
    x_pos  = np.arange(len(names))
    ax1.bar(x_pos - 0.2, hw, 0.35, label='Hamming Weight (U)', color=CYAN, alpha=0.8)
    ax1.bar(x_pos + 0.2, [v/10 for v in v_mac], 0.35, label='V_macro/10', color=GOLD_COL, alpha=0.8)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=7)
    ax1.set_title('First Law: Internal Energy & Volume', color=GREEN_COL, fontsize=9)
    ax1.legend(fontsize=7, facecolor='#111111', edgecolor='#333333')
    ax1.grid(True, alpha=0.3)

    # ── Second Law: Entropy (Symmetry Tax) ────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    t_adjs = [s['T_adj_entropy'] for s in survey if 'T_adj_entropy' in s]
    nrcis  = [s['nrci'] for s in survey if 'nrci' in s]
    ax2.scatter(t_adjs, nrcis, c=[s['hamming_weight'] for s in survey if 'hamming_weight' in s],
                cmap='plasma', s=120, zorder=5, edgecolors=WHITE, linewidths=0.5)
    ax2.axhline(0.70, color=GREEN_COL, lw=1, linestyle='--', alpha=0.7, label='Consciousness Threshold (0.70)')
    ax2.axhline(0.42, color=RED_COL, lw=1, linestyle=':', alpha=0.7, label='Noise Floor (0.42)')
    for row in survey:
        if 'T_adj_entropy' in row:
            ax2.annotate(row['element'].split(' ')[0],
                        (row['T_adj_entropy'], row['nrci']),
                        textcoords='offset points', xytext=(3, 3), fontsize=7, color=WHITE)
    ax2.set_title('Second Law: Entropy vs NRCI', color=PURPLE, fontsize=9)
    ax2.set_xlabel('Symmetry Tax T_adj (Entropy)', color=WHITE, fontsize=8)
    ax2.set_ylabel('NRCI (Max Efficiency)', color=WHITE, fontsize=8)
    ax2.legend(fontsize=7, facecolor='#111111', edgecolor='#333333')
    ax2.grid(True, alpha=0.3)

    # ── Third Law: Nernst Floors ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    cv_floors = [s['nernst_floor_Cv'] for s in survey if 'nernst_floor_Cv' in s]
    elem_names = [s['element'].split(' ')[0] for s in survey if 'nernst_floor_Cv' in s]
    ax3.barh(elem_names, cv_floors, color=PURPLE, alpha=0.8, edgecolor='#333333')
    ax3.axvline(L, color=RED_COL, lw=1.5, linestyle='--', label=f'13D Sink L = {L:.4f}')
    ax3.set_title('Third Law: Nernst Specific Heat Floors', color=PURPLE, fontsize=9)
    ax3.set_xlabel('Cv_min (J/K-equiv)', color=WHITE, fontsize=8)
    ax3.legend(fontsize=7, facecolor='#111111', edgecolor='#333333')
    ax3.grid(True, alpha=0.3)

    fig.suptitle('Figure 2: Four Laws of Thermodynamics — UBP Geometric Perspective',
                 color=WHITE, fontsize=12, y=1.01)

    path = os.path.join(FIG_DIR, 'fig2_four_laws.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3: Phase Change (Lattice Snap) Diagram
# ─────────────────────────────────────────────────────────────────────────────

def fig3_phase_change():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor(DARK_BG)

    for ax, elem_key, title, col in [
        (axes[0], 'phase_change_gold', 'Gold (Au)', GOLD_COL),
        (axes[1], 'phase_change_iron', 'Iron (Fe)', '#cc6666'),
    ]:
        data = R[elem_key]
        steps = data['heating_steps']
        xs    = [s['step'] for s in steps]
        shears = [s['shear_rads'] for s in steps]
        dists  = [s['hamming_dist'] for s in steps]
        phases = [s['correctable'] for s in steps]

        # Hamming distance bars
        bar_colors = [GREEN_COL if p else RED_COL for p in phases]
        ax.bar(xs, dists, color=bar_colors, alpha=0.7, edgecolor='#333333', label='Hamming Distance')

        # Shear overlay
        ax2 = ax.twinx()
        ax2.plot(xs, shears, color=col, lw=2, marker='o', markersize=6, label='Shear (rads)')
        ax2.set_ylabel('Shear (rads)', color=col, fontsize=9)
        ax2.tick_params(colors=col)

        # Snap line
        snap_step = data['snap_at_step']
        if snap_step:
            ax.axvline(snap_step - 0.5, color=RED_COL, lw=2, linestyle='--', alpha=0.8)
            ax.text(snap_step - 0.4, max(dists) * 0.85, 'LATTICE\nSNAP', color=RED_COL, fontsize=9)

        # Error-correction radius
        ax.axhline(3, color=WHITE, lw=1, linestyle=':', alpha=0.6, label='Golay Radius (d=3)')

        ax.set_xlabel('Heating Step', color=WHITE, fontsize=9)
        ax.set_ylabel('Hamming Distance', color=WHITE, fontsize=9)
        ax.set_title(f'{title}\nSnap @ {data["snap_shear_rads"]:.4f} rads | ΔS = {data["latent_entropy_bits"]:.4f} bits',
                     color=WHITE, fontsize=10)
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.3)

        # Legend
        green_patch = mpatches.Patch(color=GREEN_COL, alpha=0.7, label='Elastic (Correctable)')
        red_patch   = mpatches.Patch(color=RED_COL, alpha=0.7, label='Snapped (Uncorrectable)')
        ax.legend(handles=[green_patch, red_patch], fontsize=8, facecolor='#111111', edgecolor='#333333')

    fig.suptitle('Figure 3: Phase Change as Lattice Snap — Golay Error-Correction Radius',
                 color=WHITE, fontsize=12)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig3_phase_change.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4: Nernst Audit — Iron Stability Plateau
# ─────────────────────────────────────────────────────────────────────────────

def fig4_nernst():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG)

    nernst = R['nernst_audit_iron']
    L      = R['constants']['L_sink']
    k      = R['constants']['k_scale']
    T_base = nernst['T_base_symmetry_tax']
    Cv_min = nernst['Cv_min_specific_heat_floor']

    # Simulate Cv vs temperature (UBP model)
    temps = np.linspace(0.001, 1.0, 500)
    # Classical Debye: Cv ~ T^3 at low T, asymptotes to Dulong-Petit
    cv_classical = 3 * 8.314 * (1 - np.exp(-temps / 0.1))  # Simplified Debye
    cv_classical_norm = cv_classical / cv_classical.max() * (Cv_min * 8)

    # UBP model: Cv has a floor at Cv_min
    cv_ubp = np.maximum(Cv_min, cv_classical_norm)

    ax.plot(temps, cv_classical_norm, color=CYAN, lw=2, linestyle='--',
            label='Classical (Debye, no floor)', alpha=0.7)
    ax.plot(temps, cv_ubp, color=GOLD_COL, lw=2.5,
            label=f'UBP Pantograph (floor = {Cv_min:.4f})')
    ax.axhline(Cv_min, color=RED_COL, lw=1.5, linestyle=':',
               label=f'Nernst Floor Cv_min = {Cv_min:.6f}')
    ax.axhline(L, color=PURPLE, lw=1, linestyle='-.',
               label=f'13D Sink L = {L:.6f}')

    # Falsifiability zone
    ax.fill_between(temps, 0, Cv_min, alpha=0.08, color=RED_COL,
                    label='Forbidden Zone (UBP falsification region)')

    ax.set_xlabel('Temperature (normalised, approaching 0 K)', color=WHITE, fontsize=10)
    ax.set_ylabel('Specific Heat Capacity Cv (J/K-equiv)', color=WHITE, fontsize=10)
    ax.set_title(f'Figure 4: Nernst Audit — Iron (Fe) Stability Plateau\n'
                 f'T_base = {T_base:.4f} bits | Jitter = {nernst["brownian_jitter"]:.6f} units',
                 color=WHITE, fontsize=11)
    ax.legend(fontsize=9, facecolor='#111111', edgecolor='#444444')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, Cv_min * 9)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig4_nernst_iron.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 5: Universal Coupling Constant & Scaling
# ─────────────────────────────────────────────────────────────────────────────

def fig5_coupling():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor(DARK_BG)

    cc = R['universal_coupling_constant']
    survey = R['multi_element_survey']

    # Left: NRCI vs Hamming Weight
    ax = axes[0]
    hw_vals   = [s['hamming_weight'] for s in survey if 'hamming_weight' in s]
    nrci_vals = [s['nrci'] for s in survey if 'nrci' in s]
    names     = [s['element'].split(' ')[0] for s in survey if 'nrci' in s]

    sc = ax.scatter(hw_vals, nrci_vals, c=nrci_vals, cmap='plasma',
                    s=200, zorder=5, edgecolors=WHITE, linewidths=0.7)
    for i, name in enumerate(names):
        ax.annotate(name, (hw_vals[i], nrci_vals[i]),
                    textcoords='offset points', xytext=(5, 3), fontsize=8, color=WHITE)

    ax.axhline(0.70, color=GREEN_COL, lw=1.2, linestyle='--', alpha=0.7, label='Stable Zone (0.70)')
    ax.axhline(0.42, color=RED_COL, lw=1, linestyle=':', alpha=0.7, label='Noise Floor (0.42)')
    plt.colorbar(sc, ax=ax, label='NRCI')
    ax.set_xlabel('Hamming Weight (Internal Energy U)', color=WHITE, fontsize=9)
    ax.set_ylabel('NRCI (Coherence / Max Efficiency)', color=WHITE, fontsize=9)
    ax.set_title('NRCI vs Internal Energy\nAcross Representative Elements', color=WHITE, fontsize=10)
    ax.legend(fontsize=8, facecolor='#111111', edgecolor='#333333')
    ax.grid(True, alpha=0.3)

    # Right: Coupling constant verification
    ax2 = axes[1]
    labels  = ['Hydrogen\n(SSS-PHASE-LOCK)', 'Gold\n(PHASE-LOCK)']
    nrcis   = [cc['hydrogen_verification']['substrate_nrci'],
               cc['gold_verification']['substrate_nrci']]
    errors  = [cc['hydrogen_verification']['error_pct'],
               cc['gold_verification']['error_pct']]
    bar_cols = [GREEN_COL, GOLD_COL]

    bars = ax2.bar(labels, nrcis, color=bar_cols, alpha=0.8, edgecolor='#333333', width=0.4)
    for bar, err in zip(bars, errors):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                 f'err={err:.4f}%', ha='center', va='bottom', fontsize=9, color=WHITE)

    ax2.axhline(0.764677, color=CYAN, lw=1.5, linestyle='--', alpha=0.7,
                label='Target η_H = 0.764677')
    ax2.set_ylim(0, 1.0)
    ax2.set_ylabel('Substrate NRCI', color=WHITE, fontsize=9)
    ax2.set_title(f'Universal Coupling Constant\nC_u = η_H × R_p/e = {cc["C_u_coupling_constant"]:.4f}',
                  color=WHITE, fontsize=10)
    ax2.legend(fontsize=8, facecolor='#111111', edgecolor='#333333')
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Figure 5: Universal Coupling Constant & NRCI Scaling',
                 color=WHITE, fontsize=12)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig5_coupling.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 6: Brownian Motion as Aliasing Jitter
# ─────────────────────────────────────────────────────────────────────────────

def fig6_brownian():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor(DARK_BG)

    W     = R['constants']['W_wobble']
    W_frac = W % 1
    ba    = R['brownian_aliasing']

    # Left: Irrational residue spiral
    ax = axes[0]
    n_pts = 500
    angles = [2 * math.pi * i * W for i in range(n_pts)]
    xs = [math.cos(a) for a in angles]
    ys = [math.sin(a) for a in angles]
    sc = ax.scatter(xs, ys, c=range(n_pts), cmap='plasma', s=8, alpha=0.7)
    ax.set_aspect('equal')
    ax.set_title(f'Triadic Wobble Spiral (W = {W:.8f})\nNo point repeats — Irrational Aliasing',
                 color=WHITE, fontsize=10)
    ax.set_xlabel('cos(2π·i·W)', color=WHITE, fontsize=9)
    ax.set_ylabel('sin(2π·i·W)', color=WHITE, fontsize=9)
    plt.colorbar(sc, ax=ax, label='Step i')
    ax.grid(True, alpha=0.3)

    # Right: Jitter amplitudes per element
    ax2 = axes[1]
    elem_jitter = ba['element_jitter']
    elem_names  = [ej['element'] for ej in elem_jitter]
    jitters     = [ej['brownian_jitter_amplitude'] for ej in elem_jitter]
    t_bases     = [ej['T_base'] for ej in elem_jitter]

    x_pos = np.arange(len(elem_names))
    bars  = ax2.bar(x_pos, jitters, color=[CYAN, '#cc6666', GOLD_COL], alpha=0.85,
                    edgecolor='#333333')
    for bar, tb in zip(bars, t_bases):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                 f'T={tb:.3f}', ha='center', va='bottom', fontsize=9, color=WHITE)

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(elem_names, fontsize=10)
    ax2.set_ylabel('Brownian Jitter Amplitude (units)', color=WHITE, fontsize=9)
    ax2.set_title(f'Brownian Motion = Aliasing Jitter\nW_residue = {W_frac:.8f}',
                  color=WHITE, fontsize=10)
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Figure 6: Brownian Motion as Irrational Aliasing Jitter',
                 color=WHITE, fontsize=12)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig6_brownian.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 7: Multi-Element Survey — Thermodynamic Landscape
# ─────────────────────────────────────────────────────────────────────────────

def fig7_survey():
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(DARK_BG)

    survey = [s for s in R['multi_element_survey'] if 'hamming_weight' in s]
    names  = [s['element'].split(' ')[0] for s in survey]
    shears = [s['shear_tan_theta'] for s in survey]
    nrcis  = [s['nrci'] for s in survey]
    cv_fls = [s['nernst_floor_Cv'] for s in survey]
    phases = [s['phase_state'] for s in survey]

    phase_colors = {'SOLID': CYAN, 'LIQUID': GOLD_COL, 'GAS': RED_COL}
    colors = [phase_colors.get(p, WHITE) for p in phases]

    sc = ax.scatter(shears, nrcis, c=cv_fls, cmap='viridis',
                    s=[c * 1200 for c in cv_fls], alpha=0.85,
                    edgecolors=colors, linewidths=2.5, zorder=5)

    for i, name in enumerate(names):
        ax.annotate(f'{name}\n({phases[i]})', (shears[i], nrcis[i]),
                    textcoords='offset points', xytext=(8, 4), fontsize=8, color=WHITE)

    plt.colorbar(sc, ax=ax, label='Nernst Floor Cv_min (J/K-equiv)')

    ax.axhline(0.70, color=GREEN_COL, lw=1.2, linestyle='--', alpha=0.6, label='Stable Zone (0.70)')
    ax.axvline(0, color=WHITE, lw=0.8, linestyle=':', alpha=0.4)

    # Phase region labels
    ax.text(-0.5, 0.78, 'SOLID\n(Phase-Locked)', color=CYAN, fontsize=9, alpha=0.7)
    ax.text(1.0, 0.73, 'LIQUID\n(Shearing)', color=GOLD_COL, fontsize=9, alpha=0.7)
    ax.text(2.5, 0.67, 'GAS\n(Snapped)', color=RED_COL, fontsize=9, alpha=0.7)

    ax.set_xlabel('Entropy Shear tan(θ) (rads)', color=WHITE, fontsize=10)
    ax.set_ylabel('NRCI (Coherence / Efficiency)', color=WHITE, fontsize=10)
    ax.set_title('Figure 7: UBP Thermodynamic Landscape\n'
                 'Shear vs NRCI — Phase State Mapping Across Elements',
                 color=WHITE, fontsize=11)
    ax.legend(fontsize=9, facecolor='#111111', edgecolor='#444444')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'fig7_survey.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Generating figures...")
    fig1_pantograph()
    fig2_four_laws()
    fig3_phase_change()
    fig4_nernst()
    fig5_coupling()
    fig6_brownian()
    fig7_survey()
    print("All figures generated.")
