# ══════════════════════════════════════════════════════════════════════════════
# §00  CONFIGURATION & PATHS (HARDENED v3.7.6 + KB migration v4.0)
# ══════════════════════════════════════════════════════════════════════════════
# MIGRATION 2026-07-09:
#   The legacy `ubp_system_kb.json` and `ubp_lang_kb_combined_v4.json` have
#   been REPLACED by the four new system_kb files:
#       system_kb/elements.json
#       system_kb/language_words.json
#       system_kb/math.json
#       system_kb/physics_law.json
#   `system_kb/legacy_adapter.py` provides a drop-in v9.9 view of those four
#   files. Consumers that import `KB_SYSTEM_PATH` / `KB_LANG_PATH` from here
#   now transparently get the merged view.
# ══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import sys, os, json, math
from pathlib import Path

# 1. STATIC PATH ANCHORING
# We use the current working directory as the root to avoid resolve() hangs
ROOT_DIR = Path(os.getcwd())

# 2. DYNAMIC PATH CONFIGURATION
# Check environment variable, or try to locate the KB files
core_env = os.environ.get('UBP_CORE_PATH')
if core_env:
    UBP_CORE_PATH = Path(core_env)
elif os.path.exists("/app/applet/glm_test_dir/ubp_system_kb.json"):
    UBP_CORE_PATH = Path("/app/applet/glm_test_dir")
else:
    UBP_CORE_PATH = ROOT_DIR

# 3. SYSTEM PATH INTEGRATION
# Add paths to sys.path only if they aren't already there
def _update_sys_path(target_path: Path):
    path_str = str(target_path.absolute())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

_update_sys_path(ROOT_DIR)
if UBP_CORE_PATH != ROOT_DIR:
    _update_sys_path(UBP_CORE_PATH)

# 3b. KB migration — locate the four new system_kb files
# Resolution order for SYSTEM_KB_DIR:
#   (a) $UBP_SYSTEM_KB_DIR env var
#   (b) <UBP_CORE_PATH>/system_kb/
#   (c) <ROOT_DIR>/system_kb/ or <ROOT_DIR>/core_studio_v4.0/system_kb/
#   (d) Walk upward from this file's location looking for system_kb/
def _resolve_system_kb_dir() -> Path:
    env = os.environ.get('UBP_SYSTEM_KB_DIR')
    if env and Path(env).is_dir():
        return Path(env)
    candidates = [
        UBP_CORE_PATH / 'system_kb',
        ROOT_DIR / 'system_kb',
        ROOT_DIR / 'core_studio_v4.0' / 'system_kb',
    ]
    for c in candidates:
        if (c / 'elements.json').exists():
            return c
    # Walk upward from this file
    here = Path(__file__).resolve().parent
    for _ in range(6):
        if (here / 'system_kb').is_dir() and (here / 'system_kb' / 'elements.json').exists():
            return here / 'system_kb'
        if (here / 'core_studio_v4.0' / 'system_kb').is_dir():
            return here / 'core_studio_v4.0' / 'system_kb'
        here = here.parent
    return UBP_CORE_PATH / 'system_kb'  # last resort; will report missing in status()

SYSTEM_KB_DIR = _resolve_system_kb_dir()
_update_sys_path(SYSTEM_KB_DIR.parent)  # so `from system_kb.legacy_adapter import ...` works
_update_sys_path(SYSTEM_KB_DIR)         # so `import legacy_adapter` works

# 4. KB LOCATOR (Absolute referencing)
# KB_SYSTEM_PATH now points at the merged v9.9 file produced by the adapter.
# KB_LANG_PATH is the SAME merged file — `language_words.json` is one of the
# four new KBs, so the lang KB has been absorbed into the system KB.
# Consumers that call `json.load(open(KB_SYSTEM_PATH))` will get the v9.9 view.
# Consumers that import `_load_system_kb` / `_load_kb_safe` from GLM01_substrate
# will transparently use the adapter (see GLM01_substrate patch).
try:
    # Prefer the in-memory adapter; materialise to disk lazily for consumers
    # that bypass the loader (GLM23_grammar_vectors, GLM27_crg_expander).
    try:
        import legacy_adapter as _la
        KB_SYSTEM_PATH = _la.ensure_legacy_kb_on_disk()
        KB_LANG_PATH = KB_SYSTEM_PATH  # lang KB absorbed into system KB
        _ADAPTER_AVAILABLE = True
    except Exception as _e:
        # Adapter import failed — fall back to the legacy file path.
        KB_SYSTEM_PATH = SYSTEM_KB_DIR / "ubp_system_kb_v4_merged.json"
        KB_LANG_PATH = KB_SYSTEM_PATH
        _ADAPTER_AVAILABLE = False
        _ADAPTER_ERROR = str(_e)
except Exception:
    KB_SYSTEM_PATH = SYSTEM_KB_DIR / "ubp_system_kb_v4_merged.json"
    KB_LANG_PATH = KB_SYSTEM_PATH
    _ADAPTER_AVAILABLE = False

# 4b. Also expose the four canonical new-schema paths (for new code that
# wants to read them directly without going through the v9.9 view).
NEW_KB_PATHS = [
    SYSTEM_KB_DIR / "elements.json",
    SYSTEM_KB_DIR / "language_words.json",
    SYSTEM_KB_DIR / "math.json",
    SYSTEM_KB_DIR / "physics_law.json",
]

# 5. DIAGNOSTIC STATUS
def status():
    """Report module status without side effects."""
    s = {
        "module": "glm_config",
        "root_dir": str(ROOT_DIR),
        "core_path": str(UBP_CORE_PATH),
        "system_kb_dir": str(SYSTEM_KB_DIR),
        "kb_system_path": str(KB_SYSTEM_PATH),
        "kb_lang_path": str(KB_LANG_PATH),
        "kb_system_exists": KB_SYSTEM_PATH.exists(),
        "kb_lang_exists": KB_LANG_PATH.exists(),
        "adapter_available": _ADAPTER_AVAILABLE,
        "new_kb_paths": [str(p) for p in NEW_KB_PATHS],
        "new_kb_exists": {p.name: p.exists() for p in NEW_KB_PATHS},
        "cwd": os.getcwd(),
    }
    if not _ADAPTER_AVAILABLE:
        s["adapter_error"] = globals().get("_ADAPTER_ERROR", "unknown")
    return s

if __name__ == "__main__":
    print("=== GLM Config Module (Hardened + KB v4.0 migration) ===")
    stat = status()
    for k, v in stat.items():
        print(f"  {k}: {v}")
    
    if not stat["kb_system_exists"]:
        print(f"!! CRITICAL: System KB not found at {KB_SYSTEM_PATH}")
    if not all(stat["new_kb_exists"].values()):
        print(f"!! CRITICAL: One or more new KB files missing in {SYSTEM_KB_DIR}")