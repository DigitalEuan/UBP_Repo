#!/usr/bin/env python3
"""
Final Data Loader - Comprehensive JSON Periodic Table

This loader parses the complete PeriodicTableJSON.json file, 
extracting all necessary fields including electron configuration and block data.

Author: Euan Craig (via Manus AI)
Date: December 10, 2025
"""

import json
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Any

def load_periodic_table_from_json(json_path: str) -> List[Dict[str, Any]]:
    """Loads the full periodic table from the comprehensive JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        return []

    elements = data.get('elements', [])
    
    # Clean and parse data
    for elem in elements:
        for key, value in elem.items():
            if isinstance(value, (int, float)):
                try:
                    elem[key] = Decimal(str(value))
                except InvalidOperation:
                    elem[key] = None # or some other default
            elif value is None:
                elem[key] = None

    return elements

if __name__ == '__main__':
    # Example usage and data validation
    json_file_path = '../data/PeriodicTableJSON.json'
    all_elements = load_periodic_table_from_json(json_file_path)
    
    if all_elements:
        print(f"Successfully loaded {len(all_elements)} elements.")
        
        # Validate a few key elements and fields
        hydrogen = all_elements[0]
        chromium = next((e for e in all_elements if e['symbol'] == 'Cr'), None)
        oganesson = all_elements[-1]

        print("\n--- Data Validation ---")
        print(f"Hydrogen (H):")
        print(f"  - Electron Config: {hydrogen.get('electron_configuration')}")
        print(f"  - Block: {hydrogen.get('block')}")

        if chromium:
            print(f"Chromium (Cr) - Anomaly Check:")
            print(f"  - Electron Config: {chromium.get('electron_configuration')}")
            print(f"  - Expected Anomaly: 3d5 4s1")

        print(f"Oganesson (Og):")
        print(f"  - Atomic Number: {oganesson.get('number')}")
        print(f"  - Electron Config Semantic: {oganesson.get('electron_configuration_semantic')}")
        print(f"  - Block: {oganesson.get('block')}")
        print("-----------------------")
    else:
        print("Failed to load element data.")
