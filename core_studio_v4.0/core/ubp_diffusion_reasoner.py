import json
import math
from fractions import Fraction
from typing import List, Dict, Tuple, Optional
from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra
from glm_concept_relation_graph import build_default_crg

class TopologicalDiffusionReasoner:
    def __init__(self, strict_vocab_path='glm_strict_vocabulary.json'):
        print("--- INITIALIZING TOPOLOGICAL DIFFUSION REASONER ---")
        with open(strict_vocab_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.vocab = data["words"]
        self.crg = build_default_crg()
        print(f"Loaded {len(self.vocab)} phase-locked concepts.")

    def evaluate_tax(self, vec_a, vec_b):
        euclid_a = [(1 - 2*x) for x in vec_a]
        euclid_b = [(1 - 2*x) for x in vec_b]
        flow = [a + b for a, b in zip(euclid_a, euclid_b)]
        collapsed = [1 if x < 0 else 0 for x in flow]
        snapped, _ = GOLAY_ENGINE.snap_to_codeword(collapsed)
        return float(LEECH_ENGINE.calculate_symmetry_tax(snapped))

    def denoise_step(self, current_word: str, target_word: str, block_id: int) -> str:
        """
        Each block is responsible for a specific noise (Hamming distance) range.
        """
        v_curr = self.vocab[current_word]["vector"]
        v_target = self.vocab[target_word]["vector"]
        current_distance = BinaryLinearAlgebra.hamming_distance(v_curr, v_target)

        print(f"\n[Block {block_id}] Active. Current Distance (Noise \u03c3): {current_distance}")

        candidates = []
        for word, entry in self.vocab.items():
            if word == current_word:
                continue
            v_cand = entry["vector"]
            dist_to_target = BinaryLinearAlgebra.hamming_distance(v_cand, v_target)
            dist_from_curr = BinaryLinearAlgebra.hamming_distance(v_curr, v_cand)

            # Block 3: High Noise (d >= 16). Focuses on Macro-MOG alignment.
            if block_id == 3:
                # We want to make a massive jump that aligns the MOG category quadrant
                if dist_from_curr >= 12 and dist_to_target < current_distance:
                    # Score based on how well it matches the target's MOG category quadrant
                    score = dist_to_target
                    candidates.append((word, score))

            # Block 2: Mid Noise (8 <= d < 16). Focuses on Semantic Graph (CRG) routing.
            elif block_id == 2:
                if dist_from_curr <= 8 and dist_to_target < current_distance:
                    # Check if there is a semantic relation in the CRG
                    has_relation = len(self.crg.relate(current_word, word)) > 0
                    score = dist_to_target - (4 if has_relation else 0) # Semantic bias
                    candidates.append((word, score))

            # Block 1: Low Noise (d < 8). Focuses on Micro-Symmetry Tax minimization.
            elif block_id == 1:
                if dist_from_curr <= 4:
                    tax = self.evaluate_tax(v_curr, v_cand)
                    score = dist_to_target + tax # Minimize both distance and tax
                    candidates.append((word, score))

        if not candidates:
            print(f"   [Block {block_id}] No transition candidates found. Maintaining state.")
            return current_word

        # Deterministic selection: pick the candidate with the lowest score
        candidates.sort(key=lambda x: x[1])
        next_word = candidates[0][0]
        print(f"   [Block {block_id}] Denoised: '{current_word}' -> '{next_word}' (Score: {candidates[0][1]:.2f})")
        return next_word

    def resolve_path(self, start_word: str, target_word: str):
        print(f"\n================================================================================")
        print(f"TOPOLOGICAL DIFFUSION PATH: '{start_word}' -> '{target_word}'")
        print(f"================================================================================")
        
        path = [start_word]
        current = start_word

        # We run the reverse diffusion process: Block 3 -> Block 2 -> Block 1
        # This mirrors the EDM denoising schedule (Karras et al., 2022)
        for block_id in [3, 2, 1]:
            steps_in_block = 0
            while steps_in_block < 5: # Max 5 steps per block to prevent infinite loops
                next_word = self.denoise_step(current, target_word, block_id)
                if next_word == current:
                    break # Block has finished its denoising work
                
                path.append(next_word)
                current = next_word
                steps_in_block += 1
                
                # Check if we have reached the target
                if current == target_word:
                    break
            if current == target_word:
                break

        print(f"\n================================================================================")
        if current == target_word:
            print(f"✅ REVERSE DIFFUSION COMPLETE: Path resolved successfully!")
            print(f"Path: {' -> '.join(path).upper()}")
        else:
            print(f"❌ DIFFUSION SUSPENDED: Could not fully denoise the state.")
            print(f"Partial Path: {' -> '.join(path).upper()}")
        print(f"================================================================================")

if __name__ == "__main__":
    reasoner = TopologicalDiffusionReasoner()
    reasoner.resolve_path("electron", "photon")
    reasoner.resolve_path("weyl anomaly", "majorana")