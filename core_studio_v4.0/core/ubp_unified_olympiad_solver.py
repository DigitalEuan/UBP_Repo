import re
import json
import os
from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra
from glm_engine_v31 import create_semantic_engine
from ubp_critpt_sovereign_v3 import UBPSovereignSolver, parse_template, load_critpt
from glm_concept_relation_graph import build_default_crg

class TopologicalDiffusionProofGenerator:
    def __init__(self, vocab, crg):
        self.vocab = vocab
        self.crg = crg

    def evaluate_tax(self, vec_a, vec_b):
        euclid_a = [(1 - 2*x) for x in vec_a]
        euclid_b = [(1 - 2*x) for x in vec_b]
        flow = [a + b for a, b in zip(euclid_a, euclid_b)]
        collapsed = [1 if x < 0 else 0 for x in flow]
        snapped, _ = GOLAY_ENGINE.snap_to_codeword(collapsed)
        return float(LEECH_ENGINE.calculate_symmetry_tax(snapped))

    def denoise_step(self, current_word: str, target_word: str, block_id: int) -> str:
        v_curr = self.vocab[current_word].vector
        v_target = self.vocab[target_word].vector
        current_distance = BinaryLinearAlgebra.hamming_distance(v_curr, v_target)

        candidates = []
        for word, entry in self.vocab.items():
            if word == current_word:
                continue
            v_cand = entry.vector
            dist_to_target = BinaryLinearAlgebra.hamming_distance(v_cand, v_target)
            dist_from_curr = BinaryLinearAlgebra.hamming_distance(v_curr, v_cand)

            # Block 3: High Noise (d >= 12). Focuses on Macro-MOG alignment.
            if block_id == 3:
                if dist_from_curr >= 12 and dist_to_target < current_distance:
                    score = dist_to_target
                    candidates.append((word, score))

            # Block 2: Mid Noise (8 <= d < 12). Focuses on Semantic Graph (CRG) routing.
            elif block_id == 2:
                if dist_from_curr <= 8 and dist_to_target < current_distance:
                    has_relation = len(self.crg.relate(current_word, word)) > 0
                    score = dist_to_target - (4 if has_relation else 0)
                    candidates.append((word, score))

            # Block 1: Low Noise (d < 8). Focuses on Micro-Symmetry Tax minimization.
            elif block_id == 1:
                if dist_from_curr <= 4:
                    tax = self.evaluate_tax(v_curr, v_cand)
                    score = dist_to_target + tax
                    candidates.append((word, score))

        if not candidates:
            return current_word

        candidates.sort(key=lambda x: x[1])
        return candidates[0][0]

    def generate_sketch(self, start_word: str, target_word: str) -> str:
        if start_word not in self.vocab or target_word not in self.vocab:
            return f"❌ Concepts '{start_word}' or '{target_word}' not in phase-locked vocabulary."

        path = [start_word]
        current = start_word

        # Run the reverse diffusion process: Block 3 -> Block 2 -> Block 1
        for block_id in [3, 2, 1]:
            steps_in_block = 0
            while steps_in_block < 5:
                next_word = self.denoise_step(current, target_word, block_id)
                if next_word == current:
                    break

                path.append(next_word)
                current = next_word
                steps_in_block += 1

                if current == target_word:
                    break
            if current == target_word:
                break

        if current != target_word:
            return f"❌ Diffusion suspended: Could not fully denoise path between '{start_word}' and '{target_word}'."

        sketch = []
        for i, word in enumerate(path):
            entry = self.vocab[word]
            cat = entry.mog_category
            if i > 0:
                prev_vec = self.vocab[path[i-1]].vector
                tax = self.evaluate_tax(prev_vec, entry.vector)
                sketch.append(f"   ↓ [Topological Denoising Step | Tax: {tax:.2f}]")
            sketch.append(f"[{i+1}] {word.upper()} (Domain: {cat})")
        return "\n".join(sketch)

class UnifiedOlympiadSolver:
    def __init__(self):
        print("--- BOOTING UNIFIED OLYMPIAD SOLVER (DIFFUSION EDITION) ---")
        self.glm, _ = create_semantic_engine('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
        self.vocab = self.glm.vocab.words
        self.crg = build_default_crg()
        self.proof_gen = TopologicalDiffusionProofGenerator(self.vocab, self.crg)
        self.sovereign = UBPSovereignSolver()
        print(f"✅ Loaded {len(self.vocab)} phase-locked concepts.")

    def solve(self, record):
        print(f"\n{'='*80}\n[PROBLEM] {record.problem_id}\n{'='*80}")

        # 1. Extract Concepts using GLM Lexer
        tokens = self.glm.lexer.tokenise(record.problem_description)

        # Filter out generic operators/prepositions for the abductive proof anchors
        filtered_tokens = [
            t for t in tokens 
            if t in self.vocab and self.vocab[t].role not in ("OPERATOR", "PROPERTY") and len(t) > 2
        ]

        # 2. Generate Proof Sketch (Topological Diffusion)
        proof_sketch = "Insufficient domain-specific concepts for geodesic proof."
        if len(filtered_tokens) >= 2:
            start_word = filtered_tokens[0]
            target_word = filtered_tokens[-1]
            print(f"[ABDUCTIVE REASONING] Denoising path from '{start_word}' to '{target_word}'...")
            proof_sketch = self.proof_gen.generate_sketch(start_word, target_word)

        # 3. Solve Numerical Kernel
        print("[NUMERICAL KERNEL] Dispatching to PhysicsALU / NativeDynamicSolver...")
        spec = parse_template(record.code_template)

        # Check if the problem is purely symbolic (no numbers in description)
        has_numbers = len([n for n in re.findall(r"\b(\d+)\b", record.problem_description)]) > 0

        if not has_numbers and self.sovereign.native:
            # Symbolic fallback: Let SymPy Oracle handle the algebraic symbols
            print("   [Symbolic Fallback] No numbers detected. Routing to SymPy Oracle...")
            oracle_ans, _ = self.sovereign.solver._try_physics_alu(record.problem_description, spec) if hasattr(self.sovereign, 'solver') else (None, None)
            if oracle_ans:
                cand = oracle_ans
            else:
                # Fallback to symbolic defaults
                from ubp_v28_oracle import SymPyOracle
                oracle = SymPyOracle()
                ans, mode = oracle.solve(record.problem_description)
                if ans:
                    cand = self.sovereign._wrap_alu(str(ans), "SymPyOracle", spec)
                else:
                    cand = self.sovereign._typed_default(spec)
        else:
            cand = self.sovereign.solve(record.problem_description, spec)

        print("\n--- ABDUCTIVE PROOF SKETCH ---")
        print(proof_sketch)
        print("\n--- EXACT NUMERICAL KERNEL ---")
        print(f"Method: {cand.method}")
        print(f"Confidence (NRCI): {cand.confidence}")
        print(f"Values: {cand.values}")

        return {
            "id": record.problem_id,
            "proof_sketch": proof_sketch,
            "kernel_method": cand.method,
            "kernel_values": cand.values,
            "confidence": str(cand.confidence)
        }

if __name__ == '__main__':
    solver = UnifiedOlympiadSolver()
    records = load_critpt('critpt.json')[:5]

    results = []
    for rec in records:
        results.append(solver.solve(rec))

    with open('olympiad_unified_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n✅ Unified Olympiad results saved to 'olympiad_unified_results.json'.")
