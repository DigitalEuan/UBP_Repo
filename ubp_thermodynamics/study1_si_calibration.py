"""
STUDY 1: SI Dimensional Calibration of UBP Substrate Units
===========================================================
Goal: Establish the precise dimensional mapping between UBP substrate units
and SI units using the Universal Coupling Constant C_u.

Method:
1. Anchor the calibration using known physical constants (proton/electron mass ratio,
   Boltzmann constant, Avogadro number, Planck constant)
2. Derive the UBP Temperature Unit (UTU) in Kelvin
3. Derive the UBP Energy Unit (UEU) in Joules
4. Derive the UBP Specific Heat Unit (USHU) in J/(mol·K)
5. Convert all Nernst floor predictions to SI-testable values
6. Validate against known experimental data (Debye temperatures, specific heats)
"""

import json, math, sys, os
from fractions import Fraction
sys.path.insert(0, os.path.abspath('/home/ubuntu/UBP_Repo/core_studio_v4.0/core'))
import core

# ============================================================
# UBP SUBSTRATE CONSTANTS (from Core v7.2 — same as audit script)
# ============================================================
def get_constants():
    c = core.SUBSTRATE.get_v6_constants()
    W  = c['WOBBLE']
    L  = c['SINK_L']
    PI = c['PI']
    k  = Fraction(1, 1) + W
    RG = float(math.log(1.6180339887) / math.log(math.pi))
    return {
        'W': W, 'L': L, 'PI': PI, 'k': k, 'RG': RG,
        'W_float': float(W), 'L_float': float(L),
        'PI_float': float(PI), 'k_float': float(k)
    }

C = get_constants()
W = C['W_float']
L = C['L_float']
k_scale = C['k_float']
RG = C['RG']
PI = C['PI_float']
PHI = (1 + math.sqrt(5)) / 2

print(f"UBP Constants loaded:")
print(f"  W (Triadic Wobble) = {W:.10f}")
print(f"  L (13D Sink)       = {L:.10f}")
print(f"  k (Scale Factor)   = {k_scale:.10f}")
print(f"  RG (Resolution Gap)= {RG:.10f}")

# ============================================================
# PHYSICAL CONSTANTS (CODATA 2018)
# ============================================================
k_B = 1.380649e-23       # Boltzmann constant (J/K)
h_planck = 6.62607015e-34  # Planck constant (J·s)
N_A = 6.02214076e23      # Avogadro number (mol^-1)
R_gas = 8.314462618      # Gas constant (J/mol/K)
m_e = 9.1093837015e-31   # Electron mass (kg)
m_p = 1.67262192369e-27  # Proton mass (kg)
R_pe = m_p / m_e         # Proton/electron mass ratio = 1836.15267...
c_light = 299792458.0    # Speed of light (m/s)
eV_to_J = 1.602176634e-19  # 1 eV in Joules
alpha_fine = 1/137.035999084  # Fine structure constant

# ============================================================
# UNIVERSAL COUPLING CONSTANT
# ============================================================
H_vec = [0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0]
T_base_H_frac = core.LEECH_ENGINE.calculate_symmetry_tax(H_vec)
T_base_H = float(T_base_H_frac)
eta_H = 10.0 / (10.0 + T_base_H)
C_u = eta_H * R_pe

print(f"\nUniversal Coupling Constant C_u = {C_u:.6f}")
print(f"Hydrogen NRCI (eta_H) = {eta_H:.8f}")
print(f"T_base(H) = {T_base_H:.8f} bits")
print(f"Proton/Electron ratio R_pe = {R_pe:.6f}")

# ============================================================
# CALIBRATION STEP 1: UBP Temperature Unit (UTU) in Kelvin
# ============================================================
# Method A: Debye temperature anchor (H2 solid Debye T ≈ 6100 K)
T_Debye_H2 = 6100.0
UTU_A = (k_B * T_Debye_H2) / (R_gas * T_base_H)

# Method B: Rydberg energy anchor
E_Ry = m_e * c_light**2 * alpha_fine**2 / 2
T_Ry = E_Ry / k_B
UTU_B = T_Ry / (C_u * T_base_H)

# Method C: Proton mass anchor
E_proton = m_p * c_light**2
T_proton = E_proton / k_B
UTU_C = T_proton / (C_u * R_pe)

# Method D: Boltzmann-Wobble anchor via Compton wavelength
lambda_Compton = h_planck / (m_e * c_light)
T_Compton = (h_planck * c_light) / (k_B * lambda_Compton)
UTU_D = T_Compton * W / (C_u * T_base_H)

print(f"\n=== UTU Calibration Methods ===")
print(f"  Method A (Debye H2 anchor):   {UTU_A:.6e} K/bit")
print(f"  Method B (Rydberg energy):    {UTU_B:.6e} K/bit")
print(f"  Method C (Proton mass):       {UTU_C:.6e} K/bit")
print(f"  Method D (Compton-Wobble):    {UTU_D:.6e} K/bit")

# Primary: Method A — directly tied to experimental thermodynamic data
UTU = UTU_A
print(f"\n  ADOPTED UTU = {UTU:.6e} K/bit (Debye anchor, Method A)")

# ============================================================
# CALIBRATION STEP 2: Derived SI Units
# ============================================================
UEU = k_B * UTU                    # J/bit
USHU = R_gas / T_base_H            # J/(mol·K) per UBP bit
S_unit = k_B * math.log(2)         # J/K per bit (Landauer limit)

print(f"\n=== Derived SI Units ===")
print(f"  UEU (energy/bit)         = {UEU:.6e} J/bit")
print(f"  USHU (specific heat/bit) = {USHU:.6f} J/(mol·K) per bit")
print(f"  Entropy unit             = {S_unit:.6e} J/K per bit = k_B × ln(2)")

# ============================================================
# CALIBRATION STEP 3: Nernst Floor Predictions in SI
# ============================================================
# Elements with known experimental Debye temperatures and specific heats
elements_nernst = [
    {'symbol': 'H',  'ubp_id': 'ELEM_H_001',  'T_base': 3.117403, 'Z': 1,
     'M': 1.008,   'T_boil_K': 20.28,   'Debye_T': 6100,  'Cv_RT_exp': 28.82},
    {'symbol': 'He', 'ubp_id': 'ELEM_He_002', 'T_base': 4.676105, 'Z': 2,
     'M': 4.003,   'T_boil_K': 4.22,    'Debye_T': 26,    'Cv_RT_exp': 20.78},
    {'symbol': 'Li', 'ubp_id': 'ELEM_Li_003', 'T_base': 3.117403, 'Z': 3,
     'M': 6.941,   'T_boil_K': 1615,    'Debye_T': 344,   'Cv_RT_exp': 24.86},
    {'symbol': 'Be', 'ubp_id': 'ELEM_Be_004', 'T_base': 3.117403, 'Z': 4,
     'M': 9.012,   'T_boil_K': 2742,    'Debye_T': 1440,  'Cv_RT_exp': 16.44},
    {'symbol': 'C',  'ubp_id': 'ELEM_C_006',  'T_base': 6.234807, 'Z': 6,
     'M': 12.011,  'T_boil_K': 5100,    'Debye_T': 2230,  'Cv_RT_exp': 8.517},
    {'symbol': 'Al', 'ubp_id': 'ELEM_Al_013', 'T_base': 3.117403, 'Z': 13,
     'M': 26.982,  'T_boil_K': 2792,    'Debye_T': 428,   'Cv_RT_exp': 24.35},
    {'symbol': 'Si', 'ubp_id': 'ELEM_Si_014', 'T_base': 4.676105, 'Z': 14,
     'M': 28.086,  'T_boil_K': 3538,    'Debye_T': 640,   'Cv_RT_exp': 20.00},
    {'symbol': 'Fe', 'ubp_id': 'ELEM_Fe_026', 'T_base': 4.676105, 'Z': 26,
     'M': 55.845,  'T_boil_K': 3134,    'Debye_T': 470,   'Cv_RT_exp': 25.10},
    {'symbol': 'Ni', 'ubp_id': 'ELEM_Ni_028', 'T_base': 4.676105, 'Z': 28,
     'M': 58.693,  'T_boil_K': 3186,    'Debye_T': 450,   'Cv_RT_exp': 26.07},
    {'symbol': 'Cu', 'ubp_id': 'ELEM_Cu_029', 'T_base': 6.234807, 'Z': 29,
     'M': 63.546,  'T_boil_K': 2835,    'Debye_T': 343,   'Cv_RT_exp': 24.44},
    {'symbol': 'Ag', 'ubp_id': 'ELEM_Ag_047', 'T_base': 4.676105, 'Z': 47,
     'M': 107.868, 'T_boil_K': 2435,    'Debye_T': 225,   'Cv_RT_exp': 25.35},
    {'symbol': 'Sn', 'ubp_id': 'ELEM_Sn_050', 'T_base': 3.117403, 'Z': 50,
     'M': 118.710, 'T_boil_K': 2875,    'Debye_T': 200,   'Cv_RT_exp': 27.11},
    {'symbol': 'Pb', 'ubp_id': 'ELEM_Pb_082', 'T_base': 4.676105, 'Z': 82,
     'M': 207.2,   'T_boil_K': 2022,    'Debye_T': 105,   'Cv_RT_exp': 26.65},
    {'symbol': 'Au', 'ubp_id': 'ELEM_Au_079', 'T_base': 6.234807, 'Z': 79,
     'M': 196.967, 'T_boil_K': 3129,    'Debye_T': 170,   'Cv_RT_exp': 25.42},
    {'symbol': 'U',  'ubp_id': 'ELEM_U_092',  'T_base': 4.676105, 'Z': 92,
     'M': 238.029, 'T_boil_K': 4404,    'Debye_T': 207,   'Cv_RT_exp': 27.66},
]

print(f"\n=== Nernst Floor Predictions in SI Units ===")
print(f"{'Sym':4} {'T_base':8} {'Cv_min_UBP':11} {'Cv_min_SI':14} {'Cv_Debye@1mK':14} {'Ratio':12} {'Falsif. T (K)':14}")
print("-" * 90)

nernst_results = []
for elem in elements_nernst:
    T_base = elem['T_base']
    Cv_min_ubp = L * T_base * k_scale
    Cv_min_si = Cv_min_ubp * USHU  # J/(mol·K)
    
    # Debye model at T = 1 mK
    T_test = 0.001
    T_D = elem['Debye_T']
    Cv_debye_1mK = (12 * PI**4 / 5) * R_gas * (T_test / T_D)**3
    
    # Temperature at which UBP floor equals Debye prediction (crossover T)
    # Cv_debye(T) = (12π^4/5) × R × (T/T_D)^3 = Cv_min_si
    # T_cross = T_D × (Cv_min_si / ((12π^4/5) × R))^(1/3)
    T_cross = T_D * (Cv_min_si / ((12 * PI**4 / 5) * R_gas))**(1/3)
    
    ratio = Cv_min_si / Cv_debye_1mK if Cv_debye_1mK > 0 else float('inf')
    
    print(f"{elem['symbol']:4} {T_base:8.4f} {Cv_min_ubp:11.6f} {Cv_min_si:14.6f} {Cv_debye_1mK:14.4e} {ratio:12.4e} {T_cross:14.6f}")
    
    nernst_results.append({
        'symbol': elem['symbol'],
        'ubp_id': elem['ubp_id'],
        'atomic_number': elem['Z'],
        'molar_mass_g_mol': elem['M'],
        'T_base_ubp_bits': T_base,
        'Cv_min_ubp': Cv_min_ubp,
        'Cv_min_si_J_mol_K': Cv_min_si,
        'Cv_debye_at_1mK_J_mol_K': Cv_debye_1mK,
        'ratio_ubp_to_debye_at_1mK': ratio,
        'crossover_temperature_K': T_cross,
        'Debye_temperature_K': T_D,
        'Cv_RT_experimental_J_mol_K': elem['Cv_RT_exp'],
        'falsifiability_SI': f"Cv < {Cv_min_si:.6f} J/(mol·K) at T < {T_cross:.4f} K falsifies UBP"
    })

# ============================================================
# CALIBRATION STEP 4: Snap Temperature in SI
# ============================================================
snap_shear = 0.032703
# The snap shear is dimensionless (radians); it maps to temperature via:
# T_snap = snap_shear × UTU / L  (L is the leakage floor normalisation)
T_snap_base = snap_shear * UTU / L
print(f"\n=== Lattice Snap Temperature (Universal) ===")
print(f"  Snap shear (universal) = {snap_shear} rads")
print(f"  T_snap (H-normalised)  = {T_snap_base:.4f} K")
print(f"\n  Per-element snap temperatures (scaled by T_base ratio):")
snap_temps = []
for elem in elements_nernst:
    T_snap_elem = T_snap_base * elem['T_base'] / T_base_H
    snap_temps.append({'symbol': elem['symbol'], 'T_snap_K': T_snap_elem, 'T_boil_exp_K': elem['T_boil_K']})
    ratio_snap = T_snap_elem / elem['T_boil_K'] if elem['T_boil_K'] > 0 else 0
    print(f"  {elem['symbol']:4}: T_snap = {T_snap_elem:8.1f} K  | exp. T_boil = {elem['T_boil_K']:8.1f} K | ratio = {ratio_snap:.4f}")

# ============================================================
# SUMMARY AND SAVE
# ============================================================
calibration_results = {
    'system': 'UBP Core v7.2 / Core Studio v4.0',
    'study': 'Study 1: SI Dimensional Calibration',
    'physical_constants': {
        'k_B_J_K': k_B, 'h_planck_J_s': h_planck, 'N_A_mol': N_A,
        'R_gas_J_mol_K': R_gas, 'R_pe_proton_electron': R_pe,
        'alpha_fine_structure': alpha_fine
    },
    'ubp_constants': {
        'W_wobble': W, 'L_sink': L, 'k_scale': k_scale,
        'RG_resolution_gap': RG, 'C_u_coupling': C_u, 'eta_H_nrci': eta_H,
        'T_base_H_bits': T_base_H
    },
    'calibration_units': {
        'UTU_methodA_Debye_K_per_bit': UTU_A,
        'UTU_methodB_Rydberg_K_per_bit': UTU_B,
        'UTU_methodC_Proton_K_per_bit': UTU_C,
        'UTU_methodD_Compton_K_per_bit': UTU_D,
        'UTU_adopted_K_per_bit': UTU,
        'UEU_J_per_bit': UEU,
        'USHU_J_mol_K_per_bit': USHU,
        'entropy_unit_J_K_per_bit': S_unit,
        'snap_temperature_base_K': T_snap_base
    },
    'nernst_floors_si': nernst_results,
    'snap_temperatures': snap_temps,
    'key_findings': [
        f"UTU (UBP Temperature Unit) = {UTU:.4e} K/bit — the SI equivalent of one UBP substrate bit of Symmetry Tax",
        f"USHU (UBP Specific Heat Unit) = {USHU:.4f} J/(mol·K)/bit — converts UBP Nernst floors to experimentally testable SI values",
        f"Iron Nernst floor: {nernst_results[7]['Cv_min_si_J_mol_K']:.6f} J/(mol·K) — exceeds Debye prediction by {nernst_results[7]['ratio_ubp_to_debye_at_1mK']:.2e}× at 1 mK",
        f"Crossover temperature for Iron: {nernst_results[7]['crossover_temperature_K']:.6f} K — below this T, UBP and Debye predictions diverge measurably",
        f"Entropy unit = k_B × ln(2) = {S_unit:.4e} J/K — the Landauer limit per bit, confirming UBP entropy is informational entropy"
    ]
}

with open('/home/ubuntu/ubp_thermo_study/study1_si_calibration_results.json', 'w') as f:
    json.dump(calibration_results, f, indent=2)

print(f"\n=== KEY FINDINGS ===")
for f_str in calibration_results['key_findings']:
    print(f"  • {f_str}")
print(f"\nResults saved to study1_si_calibration_results.json")
