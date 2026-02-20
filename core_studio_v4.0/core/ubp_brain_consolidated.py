"""
================================================================================
UBP BRAIN v3.0 - COMPLETE REWRITE
================================================================================
Universal Binary Principal - Knowledge Reasoning Engine

Key Architecture Insights (Feb 2026):
1. Fingerprint = SHA256(math field) - this encodes MEANINGFUL dimensions
2. Vectors are PRE-COMPUTED and stored (not algorithmically generated from hash)
3. Hierarchy describes PHYSICAL composition (e.g., proton = 2×UP + 1×DOWN)
4. NRCI = 10 / (10 + TAX) - verified 100%
5. TAX encodes hierarchical complexity (NOT simple weight function)
6. Build UP: primitives -> composites -> molecules
7. Build DOWN: decompose to primitives

This rewrite focuses on:
- Clean hierarchy traversal
- TAX pattern discovery
- Building meaningful insights from information dimensions

Author: Euan R A Craig, New Zealand
Version: 3.0 (Clean Rewrite)
Date: 2026-02-20
================================================================================
"""

import json
import hashlib
import re
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any, Set
from collections import defaultdict, deque

try:
    from ubp_core_v5_3_merged import GOLAY_ENGINE, BinaryLinearAlgebra
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("[Brain v3] WARNING: Core not available")


# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class UBPEntry:
    """Single UBP knowledge base entry"""
    ubp_id: str
    fingerprint: str  # SHA256(math)
    math: str
    lexicon: str
    hierarchy: str
    vector: List[int]
    nrci: Fraction
    tax: Fraction
    weight: int
    tags: List[str] = field(default_factory=list)
    raw_data: Dict = field(default_factory=dict)
    
    @property
    def nrci_float(self) -> float:
        return float(self.nrci)
    
    @property
    def tax_float(self) -> float:
        return float(self.tax)
    
    def get_components(self) -> List[Tuple[int, str]]:
        """
        Parse hierarchy to extract components.
        Returns: [(count, ubp_id), ...]
        
        Example: "2×PARTICLE_QUARK_UP_001 + 1×PARTICLE_QUARK_DOWN_001"
        Returns: [(2, 'PARTICLE_QUARK_UP_001'), (1, 'PARTICLE_QUARK_DOWN_001')]
        """
        if self.hierarchy in ('absolute_primitive', 'atomic', ''):
            return []
        
        components = []
        # Match patterns like "2×ID" or "1×ID"
        pattern = r'(\d+)×([A-Z_0-9]+)'
        matches = re.findall(pattern, self.hierarchy)
        
        for count_str, comp_id in matches:
            count = int(count_str)
            if count > 0:  # Ignore zero coefficients
                components.append((count, comp_id))
        
        return components
    
    def is_primitive(self) -> bool:
        """Check if this is an absolute primitive"""
        return self.hierarchy in ('absolute_primitive', 'atomic')
    
    def classify_level(self) -> str:
        """Classify hierarchical level"""
        if self.is_primitive():
            return 'primitive'
        
        # Check what components it contains
        comps = self.get_components()
        if not comps:
            return 'unknown'
        
        comp_ids = [c[1] for c in comps]
        
        # Level 1: made from quarks/leptons
        if any('QUARK' in cid for cid in comp_ids):
            return 'composite_1_nucleon'
        
        # Level 2: made from protons/neutrons/electrons
        if any(cid in ['PARTICLE_PROTON_001', 'PARTICLE_NEUTRON_001', 'PARTICLE_ELECTRON_001'] for cid in comp_ids):
            return 'composite_2_element'
        
        # Level 3: made from elements
        if any('ELEM_' in cid for cid in comp_ids):
            return 'composite_3_molecule'
        
        # Level 4: made from molecules
        if any('MOLECULE_' in cid for cid in comp_ids):
            return 'composite_4_structure'
        
        return 'unknown'


# ==============================================================================
# KNOWLEDGE BASE
# ==============================================================================

class UBPKnowledgeBase:
    """Unified knowledge base with fast lookups"""
    
    def __init__(self):
        self.entries: Dict[str, UBPEntry] = {}  # ubp_id -> entry
        self.by_fingerprint: Dict[str, UBPEntry] = {}  # fingerprint -> entry
        self.by_level: Dict[str, List[UBPEntry]] = defaultdict(list)
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)  # parent -> {children}
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)  # child -> {parents}
        
    def load_from_json(self, filename: str):
        """Load KB from JSON file"""
        print(f"[KB v3] Loading {filename}...")
        
        with open(filename) as f:
            data = json.load(f)
        
        for fingerprint, raw_entry in data.items():
            try:
                # Extract fields
                ubp_id = raw_entry.get('ubp_id', 'UNKNOWN')
                math = raw_entry.get('math', '')
                lexicon = raw_entry.get('lexicon', '')
                atlas = raw_entry.get('atlas', {})
                
                hierarchy = atlas.get('hierarchy', '')
                vector = atlas.get('vector', [])
                nrci_str = atlas.get('nrci', '1/1')
                tax_str = atlas.get('tax', '0/1')
                weight = atlas.get('weight', sum(vector) if vector else 0)
                tags = raw_entry.get('tags', [])
                
                # Parse fractions
                try:
                    nrci = Fraction(nrci_str)
                except:
                    nrci = Fraction(1, 1)
                
                try:
                    tax = Fraction(tax_str)
                except:
                    tax = Fraction(0, 1)
                
                # Verify fingerprint
                computed_fp = hashlib.sha256(math.encode()).hexdigest()
                if computed_fp != fingerprint:
                    print(f"[KB v3] WARNING: Fingerprint mismatch for {ubp_id}")
                
                # Create entry
                entry = UBPEntry(
                    ubp_id=ubp_id,
                    fingerprint=fingerprint,
                    math=math,
                    lexicon=lexicon,
                    hierarchy=hierarchy,
                    vector=vector,
                    nrci=nrci,
                    tax=tax,
                    weight=weight,
                    tags=tags,
                    raw_data=raw_entry
                )
                
                # Index it
                self.entries[ubp_id] = entry
                self.by_fingerprint[fingerprint] = entry
                
                # Classify level
                level = entry.classify_level()
                self.by_level[level].append(entry)
                
                # Build dependency graph
                comps = entry.get_components()
                if comps:
                    for count, comp_id in comps:
                        self.dependency_graph[ubp_id].add(comp_id)
                        self.reverse_dependencies[comp_id].add(ubp_id)
                
            except Exception as e:
                print(f"[KB v3] Error loading entry {fingerprint[:16]}: {e}")
        
        print(f"[KB v3] Loaded {len(self.entries)} entries")
        print(f"[KB v3] Levels:")
        for level in ['primitive', 'composite_1_nucleon', 'composite_2_element', 
                      'composite_3_molecule', 'composite_4_structure', 'unknown']:
            count = len(self.by_level[level])
            if count > 0:
                print(f"  {level}: {count}")
    
    def get(self, ubp_id: str) -> Optional[UBPEntry]:
        """Get entry by ubp_id"""
        return self.entries.get(ubp_id)
    
    def get_by_fingerprint(self, fp: str) -> Optional[UBPEntry]:
        """Get entry by fingerprint"""
        return self.by_fingerprint.get(fp)
    
    def get_primitives(self) -> List[UBPEntry]:
        """Get all absolute primitives"""
        return self.by_level['primitive']
    
    def get_children(self, ubp_id: str) -> List[UBPEntry]:
        """Get direct children (components) of an entry"""
        child_ids = self.dependency_graph.get(ubp_id, set())
        return [self.get(cid) for cid in child_ids if self.get(cid)]
    
    def get_parents(self, ubp_id: str) -> List[UBPEntry]:
        """Get direct parents (objects that contain this entry)"""
        parent_ids = self.reverse_dependencies.get(ubp_id, set())
        return [self.get(pid) for pid in parent_ids if self.get(pid)]


# ==============================================================================
# HIERARCHY ENGINE
# ==============================================================================

class HierarchyEngine:
    """Traverse hierarchy up and down"""
    
    def __init__(self, kb: UBPKnowledgeBase):
        self.kb = kb
    
    def decompose_to_primitives(self, ubp_id: str) -> Dict[str, int]:
        """
        Decompose an object down to absolute primitives.
        Returns: {primitive_id: count}
        
        Example: ELEM_H_001 -> {PARTICLE_PROTON_001: 1, PARTICLE_ELECTRON_001: 1}
                 PARTICLE_PROTON_001 -> {PARTICLE_QUARK_UP_001: 2, PARTICLE_QUARK_DOWN_001: 1}
        """
        entry = self.kb.get(ubp_id)
        if not entry:
            return {}
        
        if entry.is_primitive():
            return {ubp_id: 1}
        
        # BFS decomposition
        composition = defaultdict(int)
        queue = deque([(ubp_id, 1)])  # (id, multiplier)
        visited = set()
        
        while queue:
            current_id, multiplier = queue.popleft()
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            current_entry = self.kb.get(current_id)
            if not current_entry:
                continue
            
            if current_entry.is_primitive():
                composition[current_id] += multiplier
            else:
                components = current_entry.get_components()
                for count, comp_id in components:
                    queue.append((comp_id, multiplier * count))
        
        return dict(composition)
    
    def build_from_primitives(self, primitive_ids: List[str]) -> List[UBPEntry]:
        """
        Find all objects that can be built from given primitives.
        Uses reverse dependency graph.
        """
        if not primitive_ids:
            return []
        
        # Start with primitives
        buildable = set(primitive_ids)
        result = []
        
        # Iteratively add objects whose dependencies are satisfied
        changed = True
        iterations = 0
        max_iterations = 10  # Prevent infinite loops
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            for entry in self.kb.entries.values():
                if entry.ubp_id in buildable:
                    continue
                
                # Check if all dependencies are satisfied
                comps = entry.get_components()
                if comps:
                    comp_ids = [c[1] for c in comps]
                    if all(cid in buildable for cid in comp_ids):
                        buildable.add(entry.ubp_id)
                        result.append(entry)
                        changed = True
        
        return result
    
    def find_path_to_primitive(self, ubp_id: str, target_primitive: str) -> List[str]:
        """
        Find decomposition path from object to a specific primitive.
        Returns list of ubp_ids in the path.
        """
        entry = self.kb.get(ubp_id)
        if not entry:
            return []
        
        if ubp_id == target_primitive:
            return [ubp_id]
        
        if entry.is_primitive():
            return []
        
        # BFS to find path
        queue = deque([(ubp_id, [ubp_id])])
        visited = set()
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id == target_primitive:
                return path
            
            current_entry = self.kb.get(current_id)
            if current_entry:
                comps = current_entry.get_components()
                for count, comp_id in comps:
                    if comp_id not in visited:
                        queue.append((comp_id, path + [comp_id]))
        
        return []


# ==============================================================================
# TAX ANALYZER
# ==============================================================================

class TAXAnalyzer:
    """Analyze TAX patterns to discover the formula"""
    
    def __init__(self, kb: UBPKnowledgeBase, hierarchy_engine: HierarchyEngine):
        self.kb = kb
        self.hierarchy = hierarchy_engine
    
    def analyze_composition_tax(self, ubp_id: str) -> Dict[str, Any]:
        """
        Analyze how TAX relates to component TAX values.
        """
        entry = self.kb.get(ubp_id)
        if not entry or entry.is_primitive():
            return {}
        
        components = entry.get_components()
        if not components:
            return {}
        
        comp_taxes = []
        comp_weights = []
        comp_nrcis = []
        
        for count, comp_id in components:
            comp = self.kb.get(comp_id)
            if comp:
                comp_taxes.append((count, comp.tax_float))
                comp_weights.append((count, comp.weight))
                comp_nrcis.append((count, comp.nrci_float))
        
        # Compute various aggregations
        simple_sum = sum(count * tax for count, tax in comp_taxes)
        weighted_sum = sum(count * tax * weight for (count, tax), (_, weight) in zip(comp_taxes, comp_weights))
        
        return {
            'ubp_id': ubp_id,
            'tax': entry.tax_float,
            'weight': entry.weight,
            'nrci': entry.nrci_float,
            'components': components,
            'component_taxes': comp_taxes,
            'component_weights': comp_weights,
            'simple_sum_tax': simple_sum,
            'weighted_sum_tax': weighted_sum,
            'ratio_simple': entry.tax_float / simple_sum if simple_sum > 0 else 0,
            'ratio_weighted': entry.tax_float / weighted_sum if weighted_sum > 0 else 0
        }
    
    def find_tax_patterns(self) -> Dict[str, List[Dict]]:
        """
        Analyze TAX patterns across all levels.
        """
        patterns = defaultdict(list)
        
        for level in ['composite_1_nucleon', 'composite_2_element', 'composite_3_molecule']:
            entries = self.kb.by_level[level]
            
            for entry in entries:
                analysis = self.analyze_composition_tax(entry.ubp_id)
                if analysis:
                    patterns[level].append(analysis)
        
        return dict(patterns)


# ==============================================================================
# MAIN BRAIN CLASS
# ==============================================================================

class UBPBrainV3:
    """Main brain orchestrator"""
    
    def __init__(self):
        self.kb = UBPKnowledgeBase()
        self.hierarchy = None
        self.tax_analyzer = None
    
    def load(self, kb_file: str):
        """Load knowledge base"""
        self.kb.load_from_json(kb_file)
        self.hierarchy = HierarchyEngine(self.kb)
        self.tax_analyzer = TAXAnalyzer(self.kb, self.hierarchy)
        print(f"[Brain v3] Ready!")
    
    def analyze_object(self, ubp_id: str) -> Dict[str, Any]:
        """Complete analysis of an object"""
        entry = self.kb.get(ubp_id)
        if not entry:
            return {'error': f'{ubp_id} not found'}
        
        # Decompose to primitives
        primitives = self.hierarchy.decompose_to_primitives(ubp_id)
        
        # Get parents (what contains this)
        parents = self.kb.get_parents(ubp_id)
        
        # TAX analysis
        tax_analysis = self.tax_analyzer.analyze_composition_tax(ubp_id)
        
        return {
            'ubp_id': ubp_id,
            'level': entry.classify_level(),
            'is_primitive': entry.is_primitive(),
            'math': entry.math,
            'hierarchy': entry.hierarchy,
            'vector': entry.vector,
            'weight': entry.weight,
            'nrci': entry.nrci_float,
            'tax': entry.tax_float,
            'primitive_composition': primitives,
            'used_in': [p.ubp_id for p in parents[:10]],
            'tax_analysis': tax_analysis
        }


# ==============================================================================
# INITIALIZATION
# ==============================================================================

if __name__ == '__main__':
    brain = UBPBrainV3()
    brain.load('ubp_system_kb.json')
    
    print("\n" + "="*80)
    print("UBP BRAIN v3 - Interactive Mode")
    print("="*80)
    print("\nTry: brain.analyze_object('ELEM_H_001')")
    print("     brain.analyze_object('PARTICLE_PROTON_001')")
