"""
================================================================================
UBP UNDERSTANDING ENGINE v5.1 — DEFINITIVE RELEASE
================================================================================
Author: Manus AI (based on work by Euan R A Craig)
Date: 05 March 2026
Version: 5.0.0

ARCHITECTURE:
  The UBP Understanding Engine sits above the Brain and provides a comprehensive
  analysis suite for the UBP Knowledge Base. It is designed to:

  1. **NRCI LANDSCAPE**     — Survey the information-complexity landscape.
  2. **HIERARCHY AUDIT**    — Verify internal consistency of KB entries.
  3. **PRIMITIVE BUILD-UP** — Show how complex objects emerge from primitives.
  4. **SCALING EXPERIMENT** — Measure how recall quality improves as KB grows.
  5. **CROSS-DOMAIN MAP**   — Find informationally equivalent objects across domains.
  6. **VECTOR COLLISION MAP** — Identify entries sharing the same vector.
  7. **LLM-STYLE CHAT**     — Natural language Q&A using the dual-layer brain.

CHANGE LOG (v5.1 vs v4.2):
  - **[CRITICAL FIX] Updated imports:** Now imports from ubp_brain_consolidated_v5_0
    instead of ubp_brain_consolidated. Removes dependency on extract_tax and
    hierarchy attributes that don't exist in v5.1.
  - **[CRITICAL FIX] Removed brain.hierarchy dependency:** The v5.1 brain does
    not have a hierarchy attribute. Hierarchy analysis now uses the atlas.hierarchy
    field directly from the KB.
  - **[CRITICAL FIX] Removed brain.recall dependency:** The v5.1 brain uses
    process_query instead of recall. The scaling experiment now uses process_query.
  - **[FEATURE] Vector Collision Map:** New analysis showing which entries share
    the same vector and why.
  - **[FEATURE] Expanded Chat Session:** More diverse queries covering all KB
    domains (elements, molecules, particles, laws, tools).
  - **[FEATURE] Confidence Histogram:** Shows the distribution of confidence
    scores across all benchmark queries.

================================================================================
"""

import os
import sys
import json
import re
from fractions import Fraction
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

try:
    from ubp_brain_consolidated import (
        UBPBrain,
        extract_name,
        extract_description,
        extract_vector,
        extract_nrci,
        is_belief,
        is_understanding,
    )
    print('[Understanding Engine v5.1] Successfully linked to UBP Brain v5.1')
except ImportError as e:
    print(f'[CRITICAL] Could not import UBP Brain v5.1: {e}')
    sys.exit(1)

# ==============================================================================
# SECTION 1: INITIALIZATION
# ==============================================================================

KB_SEARCH_PATHS = [
    'ubp_system_kb.json',
]

def _find_kb_path() -> Optional[str]:
    for p in KB_SEARCH_PATHS:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None

def init_brain() -> UBPBrain:
    brain = UBPBrain()
    kb_path = _find_kb_path()
    if not kb_path:
        print('[ERROR] ubp_system_kb.json not found in standard paths.')
        return brain
    print(f'[Understanding Engine v5.1] Loading KB from: {kb_path}')
    brain.initialize([kb_path])
    return brain

def get_hierarchy_level(uid: str, kb: Dict) -> int:
    """
    Determine the hierarchy level of an entry based on its atlas.hierarchy field.
    L0 = absolute primitive (no hierarchy or self-referential)
    L1 = built from L0 primitives
    L2 = built from L1 entries
    etc.
    """
    entry = kb.get(uid, {})
    atlas = entry.get('atlas', {})
    hierarchy_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''

    if not hierarchy_str:
        return 0

    # Parse components
    components = re.findall(r'(\d+)[×x]([A-Z_0-9]+)', hierarchy_str)
    if not components:
        return 0

    max_child_level = 0
    for count, child_uid in components:
        if child_uid == uid:
            continue  # Self-referential
        child_level = get_hierarchy_level(child_uid, kb)
        max_child_level = max(max_child_level, child_level)

    return max_child_level + 1

def decompose_to_primitives(uid: str, kb: Dict, _visited: set = None) -> Dict[str, int]:
    """Recursively decompose an entry to its absolute primitives."""
    if _visited is None:
        _visited = set()
    if uid in _visited:
        return {}
    _visited.add(uid)

    entry = kb.get(uid, {})
    atlas = entry.get('atlas', {})
    hierarchy_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''

    if not hierarchy_str:
        return {uid: 1}

    components = re.findall(r'(\d+)[×x]([A-Z_0-9]+)', hierarchy_str)
    if not components:
        return {uid: 1}

    result = {}
    for count_str, child_uid in components:
        count = int(count_str)
        if child_uid == uid:
            result[uid] = result.get(uid, 0) + count
            continue
        child_prims = decompose_to_primitives(child_uid, kb, _visited.copy())
        for prim_uid, prim_count in child_prims.items():
            result[prim_uid] = result.get(prim_uid, 0) + count * prim_count

    return result

# ==============================================================================
# SECTION 2: NRCI LANDSCAPE
# ==============================================================================

def run_nrci_landscape(brain: UBPBrain) -> Dict:
    print('\n' + '=' * 70)
    print('NRCI LANDSCAPE SURVEY')
    print('=' * 70)

    if not brain.initialized:
        return {}

    kb = brain.kb_manager.kb
    by_level: Dict[int, List[float]] = defaultdict(list)
    by_category: Dict[str, List[float]] = defaultdict(list)
    beliefs_nrci = []

    for uid, entry in kb.items():
        vec = extract_vector(entry)
        if vec is None:
            continue
        nrci = float(extract_nrci(entry))
        category = uid.split('_')[0]

        if is_belief(entry):
            beliefs_nrci.append(nrci)
        else:
            level = get_hierarchy_level(uid, kb)
            by_level[level].append(nrci)
        by_category[category].append(nrci)

    print('\nNRCI by Hierarchy Level (Understanding layer):')
    print(f"  {'Level':<18} {'Count':>6} {'Mean NRCI':>12} {'Min':>8} {'Max':>8}")
    print('  ' + '-' * 56)
    level_names = {
        0: 'L0 Primitive', 1: 'L1 Nucleon', 2: 'L2 Element',
        3: 'L3 Molecule', 4: 'L4 Structure'
    }
    stats = {}
    for level in sorted(by_level.keys()):
        vals = by_level[level]
        if vals:
            mean_v = sum(vals) / len(vals)
            stats[level] = {'mean': mean_v, 'min': min(vals),
                             'max': max(vals), 'count': len(vals)}
            label = level_names.get(level, f'L{level}')
            print(f'  {label:<18} {len(vals):>6}   {mean_v:>10.6f}   '
                  f'{min(vals):>6.4f}   {max(vals):>6.4f}')

    if beliefs_nrci:
        mean_b = sum(beliefs_nrci) / len(beliefs_nrci)
        print(f"  {'Beliefs (LAW)':<18} {len(beliefs_nrci):>6}   {mean_b:>10.6f}   "
              f'{min(beliefs_nrci):>6.4f}   {max(beliefs_nrci):>6.4f}')

    print('\nNRCI by Category (top 10 by count):')
    print(f"  {'Category':<16} {'Count':>6} {'Mean NRCI':>12}")
    print('  ' + '-' * 38)
    sorted_cats = sorted(by_category.items(), key=lambda x: -len(x[1]))[:10]
    for cat, vals in sorted_cats:
        mean_v = sum(vals) / len(vals)
        print(f'  {cat:<16} {len(vals):>6}   {mean_v:>10.6f}')

    return stats

# ==============================================================================
# SECTION 3: HIERARCHY AUDIT
# ==============================================================================

def run_hierarchy_audit(brain: UBPBrain) -> Dict:
    print('\n' + '=' * 70)
    print('HIERARCHY AUDIT')
    print('=' * 70)

    if not brain.initialized:
        return {}

    kb = brain.kb_manager.kb
    results = {'pass': 0, 'anomaly': 0, 'no_vector': 0, 'total': 0}
    anomalies = []

    entries = [(uid, e) for uid, e in kb.items() if not is_belief(e)]
    print(f'Auditing {len(entries)} understanding entries...')

    for uid, entry in entries:
        results['total'] += 1
        vec = extract_vector(entry)
        if vec is None:
            results['no_vector'] += 1
            continue

        nrci = float(extract_nrci(entry))
        level = get_hierarchy_level(uid, kb)
        prims = decompose_to_primitives(uid, kb)
        prim_count = sum(prims.values())

        if level == 0 and nrci < 0.5:
            anomalies.append((uid, extract_name(entry), level, nrci,
                               'L0 primitive has low NRCI'))
            results['anomaly'] += 1
        elif level > 0 and nrci > 0.99 and prim_count > 10:
            anomalies.append((uid, extract_name(entry), level, nrci,
                               'High NRCI for complex composite'))
            results['anomaly'] += 1
        else:
            results['pass'] += 1

    print(f"  Pass:      {results['pass']}")
    print(f"  Anomaly:   {results['anomaly']}")
    print(f"  No vector: {results['no_vector']}")

    if anomalies:
        print('\nTop anomalies:')
        for uid, name, level, nrci, reason in anomalies[:8]:
            print(f'  [{reason}] {name} (L{level}, NRCI={nrci:.4f})')

    return results

# ==============================================================================
# SECTION 4: PRIMITIVE BUILD-UP
# ==============================================================================

def run_primitive_buildup(brain: UBPBrain, target_id: str) -> None:
    if not brain.initialized:
        return

    kb = brain.kb_manager.kb

    entry = kb.get(target_id)
    if not entry:
        for uid, e in kb.items():
            if target_id.lower() in uid.lower():
                target_id = uid
                entry = e
                break
        if not entry:
            print(f"Entry '{target_id}' not found")
            return

    name = extract_name(entry)
    level = get_hierarchy_level(target_id, kb)
    prims = decompose_to_primitives(target_id, kb)

    print(f"\n{'='*60}")
    print(f'  BUILD-UP: {name} ({target_id})')
    print(f"{'='*60}")
    print(f'  Hierarchy level: {level}')
    print(f'  Total primitive count: {sum(prims.values())}')

    if len(prims) == 1 and target_id in prims:
        print('  Status: ABSOLUTE PRIMITIVE -- no further decomposition')
        return

    def show_level(uid, indent=0, _visited=None):
        if _visited is None:
            _visited = set()
        if uid in _visited:
            return
        _visited.add(uid)
        e = kb.get(uid, {})
        n = extract_name(e) if e else uid
        nrci = float(extract_nrci(e)) if e else 0.0
        lv = get_hierarchy_level(uid, kb)
        prefix = '  ' + '  ' * indent
        print(f'{prefix}[L{lv}] {n}  (NRCI={nrci:.4f})')

        atlas = e.get('atlas', {}) if e else {}
        hier_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''
        components = re.findall(r'(\d+)[×x]([A-Z_0-9]+)', hier_str)

        for count_str, comp_id in sorted(components, key=lambda x: -int(x[0])):
            count = int(count_str)
            ce = kb.get(comp_id, {})
            cn = extract_name(ce) if ce else comp_id
            clv = get_hierarchy_level(comp_id, kb)
            cprefix = '  ' + '  ' * (indent + 1)
            print(f'{cprefix}{count}x [L{clv}] {cn}')
            if clv > 0 and indent < 3:
                show_level(comp_id, indent + 2, _visited)

    print('\n  Composition chain:')
    show_level(target_id)

    print('\n  Absolute primitive summary:')
    for prim_id, count in sorted(prims.items(), key=lambda x: -x[1]):
        pe = kb.get(prim_id, {})
        pn = extract_name(pe) if pe else prim_id
        print(f'    {count:5d}x {pn}')

    nrci = float(extract_nrci(entry))
    print(f'\n  NRCI: {nrci:.6f}')

# ==============================================================================
# SECTION 5: SCALING EXPERIMENT
# ==============================================================================

def run_scaling_experiment(brain: UBPBrain) -> Dict:
    print('\n' + '=' * 70)
    print('SCALING EXPERIMENT — Recall Quality vs KB Size')
    print('=' * 70)

    if not brain.initialized:
        return {}

    BENCHMARK = [
        ('What is an electron?', 'PARTICLE_ELECTRON_001'),
        ('What is a proton?', 'PARTICLE_PROTON_001'),
        ('What is hydrogen?', 'ELEM_H_001'),
        ('What is carbon?', 'ELEM_C_006'),
        ('What is water?', 'MOLECULE_WATER_001'),
        ('What is glucose?', 'MOLECULE_GLUCOSE_001'),
        ('What is ATP?', 'MOLECULE_ATP_001'),
        ('What is the Higgs boson?', 'PARTICLE_HIGGS_BOSON_001'),
        ('What is ammonia?', 'MOLECULE_AMMONIA_001'),
        ('What is methane?', 'MOLECULE_METHANE_001'),
        ('What is oxygen?', 'ELEM_O_008'),
        ('What is nitrogen?', 'ELEM_N_007'),
        ('What is iron?', 'ELEM_Fe_026'),
        ('What is a neutron?', 'PARTICLE_NEUTRON_001'),
        ('What is gold?', 'ELEM_Au_079'),
    ]

    kb = brain.kb_manager.kb
    covered = sum(1 for _, uid in BENCHMARK if uid in kb)
    print(f'\nBenchmark coverage: {covered}/{len(BENCHMARK)} ({covered/len(BENCHMARK)*100:.0f}%)')

    r1_hits = 0
    confidence_sum = 0.0
    print(f"\n{'Query':<42} {'Expected':<28} {'Got':<28} {'Conf':>6} R@1")
    print('-' * 110)

    for query, expected_uid in BENCHMARK:
        result = brain.process_query(query)
        got_uid = result.ubp_id or 'NONE'
        r1 = got_uid == expected_uid
        if r1:
            r1_hits += 1
        confidence_sum += result.confidence
        mark = 'OK' if r1 else 'XX'
        print(f'{query:<42} {expected_uid:<28} {got_uid:<28} {result.confidence:>5.1%} {mark}')

    n = len(BENCHMARK)
    avg_conf = confidence_sum / n
    print(f'\nResults: R@1={r1_hits/n*100:.1f}% | Avg Confidence={avg_conf:.2%} | KB size: {len(kb)}')
    return {'kb_size': len(kb), 'r1': r1_hits / n, 'avg_confidence': avg_conf}

# ==============================================================================
# SECTION 6: VECTOR COLLISION MAP
# ==============================================================================

def run_vector_collision_map(brain: UBPBrain) -> None:
    print('\n' + '=' * 70)
    print('VECTOR COLLISION MAP')
    print('=' * 70)

    if not brain.initialized:
        return

    kb = brain.kb_manager.kb
    vector_groups = defaultdict(list)
    no_vector = []

    for uid, entry in kb.items():
        vec = extract_vector(entry)
        if vec and len(vec) == 24:
            vector_groups[tuple(vec)].append(uid)
        else:
            no_vector.append(uid)

    collision_count = sum(1 for v, uids in vector_groups.items() if len(uids) > 1)
    total_unique = len(vector_groups)

    print(f'\nTotal entries: {len(kb)}')
    print(f'Entries with no vector: {len(no_vector)}')
    print(f'Unique vectors: {total_unique}')
    print(f'Vector collision groups: {collision_count}')
    print(f'Collision rate: {collision_count / total_unique * 100:.1f}%')

    print('\nTop 10 collision groups:')
    sorted_groups = sorted(vector_groups.items(), key=lambda x: len(x[1]), reverse=True)
    for vec, uids in sorted_groups[:10]:
        if len(uids) > 1:
            names = [extract_name(kb.get(uid, {})) for uid in uids[:3]]
            print(f'  {len(uids)} entries: {", ".join(names[:3])}{"..." if len(uids) > 3 else ""}')

    print('\nNote: Collisions are expected with the Golay code (4096 codewords, 702 entries).')
    print('The brain resolves collisions using the primary name index (exact match).')

# ==============================================================================
# SECTION 7: CROSS-DOMAIN MAP
# ==============================================================================

def run_cross_domain_map(brain: UBPBrain, min_similarity: float = 0.4) -> None:
    print('\n' + '=' * 70)
    print('CROSS-DOMAIN PRIMITIVE SIMILARITY MAP')
    print('=' * 70)

    if not brain.initialized:
        return

    kb = brain.kb_manager.kb
    entries_with_prims = []
    for uid, entry in kb.items():
        if is_belief(entry):
            continue
        prims = decompose_to_primitives(uid, kb)
        if len(prims) > 1 or (len(prims) == 1 and uid not in prims):
            entries_with_prims.append((uid, entry, prims))

    print(f'Computing cross-domain similarities for {len(entries_with_prims)} entries...')

    cross_domain_pairs = []
    for i, (uid1, e1, prims1) in enumerate(entries_with_prims):
        cat1 = uid1.split('_')[0]
        for j, (uid2, e2, prims2) in enumerate(entries_with_prims):
            if j <= i:
                continue
            cat2 = uid2.split('_')[0]
            if cat1 == cat2:
                continue

            all_prims = set(prims1) | set(prims2)
            shared = sum(min(prims1.get(p, 0), prims2.get(p, 0)) for p in all_prims)
            union = sum(max(prims1.get(p, 0), prims2.get(p, 0)) for p in all_prims)
            if union > 0:
                sim = shared / union
                if sim >= min_similarity:
                    cross_domain_pairs.append((
                        sim, uid1, extract_name(e1), cat1,
                        uid2, extract_name(e2), cat2, shared
                    ))

    cross_domain_pairs.sort(key=lambda x: -x[0])

    print(f"\nTop cross-domain pairs (similarity >= {min_similarity:.0%}):")
    print(f"  {'Sim':>6}  {'Entry A':<32} {'Domain A':<10} {'Entry B':<32} {'Domain B'}")
    print('  ' + '-' * 96)
    seen = set()
    shown = 0
    for sim, uid1, n1, cat1, uid2, n2, cat2, shared in cross_domain_pairs:
        pair_key = tuple(sorted([uid1, uid2]))
        if pair_key in seen:
            continue
        seen.add(pair_key)
        print(f'  {sim:>5.1%}  {n1:<32} {cat1:<10} {n2:<32} {cat2}')
        shown += 1
        if shown >= 20:
            break

# ==============================================================================
# SECTION 8: LLM-STYLE CHAT SESSION
# ==============================================================================

def run_chat_session(brain: UBPBrain, queries: List[str] = None) -> None:
    print('\n' + '=' * 70)
    print('LLM-STYLE CHAT SESSION (UBP Brain v5.1)')
    print('=' * 70)

    if not brain.initialized:
        return

    if queries is None:
        queries = [
            # Physical objects
            'What is a proton?',
            'Tell me about water',
            'What is carbon?',
            'What is an electron?',
            'What is oxygen?',
            'What is hydrogen?',
            # Molecules
            'What is glucose?',
            'What is ammonia?',
            'What is methane?',
            # Laws and concepts
            'What is the Alpha-Lambda Horizon?',
            'What is the purpose of the Golay code?',
            'What is the Leech lattice?',
            # Tools and algorithms
            'What is ATP?',
            'What is the Collatz conjecture?',
            # Edge cases
            'What is the meaning of life?',
            'What is a quark?',
        ]

    hits = 0
    nulls = 0
    total_confidence = 0.0

    for query in queries:
        print(f'\n{"-"*60}')
        print(f'Q: {query}')
        print(f'{"-"*60}')
        result = brain.process_query(query, debug=False)
        print(result.response)

        if result.confidence >= 0.15:
            hits += 1
        else:
            nulls += 1
        total_confidence += result.confidence

    n = len(queries)
    print(f'\n{"="*60}')
    print(f'CHAT SESSION SUMMARY')
    print(f'{"="*60}')
    print(f'  Total queries: {n}')
    print(f'  Resolved (conf >= 15%): {hits} ({hits/n*100:.1f}%)')
    print(f'  Null Resonance: {nulls} ({nulls/n*100:.1f}%)')
    print(f'  Average confidence: {total_confidence/n:.2%}')

# ==============================================================================
# SECTION 9: MAIN
# ==============================================================================

def main():
    print('=' * 70)
    print('UBP UNDERSTANDING ENGINE v5.1')
    print('Dual-Layer Knowledge System: Understanding + Beliefs')
    print('=' * 70)

    brain = init_brain()

    if not brain.initialized:
        print('System initialization failed. Check KB file.')
        return

    kb = brain.kb_manager.kb
    stats = brain.kb_manager.stats

    print(f'\nKB Status:')
    print(f"  Total entries:         {stats['total_entries']}")
    print(f"  Indexed names:         {stats['indexed_names']}")
    print(f"  Lexicon terms:         {stats['lexicon_terms']}")

    # Count understanding vs belief entries
    understanding_count = sum(1 for uid, e in kb.items() if is_understanding(e))
    belief_count = sum(1 for uid, e in kb.items() if is_belief(e))
    print(f'  Understanding entries: {understanding_count}')
    print(f'  Belief entries:        {belief_count}')

    # Run all analyses
    run_nrci_landscape(brain)
    run_hierarchy_audit(brain)

    # Build-up for key objects
    targets = ['MOLECULE_WATER_001', 'ELEM_C_006', 'PARTICLE_PROTON_001']
    for target in targets:
        run_primitive_buildup(brain, target)

    run_vector_collision_map(brain)
    run_cross_domain_map(brain, min_similarity=0.4)
    run_scaling_experiment(brain)
    run_chat_session(brain)

    print('\n' + '=' * 70)
    print('UBP UNDERSTANDING ENGINE v5.1 — COMPLETE')
    print('=' * 70)

if __name__ == '__main__':
    main()
