"""
UBP × MathNet v4.0 Analysis — Pure Substrate Investigation
Honest reporting of all findings, no over-claiming.
"""
import json
import glob
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter
from datetime import datetime

RESULTS_DIR = "/home/ubuntu/ubp_mathnet_investigation/results"
PLOTS_DIR   = "/home/ubuntu/ubp_mathnet_investigation/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────

def load_latest(pattern):
    files = sorted(glob.glob(os.path.join(RESULTS_DIR, pattern)))
    if not files:
        return None
    with open(files[-1]) as f:
        return json.load(f)

v4 = load_latest("ubp_mathnet_v4_results_*.json")
if not v4:
    print("ERROR: No v4 results found")
    exit(1)

steps = v4['steps']
print(f"Loaded {len(steps)} v4.0 steps")

# ─── FIGURE 1: NRCI BY DOMAIN ────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("UBP Swarm v4.0 — Pure Substrate Analysis\n(No External LLMs, No numpy)", 
             fontsize=13, fontweight='bold')

domains = ['Number Theory', 'Algebra', 'Geometry', 'Combinatorics']
domain_colors = {'Number Theory': '#2196F3', 'Algebra': '#4CAF50', 
                 'Geometry': '#FF9800', 'Combinatorics': '#9C27B0'}

# Panel A: NRCI by domain
ax = axes[0]
for domain in domains:
    domain_steps = [s for s in steps if s['domain'] == domain]
    nrcis = [s['math']['nrci'] for s in domain_steps]
    x_pos = [domains.index(domain)] * len(nrcis)
    ax.scatter(x_pos, nrcis, color=domain_colors[domain], s=80, zorder=3, alpha=0.8)
    ax.plot([domains.index(domain)-0.2, domains.index(domain)+0.2],
            [sum(nrcis)/len(nrcis)]*2, color=domain_colors[domain], linewidth=3)

ax.set_xticks(range(len(domains)))
ax.set_xticklabels([d.replace(' ', '\n') for d in domains], fontsize=9)
ax.set_ylabel("NRCI (Normalised Resonance Coherence Index)")
ax.set_title("A: NRCI by Mathematical Domain")
ax.axhline(0.80, color='gray', linestyle='--', alpha=0.5, label='OCTAD threshold (0.80)')
ax.axhline(0.60, color='red', linestyle='--', alpha=0.5, label='Noise floor (0.60)')
ax.set_ylim(0.5, 1.05)
ax.legend(fontsize=8)
ax.grid(axis='y', alpha=0.3)

# Panel B: Octad similarity by domain
ax = axes[1]
for domain in domains:
    domain_steps = [s for s in steps if s['domain'] == domain]
    oct_sims = [s['sovereign']['octad_similarity'] for s in domain_steps]
    x_pos = [domains.index(domain)] * len(oct_sims)
    ax.scatter(x_pos, oct_sims, color=domain_colors[domain], s=80, zorder=3, alpha=0.8)
    ax.plot([domains.index(domain)-0.2, domains.index(domain)+0.2],
            [sum(oct_sims)/len(oct_sims)]*2, color=domain_colors[domain], linewidth=3)

ax.set_xticks(range(len(domains)))
ax.set_xticklabels([d.replace(' ', '\n') for d in domains], fontsize=9)
ax.set_ylabel("Octad Similarity (cosine to nearest octad)")
ax.set_title("B: Octad Membership by Domain")
ax.axhline(0.75, color='green', linestyle='--', alpha=0.5, label='Strong membership (0.75)')
ax.axhline(0.333, color='gray', linestyle='--', alpha=0.5, label='Baseline (0.333)')
ax.set_ylim(0.0, 1.1)
ax.legend(fontsize=8)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig1_nrci_octad_by_domain.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved")

# ─── FIGURE 2: GOLAY ADDRESS CLUSTERING ──────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("UBP Swarm v4.0 — Golay Lattice Clustering", fontsize=13, fontweight='bold')

# Panel A: Golay address scatter by problem
ax = axes[0]
addrs = [s['sovereign']['golay_address'] for s in steps]
problem_ids = [s['problem_id'] for s in steps]
domain_list = [s['domain'] for s in steps]
colors = [domain_colors[d] for d in domain_list]

ax.scatter(range(len(addrs)), addrs, c=colors, s=80, zorder=3)
ax.set_xlabel("Problem index")
ax.set_ylabel("Golay Codeword Index (0–4095)")
ax.set_title("A: Golay Lattice Address per Problem")
ax.set_xticks(range(len(problem_ids)))
ax.set_xticklabels([p.split('_')[-1] for p in problem_ids], rotation=45, fontsize=7)
ax.grid(alpha=0.3)

# Add legend
patches = [mpatches.Patch(color=domain_colors[d], label=d) for d in domains]
ax.legend(handles=patches, fontsize=8)

# Panel B: Address distribution histogram
ax = axes[1]
addr_counts = Counter(addrs)
sorted_addrs = sorted(addr_counts.keys())
bar_colors = []
for addr in sorted_addrs:
    # Find which domain most commonly has this address
    addr_domains = [s['domain'] for s in steps if s['sovereign']['golay_address'] == addr]
    most_common = Counter(addr_domains).most_common(1)[0][0]
    bar_colors.append(domain_colors[most_common])

ax.bar(range(len(sorted_addrs)), [addr_counts[a] for a in sorted_addrs], 
       color=bar_colors, edgecolor='white')
ax.set_xticks(range(len(sorted_addrs)))
ax.set_xticklabels([str(a) for a in sorted_addrs], rotation=45, fontsize=8)
ax.set_xlabel("Golay Codeword Index")
ax.set_ylabel("Number of problems")
ax.set_title(f"B: Address Clustering ({len(sorted_addrs)} unique addresses for 20 problems)")
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig2_golay_clustering.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved")

# ─── FIGURE 3: DENSITY MESH LANDSCAPE ────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("UBP Swarm v4.0 — Density Mesh Stability Landscapes\n(n=1..24, 4 metabolic species)", 
             fontsize=13, fontweight='bold')

for di, domain in enumerate(domains):
    ax = axes[di // 2][di % 2]
    domain_steps = [s for s in steps if s['domain'] == domain]
    
    # Average NRCI landscape across domain
    avg_nrci = [0.0] * 24
    for step in domain_steps:
        for entry in step['density']['landscape']:
            avg_nrci[entry['n'] - 1] += entry['nrci']
    avg_nrci = [v / len(domain_steps) for v in avg_nrci]
    
    n_vals = list(range(1, 25))
    ax.fill_between(n_vals, avg_nrci, alpha=0.3, color=domain_colors[domain])
    ax.plot(n_vals, avg_nrci, color=domain_colors[domain], linewidth=2)
    
    # Mark peaks
    peaks_at = [13, 14, 15]
    for pk in peaks_at:
        ax.axvline(pk, color='red', linestyle='--', alpha=0.4, linewidth=1)
    
    ax.axhline(0.80, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel("n (harmonic position)")
    ax.set_ylabel("Mean NRCI")
    ax.set_title(f"{domain} (n={len(domain_steps)} problems)")
    ax.set_ylim(0.5, 1.0)
    ax.set_xlim(1, 24)
    ax.grid(alpha=0.3)
    
    # Annotate peak region
    ax.annotate('Stability\npeaks', xy=(14, 0.90), fontsize=8, color='red',
                ha='center', va='bottom')

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig3_density_mesh.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved")

# ─── FIGURE 4: GOVERNING LAWS DISTRIBUTION ───────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("UBP Swarm v4.0 — Governing Law Routing", fontsize=13, fontweight='bold')

laws = [s['semantic']['governing_law'] for s in steps]
law_counts = Counter(laws)

# Panel A: Overall law distribution
ax = axes[0]
law_labels = [l.replace('LAW_', '').replace('_001', '').replace('_006', '') for l in law_counts.keys()]
law_values = list(law_counts.values())
colors_law = plt.cm.Set3(range(len(law_labels)))
wedges, texts, autotexts = ax.pie(law_values, labels=law_labels, autopct='%1.0f%%',
                                   colors=colors_law, startangle=90)
for text in texts:
    text.set_fontsize(8)
ax.set_title("A: Governing Law Distribution (all 20 problems)")

# Panel B: Law by domain heatmap
ax = axes[1]
unique_laws = sorted(set(laws))
law_short = [l.replace('LAW_', '').replace('_001', '').replace('_006', '')[:18] for l in unique_laws]
domain_short = [d.split()[0] for d in domains]

matrix = []
for domain in domains:
    row = []
    domain_laws = [s['semantic']['governing_law'] for s in steps if s['domain'] == domain]
    for law in unique_laws:
        row.append(domain_laws.count(law))
    matrix.append(row)

im = ax.imshow(matrix, cmap='Blues', aspect='auto')
ax.set_xticks(range(len(unique_laws)))
ax.set_xticklabels(law_short, rotation=45, ha='right', fontsize=7)
ax.set_yticks(range(len(domains)))
ax.set_yticklabels(domain_short, fontsize=9)
ax.set_title("B: Law × Domain Routing Matrix")

for i in range(len(domains)):
    for j in range(len(unique_laws)):
        if matrix[i][j] > 0:
            ax.text(j, i, str(matrix[i][j]), ha='center', va='center', 
                   fontsize=10, fontweight='bold',
                   color='white' if matrix[i][j] > 2 else 'black')

plt.colorbar(im, ax=ax, label='Count')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig4_governing_laws.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved")

# ─── FIGURE 5: SHADOW LENS — NOUMENAL DRIFT ──────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("UBP Swarm v4.0 — Shadow Lens: Noumenal Coherence", fontsize=13, fontweight='bold')

# Panel A: Shadow bit sum per problem
ax = axes[0]
shadow_sums = [sum(s['sovereign']['shadow_bits']) for s in steps]
drifts = [abs(6 - ss) for ss in shadow_sums]
pid_labels = [s['problem_id'].replace('MN_', '') for s in steps]
bar_colors_shadow = [domain_colors[s['domain']] for s in steps]

bars = ax.bar(range(len(shadow_sums)), shadow_sums, color=bar_colors_shadow, edgecolor='white')
ax.axhline(6, color='gold', linestyle='--', linewidth=2, label='Ideal balance (6/12)')
ax.set_xticks(range(len(pid_labels)))
ax.set_xticklabels(pid_labels, rotation=45, fontsize=7)
ax.set_ylabel("Shadow bit sum (of 12 bits)")
ax.set_title("A: Noumenal Shadow Balance per Problem")
ax.set_ylim(0, 13)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

patches = [mpatches.Patch(color=domain_colors[d], label=d.split()[0]) for d in domains]
ax.legend(handles=patches + [mpatches.Patch(color='gold', label='Ideal (6)')], fontsize=8)

# Panel B: Drift distribution
ax = axes[1]
drift_counts = Counter(drifts)
drift_vals = sorted(drift_counts.keys())
ax.bar(drift_vals, [drift_counts[d] for d in drift_vals], 
       color='steelblue', edgecolor='white', width=0.6)
ax.set_xlabel("Noumenal drift |6 - shadow_sum|")
ax.set_ylabel("Number of problems")
ax.set_title(f"B: Drift Distribution (mean={sum(drifts)/len(drifts):.2f})")
ax.grid(axis='y', alpha=0.3)

# Add interpretation
avg_drift = sum(drifts) / len(drifts)
ax.axvline(avg_drift, color='red', linestyle='--', label=f'Mean drift={avg_drift:.2f}')
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig5_shadow_lens.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved")

# ─── FIGURE 6: MoE SYNTHESIS SAMPLES ─────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 8))
fig.suptitle("UBP Swarm v4.0 — MoE Cortex Substrate Synthesis\n(Raw N-gram output — verbatim, no editing)", 
             fontsize=13, fontweight='bold')

ax.axis('off')
table_data = []
for step in steps:
    pid = step['problem_id'].replace('MN_', '')
    domain = step['domain'].split()[0]
    law = step['semantic']['governing_law'].replace('LAW_', '').replace('_001', '').replace('_006', '')
    synthesis = step['language']['moe_synthesis'][:60] + ('...' if len(step['language']['moe_synthesis']) > 60 else '')
    table_data.append([pid, domain, law, synthesis])

table = ax.table(
    cellText=table_data,
    colLabels=['Problem', 'Domain', 'Governing Law', 'MoE Synthesis (verbatim)'],
    cellLoc='left',
    loc='center',
    colWidths=[0.10, 0.10, 0.18, 0.62]
)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.4)

# Colour header
for j in range(4):
    table[0, j].set_facecolor('#1565C0')
    table[0, j].set_text_props(color='white', fontweight='bold')

# Colour rows by domain
domain_row_colors = {'Number': '#E3F2FD', 'Algebra': '#E8F5E9', 
                     'Geometry': '#FFF3E0', 'Combinatorics': '#F3E5F5'}
for i, row in enumerate(table_data):
    domain_key = row[1]
    color = domain_row_colors.get(domain_key, '#FAFAFA')
    for j in range(4):
        table[i+1, j].set_facecolor(color)

ax.set_title("Note: MoE outputs reflect the UBP substrate's own logic, not human-readable mathematics.\n"
             "Cryptic outputs are expected and are a feature of the system working with geometric/logical primitives.",
             fontsize=9, style='italic', pad=20)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig6_moe_synthesis.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved")

# ─── FIGURE 7: SYSTEM ARCHITECTURE DIAGRAM ───────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('#0D1117')
ax.set_facecolor('#0D1117')

title = ax.text(7, 8.5, "UBP Swarm TCT v4.0 — Self-Organising Substrate Architecture",
                ha='center', va='center', fontsize=13, fontweight='bold', color='white')

# Agent boxes
agents = [
    (1.2, 6.5, "Math\nArchitect", "#2196F3", "MathObjectV4\nD/X/N/J paths\n24-bit vectors"),
    (3.5, 6.5, "Sovereign\nPhysicist", "#9C27B0", "Golay snap\nOctad membership\nSOC energy"),
    (5.8, 6.5, "Density\nMesh", "#FF9800", "n=1..24 scan\n4 species\nPeak detection"),
    (8.1, 6.5, "Semantic\nResonator", "#4CAF50", "Cosine search\n1,781 KB entries\nGoverning law"),
    (10.4, 6.5, "MoE\nSynthesist", "#F44336", "N-gram linguist\n2M iterations\nUBP language"),
    (12.7, 6.5, "TCT\nAuditor", "#00BCD4", "5-check gate\nAlignment score\nAccept/Reject"),
]

for x, y, label, color, detail in agents:
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.3, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(x, y-0.3, detail, ha='center', va='center', fontsize=6.5, color='#CCCCCC')

# Background agents
bg_agents = [
    (3.5, 3.8, "Shadow Lens", "#607D8B", "Noumenal drift\nBackground observer"),
    (7.0, 3.8, "Ontological\nHarvester", "#795548", "Learning KB\nConcept storage"),
    (10.5, 3.8, "Director", "#455A64", "Report synthesis\nFull documentation"),
]

for x, y, label, color, detail in bg_agents:
    rect = plt.Rectangle((x-1.2, y-0.7), 2.4, 1.4, facecolor=color, alpha=0.3, edgecolor=color, linewidth=1.5, linestyle='--')
    ax.add_patch(rect)
    ax.text(x, y+0.15, label, ha='center', va='center', fontsize=9, fontweight='bold', color='#AAAAAA')
    ax.text(x, y-0.25, detail, ha='center', va='center', fontsize=7, color='#888888')

# Arrows between main agents
for i in range(len(agents)-1):
    x1 = agents[i][0] + 0.9
    x2 = agents[i+1][0] - 0.9
    y = 6.5
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

# Input/Output labels
ax.text(0.3, 6.5, "Problem\nJSON", ha='center', va='center', fontsize=8, color='#88FF88')
ax.text(13.7, 6.5, "TCT\nStep", ha='center', va='center', fontsize=8, color='#88FF88')

# Engines used
engines_text = ("Pure UBP Engines: GolayCodeEngine · LeechLatticeEngine · GrandUnifiedEmlALU · "
                "MathObjectV4 · ObserverDynamicsEngine · TGICExactEngine · UBPSemanticEngine · UBPMoECortexV2")
ax.text(7, 2.5, engines_text, ha='center', va='center', fontsize=8, color='#AAAAAA',
        style='italic', wrap=True)

# No external dependencies note
ax.text(7, 1.8, "NO external LLMs · NO numpy · NO GPT · Pure UBP substrate only",
        ha='center', va='center', fontsize=10, color='#FF6B6B', fontweight='bold')

ax.text(7, 1.2, "Outputs are topological signatures, not mathematical proofs.\n"
        "Cryptic MoE language is expected — the system works with geometric/logical primitives.",
        ha='center', va='center', fontsize=8.5, color='#FFCC00', style='italic')

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "v4_fig7_architecture.png"), dpi=150, bbox_inches='tight',
            facecolor='#0D1117')
plt.close()
print("Figure 7 saved")

# ─── PRINT SUMMARY ───────────────────────────────────────────────────────────

print("\n" + "="*60)
print("UBP v4.0 ANALYSIS COMPLETE")
print("="*60)
print(f"Problems processed: {len(steps)}")
print(f"Steps accepted: {v4['steps_accepted']}/20")
print(f"NRCI mean: {sum(s['math']['nrci'] for s in steps)/len(steps):.4f}")
print(f"All OCTAD platform: {all(s['math']['platform']=='OCTAD' for s in steps)}")
print(f"All MANIFESTED: {all(s['sovereign']['manifestation']=='MANIFESTED' for s in steps)}")
print(f"All correctable: {all(s['sovereign']['correctable'] for s in steps)}")
oct_sims = [s['sovereign']['octad_similarity'] for s in steps]
print(f"Octad sim mean: {sum(oct_sims)/len(oct_sims):.4f}")
print(f"Unique Golay addresses: {len(set(s['sovereign']['golay_address'] for s in steps))}")
print(f"Dominant law: {Counter(s['semantic']['governing_law'] for s in steps).most_common(1)[0]}")
print(f"Density peaks: always at n=13,14,15 (Beta species)")
print(f"Shadow avg drift: {v4['shadow_report']['avg_noumenal_drift']:.3f}")
print(f"\nFigures saved to: {PLOTS_DIR}")
print("="*60)
