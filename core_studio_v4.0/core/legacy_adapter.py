"""
UBP System KB — Legacy Adapter (v1.0)
=====================================

Drop-in compatibility shim that lets all existing UBP `core/` and `GLM/`
consumers read the four NEW system_kb files:

    system_kb/elements.json
    system_kb/language_words.json
    system_kb/math.json
    system_kb/physics_law.json

…without rewriting each consumer. The new files use the schema:

    {_meta, entries: [{ubp_id, lexicon, math, atlas:{hierarchy, vector,
    nrci, nrci_score, tax, weight, tilt}, tags, fingerprint, meta?, aliases?}]}

The legacy v9.9 columnar consumers (every file audited in
`_audit_reports/kb_usage_audit.md`) expect:

    {_fields, _params, _null_token,
     entries: {<fingerprint>: [ubp_id, lexicon, tags, vector,
                               nrci_str, nrci_val, tax_str, mog_tensor]}}

This module loads the four new files at first call, builds the merged v9.9
view in memory, caches it, and (optionally) materialises a synthetic
`ubp_system_kb_v4_merged.json` file on disk for the two consumers that
bypass the loader (`GLM23_grammar_vectors.py`, `GLM27_crg_expander.py`).

Public API
----------
- ``load_legacy_view()``           -> dict  (cached, in-memory v9.9 view)
- ``materialize_legacy_kb(disk_path)`` -> Path (writes a v9.9 .json to disk)
- ``LEGACY_KB_PATH``               -> Path  (default materialised-file path)
- ``NEW_KB_PATHS``                 -> list[Path]  (the four canonical KBs)
- ``status()``                     -> dict  (diagnostic info)

Author: KB migration agent  |  Date: 2026-07-09  |  License: UBP research
"""

from __future__ import annotations
import json
import hashlib
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# 1. PATH ANCHORING
# ─────────────────────────────────────────────────────────────────────────────
# Anchor to <repo>/core_studio_v4.0/system_kb/ regardless of CWD.
# Resolution order:
#   (a) $UBP_SYSTEM_KB_DIR env var (explicit override)
#   (b) <this file's parent>/  →  system_kb/legacy_adapter.py lives IN system_kb/
#   (c) ./system_kb/  (CWD fallback for legacy call sites)
#   (d) <repo>/core_studio_v4.0/system_kb/  via upward search
_THIS_DIR = Path(__file__).resolve().parent

def _resolve_system_kb_dir() -> Path:
    env = os.environ.get("UBP_SYSTEM_KB_DIR")
    if env and Path(env).is_dir():
        return Path(env)
    if (_THIS_DIR / "elements.json").exists():
        return _THIS_DIR
    cwd_candidate = Path(os.getcwd()) / "system_kb"
    if cwd_candidate.is_dir():
        return cwd_candidate
    # Walk upward looking for core_studio_v4.0/system_kb/
    p = _THIS_DIR
    for _ in range(6):
        if (p / "core_studio_v4.0" / "system_kb").is_dir():
            return p / "core_studio_v4.0" / "system_kb"
        p = p.parent
    return _THIS_DIR  # last resort; loaders will report missing files

SYSTEM_KB_DIR: Path = _resolve_system_kb_dir()

# The four canonical NEW-schema KB files (per user directive, 2026-07-09).
NEW_KB_PATHS: List[Path] = [
    SYSTEM_KB_DIR / "elements.json",
    SYSTEM_KB_DIR / "language_words.json",
    SYSTEM_KB_DIR / "math.json",
    SYSTEM_KB_DIR / "physics_law.json",
]

# Where to materialise the merged v9.9 view for consumers that bypass the
# loader (GLM23_grammar_vectors.py, GLM27_crg_expander.py, geometry.py, etc.).
LEGACY_KB_PATH: Path = SYSTEM_KB_DIR / "ubp_system_kb_v4_merged.json"

# Old path (now to be archived). Kept for backward-compat lookup only.
OLD_LEGACY_KB_PATH: Path = SYSTEM_KB_DIR / "ubp_system_kb.json"

# ─────────────────────────────────────────────────────────────────────────────
# 2. v9.9 SCHEMA CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
# Match the exact field order used by every legacy consumer (audit §0.1).
# Hardcoded positional indices in `_load_system_kb` rely on this order:
#   v[0]=ubp_id, v[1]=lexicon, v[2]=tags, v[3]=vector,
#   v[4]=nrci_str, v[5]=nrci_val, v[6]=tax_str, v[7]=mog_tensor
LEGACY_FIELDS: List[str] = [
    "ubp_id", "lexicon", "tags", "vector",
    "nrci_str", "nrci_val", "tax_str", "mog_tensor",
]

NULL_TOKEN: int = 0

# MOG_CATEGORIES — the canonical 24 categories from
# `core/archive_core/ubp_kb_architect.py` and `core/ubp_unified_v5.py`.
MOG_CATEGORIES: List[str] = [
    "M_Mass", "M_Charge", "M_Space", "M_Time", "M_Thermal", "M_Count",
    "I_Topology", "I_Symmetry", "I_Density", "I_Connectivity", "I_Dimension", "I_Complexity",
    "A_Energy", "A_Force", "A_Velocity", "A_Flux", "A_Resonance", "A_Spin",
    "P_Probability", "P_Ratio", "P_Limit", "P_Tax", "P_Coherence", "P_Phase",
]

# Direct key → MOG category mapping (from core/ubp_mog_mapper.py MAPPING).
_KEY_TO_MOG: Dict[str, str] = {
    "M": "M_Mass", "Mass": "M_Mass",
    "Z": "M_Count",
    "BP": "M_Thermal", "MP": "M_Thermal",
    "Rho": "I_Density", "Density": "I_Density",
    "Formula": "I_Connectivity",
    "Energy": "A_Energy",
    "c": "A_Velocity",
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. MOG CATEGORY RESOLUTION
# ─────────────────────────────────────────────────────────────────────────────
def _get_mog_cat(key: str) -> str:
    """Resolve a math-string key (e.g. 'MP', 'Lifetime', 'X') to a MOG category.
    Mirrors `core/ubp_mog_mapper.get_mog_cat` exactly so the reconstructed
    `mog_tensor` matches what `ubp_mog_mapper.run_ultra_migration` would
    have produced."""
    if key in _KEY_TO_MOG:
        return _KEY_TO_MOG[key]
    k = key.lower()
    if "time" in k or "period" in k:
        return "M_Time"
    if "charge" in k or "ion" in k:
        return "M_Charge"
    if "force" in k or "gravity" in k:
        return "A_Force"
    return "I_Complexity"


def _parse_math_string(math_str: str) -> Dict[str, str]:
    """Parse a UBP `math` DNA string of the form 'K1=V1|K2=V2|…' into a dict.
    Returns {} for empty/None input."""
    if not math_str or not isinstance(math_str, str):
        return {}
    out: Dict[str, str] = {}
    for chunk in math_str.split("|"):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk:
            continue
        k, v = chunk.split("=", 1)
        k = k.strip()
        if k:
            out[k] = v.strip()
    return out


def _build_master_params(all_math_strings: List[str]) -> Dict[str, List[str]]:
    """Build the `_params` map: {mog_category: sorted_list_of_param_keys}.
    Same logic as `ubp_mog_mapper.run_ultra_migration` lines 44-51."""
    param_map: Dict[str, set] = {cat: set() for cat in MOG_CATEGORIES}
    for m in all_math_strings:
        if not m or m == "0":
            continue
        for k in _parse_math_string(m).keys():
            param_map[_get_mog_cat(k)].add(k)
    return {cat: sorted(keys) for cat, keys in param_map.items()}


def _reconstruct_mog_tensor(math_str: str, master_params: Dict[str, List[str]]) -> Any:
    """Reconstruct the 24-row `mog_tensor` for a single entry from its `math`
    string. Each row is either `0` (no data for that category) or a list of
    values aligned to `master_params[cat]` (with `0` for missing keys).
    Mirrors `ubp_mog_mapper.run_ultra_migration` lines 73-86."""
    props = _parse_math_string(math_str)
    tensor: List[Any] = []
    for cat in MOG_CATEGORIES:
        cat_keys = master_params.get(cat, [])
        cat_values: List[Any] = []
        has_data = False
        for k in cat_keys:
            v = props.get(k)
            if v is not None:
                cat_values.append(v)
                has_data = True
            else:
                cat_values.append(0)
        tensor.append(cat_values if has_data else 0)
    return tensor


# ─────────────────────────────────────────────────────────────────────────────
# 4. ENTRY CONVERSION
# ─────────────────────────────────────────────────────────────────────────────
def _fingerprint_for(entry: Dict[str, Any]) -> str:
    """Return the SHA-256 fingerprint to use as the dict key for this entry.
    Prefers the entry's own `fingerprint` field (already SHA-256 of `math`
    per `ubp_kb_architect.create_entry`); falls back to computing SHA-256 of
    `math`, then SHA-256 of `ubp_id` as a last resort."""
    fp = entry.get("fingerprint")
    if isinstance(fp, str) and len(fp) == 64:
        return fp
    math_str = entry.get("math") or ""
    if math_str:
        return hashlib.sha256(math_str.encode("utf-8")).hexdigest()
    uid = entry.get("ubp_id") or "UNKNOWN"
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()


def _convert_entry(entry: Dict[str, Any], master_params: Dict[str, List[str]]) -> Tuple[str, List]:
    """Convert ONE new-schema entry to the v9.9 positional list shape.
    Returns (fingerprint, [ubp_id, lexicon, tags, vector, nrci_str, nrci_val,
    tax_str, mog_tensor])."""
    atlas = entry.get("atlas") or {}
    uid = entry.get("ubp_id") or "UNKNOWN"
    lex = entry.get("lexicon") or ""
    tags = entry.get("tags") or []
    if not isinstance(tags, list):
        tags = [tags] if tags else []
    vector = atlas.get("vector") or [0] * 24
    if not isinstance(vector, list) or len(vector) != 24:
        # Pad/truncate to 24 — UBP substrate requires 24-bit vectors.
        vector = (list(vector) + [0] * 24)[:24]
    nrci_str = atlas.get("nrci") or "0/1"
    nrci_val = atlas.get("nrci_score")
    if nrci_val is None:
        # Parse from nrci_str if possible
        try:
            num, den = nrci_str.split("/")
            nrci_val = float(num) / float(den) if float(den) != 0 else 0.0
        except Exception:
            nrci_val = 0.0
    nrci_val = float(nrci_val)
    tax_str = atlas.get("tax") or "0/1"
    math_str = entry.get("math") or ""
    mog_tensor = _reconstruct_mog_tensor(math_str, master_params)
    fp = _fingerprint_for(entry)
    positional = [uid, lex, tags, vector, nrci_str, nrci_val, tax_str, mog_tensor]
    return fp, positional


# ─────────────────────────────────────────────────────────────────────────────
# 5. LOADING + CACHING
# ─────────────────────────────────────────────────────────────────────────────
_cache_lock = threading.Lock()
_cached_view: Optional[Dict[str, Any]] = None
_cached_at: Optional[float] = None


def _load_one_new_kb(path: Path) -> List[Dict[str, Any]]:
    """Load one new-schema KB file. Returns the entries list (possibly empty).
    Tolerant of missing files (returns [])."""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        return data["entries"]
    if isinstance(data, list):  # already a bare list of entries
        return data
    return []


def _build_legacy_view() -> Dict[str, Any]:
    """Build the merged v9.9 dict from the four new KB files."""
    all_entries: List[Dict[str, Any]] = []
    sources: List[str] = []
    for p in NEW_KB_PATHS:
        entries = _load_one_new_kb(p)
        if entries:
            all_entries.extend(entries)
            sources.append(f"{p.name}({len(entries)})")

    # First pass: collect all math strings to build master _params
    all_math = [e.get("math", "") for e in all_entries]
    master_params = _build_master_params(all_math)

    # Second pass: convert each entry to v9.9 positional list
    legacy_entries: Dict[str, List] = {}
    seen_fingerprints: Dict[str, str] = {}  # fp -> ubp_id (for collision reporting)
    collisions = 0
    for e in all_entries:
        fp, positional = _convert_entry(e, master_params)
        if fp in legacy_entries:
            # Fingerprint collision — fall back to uid-hashed key
            collisions += 1
            uid = positional[0]
            fp = hashlib.sha256(f"{fp}:{uid}".encode("utf-8")).hexdigest()
        legacy_entries[fp] = positional
        seen_fingerprints[fp] = positional[0]

    view: Dict[str, Any] = {
        "_fields": list(LEGACY_FIELDS),
        "_params": master_params,
        "_null_token": NULL_TOKEN,
        "entries": legacy_entries,
        # Non-standard but harmless extras (consumers ignore unknown keys):
        "_meta": {
            "schema": "legacy_adapter_v1",
            "sources": sources,
            "entry_count": len(legacy_entries),
            "collisions_resolved": collisions,
            "generated_by": "system_kb/legacy_adapter.py",
        },
    }
    return view


def load_legacy_view(force_reload: bool = False) -> Dict[str, Any]:
    """Return the merged v9.9 view of the four new KB files.
    Cached on first call; subsequent calls return the cached dict unless
    `force_reload=True`."""
    global _cached_view, _cached_at
    with _cache_lock:
        if _cached_view is None or force_reload:
            _cached_view = _build_legacy_view()
            _cached_at = os.path.getmtime(NEW_KB_PATHS[0]) if NEW_KB_PATHS[0].exists() else 0.0
        return _cached_view


def materialize_legacy_kb(disk_path: Optional[Path] = None) -> Path:
    """Write the merged v9.9 view to disk as a minified JSON file.
    Default path is `LEGACY_KB_PATH`. Returns the path written.
    Idempotent: skips writing if the file already exists and is fresh
    (matching the cache)."""
    target = Path(disk_path) if disk_path else LEGACY_KB_PATH
    view = load_legacy_view()
    target.parent.mkdir(parents=True, exist_ok=True)
    # Minified JSON (matches `ubp_mog_mapper` output style)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(view, f, separators=(",", ":"), ensure_ascii=False)
    os.replace(tmp, target)
    return target


def ensure_legacy_kb_on_disk() -> Path:
    """Make sure a v9.9-shaped JSON file exists at `LEGACY_KB_PATH`.
    Used by the few consumers that bypass the loader. Cheap if the file
    is already up to date with the four source files."""
    target = LEGACY_KB_PATH
    # Re-materialise if any source is newer than the target, or target missing.
    needs_write = (not target.exists())
    if not needs_write:
        target_mtime = target.stat().st_mtime
        for src in NEW_KB_PATHS:
            if src.exists() and src.stat().st_mtime > target_mtime:
                needs_write = True
                break
    if needs_write:
        materialize_legacy_kb(target)
    return target


# ─────────────────────────────────────────────────────────────────────────────
# 6. DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────
def status() -> Dict[str, Any]:
    """Diagnostic snapshot. Safe to call at any time (does not load the KB)."""
    return {
        "module": "system_kb.legacy_adapter",
        "system_kb_dir": str(SYSTEM_KB_DIR),
        "new_kb_paths": [str(p) for p in NEW_KB_PATHS],
        "new_kb_exists": {p.name: p.exists() for p in NEW_KB_PATHS},
        "legacy_kb_path": str(LEGACY_KB_PATH),
        "legacy_kb_exists": LEGACY_KB_PATH.exists(),
        "old_legacy_kb_path": str(OLD_LEGACY_KB_PATH),
        "old_legacy_kb_exists": OLD_LEGACY_KB_PATH.exists(),
        "cached": _cached_view is not None,
        "cached_entry_count": (len(_cached_view["entries"]) if _cached_view else 0),
    }


def is_new_schema(data: Any) -> bool:
    """Predicate: does this loaded JSON dict use the NEW schema?
    Used by patched loaders to decide whether to invoke the adapter."""
    return (
        isinstance(data, dict)
        and "_meta" in data
        and isinstance(data.get("entries"), list)
    )


def is_legacy_schema(data: Any) -> bool:
    """Predicate: does this loaded JSON dict use the legacy v9.9 schema?"""
    return (
        isinstance(data, dict)
        and "_fields" in data
        and isinstance(data.get("entries"), dict)
    )


# ─────────────────────────────────────────────────────────────────────────────
# 7. CONVENIENCE: load_any(path) — single entry point for patched consumers
# ─────────────────────────────────────────────────────────────────────────────
def load_any(path: Optional[str] = None) -> Dict[str, Any]:
    """Load a KB file from `path` and return a v9.9-shaped dict regardless
    of whether the file uses the new schema or the legacy schema.
    If `path` is None, returns the merged view of all four new KBs.
    If `path` points to one of the four new KBs, returns just that one
    (converted to v9.9 shape)."""
    if path is None:
        return load_legacy_view()
    p = Path(path)
    if not p.exists():
        # Maybe it's a legacy path that no longer exists — return merged view
        return load_legacy_view()
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    if is_legacy_schema(data):
        return data
    if is_new_schema(data):
        # Convert this single file to v9.9 shape
        entries = data["entries"]
        all_math = [e.get("math", "") for e in entries]
        master_params = _build_master_params(all_math)
        legacy_entries: Dict[str, List] = {}
        for e in entries:
            fp, positional = _convert_entry(e, master_params)
            legacy_entries[fp] = positional
        return {
            "_fields": list(LEGACY_FIELDS),
            "_params": master_params,
            "_null_token": NULL_TOKEN,
            "entries": legacy_entries,
            "_meta": {
                "schema": "legacy_adapter_v1",
                "sources": [p.name],
                "entry_count": len(legacy_entries),
            },
        }
    # Unknown schema — return as-is and let caller decide
    return data


# ─────────────────────────────────────────────────────────────────────────────
# 8. CLI / SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    print("=== UBP System KB Legacy Adapter — self-test ===")
    s = status()
    for k, v in s.items():
        print(f"  {k}: {v}")
    print()
    if not all(s["new_kb_exists"].values()):
        print("!! One or more new KB files missing — cannot build view.")
        sys.exit(1)
    print("Loading merged v9.9 view…")
    view = load_legacy_view()
    print(f"  total entries: {len(view['entries'])}")
    print(f"  _fields: {view['_fields']}")
    print(f"  _params cats: {list(view['_params'].keys())}")
    print(f"  sources: {view['_meta']['sources']}")
    print(f"  collisions resolved: {view['_meta']['collisions_resolved']}")
    print()
    print("Materialising to disk…")
    written = materialize_legacy_kb()
    sz = written.stat().st_size
    print(f"  wrote: {written}  ({sz/1024:.1f} KB)")
    print()
    print("Self-test PASSED.")
