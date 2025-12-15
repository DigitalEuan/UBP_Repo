#!/usr/bin/env python3
"""Extract detailed content from notebook for analysis."""

import json
from pathlib import Path

def extract_detailed_content(notebook_path, output_dir):
    """Extract all markdown and code content in readable format."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Extract all markdown
    markdown_output = output_dir / 'notebook_markdown.md'
    with open(markdown_output, 'w', encoding='utf-8') as f:
        f.write("# UBP UNIFIED SYSTEM - Documentation\n\n")
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'markdown':
                source = cell.get('source', [])
                if isinstance(source, list):
                    text = ''.join(source)
                else:
                    text = source

                if text.strip():
                    f.write(f"{text}\n\n")
                    f.write("---\n\n")

    print(f"Markdown content saved to: {markdown_output}")

    # Extract code into numbered files
    code_dir = output_dir / 'notebook_code'
    code_dir.mkdir(exist_ok=True)

    code_index = []
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                code = ''.join(source)
            else:
                code = source

            if code.strip():
                code_file = code_dir / f'cell_{i:03d}.py'
                with open(code_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Cell {i} from UBP_UNIFIED_SYSTEM_1.ipynb\n\n")
                    f.write(code)

                # Extract first line for index
                first_line = code.split('\n')[0][:100]
                code_index.append({
                    'cell_number': i,
                    'file': str(code_file),
                    'preview': first_line
                })

    # Save code index
    with open(output_dir / 'code_index.json', 'w') as f:
        json.dump(code_index, f, indent=2)

    print(f"Code cells saved to: {code_dir}")
    print(f"Total code cells extracted: {len(code_index)}")

    # Extract outputs from cells
    outputs_file = output_dir / 'notebook_outputs.txt'
    with open(outputs_file, 'w', encoding='utf-8') as f:
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                outputs = cell.get('outputs', [])
                if outputs:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"CELL {i} OUTPUTS:\n")
                    f.write(f"{'='*80}\n")
                    for output in outputs:
                        if 'text' in output:
                            text = output['text']
                            if isinstance(text, list):
                                text = ''.join(text)
                            f.write(text)
                            f.write('\n')
                        if 'data' in output and 'text/plain' in output['data']:
                            data = output['data']['text/plain']
                            if isinstance(data, list):
                                data = ''.join(data)
                            f.write(data)
                            f.write('\n')

    print(f"Outputs saved to: {outputs_file}")

if __name__ == '__main__':
    notebook_path = '/app/sandbox/session_20251215_122025_664f88889fdc/user_data/UBP_UNIFIED_SYSTEM_1.ipynb'
    output_dir = '/app/sandbox/session_20251215_122025_664f88889fdc/data/notebook_extracted'

    extract_detailed_content(notebook_path, output_dir)
