"""
================================================================================
UBP UNDERSTANDING ENGINE v4.2 (Fix: Stats Calculation)
================================================================================
The UBP Understanding Engine sits above the Brain and provides:

  1. HIERARCHY AUDIT    — Verify internal consistency of KB entries.
  2. NRCI LANDSCAPE     — Survey the information-complexity landscape.
  3. PRIMITIVE BUILD-UP — Show how complex objects emerge from primitives.
  4. SCALING EXPERIMENT — Measure how recall quality improves as KB grows.
  5. CROSS-DOMAIN MAP   — Find informationally equivalent objects across domains.
  6. LLM-STYLE CHAT     — Natural language Q&A using the dual-layer brain.

Author: Euan R A Craig, New Zealand
Date: 01 March 2026
Version: 4.2 (Fixed get_stats error)
================================================================================
"""

import os
import sys
import json
import re
from fractions import Fraction
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# ── Standardized Imports ──────────────────────────────────────────────────────
try:
    from ubp_brain_consolidated import (
        UBPBrain, 
        extract_name, 
        extract_description, 
        extract_vector, 
        extract_nrci, 
        extract_tax, 
        is_belief
    )
    print("[Understanding Engine] Successfully linked to UBP Brain v4.0")
except ImportError as e:
    print(f"[CRITICAL] Could not import UBP Brain: {e}")
    sys.exit(1)

# ==============================================================================
# SECTION 1: INITIALIZATION
# ==============================================================================

def _find_kb_path() -> Optional[str]:
    """Locate the Knowledge Base file."""
    candidates = [
        'ubp_system_kb_cleanup.json', # Prioritize the cleaned file if it exists
        'ubp_system_kb.json',
        'system_kb/ubp_system_kb.json',
    ]
    for p in candidates:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None

def init_brain() -> UBPBrain:
    """Initialize the Brain with the found KB."""
    brain = UBPBrain()
    kb_path = _find_kb_path()
    if not kb_path:
        print("[ERROR] ubp_system_kb.json not found in standard paths.")
        return brain
        
    print(f"[Understanding Engine] Loading KB from: {kb_path}")
    brain.initialize([kb_path])
    return brain

def calculate_brain_stats(brain: UBPBrain) -> Dict:
    """Manually calculate statistics since UBPBrain lacks get_stats()."""
    kb = brain.kb_manager.kb
    stats = {
        'total_entries': len(kb),
        'lexicon_terms': brain.kb_manager.stats.get('lexicon_terms', 0),
        'entries_with_vectors': 0,
        'understanding_entries': 0,
        'belief_entries': 0
    }
    
    for entry in kb.values():
        if extract_vector(entry):
            stats['entries_with_vectors'] += 1
        
        if is_belief(entry):
            stats['belief_entries'] += 1
        else:
            stats['understanding_entries'] += 1
            
    return stats

# ==============================================================================
# SECTION 2: HIERARCHY AUDIT
# ==============================================================================

def run_hierarchy_audit(brain: UBPBrain) -> Dict:
    print("\n" + "=" * 70)
    print("HIERARCHY AUDIT")
    print("=" * 70)

    if not brain.initialized:
        print("Brain not initialized.")
        return {}

    kb = brain.kb_manager.kb
    hier = brain.hierarchy

    results = {"pass": 0, "anomaly": 0, "no_vector": 0, "total": 0}
    anomalies = []

    # Filter for Understanding entries (not Beliefs)
    entries = [(uid, e) for uid, e in kb.items() if not is_belief(e)]
    print(f"Auditing {len(entries)} understanding entries...")

    for uid, entry in entries:
        results["total"] += 1
        vec = extract_vector(entry)
        if vec is None:
            results["no_vector"] += 1
            continue

        nrci = float(extract_nrci(entry))
        level = hier.get_hierarchy_level(uid)
        prims = hier.decompose_to_primitives(uid)
        prim_count = sum(prims.values())

        # Anomaly Detection Rules
        if level == 0 and nrci < 0.7:
            anomalies.append((uid, extract_name(entry), level, nrci,
                               "L0 primitive has low NRCI"))
            results["anomaly"] += 1
        elif level > 0 and nrci > 0.99 and prim_count > 10:
            anomalies.append((uid, extract_name(entry), level, nrci,
                               "High NRCI for complex composite"))
            results["anomaly"] += 1
        else:
            results["pass"] += 1

    print(f"  Pass:      {results['pass']}")
    print(f"  Anomaly:   {results['anomaly']}")
    print(f"  No vector: {results['no_vector']}")

    if anomalies:
        print(f"\nTop anomalies:")
        for uid, name, level, nrci, reason in anomalies[:8]:
            print(f"  [{reason}] {name} (L{level}, NRCI={nrci:.4f})")

    return results

# ==============================================================================
# SECTION 3: NRCI LANDSCAPE
# ==============================================================================

def run_nrci_landscape(brain: UBPBrain) -> Dict:
    print("\n" + "=" * 70)
    print("NRCI LANDSCAPE SURVEY")
    print("=" * 70)

    if not brain.initialized: return {}

    kb = brain.kb_manager.kb
    hier = brain.hierarchy

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
            level = hier.get_hierarchy_level(uid)
            by_level[level].append(nrci)
        by_category[category].append(nrci)

    print("\nNRCI by Hierarchy Level (Understanding layer):")
    print(f"  {'Level':<18} {'Count':>6} {'Mean NRCI':>12} {'Min':>8} {'Max':>8}")
    print("  " + "-" * 56)
    level_names = {
        0: "L0 Primitive", 1: "L1 Nucleon", 2: "L2 Element",
        3: "L3 Molecule", 4: "L4 Structure"
    }
    stats = {}
    for level in sorted(by_level.keys()):
        vals = by_level[level]
        if vals:
            mean_v = sum(vals) / len(vals)
            stats[level] = {'mean': mean_v, 'min': min(vals),
                             'max': max(vals), 'count': len(vals)}
            label = level_names.get(level, f"L{level}")
            print(f"  {label:<18} {len(vals):>6}   {mean_v:>10.6f}   "
                  f"{min(vals):>6.4f}   {max(vals):>6.4f}")

    if beliefs_nrci:
        mean_b = sum(beliefs_nrci) / len(beliefs_nrci)
        print(f"  {'Beliefs (LAW)':<18} {len(beliefs_nrci):>6}   {mean_b:>10.6f}   "
              f"{min(beliefs_nrci):>6.4f}   {max(beliefs_nrci):>6.4f}")

    print("\nNRCI by Category (top 10 by count):")
    print(f"  {'Category':<16} {'Count':>6} {'Mean NRCI':>12}")
    print("  " + "-" * 38)
    sorted_cats = sorted(by_category.items(), key=lambda x: -len(x[1]))[:10]
    for cat, vals in sorted_cats:
        mean_v = sum(vals) / len(vals)
        print(f"  {cat:<16} {len(vals):>6}   {mean_v:>10.6f}")

    return stats

# ==============================================================================
# SECTION 4: PRIMITIVE BUILD-UP
# ==============================================================================

def run_primitive_buildup(brain: UBPBrain, target_id: str) -> None:
    if not brain.initialized: return

    kb = brain.kb_manager.kb
    hier = brain.hierarchy

    entry = kb.get(target_id)
    if not entry:
        # Try finding by short name if ID fails
        found = False
        for uid, e in kb.items():
            if target_id.lower() in uid.lower():
                target_id = uid
                entry = e
                found = True
                break
        if not found:
            print(f"Entry '{target_id}' not found")
            return

    name = extract_name(entry)
    level = hier.get_hierarchy_level(target_id)
    prims = hier.decompose_to_primitives(target_id)

    print(f"\n{'='*60}")
    print(f"  BUILD-UP: {name} ({target_id})")
    print(f"{'='*60}")
    print(f"  Hierarchy level: {level}")
    print(f"  Total primitive count: {sum(prims.values())}")

    if len(prims) == 1 and target_id in prims:
        print("  Status: ABSOLUTE PRIMITIVE -- no further decomposition")
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
        lv = hier.get_hierarchy_level(uid)
        prefix = "  " + "  " * indent
        print(f"{prefix}[L{lv}] {n}  (NRCI={nrci:.4f})")

        math_str = e.get('math', '') if e else ''
        atlas = e.get('atlas', {}) if e else {}
        hier_str = atlas.get('hierarchy', '') if isinstance(atlas, dict) else ''
        components = hier.parse_components(math_str)
        if not components:
            components = hier.parse_components(hier_str)

        for comp_id, count in sorted(components.items(), key=lambda x: -x[1]):
            ce = kb.get(comp_id, {})
            cn = extract_name(ce) if ce else comp_id
            clv = hier.get_hierarchy_level(comp_id)
            cprefix = "  " + "  " * (indent + 1)
            print(f"{cprefix}{count}x [L{clv}] {cn}")
            if clv > 0 and indent < 3:
                show_level(comp_id, indent + 2, _visited)

    print("\n  Composition chain:")
    show_level(target_id)

    print("\n  Absolute primitive summary:")
    for prim_id, count in sorted(prims.items(), key=lambda x: -x[1]):
        pe = kb.get(prim_id, {})
        pn = extract_name(pe) if pe else prim_id
        print(f"    {count:5d}x {pn}")

    nrci = float(extract_nrci(entry))
    tax = float(extract_tax(entry))
    print(f"\n  NRCI: {nrci:.6f}  |  TAX: {tax:.4f}")

# ==============================================================================
# SECTION 5: SCALING EXPERIMENT
# ==============================================================================

def run_scaling_experiment(brain: UBPBrain) -> Dict:
    print("\n" + "=" * 70)
    print("SCALING EXPERIMENT -- Intelligence vs KB Size")
    print("=" * 70)
    
    if not brain.initialized: return {}

    BENCHMARK = [
        ("What is an electron?", "PARTICLE_ELECTRON"),
        ("What is a proton?", "PARTICLE_PROTON"),
        ("What is hydrogen?", "ELEM_H"),
        ("What is carbon?", "ELEM_C"),
        ("What is water?", "MOLECULE_H2O"),
        ("What is glucose?", "MOLECULE_C6H12O6"),
        ("What is ATP?", "TOOL_ATP"),
        ("What is the Higgs boson?", "PARTICLE_HIGGS"),
        ("What is ammonia?", "MOLECULE_NH3"),
        ("What is methane?", "MOLECULE_CH4"),
    ]

    kb = brain.kb_manager.kb

    covered = sum(1 for _, prefix in BENCHMARK
                  if any(uid.startswith(prefix) for uid in kb.keys()))
    print(f"\nBenchmark coverage: {covered}/{len(BENCHMARK)} ({covered/len(BENCHMARK)*100:.0f}%)")

    r1_hits = 0
    print(f"\n{'Query':<42} {'Expected':<25} {'Got':<25} R@1")
    print("-" * 100)
    for query, expected_prefix in BENCHMARK:
        candidates = brain.recall(query, top_k=5)
        top1_id = candidates[0]['ubp_id'] if candidates else "NONE"
        r1 = top1_id.startswith(expected_prefix)
        if r1: r1_hits += 1
        mark = "OK" if r1 else "XX"
        print(f"{query:<42} {expected_prefix:<25} {top1_id:<25} {mark}")

    n = len(BENCHMARK)
    print(f"\nResults: R@1={r1_hits/n*100:.1f}% (KB size: {len(kb)})")
    return {'kb_size': len(kb), 'r1': r1_hits/n}

# ==============================================================================
# SECTION 6: CROSS-DOMAIN MAP
# ==============================================================================

def run_cross_domain_map(brain: UBPBrain, min_similarity: float = 0.4) -> None:
    print("\n" + "=" * 70)
    print("CROSS-DOMAIN PRIMITIVE SIMILARITY MAP")
    print("=" * 70)
    
    if not brain.initialized: return

    kb = brain.kb_manager.kb
    hier = brain.hierarchy

    entries_with_prims = []
    for uid, entry in kb.items():
        if is_belief(entry): continue
        prims = hier.decompose_to_primitives(uid)
        if len(prims) > 1 or (len(prims) == 1 and uid not in prims):
            entries_with_prims.append((uid, entry, prims))

    print(f"Computing cross-domain similarities for {len(entries_with_prims)} entries...")

    cross_domain_pairs = []
    for i, (uid1, e1, prims1) in enumerate(entries_with_prims):
        cat1 = uid1.split('_')[0]
        for j, (uid2, e2, prims2) in enumerate(entries_with_prims):
            if j <= i: continue
            cat2 = uid2.split('_')[0]
            if cat1 == cat2: continue

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
    print("  " + "-" * 96)
    seen = set()
    shown = 0
    for sim, uid1, n1, cat1, uid2, n2, cat2, shared in cross_domain_pairs:
        pair_key = tuple(sorted([uid1, uid2]))
        if pair_key in seen: continue
        seen.add(pair_key)
        print(f"  {sim:>5.1%}  {n1:<32} {cat1:<10} {n2:<32} {cat2}")
        shown += 1
        if shown >= 20: break

# ==============================================================================
# SECTION 7: LLM-STYLE CHAT
# ==============================================================================

def run_chat_session(brain: UBPBrain, queries: List[str] = None) -> None:
    print("\n" + "=" * 70)
    print("LLM-STYLE CHAT SESSION")
    print("=" * 70)
    
    if not brain.initialized: return

    if queries is None:
        queries = [
            "What is a proton?",
            "Tell me about water",
            "What is iron?",
            "Explain glucose",
            "What is ATP?",
        ]

    for query in queries:
        print(f"\n{'-'*60}")
        print(f"Q: {query}")
        print(f"{'-'*60}")
        result = brain.process_query(query)
        print(result.response)
        if result.warnings:
            for w in result.warnings:
                print(f"  [!] {w}")

# ==============================================================================
# SECTION 8: MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("UBP UNDERSTANDING ENGINE v4.2")
    print("Dual-Layer Knowledge System: Understanding + Beliefs")
    print("=" * 70)

    brain = init_brain()
    
    if not brain.initialized:
        print("System initialization failed. Check KB file.")
        return

    # FIX: Calculate stats manually instead of calling brain.get_stats()
    stats = calculate_brain_stats(brain)
    
    print(f"\nKB Status:")
    print(f"  Total entries:         {stats['total_entries']}")
    print(f"  With vectors:          {stats['entries_with_vectors']}")
    print(f"  Understanding (det.):  {stats['understanding_entries']}")
    print(f"  Beliefs (LAW):         {stats['belief_entries']}")
    print(f"  Lexicon terms:         {stats['lexicon_terms']}")

    run_nrci_landscape(brain)
    run_hierarchy_audit(brain)

    # Try to build up some common molecules if they exist
    targets = ["MOLECULE_H2O_001", "MOLECULE_C6H12O6_001", "TOOL_ATP_001"]
    for target in targets:
        run_primitive_buildup(brain, target)

    run_cross_domain_map(brain, min_similarity=0.4)
    run_scaling_experiment(brain)
    run_chat_session(brain)

    print("\n" + "=" * 70)
    print("UBP UNDERSTANDING ENGINE v4.2 -- COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
