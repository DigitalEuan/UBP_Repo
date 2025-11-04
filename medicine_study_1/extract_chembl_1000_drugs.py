#!/usr/bin/env python3
"""
Extract 1000 FDA-approved drugs from ChEMBL 36 HDF5 database
Real pharmaceutical compounds with complete molecular and bioactivity data
"""

import pandas as pd
import numpy as np
import h5py
import json
from collections import defaultdict

def load_chembl_hdf5(filepath='/home/ubuntu/ubp_medicine_study/chembl_36.h5'):
    """Load ChEMBL HDF5 database"""
    print("Loading ChEMBL 36 HDF5 database...")
    print("Available tables:")
    
    with h5py.File(filepath, 'r') as f:
        print(f"Tables in HDF5: {list(f.keys())}")
        
        # List all groups and datasets
        def print_structure(name, obj):
            print(f"  {name}: {type(obj)}")
        
        f.visititems(print_structure)
    
    return filepath

def extract_fda_drugs_from_hdf5(filepath, target_count=1000):
    """
    Extract FDA-approved drugs from ChEMBL HDF5
    """
    print(f"\nExtracting up to {target_count} FDA-approved drugs...")
    
    try:
        # Try to read molecule data
        with pd.HDFStore(filepath, 'r') as store:
            print(f"Store keys: {store.keys()}")
            
            # Try different possible table names
            possible_tables = ['/molecule_dictionary', '/compounds', '/molecules', 
                             '/compound_structures', '/chembl_id_lookup']
            
            for table in possible_tables:
                if table in store.keys():
                    print(f"\nReading table: {table}")
                    df = store[table]
                    print(f"Shape: {df.shape}")
                    print(f"Columns: {df.columns.tolist()}")
                    print(f"Sample:\n{df.head()}")
                    return df
                    
    except Exception as e:
        print(f"Error reading with HDFStore: {e}")
        print("\nTrying direct h5py access...")
        
        with h5py.File(filepath, 'r') as f:
            # Try to find and read datasets
            for key in f.keys():
                print(f"\nExamining: {key}")
                item = f[key]
                if isinstance(item, h5py.Dataset):
                    print(f"  Dataset shape: {item.shape}")
                    print(f"  Dataset dtype: {item.dtype}")
                    # Try to read first few rows
                    try:
                        data = item[:10]
                        print(f"  Sample data: {data}")
                    except:
                        pass
    
    return None

def main():
    """Main execution"""
    print("="*80)
    print("ChEMBL 36 Database Extraction - 1000 FDA-Approved Drugs")
    print("="*80 + "\n")
    
    filepath = '/home/ubuntu/ubp_medicine_study/chembl_36.h5'
    
    # First, explore the structure
    load_chembl_hdf5(filepath)
    
    # Extract drugs
    df = extract_fda_drugs_from_hdf5(filepath, target_count=1000)
    
    if df is not None:
        print(f"\nSuccessfully extracted {len(df)} compounds")
        output_file = '/home/ubuntu/ubp_medicine_study/chembl_1000_drugs.csv'
        df.to_csv(output_file, index=False)
        print(f"Saved to: {output_file}")
    else:
        print("\nFailed to extract data. Will try alternative approach...")

if __name__ == '__main__':
    main()
