"""
THREAD L: Proper Self-Dual [24,12] Sampling via Construction A
================================================================

EXTREMAL_004 Thread F failed to generate random self-dual [24,12] codes
via the naive G = [I | B] with B orthogonal -- 0/500 acceptance.

This script implements a smarter approach:

METHOD 1 (Construction A):
  Generate a random self-dual [24,12] code by:
  1. Generate random invertible 12x12 matrix A over GF(2).
  2. Form G = [I_12 | A + A^T] (this ensures G * G^T = I + (A+A^T)(A+A^T)^T = I + (A+A^T)^2
     ... wait that doesn't quite work.

METHOD 2 (Better): Self-dual codes from random Gram-Schmidt over GF(2):
  Given a random 12x24 matrix M, we can produce a self-dual code by:
  1. Row-reduce to find a basis.
  2. Use a symplectic-Gram-Schmidt process to make rows pairwise orthogonal.
  This is complex.

METHOD 3 (Simplest, used here): Sample many random self-dual [24,12] codes by
  generating G = [I | B] where B is symmetric with diagonal entries matching
  a specific pattern. For self-dual codes over GF(2):
    G * G^T = 0 mod 2 requires B * B^T = I mod 2 (B orthogonal)
    Plus, the diagonal of G * G^T must be 0 mod 2, which gives constraints.

METHOD 4 (Actually works): Construction via "bordering".
  Given a self-dual [n,k] code C with generator G_C = [A | B] (k x n),
  we can construct a self-dual [n+2, k+1] code by:
    G_{n+2} = [1 1 0 ... 0 | row of A | row of B]
              [0 ... 0 1 1 | rest   | rest]
  But starting from a small self-dual code (e.g. [8,4,4] ExtHamming), we can
  build up to [16,8,4] and then to [24,12,?]. This is the "doubling construction".

SIMPLEST WORKING APPROACH:
  Take ExtHamming [8,4,4] (self-dual) and Golay [24,12,8] (self-dual) as
  fixed references. For random self-dual [24,12] codes, use the doubling
  construction starting from random [12,6] self-dual codes.

  Even simpler: use the FACT that the direct sum of two self-dual [12,6] codes
  gives a self-dual [24,12] code. We need self-dual [12,6] codes -- these can
  be constructed by G = [I_6 | B] with B orthogonal 6x6 over GF(2). The
  acceptance rate for 6x6 should be much higher than 12x12.

  Actually, direct sum of two [12,6] self-dual codes gives a [24,12] code
  with d_min = min(d_1, d_2), typically d=2 or d=4. NOT d=8.

  So the only [24,12] self-dual code with d=8 is Golay (uniqueness theorem).
  Random self-dual [24,12] codes will have d in {2, 4, 6}.

STRATEGY for this script:
  1. Generate random self-dual [24,12] codes via direct sum of two [12,6]
     self-dual codes (G = [I_6 | B], B orthogonal 6x6).
  2. Compute avg_Phi for each via Monte Carlo.
  3. Compare to Golay [24,12,8].

EXPECTED RESULT: Golay wins by a large margin, because random self-dual
[24,12] codes have d <= 6, much worse than Golay's d=8.
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

def random_orthogonal_B(k, rng, max_attempts=5000):
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

def random_self_dual_12_6(rng):
    """Generate a random self-dual [12,6] code via G = [I_6 | B], B orthogonal."""
    B = random_orthogonal_B(6, rng)
    if B is None: return None
    G = []
    for i in range(6):
        row = [0]*6 + list(B[i])
        G.append(row)
    return G

def random_self_dual_24_12_direct_sum(rng):
    """Generate a random self-dual [24,12] code as direct sum of two [12,6] SD codes."""
    G1 = random_self_dual_12_6(rng)
    if G1 is None: return None
    G2 = random_self_dual_12_6(rng)
    if G2 is None: return None
    # Direct sum: G_24 = [G1 0; 0 G2] (12x24)
    G = []
    for row in G1:
        G.append(row + [0]*12)
    for row in G2:
        G.append([0]*12 + row)
    return G

def random_self_dual_24_12_bordering(rng):
    """Generate a self-dual [24,12] code via a different construction: random
    orthogonal 12x12 B, but use a smarter search."""
    # Try direct orthogonal-B construction with many attempts
    B = random_orthogonal_B(12, rng, max_attempts=10000)
    if B is None: return None
    G = []
    for i in range(12):
        row = [0]*12 + list(B[i])
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
print('THREAD L: Self-Dual [24,12] Sampling via Construction A')
print('=' * 72)

# Golay [24,12,8]
g24 = GolayCodeEngine()
all_cw_24 = np.array(g24.get_all_codewords(), dtype=np.uint8)
d_golay = d_min_np(all_cw_24)
print(f'\nGolay [24,12,8]: d_min = {d_golay}')

ap_golay, hist_golay = monte_carlo_avg_phi_fast(all_cw_24, 24, 15_000, seed=1)
print(f'  avg_Phi = {ap_golay:.6f}')
print(f'  dist hist: {dict(sorted(hist_golay.items()))}')

# Generate random self-dual [24,12] codes via direct sum of [12,6]
rng = random.Random(20260628)
print('\n--- Generating random self-dual [24,12] codes via direct sum of [12,6] ---')
sd_records = []
n_attempts = 0
n_generated = 0
while n_generated < 6 and n_attempts < 100:
    n_attempts += 1
    G = random_self_dual_24_12_direct_sum(rng)
    if G is None:
        print(f'  Attempt {n_attempts}: failed to generate')
        continue
    cw = all_codewords_np(G, 12, 24)
    if not is_self_dual(G, 12, 24):
        print(f'  Attempt {n_attempts}: not self-dual')
        continue
    n_generated += 1
    d = d_min_np(cw)
    ap, hist = monte_carlo_avg_phi_fast(cw, 24, 15_000, seed=100+n_generated)
    name = f'SD-direct-sum[24,12]#{n_generated}'
    print(f'  {name}: d={d}, avg_Phi={ap:.6f}, dist_hist={dict(sorted(hist.items()))}')
    sd_records.append({'name': name, 'd_min': d, 'self_dual': True, 'avg_phi_mc': float(ap),
                       'dist_hist': dict(hist)})

# Also try the direct 12x12 orthogonal-B construction
print('\n--- Trying direct 12x12 orthogonal-B construction ---')
n_direct_attempts = 0
n_direct_generated = 0
while n_direct_generated < 3 and n_direct_attempts < 50:
    n_direct_attempts += 1
    G = random_self_dual_24_12_bordering(rng)
    if G is None: continue
    cw = all_codewords_np(G, 12, 24)
    if not is_self_dual(G, 12, 24): continue
    n_direct_generated += 1
    d = d_min_np(cw)
    ap, hist = monte_carlo_avg_phi_fast(cw, 24, 15_000, seed=200+n_direct_generated)
    name = f'SD-direct-B[24,12]#{n_direct_generated}'
    print(f'  {name}: d={d}, avg_Phi={ap:.6f}')
    sd_records.append({'name': name, 'd_min': d, 'self_dual': True, 'avg_phi_mc': float(ap),
                       'dist_hist': dict(hist)})

# Sample 4 random [24,12] codes (not necessarily self-dual)
print('\n--- 4 random [24,12] codes for context ---')
def random_generator(k, n, rng):
    while True:
        G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
        if rank_gf2(G) == k: return G

random_records = []
for i in range(4):
    G = random_generator(12, 24, rng)
    cw = all_codewords_np(G, 12, 24)
    d = d_min_np(cw)
    ap, hist = monte_carlo_avg_phi_fast(cw, 24, 15_000, seed=300+i)
    name = f'Random[24,12]#{i+1}'
    print(f'  {name}: d={d}, avg_Phi={ap:.6f}')
    random_records.append({'name': name, 'd_min': d, 'self_dual': False, 'avg_phi_mc': float(ap),
                            'dist_hist': dict(hist)})

# Summary
print('\n--- Summary ---')
all_results = [
    {'name': 'Golay[24,12,8]', 'd_min': d_golay, 'self_dual': True, 'avg_phi_mc': float(ap_golay),
     'dist_hist': dict(hist_golay)},
] + sd_records + random_records

golay_ap = float(ap_golay)
sd_aps = [r['avg_phi_mc'] for r in sd_records]
random_aps = [r['avg_phi_mc'] for r in random_records]
print(f'  Golay [24,12,8]:              {golay_ap:.6f}')
if sd_aps:
    print(f'  Random self-dual [24,12]:     [{min(sd_aps):.6f}, {max(sd_aps):.6f}], mean {sum(sd_aps)/len(sd_aps):.6f}')
if random_aps:
    print(f'  Random non-SD [24,12]:        [{min(random_aps):.6f}, {max(random_aps):.6f}], mean {sum(random_aps)/len(random_aps):.6f}')
all_others = sd_aps + random_aps
if all_others:
    best_other = max(all_others)
    print(f'  Best non-Golay: {best_other:.6f}')
    print(f'  Golay margin over best non-Golay: {golay_ap - best_other:+.6f}')
    print(f'  Golay is highest? {golay_ap > best_other}')

# d_min distribution
print('\n--- d_min distribution ---')
for r in all_results:
    sd_label = 'SD' if r['self_dual'] else 'NSD'
    print(f'  {r["name"]:<30s}  d={r["d_min"]:>2d}  {sd_label}  avg_Phi={r["avg_phi_mc"]:.6f}')

with open('/home/z/my-project/work/sd24_results.json', 'w') as f:
    json.dump({'results': all_results}, f, indent=2)
print('\nSaved to sd24_results.json')
