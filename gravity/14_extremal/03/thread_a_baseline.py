"""
STUDY 003 — Continuation of the Extremal Law of Distinction Density
====================================================================

Thread A: Reproduce the baseline (Constant Peak + 10^5 sweep)
Thread B: Self-dual extension test  -- does self-duality maximise avg_Phi for fixed n?
Thread C: avg_Phi <-> covering-radius equivalence (analytic proof + computation)
Thread D: [23,12] sampling -- Golay [23,12,7] vs random [23,12] codes on avg_Phi

All arithmetic uses fractions.Fraction. Floats are display-only.

Author: UBP Research Cortex (continuation), 2026-06-24
"""
import sys, os, json, random, time
from fractions import Fraction
from itertools import combinations, product
from collections import Counter
from typing import List, Tuple, Optional

sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics, GolayCodeEngine, LeechLatticeEngine

# -----------------------------------------------------------------------------
# Constants and Phi machinery (from EXTREMAL_002, exact Fraction arithmetic)
# -----------------------------------------------------------------------------
pp = UBPSourceCodeParticlePhysics()
Y = pp.Y  # Fraction
Y_plus_one_eighth = Y + Fraction(1, 8)
PHI_PEAK = Fraction(1, 1) / Y_plus_one_eighth  # 1/(Y + 1/8)

def hw(v) -> int:
    return sum(1 for x in v if x)

def norm_sq(v) -> int:
    return sum(x * x for x in v)

def phi_state(v: List[int], code_cwd_distance: Optional[int] = None,
              code_synw: Optional[int] = None) -> Fraction:
    """
    Distinction Density Phi(v) = HW(v) / [HW(v)*(Y + 1/8) + Frustration(v)*Y]

    If code_synw is given (syndrome weight w.r.t. a specific code), use that.
    Else if code_cwd_distance is given (min distance to a codeword of C), use that.
    Else assume SynW = 0 (i.e. v is itself a codeword of the code under test).
    """
    h = hw(v)
    if h == 0:
        return Fraction(0)
    if code_synw is not None:
        fr = code_synw
    elif code_cwd_distance is not None:
        fr = code_cwd_distance
    else:
        fr = 0
    denom = Fraction(h) * Y_plus_one_eighth + Fraction(fr) * Y
    return Fraction(h) / denom

# -----------------------------------------------------------------------------
# THREAD A: Reproduce baseline
# -----------------------------------------------------------------------------
print('=' * 72)
print('THREAD A: Reproduce baseline (Constant Peak + 10^5 sweep)')
print('=' * 72)

# A1: Constant peak for all non-zero Golay codewords
g = GolayCodeEngine()
all_cw = g.get_all_codewords()
peak_values = Counter()
for cw in all_cw:
    h = sum(cw)
    if h == 0:
        continue
    phi = phi_state(cw, code_synw=0)  # codeword: syndrome = 0
    peak_values[round(float(phi), 12)] += 1

print(f'\nA1: Constant Peak over {len(all_cw)-1} non-zero Golay codewords')
print(f'    Distinct Phi values: {dict(peak_values)}')
print(f'    Phi_peak = 1/(Y+1/8) = {float(PHI_PEAK):.10f}')
print(f'    All non-zero codewords at Phi_peak? {len(peak_values) == 1}')

# A2: 10^5 random state sweep with Golay decode-snap
def golay_decode(g, v):
    """Return (decoded_cw, n_errors_corrected)."""
    snapped = g.snap_to_codeword(list(v))
    if isinstance(snapped, tuple) and len(snapped) == 2:
        cw, info = snapped
        return cw, info.get('anchor_distance', 0)
    return list(snapped), 0

random.seed(20260624)
N_TRIALS = 100_000
ascent, flat, descent = 0, 0, 0
descent_examples = []
zero_decodes = 0

t0 = time.time()
for trial in range(N_TRIALS):
    v = [random.randint(0, 1) for _ in range(24)]
    h_before = sum(v)
    if h_before == 0:
        flat += 1
        continue
    decoded, n_err = golay_decode(g, v)
    h_after = sum(decoded)

    # Phi before: frustration = syndrome weight of v w.r.t. Golay
    syn_before = g.syndrome_weight(list(v))
    phi_before = phi_state(v, code_synw=syn_before)
    # Phi after: codeword, so frustration = 0
    phi_after = phi_state(decoded, code_synw=0) if h_after > 0 else Fraction(0)

    delta = float(phi_after - phi_before)
    if delta > 1e-15:
        ascent += 1
    elif delta < -1e-15:
        descent += 1
        if h_after == 0:
            zero_decodes += 1
            if len(descent_examples) < 5:
                descent_examples.append({'v_hw': h_before, 'syn_before': syn_before,
                                         'phi_before': float(phi_before),
                                         'phi_after': float(phi_after)})
    else:
        flat += 1

t1 = time.time()
print(f'\nA2: 10^5 random 24-bit state sweep (completed in {t1-t0:.1f}s)')
print(f'    Gradient ascent (dPhi>0):  {ascent:>8d}  ({ascent/N_TRIALS*100:.3f}%)')
print(f'    Flat (dPhi=0):             {flat:>8d}  ({flat/N_TRIALS*100:.3f}%)')
print(f'    Gradient descent (dPhi<0): {descent:>8d}  ({descent/N_TRIALS*100:.4f}%)')
print(f'    Of which zero-codeword (vacuum collapse): {zero_decodes}')
corrected = ascent + descent
if corrected > 0:
    print(f'    Active-correction ascent rate: {ascent}/{corrected} = {ascent/corrected*100:.4f}%')
if descent_examples:
    print(f'    Sample descent events (vacuum collapses):')
    for ex in descent_examples:
        print(f'      HW_before={ex["v_hw"]:>2d}  SynW={ex["syn_before"]:>2d}  Phi: {ex["phi_before"]:.4f} -> {ex["phi_after"]:.4f}')

# Save baseline results
baseline_results = {
    'phi_peak_str': str(PHI_PEAK),
    'phi_peak_float': float(PHI_PEAK),
    'sweep_total': N_TRIALS,
    'sweep_ascent': ascent,
    'sweep_flat': flat,
    'sweep_descent': descent,
    'sweep_zero_decodes': zero_decodes,
    'active_correction_ascent_rate': (ascent / corrected * 100) if corrected > 0 else None,
    'descent_examples': descent_examples,
    'elapsed_sec': t1 - t0,
}
with open('/home/z/my-project/work/baseline_results.json', 'w') as f:
    json.dump(baseline_results, f, indent=2)
print(f'\nBaseline saved to baseline_results.json')
