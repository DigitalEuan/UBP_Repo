import json
import re
from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra
from glm_engine_v31 import create_semantic_engine
from ubp_critpt_sovereign_v3 import UBPSovereignSolver, parse_template, load_critpt
from glm_concept_relation_graph import build_default_crg

# Generic words that cause "Apophenia" (false shallow coherence)
BANNED_ANCHORS = {"order", "number", "value", "system", "result", "time", "part", "form", "case", "point"}

class HolosphericMindV2:
    def __init__(self):
        print("--- BOOTING HOLOSPHERIC MIND v2 (STRICT SEMANTICS) ---")
        self.glm, _ = create_semantic_engine('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
        self.vocab = self.glm.vocab.words
        self.crg = build_default_crg()
        self.sovereign = UBPSovereignSolver()
        print(f"✅ Hemispheres synchronized. {len(self.vocab)} concepts loaded.")

    def evaluate_tax(self, vec_a, vec_b):
        euclid_a = [(1 - 2*x) for x in vec_a]
        euclid_b = [(1 - 2*x) for x in vec_b]
        flow = [a + b for a, b in zip(euclid_a, euclid_b)]
        collapsed = [1 if x < 0 else 0 for x in flow]
        snapped, _ = GOLAY_ENGINE.snap_to_codeword(collapsed)
        return float(LEECH_ENGINE.calculate_symmetry_tax(snapped))

    def generate_thought_train(self, start_word, target_word):
        """Uses Topological Diffusion to generate the logical steps."""
        queue = [(start_word, [start_word])]
        visited = set([start_word])
        found_path = None
        
        while queue:
            current_word, current_path = queue.pop(0)
            if current_word == target_word:
                found_path = current_path
                break
            if len(current_path) > 4: continue
                
            v_curr = self.vocab[current_word].vector
            for next_word, entry in self.vocab.items():
                if next_word in visited: continue
                if BinaryLinearAlgebra.hamming_distance(v_curr, entry.vector) <= 8:
                    tax = self.evaluate_tax(v_curr, entry.vector)
                    if tax <= 3.15:
                        visited.add(next_word)
                        queue.append((next_word, current_path + [next_word]))

        if not found_path:
            return None

        sketch = []
        for i, word in enumerate(found_path):
            cat = self.vocab[word].mog_category
            if i > 0:
                prev_vec = self.vocab[found_path[i-1]].vector
                tax = self.evaluate_tax(prev_vec, self.vocab[word].vector)
                sketch.append(f"   ↓ [Logical Step | Tax: {tax:.2f}]")
            sketch.append(f"[{i+1}] {word.upper()} (Domain: {cat})")
        return "\n".join(sketch)

    def process_problem(self, record):
        print(f"\n{'='*80}\n[COGNITIVE EVENT] {record.problem_id}\n{'='*80}")
        
        # ---------------------------------------------------------
        # RIGHT HEMISPHERE (Semantic Topology)
        # ---------------------------------------------------------
        print("[RIGHT HEMISPHERE] Extracting strict physics topology...")
        tokens = self.glm.lexer.tokenise(record.problem_description)
        
        # STRICT FILTER: Must be in vocab, must not be an operator, must not be a banned generic word
        physics_tokens = [
            t for t in tokens 
            if t in self.vocab 
            and self.vocab[t].role not in ("OPERATOR", "PROPERTY") 
            and t not in BANNED_ANCHORS 
            and len(t) > 2
        ]
        
        if len(physics_tokens) < 2:
            print("❌ Insufficient physics concepts extracted.")
            return

        start_word = physics_tokens[0]
        target_word = physics_tokens[-1]
        
        print(f"  -> Physics Premise: '{start_word}'")
        print(f"  -> Physics Target:  '{target_word}'")
        
        print("\n[RIGHT HEMISPHERE] Generating Train of Thought...")
        thought_train = self.generate_thought_train(start_word, target_word)
        
        if thought_train:
            print(thought_train)
        else:
            print(f"  ❌ Topologically isolated. Cannot logically bridge '{start_word}' to '{target_word}'.")

        # ---------------------------------------------------------
        # LEFT HEMISPHERE (Logic / Exact Math ALU)
        # ---------------------------------------------------------
        print("\n[LEFT HEMISPHERE] Executing exact mathematical kernel...")
        spec = parse_template(record.code_template)
        
        # Route to SymPy if no numbers are present
        has_numbers = len([n for n in re.findall(r"\b(\d+)\b", record.problem_description)]) > 0
        if not has_numbers and self.sovereign.native:
            try:
                from ubp_v28_oracle import SymPyOracle
                oracle = SymPyOracle()
                ans, mode = oracle.solve(record.problem_description)
                cand = self.sovereign._wrap_alu(str(ans), "SymPyOracle", spec) if ans else self.sovereign._typed_default(spec)
            except:
                cand = self.sovereign._typed_default(spec)
        else:
            cand = self.sovereign.solve(record.problem_description, spec)

        print(f"  -> Mathematical Conclusion: {cand.values}")
        print(f"  -> Method: {cand.method}")

if __name__ == '__main__':
    mind = HolosphericMindV2()
    records = load_critpt('critpt.json')
    
    # Run Challenge 10 (Torsion/Palatini) and Challenge 11 (QFT Beta Function)
    for pid in ["Challenge_10_main", "Challenge_11_main"]:
        target_record = next((r for r in records if r.problem_id == pid), None)
        if target_record:
            mind.process_problem(target_record)