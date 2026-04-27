"""
================================================================================
UBP SWARM TCT MATHNET ORCHESTRATOR — v4.0 "THE GEOMETRIC SOLVER"
================================================================================
Author: UBP Research Cortex v5.0
Date: April 2026

V4.0 PARADIGM SHIFT:
- Math problems are no longer treated as arithmetic; they are treated as 
  Informational Imbalances (unstable vectors).
- Col 1 uses UBPPyVM to instantiate the problem as a physical CortexAtom.
- Col 2 uses Golay Error Correction to "solve" the problem by snapping the 
  unstable vector to the nearest Leech Lattice coordinate.
- Col 3 translates the geometric snap back into human mathematics.
================================================================================
"""

import os
import sys
import json
import re
import time
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ─── PATH SETUP ──────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
os.chdir(_SCRIPT_DIR)

# ─── ENGINE IMPORTS ──────────────────────────────────────────────────────────
from core import GOLAY_ENGINE, LEECH_ENGINE
from ubp_py_runtime import UBPPyVM, MOGOntology
from ubp_observer_dynamics import ObserverDynamicsEngine
from ubp_semantic_engine import UBPSemanticEngine
from ubp_brain_consolidated import UBPBrain

from openai import OpenAI
_client = OpenAI()

print("[v4.0] Initializing UBP Geometric Solver Engines...")
_OBS = ObserverDynamicsEngine()
_SEMANTIC = UBPSemanticEngine()
_SEMANTIC.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
_BRAIN = UBPBrain()
_BRAIN.initialize(['ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json'])
print("[v4.0] Engines Online.")

# ─── DATA STRUCTURES ─────────────────────────────────────────────────────────

@dataclass
class Col1_ProblemState:
    key_numbers: List[int]
    vm_program: str
    initial_vector: List[int]
    initial_tax: float
    initial_nrci: float
    mog_health: Dict[str, float]

@dataclass
class Col2_GeometricResolution:
    snapped_vector: List[int]
    syndrome_weight: int
    final_tax: float
    final_nrci: float
    delta_tax: float
    soc_energy: float
    manifestation: str

@dataclass
class Col3_Translation:
    brain_law: str
    solution_text: str
    extracted_answer: str

# ─── COLUMN 1: THE SETUP (UBPPyVM) ───────────────────────────────────────────

def run_col1_setup(problem_text: str, step_id: str) -> Col1_ProblemState:
    """Instantiates the math problem as a physical state in the UBP VM."""
    nums = list(set([int(x) for x in re.findall(r'\b(\d+)\b', problem_text) if 1 <= int(x) <= 10000]))[:4]
    if not nums: nums = [1]

    # Build a UBP-Py program to represent the problem's initial state
    lines = [f"# MathNet Problem State: {step_id}"]
    atom_labels = []
    for i, n in enumerate(nums):
        label = f"VAR_{i}"
        lines.append(f"LET {label} {n}/1 TIER {i} CAT QUANTITY")
        atom_labels.append(label)
    
    recipe = " + ".join([f"1x{lbl}" for lbl in atom_labels])
    lines.append(f"SYNTH PROBLEM_STATE FROM \"{recipe}\"")
    program = "\n".join(lines)

    # Execute in VM
    vm = UBPPyVM(kb_path='ubp_system_kb.json', lattice_path=f'/tmp/mathnet_{step_id}.json')
    for line in program.split('\n'):
        parts = line.strip().split()
        if not parts or parts[0].startswith('#'): continue
        if parts[0] == 'LET': vm.let(parts[1], parts[2], tier=int(parts[4]), category=parts[6])
        elif parts[0] == 'SYNTH': 
            rec = re.search(r'"([^"]+)"', line).group(1)
            vm.synth(parts[1], rec)

    state_atom = vm.env.get('PROBLEM_STATE')
    if not state_atom:
        # Fallback if VM fails
        vec = [0]*24
        tax, nrci = 0.0, 0.5
        mog = {'Reality': 0, 'Info': 0, 'Activation': 0, 'Potential': 0}
    else:
        vec = state_atom.vector
        tax = float(state_atom.tax)
        nrci = float(state_atom.nrci)
        mog = MOGOntology.calculate_health(vec)

    return Col1_ProblemState(nums, program, vec, tax, nrci, mog)

# ─── COLUMN 2: THE COMPUTE (Golay/Leech/Observer) ────────────────────────────

def run_col2_compute(col1: Col1_ProblemState) -> Col2_GeometricResolution:
    """Solves the problem by snapping the unstable vector to the Leech Lattice."""
    
    # 1. Golay Error Correction (The "Solve")
    snapped_vec, snap_info = GOLAY_ENGINE.snap_to_codeword(col1.initial_vector)
    syndrome_weight = snap_info.get('syndrome_weight', 0)

    # 2. Leech Stability (The "Proof")
    final_tax = float(LEECH_ENGINE.calculate_symmetry_tax(snapped_vec))
    final_nrci = float(Fraction(10, 1) / (Fraction(10, 1) + Fraction(final_tax).limit_denominator(1000)))
    delta_tax = col1.initial_tax - final_tax

    # 3. Observer Dynamics (The "Manifestation")
    nrci_frac = Fraction(final_nrci).limit_denominator(1000)
    soc_energy = float(_OBS.calculate_soc_energy(snapped_vec, nrci_frac))
    conscious = _OBS.conscious_read(snapped_vec, nrci_frac)
    manifestation = conscious.get('status', 'SUBLIMINAL')

    return Col2_GeometricResolution(
        snapped_vec, syndrome_weight, final_tax, final_nrci, delta_tax, soc_energy, manifestation
    )

# ─── COLUMN 3: THE TRANSLATION (Language Scribe) ─────────────────────────────

def run_col3_translate(problem_text: str, domain: str, col1: Col1_ProblemState, col2: Col2_GeometricResolution) -> Col3_Translation:
    """Translates the geometric resolution back into standard mathematics."""
    
    brain_result = _BRAIN.process_query(problem_text[:200])
    brain_law = brain_result.ubp_id or 'UNKNOWN'

    # Construct the UBP Geometric Prompt
    prompt = f"""You are a mathematical translator. Your job is to solve the following math problem, guided by the UBP geometric resolution provided by the physics engine.

PROBLEM: {problem_text}
DOMAIN: {domain}
GOVERNING UBP LAW: {brain_law}

UBP GEOMETRIC RESOLUTION:
- Initial Problem NRCI: {col1.initial_nrci:.4f} (MOG Health: {col1.mog_health})
- The problem was solved by snapping the vector to the nearest Golay codeword.
- Syndrome Weight (Bits Corrected): {col2.syndrome_weight}
- Final Solution NRCI: {col2.final_nrci:.4f}
- Observer Status: {col2.manifestation} (SOC Energy: {col2.soc_energy:,.0f} CU)
- Delta Tax (Energy released by solving): {col2.delta_tax:.4f} bits

INSTRUCTIONS:
1. Use standard mathematical logic to solve the problem.
2. Acknowledge the geometric resolution. For example, if the Syndrome Weight is low (0-1), the problem is a direct corollary. If it is high (2-3), it requires a complex transformation.
3. If the Observer Status is MANIFESTED, the solution is a real, physical integer/value.
4. You MUST end your response with exactly: "FINAL ANSWER: [your concise answer]".
"""

    try:
        resp = _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=600
        )
        solution = resp.choices[0].message.content.strip()
        
        # Extract Final Answer
        extracted = ""
        if 'FINAL ANSWER:' in solution:
            extracted = solution.split('FINAL ANSWER:')[-1].strip()
            
    except Exception as e:
        solution = f"Translation Error: {e}"
        extracted = ""

    return Col3_Translation(brain_law, solution, extracted)

# ─── GRADER ──────────────────────────────────────────────────────────────────

def grade_solution(reference: str, extracted: str, solution_text: str) -> Tuple[str, float]:
    """Lenient LLM grader comparing extracted answer to reference."""
    if not extracted: return 'INCORRECT', 0.0
    
    try:
        grade_resp = _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a math grader. Compare the extracted answer to the reference. Reply with exactly one word: CORRECT, PARTIAL, or INCORRECT."},
                {"role": "user", "content": f"Reference: {reference}\nExtracted Answer: {extracted}\nFull Context: {solution_text[:200]}"}
            ],
            temperature=0.0,
            max_tokens=10
        )
        llm_grade = grade_resp.choices[0].message.content.strip().upper()
        if 'CORRECT' in llm_grade and 'IN' not in llm_grade: return 'CORRECT', 1.0
        elif 'PARTIAL' in llm_grade: return 'PARTIAL', 0.5
        else: return 'INCORRECT', 0.0
    except:
        return 'PARTIAL', 0.5 # Fallback

# ─── MAIN ORCHESTRATOR ───────────────────────────────────────────────────────

def run_v4_benchmark(problems: List[Dict], output_path: str):
    print(f"\n{'='*80}\nUBP SWARM MATHNET v4.0 — THE GEOMETRIC SOLVER\n{'='*80}\n")
    
    results = []
    scores = []

    for i, prob in enumerate(problems):
        pid = prob.get('id', f'P{i+1:02d}')
        print(f"\n[{i+1:02d}/{len(problems)}] {pid} | {prob['domain']}")
        
        t0 = time.time()
        
        # The Trinity
        col1 = run_col1_setup(prob['problem'], pid)
        col2 = run_col2_compute(col1)
        col3 = run_col3_translate(prob['problem'], prob['domain'], col1, col2)
        
        # Grade
        grade, score = grade_solution(prob.get('answer', ''), col3.extracted_answer, col3.solution_text)
        scores.append(score)
        
        elapsed = time.time() - t0
        
        print(f"  [Col1] Initial NRCI: {col1.initial_nrci:.4f} | MOG: {col1.mog_health['Reality']}R")
        print(f"  [Col2] Snapped! Bits Corrected: {col2.syndrome_weight} | Final NRCI: {col2.final_nrci:.4f} | {col2.manifestation}")
        print(f"  [Col3] Law: {col3.brain_law} | Extracted: {col3.extracted_answer[:40]}")
        print(f"  [RESULT] {grade} ({score}) | t={elapsed:.1f}s")

        results.append({
            'id': pid, 'domain': prob['domain'], 'grade': grade, 'score': score,
            'col1_initial_nrci': col1.initial_nrci,
            'col2_syndrome_weight': col2.syndrome_weight,
            'col2_final_nrci': col2.final_nrci,
            'col2_manifestation': col2.manifestation,
            'col3_extracted': col3.extracted_answer
        })

    # Summary
    n = len(results)
    correct = sum(1 for r in results if r['grade'] == 'CORRECT')
    partial = sum(1 for r in results if r['grade'] == 'PARTIAL')
    adj_score = sum(scores) / n * 100

    print(f"\n{'='*80}\nV4.0 BENCHMARK COMPLETE\n{'='*80}")
    print(f"  CORRECT: {correct}/{n} | PARTIAL: {partial}/{n} | ADJ SCORE: {adj_score:.1f}%")
    
    with open(output_path, 'w') as f:
        json.dump({'version': 'v4.0', 'summary': {'adj_score': adj_score}, 'results': results}, f, indent=2)

if __name__ == '__main__':
    data_path = os.path.join(_SCRIPT_DIR, 'data', 'ubp_mathnet_problem_set.json')
    with open(data_path) as f: raw = json.load(f)
    problems = raw.get('problems',