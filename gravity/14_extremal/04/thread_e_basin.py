"""
THREAD E: Vacuum Collapse Basin -- Exact Characterisation (Open Q4)
====================================================================

EXTREMAL_002 Section 5.4 left this open: "What is the exact basin of
attraction of the zero codeword in the Phi landscape? This is a precisely
defined mathematical question -- it amounts to characterising all 24-bit
vectors v for which the nearest codeword under Golay decoding is the zero
word. That boundary determines the size of the 'quantum vacuum' in this
model."

We answer it exactly for the [24,12,8] extended Golay code.

DEFINITION: The vacuum basin B(0) is the set of v in F_2^24 such that
Golay-decode(v) = 0. Equivalently (under the standard nearest-codeword
decoder with tie-breaking towards lower HW):

  B(0) = { v in F_2^24 : HW(v) < HW(v XOR c) for all nonzero c in C }
       union { v in F_2^24 : HW(v) = HW(v XOR c) for all c in C, with tie-break to 0 }

For binary: HW(v XOR c) = HW(v) + HW(c) - 2 * (v . c)
where (v . c) is the overlap (number of common 1-positions).

So HW(v XOR c) > HW(v)  iff  HW(c) > 2 * (v . c)
   HW(v XOR c) = HW(v)  iff  HW(c) = 2 * (v . c)

For Golay [24,12,8]:
  - HW(c) in {0, 8, 12, 16, 24} only.
  - For c with HW=8 (octad, 759 of them): need 8 > 2*(v.c)  i.e. (v.c) <= 3
                                            or  8 = 2*(v.c) i.e. (v.c) = 4 (tie)
  - For c with HW=12 (dodecad, 2576 of them): need 12 > 2*(v.c) i.e. (v.c) <= 5
                                                or  12 = 2*(v.c) i.e. (v.c) = 6 (tie)
  - For c with HW=16: need 16 > 2*(v.c) i.e. (v.c) <= 7
                       or  16 = 2*(v.c) i.e. (v.c) = 8 (tie)
  - For c with HW=24 (all-ones): need 24 > 2*(v.c) i.e. (v.c) <= 11
                                  or  24 = 2*(v.c) i.e. (v.c) = 12 (tie, only if HW(v) = 12)

For v with HW(v) <= 3: (v.c) <= HW(v) <= 3 < 4, so all octad constraints are satisfied strictly.
  -> HW <= 3 vectors always decode to 0.
  -> Count: C(24,1) + C(24,2) + C(24,3) + 1 = 24 + 276 + 2024 + 1 = 2325.

For v with HW(v) = 4: Need (v.c) <= 3 for all octads c (no octad contains v as a subset of size 4),
   OR (v.c) = 4 for some octads but tie-break goes to 0.
  But tie-breaking depends on the decoder. For the standard Golay decoder, ties are broken
  towards the unique codeword with a specific structure (typically the lexicographically smallest).
  We'll compute this exactly by enumeration.

For v with HW(v) >= 5: there are octads with (v.c) >= 4, so HW(v XOR c) <= HW(v). Decodes to nonzero c.

So the vacuum basin has HW <= 4 vectors, with HW=4 being the boundary.

This script:
  1. Enumerates all 24-bit vectors with HW <= 4 (a tractable 11,851 vectors).
  2. For each, queries the live Golay engine for its decoded codeword.
  3. Categorises: which decode to 0, which decode to nonzero, which are codewords themselves.
  4. Confirms the HW<=3 perfect-ball result.
  5. Characterises the HW=4 boundary exactly.
"""
import sys, time, json
from itertools import combinations
from collections import Counter, defaultdict
sys.path.insert(0, '/home/z/my-project/work')
from ubp_unified_v5 import UBPSourceCodeParticlePhysics, GolayCodeEngine

pp = UBPSourceCodeParticlePhysics()
g = GolayCodeEngine()

# Get all codewords (we'll need them for analytic checks)
all_cw = g.get_all_codewords()
# Build set of tuples for membership
cw_set = set(tuple(c) for c in all_cw)
# Get octads (HW=8 codewords)
octads = [c for c in all_cw if sum(c) == 8]
print(f'Total codewords: {len(all_cw)} (expected 4096)')
print(f'Octads (HW=8): {len(octads)} (expected 759)')

# Pre-compute octad support sets for fast overlap computation
octad_supports = [frozenset(i for i, x in enumerate(c) if x) for c in octads]

print('\n' + '=' * 72)
print('THREAD E: Vacuum Collapse Basin -- Exact Characterisation')
print('=' * 72)

# Helper: get decoded codeword via the live engine
def golay_decode_to_cw(v):
    """Return the codeword (as a tuple) that v decodes to."""
    snapped = g.snap_to_codeword(list(v))
    if isinstance(snapped, tuple) and len(snapped) == 2:
        cw, info = snapped
        return tuple(cw), info
    return tuple(snapped), {}

# ----- Phase 1: HW <= 3 perfect ball -----
print('\n--- Phase 1: HW <= 3 perfect ball ---')
hw_le_3_count = 0
hw_le_3_to_zero = 0
hw_le_3_to_nonzero = 0
hw_le_3_is_codeword = 0
for hw_val in [0, 1, 2, 3]:
    for positions in combinations(range(24), hw_val):
        v = [0] * 24
        for p in positions:
            v[p] = 1
        v_t = tuple(v)
        hw_le_3_count += 1
        decoded, info = golay_decode_to_cw(v)
        is_cw = (v_t in cw_set)
        if is_cw:
            hw_le_3_is_codeword += 1
        if sum(decoded) == 0:
            hw_le_3_to_zero += 1
        else:
            hw_le_3_to_nonzero += 1
            if hw_val <= 3:
                print(f'  WARNING: HW={hw_val} vector {positions} decoded to nonzero codeword (HW={sum(decoded)})')

print(f'  Total HW<=3 vectors: {hw_le_3_count}')
print(f'    -> decodes to 0:        {hw_le_3_to_zero}')
print(f'    -> decodes to nonzero:  {hw_le_3_to_nonzero}')
print(f'    -> is itself a codeword: {hw_le_3_is_codeword}')
expected_perfect = 1 + 24 + 276 + 2024  # C(24,0)+C(24,1)+C(24,2)+C(24,3)
print(f'  Expected if d=8 perfect ball: {expected_perfect}')
print(f'  Match? {hw_le_3_count == expected_perfect and hw_le_3_to_zero == expected_perfect}')

# ----- Phase 2: HW = 4 boundary -----
print('\n--- Phase 2: HW = 4 boundary ---')
hw4_total = 0
hw4_to_zero = 0  # decodes to 0 codeword
hw4_to_octad = 0  # decodes to HW=8 codeword
hw4_to_dodecad = 0  # decodes to HW=12 codeword
hw4_to_hexadecad = 0  # decodes to HW=16 codeword
hw4_to_ones = 0  # decodes to HW=24 codeword
hw4_uncorrectable = 0  # decoder refuses (syndrome weight > 3), returns input unchanged
hw4_overlap_hist = Counter()

# For each HW=4 vector, also record:
#   - max overlap with any octad
#   - syndrome weight
#   - whether it's a valid codeword (should never be, since d=8)
#   - decoder outcome category
hw4_records = []
hw4_syndrome_hist = Counter()
hw4_decoded_hw_hist = Counter()

for positions in combinations(range(24), 4):
    v = [0] * 24
    for p in positions:
        v[p] = 1
    v_t = tuple(v)
    hw4_total += 1
    decoded, info = golay_decode_to_cw(v)
    decoded_hw = sum(decoded)
    correctable = info.get('correctable', True)
    corrected = info.get('corrected', True)
    syn_w = info.get('syndrome_weight', 0)

    # Compute overlaps with all octads
    v_set = frozenset(positions)
    overlaps = [len(v_set & oct_support) for oct_support in octad_supports]
    max_overlap = max(overlaps)
    hw4_overlap_hist[max_overlap] += 1
    hw4_syndrome_hist[syn_w] += 1
    hw4_decoded_hw_hist[decoded_hw] += 1

    if not correctable or not corrected:
        # Decoder refused to correct: returns input unchanged
        hw4_uncorrectable += 1
        category = 'uncorrectable'
    elif decoded_hw == 0:
        hw4_to_zero += 1
        category = 'to_zero'
    elif decoded_hw == 8:
        hw4_to_octad += 1
        category = 'to_octad'
    elif decoded_hw == 12:
        hw4_to_dodecad += 1
        category = 'to_dodecad'
    elif decoded_hw == 16:
        hw4_to_hexadecad += 1
        category = 'to_hexadecad'
    elif decoded_hw == 24:
        hw4_to_ones += 1
        category = 'to_ones'
    else:
        category = f'to_HW{decoded_hw}'

    hw4_records.append({
        'positions': positions,
        'max_overlap': max_overlap,
        'syn_weight': syn_w,
        'decoded_hw': decoded_hw,
        'category': category,
    })

print(f'  Total HW=4 vectors: {hw4_total}  (expected C(24,4) = {10626})')
print(f'    -> uncorrectable (decoder returns input): {hw4_uncorrectable}')
print(f'    -> decodes to 0 (zero codeword):           {hw4_to_zero}')
print(f'    -> decodes to octad (HW=8):                {hw4_to_octad}')
print(f'    -> decodes to dodecad (HW=12):             {hw4_to_dodecad}')
print(f'    -> decodes to hexadecad (HW=16):           {hw4_to_hexadecad}')
print(f'    -> decodes to all-ones (HW=24):            {hw4_to_ones}')
print(f'  Max-overlap distribution: {dict(sorted(hw4_overlap_hist.items()))}')
print(f'  Syndrome-weight distribution: {dict(sorted(hw4_syndrome_hist.items()))}')
print(f'  Decoded-HW distribution: {dict(sorted(hw4_decoded_hw_hist.items()))}')

# ----- Phase 3: Summary -----
print('\n--- Phase 3: Total vacuum basin ---')
basin_total = hw_le_3_to_zero + hw4_to_zero
print(f'  HW <= 3 in basin: {hw_le_3_to_zero}')
print(f'  HW == 4 in basin: {hw4_to_zero}')
print(f'  TOTAL vacuum basin size: {basin_total}')
print(f'  Fraction of F_2^24: {basin_total} / 2^24 = {basin_total / 16777216 * 100:.6f}%')

# ----- Phase 4: Characterise the HW=4 boundary -----
print('\n--- Phase 4: HW=4 boundary structure ---')
# Group by max_overlap
by_overlap = defaultdict(list)
for rec in hw4_records:
    by_overlap[rec['max_overlap']].append(rec)
for ov in sorted(by_overlap.keys()):
    recs = by_overlap[ov]
    n = len(recs)
    to_zero = sum(1 for r in recs if r['category'] == 'to_zero')
    to_octad = sum(1 for r in recs if r['category'] == 'to_octad')
    to_dodecad = sum(1 for r in recs if r['category'] == 'to_dodecad')
    uncorr = sum(1 for r in recs if r['category'] == 'uncorrectable')
    other = n - to_zero - to_octad - to_dodecad - uncorr
    print(f'  max_overlap={ov}: total={n}  to_0={to_zero}  to_octad={to_octad}  to_dodecad={to_dodecad}  uncorrectable={uncorr}  other={other}')

# Save results
results = {
    'hw_le_3_total': hw_le_3_count,
    'hw_le_3_to_zero': hw_le_3_to_zero,
    'hw_le_3_is_codeword': hw_le_3_is_codeword,
    'expected_perfect_ball': expected_perfect,
    'hw4_total': hw4_total,
    'hw4_uncorrectable': hw4_uncorrectable,
    'hw4_to_zero': hw4_to_zero,
    'hw4_to_octad': hw4_to_octad,
    'hw4_to_dodecad': hw4_to_dodecad,
    'hw4_to_hexadecad': hw4_to_hexadecad,
    'hw4_to_ones': hw4_to_ones,
    'hw4_overlap_hist': dict(hw4_overlap_hist),
    'hw4_syndrome_hist': dict(hw4_syndrome_hist),
    'hw4_decoded_hw_hist': dict(hw4_decoded_hw_hist),
    'basin_total': basin_total,
    'basin_fraction_of_F2_24': basin_total / 16777216,
}
with open('/home/z/my-project/work/basin_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\nSaved to basin_results.json')
