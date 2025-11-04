#!/usr/bin/env python3
"""
Fetch FDA-approved drugs from ChEMBL database for UBP medicine study
Pilot study: ~100 compounds across diverse therapeutic classes
"""

import json
import pandas as pd
from chembl_webresource_client.new_client import new_client
import time

def fetch_fda_approved_drugs(max_compounds=100):
    """
    Fetch FDA-approved drugs from ChEMBL with bioactivity and clinical data
    
    Returns:
        DataFrame with drug information
    """
    print("Connecting to ChEMBL database...")
    
    # Initialize ChEMBL clients
    molecule = new_client.molecule
    activity = new_client.activity
    target = new_client.target
    drug_indication = new_client.drug_indication
    
    # Query for FDA-approved drugs
    print("Querying FDA-approved drugs...")
    drugs = molecule.filter(
        max_phase=4,  # Phase 4 = FDA approved
        molecule_type='Small molecule'
    ).only([
        'molecule_chembl_id',
        'pref_name',
        'molecule_structures',
        'molecule_properties',
        'max_phase',
        'therapeutic_flag',
        'first_approval'
    ])
    
    drug_list = []
    count = 0
    
    for drug in drugs:
        if count >= max_compounds:
            break
            
        # Skip if no structure data
        if not drug.get('molecule_structures'):
            continue
            
        # Get molecular properties
        props = drug.get('molecule_properties', {})
        structures = drug.get('molecule_structures', {})
        
        # Basic drug info
        drug_data = {
            'chembl_id': drug.get('molecule_chembl_id'),
            'name': drug.get('pref_name', 'Unknown'),
            'smiles': structures.get('canonical_smiles'),
            'inchi': structures.get('standard_inchi'),
            'inchi_key': structures.get('standard_inchi_key'),
            'molecular_weight': props.get('full_mw'),
            'alogp': props.get('alogp'),
            'hba': props.get('hba'),  # H-bond acceptors
            'hbd': props.get('hbd'),  # H-bond donors
            'psa': props.get('psa'),  # Polar surface area
            'rtb': props.get('rtb'),  # Rotatable bonds
            'aromatic_rings': props.get('aromatic_rings'),
            'heavy_atoms': props.get('heavy_atoms'),
            'num_ro5_violations': props.get('num_ro5_violations'),
            'first_approval': drug.get('first_approval'),
            'therapeutic_flag': drug.get('therapeutic_flag')
        }
        
        # Get therapeutic indications
        try:
            indications = drug_indication.filter(
                molecule_chembl_id=drug['molecule_chembl_id']
            ).only(['mesh_heading', 'efo_term', 'max_phase_for_ind'])
            
            indication_list = []
            for ind in indications[:3]:  # Top 3 indications
                if ind.get('mesh_heading'):
                    indication_list.append(ind['mesh_heading'])
                elif ind.get('efo_term'):
                    indication_list.append(ind['efo_term'])
            
            drug_data['indications'] = '; '.join(indication_list) if indication_list else 'Unknown'
        except:
            drug_data['indications'] = 'Unknown'
        
        # Get bioactivity data
        try:
            activities = activity.filter(
                molecule_chembl_id=drug['molecule_chembl_id'],
                standard_type__in=['IC50', 'EC50', 'Ki', 'Kd'],
                standard_relation='='
            ).only(['standard_type', 'standard_value', 'standard_units', 'target_chembl_id'])
            
            activity_values = []
            target_ids = set()
            
            for act in activities[:10]:  # Top 10 activities
                if act.get('standard_value'):
                    activity_values.append(float(act['standard_value']))
                if act.get('target_chembl_id'):
                    target_ids.add(act['target_chembl_id'])
            
            drug_data['num_bioactivities'] = len(activity_values)
            drug_data['num_targets'] = len(target_ids)
            drug_data['mean_activity_nm'] = sum(activity_values) / len(activity_values) if activity_values else None
        except:
            drug_data['num_bioactivities'] = 0
            drug_data['num_targets'] = 0
            drug_data['mean_activity_nm'] = None
        
        drug_list.append(drug_data)
        count += 1
        
        if count % 10 == 0:
            print(f"Fetched {count} drugs...")
            time.sleep(0.5)  # Rate limiting
    
    print(f"\nTotal drugs fetched: {len(drug_list)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(drug_list)
    
    # Filter for quality data
    df = df[df['smiles'].notna()]
    df = df[df['molecular_weight'].notna()]
    df = df[(df['molecular_weight'] >= 150) & (df['molecular_weight'] <= 1000)]
    
    print(f"After filtering: {len(df)} drugs")
    
    return df

def classify_therapeutic_area(indications):
    """
    Classify drug into therapeutic area based on indications
    """
    if pd.isna(indications) or indications == 'Unknown':
        return 'Other'
    
    indications_lower = indications.lower()
    
    # Classification rules
    if any(term in indications_lower for term in ['cancer', 'tumor', 'carcinoma', 'leukemia', 'lymphoma', 'oncology']):
        return 'Oncology'
    elif any(term in indications_lower for term in ['hypertension', 'heart', 'cardiac', 'cardiovascular', 'angina']):
        return 'Cardiovascular'
    elif any(term in indications_lower for term in ['infection', 'bacterial', 'antibiotic', 'antimicrobial', 'antiviral', 'fungal']):
        return 'Anti-infective'
    elif any(term in indications_lower for term in ['diabetes', 'glucose', 'insulin', 'metabolic']):
        return 'Metabolic'
    elif any(term in indications_lower for term in ['depression', 'anxiety', 'schizophrenia', 'psychosis', 'seizure', 'epilepsy', 'neurological']):
        return 'CNS/Neurology'
    elif any(term in indications_lower for term in ['pain', 'analgesic', 'inflammation', 'arthritis']):
        return 'Pain/Inflammation'
    elif any(term in indications_lower for term in ['immune', 'autoimmune', 'transplant', 'immunosuppressant']):
        return 'Immunology'
    elif any(term in indications_lower for term in ['respiratory', 'asthma', 'copd', 'bronchitis']):
        return 'Respiratory'
    else:
        return 'Other'

def main():
    """Main execution"""
    print("="*80)
    print("UBP Medicine Study - ChEMBL Data Acquisition")
    print("Pilot Study: Fetching ~100 FDA-approved drugs")
    print("="*80 + "\n")
    
    # Fetch drugs
    df = fetch_fda_approved_drugs(max_compounds=150)  # Fetch extra to ensure 100+ after filtering
    
    # Classify therapeutic areas
    print("\nClassifying therapeutic areas...")
    df['therapeutic_area'] = df['indications'].apply(classify_therapeutic_area)
    
    # Display distribution
    print("\nTherapeutic area distribution:")
    print(df['therapeutic_area'].value_counts())
    
    # Save to CSV
    output_file = '/home/ubuntu/ubp_medicine_study/chembl_pilot_drugs.csv'
    df.to_csv(output_file, index=False)
    print(f"\nData saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("PILOT DATASET SUMMARY")
    print("="*80)
    print(f"Total compounds: {len(df)}")
    print(f"Therapeutic areas: {df['therapeutic_area'].nunique()}")
    print(f"\nMolecular weight range: {df['molecular_weight'].min():.1f} - {df['molecular_weight'].max():.1f}")
    print(f"Mean molecular weight: {df['molecular_weight'].mean():.1f}")
    print(f"\nCompounds with bioactivity data: {df['num_bioactivities'].gt(0).sum()}")
    print(f"Mean targets per compound: {df['num_targets'].mean():.1f}")
    print(f"\nFirst approval years: {df['first_approval'].min()} - {df['first_approval'].max()}")
    
    # Save summary
    summary = {
        'total_compounds': len(df),
        'therapeutic_areas': df['therapeutic_area'].value_counts().to_dict(),
        'mw_range': [float(df['molecular_weight'].min()), float(df['molecular_weight'].max())],
        'mw_mean': float(df['molecular_weight'].mean()),
        'compounds_with_bioactivity': int(df['num_bioactivities'].gt(0).sum()),
        'mean_targets': float(df['num_targets'].mean())
    }
    
    with open('/home/ubuntu/ubp_medicine_study/pilot_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nPilot data acquisition complete!")

if __name__ == '__main__':
    main()
