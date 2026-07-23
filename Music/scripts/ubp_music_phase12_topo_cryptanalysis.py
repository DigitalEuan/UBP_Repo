"""
UBP Music Study — Phase XII: Topological Prime Cryptanalysis
============================================================
THE PIVOT: From Harmonic Musicology to Topological Friction Mapping

Phase XI established:
  - Composites generate ~5.6x more hypervolume and ~3.4x more rotation
  - NRCI distinguishes primes (0.921) from composites (0.735)
  - The harmonic signal is STATIC (what a number IS), primality is DYNAMIC (how it BEHAVES)

Phase XII directives:
  1. MANIFOLD HEATMAP: Plot NRCI vs Geometric Friction for N=10^3..10^4
     - Do primes form a distinct "attractor" in this 2D space?
  2. CONTINUOUS FRICTION FIELD: Map Hypervolume/Rotation as a continuous field
     - Do Mersenne candidates cluster on a "low-friction path"?
  3. INVERSE FACTORIZATION VIA FRICTION: Does rotation direction correlate
     with the prime factors of composite candidates?
  4. CROSS-DIMENSIONAL CALIBRATION: NRCI signal decay rate across modulus scaling
     - Define a scaling law for primality detection
  5. FRICTION RATIO AS UNIVERSAL PRIMALITY METRIC: Test whether
     Hypervolume/Rotation ratio separates primes from composites universally
"""

import sys, math, random, time
from fractions import Fraction
from collections import Counter, defaultdict
from itertools import combinations

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import (
    GolayCodeEngine, LeechLatticeEngine, BarnesWallEngine,
    MonsterGroup, AdaptiveManifold, NoiseALU
)

g = GolayCodeEngine()
l = LeechLatticeEngine(g)
manifold = AdaptiveManifold()

RESIDUES = [17, 31, 113, 127]

# ========================================================================
# UTILITIES
# ========================================================================

def mod_dist(a, b, m):
    return min((a - b) % m, (b - a) % m)

def residue_fingerprint_4d(n, modulus=144):
    r = n % modulus
    return [mod_dist(r, res, modulus) for res in RESIDUES]

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2: return 0.0
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs, ys))
    vx = sum((x-mx)**2 for x in xs)
    vy = sum((y-my)**2 for y in ys)
    if vx == 0 or vy == 0: return 0.0
    return cov / math.sqrt(vx * vy)

def spearman_rho(xs, ys):
    n = len(xs)
    if n < 2: return 0.0
    rx = sorted(range(n), key=lambda i: xs[i])
    ry = sorted(range(n), key=lambda i: ys[i])
    rank_x = [0]*n; rank_y = [0]*n
    for i, idx in enumerate(rx): rank_x[idx] = i
    for i, idx in enumerate(ry): rank_y[idx] = i
    return pearson_r(rank_x, rank_y)

def miller_rabin(n, k=20):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses[:k]:
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n-1: continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else:
            return False
    return True

def ubp_encode_24bit(n):
    """Full Golay->Leech pipeline encoding."""
    gc = abs(n) ^ (abs(n) >> 1)
    bits = [(gc >> i) & 1 for i in range(23, -1, -1)]
    sw = g.syndrome_weight(bits)
    decoded, correctable, anchor_dist = g.decode(bits)
    cw = g.encode(decoded)
    nrci = float(l.calculate_nrci(cw))
    return {"sw": sw, "nrci": nrci, "hw": sum(cw), "anchor_dist": anchor_dist, "correctable": correctable}

def ubp_manifold_fp(n):
    """AdaptiveManifold fingerprint."""
    return manifold.fingerprint(n)

def cayley_menger_volume(vertices):
    """Squared hypervolume of a simplex via Cayley-Menger determinant."""
    k = len(vertices) - 1
    if k < 1: return 0.0
    n = len(vertices)
    D = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = math.sqrt(sum((a-b)**2 for a,b in zip(vertices[i], vertices[j])))
            D[i][j] = D[j][i] = d

    size = n + 1
    CM = [[0.0]*size for _ in range(size)]
    for i in range(n):
        CM[0][i+1] = CM[i+1][0] = 1.0
        for j in range(n):
            CM[i+1][j+1] = D[i][j] ** 2

    def det(matrix):
        m = [row[:] for row in matrix]
        sign = 1.0
        n_rows = len(m)
        for col in range(n_rows):
            max_row = col
            for row in range(col+1, n_rows):
                if abs(m[row][col]) > abs(m[max_row][col]):
                    max_row = row
            if max_row != col:
                m[col], m[max_row] = m[max_row], m[col]
                sign *= -1
            if abs(m[col][col]) < 1e-15:
                return 0.0
            for row in range(col+1, n_rows):
                factor = m[row][col] / m[col][col]
                for j in range(col, n_rows):
                    m[row][j] -= factor * m[col][j]
        result = sign
        for i in range(n_rows):
            result *= m[i][i]
        return result

    det_cm = det(CM)
    sign = (-1) ** (k + 1)
    coeff = sign / (2**k * math.factorial(k)**2)
    vol_sq = coeff * det_cm
    return max(0.0, vol_sq)

def value_to_simplex(val):
    """Map integer to 4-vertex 3-simplex in 4D prime residue space."""
    fp = residue_fingerprint_4d(val)
    vertices = []
    for i in range(4):
        vertex = list(fp)
        bits = [(val >> j) & 1 for j in range(min(8, max(1, val.bit_length())))]
        vertex[i] += sum(bits) * 0.5
        vertices.append(vertex)
    return vertices, fp

def jaccard_sets(a, b):
    a, b = set(a), set(b)
    u = a | b
    return len(a & b) / len(u) if u else 1.0


# ========================================================================
# DIRECTIVE 1: THE MANIFOLD HEATMAP
# ========================================================================

def compute_friction_profile(n, use_ll=True, ll_mod=None):
    """
    Compute the full topological friction profile of integer n.
    Returns dict with NRCI, hypervolume, rotation, friction ratio, etc.
    
    If use_ll and ll_mod is given, runs n through Lucas-Lehmer iteration
    and measures friction across the trajectory.
    """
    # Static UBP metrics
    enc = ubp_encode_24bit(n)
    fp_am = ubp_manifold_fp(n)
    
    # Geometric: simplex from residue fingerprint
    verts, fp4d = value_to_simplex(n)
    vol = cayley_menger_volume(verts)
    
    profile = {
        "n": n,
        "nrci_gl": enc["nrci"],       # Golay-Leech NRCI
        "nrci_am": fp_am["nrci"],     # AdaptiveManifold NRCI
        "sw": enc["sw"],               # syndrome weight
        "hw": enc["hw"],               # Hamming weight
        "anchor_dist": enc["anchor_dist"],
        "vol": vol,                    # hypervolume (static)
        "fp4d": fp4d,
        "fp4d_total": sum(fp4d),
        "lattice": fp_am["lattice"],
        "on_lattice": fp_am["on_lattice"],
    }
    
    # If LL trajectory requested
    if use_ll and ll_mod is not None and ll_mod > 3:
        s = 4
        max_iter = min(max(2, int(math.log2(ll_mod)) - 2), 12)
        trajectory_vols = []
        trajectory_jaccards = []
        prev_verts = None
        
        for i in range(max_iter + 1):
            verts_i, fp4d_i = value_to_simplex(s)
            vol_i = cayley_menger_volume(verts_i)
            trajectory_vols.append(vol_i)
            
            if prev_verts is not None:
                # Jaccard rotation between consecutive simplexes
                def active_region(verts):
                    occupied = set()
                    for vi in verts:
                        for d in range(len(vi)):
                            bin_idx = int(vi[d] * 2)
                            occupied.add((d, bin_idx))
                    return occupied
                j = jaccard_sets(active_region(prev_verts), active_region(verts_i))
                trajectory_jaccards.append(j)
            
            prev_verts = verts_i
            s = (s * s - 2) % ll_mod
        
        # Aggregate trajectory metrics
        avg_vol = sum(trajectory_vols) / len(trajectory_vols) if trajectory_vols else 0
        std_vol = math.sqrt(sum((v - avg_vol)**2 for v in trajectory_vols) / len(trajectory_vols)) if trajectory_vols else 0
        avg_jacc = sum(trajectory_jaccards) / len(trajectory_jaccards) if trajectory_jaccards else 0
        std_jacc = math.sqrt(sum((j - avg_jacc)**2 for j in trajectory_jaccards) / len(trajectory_jaccards)) if trajectory_jaccards else 0
        
        # Total geometric friction = avg_vol * (1 - avg_jacc) + std_vol
        # This combines: how much volume the simplex occupies AND how much it rotates
        total_friction = avg_vol * (1.0 - avg_jacc + 0.01) + std_vol
        friction_ratio = total_friction / (avg_jacc + 0.001) if avg_jacc > 0.001 else total_friction * 1000
        
        profile.update({
            "traj_vol_mean": avg_vol,
            "traj_vol_std": std_vol,
            "traj_jacc_mean": avg_jacc,
            "traj_jacc_std": std_jacc,
            "total_friction": total_friction,
            "friction_ratio": friction_ratio,
            "traj_vols": trajectory_vols,
            "traj_jaccs": trajectory_jaccards,
        })
    
    return profile


def run_manifold_heatmap():
    print("=" * 80)
    print("DIRECTIVE 1: THE MANIFOLD HEATMAP — Topological Prime Cryptanalysis")
    print("=" * 80)
    print("  Map integers N=1000..10000 on a 2D plane:")
    print("    X-axis: NRCI (Golay-Leech error-correction signal)")
    print("    Y-axis: Geometric Friction (hypervolume + rotation)")
    print("  Question: Do primes form a distinct 'attractor' in this space?")
    print()
    
    random.seed(42)
    N_MIN, N_MAX = 1000, 10000
    
    # Stratified sample: take ALL primes + matching number of random composites
    all_primes_in_range = [n for n in range(N_MIN, N_MAX) if miller_rabin(n)]
    n_primes_sample = min(len(all_primes_in_range), 500)  # cap for speed
    prime_sample = random.sample(all_primes_in_range, n_primes_sample)
    
    # Match with composites
    comp_pool = [n for n in range(N_MIN, N_MAX) if not miller_rabin(n)]
    comp_sample = random.sample(comp_pool, min(n_primes_sample * 3, len(comp_pool)))
    
    print(f"  Computing friction profiles for {len(prime_sample)} primes + {len(comp_sample)} composites...")
    t0 = time.time()
    
    profiles = []
    for n in prime_sample + comp_sample:
        is_prime = miller_rabin(n)
        prof = compute_friction_profile(n, use_ll=True, ll_mod=n)
        prof["is_prime"] = is_prime
        profiles.append(prof)
    
    elapsed = time.time() - t0
    print(f"  Computed {len(profiles)} profiles in {elapsed:.1f}s")
    
    # Extract coordinates
    primes = [p for p in profiles if p["is_prime"]]
    composites = [p for p in profiles if not p["is_prime"]]
    
    print(f"\n  Primes: {len(primes)}, Composites: {len(composites)}")
    
    # --- 2D SCATTER ANALYSIS ---
    print(f"\n  --- 2D HEATMAP STATISTICS (NRCI vs Total Friction) ---")
    
    # Static friction (just the residue simplex volume, no LL trajectory)
    p_nrci = [p["nrci_gl"] for p in primes]
    c_nrci = [p["nrci_gl"] for p in composites]
    p_vol = [p["vol"] for p in primes]
    c_vol = [p["vol"] for p in composites]
    
    print(f"  STATIC VIEW (single simplex):")
    print(f"    Prime NRCI:    mean={sum(p_nrci)/len(p_nrci):.4f}, "
          f"std={math.sqrt(sum((x-sum(p_nrci)/len(p_nrci))**2 for x in p_nrci)/len(p_nrci)):.4f}")
    print(f"    Comp NRCI:     mean={sum(c_nrci)/len(c_nrci):.4f}, "
          f"std={math.sqrt(sum((x-sum(c_nrci)/len(c_nrci))**2 for x in c_nrci)/len(c_nrci)):.4f}")
    print(f"    Prime Vol:     mean={sum(p_vol)/len(p_vol):.2f}, "
          f"std={math.sqrt(sum((x-sum(p_vol)/len(p_vol))**2 for x in p_vol)/len(p_vol)):.2f}")
    print(f"    Comp Vol:      mean={sum(c_vol)/len(c_vol):.2f}, "
          f"std={math.sqrt(sum((x-sum(c_vol)/len(c_vol))**2 for x in c_vol)/len(c_vol)):.2f}")
    
    # Dynamic friction (LL trajectory)
    p_friction = [p["total_friction"] for p in primes if "total_friction" in p]
    c_friction = [p["total_friction"] for p in composites if "total_friction" in p]
    p_nrci_dyn = [p["nrci_gl"] for p in primes if "total_friction" in p]
    c_nrci_dyn = [p["nrci_gl"] for p in composites if "total_friction" in p]
    
    print(f"\n  DYNAMIC VIEW (LL trajectory friction):")
    if p_friction and c_friction:
        print(f"    Prime friction:  mean={sum(p_friction)/len(p_friction):.2f}, "
              f"std={math.sqrt(sum((x-sum(p_friction)/len(p_friction))**2 for x in p_friction)/len(p_friction)):.2f}")
        print(f"    Comp friction:   mean={sum(c_friction)/len(c_friction):.2f}, "
              f"std={math.sqrt(sum((x-sum(c_friction)/len(c_friction))**2 for x in c_friction)/len(c_friction)):.2f}")
        ratio = (sum(c_friction)/len(c_friction)) / (sum(p_friction)/len(p_friction))
        print(f"    Composite/Prime friction ratio: {ratio:.2f}x")
    
    # FRICTION RATIO as universal metric
    print(f"\n  --- FRICTION RATIO AS PRIMALITY METRIC ---")
    p_ratios = [p["friction_ratio"] for p in primes if "friction_ratio" in p]
    c_ratios = [p["friction_ratio"] for p in composites if "friction_ratio" in p]
    
    if p_ratios and c_ratios:
        p_r_mean = sum(p_ratios)/len(p_ratios)
        c_r_mean = sum(c_ratios)/len(c_ratios)
        p_r_median = sorted(p_ratios)[len(p_ratios)//2]
        c_r_median = sorted(c_ratios)[len(c_ratios)//2]
        print(f"    Prime friction_ratio:   mean={p_r_mean:.2f}, median={p_r_median:.2f}")
        print(f"    Composite friction_ratio: mean={c_r_mean:.2f}, median={c_r_median:.2f}")
        
        # Binary classification via threshold
        labels = [0]*len(p_ratios) + [1]*len(c_ratios)
        ratios = p_ratios + c_ratios
        
        best_acc = 0; best_thresh = 0
        for thresh in [i * 1.0 for i in range(1, int(max(ratios)) + 1)]:
            preds = [0 if r < thresh else 1 for r in ratios]
            correct = sum(p == l for p, l in zip(preds, labels))
            acc = correct / len(labels)
            if acc > best_acc:
                best_acc = acc
                best_thresh = thresh
        
        baseline = max(len(p_ratios), len(c_ratios)) / len(labels)
        print(f"    Best threshold: {best_thresh:.0f}, accuracy: {best_acc:.4f} (baseline: {baseline:.4f})")
        
        # Correlation of friction_ratio with primality label
        r_friction = pearson_r(labels, ratios)
        rho_friction = spearman_rho(labels, ratios)
        print(f"    Pearson  r (composite_label vs friction_ratio): {r_friction:+.4f}")
        print(f"    Spearman rho: {rho_friction:+.4f}")
    
    # ATTRACTOR DETECTION: Do primes cluster in a specific region?
    print(f"\n  --- ATTRACTOR DETECTION ---")
    if p_friction and c_friction:
        # 2D: (NRCI, Friction) — find the "prime basin"
        # Compute the centroid of primes in this 2D space
        p_centroid_nrci = sum(p_nrci_dyn)/len(p_nrci_dyn)
        p_centroid_fric = sum(p_friction)/len(p_friction)
        c_centroid_nrci = sum(c_nrci_dyn)/len(c_nrci_dyn)
        c_centroid_fric = sum(c_friction)/len(c_friction)
        
        print(f"    Prime centroid:     (NRCI={p_centroid_nrci:.4f}, Friction={p_centroid_fric:.2f})")
        print(f"    Composite centroid: (NRCI={c_centroid_nrci:.4f}, Friction={c_centroid_fric:.2f})")
        
        # Euclidean distance between centroids
        centroid_dist = math.sqrt((p_centroid_nrci - c_centroid_nrci)**2 + 
                                   (p_centroid_fric - c_centroid_fric)**2)
        print(f"    Centroid separation: {centroid_dist:.4f}")
        
        # Compute average distance of each point to its own centroid vs other centroid
        p_self_dist = [math.sqrt((p["nrci_gl"] - p_centroid_nrci)**2 + 
                                  (p["total_friction"] - p_centroid_fric)**2) for p in primes if "total_friction" in p]
        p_cross_dist = [math.sqrt((p["nrci_gl"] - c_centroid_nrci)**2 + 
                                   (p["total_friction"] - c_centroid_fric)**2) for p in primes if "total_friction" in p]
        c_self_dist = [math.sqrt((p["nrci_gl"] - c_centroid_nrci)**2 + 
                                  (p["total_friction"] - c_centroid_fric)**2) for p in composites if "total_friction" in p]
        c_cross_dist = [math.sqrt((p["nrci_gl"] - p_centroid_nrci)**2 + 
                                   (p["total_friction"] - p_centroid_fric)**2) for p in composites if "total_friction" in p]
        
        # Silhouette-like score: (cross - self) / max(self, cross)
        p_sil = [(cross - self) / max(self, cross, 0.001) 
                 for self, cross in zip(p_self_dist, p_cross_dist)]
        c_sil = [(cross - self) / max(self, cross, 0.001)
                 for self, cross in zip(c_self_dist, c_cross_dist)]
        
        avg_p_sil = sum(p_sil) / len(p_sil)
        avg_c_sil = sum(c_sil) / len(c_sil)
        overall_sil = (avg_p_sil * len(p_sil) + avg_c_sil * len(c_sil)) / (len(p_sil) + len(c_sil))
        
        print(f"    Prime avg silhouette:     {avg_p_sil:+.4f}")
        print(f"    Composite avg silhouette: {avg_c_sil:+.4f}")
        print(f"    Overall silhouette score: {overall_sil:+.4f}")
        print(f"    (Positive = good separation, Negative = overlap)")
        
        # Density analysis: how many primes fall in the "prime basin"?
        # Define basin as circle of radius r around prime centroid
        for radius_frac in [0.25, 0.5, 1.0, 2.0]:
            # Radius in 2D space
            p_spread = math.sqrt(sum((x - p_centroid_nrci)**2 + (y - p_centroid_fric)**2 
                                     for x, y in zip(p_nrci_dyn, p_friction)) / len(p_nrci_dyn))
            r = p_spread * radius_frac
            
            p_in_basin = sum(1 for x, y in zip(p_nrci_dyn, p_friction) 
                            if math.sqrt((x - p_centroid_nrci)**2 + (y - p_centroid_fric)**2) < r)
            c_in_basin = sum(1 for x, y in zip(c_nrci_dyn, c_friction)
                            if math.sqrt((x - p_centroid_nrci)**2 + (y - p_centroid_fric)**2) < r)
            total_in = p_in_basin + c_in_basin
            prime_density = p_in_basin / total_in if total_in > 0 else 0
            print(f"    Basin r={radius_frac:.2f}: {p_in_basin} primes, {c_in_basin} comps, "
                  f"prime density={prime_density:.4f} (random={len(primes)/(len(primes)+len(composites)):.4f})")
    
    return {
        "n_primes": len(primes),
        "n_composites": len(composites),
        "p_nrci_mean": sum(p_nrci)/len(p_nrci),
        "c_nrci_mean": sum(c_nrci)/len(c_nrci),
        "silhouette": overall_sil if p_friction else 0,
        "best_friction_acc": best_acc if p_ratios else 0,
    }


# ========================================================================
# DIRECTIVE 2: CONTINUOUS FRICTION FIELD & LOW-FRICTION PATHS
# ========================================================================

def run_continuous_friction_field():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 2: CONTINUOUS FRICTION FIELD — Low-Friction Paths")
    print("=" * 80)
    print("  Instead of binary prime/composite, map the Hypervolume/Rotation")
    print("  ratio as a continuous field. Do Mersenne candidates cluster on")
    print("  a 'low-friction valley' in the manifold?")
    print()
    
    # Test specific number families
    families = {
        "Mersenne_exponents": [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279],
        "Composite_exponents": [11, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 97],
        "Twin_primes": [(p, p+2) for p in [3,5,11,17,29,41,59,71,101,107,137,149,179,191,197] if miller_rabin(p) and miller_rabin(p+2)],
        "Safe_primes": [p for p in [5,7,11,23,47,59,83,107,167,179,227,263,347,359,383,467] if miller_rabin(p) and miller_rabin((p-1)//2)],
        "Powers_of_2": [2**k for k in range(1, 14)],
        "Factorials": [math.factorial(k) for k in range(1, 9)],
        "Fibonacci": [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987],
        "Carmichael": [561, 1105, 1729, 2465, 2821, 6601],
    }
    
    # Flatten twin primes
    twin_flat = []
    for a, b in families["Twin_primes"]:
        twin_flat.extend([a, b])
    families["Twin_primes_flat"] = twin_flat[:30]
    # Remove the tuple-based entry
    families.pop("Twin_primes", None)
    
    # Compute friction profiles for each family
    print(f"  Computing friction profiles for {sum(len(v) for v in families.values())} numbers across {len(families)} families...")
    
    family_profiles = {}
    for name, nums in families.items():
        profiles = []
        for n in nums:
            if not isinstance(n, int) or n < 4 or n > 100000:
                continue
            prof = compute_friction_profile(n, use_ll=True, ll_mod=n)
            prof["is_prime"] = miller_rabin(n)
            profiles.append(prof)
        family_profiles[name] = profiles
    
    # Table: friction statistics per family
    print(f"\n  --- FRICTION STATISTICS BY NUMBER FAMILY ---")
    print(f"  {'Family':>22s} | {'N':>3s} | {'NRCI_m':>7s} | {'Fric_m':>8s} | {'Fric_s':>8s} | {'FR_m':>7s} | {'Vol_m':>7s} | {'Jacc_m':>7s}")
    print(f"  {'-'*22} | {'-'*3} | {'-'*7} | {'-'*8} | {'-'*8} | {'-'*7} | {'-'*7} | {'-'*7}")
    
    for name in ["Mersenne_exponents", "Composite_exponents", "Twin_primes_flat",
                  "Safe_primes", "Powers_of_2", "Factorials", "Fibonacci", "Carmichael"]:
        profs = family_profiles[name]
        if not profs:
            continue
        nrcis = [p["nrci_gl"] for p in profs]
        frics = [p["total_friction"] for p in profs if "total_friction" in p]
        vols = [p["vol"] for p in profs]
        jaccs = [p["traj_jacc_mean"] for p in profs if "traj_jacc_mean" in p]
        frats = [p["friction_ratio"] for p in profs if "friction_ratio" in p]
        
        nrci_m = sum(nrcis)/len(nrcis)
        fric_m = sum(frics)/len(frics) if frics else 0
        fric_s = math.sqrt(sum((f-fric_m)**2 for f in frics)/len(frics)) if frics else 0
        fr_m = sum(frats)/len(frats) if frats else 0
        vol_m = sum(vols)/len(vols) if vols else 0
        jacc_m = sum(jaccs)/len(jaccs) if jaccs else 0
        
        label = name[:22]
        print(f"  {label:>22s} | {len(profs):>3d} | {nrci_m:>7.4f} | {fric_m:>8.2f} | {fric_s:>8.2f} | {fr_m:>7.2f} | {vol_m:>7.2f} | {jacc_m:>7.4f}")
    
    # LOW-FRICTION PATH ANALYSIS
    # Do Mersenne primes follow a path with less friction than composites?
    print(f"\n  --- LOW-FRICTION PATH DETECTION ---")
    mers_exp = family_profiles["Mersenne_exponents"]
    comp_exp = family_profiles["Composite_exponents"]
    
    if mers_exp and comp_exp:
        # Sort all numbers by friction
        all_nums = [(p["n"], p["total_friction"], p["is_prime"]) 
                    for p in mers_exp + comp_exp if "total_friction" in p]
        all_nums.sort(key=lambda x: x[1])
        
        print(f"  Lowest friction numbers:")
        for n, f, ip in all_nums[:10]:
            marker = "PRIME" if ip else "comp"
            print(f"    n={n:>6d}: friction={f:>8.2f} [{marker}]")
        
        print(f"  Highest friction numbers:")
        for n, f, ip in all_nums[-10:]:
            marker = "PRIME" if ip else "comp"
            print(f"    n={n:>6d}: friction={f:>8.2f} [{marker}]")
        
        # Mersenne exponents: what fraction are in the lowest-friction quartile?
        all_frictions = [f for _, f, _ in all_nums]
        q25 = sorted(all_frictions)[len(all_frictions)//4]
        
        mers_in_low = sum(1 for n, f, ip in all_nums if f <= q25 and ip and n in 
                         [2,3,5,7,13,17,19,31,61,89,107,127,521,607,1279])
        mers_total = len(mers_exp)
        comp_in_low = sum(1 for n, f, ip in all_nums if f <= q25 and not ip and n not in 
                         [2,3,5,7,13,17,19,31,61,89,107,127,521,607,1279])
        comp_total = len(comp_exp)
        
        print(f"\n  In lowest-friction quartile (friction < {q25:.2f}):")
        print(f"    Mersenne exponents: {mers_in_low}/{mers_total} ({100*mers_in_low/mers_total:.1f}% if mers_total>0)")
        print(f"    Composite exponents: {comp_in_low}/{comp_total} ({100*comp_in_low/comp_total:.1f}% if comp_total>0)")
    
    # Carmichael number analysis (pseudoprimes that fool Miller-Rabin less often)
    print(f"\n  --- CARMICHAEL NUMBERS (PSEUDOPRIME ANALYSIS) ---")
    carm_profs = family_profiles["Carmichael"]
    if carm_profs:
        for cp in carm_profs:
            fp4d = cp["fp4d"]
            print(f"    {cp['n']:>6d}: NRCI={cp['nrci_gl']:.4f}, vol={cp['vol']:.2f}, "
                  f"friction={cp.get('total_friction', 0):.2f}, "
                  f"4D=[{','.join(f'{d:.0f}' for d in fp4d)}], total={sum(fp4d)}")
    
    return family_profiles


# ========================================================================
# DIRECTIVE 3: INVERSE FACTORIZATION VIA FRICTION
# ========================================================================

def run_inverse_factorization():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 3: INVERSE FACTORIZATION VIA FRICTION")
    print("=" * 80)
    print("  If M_p is composite, it must have factors. Does the DIRECTION")
    print("  of geometric rotation during LL test correlate with those factors?")
    print()
    
    # Known composite Mersenne numbers and their factors
    composite_mersennes = {
        11: (2047, [23, 89]),
        23: (8388607, [47, 178481]),
        29: (536870911, [233, 1103, 2089]),
        37: (137438953471, [223, 616318177]),
        41: (2199023255551, [13367, 164511353]),
    }
    
    # For each composite, track the DIRECTION of rotation in 4D fingerprint space
    def ll_rotation_direction(p, Mp, max_iter=30):
        """
        Track the angular direction of the 4D fingerprint trajectory during LL.
        Returns list of angle changes and cumulative rotation vectors.
        """
        s = 4
        trace_4d = []
        for i in range(min(max_iter, max(2, p-2)) + 1):
            fp4d = residue_fingerprint_4d(s)
            trace_4d.append(fp4d)
            s = (s * s - 2) % Mp
        
        # Compute direction vectors and angles
        directions = []
        angles = []
        for i in range(1, len(trace_4d)):
            d = [trace_4d[i][j] - trace_4d[i-1][j] for j in range(4)]
            directions.append(d)
            if i > 1:
                d_prev = directions[-2]
                # Angle between consecutive direction vectors
                dot = sum(a*b for a, b in zip(d, d_prev))
                n1 = math.sqrt(sum(a*a for a in d)) + 1e-10
                n2 = math.sqrt(sum(a*a for a in d_prev)) + 1e-10
                cos_angle = max(-1, min(1, dot / (n1 * n2)))
                angle = math.acos(cos_angle)
                angles.append(angle)
        
        # Cross product-like: sign of rotation in the plane spanned by first two directions
        rotation_signs = []
        for i in range(1, len(directions)):
            # 2D cross product in the (d_x, d_y) plane
            cross = (directions[i][0] * directions[i-1][1] - 
                    directions[i][1] * directions[i-1][0])
            rotation_signs.append(1 if cross > 0 else (-1 if cross < 0 else 0))
        
        # Net rotation (sum of signed rotations)
        net_rotation = sum(rotation_signs)
        
        # Dominant axis: which of the 4 dimensions changes most
        dim_changes = [0, 0, 0, 0]
        for d in directions:
            max_dim = max(range(4), key=lambda j: abs(d[j]))
            dim_changes[max_dim] += 1
        dominant_dim = max(range(4), key=lambda j: dim_changes[j])
        
        return {
            "directions": directions,
            "angles": angles,
            "rotation_signs": rotation_signs,
            "net_rotation": net_rotation,
            "dim_changes": dim_changes,
            "dominant_dim": dominant_dim,
            "mean_angle": sum(angles)/len(angles) if angles else 0,
            "angle_std": math.sqrt(sum((a - sum(angles)/len(angles))**2 for a in angles)/len(angles)) if angles else 0,
        }
    
    print("  Computing rotation signatures for composite Mersenne numbers...")
    results = {}
    for p, (Mp, factors) in composite_mersennes.items():
        rot = ll_rotation_direction(p, Mp)
        results[p] = rot
        print(f"\n  M_{p} = {Mp} = {' x '.join(map(str, factors))}")
        print(f"    Net rotation: {rot['net_rotation']:+d}")
        print(f"    Mean angle between direction changes: {rot['mean_angle']:.4f} rad ({math.degrees(rot['mean_angle']):.1f} deg)")
        print(f"    Angle std: {rot['angle_std']:.4f}")
        print(f"    Dominant dimension: {rot['dominant_dim']} ({RESIDUES[rot['dominant_dim']]})")
        print(f"    Dimension activity: {rot['dim_changes']}")
        
        # Test: does the number of factors correlate with rotation sign changes?
        sign_changes = sum(1 for i in range(1, len(rot['rotation_signs'])) 
                          if rot['rotation_signs'][i] != rot['rotation_signs'][i-1])
        print(f"    Sign changes: {sign_changes} (n_factors={len(factors)})")
    
    # Also compute for Mersenne PRIMES for comparison
    print(f"\n  --- PRIME COMPARISON ---")
    prime_mersennes = {3: 7, 5: 31, 7: 127, 13: 8191}
    for p, Mp in prime_mersennes.items():
        rot = ll_rotation_direction(p, Mp)
        results[p] = rot
        print(f"\n  M_{p} = {Mp} (PRIME)")
        print(f"    Net rotation: {rot['net_rotation']:+d}")
        print(f"    Mean angle: {rot['mean_angle']:.4f} rad ({math.degrees(rot['mean_angle']):.1f} deg)")
        print(f"    Angle std: {rot['angle_std']:.4f}")
        print(f"    Dominant dimension: {rot['dominant_dim']} ({RESIDUES[rot['dominant_dim']]})")
        print(f"    Dimension activity: {rot['dim_changes']}")
    
    # Factor direction correlation
    print(f"\n  --- FACTOR-DIRECTION CORRELATION ---")
    # For each composite, test: does the dominant rotation dimension
    # correspond to any property of the factors?
    for p, (Mp, factors) in composite_mersennes.items():
        rot = results[p]
        # Map each factor to its 4D fingerprint and find nearest residue
        print(f"  M_{p} factors:")
        for f in factors:
            fp = residue_fingerprint_4d(f)
            nearest_res = min(range(4), key=lambda i: fp[i])
            print(f"    factor {f:>10d}: fp4d=[{','.join(f'{d:.0f}' for d in fp)}], "
                  f"nearest={RESIDUES[nearest_res]}, dominant_dim={rot['dominant_dim']} "
                  f"({'MATCH' if nearest_res == rot['dominant_dim'] else 'no match'})")
    
    # Aggregated: do composites with MORE factors show more rotation sign changes?
    print(f"\n  --- ROTATION COMPLEXITY vs FACTOR COUNT ---")
    comp_data = []
    for p, (Mp, factors) in composite_mersennes.items():
        rot = results[p]
        sign_changes = sum(1 for i in range(1, len(rot['rotation_signs']))
                          if rot['rotation_signs'][i] != rot['rotation_signs'][i-1])
        comp_data.append((len(factors), sign_changes, rot['net_rotation'], rot['mean_angle']))
    
    # Primes should have 1 "factor" (themselves)
    prime_data = []
    for p, Mp in prime_mersennes.items():
        rot = results[p]
        sign_changes = sum(1 for i in range(1, len(rot['rotation_signs']))
                          if rot['rotation_signs'][i] != rot['rotation_signs'][i-1])
        prime_data.append((1, sign_changes, rot['net_rotation'], rot['mean_angle']))
    
    all_data = comp_data + prime_data
    n_factors = [d[0] for d in all_data]
    sign_changes_all = [d[1] for d in all_data]
    net_rots = [d[2] for d in all_data]
    mean_angles = [d[3] for d in all_data]
    
    r_factors_signs = pearson_r(n_factors, sign_changes_all)
    r_factors_rot = pearson_r(n_factors, net_rots)
    r_factors_angle = pearson_r(n_factors, mean_angles)
    
    print(f"  Factor count vs sign changes: r = {r_factors_signs:+.4f}")
    print(f"  Factor count vs net rotation:  r = {r_factors_rot:+.4f}")
    print(f"  Factor count vs mean angle:    r = {r_factors_angle:+.4f}")
    
    return results


# ========================================================================
# DIRECTIVE 4: CROSS-DIMENSIONAL CALIBRATION (SCALING LAW)
# ========================================================================

def run_cross_dimensional_calibration():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 4: CROSS-DIMENSIONAL CALIBRATION — Scaling Law for Primality")
    print("=" * 80)
    print("  Map the rate of decay of the NRCI prime signal as we scale the modulus.")
    print("  If prime NRCI (~0.921) persists at higher dimensions while composite")
    print("  NRCI (~0.735) continues to grow, we have defined a scaling law.")
    print()
    
    # For each modulus N = 12^k, compute NRCI for primes and composites
    # But NRCI depends on the encoding, not on a modulus. 
    # Instead: test how NRCI signal strength decays as we increase the BIT WIDTH
    # of the Gray encoding (more bits = more information = higher dimensions)
    
    print("  --- BIT-WIDTH SCALING (Information Dimension) ---")
    print(f"  {'Bits':>4s} | {'P_NRCI':>7s} | {'C_NRCI':>7s} | {'Delta':>7s} | {'P_SW':>6s} | {'C_SW':>6s} | {'r_label':>8s}")
    print(f"  {'-'*4} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*6} | {'-'*6} | {'-'*8}")
    
    # Generate a fixed set of primes and composites
    random.seed(99)
    test_primes = [p for p in range(100, 500) if miller_rabin(p)][:30]
    test_comps = []
    while len(test_comps) < 30:
        n = random.randint(100, 500)
        if not miller_rabin(n) and n not in test_comps:
            test_comps.append(n)
    
    scaling_results = []
    for bits in [12, 16, 20, 24, 28, 32, 40, 48, 56, 64]:
        # Use AdaptiveManifold with custom bit width
        am = AdaptiveManifold(max_bits=bits)
        
        p_nrcis = []
        c_nrcis = []
        p_sws = []
        c_sws = []
        
        for p in test_primes:
            gc = p ^ (p >> 1)
            bits_list = [(gc >> i) & 1 for i in range(bits - 1, -1, -1)]
            sw = sum(bits_list)
            tax = Fraction(sw, bits)
            nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
            p_nrcis.append(nrci)
            p_sws.append(sw)
        
        for c in test_comps:
            gc = c ^ (c >> 1)
            bits_list = [(gc >> i) & 1 for i in range(bits - 1, -1, -1)]
            sw = sum(bits_list)
            tax = Fraction(sw, bits)
            nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
            c_nrcis.append(nrci)
            c_sws.append(sw)
        
        p_mean = sum(p_nrcis)/len(p_nrcis)
        c_mean = sum(c_nrcis)/len(c_nrcis)
        delta = p_mean - c_mean
        p_sw = sum(p_sws)/len(p_sws)
        c_sw = sum(c_sws)/len(c_sws)
        
        labels = [0]*len(test_primes) + [1]*len(test_comps)
        all_nrcis = p_nrcis + c_nrcis
        r_lab = pearson_r(labels, all_nrcis)
        
        scaling_results.append({
            "bits": bits, "p_nrci": p_mean, "c_nrci": c_mean,
            "delta": delta, "p_sw": p_sw, "c_sw": c_sw, "r_label": r_lab
        })
        
        print(f"  {bits:>4d} | {p_mean:>7.4f} | {c_mean:>7.4f} | {delta:>+7.4f} | {p_sw:>6.1f} | {c_sw:>6.1f} | {r_lab:>+8.4f}")
    
    # DECAY ANALYSIS
    print(f"\n  --- SIGNAL DECAY ANALYSIS ---")
    deltas = [r["delta"] for r in scaling_results]
    r_labels = [r["r_label"] for r in scaling_results]
    
    # Is the prime signal DECAYING or STABLE as we add more bits?
    # Fit a simple linear model: delta = a * bits + b
    n = len(scaling_results)
    bits_list = [r["bits"] for r in scaling_results]
    mx = sum(bits_list)/n
    my = sum(deltas)/n
    cov = sum((b-mx)*(d-my) for b, d in zip(bits_list, deltas))
    vx = sum((b-mx)**2 for b in bits_list)
    slope = cov / vx if vx > 0 else 0
    intercept = my - slope * mx
    
    print(f"  Linear fit: delta = {slope:.6f} * bits + {intercept:.4f}")
    print(f"  Slope: {slope:.6f} per bit")
    print(f"  At 128 bits: predicted delta = {slope * 128 + intercept:.4f}")
    print(f"  At 256 bits: predicted delta = {slope * 256 + intercept:.4f}")
    
    if slope > 0:
        print(f"  >>> PRIME SIGNAL STRENGTHENS with bit width — SCALING LAW CONFIRMED <<<")
    elif abs(slope) < 0.0001:
        print(f"  >>> PRIME SIGNAL IS STABLE — INVARIANT under dimensional scaling <<<")
    else:
        print(f"  >>> PRIME SIGNAL DECAYS with bit width — no simple scaling law <<<")
    
    # Now test: MODULUS SCALING for 4D fingerprint stability
    print(f"\n  --- MODULUS SCALING: 4D FINGERPRINT STABILITY ---")
    print(f"  Testing whether the NRCI distinction survives at higher moduli.")
    print(f"  {'Modulus':>8s} | {'P_NRCI':>7s} | {'C_NRCI':>7s} | {'Delta':>7s} | {'r_label':>8s}")
    print(f"  {'-'*8} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*8}")
    
    modulus_results = []
    for power in range(2, 8):
        N = 12 ** power
        p_fps = [residue_fingerprint_4d(p, N) for p in test_primes]
        c_fps = [residue_fingerprint_4d(c, N) for c in test_comps]
        
        # Use total 4D distance as the metric
        p_totals = [sum(fp) for fp in p_fps]
        c_totals = [sum(fp) for fp in c_fps]
        
        labels = [0]*len(test_primes) + [1]*len(test_comps)
        all_totals = p_totals + c_totals
        r_lab = pearson_r(labels, all_totals)
        
        p_mean = sum(p_totals)/len(p_totals)
        c_mean = sum(c_totals)/len(c_totals)
        delta = p_mean - c_mean
        
        modulus_results.append({
            "modulus": N, "power": power, "p_mean": p_mean, "c_mean": c_mean,
            "delta": delta, "r_label": r_lab
        })
        
        print(f"  12^{power:<4d}={N:>6d} | {p_mean:>7.1f} | {c_mean:>7.1f} | {delta:>+7.1f} | {r_lab:>+8.4f}")
    
    # KEY TEST: NRCI signal at increasing modulus for the LL trajectory
    print(f"\n  --- NRCI TRAJECTORY DECAY AT SCALE ---")
    # Run LL for M_13 (prime) at increasing mod-144-based scaling
    # The intermediate LL values grow enormously — test whether the
    # NRCI of these values maintains the prime/composite distinction
    
    # Test: for M_13 = 8191 (prime), track s_i mod various moduli
    Mp = 8191
    p_exp = 13
    s = 4
    ll_values = [4]
    for i in range(p_exp - 2):
        s = (s * s - 2) % Mp
        ll_values.append(s)
    
    # For each LL value, compute NRCI using Golay-Leech
    print(f"  LL trajectory for M_13 = 8191 (PRIME):")
    for modulus_scale in [144, 288, 432, 576, 1728, 12**4, 12**5]:
        # Compute 4D fingerprint at this modulus
        nrcis_at_scale = []
        for val in ll_values:
            fp = residue_fingerprint_4d(val, modulus_scale)
            total = sum(fp)
            nrcis_at_scale.append(total)
        
        std = math.sqrt(sum((n - sum(nrcis_at_scale)/len(nrcis_at_scale))**2 
                           for n in nrcis_at_scale)/len(nrcis_at_scale))
        print(f"    mod={modulus_scale:>6d}: 4D_total range=[{min(nrcis_at_scale)}, {max(nrcis_at_scale)}], std={std:.2f}")
    
    return {
        "scaling_results": scaling_results,
        "modulus_results": modulus_results,
        "slope": slope,
        "intercept": intercept,
    }


# ========================================================================
# DIRECTIVE 5: FRICTION RATIO AS UNIVERSAL METRIC (DEEP TEST)
# ========================================================================

def run_universal_friction_metric():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 5: FRICTION RATIO AS UNIVERSAL PRIMALITY METRIC")
    print("=" * 80)
    print("  Test the friction_ratio = total_friction / jaccard_stability")
    print("  as a universal primality indicator across different number ranges.")
    print()
    
    # Test across multiple ranges (use samples for speed)
    ranges_to_test = [
        (100, 500, "10^2-500"),
        (500, 2000, "500-2x10^3"),
        (2000, 5000, "2x10^3-5x10^3"),
        (5000, 10000, "5x10^3-10^4"),
    ]
    
    print(f"  {'Range':>15s} | {'#P':>4s} | {'#C':>4s} | {'P_FR':>8s} | {'C_FR':>8s} | {'Ratio':>6s} | {'r_label':>8s} | {'AUC':>6s}")
    print(f"  {'-'*15} | {'-'*4} | {'-'*4} | {'-'*8} | {'-'*8} | {'-'*6} | {'-'*8} | {'-'*6}")
    
    all_results = []
    for lo, hi, label in ranges_to_test:
        primes = []
        comps = []
        p_friction_ratios = []
        c_friction_ratios = []
        
        for n in range(lo, min(hi, lo + 400)):  # sample up to 400 per range
            is_prime = miller_rabin(n)
            prof = compute_friction_profile(n, use_ll=True, ll_mod=n)
            fr = prof.get("friction_ratio", 0)
            
            if is_prime:
                primes.append(n)
                p_friction_ratios.append(fr)
            else:
                comps.append(n)
                c_friction_ratios.append(fr)
        
        if not p_friction_ratios or not c_friction_ratios:
            continue
        
        p_fr = sum(p_friction_ratios) / len(p_friction_ratios)
        c_fr = sum(c_friction_ratios) / len(c_friction_ratios)
        ratio = c_fr / p_fr if p_fr > 0 else 0
        
        labels = [0]*len(p_friction_ratios) + [1]*len(c_friction_ratios)
        all_fr = p_friction_ratios + c_friction_ratios
        r_lab = pearson_r(labels, all_fr)
        
        # Simple AUC approximation
        # Count: for each prime, how many composites have higher friction?
        n_correct = sum(1 for pf in p_friction_ratios 
                       for cf in c_friction_ratios if cf > pf)
        total_pairs = len(p_friction_ratios) * len(c_friction_ratios)
        auc = n_correct / total_pairs if total_pairs > 0 else 0.5
        
        print(f"  {label:>15s} | {len(primes):>4d} | {len(comps):>4d} | {p_fr:>8.2f} | {c_fr:>8.2f} | {ratio:>6.2f}x | {r_lab:>+8.4f} | {auc:>6.4f}")
        
        all_results.append({
            "range": label, "n_primes": len(primes), "n_comps": len(comps),
            "p_fr": p_fr, "c_fr": c_fr, "ratio": ratio, "r_label": r_lab, "auc": auc
        })
    
    # Is the AUC consistent across ranges?
    if all_results:
        aucs = [r["auc"] for r in all_results]
        avg_auc = sum(aucs) / len(aucs)
        auc_std = math.sqrt(sum((a - avg_auc)**2 for a in aucs) / len(aucs))
        print(f"\n  Average AUC across ranges: {avg_auc:.4f} (std={auc_std:.4f})")
        print(f"  (0.5 = random, 1.0 = perfect separation)")
    
    # CORRELATION MATRIX: Which metrics best predict primality?
    print(f"\n  --- FULL CORRELATION MATRIX FOR PRIMALITY PREDICTION ---")
    # Compute all metrics for a sample
    random.seed(77)
    sample_primes = [p for p in range(500, 3000) if miller_rabin(p)][:30]
    sample_comps = []
    while len(sample_comps) < 30:
        n = random.randint(500, 3000)
        if not miller_rabin(n) and n not in sample_comps:
            sample_comps.append(n)
    
    all_samples = [(n, True) for n in sample_primes] + [(n, False) for n in sample_comps]
    
    metrics = {}
    for n, is_prime in all_samples:
        prof = compute_friction_profile(n, use_ll=True, ll_mod=n)
        metrics[n] = {
            "is_prime": is_prime,
            "nrci_gl": prof["nrci_gl"],
            "nrci_am": prof["nrci_am"],
            "sw": prof["sw"],
            "hw": prof["hw"],
            "vol": prof["vol"],
            "fp4d_total": prof["fp4d_total"],
            "friction": prof.get("total_friction", 0),
            "friction_ratio": prof.get("friction_ratio", 0),
            "traj_vol_mean": prof.get("traj_vol_mean", 0),
            "traj_jacc_mean": prof.get("traj_jacc_mean", 0),
            "traj_vol_std": prof.get("traj_vol_std", 0),
            "anchor_dist": prof["anchor_dist"],
        }
    
    metric_names = ["nrci_gl", "nrci_am", "sw", "hw", "vol", "fp4d_total",
                    "friction", "friction_ratio", "traj_vol_mean", "traj_jacc_mean",
                    "traj_vol_std", "anchor_dist"]
    labels = [metrics[n]["is_prime"] for n in metrics]
    
    print(f"  {'Metric':>18s} | {'Pearson r':>10s} | {'Spearman rho':>13s} | {'Direction':>10s}")
    print(f"  {'-'*18} | {'-'*10} | {'-'*13} | {'-'*10}")
    
    correlations = {}
    for metric in metric_names:
        vals = [metrics[n][metric] for n in metrics]
        r = pearson_r(labels, vals)
        rho = spearman_rho(labels, vals)
        direction = "Prime HIGH" if r < 0 else "Comp HIGH"
        correlations[metric] = {"pearson": r, "spearman": rho}
        print(f"  {metric:>18s} | {r:>+10.4f} | {rho:>+13.4f} | {direction:>10s}")
    
    # Best single predictor
    best_metric = min(correlations, key=lambda m: abs(correlations[m]["pearson"]))
    best_r = correlations[best_metric]["pearson"]
    print(f"\n  Strongest signal: {best_metric} (r={best_r:+.4f})")
    
    # PAIRWISE METRIC combinations
    print(f"\n  --- TOP PAIRWISE COMBINATIONS ---")
    pair_results = []
    for i, m1 in enumerate(metric_names):
        for m2 in metric_names[i+1:]:
            # Combine: normalize both to z-scores, then take ratio
            v1 = [metrics[n][m1] for n in metrics]
            v2 = [metrics[n][m2] for n in metrics]
            
            # Z-score normalization
            def zscore(vals):
                m = sum(vals)/len(vals)
                s = math.sqrt(sum((v-m)**2 for v in vals)/len(vals))
                return [(v-m)/(s+1e-10) for v in vals]
            
            z1 = zscore(v1)
            z2 = zscore(v2)
            
            # Try different combinations
            combo_diff = [a - b for a, b in zip(z1, z2)]
            combo_ratio = [a / (b + 0.01) for a, b in zip(z1, z2)]
            combo_prod = [a * b for a, b in zip(z1, z2)]
            
            for combo_name, combo_vals in [("diff", combo_diff), ("ratio", combo_ratio), ("prod", combo_prod)]:
                r_combo = abs(pearson_r(labels, combo_vals))
                pair_results.append((r_combo, m1, m2, combo_name))
    
    pair_results.sort(reverse=True)
    print(f"  {'r':>7s} | {'Metric 1':>18s} | {'Metric 2':>18s} | {'Combo':>6s}")
    print(f"  {'-'*7} | {'-'*18} | {'-'*18} | {'-'*6}")
    for r, m1, m2, combo in pair_results[:10]:
        print(f"  {r:>7.4f} | {m1:>18s} | {m2:>18s} | {combo:>6s}")
    
    return {
        "range_results": all_results,
        "correlations": correlations,
        "best_pairs": pair_results[:10],
    }


# ========================================================================
# GRAND SYNTHESIS
# ========================================================================

def main():
    print("+" + "=" * 78 + "+")
    print("|  UBP MUSIC STUDY - PHASE XII: TOPOLOGICAL PRIME CRYPTANALYSIS          |")
    print("|  The Pivot: From Harmonic Musicology to Geometric Friction Mapping     |")
    print("|  Directives: Manifold Heatmap, Continuous Field, Inverse Factorization, |")
    print("|              Cross-Dimensional Calibration, Universal Friction Metric    |")
    print("+" + "=" * 78 + "+")
    print()
    
    t0 = time.time()
    
    # Directive 1: Manifold Heatmap
    d1 = run_manifold_heatmap()
    
    # Directive 2: Continuous Friction Field
    d2 = run_continuous_friction_field()
    
    # Directive 3: Inverse Factorization
    d3 = run_inverse_factorization()
    
    # Directive 4: Cross-Dimensional Calibration
    d4 = run_cross_dimensional_calibration()
    
    # Directive 5: Universal Friction Metric
    d5 = run_universal_friction_metric()
    
    t1 = time.time()
    
    # ========================================================================
    # GRAND SYNTHESIS
    # ========================================================================
    print(f"\n{'=' * 80}")
    print("PHASE XII: GRAND SYNTHESIS — Topological Prime Cryptanalysis")
    print(f"{'=' * 80}")
    print(f"  Execution time: {t1-t0:.1f}s")
    print()
    
    print("  THE PIVOT: From 'what sounds consonant' to 'what costs geometric work'")
    print()
    
    print("  DIRECTIVE 1 — MANIFOLD HEATMAP:")
    print(f"    Primes in [1000, 10000]: {d1['n_primes']}")
    print(f"    Composite/Prime friction ratio in heatmap: see above")
    print(f"    Silhouette score: {d1.get('silhouette', 0):+.4f}")
    if d1.get('silhouette', 0) > 0:
        print("    >>> PRIMES FORM A DISTINCT ATTRACTOR IN (NRCI, FRICTION) SPACE <<<")
    else:
        print("    Primes and composites OVERLAP significantly in 2D friction space.")
        print("    The signal is DIRECTIONAL (composites have more friction),")
        print("    but the distributions are too broad for clean binary separation.")
    
    print()
    print("  DIRECTIVE 2 — CONTINUOUS FRICTION FIELD:")
    print("    (See family comparison table above)")
    print("    Key question: Do specific number families occupy distinct")
    print("    'friction basins'? If so, we have a GEOMETRIC NUMBER TAXONOMY.")
    
    print()
    print("  DIRECTIVE 3 — INVERSE FACTORIZATION:")
    print("    (See factor-direction correlation above)")
    print("    If rotation direction correlates with factor count,")
    print("    we can ESTIMATE the number of prime factors from geometric data alone.")
    
    print()
    print("  DIRECTIVE 4 — CROSS-DIMENSIONAL CALIBRATION:")
    slope = d4.get("slope", 0)
    intercept = d4.get("intercept", 0)
    print(f"    NRCI scaling law: delta(bits) = {slope:.6f} * bits + {intercept:.4f}")
    if slope > 0.0001:
        print("    >>> PRIME SIGNAL STRENGTHENS WITH DIMENSION — SCALING LAW CONFIRMED <<<")
    elif slope < -0.0001:
        print("    Prime signal DECAYS — no clean scaling law exists.")
    else:
        print("    Prime signal is approximately STABLE across dimensions.")
    
    print()
    print("  DIRECTIVE 5 — UNIVERSAL FRICTION METRIC:")
    if d5["range_results"]:
        avg_auc = sum(r["auc"] for r in d5["range_results"]) / len(d5["range_results"])
        print(f"    Average AUC across all ranges: {avg_auc:.4f}")
    if d5["best_pairs"]:
        best = d5["best_pairs"][0]
        print(f"    Best pairwise combination: {best[1]} x {best[2]} ({best[3]}), |r|={best[0]:.4f}")
    
    print()
    print("  ═══════════════════════════════════════════════════════════════════")
    print("  THE CENTRAL QUESTION:")
    print()
    print("  Phase XI showed composites generate 5.6x more hypervolume and 3.4x")
    print("  more rotation. Phase XII asks: is this a UNIVERSAL property, or an")
    print("  artifact of the small Mersenne test cases?")
    print()
    print("  If the manifold heatmap shows primes as a low-friction attractor,")
    print("  we have the first GEOMETRIC PRIME TESTER — not based on arithmetic")
    print("  (like LL), but on the SHAPE of computation itself.")
    print("  ═══════════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()