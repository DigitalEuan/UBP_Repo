"""
THREAD D: [23,12] Sampling -- Golay [23,12,7] vs random [23,12] codes on avg_Phi
==================================================================================

CONVERSE_001 Priority 4: "Run the avg_Phi test on [23,12] codes."

Exhaustive enumeration over all [23,12] codes is infeasible (2^276 candidate
generator matrices). Instead we sample.

The complication: avg_Phi over all 2^23 = 8,388,608 vectors is computationally
expensive if done naively (2^23 * 2^12 = 2^35 operations per code).

We exploit Golay-code structure: if C is a *perfect* code, every non-codeword is
at distance <= t from exactly one codeword, so dist(v, C) is uniformly bounded.
For perfect [23,12,7] Golay: t = (d-1)/2 = 3.

For RANDOM codes, the distances are not so uniform, and computing them naively
is 2^23 * 2^12 ~ 3.4e10 operations per code. We need a smarter approach.

ALGORITHM (coset-leader enumeration):
  - For each code C, compute the syndrome -> coset leader table up to weight w.
  - For each v in F_2^23, dist(v, C) = weight of coset leader of v's coset.
  - The number of distinct syndromes is 2^(n-k) = 2^11 = 2048.
  - So we enumerate cosets, not vectors.

But computing coset leaders for 2048 syndromes for arbitrary codes is complex.
For our purposes, we instead:
  1. Confirm Golay [23,12,7] (punctured Golay) is perfect -> every v at dist <= 3.
  2. For a small random sample of [23,12] codes, *estimate* avg_Phi by sampling
     10^5 random vectors (Monte Carlo), computing exact dist to all 4096 codewords.
"""
import sys, random, time, json
from fractions import Fraction
from itertools import product, combinations
from collections import Counter
sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics, GolayCodeEngine

pp = UBPSourceCodeParticlePhysics()
Y = pp.Y
Y_plus_one_eighth = Y + Fraction(1, 8)
PHI_PEAK = Fraction(1, 1) / Y_plus_one_eighth


def hw(v): return sum(1 for x in v if x)

def phi_with_dist(h_state, dist):
    if h_state == 0: return Fraction(0)
    denom = Fraction(h_state) * Y_plus_one_eighth + Fraction(dist) * Y
    return Fraction(h_state) / denom


# ---- Linear code utilities ----
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

def all_codewords(G, k, n):
    cw = []
    for bits in product([0, 1], repeat=k):
        cw.append(tuple(sum(g[i][j] for i, b in enumerate(bits) if b) & 1 for j in range(n)))
    return cw

def random_generator(k, n, rng):
    while True:
        G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
        if rank_gf2(G) == k: return G

def d_min(codewords):
    return min(sum(c) for c in codewords if sum(c) > 0)


# ---- Build the [23,12,7] perfect Golay code (puncture the [24,12,8] extended Golay) ----
print('=' * 72)
print('THREAD D: [23,12] sampling -- Golay[23,12,7] vs random [23,12] codes')
print('=' * 72)

g24 = GolayCodeEngine()
all_cw_24 = g24.get_all_codewords()
# Puncture the last coordinate: just drop it
all_cw_23 = [tuple(cw[:-1]) for cw in all_cw_24]
# Verify it's a [23,12] linear code with d=7
print(f'\nPunctured Golay [23,12] code:')
print(f'  Number of codewords: {len(all_cw_23)} (expected 4096)')
d_punct = d_min(all_cw_23)
print(f'  d_min: {d_punct} (expected 7 for perfect Golay)')

# Test perfectness: every vector in F_2^23 should be at distance <= 3 from a codeword.
# We Monte Carlo this rather than exhaustively checking 2^23 vectors.
rng = random.Random(20260624)
PERFECT_TEST = 10_000
max_dist = 0
for _ in range(PERFECT_TEST):
    v = tuple(rng.randint(0, 1) for _ in range(23))
    if sum(v) == 0: continue
    if v in set(all_cw_23): continue
    md = min(sum((a + b) & 1 for a, b in zip(v, c)) for c in all_cw_23)
    max_dist = max(max_dist, md)
print(f'  Perfectness check (10^4 random vectors): max dist to nearest codeword = {max_dist}')
print(f'  (Expected: <= 3 if the code is perfect [23,12,7])')


# ---- Monte Carlo estimate avg_Phi for [23,12,7] Golay and random [23,12] codes ----
def monte_carlo_avg_phi(codewords, n, n_trials=20_000, rng=None):
    """Estimate avg_Phi by random sampling."""
    if rng is None: rng = random.Random(0)
    cw_set = set(codewords)
    total = Fraction(0)
    dist_hist = Counter()
    for _ in range(n_trials):
        v = tuple(rng.randint(0, 1) for _ in range(n))
        h = sum(v)
        if h == 0:
            continue
        if v in cw_set:
            total += PHI_PEAK
            dist_hist[0] += 1
        else:
            md = min(sum((a + b) & 1 for a, b in zip(v, c)) for c in codewords)
            total += phi_with_dist(h, md)
            dist_hist[md] += 1
    return Fraction(total, n_trials), dist_hist


print('\n--- Monte Carlo avg_Phi (20,000 samples per code) ---')
print(f'{"name":<25s}  {"d_min":>5s}  {"avg_Phi":>10s}  {"dist histogram":<40s}')
print('-' * 90)

all_results = []

# Golay [23,12,7]
t0 = time.time()
ap_golay, hist_golay = monte_carlo_avg_phi(all_cw_23, 23, 20_000, rng)
t1 = time.time()
hist_top6 = dict(sorted(hist_golay.items())[:6])
print(f'{"Golay[23,12,7]":<25s}  {d_punct:>5d}  {float(ap_golay):>10.6f}  {hist_top6}')
print(f'  (computed in {t1-t0:.1f}s)')
all_results.append({
    'name': 'Golay[23,12,7]',
    'd_min': d_punct,
    'avg_phi_mc': float(ap_golay),
    'dist_hist': dict(hist_golay),
    'samples': 20_000,
})

# Random [23,12] codes -- 5 of them
for i in range(5):
    G = random_generator(12, 23, rng)
    cw = all_codewords(G, 12, 23)
    d = d_min(cw)
    t0 = time.time()
    ap, hist = monte_carlo_avg_phi(cw, 23, 20_000, rng)
    t1 = time.time()
    name = f'Random[23,12]#{i+1}'
    hist_top6 = dict(sorted(hist.items())[:6])
    print(f'{name:<25s}  {d:>5d}  {float(ap):>10.6f}  {hist_top6}')
    print(f'  (computed in {t1-t0:.1f}s)')
    all_results.append({
        'name': name, 'd_min': d, 'avg_phi_mc': float(ap),
        'dist_hist': dict(hist), 'samples': 20_000,
    })

# Summary
print('\n--- Summary ---')
golay_ap = all_results[0]['avg_phi_mc']
random_aps = [r['avg_phi_mc'] for r in all_results[1:]]
print(f'  Golay [23,12,7] avg_Phi:    {golay_ap:.6f}')
print(f'  Random [23,12] codes avg_Phi range: [{min(random_aps):.6f}, {max(random_aps):.6f}]')
print(f'  Random [23,12] codes avg_Phi mean:  {sum(random_aps)/len(random_aps):.6f}')
print(f'  Golay is highest? {golay_ap > max(random_aps)}')
print(f'  Golay margin over best random: {golay_ap - max(random_aps):+.6f}')
print(f'  Golay margin over mean random: {golay_ap - sum(random_aps)/len(random_aps):+.6f}')

# Also check: distance histograms
print('\n--- Distance histogram comparison ---')
print(f'  Golay:    {dict(sorted(all_results[0]["dist_hist"].items()))}')
for r in all_results[1:4]:
    print(f'  {r["name"]:<20s} d_min={r["d_min"]}: {dict(sorted(r["dist_hist"].items()))}')

# Save
with open('/home/z/my-project/work/golay23_results.json', 'w') as f:
    json.dump({'results': all_results}, f, indent=2, default=str)
print('\nSaved to golay23_results.json')
