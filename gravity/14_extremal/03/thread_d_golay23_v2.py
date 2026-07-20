"""
THREAD D (v2): Faster Monte Carlo for [23,12] codes.
Uses numpy for batched distance computation.
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
# Float versions for fast Monte Carlo
Y_f = float(Y)
Y_18_f = float(Y_plus_one_eighth)
PHI_PEAK_f = float(PHI_PEAK)
BETA = Y_f / Y_18_f  # weight on dist/HW

def phi_with_dist_f(h_state, dist):
    if h_state == 0: return 0.0
    denom = h_state * Y_18_f + dist * Y_f
    return h_state / denom


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
    """Generate all 2^k codewords as a numpy array of shape (2^k, n) of uint8."""
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


def monte_carlo_avg_phi_fast(cw_arr, n, n_trials=20_000, seed=0):
    """
    Fast Monte Carlo: sample n_trials random vectors, compute min distance to
    each codeword via numpy, accumulate Phi in float.
    Returns (avg_phi_float, dist_histogram Counter).
    """
    rng = np.random.default_rng(seed)
    cw_arr = cw_arr.astype(np.uint8)
    n_cw = cw_arr.shape[0]
    # Pack codewords into bytes for fast XOR distance
    # For [23,12], n=23 fits in 4 bytes (32 bits). Use uint32 with XOR + popcount.
    # Pad each codeword to 32 bits, then xor and popcount.
    PAD = 32
    cw_padded = np.zeros((n_cw, PAD), dtype=np.uint8)
    cw_padded[:, :n] = cw_arr
    # Pack into uint32 (little-endian)
    cw_packed = np.packbits(cw_padded, axis=1).view(np.uint32).reshape(n_cw)

    total_phi = 0.0
    dist_hist = Counter()
    BATCH = 500
    remaining = n_trials
    while remaining > 0:
        b = min(BATCH, remaining)
        # Sample b random vectors
        vs = rng.integers(0, 2, size=(b, n), dtype=np.uint8)
        # Pad to 32 bits
        vs_padded = np.zeros((b, PAD), dtype=np.uint8)
        vs_padded[:, :n] = vs
        vs_packed = np.packbits(vs_padded, axis=1).view(np.uint32).reshape(b)

        # Compute HW(v) for each v
        hw_v = vs.sum(axis=1).astype(np.int32)

        # For each v, compute min distance to any codeword
        # XOR each v with each codeword, popcount, find min
        # Broadcasting: (b, 1) ^ (1, n_cw) -> (b, n_cw)
        xor = vs_packed[:, None] ^ cw_packed[None, :]
        # Popcount on uint32
        # numpy has bit_count() in 3.10+ for uint -- let me check
        # For Python 3.10+, np.uint32 has .bit_count() since numpy 2.0
        try:
            dists = xor.view(np.uint64).bit_count()  # may not work for uint32
        except AttributeError:
            # Fallback: use np.unpackbits
            dists = np.unpackbits(xor.view(np.uint8).reshape(b, n_cw, 4), axis=2).sum(axis=2)

        # Find min distance per v
        min_dists = dists.min(axis=1).astype(np.int32)

        # Check if v is itself a codeword (min_dist == 0)
        is_cw = (min_dists == 0)

        # Compute Phi for each v
        # If is_cw: phi = PHI_PEAK (assuming HW > 0; if HW == 0, phi = 0)
        # Else: phi = hw_v / (hw_v * Y_18 + min_dists * Y)
        phis = np.where(
            is_cw,
            np.where(hw_v > 0, PHI_PEAK_f, 0.0),
            np.where(hw_v > 0, hw_v / (hw_v * Y_18_f + min_dists * Y_f), 0.0)
        )
        total_phi += phis.sum()

        # Update distance histogram
        for md in min_dists:
            dist_hist[int(md)] += 1

        remaining -= b

    return total_phi / n_trials, dist_hist


print('=' * 72)
print('THREAD D (v2): [23,12] sampling -- Golay[23,12,7] vs random [23,12] codes')
print('=' * 72)

g24 = GolayCodeEngine()
all_cw_24 = g24.get_all_codewords()
all_cw_23 = np.array([cw[:-1] for cw in all_cw_24], dtype=np.uint8)
print(f'\nPunctured Golay [23,12] code:')
print(f'  Number of codewords: {all_cw_23.shape[0]} (expected 4096)')
d_punct = d_min_np(all_cw_23)
print(f'  d_min: {d_punct} (expected 7 for perfect Golay)')

# Test perfectness
rng = random.Random(20260624)
PERFECT_TEST = 10_000
max_dist = 0
cw_set = set(tuple(int(x) for x in c) for c in all_cw_23)
for _ in range(PERFECT_TEST):
    v = tuple(rng.randint(0, 1) for _ in range(23))
    if sum(v) == 0: continue
    if v in cw_set: continue
    md = min(sum((a + b) & 1 for a, b in zip(v, c)) for c in cw_set)
    max_dist = max(max_dist, md)
print(f'  Perfectness check (10^4 random vectors): max dist to nearest codeword = {max_dist}')

print('\n--- Monte Carlo avg_Phi (20,000 samples per code) ---')
print(f'{"name":<25s}  {"d_min":>5s}  {"avg_Phi":>10s}  {"dist histogram":<40s}')
print('-' * 90)

all_results = []

t0 = time.time()
ap_golay, hist_golay = monte_carlo_avg_phi_fast(all_cw_23, 23, 20_000, seed=1)
t1 = time.time()
hist_top6 = dict(sorted(hist_golay.items())[:6])
print(f'{"Golay[23,12,7]":<25s}  {d_punct:>5d}  {ap_golay:>10.6f}  {hist_top6}')
print(f'  (computed in {t1-t0:.1f}s)')
all_results.append({
    'name': 'Golay[23,12,7]', 'd_min': d_punct, 'avg_phi_mc': ap_golay,
    'dist_hist': dict(hist_golay), 'samples': 20_000,
})

for i in range(5):
    G = random_generator(12, 23, rng)
    cw_arr = all_codewords_np(G, 12, 23)
    d = d_min_np(cw_arr)
    t0 = time.time()
    ap, hist = monte_carlo_avg_phi_fast(cw_arr, 23, 20_000, seed=i+10)
    t1 = time.time()
    name = f'Random[23,12]#{i+1}'
    hist_top6 = dict(sorted(hist.items())[:6])
    print(f'{name:<25s}  {d:>5d}  {ap:>10.6f}  {hist_top6}')
    print(f'  (computed in {t1-t0:.1f}s)')
    all_results.append({
        'name': name, 'd_min': d, 'avg_phi_mc': ap,
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

print('\n--- Distance histogram comparison ---')
print(f'  Golay:    {dict(sorted(all_results[0]["dist_hist"].items()))}')
for r in all_results[1:4]:
    print(f'  {r["name"]:<20s} d_min={r["d_min"]}: {dict(sorted(r["dist_hist"].items()))}')

with open('/home/z/my-project/work/golay23_results.json', 'w') as f:
    json.dump({'results': all_results}, f, indent=2)
print('\nSaved to golay23_results.json')
