"""
THREAD F: [24,12,8] Sampling -- Random vs Self-Dual vs Golay (Open Q5)
=======================================================================

EXTREMAL_003 left this open: "avg_Phi test on [24,12,8] codes vs Golay
(sampled, not exhaustive)."

Strategy:
  1. Golay [24,12,8] is the unique d=8 self-dual code at these parameters.
  2. Sample random [24,12] codes (typically d=1 or d=2).
  3. Sample random self-dual [24,12] codes (via Construction A or random
     self-dual generator construction) -- their d_min will be 2, 4, or 6
     typically; d=8 is rare (= Golay-equivalent).
  4. Monte Carlo avg_Phi for each.

For self-dual code generation: a binary linear code C is self-dual iff
its generator matrix G (k x n) satisfies G * G^T = 0 over GF(2) and
rank(G) = k = n/2. We construct such G by:
  - Choose a random k x n matrix M.
  - Find its row-reduced form, then enforce orthogonality by Gram-Schmidt
    over GF(2).

A simpler approach: use Construction A. A self-dual code of length n=24
can be constructed from a random invertible 12x12 matrix B by:
  G = [I_12 | B]  where B satisfies B * B^T = I_12 mod 2 ... actually that's
  for orthogonal, not self-dual. For self-dual we need B * B^T = B^T * B = B
  symmetric? No.

Self-dual code with generator G = [I | B]: C is self-dual iff
G * G^T = 0, i.e. I + B * B^T = 0, i.e. B * B^T = I (over GF(2)).
So B must be an orthogonal matrix over GF(2).

Random orthogonal matrices over GF(2) form a group; we can generate one
by composing random reflections, or by rejection sampling: pick random
B, check if B * B^T = I.

Acceptance rate for random 12x12 B: |O(12, F_2)| / |GL(12, F_2)|.
This is small but workable for small samples.
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

def random_generator(k, n, rng):
    while True:
        G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
        if rank_gf2(G) == k: return G

def random_orthogonal_B(k, rng, max_attempts=1000):
    """Generate a random k x k orthogonal matrix B over GF(2): B * B^T = I."""
    for _ in range(max_attempts):
        B = [[rng.randint(0, 1) for _ in range(k)] for _ in range(k)]
        if rank_gf2(B) != k: continue
        # Check B * B^T = I over GF(2)
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
    """Generate G = [I_k | B] where B is k x k orthogonal over GF(2)."""
    assert n == 2 * k
    B = random_orthogonal_B(k, rng)
    if B is None: return None
    G = []
    for i in range(k):
        row = [0] * k + B[i]
        G.append(row)
    return G

def all_codewords_np(G, k, n):
    cw_list = []
    for bits in product([0, 1], repeat=k):
        cw_list.append([sum(G[i][j] for i, b in enumerate(bits) if b) & 1 for j in range(n)])
    return np.array(cw_list, dtype=np.uint8)

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

def is_self_dual(G, k, n):
    if k != n - k: return False
    if rank_gf2(G) != k: return False
    for i in range(k):
        for j in range(i, k):
            dot = sum(G[i][t] * G[j][t] for t in range(n)) & 1
            if dot != 0: return False
    return True


print('=' * 72)
print('THREAD F: [24,12,8] sampling -- Random vs Self-Dual vs Golay')
print('=' * 72)

# Golay [24,12,8]
g24 = GolayCodeEngine()
all_cw_24 = np.array(g24.get_all_codewords(), dtype=np.uint8)
print(f'\nGolay [24,12,8]: {all_cw_24.shape[0]} codewords, d_min = {d_min_np(all_cw_24)}')
print(f'  is_self_dual: {is_self_dual([list(c) for c in all_cw_24[:12]], 12, 24)}')
# Check self-dual using the parity-check matrix approach: G = [I | B] form?
# Easier: check that all codewords are pairwise orthogonal
def check_self_dual_fast(cw_arr):
    # Sample-check: 100 random codeword pairs
    n = cw_arr.shape[0]
    rng = np.random.default_rng(0)
    for _ in range(200):
        i, j = rng.integers(0, n, size=2)
        dot = (cw_arr[i] & cw_arr[j]).sum() & 1
        if dot != 0: return False
    return True
print(f'  self-dual (sample check): {check_self_dual_fast(all_cw_24)}')

rng = random.Random(20260624)

print(f'\n{"name":<30s}  {"d_min":>5s}  {"self_dual":>10s}  {"avg_Phi":>10s}  {"dist_hist":<35s}')
print('-' * 100)

all_results = []

# Golay
t0 = time.time()
ap_golay, hist_golay = monte_carlo_avg_phi_fast(all_cw_24, 24, 15_000, seed=1)
t1 = time.time()
hist_top = dict(sorted(hist_golay.items())[:6])
print(f'{"Golay[24,12,8]":<30s}  {d_min_np(all_cw_24):>5d}  {str(True):>10s}  {ap_golay:>10.6f}  {hist_top}')
print(f'  (computed in {t1-t0:.1f}s)')
all_results.append({'name': 'Golay[24,12,8]', 'd_min': 8, 'self_dual': True, 'avg_phi_mc': ap_golay,
                    'dist_hist': dict(hist_golay), 'samples': 15_000})

# Random [24,12] codes
print()
for i in range(4):
    G = random_generator(12, 24, rng)
    cw_arr = all_codewords_np(G, 12, 24)
    d = d_min_np(cw_arr)
    t0 = time.time()
    ap, hist = monte_carlo_avg_phi_fast(cw_arr, 24, 15_000, seed=i+10)
    t1 = time.time()
    name = f'Random[24,12]#{i+1}'
    hist_top = dict(sorted(hist.items())[:6])
    print(f'{name:<30s}  {d:>5d}  {str(False):>10s}  {ap:>10.6f}  {hist_top}')
    print(f'  (computed in {t1-t0:.1f}s)')
    all_results.append({'name': name, 'd_min': d, 'self_dual': False, 'avg_phi_mc': ap,
                        'dist_hist': dict(hist), 'samples': 15_000})

# Random self-dual [24,12] codes
print()
print('Generating random self-dual [24,12] codes via G = [I | B], B orthogonal...')
n_sd_attempted = 0
n_sd_generated = 0
for i in range(10):
    G = random_self_dual_generator(12, 24, rng)
    if G is None:
        print(f'  Attempt {i+1}: failed to generate orthogonal B')
        continue
    n_sd_attempted += 1
    cw_arr = all_codewords_np(G, 12, 24)
    d = d_min_np(cw_arr)
    sd_check = is_self_dual(G, 12, 24)
    if not sd_check:
        print(f'  Attempt {i+1}: G failed self-dual verification, skipping')
        continue
    n_sd_generated += 1
    t0 = time.time()
    ap, hist = monte_carlo_avg_phi_fast(cw_arr, 24, 15_000, seed=i+100)
    t1 = time.time()
    name = f'SelfDual[24,12]#{n_sd_generated}'
    hist_top = dict(sorted(hist.items())[:6])
    print(f'{name:<30s}  {d:>5d}  {str(sd_check):>10s}  {ap:>10.6f}  {hist_top}')
    print(f'  (computed in {t1-t0:.1f}s)')
    all_results.append({'name': name, 'd_min': d, 'self_dual': sd_check, 'avg_phi_mc': ap,
                        'dist_hist': dict(hist), 'samples': 15_000})
    if n_sd_generated >= 4:
        break

# Summary
print('\n--- Summary ---')
golay_ap = all_results[0]['avg_phi_mc']
print(f'  Golay [24,12,8]:              {golay_ap:.6f}')
random_aps = [r['avg_phi_mc'] for r in all_results if not r['self_dual']]
sd_aps = [r['avg_phi_mc'] for r in all_results[1:] if r['self_dual']]
if random_aps:
    print(f'  Random [24,12] (non-self-dual): [{min(random_aps):.6f}, {max(random_aps):.6f}], mean {sum(random_aps)/len(random_aps):.6f}')
if sd_aps:
    print(f'  Random self-dual [24,12]:       [{min(sd_aps):.6f}, {max(sd_aps):.6f}], mean {sum(sd_aps)/len(sd_aps):.6f}')
all_others = random_aps + sd_aps
if all_others:
    best_other = max(all_others)
    print(f'  Best non-Golay: {best_other:.6f}')
    print(f'  Golay margin over best non-Golay: {golay_ap - best_other:+.6f}')
    print(f'  Golay is highest? {golay_ap > best_other}')

# d_min distribution
print('\n--- d_min distribution ---')
for r in all_results:
    print(f'  {r["name"]:<30s}  d_min={r["d_min"]:>2d}  self_dual={r["self_dual"]}  avg_Phi={r["avg_phi_mc"]:.6f}')

with open('/home/z/my-project/work/golay24_results.json', 'w') as f:
    json.dump({'results': all_results}, f, indent=2)
print('\nSaved to golay24_results.json')
