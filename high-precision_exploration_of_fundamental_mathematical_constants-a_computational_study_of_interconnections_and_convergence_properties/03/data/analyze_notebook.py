#!/usr/bin/env python3
"""Analyze the UBP notebook to extract key information."""

import json
import re
from pathlib import Path

notebook_path = Path("/app/sandbox/session_20251215_122025_664f88889fdc/user_data/UBP_UNIFIED_SYSTEM_1.ipynb")

print("Loading notebook...")
with open(notebook_path, 'r') as f:
    nb = json.load(f)

cells = nb.get('cells', [])
print(f"Total cells: {len(cells)}")

# Extract markdown headers
print("\n=== Notebook Structure (Headers) ===")
for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = cell.get('source', [])
        if isinstance(source, list):
            source = ''.join(source)
        # Find headers
        lines = source.split('\n')
        for line in lines[:5]:  # First 5 lines of each markdown cell
            if line.strip().startswith('#'):
                print(f"Cell {i}: {line.strip()}")

# Search for delta_tau and delta_W mentions
print("\n=== Mentions of δ_τ (delta_tau) and δ_W (delta_W) ===")
for i, cell in enumerate(cells):
    source = cell.get('source', [])
    if isinstance(source, list):
        source = ''.join(source)

    # Search for relevant terms
    if any(term in source.lower() for term in ['delta_tau', 'δ_τ', 'tau', 'delta_w', 'δ_w', 'weak boson', 'dynamic field']):
        # Only show if it's in markdown or has significant mention
        if cell.get('cell_type') == 'markdown' or len(source) < 500:
            print(f"\n--- Cell {i} ({cell.get('cell_type')}) ---")
            print(source[:500])

# Look for the geometric law Y definition
print("\n=== Searching for Y = π/(π² + 2) definition ===")
for i, cell in enumerate(cells):
    source = cell.get('source', [])
    if isinstance(source, list):
        source = ''.join(source)

    if 'pi**2 + 2' in source or 'π²' in source or 'Y =' in source:
        print(f"\n--- Cell {i} ({cell.get('cell_type')}) ---")
        print(source[:400])

print("\n=== Analysis complete ===")
