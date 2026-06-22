"""
Visualisation: The UBP Computational Cycle — the overall framework.
"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams.update({
    'font.sans-serif': ['DejaVu Sans'],
    'axes.unicode_minus': False,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'figure.dpi': 200,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#FFFFFF',
    'savefig.pad_inches': 0.3,
})

OUT = Path("/home/z/my-project/download/visualisations")

C_BLUE   = '#3B82F6'
C_CYAN   = '#06B6D4'
C_PURPLE = '#8B5CF6'
C_AMBER  = '#F59E0B'
C_RED    = '#EF4444'
C_GREEN  = '#10B981'
C_INDIGO = '#6366F1'
C_TEAL   = '#14B8A6'
G900, G700, G500, G400, G300, G200, G100 = '#111827', '#374151', '#6B7280', '#9CA3AF', '#D1D5DB', '#E5E7EB', '#F3F4F6'

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 8: The UBP Computational Cycle
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(16, 9), constrained_layout=True)

# Draw the cycle as a circular arrangement
# k-values: 0, 3, 6, 9, 12, 15, 18, 21 (8 positions on a circle)
k_values = [0, 3, 6, 9, 12, 15, 18, 21]
n = len(k_values)
angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, n, endpoint=False)
radius = 3.5

# Formula labels at each k-value
formulas_at_k = {
    0: ("Pre-manifest", "(no formula)", G400, ""),
    3: ("α, α_s, H₀", "Couplings emerge", C_GREEN, "det+sto"),
    6: ("m_p/m_e", "Baryon mass", C_BLUE, "det (inv)"),
    9: ("m_τ/m_e", "Heavy lepton", C_CYAN, "det (inv)"),
    12: ("V_ub², α³", "MANIFESTATION PEAK\nWeakest transitions", C_AMBER, "self-pair"),
    15: ("Ω_k", "Curvature", C_PURPLE, "det"),
    18: ("G", "Gravity", C_INDIGO, "det"),
    21: ("n_γ/n_b", "Baryon asymmetry", C_RED, "det"),
}

# Draw the cycle circle
theta_circle = np.linspace(0, 2*np.pi, 100)
ax.plot(radius * np.cos(theta_circle), radius * np.sin(theta_circle),
        '-', color=G300, linewidth=2, zorder=1)

# Draw arrows on the circle (clockwise = forward time)
for i in range(n):
    a1 = angles[i]
    a2 = angles[(i + 1) % n]
    # Midpoint angle for arrow
    am = (a1 + a2) / 2
    if a1 - a2 > np.pi:
        am -= np.pi
    r_arrow = radius
    dx = -0.3 * np.sin(am)
    dy = 0.3 * np.cos(am)
    ax.annotate('', xy=(r_arrow * np.cos(a2) + dx, r_arrow * np.sin(a2) + dy),
                xytext=(r_arrow * np.cos(a1) - dx, r_arrow * np.sin(a1) - dy),
                arrowprops=dict(arrowstyle='->', color=G400, lw=1.5,
                               connectionstyle='arc3,rad=0.2'))

# Draw bit-inversion connections (diameter lines)
bit_inv_pairs = [(3, 21), (6, 18), (9, 15)]
bit_inv_colors = [C_GREEN, C_BLUE, C_CYAN]
bit_inv_labels = ['k=3↔21', 'k=6↔18', 'k=9↔15']

for (k1, k2), color, label in zip(bit_inv_pairs, bit_inv_colors, bit_inv_labels):
    i1 = k_values.index(k1)
    i2 = k_values.index(k2)
    a1 = angles[i1]
    a2 = angles[i2]
    ax.plot([radius * np.cos(a1), radius * np.cos(a2)],
            [radius * np.sin(a1), radius * np.sin(a2)],
            '--', color=color, linewidth=1.5, alpha=0.5, zorder=2)
    # Label at midpoint
    mx = (radius * np.cos(a1) + radius * np.cos(a2)) / 2
    my = (radius * np.sin(a1) + radius * np.sin(a2)) / 2
    ax.text(mx * 0.4, my * 0.4, label, ha='center', va='center', fontsize=7,
            color=color, fontweight='bold', alpha=0.7)

# Self-pairing at k=12
ax.plot(0, 0, 'o', color=C_AMBER, markersize=10, zorder=5)
ax.text(0, -0.3, 'k=12\n(self)', ha='center', fontsize=8, color=C_AMBER, fontweight='bold')

# Draw each k-position
for i, k in enumerate(k_values):
    x = radius * np.cos(angles[i])
    y = radius * np.sin(angles[i])
    label, desc, color, arm = formulas_at_k[k]

    # Circle for the position
    circle_size = 800 if k == 12 else 500
    ax.scatter(x, y, s=circle_size, color=color, edgecolors='white', linewidth=2, zorder=4)

    # Label (outside the circle)
    offset_x = 1.3 * np.cos(angles[i])
    offset_y = 1.3 * np.sin(angles[i])
    text_x = x + offset_x
    text_y = y + offset_y

    # Bold formula name
    ax.text(text_x, text_y + 0.15, f'k={k}: {label}',
            ha='center', va='center', fontsize=10, fontweight='bold', color=color)
    # Description
    ax.text(text_x, text_y - 0.2, desc,
            ha='center', va='center', fontsize=8, color=G700)

    # Arm label (inside, near the position)
    if arm:
        ax.text(x * 0.7, y * 0.7, arm, ha='center', va='center', fontsize=6, color=G500, style='italic')

# Add the w-based formulas as "external input"
ax.annotate('w-based (stochastic):\nm_μ/m_e = 169/w\nH₀ = ⅓·w·Y³·U_e',
            xy=(-radius - 0.5, 0), fontsize=9, ha='center', color=C_RED,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF2F2', edgecolor=C_RED, alpha=0.9))

# Arrow from w to the cycle
ax.annotate('', xy=(-radius * 0.9, 0), xytext=(-radius - 0.3, 0),
            arrowprops=dict(arrowstyle='->', color=C_RED, lw=2))

# Add the center labels
ax.text(0, 0.5, 'UBP\nSubstrate', ha='center', va='center', fontsize=10,
        fontweight='bold', color=G500)

# Title and annotations
ax.set_title('The UBP Substrate as a Computational Cycle\n'
             'Clock: Y^k (step = 3 = Triad) | Input: w (Entropic Wobble) | Mirror: k ↔ (24−k)',
             fontsize=14, fontweight='bold', pad=15)

# Bottom annotations
ax.text(0, -radius - 1.5,
        'Top half (k=0→12): MANIFESTATION phase — Reality grows (Y_inv^k), constants get larger\n'
        'Bottom half (k=12→24): POTENTIAL phase — Potential decays (Y^(24−k)), constants get smaller\n'
        'k=12: Manifestation peak — self-pairing, weakest transitions (V_ub², α³)',
        ha='center', fontsize=9, color=G700, linespacing=1.5)

# Friction and cooling annotations
ax.text(radius + 1.5, radius * 0.5,
        'FRICTION (Topological Shear):\n1 + 3·(L·Y) + 12·(L·Y)²\n'
        'Coefficients: 1 (observer), 3 (Triad), 12 (Leech/2)',
        fontsize=8, color=C_INDIGO, va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#EEF2FF', edgecolor=C_INDIGO, alpha=0.8))

ax.text(radius + 1.5, -radius * 0.5,
        'COOLING (Symmetry Tax Rebate):\nNRCI(α) = 10/(10 + α·tax)\n'
        'α = target\'s UBP concept:\n  1/8 (cosmo), 2 (baryon), 13 (CKM)',
        fontsize=8, color=C_PURPLE, va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F3FF', edgecolor=C_PURPLE, alpha=0.8))

ax.set_xlim(-radius - 2.5, radius + 3.5)
ax.set_ylim(-radius - 2, radius + 1.5)
ax.set_aspect('equal')
ax.axis('off')

plt.savefig(OUT / '08_computational_cycle.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 8: UBP Computational Cycle")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 9: The Generator Function — all 8 formulas as instances of Φ
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6), constrained_layout=True)

# Table-like layout
headers = ['Target', 'k', 'Arm', 'Layer', 'C', 'Correction', 'Error %']
data = [
    ('m_μ/m_e', '1', 'stochastic', 'w-source', '169', 'none', '0.029'),
    ('α_s', '4', 'deterministic', 'Information', '24', 'none', '0.188'),
    ('m_W', '4', 'det (cross)', 'Cross-layer', '13/L·24·π', 'shear₁', '0.094'),
    ('Ω_k', '15', 'deterministic', 'Potential', '24', 'NRCI(1/8)', '0.035'),
    ('n_γ/n_b', '21', 'deterministic', 'Potential', '1/4', 'shear₂+NRCI(2)', '0.055'),
    ('V_ub²', '12', 'deterministic', 'Potential (self)', '1/24', 'NRCI(13)', '0.032'),
    ('α³', '12', 'deterministic', 'Potential (self)', '29/24', 'none (uses e)', '0.104'),
    ('H₀', '3', 'stochastic', 'w-based', '1/3', 'none', '0.495'),
]

colors = [C_RED, C_GREEN, C_INDIGO, C_PURPLE, C_TEAL, C_AMBER, C_GREEN, C_RED]

# Draw header
for j, h in enumerate(headers):
    ax.text(j, len(data), h, ha='center', va='center', fontsize=10, fontweight='bold', color=G700)

# Draw data rows
for i, (row, color) in enumerate(zip(data, colors)):
    y = len(data) - 1 - i
    for j, val in enumerate(row):
        weight = 'bold' if j == 0 else 'normal'
        ax.text(j, y, val, ha='center', va='center', fontsize=9, color=color if j == 0 else G900,
                fontweight=weight)
    # Row background
    ax.fill_between([-0.5, len(headers) - 0.5], y - 0.4, y + 0.4, color=color, alpha=0.05)

# Bottom: the generator function
ax.text(len(headers) / 2 - 0.5, -1.5,
        'Φ(k, arm, layer, C, correction) = C × Base(k, arm, layer) × Correction(correction)',
        ha='center', fontsize=11, fontweight='bold', color=G900,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', edgecolor=G300))

ax.set_xlim(-0.5, len(headers) - 0.5)
ax.set_ylim(-2.5, len(data) + 0.8)
ax.axis('off')
ax.set_title('The UBP Generator Function: All 8 Formulas as Instances of Φ',
             fontsize=14, fontweight='bold', pad=15)

plt.savefig(OUT / '09_generator_function.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 9: Generator Function")

print(f"\nAll charts saved to {OUT}/")
for f in sorted(os.listdir(OUT)):
    print(f"  {f}")
