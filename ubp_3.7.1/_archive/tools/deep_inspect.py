#!/usr/bin/env python3.11
"""
UBP 3.7 Deep Inspection Script
Checks every file for real implementations vs mocks/placeholders/simplified code
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple

class DeepInspector:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.results = {}
        self.issues = []
        
    def inspect_file(self, filepath: Path) -> Dict:
        """Inspect a single Python file from multiple angles"""
        result = {
            'path': str(filepath.relative_to(self.root_dir)),
            'imports_ok': False,
            'has_real_impl': False,
            'has_placeholders': False,
            'has_todos': False,
            'class_count': 0,
            'function_count': 0,
            'line_count': 0,
            'issues': []
        }
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                result['line_count'] = len(content.split('\n'))
                
            # Check for placeholder/mock indicators
            placeholder_indicators = [
                'TODO', 'FIXME', 'HACK', 'XXX',
                'placeholder', 'mock', 'stub', 'simplified',
                'not implemented', 'pass  # implementation',
                'raise NotImplementedError'
            ]
            
            for indicator in placeholder_indicators:
                if indicator.lower() in content.lower():
                    result['has_placeholders'] = True
                    result['issues'].append(f"Contains '{indicator}'")
                    
            # Parse AST to count classes and functions
            try:
                tree = ast.parse(content)
                result['class_count'] = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
                result['function_count'] = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
                
                # Check for empty functions (just 'pass')
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                            result['issues'].append(f"Empty function: {node.name}")
                            
            except SyntaxError as e:
                result['issues'].append(f"Syntax error: {e}")
                
            # Try to import the module
            try:
                spec = importlib.util.spec_from_file_location("test_module", filepath)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules['test_module'] = module
                    spec.loader.exec_module(module)
                    result['imports_ok'] = True
                    del sys.modules['test_module']
            except Exception as e:
                result['issues'].append(f"Import failed: {str(e)[:100]}")
                
            # Determine if implementation is real
            if result['class_count'] > 0 or result['function_count'] > 0:
                if not result['has_placeholders'] and result['line_count'] > 50:
                    result['has_real_impl'] = True
                elif result['line_count'] > 20 and not result['has_placeholders']:
                    result['has_real_impl'] = True
                    
        except Exception as e:
            result['issues'].append(f"File read error: {e}")
            
        return result
    
    def inspect_all(self) -> Dict:
        """Inspect all Python files in the directory"""
        py_files = list(self.root_dir.rglob("*.py"))
        py_files = [f for f in py_files if '__pycache__' not in str(f)]
        
        print(f"Inspecting {len(py_files)} Python files...")
        
        for filepath in sorted(py_files):
            result = self.inspect_file(filepath)
            self.results[result['path']] = result
            
            if result['issues']:
                self.issues.append((result['path'], result['issues']))
                
        return self.results
    
    def generate_report(self) -> str:
        """Generate inspection report"""
        report = []
        report.append("=" * 80)
        report.append("UBP 3.7 DEEP INSPECTION REPORT")
        report.append("=" * 80)
        report.append("")
        
        total_files = len(self.results)
        imports_ok = sum(1 for r in self.results.values() if r['imports_ok'])
        real_impl = sum(1 for r in self.results.values() if r['has_real_impl'])
        has_placeholders = sum(1 for r in self.results.values() if r['has_placeholders'])
        
        report.append(f"Total files inspected: {total_files}")
        report.append(f"Files with successful imports: {imports_ok}/{total_files} ({imports_ok/total_files*100:.1f}%)")
        report.append(f"Files with real implementations: {real_impl}/{total_files} ({real_impl/total_files*100:.1f}%)")
        report.append(f"Files with placeholders/TODOs: {has_placeholders}/{total_files}")
        report.append("")
        
        if self.issues:
            report.append("=" * 80)
            report.append(f"ISSUES FOUND ({len(self.issues)} files with issues)")
            report.append("=" * 80)
            report.append("")
            
            for filepath, issues in self.issues:
                report.append(f"\n{filepath}:")
                for issue in issues:
                    report.append(f"  - {issue}")
        else:
            report.append("✅ NO ISSUES FOUND - All files appear to be real, working implementations")
            
        report.append("")
        report.append("=" * 80)
        report.append("DETAILED RESULTS")
        report.append("=" * 80)
        report.append("")
        
        for filepath, result in sorted(self.results.items()):
            status = "✅" if result['imports_ok'] and result['has_real_impl'] else "⚠️"
            report.append(f"{status} {filepath}")
            report.append(f"   Imports: {'✓' if result['imports_ok'] else '✗'} | "
                         f"Real impl: {'✓' if result['has_real_impl'] else '✗'} | "
                         f"Classes: {result['class_count']} | "
                         f"Functions: {result['function_count']} | "
                         f"Lines: {result['line_count']}")
            if result['issues']:
                for issue in result['issues']:
                    report.append(f"   ⚠️  {issue}")
            report.append("")
            
        return "\n".join(report)

if __name__ == "__main__":
    inspector = DeepInspector("/home/ubuntu/UBP_Repo/ubp_3.7")
    inspector.inspect_all()
    report = inspector.generate_report()
    
    print(report)
    
    # Save report
    with open("/home/ubuntu/ubp37_deep_inspection_results.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Report saved to /home/ubuntu/ubp37_deep_inspection_results.txt")
