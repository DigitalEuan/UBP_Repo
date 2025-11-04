#!/usr/bin/env python3
"""
UBP 3.3 Analysis of 1000 Pharmaceutical Compounds
Comprehensive study using Universal Binary Principle framework
"""

import sys
import os
import pandas as pd
import numpy as np
import json
from datetime import datetime

# Add UBP 3.3 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.3')

from pharmaceutical_realm import PharmaceuticalRealm


def load_compound_dataset(filepath):
    """Load the 1000-compound dataset."""
    print(f"Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} compounds")
    return df


def prepare_compound_for_ubp(row):
    """Convert DataFrame row to compound dictionary for UBP analysis."""
    return {
        'chembl_id': row['chembl_id'],
        'name': row.get('name', 'Unknown'),
        'smiles': row['smiles'],
        'molecular_weight': row['molecular_weight'],
        'logp': row['logp'],
        'complexity': row['complexity'],
        'hbd': row['hbd'],
        'hba': row['hba'],
        'tpsa': row['tpsa'],
        'rotatable_bonds': row['rotatable_bonds'],
        'aromatic_rings': row['aromatic_rings'],
        'heavy_atoms': row['heavy_atoms'],
        'therapeutic_area': row.get('therapeutic_area', 'Other')
    }


def run_ubp_analysis(df, output_dir):
    """Run UBP analysis on all compounds."""
    print("\n" + "="*80)
    print("Starting UBP 3.3 Analysis of 1000 Pharmaceutical Compounds")
    print("="*80 + "\n")
    
    # Initialize pharmaceutical realm
    realm = PharmaceuticalRealm()
    
    # Prepare results storage
    results = []
    errors = []
    
    # Process compounds
    total = len(df)
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"Processing compound {idx + 1}/{total}...")
        
        try:
            # Prepare compound data
            compound_data = prepare_compound_for_ubp(row)
            
            # Run UBP analysis
            result = realm.analyze_compound(compound_data)
            
            # Add original data
            result['smiles'] = row['smiles']
            result['inchi_key'] = row.get('inchi_key', 'Unknown')
            
            results.append(result)
            
        except Exception as e:
            error_entry = {
                'chembl_id': row['chembl_id'],
                'error': str(e),
                'index': idx
            }
            errors.append(error_entry)
            print(f"  Error processing {row['chembl_id']}: {e}")
    
    print(f"\nCompleted analysis: {len(results)} successful, {len(errors)} errors")
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f'ubp_analysis_results_{timestamp}.csv')
    results_df.to_csv(results_file, index=False)
    print(f"\n✓ Results saved to: {results_file}")
    
    # Save errors if any
    if errors:
        errors_file = os.path.join(output_dir, f'ubp_analysis_errors_{timestamp}.json')
        with open(errors_file, 'w') as f:
            json.dump(errors, f, indent=2)
        print(f"✓ Errors saved to: {errors_file}")
    
    return results_df, errors


def analyze_results(results_df, output_dir):
    """Analyze and summarize UBP results."""
    print("\n" + "="*80)
    print("UBP ANALYSIS SUMMARY")
    print("="*80 + "\n")
    
    # Basic statistics
    print(f"Total compounds analyzed: {len(results_df)}")
    print(f"\nTherapeutic area distribution:")
    print(results_df['therapeutic_area'].value_counts())
    
    # UBP metrics statistics
    print(f"\n{'='*60}")
    print("UBP ENERGY STATISTICS")
    print(f"{'='*60}")
    print(f"Mean: {results_df['ubp_energy'].mean():.6e} CU")
    print(f"Median: {results_df['ubp_energy'].median():.6e} CU")
    print(f"Std Dev: {results_df['ubp_energy'].std():.6e} CU")
    print(f"Range: {results_df['ubp_energy'].min():.6e} - {results_df['ubp_energy'].max():.6e} CU")
    
    print(f"\n{'='*60}")
    print("UBP NRCI (NON-RANDOM COHERENCE INDEX) STATISTICS")
    print(f"{'='*60}")
    print(f"Mean: {results_df['ubp_nrci'].mean():.10f}")
    print(f"Median: {results_df['ubp_nrci'].median():.10f}")
    print(f"Std Dev: {results_df['ubp_nrci'].std():.10f}")
    print(f"Range: {results_df['ubp_nrci'].min():.10f} - {results_df['ubp_nrci'].max():.10f}")
    
    print(f"\n{'='*60}")
    print("UBP CRV (COMPUTATIONAL RESONANCE VALUE) STATISTICS")
    print(f"{'='*60}")
    print(f"Mean: {results_df['ubp_crv'].mean():.6f}")
    print(f"Median: {results_df['ubp_crv'].median():.6f}")
    print(f"Std Dev: {results_df['ubp_crv'].std():.6f}")
    print(f"Range: {results_df['ubp_crv'].min():.6f} - {results_df['ubp_crv'].max():.6f}")
    
    print(f"\n{'='*60}")
    print("UBP RESONANCE STATISTICS")
    print(f"{'='*60}")
    print(f"Mean: {results_df['ubp_resonance'].mean():.6f}")
    print(f"Median: {results_df['ubp_resonance'].median():.6f}")
    print(f"Std Dev: {results_df['ubp_resonance'].std():.6f}")
    print(f"Range: {results_df['ubp_resonance'].min():.6f} - {results_df['ubp_resonance'].max():.6f}")
    
    # Therapeutic area analysis
    print(f"\n{'='*60}")
    print("UBP METRICS BY THERAPEUTIC AREA")
    print(f"{'='*60}")
    
    therapeutic_stats = results_df.groupby('therapeutic_area').agg({
        'ubp_energy': ['mean', 'std'],
        'ubp_nrci': ['mean', 'std'],
        'ubp_crv': ['mean', 'std'],
        'ubp_resonance': ['mean', 'std'],
        'drug_likeness_score': ['mean', 'std'],
        'ubp_therapeutic_potential': ['mean', 'std']
    }).round(6)
    
    print(therapeutic_stats)
    
    # Correlations
    print(f"\n{'='*60}")
    print("CORRELATIONS: UBP METRICS vs MOLECULAR PROPERTIES")
    print(f"{'='*60}")
    
    correlation_vars = [
        'ubp_energy', 'ubp_nrci', 'ubp_crv', 'ubp_resonance',
        'molecular_weight', 'logp', 'complexity', 'heavy_atoms', 'aromatic_rings'
    ]
    
    corr_matrix = results_df[correlation_vars].corr()
    
    # Print key correlations
    print("\nUBP Energy correlations:")
    print(corr_matrix['ubp_energy'].sort_values(ascending=False))
    
    print("\nUBP NRCI correlations:")
    print(corr_matrix['ubp_nrci'].sort_values(ascending=False))
    
    print("\nUBP CRV correlations:")
    print(corr_matrix['ubp_crv'].sort_values(ascending=False))
    
    # Top compounds by UBP metrics
    print(f"\n{'='*60}")
    print("TOP 10 COMPOUNDS BY UBP ENERGY")
    print(f"{'='*60}")
    top_energy = results_df.nlargest(10, 'ubp_energy')[
        ['chembl_id', 'name', 'therapeutic_area', 'ubp_energy', 'ubp_nrci', 'ubp_crv']
    ]
    print(top_energy.to_string(index=False))
    
    print(f"\n{'='*60}")
    print("TOP 10 COMPOUNDS BY UBP NRCI (COHERENCE)")
    print(f"{'='*60}")
    top_nrci = results_df.nlargest(10, 'ubp_nrci')[
        ['chembl_id', 'name', 'therapeutic_area', 'ubp_energy', 'ubp_nrci', 'ubp_crv']
    ]
    print(top_nrci.to_string(index=False))
    
    print(f"\n{'='*60}")
    print("TOP 10 COMPOUNDS BY THERAPEUTIC POTENTIAL")
    print(f"{'='*60}")
    top_potential = results_df.nlargest(10, 'ubp_therapeutic_potential')[
        ['chembl_id', 'name', 'therapeutic_area', 'ubp_therapeutic_potential', 'drug_likeness_score']
    ]
    print(top_potential.to_string(index=False))
    
    # Save summary statistics
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    summary = {
        'total_compounds': len(results_df),
        'therapeutic_areas': results_df['therapeutic_area'].value_counts().to_dict(),
        'ubp_energy': {
            'mean': float(results_df['ubp_energy'].mean()),
            'median': float(results_df['ubp_energy'].median()),
            'std': float(results_df['ubp_energy'].std()),
            'min': float(results_df['ubp_energy'].min()),
            'max': float(results_df['ubp_energy'].max())
        },
        'ubp_nrci': {
            'mean': float(results_df['ubp_nrci'].mean()),
            'median': float(results_df['ubp_nrci'].median()),
            'std': float(results_df['ubp_nrci'].std()),
            'min': float(results_df['ubp_nrci'].min()),
            'max': float(results_df['ubp_nrci'].max())
        },
        'ubp_crv': {
            'mean': float(results_df['ubp_crv'].mean()),
            'median': float(results_df['ubp_crv'].median()),
            'std': float(results_df['ubp_crv'].std()),
            'min': float(results_df['ubp_crv'].min()),
            'max': float(results_df['ubp_crv'].max())
        },
        'correlations': corr_matrix.to_dict()
    }
    
    summary_file = os.path.join(output_dir, f'ubp_analysis_summary_{timestamp}.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n✓ Summary statistics saved to: {summary_file}")
    
    return summary


def main():
    """Main execution."""
    # Setup
    data_file = '/home/ubuntu/ubp_medicine_study/pharmaceutical_1000_compounds.csv'
    output_dir = '/home/ubuntu/ubp_medicine_study/ubp_results'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    df = load_compound_dataset(data_file)
    
    # Run UBP analysis
    results_df, errors = run_ubp_analysis(df, output_dir)
    
    # Analyze results
    summary = analyze_results(results_df, output_dir)
    
    print("\n" + "="*80)
    print("UBP ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nResults directory: {output_dir}")
    print(f"Total compounds analyzed: {len(results_df)}")
    print(f"Errors: {len(errors)}")
    
    return results_df, summary


if __name__ == '__main__':
    results_df, summary = main()
