# Second UBP Core Studio Study: Element Chromatics

This package reruns and extends the uploaded Element Chromatics study using the **full** UBP repository.

## Upstream sources
- Repo: https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0
- README: https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/README.md
- Core usage: https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/core/ubp_files_and_usage.md
- System KB usage: https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/system_kb/ubp_files_and_usage.md
- Commit pinned in this package: `a024e223d6133fdac400a985c5ab6e8356dd3729`

## Contents
- `src/reproduce_study.py` — main reproducibility driver.
- `run_study.sh` — convenience wrapper that can clone the upstream repo if needed.
- `original_user_scripts/` — the 19 uploaded scripts preserved verbatim.
- `ubp_elemental_chromatic.png` — original uploaded visualization.
- `results/` — regenerated outputs, extension analyses, figures, and documentation.

## Quick start
```bash
bash run_study.sh /path/to/UBP_Repo
```
If no repo path is supplied, the script will clone the upstream repository next to this package and checkout commit `a024e223d6133fdac400a985c5ab6e8356dd3729`.

## Notes
- The rerun uses the **columnar** `ubp_system_kb.json` now shipped in the full UBP repo.
- A canonical 118-element table is rebuilt directly from the KB while excluding isotope-tagged entries.
- All original scripts are rerun in isolated directories so file outputs do not overwrite each other.
