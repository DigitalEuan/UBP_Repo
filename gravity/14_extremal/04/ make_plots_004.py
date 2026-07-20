"""Generate plots for EXTREMAL_004 deck."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'

OUT = '/home/z/my-project/download/slides'
os.makedirs(OUT, exist_ok=True)

BG = '#0E1116'
FG = '#E6E6E6'
AMBER = '#FFB454'
TEAL = '#6FE3D2'
VIOLET = '#B097FF'
RED = '#FF6B6B'

# --- Plot 6: Vacuum basin (Thread E) ---
basin = json.load(open('/home/z/my-project/work/basin_results.json'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=BG, constrained_layout=True,
                                gridspec_kw={'width_ratios': [1, 1.3]})

# Left: basin composition
ax1.set_facecolor(BG)
labels = ['HW=0\n(zero itself)', 'HW=1', 'HW=2', 'HW=3', 'HW=4\n(uncorrectable)']
sizes = [1, 24, 276, 2024, 10626]
colors = [TEAL, TEAL, TEAL, TEAL, RED]
bars = ax1.bar(labels, sizes, color=colors, edgecolor=FG, linewidth=0.6)
for b, c in zip(bars, sizes):
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 200,
             f'{c:,}', ha='center', va='bottom', color=FG, fontsize=9)
ax1.set_ylabel('Number of vectors', color=FG)
ax1.set_title('Vacuum basin = perfect ball (HW \u2264 3) = 2,325 vectors', color=FG, fontsize=11, pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_color(FG)
ax1.grid(True, alpha=0.15, color=FG, axis='y')
ax1.set_ylim(0, 12500)

# Right: HW=4 syndrome weight distribution
ax2.set_facecolor(BG)
syn_w = basin['hw4_syndrome_hist']
xs = sorted([int(k) for k in syn_w.keys()])
ys = [syn_w[str(x)] for x in xs]
ax2.bar([str(x) for x in xs], ys, color=AMBER, edgecolor=FG, linewidth=0.6)
for x, y in zip([str(x) for x in xs], ys):
    ax2.text(x, y + 80, f'{y:,}', ha='center', va='bottom', color=FG, fontsize=9)
# Vertical line at t=3 (correction capability)
ax2.axvline(x=1.5, color=RED, linestyle='--', linewidth=1.2, alpha=0.7)
ax2.text(1.7, max(ys) * 0.9, 't = 3\n(correction\nlimit)', color=RED, fontsize=9)
ax2.set_xlabel('syndrome weight of HW=4 vectors', color=FG)
ax2.set_ylabel('count', color=FG)
ax2.set_title('All HW=4 vectors have SynW > 3 \u2192 all uncorrectable', color=FG, fontsize=11, pad=10)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_color(FG)
ax2.grid(True, alpha=0.15, color=FG, axis='y')
ax2.set_ylim(0, max(ys) * 1.15)
plt.savefig(f'{OUT}/fig6_basin.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig6_basin.png')

# --- Plot 7: [24,12,8] sampling (Thread F) ---
golay24 = json.load(open('/home/z/my-project/work/golay24_results.json'))
results = golay24['results']
fig, ax = plt.subplots(figsize=(9, 4.2), facecolor=BG, constrained_layout=True)
ax.set_facecolor(BG)
names = [r['name'] for r in results]
aps = [r['avg_phi_mc'] for r in results]
dmins = [r['d_min'] for r in results]
colors_b = [AMBER] + [TEAL] * 4
bars = ax.bar(range(len(names)), aps, color=colors_b, edgecolor=FG, linewidth=0.6)
for b, v, d in zip(bars, aps, dmins):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.002,
            f'{v:.4f}\nd={d}', ha='center', va='bottom', color=FG, fontsize=9)
ax.set_xticks(range(len(names)))
ax.set_xticklabels(names, rotation=20, ha='right', color=FG)
ax.set_ylabel('avg \u03A6 (Monte Carlo, 15k samples)', color=FG)
ax.set_title('[24,12,8] codes: Golay vs 4 random [24,12] codes', color=FG, fontsize=12, pad=10)
ax.tick_params(colors=FG)
ax.set_ylim(min(aps) - 0.025, max(aps) + 0.04)
for spine in ax.spines.values(): spine.set_color(FG)
ax.grid(True, alpha=0.15, color=FG, axis='y')
ax.annotate('', xy=(0, aps[0]), xytext=(2, aps[1]),
            arrowprops=dict(arrowstyle='<->', color=FG, lw=0.8))
ax.text(1, (aps[0] + aps[1]) / 2 + 0.005, f'  +{aps[0] - aps[1]:.4f}', color=FG, fontsize=10)
plt.savefig(f'{OUT}/fig7_golay24.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig7_golay24.png')

# --- Plot 8: [16,8] qualified self-dual test (Thread H) ---
sd16 = json.load(open('/home/z/my-project/work/self_dual16_results.json'))
records = sd16['records']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=BG, constrained_layout=True,
                                gridspec_kw={'width_ratios': [1.2, 1]})

# Left: scatter of avg_Phi vs d_min, color by self_dual
ax1.set_facecolor(BG)
nsd = [(r['d_min'], r['avg_phi']) for r in records if not r['self_dual']]
sd  = [(r['d_min'], r['avg_phi']) for r in records if r['self_dual']]
if nsd:
    ax1.scatter([x[0] for x in nsd], [x[1] for x in nsd], c=TEAL, s=36, alpha=0.6,
                edgecolor=FG, linewidth=0.4, label=f'non-self-dual (n={len(nsd)})')
if sd:
    ax1.scatter([x[0] for x in sd], [x[1] for x in sd], c=AMBER, s=180, marker='*',
                edgecolor=FG, linewidth=1.0, label=f'self-dual (n={len(sd)})', zorder=10)
ax1.set_xlabel('d_min', color=FG)
ax1.set_ylabel('avg \u03A6 (Monte Carlo, 10k samples)', color=FG)
ax1.set_title('[16,8] codes: avg \u03A6 vs d_min', color=FG, fontsize=11, pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_color(FG)
ax1.grid(True, alpha=0.15, color=FG)
ax1.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='lower right', fontsize=9)

# Right: focus on d=4 codes only -- the qualified comparison
ax2.set_facecolor(BG)
d4_recs = [r for r in records if r['d_min'] == 4]
d4_names = [r['name'].replace('Random[16,8]#', 'R#').replace('E8+E8[16,8,4]', 'E8+E8') for r in d4_recs]
d4_aps = [r['avg_phi'] for r in d4_recs]
d4_colors = [AMBER if 'E8' in n else TEAL for n in d4_names]
bars = ax2.bar(range(len(d4_names)), d4_aps, color=d4_colors, edgecolor=FG, linewidth=0.5)
for b, v in zip(bars, d4_aps):
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.001,
             f'{v:.4f}', ha='center', va='bottom', color=FG, fontsize=8)
ax2.set_xticks(range(len(d4_names)))
ax2.set_xticklabels(d4_names, rotation=30, ha='right', color=FG, fontsize=8)
ax2.set_ylabel('avg \u03A6', color=FG)
ax2.set_title('Among d=4 [16,8] codes: E8+E8 (self-dual) loses', color=FG, fontsize=11, pad=10)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_color(FG)
ax2.grid(True, alpha=0.15, color=FG, axis='y')
ax2.set_ylim(min(d4_aps) - 0.02, max(d4_aps) + 0.02)
plt.savefig(f'{OUT}/fig8_self_dual16.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig8_self_dual16.png')

# --- Plot 9: Open Questions Status Dashboard ---
fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG, constrained_layout=True)
ax.set_facecolor(BG)
ax.axis('off')

questions = [
    ('Q1', 'Golay uniqueness\nas [23,12] max', 'THEOREM\nSTATED', AMBER,
     'avg_\\Phi\\ down in \\rho_\\Phi\n+ classical uniqueness'),
    ('Q2', 'Self-dual\nextension', 'FALSIFIED\n(qualified too)', RED,
     'Even d>=4 self-dual\nloses at n=16'),
    ('Q3', 'Why n=24?', 'OPEN\n(speculative direction)', VIOLET,
     'Likely outside \\Phi\n(Leech/Monster)'),
    ('Q4', 'Vacuum basin\ncharacterisation', 'CLOSED', TEAL,
     'Exactly 2,325 vectors\n= perfect ball HW<=3'),
    ('Q5', '[24,12,8] sampling\nvs Golay', 'PARTIALLY\nCLOSED', AMBER,
     'Golay wins +0.015\n(self-dual sampling failed)'),
]

for i, (qid, q, status, color, detail) in enumerate(questions):
    x = 0.05 + (i % 3) * 0.32
    y = 0.55 - (i // 3) * 0.45
    # Card background
    rect = plt.Rectangle((x, y), 0.28, 0.35, facecolor='#1F2630', edgecolor=color,
                          linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    # QID
    ax.text(x + 0.02, y + 0.28, qid, transform=ax.transAxes,
            fontsize=14, color=color, fontweight='bold', family='monospace')
    # Question
    ax.text(x + 0.08, y + 0.28, q, transform=ax.transAxes,
            fontsize=9, color=FG, va='top')
    # Status
    ax.text(x + 0.14, y + 0.15, status, transform=ax.transAxes,
            fontsize=10, color=color, ha='center', fontweight='bold', va='center')
    # Detail
    ax.text(x + 0.14, y + 0.04, detail, transform=ax.transAxes,
            fontsize=7.5, color='#B5BAC4', ha='center', va='center')

ax.text(0.5, 0.98, 'EXTREMAL_004 -- Open Questions Status',
        transform=ax.transAxes, fontsize=14, color=FG, ha='center', fontweight='bold')
ax.text(0.5, 0.04, '3 closed (1 fully, 1 partially, 1 falsified)  /  1 theorem stated  /  1 still open',
        transform=ax.transAxes, fontsize=9, color='#888', ha='center')
plt.savefig(f'{OUT}/fig9_status.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig9_status.png')

print('\nAll EXTREMAL_004 plots saved.')
