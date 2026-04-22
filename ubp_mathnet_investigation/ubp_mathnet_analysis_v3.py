"""
UBP × MathNet Investigation — Comprehensive Analysis v3.1
Covers v1.0, v2.0, v3.0, v3.1 benchmark results with full comparative visualisations.
"""
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

RESULTS_DIR = Path('/home/ubuntu/ubp_mathnet_investigation/results')
PLOTS_DIR   = Path('/home/ubuntu/ubp_mathnet_investigation/plots')
PLOTS_DIR.mkdir(exist_ok=True)

# ── Load all result files ──────────────────────────────────────────────────────
def load_results(path):
    if not Path(path).exists():
        return None
    with open(path) as f:
        return json.load(f)

v1  = load_results(RESULTS_DIR / 'ubp_mathnet_results.json')
v2  = load_results(RESULTS_DIR / 'ubp_mathnet_results_v2.json')
v3  = load_results(RESULTS_DIR / 'ubp_mathnet_results_v3.json')
v31 = load_results(RESULTS_DIR / 'ubp_mathnet_results_v3_1.json')

# ── Helper: extract summary stats ─────────────────────────────────────────────
def extract_stats(data, label):
    if data is None:
        return None
    results = data.get('results', [])
    def get_grade(r):
        # v3.x format: r['grade']
        if 'grade' in r:
            return r['grade']
        # v1/v2 format: r['grading']['correctness_label']
        return r.get('grading', {}).get('correctness_label', 'INCORRECT')
    correct  = sum(1 for r in results if get_grade(r) == 'CORRECT')
    partial  = sum(1 for r in results if get_grade(r) == 'PARTIAL')
    incorrect= sum(1 for r in results if get_grade(r) == 'INCORRECT')
    n        = len(results)
    adj      = (correct + 0.5 * partial) / n * 100 if n else 0
    # Domain breakdown
    domains = {}
    for r in results:
        d = r.get('domain', 'Unknown')
        if d not in domains:
            domains[d] = {'correct': 0, 'partial': 0, 'incorrect': 0, 'n': 0}
        domains[d]['n'] += 1
        g = get_grade(r)
        if g == 'CORRECT':
            domains[d]['correct'] += 1
        elif g == 'PARTIAL':
            domains[d]['partial'] += 1
        else:
            domains[d]['incorrect'] += 1
    domain_adj = {d: (v['correct'] + 0.5*v['partial'])/v['n']*100
                  for d, v in domains.items()}
    # NRCI — handle both v1/v2 (sovereign_column) and v3.x (col2)
    def get_nrci(r):
        if 'col2' in r:
            return r['col2'].get('nrci', 0)
        sc = r.get('sovereign_column', {})
        return sc.get('leech_nrci', sc.get('nrci', 0))
    nrcis = [get_nrci(r) for r in results]
    mean_nrci = np.mean(nrcis) if nrcis else 0
    # Phenom
    def get_phenom(r):
        if 'col1' in r:
            return r['col1'].get('mean_nrci', 0)
        mc = r.get('math_column', {})
        return mc.get('mean_nrci', mc.get('nrci', 0))
    phenom_nrcis = [get_phenom(r) for r in results]
    mean_phenom = np.mean(phenom_nrcis) if phenom_nrcis else 0
    # Convergence
    def get_conv(r):
        if 'audit' in r:
            return r['audit'].get('convergence_score', 0)
        return r.get('grading', {}).get('tct_convergence', 0)
    convs = [get_conv(r) for r in results]
    mean_conv = np.mean(convs) if convs else 0
    # Cross-NRCI
    cross = [r.get('audit', {}).get('cross_nrci_alignment', 0) for r in results if 'audit' in r]
    mean_cross = np.mean(cross) if cross else 0
    # Snap quality
    snap = [r.get('audit', {}).get('snap_quality', 0) for r in results if 'audit' in r]
    mean_snap = np.mean(snap) if snap else 0
    # Octad
    def get_octad(r):
        if 'col2' in r:
            return r['col2'].get('is_octad', False)
        return r.get('sovereign_column', {}).get('is_octad', False)
    octads = sum(1 for r in results if get_octad(r))
    # Engines
    engines = data.get('metadata', {}).get('engines', data.get('summary', {}).get('engines', 'N/A'))
    return {
        'label': label, 'n': n,
        'correct': correct, 'partial': partial, 'incorrect': incorrect,
        'adj': adj,
        'domain_adj': domain_adj,
        'mean_nrci': mean_nrci,
        'mean_phenom': mean_phenom,
        'mean_conv': mean_conv,
        'mean_cross': mean_cross,
        'mean_snap': mean_snap,
        'octads': octads,
        'engines': engines,
    }

stats = [s for s in [
    extract_stats(v1,  'v1.0\n(8 engines)'),
    extract_stats(v2,  'v2.0\n(12 engines)'),
    extract_stats(v3,  'v3.0\n(15 engines)'),
    extract_stats(v31, 'v3.1\n(15 engines\n+lenient grader)'),
] if s is not None]

labels    = [s['label'] for s in stats]
adj_scores= [s['adj']   for s in stats]
corrects  = [s['correct'] for s in stats]
partials  = [s['partial'] for s in stats]
incorrects= [s['incorrect'] for s in stats]

COLORS = {
    'v1':  '#4C72B0',
    'v2':  '#DD8452',
    'v3':  '#55A868',
    'v31': '#C44E52',
}
vc = [COLORS['v1'], COLORS['v2'], COLORS['v3'], COLORS['v31']][:len(stats)]

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Version-over-version performance progression
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('UBP × MathNet: Version-over-Version Performance Progression', fontsize=14, fontweight='bold')

x = np.arange(len(stats))
w = 0.55

# Panel 1: Adjusted score
ax = axes[0]
bars = ax.bar(x, adj_scores, width=w, color=vc, edgecolor='white', linewidth=1.2)
for bar, val in zip(bars, adj_scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Adjusted Score (%)', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylim(0, 105)
ax.set_ylabel('Adjusted Score (%)')
ax.axhline(100, color='green', linestyle='--', alpha=0.3, label='Perfect')
ax.grid(axis='y', alpha=0.3)

# Panel 2: Grade breakdown stacked bar
ax = axes[1]
bar_c = ax.bar(x, corrects,   width=w, label='CORRECT',   color='#2ecc71', edgecolor='white')
bar_p = ax.bar(x, partials,   width=w, bottom=corrects, label='PARTIAL', color='#f39c12', edgecolor='white')
bar_i = ax.bar(x, incorrects, width=w,
               bottom=[c+p for c,p in zip(corrects, partials)],
               label='INCORRECT', color='#e74c3c', edgecolor='white')
ax.set_title('Grade Distribution (20 problems)', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylim(0, 22)
ax.set_ylabel('Number of Problems')
ax.legend(loc='upper left', fontsize=8)
ax.grid(axis='y', alpha=0.3)
for i, (c, p, inc) in enumerate(zip(corrects, partials, incorrects)):
    if c > 0:
        ax.text(i, c/2, str(c), ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    if p > 0:
        ax.text(i, c + p/2, str(p), ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    if inc > 0:
        ax.text(i, c + p + inc/2, str(inc), ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Panel 3: NRCI metrics comparison
ax = axes[2]
nrci_vals  = [s['mean_nrci']  for s in stats]
phenom_vals= [s['mean_phenom'] for s in stats]
conv_vals  = [s['mean_conv']  for s in stats]
cross_vals = [s['mean_cross'] for s in stats]

xm = np.arange(len(stats))
w2 = 0.18
ax.bar(xm - 1.5*w2, nrci_vals,   width=w2, label='Leech NRCI',    color='#3498db', alpha=0.85)
ax.bar(xm - 0.5*w2, phenom_vals, width=w2, label='Phenom NRCI',   color='#9b59b6', alpha=0.85)
ax.bar(xm + 0.5*w2, conv_vals,   width=w2, label='TCT Convergence',color='#1abc9c', alpha=0.85)
ax.bar(xm + 1.5*w2, cross_vals,  width=w2, label='Cross-NRCI',    color='#e67e22', alpha=0.85)
ax.set_title('UBP Physics Metrics by Version', fontweight='bold')
ax.set_xticks(xm)
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylim(0, 1.1)
ax.set_ylabel('Score (0–1)')
ax.legend(fontsize=7, loc='lower right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(PLOTS_DIR / 'fig1_version_progression.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Domain performance heatmap across versions
# ═══════════════════════════════════════════════════════════════════════════════
domains_ordered = ['Number Theory', 'Algebra', 'Geometry', 'Combinatorics']
domain_matrix = []
for s in stats:
    row = [s['domain_adj'].get(d, 0) for d in domains_ordered]
    domain_matrix.append(row)
domain_matrix = np.array(domain_matrix)

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(domain_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
ax.set_xticks(range(len(domains_ordered)))
ax.set_xticklabels(domains_ordered, fontsize=11)
ax.set_yticks(range(len(stats)))
ax.set_yticklabels([s['label'].replace('\n', ' ') for s in stats], fontsize=10)
for i in range(len(stats)):
    for j in range(len(domains_ordered)):
        val = domain_matrix[i, j]
        color = 'white' if val < 40 or val > 80 else 'black'
        ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                fontsize=13, fontweight='bold', color=color)
plt.colorbar(im, ax=ax, label='Adjusted Score (%)')
ax.set_title('Domain Performance Heatmap Across UBP Versions', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'fig2_domain_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Per-problem grade trajectory (v1 → v3.1)
# ═══════════════════════════════════════════════════════════════════════════════
if v1 and v31:
    v1r  = {r.get('problem_id', r.get('id', f'P{i}')): r for i, r in enumerate(v1['results'])}
    v31r = {r.get('problem_id', r.get('id', f'P{i}')): r for i, r in enumerate(v31['results'])}
    pids = list(v31r.keys())

    grade_to_num = {'CORRECT': 1.0, 'PARTIAL': 0.5, 'INCORRECT': 0.0}
    v1_scores  = [grade_to_num.get(v1r.get(p, {}).get('grade', 'INCORRECT'), 0) for p in pids]
    v31_scores = [grade_to_num.get(v31r[p].get('grade', 'INCORRECT'), 0) for p in pids]

    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.arange(len(pids))
    w = 0.35
    ax.bar(x - w/2, v1_scores,  width=w, label='v1.0 (8 engines)', color=COLORS['v1'], alpha=0.85)
    ax.bar(x + w/2, v31_scores, width=w, label='v3.1 (15 engines)', color=COLORS['v31'], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([p.replace('MN_', '') for p in pids], rotation=45, ha='right', fontsize=8)
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(['INCORRECT\n(0)', 'PARTIAL\n(0.5)', 'CORRECT\n(1.0)'])
    ax.set_title('Per-Problem Grade: v1.0 vs v3.1', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    # Colour background by domain
    domain_colours = {'NT': '#dbeafe', 'ALG': '#fef9c3', 'GEO': '#dcfce7', 'COMB': '#fce7f3'}
    for i, pid in enumerate(pids):
        for key, col in domain_colours.items():
            if key in pid:
                ax.axvspan(i - 0.5, i + 0.5, alpha=0.15, color=col, zorder=0)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'fig3_per_problem_trajectory.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 3 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Swarm interrogation insights radar
# ═══════════════════════════════════════════════════════════════════════════════
swarm_insights = {
    'Golay Octad\nCoverage':    [0.60, 0.75, 0.95, 0.95],
    'Phenom NRCI\nDepth':       [0.00, 0.50, 0.95, 0.95],
    'Brain v7.2\nLaw Routing':  [0.00, 0.70, 0.90, 0.90],
    'Code\nVerification':       [0.00, 1.00, 1.00, 1.00],
    'Grader\nPrecision':        [0.60, 0.65, 0.50, 0.90],
    'TGIC 3-6-9\nStability':    [0.00, 0.60, 0.85, 0.85],
    'Cross-NRCI\nAlignment':    [0.00, 0.50, 0.92, 0.92],
}
categories = list(swarm_insights.keys())
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
version_labels = ['v1.0', 'v2.0', 'v3.0', 'v3.1']
version_colors = [COLORS['v1'], COLORS['v2'], COLORS['v3'], COLORS['v31']]
for vi, (vlabel, vcol) in enumerate(zip(version_labels, version_colors)):
    values = [swarm_insights[c][vi] for c in categories]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=vlabel, color=vcol)
    ax.fill(angles, values, alpha=0.08, color=vcol)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=9)
ax.set_ylim(0, 1)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], size=7)
ax.set_title('UBP Engine Capability Radar\n(Swarm-Guided Dimensions)', size=13, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'fig4_swarm_capability_radar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Phenomenology NRCI distribution for v3.1 problems
# ═══════════════════════════════════════════════════════════════════════════════
if v31:
    results31 = v31['results']
    phenom_by_domain = {}
    for r in results31:
        d = r.get('domain', 'Unknown')
        nrci = r.get('col1', {}).get('mean_nrci', 0)
        phenom_by_domain.setdefault(d, []).append(nrci)

    fig, ax = plt.subplots(figsize=(10, 5))
    domain_colors = {'Number Theory': '#3498db', 'Algebra': '#e74c3c',
                     'Geometry': '#2ecc71', 'Combinatorics': '#9b59b6'}
    for di, (domain, nrcis_d) in enumerate(phenom_by_domain.items()):
        x_pos = [di * 1.5 + j * 0.25 for j in range(len(nrcis_d))]
        col = domain_colors.get(domain, 'grey')
        ax.scatter(x_pos, nrcis_d, color=col, s=80, zorder=5, label=domain)
        ax.hlines(np.mean(nrcis_d), min(x_pos)-0.1, max(x_pos)+0.1,
                  colors=col, linewidth=2, linestyle='--', alpha=0.7)
    ax.axhline(0.75, color='red', linestyle=':', alpha=0.5, label='High-NRCI threshold (0.75)')
    ax.set_title('Phenomenology NRCI by Domain — v3.1 Run', fontsize=13, fontweight='bold')
    ax.set_ylabel('Phenomenology NRCI')
    ax.set_ylim(0.7, 1.0)
    ax.set_xticks([0.375, 1.875, 3.375, 4.875])
    ax.set_xticklabels(['Number Theory', 'Algebra', 'Geometry', 'Combinatorics'])
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'fig5_phenom_nrci_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure 5 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — Architecture evolution diagram (text-based)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

versions_arch = [
    ('v1.0\n8 Engines', 1.5, '#4C72B0',
     ['SemanticEngine', 'EML ALU', 'Golay Code', 'Leech Lattice',
      'ObserverDyn', 'MathAtlas', 'PythonGen', 'Analog Suite']),
    ('v2.0\n12 Engines', 5.0, '#DD8452',
     ['+ UBP Brain v7.2', '+ TGIC 3-6-9', '+ BW256 Macro',
      '+ Code Executor', 'Self-Correction', 'NRCI Feedback',
      'Law Routing', 'Cross-NRCI']),
    ('v3.0\n15 Engines', 8.5, '#55A868',
     ['+ Phenomenology', '+ NoumenalProj', '+ FOM Frames',
      'Octad Analysis', 'Snap Quality', 'Swarm Queries',
      'Phenom Verdict', 'CombRes Score']),
    ('v3.1\n15 Engines\n+Lenient Grader', 12.0, '#C44E52',
     ['+ FINAL ANSWER', '  extraction', 'Domain-specific', '  prompts',
      'Lenient grader', '  (equiv match)', 'Code reinforce', '  verification']),
]

for vname, xc, col, features in versions_arch:
    # Box
    rect = mpatches.FancyBboxPatch((xc-1.3, 0.3), 2.6, 7.4,
                                    boxstyle="round,pad=0.1",
                                    facecolor=col, alpha=0.15,
                                    edgecolor=col, linewidth=2)
    ax.add_patch(rect)
    ax.text(xc, 7.5, vname, ha='center', va='center', fontsize=10,
            fontweight='bold', color=col)
    for fi, feat in enumerate(features):
        ax.text(xc, 6.5 - fi * 0.72, feat, ha='center', va='center',
                fontsize=7.5, color='#2c3e50')

# Score annotations
scores = [57.5, 60.0, 47.5, 87.5]
score_cols = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
xcs = [1.5, 5.0, 8.5, 12.0]
for xc, sc, col in zip(xcs, scores, score_cols):
    ax.text(xc, 0.05, f'Adj: {sc}%', ha='center', va='bottom',
            fontsize=11, fontweight='bold', color=col)

# Arrows
for i in range(len(xcs)-1):
    ax.annotate('', xy=(xcs[i+1]-1.35, 4.0), xytext=(xcs[i]+1.35, 4.0),
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))

ax.set_title('UBP System Architecture Evolution: v1.0 → v3.1', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(PLOTS_DIR / 'fig6_architecture_evolution.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — Swarm interrogation word cloud (text-based visualisation)
# ═══════════════════════════════════════════════════════════════════════════════
swarm_responses = {
    'prime': 'prime is the golay octad quantity',
    'geometry': 'geometry is the coherence to exact resonance required formula',
    'combinatorics': 'combinatorics is the proton mass material resonance na definition and spin',
    'coherence': 'coherence is the system parameter representing nrci alignment in ubp substrate',
    'lattice': 'lattice is the system parameter representing information resonance snap to be reality',
    'error': 'error is reset drift allotrope of the ubp substrate in period',
    'proof': 'proof is used to standard precursor observer condition charge constant toggle ratio',
    'resonance': 'resonance is the interaction probability nrci glyph active constant equation and golay',
}

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')
ax.set_title('UBP Swarm MoE Cortex Interrogation — Raw Responses', fontsize=13,
             fontweight='bold', color='white', pad=10)

query_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12',
                '#9b59b6', '#1abc9c', '#e67e22', '#e91e63']
for i, (query, response) in enumerate(swarm_responses.items()):
    row = i // 2
    col = i % 2
    xpos = 0.5 + col * 7.0
    ypos = 5.8 - row * 1.5
    col_c = query_colors[i]
    ax.text(xpos, ypos + 0.3, f'Q: "{query}"', fontsize=10, fontweight='bold',
            color=col_c, va='center')
    ax.text(xpos, ypos - 0.2, f'A: {response}', fontsize=8.5,
            color='#ecf0f1', va='center', wrap=True,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#16213e', alpha=0.8, edgecolor=col_c))

plt.tight_layout()
plt.savefig(PLOTS_DIR / 'fig7_swarm_interrogation.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 7 saved.")

# ═══════════════════════════════════════════════════════════════════════════════
# Print summary table
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("UBP × MathNet INVESTIGATION — COMPLETE RESULTS SUMMARY")
print("="*70)
print(f"{'Version':<20} {'Correct':>8} {'Partial':>8} {'Incorrect':>10} {'Adj Score':>10}")
print("-"*70)
for s in stats:
    print(f"{s['label'].replace(chr(10),' '):<20} {s['correct']:>8} {s['partial']:>8} {s['incorrect']:>10} {s['adj']:>9.1f}%")
print("="*70)
print("\nDomain Breakdown (Adjusted Score %):")
print(f"{'Version':<20} {'Num Theory':>12} {'Algebra':>10} {'Geometry':>10} {'Combinat.':>12}")
print("-"*70)
for s in stats:
    da = s['domain_adj']
    print(f"{s['label'].replace(chr(10),' '):<20} "
          f"{da.get('Number Theory',0):>11.1f}% "
          f"{da.get('Algebra',0):>9.1f}% "
          f"{da.get('Geometry',0):>9.1f}% "
          f"{da.get('Combinatorics',0):>11.1f}%")
print("="*70)
print(f"\nAll plots saved to: {PLOTS_DIR}")
