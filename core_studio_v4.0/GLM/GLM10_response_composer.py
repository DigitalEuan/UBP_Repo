# ══════════════════════════════════════════════════════════════════════════════
# §10  RESPONSE COMPOSER — THE VOICE (v3.7.6 Hardened)
# ══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import re
from typing import List, Dict, Optional, Tuple, Any

# IMPORT SUBSTRATE & CONSTANTS
from GLM01_substrate import LEECH_ENGINE, _load_kb_safe
from GLM02_constants import _OP_SYNTAX_RE, PRONOUNS
from GLM00_config import KB_SYSTEM_PATH

# ── 1. INTERNAL HELPERS ────────────────────────────────────────────────
def _kb_description(word: str, vocab: Any, kb: Dict[str, Any]) -> Tuple[str, float, float]:
    """Look up the KB description + metrics for a vocab word."""
    target_dict = vocab.words if hasattr(vocab, 'words') else vocab
    entry = target_dict.get(word)
    if not entry: return ("", 0.0, 0.0)
    
    vec = entry.vector
    nrci = float(entry.nrci)
    try: 
        tax = float(LEECH_ENGINE.calculate_symmetry_tax(vec))
    except: 
        tax = 0.0
        
    desc = ""
    # Hardening fix: ensure vector comparison is list-to-list
    vec_list = list(vec)
    for uid, kbe in kb.items():
        if list(kbe.get("vector", [])) == vec_list:
            name = kbe.get("name", uid)
            d = kbe.get("lexicon", "")
            m = re.match(r"([^.]{12,}\.)", d)
            desc = f"{name}: {m.group(1).strip()}" if m else f"{name}: {d[:90]}"
            break
    return (desc, nrci, tax)

def _verbalise_edge(e: Any) -> str:
    """Turns a CRG edge into a natural language string."""
    src = e.src if hasattr(e, 'src') else e.get('src', 'unknown')
    label = e.label if hasattr(e, 'label') else e.get('label', 'relates_to')
    dst = e.dst if hasattr(e, 'dst') else e.get('dst', 'unknown')
    
    label_text = label.replace("_", " ")
    m = {
        "is_a": f"{src} is a {dst}",
        "is_dual_to": f"{src} is dual to {dst}",
        "commutes_with": f"{src} commutes with {dst}",
        "generates": f"{src} generates {dst}",
        "scales_as": f"{src} scales as {dst}",
        "depends_on": f"{src} depends on {dst}",
        "measures": f"{src} measures {dst}",
        "auto_proposed": f"{src} relates to {dst}"
    }
    return m.get(label, f"{src} {label_text} {dst}")

# ── 2. MASTER COMPOSER ─────────────────────────────────────────────────
def compose_response(
    query: str, 
    content: List[Tuple[str, Any]], 
    unknown: List[str], 
    zone: Any, 
    manager: Any, 
    vocab: Any, 
    qtype: str,
    compute_result: Optional[Dict] = None, 
    symbolic_result: Optional[Dict] = None, 
    warm_start: Optional[Any] = None,
    deliberation: Optional[Dict] = None # <--- ADDED
) -> str:
    """Weaves internal state into a coherent multi-layered response."""
    
    kb = _load_kb_safe(KB_SYSTEM_PATH)
    parts: List[str] = []

    if manager is not None and hasattr(manager, 'zones') and len(manager.zones) > 1:
        parts.append(f"[Zones: {len(manager.zones)} | Active: {manager.active_idx}]")

    if zone is not None and hasattr(zone, 'evidence') and zone.evidence:
        parts.append(zone.status_line())

    if warm_start is not None:
        parts.append(f"[Warm-Start] Resembles prior idea: '{warm_start.thesis}'")

    if zone is not None and getattr(zone, 'crystallized', False) and zone.thesis:
        parts.append(f"[I get it] {zone.thesis}")

    if compute_result:
        res = compute_result["result"]
        parts.append(f"[Computed] {compute_result['computation']['expr']} = {res['exact']}")

    if symbolic_result:
        res = symbolic_result["result"]
        parts.append(f"[Symbolic] {symbolic_result['computation']['kind']}: {res['exact']}")

    # NEW: Deliberation Block
    if deliberation:
        parts.append(format_deliberation(deliberation))

    topic_word = getattr(zone, 'last_topic_noun', None) if zone else None
    if not topic_word and content:
        topic_word = content[0][0]
        
    if topic_word:
        desc, nrci, tax = _kb_description(topic_word, vocab, kb)
        if desc: parts.append(f"[KB] {desc}")
        parts.append(f"[Verify] NRCI={nrci:.3f} | Tax={tax:.2f}")

    if zone is not None and hasattr(zone, 'crg_backbone') and zone.crg_backbone:
        edges = [_verbalise_edge(e) for e in zone.crg_backbone[:2]]
        if edges: parts.append(f"[Backbone] {' | '.join(edges)}")

    real_gaps = [u for u in unknown if u.lower() not in {"hello", "hi", "help"}]
    if real_gaps:
        parts.append(f"[Gap] No verified vector for: {', '.join(real_gaps[:3])}")

    if not parts:
        parts.append("I am listening. Name a concept or provide a mathematical expression to begin.")

    return "  ".join(parts)

# ── 3. ISOLATION TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Testing Module 10: Response Composer ===")
    # Mock data for testing
    mock_vocab = {"entropy": type('obj', (), {'vector': [0]*24, 'nrci': 0.8})()}
    
    # Fix: lambda now accepts 'self' argument (_) to prevent TypeError
    mock_zone = type('obj', (), {
        'evidence': [True], 
        'status_line': lambda _: "[Zone: Testing]", 
        'crystallized': True, 
        'thesis': 'Entropy is increasing.',
        'last_topic_noun': 'entropy', 
        'crg_backbone': []
    })()
    
    resp = compose_response("test", [], [], mock_zone, None, mock_vocab, "general")
    print(f"✅ Sample Response:\n   {resp}")