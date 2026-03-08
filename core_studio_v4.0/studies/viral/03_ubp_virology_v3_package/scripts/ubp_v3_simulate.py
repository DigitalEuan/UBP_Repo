"""
UBP Geometric Virology v3.0 — Full Simulation Engine (Corrected API)
Uses proper UBP Core v5.7 API: OffBit, TGICExactEngine, GOLAY_ENGINE, LEECH_ENGINE, KBArchitect
"""
import json
import sys
import os
import math
from fractions import Fraction
from dataclasses import dataclass
from typing import Tuple, List, Dict

sys.path.insert(0, '/home/ubuntu/UBP_Repo/core_studio_v4.0/core')

from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE
from ubp_kb_architect import KBArchitect
from ubp_tgic_engine import TGICExactEngine, OffBit

print("=== UBP Geometric Virology v3.0 — Full Simulation Engine ===")
print("Loading protein data...")

with open('/home/ubuntu/ubp_v3_protein_data_raw.json') as f:
    proteins_raw = json.load(f)

print(f"Loaded {len(proteins_raw)} proteins")

# ============================================================
# STEP 1: BUILD ALL KB ENTRIES + EXTRACT VECTORS
# ============================================================
print("\n--- Step 1: Building KB Entries ---")

arch = KBArchitect()
ge = GOLAY_ENGINE
le = LEECH_ENGINE
tgic_eng = TGICExactEngine()

kb_entries = {}
vector_map = {}
tax_map = {}
tilt_map = {}
nrci_map = {}

for key, prot in proteins_raw.items():
    math_dna = prot['math_dna']
    name = prot['name'][:80]
    definition = prot['definition'][:300]
    group = prot['group']
    organism = prot['organism']
    
    # Build hierarchy
    hierarchy_map = {
        'CoV2_Structural': 'BIOLOGY.VIRUS.SARS-CoV-2.STRUCTURAL',
        'CoV2_Nonstructural': 'BIOLOGY.VIRUS.SARS-CoV-2.NONSTRUCTURAL',
        'CoV2_Variants': 'BIOLOGY.VIRUS.SARS-CoV-2.VARIANTS',
        'Influenza': 'BIOLOGY.VIRUS.INFLUENZA',
        'HIV': 'BIOLOGY.VIRUS.HIV',
        'Dengue': 'BIOLOGY.VIRUS.DENGUE',
        'Ebola': 'BIOLOGY.VIRUS.EBOLA',
        'RSV': 'BIOLOGY.VIRUS.RSV',
        'Enterovirus': 'BIOLOGY.VIRUS.ENTEROVIRUS',
        'Host': 'BIOLOGY.HOST.HUMAN',
        'Antibody': 'BIOLOGY.THERAPEUTIC.ANTIBODY',
        'Therapeutic': 'BIOLOGY.THERAPEUTIC.SMALLMOLECULE',
    }
    hierarchy = hierarchy_map.get(group, 'BIOLOGY.VIRUS')
    
    tags = [group, organism.split()[0]]
    if 'variant_metadata' in prot:
        tags.append('VoC')
    if 'therapeutic_metadata' in prot:
        tags.append('Therapeutic')
    
    try:
        fingerprint, entry = arch.create_entry(
            ubp_id=f"VIROME_{key}_001",
            lexicon_name=name,
            definition=definition,
            math_dna=math_dna,
            hierarchy=hierarchy,
            tags=tags
        )
        
        kb_entries[key] = entry
        vector_map[key] = entry['atlas']['vector']
        tax_map[key] = float(Fraction(entry['atlas']['tax']))
        tilt_map[key] = entry['atlas']['tilt']
        nrci_map[key] = entry['atlas']['nrci_score']
        
    except Exception as e:
        print(f"  ERROR building {key}: {e}")
        continue

print(f"Built {len(kb_entries)} KB entries")

# ============================================================
# STEP 2: DISCOVERY ENGINE COLLIDER — ALL PAIRS
# ============================================================
print(f"\n--- Step 2: Discovery Engine Collider ---")

all_keys = list(vector_map.keys())
n = len(all_keys)
total_pairs = n * (n - 1) // 2
print(f"Computing {total_pairs} pairwise interactions for {n} proteins...")

collider_results = []

for i, key_a in enumerate(all_keys):
    for j, key_b in enumerate(all_keys):
        if j <= i:
            continue
        
        vec_a = vector_map[key_a]
        vec_b = vector_map[key_b]
        
        # XOR product
        xor = [a ^ b for a, b in zip(vec_a, vec_b)]
        
        # Hamming distance
        hamming = sum(xor)
        
        # Golay snap of XOR product
        snapped_vec, snap_info = ge.snap_to_codeword(xor)
        gap = snap_info.get('anchor_distance', 0) if isinstance(snap_info, dict) else snap_info
        
        # Interaction NRCI (hyperbolic coherence of XOR)
        # NRCI = 1 - hamming/24 (simplified coherence measure)
        interaction_nrci = round(1.0 - hamming / 24.0, 6)
        
        # Classify binding affinity
        if gap == 0 and hamming <= 4:
            binding_class = "PERFECT_RESONANCE"
            affinity_label = "Very High (sub-nM)"
        elif gap == 0 and hamming <= 8:
            binding_class = "STRONG_RESONANCE"
            affinity_label = "High (1-10 nM)"
        elif gap == 0 and hamming <= 12:
            binding_class = "MODERATE_RESONANCE"
            affinity_label = "Moderate (10-100 nM)"
        elif gap == 0:
            binding_class = "WEAK_RESONANCE"
            affinity_label = "Low (100-1000 nM)"
        elif gap <= 3:
            binding_class = "NEAR_RESONANCE"
            affinity_label = "Marginal (>1 μM)"
        else:
            binding_class = "NO_RESONANCE"
            affinity_label = "None"
        
        group_a = proteins_raw[key_a]['group']
        group_b = proteins_raw[key_b]['group']
        
        # Biological relevance
        bio_relevant = False
        bio_context = ""
        
        if (group_a in ['CoV2_Structural', 'CoV2_Variants'] and group_b == 'Host') or \
           (group_b in ['CoV2_Structural', 'CoV2_Variants'] and group_a == 'Host'):
            bio_relevant = True
            bio_context = "Viral entry"
        
        if (group_a == 'Antibody' and 'CoV2' in group_b) or \
           (group_b == 'Antibody' and 'CoV2' in group_a):
            bio_relevant = True
            bio_context = "Ab-Ag neutralization"
        
        if (group_a == 'Antibody' and group_b == 'HIV') or \
           (group_b == 'Antibody' and group_a == 'HIV'):
            bio_relevant = True
            bio_context = "HIV neutralization"
        
        if (group_a == 'Antibody' and group_b == 'Ebola') or \
           (group_b == 'Antibody' and group_a == 'Ebola'):
            bio_relevant = True
            bio_context = "Ebola neutralization"
        
        if (group_a == 'Therapeutic' and group_b in ['Influenza', 'CoV2_Nonstructural']) or \
           (group_b == 'Therapeutic' and group_a in ['Influenza', 'CoV2_Nonstructural']):
            bio_relevant = True
            bio_context = "Drug-target"
        
        if group_a == 'CoV2_Variants' and group_b == 'CoV2_Variants':
            bio_relevant = True
            bio_context = "Variant comparison"
        
        if group_a == 'HIV' and group_b == 'Host':
            bio_relevant = True
            bio_context = "HIV-host interaction"
        
        collider_results.append({
            "protein_a": key_a,
            "protein_b": key_b,
            "group_a": group_a,
            "group_b": group_b,
            "hamming_distance": hamming,
            "gap_score": gap,
            "interaction_nrci": interaction_nrci,
            "binding_class": binding_class,
            "affinity_label": affinity_label,
            "bio_relevant": bio_relevant,
            "bio_context": bio_context
        })

print(f"Collider: {len(collider_results)} interactions computed")

# ============================================================
# STEP 3: TGIC ENERGY LANDSCAPE — KEY INTERACTIONS
# ============================================================
print("\n--- Step 3: TGIC Energy Landscape ---")

key_interactions = [
    # SARS-CoV-2 variant entry
    ("SARS2_SPIKE_WT", "HOST_ACE2", "SARS-CoV-2 WT entry"),
    ("SARS2_ALPHA_SPIKE", "HOST_ACE2", "Alpha variant entry"),
    ("SARS2_BETA_SPIKE", "HOST_ACE2", "Beta variant entry"),
    ("SARS2_GAMMA_SPIKE", "HOST_ACE2", "Gamma variant entry"),
    ("SARS2_DELTA_SPIKE", "HOST_ACE2", "Delta variant entry"),
    ("SARS2_OMICRON_BA1", "HOST_ACE2", "Omicron BA.1 entry"),
    ("SARS2_OMICRON_BA2", "HOST_ACE2", "Omicron BA.2 entry"),
    ("SARS2_OMICRON_BA45", "HOST_ACE2", "Omicron BA.4/5 entry"),
    ("SARS2_OMICRON_XBB", "HOST_ACE2", "Omicron XBB.1.5 entry"),
    ("SARS2_OMICRON_JN1", "HOST_ACE2", "Omicron JN.1 entry"),
    # Antibody neutralization
    ("AB_CR3022", "SARS2_SPIKE_RBD", "CR3022 neutralization"),
    ("AB_S309_SOTROVIMAB", "SARS2_SPIKE_RBD", "S309/Sotrovimab neutralization"),
    ("AB_LY_COV555_BAMA", "SARS2_SPIKE_RBD", "Bamlanivimab neutralization"),
    ("AB_REGN10933_CASIRI", "SARS2_SPIKE_RBD", "Casirivimab neutralization"),
    # HIV
    ("HIV_GP120", "HOST_CD4", "HIV entry via CD4"),
    ("AB_VRC01_HIV", "HIV_GP120", "VRC01 HIV neutralization"),
    ("AB_2G12_HIV", "HIV_GP120", "2G12 HIV neutralization"),
    # Influenza
    ("FLU_HA_H1N1", "HOST_ACE2", "H1N1 cross-reactivity check"),
    ("FLU_HA_H5N1", "HOST_ACE2", "H5N1 cross-reactivity check"),
    ("DRUG_OSELTAMIVIR", "FLU_NA_N1", "Oseltamivir-NA1 binding"),
    ("DRUG_OSELTAMIVIR", "FLU_NA_N2", "Oseltamivir-NA2 binding"),
    # Ebola
    ("EBOLA_GP", "HOST_DCSIGN", "Ebola entry via DC-SIGN"),
    ("AB_MAB114_EBOLA", "EBOLA_GP", "mAb114 Ebola neutralization"),
    # Drug-target
    ("DRUG_REMDESIVIR", "SARS2_NSP12_RDRP", "Remdesivir-RdRp binding"),
    ("DRUG_DEXAMETHASONE", "HOST_ACE2", "Dexamethasone host modulation"),
    # Cross-pathogen comparisons
    ("SARS2_SPIKE_WT", "FLU_HA_H3N2", "CoV2 vs Flu cross-reactivity"),
    ("SARS2_SPIKE_WT", "HIV_GP120", "CoV2 vs HIV cross-reactivity"),
    ("SARS2_SPIKE_WT", "EBOLA_GP", "CoV2 vs Ebola cross-reactivity"),
]

energy_landscape = []
for key_a, key_b, context in key_interactions:
    if key_a not in vector_map or key_b not in vector_map:
        print(f"  SKIP: {key_a} or {key_b} not in vector map")
        continue
    
    vec_a = vector_map[key_a]
    vec_b = vector_map[key_b]
    
    # Build TGIC substrate with OffBit objects
    S = {
        0: OffBit(v=tuple(vec_a), phi=0),
        1: OffBit(v=tuple(vec_b), phi=0)
    }
    
    # Compute total energy
    total_energy = float(tgic_eng.get_total_energy(S))
    
    # Compute individual node energies
    energy_a = float(tgic_eng.get_node_energy(0, vec_a, S))
    energy_b = float(tgic_eng.get_node_energy(1, vec_b, S))
    
    # Relational pull (binding strength)
    pull_a = float(tgic_eng.get_relational_pull(0, vec_a, S))
    pull_b = float(tgic_eng.get_relational_pull(1, vec_b, S))
    
    # Hamming
    hamming = sum(a ^ b for a, b in zip(vec_a, vec_b))
    
    energy_landscape.append({
        "protein_a": key_a,
        "protein_b": key_b,
        "biological_context": context,
        "tgic_total_energy": round(total_energy, 4),
        "energy_a": round(energy_a, 4),
        "energy_b": round(energy_b, 4),
        "relational_pull_a": round(pull_a, 4),
        "relational_pull_b": round(pull_b, 4),
        "hamming_distance": hamming,
        "delta_e_vs_wt": None
    })
    print(f"  {context}: E_total={total_energy:.4f}, Pull={pull_a:.4f}, H={hamming}")

# Compute ΔE relative to WT+ACE2
wt_ace2 = next((e for e in energy_landscape 
                if e['protein_a'] == 'SARS2_SPIKE_WT' and e['protein_b'] == 'HOST_ACE2'), None)
if wt_ace2:
    wt_e = wt_ace2['tgic_total_energy']
    for e in energy_landscape:
        if 'entry' in e['biological_context'].lower() and 'ACE2' in e['biological_context']:
            e['delta_e_vs_wt'] = round(e['tgic_total_energy'] - wt_e, 4)

# ============================================================
# STEP 4: VARIANT FITNESS RANKING
# ============================================================
print("\n--- Step 4: Variant Fitness Ranking ---")

variant_keys = [k for k in all_keys if proteins_raw[k]['group'] == 'CoV2_Variants']
variant_keys.insert(0, 'SARS2_SPIKE_WT')  # Add WT

variant_ranking = []
for key in variant_keys:
    if key not in tax_map:
        continue
    prot = proteins_raw[key]
    var_meta = prot.get('variant_metadata', {})
    
    # Get TGIC energy with ACE2
    ace2_interaction = next((e for e in energy_landscape 
                             if e['protein_a'] == key and e['protein_b'] == 'HOST_ACE2'), None)
    
    variant_ranking.append({
        "key": key,
        "name": prot['name'][:60],
        "leech_tax": round(tax_map[key], 6),
        "tilt_degrees": tilt_map[key],
        "nrci": round(nrci_map[key], 6),
        "r0_approx": var_meta.get('r0_approx', 3.5),
        "transmissibility_class": var_meta.get('transmissibility_class', 'Moderate'),
        "mutations": var_meta.get('mutations', 0),
        "stabilizing": var_meta.get('stabilizing', 0),
        "destabilizing": var_meta.get('destabilizing', 0),
        "clinical_notes": var_meta.get('clinical_notes', 'Ancestral strain'),
        "tgic_ace2_energy": ace2_interaction['tgic_total_energy'] if ace2_interaction else None,
        "delta_e_vs_wt": ace2_interaction['delta_e_vs_wt'] if ace2_interaction else None
    })

variant_ranking.sort(key=lambda x: x['r0_approx'])
print(f"Ranked {len(variant_ranking)} variants")
for v in variant_ranking:
    print(f"  {v['key']}: Tax={v['leech_tax']:.4f}, Tilt={v['tilt_degrees']}°, R0~{v['r0_approx']}, E_ACE2={v['tgic_ace2_energy']}")

# ============================================================
# STEP 5: THERAPEUTIC SCREENING
# ============================================================
print("\n--- Step 5: Therapeutic Screening ---")

therapeutic_keys = [k for k in all_keys if proteins_raw[k]['group'] in ['Antibody', 'Therapeutic']]
target_keys = [k for k in all_keys if proteins_raw[k]['group'] not in ['Antibody', 'Therapeutic', 'Host']]

screening_results = []
for t_key in therapeutic_keys:
    prot_t = proteins_raw[t_key]
    t_meta = prot_t.get('therapeutic_metadata', {})
    target_key_lit = t_meta.get('target', '')
    known_ic50 = t_meta.get('known_ic50_nM')
    
    for ag_key in target_keys:
        # Find pair in collider
        pair = next((r for r in collider_results 
                     if (r['protein_a'] == t_key and r['protein_b'] == ag_key) or
                        (r['protein_a'] == ag_key and r['protein_b'] == t_key)), None)
        
        if pair is None:
            continue
        
        hamming = pair['hamming_distance']
        gap = pair['gap_score']
        
        # Predict affinity
        if gap == 0 and hamming <= 6:
            affinity = "VERY_HIGH"
            ic50_pred = "0.01-0.1 nM"
        elif gap == 0 and hamming <= 10:
            affinity = "HIGH"
            ic50_pred = "0.1-10 nM"
        elif gap == 0 and hamming <= 14:
            affinity = "MODERATE"
            ic50_pred = "10-100 nM"
        elif gap == 0:
            affinity = "LOW"
            ic50_pred = "100-1000 nM"
        else:
            affinity = "NEGLIGIBLE"
            ic50_pred = ">1000 nM"
        
        # Validation
        validation = "UNKNOWN"
        if known_ic50 is not None:
            if affinity in ["VERY_HIGH", "HIGH"] and known_ic50 < 10:
                validation = "CONFIRMED_HIGH_AFFINITY"
            elif affinity == "MODERATE" and 10 <= known_ic50 < 100:
                validation = "CONFIRMED_MODERATE"
            elif affinity == "LOW" and known_ic50 >= 100:
                validation = "CONFIRMED_LOW"
            elif affinity in ["VERY_HIGH", "HIGH"] and known_ic50 >= 100:
                validation = "OVERPREDICTED"
            elif affinity in ["LOW", "NEGLIGIBLE"] and known_ic50 < 10:
                validation = "UNDERPREDICTED"
            else:
                validation = "PARTIAL_MATCH"
        
        is_target_match = (target_key_lit in ag_key or ag_key in target_key_lit)
        is_bio_relevant = pair.get('bio_relevant', False)
        
        if is_target_match or is_bio_relevant or hamming <= 8:
            screening_results.append({
                "therapeutic": t_key,
                "therapeutic_name": prot_t['name'][:60],
                "antigen": ag_key,
                "antigen_name": proteins_raw[ag_key]['name'][:60],
                "hamming_distance": hamming,
                "gap_score": gap,
                "interaction_nrci": pair['interaction_nrci'],
                "predicted_affinity": affinity,
                "predicted_ic50_range": ic50_pred,
                "known_ic50_nM": known_ic50,
                "validation": validation,
                "is_primary_target": is_target_match
            })

print(f"Screening: {len(screening_results)} therapeutic-antigen interactions")

# ============================================================
# STEP 6: STATISTICAL VALIDATION
# ============================================================
print("\n--- Step 6: Statistical Validation ---")

# Tax vs R0 correlation
variant_data = [(v['leech_tax'], v['r0_approx']) for v in variant_ranking if v['r0_approx'] > 0]
taxes = [d[0] for d in variant_data]
r0s = [d[1] for d in variant_data]

n_v = len(taxes)
mean_tax = sum(taxes) / n_v
mean_r0 = sum(r0s) / n_v
cov = sum((t - mean_tax) * (r - mean_r0) for t, r in zip(taxes, r0s)) / n_v
std_tax = math.sqrt(sum((t - mean_tax)**2 for t in taxes) / n_v)
std_r0 = math.sqrt(sum((r - mean_r0)**2 for r in r0s) / n_v)
pearson_tax_r0 = cov / (std_tax * std_r0) if (std_tax * std_r0) > 0 else 0

# Tilt vs R0 correlation
tilts = [v['tilt_degrees'] for v in variant_ranking if v['r0_approx'] > 0]
mean_tilt = sum(tilts) / n_v
cov_tilt = sum((t - mean_tilt) * (r - mean_r0) for t, r in zip(tilts, r0s)) / n_v
std_tilt = math.sqrt(sum((t - mean_tilt)**2 for t in tilts) / n_v)
pearson_tilt_r0 = cov_tilt / (std_tilt * std_r0) if (std_tilt * std_r0) > 0 else 0

# TGIC energy vs R0 correlation
energy_data = [(v['tgic_ace2_energy'], v['r0_approx']) for v in variant_ranking 
               if v['tgic_ace2_energy'] is not None and v['r0_approx'] > 0]
energies = [d[0] for d in energy_data]
r0s_e = [d[1] for d in energy_data]
pearson_energy_r0 = 0
if len(energies) >= 3:
    n_e = len(energies)
    mean_e = sum(energies) / n_e
    mean_r0_e = sum(r0s_e) / n_e
    cov_e = sum((e - mean_e) * (r - mean_r0_e) for e, r in zip(energies, r0s_e)) / n_e
    std_e = math.sqrt(sum((e - mean_e)**2 for e in energies) / n_e)
    std_r0_e = math.sqrt(sum((r - mean_r0_e)**2 for r in r0s_e) / n_e)
    pearson_energy_r0 = cov_e / (std_e * std_r0_e) if (std_e * std_r0_e) > 0 else 0

# Hamming vs IC50 correlation
ab_data = [(r['hamming_distance'], r['known_ic50_nM']) 
           for r in screening_results 
           if r['known_ic50_nM'] is not None and r['is_primary_target']]
pearson_gap_ic50 = 0
if len(ab_data) >= 3:
    gaps = [d[0] for d in ab_data]
    ic50s = [math.log10(d[1] + 0.001) for d in ab_data]
    mean_gap = sum(gaps) / len(gaps)
    mean_ic50 = sum(ic50s) / len(ic50s)
    cov_ab = sum((g - mean_gap) * (i - mean_ic50) for g, i in zip(gaps, ic50s)) / len(gaps)
    std_gap = math.sqrt(sum((g - mean_gap)**2 for g in gaps) / len(gaps))
    std_ic50 = math.sqrt(sum((i - mean_ic50)**2 for i in ic50s) / len(ic50s))
    pearson_gap_ic50 = cov_ab / (std_gap * std_ic50) if (std_gap * std_ic50) > 0 else 0

print(f"  Tax vs R0:           r = {pearson_tax_r0:.4f} (n={n_v})")
print(f"  Tilt vs R0:          r = {pearson_tilt_r0:.4f} (n={n_v})")
print(f"  TGIC Energy vs R0:   r = {pearson_energy_r0:.4f} (n={len(energies)})")
print(f"  Hamming vs log(IC50): r = {pearson_gap_ic50:.4f} (n={len(ab_data)})")

# ============================================================
# STEP 7: PREDICTIVE SURVEILLANCE PIPELINE
# ============================================================
print("\n--- Step 7: Predictive Surveillance Pipeline ---")

def classify_risk(tax, tilt, mutations=0):
    risk_score = 0
    if tax < 3.5: risk_score += 4
    elif tax < 4.0: risk_score += 3
    elif tax < 4.5: risk_score += 2
    else: risk_score += 1
    
    if tilt < 45: risk_score += 4
    elif tilt < 90: risk_score += 3
    elif tilt < 120: risk_score += 2
    else: risk_score += 1
    
    if mutations >= 30: risk_score += 3
    elif mutations >= 20: risk_score += 2
    elif mutations >= 10: risk_score += 1
    
    if risk_score >= 9: return "CRITICAL", risk_score
    elif risk_score >= 7: return "HIGH", risk_score
    elif risk_score >= 5: return "MODERATE", risk_score
    elif risk_score >= 3: return "LOW", risk_score
    else: return "MINIMAL", risk_score

surveillance_results = []
for key in all_keys:
    if key not in tax_map:
        continue
    prot = proteins_raw[key]
    var_meta = prot.get('variant_metadata', {})
    mutations = var_meta.get('mutations', 0)
    risk_class, risk_score = classify_risk(tax_map[key], tilt_map[key], mutations)
    
    surveillance_results.append({
        "key": key,
        "name": prot['name'][:60],
        "group": prot['group'],
        "leech_tax": round(tax_map[key], 6),
        "tilt_degrees": tilt_map[key],
        "nrci": round(nrci_map[key], 6),
        "mutations": mutations,
        "risk_class": risk_class,
        "risk_score": risk_score,
        "r0_approx": var_meta.get('r0_approx', None)
    })

surveillance_results.sort(key=lambda x: x['risk_score'], reverse=True)
print("Top 10 highest-risk proteins:")
for r in surveillance_results[:10]:
    print(f"  {r['key']}: {r['risk_class']} (score={r['risk_score']}, Tax={r['leech_tax']:.4f}, Tilt={r['tilt_degrees']}°)")

# ============================================================
# COMPILE AND SAVE FULL REPORT
# ============================================================
print("\n--- Compiling Full Report ---")

from collections import Counter
groups = Counter(proteins_raw[k]['group'] for k in all_keys)

full_report = {
    "study_metadata": {
        "title": "UBP Geometric Virology v3.0 — Geometric Virome",
        "version": "3.0",
        "date": "2026-03-08",
        "proteins_analyzed": len(kb_entries),
        "total_pairwise_interactions": len(collider_results),
        "tgic_energy_points": len(energy_landscape),
        "ubp_engine": "UBP Core v5.7",
        "data_sources": ["UniProt REST API", "Published Literature (Tortorici 2020, Pinto 2020, Shi 2020, Cao 2022, Planas 2021)"]
    },
    "kb_summary": {
        "total_entries": len(kb_entries),
        "groups": dict(groups)
    },
    "statistical_validation": {
        "pearson_tax_vs_r0": round(pearson_tax_r0, 4),
        "pearson_tilt_vs_r0": round(pearson_tilt_r0, 4),
        "pearson_tgic_energy_vs_r0": round(pearson_energy_r0, 4),
        "pearson_hamming_vs_log_ic50": round(pearson_gap_ic50, 4),
        "n_variants": n_v,
        "n_ab_pairs": len(ab_data),
        "interpretation": {
            "tax_r0": f"r={pearson_tax_r0:.4f}: {'Strong negative — lower Tax predicts higher R0' if pearson_tax_r0 < -0.5 else 'Moderate' if abs(pearson_tax_r0) > 0.3 else 'Weak'}",
            "tilt_r0": f"r={pearson_tilt_r0:.4f}: {'Strong negative — lower Tilt predicts higher transmissibility' if pearson_tilt_r0 < -0.5 else 'Moderate' if abs(pearson_tilt_r0) > 0.3 else 'Weak'}",
            "energy_r0": f"r={pearson_energy_r0:.4f}: {'Strong — TGIC energy correlates with R0' if abs(pearson_energy_r0) > 0.5 else 'Moderate' if abs(pearson_energy_r0) > 0.3 else 'Weak'}",
            "gap_ic50": f"r={pearson_gap_ic50:.4f}: {'Strong — Hamming distance predicts antibody potency' if abs(pearson_gap_ic50) > 0.5 else 'Moderate' if abs(pearson_gap_ic50) > 0.3 else 'Weak'}"
        }
    },
    "variant_fitness_ranking": variant_ranking,
    "discovery_collider_summary": {
        "total_interactions": len(collider_results),
        "bio_relevant": sum(1 for r in collider_results if r['bio_relevant']),
        "binding_classes": dict(Counter(r['binding_class'] for r in collider_results))
    },
    "discovery_collider_bio_relevant": [r for r in collider_results if r['bio_relevant']],
    "therapeutic_screening": screening_results,
    "tgic_energy_landscape": energy_landscape,
    "surveillance_pipeline": surveillance_results,
    "vector_map": {k: v for k, v in vector_map.items()},
    "tax_map": {k: round(v, 6) for k, v in tax_map.items()},
    "tilt_map": tilt_map,
    "nrci_map": {k: round(v, 6) for k, v in nrci_map.items()}
}

with open('/home/ubuntu/ubp_v3_full_report.json', 'w') as f:
    json.dump(full_report, f, indent=2, default=str)

print(f"\n=== SIMULATION COMPLETE ===")
print(f"Proteins: {len(kb_entries)}")
print(f"Pairwise interactions: {len(collider_results)}")
print(f"Biologically relevant: {sum(1 for r in collider_results if r['bio_relevant'])}")
print(f"Therapeutic screenings: {len(screening_results)}")
print(f"TGIC energy points: {len(energy_landscape)}")
print(f"\nKey Correlations:")
print(f"  Tax vs R0:            r = {pearson_tax_r0:.4f}")
print(f"  Tilt vs R0:           r = {pearson_tilt_r0:.4f}")
print(f"  TGIC Energy vs R0:    r = {pearson_energy_r0:.4f}")
print(f"  Hamming vs log(IC50): r = {pearson_gap_ic50:.4f}")
print(f"\nReport saved to ubp_v3_full_report.json")
