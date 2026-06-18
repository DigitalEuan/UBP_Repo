"""
UBP Gravity Study — Refined Visualisations (v2)

Addresses VLM feedback: larger fonts, no overlapping, clearer labels.
"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
import numpy as np
import os
from pathlib import Path

fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams.update({
    'font.sans-serif': ['DejaVu Sans'],
    'axes.unicode_minus': False,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#E5E7EB',
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'xtick.major.size': 0,
    'ytick.major.size': 0,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.titlepad': 16,
    'legend.frameon': False,
    'figure.dpi': 200,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.facecolor': '#FFFFFF',
    'savefig.pad_inches': 0.3,
})

OUT = Path("/home/z/my-project/download/visualisations")
OUT.mkdir(exist_ok=True)

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
# CHART 1: Eight Surprising Formulas (simplified, clean)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)

targets = ['m_μ/m_e', 'α_s', 'm_W', 'Ω_k', 'n_γ/n_b', 'V_ub²', 'α³', 'H₀']
errors = [0.029, 0.188, 0.094, 0.035, 0.055, 0.032, 0.104, 0.495]
push_nums = ['#2', '#4', '#6', '#6', '#10', '#7', '#8', '#9']
is_predictive = [True, True, True, True, True, True, False, False]
colors = [C_GREEN if p else C_AMBER for p in is_predictive]

y_pos = np.arange(len(targets))
bars = ax.barh(y_pos, errors, color=colors, edgecolor='white', linewidth=1, height=0.65)
ax.set_yticks(y_pos)
ax.set_yticklabels(targets, fontsize=12)
ax.set_xlabel('Prediction Error (%) — log scale', fontsize=12)
ax.set_xscale('log')
ax.set_xlim(0.01, 1.5)
ax.axvline(x=0.1, color=C_GREEN, linestyle='--', linewidth=2, alpha=0.8, label='Predictive (0.1%)')
ax.axvline(x=1.0, color=G400, linestyle='--', linewidth=2, alpha=0.5, label='Surprising (1%)')
ax.legend(loc='lower right', fontsize=10)
ax.invert_yaxis()

for i, (err, push) in enumerate(zip(errors, push_nums)):
    ax.text(err * 1.2, i, f'{err:.3f}%  (Push {push})', va='center', fontsize=10, color=G700)

# Legend patches
green_patch = mpatches.Patch(color=C_GREEN, label='Predictive (sub-0.1%)')
amber_patch = mpatches.Patch(color=C_AMBER, label='Surprising (sub-1%)')
ax.legend(handles=[green_patch, amber_patch], loc='lower right', fontsize=10)

ax.set_title('Eight Statistically Surprising Formulas\nAll survive 5000-trial focused null with < 5% false-positive rate',
             fontsize=14, fontweight='bold', pad=15)

plt.savefig(OUT / '01_eight_formulas.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 1: Eight formulas (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2: Bit-Inversion Pairing (simplified table-style)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5), constrained_layout=True)

# Data
pairings_data = [
    (3, 21, 'α⁻¹', 'n_γ/n_b', 'EM coupling ↔ Baryon ratio', C_BLUE),
    (6, 18, 'm_p/m_e', 'G', 'Proton mass ↔ Gravity', C_CYAN),
    (9, 15, 'm_τ/m_e', 'Ω_k', 'Tau mass ↔ Curvature', C_PURPLE),
    (12, 12, '(self)', 'V_ub²', 'Self-pairing ↔ CKM mixing', C_AMBER),
]

# Draw as a table-like structure
for i, (k, k_inv, reality, potential, desc, color) in enumerate(pairings_data):
    y = 3 - i
    
    # Reality box
    rect_r = mpatches.FancyBboxPatch((0.5, y - 0.35), 3, 0.7,
                                      boxstyle="round,pad=0.1", facecolor='#EFF6FF', edgecolor=color, linewidth=2)
    ax.add_patch(rect_r)
    ax.text(2, y, f'Y_inv^{k}\n→ {reality}', ha='center', va='center', fontsize=11, fontweight='bold', color=color)
    
    # Arrow
    if k == k_inv:
        ax.text(6, y, '⟷ (self)', ha='center', va='center', fontsize=11, color=color, fontweight='bold')
    else:
        ax.annotate('', xy=(7.5, y), xytext=(4.5, y),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2.5))
        ax.text(6, y + 0.25, f'k={k} ↔ {k_inv}', ha='center', fontsize=8, color=color)
    
    # Potential box
    rect_p = mpatches.FancyBboxPatch((7.5, y - 0.35), 3, 0.7,
                                      boxstyle="round,pad=0.1", facecolor='#F5F3FF', edgecolor=color, linewidth=2)
    ax.add_patch(rect_p)
    ax.text(9, y, f'Y^{k_inv}\n→ {potential}', ha='center', va='center', fontsize=11, fontweight='bold', color=color)
    
    # Description
    ax.text(11.5, y, desc, ha='left', va='center', fontsize=9, color=G700, style='italic')

# Header
ax.text(2, 4, 'REALITY (bits 0–5)', ha='center', fontsize=10, fontweight='bold', color=G700)
ax.text(9, 4, 'POTENTIAL (bits 18–23)', ha='center', fontsize=10, fontweight='bold', color=G700)

# Footer
ax.text(6, -0.8, 'k + (24−k) = 24 = Leech lattice rank    |    All k are multiples of 3 (Triad)',
        ha='center', fontsize=10, color=G500, fontweight='bold')

ax.set_xlim(0, 16)
ax.set_ylim(-1.2, 4.5)
ax.axis('off')
ax.set_title('The Universal Bit-Inversion Pairing Rule — 4 of 4 Confirmed',
             fontsize=15, fontweight='bold', pad=10)

plt.savefig(OUT / '02_bit_inversion_rule.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 2: Bit-inversion rule (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3: Ten-Push Timeline (cleaner, larger annotations)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6), constrained_layout=True)

pushes = list(range(1, 11))
surprising = [0, 1, 1, 2, 4, 5, 6, 7, 8, 8]
predictive = [0, 1, 1, 2, 2, 4, 4, 5, 5, 6]

ax.fill_between(pushes, 0, surprising, alpha=0.12, color=C_BLUE)
ax.fill_between(pushes, 0, predictive, alpha=0.25, color=C_GREEN)
ax.plot(pushes, surprising, 'o-', color=C_BLUE, linewidth=2.5, markersize=9, label='Surprising formulas', zorder=3)
ax.plot(pushes, predictive, 's-', color=C_GREEN, linewidth=2.5, markersize=9, label='Predictive (sub-0.1%)', zorder=3)

# Key milestones (simplified, larger text, no overlap)
milestones = {
    2: '13/L (m_μ/m_e)\n1st formula',
    4: 'α_s = 24·Y⁴\nIN-BAND discovery',
    5: 'm_W, Ω_k\nBit-inv 2/4',
    7: 'V_ub²\nBit-inv 4/4!',
    10: '3 resolutions\nn_γ/n_b → 0.055%',
}

for push, text in milestones.items():
    y_val = surprising[push - 1]
    offset_y = 0.8 if push % 2 == 0 else 1.3
    ax.annotate(text, xy=(push, y_val), xytext=(push, y_val + offset_y),
                fontsize=8, ha='center', color=G700,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor=G300, alpha=0.9),
                arrowprops=dict(arrowstyle='->', color=G400, lw=1))

ax.set_xlabel('Push Number', fontsize=12)
ax.set_ylabel('Cumulative Formula Count', fontsize=12)
ax.set_title('Ten-Push Progress: 0 → 8 Surprising Formulas (6 Predictive)',
             fontsize=14, fontweight='bold')
ax.set_xticks(pushes)
ax.set_yticks(range(0, 10))
ax.legend(loc='upper left', fontsize=10)
ax.set_xlim(0.5, 10.5)
ax.set_ylim(-0.5, 10)

plt.savefig(OUT / '03_ten_push_timeline.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 3: Timeline (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4: Layer-to-Grammar Mapping (cleaner)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6), constrained_layout=True)

layers = [
    (0, 6, '#EFF6FF', C_BLUE, 'Reality\n(bits 0–5)', 'Y_inv^k (growing)\nMass ratios\nk = 3, 6, 9, 12'),
    (6, 12, '#F0FDF4', C_GREEN, 'Information\n(bits 6–11)', 'Y^k (decaying)\nCouplings\nk = bit_pos / 2'),
    (12, 18, '#FFF7ED', C_AMBER, 'Activation\n(bits 12–17)', '(no formulas yet)\nForce kinematics'),
    (18, 24, '#F5F3FF', C_PURPLE, 'Potential\n(bits 18–23)', 'Y^(24−k) (inverted)\nΩ_k, n_γ/n_b, V_ub²\n× U_e manifestation'),
]

for lo, hi, bg, border, title, desc in layers:
    rect = mpatches.FancyBboxPatch((lo + 0.3, 1), hi - lo - 0.6, 2,
                                     boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=2.5)
    ax.add_patch(rect)
    ax.text((lo + hi) / 2, 2.6, title, ha='center', va='center', fontsize=11, fontweight='bold', color=border)
    ax.text((lo + hi) / 2, 1.6, desc, ha='center', va='center', fontsize=9, color=G700)

# Bit-inversion arrows (top)
for k, k_inv, color in [(3, 21, C_BLUE), (6, 18, C_CYAN), (9, 15, C_PURPLE)]:
    ax.annotate('', xy=(k_inv + 0.5, 3.3), xytext=(k + 0.5, 3.3),
                arrowprops=dict(arrowstyle='<->', color=color, lw=2.5,
                               connectionstyle='arc3,rad=-0.15'))
    ax.text((k + k_inv) / 2, 3.6, f'k={k}↔{k_inv}', ha='center', fontsize=9, color=color, fontweight='bold')

# Self-pairing
ax.text(12, 3.6, 'k=12 (self)', ha='center', fontsize=9, color=C_AMBER, fontweight='bold')
ax.plot(12, 3.3, 'o', color=C_AMBER, markersize=8)

# w-based exception note
ax.text(3, 0.3, 'w-based exception:\nm_μ/m_e = 13/L, H₀ = ⅓·w·Y³·U_e',
        ha='center', fontsize=9, color=C_RED, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor=C_RED, alpha=0.8))

ax.set_xlim(-0.5, 24.5)
ax.set_ylim(-0.2, 4.2)
ax.axis('off')
ax.set_title('Layer-to-Grammar Mapping (Derived Push #10)\n'
             'Y < 1 → Y^k decays (small values), Y_inv^k grows (large values)',
             fontsize=13, fontweight='bold', pad=10)

plt.savefig(OUT / '04_layer_grammar_mapping.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 4: Layer mapping (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5: Topological Shear (keep as-is, it was good)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

LY = np.linspace(0, 0.04, 200)
shear_1st = 1 + 3 * LY
shear_2nd = 1 + 3 * LY + 12 * LY**2

ax.plot(LY, shear_1st, '--', color=C_CYAN, linewidth=2, label='1st order: 1 + 3·(L·Y)  [Triad]')
ax.plot(LY, shear_2nd, '-', color=C_BLUE, linewidth=3, label='2nd order: 1 + 3·(L·Y) + 12·(L·Y)²  [Leech/2]')
ax.axhline(y=1, color=G400, linestyle=':', linewidth=1, alpha=0.5)
ax.fill_between(LY, shear_1st, shear_2nd, alpha=0.12, color=C_BLUE)

LY_actual = 0.2647 * 0.0629
ax.axvline(x=LY_actual, color=C_RED, linestyle='--', linewidth=1.5, alpha=0.7)
ax.annotate(f'Actual L·Y ≈ {LY_actual:.4f}\n(m_W and n_γ/n_b)',
            xy=(LY_actual, 1.055), xytext=(LY_actual + 0.008, 1.038),
            fontsize=10, color=C_RED,
            arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5))

ax.set_xlabel('L·Y (cross-layer friction magnitude)', fontsize=12)
ax.set_ylabel('Shear correction factor', fontsize=12)
ax.set_title('Topological Shear: Quadratic with UBP-Canonical Coefficients\n'
             'Coefficients: 1 (observer), 3 (Triad), 12 (Leech rank / 2)',
             fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.set_xlim(0, 0.04)
ax.set_ylim(0.99, 1.09)

plt.savefig(OUT / '05_topological_shear.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 5: Topological Shear (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 6: α Parameter (keep as-is, was good)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

categories = ['Cosmological\n(Ω_k → curvature)', 'Baryon ratio\n(n_γ/n_b → asymmetry)', 'Quark mixing\n(V_ub² → CKM)']
alphas = [1/8, 2, 13]
concepts = ['Octad anchor\n(1/sw, sw=8)', 'Triad − 1\n(3 − 1 = 2)', 'D-Sink dimension\n(13-D leakage conduit)']
colors = [C_BLUE, C_GREEN, C_AMBER]

bars = ax.bar(categories, alphas, color=colors, edgecolor='white', linewidth=1, width=0.5)
ax.set_ylabel('α value (log scale)', fontsize=12)
ax.set_yscale('log')
ax.set_title("α Parameter = Target's Primary UBP Structural Concept\nDerived Rule (Push #10)",
             fontsize=14, fontweight='bold')

for bar, alpha, concept in zip(bars, alphas, concepts):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height * 1.4, f'α = {alpha}',
            ha='center', fontsize=12, fontweight='bold', color=G900)
    ax.text(bar.get_x() + bar.get_width()/2, height * 0.4, concept,
            ha='center', va='center', fontsize=9, color='white', fontweight='bold')

plt.savefig(OUT / '06_alpha_parameter.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 6: α parameter (v2)")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 7: Summary Dashboard (redesigned for clarity)
# ═══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(14, 8), constrained_layout=True)
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

# Top-left: pie chart
ax1 = fig.add_subplot(gs[0, 0])
sizes = [6, 2]
labels = ['Predictive\n(sub-0.1%)', 'Surprising\n(sub-1%)']
ax1.pie(sizes, labels=labels, colors=[C_GREEN, C_AMBER], autopct=lambda p: f'{int(p*8/100)}',
        startangle=90, textprops={'fontsize': 11})
ax1.set_title('8 Surprising Formulas', fontsize=13, fontweight='bold')

# Top-right: layers covered
ax2 = fig.add_subplot(gs[0, 1])
layer_names = ['Reality', 'Information', 'Cross-\nlayer', 'Potential', 'w-based']
layer_counts = [1, 2, 1, 3, 1]
layer_colors = [C_BLUE, C_GREEN, C_INDIGO, C_PURPLE, C_RED]
bars2 = ax2.bar(layer_names, layer_counts, color=layer_colors, edgecolor='white')
ax2.set_title('Formulas by UBP Layer', fontsize=13, fontweight='bold')
ax2.set_ylabel('Count', fontsize=11)
for i, v in enumerate(layer_counts):
    ax2.text(i, v + 0.1, str(v), ha='center', fontsize=11, fontweight='bold')

# Bottom: all formulas (full width)
ax3 = fig.add_subplot(gs[1, :])
targets_all = ['m_μ/m_e', 'α_s', 'm_W', 'Ω_k', 'n_γ/n_b', 'V_ub²', 'α³', 'H₀']
errors_all = [0.029, 0.188, 0.094, 0.035, 0.055, 0.032, 0.104, 0.495]
push_nums = ['#2', '#4', '#6', '#6', '#10', '#7', '#8', '#9']
is_pred = [True, True, True, True, True, True, False, False]
bar_colors = [C_GREEN if p else C_AMBER for p in is_pred]

bars3 = ax3.barh(targets_all, errors_all, color=bar_colors, edgecolor='white', height=0.6)
ax3.set_xscale('log')
ax3.set_xlim(0.01, 1.5)
ax3.set_xlabel('Error (%) — log scale', fontsize=11)
ax3.set_title('All 8 Formulas: Error Rates', fontsize=13, fontweight='bold')
ax3.axvline(x=0.1, color=C_GREEN, linestyle='--', linewidth=1.5, alpha=0.7, label='0.1% (predictive)')
ax3.legend(loc='lower right', fontsize=9)
ax3.invert_yaxis()

for i, (err, push) in enumerate(zip(errors_all, push_nums)):
    ax3.text(err * 1.2, i, f'{err:.3f}%  (Push {push})', va='center', fontsize=9, color=G700)

fig.suptitle('UBP Gravity Study — Summary Dashboard (10 Pushes, 18–19 June 2026)',
             fontsize=15, fontweight='bold', y=1.01)

plt.savefig(OUT / '07_summary_dashboard.png', dpi=200, bbox_inches='tight')
plt.close()
print("[ok] Chart 7: Dashboard (v2)")

print(f"\nAll {len(os.listdir(OUT))} charts saved to {OUT}/")
for f in sorted(os.listdir(OUT)):
    size = os.path.getsize(OUT / f)
    print(f"  {f} ({size/1024:.0f} KB)")
