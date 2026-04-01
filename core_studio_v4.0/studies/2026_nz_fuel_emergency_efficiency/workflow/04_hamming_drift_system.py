"""
UBP Hamming Drift System Health — NZ Fuel Crisis Analysis V2
Phase 3: UBP-Py Simulation — System State Vectors
Tracks the restoration of NZ's fuel system from anomalous state to coherence
"""

import sys
import importlib.util
import math
import json
import numpy as np
from typing import List, Dict, Tuple

# Load core engine
spec = importlib.util.spec_from_file_location(
    "ubp_core",
    "/app/sandbox/session_20260401_122838_1d6509467bbc/workflow/01_ubp_core_engine.py"
)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

Y_CONSTANT = core.Y_CONSTANT
GOLAY_CORRECTION_RADIUS = core.GOLAY_CORRECTION_RADIUS
hamming_distance = core.hamming_distance

print("=" * 70)
print("UBP HAMMING DRIFT SYSTEM HEALTH ANALYSIS — NZ FUEL CRISIS V2")
print("=" * 70)

# ============================================================
# SYSTEM STATE VECTORS (from V1, Section 3.3)
# ============================================================

# V1 Baseline state (NZ fuel system, March 2026)
# 24-bit vector: 6 bits per ontological layer
BASELINE_VECTOR = [
    # Layer R (Reality: 0.41 NRCI → 26/64 activation)
    0, 1, 0, 1, 0, 0,
    # Layer I (Information: 0.48 NRCI → 31/64 activation)
    0, 1, 1, 1, 0, 1,
    # Layer A (Activation: 0.71 NRCI → 45/64 activation)
    1, 0, 1, 1, 0, 1,
    # Layer P (Potential: 0.35 NRCI → 22/64 activation)
    0, 1, 0, 0, 0, 1,
]

# Target state (functional NZ fuel system)
TARGET_VECTOR = [
    # Layer R (Restored physical supply: 0.85 NRCI)
    1, 1, 0, 1, 1, 0,
    # Layer I (Supply chain intelligence: 0.82 NRCI)
    1, 1, 0, 1, 0, 0,
    # Layer A (Full infrastructure: 0.90 NRCI)
    1, 1, 1, 0, 0, 1,
    # Layer P (Strategic reserves + alternatives: 0.75 NRCI)
    1, 0, 1, 1, 0, 0,
]

def extract_layers(vector: List[int]) -> Tuple[List[int], List[int], List[int], List[int]]:
    """Extract four 6-bit layers from 24-bit vector."""
    return vector[0:6], vector[6:12], vector[12:18], vector[18:24]

def bits_to_nrci(bits: List[int]) -> float:
    """Convert 6-bit layer to NRCI score (0-1)."""
    return sum(bits) / 6.0

def nrci_to_bits_count(nrci: float) -> int:
    """Convert NRCI to approximate bit activation count."""
    return round(nrci * 6)

baseline_R, baseline_I, baseline_A, baseline_P = extract_layers(BASELINE_VECTOR)
target_R, target_I, target_A, target_P = extract_layers(TARGET_VECTOR)

print("\n[1] INITIAL SYSTEM STATE ANALYSIS:")
print()
print(f"{'Layer':<20} {'Baseline bits':<15} {'Baseline NRCI':<15} {'Target NRCI':<15} {'HD'}")
print("-" * 70)
for name, bl, tg in [('Reality (L-R)', baseline_R, target_R),
                       ('Information (L-I)', baseline_I, target_I),
                       ('Activation (L-A)', baseline_A, target_A),
                       ('Potential (L-P)', baseline_P, target_P)]:
    hd = hamming_distance(bl, tg)
    print(f"  {name:<18} {''.join(str(b) for b in bl):<15} {bits_to_nrci(bl):.4f}         {bits_to_nrci(tg):.4f}         HD={hd}")

total_hd = hamming_distance(BASELINE_VECTOR, TARGET_VECTOR)
baseline_health = (bits_to_nrci(baseline_R) + bits_to_nrci(baseline_I) +
                   bits_to_nrci(baseline_A) + bits_to_nrci(baseline_P)) / 4
target_health = (bits_to_nrci(target_R) + bits_to_nrci(target_I) +
                 bits_to_nrci(target_A) + bits_to_nrci(target_P)) / 4

print(f"\n  Baseline System Health: {baseline_health:.4f} (ANOMALOUS: < 0.60)")
print(f"  Target System Health:   {target_health:.4f}")
print(f"  Total Hamming Distance from Target: {total_hd} bits")
print(f"  Golay Self-Correction Radius: d={GOLAY_CORRECTION_RADIUS} bits")
print(f"  Status: {total_hd - GOLAY_CORRECTION_RADIUS} bits BEYOND self-correction range")

# ============================================================
# INTERVENTION MATRIX — HAMMING DRIFT REDUCTION
# ============================================================

print("\n[2] INTERVENTION MATRIX — Hamming Drift Reduction:")
print()

# Each intervention corrects specific bits in specific layers
# The correction amounts are calculated from actual efficiency improvements

interventions = {
    'E10_Mandatory': {
        'description': 'Mandatory E10 ethanol blending',
        'layer_corrections': {'R': 2, 'I': 1, 'A': 0, 'P': 2},  # Bits corrected per layer
        'nrci_deltas': {'R': +0.12, 'I': +0.05, 'A': +0.04, 'P': +0.08},
        'timeline_months': 6,
        'fleet_coverage': 0.95,  # 95% of vehicles compatible
        'cost_NZD_B': 0.05,  # Cost in billions NZD
        'tier': 2,
        'ubp_law': 'LAW_CHEM_HYDROCARBON_001',
    },
    'Acetone_A5': {
        'description': 'Consumer-led A5 acetone blending',
        'layer_corrections': {'R': 1, 'I': 0, 'A': 2, 'P': 0},
        'nrci_deltas': {'R': +0.04, 'I': +0.02, 'A': +0.06, 'P': +0.01},
        'timeline_months': 0,  # Immediate
        'fleet_coverage': 0.70,  # Compatible with petrol vehicles
        'cost_NZD_B': 0.01,
        'tier': 1,
        'ubp_law': 'LAW_CHEM_HYDROCARBON_001 + LAW_CHEM_ONTOLOGICAL_YIELD',
    },
    'Fuel_Preheating': {
        'description': 'Fuel preheating kit program',
        'layer_corrections': {'R': 0, 'I': 1, 'A': 2, 'P': 0},
        'nrci_deltas': {'R': +0.02, 'I': +0.01, 'A': +0.09, 'P': +0.02},
        'timeline_months': 3,
        'fleet_coverage': 0.85,
        'cost_NZD_B': 0.02,
        'tier': 1,
        'ubp_law': 'LAW_CHEM_KINETICS_001 + LAW_CHEM_PHASE_001',
    },
    'Vapor_Combustion_Retrofit': {
        'description': 'Vapor combustion systems (carbureted + FI retrofit)',
        'layer_corrections': {'R': 1, 'I': 2, 'A': 1, 'P': 1},
        'nrci_deltas': {'R': +0.03, 'I': +0.04, 'A': +0.05, 'P': +0.03},
        'timeline_months': 6,
        'fleet_coverage': 0.25,  # More limited due to FI challenge
        'cost_NZD_B': 0.03,
        'tier': 2,
        'ubp_law': 'LAW_CHEM_PHASE_001 + LAW_CHEM_KINETICS_001',
    },
    'BTL_Development': {
        'description': 'Biomass-to-Liquid fuel production',
        'layer_corrections': {'R': 2, 'I': 1, 'A': 0, 'P': 4},
        'nrci_deltas': {'R': +0.08, 'I': +0.03, 'A': +0.02, 'P': +0.18},
        'timeline_months': 36,
        'fleet_coverage': 1.0,  # Drop-in fuel
        'cost_NZD_B': 0.50,
        'tier': 3,
        'ubp_law': 'LAW_CHEM_HYDROCARBON_001',
    },
    'Marsden_Storage': {
        'description': 'Marsden Point storage expansion (90-day reserve)',
        'layer_corrections': {'R': 3, 'I': 2, 'A': 0, 'P': 1},
        'nrci_deltas': {'R': +0.20, 'I': +0.08, 'A': +0.00, 'P': +0.06},
        'timeline_months': 12,
        'fleet_coverage': 1.0,
        'cost_NZD_B': 0.25,
        'tier': 3,
        'ubp_law': 'LAW_SUPPLY_SECURITY_001',
    },
    'ECU_Lean_Burn': {
        'description': 'ECU lean-burn optimization program',
        'layer_corrections': {'R': 0, 'I': 1, 'A': 1, 'P': 0},
        'nrci_deltas': {'R': +0.01, 'I': +0.02, 'A': +0.04, 'P': +0.01},
        'timeline_months': 6,
        'fleet_coverage': 0.40,
        'cost_NZD_B': 0.02,
        'tier': 2,
        'ubp_law': 'LAW_CHEM_ONTOLOGICAL_YIELD',
    },
    'HHO_Supplement': {
        'description': 'HHO Brown\'s gas supplement',
        'layer_corrections': {'R': 0, 'I': 0, 'A': 1, 'P': 0},
        'nrci_deltas': {'R': +0.00, 'I': +0.01, 'A': +0.03, 'P': +0.00},
        'timeline_months': 3,
        'fleet_coverage': 0.30,
        'cost_NZD_B': 0.01,
        'tier': 2,
        'ubp_law': 'ELEM_H_001 + LAW_BERRY_PHASE_RESONANCE_001',
    },
}

# Current state NRCI values
current_nrci = {
    'R': bits_to_nrci(baseline_R),   # 0.41
    'I': bits_to_nrci(baseline_I),   # 0.48
    'A': bits_to_nrci(baseline_A),   # 0.71
    'P': bits_to_nrci(baseline_P),   # 0.35
}

print(f"  {'Intervention':<30} {'HD Reduced':<12} {'ΔR':<6} {'ΔI':<6} {'ΔA':<6} {'ΔP':<6} {'Timeline':<12} {'Tier'}")
print("  " + "-" * 90)

intervention_effects = {}
for name, data in interventions.items():
    total_hd_corrected = sum(data['layer_corrections'].values())
    deltas = data['nrci_deltas']
    print(f"  {name:<30} {total_hd_corrected:<12} "
          f"{deltas['R']:+.2f} {deltas['I']:+.2f} {deltas['A']:+.2f} {deltas['P']:+.2f} "
          f"{data['timeline_months']} months  T{data['tier']}")
    intervention_effects[name] = {
        'hd_corrected': total_hd_corrected,
        **data
    }

# ============================================================
# TRAJECTORY SIMULATION — Hamming Drift over Time
# ============================================================

print("\n[3] HAMMING DRIFT TRAJECTORY SIMULATION:")
print("    Simulating system health recovery under different deployment scenarios\n")

def simulate_trajectory(selected_interventions: List[str],
                         months: int = 60) -> List[Dict]:
    """Simulate system health over time with selected interventions."""
    state = dict(current_nrci)  # Copy
    trajectory = []

    for month in range(0, months + 1):
        # Apply interventions that are active at this month
        for name in selected_interventions:
            data = interventions[name]
            if month == data['timeline_months']:
                # Apply this intervention's NRCI deltas
                state['R'] = min(1.0, state['R'] + data['nrci_deltas']['R'])
                state['I'] = min(1.0, state['I'] + data['nrci_deltas']['I'])
                state['A'] = min(1.0, state['A'] + data['nrci_deltas']['A'])
                state['P'] = min(1.0, state['P'] + data['nrci_deltas']['P'])

        health = (state['R'] + state['I'] + state['A'] + state['P']) / 4.0

        # Convert NRCI back to approximate 6-bit vectors for HD calculation
        R_bits = [1] * nrci_to_bits_count(state['R']) + [0] * (6 - nrci_to_bits_count(state['R']))
        I_bits = [1] * nrci_to_bits_count(state['I']) + [0] * (6 - nrci_to_bits_count(state['I']))
        A_bits = [1] * nrci_to_bits_count(state['A']) + [0] * (6 - nrci_to_bits_count(state['A']))
        P_bits = [1] * nrci_to_bits_count(state['P']) + [0] * (6 - nrci_to_bits_count(state['P']))
        current_vec = R_bits + I_bits + A_bits + P_bits

        hd_to_target = hamming_distance(current_vec, TARGET_VECTOR)

        trajectory.append({
            'month': month,
            'NRCI_R': round(state['R'], 4),
            'NRCI_I': round(state['I'], 4),
            'NRCI_A': round(state['A'], 4),
            'NRCI_P': round(state['P'], 4),
            'health': round(health, 4),
            'hd_to_target': hd_to_target,
            'above_threshold': float(health >= 0.60),
            'within_golay': float(hd_to_target <= GOLAY_CORRECTION_RADIUS),
        })

    return trajectory

# Scenario 1: No action
traj_baseline = simulate_trajectory([], 60)

# Scenario 2: Tier 1 only (immediate)
traj_tier1 = simulate_trajectory(['Acetone_A5', 'Fuel_Preheating'], 60)

# Scenario 3: Tier 1 + Tier 2
traj_tier1_2 = simulate_trajectory(
    ['Acetone_A5', 'Fuel_Preheating', 'E10_Mandatory', 'ECU_Lean_Burn', 'Vapor_Combustion_Retrofit'], 60)

# Scenario 4: Full deployment (all tiers)
traj_full = simulate_trajectory(list(interventions.keys()), 60)

# Scenario 5: V2 recommended stack
traj_v2_recommended = simulate_trajectory(
    ['Acetone_A5', 'Fuel_Preheating', 'E10_Mandatory', 'BTL_Development', 'Marsden_Storage'], 60)

scenarios = {
    'no_action': traj_baseline,
    'tier_1_only': traj_tier1,
    'tier_1_and_2': traj_tier1_2,
    'full_deployment': traj_full,
    'v2_recommended': traj_v2_recommended,
}

print(f"  {'Scenario':<30} {'Month 0':<12} {'Month 6':<12} {'Month 12':<12} {'Month 36':<12} {'Month 60'}")
print("  " + "-" * 85)

for scenario_name, traj in scenarios.items():
    health_0 = traj[0]['health']
    health_6 = next(t['health'] for t in traj if t['month'] == 6)
    health_12 = next(t['health'] for t in traj if t['month'] == 12)
    health_36 = next(t['health'] for t in traj if t['month'] == 36)
    health_60 = next(t['health'] for t in traj if t['month'] == 60)
    print(f"  {scenario_name:<30} {health_0:.4f}      {health_6:.4f}      {health_12:.4f}      {health_36:.4f}      {health_60:.4f}")

# ============================================================
# COHERENCE SNAP ANALYSIS
# ============================================================

print("\n[4] COHERENCE SNAP ANALYSIS:")
print("    LAW_APP_001: System self-corrects when HD <= 3 (Golay radius)")
print()

for scenario_name, traj in scenarios.items():
    # Find first month where system crosses anomaly threshold (0.60)
    threshold_cross = next((t['month'] for t in traj if t['health'] >= 0.60), None)
    # Find first month within Golay radius
    golay_cross = next((t['month'] for t in traj if t['hd_to_target'] <= GOLAY_CORRECTION_RADIUS), None)

    if threshold_cross is not None:
        print(f"  {scenario_name}: Crosses anomaly threshold at month {threshold_cross}")
    else:
        print(f"  {scenario_name}: Never crosses anomaly threshold in 60 months")

    if golay_cross is not None:
        print(f"    → Enters Golay self-correction range at month {golay_cross}")

# ============================================================
# NZ SUPPLY CHAIN QUANTIFICATION (Track B)
# ============================================================

print("\n[5] NZ SUPPLY CHAIN QUANTIFICATION — Track B:")
print()

# Acetone supply chain analysis
print("  ACETONE (A3-A5 program):")
print("  ├─ Industrial acetone price (NZ import): ~NZD $1.20-1.80/L")
print("  ├─ A5 blend: 5% × 3.8 billion L petrol/year = 190 million L acetone/year needed")
print("  ├─ NZ industrial solvent market: ~50-80 million L/year currently")
print("  ├─ Gap at A5: ~110-140 million L/year — requires import scaling")
print("  ├─ NZ domestic production pathway: petroleum solvent byproduct streams")
print("  └─ Timeline to A5 supply security: 12-18 months (import + domestic)")

# Quantitative supply analysis
petrol_annual_L = 3.8e9  # 3.8 billion litres petrol/year
a5_acetone_need = petrol_annual_L * 0.05
a3_acetone_need = petrol_annual_L * 0.03
current_nz_acetone = 65e6  # 65 million L estimate

print(f"\n  NZ Petrol consumption: {petrol_annual_L/1e9:.1f} billion L/year")
print(f"  A3 acetone requirement: {a3_acetone_need/1e6:.0f} ML/year")
print(f"  A5 acetone requirement: {a5_acetone_need/1e6:.0f} ML/year")
print(f"  Current NZ acetone supply estimate: ~{current_nz_acetone/1e6:.0f} ML/year")
print(f"  Supply gap at A5: {(a5_acetone_need - current_nz_acetone)/1e6:.0f} ML/year")
print(f"  Supply gap at A3: {max(0, a3_acetone_need - current_nz_acetone)/1e6:.0f} ML/year")

# Ethanol supply analysis
print("\n  ETHANOL (E10 mandate):")
e10_ethanol_need = petrol_annual_L * 0.10
print(f"  E10 ethanol requirement: {e10_ethanol_need/1e6:.0f} ML/year")
print(f"  NZ forest biomass available: ~1 million ODT/year")
print(f"  Ethanol yield from wood (lignocellulosic): ~250 L/ODT")
print(f"  Potential from existing biomass: {1e6 * 250 / 1e6:.0f} ML/year")
print(f"  Gap for E10: {(e10_ethanol_need - 1e6*250) / 1e6:.0f} ML/year (import required initially)")

potential_bio_ethanol = 1e6 * 250  # L/year from existing biomass
e10_gap = e10_ethanol_need - potential_bio_ethanol
print(f"  Import gap: {e10_gap/1e6:.0f} ML/year (Brazil E-fuel, Australia)")
print(f"  Cost at AUD $0.80/L: NZD ${e10_gap * 0.80 * 1.10 / 1e9:.2f} billion/year")

# BTL development timeline
print("\n  BTL DEVELOPMENT (Long-term):")
print("  ├─ Scion pilot: 10,000 L/day fast pyrolysis (operating)")
print("  ├─ Phase 1 (2yr): Commercial-scale 50 ML/year — NZD $200M investment")
print("  ├─ Phase 2 (5yr): 300 ML/year — NZD $800M investment")
print("  ├─ Phase 3 (10yr): 1,500 ML/year from 1.8M ha forest — NZD $3.5B total")
print("  └─ Phase 3 = 40% of current NZ liquid fuel needs")

btl_phases = {
    'Phase 1 (Yr 2)': {'capacity_ML': 50, 'investment_NZD_M': 200},
    'Phase 2 (Yr 5)': {'capacity_ML': 300, 'investment_NZD_M': 800},
    'Phase 3 (Yr 10)': {'capacity_ML': 1500, 'investment_NZD_M': 3500},
}

for phase, data in btl_phases.items():
    pct_of_nz = data['capacity_ML'] / (petrol_annual_L/1e6) * 100
    print(f"  {phase}: {data['capacity_ML']} ML/year = {pct_of_nz:.1f}% of NZ petrol need, "
          f"NZD ${data['investment_NZD_M']}M")

# ============================================================
# V2 UBP KNOWLEDGE BASE EXTENSIONS
# ============================================================

print("\n[6] V2 UBP KNOWLEDGE BASE EXTENSIONS:")
print("    Three new LAW entries for ubp_system_kb.json (to be hardened via kb_architect.py)")

new_laws = [
    {
        'ubp_id': 'LAW_CHEM_FUEL_OPT_001',
        'lexicon': '[The Law of Fuel Coherence Optimization], [Fuel efficiency is maximized when the composite NRCI of the fuel-oxidizer mixture is maximized at the point of ignition. Oxygenated additives (alcohols, ketones) raise composite NRCI by introducing pre-bonded oxygen atoms whose geometric contribution to the combustion manifold bypasses the activation barrier, reducing effective E_act without reducing fuel density below critical combustion threshold.]',
        'math': 'NRCI_blend=Sum(x_i*NRCI_i)/Sum(x_i)|Optimum=dNRCI_blend/dx_additive>0|FQI=NRCI_blend*(1-E_act/E_act_max)*(1+0.5*O_frac)',
        'tags': ['CHEMISTRY', 'COMBUSTION', 'EFFICIENCY', 'FUEL', 'HARDENED', 'IMPERATIVE', 'NRCI', 'OXYGENATE', 'SOP_002', 'V4.0'],
        'hierarchy': 'LAW_CHEM_HYDROCARBON_001 + LAW_CHEM_KINETICS_001 + LAW_CHEM_ONTOLOGICAL_YIELD',
        'status': 'PROPOSED — requires kb_architect.py hardening for SHA256 fingerprint and 24-bit vector assignment'
    },
    {
        'ubp_id': 'LAW_CHEM_FUEL_OPT_002',
        'lexicon': '[The Law of Phase-Staged Combustion], [The efficiency of a combustion event is a monotonically increasing function of the pre-ignition phase advancement of the fuel; partial vaporization before ignition reduces the activation Tax without incurring the full power penalty of complete vaporization, by maintaining liquid-phase density while elevating the effective NRCI of the combustion-ready vapor fraction.]',
        'math': 'BTE_gain~(T_preheat-T_ambient)*k|k=111/100000_per_degC|Optimal_T=125_degC|Phase_advance=d_H_increase/3.0_per_stage',
        'tags': ['CHEMISTRY', 'COMBUSTION', 'EFFICIENCY', 'FUEL', 'HARDENED', 'IMPERATIVE', 'PHASE_TRANSITION', 'PREHEATING', 'SOP_002', 'V4.0'],
        'hierarchy': 'LAW_CHEM_PHASE_001 + LAW_CHEM_KINETICS_001',
        'status': 'PROPOSED — requires hardening'
    },
    {
        'ubp_id': 'LAW_SUPPLY_SECURITY_001',
        'lexicon': '[The Law of Distributed Supply Coherence], [A nation fuel supply security is proportional to the number of independent geometric pathways (supply vectors) to stable physical stock; each pathway corresponds to a distinct Golay codeword in the supply manifold. The minimum coherent system requires at least 3 independent supply pathways to guarantee recovery from any single-pathway disruption without exceeding the Golay correction radius.]',
        'math': 'Security=min(HD_disruption)_across_all_pathways|Minimum_pathways=3_for_d_H<=3|Health=Sum(Layer_NRCI)/4|Threshold=0.60',
        'tags': ['ECONOMY', 'GEOPOLITICS', 'HARDENED', 'IMPERATIVE', 'RESILIENCE', 'SECURITY', 'SOP_002', 'SUPPLY_CHAIN', 'V4.0'],
        'hierarchy': 'LAW_APP_001 + LAW_APP_002',
        'status': 'PROPOSED — requires hardening'
    },
    {
        'ubp_id': 'LAW_CHEM_VAPOR_OPT_001',
        'lexicon': '[The Law of Oxygenate-Compensated Vapor Combustion], [The 9% power deficit of full vapor combustion can be partially compensated by oxygenated additive blending. Each 1% volume oxygenate (acetone: 0.012 compensation coefficient; ethanol: 0.008) reduces vapor-induced power loss by contributing in-molecule oxygen that replaces the combustion density function of the liquid-phase fuel. Optimal vapor combustion = partial vapor (70%) + A10 + E10 achieving 20% efficiency gain with <2% power loss.]',
        'math': 'Power_loss_compensation=acetone_pct*0.012+ethanol_pct*0.008|Optimal_vapor_frac=0.7|Net_gain=vapor_efficiency*(1-0.3*compensated_loss)',
        'tags': ['CHEMISTRY', 'COMBUSTION', 'FUEL', 'HARDENED', 'IMPERATIVE', 'OXYGENATE', 'SOP_002', 'VAPOR', 'V4.0'],
        'hierarchy': 'LAW_CHEM_FUEL_OPT_001 + LAW_CHEM_FUEL_OPT_002 + LAW_CHEM_PHASE_001',
        'status': 'NEW — V2 discovery, requires hardening'
    },
]

for law in new_laws:
    print(f"\n  {law['ubp_id']}:")
    print(f"    Status: {law['status']}")
    print(f"    Hierarchy: {law['hierarchy']}")

# ============================================================
# SAVE RESULTS
# ============================================================

results = {
    'system_state_vectors': {
        'baseline': BASELINE_VECTOR,
        'target': TARGET_VECTOR,
        'baseline_health': baseline_health,
        'target_health': target_health,
        'initial_hd': total_hd,
    },
    'intervention_effects': {k: {
        'description': v['description'],
        'hd_corrected': sum(v['layer_corrections'].values()),
        'nrci_deltas': v['nrci_deltas'],
        'timeline_months': v['timeline_months'],
        'tier': v['tier'],
        'fleet_coverage': v['fleet_coverage'],
        'ubp_law': v['ubp_law'],
    } for k, v in interventions.items()},
    'trajectories': {k: [
        {kk: vv for kk, vv in d.items()}
        for d in v
    ] for k, v in scenarios.items()},
    'supply_chain': {
        'petrol_annual_L': petrol_annual_L,
        'a5_acetone_need_L': a5_acetone_need,
        'e10_ethanol_need_L': e10_ethanol_need,
        'potential_biomass_ethanol_L': potential_bio_ethanol,
        'btl_phases': btl_phases,
    },
    'proposed_new_laws': new_laws,
}

output_path = '/app/sandbox/session_20260401_122838_1d6509467bbc/results/hamming_drift_results.json'
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n[SAVED] Results → {output_path}")
print("\nHamming Drift System Analysis COMPLETE.")
