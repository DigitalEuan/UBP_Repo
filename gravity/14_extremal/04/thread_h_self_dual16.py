"""
THREAD H: Qualified Self-Dual Conjecture Test on [16,8] (Open Q2)
==================================================================

EXTREMAL_003 falsified the UNQUALIFIED self-dual conjecture (self-dual
codes do NOT maximise avg_Phi for fixed n in general).

But the QUALIFIED conjecture -- "among codes with d_min >= some threshold,
self-dual codes maximise avg_Phi" -- was left open.

We test this on [16,8] codes. There are multiple known self-dual [16,8]
codes:
  - Self-dual d=4 codes: 2 inequivalent (one is direct sum of E8, the other
    is the Reed-Muller [16,8,4] = RM(1,4) extended, etc.)
  - Self-dual d=2 codes: many.

The strategy:
  1. Sample random [16,8] codes (mostly d=1 or d=2).
  2. Sample random self-dual [16,8] codes via G = [I_8 | B] with B orthogonal.
  3. For each, compute avg_Phi exactly (2^16 = 65536 vectors -- tractable
     exactly, no Monte Carlo needed).
  4. Classify by (self_dual, d_min) and see which subgroup wins.
"""
import sys, random, time, json
from fractions import Fraction
from itertools import product
from collections import Counter, defaultdict
sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics

pp = UBPSourceCodeParticlePhysics()
Y = pp.Y
Y_plus_one_eighth = Y + Fraction(1, 8)
PHI_PEAK = Fraction(1, 1) / Y_plus_one_eighth


def hw(v): return sum(1 for x in v if x)

def phi_with_dist(h_state, dist):
    if h_state == 0: return Fraction(0)
    denom = Fraction(h_state) * Y_plus_one_eighth + Fraction(dist) * Y
    return Fraction(h_state) / denom

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
        cw.append(tuple(sum(G[i][j] for i, b in enumerate(bits) if b) & 1 for j in range(n)))
    return cw

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

def d_min(codewords):
    return min(sum(c) for c in codewords if sum(c) > 0)

def avg_phi_exact(codewords, n):
    """Exact avg_Phi over all 2^n vectors. Tractable for n <= 16."""
    cw_set = set(codewords)
    total = Fraction(0)
    for v in product([0, 1], repeat=n):
        h = sum(v)
        if h == 0: continue
        if v in cw_set:
            total += PHI_PEAK
        else:
            md = min(sum((a + b) & 1 for a, b in zip(v, c)) for c in codewords)
            total += phi_with_dist(h, md)
    return Fraction(total, 1 << n)


print('=' * 72)
print('THREAD H: Qualified Self-Dual Conjecture Test on [16,8]')
print('=' * 72)

rng = random.Random(20260625)
N_RANDOM = 60
N_SELFDUAL = 25  # try to generate this many self-dual codes

records = []

print(f'\nSampling {N_RANDOM} random [16,8] codes (exact avg_Phi, ~3s each)...')
t0_total = time.time()
for i in range(N_RANDOM):
    G = random_generator(8, 16, rng)
    cw = all_codewords(G, 8, 16)
    d = d_min(cw)
    sd = is_self_dual(G, 8, 16)
    ap = avg_phi_exact(cw, 16)
    records.append({'name': f'Random[16,8]#{i+1}', 'd_min': d, 'self_dual': sd,
                    'avg_phi': float(ap), 'avg_phi_str': str(ap)})
    if (i+1) % 10 == 0:
        print(f'  {i+1}/{N_RANDOM} done ({time.time()-t0_total:.1f}s)')

print(f'\nSampling self-dual [16,8] codes via G = [I_8 | B], B orthogonal...')
n_sd_generated = 0
n_attempts = 0
while n_sd_generated < N_SELFDUAL and n_attempts < 200:
    n_attempts += 1
    G = random_self_dual_generator(8, 16, rng)
    if G is None: continue
    cw = all_codewords(G, 8, 16)
    d = d_min(cw)
    sd = is_self_dual(G, 8, 16)
    if not sd: continue
    n_sd_generated += 1
    ap = avg_phi_exact(cw, 16)
    records.append({'name': f'SelfDual[16,8]#{n_sd_generated}', 'd_min': d, 'self_dual': True,
                    'avg_phi': float(ap), 'avg_phi_str': str(ap)})
    if n_sd_generated % 5 == 0:
        print(f'  {n_sd_generated}/{N_SELFDUAL} generated ({n_attempts} attempts)')

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
    print(f'  Self-dual d>=4:     {len(sd_d4)} codes, avg_Phi range [{min(r["avg_phi"] for r in sd_d4):.5f}, {max(r["avg_phi"] for r in sd_d4):.5f}]' if sd_d4 else f'  Self-dual d>=4:     0 codes')
    print(f'  Non-self-dual d>=4: {len(nsd_d4)} codes, avg_Phi range [{min(r["avg_phi"] for r in nsd_d4):.5f}, {max(r["avg_phi"] for r in nsd_d4):.5f}]' if nsd_d4 else f'  Non-self-dual d>=4: 0 codes')
    top_d4 = sorted(d4plus, key=lambda r: -r['avg_phi'])[:5]
    print(f'  Top 5 by avg_Phi among d>=4:')
    for r in top_d4:
        sd_label = 'SD' if r['self_dual'] else 'NSD'
        print(f'    {r["name"]:<25s}  d={r["d_min"]}  {sd_label}  avg_Phi={r["avg_phi"]:.6f}')

# Among d >= 2 (low-threshold qualified)
print('\n--- Among d_min >= 2 codes ---')
d2plus = [r for r in records if r['d_min'] >= 2]
if d2plus:
    sd_d2 = [r for r in d2plus if r['self_dual']]
    nsd_d2 = [r for r in d2plus if not r['self_dual']]
    if sd_d2:
        print(f'  Self-dual d>=2:     {len(sd_d2)} codes, avg_Phi mean {sum(r["avg_phi"] for r in sd_d2)/len(sd_d2):.5f}')
    if nsd_d2:
        print(f'  Non-self-dual d>=2: {len(nsd_d2)} codes, avg_Phi mean {sum(r["avg_phi"] for r in nsd_d2)/len(nsd_d2):.5f}')

# Save
with open('/home/z/my-project/work/self_dual16_results.json', 'w') as f:
    json.dump({'records': records, 'n_random': N_RANDOM, 'n_self_dual': n_sd_generated}, f, indent=2)
print('\nSaved to self_dual16_results.json')
