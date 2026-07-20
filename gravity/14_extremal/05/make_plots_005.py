"""Generate plots for EXTREMAL_005 deck."""
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

OUT = '/home/z/my-project/download/slides_005'
os.makedirs(OUT, exist_ok=True)

BG = '#0E1116'
FG = '#E6E6E6'
AMBER = '#FFB454'
TEAL = '#6FE3D2'
VIOLET = '#B097FF'
RED = '#FF6B6B'

# --- Plot 10: Thread J -- Step 3 verification ---
step3 = json.load(open('/home/z/my-project/work/step3_results.json'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), facecolor=BG, constrained_layout=True)

# Left: avg_Phi vs rho_Phi scatter
ax1.set_facecolor(BG)
random_codes = step3['random_codes']
ap_random = [r['avg_phi'] for r in random_codes]
rho_random = [r['rho_phi'] for r in random_codes]
ap_h = step3['hamming']['avg_phi']
rho_h = step3['hamming']['rho_phi']
ax1.scatter(rho_random, ap_random, c=TEAL, s=24, alpha=0.55, edgecolor=FG, linewidth=0.3,
            label=f'100 random [7,4] codes')
ax1.scatter([rho_h], [ap_h], c=AMBER, s=220, marker='*', edgecolor=FG, linewidth=1.2,
            label='Hamming [7,4,3] (perfect)', zorder=10)
ax1.set_xlabel('rho_Phi  =  E_v[ dist(v,C) / HW(v) ]', color=FG)
ax1.set_ylabel('avg_Phi(C)', color=FG)
ax1.set_title(f'Step 3 verified: Hamming has lowest rho_Phi\nPearson = {step3["pearson_corr"]:+.3f}, Spearman = {step3["spearman_corr"]:+.3f}',
              color=FG, fontsize=11, pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_color(FG)
ax1.grid(True, alpha=0.15, color=FG)
ax1.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='lower left', fontsize=9)

# Right: distance distribution comparison
ax2.set_facecolor(BG)
labels = ['dist=0\n(codeword)', 'dist=1', 'dist=2', 'dist=3', 'dist=4']
h_hist = step3['hamming']['dist_hist']
# Pick 5 best random by avg_Phi
top5 = sorted(random_codes, key=lambda r: -r['avg_phi'])[:5]
h_counts = [h_hist.get(str(k), h_hist.get(k, 0)) for k in range(5)]
random_mean = []
for k in range(5):
    vals = [r['dist_hist'].get(str(k), r['dist_hist'].get(k, 0)) for r in top5]
    random_mean.append(np.mean(vals) if vals else 0)
x = np.arange(len(labels))
width = 0.35
ax2.bar(x - width/2, h_counts, width, color=AMBER, edgecolor=FG, linewidth=0.5, label='Hamming')
ax2.bar(x + width/2, random_mean, width, color=TEAL, edgecolor=FG, linewidth=0.5, label='Random (top-5 avg)')
ax2.set_xticks(x)
ax2.set_xticklabels(labels, color=FG, fontsize=9)
ax2.set_ylabel('count of vectors', color=FG)
ax2.set_title('Distance distribution: Hamming vs random\nHamming is uniquely concentrated at dist <= 1', color=FG, fontsize=11, pad=10)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_color(FG)
ax2.grid(True, alpha=0.15, color=FG, axis='y')
ax2.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='upper right', fontsize=9)
plt.savefig(f'{OUT}/fig10_step3.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig10_step3.png')

# --- Plot 11: Thread K -- Refined SD conjecture falsified ---
refined = json.load(open('/home/z/my-project/work/refined_sd_results.json'))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), facecolor=BG, constrained_layout=True)

# Left: avg_Phi vs d_min, color by SD/DE
ax1.set_facecolor(BG)
records = refined['random_codes']
nsd = [(r['d_min'], r['avg_phi']) for r in records if not r['self_dual']]
ax1.scatter([x[0] for x in nsd], [x[1] for x in nsd], c=TEAL, s=28, alpha=0.55,
            edgecolor=FG, linewidth=0.3, label=f'non-self-dual (n={len(nsd)})')
# Plot the two SD codes
ax1.scatter([4], [refined['canonical_de']['avg_phi']], c=AMBER, s=180, marker='*',
            edgecolor=FG, linewidth=1.0, label='DE [16,8,4] canonical', zorder=10)
ax1.scatter([4], [refined['e8_plus_e8']['avg_phi']], c=VIOLET, s=180, marker='*',
            edgecolor=FG, linewidth=1.0, label='E8+E8 [16,8,4]', zorder=10)
ax1.set_xlabel('d_min', color=FG)
ax1.set_ylabel('avg_Phi (Monte Carlo 10k)', color=FG)
ax1.set_title('Refined conjecture: DE SD codes do NOT win at n=16', color=FG, fontsize=11, pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_color(FG)
ax1.grid(True, alpha=0.15, color=FG)
ax1.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='lower right', fontsize=9)

# Right: bar chart of all [16,8,4] codes specifically
ax2.set_facecolor(BG)
d4_recs = [r for r in records if r['d_min'] == 4 and not r['self_dual']]
# Also include canonical DE and E8+E8
all_d4 = [
    ('Random\n(best NSD)', max(r['avg_phi'] for r in d4_recs), TEAL),
    ('Random\n(median NSD)', sorted(r['avg_phi'] for r in d4_recs)[len(d4_recs)//2], TEAL),
    ('E8+E8\n(DE SD)', refined['e8_plus_e8']['avg_phi'], VIOLET),
    ('DE canonical\n(DE SD)', refined['canonical_de']['avg_phi'], AMBER),
]
names = [x[0] for x in all_d4]
vals = [x[1] for x in all_d4]
colors_b = [x[2] for x in all_d4]
bars = ax2.bar(range(len(names)), vals, color=colors_b, edgecolor=FG, linewidth=0.5)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.002,
             f'{v:.4f}', ha='center', va='bottom', color=FG, fontsize=9)
ax2.set_xticks(range(len(names)))
ax2.set_xticklabels(names, color=FG, fontsize=9)
ax2.set_ylabel('avg_Phi', color=FG)
ax2.set_title('Among d=4 [16,8] codes: self-dual codes LOSE', color=FG, fontsize=11, pad=10)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_color(FG)
ax2.grid(True, alpha=0.15, color=FG, axis='y')
ax2.set_ylim(min(vals) - 0.03, max(vals) + 0.03)
plt.savefig(f'{OUT}/fig11_refined_sd.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig11_refined_sd.png')

# --- Plot 12: Thread M -- 50 [23,12] codes vs Golay ---
large23 = json.load(open('/home/z/my-project/work/large_23_12_results.json'))
results = large23['results']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), facecolor=BG, constrained_layout=True)

# Left: histogram of random code avg_Phi with Golay as vertical line
ax1.set_facecolor(BG)
ap_all = [r['avg_phi_mc'] for r in results[1:]]  # skip Golay
ax1.hist(ap_all, bins=20, color=TEAL, edgecolor=FG, linewidth=0.5, alpha=0.75)
ax1.axvline(results[0]['avg_phi_mc'], color=AMBER, linewidth=2.5, label=f"Golay [23,12,7] = {results[0]['avg_phi_mc']:.4f}")
ax1.axvline(max(ap_all), color=RED, linestyle='--', linewidth=1.2, label=f'Best random = {max(ap_all):.4f}')
ax1.axvline(sum(ap_all)/len(ap_all), color=FG, linestyle=':', linewidth=1.2, label=f'Mean random = {sum(ap_all)/len(ap_all):.4f}')
ax1.set_xlabel('avg_Phi (Monte Carlo 15k)', color=FG)
ax1.set_ylabel('count of [23,12] codes', color=FG)
ax1.set_title(f'50 random [23,12] codes vs Golay\nGolay margin: +{large23["golay_margin_over_best"]:.4f} (46 sigma)', color=FG, fontsize=11, pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values(): spine.set_color(FG)
ax1.grid(True, alpha=0.15, color=FG, axis='y')
ax1.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='upper left', fontsize=9)

# Right: avg_Phi vs d_min, with Golay as star
ax2.set_facecolor(BG)
d_all = [r['d_min'] for r in results[1:]]
ax2.scatter(d_all, ap_all, c=TEAL, s=28, alpha=0.6, edgecolor=FG, linewidth=0.3,
            label='Random [23,12] codes')
ax2.scatter([7], [results[0]['avg_phi_mc']], c=AMBER, s=260, marker='*',
            edgecolor=FG, linewidth=1.2, label='Golay [23,12,7]', zorder=10)
ax2.set_xlabel('d_min', color=FG)
ax2.set_ylabel('avg_Phi', color=FG)
ax2.set_title('avg_Phi vs d_min: Golay is structurally unique (d=7)', color=FG, fontsize=11, pad=10)
ax2.tick_params(colors=FG)
for spine in ax2.spines.values(): spine.set_color(FG)
ax2.grid(True, alpha=0.15, color=FG)
ax2.legend(facecolor=BG, edgecolor=FG, labelcolor=FG, loc='lower right', fontsize=9)
plt.savefig(f'{OUT}/fig12_large_23.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig12_large_23.png')

# --- Plot 13: Final program status (consolidated) ---
fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG, constrained_layout=True)
ax.set_facecolor(BG)
ax.axis('off')

# Draw 5 program-status cards
items = [
    ('EXTREMAL_001', 'Initial \\Phi definition\n10^5 sweep, vacuum collapse', 'PROVISIONAL', '#888', 'Jun 2026'),
    ('EXTREMAL_002', 'Constant Peak Theorem\nAnalytic Dominance Theorem', 'CANDIDATE\nFOUNDATION', AMBER, 'Jun 2026'),
    ('CONVERSE_001', 'Two breaks identified\navg_\\Phi covering connection', 'SELF-\nFALSIFICATION', RED, 'Jun 2026'),
    ('EXTREMAL_003', 'avg_\\Phi-covering theorem\n[23,12] Golay wins +0.036', 'PROGRAM\nADVANCED', TEAL, 'Jun 2026'),
    ('EXTREMAL_004', 'Vacuum basin = 2,325\nUniqueness theorem stated\nRefined SD conjecture', '3 OPEN QS\nCLOSED', VIOLET, 'Jun 2026'),
    ('EXTREMAL_005\n(this doc)', 'Step 3 verified (Spearman -0.99)\n46-sigma [23,12] result\nRefined SD ALSO falsified', 'SOLIDIFIED', AMBER, 'Jun 2026'),
]

for i, (doc, result, status, color, date) in enumerate(items):
    x = 0.04 + (i % 3) * 0.32
    y = 0.55 - (i // 3) * 0.45
    rect = plt.Rectangle((x, y), 0.28, 0.38, facecolor='#1F2630', edgecolor=color,
                          linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x + 0.14, y + 0.34, doc, transform=ax.transAxes,
            fontsize=10, color=color, fontweight='bold', ha='center', family='monospace')
    ax.text(x + 0.14, y + 0.28, date, transform=ax.transAxes,
            fontsize=8, color='#888', ha='center', family='monospace')
    ax.text(x + 0.14, y + 0.18, result, transform=ax.transAxes,
            fontsize=8.5, color=FG, ha='center', va='center')
    ax.text(x + 0.14, y + 0.06, status, transform=ax.transAxes,
            fontsize=10, color=color, ha='center', fontweight='bold', va='center')

ax.text(0.5, 0.98, 'UBP Extremal Law Program -- 6-Document Trajectory',
        transform=ax.transAxes, fontsize=14, color=FG, ha='center', fontweight='bold')
ax.text(0.5, 0.02, 'From PROVISIONAL (001) -> SOLIDIFIED (005):  5 closed open questions, 2 theorems (1 with full proof, 1 with sketch), 3 falsifications published honestly.',
        transform=ax.transAxes, fontsize=9, color='#888', ha='center')
plt.savefig(f'{OUT}/fig13_program.png', dpi=160, facecolor=BG)
plt.close()
print(f'Wrote {OUT}/fig13_program.png')

print('\nAll EXTREMAL_005 plots saved.')
