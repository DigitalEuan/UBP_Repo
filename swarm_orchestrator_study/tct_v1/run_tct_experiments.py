"""
================================================================================
UBP TCT SWARM — FULL EXPERIMENT BATCH RUNNER
================================================================================
Runs 6 experiments across different topics and agent counts.
Each experiment uses the full UBP TCT v1.0 orchestrator with real engines.

Experiment Matrix:
  E1: Hydrogen bonding (5 steps, 26 agents) — chemistry baseline
  E2: Quantum entanglement (8 steps, 41 agents) — physics
  E3: DNA replication (8 steps, 41 agents) — biology
  E4: Leech Lattice geometry (10 steps, 51 agents) — pure mathematics
  E5: Neural network learning (10 steps, 51 agents) — computer science
  E6: Stellar nucleosynthesis (10 steps, 51 agents) — astrophysics
================================================================================
"""

import os
import sys
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from ubp_swarm_tct_v1 import UBPSwarmTCT

EXPERIMENTS = [
    {
        "id": "E1",
        "name": "tct_E1_hydrogen_bonding",
        "directive": "Hydrogen bonding in water molecules and its role in biological systems",
        "steps": 5,
        "retries": 3,
        "seed": 42,
        "description": "Chemistry baseline — small swarm"
    },
    {
        "id": "E2",
        "name": "tct_E2_quantum_entanglement",
        "directive": "Quantum entanglement and non-local correlations in particle physics",
        "steps": 8,
        "retries": 3,
        "seed": 43,
        "description": "Physics — medium swarm"
    },
    {
        "id": "E3",
        "name": "tct_E3_dna_replication",
        "directive": "DNA replication mechanisms and error correction in biological cells",
        "steps": 8,
        "retries": 3,
        "seed": 44,
        "description": "Biology — medium swarm"
    },
    {
        "id": "E4",
        "name": "tct_E4_leech_lattice",
        "directive": "The Leech Lattice as a 24-dimensional error-correcting geometric substrate",
        "steps": 10,
        "retries": 3,
        "seed": 45,
        "description": "Pure mathematics — large swarm"
    },
    {
        "id": "E5",
        "name": "tct_E5_neural_networks",
        "directive": "Gradient descent and backpropagation in deep neural network learning",
        "steps": 10,
        "retries": 3,
        "seed": 46,
        "description": "Computer science — large swarm"
    },
    {
        "id": "E6",
        "name": "tct_E6_stellar_nucleosynthesis",
        "directive": "Stellar nucleosynthesis and the formation of heavy elements in supernovae",
        "steps": 10,
        "retries": 3,
        "seed": 47,
        "description": "Astrophysics — large swarm"
    },
]

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "results_tct")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "tct_experiment_summary.json")

def run_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary = []
    total_start = time.time()
    
    for exp in EXPERIMENTS:
        print(f"\n{'='*70}")
        print(f"EXPERIMENT {exp['id']}: {exp['description']}")
        print(f"Directive: {exp['directive']}")
        print(f"Steps: {exp['steps']} | Retries: {exp['retries']}")
        print(f"{'='*70}")
        
        exp_start = time.time()
        
        try:
            orch = UBPSwarmTCT(
                directive=exp['directive'],
                num_steps=exp['steps'],
                max_retries=exp['retries'],
                seed=exp['seed'],
                verbose=True
            )
            
            doc = orch.run()
            json_path, md_path = orch.save(doc, OUTPUT_DIR, exp['name'])
            
            exp_elapsed = time.time() - exp_start
            
            # Agent count formula: 1 Director + N*(1 Math + 1 Python + 1 Scribe + 1 Auditor) + 1 Synthesizer
            # = 2 + N*4 (but retries add more agents)
            
            result = {
                "id": exp['id'],
                "name": exp['name'],
                "directive": exp['directive'],
                "description": exp['description'],
                "steps": exp['steps'],
                "total_agents": doc.total_agents,
                "total_words": doc.total_words,
                "macro_nrci": doc.macro_nrci,
                "avg_alignment": doc.avg_alignment,
                "elapsed_seconds": exp_elapsed,
                "json_path": json_path,
                "md_path": md_path,
                "status": "SUCCESS"
            }
            
            print(f"\n[{exp['id']}] COMPLETE: {doc.total_agents} agents, {doc.total_words} words, "
                  f"NRCI={doc.macro_nrci:.4f}, align={doc.avg_alignment:.4f}, t={exp_elapsed:.1f}s")
        
        except Exception as e:
            exp_elapsed = time.time() - exp_start
            result = {
                "id": exp['id'],
                "name": exp['name'],
                "directive": exp['directive'],
                "description": exp['description'],
                "steps": exp['steps'],
                "total_agents": 0,
                "total_words": 0,
                "macro_nrci": 0,
                "avg_alignment": 0,
                "elapsed_seconds": exp_elapsed,
                "status": "FAILED",
                "error": str(e)
            }
            print(f"\n[{exp['id']}] FAILED: {e}")
        
        summary.append(result)
        
        # Save intermediate summary after each experiment
        with open(SUMMARY_PATH, 'w') as f:
            json.dump(summary, f, indent=2)
    
    total_elapsed = time.time() - total_start
    
    print(f"\n{'='*70}")
    print(f"ALL EXPERIMENTS COMPLETE — Total time: {total_elapsed:.1f}s")
    print(f"{'='*70}")
    print(f"\n{'Exp':>4} {'Agents':>7} {'Words':>6} {'NRCI':>7} {'Align':>7} {'Time':>7} Status")
    print(f"{'─'*55}")
    for r in summary:
        print(f"{r['id']:>4} {r['total_agents']:>7} {r['total_words']:>6} "
              f"{r['macro_nrci']:>7.4f} {r['avg_alignment']:>7.4f} "
              f"{r['elapsed_seconds']:>6.1f}s {r['status']}")
    
    print(f"\nSummary saved to: {SUMMARY_PATH}")
    return summary

if __name__ == "__main__":
    run_all()
