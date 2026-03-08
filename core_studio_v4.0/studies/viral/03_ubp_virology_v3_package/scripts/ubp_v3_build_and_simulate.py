"""
UBP Geometric Virology v3.0 — Full Geometric Virome KB Builder + Simulation Engine
Builds SOP_002 KB entries for all 53 proteins and runs the complete simulation suite.
Uses UBP Core v5.3 modules: KBArchitect, LeechEngine, DiscoveryEngine, TGICEngine.
"""
import json
import sys
import os
import math
from fractions import Fraction
from itertools import combinations

# Add UBP core to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/core_studio_v4.0/core')

# Import UBP modules
from ubp_core_v5_3_merged import (
    golay_encode, golay_decode, leech_tax, leech_tilt,
    nrci_hyperbolic, compute_tgic_exact
)
from ubp_kb_architect import KBArchitect

print("=== UBP Geometric Virology v3.0 — Full Simulation Suite ===")
print("Loading protein data...")

with open('/home/ubuntu/ubp_v3_protein_data_raw.json') as f:
    proteins_raw = json.load(f)

print(f"Loaded {len(proteins_raw)} proteins")

# ============================================================
# STEP 1: BUILD SOP_002 KB ENTRIES
# ============================================================
print("\n--- Step 1: Building SOP_002 KB Entries ---")

architect = KBArchitect()

kb_entries = {}
vector_map = {}  # key -> 24-bit vector
tax_map = {}     # key -> leech tax
tilt_map = {}    # key -> tilt angle
nrci_map = {}    # key -> NRCI

for key, prot in proteins_raw.items():
    math_dna = prot['math_dna']
    
    # Build lexicon string
    lexicon = f"[Protein: {prot['name']}], [{prot['definition'][:200]}]"
    
    # Determine tags
    tags = [prot['group'], prot['organism'].split()[0]]
    if 'variant_metadata' in prot:
        tags.append('VoC')
        tags.append(f"R0_{prot['variant_metadata']['transmissibility_class'].replace(' ', '_')}")
    if 'therapeutic_metadata' in prot:
        tags.append('Therapeutic')
        tags.append(prot['therapeutic_metadata'].get('mechanism', '').split()[0])
    
    # Build KB entry using KBArchitect
    entry = architect.build_entry(
        ubp_id=f"PROTEIN_{key}_001",
        lexicon=lexicon,
        math_dna=math_dna,
        tags=tags,
        fingerprint=f"UBP_VIROLOGY_V3_{key}"
    )
    
    kb_entries[key] = entry
    
    # Extract vector and compute metrics
    vector = entry['atlas']['vector']
    vector_map[key] = vector
    
    # Compute Leech Tax
    tax_val = float(Fraction(entry['atlas']['tax']))
    tax_map[key] = tax_val
    
    # Compute Tilt
    tilt_map[key] = entry['atlas']['tilt']
    
    # Compute NRCI
    nrci_map[key] = entry['atlas']['nrci_score']
    
    print(f"  {key}: vector={vector[:8]}..., tax={tax_val:.4f}, tilt={entry['atlas']['tilt']}°, NRCI={entry['atlas']['nrci_score']:.6f}")

print(f"\nBuilt {len(kb_entries)} KB entries")

# Save KB
with open('/home/ubuntu/ubp_v3_geometric_virome_kb.json', 'w') as f:
    json.dump(kb_entries, f, indent=2, default=str)
print("KB saved to ubp_v3_geometric_virome_kb.json")

# ============================================================
# STEP 2: DISCOVERY ENGINE COLLIDER — ALL PAIRS
# ============================================================
print("\n--- Step 2: Discovery Engine Collider ---")

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
        
        # Golay decode the XOR product
        decoded, gap = golay_decode(xor)
        
        # Interaction NRCI
        interaction_nrci = nrci_hyperbolic(hamming, 24)
        
        # Classify binding
        if gap == 0 and hamming <= 4:
            binding_class = "PERFECT_RESONANCE|Potential high-affinity binding"
        elif gap == 0 and hamming <= 8:
            binding_class = "STRONG_RESONANCE|Moderate-high affinity"
        elif gap == 0 and hamming <= 12:
            binding_class = "MODERATE_RESONANCE|Moderate affinity"
        elif gap == 0:
            binding_class = "WEAK_RESONANCE|Low affinity"
        elif gap <= 3:
            binding_class = "NEAR_RESONANCE|Marginal interaction"
        else:
            binding_class = "NO_RESONANCE|No significant interaction"
        
        # Get group info for biological context
        group_a = proteins_raw[key_a]['group']
        group_b = proteins_raw[key_b]['group']
        
        # Determine biological relevance
        bio_relevant = False
        bio_context = ""
        
        # Virus-host interactions
        if (group_a in ['CoV2_Structural', 'CoV2_Variants'] and group_b == 'Host') or \
           (group_b in ['CoV2_Structural', 'CoV2_Variants'] and group_a == 'Host'):
            bio_relevant = True
            bio_context = "Viral entry interaction"
        
        # Antibody-antigen interactions
        if (group_a == 'Antibody' and 'CoV2' in group_b) or \
           (group_b == 'Antibody' and 'CoV2' in group_a):
            bio_relevant = True
            bio_context = "Antibody neutralization"
        
        if (group_a == 'Antibody' and group_b == 'HIV') or \
           (group_b == 'Antibody' and group_a == 'HIV'):
            bio_relevant = True
            bio_context = "HIV antibody interaction"
        
        if (group_a == 'Antibody' and group_b == 'Ebola') or \
           (group_b == 'Antibody' and group_a == 'Ebola'):
            bio_relevant = True
            bio_context = "Ebola antibody interaction"
        
        # Drug-target interactions
        if (group_a == 'Therapeutic' and group_b == 'Influenza') or \
           (group_b == 'Therapeutic' and group_a == 'Influenza'):
            bio_relevant = True
            bio_context = "Antiviral drug-target"
        
        if (group_a == 'Therapeutic' and 'CoV2' in group_b) or \
           (group_b == 'Therapeutic' and 'CoV2' in group_a):
            bio_relevant = True
            bio_context = "COVID-19 therapeutic"
        
        # Variant comparisons
        if group_a == 'CoV2_Variants' and group_b == 'CoV2_Variants':
            bio_relevant = True
            bio_context = "Variant comparison"
        
        collider_results.append({
            "protein_a": key_a,
            "protein_b": key_b,
            "group_a": group_a,
            "group_b": group_b,
            "hamming_distance": hamming,
            "gap_score": gap,
            "interaction_nrci": round(interaction_nrci, 6),
            "binding_class": binding_class,
            "bio_relevant": bio_relevant,
            "bio_context": bio_context
        })

print(f"Collider complete: {len(collider_results)} interactions computed")

# ============================================================
# STEP 3: VARIANT FITNESS RANKING
# ============================================================
print("\n--- Step 3: Variant Fitness Ranking ---")

variant_keys = [k for k in all_keys if proteins_raw[k]['group'] == 'CoV2_Variants']
variant_keys += ['SARS2_SPIKE_WT']  # Add WT for comparison

variant_ranking = []
for key in variant_keys:
    prot = proteins_raw[key]
    var_meta = prot.get('variant_metadata', {})
    
    variant_ranking.append({
        "key": key,
        "name": prot['name'],
        "leech_tax": round(tax_map[key], 6),
        "tilt_degrees": tilt_map[key],
        "nrci": round(nrci_map[key], 6),
        "r0_approx": var_meta.get('r0_approx', 3.5),  # WT R0 ~3.5
        "transmissibility_class": var_meta.get('transmissibility_class', 'Moderate'),
        "mutations": var_meta.get('mutations', 0),
        "stabilizing": var_meta.get('stabilizing', 0),
        "destabilizing": var_meta.get('destabilizing', 0),
        "clinical_notes": var_meta.get('clinical_notes', 'Ancestral strain')
    })

# Sort by R0 (ascending) to show progression
variant_ranking.sort(key=lambda x: x['r0_approx'])
print(f"Ranked {len(variant_ranking)} variants by R0")

# ============================================================
# STEP 4: ANTIBODY THERAPEUTIC SCREENING
# ============================================================
print("\n--- Step 4: Antibody/Therapeutic Screening ---")

therapeutic_keys = [k for k in all_keys if proteins_raw[k]['group'] in ['Antibody', 'Therapeutic']]
target_keys = [k for k in all_keys if proteins_raw[k]['group'] not in ['Antibody', 'Therapeutic', 'Host']]

screening_results = []
for t_key in therapeutic_keys:
    prot_t = proteins_raw[t_key]
    t_meta = prot_t.get('therapeutic_metadata', {})
    target_key_lit = t_meta.get('target', '')
    
    for ag_key in target_keys:
        # Find this pair in collider results
        pair = next((r for r in collider_results 
                     if (r['protein_a'] == t_key and r['protein_b'] == ag_key) or
                        (r['protein_a'] == ag_key and r['protein_b'] == t_key)), None)
        
        if pair is None:
            continue
        
        hamming = pair['hamming_distance']
        gap = pair['gap_score']
        
        # Predict affinity class
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
        
        # Check against known IC50 if available
        known_ic50 = t_meta.get('known_ic50_nM')
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
        
        # Only include if target matches or is biologically relevant
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

print(f"Screening complete: {len(screening_results)} therapeutic-antigen interactions")

# ============================================================
# STEP 5: TGIC ENERGY LANDSCAPE — KEY INTERACTIONS
# ============================================================
print("\n--- Step 5: TGIC Energy Landscape ---")

# Key biological interactions to model
key_interactions = [
    # SARS-CoV-2 entry
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
    ("AB_S309_SOTROVIMAB", "SARS2_SPIKE_RBD", "S309 neutralization"),
    ("AB_LY_COV555_BAMA", "SARS2_SPIKE_RBD", "Bamlanivimab neutralization"),
    ("AB_REGN10933_CASIRI", "SARS2_SPIKE_RBD", "Casirivimab neutralization"),
    # HIV
    ("HIV_GP120", "HOST_CD4", "HIV entry via CD4"),
    ("AB_VRC01_HIV", "HIV_GP120", "VRC01 HIV neutralization"),
    # Influenza
    ("FLU_HA_H1N1", "HOST_ACE2", "H1N1 cross-reactivity"),
    ("FLU_HA_H5N1", "HOST_ACE2", "H5N1 cross-reactivity"),
    ("DRUG_OSELTAMIVIR", "FLU_NA_N1", "Oseltamivir-NA1 binding"),
    # Ebola
    ("EBOLA_GP", "HOST_DCSIGN", "Ebola entry via DC-SIGN"),
    ("AB_MAB114_EBOLA", "EBOLA_GP", "mAb114 Ebola neutralization"),
    # Drug-target
    ("DRUG_REMDESIVIR", "SARS2_NSP12_RDRP", "Remdesivir-RdRp binding"),
    ("DRUG_DEXAMETHASONE", "HOST_ACE2", "Dexamethasone host effect"),
]

energy_landscape = []
for key_a, key_b, context in key_interactions:
    if key_a not in vector_map or key_b not in vector_map:
        print(f"  SKIP: {key_a} or {key_b} not in vector map")
        continue
    
    vec_a = vector_map[key_a]
    vec_b = vector_map[key_b]
    
    # TGIC exact engine
    energy = compute_tgic_exact(vec_a, vec_b)
    
    # Also get Hamming
    hamming = sum(a ^ b for a, b in zip(vec_a, vec_b))
    
    energy_landscape.append({
        "protein_a": key_a,
        "protein_b": key_b,
        "interaction": f"{key_a} + {key_b}",
        "biological_context": context,
        "tgic_energy": round(energy, 4),
        "hamming_distance": hamming,
        "delta_e_vs_wt": None  # Will fill in next step
    })
    print(f"  {context}: E={energy:.4f}, H={hamming}")

# Compute ΔE relative to WT+ACE2 for variant comparisons
wt_ace2_energy = next((e['tgic_energy'] for e in energy_landscape 
                        if e['protein_a'] == 'SARS2_SPIKE_WT' and e['protein_b'] == 'HOST_ACE2'), None)

for e in energy_landscape:
    if 'entry' in e['biological_context'].lower() and 'HOST_ACE2' in e['protein_b']:
        if wt_ace2_energy is not None:
            e['delta_e_vs_wt'] = round(e['tgic_energy'] - wt_ace2_energy, 4)

# ============================================================
# STEP 6: STATISTICAL VALIDATION
# ============================================================
print("\n--- Step 6: Statistical Validation ---")

# Tax vs R0 correlation
variant_data = [(v['leech_tax'], v['r0_approx']) for v in variant_ranking if v['r0_approx'] > 0]
taxes = [d[0] for d in variant_data]
r0s = [d[1] for d in variant_data]

# Pearson correlation
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

# Gap Score vs IC50 correlation (for antibodies with known IC50)
ab_data = [(r['hamming_distance'], r['known_ic50_nM']) 
           for r in screening_results 
           if r['known_ic50_nM'] is not None and r['is_primary_target']]

pearson_gap_ic50 = 0
if len(ab_data) >= 3:
    gaps = [d[0] for d in ab_data]
    ic50s = [math.log10(d[1] + 0.001) for d in ab_data]  # log scale
    mean_gap = sum(gaps) / len(gaps)
    mean_ic50 = sum(ic50s) / len(ic50s)
    cov_ab = sum((g - mean_gap) * (i - mean_ic50) for g, i in zip(gaps, ic50s)) / len(gaps)
    std_gap = math.sqrt(sum((g - mean_gap)**2 for g in gaps) / len(gaps))
    std_ic50 = math.sqrt(sum((i - mean_ic50)**2 for i in ic50s) / len(ic50s))
    pearson_gap_ic50 = cov_ab / (std_gap * std_ic50) if (std_gap * std_ic50) > 0 else 0

print(f"  Pearson r (Tax vs R0): {pearson_tax_r0:.4f}")
print(f"  Pearson r (Tilt vs R0): {pearson_tilt_r0:.4f}")
print(f"  Pearson r (Hamming vs log IC50): {pearson_gap_ic50:.4f}")

# ============================================================
# STEP 7: PREDICTIVE SURVEILLANCE PIPELINE
# ============================================================
print("\n--- Step 7: Predictive Surveillance Pipeline ---")

# Build risk classifier based on Tax and Tilt
def classify_risk(tax, tilt, mutations=0):
    """Classify evolutionary risk based on UBP metrics."""
    risk_score = 0
    
    # Tax contribution (lower tax = higher fitness = higher risk)
    if tax < 3.5:
        risk_score += 4
    elif tax < 4.0:
        risk_score += 3
    elif tax < 4.5:
        risk_score += 2
    else:
        risk_score += 1
    
    # Tilt contribution (lower tilt = closer to Universal North = higher fitness)
    if tilt < 45:
        risk_score += 4
    elif tilt < 90:
        risk_score += 3
    elif tilt < 120:
        risk_score += 2
    else:
        risk_score += 1
    
    # Mutation count contribution
    if mutations >= 30:
        risk_score += 3
    elif mutations >= 20:
        risk_score += 2
    elif mutations >= 10:
        risk_score += 1
    
    # Classify
    if risk_score >= 9:
        return "CRITICAL", risk_score
    elif risk_score >= 7:
        return "HIGH", risk_score
    elif risk_score >= 5:
        return "MODERATE", risk_score
    elif risk_score >= 3:
        return "LOW", risk_score
    else:
        return "MINIMAL", risk_score

surveillance_results = []
for key in all_keys:
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

# Sort by risk score descending
surveillance_results.sort(key=lambda x: x['risk_score'], reverse=True)

print("Top 10 highest-risk proteins:")
for r in surveillance_results[:10]:
    print(f"  {r['key']}: {r['risk_class']} (score={r['risk_score']}, Tax={r['leech_tax']:.4f}, Tilt={r['tilt_degrees']}°)")

# ============================================================
# COMPILE FULL REPORT
# ============================================================
print("\n--- Compiling Full Report ---")

full_report = {
    "study_metadata": {
        "title": "UBP Geometric Virology v3.0 — Geometric Virome",
        "version": "3.0",
        "date": "2026-03-08",
        "proteins_analyzed": len(kb_entries),
        "total_interactions": len(collider_results),
        "ubp_engine": "UBP Core v5.3"
    },
    "kb_summary": {
        "total_entries": len(kb_entries),
        "groups": {}
    },
    "sections": {
        "1_variant_fitness_ranking": variant_ranking,
        "2_discovery_collider_all": collider_results,
        "3_therapeutic_screening": screening_results,
        "4_tgic_energy_landscape": energy_landscape,
        "5_statistical_validation": {
            "pearson_tax_vs_r0": round(pearson_tax_r0, 4),
            "pearson_tilt_vs_r0": round(pearson_tilt_r0, 4),
            "pearson_hamming_vs_log_ic50": round(pearson_gap_ic50, 4),
            "n_variants": n_v,
            "n_ab_pairs": len(ab_data),
            "interpretation": {
                "tax_r0": f"r={pearson_tax_r0:.4f}: {'Strong negative correlation — lower Tax predicts higher R0' if pearson_tax_r0 < -0.5 else 'Moderate correlation' if abs(pearson_tax_r0) > 0.3 else 'Weak correlation'}",
                "tilt_r0": f"r={pearson_tilt_r0:.4f}: {'Strong negative correlation — lower Tilt predicts higher transmissibility' if pearson_tilt_r0 < -0.5 else 'Moderate correlation' if abs(pearson_tilt_r0) > 0.3 else 'Weak correlation'}",
                "gap_ic50": f"r={pearson_gap_ic50:.4f}: {'Strong positive correlation — higher Hamming distance predicts weaker antibody' if pearson_gap_ic50 > 0.5 else 'Moderate correlation' if abs(pearson_gap_ic50) > 0.3 else 'Weak correlation'}"
            }
        },
        "6_surveillance_pipeline": surveillance_results
    },
    "vector_map": {k: v for k, v in vector_map.items()},
    "tax_map": {k: round(v, 6) for k, v in tax_map.items()},
    "tilt_map": tilt_map,
    "nrci_map": {k: round(v, 6) for k, v in nrci_map.items()}
}

# Group summary
from collections import Counter
groups = Counter(proteins_raw[k]['group'] for k in all_keys)
full_report['kb_summary']['groups'] = dict(groups)

with open('/home/ubuntu/ubp_v3_full_report.json', 'w') as f:
    json.dump(full_report, f, indent=2, default=str)

print(f"\n=== SIMULATION COMPLETE ===")
print(f"Proteins: {len(kb_entries)}")
print(f"Interactions: {len(collider_results)}")
print(f"Therapeutic screenings: {len(screening_results)}")
print(f"TGIC energy points: {len(energy_landscape)}")
print(f"Surveillance results: {len(surveillance_results)}")
print(f"\nKey Statistics:")
print(f"  Tax vs R0 correlation: r={pearson_tax_r0:.4f}")
print(f"  Tilt vs R0 correlation: r={pearson_tilt_r0:.4f}")
print(f"  Hamming vs log(IC50) correlation: r={pearson_gap_ic50:.4f}")
print(f"\nReport saved to ubp_v3_full_report.json")
