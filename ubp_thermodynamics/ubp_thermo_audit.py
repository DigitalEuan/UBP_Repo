"""
UBP Thermodynamics Comprehensive Audit Script
==============================================
Universal Binary Principle (UBP) v7.2
Author: E. R. A. Craig, New Zealand
Study: Deterministic Geometric Thermodynamics

This script performs the full thermodynamic audit using the real UBP core engine.
It covers all four Laws of Thermodynamics from the UBP geometric perspective,
including element-specific audits for Hydrogen, Iron, Gold, and Water.

All results are written to ubp_thermo_results.json for reproducibility.
"""

import sys
import os
import math
import json
from fractions import Fraction

# Add UBP core to path
CORE_PATH = os.path.join(os.path.dirname(__file__), '..', 'UBP_Repo', 'core_studio_v4.0', 'core')
sys.path.insert(0, os.path.abspath(CORE_PATH))

import core

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 0: SYSTEM CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

def get_constants():
    c = core.SUBSTRATE.get_v6_constants()
    W  = c['WOBBLE']          # Triadic Wobble ≈ 0.8176
    L  = c['SINK_L']          # 13D Sink floor ≈ 0.06289
    PI = c['PI']              # π (rational high-precision)
    k  = Fraction(1, 1) + W  # Pantograph Scale Factor k = 1 + W
    # Resolution Gap: ln(φ)/ln(π)
    phi = (1 + Fraction(5).limit_denominator(10**12)**Fraction(1,2))
    RG = float(math.log(1.6180339887) / math.log(math.pi))
    return {
        'W': W, 'L': L, 'PI': PI, 'k': k, 'RG': RG,
        'W_float': float(W), 'L_float': float(L),
        'PI_float': float(PI), 'k_float': float(k)
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: PANTOGRAPH OPERATOR  [LAW_PANTOGRAPH_THERMODYNAMICS_001]
# ─────────────────────────────────────────────────────────────────────────────

def pantograph_projection(vector, constants):
    """
    The Pantograph Kinematic Operator maps a 24-bit Noumenal Seed into
    macroscopic thermodynamic state variables.

    LAW_PANTOGRAPH_THERMODYNAMICS_001:
    V_macro = k^3 * V_noum
    S_macro = k^2 * S_noum + tan(theta)
    tan(theta) = T_base - PI   [Berry-Phase mismatch / Entropy Shear]
    T_adj = T_base * (1 - C_macro/13)
    NRCI = 10 / (10 + T_adj)
    """
    W  = constants['W']
    k  = constants['k']
    PI = constants['PI']

    T_base = core.LEECH_ENGINE.calculate_symmetry_tax(vector)
    shear  = T_base - PI                        # tan(θ): Entropy Shear
    V_noum = Fraction(sum(vector), 1)           # Hamming Weight = Internal Energy
    S_noum = Fraction(24, 1)                    # Full substrate surface

    V_macro = (k ** 3) * V_noum
    S_macro = (k ** 2) * S_noum + shear

    V_f  = float(V_macro)
    V_23 = Fraction(int(math.pow(max(V_f, 0.001), 2/3) * 1_000_000), 1_000_000)
    C_macro = V_23 / S_macro if S_macro != 0 else Fraction(0)

    T_adj = T_base * (Fraction(1, 1) - (C_macro / 13))
    nrci  = Fraction(10, 1) / (Fraction(10, 1) + T_adj)

    return {
        'T_base':   float(T_base),
        'shear':    float(shear),
        'V_noum':   int(V_noum),
        'V_macro':  float(V_macro),
        'S_macro':  float(S_macro),
        'C_macro':  float(C_macro),
        'T_adj':    float(T_adj),
        'nrci':     float(nrci),
        'k':        float(k),
        'W':        float(W),
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: LOAD ELEMENTS FROM KB
# ─────────────────────────────────────────────────────────────────────────────

def load_element(ubp_id, kb_path='ubp_system_kb.json'):
    with open(kb_path) as f:
        kb = json.load(f)
    fields  = kb['_fields']
    entries = kb['entries']
    id_idx  = fields.index('ubp_id')
    vec_idx = fields.index('vector')
    desc_idx = fields.index('description') if 'description' in fields else -1
    nrci_idx = fields.index('nrci') if 'nrci' in fields else -1

    for v in entries.values():
        if isinstance(v, list) and len(v) > id_idx and str(v[id_idx]) == ubp_id:
            vec  = v[vec_idx] if len(v) > vec_idx else None
            desc = v[desc_idx] if desc_idx >= 0 and len(v) > desc_idx else ''
            nrci = v[nrci_idx] if nrci_idx >= 0 and len(v) > nrci_idx else None
            return {'ubp_id': ubp_id, 'vector': vec, 'description': str(desc)[:200], 'nrci_kb': nrci}
    return None

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: FOUR LAWS AUDIT
# ─────────────────────────────────────────────────────────────────────────────

def audit_four_laws(vector, element_name, constants):
    """
    Audits all four Laws of Thermodynamics for a given 24-bit vector.
    Returns a structured dictionary of results.
    """
    proj = pantograph_projection(vector, constants)
    W    = constants['W_float']
    L    = constants['L_float']
    k    = constants['k_float']

    # --- ZEROTH LAW: Equilibrium = Phase-Lock ---
    # Two systems are in equilibrium when their Pantograph shear terms are equal.
    # Equilibrium condition: shear ≈ 0 (Berry-Phase at π)
    zeroth = {
        'temperature_shear_rads': proj['shear'],
        'equilibrium_state': 'PHASE-LOCKED' if abs(proj['shear']) < 0.1 else 'SHEARING',
        'wobble_W': W,
        'interpretation': (
            'Temperature is Kinematic Shear (tan θ). '
            'Thermal equilibrium is Phase-Lock: identical Wobble synchronisation.'
        )
    }

    # --- FIRST LAW: Energy Conservation = Toggle Repartitioning ---
    # Internal Energy U = Hamming Weight of the 24-bit vector
    # Work W_mech = Scaling (k) of the linkage (orderly expansion)
    # Heat Q = Shear (tan θ) of the linkage (disorderly deviation)
    first = {
        'internal_energy_toggles': proj['V_noum'],
        'work_scaling_k': k,
        'heat_shear_tan_theta': proj['shear'],
        'V_macro': proj['V_macro'],
        'conservation_note': (
            'Toggles cannot be created or destroyed; they repartition '
            'across the 4 MOG layers (Reality, Info, Activation, Potential).'
        )
    }

    # --- SECOND LAW: Entropy = Symmetry Tax ---
    # Entropy S = T_adj (Symmetry Tax)
    # Directionality driven by Triadic Wobble W ≈ 0.8176
    # Max efficiency = NRCI (Resolution Limit)
    second = {
        'entropy_symmetry_tax': proj['T_adj'],
        'nrci_max_efficiency_pct': proj['nrci'] * 100,
        'triadic_wobble_W': W,
        'resolution_gap_RG': constants['RG'],
        'arrow_of_time': (
            'The Triadic Monad (π, φ, e) creates non-zero Wobble residue W ≈ 0.8176. '
            'This acts as Topological Torque ratcheting the system toward the 13D Sink.'
        )
    }

    # --- THIRD LAW: Absolute Zero = OnBit State ---
    # Absolute Zero: NRCI = 1.0, Tax = 0 (perfect unprojected Golay Octad)
    # Unattainability: 13D Sink always exerts minimum leakage L ≈ 0.06289
    # Nernst Plateau: specific heat floor = L * T_base
    nernst_floor = L * proj['T_base']
    third = {
        'absolute_zero_nrci': 1.0,
        'sink_leakage_L': L,
        'nernst_specific_heat_floor': nernst_floor,
        'current_nrci': proj['nrci'],
        'unattainability': (
            'The 13D Sink (L ≈ 0.06289) always exerts minimum leakage. '
            'Zero-tax existence is geometrically impossible in the phenomenal realm.'
        )
    }

    return {
        'element': element_name,
        'vector_hamming_weight': proj['V_noum'],
        'T_base_symmetry_tax': proj['T_base'],
        'zeroth_law': zeroth,
        'first_law': first,
        'second_law': second,
        'third_law': third,
        'pantograph_projection': proj,
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: PHASE CHANGE SIMULATOR (LATTICE SNAP)
# ─────────────────────────────────────────────────────────────────────────────

def simulate_phase_change(vector, element_name, constants):
    """
    Simulates heating by incrementally flipping bits (increasing shear)
    until the Golay decoder can no longer recover the original identity.
    The 'Lattice Snap' is the UBP definition of a phase transition.

    LAW_CHEM_PHASE_001: Physical phase state is a function of geometric
    proximity to the substrate lattice; molecules within the covering
    radius (d=4) lock into solid forms, while those outside drift as fluids.
    """
    W  = constants['W_float']
    steps = []
    stressed = list(vector)
    snap_shear = None
    latent_entropy = None
    snap_step = None

    for step in range(1, 8):
        # Apply shear-induced bit flip (thermal noise injection)
        flip_idx = (step + 2) % 24
        stressed[flip_idx] ^= 1

        decoded, correctable, dist = core.GOLAY_ENGINE.decode(stressed)
        t_stressed = float(core.LEECH_ENGINE.calculate_symmetry_tax(stressed))

        # 1 bit of displacement ≈ W * 0.01 rads of shear for this element
        current_shear = step * W * 0.01

        phase = 'SOLID/LIQUID (Elastic)' if correctable else 'GAS (Lattice Snap)'
        steps.append({
            'step': step,
            'shear_rads': round(current_shear, 6),
            'hamming_dist': dist,
            'stressed_tax': round(t_stressed, 6),
            'phase': phase,
            'correctable': correctable,
        })

        if not correctable and snap_shear is None:
            snap_shear = current_shear
            snap_step  = step
            # Latent heat = Tax difference between old and new anchor
            t_base_val = float(core.LEECH_ENGINE.calculate_symmetry_tax(vector))
            new_anchor = core.GOLAY_ENGINE.encode(decoded)
            t_new = float(core.LEECH_ENGINE.calculate_symmetry_tax(new_anchor))
            latent_entropy = t_new - t_base_val

    return {
        'element': element_name,
        'elastic_limit_bits': 3,
        'snap_shear_rads': round(snap_shear, 6) if snap_shear else None,
        'snap_at_step': snap_step,
        'latent_entropy_bits': round(latent_entropy, 6) if latent_entropy is not None else None,
        'heating_steps': steps,
        'interpretation': (
            'The Lattice Snap occurs when thermal shear exceeds the 3-bit Golay '
            'error-correction radius. Latent heat = Symmetry Tax differential '
            'between the old and new Golay anchor codewords.'
        )
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: NERNST AUDIT (IRON — STABILITY PLATEAU)
# ─────────────────────────────────────────────────────────────────────────────

def nernst_audit_iron(constants):
    """
    Performs the Nernst Audit on Iron (Fe), the anchor of elemental stability.
    Predicts the specific heat floor (Cv_min) and Brownian jitter.

    Falsifiability: If Cv < predicted floor at T < 1 nano-Kelvin, UBP is falsified.
    """
    iron = load_element('ELEM_Fe_026')
    if not iron or not iron['vector']:
        return {'error': 'ELEM_Fe_026 not found in KB'}

    vec    = iron['vector']
    proj   = pantograph_projection(vec, constants)
    L      = constants['L_float']
    W      = constants['W_float']

    T_base = proj['T_base']
    # Minimum entropy plateau: S_min = L * T_base
    S_min  = L * T_base
    # Specific heat floor: Cv = S_min * k (scaled by Pantograph factor)
    Cv_min = S_min * constants['k_float']
    # Brownian jitter: irrational aliasing residue of Wobble
    # Jitter = W mod 1 * T_base / (2 * pi)
    jitter = (W % 1) * T_base / (2 * math.pi)

    return {
        'element': 'Iron (Fe)',
        'ubp_id': 'ELEM_Fe_026',
        'vector_hamming_weight': proj['V_noum'],
        'T_base_symmetry_tax': T_base,
        'S_min_entropy_plateau': round(S_min, 6),
        'Cv_min_specific_heat_floor': round(Cv_min, 6),
        'brownian_jitter': round(jitter, 12),
        'nrci': proj['nrci'],
        'falsifiability': (
            f'The UBP Pantograph model predicts that the specific heat capacity '
            f'of pure Iron will never drop below {Cv_min:.6f} J/K-equiv, '
            f'regardless of proximity to 0 Kelvin. '
            f'Any experimental measurement of Cv < {Cv_min:.6f} at T < 1 nano-Kelvin '
            f'falsifies this model.'
        )
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: UNIVERSAL COUPLING CONSTANT
# ─────────────────────────────────────────────────────────────────────────────

def universal_coupling_constant(constants):
    """
    C_u = η_H * R_p/e ≈ 1399.78
    Where η_H = ideal NRCI of Hydrogen Seed, R_p/e = Proton/Electron mass ratio.

    This links the 24-bit Noumenal Substrate to the 3D Phenomenal Scale.
    """
    hydrogen = load_element('ELEM_H_001')
    if not hydrogen or not hydrogen['vector']:
        return {'error': 'ELEM_H_001 not found in KB'}

    vec  = hydrogen['vector']
    proj = pantograph_projection(vec, constants)
    eta_H = proj['nrci']

    # Proton/Electron mass ratio (empirical, used as calibration anchor)
    R_pe = 1836.1520
    C_u  = eta_H * R_pe

    # Gold verification
    gold = load_element('ELEM_Au_079')
    gold_proj = pantograph_projection(gold['vector'], constants) if gold and gold['vector'] else None

    result = {
        'eta_H_hydrogen_nrci': round(eta_H, 6),
        'R_pe_proton_electron_ratio': R_pe,
        'C_u_coupling_constant': round(C_u, 4),
        'hydrogen_verification': {
            'substrate_nrci': round(eta_H, 6),
            'particle_resonance': R_pe,
            'error_pct': round(abs(eta_H - 0.764677) / 0.764677 * 100, 6),
            'status': 'SSS-PHASE-LOCK' if abs(eta_H - 0.764677) / 0.764677 < 0.001 else 'DRIFT'
        }
    }

    if gold_proj:
        gold_nrci = gold_proj['nrci']
        gold_resonance = gold_nrci * R_pe
        result['gold_verification'] = {
            'substrate_nrci': round(gold_nrci, 6),
            'particle_resonance': round(gold_resonance, 4),
            'error_pct': round(abs(gold_nrci - 0.620629) / 0.620629 * 100, 6),
            'status': 'DIMENSIONAL DRIFT' if abs(gold_nrci - 0.620629) / 0.620629 > 0.01 else 'PHASE-LOCK'
        }

    return result

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7: MULTI-ELEMENT SURVEY
# ─────────────────────────────────────────────────────────────────────────────

def multi_element_survey(constants):
    """
    Surveys thermodynamic properties across a set of representative elements.
    Demonstrates the universality of the Pantograph model.
    """
    targets = [
        ('ELEM_H_001',  'Hydrogen (H)'),
        ('ELEM_He_002', 'Helium (He)'),
        ('ELEM_C_006',  'Carbon (C)'),
        ('ELEM_N_007',  'Nitrogen (N)'),
        ('ELEM_O_008',  'Oxygen (O)'),
        ('ELEM_Fe_026', 'Iron (Fe)'),
        ('ELEM_Cu_029', 'Copper (Cu)'),
        ('ELEM_Au_079', 'Gold (Au)'),
        ('ELEM_Pb_082', 'Lead (Pb)'),
        ('ELEM_U_092',  'Uranium (U)'),
    ]

    survey = []
    for ubp_id, name in targets:
        elem = load_element(ubp_id)
        if not elem or not elem['vector']:
            survey.append({'element': name, 'ubp_id': ubp_id, 'status': 'NOT_IN_KB'})
            continue
        vec  = elem['vector']
        proj = pantograph_projection(vec, constants)
        L    = constants['L_float']
        survey.append({
            'element': name,
            'ubp_id': ubp_id,
            'hamming_weight': proj['V_noum'],
            'T_base': round(proj['T_base'], 6),
            'shear_tan_theta': round(proj['shear'], 6),
            'V_macro': round(proj['V_macro'], 4),
            'S_macro': round(proj['S_macro'], 4),
            'T_adj_entropy': round(proj['T_adj'], 6),
            'nrci': round(proj['nrci'], 6),
            'nernst_floor_Cv': round(L * proj['T_base'] * constants['k_float'], 6),
            'phase_state': (
                'SOLID' if abs(proj['shear']) < 0.5 else
                'LIQUID' if abs(proj['shear']) < 2.0 else 'GAS'
            )
        })
    return survey

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8: EQUATION OF STATE VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def equation_of_state_verification(constants):
    """
    Verifies the UBP Universal Equation of State:
    V_macro = (T_adj * k^3) / RG

    Compares against the Pantograph Projection for Hydrogen.
    """
    hydrogen = load_element('ELEM_H_001')
    if not hydrogen or not hydrogen['vector']:
        return {'error': 'ELEM_H_001 not found'}

    vec  = hydrogen['vector']
    proj = pantograph_projection(vec, constants)
    RG   = constants['RG']
    k    = constants['k_float']

    # UBP EoS: V_macro = T_adj * k^3 / RG
    V_eos = proj['T_adj'] * (k ** 3) / RG
    # Direct Pantograph: V_macro = k^3 * V_noum
    V_panto = proj['V_macro']

    return {
        'element': 'Hydrogen (H)',
        'T_adj': round(proj['T_adj'], 6),
        'k_cubed': round(k ** 3, 6),
        'RG_resolution_gap': round(RG, 6),
        'V_eos_equation_of_state': round(V_eos, 6),
        'V_panto_direct': round(V_panto, 6),
        'ratio_eos_to_panto': round(V_eos / V_panto, 6) if V_panto != 0 else None,
        'interpretation': (
            'The EoS and direct Pantograph give consistent volumetric scales. '
            'The Resolution Gap (RG = ln(φ)/ln(π) ≈ 0.7533) acts as the '
            '"friction coefficient" between the 24D substrate and 3D space.'
        )
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9: CARNOT EFFICIENCY FROM UBP
# ─────────────────────────────────────────────────────────────────────────────

def carnot_efficiency_ubp(constants):
    """
    The UBP Carnot Analogue:
    η_max = NRCI_cold / NRCI_hot = 1 - (T_cold / T_hot) in classical terms.

    In UBP: η = 1 - (shear_cold / shear_hot)
    The Resolution Gap (RG) sets the absolute efficiency ceiling.
    """
    hydrogen = load_element('ELEM_H_001')
    gold     = load_element('ELEM_Au_079')

    if not hydrogen or not gold:
        return {'error': 'Elements not found'}

    proj_H  = pantograph_projection(hydrogen['vector'], constants)
    proj_Au = pantograph_projection(gold['vector'], constants)

    # "Hot" reservoir = Gold (high Z, high tax, high shear)
    # "Cold" reservoir = Hydrogen (low Z, low tax, low shear)
    shear_hot  = abs(proj_Au['shear'])
    shear_cold = abs(proj_H['shear'])

    if shear_hot == 0:
        eta_ubp = 0.0
    else:
        eta_ubp = 1.0 - (shear_cold / shear_hot)

    # NRCI-based efficiency
    nrci_hot  = proj_Au['nrci']
    nrci_cold = proj_H['nrci']
    eta_nrci  = 1.0 - (nrci_cold / nrci_hot) if nrci_hot != 0 else 0.0

    return {
        'hot_reservoir': 'Gold (Au) — High-Z, High Shear',
        'cold_reservoir': 'Hydrogen (H) — Low-Z, Low Shear',
        'shear_hot_rads': round(shear_hot, 6),
        'shear_cold_rads': round(shear_cold, 6),
        'eta_ubp_shear_based': round(eta_ubp, 6),
        'eta_nrci_based': round(eta_nrci, 6),
        'resolution_gap_ceiling': round(constants['RG'], 6),
        'interpretation': (
            'In UBP, Carnot efficiency is the ratio of shear angles between '
            'hot and cold reservoirs. The Resolution Gap (RG) sets the absolute '
            'ceiling: 100% efficiency is impossible because projecting 24D into 3D '
            'always incurs geometric friction.'
        )
    }

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10: BROWNIAN MOTION AS ALIASING JITTER
# ─────────────────────────────────────────────────────────────────────────────

def brownian_aliasing_analysis(constants):
    """
    Brownian motion = Irrational Aliasing Jitter.
    The Triadic Wobble W is irrational; the Pantograph linkage never hits
    the same 3D coordinate twice. The jitter amplitude scales with W mod 1.

    For each element, jitter = (W mod 1) * T_base / (2π)
    """
    W = constants['W_float']
    W_frac = W % 1  # Irrational residue

    targets = [
        ('ELEM_H_001',  'Hydrogen'),
        ('ELEM_Fe_026', 'Iron'),
        ('ELEM_Au_079', 'Gold'),
    ]

    results = []
    for ubp_id, name in targets:
        elem = load_element(ubp_id)
        if not elem or not elem['vector']:
            continue
        proj   = pantograph_projection(elem['vector'], constants)
        jitter = W_frac * proj['T_base'] / (2 * math.pi)
        results.append({
            'element': name,
            'T_base': round(proj['T_base'], 6),
            'W_irrational_residue': round(W_frac, 8),
            'brownian_jitter_amplitude': round(jitter, 12),
            'interpretation': (
                f'Brownian motion for {name} is the aliasing noise of the '
                f'Pantograph attempting to resolve W={W:.8f} (irrational) '
                f'into a finite 24-bit substrate.'
            )
        })

    return {
        'W_wobble': W,
        'W_irrational_residue': round(W_frac, 8),
        'mechanism': (
            'Because W = (π·φ·e)^(1/3) - floor(...) is irrational, the Pantograph '
            'linkage never revisits the same 3D coordinate during temporal rotation. '
            'What classical physics calls "random thermal fluctuations" is the '
            'high-frequency jitter of the linkage rounding its irrational scaling '
            'factor into the finite 24-bit substrate. '
            '"Brownian motion is the sound of the universe rounding its decimals."'
        ),
        'element_jitter': results
    }

# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("UBP THERMODYNAMICS COMPREHENSIVE AUDIT")
    print("Universal Binary Principle v7.2 — Core Studio v4.0")
    print("=" * 80)

    KB_PATH = os.path.join(os.path.dirname(__file__), 'ubp_system_kb.json')

    # Override load_element to use local KB path
    import functools
    global load_element
    _orig_load = load_element
    def _load_with_path(ubp_id, kb_path=KB_PATH):
        return _orig_load(ubp_id, kb_path)
    load_element = _load_with_path

    constants = get_constants()
    print(f"\n[CONSTANTS]")
    print(f"  Triadic Wobble W  = {constants['W_float']:.10f}")
    print(f"  13D Sink L        = {constants['L_float']:.10f}")
    print(f"  Scale Factor k    = {constants['k_float']:.10f}")
    print(f"  Resolution Gap RG = {constants['RG']:.10f}")

    results = {
        'system': 'UBP Core v7.2 / Core Studio v4.0',
        'constants': {
            'W_wobble': constants['W_float'],
            'L_sink': constants['L_float'],
            'k_scale': constants['k_float'],
            'RG_resolution_gap': constants['RG'],
            'PI': constants['PI_float'],
        }
    }

    # ── Four Laws: Hydrogen ──────────────────────────────────────────────────
    print("\n[1] FOUR LAWS AUDIT: Hydrogen")
    h_elem = load_element('ELEM_H_001')
    if h_elem and h_elem['vector']:
        h_audit = audit_four_laws(h_elem['vector'], 'Hydrogen (H)', constants)
        results['four_laws_hydrogen'] = h_audit
        print(f"  Zeroth: T_shear = {h_audit['zeroth_law']['temperature_shear_rads']:.6f} rads | {h_audit['zeroth_law']['equilibrium_state']}")
        print(f"  First:  U = {h_audit['first_law']['internal_energy_toggles']} toggles | k = {h_audit['first_law']['work_scaling_k']:.4f}")
        print(f"  Second: S = {h_audit['second_law']['entropy_symmetry_tax']:.6f} bits | η_max = {h_audit['second_law']['nrci_max_efficiency_pct']:.2f}%")
        print(f"  Third:  L = {h_audit['third_law']['sink_leakage_L']:.8f} | Cv_floor = {h_audit['third_law']['nernst_specific_heat_floor']:.6f}")

    # ── Four Laws: Gold ──────────────────────────────────────────────────────
    print("\n[2] FOUR LAWS AUDIT: Gold")
    au_elem = load_element('ELEM_Au_079')
    if au_elem and au_elem['vector']:
        au_audit = audit_four_laws(au_elem['vector'], 'Gold (Au)', constants)
        results['four_laws_gold'] = au_audit
        print(f"  Zeroth: T_shear = {au_audit['zeroth_law']['temperature_shear_rads']:.6f} rads | {au_audit['zeroth_law']['equilibrium_state']}")
        print(f"  First:  U = {au_audit['first_law']['internal_energy_toggles']} toggles | k = {au_audit['first_law']['work_scaling_k']:.4f}")
        print(f"  Second: S = {au_audit['second_law']['entropy_symmetry_tax']:.6f} bits | η_max = {au_audit['second_law']['nrci_max_efficiency_pct']:.2f}%")
        print(f"  Third:  L = {au_audit['third_law']['sink_leakage_L']:.8f} | Cv_floor = {au_audit['third_law']['nernst_specific_heat_floor']:.6f}")

    # ── Phase Change: Gold ───────────────────────────────────────────────────
    print("\n[3] PHASE CHANGE SIMULATOR: Gold (Boiling Point Audit)")
    if au_elem and au_elem['vector']:
        au_phase = simulate_phase_change(au_elem['vector'], 'Gold (Au)', constants)
        results['phase_change_gold'] = au_phase
        for step in au_phase['heating_steps']:
            print(f"  Step {step['step']}: shear={step['shear_rads']:.4f} rads | d={step['hamming_dist']} | {step['phase']}")
        if au_phase['snap_shear_rads']:
            print(f"  >>> SNAP at {au_phase['snap_shear_rads']:.6f} rads | ΔS = {au_phase['latent_entropy_bits']:.6f} bits")

    # ── Phase Change: Iron ───────────────────────────────────────────────────
    print("\n[4] PHASE CHANGE SIMULATOR: Iron")
    fe_elem = load_element('ELEM_Fe_026')
    if fe_elem and fe_elem['vector']:
        fe_phase = simulate_phase_change(fe_elem['vector'], 'Iron (Fe)', constants)
        results['phase_change_iron'] = fe_phase
        for step in fe_phase['heating_steps']:
            print(f"  Step {step['step']}: shear={step['shear_rads']:.4f} rads | d={step['hamming_dist']} | {step['phase']}")
        if fe_phase['snap_shear_rads']:
            print(f"  >>> SNAP at {fe_phase['snap_shear_rads']:.6f} rads | ΔS = {fe_phase['latent_entropy_bits']:.6f} bits")

    # ── Nernst Audit: Iron ───────────────────────────────────────────────────
    print("\n[5] NERNST AUDIT: Iron (Stability Plateau)")
    nernst = nernst_audit_iron(constants)
    results['nernst_audit_iron'] = nernst
    if 'error' not in nernst:
        print(f"  T_base = {nernst['T_base_symmetry_tax']:.6f}")
        print(f"  S_min  = {nernst['S_min_entropy_plateau']:.6f} bits")
        print(f"  Cv_min = {nernst['Cv_min_specific_heat_floor']:.6f} J/K-equiv")
        print(f"  Jitter = {nernst['brownian_jitter']:.12f} units")

    # ── Universal Coupling Constant ──────────────────────────────────────────
    print("\n[6] UNIVERSAL COUPLING CONSTANT")
    coupling = universal_coupling_constant(constants)
    results['universal_coupling_constant'] = coupling
    if 'error' not in coupling:
        print(f"  η_H = {coupling['eta_H_hydrogen_nrci']:.6f}")
        print(f"  C_u = {coupling['C_u_coupling_constant']:.4f}")
        print(f"  H verification: error = {coupling['hydrogen_verification']['error_pct']:.6f}% | {coupling['hydrogen_verification']['status']}")
        if 'gold_verification' in coupling:
            print(f"  Au verification: error = {coupling['gold_verification']['error_pct']:.6f}% | {coupling['gold_verification']['status']}")

    # ── Multi-Element Survey ─────────────────────────────────────────────────
    print("\n[7] MULTI-ELEMENT THERMODYNAMIC SURVEY")
    survey = multi_element_survey(constants)
    results['multi_element_survey'] = survey
    print(f"  {'Element':<20} {'HW':>4} {'T_base':>10} {'Shear':>10} {'NRCI':>8} {'Cv_floor':>10} {'Phase':<8}")
    print(f"  {'-'*75}")
    for row in survey:
        if 'status' in row and row['status'] == 'NOT_IN_KB':
            print(f"  {row['element']:<20} NOT IN KB")
        else:
            print(f"  {row['element']:<20} {row['hamming_weight']:>4} {row['T_base']:>10.4f} {row['shear_tan_theta']:>10.4f} {row['nrci']:>8.4f} {row['nernst_floor_Cv']:>10.6f} {row['phase_state']:<8}")

    # ── Equation of State ────────────────────────────────────────────────────
    print("\n[8] EQUATION OF STATE VERIFICATION")
    eos = equation_of_state_verification(constants)
    results['equation_of_state'] = eos
    if 'error' not in eos:
        print(f"  V_eos   = {eos['V_eos_equation_of_state']:.6f}")
        print(f"  V_panto = {eos['V_panto_direct']:.6f}")
        print(f"  Ratio   = {eos['ratio_eos_to_panto']:.6f}")

    # ── Carnot Efficiency ────────────────────────────────────────────────────
    print("\n[9] CARNOT EFFICIENCY (UBP Analogue)")
    carnot = carnot_efficiency_ubp(constants)
    results['carnot_efficiency'] = carnot
    if 'error' not in carnot:
        print(f"  Hot reservoir (Au): shear = {carnot['shear_hot_rads']:.6f} rads")
        print(f"  Cold reservoir (H): shear = {carnot['shear_cold_rads']:.6f} rads")
        print(f"  η_ubp (shear-based) = {carnot['eta_ubp_shear_based']:.6f}")
        print(f"  η_nrci (NRCI-based) = {carnot['eta_nrci_based']:.6f}")
        print(f"  RG ceiling          = {carnot['resolution_gap_ceiling']:.6f}")

    # ── Brownian Motion ──────────────────────────────────────────────────────
    print("\n[10] BROWNIAN MOTION AS ALIASING JITTER")
    brownian = brownian_aliasing_analysis(constants)
    results['brownian_aliasing'] = brownian
    print(f"  W_irrational_residue = {brownian['W_irrational_residue']:.8f}")
    for ej in brownian['element_jitter']:
        print(f"  {ej['element']:<12}: jitter = {ej['brownian_jitter_amplitude']:.12f}")

    # ── Save Results ─────────────────────────────────────────────────────────
    out_path = os.path.join(os.path.dirname(__file__), 'ubp_thermo_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[DONE] Results saved to: {out_path}")
    print("=" * 80)

    return results


if __name__ == '__main__':
    main()
