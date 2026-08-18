# ARC-AGI v15 — Current Solver

**What it is:** The working ARC-AGI solver using the GLM mind + toolkit.  
**Score:** 9/50 (18%) on 50 training tasks.  
**Parent:** `../README.md`

---

## Role in the System

```
glm_machine/        ← provides mind (substrate_mind, reasoning_loop)
data_object/        ← provides encoding (arc_to_24bit)
GMHGL/              ← provides Golay engine
  ↓ all used by
arc_agi_15/ (this folder)
  └── writes results to → ../long_term_memory/glm_training_data.json
```

---

## Dependencies

| Needs From | What |
|-----------|------|
| `../glm_machine/substrate_mind.py` | Settlement dynamics |
| `../glm_machine/reasoning_loop.py` | Cognitive cycle |
| `../glm_machine/consolidated_mind.py` | All styles + toolkit |
| `../GMHGL/ubp_unified_v5.py` | Golay engine |
| `arc_loader/` | ARC task loader |
| `data/training/*.json` | 50 ARC tasks |

---

## Quick Start

```bash
# Run the consolidated mind (9/50)
python3 consolidated_mind.py

# Run the substrate mind
python3 substrate_mind.py

# Run the reasoning loop
python3 reasoning_loop.py
```

---

## Solved Tasks (9/50)

3 by mind (settlement dynamics + conditional reasoning), 6 by toolkit.

---

## Key Files

| File | Purpose |
|------|---------|
| `consolidated_mind.py` | Main solver (9/50) |
| `substrate_mind.py` | Settlement dynamics |
| `reasoning_loop.py` | Cognitive cycle |
| `semantic_layer.py` | Lingo vocabulary |
| `conditional_lobe.py` | Conditional reasoning |
| `arc_loader/` | ARC task loader |
| `data/training/` | 50 training tasks |
