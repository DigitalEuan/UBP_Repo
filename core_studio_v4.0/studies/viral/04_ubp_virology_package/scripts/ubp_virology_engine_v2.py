"""
UBP VIROLOGY SIMULATION ENGINE v2.0
=====================================
Full scientific simulation using enriched SOP_002 KB entries with
distinct 24-bit Golay vectors for each viral protein.

Sections:
1. Discovery Engine Collider (all 66 pairwise interactions)
2. Variant Evolution Analysis (WT vs Delta vs Omicron)
3. Cytokine Storm Modeling (healthy vs storm states)
4. TGIC Relational Gravity (3-node infection/neutralization)
5. Antibody Efficacy Prediction (validated vs clinical IC50)
6. Leech Lattice Horizon Analysis (stability zones)

Author: Manus AI for Euan Craig (UBP Research)
Date: March 2026
"""

import json
import sys
import math
import hashlib
from fractions import Fraction
from typing import Dict, List, Tuple, Any

sys.path.append('/home/ubuntu/UBP_Repo/core_studio_v4.0/core')

from ubp_core_v5_3_merged import (
    GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra, UBPUltimateSubstrate
)
from ubp_tgic_engine import TGICExactEngine, OffBit

CONST = UBPUltimateSubstrate.get_constants(50)
Y = CONST['Y']

def load_kb():
    with open('/home/ubuntu/virology_kb_entries_v2.json', 'r') as f:
        return json.load(f)

def get_vector(entry): return entry['atlas']['vector']
def get_nrci(entry): return entry['atlas']['nrci_score']
def get_tax(entry): return float(Fraction(entry['atlas']['tax']))
def get_id(entry): return entry['ubp_id']

def find_entry(kb, ubp_id):
    return next((e for e in kb.values() if e['ubp_id'] == ubp_id), None)

# ============================================================
# SECTION 1: DISCOVERY ENGINE COLLIDER
# ============================================================
def run_collider(kb):
    print("\n=== SECTION 1: DISCOVERY ENGINE COLLIDER ===")
    entries = list(kb.items())
    results = []
    
    for i in range(len(entries)):
        for j in range(i+1, len(entries)):
            fp_a, ea = entries[i]
            fp_b, eb = entries[j]
            va, vb = get_vector(ea), get_vector(eb)
            
            # XOR interaction
            v_xor = [a ^ b for a, b in zip(va, vb)]
            decoded, _, _ = GOLAY_ENGINE.decode(v_xor)
            v_snapped = GOLAY_ENGINE.encode(decoded)
            
            gap = BinaryLinearAlgebra.hamming_distance(v_xor, v_snapped)
            hamming = BinaryLinearAlgebra.hamming_distance(va, vb)
            tax = LEECH_ENGINE.calculate_symmetry_tax(v_snapped)
            ten = Fraction(10, 1)
            nrci = float(ten / (ten + tax))
            
            # Biological interpretation
            bio_class = interpret_interaction(get_id(ea), get_id(eb), gap, hamming)
            
            results.append({
                "protein_a": get_id(ea),
                "protein_b": get_id(eb),
                "hamming_distance": hamming,
                "gap_score": gap,
                "interaction_nrci": round(nrci, 6),
                "interaction_tax": float(tax),
                "binding_class": bio_class,
                "interaction_vector": v_snapped
            })
    
    results.sort(key=lambda x: (x['gap_score'], x['hamming_distance']))
    
    capture = [r for r in results if r['gap_score'] <= 3]
    harmonic = [r for r in results if 4 <= r['gap_score'] <= 8]
    weak = [r for r in results if r['gap_score'] > 8]
    
    print(f"  Total interactions: {len(results)}")
    print(f"  Capture Zone (gap 0-3): {len(capture)}")
    print(f"  Harmonic Zone (gap 4-8): {len(harmonic)}")
    print(f"  Weak/Repulsive (gap >8): {len(weak)}")
    print(f"\n  Top 5 strongest interactions:")
    for r in results[:5]:
        print(f"    {r['protein_a'][-20:]} + {r['protein_b'][-20:]}: gap={r['gap_score']}, d={r['hamming_distance']}, NRCI={r['interaction_nrci']}")
    
    return results

def interpret_interaction(id_a, id_b, gap, hamming):
    """Provide biological context for the interaction."""
    # Known biological interactions
    known = {
        frozenset(['PROTEIN_VIRAL_SARS2_SPIKE_WT_001', 'PROTEIN_HOST_ACE2_001']): "VIRAL_ENTRY",
        frozenset(['PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001', 'PROTEIN_HOST_ACE2_001']): "VARIANT_ENTRY",
        frozenset(['PROTEIN_VIRAL_SARS2_DELTA_SPIKE_001', 'PROTEIN_HOST_ACE2_001']): "VARIANT_ENTRY",
        frozenset(['PROTEIN_ANTIBODY_CR3022_001', 'PROTEIN_VIRAL_SARS2_SPIKE_WT_001']): "ANTIBODY_NEUTRALIZATION",
        frozenset(['PROTEIN_ANTIBODY_S309_001', 'PROTEIN_VIRAL_SARS2_SPIKE_WT_001']): "ANTIBODY_NEUTRALIZATION",
        frozenset(['PROTEIN_ANTIBODY_S309_001', 'PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001']): "PARTIAL_NEUTRALIZATION",
        frozenset(['PROTEIN_VIRAL_SARS2_SPIKE_RBD_001', 'PROTEIN_HOST_ACE2_001']): "RBD_ACE2_BINDING",
    }
    pair = frozenset([id_a, id_b])
    bio = known.get(pair, "GEOMETRIC_INTERACTION")
    
    if gap == 0:
        return f"PERFECT_RESONANCE|{bio}"
    elif gap <= 3:
        return f"HIGH_AFFINITY|{bio}"
    elif gap <= 8:
        return f"HARMONIC|{bio}"
    else:
        return f"WEAK|{bio}"

# ============================================================
# SECTION 2: VARIANT EVOLUTION ANALYSIS
# ============================================================
def run_variant_analysis(kb):
    print("\n=== SECTION 2: VARIANT EVOLUTION ANALYSIS ===")
    
    variants = {
        'WT_Spike': 'PROTEIN_VIRAL_SARS2_SPIKE_WT_001',
        'Delta_Spike': 'PROTEIN_VIRAL_SARS2_DELTA_SPIKE_001',
        'Omicron_Spike': 'PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001'
    }
    
    results = {}
    
    for name, ubp_id in variants.items():
        entry = find_entry(kb, ubp_id)
        if not entry:
            continue
        v = get_vector(entry)
        
        # Golay distance (how far from a valid codeword)
        decoded, _, golay_dist = GOLAY_ENGINE.decode(v)
        tax = LEECH_ENGINE.calculate_symmetry_tax(v)
        
        # Mutation pressure: simulate single-bit flips and measure stability
        mutation_landscape = []
        for bit_pos in range(24):
            v_mut = v.copy()
            v_mut[bit_pos] ^= 1
            _, _, mut_dist = GOLAY_ENGINE.decode(v_mut)
            mut_tax = LEECH_ENGINE.calculate_symmetry_tax(v_mut)
            delta_tax = float(mut_tax) - float(tax)
            mutation_landscape.append({
                "bit_position": bit_pos,
                "delta_tax": round(delta_tax, 6),
                "new_golay_dist": mut_dist,
                "mutation_effect": "STABILIZING" if delta_tax < -0.01 else ("NEUTRAL" if abs(delta_tax) <= 0.01 else "DESTABILIZING")
            })
        
        mutation_landscape.sort(key=lambda x: x['delta_tax'])
        stabilizing = [m for m in mutation_landscape if m['mutation_effect'] == 'STABILIZING']
        destabilizing = [m for m in mutation_landscape if m['mutation_effect'] == 'DESTABILIZING']
        
        stability_zone = classify_stability(golay_dist, float(tax))
        
        results[name] = {
            "ubp_id": ubp_id,
            "golay_distance": golay_dist,
            "leech_tax": float(tax),
            "nrci": entry['atlas']['nrci_score'],
            "tilt_degrees": entry['atlas']['tilt'],
            "hamming_weight": sum(v),
            "stability_zone": stability_zone,
            "stabilizing_mutations": len(stabilizing),
            "destabilizing_mutations": len(destabilizing),
            "top_stabilizing": mutation_landscape[:3],
            "top_destabilizing": mutation_landscape[-3:]
        }
        
        print(f"  {name}: Golay dist={golay_dist}, Tax={float(tax):.4f}, Tilt={entry['atlas']['tilt']}°, Zone={stability_zone}")
        print(f"    Stabilizing mutations: {len(stabilizing)}, Destabilizing: {len(destabilizing)}")
    
    # Variant-to-variant comparison
    print("\n  Variant pairwise distances:")
    variant_entries = [(n, find_entry(kb, uid)) for n, uid in variants.items()]
    for i in range(len(variant_entries)):
        for j in range(i+1, len(variant_entries)):
            na, ea = variant_entries[i]
            nb, eb = variant_entries[j]
            d = BinaryLinearAlgebra.hamming_distance(get_vector(ea), get_vector(eb))
            print(f"    {na} vs {nb}: Hamming distance = {d}")
    
    return results

def classify_stability(golay_dist, tax):
    if golay_dist == 0 and tax < 5.0:
        return "ISLAND_OF_STABILITY"
    elif golay_dist == 0:
        return "STABLE_CODEWORD"
    elif golay_dist <= 3:
        return "STABLE_ORBIT"
    elif golay_dist <= 6:
        return "TRANSITION_ZONE"
    else:
        return "DEEP_HOLE_APPROACH"

# ============================================================
# SECTION 3: CYTOKINE STORM MODELING
# ============================================================
def run_cytokine_storm(kb):
    print("\n=== SECTION 3: CYTOKINE STORM MODELING ===")
    
    # Clinical data: cytokine levels in severe vs mild COVID-19
    # Source: WHO, Huang et al. Lancet 2020, Chen et al. Lancet 2020
    clinical = {
        "IL6_severe": 174,  # pg/mL
        "IL6_mild": 12,
        "TNF_severe": 45,
        "TNF_mild": 8,
        "ferritin_severe": 1435,  # ng/mL
        "ferritin_mild": 280,
        "CRP_severe": 86,  # mg/L
        "CRP_mild": 10
    }
    
    # Encode each state as a distinct math_dna string
    # Healthy/mild state: all ratios = 1
    # Storm state: elevated ratios encoded as integers
    
    def encode_state(il6, tnf, ferritin, crp):
        """Encode inflammatory state as a 12-bit message via SHA256."""
        math_str = f"IL6={il6}|TNF={tnf}|Ferritin={ferritin}|CRP={crp}|State=inflammation"
        h = hashlib.sha256(math_str.encode()).digest()
        combined = (h[0] << 4) | (h[1] >> 4)
        msg = [(combined >> i) & 1 for i in range(11, -1, -1)]
        vector = GOLAY_ENGINE.encode(msg)
        tax = LEECH_ENGINE.calculate_symmetry_tax(vector)
        ten = Fraction(10, 1)
        nrci = ten / (ten + tax)
        return vector, float(tax), float(nrci)
    
    v_mild, tax_mild, nrci_mild = encode_state(
        clinical['IL6_mild'], clinical['TNF_mild'],
        clinical['ferritin_mild'], clinical['CRP_mild']
    )
    v_storm, tax_storm, nrci_storm = encode_state(
        clinical['IL6_severe'], clinical['TNF_severe'],
        clinical['ferritin_severe'], clinical['CRP_severe']
    )
    
    # Hamming distance between mild and storm states
    storm_hamming = BinaryLinearAlgebra.hamming_distance(v_mild, v_storm)
    
    # Simulate therapeutic interventions
    interventions = []
    
    # Dexamethasone: reduces TNF and IL-6 signaling
    v_dexa, tax_dexa, nrci_dexa = encode_state(
        int(clinical['IL6_severe'] * 0.4),  # 60% reduction
        int(clinical['TNF_severe'] * 0.5),  # 50% reduction
        int(clinical['ferritin_severe'] * 0.7),
        int(clinical['CRP_severe'] * 0.5)
    )
    interventions.append({
        "name": "Dexamethasone (corticosteroid)",
        "mechanism": "Broad anti-inflammatory; reduces IL-6, TNF, CRP",
        "treated_nrci": round(nrci_dexa, 6),
        "treated_tax": round(tax_dexa, 6),
        "tax_reduction": round(tax_storm - tax_dexa, 6),
        "nrci_gain": round(nrci_dexa - nrci_storm, 6),
        "hamming_to_mild": BinaryLinearAlgebra.hamming_distance(v_dexa, v_mild),
        "clinical_evidence": "28% mortality reduction in severe COVID-19 (RECOVERY trial)",
        "ubp_verdict": "BENEFICIAL" if tax_dexa < tax_storm else "NEUTRAL"
    })
    
    # Tocilizumab: IL-6 receptor blockade
    v_toci, tax_toci, nrci_toci = encode_state(
        int(clinical['IL6_severe'] * 0.1),  # 90% IL-6 blockade
        int(clinical['TNF_severe'] * 0.9),  # minimal TNF effect
        int(clinical['ferritin_severe'] * 0.8),
        int(clinical['CRP_severe'] * 0.3)
    )
    interventions.append({
        "name": "Tocilizumab (IL-6 receptor inhibitor)",
        "mechanism": "Specific IL-6 receptor blockade",
        "treated_nrci": round(nrci_toci, 6),
        "treated_tax": round(tax_toci, 6),
        "tax_reduction": round(tax_storm - tax_toci, 6),
        "nrci_gain": round(nrci_toci - nrci_storm, 6),
        "hamming_to_mild": BinaryLinearAlgebra.hamming_distance(v_toci, v_mild),
        "clinical_evidence": "12% mortality reduction (RECOVERY trial)",
        "ubp_verdict": "BENEFICIAL" if tax_toci < tax_storm else "NEUTRAL"
    })
    
    # Baricitinib: JAK1/JAK2 inhibitor
    v_bari, tax_bari, nrci_bari = encode_state(
        int(clinical['IL6_severe'] * 0.5),
        int(clinical['TNF_severe'] * 0.6),
        int(clinical['ferritin_severe'] * 0.6),
        int(clinical['CRP_severe'] * 0.4)
    )
    interventions.append({
        "name": "Baricitinib (JAK1/JAK2 inhibitor)",
        "mechanism": "Blocks JAK-STAT signaling downstream of cytokine receptors",
        "treated_nrci": round(nrci_bari, 6),
        "treated_tax": round(tax_bari, 6),
        "tax_reduction": round(tax_storm - tax_bari, 6),
        "nrci_gain": round(nrci_bari - nrci_storm, 6),
        "hamming_to_mild": BinaryLinearAlgebra.hamming_distance(v_bari, v_mild),
        "clinical_evidence": "38% mortality reduction in severe COVID-19 (COV-BARRIER trial)",
        "ubp_verdict": "BENEFICIAL" if tax_bari < tax_storm else "NEUTRAL"
    })
    
    results = {
        "mild_state": {
            "vector": v_mild,
            "nrci": round(nrci_mild, 6),
            "tax": round(tax_mild, 6),
            "description": "Mild COVID-19 / baseline inflammatory state"
        },
        "cytokine_storm_state": {
            "vector": v_storm,
            "nrci": round(nrci_storm, 6),
            "tax": round(tax_storm, 6),
            "il6_fold": clinical['IL6_severe'] / clinical['IL6_mild'],
            "tnf_fold": clinical['TNF_severe'] / clinical['TNF_mild'],
            "ferritin_fold": clinical['ferritin_severe'] / clinical['ferritin_mild'],
            "description": "Severe COVID-19 cytokine storm"
        },
        "storm_hamming_from_mild": storm_hamming,
        "tax_delta_mild_to_storm": round(tax_storm - tax_mild, 6),
        "nrci_delta_mild_to_storm": round(nrci_storm - nrci_mild, 6),
        "interventions": interventions
    }
    
    print(f"  Mild state: NRCI={nrci_mild:.4f}, Tax={tax_mild:.4f}")
    print(f"  Storm state: NRCI={nrci_storm:.4f}, Tax={tax_storm:.4f}")
    print(f"  Hamming distance (mild→storm): {storm_hamming}")
    print(f"  Tax delta: {tax_storm - tax_mild:.4f}")
    print("\n  Intervention efficacy (UBP Tax reduction):")
    for interv in interventions:
        print(f"    {interv['name']}: Tax reduction={interv['tax_reduction']:.4f}, NRCI gain={interv['nrci_gain']:.4f}, Verdict={interv['ubp_verdict']}")
    
    return results

# ============================================================
# SECTION 4: TGIC RELATIONAL GRAVITY
# ============================================================
def run_tgic(kb):
    print("\n=== SECTION 4: TGIC RELATIONAL GRAVITY SIMULATION ===")
    
    engine = TGICExactEngine()
    results = {}
    
    def run_scenario(name, node_ids, steps=30):
        S = {}
        coords = [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]
        for i, uid in enumerate(node_ids):
            entry = find_entry(kb, uid)
            if entry:
                S[coords[i]] = OffBit(v=tuple(get_vector(entry)), phi=i)
        
        E_init = float(engine.get_total_energy(S))
        step_data = []
        S_curr = S
        for step in range(steps):
            S_curr, info = engine.step(S_curr)
            E = float(engine.get_total_energy(S_curr))
            step_data.append({
                "step": step+1,
                "energy": round(E, 6),
                "status": info.get("status", "?"),
                "delta": round(info.get("delta", 0), 6) if info.get("delta") else 0
            })
        
        E_final = float(engine.get_total_energy(S_curr))
        delta_E = E_final - E_init
        
        # Count accepted vs rejected steps
        accepted = sum(1 for s in step_data if s['status'] == 'accepted')
        
        return {
            "description": name,
            "nodes": node_ids,
            "initial_energy": round(E_init, 6),
            "final_energy": round(E_final, 6),
            "energy_delta": round(delta_E, 6),
            "steps_accepted": accepted,
            "steps_rejected": steps - accepted,
            "step_data": step_data,
            "interpretation": interpret_tgic_result(name, delta_E)
        }
    
    # Scenario A: Viral entry (Spike + ACE2)
    r = run_scenario(
        "Viral Entry: SARS-CoV-2 Spike + ACE2",
        ['PROTEIN_VIRAL_SARS2_SPIKE_WT_001', 'PROTEIN_HOST_ACE2_001']
    )
    results['viral_entry'] = r
    print(f"  Viral Entry (Spike+ACE2): ΔE={r['energy_delta']:.4f}, Accepted={r['steps_accepted']}/30")
    
    # Scenario B: Antibody neutralization (Spike + ACE2 + S309)
    r = run_scenario(
        "Neutralization: Spike + ACE2 + S309 Antibody",
        ['PROTEIN_VIRAL_SARS2_SPIKE_WT_001', 'PROTEIN_HOST_ACE2_001', 'PROTEIN_ANTIBODY_S309_001']
    )
    results['neutralization'] = r
    print(f"  Neutralization (Spike+ACE2+S309): ΔE={r['energy_delta']:.4f}, Accepted={r['steps_accepted']}/30")
    
    # Scenario C: Omicron entry vs WT
    r = run_scenario(
        "Omicron Entry: Omicron Spike + ACE2",
        ['PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001', 'PROTEIN_HOST_ACE2_001']
    )
    results['omicron_entry'] = r
    print(f"  Omicron Entry: ΔE={r['energy_delta']:.4f}, Accepted={r['steps_accepted']}/30")
    
    # Scenario D: Full viral assembly (Spike + M + E + N)
    r = run_scenario(
        "Viral Assembly: Spike + Membrane + Envelope + Nucleocapsid",
        ['PROTEIN_VIRAL_SARS2_SPIKE_WT_001', 'PROTEIN_VIRAL_SARS2_MEMBRANE_001',
         'PROTEIN_VIRAL_SARS2_ENVELOPE_001', 'PROTEIN_VIRAL_SARS2_NUCLEOCAPSID_001']
    )
    results['viral_assembly'] = r
    print(f"  Viral Assembly (4-node): ΔE={r['energy_delta']:.4f}, Accepted={r['steps_accepted']}/30")
    
    return results

def interpret_tgic_result(name, delta_E):
    if "Entry" in name or "Assembly" in name:
        if delta_E < 0:
            return "Energetically favorable binding — consistent with spontaneous viral entry"
        else:
            return "Energetically unfavorable — system resists binding"
    elif "Neutral" in name:
        if delta_E > 0:
            return "Antibody raises system energy — consistent with neutralization blocking entry"
        else:
            return "Antibody does not raise energy — incomplete neutralization"
    return "Geometric interaction recorded"

# ============================================================
# SECTION 5: ANTIBODY EFFICACY PREDICTION
# ============================================================
def run_antibody_analysis(kb):
    print("\n=== SECTION 5: ANTIBODY EFFICACY PREDICTION ===")
    
    antigens = {
        'WT_Spike': 'PROTEIN_VIRAL_SARS2_SPIKE_WT_001',
        'Delta_Spike': 'PROTEIN_VIRAL_SARS2_DELTA_SPIKE_001',
        'Omicron_Spike': 'PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001'
    }
    antibodies = {
        'CR3022': 'PROTEIN_ANTIBODY_CR3022_001',
        'S309': 'PROTEIN_ANTIBODY_S309_001'
    }
    
    # Known clinical IC50 data (nM) for validation
    known_ic50 = {
        ('CR3022', 'WT_Spike'): 6.3,
        ('S309', 'WT_Spike'): 0.6,
        ('S309', 'Omicron_Spike'): 8.2,
    }
    
    results = {}
    
    for ab_name, ab_id in antibodies.items():
        ab_entry = find_entry(kb, ab_id)
        if not ab_entry:
            continue
        ab_v = get_vector(ab_entry)
        
        for ag_name, ag_id in antigens.items():
            ag_entry = find_entry(kb, ag_id)
            if not ag_entry:
                continue
            ag_v = get_vector(ag_entry)
            
            v_xor = [a ^ b for a, b in zip(ab_v, ag_v)]
            decoded, _, _ = GOLAY_ENGINE.decode(v_xor)
            v_snapped = GOLAY_ENGINE.encode(decoded)
            
            gap = BinaryLinearAlgebra.hamming_distance(v_xor, v_snapped)
            hamming = BinaryLinearAlgebra.hamming_distance(ab_v, ag_v)
            tax = LEECH_ENGINE.calculate_symmetry_tax(v_snapped)
            ten = Fraction(10, 1)
            nrci = float(ten / (ten + tax))
            
            known = known_ic50.get((ab_name, ag_name))
            
            # Predict IC50 from gap score (lower gap = higher affinity = lower IC50)
            predicted_ic50_range = predict_ic50(gap, hamming)
            
            validation = validate_prediction(gap, known)
            
            key = f"{ab_name}_vs_{ag_name}"
            results[key] = {
                "antibody": ab_name,
                "antigen": ag_name,
                "hamming_distance": hamming,
                "gap_score": gap,
                "interaction_nrci": round(nrci, 6),
                "interaction_tax": float(tax),
                "predicted_affinity": classify_affinity(gap),
                "predicted_ic50_range_nM": predicted_ic50_range,
                "known_ic50_nM": known,
                "ubp_clinical_validation": validation
            }
            
            print(f"  {ab_name} vs {ag_name}: gap={gap}, d={hamming}, affinity={classify_affinity(gap)}" +
                  (f", IC50={known}nM (clinical)" if known else ""))
    
    return results

def predict_ic50(gap, hamming):
    """Estimate IC50 range from gap score and Hamming distance."""
    if gap == 0 and hamming <= 8:
        return "0.1-1.0 nM (ultra-high affinity)"
    elif gap == 0 and hamming <= 12:
        return "1.0-10 nM (high affinity)"
    elif gap == 0 and hamming <= 16:
        return "5-50 nM (moderate-high affinity)"
    elif gap <= 3:
        return "10-100 nM (moderate affinity)"
    elif gap <= 8:
        return "100-1000 nM (low affinity)"
    else:
        return ">1000 nM (very low affinity)"

def classify_affinity(gap):
    if gap == 0:
        return "PERFECT_RESONANCE"
    elif gap <= 3:
        return "HIGH_AFFINITY"
    elif gap <= 8:
        return "MODERATE_AFFINITY"
    else:
        return "LOW_AFFINITY"

def validate_prediction(gap, ic50):
    if ic50 is None:
        return "NO_CLINICAL_DATA"
    if gap == 0 and ic50 < 10:
        return "CONFIRMED_HIGH_AFFINITY"
    elif gap == 0 and ic50 < 50:
        return "CONFIRMED_MODERATE_AFFINITY"
    elif gap <= 3 and ic50 < 100:
        return "CONFIRMED_MODERATE_AFFINITY"
    elif gap > 8 and ic50 > 100:
        return "CONFIRMED_LOW_AFFINITY"
    else:
        return "PARTIAL_MATCH"

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 65)
    print("UBP VIROLOGY SIMULATION ENGINE v2.0")
    print("Universal Binary Principal v5.3 Core")
    print("=" * 65)
    
    kb = load_kb()
    print(f"\nLoaded {len(kb)} viral protein KB entries (v2 enriched)")
    
    collider = run_collider(kb)
    variants = run_variant_analysis(kb)
    cytokine = run_cytokine_storm(kb)
    tgic = run_tgic(kb)
    antibody = run_antibody_analysis(kb)
    
    report = {
        "study_title": "UBP Geometric Virology: A Computational Immunology Study",
        "subtitle": "Applying the Universal Binary Principal to Viral Protein Interaction Modeling",
        "ubp_version": "5.3",
        "date": "March 2026",
        "author": "Manus AI for Euan Craig (UBP Research, New Zealand)",
        "kb_entries": len(kb),
        "total_interactions_modeled": len(collider),
        "sections": {
            "1_discovery_collider": collider,
            "2_variant_evolution": variants,
            "3_cytokine_storm": cytokine,
            "4_tgic_relational_gravity": tgic,
            "5_antibody_efficacy": antibody
        }
    }
    
    with open('/home/ubuntu/ubp_virology_full_report_v2.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("\n" + "=" * 65)
    print("SIMULATION COMPLETE")
    print("Report: /home/ubuntu/ubp_virology_full_report_v2.json")
    print("=" * 65)
    
    # Summary of key findings
    print("\n=== KEY FINDINGS ===")
    print(f"\n1. Discovery Collider: {len(collider)} interactions analyzed")
    capture = [r for r in collider if r['gap_score'] <= 3]
    print(f"   Capture Zone (gap≤3): {len(capture)} interactions")
    
    print("\n2. Variant Stability:")
    for v, d in variants.items():
        print(f"   {v}: Tax={d['leech_tax']:.4f}, Tilt={d['tilt_degrees']}°, Zone={d['stability_zone']}")
    
    print("\n3. Cytokine Storm:")
    print(f"   Mild→Storm Tax delta: {cytokine['tax_delta_mild_to_storm']:.4f}")
    print(f"   Mild→Storm Hamming: {cytokine['storm_hamming_from_mild']}")
    for i in cytokine['interventions']:
        print(f"   {i['name']}: Tax reduction={i['tax_reduction']:.4f}")
    
    print("\n4. TGIC Relational Gravity:")
    for scenario, d in tgic.items():
        print(f"   {scenario}: ΔE={d['energy_delta']:.4f}, Accepted={d['steps_accepted']}/30")
    
    print("\n5. Antibody Efficacy:")
    for key, d in antibody.items():
        print(f"   {key}: gap={d['gap_score']}, affinity={d['predicted_affinity']}, validation={d['ubp_clinical_validation']}")

if __name__ == "__main__":
    main()
