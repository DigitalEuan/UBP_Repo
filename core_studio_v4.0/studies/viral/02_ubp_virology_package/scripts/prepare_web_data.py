"""Prepare web data for the interactive HTML tool."""
import json
from fractions import Fraction

with open('/home/ubuntu/virology_kb_entries_v2.json') as f:
    kb = json.load(f)
with open('/home/ubuntu/ubp_virology_full_report_v2.json') as f:
    report = json.load(f)
with open('/home/ubuntu/ubp_validation_report.json') as f:
    validation = json.load(f)

proteins = []
for fp, entry in kb.items():
    lexicon_str = entry['lexicon']
    # Parse: "[Name], [Definition]"
    parts = lexicon_str.split('], [')
    name = parts[0].lstrip('[') if parts else lexicon_str
    definition = parts[1].rstrip(']') if len(parts) > 1 else ''
    
    tax_val = float(Fraction(entry['atlas']['tax']))
    
    # Determine category
    uid = entry['ubp_id']
    if 'ANTIBODY' in uid:
        category = 'Antibody'
        color = '#06d6a0'
    elif 'ACE2' in uid:
        category = 'Host Receptor'
        color = '#00b4d8'
    elif 'OMICRON' in uid:
        category = 'Variant (Omicron)'
        color = '#ef233c'
    elif 'DELTA' in uid:
        category = 'Variant (Delta)'
        color = '#f77f00'
    elif 'INFLUENZA' in uid:
        category = 'Influenza'
        color = '#7209b7'
    elif 'HIV' in uid:
        category = 'HIV'
        color = '#ffd60a'
    else:
        category = 'SARS-CoV-2'
        color = '#1a3a5c'
    
    proteins.append({
        'id': uid,
        'short': uid.replace('PROTEIN_', '').replace('_001', '').replace('VIRAL_', '').replace('HOST_', '').replace('ANTIBODY_', 'Ab_'),
        'name': name,
        'definition': definition,
        'math': entry['math'],
        'vector': entry['atlas']['vector'],
        'nrci': round(entry['atlas']['nrci_score'], 6),
        'tax': round(tax_val, 6),
        'tilt': entry['atlas']['tilt'],
        'tags': entry.get('tags', []),
        'category': category,
        'color': color
    })

# Collider results - take all 66
collider = report['sections']['1_discovery_collider']

# Variants
variants_raw = report['sections']['2_variant_evolution']
variants = []
for name, d in variants_raw.items():
    variants.append({
        'name': name,
        'tax': round(d['leech_tax'], 6),
        'tilt': d['tilt_degrees'],
        'nrci': d['nrci'],
        'zone': d['stability_zone'],
        'stabilizing': d['stabilizing_mutations'],
        'destabilizing': d['destabilizing_mutations']
    })

# Cytokine
cs = report['sections']['3_cytokine_storm']
cytokine = {
    'mild': {'nrci': cs['mild_state']['nrci'], 'tax': cs['mild_state']['tax']},
    'storm': {'nrci': cs['cytokine_storm_state']['nrci'], 'tax': cs['cytokine_storm_state']['tax']},
    'interventions': [
        {'name': i['name'], 'tax': i['treated_tax'], 'nrci': i['treated_nrci'],
         'tax_reduction': i['tax_reduction'], 'evidence': i['clinical_evidence']}
        for i in cs['interventions']
    ]
}

# Antibody
antibody_raw = report['sections']['5_antibody_efficacy']
antibody = []
for key, d in antibody_raw.items():
    antibody.append({
        'key': key,
        'antibody': d['antibody'],
        'antigen': d['antigen'],
        'hamming': d['hamming_distance'],
        'gap': d['gap_score'],
        'nrci': d['interaction_nrci'],
        'affinity': d['predicted_affinity'],
        'ic50_range': d['predicted_ic50_range_nM'],
        'known_ic50': d['known_ic50_nM'],
        'validation': d['ubp_clinical_validation']
    })

# Energy landscape
landscape = validation['energy_landscape']

# Validation
validations = validation['validations']

data = {
    'proteins': proteins,
    'collider': collider,
    'variants': variants,
    'cytokine': cytokine,
    'antibody': antibody,
    'landscape': landscape,
    'validations': validations
}

with open('/home/ubuntu/ubp_virology_web_data.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print(f'Web data saved: {len(proteins)} proteins, {len(collider)} interactions, {len(landscape)} energy points')
