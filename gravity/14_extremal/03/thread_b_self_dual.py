"""
THREAD B: Self-Dual Extension Test
====================================

CONVERSE_001 Section 9 left this as Priority 2:
  "Is avg_Phi maximised (over all codes of length n) by self-dual codes?
   If yes, this would provide a Phi-motivated derivation of self-duality
   and hence k = n/2."

We test exhaustively for small n (4, 6, 8) where enumeration of self-dual codes
is tractable. For each n we:

  1. Enumerate many [n, n/2] linear codes (random generator matrices).
  2. Classify each as self-dual or not.
  3. Compute avg_Phi for each (over all 2^n vectors).
  4. Compare distributions.

We also include Hamming [8,4,4] (extended Hamming code = first-order Reed-Muller
[8,4,4], self-dual) as the canonical reference.

For larger n we cannot enumerate all codes, so we sample.
"""
import sys, random, time
from fractions import Fraction
from itertools import product
from collections import Counter
sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics

pp = UBPSourceCodeParticlePhysics()
Y = pp.Y
Y_plus_one_eighth = Y + Fraction(1, 8)
PHI_PEAK = Fraction(1, 1) / Y_plus_one_eighth


def hw(v): return sum(1 for x in v if x)

def phi_with_dist(h_state: int, dist: int) -> Fraction:
    """Phi for a state of Hamming weight h_state with min distance dist to nearest codeword."""
    if h_state == 0:
        return Fraction(0)
    denom = Fraction(h_state) * Y_plus_one_eighth + Fraction(dist) * Y
    return Fraction(h_state) / denom


# ---- Linear-code utilities over GF(2) ----
def rref_gf2(M):
    """Reduced row echelon form over GF(2). M is list of rows of 0/1 ints."""
    M = [row[:] for row in M]
    rows = len(M); cols = len(M[0]) if rows else 0
    r = 0
    pivots = []
    for c in range(cols):
        pivot_row = None
        for rr in range(r, rows):
            if M[rr][c] == 1:
                pivot_row = rr
                break
        if pivot_row is None:
            continue
        M[r], M[pivot_row] = M[pivot_row], M[r]
        for rr in range(rows):
            if rr != r and M[rr][c] == 1:
                M[rr] = [(a + b) & 1 for a, b in zip(M[rr], M[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return M, pivots

def rank_gf2(M):
    _, pivots = rref_gf2(M)
    return len(pivots)

def row_reduce_to_basis(M):
    """Return the row-space basis of M over GF(2)."""
    M, pivots = rref_gf2(M)
    return [row for row in M if any(row)]  # nonzero rows

def all_codewords(G, k, n):
    """Generate all 2^k codewords from generator matrix G (k x n)."""
    cw = []
    for bits in product([0, 1], repeat=k):
        cw.append([sum(G[i][j] for i, b in enumerate(bits) if b) & 1 for j in range(n)])
    return cw

def is_self_dual(G, k, n):
    """
    A linear [n,k] code C with generator matrix G is self-dual iff
    C = C^perp, which requires:
      (a) k = n/2
      (b) every pair of rows of G is orthogonal (G * G^T = 0 over GF(2))
      (c) rows of G have full rank k
    (b)+(c) imply C subset C^perp, and dim C = n/2 = dim C^perp, hence C = C^perp.
    """
    if k != n - k:
        return False
    if rank_gf2(G) != k:
        return False
    for i in range(k):
        for j in range(i, k):
            dot = sum(G[i][t] * G[j][t] for t in range(n)) & 1
            if dot != 0:
                return False
    return True

def d_min(codewords):
    """Minimum distance of a code from its codeword list."""
    nonzero = [c for c in codewords if sum(c) > 0]
    if not nonzero:
        return 0
    d = float('inf')
    for c in nonzero:
        d = min(d, sum(c))
    return d

def avg_phi(codewords, n):
    """Compute avg_Phi(C) = (1/2^n) * sum_v Phi(v, C).
    For each v in F_2^n, find min dist to any codeword, then Phi.
    For n <= 10 this is exhaustive."""
    # Build a set of codeword tuples for fast membership
    cw_set = set(tuple(c) for c in codewords)
    total = Fraction(0)
    for v in product([0, 1], repeat=n):
        h = sum(v)
        if h == 0:
            continue  # Phi = 0
        if tuple(v) in cw_set:
            phi = PHI_PEAK
        else:
            # find min dist
            md = min(sum((a + b) & 1 for a, b in zip(v, c)) for c in codewords)
            phi = phi_with_dist(h, md)
        total += phi
    return Fraction(total, 1 << n)


def random_generator(k, n, rng):
    """Generate a random k x n binary matrix with full row rank k."""
    while True:
        G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
        if rank_gf2(G) == k:
            return G


print('=' * 72)
print('THREAD B: Self-Dual Extension Test')
print('   Question: does self-duality maximise avg_Phi for fixed n?')
print('=' * 72)

rng = random.Random(20260624)

results = {}
for n in [4, 6, 8, 10]:
    k = n // 2
    n_samples = 400 if n <= 8 else 80
    print(f'\n--- n={n}, k={k}, sampling {n_samples} random [n,k] codes ---')

    self_dual = []
    not_self_dual = []

    t0 = time.time()
    for trial in range(n_samples):
        G = random_generator(k, n, rng)
        sd = is_self_dual(G, k, n)
        cw = all_codewords(G, k, n)
        ap = avg_phi(cw, n)
        d = d_min(cw)
        rec = {'avg_phi': float(ap), 'd_min': d, 'self_dual': sd, 'G': G}
        if sd:
            self_dual.append(rec)
        else:
            not_self_dual.append(rec)
    t1 = time.time()

    sd_phis = [r['avg_phi'] for r in self_dual]
    nsd_phis = [r['avg_phi'] for r in not_self_dual]
    sd_dmins = [r['d_min'] for r in self_dual]
    nsd_dmins = [r['d_min'] for r in not_self_dual]

    print(f'  Time: {t1-t0:.1f}s')
    print(f'  Self-dual codes found:   {len(self_dual):>4d}   avg_Phi range: '
          f'[{min(sd_phis):.5f}, {max(sd_phis):.5f}]  d_min range: {min(sd_dmins)}..{max(sd_dmins)}'
          if sd_phis else
          f'  Self-dual codes found:   {len(self_dual):>4d}')
    print(f'  Non-self-dual codes:     {len(not_self_dual):>4d}   avg_Phi range: '
          f'[{min(nsd_phis):.5f}, {max(nsd_phis):.5f}]  d_min range: {min(nsd_dmins)}..{max(nsd_dmins)}'
          if nsd_phis else
          f'  Non-self-dual codes:     {len(not_self_dual):>4d}')

    # Highest avg_Phi
    all_recs = self_dual + not_self_dual
    best = max(all_recs, key=lambda r: r['avg_phi'])
    worst = min(all_recs, key=lambda r: r['avg_phi'])
    print(f'  Best avg_Phi:  {best["avg_phi"]:.5f}  self_dual={best["self_dual"]}  d_min={best["d_min"]}')
    print(f'  Worst avg_Phi: {worst["avg_phi"]:.5f}  self_dual={worst["self_dual"]}  d_min={worst["d_min"]}')

    if sd_phis and nsd_phis:
        sd_mean = sum(sd_phis) / len(sd_phis)
        nsd_mean = sum(nsd_phis) / len(nsd_phis)
        print(f'  Mean avg_Phi: self-dual={sd_mean:.5f}  non-self-dual={nsd_mean:.5f}  delta={sd_mean-nsd_mean:+.5f}')
        if sd_mean > nsd_mean:
            print(f'  >> Self-dual codes have HIGHER mean avg_Phi (consistent with conjecture)')
        else:
            print(f'  >> Self-dual codes have LOWER mean avg_Phi (against conjecture)')

    # Top-5 by avg_Phi
    top5 = sorted(all_recs, key=lambda r: -r['avg_phi'])[:5]
    sd_in_top = sum(1 for r in top5 if r['self_dual'])
    print(f'  Top-5 by avg_Phi: {sd_in_top}/5 are self-dual')
    results[n] = {
        'n_samples': n_samples,
        'n_self_dual': len(self_dual),
        'n_not_self_dual': len(not_self_dual),
        'sd_avg_phi_range': (min(sd_phis), max(sd_phis)) if sd_phis else None,
        'nsd_avg_phi_range': (min(nsd_phis), max(nsd_phis)) if nsd_phis else None,
        'sd_mean': (sum(sd_phis)/len(sd_phis)) if sd_phis else None,
        'nsd_mean': (sum(nsd_phis)/len(nsd_phis)) if nsd_phis else None,
        'top5_self_dual_count': sd_in_top,
        'best_avg_phi': best['avg_phi'],
        'best_is_self_dual': best['self_dual'],
    }

# Also explicitly test the [8,4,4] extended Hamming code (well-known self-dual)
print('\n--- Explicit check: Extended Hamming [8,4,4] (self-dual) ---')
# Standard generator for [8,4,4] extended Hamming (= first-order Reed-Muller RM(1,3))
G_hamming = [
    [1, 1, 1, 1, 1, 1, 1, 1],   # all-ones
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
]
print(f'  is_self_dual: {is_self_dual(G_hamming, 4, 8)}')
cw = all_codewords(G_hamming, 4, 8)
ap = avg_phi(cw, 8)
d = d_min(cw)
print(f'  d_min: {d}')
print(f'  avg_Phi: {float(ap):.6f}')

# Compare extended Hamming avg_Phi to random [8,4] codes from the earlier sample
print('\n--- Direct comparison: Extended Hamming [8,4,4] vs random [8,4] codes ---')
# Re-sample [8,4] codes (this time without restricting to self-dual filtering)
rng2 = random.Random(20260625)
print(f'{"name":<30s}  {"d_min":>5s}  {"avg_Phi":>10s}  {"is_self_dual":>14s}')
print('-' * 70)
print(f'{"ExtHamming[8,4,4]":<30s}  {d:>5d}  {float(ap):>10.6f}  {True:>14}')
random_codes = []
for i in range(30):
    G = random_generator(4, 8, rng2)
    cw_r = all_codewords(G, 4, 8)
    ap_r = avg_phi(cw_r, 8)
    d_r = d_min(cw_r)
    sd_r = is_self_dual(G, 4, 8)
    random_codes.append((ap_r, d_r, sd_r))
    print(f'{"Random[8,4]#"+str(i+1):<30s}  {d_r:>5d}  {float(ap_r):>10.6f}  {sd_r:>14}')
all_ap_r = [float(ap)] + [float(r[0]) for r in random_codes]
all_d_r = [d] + [r[1] for r in random_codes]
all_sd_r = [True] + [r[2] for r in random_codes]
# Find codes with d >= 4 (the d_min of ExtHamming)
d4_codes = [(a, b, c) for a, b, c in zip(all_ap_r, all_d_r, all_sd_r) if b >= 4]
print(f'\n  Codes with d_min >= 4: {len(d4_codes)}')
for a, b, c in sorted(d4_codes, key=lambda x: -x[0]):
    print(f'    avg_Phi={a:.6f}  d_min={b}  self_dual={c}')
print(f'  Among d>=4 codes, the BEST is {"ExtHamming" if d4_codes[0][2] else "random"}')

# Save results
import json
with open('/home/z/my-project/work/self_dual_results.json', 'w') as f:
    json.dump({'results': results,
               'extended_hamming_avg_phi': float(ap),
               'extended_hamming_dmin': d}, f, indent=2)
print('\nResults saved to self_dual_results.json')
