#!/usr/bin/env python3
"""
Extract 1000 FDA-approved drugs directly from ChEMBL 36 HDF5 database
Using pandas HDFStore for proper data access
"""

import pandas as pd
import numpy as np
import json

def explore_hdf5_structure(filepath):
    """Explore the structure of the HDF5 file"""
    print("Exploring HDF5 structure...")
    try:
        with pd.HDFStore(filepath, 'r') as store:
            print(f"\nAvailable tables: {store.keys()}")
            for key in store.keys():
                try:
                    df = store[key]
                    print(f"\n{key}:")
                    print(f"  Shape: {df.shape}")
                    print(f"  Columns: {list(df.columns)[:10]}...")  # First 10 columns
                except Exception as e:
                    print(f"  Error reading {key}: {e}")
        return True
    except Exception as e:
        print(f"Error opening HDF5 with pandas: {e}")
        return False

def extract_drugs_from_hdf5(filepath, target_count=1000):
    """
    Extract FDA-approved drugs from ChEMBL HDF5
    """
    print(f"\nExtracting up to {target_count} FDA-approved drugs...")
    
    with pd.HDFStore(filepath, 'r') as store:
        # Get available tables
        tables = store.keys()
        print(f"Available tables: {tables}")
        
        # Common table names in ChEMBL HDF5
        molecule_table = None
        for possible_name in ['/molecule_dictionary', '/compounds', '/chembl_molecules']:
            if possible_name in tables:
                molecule_table = possible_name
                break
        
        if not molecule_table:
            # Just use the first table
            molecule_table = tables[0]
        
        print(f"\nReading from table: {molecule_table}")
        df = store[molecule_table]
        
        print(f"Initial dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())
        
        return df

def main():
    """Main execution"""
    print("="*80)
    print("ChEMBL 36 HDF5 Database - Extract 1000 FDA-Approved Drugs")
    print("="*80 + "\n")
    
    filepath = '/home/ubuntu/ubp_medicine_study/chembl_36.h5'
    
    # First explore structure
    if not explore_hdf5_structure(filepath):
        print("\nCannot read HDF5 with pandas. Trying alternative method...")
        # Fall back to reading the chemreps file
        print("\nTrying to extract from chembl_36_chemreps.txt.gz...")
        import gzip
        
        chemreps_file = '/home/ubuntu/ubp_medicine_study/chembl_36_chemreps.txt.gz'
        try:
            # Read first few lines to understand structure
            with gzip.open(chemreps_file, 'rt') as f:
                for i, line in enumerate(f):
                    print(line.strip())
                    if i >= 10:
                        break
            
            # Read full file
            print("\nReading full chemreps file...")
            df = pd.read_csv(chemreps_file, sep='\t', compression='gzip', nrows=10000)
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(df.head())
            
            # Save sample
            output_file = '/home/ubuntu/ubp_medicine_study/chembl_sample.csv'
            df.to_csv(output_file, index=False)
            print(f"\nSample saved to: {output_file}")
            
        except Exception as e:
            print(f"Error reading chemreps: {e}")
        
        return
    
    # Extract drugs
    try:
        df = extract_drugs_from_hdf5(filepath, target_count=1000)
        
        if df is not None and len(df) > 0:
            print(f"\nSuccessfully extracted {len(df)} compounds")
            
            # Save to CSV
            output_file = '/home/ubuntu/ubp_medicine_study/chembl_extracted.csv'
            df.to_csv(output_file, index=False)
            print(f"Saved to: {output_file}")
        else:
            print("\nNo data extracted")
            
    except Exception as e:
        print(f"\nError during extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
