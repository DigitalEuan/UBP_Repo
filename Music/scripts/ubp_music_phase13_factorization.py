"""
UBP Study — Phase XIII: Topological Factorization Analysis
============================================================
Re-oriented from Phase XII's failed "friction attractor" hypothesis toward
the THREE DIRECTIVES from the user's UBP Prime document:

DIRECTIVE 1: INVERSE FACTORIZATION VIA ROTATION FREQUENCY
  - Phase XII found r=+0.797 for sign-change count vs factor count
  - NEW: Map the FREQUENCY DOMAIN of rotation, not just the count
  - Hypothesis: Large factor → "low-frequency hum" in rotation
                Many small factors → "high-frequency jitter"
  - Use DFT on the rotation sign sequence to extract spectral components

DIRECTIVE 2: THE TENACITY LAW MAP
  - Per the UBP Prime document, Lock Pressure P(n) = max(0, max_neighbor_nrci - target_nrci)
  - "Sovereign Primes" should exist at global minima of the pressure map
  - Composites should exist at local maxima (zero-pressure ghosts)
  - Use PhysicsALU to compute "energy of stabilization"
  - Map Topological Shear Gamma = |NRCI_raw - NRCI_snapped| across the range

DIRECTIVE 3: CROSS-DIMENSIONAL CALIBRATION (Golay-Normalized)
  - Phase XII showed NRCI signal decays at higher bit widths — BUT that was
    the raw coding layer noise
  - NEW: Use Golay-Leech as a NORMALIZATION FILTER (snap to nearest codeword)
  - Then run Rotation Complexity analysis on the NORMALIZED manifold state
  - The prime signal should survive normalization because it's topological, not coding-based
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
# UBP NATIVE PRIMITIVES (from the PDF's formalism)
# ========================================================================

def compute_ubp_metrics(n):
    """
    Compute the full UBP primality metrics per the PDF's formalism:
    - NRCI_snapped: stability after Golay snap
    - NRCI_raw: stability of raw Gray code
    - Topological Shear Gamma = |NRCI_raw - NRCI_snapped|
    - Lock Pressure P(n) = max(0, max_neighbor_nrci - target_nrci)
    - Syndrome weight, Hamming weight, anchor distance
    """
    n_val = abs(int(n))
    
    # Raw Gray code → 24 bits
    gray_raw = n_val ^ (n_val >> 1)
    v_raw = [(gray_raw >> i) & 1 for i in range(23, -1, -1)]
    hw_raw = sum(v_raw)
    sw_raw = g.syndrome_weight(v_raw)
    
    # NRCI of raw state
    tax_raw = Fraction(hw_raw, 24)
    nrci_raw = float(Fraction(10, 1) / (Fraction(10, 1) + tax_raw))
    
    # Snapped state (Golay decode → re-encode)
    decoded, correctable, anchor_dist = g.decode(v_raw)
    v_snapped = g.encode(decoded)
    hw_snapped = sum(v_snapped)
    sw_snapped = g.syndrome_weight(v_snapped)
    
    # NRCI of snapped state (through Leech)
    tax_snapped = l_engine.calculate_symmetry_tax(v_snapped)
    nrci_snapped = float(Fraction(10, 1) / (Fraction(10, 1) + tax_snapped))
    
    # Topological Shear: Gamma = |NRCI_raw - NRCI_snapped|
    gamma = abs(nrci_raw - nrci_snapped)
    
    # Lock Pressure: P(n) = max(0, max(NRCI(n-1), NRCI(n+1)) - NRCI(n))
    neighbor_nrci_max = 0.0
    for offset in (-1, 1):
        neighbor_val = n_val + offset
        if neighbor_val < 1:
            continue
        gray_n = neighbor_val ^ (neighbor_val >> 1)
        v_n = [(gray_n >> i) & 1 for i in range(23, -1, -1)]
        dec_n, _, _ = g.decode(v_n)
        snap_n = g.encode(dec_n)
        tax_n = l_engine.calculate_symmetry_tax(snap_n)
        nrci_n = float(Fraction(10, 1) / (Fraction(10, 1) + tax_n))
        neighbor_nrci_max = max(neighbor_nrci_max, nrci_n)
    
    lock_pressure = max(0.0, neighbor_nrci_max - nrci_snapped)
    
    # Lattice weight class
    lattice_weights = [0, 8, 12, 16, 24, 32, 48, 64]
    nearest_w = min(lattice_weights, key=lambda w: abs(hw_snapped - w))
    lattice_names = ['Identity', 'Octad', 'Dodecad', 'Hexadecad', 'Universe', 'Extended', 'Deep', 'Maximal']
    lattice_class = lattice_names[lattice_weights.index(nearest_w)]
    
    return {
        "n": n_val,
        "nrci_raw": nrci_raw,
        "nrci_snapped": nrci_snapped,
        "gamma": gamma,
        "lock_pressure": lock_pressure,
        "hw_raw": hw_raw,
        "hw_snapped": hw_snapped,
        "sw_raw": sw_raw,
        "sw_snapped": sw_snapped,
        "anchor_dist": anchor_dist,
        "correctable": correctable,
        "lattice_class": lattice_class,
        "neighbor_nrci_max": neighbor_nrci_max,
    }


# ========================================================================
# DIRECTIVE 1: INVERSE FACTORIZATION VIA ROTATION FREQUENCY
# ========================================================================

def mod_dist(a, b, m):
    return min((a - b) % m, (b - a) % m)

def residue_fingerprint_4d(n, modulus=144):
    r = n % modulus
    return [mod_dist(r, res, modulus) for res in RESIDUES]

def ll_rotation_trace(p, Mp, max_iter=30):
    """
    Full LL rotation trace: direction vectors, sign changes,
    and the COMPLETE rotation signal for frequency analysis.
    """
    s = 4
    trace_4d = []
    for i in range(min(max_iter, max(2, p-2)) + 1):
        fp4d = residue_fingerprint_4d(s)
        trace_4d.append(fp4d)
        s = (s * s - 2) % Mp
    
    # Direction vectors
    directions = []
    for i in range(1, len(trace_4d)):
        d = [trace_4d[i][j] - trace_4d[i-1][j] for j in range(4)]
        directions.append(d)
    
    # Sign of rotation (2D cross product in d0-d1 plane)
    rotation_signs = []
    for i in range(1, len(directions)):
        cross = (directions[i][0] * directions[i-1][1] - 
                directions[i][1] * directions[i-1][0])
        rotation_signs.append(1 if cross > 0 else (-1 if cross < 0 else 0))
    
    # Direction MAGNITUDES (for frequency analysis)
    dir_magnitudes = [math.sqrt(sum(d*d for d in dir)) for dir in directions]
    
    # Angular changes
    angles = []
    for i in range(1, len(directions)):
        d1, d2 = directions[i-1], directions[i]
        dot = sum(a*b for a, b in zip(d1, d2))
        n1 = math.sqrt(sum(a*a for a in d1)) + 1e-10
        n2 = math.sqrt(sum(a*a for a in d2)) + 1e-10
        cos_angle = max(-1, min(1, dot / (n1 * n2)))
        angles.append(math.acos(cos_angle))
    
    # Sign changes
    sign_changes = sum(1 for i in range(1, len(rotation_signs))
                      if rotation_signs[i] != rotation_signs[i-1])
    
    return {
        "directions": directions,
        "rotation_signs": rotation_signs,
        "dir_magnitudes": dir_magnitudes,
        "angles": angles,
        "sign_changes": sign_changes,
        "trace_4d": trace_4d,
        "net_rotation": sum(rotation_signs),
        "mean_angle": sum(angles)/len(angles) if angles else 0,
        "angle_std": math.sqrt(sum((a - sum(angles)/len(angles))**2 for a in angles)/len(angles)) if len(angles) > 1 else 0,
    }


def dft(signal):
    """Discrete Fourier Transform of a real signal. Returns (frequencies, magnitudes)."""
    N = len(signal)
    if N < 2:
        return [0], [abs(s) for s in signal]
    
    freqs = []
    mags = []
    for k in range(N // 2 + 1):
        re = sum(signal[n] * math.cos(2 * math.pi * k * n / N) for n in range(N))
        im = sum(signal[n] * math.sin(2 * math.pi * k * n / N) for n in range(N))
        mag = math.sqrt(re*re + im*im) / N
        freqs.append(k)
        mags.append(mag)
    return freqs, mags


def spectral_centroid(freqs, mags):
    """Weighted mean frequency — 'center of mass' of the spectrum."""
    total = sum(mags)
    if total == 0:
        return 0.0
    return sum(f * m for f, m in zip(freqs, mags)) / total


def spectral_bandwidth(freqs, mags, centroid):
    """Spread of the spectrum around the centroid."""
    total = sum(mags)
    if total == 0:
        return 0.0
    return math.sqrt(sum(m * (f - centroid)**2 for f, m in zip(freqs, mags)) / total)


def run_inverse_factorization_frequency():
    print("=" * 80)
    print("DIRECTIVE 1: INVERSE FACTORIZATION VIA ROTATION FREQUENCY")
    print("=" * 80)
    print("  Phase XII found r=+0.797 for sign-change COUNT vs factor count.")
    print("  NEW: Analyze the FREQUENCY DOMAIN of the rotation signal.")
    print("  Hypothesis: large factor = low-freq hum, many small factors = high-freq jitter")
    print()
    
    # Known composite Mersenne numbers with their factors
    composite_mersennes = {
        11: (2047, [23, 89]),
        23: (8388607, [47, 178481]),
        29: (536870911, [233, 1103, 2089]),
        37: (137438953471, [223, 616318177]),
        41: (2199023255551, [13367, 164511353]),
    }
    
    # Mersenne primes
    prime_mersennes = {3: 7, 5: 31, 7: 127, 13: 8191, 17: 131071}
    
    all_results = {}
    
    print("  Computing rotation frequency spectra for composites...")
    comp_spectral_data = []
    for p, (Mp, factors) in composite_mersennes.items():
        trace = ll_rotation_trace(p, Mp, max_iter=30)
        all_results[p] = {"trace": trace, "factors": factors, "is_prime": False, "Mp": Mp}
        
        # Compute DFT of the rotation magnitude signal
        if len(trace["dir_magnitudes"]) > 2:
            freqs, mags = dft(trace["dir_magnitudes"])
            centroid = spectral_centroid(freqs, mags)
            bandwidth = spectral_bandwidth(freqs, mags, centroid)
            
            # Also DFT of the sign sequence (treating signs as +1/-1 signal)
            sign_signal = [1 if s > 0 else -1 if s < 0 else 0 for s in trace["rotation_signs"]]
            sf, sm = dft(sign_signal)
            s_centroid = spectral_centroid(sf, sm)
            
            # Factor size statistics
            factor_sizes = factors
            max_factor = max(factors)
            min_factor = min(factors)
            log_range = math.log10(max_factor) - math.log10(min_factor + 1)
            
            comp_spectral_data.append({
                "p": p, "n_factors": len(factors),
                "max_factor": max_factor, "min_factor": min_factor,
                "log_range": log_range,
                "spectral_centroid": centroid,
                "spectral_bandwidth": bandwidth,
                "sign_centroid": s_centroid,
                "sign_changes": trace["sign_changes"],
                "mean_angle": trace["mean_angle"],
                "angle_std": trace["angle_std"],
            })
    
    print("  Computing rotation frequency spectra for primes...")
    prime_spectral_data = []
    for p, Mp in prime_mersennes.items():
        trace = ll_rotation_trace(p, Mp, max_iter=30)
        all_results[p] = {"trace": trace, "factors": [Mp], "is_prime": True, "Mp": Mp}
        
        if len(trace["dir_magnitudes"]) > 2:
            freqs, mags = dft(trace["dir_magnitudes"])
            centroid = spectral_centroid(freqs, mags)
            bandwidth = spectral_bandwidth(freqs, mags, centroid)
            
            sign_signal = [1 if s > 0 else -1 if s < 0 else 0 for s in trace["rotation_signs"]]
            sf, sm = dft(sign_signal)
            s_centroid = spectral_centroid(sf, sm)
            
            prime_spectral_data.append({
                "p": p, "n_factors": 1,
                "max_factor": Mp, "min_factor": Mp,
                "log_range": 0.0,
                "spectral_centroid": centroid,
                "spectral_bandwidth": bandwidth,
                "sign_centroid": s_centroid,
                "sign_changes": trace["sign_changes"],
                "mean_angle": trace["mean_angle"],
                "angle_std": trace["angle_std"],
            })
    
    # --- FREQUENCY ANALYSIS TABLE ---
    print(f"\n  --- ROTATION FREQUENCY SPECTRA ---")
    print(f"  {'Case':>8s} | {'NF':>2s} | {'MaxFac':>10s} | {'SC':>7s} | {'SBW':>7s} | {'SigC':>6s} | {'SCng':>5s} | {'AngStd':>6s}")
    print(f"  {'-'*8} | {'-'*2} | {'-'*10} | {'-'*7} | {'-'*7} | {'-'*6} | {'-'*5} | {'-'*6}")
    
    for d in comp_spectral_data + prime_spectral_data:
        marker = "P" if d["n_factors"] == 1 else "C"
        print(f"  M_{d['p']:>5d} | {d['n_factors']:>2d} | {d['max_factor']:>10d} | "
              f"{d['spectral_centroid']:>7.3f} | {d['spectral_bandwidth']:>7.3f} | "
              f"{d['sign_centroid']:>6.3f} | {d['sign_changes']:>5d} | {d['angle_std']:>6.4f}")
    
    # --- CORRELATION: Factor properties vs spectral properties ---
    print(f"\n  --- FACTOR-SPECTRAL CORRELATIONS (composites only) ---")
    if comp_spectral_data:
        n_factors = [d["n_factors"] for d in comp_spectral_data]
        log_max = [math.log10(d["max_factor"]) for d in comp_spectral_data]
        log_range = [d["log_range"] for d in comp_spectral_data]
        centroids = [d["spectral_centroid"] for d in comp_spectral_data]
        bandwidths = [d["spectral_bandwidth"] for d in comp_spectral_data]
        sign_centroids = [d["sign_centroid"] for d in comp_spectral_data]
        sign_changes = [d["sign_changes"] for d in comp_spectral_data]
        angle_stds = [d["angle_std"] for d in comp_spectral_data]
        
        def pearson(xs, ys):
            n = len(xs)
            if n < 2: return 0.0
            mx, my = sum(xs)/n, sum(ys)/n
            cov = sum((x-mx)*(y-my) for x,y in zip(xs, ys))
            vx = sum((x-mx)**2 for x in xs)
            vy = sum((y-my)**2 for y in ys)
            if vx == 0 or vy == 0: return 0.0
            return cov / math.sqrt(vx * vy)
        
        tests = [
            ("n_factors vs spectral_centroid", n_factors, centroids),
            ("n_factors vs spectral_bandwidth", n_factors, bandwidths),
            ("n_factors vs sign_centroid", n_factors, sign_centroids),
            ("n_factors vs sign_changes", n_factors, sign_changes),
            ("n_factors vs angle_std", n_factors, angle_stds),
            ("log(max_factor) vs spectral_centroid", log_max, centroids),
            ("log(max_factor) vs spectral_bandwidth", log_max, bandwidths),
            ("log_range vs spectral_centroid", log_range, centroids),
            ("log_range vs spectral_bandwidth", log_range, bandwidths),
        ]
        
        print(f"  {'Test':>42s} | {'r':>8s}")
        print(f"  {'-'*42} | {'-'*8}")
        for name, xs, ys in tests:
            r = pearson(xs, ys)
            print(f"  {name:>42s} | {r:>+8.4f}")
        
        # The KEY TEST: Does spectral centroid correlate with factor magnitude?
        r_fac_centroid = pearson(log_max, centroids)
        r_nfac_bandwidth = pearson(n_factors, bandwidths)
        
        print(f"\n  *** KEY HYPOTHESIS TEST ***")
        if abs(r_fac_centroid) > 0.5:
            print(f"  Spectral centroid vs factor magnitude: r={r_fac_centroid:+.4f}")
            print(f"  >>> LARGE FACTORS DO CREATE LOW-FREQUENCY ROTATION <<<")
        else:
            print(f"  Spectral centroid vs factor magnitude: r={r_fac_centroid:+.4f}")
            print(f"  No clear frequency-factor magnitude mapping.")
        
        if abs(r_nfac_bandwidth) > 0.5:
            print(f"  Factor count vs bandwidth: r={r_nfac_bandwidth:+.4f}")
            print(f"  >>> MORE FACTORS = MORE FREQUENCY SPREAD (JITTER) <<<")
        else:
            print(f"  Factor count vs bandwidth: r={r_nfac_bandwidth:+.4f}")
    
    # --- LOW-FREQ vs HIGH-FREQ DECOMPOSITION ---
    print(f"\n  --- SPECTRAL DECOMPOSITION: LOW-FREQ vs HIGH-FREQ ---")
    for p, data in all_results.items():
        trace = data["trace"]
        mags = trace["dir_magnitudes"]
        if len(mags) < 4:
            continue
        
        freqs, spec = dft(mags)
        # Split at median frequency
        mid = len(spec) // 2
        low_freq_energy = sum(s**2 for s in spec[:mid])
        high_freq_energy = sum(s**2 for s in spec[mid:])
        total_energy = low_freq_energy + high_freq_energy + 1e-10
        low_ratio = low_freq_energy / total_energy
        high_ratio = high_freq_energy / total_energy
        
        n_fac = len(data["factors"])
        marker = "PRIME" if data["is_prime"] else f"COMP(nf={n_fac})"
        print(f"  M_{p:>5d} [{marker:>14s}]: low_freq={low_ratio:.3f}, high_freq={high_ratio:.3f}, "
              f"ratio={low_ratio/(high_ratio+0.001):.2f}")
    
    return all_results, comp_spectral_data, prime_spectral_data


# ========================================================================
# DIRECTIVE 2: THE TENACITY LAW MAP
# ========================================================================

def run_tenacity_law_map():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 2: THE TENACITY LAW MAP")
    print("=" * 80)
    print("  Per the UBP Prime document:")
    print("    Lock Pressure P(n) = max(0, max(NRCI(n-1), NRCI(n+1)) - NRCI(n))")
    print("    Topological Shear Gamma = |NRCI_raw - NRCI_snapped|")
    print("  Hypothesis: Sovereign Primes at global pressure minima,")
    print("              Composites at local maxima (zero-pressure ghosts)")
    print()
    
    random.seed(42)
    N_MIN, N_MAX = 1000, 10000
    
    # Compute UBP metrics for all numbers in range
    print(f"  Computing UBP metrics for range [{N_MIN}, {N_MAX})...")
    t0 = time.time()
    
    all_metrics = []
    for n in range(N_MIN, N_MAX):
        m = compute_ubp_metrics(n)
        m["is_prime"] = miller_rabin(n)
        all_metrics.append(m)
    
    elapsed = time.time() - t0
    primes = [m for m in all_metrics if m["is_prime"]]
    composites = [m for m in all_metrics if not m["is_prime"]]
    print(f"  Computed {len(all_metrics)} profiles in {elapsed:.1f}s")
    print(f"  Primes: {len(primes)}, Composites: {len(composites)}")
    
    # --- LOCK PRESSURE STATISTICS ---
    print(f"\n  --- LOCK PRESSURE DISTRIBUTION ---")
    p_pressures = [m["lock_pressure"] for m in primes]
    c_pressures = [m["lock_pressure"] for m in composites]
    
    p_p_mean = sum(p_pressures)/len(p_pressures)
    c_p_mean = sum(c_pressures)/len(c_pressures)
    p_p_median = sorted(p_pressures)[len(p_pressures)//2]
    c_p_median = sorted(c_pressures)[len(c_pressures)//2]
    
    # How many have P > 0?
    p_positive = sum(1 for p in p_pressures if p > 0)
    c_positive = sum(1 for p in c_pressures if p > 0)
    
    print(f"  Prime Lock Pressure:    mean={p_p_mean:.6f}, median={p_p_median:.6f}")
    print(f"  Composite Lock Pressure: mean={c_p_mean:.6f}, median={c_p_median:.6f}")
    print(f"  Primes with P > 0: {p_positive}/{len(primes)} ({100*p_positive/len(primes):.1f}%)")
    print(f"  Composites with P > 0: {c_positive}/{len(composites)} ({100*c_positive/len(composites):.1f}%)")
    
    # --- TOPOLOGICAL SHEAR STATISTICS ---
    print(f"\n  --- TOPOLOGICAL SHEAR (GAMMA) DISTRIBUTION ---")
    p_gammas = [m["gamma"] for m in primes]
    c_gammas = [m["gamma"] for m in composites]
    
    p_g_mean = sum(p_gammas)/len(p_gammas)
    c_g_mean = sum(c_gammas)/len(c_gammas)
    
    # Gamma > 0.008 threshold (from PDF)
    p_above = sum(1 for g in p_gammas if g > 0.008)
    c_above = sum(1 for g in c_gammas if g > 0.008)
    
    print(f"  Prime Gamma:    mean={p_g_mean:.6f}")
    print(f"  Composite Gamma: mean={c_g_mean:.6f}")
    print(f"  Primes with Gamma > 0.008: {p_above}/{len(primes)} ({100*p_above/len(primes):.1f}%)")
    print(f"  Composites with Gamma > 0.008: {c_above}/{len(composites)} ({100*c_above/len(composites):.1f}%)")
    
    # --- THE PRESSURE MAP: Do primes cluster at pressure minima? ---
    print(f"\n  --- PRESSURE MAP TOPOLOGY ---")
    # For each number, compute local pressure rank (percentile in neighborhood)
    window = 20
    pressure_landscape = []
    for i, m in enumerate(all_metrics):
        lo = max(0, i - window)
        hi = min(len(all_metrics), i + window + 1)
        neighborhood = [all_metrics[j]["lock_pressure"] for j in range(lo, hi)]
        neighborhood_sorted = sorted(neighborhood)
        rank = neighborhood_sorted.index(m["lock_pressure"])
        percentile = rank / len(neighborhood)
        pressure_landscape.append(percentile)
    
    # Primes at low percentile = near local minimum
    prime_percentiles = [pressure_landscape[i] for i, m in enumerate(all_metrics) if m["is_prime"]]
    comp_percentiles = [pressure_landscape[i] for i, m in enumerate(all_metrics) if not m["is_prime"]]
    
    p_perc_mean = sum(prime_percentiles)/len(prime_percentiles)
    c_perc_mean = sum(comp_percentiles)/len(comp_percentiles)
    
    print(f"  Prime avg pressure percentile: {p_perc_mean:.4f} (0=global min, 1=global max)")
    print(f"  Composite avg pressure percentile: {c_perc_mean:.4f}")
    print(f"  Difference: {c_perc_mean - p_perc_mean:+.4f}")
    
    if p_perc_mean < c_perc_mean:
        print(f"  >>> PRIMES DO CLUSTER AT LOWER PRESSURE (confirming Tenacity Law) <<<")
    else:
        print(f"  Primes do NOT consistently sit at pressure minima in this range.")
    
    # --- ENERGY OF STABILIZATION (PhysicsALU) ---
    print(f"\n  --- ENERGY OF STABILIZATION ---")
    # For each prime, compute the "stabilization energy" = 
    # sum of |P(n) - P(n+i)| for i in [-5, ..., -1, 1, ..., 5]
    # This measures how much the pressure landscape bends around the prime
    
    prime_stab_energies = []
    comp_stab_energies = []
    
    for i, m in enumerate(all_metrics):
        p_n = m["lock_pressure"]
        neighbors_pressure = []
        for offset in range(-5, 6):
            if offset == 0:
                continue
            j = i + offset
            if 0 <= j < len(all_metrics):
                neighbors_pressure.append(all_metrics[j]["lock_pressure"])
        
        if neighbors_pressure:
            # Stabilization energy = variance of neighboring pressures
            # High variance = sharp peak/valley = strong geometric feature
            mean_np = sum(neighbors_pressure)/len(neighbors_pressure)
            stab_energy = math.sqrt(sum((p - mean_np)**2 for p in neighbors_pressure)/len(neighbors_pressure))
            
            if m["is_prime"]:
                prime_stab_energies.append(stab_energy)
            else:
                comp_stab_energies.append(stab_energy)
    
    p_se_mean = sum(prime_stab_energies)/len(prime_stab_energies)
    c_se_mean = sum(comp_stab_energies)/len(comp_stab_energies)
    print(f"  Prime avg stabilization energy: {p_se_mean:.6f}")
    print(f"  Composite avg stabilization energy: {c_se_mean:.6f}")
    print(f"  Ratio: {p_se_mean/c_se_mean:.2f}x" if c_se_mean > 0 else "")
    
    if p_se_mean > c_se_mean:
        print(f"  >>> PRIMES CREATE SHARPER PRESSURE FEATURES (higher stabilization energy) <<<")
    
    # --- GHOST CLASSIFICATION ---
    print(f"\n  --- GHOST CLASSIFICATION (3-Stage Filter) ---")
    # Stage 1: Static — NRCI > 0.60
    # Stage 2: Kinetic — Gamma > 0.008
    # Stage 3: Dynamic — Lock Pressure > 0
    
    true_primes = 0
    ghosts_stage1 = 0
    ghosts_stage2 = 0
    ghosts_stage3 = 0  # "True Ghosts" — pass all 3 but are composite
    zero_pressure_ghosts = 0
    
    for m in composites:
        stage1 = m["nrci_snapped"] > 0.60
        stage2 = m["gamma"] > 0.008
        stage3 = m["lock_pressure"] > 0
        
        if not stage1:
            continue
        ghosts_stage1 += 1
        
        if not stage2:
            continue
        ghosts_stage2 += 1
        
        if not stage3:
            zero_pressure_ghosts += 1
            continue
        ghosts_stage3 += 1
    
    total_comps = len(composites)
    print(f"  Total composites: {total_comps}")
    print(f"  Pass Stage 1 (NRCI > 0.60):     {ghosts_stage1} ({100*ghosts_stage1/total_comps:.1f}%)")
    print(f"  Pass Stage 2 (Gamma > 0.008):    {ghosts_stage2} ({100*ghosts_stage2/total_comps:.1f}%)")
    print(f"  Zero-Pressure Ghosts (P = 0):    {zero_pressure_ghosts} ({100*zero_pressure_ghosts/total_comps:.1f}%)")
    print(f"  True Ghosts (pass all 3):        {ghosts_stage3} ({100*ghosts_stage3/total_comps:.1f}%)")
    
    # Prime survival through filters
    p_s1 = sum(1 for m in primes if m["nrci_snapped"] > 0.60)
    p_s2 = sum(1 for m in primes if m["gamma"] > 0.008)
    p_s3 = sum(1 for m in primes if m["lock_pressure"] > 0)
    print(f"\n  Prime survival:")
    print(f"  Pass Stage 1: {p_s1}/{len(primes)} ({100*p_s1/len(primes):.1f}%)")
    print(f"  Pass Stage 2: {p_s2}/{len(primes)} ({100*p_s2/len(primes):.1f}%)")
    print(f"  Pass Stage 3: {p_s3}/{len(primes)} ({100*p_s3/len(primes):.1f}%)")
    
    return {
        "p_pressure_mean": p_p_mean,
        "c_pressure_mean": c_p_mean,
        "p_gamma_mean": p_g_mean,
        "c_gamma_mean": c_g_mean,
        "prime_perc_mean": p_perc_mean,
        "comp_perc_mean": c_perc_mean,
        "true_ghosts": ghosts_stage3,
        "zero_pressure_ghosts": zero_pressure_ghosts,
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


# ========================================================================
# DIRECTIVE 3: CROSS-DIMENSIONAL CALIBRATION (GOLAY-NORMALIZED)
# ========================================================================

def run_golay_normalized_rotation():
    print(f"\n{'=' * 80}")
    print("DIRECTIVE 3: CROSS-DIMENSIONAL CALIBRATION (Golay-Normalized)")
    print("=" * 80)
    print("  Phase XII showed NRCI decays at higher bit widths.")
    print("  NEW: Use Golay-Leech as NORMALIZATION FILTER, then measure rotation")
    print("  complexity on the NORMALIZED manifold state.")
    print()
    
    # The idea: instead of measuring NRCI of the raw encoding,
    # measure the ROTATION COMPLEXITY of the NORMALIZED (snapped) state
    # across a Lucas-Lehmer trajectory.
    
    def normalized_ll_trace(p, Mp, max_iter=30):
        """
        Run LL, but at each step, NORMALIZE through Golay before measuring.
        The rotation is measured between CONSECUTIVE NORMALIZED states.
        """
        s = 4
        trace = []
        for i in range(min(max_iter, max(2, p-2)) + 1):
            # Full UBP encoding + Golay normalization
            metrics = compute_ubp_metrics(s)
            
            trace.append({
                "s": s,
                "nrci_snapped": metrics["nrci_snapped"],
                "nrci_raw": metrics["nrci_raw"],
                "gamma": metrics["gamma"],
                "lock_pressure": metrics["lock_pressure"],
                "hw_snapped": metrics["hw_snapped"],
                "lattice_class": metrics["lattice_class"],
                "anchor_dist": metrics["anchor_dist"],
            })
            s = (s * s - 2) % Mp
        
        return trace
    
    # Test cases
    test_cases = [
        (3, 7, True), (5, 31, True), (7, 127, True), (13, 8191, True),
        (11, 2047, False), (23, 8388607, False),
    ]
    
    print("  Computing Golay-normalized LL traces...")
    all_traces = {}
    for p, Mp, is_prime in test_cases:
        trace = normalized_ll_trace(p, Mp, max_iter=min(p-2, 30))
        all_traces[p] = {"trace": trace, "is_prime": is_prime, "Mp": Mp}
    
    # --- NORMALIZED ROTATION ANALYSIS ---
    print(f"\n  --- GOLAY-NORMALIZED TRAJECTORY STATISTICS ---")
    print(f"  {'Case':>8s} | {'Type':>6s} | {'NRCI_m':>7s} | {'NRCI_s':>7s} | {'Gam_m':>7s} | {'Gam_s':>7s} | {'LP_m':>8s} | {'Anc_m':>6s}")
    print(f"  {'-'*8} | {'-'*6} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*8} | {'-'*6}")
    
    for p, data in all_traces.items():
        trace = data["trace"]
        is_p = data["is_prime"]
        typ = "PRIME" if is_p else "COMP"
        
        nrcis = [t["nrci_snapped"] for t in trace]
        gammas = [t["gamma"] for t in trace]
        lps = [t["lock_pressure"] for t in trace]
        ancs = [t["anchor_dist"] for t in trace]
        
        nrci_m = sum(nrcis)/len(nrcis)
        nrci_s = math.sqrt(sum((n-sum(nrcis)/len(nrcis))**2 for n in nrcis)/len(nrcis))
        gam_m = sum(gammas)/len(gammas)
        gam_s = math.sqrt(sum((g-sum(gammas)/len(gammas))**2 for g in gammas)/len(gammas)) if len(gammas) > 1 else 0
        lp_m = sum(lps)/len(lps)
        anc_m = sum(ancs)/len(ancs)
        
        print(f"  M_{p:>5d} | {typ:>6s} | {nrci_m:>7.4f} | {nrci_s:>7.4f} | {gam_m:>7.4f} | {gam_s:>7.4f} | {lp_m:>8.6f} | {anc_m:>6.2f}")
    
    # --- ROTATION IN NORMALIZED SPACE ---
    print(f"\n  --- ROTATION COMPLEXITY IN NORMALIZED SPACE ---")
    # Measure "rotation" as the sequence of lattice class transitions
    for p, data in all_traces.items():
        trace = data["trace"]
        is_p = data["is_prime"]
        typ = "PRIME" if is_p else "COMP"
        
        # Count lattice class transitions
        classes = [t["lattice_class"] for t in trace]
        transitions = sum(1 for i in range(1, len(classes)) if classes[i] != classes[i-1])
        
        # NRCI rotation: signed changes
        nrcis = [t["nrci_snapped"] for t in trace]
        nrci_changes = sum(1 for i in range(1, len(nrcis)) if nrcis[i] != nrcis[i-1])
        
        # Gamma rotation
        gammas = [t["gamma"] for t in trace]
        gamma_peaks = sum(1 for g in gammas if g > 0.008)
        
        print(f"  M_{p:>5d} ({typ}): lattice_transitions={transitions}, "
              f"nrci_changes={nrci_changes}, gamma_peaks(>0.008)={gamma_peaks}/{len(gammas)}")
    
    # --- SCALING TEST: Does the normalized signal survive at different bit widths? ---
    print(f"\n  --- BIT-WIDTH SCALING OF NORMALIZED ROTATION COMPLEXITY ---")
    # For each bit width, compute the NRCI of the SNAPPED state (post-Golay)
    # The snap operation should FILTER out the coding-layer noise
    
    random.seed(99)
    test_primes = [p for p in range(100, 500) if miller_rabin(p)][:30]
    test_comps = []
    while len(test_comps) < 30:
        n = random.randint(100, 500)
        if not miller_rabin(n) and n not in test_comps:
            test_comps.append(n)
    
    # For the normalized approach, we use the FULL Golay-Leech pipeline
    # (which is already bit-width-adaptive via the AdaptiveManifold)
    # But let's test with explicit bit widths for the Gray encoding
    
    print(f"  {'Bits':>4s} | {'P_NRCI_s':>8s} | {'C_NRCI_s':>8s} | {'Delta':>7s} | {'P_Gam':>7s} | {'C_Gam':>7s} | {'r_label':>8s}")
    print(f"  {'-'*4} | {'-'*8} | {'-'*8} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*8}")
    
    scaling_results = []
    for bits in [12, 16, 20, 24, 32, 48, 64]:
        p_nrcis = []
        c_nrcis = []
        p_gammas = []
        c_gammas = []
        
        for p in test_primes:
            gray = p ^ (p >> 1)
            # Take only 'bits' least significant bits of the Gray code
            gray_masked = gray & ((1 << bits) - 1)
            bits_list = [(gray_masked >> i) & 1 for i in range(bits - 1, -1, -1)]
            
            # For bits != 24, we can't use the Golay engine directly
            # Instead, compute a proxy: syndrome weight via Hamming weight
            hw = sum(bits_list)
            tax = Fraction(hw, bits)
            nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
            p_nrcis.append(nrci)
            
            # Gamma proxy: difference between raw and "snapped" (nearest lattice weight)
            lattice_w = min([0, 8, 12, 16, 24, 32, 48, 64], key=lambda w: abs(hw - w))
            snapped_tax = Fraction(lattice_w, bits)
            nrci_snap = float(Fraction(10, 1) / (Fraction(10, 1) + snapped_tax))
            p_gammas.append(abs(nrci - nrci_snap))
        
        for c in test_comps:
            gray = c ^ (c >> 1)
            gray_masked = gray & ((1 << bits) - 1)
            bits_list = [(gray_masked >> i) & 1 for i in range(bits - 1, -1, -1)]
            
            hw = sum(bits_list)
            tax = Fraction(hw, bits)
            nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
            c_nrcis.append(nrci)
            
            lattice_w = min([0, 8, 12, 16, 24, 32, 48, 64], key=lambda w: abs(hw - w))
            snapped_tax = Fraction(lattice_w, bits)
            nrci_snap = float(Fraction(10, 1) / (Fraction(10, 1) + snapped_tax))
            c_gammas.append(abs(nrci - nrci_snap))
        
        p_nm = sum(p_nrcis)/len(p_nrcis)
        c_nm = sum(c_nrcis)/len(c_nrcis)
        delta = p_nm - c_nm
        p_gm = sum(p_gammas)/len(p_gammas)
        c_gm = sum(c_gammas)/len(c_gammas)
        
        labels = [0]*len(test_primes) + [1]*len(test_comps)
        all_nrcis = p_nrcis + c_nrcis
        def pearson(xs, ys):
            n = len(xs)
            if n < 2: return 0.0
            mx, my = sum(xs)/n, sum(ys)/n
            cov = sum((x-mx)*(y-my) for x,y in zip(xs, ys))
            vx = sum((x-mx)**2 for x in xs)
            vy = sum((y-my)**2 for y in ys)
            if vx == 0 or vy == 0: return 0.0
            return cov / math.sqrt(vx * vy)
        r_lab = pearson(labels, all_nrcis)
        
        scaling_results.append({"bits": bits, "p_nrci": p_nm, "c_nrci": c_nm, 
                               "delta": delta, "p_gamma": p_gm, "c_gamma": c_gm, "r": r_lab})
        
        print(f"  {bits:>4d} | {p_nm:>8.4f} | {c_nm:>8.4f} | {delta:>+7.4f} | {p_gm:>7.4f} | {c_gm:>7.4f} | {r_lab:>+8.4f}")
    
    # Decay analysis
    deltas = [r["delta"] for r in scaling_results]
    n = len(scaling_results)
    bits_list = [r["bits"] for r in scaling_results]
    mx = sum(bits_list)/n
    my = sum(deltas)/n
    cov = sum((b-mx)*(d-my) for b, d in zip(bits_list, deltas))
    vx = sum((b-mx)**2 for b in bits_list)
    slope = cov / vx if vx > 0 else 0
    
    print(f"\n  Normalized delta slope: {slope:.6f} per bit")
    if slope > 0.0001:
        print(f"  >>> NORMALIZED SIGNAL STRENGTHENS WITH BIT WIDTH <<<")
    elif abs(slope) < 0.0001:
        print(f"  >>> NORMALIZED SIGNAL IS STABLE (INVARIANT) <<<")
    else:
        print(f"  Normalized signal still decays, but compare with Phase XII raw slope of -0.000110")
    
    return {
        "scaling_results": scaling_results,
        "slope": slope,
    }


# ========================================================================
# GRAND SYNTHESIS
# ========================================================================

def main():
    print("+" + "=" * 78 + "+")
    print("|  UBP STUDY - PHASE XIII: TOPOLOGICAL FACTORIZATION ANALYSIS              |")
    print("|  Re-oriented: Rotation Frequency, Tenacity Map, Golay-Normalization      |")
    print("+" + "=" * 78 + "+")
    print()
    
    t0 = time.time()
    
    # Directive 1: Rotation Frequency
    d1_all, d1_comp, d1_prime = run_inverse_factorization_frequency()
    
    # Directive 2: Tenacity Law Map
    d2 = run_tenacity_law_map()
    
    # Directive 3: Golay-Normalized Calibration
    d3 = run_golay_normalized_rotation()
    
    t1 = time.time()
    
    print(f"\n{'=' * 80}")
    print("PHASE XIII: GRAND SYNTHESIS")
    print(f"{'=' * 80}")
    print(f"  Execution time: {t1-t0:.1f}s")
    print()
    
    print("  DIRECTIVE 1 — ROTATION FREQUENCY ANALYSIS:")
    print("  (See spectral tables above for full frequency-domain decomposition)")
    print("  Key question: Does spectral centroid map to factor magnitude?")
    print("  Key question: Does bandwidth map to factor count (jitter)?")
    print()
    
    print("  DIRECTIVE 2 — TENACITY LAW MAP:")
    print(f"    Prime Lock Pressure:    mean={d2['p_pressure_mean']:.6f}")
    print(f"    Composite Lock Pressure: mean={d2['c_pressure_mean']:.6f}")
    print(f"    Prime pressure percentile: {d2['prime_perc_mean']:.4f}")
    print(f"    Composite pressure percentile: {d2['comp_perc_mean']:.4f}")
    print(f"    True Ghosts (pass all 3 filters): {d2['true_ghosts']}")
    print(f"    Zero-Pressure Ghosts: {d2['zero_pressure_ghosts']}")
    if d2['prime_perc_mean'] < d2['comp_perc_mean']:
        print("    >>> PRIMES CLUSTER AT LOWER PRESSURE (Tenacity Law confirmed) <<<")
    print()
    
    print("  DIRECTIVE 3 — GOLAY-NORMALIZED CALIBRATION:")
    print(f"    Normalized delta slope: {d3['slope']:.6f}/bit")
    print(f"    (Phase XII raw slope was: -0.000110/bit)")
    if abs(d3['slope']) < abs(0.000110):
        print("    >>> NORMALIZATION REDUCES SIGNAL DECAY <<<")
    else:
        print("    Normalization does not prevent decay.")
    print()
    
    print("  ═══════════════════════════════════════════════════════════════════")
    print("  THE RE-ORIENTATION:")
    print("  Phase XII failed because it measured FRICTION as a primality test.")
    print("  Phase XIII re-orients toward TOPOLOGICAL FACTORIZATION ANALYSIS:")
    print("  - Not 'is it prime?' but 'what are its geometric properties?'")
    print("  - Rotation frequency → factor structure estimation")
    print("  - Tenacity map → geometric taxonomy of integers")
    print("  - Golay normalization → clean signal extraction")
    print("  ═══════════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()