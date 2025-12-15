#!/usr/bin/env python3
"""Extract summary and key information from the UBP notebook."""

import json
import sys
from pathlib import Path

def extract_notebook_summary(notebook_path, output_path):
    """Extract structured summary from notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    total_cells = len(nb['cells'])
    code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
    markdown_cells = [c for c in nb['cells'] if c['cell_type'] == 'markdown']

    print(f"Total cells: {total_cells}")
    print(f"Code cells: {len(code_cells)}")
    print(f"Markdown cells: {len(markdown_cells)}")

    # Extract cell contents
    summary = {
        'metadata': nb.get('metadata', {}),
        'total_cells': total_cells,
        'code_cell_count': len(code_cells),
        'markdown_cell_count': len(markdown_cells),
        'markdown_sections': [],
        'code_summaries': [],
        'all_markdown_text': [],
        'key_variables': set(),
        'imports': set()
    }

    # Extract markdown (documentation)
    for i, cell in enumerate(markdown_cells):
        source = cell.get('source', [])
        if isinstance(source, list):
            text = ''.join(source)
        else:
            text = source

        if text.strip():
            summary['all_markdown_text'].append({
                'cell_index': i,
                'text': text[:1000]  # First 1000 chars
            })

            # Check for section headers
            if text.startswith('#'):
                summary['markdown_sections'].append(text.split('\n')[0])

    # Extract code patterns
    for i, cell in enumerate(code_cells[:50]):  # First 50 code cells for analysis
        source = cell.get('source', [])
        if isinstance(source, list):
            code = ''.join(source)
        else:
            code = source

        # Extract imports
        for line in code.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                summary['imports'].add(line.split('#')[0].strip())

        # Look for key variable definitions
        if '=' in code:
            for line in code.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    var_name = line.split('=')[0].strip()
                    if var_name and not var_name.startswith('_'):
                        summary['key_variables'].add(var_name.split()[0] if ' ' in var_name else var_name)

    # Convert sets to lists for JSON serialization
    summary['key_variables'] = sorted(list(summary['key_variables']))[:100]
    summary['imports'] = sorted(list(summary['imports']))

    # Save summary
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary saved to: {output_path}")
    print(f"\nMarkdown sections found:")
    for section in summary['markdown_sections'][:20]:
        print(f"  {section}")

    print(f"\nKey imports:")
    for imp in summary['imports'][:15]:
        print(f"  {imp}")

    return summary

if __name__ == '__main__':
    notebook_path = '/app/sandbox/session_20251215_122025_664f88889fdc/user_data/UBP_UNIFIED_SYSTEM_1.ipynb'
    output_path = '/app/sandbox/session_20251215_122025_664f88889fdc/data/notebook_summary.json'

    extract_notebook_summary(notebook_path, output_path)
