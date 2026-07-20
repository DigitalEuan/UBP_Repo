"""
THREAD M: Larger [23,12] Sampling -- 50+ codes (verify Thread G theorem)
========================================================================

EXTREMAL_003 Thread D sampled 5 random [23,12] codes vs Golay [23,12,7].
Result: Golay won by +0.036.

This script scales up to 50+ random [23,12] codes to verify the result
is stable and the margin is reproducible.

Uses the fast numpy Monte Carlo from EXTREMAL_003.
"""
import sys, random, time, json
from fractions import Fraction
from itertools import product
from collections import Counter
import numpy as np

sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics, GolayCodeEngine

pp = UBPSourceCodeParticlePhysics()
Y = pp.Y
Y_plus_one_eighth = Y + Fraction(1, 8)
PHI_PEAK = Fraction(1, 1) / Y_plus_one_eighth
Y_f = float(Y)
Y_18_f = float(Y_plus_one_eighth)
PHI_PEAK_f = float(PHI_PEAK)


def rref_gf2(M):
    M = [row[:] for row in M]
    rows = len(M); cols = len(M[0]) if rows else 0
    r = 0; pivots = []
    for c in range(cols):
        pr = None
        for rr in range(r, rows):
            if M[rr][c] == 1: pr = rr; break
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]
        for rr in range(rows):
            if rr != r and M[rr][c] == 1:
                M[rr] = [(a + b) & 1 for a, b in zip(M[rr], M[r])]
        pivots.append(c); r += 1
        if r == rows: break
    return M, pivots

def rank_gf2(M):
    _, pivots = rref_gf2(M); return len(pivots)

def all_codewords_np(G, k, n):
    cw_list = []
    for bits in product([0, 1], repeat=k):
        cw_list.append([sum(G[i][j] for i, b in enumerate(bits) if b) & 1 for j in range(n)])
    return np.array(cw_list, dtype=np.uint8)

def random_generator(k, n, rng):
    while True:
        G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
        if rank_gf2(G) == k: return G

def d_min_np(cw_arr):
    nonzero = cw_arr[cw_arr.sum(axis=1) > 0]
    return int(nonzero.sum(axis=1).min())

def monte_carlo_avg_phi_fast(cw_arr, n, n_trials=15_000, seed=0):
    rng = np.random.default_rng(seed)
    cw_arr = cw_arr.astype(np.uint8)
    n_cw = cw_arr.shape[0]
    PAD = 32
    cw_padded = np.zeros((n_cw, PAD), dtype=np.uint8)
    cw_padded[:, :n] = cw_arr
    cw_packed = np.packbits(cw_padded, axis=1).view(np.uint32).reshape(n_cw)
    total_phi = 0.0
    dist_hist = Counter()
    BATCH = 500
    remaining = n_trials
    while remaining > 0:
        b = min(BATCH, remaining)
        vs = rng.integers(0, 2, size=(b, n), dtype=np.uint8)
        vs_padded = np.zeros((b, PAD), dtype=np.uint8)
        vs_padded[:, :n] = vs
        vs_packed = np.packbits(vs_padded, axis=1).view(np.uint32).reshape(b)
        hw_v = vs.sum(axis=1).astype(np.int32)
        xor = vs_packed[:, None] ^ cw_packed[None, :]
        try:
            dists = xor.view(np.uint64).bit_count()
        except AttributeError:
            dists = np.unpackbits(xor.view(np.uint8).reshape(b, n_cw, 4), axis=2).sum(axis=2)
        min_dists = dists.min(axis=1).astype(np.int32)
        is_cw = (min_dists == 0)
        phis = np.where(
            is_cw,
            np.where(hw_v > 0, PHI_PEAK_f, 0.0),
            np.where(hw_v > 0, hw_v / (hw_v * Y_18_f + min_dists * Y_f), 0.0)
        )
        total_phi += phis.sum()
        for md in min_dists:
            dist_hist[int(md)] += 1
        remaining -= b
    return total_phi / n_trials, dist_hist


print('=' * 72)
print('THREAD M: 50+ [23,12] codes vs Golay [23,12,7] -- verifying uniqueness')
print('=' * 72)

# Golay [23,12,7]
g24 = GolayCodeEngine()
all_cw_23 = np.array([cw[:-1] for cw in g24.get_all_codewords()], dtype=np.uint8)
d_golay = d_min_np(all_cw_23)
print(f'\nGolay [23,12,7]: d_min = {d_golay}')
ap_golay, hist_golay = monte_carlo_avg_phi_fast(all_cw_23, 23, 30_000, seed=1)
print(f'  avg_Phi (30k MC) = {ap_golay:.6f}')

# Sample 50 random [23,12] codes
rng = random.Random(20260629)
N_RANDOM = 50
print(f'\nSampling {N_RANDOM} random [23,12] codes (15k MC each, ~3s per code)...')
all_results = [{'name': 'Golay[23,12,7]', 'd_min': d_golay, 'avg_phi_mc': float(ap_golay)}]
t0_total = time.time()
for i in range(N_RANDOM):
    G = random_generator(12, 23, rng)
    cw = all_codewords_np(G, 12, 23)
    d = d_min_np(cw)
    ap, hist = monte_carlo_avg_phi_fast(cw, 23, 15_000, seed=i+10)
    all_results.append({'name': f'Random[23,12]#{i+1}', 'd_min': d, 'avg_phi_mc': float(ap)})
    if (i+1) % 10 == 0:
        print(f'  {i+1}/{N_RANDOM} done ({time.time()-t0_total:.1f}s)')

# Summary
print('\n--- Summary ---')
golay_ap = all_results[0]['avg_phi_mc']
random_aps = [r['avg_phi_mc'] for r in all_results[1:]]
print(f'  Golay [23,12,7]:     {golay_ap:.6f}')
print(f'  Random [23,12] codes ({len(random_aps)} sampled):')
print(f'    min:    {min(random_aps):.6f}')
print(f'    max:    {max(random_aps):.6f}')
print(f'    mean:   {sum(random_aps)/len(random_aps):.6f}')
print(f'    median: {sorted(random_aps)[len(random_aps)//2]:.6f}')
print(f'  Golay margin over best random: {golay_ap - max(random_aps):+.6f}')
print(f'  Golay margin over mean random: {golay_ap - sum(random_aps)/len(random_aps):+.6f}')
print(f'  Golay is highest? {golay_ap > max(random_aps)}')

# d_min distribution
print('\n--- d_min distribution ---')
from collections import Counter
d_hist = Counter(r['d_min'] for r in all_results[1:])
print(f'  Random [23,12] codes d_min distribution: {dict(sorted(d_hist.items()))}')
print(f'  Golay d_min = {d_golay} (unique)')

# Top 10 random codes by avg_Phi
print('\n--- Top 10 random [23,12] codes by avg_Phi ---')
top10 = sorted(all_results[1:], key=lambda r: -r['avg_phi_mc'])[:10]
for r in top10:
    print(f'  {r["name"]:<22s}  d={r["d_min"]}  avg_Phi={r["avg_phi_mc"]:.6f}')

# Bottom 5
print('\n--- Bottom 5 random [23,12] codes by avg_Phi ---')
bot5 = sorted(all_results[1:], key=lambda r: r['avg_phi_mc'])[:5]
for r in bot5:
    print(f'  {r["name"]:<22s}  d={r["d_min"]}  avg_Phi={r["avg_phi_mc"]:.6f}')

# Standard error of the margin
n = len(random_aps)
mean_random = sum(random_aps) / n
var_random = sum((x - mean_random) ** 2 for x in random_aps) / (n - 1)
se_random = (var_random / n) ** 0.5
print(f'\n  Standard error of mean random avg_Phi: {se_random:.6f}')
print(f'  Margin / SE: {(golay_ap - mean_random) / se_random:.1f} sigma')

with open('/home/z/my-project/work/large_23_12_results.json', 'w') as f:
    json.dump({'results': all_results, 'n_random': N_RANDOM,
               'golay_margin_over_best': golay_ap - max(random_aps),
               'golay_margin_over_mean': golay_ap - mean_random,
               'se_mean': se_random}, f, indent=2)
print('\nSaved to large_23_12_results.json')
