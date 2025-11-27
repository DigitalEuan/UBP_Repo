#!/usr/bin/env python3.11
"""Fix all import paths and version headers in UBP 3.7"""

import os
import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_FIXES = [
    # Old absolute imports to new relative imports
    (r'from core.system_constants import', 'from core.system_constants import'),
    (r'from core.y_constants import', 'from core.y_constants import'),
    (r'from core.coherence_substrate import', 'from core.coherence_substrate import'),
    (r'from core.state import', 'from core.state import'),
    (r'from error_correction.glr_base import', 'from error_correction.glr_base import'),
    (r'from core from core import system_constants', 'from core from core from core import system_constants'),
    (r'from core from core import y_constants', 'from core from core from core import y_constants'),
    
    # Fix version headers
    (r'v3\.[0-6]\+?', 'v3.7'),
]

def fix_file(filepath):
    """Fix imports and headers in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for pattern, replacement in IMPORT_FIXES:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes.append(f"  - {pattern} → {replacement}")
            content = new_content
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes
    return None

def main():
    """Fix all Python files in UBP 3.7."""
    root = Path('/home/ubuntu/UBP_Repo/ubp_3.7')
    fixed_count = 0
    
    for pyfile in root.rglob('*.py'):
        if '__pycache__' in str(pyfile):
            continue
        
        changes = fix_file(pyfile)
        if changes:
            print(f"\n✓ Fixed: {pyfile.relative_to(root)}")
            for change in changes:
                print(change)
            fixed_count += 1
    
    print(f"\n{'='*70}")
    print(f"Fixed {fixed_count} files")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
