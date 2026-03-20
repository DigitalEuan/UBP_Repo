import json
import math
from fractions import Fraction
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Make core_studio imports work without package install
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent/'ubp'/'core_studio_v4.0'/'core'))

# However when running inside repo checkout, prefer repo-local core path
repo_core = Path('/home/user/ubp/core_studio_v4.0/core')
if repo_core.exists():
    sys.path.insert(0, str(repo_core))

import ubp_core_v5_3_merged as ubp
from ubp_kb_architect import KBArchitect

GOLAY_ENGINE = ubp.GOLAY_ENGINE
LEECH_ENGINE = ubp.LEECH_ENGINE

OUT = Path('/mnt/user-data/outputs/ubp-geometry-study')
DATA = OUT/'data'
FIG = OUT/'figures'
REPORT = OUT/'report'


def vec_to_int(vec):
    x = 0
    for b in vec:
        x = (x << 1) | int(b)
    return x

def fold24_to3(vec24):
    """Fold 24->12->6->3 by pairwise XOR."""
    v = list(map(int, vec24))
    for n in (12, 6, 3):
        v = [v[2*i] ^ v[2*i+1] for i in range(n)]
    return v

def spiral_step(vec24):
    """UBP-Py-like step: flip even indices then snap to Golay."""
    new_vec = [(b ^ 1) if (i % 2 == 0) else b for i, b in enumerate(vec24)]
    decoded, _, _ = GOLAY_ENGINE.decode(new_vec)
    return GOLAY_ENGINE.encode(decoded)

def cycle_length(start_vec, max_steps=800):
    """Return period length if cycle found within max_steps."""
    seen = {}
    v = start_vec
    for t in range(max_steps):
        key = tuple(v)
        if key in seen:
            return t - seen[key]
        seen[key] = t
        v = spiral_step(v)
    return None


def codeword_metrics(vec):
    w = int(sum(vec))
    tax = LEECH_ENGINE.calculate_symmetry_tax(vec)
    ten = Fraction(10, 1)
    nrci = ten / (ten + tax)
    tilt = KBArchitect.calculate_tilt(vec)
    fold3 = fold24_to3(vec)
    fold_w = int(sum(fold3))
    return {
        'weight': w,
        'tax': float(tax),
        'tax_frac': f"{tax.numerator}/{tax.denominator}",
        'nrci': float(nrci),
        'nrci_frac': f"{nrci.numerator}/{nrci.denominator}",
        'tilt_deg': tilt,
        'fold3': ''.join(map(str, fold3)),
        'fold3_weight': fold_w,
        'vec_int': vec_to_int(vec)
    }


def save_bar(x, y, title, xlabel, ylabel, path):
    plt.figure(figsize=(10, 4))
    plt.bar(x, y, color='#4C72B0')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def main():
    # 0) Full Golay codebook
    codewords = GOLAY_ENGINE.get_all_codewords()
    rows = []
    for idx, v in enumerate(codewords):
        m = codeword_metrics(v)
        m['codeword_index'] = idx
        rows.append(m)
    df = pd.DataFrame(rows)
    df.to_csv(DATA/'golay_codeword_metrics.csv', index=False)

    # weight distribution
    wdist = df['weight'].value_counts().sort_index()
    wdist.to_csv(DATA/'golay_weight_distribution.csv', header=['count'])
    save_bar(
        x=wdist.index.astype(int),
        y=wdist.values.astype(int),
        title='Golay [24,12,8] Codeword Weight Distribution (all 4096 codewords)',
        xlabel='Hamming weight (number of 1 bits)',
        ylabel='count',
        path=FIG/'weight_distribution.png'
    )

    # 1) Platonic-family lens: weights 4,6,8,12
    target_weights = [4, 6, 8, 12]
    df_plat = df[df['weight'].isin(target_weights)].copy()
    df_plat.to_csv(DATA/'platonic_weight_slices.csv', index=False)

    # Tilt summary by weight
    tilt_stats = df_plat.groupby('weight')['tilt_deg'].describe()
    tilt_stats.to_csv(DATA/'tilt_stats_platonic_weights.csv')

    plt.figure(figsize=(9, 4))
    for w in target_weights:
        vals = df_plat[df_plat['weight']==w]['tilt_deg'].values
        plt.hist(vals, bins=25, alpha=0.5, label=f'w={w}')
    plt.title('Tilt histograms for selected weights (4,6,8,12)')
    plt.xlabel('tilt (deg)')
    plt.ylabel('count')
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG/'tilt_hist_platonic_weights.png', dpi=200)
    plt.close()

    # Fold3 weight distribution by weight
    fold_counts = df_plat.groupby(['weight','fold3_weight']).size().reset_index(name='count')
    fold_counts.to_csv(DATA/'fold3_weight_by_weight_counts.csv', index=False)

    plt.figure(figsize=(9, 4))
    for w in target_weights:
        sub = fold_counts[fold_counts['weight']==w]
        plt.plot(sub['fold3_weight'], sub['count'], marker='o', label=f'w={w}')
    plt.title('3-fold core-tension (fold24→12→6→3): counts by codeword weight')
    plt.xlabel('fold3 weight (0..3)')
    plt.ylabel('count')
    plt.xticks([0,1,2,3])
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG/'fold3_weight_by_weight.png', dpi=200)
    plt.close()

    # 2) Octad triads: closure under XOR among 759 octads
    octads = GOLAY_ENGINE.get_octads()  # 759
    oct_int = [vec_to_int(v) for v in octads]
    int_to_idx = {oct_int[i]: i for i in range(len(octads))}

    triads = set()
    for i in range(len(octads)):
        ai = oct_int[i]
        for j in range(i+1, len(octads)):
            k = int_to_idx.get(ai ^ oct_int[j])
            if k is not None:
                triads.add(tuple(sorted((i, j, k))))

    triads = sorted(triads)
    # Store only first 5000 triads in file (full set can be regenerated)
    (DATA/'octad_triads.json').write_text(json.dumps({
        'octads_total': len(octads),
        'triad_count': len(triads),
        'triads_sample_first_5000': triads[:5000]
    }, indent=2))

    # Build graph
    G = nx.Graph()
    G.add_nodes_from(range(len(octads)))
    for a,b,c in triads:
        G.add_edge(a,b)
        G.add_edge(b,c)
        G.add_edge(a,c)

    deg = np.array([d for _, d in G.degree()], dtype=int)
    pd.DataFrame({'degree': deg}).to_csv(DATA/'octad_graph_degree.csv', index=False)

    plt.figure(figsize=(10, 4))
    plt.hist(deg, bins=40, color='#C44E52', edgecolor='white')
    plt.title('Octad triad-closure graph degree distribution (759 octads)')
    plt.xlabel('degree')
    plt.ylabel('count')
    plt.tight_layout()
    plt.savefig(FIG/'octad_degree_hist.png', dpi=200)
    plt.close()

    # Subgraph visualization of top-degree nodes
    top_nodes = list(np.argsort(-deg)[:60])
    H = G.subgraph(top_nodes).copy()
    pos = nx.spring_layout(H, seed=7)

    plt.figure(figsize=(9, 7))
    node_colors = [deg[n] for n in H.nodes()]
    nx.draw_networkx_nodes(H, pos, node_size=120, node_color=node_colors, cmap='viridis')
    nx.draw_networkx_edges(H, pos, alpha=0.35, width=0.8)
    plt.title('Octad triad-closure subgraph (top 60 by degree)')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(FIG/'octad_triads_subgraph.png', dpi=200)
    plt.close()

    # 3) UBPPy spiral dynamics on different weight strata (sampling)
    rng = np.random.default_rng(42)

    def sample_periods(weight, n=120):
        sl = df[df['weight']==weight]
        if len(sl) == 0:
            return []
        idxs = rng.choice(sl['codeword_index'].to_numpy(), size=min(n, len(sl)), replace=False)
        periods = []
        for idx in idxs:
            v = codewords[int(idx)]
            p = cycle_length(v, max_steps=800)
            periods.append(-1 if p is None else int(p))
        return periods

    period_rows = []
    for w in [0,4,6,8,12,16,24]:
        for p in sample_periods(w, n=120):
            period_rows.append({'weight': w, 'period': p})

    period_df = pd.DataFrame(period_rows)
    period_df.to_csv(DATA/'spiral_period_samples.csv', index=False)

    # Plot histogram per weight
    plt.figure(figsize=(10, 5))
    for w in sorted(period_df['weight'].unique()):
        vals = period_df[(period_df['weight']==w) & (period_df['period']>0)]['period'].values
        if len(vals):
            plt.hist(vals, bins=30, alpha=0.5, label=f'w={w}')
    plt.title('UBP-Py-like spiral: cycle period histograms (samples)')
    plt.xlabel('cycle period (steps)')
    plt.ylabel('count')
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG/'spiral_period_hist.png', dpi=200)
    plt.close()

    # Summary JSON for report
    summary = {
        'codewords_total': int(len(df)),
        'weights_present': sorted(map(int, wdist.index.tolist())),
        'weight_counts': {int(k): int(v) for k,v in wdist.items()},
        'tax_formula_note': 'Tax = (Hamming*Y) + (NormSq/8); for 0/1 Golay codewords, NormSq=Hamming, so Tax = weight*(Y + 1/8)',
        'Y_constant': str(ubp.SUBSTRATE.get_constants(50)['Y']),
        'octads_total': int(len(octads)),
        'octad_triads_count': int(len(triads)),
        'octad_degree_stats': {
            'min': int(deg.min()),
            'max': int(deg.max()),
            'mean': float(deg.mean()),
            'median': float(np.median(deg)),
        },
        'fold3_weight_distribution_all': {int(k): int(v) for k,v in Counter(df['fold3_weight']).items()},
        'fold3_weight_distribution_octads': {int(k): int(v) for k,v in Counter(df[df['weight']==8]['fold3_weight']).items()},
        'spiral_period_summary': period_df[period_df['period']>0].groupby('weight')['period'].describe().to_dict(),
        'note': 'triads stored are a sample (first 5000); full triad_count is in this summary'
    }
    (DATA/'summary.json').write_text(json.dumps(summary, indent=2))

    print('Wrote outputs to', OUT)


if __name__ == '__main__':
    main()
