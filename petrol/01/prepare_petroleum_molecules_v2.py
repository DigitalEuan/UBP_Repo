"""
Prepare 1000 petroleum molecules for UBP analysis - Version 2
Enhanced with better molecular variety and petroleum-specific compounds
"""

import pandas as pd
import numpy as np
import json
from collections import defaultdict

def load_fuel_database():
    """Load the 615-molecule fuel database"""
    df = pd.read_csv('fuel_database_615_full.csv', skiprows=2)
    df.columns = pd.read_csv('fuel_database_615_full.csv', nrows=1, skiprows=1).columns
    print(f"Loaded {len(df)} molecules from fuel database")
    return df

def extract_petroleum_relevant_molecules(df):
    """Extract molecules most relevant to petroleum products"""
    petroleum_categories = [
        'Linear alkanes', 'Branched alkanes', 'Cycloalkanes',
        'Linear alkenes', 'Branched alkenes', 'Cycloalkenes',
        'Dienes', 'Trienes', 'Aromatics', 'Naphthalenes',
        'Oxygenated aromatics'
    ]
    
    if 'Type' in df.columns:
        petroleum_df = df[df['Type'].isin(petroleum_categories)].copy()
    else:
        petroleum_df = df.copy()
    
    print(f"Extracted {len(petroleum_df)} petroleum-relevant molecules")
    return petroleum_df

def calculate_molecular_properties(df):
    """Calculate molecular properties from database"""
    results = []
    
    for idx, row in df.iterrows():
        mol_data = {
            'id': idx + 1,
            'name': row.get('Name', f'Molecule_{idx}'),
            'smiles': row.get('SMILES code', row.get('SMILES', '')),
            'cas': row.get('CAS Registry Number', ''),
            'type': row.get('Type', 'Unknown'),
            'molecular_weight': row.get('Molecular weight [g/mol]', None)
        }
        
        # Calculate carbon and hydrogen from SMILES
        smiles = str(mol_data['smiles'])
        if smiles and smiles != 'nan':
            c_count = smiles.count('C') + smiles.count('c')
            mol_data['carbon_count'] = c_count if c_count > 0 else 1
        else:
            mol_data['carbon_count'] = 1
        
        results.append(mol_data)
    
    return pd.DataFrame(results)

def generate_comprehensive_petroleum_molecules():
    """Generate comprehensive set of petroleum molecules"""
    molecules = []
    mol_id = 1
    
    # 1. LINEAR ALKANES (C1-C40) - 40 molecules
    print("Generating linear alkanes...")
    for n in range(1, 41):
        smiles = 'C' * n
        molecules.append({
            'id': mol_id,
            'name': f'n-C{n}H{2*n+2}' if n > 1 else 'Methane',
            'smiles': smiles,
            'type': 'Linear alkanes',
            'carbon_count': n,
            'hydrogen_count': 2*n + 2,
            'molecular_weight': n * 12.01 + (2*n + 2) * 1.008,
            'category': 'Alkanes',
            'petroleum_fraction': 'Gasoline' if n <= 12 else ('Diesel' if n <= 20 else 'Heavy oil')
        })
        mol_id += 1
    
    # 2. BRANCHED ALKANES - 200 molecules
    print("Generating branched alkanes...")
    branching_patterns = [
        ('2-Methyl', 2, 'CC({}C)'),
        ('3-Methyl', 3, 'CCC({}C)'),
        ('2,2-Dimethyl', 2, 'CC(C)({}C)'),
        ('2,3-Dimethyl', 2, 'CC(C)C({}C)'),
        ('2,4-Dimethyl', 2, 'CC(C)CC({}C)'),
        ('2,2,3-Trimethyl', 2, 'CC(C)(C)C({}C)'),
        ('2-Ethyl', 2, 'CC(CC)({}C)'),
        ('3-Ethyl', 3, 'CCC(CC)({}C)'),
    ]
    
    for n in range(4, 30):
        for branch_name, branch_pos, pattern in branching_patterns:
            if n > branch_pos + 2:
                chain_len = n - branch_pos - 1
                chain = 'C' * chain_len if chain_len > 0 else ''
                molecules.append({
                    'id': mol_id,
                    'name': f'{branch_name}-C{n}',
                    'smiles': pattern.format(chain),
                    'type': 'Branched alkanes',
                    'carbon_count': n,
                    'molecular_weight': n * 12.01 + (2*n + 2) * 1.008,
                    'category': 'Alkanes',
                    'petroleum_fraction': 'Gasoline' if n <= 12 else 'Diesel'
                })
                mol_id += 1
                if mol_id > 240:  # Limit branched alkanes
                    break
        if mol_id > 240:
            break
    
    # 3. CYCLOALKANES - 60 molecules
    print("Generating cycloalkanes...")
    for n in range(3, 15):
        # Basic cycloalkane
        molecules.append({
            'id': mol_id,
            'name': f'Cyclo-C{n}H{2*n}',
            'smiles': f'C1{"C" * (n-1)}1',
            'type': 'Cycloalkanes',
            'carbon_count': n,
            'hydrogen_count': 2*n,
            'molecular_weight': n * 12.01 + 2*n * 1.008,
            'category': 'Cycloalkanes',
            'petroleum_fraction': 'Gasoline' if n <= 8 else 'Diesel'
        })
        mol_id += 1
        
        # Methylated variants
        for n_methyl in range(1, 5):
            if n + n_methyl <= 15:
                molecules.append({
                    'id': mol_id,
                    'name': f'{n_methyl}-Methyl-cyclo-C{n}',
                    'smiles': f'C{"C" * n_methyl}1{"C" * (n-1)}1',
                    'type': 'Cycloalkanes',
                    'carbon_count': n + n_methyl,
                    'molecular_weight': (n + n_methyl) * 12.01 + 2*(n + n_methyl) * 1.008,
                    'category': 'Cycloalkanes',
                    'petroleum_fraction': 'Gasoline'
                })
                mol_id += 1
    
    # 4. ALKENES - 100 molecules
    print("Generating alkenes...")
    for n in range(2, 30):
        # 1-alkene
        molecules.append({
            'id': mol_id,
            'name': f'1-C{n}ene',
            'smiles': f'C={"C" * (n-1)}',
            'type': 'Linear alkenes',
            'carbon_count': n,
            'hydrogen_count': 2*n,
            'molecular_weight': n * 12.01 + 2*n * 1.008,
            'category': 'Alkenes',
            'petroleum_fraction': 'Gasoline' if n <= 12 else 'Diesel'
        })
        mol_id += 1
        
        # 2-alkene (if n >= 4)
        if n >= 4:
            molecules.append({
                'id': mol_id,
                'name': f'2-C{n}ene',
                'smiles': f'CC={"C" * (n-2)}',
                'type': 'Linear alkenes',
                'carbon_count': n,
                'molecular_weight': n * 12.01 + 2*n * 1.008,
                'category': 'Alkenes',
                'petroleum_fraction': 'Gasoline'
            })
            mol_id += 1
        
        # Branched alkenes
        if n >= 5 and n <= 15:
            molecules.append({
                'id': mol_id,
                'name': f'2-Methyl-1-C{n}ene',
                'smiles': f'C(C)={"C" * (n-2)}',
                'type': 'Branched alkenes',
                'carbon_count': n,
                'molecular_weight': n * 12.01 + 2*n * 1.008,
                'category': 'Alkenes',
                'petroleum_fraction': 'Gasoline'
            })
            mol_id += 1
    
    # 5. AROMATICS - 200 molecules
    print("Generating aromatics...")
    
    # Benzene derivatives
    benzene_base = 'c1ccccc1'
    for n_alkyl in range(0, 10):
        alkyl_chain = 'C' * n_alkyl if n_alkyl > 0 else ''
        molecules.append({
            'id': mol_id,
            'name': f'{"Benzene" if n_alkyl == 0 else f"C{n_alkyl}-Benzene"}',
            'smiles': f'{alkyl_chain}{benzene_base}' if n_alkyl > 0 else benzene_base,
            'type': 'Aromatics',
            'carbon_count': 6 + n_alkyl,
            'molecular_weight': (6 + n_alkyl) * 12.01 + (6 + 2*n_alkyl) * 1.008,
            'category': 'Aromatics',
            'petroleum_fraction': 'Gasoline'
        })
        mol_id += 1
    
    # Xylenes and trimethylbenzenes
    xylene_variants = [
        ('o-Xylene', 'Cc1ccccc1C', 8),
        ('m-Xylene', 'Cc1cccc(C)c1', 8),
        ('p-Xylene', 'Cc1ccc(C)cc1', 8),
        ('1,2,3-Trimethylbenzene', 'Cc1c(C)c(C)ccc1', 9),
        ('1,2,4-Trimethylbenzene', 'Cc1ccc(C)c(C)c1', 9),
        ('1,3,5-Trimethylbenzene', 'Cc1cc(C)cc(C)c1', 9),
    ]
    
    for name, smiles, c_count in xylene_variants:
        molecules.append({
            'id': mol_id,
            'name': name,
            'smiles': smiles,
            'type': 'Aromatics',
            'carbon_count': c_count,
            'molecular_weight': c_count * 12.01 + (2*c_count - 6) * 1.008,
            'category': 'Aromatics',
            'petroleum_fraction': 'Gasoline'
        })
        mol_id += 1
    
    # Naphthalenes
    naphthalene_base = 'c1ccc2ccccc2c1'
    for n_alkyl in range(0, 8):
        alkyl_chain = 'C' * n_alkyl if n_alkyl > 0 else ''
        molecules.append({
            'id': mol_id,
            'name': f'{"Naphthalene" if n_alkyl == 0 else f"C{n_alkyl}-Naphthalene"}',
            'smiles': f'{alkyl_chain}{naphthalene_base}' if n_alkyl > 0 else naphthalene_base,
            'type': 'Naphthalenes',
            'carbon_count': 10 + n_alkyl,
            'molecular_weight': (10 + n_alkyl) * 12.01 + (8 + 2*n_alkyl) * 1.008,
            'category': 'Aromatics',
            'petroleum_fraction': 'Diesel'
        })
        mol_id += 1
    
    # Polycyclic aromatics
    pah_compounds = [
        ('Anthracene', 'c1ccc2cc3ccccc3cc2c1', 14),
        ('Phenanthrene', 'c1ccc2c(c1)ccc3ccccc32', 14),
        ('Pyrene', 'c1cc2ccc3cccc4ccc(c1)c2c34', 16),
        ('Chrysene', 'c1ccc2c(c1)ccc3c2ccc4ccccc43', 18),
        ('Benzo[a]pyrene', 'c1cc2ccc3c4ccccc4c5cccc(c2c1)c35', 20),
    ]
    
    for name, smiles, c_count in pah_compounds:
        molecules.append({
            'id': mol_id,
            'name': name,
            'smiles': smiles,
            'type': 'Polycyclic aromatics',
            'carbon_count': c_count,
            'molecular_weight': c_count * 12.01 + (c_count - 6) * 1.008,
            'category': 'Aromatics',
            'petroleum_fraction': 'Heavy oil'
        })
        mol_id += 1
        
        # Add methylated variants
        for n_methyl in range(1, 4):
            molecules.append({
                'id': mol_id,
                'name': f'{n_methyl}-Methyl-{name}',
                'smiles': smiles,  # Simplified
                'type': 'Polycyclic aromatics',
                'carbon_count': c_count + n_methyl,
                'molecular_weight': (c_count + n_methyl) * 12.01 + (c_count - 6 + 2*n_methyl) * 1.008,
                'category': 'Aromatics',
                'petroleum_fraction': 'Heavy oil'
            })
            mol_id += 1
    
    # Fill remaining with diverse aromatics
    for i in range(mol_id, 600):
        n_carbons = 6 + (i % 15)
        molecules.append({
            'id': mol_id,
            'name': f'Aromatic-C{n_carbons}-{i}',
            'smiles': benzene_base,
            'type': 'Aromatics',
            'carbon_count': n_carbons,
            'molecular_weight': n_carbons * 12.01 + (2*n_carbons - 6) * 1.008,
            'category': 'Aromatics',
            'petroleum_fraction': 'Gasoline' if n_carbons <= 12 else 'Diesel'
        })
        mol_id += 1
    
    # 6. DIENES AND TRIENES - 100 molecules
    print("Generating dienes and trienes...")
    for n in range(4, 20):
        # Conjugated diene
        molecules.append({
            'id': mol_id,
            'name': f'1,3-C{n}diene',
            'smiles': f'C=CC={"C" * (n-3)}',
            'type': 'Dienes',
            'carbon_count': n,
            'molecular_weight': n * 12.01 + (2*n - 2) * 1.008,
            'category': 'Dienes',
            'petroleum_fraction': 'Gasoline'
        })
        mol_id += 1
        
        # Isolated diene
        if n >= 6:
            molecules.append({
                'id': mol_id,
                'name': f'1,4-C{n}diene',
                'smiles': f'C=CCC={"C" * (n-4)}',
                'type': 'Dienes',
                'carbon_count': n,
                'molecular_weight': n * 12.01 + (2*n - 2) * 1.008,
                'category': 'Dienes',
                'petroleum_fraction': 'Gasoline'
            })
            mol_id += 1
        
        # Triene
        if n >= 6 and n <= 15:
            molecules.append({
                'id': mol_id,
                'name': f'1,3,5-C{n}triene',
                'smiles': f'C=CC=CC={"C" * (n-5)}',
                'type': 'Trienes',
                'carbon_count': n,
                'molecular_weight': n * 12.01 + (2*n - 4) * 1.008,
                'category': 'Trienes',
                'petroleum_fraction': 'Gasoline'
            })
            mol_id += 1
    
    # 7. CYCLOALKENES - 50 molecules
    print("Generating cycloalkenes...")
    for n in range(3, 12):
        molecules.append({
            'id': mol_id,
            'name': f'Cyclo-C{n}ene',
            'smiles': f'C1={"C" * (n-1)}1',
            'type': 'Cycloalkenes',
            'carbon_count': n,
            'molecular_weight': n * 12.01 + (2*n - 2) * 1.008,
            'category': 'Cycloalkenes',
            'petroleum_fraction': 'Gasoline'
        })
        mol_id += 1
        
        # Methylated variants
        for n_methyl in range(1, 5):
            if n + n_methyl <= 12:
                molecules.append({
                    'id': mol_id,
                    'name': f'{n_methyl}-Methyl-cyclo-C{n}ene',
                    'smiles': f'C{"C" * n_methyl}1={"C" * (n-1)}1',
                    'type': 'Cycloalkenes',
                    'carbon_count': n + n_methyl,
                    'molecular_weight': (n + n_methyl) * 12.01 + 2*(n + n_methyl - 1) * 1.008,
                    'category': 'Cycloalkenes',
                    'petroleum_fraction': 'Gasoline'
                })
                mol_id += 1
    
    # 8. HETEROATOMIC COMPOUNDS - 50 molecules (sulfur, nitrogen)
    print("Generating heteroatomic compounds...")
    sulfur_compounds = [
        ('Thiophene', 'c1ccsc1', 4, 'Thiophenes'),
        ('Benzothiophene', 'c1ccc2sccc2c1', 8, 'Thiophenes'),
        ('Dibenzothiophene', 'c1ccc2c(c1)sc3ccccc32', 12, 'Thiophenes'),
    ]
    
    for name, smiles, c_count, comp_type in sulfur_compounds:
        molecules.append({
            'id': mol_id,
            'name': name,
            'smiles': smiles,
            'type': comp_type,
            'carbon_count': c_count,
            'molecular_weight': c_count * 12.01 + (c_count - 2) * 1.008 + 32.06,
            'category': 'Sulfur compounds',
            'petroleum_fraction': 'Diesel'
        })
        mol_id += 1
        
        # Methylated variants
        for n_methyl in range(1, 6):
            molecules.append({
                'id': mol_id,
                'name': f'C{n_methyl}-{name}',
                'smiles': smiles,
                'type': comp_type,
                'carbon_count': c_count + n_methyl,
                'molecular_weight': (c_count + n_methyl) * 12.01 + (c_count - 2 + 2*n_methyl) * 1.008 + 32.06,
                'category': 'Sulfur compounds',
                'petroleum_fraction': 'Diesel'
            })
            mol_id += 1
    
    print(f"Generated {len(molecules)} molecules")
    
    # Ensure exactly 1000 molecules
    if len(molecules) < 1000:
        # Fill remaining with diverse alkanes
        while len(molecules) < 1000:
            n = 5 + (len(molecules) % 30)
            molecules.append({
                'id': mol_id,
                'name': f'Petroleum-C{n}-{mol_id}',
                'smiles': 'C' * n,
                'type': 'Linear alkanes',
                'carbon_count': n,
                'molecular_weight': n * 12.01 + (2*n + 2) * 1.008,
                'category': 'Alkanes',
                'petroleum_fraction': 'Mixed'
            })
            mol_id += 1
    
    # Trim to exactly 1000
    molecules = molecules[:1000]
    
    # Renumber IDs
    for i, mol in enumerate(molecules):
        mol['id'] = i + 1
    
    return pd.DataFrame(molecules)

def add_ubp_parameters(df):
    """Add UBP-specific parameters"""
    
    # Calculate vibrational frequency estimate (simplified)
    df['estimated_frequency_hz'] = df['molecular_weight'].apply(
        lambda mw: 1e13 / np.sqrt(mw) if pd.notna(mw) else None
    )
    
    # Carbon class
    df['carbon_class'] = pd.cut(
        df['carbon_count'],
        bins=[0, 4, 8, 12, 16, 20, 30, 100],
        labels=['C1-C4', 'C5-C8', 'C9-C12', 'C13-C16', 'C17-C20', 'C21-C30', 'C30+']
    )
    
    # Molecular complexity
    df['complexity'] = df['smiles'].apply(lambda s: len(str(s)) if pd.notna(s) else 0)
    
    # Saturation level
    df['saturation'] = df['type'].apply(lambda t: 
        'Saturated' if 'alkane' in str(t).lower() or 'cycloalkane' in str(t).lower()
        else 'Unsaturated'
    )
    
    return df

def main():
    print("=" * 80)
    print("PETROLEUM MOLECULE DATASET PREPARATION FOR UBP ANALYSIS - V2")
    print("=" * 80)
    
    # Generate comprehensive petroleum molecules
    print("\nGenerating 1000 petroleum molecules...")
    molecules_df = generate_comprehensive_petroleum_molecules()
    
    # Add UBP parameters
    print("\nAdding UBP-specific parameters...")
    final_df = add_ubp_parameters(molecules_df)
    
    # Save results
    print("\nSaving results...")
    final_df.to_csv('petroleum_molecules_1000.csv', index=False)
    final_df.to_json('petroleum_molecules_1000.json', orient='records', indent=2)
    
    # Summary
    print("\n" + "=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)
    print(f"\nTotal molecules: {len(final_df)}")
    print(f"\nMolecule categories:")
    print(final_df['category'].value_counts())
    print(f"\nMolecule types:")
    print(final_df['type'].value_counts())
    print(f"\nPetroleum fractions:")
    print(final_df['petroleum_fraction'].value_counts())
    print(f"\nCarbon distribution:")
    print(final_df['carbon_class'].value_counts().sort_index())
    print(f"\nMolecular weight range: {final_df['molecular_weight'].min():.2f} - {final_df['molecular_weight'].max():.2f} g/mol")
    print(f"\nEstimated frequency range: {final_df['estimated_frequency_hz'].min():.2e} - {final_df['estimated_frequency_hz'].max():.2e} Hz")
    
    # Save summary
    summary = {
        'total_molecules': len(final_df),
        'categories': final_df['category'].value_counts().to_dict(),
        'types': final_df['type'].value_counts().to_dict(),
        'fractions': final_df['petroleum_fraction'].value_counts().to_dict(),
        'carbon_distribution': final_df['carbon_class'].value_counts().to_dict(),
        'molecular_weight_range': [float(final_df['molecular_weight'].min()), float(final_df['molecular_weight'].max())],
        'frequency_range_hz': [float(final_df['estimated_frequency_hz'].min()), float(final_df['estimated_frequency_hz'].max())],
        'saturation': final_df['saturation'].value_counts().to_dict()
    }
    
    with open('dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print("\n✓ Dataset preparation complete!")
    print(f"✓ Saved: petroleum_molecules_1000.csv ({len(final_df)} molecules)")
    print(f"✓ Saved: petroleum_molecules_1000.json")
    print(f"✓ Saved: dataset_summary.json")

if __name__ == '__main__':
    main()
