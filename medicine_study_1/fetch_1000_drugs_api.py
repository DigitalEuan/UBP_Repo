#!/usr/bin/env python3
"""
Fetch 1000 FDA-approved drugs from ChEMBL using REST API
Batch processing with robust error handling
"""

import requests
import pandas as pd
import json
import time
from typing import List, Dict

CHEMBL_BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

def fetch_approved_drugs_batch(offset=0, limit=100):
    """
    Fetch batch of FDA-approved drugs from ChEMBL REST API
    """
    url = f"{CHEMBL_BASE_URL}/molecule.json"
    params = {
        'max_phase': 4,  # FDA approved
        'molecule_type': 'Small molecule',
        'limit': limit,
        'offset': offset
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('molecules', [])
    except Exception as e:
        print(f"Error fetching batch at offset {offset}: {e}")
        return []

def fetch_molecule_details(chembl_id):
    """
    Fetch detailed information for a specific molecule
    """
    url = f"{CHEMBL_BASE_URL}/molecule/{chembl_id}.json"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except:
        return None

def fetch_bioactivities(chembl_id, max_activities=5):
    """
    Fetch bioactivity data for a molecule
    """
    url = f"{CHEMBL_BASE_URL}/activity.json"
    params = {
        'molecule_chembl_id': chembl_id,
        'standard_type__in': 'IC50,EC50,Ki,Kd',
        'standard_relation': '=',
        'limit': max_activities
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get('activities', [])
    except:
        return []

def process_molecule(mol_data):
    """
    Process molecule data into structured format
    """
    chembl_id = mol_data.get('molecule_chembl_id')
    
    # Basic info
    result = {
        'chembl_id': chembl_id,
        'name': mol_data.get('pref_name', 'Unknown'),
        'max_phase': mol_data.get('max_phase'),
        'first_approval': mol_data.get('first_approval'),
        'therapeutic_flag': mol_data.get('therapeutic_flag', False),
        'oral': mol_data.get('oral', False),
        'parenteral': mol_data.get('parenteral', False),
        'topical': mol_data.get('topical', False)
    }
    
    # Molecular structures
    structures = mol_data.get('molecule_structures', {})
    if structures:
        result['smiles'] = structures.get('canonical_smiles')
        result['inchi_key'] = structures.get('standard_inchi_key')
    else:
        result['smiles'] = None
        result['inchi_key'] = None
    
    # Molecular properties
    props = mol_data.get('molecule_properties', {})
    if props:
        result['molecular_weight'] = props.get('full_mw')
        result['alogp'] = props.get('alogp')
        result['hba'] = props.get('hba')
        result['hbd'] = props.get('hbd')
        result['psa'] = props.get('psa')
        result['rtb'] = props.get('rtb')
        result['aromatic_rings'] = props.get('aromatic_rings')
        result['heavy_atoms'] = props.get('heavy_atoms')
        result['num_ro5_violations'] = props.get('num_ro5_violations')
        result['molecular_species'] = props.get('molecular_species')
    else:
        for key in ['molecular_weight', 'alogp', 'hba', 'hbd', 'psa', 'rtb', 
                    'aromatic_rings', 'heavy_atoms', 'num_ro5_violations', 'molecular_species']:
            result[key] = None
    
    # Hierarchy
    hierarchy = mol_data.get('molecule_hierarchy', {})
    result['parent_chembl_id'] = hierarchy.get('parent_chembl_id')
    
    return result

def classify_therapeutic_area(indications_text):
    """
    Classify therapeutic area based on indication text
    """
    if not indications_text or indications_text == 'Unknown':
        return 'Other'
    
    text_lower = indications_text.lower()
    
    # Classification rules
    if any(term in text_lower for term in ['cancer', 'tumor', 'carcinoma', 'leukemia', 'lymphoma', 'oncology', 'neoplasm']):
        return 'Oncology'
    elif any(term in text_lower for term in ['hypertension', 'heart', 'cardiac', 'cardiovascular', 'angina', 'arrhythmia']):
        return 'Cardiovascular'
    elif any(term in text_lower for term in ['infection', 'bacterial', 'antibiotic', 'antimicrobial', 'antiviral', 'fungal', 'hiv', 'hepatitis']):
        return 'Anti-infective'
    elif any(term in text_lower for term in ['diabetes', 'glucose', 'insulin', 'metabolic', 'obesity']):
        return 'Metabolic'
    elif any(term in text_lower for term in ['depression', 'anxiety', 'schizophrenia', 'psychosis', 'seizure', 'epilepsy', 'neurological', 'alzheimer', 'parkinson']):
        return 'CNS/Neurology'
    elif any(term in text_lower for term in ['pain', 'analgesic', 'inflammation', 'arthritis', 'rheumatoid']):
        return 'Pain/Inflammation'
    elif any(term in text_lower for term in ['immune', 'autoimmune', 'transplant', 'immunosuppressant', 'lupus']):
        return 'Immunology'
    elif any(term in text_lower for term in ['respiratory', 'asthma', 'copd', 'bronchitis', 'pulmonary']):
        return 'Respiratory'
    elif any(term in text_lower for term in ['gastrointestinal', 'ulcer', 'crohn', 'colitis', 'gastric']):
        return 'Gastrointestinal'
    elif any(term in text_lower for term in ['dermatology', 'skin', 'psoriasis', 'eczema', 'dermatitis']):
        return 'Dermatology'
    else:
        return 'Other'

def fetch_drug_indications(chembl_id):
    """
    Fetch drug indications from ChEMBL
    """
    url = f"{CHEMBL_BASE_URL}/drug_indication.json"
    params = {
        'molecule_chembl_id': chembl_id,
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        indications = data.get('drug_indications', [])
        
        indication_list = []
        for ind in indications:
            if ind.get('mesh_heading'):
                indication_list.append(ind['mesh_heading'])
            elif ind.get('efo_term'):
                indication_list.append(ind['efo_term'])
        
        return '; '.join(indication_list) if indication_list else 'Unknown'
    except:
        return 'Unknown'

def main():
    """Main execution"""
    print("="*80)
    print("Fetching 1000 FDA-Approved Drugs from ChEMBL API")
    print("="*80 + "\n")
    
    target_count = 1000
    batch_size = 100
    all_drugs = []
    
    # Fetch in batches
    for batch_num in range(0, target_count, batch_size):
        print(f"\nFetching batch {batch_num//batch_size + 1} (offset {batch_num})...")
        
        molecules = fetch_approved_drugs_batch(offset=batch_num, limit=batch_size)
        
        if not molecules:
            print("No more molecules returned")
            break
        
        print(f"Processing {len(molecules)} molecules...")
        
        for mol in molecules:
            # Process molecule
            drug_data = process_molecule(mol)
            
            # Skip if no SMILES
            if not drug_data['smiles']:
                continue
            
            # Skip if no molecular weight
            if not drug_data['molecular_weight']:
                continue
            
            # Filter molecular weight range
            if drug_data['molecular_weight'] < 150 or drug_data['molecular_weight'] > 1000:
                continue
            
            # Fetch indications
            chembl_id = drug_data['chembl_id']
            indications = fetch_drug_indications(chembl_id)
            drug_data['indications'] = indications
            drug_data['therapeutic_area'] = classify_therapeutic_area(indications)
            
            # Fetch bioactivities
            activities = fetch_bioactivities(chembl_id, max_activities=10)
            activity_values = []
            target_ids = set()
            
            for act in activities:
                if act.get('standard_value'):
                    try:
                        activity_values.append(float(act['standard_value']))
                    except:
                        pass
                if act.get('target_chembl_id'):
                    target_ids.add(act['target_chembl_id'])
            
            drug_data['num_bioactivities'] = len(activity_values)
            drug_data['num_targets'] = len(target_ids)
            drug_data['mean_activity_nm'] = sum(activity_values) / len(activity_values) if activity_values else None
            
            all_drugs.append(drug_data)
            
            if len(all_drugs) >= target_count:
                break
        
        print(f"Total drugs collected: {len(all_drugs)}")
        
        if len(all_drugs) >= target_count:
            break
        
        # Rate limiting
        time.sleep(1)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_drugs)
    
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    print(f"Total compounds: {len(df)}")
    print(f"\nTherapeutic area distribution:")
    print(df['therapeutic_area'].value_counts())
    print(f"\nMolecular weight range: {df['molecular_weight'].min():.1f} - {df['molecular_weight'].max():.1f}")
    print(f"Mean molecular weight: {df['molecular_weight'].mean():.1f}")
    print(f"\nCompounds with bioactivity data: {df['num_bioactivities'].gt(0).sum()}")
    print(f"Mean targets per compound: {df['num_targets'].mean():.1f}")
    
    # Save to CSV
    output_file = '/home/ubuntu/ubp_medicine_study/chembl_1000_drugs.csv'
    df.to_csv(output_file, index=False)
    print(f"\nData saved to: {output_file}")
    
    # Save summary
    summary = {
        'total_compounds': len(df),
        'therapeutic_areas': df['therapeutic_area'].value_counts().to_dict(),
        'mw_range': [float(df['molecular_weight'].min()), float(df['molecular_weight'].max())],
        'mw_mean': float(df['molecular_weight'].mean()),
        'compounds_with_bioactivity': int(df['num_bioactivities'].gt(0).sum()),
        'mean_targets': float(df['num_targets'].mean())
    }
    
    with open('/home/ubuntu/ubp_medicine_study/dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nDataset acquisition complete!")

if __name__ == '__main__':
    main()
