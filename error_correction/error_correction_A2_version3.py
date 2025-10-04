"""
A2 Lattice Error Correction & Geo-Structural Resonance (GLR/NRCI/Feedback)
--------------------------------------------------------------------------
Author: Euan Craig, New Zealand
Date: 04 October 2025

Integrates:
- A2 lattice geometric mapping
- Geometric resonance parser
- NRCI feedback loop
- GLR layer (weighted correction & escalation)
- Automatic recommendation & correction history

Usage:
    from error_correction.A2_version3 import full_error_correction

    result = full_error_correction(offbit, symbol_A, symbol_B, features, realm_encoding, crv, realm)
    print(result)
"""

import numpy as np

# --- 1. A2 Lattice Mapping ---
A2_VECTORS = {
    0: (0.0, 0.0),
    1: (1.0, 0.0),
    2: (0.5, np.sqrt(3)/2),
    3: (-0.5, np.sqrt(3)/2)
}

def map_offbit_to_a2_coordinate(offbit: np.ndarray) -> tuple[float, float]:
    offbit = offbit.astype(int)
    padded = np.pad(offbit, (0, max(0, 32 - len(offbit))), "constant")[:32]
    pairs = padded.reshape(16, 2)
    pair_values = pairs[:, 0] * 2 + pairs[:, 1]
    x_coord = sum(A2_VECTORS.get(val, (0.0,0.0))[0] for val in pair_values)
    y_coord = sum(A2_VECTORS.get(val, (0.0,0.0))[1] for val in pair_values)
    scale = 5.0 / (16.0 / 2)
    return x_coord * scale, y_coord * scale

# --- 2. Geo-Parser Resonance ---
def geometric_add(segments_A, segments_B):
    set_A = set(tuple(sorted(seg)) for seg in segments_A)
    set_B = set(tuple(sorted(seg)) for seg in segments_B)
    result_segments = list(set_A.union(set_B))
    coincident_segments = list(set_A.intersection(set_B))
    coherence_count = len(coincident_segments)
    total_unique_segments = len(result_segments)
    return result_segments, coherence_count, total_unique_segments

def compute_resonance_score(segments_A, segments_B, target_segments=None):
    result_segs, coherence, total = geometric_add(segments_A, segments_B)
    if target_segments:
        target_set = set(tuple(sorted(seg)) for seg in target_segments)
        matched = len(set(result_segs).intersection(target_set))
        error = len(set(result_segs).difference(target_set))
        TARGET_SEG_COUNT = len(target_set)
        resonance_score = (matched - error) / (TARGET_SEG_COUNT or 1)
        return resonance_score, matched, error, total
    else:
        return coherence / (total or 1), coherence, total-coherence, total

# --- 3. NRCI Feedback (adapted from your repo logic) ---
def calculate_nrci(system_values, target_values):
    S, T = np.array(system_values), np.array(target_values)
    n = len(S)
    numerator = np.sqrt(np.sum((S - T) ** 2) / n)
    denominator = np.std(T) if np.std(T) > 0 else 1.0
    nrci = 1 - (numerator / denominator)
    return float(max(0.0, min(1.0, nrci)))

# --- 4. GLR Correction Layer ---
def glr_correction(frequencies, nrcis, candidates=[3.14159, 36.339691]):
    errors = []
    for f in candidates:
        err = sum(w * abs(fi - f) for fi, w in zip(frequencies, nrcis))
        errors.append((err, f))
    err_min, f_corrected = min(errors)
    return f_corrected, err_min

# --- 5. Full Correction Wrapper ---
def full_error_correction(offbit, symbol_A, symbol_B, features, realm_encoding, crv, realm="electromagnetic", feedback_loops=2, nrci_thresholds=(0.2, 0.5, 0.9997)):
    # Step 1: A2 mapping
    coord_xy = map_offbit_to_a2_coordinate(offbit)
    # Step 2: Geo-Parser resonance
    # Placeholder: Replace with your actual segment definitions
    GEO_FORMS = {
        '1': [('V0', 'V1')],
        '0': [('C1', 'C2'), ('C2', 'C4'), ('C4', 'C3'), ('C3', 'C1')],
        # Add others as needed...
    }
    seg_A = GEO_FORMS.get(symbol_A, [])
    seg_B = GEO_FORMS.get(symbol_B, [])
    resonance_score, matched, error, total = compute_resonance_score(seg_A, seg_B, target_segments=seg_B)
    # Step 3: NRCI feedback loop
    system_values = [resonance_score, coord_xy[0]/5.0, coord_xy[1]/5.0]
    target_values = [1.0, 0.0, 0.0]
    nrci = calculate_nrci(system_values, target_values)
    history = []
    details = []
    current_offbit = offbit.copy()

    for loop in range(feedback_loops):
        if nrci < nrci_thresholds[0]:
            flip_idx = np.random.randint(0, current_offbit.size)
            current_offbit[flip_idx] ^= 1
            coord_xy = map_offbit_to_a2_coordinate(current_offbit)
            system_values = [resonance_score, coord_xy[0]/5.0, coord_xy[1]/5.0]
            nrci = calculate_nrci(system_values, target_values)
            details.append(f"Loop {loop+1}: NRCI low, bit {flip_idx} flipped, new NRCI={nrci:.6f}")
        elif nrci < nrci_thresholds[2]:
            details.append(f"Loop {loop+1}: NRCI moderate ({nrci:.6f}), geometric correction sufficient.")
        else:
            details.append(f"Loop {loop+1}: NRCI high ({nrci:.6f}), no correction needed.")
        history.append({'loop': loop+1, 'coordinate': coord_xy, 'nrci': nrci})

    # Step 4: GLR Layer (if NRCI is not sufficient)
    glr_status = None
    recommendation = 'A2'
    z_layer = 0
    if nrci < nrci_thresholds[1]:
        # Frequencies & NRCI weights: placeholder logic
        frequencies = [3.10, 36.34] * 10000  # Example
        nrcis = [nrci] * len(frequencies)
        f_corrected, err_min = glr_correction(frequencies, nrcis)
        glr_status = f"GLR correction applied: f_corrected={f_corrected}, error={err_min:.6f}"
        recommendation = 'GLR'
        z_layer = 1
        details.append(f"NRCI ({nrci:.6f}) below threshold: invoked GLR correction.")
    elif nrci < nrci_thresholds[2]:
        recommendation = 'A2'
        details.append(f"NRCI ({nrci:.6f}) moderate: A2 geometric correction recommended.")
    else:
        recommendation = 'A2-high'
        details.append(f"NRCI ({nrci:.6f}) high: A2 correction sufficient.")

    result = {
        'coordinate': (coord_xy[0], coord_xy[1], z_layer),
        'resonance_score': resonance_score,
        'nrci': nrci,
        'recommendation': recommendation,
        'glr_status': glr_status,
        'details': details,
        'history': history
    }
    return result

if __name__ == "__main__":
    # Example Usage
    dummy_offbit = np.random.randint(0, 2, 24)
    # Example symbols (can be replaced with your real segment definitions)
    symbol_A = '1'
    symbol_B = '0'
    features = {'nsites': 12, 'volume': 100, 'density': 5.0}
    realm_encoding = {'primary_realm': 'electromagnetic', 'electromagnetic_coherence': 0.95}
    crv = {'freq': 1e14, 'wavelength': 500, 'toggle_bias': 0.5}

    result = full_error_correction(dummy_offbit, symbol_A, symbol_B, features, realm_encoding, crv)
    print("\nCorrection Result:")
    for k, v in result.items():
        print(f"{k}: {v}")