"""
THREAD K: Generate Doubly-Even Self-Dual [16,8] Codes -- Test Refined Conjecture
=================================================================================

EXTREMAL_004 proposed a refined conjecture (slide 14):
  Among [n, n/2] binary linear codes, DOUBLY-EVEN self-dual codes uniquely
  maximise avg_Phi -- provided such a code exists.

Evidence so far:
  n=8:  ExtHamming [8,4,4] (DE SD) WINS.
  n=16: E8+E8 [16,8,4] (SE SD) LOSES. (singly-even, not doubly-even)
  n=24: Golay [24,12,8] (DE SD) WINS.

To test the refined conjecture at n=16, we need to generate random DOUBLY-EVEN
self-dual [16,8] codes and check if they beat:
  (a) E8+E8 (the singly-even self-dual baseline), and
  (b) random non-self-dual d=4 codes (which beat E8+E8 in Thread H).

METHOD:
  A binary [n, n/2] code C is doubly-even self-dual iff:
    (1) C is self-dual: C = C^perp, i.e. G * G^T = 0 mod 2, rank(G) = n/2.
    (2) Every codeword has weight divisible by 4 (doubly-even).

  A standard construction: take the generator matrix G = [I_k | B] where B
  is a symmetric k x k matrix over GF(2) with:
    - diagonal entries all 0 (so that the row vectors have even weight:
      I_k contributes weight 1, B row contributes weight = (sum of B row) +
      diagonal 0, so total weight = 1 + sum(B row). For doubly-even, need
      1 + sum(B row) = 0 mod 4. Hmm, that's a constraint on B.
    - For self-duality, B * B^T = I + something... actually let me reconsider.

  Actually, for G = [I | B], the rows of G have weight 1 + HW(B_row).
  Self-dual requires every pair of rows orthogonal mod 2:
    <row_i, row_j> = (I_i . I_j) + (B_i . B_j) = delta_ij + (B_i . B_j) = 0 mod 2
    So for i != j: B_i . B_j = 0 mod 2
    For i = j: 1 + HW(B_i) = 0 mod 2, i.e. HW(B_i) is odd.

  For doubly-even, every codeword (not just rows) must have weight divisible by 4.
  Codewords are sums of rows: sum over a subset S of rows.
  Weight of codeword = HW( sum_{i in S} (I_i + B_i) ) = HW(S) + HW( sum_{i in S} B_i ) - 2 * (overlap)
  This is complex.

  ALTERNATIVE: Use known construction. The doubly-even self-dual [16,8,4] code
  is the Barnes-Wall lattice code (or equivalently, the Reed-Muller RM(1,4)
  with a different extension). Its generator matrix is:

  G_BW_16 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
    [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
    [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],  # ???
    ...
  ]

  This is getting complicated. Let me use a different approach: SAMPLE
  self-dual [16,8] codes via G = [I_8 | B] with B orthogonal, then FILTER
  for doubly-even (all codeword weights divisible by 4).

  For G = [I_8 | B] with B orthogonal (B * B^T = I mod 2):
    Row i has weight 1 + HW(B_i).
    For doubly-even: 1 + HW(B_i) = 0 mod 4, so HW(B_i) = 3 mod 4.
    But this is necessary for ROWS, not sufficient for all codewords.

  Simpler approach: construct via the standard doubling construction.
  Given a self-dual [n, n/2] code C, we can construct a doubly-even self-dual
  [2n, n] code via a specific doubling matrix. But for n=16 starting from
  smaller codes, we'd need to start from n=4 or n=8.

  EVEN SIMPLER: just brute-force search. Enumerate random self-dual [16,8]
  codes via G = [I | B] with B orthogonal, then check which are doubly-even.
  The acceptance rate for "doubly-even" among self-dual codes is non-trivial
  but tractable for small samples.
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

def is_doubly_even(cw_arr):
    """Check that all codeword weights are divisible by 4 (excluding weight 0)."""
    weights = cw_arr.sum(axis=1)
    nonzero_weights = weights[weights > 0]
    return int((nonzero_weights % 4 == 0).all())

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


# Also need the canonical doubly-even [16,8,4] code: RM(1,4) extended? Actually
# RM(1,4) is [16,5,8] not [16,8,4]. The [16,8,4] DE self-dual code is the
# "Barnes-Wall" code or the "2x2 extended Hamming" construction.
# Standard construction: take [8,4,4] ExtHamming, build [16,8,4] via the doubling:
#   G_16 = [G_8 | 0; G_8 | G_8] where G_8 is the [8,4,4] generator
# This gives a [16,8,4] code with all weights divisible by 4 (doubly-even).

def build_doubly_even_16():
    """Construct a [16,8,4] doubly-even self-dual code via doubling ExtHamming."""
    G_8 = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
    ]
    # Doubling: G_16 = [G_8 0; G_8 G_8] -- this is 8x16
    G_16 = []
    for row in G_8:
        G_16.append(row + [0]*8)
    for row in G_8:
        G_16.append(row + row)  # [G_8 G_8]
    return G_16


print('=' * 72)
print('THREAD K: Doubly-Even Self-Dual [16,8] Codes -- Test Refined Conjecture')
print('=' * 72)

# Build canonical doubly-even [16,8,4] code
G_de16 = build_doubly_even_16()
cw_de16 = all_codewords_np(G_de16, 8, 16)
d_de16 = d_min_np(cw_de16)
de_de16 = is_doubly_even(cw_de16)
sd_de16 = is_self_dual(G_de16, 8, 16)
print(f'\nCanonical DE [16,8,4] code (doubling ExtHamming):')
print(f'  d_min = {d_de16}')
print(f'  is_doubly_even = {de_de16}')
print(f'  is_self_dual = {sd_de16}')

ap_de16, hist_de16 = monte_carlo_avg_phi_fast(cw_de16, 16, 20_000, seed=0)
print(f'  avg_Phi (Monte Carlo 20k) = {ap_de16:.6f}')
print(f'  dist hist: {dict(sorted(hist_de16.items()))}')

# Build E8+E8 [16,8,4] (singly-even self-dual) for comparison
G_e8e8 = []
G_8 = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
]
for row in G_8:
    G_e8e8.append(row + [0]*8)
for row in G_8:
    G_e8e8.append([0]*8 + row)
cw_e8e8 = all_codewords_np(G_e8e8, 8, 16)
d_e8e8 = d_min_np(cw_e8e8)
de_e8e8 = is_doubly_even(cw_e8e8)
sd_e8e8 = is_self_dual(G_e8e8, 8, 16)
ap_e8e8, hist_e8e8 = monte_carlo_avg_phi_fast(cw_e8e8, 16, 20_000, seed=1)
print(f'\nE8+E8 [16,8,4] (singly-even self-dual):')
print(f'  d_min = {d_e8e8}, is_doubly_even = {de_e8e8}, is_self_dual = {sd_e8e8}')
print(f'  avg_Phi = {ap_e8e8:.6f}')

# Sample random [16,8] codes
rng = random.Random(20260627)
print('\n--- Sampling 80 random [16,8] codes ---')
records = []
for i in range(80):
    G = random_generator(8, 16, rng)
    cw = all_codewords_np(G, 8, 16)
    d = d_min_np(cw)
    sd = is_self_dual(G, 8, 16)
    de = is_doubly_even(cw)
    ap, _ = monte_carlo_avg_phi_fast(cw, 16, 10_000, seed=i+10)
    records.append({'name': f'Random[16,8]#{i+1}', 'd_min': d, 'self_dual': sd,
                    'doubly_even': de, 'avg_phi': float(ap)})
    if (i+1) % 20 == 0:
        print(f'  {i+1}/80 done')

# Try to generate random DE self-dual codes by rejection sampling
print('\n--- Attempting random DE self-dual [16,8] generation ---')
n_de_sd = 0
n_attempts = 0
de_sd_records = []
while n_de_sd < 5 and n_attempts < 2000:
    n_attempts += 1
    G = random_self_dual_generator(8, 16, rng)
    if G is None: continue
    cw = all_codewords_np(G, 8, 16)
    if not is_self_dual(G, 8, 16): continue
    if not is_doubly_even(cw): continue
    n_de_sd += 1
    d = d_min_np(cw)
    ap, _ = monte_carlo_avg_phi_fast(cw, 16, 10_000, seed=2000+n_de_sd)
    de_sd_records.append({'name': f'DESD[16,8]#{n_de_sd}', 'd_min': d,
                          'self_dual': True, 'doubly_even': True, 'avg_phi': float(ap)})
    print(f'  Generated DESD #{n_de_sd} (d={d}, avg_Phi={ap:.6f}) -- attempt {n_attempts}')

print(f'\n  Acceptance rate: {n_de_sd}/{n_attempts} = {n_de_sd/max(n_attempts,1)*100:.2f}%')

# Add canonical and DE-SD records
all_records = [
    {'name': 'DE[16,8,4] canonical', 'd_min': d_de16, 'self_dual': sd_de16,
     'doubly_even': de_de16, 'avg_phi': float(ap_de16)},
    {'name': 'E8+E8[16,8,4]', 'd_min': d_e8e8, 'self_dual': sd_e8e8,
     'doubly_even': de_e8e8, 'avg_phi': float(ap_e8e8)},
] + de_sd_records + records

# Summary
print('\n--- Summary by category ---')
groups = defaultdict(list)
for r in all_records:
    key = (r['self_dual'], r['doubly_even'], r['d_min'])
    groups[key].append(r['avg_phi'])
for (sd, de, d), phis in sorted(groups.items(), key=lambda x: (-x[0][0], -x[0][1], -x[0][2])):
    sd_label = 'SD' if sd else 'NSD'
    de_label = 'DE' if de else 'SE'
    print(f'  {sd_label} {de_label} d={d}: n={len(phis):>3d}  '
          f'avg_Phi range [{min(phis):.5f}, {max(phis):.5f}]  mean {sum(phis)/len(phis):.5f}')

# Direct comparison: canonical DE vs E8+E8 vs best random d=4
print('\n--- Direct comparison: canonical DE [16,8,4] vs E8+E8 vs best random d=4 ---')
print(f'  DE [16,8,4] canonical (DE SD):  {float(ap_de16):.6f}')
print(f'  E8+E8 [16,8,4] (SE SD):         {float(ap_e8e8):.6f}')
print(f'  Best random NSD d=4:            {max(r["avg_phi"] for r in records if r["d_min"] == 4 and not r["self_dual"]):.6f}')

# Top 10
print('\n--- Top 10 by avg_Phi ---')
top10 = sorted(all_records, key=lambda r: -r['avg_phi'])[:10]
for r in top10:
    sd_label = 'SD' if r['self_dual'] else 'NSD'
    de_label = 'DE' if r.get('doubly_even', False) else 'SE'
    print(f'  {r["name"]:<28s}  d={r["d_min"]}  {sd_label} {de_label}  avg_Phi={r["avg_phi"]:.6f}')

# Save
with open('/home/z/my-project/work/refined_sd_results.json', 'w') as f:
    json.dump({
        'canonical_de': {'name': 'DE[16,8,4] canonical', 'd_min': d_de16, 'self_dual': sd_de16,
                          'doubly_even': de_de16, 'avg_phi': float(ap_de16)},
        'e8_plus_e8': {'name': 'E8+E8[16,8,4]', 'd_min': d_e8e8, 'self_dual': sd_e8e8,
                       'doubly_even': de_e8e8, 'avg_phi': float(ap_e8e8)},
        'de_sd_random': de_sd_records,
        'random_codes': records,
    }, f, indent=2)
print('\nSaved to refined_sd_results.json')
