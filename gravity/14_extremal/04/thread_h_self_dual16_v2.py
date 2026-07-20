"""
THREAD H (v2): Qualified Self-Dual Conjecture Test on [16,8] -- Monte Carlo
==========================================================================

Switched from exact avg_Phi (14s/code) to Monte Carlo (1s/code) so we can
test 60+ random codes and 15+ self-dual codes.
"""
import sys, random, time, json
from fractions import Fraction
from itertools import product
from collections import Counter, defaultdict
import numpy as np

sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics

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

def random_orthogonal_B(k, rng, max_attempts=500):
    for _ in range(max_attempts):
        B = [[rng.randint(0, 1) for _ in range(k)] for _ in range(k)]
        if rank_gf2(B) != k: continue
        ok = True
        for i in range(k):
            for j in range(k):
                dot = sum(B[i][t] * B[j][t] for t in range(k)) & 1
                expected = 1 if i == j else 0
                if dot != expected:
                    ok = False; break
            if not ok: break
        if ok: return B
    return None

def random_self_dual_generator(k, n, rng):
    assert n == 2 * k
    B = random_orthogonal_B(k, rng)
    if B is None: return None
    G = []
    for i in range(k):
        row = [0] * k + list(B[i])
        G.append(row)
    return G

def is_self_dual(G, k, n):
    if k != n - k: return False
    if rank_gf2(G) != k: return False
    for i in range(k):
        for j in range(i, k):
            dot = sum(G[i][t] * G[j][t] for t in range(n)) & 1
            if dot != 0: return False
    return True

def d_min_np(cw_arr):
    nonzero = cw_arr[cw_arr.sum(axis=1) > 0]
    return int(nonzero.sum(axis=1).min())

def monte_carlo_avg_phi_fast(cw_arr, n, n_trials=10_000, seed=0):
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
print('THREAD H (v2): Qualified Self-Dual Conjecture Test on [16,8]')
print('=' * 72)

rng = random.Random(20260625)
N_RANDOM = 80
N_SELFDUAL_TARGET = 20

records = []

print(f'\nSampling {N_RANDOM} random [16,8] codes (Monte Carlo 10k each, ~0.5s)...')
t0_total = time.time()
for i in range(N_RANDOM):
    G = random_generator(8, 16, rng)
    cw_arr = all_codewords_np(G, 8, 16)
    d = d_min_np(cw_arr)
    sd = is_self_dual(G, 8, 16)
    ap, hist = monte_carlo_avg_phi_fast(cw_arr, 16, 10_000, seed=i)
    records.append({'name': f'Random[16,8]#{i+1}', 'd_min': d, 'self_dual': sd,
                    'avg_phi': float(ap)})
    if (i+1) % 20 == 0:
        print(f'  {i+1}/{N_RANDOM} done ({time.time()-t0_total:.1f}s)')

print(f'\nGenerating self-dual [16,8] codes via G = [I_8 | B], B orthogonal...')
n_sd_generated = 0
n_attempts = 0
while n_sd_generated < N_SELFDUAL_TARGET and n_attempts < 500:
    n_attempts += 1
    G = random_self_dual_generator(8, 16, rng)
    if G is None: continue
    cw_arr = all_codewords_np(G, 8, 16)
    d = d_min_np(cw_arr)
    sd = is_self_dual(G, 8, 16)
    if not sd: continue
    n_sd_generated += 1
    ap, hist = monte_carlo_avg_phi_fast(cw_arr, 16, 10_000, seed=1000+n_sd_generated)
    records.append({'name': f'SelfDual[16,8]#{n_sd_generated}', 'd_min': d, 'self_dual': True,
                    'avg_phi': float(ap)})

print(f'\n  Generated {n_sd_generated} self-dual codes in {n_attempts} attempts '
      f'(acceptance rate {n_sd_generated/n_attempts*100:.1f}%)')

# Also explicitly include the RM[16,8,4] code (canonical self-dual)
print('\n--- Explicit: Reed-Muller [16,5,8] vs RM[16,8,4] (self-dual d=4) ---')
# RM(1,4) is [16,5,8] -- self-dual? No, dim is 5 not 8.
# RM(2,4) is [16,11,4] -- also not self-dual.
# The [16,8,4] self-dual code is RM(1,4) extended? Actually it's the "first-order Reed-Muller"
# punctured differently. Let me just use the direct-sum E8 + E8 construction.
# E8 generator (8x8 self-dual): the [8,4,4] extended Hamming, doubled.
G_hamming8 = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
]
# E8 + E8 direct sum: 8x16 generator
G_e8e8 = []
for row in G_hamming8:
    G_e8e8.append(row + [0]*8)
for row in G_hamming8:
    G_e8e8.append([0]*8 + row)
cw_e8e8 = all_codewords_np(G_e8e8, 8, 16)
d_e8e8 = d_min_np(cw_e8e8)
sd_e8e8 = is_self_dual(G_e8e8, 8, 16)
ap_e8e8, _ = monte_carlo_avg_phi_fast(cw_e8e8, 16, 10_000, seed=9999)
print(f'  E8+E8 [16,8,4] (self-dual):  d={d_e8e8}  avg_Phi={ap_e8e8:.6f}')
records.append({'name': 'E8+E8[16,8,4]', 'd_min': d_e8e8, 'self_dual': sd_e8e8, 'avg_phi': float(ap_e8e8)})

print(f'\nTotal codes tested: {len(records)}')
print(f'  Self-dual: {sum(1 for r in records if r["self_dual"])}')
print(f'  Non-self-dual: {sum(1 for r in records if not r["self_dual"])}')

# Group by (self_dual, d_min) and report avg_Phi stats
print('\n--- avg_Phi by (self_dual, d_min) ---')
groups = defaultdict(list)
for r in records:
    groups[(r['self_dual'], r['d_min'])].append(r['avg_phi'])
for (sd, d), phis in sorted(groups.items(), key=lambda x: (x[0][1], x[0][0])):
    sd_label = 'SD' if sd else 'NSD'
    if phis:
        print(f'  {sd_label} d={d}: n={len(phis):>3d}  avg_Phi range [{min(phis):.5f}, {max(phis):.5f}]  mean {sum(phis)/len(phis):.5f}')

# Top 10 by avg_Phi
print('\n--- Top 10 by avg_Phi ---')
top10 = sorted(records, key=lambda r: -r['avg_phi'])[:10]
for r in top10:
    sd_label = 'SD' if r['self_dual'] else 'NSD'
    print(f'  {r["name"]:<25s}  d={r["d_min"]}  {sd_label}  avg_Phi={r["avg_phi"]:.6f}')
top10_sd_count = sum(1 for r in top10 if r['self_dual'])
print(f'  Top 10 contains {top10_sd_count} self-dual codes')

# Among d >= 4 codes specifically
print('\n--- Among d_min >= 4 codes ---')
d4plus = [r for r in records if r['d_min'] >= 4]
if d4plus:
    sd_d4 = [r for r in d4plus if r['self_dual']]
    nsd_d4 = [r for r in d4plus if not r['self_dual']]
    if sd_d4:
        print(f'  Self-dual d>=4:     {len(sd_d4)} codes, avg_Phi range [{min(r['avg_phi'] for r in sd_d4):.5f}, {max(r['avg_phi'] for r in sd_d4):.5f}]')
    else:
        print(f'  Self-dual d>=4:     0 codes')
    if nsd_d4:
        print(f'  Non-self-dual d>=4: {len(nsd_d4)} codes, avg_Phi range [{min(r['avg_phi'] for r in nsd_d4):.5f}, {max(r['avg_phi'] for r in nsd_d4):.5f}]')
    else:
        print(f'  Non-self-dual d>=4: 0 codes')
    top_d4 = sorted(d4plus, key=lambda r: -r['avg_phi'])[:5]
    print(f'  Top 5 by avg_Phi among d>=4:')
    for r in top_d4:
        sd_label = 'SD' if r['self_dual'] else 'NSD'
        print(f'    {r["name"]:<25s}  d={r["d_min"]}  {sd_label}  avg_Phi={r["avg_phi"]:.6f}')

with open('/home/z/my-project/work/self_dual16_results.json', 'w') as f:
    json.dump({'records': records, 'n_random': N_RANDOM, 'n_self_dual': n_sd_generated}, f, indent=2)
print('\nSaved to self_dual16_results.json')
