"""
Visualization: The fully realized UBP Cycle as a closed 4×3 = 12 formal system.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
from pathlib import Path

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.size": 10,
})

OUT = Path("/home/z/my-project/download/figures/deep_dive")
OUT.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Figure: The 4×3 = 12 Closed Cycle
# ══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(16, 12), constrained_layout=True)
ax.set_aspect('equal')

# 4 layers (rows) × 3 functions (columns) = 12 components
layers = [
    ("Layer 1: REALITY\n(bits 0-5)",     '#E3F2FD', '#1565C0', 
     [("INPUT", "w → state"), ("OBSERVER", "trigger clock"), ("CLOCK", "k → k+3")]),
    ("Layer 2: INFORMATION\n(bits 6-11)", '#E8F5E9', '#2E7D32',
     [("MIRROR", "k ↔ 24-k"), ("FRICTION", "× Shear"), ("DUALITY", "Shear ↔ Shear⁻¹")]),
    ("Layer 3: ACTIVATION\n(bits 12-17)", '#FFF4E5', '#E59400',
     [("COOLING", "× NRCI(α)"), ("LAYER-CROSSING", "Shear+NRCI"), ("MANIFESTATION", "NRCI ≥ 0.70?")]),
    ("Layer 4: POTENTIAL\n(bits 18-23)", '#F3E5F5', '#6A1B9A',
     [("SELF-VALIDATION", "IN-BAND?"), ("OUTPUT", "→ constant"), ("RECURSION", "→ input")]),
]

functions = ["WHEN\n(timing)", "HOW\n(correction)", "WHAT\n(extraction)"]

# Grid positions
x_start = 2.5
y_start = 4.0
cell_w = 3.0
cell_h = 1.4
row_gap = 0.3

# Draw function headers (columns)
for j, func in enumerate(functions):
    x = x_start + j * cell_w
    box = FancyBboxPatch((x, y_start + 4 * (cell_h + row_gap) + 0.2), cell_w, 0.6,
                         boxstyle="round,pad=0.1", facecolor='#1F4E79', edgecolor='#1F4E79', linewidth=2)
    ax.add_patch(box)
    ax.text(x + cell_w/2, y_start + 4 * (cell_h + row_gap) + 0.5, func,
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# Draw layer labels (rows) and component cells
for i, (layer_name, bg_color, edge_color, comps) in enumerate(layers):
    y = y_start + (3 - i) * (cell_h + row_gap)
    
    # Layer label
    box = FancyBboxPatch((0, y), 2.3, cell_h,
                         boxstyle="round,pad=0.1", facecolor=edge_color, edgecolor=edge_color, linewidth=2)
    ax.add_patch(box)
    ax.text(1.15, y + cell_h/2, layer_name,
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Component cells
    for j, (comp_name, comp_desc) in enumerate(comps):
        x = x_start + j * cell_w
        box = FancyBboxPatch((x, y), cell_w, cell_h,
                             boxstyle="round,pad=0.1", facecolor=bg_color, edgecolor=edge_color, linewidth=2)
        ax.add_patch(box)
        ax.text(x + cell_w/2, y + cell_h * 0.65, comp_name,
                ha='center', va='center', fontsize=11, fontweight='bold', color=edge_color)
        ax.text(x + cell_w/2, y + cell_h * 0.30, comp_desc,
                ha='center', va='center', fontsize=8, color='#333', style='italic')

# Draw arrows showing the cycle flow
# Within each row: left to right
for i in range(4):
    y = y_start + (3 - i) * (cell_h + row_gap) + cell_h / 2
    for j in range(2):
        x1 = x_start + j * cell_w + cell_w
        x2 = x_start + (j + 1) * cell_w
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='#1F4E79', lw=2))

# Between rows: rightmost of row i → leftmost of row i+1 (spiral)
for i in range(3):
    y1 = y_start + (3 - i) * (cell_h + row_gap) + cell_h / 2
    y2 = y_start + (3 - i - 1) * (cell_h + row_gap) + cell_h / 2
    x1 = x_start + 2 * cell_w  # rightmost
    x2 = x_start  # leftmost of next row
    # Draw a curved arrow
    ax.annotate('', xy=(x2 + cell_w/2, y2 + cell_h), xytext=(x1 + cell_w/2, y1),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2.5,
                                connectionstyle='arc3,rad=-0.3'))

# Recursion arrow: from RECURSION (bottom-right) back to INPUT (top-left)
y_rec = y_start + 0 * (cell_h + row_gap) + cell_h / 2
x_rec = x_start + 2 * cell_w + cell_w / 2
y_in = y_start + 3 * (cell_h + row_gap) + cell_h / 2
x_in = x_start + 0 * cell_w + cell_w / 2
ax.annotate('', xy=(x_in, y_in + cell_h * 0.7), xytext=(x_rec, y_rec - cell_h * 0.3),
            arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=3, linestyle='--',
                            connectionstyle='arc3,rad=0.4'))
ax.text(0.5, y_start + 2 * (cell_h + row_gap), "RECURSION\n(feedback)",
        ha='center', va='center', fontsize=10, fontweight='bold', color='#6A1B9A',
        style='italic', rotation=90)

# Title and formal definition
ax.text(x_start + 1.5 * cell_w, y_start + 4 * (cell_h + row_gap) + 1.2,
        "The UBP Cycle: Fully Realized as (S, G, M, Φ)",
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1F4E79')

ax.text(x_start + 1.5 * cell_w, y_start + 4 * (cell_h + row_gap) + 0.8,
        "4 layers × 3 functions = 12 components — CLOSED at 12 (no 13th needed)",
        ha='center', va='center', fontsize=11, color='#333', style='italic')

# Bottom: closure properties
closure_text = (
    "CLOSURE PROPERTIES:\n"
    "(1) Group: D8 x Z2 (order 32)  (2) Monad: (T, eta, mu) laws satisfied  (3) Combinatorial: 4x3=12 complete\n"
    "(4) Algebraic: product of 4 monoids  (5) Self-referential: RECURSION closes the loop"
)
ax.text(x_start + 1.5 * cell_w, -0.8, closure_text,
        ha='center', va='center', fontsize=9, color='#1F4E79',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F5F7FA', edgecolor='#1F4E79', linewidth=1.5))

ax.set_xlim(-0.5, x_start + 3 * cell_w + 0.5)
ax.set_ylim(-1.5, y_start + 4 * (cell_h + row_gap) + 1.8)
ax.axis('off')

plt.savefig(OUT / "formalized_cycle_4x3.png", dpi=200, bbox_inches='tight', pad_inches=0.15)
plt.close()
print(f"[ok] Figure saved: {OUT / 'formalized_cycle_4x3.png'}")
