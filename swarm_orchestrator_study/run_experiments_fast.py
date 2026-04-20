"""
================================================================================
UBP SWARM ORCHESTRATOR V3 — FAST BATCH EXPERIMENT RUNNER
================================================================================
Uses UBP_MOE_TRAINING_STEPS=200000 (real training, 10x faster) to allow
all 8 experiments to complete in a reasonable time.

The n-gram manifold is still built from the full 290k character corpus,
just with fewer random sampling steps. The resulting manifold is still
functional for scientific study of swarm scaling.
================================================================================
"""

import json
import os
import sys
import time
from pathlib import Path

# Set training steps BEFORE importing the MoE module
os.environ['UBP_MOE_TRAINING_STEPS'] = '200000'

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))

from ubp_swarm_orchestrator_v3 import UBPOrchestratorV3, run_experiments

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / 'results_v3'
RESULTS_DIR.mkdir(exist_ok=True)

# Load experiment configs
with open(BASE_DIR / 'experiments_v3.json', 'r', encoding='utf-8') as f:
    configs = json.load(f)

print(f"Loaded {len(configs)} experiment configurations.")
print(f"Training steps: {os.environ['UBP_MOE_TRAINING_STEPS']}")
print(f"Results will be saved to: {RESULTS_DIR}")

# Boot the orchestrator ONCE (shared cortex)
t_boot = time.time()
orch = UBPOrchestratorV3(seed=42)
print(f"Orchestrator booted in {time.time() - t_boot:.1f}s")

# Run all experiments
summary = run_experiments(orch, configs, results_dir=str(RESULTS_DIR))

# Save summary
summary_path = RESULTS_DIR / 'experiment_summary.json'
summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')

print("\n" + "=" * 80)
print("ALL EXPERIMENTS COMPLETE")
print("=" * 80)
print(f"\n{'Experiment':<42} {'Agents':>6} {'Paras':>6} {'Words':>6} {'NRCI':>8} {'Time':>8}")
print("-" * 80)
for s in summary:
    print(f"{s['name']:<42} {s['total_agents']:>6} {s['total_paragraphs']:>6} "
          f"{s['total_words']:>6} {s['final_macro_nrci']:>8.4f} {s['elapsed_seconds']:>7.1f}s")
print(f"\nSummary saved to: {summary_path}")
