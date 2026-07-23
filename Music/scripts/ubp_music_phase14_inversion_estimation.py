"""
UBP Study — Phase XIV: Range-Dependent Inversion Map & Factor Size Estimation
==============================================================================
Phase XIII FOUND r=+0.7963 (log max_factor vs spectral centroid) — the rotation
frequency domain carries factor-magnitude information. BUT only on 5 Mersenne
composites.

Phase XII REVEALED a critical inversion: Phase XI's "composites have more friction"
was Mersenne-specific; the broad landscape shows the OPPOSITE (primes > composites).

NEW DIRECTIVES:
  1. RANGE-DEPENDENT INVERSION MAP
     - Where exactly does the signal flip between bands?
     - Break 10^3–10^4 into sub-bands, compute all key correlations per band
     - Identify "transition zones" where metrics change behavior
     - Map: which metrics are useful in which ranges?

  2. FACTOR SIZE ESTIMATION
     - Can we ESTIMATE unknown factor sizes from rotation spectra?
     - Generalize beyond Mersenne numbers to GENERAL composites
     - Build regression: spectral features → log(factor magnitude)
     - Test with held-out composites (train/test split)
     - Estimate: max factor, min factor, total factor count, log(product of factors)
"""

import sys, math, random, time
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import (
    GolayCodeEngine, LeechLatticeEngine, BarnesWallEngine,
    MonsterGroup, AdaptiveManifold, NoiseALU, PhysicsALU,
    GOLAY_ENGINE, LEECH_ENGINE
)

g = GOLAY_ENGINE
l_engine = LEECH_ENGINE
physalu = PhysicsALU()
manifold = AdaptiveManifold()

RESIDUES = [17, 31, 113, 127]

# ========================================================================
# CORE UTILITIES (from Phase XIII)
# ========================================================================

def mod_dist(a, b, m):
    return min((a - b) % m, (b - a) % m)

def residue_fingerprint_4d(n, modulus=144):
    r = n % modulus
    return [mod_dist(r, res, modulus) for res in RESIDUES]

def compute_ubp_metrics(n):
    n_val = abs(int(n))
    gray_raw = n_val ^ (n_val >> 1)
    v_raw = [(gray_raw >> i) & 1 for i in range(23, -1, -1)]
    hw_raw = sum(v_raw)
    sw_raw = g.syndrome_weight(v_raw)
    tax_raw = Fraction(hw_raw, 24)
    nrci_raw = float(Fraction(10, 1) / (Fraction(10, 1) + tax_raw))
    decoded, correctable, anchor_dist = g.decode(v_raw)
    v_snapped = g.encode(decoded)
    hw_snapped = sum(v_snapped)
    sw_snapped = g.syndrome_weight(v_snapped)
    tax_snapped = l_engine.calculate_symmetry_tax(v_snapped)
    nrci_snapped = float(Fraction(10, 1) / (Fraction(10, 1) + tax_snapped))
    gamma = abs(nrci_raw - nrci_snapped)
    neighbor_nrci_max = 0.0
    for offset in (-1, 1):
        neighbor_val = n_val + offset
        if neighbor_val < 1: continue
        gray_n = neighbor_val ^ (neighbor_val >> 1)
        v_n = [(gray_n >> i) & 1 for i in range(23, -1, -1)]
        dec_n, _, _ = g.decode(v_n)
        snap_n = g.encode(dec_n)
        tax_n = l_engine.calculate_symmetry_tax(snap_n)
        nrci_n = float(Fraction(10, 1) / (Fraction(10, 1) + tax_n))
        neighbor_nrci_max = max(neighbor_nrci_max, nrci_n)
    lock_pressure = max(0.0, neighbor_nrci_max - nrci_snapped)
    lattice_weights = [0, 8, 12, 16, 24, 32, 48, 64]
    nearest_w = min(lattice_weights, key=lambda w: abs(hw_snapped - w))
    lattice_names = ['Identity', 'Octad', 'Dodecad', 'Hexadecad', 'Extended', 'Deep', 'Maximal', 'Maximal']
    lattice_class = lattice_names[min(len(lattice_names)-1, lattice_weights.index(nearest_w))]
    return {
        "n": n_val, "nrci_raw": nrci_raw, "nrci_snapped": nrci_snapped,
        "gamma": gamma, "lock_pressure": lock_pressure,
        "hw_raw": hw_raw, "hw_snapped": hw_snapped,
        "sw_raw": sw_raw, "sw_snapped": sw_snapped,
        "anchor_dist": anchor_dist, "correctable": correctable,
        "lattice_class": lattice_class,
    }

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

def trial_factor(n):
    """Return sorted list of prime factors with multiplicity."""
    if n < 2: return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

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

# ========================================================================
# GENERALIZED ROTATION TRAJECTORY (for non-Mersenne composites)
# ========================================================================

def generalized_rotation_trace(n, max_iter=50, seed=4):
    """
    Run the Lucas-type recurrence s_{i+1} = s_i^2 - 2 (mod n)
    and track 4D residue fingerprint rotation.
    This generalizes LL to ANY odd number.
    """
    if n < 3 or n % 2 == 0:
        return None
    
    s = seed
    trace_4d = []
    for i in range(max_iter + 1):
        fp = residue_fingerprint_4d(s)
        trace_4d.append(fp)
        s = (s * s - 2) % n
        if s == 0 or s == n - 2:  # trajectory collapses
            # fill remaining with last known state
            for _ in range(max_iter - i):
                trace_4d.append(fp)
            break
    
    # Direction vectors
    directions = []
    for i in range(1, len(trace_4d)):
        d = [trace_4d[i][j] - trace_4d[i-1][j] for j in range(4)]
        directions.append(d)
    
    if not directions:
        return None
    
    # Rotation signs (cross product in d0-d1 plane)
    rotation_signs = []
    for i in range(1, len(directions)):
        cross = (directions[i][0] * directions[i-1][1] -
                directions[i][1] * directions[i-1][0])
        rotation_signs.append(1 if cross > 0 else (-1 if cross < 0 else 0))
    
    # Magnitudes and angles
    dir_magnitudes = [math.sqrt(sum(d*d for d in dir)) for dir in directions]
    
    angles = []
    for i in range(1, len(directions)):
        d1, d2 = directions[i-1], directions[i]
        dot = sum(a*b for a, b in zip(d1, d2))
        n1 = math.sqrt(sum(a*a for a in d1)) + 1e-10
        n2 = math.sqrt(sum(a*a for a in d2)) + 1e-10
        cos_angle = max(-1, min(1, dot / (n1 * n2)))
        angles.append(math.acos(cos_angle))
    
    sign_changes = sum(1 for i in range(1, len(rotation_signs))
                      if rotation_signs[i] != rotation_signs[i-1])
    
    # Unique 4D states (trajectory diversity)
    unique_states = len(set(tuple(fp) for fp in trace_4d))
    
    # 4D fingerprint std (spread of trajectory)
    fp_std = 0.0
    if len(trace_4d) > 1:
        means = [sum(fp)/4 for fp in trace_4d]
        mean_of_means = sum(means)/len(means)
        fp_std = math.sqrt(sum((m - mean_of_means)**2 for m in means)/len(means))
    
    return {
        "directions": directions,
        "rotation_signs": rotation_signs,
        "dir_magnitudes": dir_magnitudes,
        "angles": angles,
        "sign_changes": sign_changes,
        "trace_4d": trace_4d,
        "net_rotation": sum(rotation_signs),
        "mean_magnitude": sum(dir_magnitudes)/len(dir_magnitudes) if dir_magnitudes else 0,
        "magnitude_std": math.sqrt(sum((m - sum(dir_magnitudes)/max(1,len(dir_magnitudes)))**2 
                                       for m in dir_magnitudes)/max(1,len(dir_magnitudes))),
        "mean_angle": sum(angles)/len(angles) if angles else 0,
        "angle_std": math.sqrt(sum((a - sum(angles)/len(angles))**2 for a in angles)/len(angles)) if len(angles) > 1 else 0,
        "unique_states": unique_states,
        "fp_std": fp_std,
        "trajectory_length": len(trace_4d),
    }


def extract_spectral_features(trace_result):
    """Extract frequency-domain features from a rotation trace."""
    if trace_result is None or len(trace_result["dir_magnitudes"]) < 3:
        return None
    
    mags = trace_result["dir_magnitudes"]
    N = len(mags)
    
    # DFT
    freqs = []
    spectrum = []
    for k in range(N // 2 + 1):
        re = sum(mags[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(mags[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        mag = math.sqrt(re*re + im*im) / N
        freqs.append(k)
        spectrum.append(mag)
    
    total_energy = sum(s*s for s in spectrum) + 1e-10
    
    # Spectral centroid (center of mass of spectrum)
    centroid = sum(f * m for f, m in zip(freqs, spectrum)) / (sum(spectrum) + 1e-10)
    
    # Spectral bandwidth (spread around centroid)
    bandwidth = math.sqrt(sum(m * (f - centroid)**2 for f, m in zip(freqs, spectrum)) / (sum(spectrum) + 1e-10))
    
    # Low/high frequency energy split (at median frequency)
    mid = len(spectrum) // 2
    low_energy = sum(s*s for s in spectrum[:mid])
    high_energy = sum(s*s for s in spectrum[mid:])
    low_ratio = low_energy / total_energy
    high_ratio = high_energy / total_energy
    
    # Dominant frequency (peak of spectrum, excluding DC)
    if len(spectrum) > 1:
        dominant_freq = freqs[1 + spectrum[1:].index(max(spectrum[1:]))]
    else:
        dominant_freq = 0
    
    # Spectral flatness (geometric mean / arithmetic mean)
    log_sum = sum(math.log(s + 1e-15) for s in spectrum)
    geo_mean = math.exp(log_sum / len(spectrum))
    ari_mean = sum(spectrum) / len(spectrum)
    flatness = geo_mean / (ari_mean + 1e-10)
    
    # Spectral rolloff (frequency below which 85% of energy is concentrated)
    cumul = 0.0
    rolloff = freqs[-1]
    for i, s in enumerate(spectrum):
        cumul += s * s
        if cumul >= 0.85 * total_energy:
            rolloff = freqs[i]
            break
    
    # Also analyze the SIGN signal
    signs = trace_result["rotation_signs"]
    if len(signs) > 2:
        sign_signal = [1.0 if s > 0 else (-1.0 if s < 0 else 0.0) for s in signs]
        N_s = len(sign_signal)
        sf, ss = [], []
        for k in range(N_s // 2 + 1):
            re = sum(sign_signal[n] * math.cos(2 * math.pi * k * n / N_s) for n in range(N_s))
            im = sum(sign_signal[n] * math.sin(2 * math.pi * k * n / N_s) for n in range(N_s))
            mag_s = math.sqrt(re*re + im*im) / N_s
            sf.append(k)
            ss.append(mag_s)
        sign_centroid = sum(f * m for f, m in zip(sf, ss)) / (sum(ss) + 1e-10)
        sign_total = sum(s*s for s in ss) + 1e-10
        sign_mid = len(ss) // 2
        sign_low = sum(s*s for s in ss[:sign_mid]) / sign_total
    else:
        sign_centroid = 0
        sign_low = 0.5
    
    return {
        "spectral_centroid": centroid,
        "spectral_bandwidth": bandwidth,
        "low_freq_ratio": low_ratio,
        "high_freq_ratio": high_ratio,
        "dominant_freq": dominant_freq,
        "spectral_flatness": flatness,
        "spectral_rolloff": rolloff,
        "sign_centroid": sign_centroid,
        "sign_low_ratio": sign_low,
        # Time-domain features
        "sign_changes": trace_result["sign_changes"],
        "mean_magnitude": trace_result["mean_magnitude"],
        "magnitude_std": trace_result["magnitude_std"],
        "mean_angle": trace_result["mean_angle"],
        "angle_std": trace_result["angle_std"],
        "unique_states": trace_result["unique_states"],
        "fp_std": trace_result["fp_std"],
    }


# ========================================================================
# DIRECTIVE 1: RANGE-DEPENDENT INVERSION MAP
# ========================================================================

def run_range_inversion_map():
    print("=" * 80)
    print("DIRECTIVE 1: RANGE-DEPENDENT INVERSION MAP")
    print("=" * 80)
    print("  Phase XII found: NRCI signal INVERTS between Mersenne-specific and general")
    print("  Phase XI found: composites have MORE friction (Mersenne-only)")
    print("  Phase XII found: primes have MORE friction (general landscape)")
    print("  QUESTION: Where exactly does the transition happen? Which bands do what?")
    print()
    
    random.seed(42)
    N_MIN, N_MAX = 1000, 10000
    
    # Compute UBP metrics for ALL numbers in range
    print(f"  Computing UBP metrics for [{N_MIN}, {N_MAX})...")
    t0 = time.time()
    all_data = []
    for n in range(N_MIN, N_MAX):
        if not isinstance(n, int) or n < 4:
            continue
        m = compute_ubp_metrics(n)
        m["is_prime"] = miller_rabin(n)
        factors = trial_factor(n)
        m["n_factors"] = len(factors)
        m["max_factor"] = max(factors) if factors else n
        m["min_factor"] = min(factors) if factors else n
        all_data.append(m)
    elapsed = time.time() - t0
    print(f"  Computed {len(all_data)} profiles in {elapsed:.1f}s")
    
    primes = [m for m in all_data if m["is_prime"]]
    composites = [m for m in all_data if not m["is_prime"]]
    print(f"  Primes: {len(primes)}, Composites: {len(composites)}")
    
    # Define sub-bands
    band_width = 500
    bands = []
    for lo in range(N_MIN, N_MAX, band_width):
        hi = min(lo + band_width, N_MAX)
        bands.append((lo, hi))
    
    print(f"\n  Analyzing {len(bands)} bands of width {band_width}...")
    print()
    
    # For each band, compute key metric comparisons
    # Metrics to track per band
    metric_names = [
        "nrci_snapped", "nrci_raw", "gamma", "lock_pressure",
        "hw_snapped", "sw_snapped", "anchor_dist"
    ]
    
    print(f"  {'Band':>12s} | {'N_P':>4s} {'N_C':>4s} | ", end="")
    for mn in metric_names[:4]:
        print(f"{mn[:5]:>7s}_d ", end="")
    print(f"| {'r_nci':>6s} | {'r_gam':>6s} | {'r_sw':>6s} | {'r_ad':>6s}")
    print(f"  {'-'*12} | {'-'*4} {'-'*4} | ", end="")
    for _ in metric_names[:4]:
        print(f"{'-'*7} ", end="")
    print(f"| {'-'*6} | {'-'*6} | {'-'*6} | {'-'*6}")
    
    band_results = []
    for lo, hi in bands:
        band_data = [m for m in all_data if lo <= m["n"] < hi]
        b_primes = [m for m in band_data if m["is_prime"]]
        b_comps = [m for m in band_data if not m["is_prime"]]
        
        if len(b_primes) < 3 or len(b_comps) < 5:
            continue
        
        # Mean difference (prime - composite) for each metric
        deltas = {}
        for mn in metric_names:
            p_mean = sum(m[mn] for m in b_primes) / len(b_primes)
            c_mean = sum(m[mn] for m in b_comps) / len(b_comps)
            deltas[mn] = p_mean - c_mean
        
        # Correlation: metric vs is_prime within band
        labels = [1 if m["is_prime"] else 0 for m in band_data]
        r_nrci = pearson_r(labels, [m["nrci_snapped"] for m in band_data])
        r_gamma = pearson_r(labels, [m["gamma"] for m in band_data])
        r_sw = pearson_r(labels, [m["sw_snapped"] for m in band_data])
        r_ad = pearson_r(labels, [m["anchor_dist"] for m in band_data])
        
        band_results.append({
            "lo": lo, "hi": hi,
            "n_primes": len(b_primes), "n_comps": len(b_comps),
            "deltas": deltas,
            "r_nrci": r_nrci, "r_gamma": r_gamma, "r_sw": r_sw, "r_ad": r_ad,
        })
        
        print(f"  {lo:>5d}-{hi:<5d} | {len(b_primes):>4d} {len(b_comps):>4d} | ", end="")
        for mn in metric_names[:4]:
            print(f"{deltas[mn]:>+7.4f} ", end="")
        print(f"| {r_nrci:>+6.3f} | {r_gamma:>+6.3f} | {r_sw:>+6.3f} | {r_ad:>+6.3f}")
    
    # --- INVERSION DETECTION ---
    print(f"\n  --- INVERSION ZONE ANALYSIS ---")
    # Find where deltas change sign
    for mn in metric_names:
        sign_sequence = [(br["lo"], br["deltas"][mn]) for br in band_results]
        inversions = []
        for i in range(1, len(sign_sequence)):
            prev_sign = 1 if sign_sequence[i-1][1] > 0 else (-1 if sign_sequence[i-1][1] < 0 else 0)
            curr_sign = 1 if sign_sequence[i][1] > 0 else (-1 if sign_sequence[i][1] < 0 else 0)
            if prev_sign != 0 and curr_sign != 0 and prev_sign != curr_sign:
                inversions.append((sign_sequence[i-1][0], sign_sequence[i][0], mn))
        
        if inversions:
            for lo, hi, name in inversions:
                print(f"  {name:>15s}: INVERSION between {lo}-{hi}")
        else:
            # Check if consistently signed
            all_pos = all(d > 0 for _, d in sign_sequence)
            all_neg = all(d < 0 for _, d in sign_sequence)
            if all_pos:
                print(f"  {mn:>15s}: CONSISTENTLY positive (primes > composites) across all bands")
            elif all_neg:
                print(f"  {mn:>15s}: CONSISTENTLY negative (composites > primes) across all bands")
            else:
                print(f"  {mn:>15s}: No clean inversion; mixed behavior")
    
    # --- DYNAMIC RANGE ANALYSIS (rotation-based per band) ---
    print(f"\n  --- ROTATION-BAND ANALYSIS (subsample per band) ---")
    print(f"  Computing rotation traces for subsamples in each band...")
    
    # For each band, sample some numbers and compute rotation features
    band_rotation_data = []
    for lo, hi in bands[::2]:  # every other band for speed
        band_numbers = [m["n"] for m in all_data if lo <= m["n"] < hi]
        if len(band_numbers) < 10:
            continue
        
        # Sample 30 numbers: ~10 primes + ~20 composites
        band_primes_n = [n for n in band_numbers if miller_rabin(n)]
        band_comps_n = [n for n in band_numbers if not miller_rabin(n)]
        
        sample_p = random.sample(band_primes_n, min(10, len(band_primes_n)))
        sample_c = random.sample(band_comps_n, min(20, len(band_comps_n)))
        
        p_sign_changes = []
        c_sign_changes = []
        p_fp_stds = []
        c_fp_stds = []
        p_unique = []
        c_unique = []
        
        for n in sample_p:
            tr = generalized_rotation_trace(n, max_iter=30)
            if tr:
                p_sign_changes.append(tr["sign_changes"])
                p_fp_stds.append(tr["fp_std"])
                p_unique.append(tr["unique_states"])
        
        for n in sample_c:
            tr = generalized_rotation_trace(n, max_iter=30)
            if tr:
                c_sign_changes.append(tr["sign_changes"])
                c_fp_stds.append(tr["fp_std"])
                c_unique.append(tr["unique_states"])
        
        if not p_sign_changes or not c_sign_changes:
            continue
        
        band_rotation_data.append({
            "lo": lo, "hi": hi,
            "p_sc_mean": sum(p_sign_changes)/len(p_sign_changes),
            "c_sc_mean": sum(c_sign_changes)/len(c_sign_changes),
            "p_fpstd": sum(p_fp_stds)/len(p_fp_stds) if p_fp_stds else 0,
            "c_fpstd": sum(c_fp_stds)/len(c_fp_stds) if c_fp_stds else 0,
            "p_unique": sum(p_unique)/len(p_unique) if p_unique else 0,
            "c_unique": sum(c_unique)/len(c_unique) if c_unique else 0,
        })
    
    print(f"\n  {'Band':>12s} | {'P_SCM':>6s} | {'C_SCM':>6s} | {'Delta':>6s} | {'P_FPstd':>7s} | {'C_FPstd':>7s} | {'P_Uniq':>6s} | {'C_Uniq':>6s}")
    print(f"  {'-'*12} | {'-'*6} | {'-'*6} | {'-'*6} | {'-'*7} | {'-'*7} | {'-'*6} | {'-'*6}")
    
    for br in band_rotation_data:
        delta = br["p_sc_mean"] - br["c_sc_mean"]
        print(f"  {br['lo']:>5d}-{br['hi']:<5d} | {br['p_sc_mean']:>6.2f} | {br['c_sc_mean']:>6.2f} | {delta:>+6.2f} | "
              f"{br['p_fpstd']:>7.3f} | {br['c_fpstd']:>7.3f} | {br['p_unique']:>6.1f} | {br['c_unique']:>6.1f}")
    
    # Detect rotation inversions
    print(f"\n  --- ROTATION INVERSION ZONES ---")
    sc_deltas = [(br["lo"], br["p_sc_mean"] - br["c_sc_mean"]) for br in band_rotation_data]
    for i in range(1, len(sc_deltas)):
        prev_pos = sc_deltas[i-1][1] > 0
        curr_pos = sc_deltas[i][1] > 0
        if prev_pos != curr_pos:
            print(f"  Sign-change INVERSION: band {sc_deltas[i-1][0]}-{sc_deltas[i][0]}")
            print(f"    Before: {'P > C' if prev_pos else 'C > P'} (+{sc_deltas[i-1][1]:.2f})")
            print(f"    After:  {'P > C' if curr_pos else 'C > P'} ({sc_deltas[i][1]:+.2f})")
    
    return {
        "band_results": band_results,
        "band_rotation_data": band_rotation_data,
    }


# ========================================================================
# DIRECTIVE 2: FACTOR SIZE ESTIMATION
# ========================================================================

def run_factor_size_estimation():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 2: FACTOR SIZE ESTIMATION")
    print("=" * 80)
    print("  Phase XIII found r=+0.7963 (log max_factor vs spectral centroid)")
    print("  on only 5 Mersenne composites. NOW we test on GENERAL composites.")
    print("  Goal: Given an unknown composite, ESTIMATE the sizes of its factors")
    print("  from the rotation frequency spectrum alone.")
    print()
    
    random.seed(123)
    
    # --- GENERATE TEST COMPOSITES WITH KNOWN FACTORS ---
    print("  Generating test composites with known factorizations...")
    
    # Strategy 1: Semiprimes (product of exactly 2 primes) of various sizes
    small_primes = [p for p in range(3, 500) if miller_rabin(p)]
    
    semiprimes = []
    for _ in range(60):
        p1 = random.choice(small_primes)
        p2 = random.choice(small_primes)
        if p1 == p2:
            continue
        n = p1 * p2
        if 100 < n < 100000:
            semiprimes.append({"n": n, "factors": sorted([p1, p2])})
    
    # Strategy 2: 3-factor composites
    three_factor = []
    for _ in range(40):
        p1 = random.choice(small_primes[:50])
        p2 = random.choice(small_primes[:50])
        p3 = random.choice(small_primes[:50])
        if len(set([p1, p2, p3])) < 2:
            continue
        n = p1 * p2 * p3
        if 100 < n < 100000:
            three_factor.append({"n": n, "factors": sorted([p1, p2, p3])})
    
    # Strategy 3: Mersenne composites (known factors)
    mersenne_composites = {
        11: (2047, [23, 89]),
        23: (8388607, [47, 178481]),
        29: (536870911, [233, 1103, 2089]),
        37: (137438953471, [223, 616318177]),
        41: (2199023255551, [13367, 164511353]),
    }
    
    # Strategy 4: Powers of primes
    prime_powers = []
    for p in small_primes[:30]:
        for e in [2, 3, 4]:
            n = p ** e
            if 100 < n < 100000:
                prime_powers.append({"n": n, "factors": [p] * e})
    
    # Strategy 5: Random general composites from [100, 50000]
    general_comps = []
    for _ in range(60):
        n = random.randint(100, 50000)
        if n % 2 == 0 or miller_rabin(n):
            continue
        factors = trial_factor(n)
        if len(factors) >= 2:
            general_comps.append({"n": n, "factors": factors})
    
    # Combine all (except Mersenne which use different trajectory)
    all_test_composites = semiprimes + three_factor + prime_powers + general_comps
    # Remove duplicates
    seen = set()
    deduped = []
    for tc in all_test_composites:
        if tc["n"] not in seen:
            seen.add(tc["n"])
            deduped.append(tc)
    all_test_composites = deduped
    
    print(f"  Total test composites: {len(all_test_composites)}")
    print(f"    Semiprimes:          {len(semiprimes)}")
    print(f"    3-factor:            {len(three_factor)}")
    print(f"    Prime powers:        {len(prime_powers)}")
    print(f"    General:             {len(general_comps)}")
    print(f"    Mersenne (separate): {len(mersenne_composites)}")
    
    # --- COMPUTE ROTATION SPECTRA FOR ALL COMPOSITES ---
    print(f"\n  Computing rotation spectra (this may take a moment)...")
    t0 = time.time()
    
    composite_spectral = []
    for tc in all_test_composites:
        n = tc["n"]
        factors = tc["factors"]
        
        trace = generalized_rotation_trace(n, max_iter=40)
        if trace is None:
            continue
        
        spectral = extract_spectral_features(trace)
        if spectral is None:
            continue
        
        # Factor statistics
        unique_factors = sorted(set(factors))
        max_f = max(unique_factors)
        min_f = min(unique_factors)
        n_unique = len(unique_factors)
        n_total = len(factors)
        log_max = math.log10(max_f)
        log_min = math.log10(min_f)
        log_range = log_max - log_min
        log_n = math.log10(n)
        
        # Factor size ratio (max/min)
        factor_ratio = max_f / min_f
        
        composite_spectral.append({
            "n": n,
            "factors": factors,
            "unique_factors": unique_factors,
            "n_unique": n_unique,
            "n_total": n_total,
            "max_factor": max_f,
            "min_factor": min_f,
            "log_max": log_max,
            "log_min": log_min,
            "log_range": log_range,
            "log_n": log_n,
            "factor_ratio": factor_ratio,
            **spectral,
        })
    
    elapsed = time.time() - t0
    print(f"  Computed {len(composite_spectral)} spectral profiles in {elapsed:.1f}s")
    
    # --- ALSO COMPUTE FOR PRIMES (baseline) ---
    print(f"  Computing prime baselines...")
    test_primes = [p for p in range(100, 10000) if miller_rabin(p)]
    prime_sample = random.sample(test_primes, min(50, len(test_primes)))
    
    prime_spectral = []
    for p in prime_sample:
        trace = generalized_rotation_trace(p, max_iter=40)
        if trace is None:
            continue
        spectral = extract_spectral_features(trace)
        if spectral is None:
            continue
        prime_spectral.append({"n": p, **spectral})
    
    print(f"  Prime baselines: {len(prime_spectral)}")
    
    # --- CORRELATION MATRIX: SPECTRAL FEATURES vs FACTOR PROPERTIES ---
    print(f"\n  --- SPECTRAL-FACTOR CORRELATION MATRIX ({len(composite_spectral)} composites) ---")
    
    factor_props = ["log_max", "log_min", "log_range", "n_unique", "n_total", 
                    "factor_ratio", "log_n"]
    spectral_feats = ["spectral_centroid", "spectral_bandwidth", "low_freq_ratio",
                      "high_freq_ratio", "dominant_freq", "spectral_flatness",
                      "spectral_rolloff", "sign_centroid", "sign_low_ratio",
                      "sign_changes", "mean_magnitude", "magnitude_std",
                      "mean_angle", "angle_std", "unique_states", "fp_std"]
    
    # Header
    print(f"  {'Factor\\Spect':>15s} | ", end="")
    for sf in spectral_feats:
        print(f"{sf[:6]:>7s} ", end="")
    print()
    print(f"  {'-'*15} | ", end="")
    for _ in spectral_feats:
        print(f"{'-'*7} ", end="")
    print()
    
    # Compute all correlations
    corr_matrix = {}
    for fp in factor_props:
        fp_vals = [c[fp] for c in composite_spectral]
        row = {}
        print(f"  {fp:>15s} | ", end="")
        for sf in spectral_feats:
            sf_vals = [c[sf] for c in composite_spectral]
            r = pearson_r(fp_vals, sf_vals)
            row[sf] = r
            marker = " ***" if abs(r) > 0.4 else (" **" if abs(r) > 0.3 else (" *" if abs(r) > 0.2 else ""))
            print(f"{r:>+7.3f}{marker} ", end="")
        print()
        corr_matrix[fp] = row
    
    # --- TOP CORRELATIONS ---
    print(f"\n  --- TOP 15 CORRELATIONS (by |r|) ---")
    all_corrs = []
    for fp, row in corr_matrix.items():
        for sf, r in row.items():
            all_corrs.append((fp, sf, r))
    all_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    for fp, sf, r in all_corrs[:15]:
        direction = "LARGER → MORE" if r > 0 else "LARGER → LESS"
        print(f"  {fp:>15s} vs {sf:>20s}: r={r:+.4f}  ({direction})")
    
    # --- FACTOR SIZE ESTIMATION: REGRESSION ---
    print(f"\n  --- FACTOR SIZE ESTIMATION (Train/Test Split) ---")
    
    # Use the top spectral features as predictors
    top_features = [sf for _, sf, _ in all_corrs[:8]]
    # Remove duplicates
    seen_feat = set()
    unique_top = []
    for f in top_features:
        if f not in seen_feat:
            seen_feat.add(f)
            unique_top.append(f)
    top_features = unique_top[:5]  # Use top 5 unique features
    
    print(f"  Predictor features: {top_features}")
    
    # Target: log(max_factor)
    # Train/test split (70/30)
    random.shuffle(composite_spectral)
    split = int(0.7 * len(composite_spectral))
    train = composite_spectral[:split]
    test = composite_spectral[split:]
    
    print(f"  Training set: {len(train)}, Test set: {len(test)}")
    
    # Simple linear regression (manual, no numpy needed)
    def linear_regression(xs_list, ys):
        """Multiple linear regression via normal equations."""
        n = len(ys)
        if n < len(xs_list) + 1:
            return None
        # Build X matrix (with intercept)
        k = len(xs_list)
        # Compute X^T X and X^T y
        XtX = [[0.0]*(k+1) for _ in range(k+1)]
        Xty = [0.0]*(k+1)
        
        for i in range(n):
            xi = [1.0] + [xs_list[j][i] for j in range(k)]
            yi = ys[i]
            for a in range(k+1):
                Xty[a] += xi[a] * yi
                for b in range(k+1):
                    XtX[a][b] += xi[a] * xi[b]
        
        # Gaussian elimination
        M = [row[:] for row in XtX]
        rhs = Xty[:]
        for col in range(k+1):
            max_row = col
            for row in range(col+1, k+1):
                if abs(M[row][col]) > abs(M[max_row][col]):
                    max_row = row
            M[col], M[max_row] = M[max_row], M[col]
            rhs[col], rhs[max_row] = rhs[max_row], rhs[col]
            if abs(M[col][col]) < 1e-12:
                return None
            for row in range(col+1, k+1):
                factor = M[row][col] / M[col][col]
                for j in range(col, k+1):
                    M[row][j] -= factor * M[col][j]
                rhs[row] -= factor * rhs[col]
        
        # Back substitution
        coeffs = [0.0] * (k+1)
        for i in range(k, -1, -1):
            coeffs[i] = rhs[i]
            for j in range(i+1, k+1):
                coeffs[i] -= M[i][j] * coeffs[j]
            coeffs[i] /= M[i][i]
        
        return coeffs
    
    def predict(coeffs, x_vals):
        return coeffs[0] + sum(c * x for c, x in zip(coeffs[1:], x_vals))
    
    # Train models for different targets
    targets = {
        "log_max_factor": "log_max",
        "log_min_factor": "log_min",
        "n_unique_factors": "n_unique",
        "log_factor_range": "log_range",
    }
    
    estimation_results = {}
    
    for target_name, target_key in targets.items():
        train_y = [c[target_key] for c in train]
        train_xs = [[c[f] for f in top_features] for c in train]
        
        coeffs = linear_regression(train_xs, train_y)
        if coeffs is None:
            print(f"\n  {target_name}: Regression failed (singular matrix)")
            continue
        
        # Training fit
        train_pred = [predict(coeffs, x) for x in train_xs]
        r_train = pearson_r(train_y, train_pred)
        train_rmse = math.sqrt(sum((y - yp)**2 for y, yp in zip(train_y, train_pred))/len(train_y))
        
        # Test prediction
        test_y = [c[target_key] for c in test]
        test_xs = [[c[f] for f in top_features] for c in test]
        test_pred = [predict(coeffs, x) for x in test_xs]
        r_test = pearson_r(test_y, test_pred)
        test_rmse = math.sqrt(sum((y - yp)**2 for y, yp in zip(test_y, test_pred))/len(test_y))
        
        # Spearman
        rho_test = spearman_rho(test_y, test_pred)
        
        # Mean absolute error
        mae = sum(abs(y - yp) for y, yp in zip(test_y, test_pred))/len(test_y)
        
        estimation_results[target_name] = {
            "r_train": r_train, "r_test": r_test, "rho_test": rho_test,
            "rmse_train": train_rmse, "rmse_test": test_rmse, "mae_test": mae,
            "coeffs": coeffs,
        }
        
        print(f"\n  --- {target_name} (using {top_features}) ---")
        print(f"  Coefficients: intercept={coeffs[0]:.4f}", end="")
        for i, f in enumerate(top_features):
            print(f", {f[:6]}={coeffs[i+1]:+.4f}", end="")
        print()
        print(f"  Training:  r={r_train:+.4f}, RMSE={train_rmse:.4f}")
        print(f"  Test:      r={r_test:+.4f}, rho={rho_test:+.4f}, RMSE={test_rmse:.4f}, MAE={mae:.4f}")
        
        if target_name == "log_max_factor":
            print(f"  Interpretation: MAE of {mae:.3f} in log10 space means")
            print(f"    we estimate the max factor within ~10^{mae:.1f}x of its true value")
    
    # --- BLIND TEST: Can we estimate factor sizes on Mersenne composites? ---
    print(f"\n  --- BLIND TEST: Mersenne Composite Factor Estimation ---")
    print(f"  Training on general composites, testing on Mersenne composites")
    
    # Retrain on ALL general composites
    all_train_y = [c["log_max"] for c in composite_spectral]
    all_train_xs = [[c[f] for f in top_features] for c in composite_spectral]
    
    coeffs_all = linear_regression(all_train_xs, all_train_y)
    if coeffs_all:
        print(f"  Full-model coefficients: intercept={coeffs_all[0]:.4f}", end="")
        for i, f in enumerate(top_features):
            print(f", {f[:6]}={coeffs_all[i+1]:+.4f}", end="")
        print()
        
        print(f"\n  {'Case':>8s} | {'True logF':>9s} | {'Pred logF':>9s} | {'Error':>7s} | {'True Factor':>12s} | {'Est Factor':>12s}")
        print(f"  {'-'*8} | {'-'*9} | {'-'*9} | {'-'*7} | {'-'*12} | {'-'*12}")
        
        for p, (Mp, factors) in mersenne_composites.items():
            trace = generalized_rotation_trace(Mp, max_iter=min(p-2, 40))
            if trace is None:
                continue
            spectral = extract_spectral_features(trace)
            if spectral is None:
                continue
            
            x_vals = [spectral[f] for f in top_features]
            pred_log = predict(coeffs_all, x_vals)
            true_max = max(factors)
            true_log = math.log10(true_max)
            est_factor = 10 ** pred_log
            error = pred_log - true_log
            
            print(f"  M_{p:>5d} | {true_log:>9.4f} | {pred_log:>9.4f} | {error:>+7.3f} | {true_max:>12d} | {est_factor:>12.1f}")
    
    # --- PRIME vs COMPOSITE SEPARATION USING SPECTRAL FEATURES ---
    print(f"\n  --- PRIME-COMPOSITE SEPARATION VIA SPECTRAL FEATURES ---")
    # Can spectral features ALONE distinguish primes from composites?
    
    all_spectral_data = []
    for c in composite_spectral:
        all_spectral_data.append({**{f: c[f] for f in top_features}, "label": 1})
    for p in prime_spectral:
        all_spectral_data.append({**{f: p[f] for f in top_features}, "label": 0})
    
    if len(all_spectral_data) > 20:
        labels = [d["label"] for d in all_spectral_data]
        print(f"  Individual feature correlations with primality:")
        for f in top_features:
            vals = [d[f] for d in all_spectral_data]
            r = pearson_r(labels, vals)
            print(f"    {f:>20s}: r={r:+.4f}")
        
        # Combined: train a logistic-like classifier using linear regression on labels
        train_y_binary = [d["label"] for d in all_spectral_data[:int(0.7*len(all_spectral_data))]]
        test_y_binary = [d["label"] for d in all_spectral_data[int(0.7*len(all_spectral_data)):]]
        
        train_xs_binary = [[d[f] for f in top_features] for d in all_spectral_data[:int(0.7*len(all_spectral_data))]]
        test_xs_binary = [[d[f] for f in top_features] for d in all_spectral_data[int(0.7*len(all_spectral_data)):]]
        
        bin_coeffs = linear_regression(train_xs_binary, train_y_binary)
        if bin_coeffs:
            train_pred_bin = [predict(bin_coeffs, x) for x in train_xs_binary]
            test_pred_bin = [predict(bin_coeffs, x) for x in test_xs_binary]
            
            # Threshold at 0.5
            train_correct = sum(1 for y, p in zip(train_y_binary, train_pred_bin)
                              if (p >= 0.5) == (y >= 0.5))
            test_correct = sum(1 for y, p in zip(test_y_binary, test_pred_bin)
                             if (p >= 0.5) == (y >= 0.5))
            
            train_acc = train_correct / len(train_y_binary)
            test_acc = test_correct / len(test_y_binary)
            
            # Also compute AUC-like measure: correlation of predictions with labels
            r_test_bin = pearson_r(test_y_binary, test_pred_bin)
            
            print(f"\n  Combined spectral classifier:")
            print(f"    Training accuracy: {train_acc:.1%}")
            print(f"    Test accuracy:     {test_acc:.1%} (random = {max(len(test_y_binary) - sum(test_y_binary), sum(test_y_binary))/len(test_y_binary):.1%})")
            print(f"    Test r(label, pred): {r_test_bin:+.4f}")
    
    return {
        "composite_spectral": composite_spectral,
        "estimation_results": estimation_results,
        "top_features": top_features,
    }


# ========================================================================
# GRAND SYNTHESIS
# ========================================================================

def main():
    print("+" + "=" * 78 + "+")
    print("|  UBP STUDY - PHASE XIV: RANGE INVERSION MAP & FACTOR ESTIMATION    |")
    print("|  Can we map WHERE signals flip? Can we ESTIMATE unknown factors?    |")
    print("+" + "=" * 78 + "+")
    print()
    
    t0 = time.time()
    
    # Directive 1: Range-Dependent Inversion Map
    d1 = run_range_inversion_map()
    
    # Directive 2: Factor Size Estimation
    d2 = run_factor_size_estimation()
    
    t1 = time.time()
    
    print(f"\n{'=' * 80}")
    print("PHASE XIV: GRAND SYNTHESIS")
    print(f"{'=' * 80}")
    print(f"  Execution time: {t1-t0:.1f}s")
    print()
    
    print("  DIRECTIVE 1 — RANGE-DEPENDENT INVERSION MAP:")
    print("  (See band-by-band tables above)")
    print("  Key question: Where does the Phase XI→XII inversion occur?")
    print("  Key question: Which metrics are stable across which ranges?")
    print()
    
    print("  DIRECTIVE 2 — FACTOR SIZE ESTIMATION:")
    if "estimation_results" in d2:
        for target, res in d2["estimation_results"].items():
            print(f"    {target}: test r={res['r_test']:+.4f}, test rho={res['rho_test']:+.4f}")
    print()
    
    print("  ═══════════════════════════════════════════════════════════════════")
    print("  THE CRITICAL QUESTIONS:")
    print("  1. Does the range-dependent inversion reveal geometric structure?")
    print("  2. Can rotation frequency spectra PREDICT unknown factor sizes?")
    print("  3. Is the r=+0.7963 finding generalizable beyond Mersenne numbers?")
    print("  ═══════════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()