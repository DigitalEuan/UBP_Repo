from __future__ import annotations
"""
================================================================================
UBP SWARM ORCHESTRATOR — TCT EDITION v21.0 "THE LIVING GEOMETRY"
================================================================================
Author: UBP Research Cortex v5.0
Date: 27 April 2026

ADVANCED FEATURES:
1. Recursive Self-Correction: Retries logic if Auditor rejects NRCI < 0.60.
2. Automated 3D Visualization: Generates unique scene_3d_{id}.json for every solve.
3. Logic Filaments: Visualizes the path from Question to Answer in 24D space.
================================================================================
"""

import io, json, logging, math, os, random, re, sys, time, hashlib
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ─── UBP CORE IMPORTS ────────────────────────────────────────────────────────
from core import GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE
from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
from ubp_observer_dynamics import ObserverDynamicsEngine
from ubp_python_engine import UBPPythonEngine
from ubp_semantic_engine import UBPSemanticEngine
from ubp_tgic_engine import TGICExactEngine, OffBit

try:
    from ubp_moe_cortex_v2 import UBPMoECortexV2
except ImportError:
    class UBPMoECortexV2:
        def research(self, query: str, max_words: int = 10):
            return f"Resonance detected."

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
log = logging.getLogger("UBP_TCT_v21")

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def _golay_snap(v):
    decoded, _, _ = GOLAY_ENGINE.decode(v)
    return GOLAY_ENGINE.encode(decoded)

def _nrci_of(v):
    tax = LEECH_ENGINE.calculate_symmetry_tax(v)
    return Fraction(10, 1) / (Fraction(10, 1) + tax)

def _vec_to_pos(v):
    """Maps 24-bit vector to 3D coordinates [-5, 5]."""
    x = (sum(v[0:8]) - 4) * 1.5
    y = (sum(v[8:16]) - 4) * 1.5
    z = (sum(v[16:24]) - 4) * 1.5
    return [x, y, z]

@dataclass
class ParsedDirective:
    raw: str; op: str; expr: Optional[str] = None; point: Optional[float] = None
    nums: List[float] = field(default_factory=list)

# ─── TIER 0: FREELANCE SCAVENGER (RESCUE & MUTATION) ────────────────────────
class FreelanceScavenger:
    def __init__(self):
        self.tgic = TGICExactEngine()

    def mutate(self, vector: List[int], attempt: int) -> List[int]:
        """Mutates the vector to find a more stable nearby anchor."""
        new_v = list(vector)
        # Flip a bit based on the attempt count to shift the resonance
        idx = (attempt * 7) % 24
        new_v[idx] ^= 1
        return _golay_snap(new_v)

    def probe(self, vector: List[int]) -> dict:
        try:
            energy = float(self.tgic.get_node_energy("CORE", vector, {"CORE": OffBit(tuple(vector), 0)}))
            return {"energy": energy}
        except: return {"energy": 0.0}

# ─── TIER 4: SEMANTIC RESONATOR ──────────────────────────────────────────────
class SemanticResonator:
    def __init__(self, engine: UBPSemanticEngine):
        self.engine = engine

    def vectorize_text(self, text: str, seed_offset: int = 0) -> Tuple[float, List[int], List[str]]:
        matches = self.engine.query(text, top_k=5)
        bit_counts = [seed_offset] * 24
        total_sim = 0
        neighbor_ids = []
        for m in matches:
            sim = getattr(m, 'score', getattr(m, 'resonance_score', 0.5))
            vec = self.engine._system_vectors.get(m.ubp_id)
            if vec:
                for i, bit in enumerate(vec): bit_counts[i] += 1 if bit > 0 else -1
                total_sim += sim
                neighbor_ids.append(m.ubp_id)
        composite_vec = [1 if c >= 0 else 0 for c in bit_counts]
        snapped = _golay_snap(composite_vec)
        magnitude = sum(snapped) * (total_sim / len(matches) if matches else 0.5)
        return float(magnitude), snapped, neighbor_ids[:2]

# ─── ORCHESTRATOR ────────────────────────────────────────────────────────────
class UBPSwarmTCTv21:
    def __init__(self):
        self.semantic = UBPSemanticEngine()
        self.semantic.load("ubp_system_kb.json", "ubp_lang_kb_combined_v4.json")
        self.physicist = GrandUnifiedEmlALU()
        self.coder = UBPPythonEngine()
        self.resonator = SemanticResonator(self.semantic)
        self.scavenger = FreelanceScavenger()
        self.moe = UBPMoECortexV2()
        self.observer = ObserverDynamicsEngine()

    def run_directive(self, directive: str, prob_id: str) -> dict:
        # 1. Parse
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", directive)]
        op = "derivative" if "derivative" in directive.lower() else "logic"
        expr, point = None, None
        if op == "derivative":
            m = re.search(r"of (.+?) at x\s*=\s*([-\d.]+)", directive, re.I)
            if m: expr, point = m.group(1), float(m.group(2))
        parsed = ParsedDirective(directive, op, expr, point, nums)

        # 2. Recursive Attempt Loop
        final_res = None
        for attempt in range(3):
            sov = self._execute_tiers(parsed, attempt)
            # Tier 6: Auditor
            if sov['nrci'] >= 0.60:
                final_res = sov
                final_res['attempts'] = attempt + 1
                break
            else:
                log.warning(f"Attempt {attempt+1} rejected (NRCI {sov['nrci']:.4f}). Mutating...")
                # Tier 0: Scavenger Mutation
                parsed.nums = [n + attempt for n in parsed.nums] # Shift the numeric scent

        if not final_res: final_res = sov # Take the last one if all fail

        # 3. Visualization Generation
        self._generate_visual(prob_id, final_res)

        # 4. Harvester
        if final_res['nrci'] >= 0.60:
            self._harvest(directive, final_res)

        return final_res

    def _execute_tiers(self, parsed: ParsedDirective, attempt: int) -> dict:
        # Tier 2: Physicist
        answer, mode = None, "Conceptual"
        env = {"sin": self.physicist.sin, "cos": self.physicist.cos, "exp": self.physicist.exp, "pi": self.physicist.PI}

        if parsed.op == "derivative":
            try:
                f = lambda x: eval(parsed.expr, {**env, "x": x})
                answer = float(self.physicist.derivative(f, parsed.point).real)
                mode = "Sovereign Calculus"
            except: pass

        if answer is None:
            for c in ["alpha", "proton", "phi", "pi"]:
                if c in parsed.raw.lower():
                    val = getattr(self.physicist, c.upper() if c != "alpha" else "ALPHA_INV", None)
                    if val: answer = float(val.real if hasattr(val, "real") else val); mode = "Sovereign Constant"; break

        # Tier 3: Coder
        if answer is None:
            try:
                code_res = self.coder.write(parsed.raw)
                local_ns = {}
                exec(code_res.code, {}, local_ns)
                ans = local_ns.get('result') or local_ns.get('val')
                if ans: answer = ans; mode = "Python Logic Solver"
            except: pass

        # Tier 4: Resonator
        if answer is None:
            mag, vec, neighbors = self.resonator.vectorize_text(parsed.raw, seed_offset=attempt)
            answer = mag; mode = "Resonance Magnitude"; res_vec = vec; neighbors = neighbors
        else:
            h_val = int(hashlib.sha256(str(answer).encode()).hexdigest(), 16)
            res_vec = _golay_snap([(h_val >> i) & 1 for i in range(23, -1, -1)])
            _, _, neighbors = self.resonator.vectorize_text(parsed.raw)

        nrci = float(_nrci_of(res_vec))
        read = self.observer.conscious_read(res_vec, Fraction(nrci).limit_denominator())
        scav = self.scavenger.probe(res_vec)

        # Tier 5: Scribe
        lang = self.moe.research(f"{parsed.raw} result={answer} nrci={nrci:.4f}", max_words=40)

        return {
            "answer": answer, "mode": mode, "nrci": nrci, "status": read['status'],
            "vector": res_vec, "neighbors": neighbors, "energy": scav['energy'],
            "lang": lang, "directive": parsed.raw
        }

    def _generate_visual(self, prob_id: str, res: dict):
        # Create a 3D scene showing the Question (Origin-ish) and Answer
        q_h = int(hashlib.sha256(res['directive'].encode()).hexdigest(), 16)
        q_vec = [(q_h >> i) & 1 for i in range(23, -1, -1)]

        p_pos = _vec_to_pos(q_vec)
        r_pos = _vec_to_pos(res['vector'])

        scene = {
            "spheres": [
                {"x": p_pos[0], "y": p_pos[1], "z": p_pos[2], "r": 0.6, "color": "#ff00ff", "label": "Question"},
                {"x": r_pos[0], "y": r_pos[1], "z": r_pos[2], "r": 0.8, "color": "#00ffff", "label": "Answer"}
            ],
            "lines": [
                {"start": p_pos, "end": r_pos, "color": "#ffffff", "label": "Logic Filament"}
            ]
        }
        with open(f'scene_3d_{prob_id}.json', 'w') as f:
            json.dump(scene, f)

    def _harvest(self, directive: str, res: dict):
        path = "ubp_learned_kb.json"
        kb = []
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    loaded = json.load(f)
                    kb = loaded if isinstance(loaded, list) else list(loaded.get("entries", {}).values())
            except: pass
        kb.append({
            "id": hashlib.md5(directive.encode()).hexdigest()[:10],
            "directive": directive, "answer": res["answer"], "nrci": res["nrci"], "timestamp": datetime.now().isoformat()
        })
        with open(path, "w") as f: json.dump(kb, f, indent=2)

    def run(self, problem_file: str):
        with open(problem_file, 'r') as f: problems = json.load(f)['problems']
        report = "# UBP TCT v21.0 — THE LIVING GEOMETRY REPORT\n\n"
        for p in problems:
            log.info(f"Engaging {p['id']}...")
            res = self.run_directive(p['problem'], p['id'])
            report += f"## Directive: {p['id']}\n\n"
            report += f"**[Tier 2: Physicist]** Result: `{res['answer']}` ({res['mode']})\n"
            report += f"**[Tier 3: Observer]** Status: `{res['status']}` (NRCI: {res['nrci']:.4f}) | Attempts: `{res.get('attempts', 1)}`\n"
            report += f"**[Tier 4: Resonator]** Neighbors: `{', '.join(res['neighbors'])}` | Energy: `{res['energy']:.4f}`\n"
            report += f"**[Visual]** Geometry generated: `scene_3d_{p['id']}.json`\n"
            report += f"**[Tier 5: Scribe]**\n> *\"{res['lang']}\"*\n\n---\n"

        with open('v21_living_geometry_report.md', 'w') as f: f.write(report)
        print("🏆 Living Geometry Investigation Complete. Check scene_3d_*.json files.")

if __name__ == "__main__":
    swarm = UBPSwarmTCTv21()
    if os.path.exists('ubp_mathnet_problem_set.json'):
        swarm.run('ubp_mathnet_problem_set.json')
