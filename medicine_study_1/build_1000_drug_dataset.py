#!/usr/bin/env python3
"""
Build comprehensive dataset of 1000 FDA-approved drugs
Combines ChEMBL chemreps with web API data and RDKit descriptors
"""

import pandas as pd
import numpy as np
import gzip
import json
import requests
import time
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors
from collections import defaultdict

def load_chembl_structures(chemreps_file, max_compounds=50000):
    """Load molecular structures from ChEMBL chemreps file"""
    print(f"Loading ChEMBL structures from {chemreps_file}...")
    
    df = pd.read_csv(chemreps_file, sep='\t', compression='gzip', nrows=max_compounds)
    print(f"Loaded {len(df)} compound structures")
    
    return df

def fetch_molecule_info_batch(chembl_ids):
    """Fetch molecule information for a batch of ChEMBL IDs"""
    url = "https://www.ebi.ac.uk/chembl/api/data/molecule.json"
    
    # ChEMBL API supports filtering by multiple IDs
    chembl_id_list = ','.join(chembl_ids[:50])  # Limit to 50 at a time
    params = {
        'molecule_chembl_id__in': chembl_id_list,
        'limit': 50
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('molecules', [])
    except Exception as e:
        print(f"Error fetching batch: {e}")
        return []

def compute_rdkit_descriptors(smiles):
    """Compute molecular descriptors using RDKit"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        descriptors = {
            'molecular_weight': Descriptors.MolWt(mol),
            'logp': Crippen.MolLogP(mol),
            'hbd': Lipinski.NumHDonors(mol),
            'hba': Lipinski.NumHAcceptors(mol),
            'tpsa': Descriptors.TPSA(mol),
            'rotatable_bonds': Lipinski.NumRotatableBonds(mol),
            'aromatic_rings': Lipinski.NumAromaticRings(mol),
            'heavy_atoms': Lipinski.HeavyAtomCount(mol),
            'num_rings': Lipinski.RingCount(mol),
            'sp3_fraction': rdMolDescriptors.CalcFractionCsp3(mol),
            'complexity': Descriptors.BertzCT(mol),  # Bertz complexity index
            'num_heteroatoms': Lipinski.NumHeteroatoms(mol),
            'num_saturated_rings': Lipinski.NumSaturatedRings(mol),
            'num_aliphatic_rings': Lipinski.NumAliphaticRings(mol)
        }
        
        return descriptors
    except Exception as e:
        return None

def classify_therapeutic_area(indications_text):
    """Classify therapeutic area based on indication text"""
    if not indications_text or indications_text == 'Unknown':
        return 'Other'
    
    text_lower = indications_text.lower()
    
    if any(term in text_lower for term in ['cancer', 'tumor', 'carcinoma', 'leukemia', 'lymphoma', 'oncology', 'neoplasm', 'melanoma']):
        return 'Oncology'
    elif any(term in text_lower for term in ['hypertension', 'heart', 'cardiac', 'cardiovascular', 'angina', 'arrhythmia', 'cholesterol']):
        return 'Cardiovascular'
    elif any(term in text_lower for term in ['infection', 'bacterial', 'antibiotic', 'antimicrobial', 'antiviral', 'fungal', 'hiv', 'hepatitis', 'tuberculosis']):
        return 'Anti-infective'
    elif any(term in text_lower for term in ['diabetes', 'glucose', 'insulin', 'metabolic', 'obesity', 'thyroid']):
        return 'Metabolic'
    elif any(term in text_lower for term in ['depression', 'anxiety', 'schizophrenia', 'psychosis', 'seizure', 'epilepsy', 'neurological', 'alzheimer', 'parkinson', 'migraine']):
        return 'CNS/Neurology'
    elif any(term in text_lower for term in ['pain', 'analgesic', 'inflammation', 'arthritis', 'rheumatoid', 'osteoarthritis']):
        return 'Pain/Inflammation'
    elif any(term in text_lower for term in ['immune', 'autoimmune', 'transplant', 'immunosuppressant', 'lupus', 'multiple sclerosis']):
        return 'Immunology'
    elif any(term in text_lower for term in ['respiratory', 'asthma', 'copd', 'bronchitis', 'pulmonary', 'cystic fibrosis']):
        return 'Respiratory'
    elif any(term in text_lower for term in ['gastrointestinal', 'ulcer', 'crohn', 'colitis', 'gastric', 'gerd', 'ibs']):
        return 'Gastrointestinal'
    elif any(term in text_lower for term in ['dermatology', 'skin', 'psoriasis', 'eczema', 'dermatitis', 'acne']):
        return 'Dermatology'
    elif any(term in text_lower for term in ['ophthalmology', 'eye', 'glaucoma', 'macular', 'vision']):
        return 'Ophthalmology'
    elif any(term in text_lower for term in ['hematology', 'blood', 'anemia', 'coagulation', 'thrombosis']):
        return 'Hematology'
    else:
        return 'Other'

def build_dataset(chemreps_file, target_count=1000):
    """Build comprehensive dataset of FDA-approved drugs"""
    
    # Load structures
    structures_df = load_chembl_structures(chemreps_file, max_compounds=100000)
    
    print(f"\nProcessing compounds to find FDA-approved drugs...")
    print("This will take several minutes...")
    
    approved_drugs = []
    batch_size = 50
    processed = 0
    
    # Process in batches
    chembl_ids = structures_df['chembl_id'].tolist()
    
    for i in range(0, len(chembl_ids), batch_size):
        batch_ids = chembl_ids[i:i+batch_size]
        
        # Fetch molecule info
        molecules = fetch_molecule_info_batch(batch_ids)
        
        for mol_data in molecules:
            chembl_id = mol_data.get('molecule_chembl_id')
            
            # Check if FDA approved (max_phase = 4)
            max_phase = mol_data.get('max_phase')
            if max_phase != 4:
                continue
            
            # Get structure
            structure_row = structures_df[structures_df['chembl_id'] == chembl_id]
            if structure_row.empty:
                continue
            
            smiles = structure_row.iloc[0]['canonical_smiles']
            if pd.isna(smiles):
                continue
            
            # Compute RDKit descriptors
            descriptors = compute_rdkit_descriptors(smiles)
            if descriptors is None:
                continue
            
            # Filter molecular weight
            if descriptors['molecular_weight'] < 150 or descriptors['molecular_weight'] > 1000:
                continue
            
            # Build drug data
            drug_data = {
                'chembl_id': chembl_id,
                'name': mol_data.get('pref_name', 'Unknown'),
                'smiles': smiles,
                'inchi_key': structure_row.iloc[0]['standard_inchi_key'],
                'max_phase': max_phase,
                'first_approval': mol_data.get('first_approval'),
                'therapeutic_flag': mol_data.get('therapeutic_flag', False),
                'oral': mol_data.get('oral', False),
                'parenteral': mol_data.get('parenteral', False),
                'topical': mol_data.get('topical', False)
            }
            
            # Add RDKit descriptors
            drug_data.update(descriptors)
            
            # Get molecule properties from API
            props = mol_data.get('molecule_properties', {})
            if props:
                drug_data['alogp'] = props.get('alogp')
                drug_data['psa'] = props.get('psa')
                drug_data['num_ro5_violations'] = props.get('num_ro5_violations')
            
            # Placeholder for indications (would need separate API call)
            drug_data['indications'] = 'Unknown'
            drug_data['therapeutic_area'] = 'Other'
            
            approved_drugs.append(drug_data)
            
            if len(approved_drugs) >= target_count:
                break
        
        processed += len(batch_ids)
        if len(approved_drugs) >= target_count:
            print(f"\nReached target of {target_count} drugs!")
            break
        
        if processed % 500 == 0:
            print(f"Processed {processed} compounds, found {len(approved_drugs)} FDA-approved drugs...")
        
        # Rate limiting
        time.sleep(0.5)
    
    return pd.DataFrame(approved_drugs)

def main():
    """Main execution"""
    print("="*80)
    print("Building Comprehensive Dataset of 1000 FDA-Approved Drugs")
    print("="*80 + "\n")
    
    chemreps_file = '/home/ubuntu/ubp_medicine_study/chembl_36_chemreps.txt.gz'
    target_count = 1000
    
    # Build dataset
    df = build_dataset(chemreps_file, target_count=target_count)
    
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    print(f"Total compounds: {len(df)}")
    
    if len(df) > 0:
        print(f"\nMolecular weight range: {df['molecular_weight'].min():.1f} - {df['molecular_weight'].max():.1f}")
        print(f"Mean molecular weight: {df['molecular_weight'].mean():.1f}")
        print(f"\nLogP range: {df['logp'].min():.2f} - {df['logp'].max():.2f}")
        print(f"Mean LogP: {df['logp'].mean():.2f}")
        print(f"\nComplexity range: {df['complexity'].min():.1f} - {df['complexity'].max():.1f}")
        print(f"Mean complexity: {df['complexity'].mean():.1f}")
        
        # Save to CSV
        output_file = '/home/ubuntu/ubp_medicine_study/fda_approved_1000_drugs.csv'
        df.to_csv(output_file, index=False)
        print(f"\nData saved to: {output_file}")
        
        # Save summary
        summary = {
            'total_compounds': len(df),
            'mw_range': [float(df['molecular_weight'].min()), float(df['molecular_weight'].max())],
            'mw_mean': float(df['molecular_weight'].mean()),
            'logp_range': [float(df['logp'].min()), float(df['logp'].max())],
            'logp_mean': float(df['logp'].mean()),
            'complexity_range': [float(df['complexity'].min()), float(df['complexity'].max())],
            'complexity_mean': float(df['complexity'].mean())
        }
        
        with open('/home/ubuntu/ubp_medicine_study/dataset_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\nDataset construction complete!")
    else:
        print("\nNo drugs extracted. Check API connectivity and data availability.")

if __name__ == '__main__':
    main()
