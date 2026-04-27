from __future__ import annotations
"""
================================================================================
UBP SWARM ORCHESTRATOR — TCT EDITION v22.0 "THE MANIFOLD MAP"
================================================================================
Author: UBP Research Cortex v5.0
Date: 27 April 2026

ADVANCED VISUALIZATION:
1. Resonance Cluster: Plots Answer, Question, and Semantic Neighbors.
2. Mesh Satellites: Visualizes 8-bit window densities as orbiting spheres.
3. Logic Web: Draws the semantic connections between the result and the KB.
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
log = logging.getLogger("UBP_TCT_v22")

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def _golay_snap(v):
    decoded, _, _ = GOLAY_ENGINE.decode(v)
    return GOLAY_ENGINE.encode(decoded)

def _nrci_of(v):
    tax = LEECH_ENGINE.calculate_symmetry_tax(v)
    return Fraction(10, 1) / (Fraction(10, 1) + tax)

def _vec_to_pos(v):
    """Maps 24-bit vector to 3D coordinates [-8, 8]."""
    x = (sum(v[0:8]) - 4) * 2.0
    y = (sum(v[8:16]) - 4) * 2.0
    z = (sum(v[16:24]) - 4) * 2.0
    return [x, y, z]

@dataclass
class ParsedDirective:
    raw: str; op: str; expr: Optional[str] = None; point: Optional[float] = None
    nums: List[float] = field(default_factory=list)

# ─── TIER 4: SEMANTIC RESONATOR (WITH VECTOR EXPORT) ────────────────────────
class SemanticResonator:
    def __init__(self, engine: UBPSemanticEngine):
        self.engine = engine

    def vectorize_text(self, text: str, seed_offset: int = 0) -> dict:
        matches = self.engine.query(text, top_k=5)
        bit_counts = [seed_offset] * 24
        total_sim = 0
        neighbors = []

        for m in matches:
            sim = getattr(m, 'score', getattr(m, 'resonance_score', 0.5))
            vec = self.engine._system_vectors.get(m.ubp_id)
            if vec:
                for i, bit in enumerate(vec): bit_counts[i] += 1 if bit > 0 else -1
                total_sim += sim
                neighbors.append({"id": m.ubp_id, "vector": [(b+1)//2 for b in vec], "sim": sim})

        composite_vec = [1 if c >= 0 else 0 for c in bit_counts]
        snapped = _golay_snap(composite_vec)
        magnitude = sum(snapped) * (total_sim / len(matches) if matches else 0.5)

        return {"magnitude": float(magnitude), "vector": snapped, "neighbors": neighbors[:3]}

# ─── ORCHESTRATOR ────────────────────────────────────────────────────────────
class UBPSwarmTCTv22:
    def __init__(self):
        self.semantic = UBPSemanticEngine()
        self.semantic.load("ubp_system_kb.json", "ubp_lang_kb_combined_v4.json")
        self.physicist = GrandUnifiedEmlALU()
        self.coder = UBPPythonEngine()
        self.resonator = SemanticResonator(self.semantic)
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

        # 2. Solve
        sov = self._execute_tiers(parsed)

        # 3. Visualization Generation (The Manifold Map)
        self._generate_manifold_map(prob_id, sov)

        return sov

    def _execute_tiers(self, parsed: ParsedDirective) -> dict:
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

        if answer is None:
            try:
                code_res = self.coder.write(parsed.raw)
                local_ns = {}
                exec(code_res.code, {}, local_ns)
                ans = local_ns.get('result') or local_ns.get('val')
                if ans: answer = ans; mode = "Python Logic Solver"
            except: pass

        # Semantic Context
        res_data = self.resonator.vectorize_text(parsed.raw)
        if answer is None:
            answer = res_data["magnitude"]
            mode = "Resonance Magnitude"
            res_vec = res_data["vector"]
        else:
            h_val = int(hashlib.sha256(str(answer).encode()).hexdigest(), 16)
            res_vec = _golay_snap([(h_val >> i) & 1 for i in range(23, -1, -1)])

        nrci = float(_nrci_of(res_vec))
        read = self.observer.conscious_read(res_vec, Fraction(nrci).limit_denominator())

        return {
            "answer": answer, "mode": mode, "nrci": nrci, "status": read['status'],
            "vector": res_vec, "neighbors": res_data["neighbors"], "directive": parsed.raw
        }

    def _generate_manifold_map(self, prob_id: str, res: dict):
        # 1. Question Position
        q_h = int(hashlib.sha256(res['directive'].encode()).hexdigest(), 16)
        q_vec = [(q_h >> i) & 1 for i in range(23, -1, -1)]
        q_pos = _vec_to_pos(q_vec)

        # 2. Answer Position
        r_pos = _vec_to_pos(res['vector'])

        spheres = [
            {"x": q_pos[0], "y": q_pos[1], "z": q_pos[2], "r": 0.6, "color": "#ff00ff", "label": "Question"},
            {"x": r_pos[0], "y": r_pos[1], "z": r_pos[2], "r": 1.0, "color": "#00ffff", "label": f"Answer: {res['mode']}"}
        ]
        lines = [{"start": q_pos, "end": r_pos, "color": "#ffffff", "label": "Logic Filament"}]

        # 3. Neighbor Positions (The Semantic Web)
        for n in res['neighbors']:
            n_pos = _vec_to_pos(n['vector'])
            spheres.append({"x": n_pos[0], "y": n_pos[1], "z": n_pos[2], "r": 0.4, "color": "#ffff00", "label": n['id']})
            lines.append({"start": r_pos, "end": n_pos, "color": "#ffff00", "label": "Resonance"})

        # 4. Mesh Satellites (8-bit Window Densities)
        windows = [sum(res['vector'][i:i+8]) for i in range(0, 24, 8)]
        offsets = [[2,0,0], [0,2,0], [0,0,2]]
        for i, w in enumerate(windows):
            s_pos = [r_pos[j] + offsets[i][j] for j in range(3)]
            spheres.append({"x": s_pos[0], "y": s_pos[1], "z": s_pos[2], "r": w * 0.1, "color": "#ffffff", "label": f"Window {i+1}"})

        scene = {"spheres": spheres, "lines": lines}
        with open(f'scene_3d_{prob_id}.json', 'w') as f:
            json.dump(scene, f)

    def run(self, problem_file: str):
        with open(problem_file, 'r') as f: problems = json.load(f)['problems']
        report = "# UBP TCT v22.0 — THE MANIFOLD MAP REPORT\n\n"
        for p in problems:
            log.info(f"Engaging {p['id']}...")
            res = self.run_directive(p['problem'], p['id'])
            report += f"## Directive: {p['id']}\n\n"
            report += f"**[Tier 2: Physicist]** Result: `{res['answer']}` ({res['mode']})\n"
            report += f"**[Tier 3: Observer]** Status: `{res['status']}` (NRCI: {res['nrci']:.4f})\n"
            report += f"**[Tier 4: Resonator]** Neighbors: `{', '.join([n['id'] for n in res['neighbors']])}`\n"
            report += f"**[Visual]** Manifold Map generated: `scene_3d_{p['id']}.json`\n\n---\n"

        with open('v22_manifold_map_report.md', 'w') as f: f.write(report)
        print("🏆 Manifold Mapping Complete. Check scene_3d_*.json files.")

if __name__ == "__main__":
    swarm = UBPSwarmTCTv22()
    if os.path.exists('ubp_mathnet_problem_set.json'):
        swarm.run('ubp_mathnet_problem_set.json')
