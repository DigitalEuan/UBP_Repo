import json
from fractions import Fraction
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import networkx as nx

import sys
sys.path.insert(0, '/home/user/ubp/core_studio_v4.0/core')
import ubp_core_v5_3_merged as ubp
from ubp_kb_architect import KBArchitect

OUT = Path('/mnt/user-data/outputs/ubp-geometry-study')
DATA = OUT/'data'

GOLAY = ubp.GOLAY_ENGINE


def vec_to_int(vec):
    x=0
    for b in vec:
        x = (x<<1)|int(b)
    return x

def fold24_to3(vec24):
    v = list(map(int, vec24))
    for n in (12,6,3):
        v = [v[2*i] ^ v[2*i+1] for i in range(n)]
    return tuple(v)

def spiral_step(vec24):
    new_vec = [(b ^ 1) if (i % 2 == 0) else b for i, b in enumerate(vec24)]
    msg, _, _ = GOLAY.decode(new_vec)
    return GOLAY.encode(msg)

def orbit_decomp(codewords):
    seen=set()
    orbits=[]
    for v in codewords:
        t=tuple(v)
        if t in seen:
            continue
        a=t
        b=tuple(spiral_step(list(a)))
        if b==a:
            orbits.append([a])
            seen.add(a)
        else:
            # check involution
            c=tuple(spiral_step(list(b)))
            if c!=a:
                # longer orbit; trace until repeats
                orbit=[a]
                seen.add(a)
                cur=b
                while cur not in orbit:
                    orbit.append(cur)
                    seen.add(cur)
                    cur=tuple(spiral_step(list(cur)))
                orbits.append(orbit)
            else:
                orbits.append([a,b])
                seen.add(a)
                seen.add(b)
    return orbits


def build_octad_graph():
    octads = GOLAY.get_octads()
    oct_int = [vec_to_int(v) for v in octads]
    int_to_idx={oct_int[i]: i for i in range(len(octads))}

    triads=set()
    for i in range(len(octads)):
        ai=oct_int[i]
        for j in range(i+1, len(octads)):
            k=int_to_idx.get(ai ^ oct_int[j])
            if k is not None:
                triads.add(tuple(sorted((i,j,k))))

    G=nx.Graph()
    G.add_nodes_from(range(len(octads)))
    for a,b,c in triads:
        G.add_edge(a,b)
        G.add_edge(b,c)
        G.add_edge(a,c)
    return G, triads


def strongly_regular_params(G, sample_edges=500, sample_nonedges=500, seed=123):
    rng=np.random.default_rng(seed)
    nodes=np.array(G.nodes())
    edges=list(G.edges())
    nonedges=list(nx.non_edges(G))

    e_idx=rng.choice(len(edges), size=min(sample_edges,len(edges)), replace=False)
    ne_idx=rng.choice(len(nonedges), size=min(sample_nonedges,len(nonedges)), replace=False)

    common_edge=[]
    for idx in e_idx:
        u,v = edges[int(idx)]
        common_edge.append(len(list(nx.common_neighbors(G,u,v))))

    common_non=[]
    for idx in ne_idx:
        u,v = nonedges[int(idx)]
        common_non.append(len(list(nx.common_neighbors(G,u,v))))

    return {
        'k': int(np.mean([d for _,d in G.degree()])),
        'common_neighbors_edge_unique': sorted(set(common_edge)),
        'common_neighbors_nonedge_unique': sorted(set(common_non)),
        'edge_common_neighbors_counts': Counter(common_edge),
        'nonedge_common_neighbors_counts': Counter(common_non)
    }


def main():
    codewords = GOLAY.get_all_codewords()

    # A) Spiral orbit structure across ALL 4096 codewords
    orbits = orbit_decomp(codewords)
    orbit_sizes = Counter(len(o) for o in orbits)

    # verify mapping is involution (all orbits size <=2)
    max_orbit=max(orbit_sizes)

    (DATA/'spiral_orbit_summary.json').write_text(json.dumps({
        'orbits_total': len(orbits),
        'orbit_size_counts': {str(k): int(v) for k,v in orbit_sizes.items()},
        'max_orbit_size': int(max_orbit),
        'note': 'if max_orbit_size==2, spiral_step is an involution on the codebook'
    }, indent=2))

    # B) fold3 string distribution for all codewords and octads
    fold_all = Counter(fold24_to3(v) for v in codewords)
    fold_oct = Counter(fold24_to3(v) for v in GOLAY.get_octads())

    (DATA/'fold3_string_distribution.json').write_text(json.dumps({
        'fold3_all_codewords': {''.join(map(str,k)): int(v) for k,v in fold_all.items()},
        'fold3_octads': {''.join(map(str,k)): int(v) for k,v in fold_oct.items()},
    }, indent=2))

    # C) strongly-regular-ish params for octad graph
    G, triads = build_octad_graph()
    srg = strongly_regular_params(G)

    # Save exact degree uniformity
    deg = [d for _,d in G.degree()]
    srg['degree_min']=int(min(deg))
    srg['degree_max']=int(max(deg))

    # Save triad count and edge/nonedge common neighbor distributions
    # (convert Counters to dicts)
    srg['edge_common_neighbors_counts'] = {str(k): int(v) for k,v in srg['edge_common_neighbors_counts'].items()}
    srg['nonedge_common_neighbors_counts'] = {str(k): int(v) for k,v in srg['nonedge_common_neighbors_counts'].items()}
    srg['triad_count'] = int(len(triads))
    srg['nodes']=int(G.number_of_nodes())
    srg['edges']=int(G.number_of_edges())

    (DATA/'octad_graph_srg_probe.json').write_text(json.dumps(srg, indent=2))

    print('done')

if __name__=='__main__':
    main()
