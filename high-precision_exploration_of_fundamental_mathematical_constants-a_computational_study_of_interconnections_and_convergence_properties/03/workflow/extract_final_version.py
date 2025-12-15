#!/usr/bin/env python3
"""Extract the final v4.0 code and documentation from the notebook."""

import json
from pathlib import Path

notebook_path = Path("/app/sandbox/session_20251215_122025_664f88889fdc/user_data/UBP_UNIFIED_SYSTEM_1.ipynb")

with open(notebook_path, 'r') as f:
    nb = json.load(f)

cells = nb.get('cells', [])

# Find cells 147-150 (final documentation and v4.0 code)
print("=== EXTRACTING FINAL CELLS (147-150) ===\n")

for i in [147, 148, 149, 150]:
    if i < len(cells):
        cell = cells[i]
        cell_type = cell.get('cell_type')
        source = cell.get('source', [])
        if isinstance(source, list):
            source = ''.join(source)

        print(f"\n{'='*80}")
        print(f"CELL {i} ({cell_type})")
        print('='*80)
        print(source)

        # Save code cells to files
        if cell_type == 'code' and i == 149:
            output_path = Path("/app/sandbox/session_20251215_122025_664f88889fdc/workflow/ubp_v4_0_original.py")
            with open(output_path, 'w') as f:
                f.write(source)
            print(f"\n[Saved to {output_path}]")

print("\n\n=== EXTRACTION COMPLETE ===")
