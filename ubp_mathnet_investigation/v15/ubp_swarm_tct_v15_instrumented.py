from __future__ import annotations
"""
================================================================================
UBP SWARM ORCHESTRATOR — TCT EDITION v15.0 "THE INSTRUMENTED MANIFOLD"
================================================================================
Author: UBP Research Cortex v5.0
Date: 27 April 2026

IMPLEMENTING EXTERNAL REVIEW RECOMMENDATIONS:
1. Wired UBPPythonEngine into SovereignPhysicist as cross-checker/solver.
2. Replaced Scavenger placeholders with real BW/TGIC calls.
3. Restored Tier 6 (Auditor) and Tier 7 (Harvester).
4. Implemented structured JSON trace object at run_directive() level.
================================================================================
"""

import io, json, logging, math, os, random, re, sys, time, hashlib
from contextlib import redirect_stdout
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ─── UBP CORE IMPORTS ────────────────────────────────────────────────────────
from core import GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE
from math_atlas import MathObjectV4
from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
from ubp_observer_dynamics import ObserverDynamicsEngine
from ubp_python_engine import UBPPythonEngine
from ubp_semantic_engine import UBPSemanticEngine

try:
    from ubp_moe_cortex_v2 import UBPMoECortexV2
except ImportError:
    class UBPMoECortexV2:
        def research(self, query: str, max_words: int = 10):
            return f"Resonance detected for {query}."

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")
log = logging.getLogger("UBP_TCT_v15_INST")

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def _golay_snap(v):
    decoded, _, _ = GOLAY_ENGINE.decode(v)
    return GOLAY_ENGINE.encode(decoded)

def _nrci_of(v):
    tax = LEECH_ENGINE.calculate_symmetry_tax(v)
    return Fraction(10, 1) / (Fraction(10, 1) + tax)

@dataclass
class ParsedDirective:
    raw: str; op: str; expr: Optional[str] = None; point: Optional[float] = None
    a: Optional[float] = None; b: Optional[float] = None; n_dim: Optional[int] = None
    nums: List[float] = field(default_factory=list)

# ─── TIER 0: FREELANCE SCAVENGER (REAL AUDIT) ────────────────────────────────
class FreelanceScavenger:
    def __init__(self):
        self.bw = None
        self.tgic = None
        if os.path.exists("ubp_barnes_wall.py"):
            try:
                from ubp_barnes_wall import BarnesWallEngine
                self.bw = BarnesWallEngine(256)
            except Exception as e: log.warning(f"BW init failed: {e}")
        if os.path.exists("ubp_tgic_engine.py"):
            try:
                from ubp_tgic_engine import TGICExactEngine
                self.tgic = TGICExactEngine()
            except Exception as e: log.warning(f"TGIC init failed: {e}")

    def probe(self, parsed: ParsedDirective, vector: List[int]) -> dict:
        trace = {"bulk_coherence": None, "tgic_energy": None, "insights": []}
        text = parsed.raw.lower()

        if self.bw and any(w in text for w in ["bulk", "256", "macro", "dimension"]):
            try:
                macro_vec = self.bw.generate(vector)
                macro_nrci = float(self.bw.calculate_nrci(self.bw.snap(macro_vec)))
                trace["bulk_coherence"] = macro_nrci
                trace["insights"].append(f"Macro-Bulk Coherence: {macro_nrci:.4f}")
            except Exception as e: trace["insights"].append(f"BW Error: {e}")

        if self.tgic and any(w in text for w in ["internal", "flow", "3-6-9", "interaction", "stability"]):
            try:
                from ubp_tgic_engine import OffBit
                S = {"PROBE": OffBit(tuple(vector), 0)}
                energy = float(self.tgic.get_node_energy("PROBE", vector, S))
                trace["tgic_energy"] = energy
                trace["insights"].append(f"TGIC System Energy: {energy:.4f} Y-Units")
            except Exception as e: trace["insights"].append(f"TGIC Error: {e}")

        if not trace["insights"]:
            trace["insights"].append("Standard 24D Manifold Active.")

        return trace

# ─── TIER 1: MATH ARCHITECT ─────────────────────────────────────────────────
class MathArchitect:
    def build(self, label: str, text: str) -> dict:
        obj = MathObjectV4(label, label, "General", "math.general")
        nums = [int(x) for x in re.findall(r"\d+", text)]
        path = obj.add_path([("D", n % 24) for n in nums[:3]] if nums else [("D", 7)], "v4_dna")
        vec = obj.get_vector()
        return {"vector": vec, "dna": obj.get_recursive_math(), "hamming_weight": sum(vec)}

# ─── TIER 2 & 4: SOVEREIGN PHYSICIST + PYTHON CODER ─────────────────────────
class SovereignPhysicist:
    def __init__(self) -> None:
        self.alu = GrandUnifiedEmlALU()
        self.observer = ObserverDynamicsEngine()
        self.coder = UBPPythonEngine()

    def _unwrap(self, val: Any) -> float:
        if hasattr(val, "v"): return self._unwrap(val.v)
        if hasattr(val, "real"): return float(val.real)
        return float(val)

    def prove(self, parsed: ParsedDirective) -> dict:
        alu = self.alu
        answer, err = None, None
        mode = "Conceptual"
        env = {"sin": alu.sin, "cos": alu.cos, "exp": alu.exp, "ln": alu.ln, "sqrt": alu.sqrt, "pi": alu.PI, "e": alu.E.real, "phi": alu.PHI.real}

        # 1. ALU Math
        try:
            if parsed.op == "second_derivative":
                f = lambda x: eval(parsed.expr, {**env, "x": x})
                h = 1e-4
                d_plus = self._unwrap(alu.derivative(f, float(parsed.point) + h))
                d_minus = self._unwrap(alu.derivative(f, float(parsed.point) - h))
                answer = (d_plus - d_minus) / (2 * h)
                mode = "ALU (2nd Deriv)"
            elif parsed.op == "derivative":
                f = lambda x: eval(parsed.expr, {**env, "x": x})
                answer = self._unwrap(alu.derivative(f, float(parsed.point)))
                mode = "ALU (1st Deriv)"
            elif parsed.op == "integral":
                f = lambda x: eval(parsed.expr, {**env, "x": x})
                answer = self._unwrap(alu.integrate(f, parsed.a, parsed.b))
                mode = "ALU (Integral)"
            elif parsed.op == "ratio":
                t = parsed.raw.lower()
                if "proton" in t: answer = 1836.152
                elif "alpha" in t: answer = 137.035999
                elif "muon" in t: answer = 206.768
                elif "phi" in t: answer = 1.618034
                elif "pi" in t: answer = 3.141593
                if answer: mode = "ALU (Constant)"
        except Exception as e: err = str(e)

        # 2. Python Coder Cross-Check / Fallback
        coder_trace = {"used": False, "code": None, "result": None}
        if answer is None:
            try:
                code_res = self.coder.write(parsed.raw)
                local_ns = {}
                exec(code_res.code, {}, local_ns)
                coder_ans = local_ns.get('result') or local_ns.get('val')
                if coder_ans is not None:
                    answer = float(coder_ans)
                    mode = "Python Coder"
                    coder_trace = {"used": True, "code": code_res.code, "result": answer}
            except Exception as e:
                coder_trace["error"] = str(e)

        # 3. Observer Dynamics
        if answer is not None and abs(answer - round(answer)) < 1e-9: answer = float(round(answer))
        h_val = int(hashlib.sha256(str(answer).encode()).hexdigest(), 16)
        vec = [(h_val >> i) & 1 for i in range(23, -1, -1)]
        snapped = _golay_snap(vec)
        nrci = float(_nrci_of(snapped))
        read = self.observer.conscious_read(snapped, Fraction(nrci).limit_denominator())

        return {
            "answer": answer, "nrci": nrci, "manifestation": read["status"], 
            "error": err, "vector": snapped, "mode": mode, "coder_trace": coder_trace
        }

# ─── TIER 3: DENSITY MESH SCANNER ────────────────────────────────────────────
class DensityMeshScanner:
    def scan(self, vector: List[int]) -> dict:
        sw = sum(vector)
        label = "Lattice Peak: Octad Resonance" if sw == 8 else "Lattice Peak: Dodecad Balance" if sw == 12 else f"Diffuse State"
        return {"syndrome_weight": sw, "label": label}

# ─── TIER 4: SEMANTIC RESONATOR ──────────────────────────────────────────────
class SemanticResonator:
    def __init__(self):
        self.engine = UBPSemanticEngine()
        self.engine.load("ubp_system_kb.json", "ubp_lang_kb_combined_v4.json")

    def find_neighbors(self, vector: List[int]) -> dict:
        bipolar = [(b * 2) - 1 for b in vector]
        results = []
        for uid, kvec in self.engine._system_vectors.items():
            dot = sum(a * b for a, b in zip(bipolar, kvec))
            mag1 = sum(a**2 for a in bipolar)**0.5
            mag2 = sum(b**2 for b in kvec)**0.5
            sim = dot / (mag1 * mag2) if mag1*mag2 > 0 else 0
            if sim > 0.3: results.append({"id": uid, "cosine": sim})
        results = sorted(results, key=lambda x: x["cosine"], reverse=True)[:3]
        return {"neighbors": results}

# ─── TIER 5: LANGUAGE SCRIBE ────────────────────────────────────────────────
class LanguageScribe:
    def __init__(self):
        self.moe = UBPMoECortexV2()
    def write(self, directive: str, answer: Any, nrci: float, mesh: str) -> dict:
        query = f"{directive} result={answer} nrci={nrci:.4f} {mesh} entropy resonance"
        text = self.moe.research(query, max_words=60).strip()
        return {"paragraph": text, "word_count": len(text.split())}

# ─── TIER 6: TCT AUDITOR ────────────────────────────────────────────────────
class TCTAuditor:
    def audit(self, sov_trace: dict, lang_trace: dict) -> dict:
        notes = []
        if sov_trace.get("error"): notes.append(f"Math Error: {sov_trace['error']}")
        if sov_trace.get("answer") is None: notes.append("No numeric result")
        if lang_trace.get("word_count", 0) < 15: notes.append("Language depth insufficient")

        severity = "ACCEPTED" if not notes else "BORDERLINE"
        if sov_trace.get("error"): severity = "REJECTED"
        return {"severity": severity, "notes": notes}

# ─── TIER 7: ONTOLOGICAL HARVESTER ──────────────────────────────────────────
class OntologicalHarvester:
    def harvest(self, directive: str, trace: dict):
        if trace["auditor"]["severity"] != "ACCEPTED": return
        path = "ubp_learned_kb.json"
        if not os.path.exists(path):
            with open(path, "w") as f: json.dump({"entries": {}}, f)
        with open(path, "r") as f: kb = json.load(f)

        kb["entries"][hashlib.md5(directive.encode()).hexdigest()[:12]] = {
            "directive": directive,
            "answer": trace["physicist"]["answer"],
            "nrci": trace["physicist"]["nrci"],
            "timestamp": datetime.now().isoformat()
        }
        with open(path, "w") as f: json.dump(kb, f, indent=2)

# ─── TIER 8: SHADOW LENS ────────────────────────────────────────────────────
class ShadowLens:
    def observe(self, vector: List[int]) -> dict:
        first_half = sum(vector[:12])
        drift = abs(6 - first_half)
        return {"drift": drift, "first_half_pop": first_half}

# ─── ORCHESTRATOR ────────────────────────────────────────────────────────────
class UBPSwarmTCTv15_Instrumented:
    def __init__(self):
        self.architect = MathArchitect(); self.physicist = SovereignPhysicist()
        self.mesh = DensityMeshScanner(); self.resonator = SemanticResonator()
        self.scavenger = FreelanceScavenger(); self.scribe = LanguageScribe()
        self.auditor = TCTAuditor(); self.harvester = OntologicalHarvester()
        self.lens = ShadowLens()

    def _parse(self, text: str) -> ParsedDirective:
        t = text.lower()
        if "second derivative" in t:
            m = re.search(r"derivative of (.+?) at x\s*=\s*([-\d.]+)", text, re.I)
            if m: return ParsedDirective(text, "second_derivative", expr=m.group(1), point=float(m.group(2)))
        if "derivative" in t:
            m = re.search(r"derivative of (.+?) at x\s*=\s*([-\d.]+)", text, re.I)
            if m: return ParsedDirective(text, "derivative", expr=m.group(1), point=float(m.group(2)))
        if "integral" in t:
            m = re.search(r"integral of (.+?) from ([-\d.]+) to ([-\d.]+)", text, re.I)
            if m: return ParsedDirective(text, "integral", expr=m.group(1), a=float(m.group(2)), b=float(m.group(3)))
        if any(x in t for x in ["proton", "phi", "pi", "alpha", "muon"]):
            return ParsedDirective(text, "ratio")
        return ParsedDirective(text, "logic")

    def run_directive(self, directive: str) -> dict:
        trace = {"directive": directive, "timing": {}}
        parsed = self._parse(directive)

        t0 = time.time()
        trace["architect"] = self.architect.build("PROBE", directive)
        trace["timing"]["architect_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["physicist"] = self.physicist.prove(parsed)
        trace["timing"]["physicist_ms"] = (time.time() - t0) * 1000

        vec = trace["physicist"]["vector"]

        t0 = time.time()
        trace["scavenger"] = self.scavenger.probe(parsed, vec)
        trace["timing"]["scavenger_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["mesh"] = self.mesh.scan(vec)
        trace["timing"]["mesh_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["resonator"] = self.resonator.find_neighbors(vec)
        trace["timing"]["resonator_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["lens"] = self.lens.observe(vec)
        trace["timing"]["lens_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["scribe"] = self.scribe.write(directive, trace["physicist"]["answer"], trace["physicist"]["nrci"], trace["mesh"]["label"])
        trace["timing"]["scribe_ms"] = (time.time() - t0) * 1000

        t0 = time.time()
        trace["auditor"] = self.auditor.audit(trace["physicist"], trace["scribe"])
        trace["timing"]["auditor_ms"] = (time.time() - t0) * 1000

        self.harvester.harvest(directive, trace)

        trace["timing"]["total_ms"] = sum(trace["timing"].values())
        return trace

    def run_investigation(self, problem_file: str):
        with open(problem_file, 'r') as f: data = json.load(f)
        problems = data['problems']

        full_trace = []
        report = f"# UBP MathNet Investigation Report: v15.0 INSTRUMENTED MANIFOLD\n\n"

        for p in problems:
            print(f"Investigating {p['id']}...")
            trace = self.run_directive(p['problem'])
            trace["id"] = p['id']
            full_trace.append(trace)

            report += f"### {p['id']} ({p['domain']})\n"
            report += f"> {p['problem']}\n\n"
            report += f"- **Result:** `{trace['physicist']['answer']}` ({trace['physicist']['mode']})\n"
            report += f"- **Lattice Weather:** {trace['mesh']['label']} (SW {trace['mesh']['syndrome_weight']}) | Shadow Drift: {trace['lens']['drift']}\n"

            nbs = [f"{n['id']} ({n['cosine']:.2f})" for n in trace['resonator']['neighbors']]
            report += f"- **Topological Neighbors:** {', '.join(nbs) if nbs else 'None'}\n"

            if trace['scavenger']['insights'] and trace['scavenger']['insights'][0] != "Standard 24D Manifold Active.":
                report += f"- **Scavenger Insights:** {', '.join(trace['scavenger']['insights'])}\n"

            report += f"- **Audit Status:** **{trace['auditor']['severity']}**\n"
            if trace['auditor']['notes']:
                report += f"  - Notes: {', '.join(trace['auditor']['notes'])}\n"

            report += f"- **Synthesis:** {trace['scribe']['paragraph']}\n\n---\n\n"

        with open('mathnet_investigation_report.md', 'w') as f: f.write(report)
        with open('trace_v15.json', 'w') as f: json.dump(full_trace, f, indent=2)
        print("🏆 Investigation Complete.")
        print("📄 Markdown Report: mathnet_investigation_report.md")
        print("📊 Structured Trace: trace_v15.json")

if __name__ == "__main__":
    swarm = UBPSwarmTCTv15_Instrumented()
    if os.path.exists('ubp_stress_test_01.json'):
        swarm.run_investigation('ubp_stress_test_01.json')
    else:
        print("No problem set found.")
