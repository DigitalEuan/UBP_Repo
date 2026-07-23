"""
UBP x RLS Fusion Study — Phase XIV: Extended Grid, Fine Resolution,
Higher-Order Prime Distribution, and 3D Temporal Structure
======================================================================

Extensions over Phase XIII:
  1. 10^6-cell RLS grid (20x expansion)
  2. 1-degree angular resolution (360 sectors, vs 36 at 10 deg)
  3. Prime k-tuple spatial analysis (twins, cousins, sexy, triplets, quadruplets)
  4. Hardy-Littlewood conjecture testing across angular sectors
  5. Short-interval angular distribution of primes
  6. 3D RLS structure with Time dimension
  7. Higher-dimensional projection analysis

Key question from user:
  "These 2D projections may have a 3D structure as a counterpart...
   I would be interested to see what the 3D version is doing when
   Time is involved."
"""

import math
import time
import sys
import json
import random
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, '/home/z/my-project')
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine, AdaptiveManifold

# ════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════

MODULUS = 144
RESIDUES = [1, 5, 7, 11]  # First 4 odd primes mod-144 reference points

# Hardy-Littlewood k-tuple constants (admissible patterns)
# C(H) = product_{p} (1 - v_p(H)/p) * (1 - 1/p)^(-k)  for pattern H
# where v_p(H) = number of distinct residue classes mod p occupied by H

def mod_dist(r, target, mod):
    return min(abs(r - target), mod - abs(r - target))

def residue_fingerprint_4d(n, modulus=MODULUS):
    """4D prime residue fingerprint: distances to reference primes mod-144."""
    r = n % modulus
    return [mod_dist(r, res, modulus) for res in RESIDUES]

def miller_rabin(n, k=12):
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
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

# ════════════════════════════════════════════════════════════════════════
# OPTIMIZED RLS GRID CONSTRUCTION
# ════════════════════════════════════════════════════════════════════════

def build_rls_grid_fast(max_n):
    """
    Optimized RLS grid construction for large N.
    Returns list of dicts: n, i, j, m, layer_idx, angle_rad, angle_deg, radius
    """
    cells = []
    n = 0
    m = 0
    layer_idx = 0

    while n < max_n:
        # Find all (i,j) with i^2 + j^2 = m
        max_ij = int(math.isqrt(m)) + 1
        layer_cells = []

        for i in range(-max_ij, max_ij + 1):
            j_sq = m - i * i
            if j_sq < 0:
                continue
            j = int(math.isqrt(j_sq))
            if j * j == j_sq:
                layer_cells.append((i, j))
                if j != 0:
                    layer_cells.append((i, -j))

        # Deduplicate
        seen = set()
        unique = []
        for pair in layer_cells:
            if pair not in seen:
                seen.add(pair)
                unique.append(pair)

        if not unique:
            m += 1
            continue

        # Sort by angle
        unique.sort(key=lambda p: math.atan2(p[1], p[0]) % (2 * math.pi))

        for (i, j) in unique:
            n += 1
            if n > max_n:
                break
            angle = math.atan2(j, i)
            if angle < 0:
                angle += 2 * math.pi
            cells.append({
                "n": n, "i": i, "j": j, "m": m,
                "layer_idx": layer_idx,
                "angle_rad": angle,
                "angle_deg": math.degrees(angle),
                "radius": math.sqrt(m),
            })

        layer_idx += 1
        m += 1

    return cells


# ════════════════════════════════════════════════════════════════════════
# UBP METRICS (lightweight for bulk computation)
# ════════════════════════════════════════════════════════════════════════

# Initialize UBP engines once
_golay = GolayCodeEngine()
_leech = LeechLatticeEngine(golay=_golay)
_am = AdaptiveManifold()


def ubp_nrci_golay_leech(n):
    gc = abs(n) ^ (abs(n) >> 1)
    bits = [(gc >> i) & 1 for i in range(23, -1, -1)]
    decoded, correctable, anchor_dist = _golay.decode(bits)
    cw = _golay.encode(decoded)
    nrci = float(_leech.calculate_nrci(cw))
    hw = sum(cw)
    return {"nrci_gl": nrci, "hw": hw, "anchor_dist": anchor_dist}


def ubp_nrci_adaptive(n):
    fp = _am.fingerprint(n)
    return {"nrci_am": fp["nrci"], "sw_am": fp["sw"], "on_lattice": fp["on_lattice"]}


def rotation_sign_changes_fast(n, max_iter=10):
    """Optimized rotation sign changes for bulk use."""
    if n <= 3 or n % 2 == 0:
        return 0, 0, 0, 0

    Mp = n
    s = 4
    trace = []
    iters = min(max_iter, max(2, int(math.log2(max(Mp, 4))) - 2))

    for _ in range(iters + 1):
        fp4d = residue_fingerprint_4d(s)
        trace.append(fp4d)
        s = (s * s - 2) % Mp

    if len(trace) < 3:
        return 0, 0, 0, 0

    directions = []
    for idx in range(1, len(trace)):
        d = [trace[idx][j] - trace[idx-1][j] for j in range(4)]
        directions.append(d)

    if len(directions) < 2:
        return 0, 0, 0, 0

    rotation_signs = []
    angles = []
    for idx in range(1, len(directions)):
        cross = (directions[idx][0] * directions[idx-1][1] -
                 directions[idx][1] * directions[idx-1][0])
        rotation_signs.append(1 if cross > 0 else (-1 if cross < 0 else 0))

        dot = sum(a * b for a, b in zip(directions[idx], directions[idx-1]))
        n1 = math.sqrt(sum(a * a for a in directions[idx])) + 1e-10
        n2 = math.sqrt(sum(a * a for a in directions[idx-1])) + 1e-10
        cos_a = max(-1, min(1, dot / (n1 * n2)))
        angles.append(math.acos(cos_a))

    sign_changes = sum(1 for i in range(1, len(rotation_signs))
                       if rotation_signs[i] != rotation_signs[i-1])
    net_rot = sum(rotation_signs)
    mean_a = sum(angles) / len(angles) if angles else 0
    std_a = math.sqrt(sum((a - mean_a)**2 for a in angles) / len(angles)) if angles else 0

    return sign_changes, net_rot, mean_a, std_a


def compute_ubp_metrics_fast(n):
    """Lightweight UBP metrics for bulk computation."""
    gl = ubp_nrci_golay_leech(n)
    am = ubp_nrci_adaptive(n)
    rsc, net_rot, mean_a, std_a = rotation_sign_changes_fast(n)

    return {
        "n": n,
        "nrci_gl": gl["nrci_gl"],
        "hw": gl["hw"],
        "anchor_dist": gl["anchor_dist"],
        "nrci_am": am["nrci_am"],
        "sw_am": am["sw_am"],
        "rot_sign_changes": rsc,
        "net_rotation": net_rot,
        "mean_angle": mean_a,
        "angle_std": std_a,
    }


# ════════════════════════════════════════════════════════════════════════
# STATISTICS UTILITIES
# ════════════════════════════════════════════════════════════════════════

def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0, 0.0
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    vx = sum((x-mx)**2 for x in xs)
    vy = sum((y-my)**2 for y in ys)
    if vx == 0 or vy == 0:
        return 0.0, 0.0
    r = cov / math.sqrt(vx * vy)
    return r, r**2


def spearman_rho(xs, ys):
    """Spearman rank correlation."""
    n = len(xs)
    if n < 3:
        return 0.0
    rx = sorted(range(n), key=lambda i: xs[i])
    ry = sorted(range(n), key=lambda i: ys[i])
    rank_x = [0]*n
    rank_y = [0]*n
    for rnk, idx in enumerate(rx):
        rank_x[idx] = rnk + 1
    for rnk, idx in enumerate(ry):
        rank_y[idx] = rnk + 1
    return pearson_r(rank_x, rank_y)[0]


def angular_sector_analysis(cells, n_sectors=360):
    """Divide circle into n_sectors angular bins."""
    sector_width = 360.0 / n_sectors
    sectors = defaultdict(lambda: {"ns": [], "metrics": []})

    for cell in cells:
        s_idx = int(cell["angle_deg"] / sector_width) % n_sectors
        sectors[s_idx]["ns"].append(cell["n"])
        sectors[s_idx]["metrics"].append(cell)

    sector_stats = []
    metric_keys = ["nrci_gl", "nrci_am", "rot_sign_changes",
                    "net_rotation", "mean_angle", "hw", "anchor_dist"]

    for s_idx in range(n_sectors):
        cells_in = sectors[s_idx]["metrics"]
        if not cells_in:
            continue
        n_total = len(cells_in)
        n_primes = sum(1 for c in cells_in if c.get("is_prime", False))
        prime_density = n_primes / n_total

        means = {}
        for key in metric_keys:
            vals = [c[key] for c in cells_in if key in c]
            means[key] = sum(vals) / len(vals) if vals else 0

        radii = [c["radius"] for c in cells_in]
        sector_stats.append({
            "sector": s_idx,
            "angle_mid": (s_idx + 0.5) * sector_width,
            "n_total": n_total,
            "n_primes": n_primes,
            "prime_density": prime_density,
            "mean_radius": sum(radii)/len(radii) if radii else 0,
            **means,
        })

    sector_stats.sort(key=lambda x: x["sector"])
    return sector_stats


# ════════════════════════════════════════════════════════════════════════
# PRIME K-TUPLE ANALYSIS
# ════════════════════════════════════════════════════════════════════════

def find_k_tuples(rls_cells, max_n):
    """
    Find prime k-tuples in the RLS grid.
    Returns dict mapping tuple_type -> list of (n, rls_angle, rls_radius, layer)
    """
    # Build fast lookup: n -> cell
    n_to_cell = {}
    primes_set = set()
    for c in rls_cells:
        n_to_cell[c["n"]] = c
        if c.get("is_prime", False):
            primes_set.add(c["n"])

    tuples = {
        "twins": [],          # (p, p+2)
        "cousins": [],        # (p, p+4)
        "sexy": [],           # (p, p+6)
        "triplets_1": [],     # (p, p+2, p+6)
        "triplets_2": [],     # (p, p+4, p+6)
        "quadruplets": [],    # (p, p+2, p+6, p+8)
    }

    # Scan for tuples
    for p in sorted(primes_set):
        # Twins
        if p + 2 in primes_set:
            cell = n_to_cell[p]
            tuples["twins"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })
        # Cousins
        if p + 4 in primes_set:
            cell = n_to_cell[p]
            tuples["cousins"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })
        # Sexy
        if p + 6 in primes_set:
            cell = n_to_cell[p]
            tuples["sexy"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })
        # Triplets type 1: (p, p+2, p+6)
        if (p + 2 in primes_set) and (p + 6 in primes_set):
            cell = n_to_cell[p]
            tuples["triplets_1"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })
        # Triplets type 2: (p, p+4, p+6)
        if (p + 4 in primes_set) and (p + 6 in primes_set):
            cell = n_to_cell[p]
            tuples["triplets_2"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })
        # Quadruplets: (p, p+2, p+6, p+8)
        if (p+2 in primes_set) and (p+6 in primes_set) and (p+8 in primes_set):
            cell = n_to_cell[p]
            tuples["quadruplets"].append({
                "p": p, "angle": cell["angle_deg"], "radius": cell["radius"],
                "layer": cell["layer_idx"], "m": cell["m"]
            })

    return tuples


def hardy_littlewood_constant(pattern):
    """
    Compute the Hardy-Littlewood constant C for a prime k-tuple pattern.
    C(H) = prod_p (1 - 1/p)^(-1-k) * prod_p (1 - v_p(H)/p)

    For the first Hardy-Littlewood conjecture:
    pi_2(N; H) ~ C(H) * integral_2^N dt / (log t)^k
    """
    k = len(pattern)
    # Compute product over primes
    # We compute for primes up to a reasonable limit
    primes_hl = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

    product = 1.0
    for p in primes_hl:
        # v_p(H) = number of distinct residue classes mod p occupied by the pattern
        residues = set((h % p) for h in pattern)
        v_p = len(residues)
        if v_p == p:
            # All residue classes covered -> inadmissible, C=0
            return 0.0
        if v_p > 0:
            product *= (1.0 - v_p / p) / ((1.0 - 1.0/p) ** k)
        else:
            product *= 1.0 / ((1.0 - 1.0/p) ** k)

    return product


def k_tuple_angular_distribution(tuples_list, n_sectors=36):
    """Compute angular distribution of k-tuples."""
    sector_width = 360.0 / n_sectors
    counts = [0] * n_sectors
    for t in tuples_list:
        s_idx = int(t["angle"] / sector_width) % n_sectors
        counts[s_idx] += 1
    return counts


# ════════════════════════════════════════════════════════════════════════
# SHORT-INTERVAL ANGULAR ANALYSIS
# ════════════════════════════════════════════════════════════════════════

def short_interval_angular(rls_cells, window_size="sqrt"):
    """
    For numbers in short intervals [x, x+sqrt(x)], analyze the angular
    distribution of primes. Tests whether the RLS angular bias persists
    at the finest scale.
    """
    # Select anchor points at logarithmic intervals
    anchors = []
    n_max = max(c["n"] for c in rls_cells)
    for exp in range(3, int(math.log10(n_max))):
        x = 10 ** exp
        w = int(math.sqrt(x))
        anchors.append((x, x + w, w))

    n_to_cell = {c["n"]: c for c in rls_cells}

    results = []
    for (x_lo, x_hi, w) in anchors:
        primes_in_window = []
        for n in range(x_lo, min(x_hi, n_max + 1)):
            if n in n_to_cell and n_to_cell[n].get("is_prime", False):
                primes_in_window.append(n_to_cell[n])

        if len(primes_in_window) < 3:
            continue

        # Angular distribution in this window
        angles = [c["angle_deg"] for c in primes_in_window]
        mean_angle = sum(angles) / len(angles)

        # Rayleigh test for uniformity
        n_primes = len(angles)
        C = sum(math.cos(math.radians(a)) for a in angles) / n_primes
        S = sum(math.sin(math.radians(a)) for a in angles) / n_primes
        R = math.sqrt(C**2 + S**2)  # Mean resultant length

        # Angular spread (circular std dev)
        angular_std = math.sqrt(-2 * math.log(max(R, 1e-10)))

        results.append({
            "x_center": (x_lo + x_hi) / 2,
            "window_size": w,
            "n_primes": n_primes,
            "mean_angle": mean_angle,
            "R": R,  # Rayleigh R (0=uniform, 1=concentrated)
            "angular_std": angular_std,
            "angles": angles[:20],  # Store first 20 for reference
        })

    return results


# ════════════════════════════════════════════════════════════════════════
# 3D RLS STRUCTURE WITH TIME
# ════════════════════════════════════════════════════════════════════════

def build_3d_rls(max_n, time_mode="layer"):
    """
    Build 3D RLS where the 3rd dimension represents Time.

    Time modes:
      "layer"  - z = layer index m (the natural RLS layering)
      "ll_step"- z = Lucas-Lehmer iteration step (dynamic time)
      "n"      - z = log(n) (logarithmic time / natural ordering)

    Returns cells with x, y, z, angle, radius, is_prime, n
    """
    cells_2d = build_rls_grid_fast(max_n)

    for c in cells_2d:
        c["is_prime"] = miller_rabin(c["n"])

        if time_mode == "layer":
            c["z"] = c["layer_idx"]
        elif time_mode == "n":
            c["z"] = math.log(c["n"]) if c["n"] > 1 else 0
        elif time_mode == "ll_step":
            # For primes, z = number of LL iterations before reaching fixed point
            # For composites, z = same
            if c["n"] > 3 and c["n"] % 2 == 1:
                s = 4
                Mp = c["n"]
                steps = 0
                for _ in range(20):
                    s_new = (s * s - 2) % Mp
                    if s_new == s:
                        break
                    s = s_new
                    steps += 1
                c["z"] = steps
            else:
                c["z"] = 0

        c["x"] = c["i"]
        c["y"] = c["j"]

    return cells_2d


# ════════════════════════════════════════════════════════════════════════
# HIGHER-DIMENSIONAL PROJECTION ANALYSIS
# ════════════════════════════════════════════════════════════════════════

def projection_analysis(cells_3d, n_sectors_2d=36, n_bands_z=10):
    """
    Analyze whether the 3D structure reveals patterns invisible in 2D projection.

    Compare:
      1. 2D angular correlation (x-y projection)
      2. 2D z-slice correlations (prime density in z-slices)
      3. 3D voxel correlations (angular sectors × z-bands)
    """
    sector_w = 360.0 / n_sectors_2d
    z_values = [c["z"] for c in cells_3d]
    z_min, z_max = min(z_values), max(z_values)
    z_band_w = (z_max - z_min) / n_bands_z if z_max > z_min else 1

    # 3D voxel grid: sectors × z-bands
    voxel_grid = defaultdict(lambda: {"total": 0, "primes": 0})

    for c in cells_3d:
        s_idx = int(c["angle_deg"] / sector_w) % n_sectors_2d
        z_idx = int((c["z"] - z_min) / z_band_w) if z_band_w > 0 else 0
        z_idx = min(z_idx, n_bands_z - 1)
        voxel_grid[(s_idx, z_idx)]["total"] += 1
        if c["is_prime"]:
            voxel_grid[(s_idx, z_idx)]["primes"] += 1

    # Compute per-voxel prime density
    voxel_data = []
    for (s, z), counts in voxel_grid.items():
        if counts["total"] >= 5:
            voxel_data.append({
                "sector": s, "z_band": z,
                "angle_mid": (s + 0.5) * sector_w,
                "z_mid": z_min + (z + 0.5) * z_band_w,
                "n_total": counts["total"],
                "n_primes": counts["primes"],
                "prime_density": counts["primes"] / counts["total"],
            })

    return voxel_data, z_min, z_max


# ════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 80)
    print("PHASE XIV: UBP x RLS FUSION — Extended Grid, Fine Resolution,")
    print("            Higher-Order Primes, and 3D Temporal Structure")
    print("=" * 80)
    print()

    MAX_N = 1_000_000
    UBP_SAMPLE_SIZE = 200_000  # Compute full UBP metrics for a sample
    random.seed(42)

    # ═══════════════════════════════════════════════════════════════
    # PART A: BUILD 10^6 RLS GRID
    # ═══════════════════════════════════════════════════════════════
    print("PART A: Constructing 10^6-cell RLS Grid...")
    t0 = time.time()
    rls_cells = build_rls_grid_fast(MAX_N)
    t1 = time.time()

    n_layers = max(c["layer_idx"] for c in rls_cells)
    max_m = max(c["m"] for c in rls_cells)
    max_radius = max(c["radius"] for c in rls_cells)

    # Tag primes
    print("  Tagging primes (Miller-Rabin k=12)...")
    t_primes = time.time()
    for c in rls_cells:
        c["is_prime"] = miller_rabin(c["n"])
    t_primes_done = time.time()

    n_primes = sum(1 for c in rls_cells if c["is_prime"])

    print(f"  Grid: {len(rls_cells)} cells, {n_layers} layers, "
          f"m_max={max_m}, r_max={max_radius:.1f}")
    print(f"  Primes: {n_primes}/{len(rls_cells)} ({100*n_primes/len(rls_cells):.2f}%)")
    print(f"  Grid build: {t1-t0:.1f}s, Prime tagging: {t_primes_done-t_primes:.1f}s")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART B: 1-DEGREE ANGULAR ANALYSIS (PRIME DENSITY ONLY)
    # ═══════════════════════════════════════════════════════════════
    print("PART B: 1-Degree Angular Resolution Analysis (360 sectors)")
    print("-" * 70)

    sector_stats_1deg = angular_sector_analysis(rls_cells, n_sectors=360)
    pd_360 = [s["prime_density"] for s in sector_stats_1deg]

    # Basic statistics
    pd_mean = sum(pd_360) / len(pd_360)
    pd_std = math.sqrt(sum((p - pd_mean)**2 for p in pd_360) / len(pd_360))
    pd_max = max(pd_360)
    pd_min = min(pd_360)
    pd_max_sector = sector_stats_1deg[pd_360.index(pd_max)]
    pd_min_sector = sector_stats_1deg[pd_360.index(pd_min)]

    print(f"  Prime density across 360 sectors:")
    print(f"    Mean: {pd_mean:.4f}  Std: {pd_std:.4f}  CV: {pd_std/pd_mean:.4f}")
    print(f"    Max:  {pd_max:.4f} at sector {pd_max_sector['sector']} "
          f"({pd_max_sector['angle_mid']:.1f} deg)")
    print(f"    Min:  {pd_min:.4f} at sector {pd_min_sector['sector']} "
          f"({pd_min_sector['angle_mid']:.1f} deg)")
    print(f"    Range ratio: {pd_max/max(pd_min, 1e-10):.2f}x")
    print()

    # Autocorrelation of prime density (circular)
    print("  Circular autocorrelation of 1-degree prime density:")
    best_lag_r = 0
    best_lag = 0
    autocorr = []
    for lag in range(1, 180):
        shifted = pd_360[lag:] + pd_360[:lag]
        r, _ = pearson_r(pd_360, shifted)
        autocorr.append((lag, r))
        if abs(r) > abs(best_lag_r):
            best_lag_r = r
            best_lag = lag

    print(f"    Peak autocorrelation: r={best_lag_r:+.4f} at lag={best_lag} deg")
    # Check for 90-degree periodicity (4-fold symmetry)
    r_90, _ = pearson_r(pd_360, pd_360[90:] + pd_360[:90])
    r_45, _ = pearson_r(pd_360, pd_360[45:] + pd_360[:45])
    r_180, _ = pearson_r(pd_360, pd_360[180:] + pd_360[:180])
    print(f"    Symmetry tests: 45 deg r={r_45:+.4f}, "
          f"90 deg r={r_90:+.4f}, 180 deg r={r_180:+.4f}")
    print()

    # Compare with 10-degree sectors for consistency
    print("  Cross-validation: 10-degree vs 1-degree sector means")
    sector_stats_10deg = angular_sector_analysis(rls_cells, n_sectors=36)
    pd_36 = [s["prime_density"] for s in sector_stats_10deg]

    # Downsample 1-degree to 10-degree and compare
    pd_1deg_downsampled = []
    for s10 in range(36):
        sector_cells = [s for s in sector_stats_1deg
                       if s10 * 10 <= s["angle_mid"] < (s10 + 1) * 10]
        if sector_cells:
            total = sum(s["n_total"] for s in sector_cells)
            primes = sum(s["n_primes"] for s in sector_cells)
            pd_1deg_downsampled.append(primes / total if total > 0 else 0)

    r_consistency, _ = pearson_r(pd_36, pd_1deg_downsampled)
    print(f"    Consistency r(10deg, 1deg-downsampled) = {r_consistency:.6f}")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART C: UBP METRICS FOR SAMPLE + 1-DEGREE CORRELATION
    # ═══════════════════════════════════════════════════════════════
    print(f"PART C: UBP Metrics Computation ({UBP_SAMPLE_SIZE:,} sampled cells)")
    print("-" * 70)

    # Stratified sample: ensure representation across all radii
    sample_indices = sorted(random.sample(range(len(rls_cells)),
                                           min(UBP_SAMPLE_SIZE, len(rls_cells))))
    sample_cells = [rls_cells[i] for i in sample_indices]

    t0 = time.time()
    for i, cell in enumerate(sample_cells):
        metrics = compute_ubp_metrics_fast(cell["n"])
        cell.update(metrics)
        if (i + 1) % 20000 == 0:
            print(f"  ... {i+1}/{len(sample_cells)} ({100*(i+1)/len(sample_cells):.0f}%)")

    t1 = time.time()
    print(f"  UBP metrics computed in {t1-t0:.1f}s ({len(sample_cells)/(t1-t0):.0f} cells/s)")
    print()

    # 1-degree angular correlation with UBP metrics
    print("  1-Degree Angular Correlation (sampled UBP metrics):")
    sector_stats_1deg_ubp = angular_sector_analysis(sample_cells, n_sectors=360)
    pd_360_ubp = [s["prime_density"] for s in sector_stats_1deg_ubp]

    metric_names = {
        "nrci_gl": "NRCI (Golay-Leech)",
        "nrci_am": "NRCI (AdaptiveManifold)",
        "rot_sign_changes": "Rotation Sign Changes",
        "net_rotation": "Net Rotation",
        "mean_angle": "Mean Angle",
        "anchor_dist": "Anchor Distance",
        "hw": "Hamming Weight",
    }

    corr_1deg = {}
    for key, name in metric_names.items():
        mv = [s[key] for s in sector_stats_1deg_ubp]
        r, r2 = pearson_r(pd_360_ubp, mv)
        rho = spearman_rho(pd_360_ubp, mv)
        corr_1deg[key] = {"pearson_r": r, "R2": r2, "spearman_rho": rho}
        sig = "***" if abs(r) > 0.5 else ("**" if abs(r) > 0.3 else ("*" if abs(r) > 0.15 else ""))
        print(f"    {name:<30s}: r={r:+.4f} rho={rho:+.4f} R2={r2:.4f} {sig}")

    # Compare: 1-degree (360 sectors) vs 10-degree (36 sectors) correlation stability
    print()
    print("  Correlation Stability: 10-deg vs 1-deg")
    sector_stats_10deg_ubp = angular_sector_analysis(sample_cells, n_sectors=36)
    pd_36_ubp = [s["prime_density"] for s in sector_stats_10deg_ubp]

    for key, name in metric_names.items():
        mv_36 = [s[key] for s in sector_stats_10deg_ubp]
        mv_360 = [s[key] for s in sector_stats_1deg_ubp]
        r_36, _ = pearson_r(pd_36_ubp, mv_36)
        r_360, _ = pearson_r(pd_360_ubp, mv_360)
        delta = r_360 - r_36
        stable = "STABLE" if abs(delta) < 0.1 else "SHIFTED"
        print(f"    {name:<30s}: r_36={r_36:+.4f} -> r_360={r_360:+.4f} "
              f"(delta={delta:+.4f}) [{stable}]")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART D: PRIME K-TUPLE ANALYSIS
    # ═══════════════════════════════════════════════════════════════
    print("PART D: Prime K-Tuple Spatial Analysis")
    print("-" * 70)
    t0 = time.time()
    k_tuples = find_k_tuples(rls_cells, MAX_N)
    t1 = time.time()
    print(f"  K-tuple scan completed in {t1-t0:.1f}s")

    for name, tlist in k_tuples.items():
        print(f"  {name:<15s}: {len(tlist):>6d} occurrences")

    # Angular distribution of k-tuples
    print()
    print("  Angular distribution of k-tuples (36 sectors):")
    n_sectors_kt = 36

    for name, tlist in k_tuples.items():
        if not tlist:
            continue
        counts = k_tuple_angular_distribution(tlist, n_sectors_kt)
        total = sum(counts)
        if total == 0:
            continue

        # Compare k-tuple density vs prime density
        prime_density_36 = [s["prime_density"] for s in sector_stats_10deg]
        kt_density = [c / max(sum(s["n_total"] for s in sector_stats_10deg
                                  if s["sector"] == i) / len(sector_stats_10deg), 1)
                      for i, c in enumerate(counts)]
        # Normalize: k-tuples per prime
        kt_per_prime = []
        for i in range(n_sectors_kt):
            s = sector_stats_10deg[i]
            if s["n_primes"] > 0:
                kt_per_prime.append(counts[i] / s["n_primes"])
            else:
                kt_per_prime.append(0)

        r_kt_primes, _ = pearson_r(prime_density_36, kt_density)
        r_kt_norm, _ = pearson_r(prime_density_36, kt_per_prime)

        # Rayleigh test for k-tuple angular uniformity
        angles = [t["angle"] for t in tlist]
        C = sum(math.cos(math.radians(a)) for a in angles) / len(angles)
        S = sum(math.sin(math.radians(a)) for a in angles) / len(angles)
        R = math.sqrt(C**2 + S**2)

        print(f"    {name:<15s}: r(density)={r_kt_primes:+.4f} "
              f"r(per_prime)={r_kt_norm:+.4f} "
              f"Rayleigh_R={R:.4f} "
              f"({'clustered' if R > 0.05 else 'uniform'})")
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART E: HARDY-LITTLEWOOD CONJECTURE TESTING
    # ═══════════════════════════════════════════════════════════════
    print("PART E: Hardy-Littlewood Conjecture Testing")
    print("-" * 70)

    # Compute HL constants for standard patterns
    patterns = {
        "twins": (0, 2),
        "cousins": (0, 4),
        "sexy": (0, 6),
        "triplet_1": (0, 2, 6),
        "triplet_2": (0, 4, 6),
        "quadruplet": (0, 2, 6, 8),
    }

    hl_results = {}
    for name, pattern in patterns.items():
        C = hardy_littlewood_constant(pattern)
        k = len(pattern)

        # Count observed tuples
        observed = len(k_tuples.get(name, []))

        # Expected count via Hardy-Littlewood (integral approximation)
        # pi_k(N; H) ~ C * N / (log N)^k  for large N
        if C > 0 and k > 0:
            log_N = math.log(MAX_N)
            expected = C * MAX_N / (log_N ** k)
        else:
            expected = 0

        ratio = observed / expected if expected > 0 else float('inf')

        hl_results[name] = {
            "pattern": pattern, "k": k,
            "C_HL": C, "observed": observed,
            "expected": expected, "ratio": ratio,
        }

        print(f"  {name:<15s}: C={C:.4f}  "
              f"observed={observed:>6d}  expected={expected:>8.1f}  "
              f"ratio={ratio:.4f}")

    # Test HL sector-by-sector (angular bias)
    print()
    print("  Sector-wise Hardy-Littlewood deviation (twin primes, 36 sectors):")
    n_sectors_hl = 36
    sector_w_hl = 360.0 / n_sectors_hl

    # Build n-to-cell lookup
    n_to_cell = {c["n"]: c for c in rls_cells}
    primes_in_grid = set(c["n"] for c in rls_cells if c["is_prime"])

    twin_sector_observed = [0] * n_sectors_hl
    twin_sector_expected = [0.0] * n_sectors_hl

    for p in sorted(primes_in_grid):
        if p + 2 in primes_in_grid:
            cell = n_to_cell[p]
            s_idx = int(cell["angle_deg"] / sector_w_hl) % n_sectors_hl
            twin_sector_observed[s_idx] += 1

            # Expected twins in this sector (proportional to sector prime count)
            twin_sector_expected[s_idx] += 1.0  # Will normalize

    # Normalize expected by total twin primes / total sectors
    total_obs = sum(twin_sector_observed)
    if total_obs > 0:
        # Expected = uniform distribution
        expected_per_sector = total_obs / n_sectors_hl
        chi_sq = sum((o - expected_per_sector)**2 / expected_per_sector
                     for o in twin_sector_observed)

        # Chi-squared test
        # For 36 sectors, df=35, critical value at p=0.05 is ~49.8
        print(f"    Chi-squared (uniform) = {chi_sq:.1f}  (df=35, critical=49.8)")
        print(f"    {'REJECT uniformity' if chi_sq > 49.8 else 'Cannot reject uniformity'}")

        # Angular bias ratio
        max_obs = max(twin_sector_observed)
        min_obs = min(twin_sector_observed)
        print(f"    Max/min sector ratio: {max_obs}/{max(min_obs,1)} = "
              f"{max_obs/max(min_obs,1):.2f}x")

    print()

    # ═══════════════════════════════════════════════════════════════
    # PART F: SHORT-INTERVAL ANGULAR DISTRIBUTION
    # ═══════════════════════════════════════════════════════════════
    print("PART F: Short-Interval Angular Distribution of Primes")
    print("-" * 70)
    print("  Testing: do primes in [x, x+sqrt(x)] show angular clustering on RLS?")
    print()

    short_int = short_interval_angular(rls_cells)
    for si in short_int:
        uniformity = "CLUSTERED" if si["R"] > 0.1 else ("weak" if si["R"] > 0.05 else "UNIFORM")
        print(f"    x~{si['x_center']:>8.0f}  window=[{int(si['x_center']-si['window_size']/2)}, "
              f"{int(si['x_center']+si['window_size']/2)}]  "
              f"primes={si['n_primes']:>4d}  R={si['R']:.4f}  "
              f"angular_std={si['angular_std']:.1f} deg  [{uniformity}]")

    print()

    # ═══════════════════════════════════════════════════════════════
    # PART G: 3D RLS STRUCTURE WITH TIME
    # ═══════════════════════════════════════════════════════════════
    print("PART G: 3D RLS Structure — Time Dimension Analysis")
    print("-" * 70)

    # Use a subset for 3D analysis (visualization + computation)
    N_3D = 100_000
    print(f"  Building 3D RLS ({N_3D:,} cells, time_mode='layer')...")
    t0 = time.time()
    cells_3d = build_3d_rls(N_3D, time_mode="layer")
    t1 = time.time()
    print(f"  3D grid built in {t1-t0:.1f}s")

    n_primes_3d = sum(1 for c in cells_3d if c["is_prime"])
    print(f"  Primes: {n_primes_3d}/{len(cells_3d)} "
          f"({100*n_primes_3d/len(cells_3d):.2f}%)")
    print()

    # Projection analysis: 2D vs 3D
    print("  2D vs 3D Projection Analysis:")
    print("  (Does adding the z-dimension reveal structure invisible in 2D?)")
    print()

    # 2D-only angular correlation (prime density)
    sector_stats_2d = angular_sector_analysis(cells_3d, n_sectors=36)
    pd_2d = [s["prime_density"] for s in sector_stats_2d]

    # 3D voxel analysis
    voxel_data, z_min, z_max = projection_analysis(cells_3d, 36, 10)

    # Z-band prime density
    n_z_bands = 10
    z_band_width = (z_max - z_min) / n_z_bands if z_max > z_min else 1
    z_bands = defaultdict(lambda: {"total": 0, "primes": 0})
    for c in cells_3d:
        z_idx = int((c["z"] - z_min) / z_band_width) if z_band_width > 0 else 0
        z_idx = min(z_idx, n_z_bands - 1)
        z_bands[z_idx]["total"] += 1
        if c["is_prime"]:
            z_bands[z_idx]["primes"] += 1

    print(f"  {'Z-band':>8} {'Z_range':>15} {'N_cells':>8} {'N_primes':>9} {'PD%':>7} {'Primes/cell':>12}")
    print("  " + "-" * 65)
    for z_idx in range(n_z_bands):
        band = z_bands[z_idx]
        pd = band["primes"] / band["total"] if band["total"] > 0 else 0
        z_lo = z_min + z_idx * z_band_width
        z_hi = z_lo + z_band_width
        print(f"  {z_idx:>8d} [{z_lo:>6.0f},{z_hi:>6.0f}) {band['total']:>8d} "
              f"{band['primes']:>9d} {pd*100:>6.2f}% {pd:>11.6f}")

    # 3D interaction: angular correlation varies with z?
    print()
    print("  Angular correlation within each z-band:")
    for z_idx in range(n_z_bands):
        z_lo = z_min + z_idx * z_band_width
        z_hi = z_lo + z_band_width
        band_cells = [c for c in cells_3d if z_lo <= c["z"] < z_hi]
        if len(band_cells) < 100:
            continue
        band_sectors = angular_sector_analysis(band_cells, n_sectors=36)
        if len(band_sectors) < 10:
            continue
        pd_band = [s["prime_density"] for s in band_sectors]
        # Mean angle autocorrelation within this z-band
        # Compute pairwise differences
        pd_mean_b = sum(pd_band) / len(pd_band)
        pd_var_b = sum((p - pd_mean_b)**2 for p in pd_band) / len(pd_band)
        print(f"    Z-band {z_idx}: {len(band_cells):>6d} cells, "
              f"{len(band_sectors)} sectors, PD_var={pd_var_b:.6f}")

    # 3D "unfolding" test: does the 2D projection distort?
    print()
    print("  3D vs 2D Distortion Analysis:")
    # In 3D, each layer m is a circle of radius sqrt(m).
    # The 2D projection maps (i,j) -> (i,j) with angle = atan2(j,i).
    # The "distortion" is that layers with different m values are superimposed.
    # We measure: does the angular prime bias DEPEND on which layers are combined?

    # Split into inner (z < median) and outer (z >= median) halves
    z_median = z_min + (z_max - z_min) / 2
    inner = [c for c in cells_3d if c["z"] < z_median]
    outer = [c for c in cells_3d if c["z"] >= z_median]

    inner_sectors = angular_sector_analysis(inner, n_sectors=36)
    outer_sectors = angular_sector_analysis(outer, n_sectors=36)

    pd_inner = [s["prime_density"] for s in inner_sectors]
    pd_outer = [s["prime_density"] for s in outer_sectors]

    r_inner_outer, _ = pearson_r(pd_inner, pd_outer)
    print(f"    Inner vs Outer angular PD correlation: r = {r_inner_outer:+.4f}")
    print(f"    ({'CONSISTENT' if r_inner_outer > 0.5 else 'DIFFERING'} angular structure)")

    # "Forced shape" test: compare 2D projection variance with 3D voxel variance
    # If the 2D projection is "forced", the 3D structure should have MORE variance
    pd_2d_var = sum((p - sum(pd_2d)/len(pd_2d))**2 for p in pd_2d) / len(pd_2d)
    if voxel_data:
        pd_3d = [v["prime_density"] for v in voxel_data]
        pd_3d_var = sum((p - sum(pd_3d)/len(pd_3d))**2 for p in pd_3d) / len(pd_3d)
        print(f"    2D angular PD variance: {pd_2d_var:.6f}")
        print(f"    3D voxel PD variance:   {pd_3d_var:.6f}")
        print(f"    3D/2D variance ratio:   {pd_3d_var/max(pd_2d_var, 1e-10):.2f}x")
        print(f"    ({'3D REVEALS MORE STRUCTURE' if pd_3d_var > pd_2d_var else '2D captures the structure'})")

    print()

    # ═══════════════════════════════════════════════════════════════
    # PART H: GAUSSIAN INTEGER DEEP DIVE (p=1(4) vs p=3(4) in 3D)
    # ═══════════════════════════════════════════════════════════════
    print("PART H: Gaussian Integer Classification in 3D Context")
    print("-" * 70)

    p1_mod4 = []  # Primes p ≡ 1 (mod 4) — on RLS layers
    p3_mod4 = []  # Primes p ≡ 3 (mod 4) — NOT on RLS layers

    for c in rls_cells[:200000]:  # Use subset for speed
        if c["is_prime"]:
            if c["n"] % 4 == 1:
                p1_mod4.append(c)
            elif c["n"] % 4 == 3:
                p3_mod4.append(c)

    print(f"  p=1(4) primes (on RLS layers):     {len(p1_mod4)}")
    print(f"  p=3(4) primes (NOT on RLS layers):  {len(p3_mod4)}")

    # Angular distribution comparison
    for label, group in [("p=1(4)", p1_mod4), ("p=3(4)", p3_mod4)]:
        if not group:
            continue
        angles = [c["angle_deg"] for c in group]
        C = sum(math.cos(math.radians(a)) for a in angles) / len(angles)
        S = sum(math.sin(math.radians(a)) for a in angles) / len(angles)
        R = math.sqrt(C**2 + S**2)

        # Angular distribution by 36 sectors
        counts = [0] * 36
        for a in angles:
            s_idx = int(a / 10) % 36
            counts[s_idx] += 1

        chi_sq = sum((c - sum(counts)/36)**2 / (sum(counts)/36) for c in counts)

        print(f"  {label}: Rayleigh R={R:.4f}, chi-squared={chi_sq:.1f}, "
              f"mean_radius={sum(c['radius'] for c in group)/len(group):.1f}")

    # Cross-class angular correlation
    if p1_mod4 and p3_mod4:
        counts_1 = [0] * 36
        counts_3 = [0] * 36
        for c in p1_mod4:
            counts_1[int(c["angle_deg"] / 10) % 36] += 1
        for c in p3_mod4:
            counts_3[int(c["angle_deg"] / 10) % 36] += 1

        r_cross, _ = pearson_r(counts_1, counts_3)
        print(f"  Cross-class angular correlation (p1 vs p3): r = {r_cross:+.4f}")
        print(f"  ({'SAME angular structure' if r_cross > 0.5 else 'DIFFERENT angular structure'})")

    print()

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PHASE XIV — SUMMARY OF KEY FINDINGS")
    print("=" * 80)
    print()
    print(f"1. 1-DEGREE RESOLUTION:")
    print(f"   Prime density range: {pd_min:.4f} to {pd_max:.4f} "
          f"({pd_max/max(pd_min, 1e-10):.2f}x ratio)")
    print(f"   Circular autocorrelation peak: r={best_lag_r:+.4f} at lag={best_lag} deg")
    print(f"   90-deg symmetry: r={r_90:+.4f}")
    print()
    print(f"2. UBP CORRELATION AT 1-DEGREE:")
    for key in ["mean_angle", "anchor_dist", "rot_sign_changes", "nrci_gl", "hw"]:
        if key in corr_1deg:
            r = corr_1deg[key]["pearson_r"]
            rho = corr_1deg[key]["spearman_rho"]
            print(f"   {metric_names[key]:<30s}: r={r:+.4f} rho={rho:+.4f}")
    print()
    print(f"3. K-TUPLE SPATIAL STRUCTURE:")
    for name in ["twins", "cousins", "sexy", "triplets_1", "quadruplets"]:
        if name in k_tuples:
            print(f"   {name:<15s}: {len(k_tuples[name]):>6d} occurrences in 10^6 grid")
    print()
    print(f"4. HARDY-LITTLEWOOD:")
    for name, hl in hl_results.items():
        print(f"   {name:<15s}: C={hl['C_HL']:.4f}  "
              f"obs/exp={hl['ratio']:.4f}")
    print()
    print(f"5. 3D STRUCTURE:")
    print(f"   Inner vs Outer angular correlation: r={r_inner_outer:+.4f}")
    if 'pd_3d_var' in dir() and 'pd_2d_var' in dir():
        print(f"   3D/2D variance ratio: {pd_3d_var/max(pd_2d_var,1e-10):.2f}x")
    print()
    print(f"6. GAUSSIAN INTEGER SPLIT:")
    print(f"   p=1(4) count: {len(p1_mod4)}, p=3(4) count: {len(p3_mod4)}")
    if p1_mod4 and p3_mod4:
        print(f"   Cross-class angular r: {r_cross:+.4f}")

    # Save results as JSON for visualization script
    results = {
        "grid_info": {
            "max_n": MAX_N, "n_cells": len(rls_cells),
            "n_layers": n_layers, "n_primes": n_primes,
            "prime_fraction": n_primes / len(rls_cells),
        },
        "1deg_analysis": {
            "pd_mean": pd_mean, "pd_std": pd_std,
            "pd_max": pd_max, "pd_min": pd_min,
            "peak_autocorr_lag": best_lag,
            "peak_autocorr_r": best_lag_r,
            "symmetry_45": r_45, "symmetry_90": r_90, "symmetry_180": r_180,
            "consistency_10vs1": r_consistency,
        },
        "1deg_correlations": corr_1deg,
        "k_tuples": {name: len(tlist) for name, tlist in k_tuples.items()},
        "hardy_littlewood": hl_results,
        "3d_analysis": {
            "inner_outer_r": r_inner_outer,
        },
        "sector_stats_1deg": [
            {k: v for k, v in s.items() if k != "metrics"}
            for s in sector_stats_1deg
        ],
        "sector_stats_10deg": sector_stats_10deg,
    }

    # Save k-tuple angular distributions for visualization
    kt_angular = {}
    for name, tlist in k_tuples.items():
        if tlist:
            counts_36 = k_tuple_angular_distribution(tlist, 36)
            kt_angular[name] = counts_36
    results["k_tuple_angular_36"] = kt_angular

    # Save short interval results
    results["short_intervals"] = short_int

    with open("/home/z/my-project/scripts/phase14_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print(f"Results saved to phase14_results.json")

    # Save RLS grid data for visualization (sample for size)
    viz_data = []
    for c in rls_cells[::10]:  # Every 10th cell
        viz_data.append({
            "n": c["n"], "i": c["i"], "j": c["j"],
            "angle_deg": c["angle_deg"], "radius": c["radius"],
            "layer_idx": c["layer_idx"], "m": c["m"],
            "is_prime": c["is_prime"],
        })
    with open("/home/z/my-project/scripts/phase14_rls_grid.json", "w") as f:
        json.dump(viz_data, f)
    print(f"RLS grid sample saved to phase14_rls_grid.json ({len(viz_data)} points)")
    print()
    print("PHASE XIV COMPUTATION COMPLETE")


if __name__ == "__main__":
    main()