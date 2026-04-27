"""
================================================================================
UBP SWARM ORCHESTRATOR — TCT EDITION v5.5 "PURE SOVEREIGNTY"
================================================================================
Author: UBP Research Cortex v5.0
Date: 22 April 2026

PARADIGM SHIFT:
- ZERO EXTERNAL DEPENDENCIES. No OpenAI. No probabilistic LLMs.
- All language generation is handled by the local, deterministic MoE Cortex.
- All physics calculations are handled by the Sovereign EML-ALU and Observer.
- The system learns and harvests its own geometric discoveries locally.
================================================================================
"""

import os
import sys
import json
import time
import hashlib
import re
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from fractions import Fraction
from typing import List, Dict, Optional, Any

# ─── SETUP ───────────────────────────────────────────────────────────────────
CORE_DIR = '.'
LEARNING_FILE = 'ubp_learned_geometry.json'
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("UBP_PURE_v5")

# ─── ENGINE IMPORTS ──────────────────────────────────────────────────────────
try:
    from ubp_semantic_engine import UBPSemanticEngine
    from math_atlas import MathObjectV4
    from ubp_py_runtime import UBPPyVM, MOGOntology
    from ubp_moe_cortex_v2 import UBPMoECortexV2 as MoECortex
    from ubp_tgic_engine import TGICExactEngine, OffBit
    from ubp_observer_dynamics import ObserverDynamicsEngine
    from ubp_eml_alu_sovereign import GrandUnifiedEmlALU, EmlTreeNode
    ENGINES_OK = True
except ImportError as e:
    ENGINES_OK = False
    logger.error(f"Engine import error: {e}. Ensure all core files are present.")

LEECH_PLATFORMS = {
    "OCTAD": {"weight": 8, "target_nrci": 0.7647, "desc": "Foundational Stability"},
    "DODECAD": {"weight": 12, "target_nrci": 0.6850, "desc": "Structural Interaction"},
    "HEXADECAD": {"weight": 16, "target_nrci": 0.6206, "desc": "High-Tension Complexity"},
}

# ─── DATA STRUCTURES ─────────────────────────────────────────────────────────
@dataclass
class MathColumn:
    step_id: str; concept: str; ubp_id: str; voxel_path: str; voxel_count: int
    tax_str: str; nrci: float; vector: List[int]; math_dna: str; kb_anchors: List[str]

@dataclass
class SovereignColumn:
    eml_tree: str; golay_address: int; snapped_vector: List[int]
    soc_energy: float; manifestation: str

@dataclass
class PythonColumn:
    step_id: str; concept: str; ubp_program: str; exec_nrci: float; exec_dqi: float
    exec_mog: Dict; exec_success: bool; atoms_created: List[str]

@dataclass
class LanguageColumn:
    step_id: str; concept: str; paragraph: str; word_count: int; lang_resonance: float
    nrci: float; is_complete: bool

@dataclass
class TCTStep:
    step_id: str; step_title: str; platform: str
    math: MathColumn; sovereign: SovereignColumn; python: PythonColumn; language: LanguageColumn
    alignment_score: float; accepted: bool; attempts: int; audit_notes: List[str]

# ─── TIER 1-4: THE PURE ENGINES ──────────────────────────────────────────────

class MathArchitectEngine:
    def __init__(self, semantic_engine):
        self.semantic = semantic_engine
        self._used_ids = set()
    
    def build(self, concept: str, step_id: str, platform: str) -> MathColumn:
        results = self.semantic.query(concept, top_k=5) if self.semantic else []
        fresh = [r for r in results if r.ubp_id not in self._used_ids]
        anchors = fresh[:3] if fresh else results[:3]
        for a in anchors: self._used_ids.add(a.ubp_id)
        
        ubp_id = f"TCT_MATH_{step_id.upper()}"
        target_nrci = LEECH_PLATFORMS[platform]["target_nrci"]
        
        best_d, best_x, best_nrci, best_tax, best_vec = 1, 0, 0.0, Fraction(0), []
        min_diff = 999.0
        
        for d in range(1, 15):
            for x in range(0, 8):
                try:
                    obj = MathObjectV4(ubp_id, concept[:40], "TCT", "math.tct")
                    prims = [('D', d)]
                    if x > 0: prims.append(('X', x))
                    path = obj.add_path(prims, "test")
                    nrci_val = float(Fraction(10, 1) / (Fraction(10, 1) + path.tax))
                    diff = abs(nrci_val - target_nrci)
                    if diff < min_diff:
                        min_diff = diff
                        best_d, best_x, best_nrci, best_tax, best_vec = d, x, nrci_val, path.tax, obj.get_vector()
                except: continue
                    
        return MathColumn(
            step_id=step_id, concept=concept, ubp_id=ubp_id,
            voxel_path=f"D({best_d}) X({best_x})", voxel_count=best_d + best_x,
            tax_str=f"{best_tax.numerator}/{best_tax.denominator}", nrci=best_nrci,
            vector=best_vec, math_dna=f"D={best_d}|X={best_x}",
            kb_anchors=[a.ubp_id for a in anchors]
        )

class SovereignPhysicist:
    def __init__(self):
        self.alu = GrandUnifiedEmlALU()
        self.observer = ObserverDynamicsEngine()

    def prove(self, concept: str, math_col: MathColumn) -> SovereignColumn:
        # Build EML tree from the Math Architect's voxel count
        tree = EmlTreeNode("eml", EmlTreeNode("leaf", leaf=float(math_col.voxel_count)), EmlTreeNode("leaf", leaf=1.0))
        
        # Snap to Lattice using the Triadic Monad as the input
        snapped_vec, addr = self.alu.snap_eml_to_lattice(tree, x_input=complex(self.alu.TRIADIC_MONAD))
        
        # Observer Audit
        nrci_frac = Fraction(math_col.nrci).limit_denominator(1000)
        soc = self.observer.calculate_soc_energy(snapped_vec, nrci_frac)
        read = self.observer.conscious_read(snapped_vec, nrci_frac)
        
        return SovereignColumn(
            eml_tree=str(tree), golay_address=addr, snapped_vector=snapped_vec,
            soc_energy=float(soc), manifestation=read.get('status', 'SUBLIMINAL')
        )

class PythonCoderEngine:
    def code_and_run(self, concept: str, math_col: MathColumn, step_id: str, platform: str) -> PythonColumn:
        target_nrci = LEECH_PLATFORMS[platform]["target_nrci"]
        lines = [f"# TCT Step {step_id}: {concept}"]
        atom_labels = []
        for i, anchor_id in enumerate(math_col.kb_anchors[:3]):
            label = f"A{i+1}"
            lines.append(f"LET {label} 1/1 TIER {i} CAT CONCEPT")
            atom_labels.append(label)
        if not atom_labels:
            lines.append(f"LET BASE 1/1 TIER 0 CAT CONCEPT")
            atom_labels = ["BASE"]
            
        u_score = target_nrci / 0.7623 
        recipe = " + ".join([f"1x{lbl}" for lbl in atom_labels])
        lines.append(f"SYNTH RESULT FROM \"{recipe}\" U_SCORE {u_score:.4f}")
        program = "\n".join(lines)
            
        try:
            vm = UBPPyVM(kb_path='ubp_system_kb.json', lattice_path=f'tct_lattice_{step_id}.json')
            for line in program.split('\n'):
                parts = line.strip().split()
                if not parts or parts[0].startswith('#'): continue
                if parts[0] == 'LET': vm.let(parts[1], parts[2])
                elif parts[0] == 'SYNTH': 
                    recipe_str = re.search(r'"([^"]+)"', line).group(1)
                    u_val = float(parts[-1]) if "U_SCORE" in line else 1.0
                    vm.synth(parts[1], recipe_str, u_score=u_val)
            
            res_atom = vm.env.get('RESULT') or list(vm.env.values())[-1]
            return PythonColumn(step_id, concept, program, float(res_atom.dqi), res_atom.dqi, MOGOntology.calculate_health(res_atom.vector), True, atom_labels)
        except Exception as e:
            return PythonColumn(step_id, concept, program, 0.5, 0.5, {}, False, [], str(e))

class LanguageScribeEngine:
    def __init__(self, moe):
        self.moe = moe

    def write(self, concept: str, math_col: MathColumn, sov_col: SovereignColumn, py_col: PythonColumn, platform: str) -> LanguageColumn:
        target = LEECH_PLATFORMS[platform]["target_nrci"]
        
        base_para = (f"The concept of **{concept}** is geometrically anchored to the **{platform}** platform. "
                f"The Math Architect tuned a {math_col.voxel_count}-voxel manifold via `{math_col.voxel_path}`, yielding NRCI {math_col.nrci:.4f}. "
                f"The Sovereign Physicist evaluated the EML tree `{sov_col.eml_tree}`, snapping to Golay Address **{sov_col.golay_address}**. "
                f"The Observer confirms this state is **{sov_col.manifestation}** with an SOC Energy of {sov_col.soc_energy:,.2f} CU. "
                f"Python synthesis achieved operational NRCI {py_col.exec_nrci:.4f}.")

        moe_para = ""
        if self.moe:
            try:
                moe_para = " " + self.moe.research(f"{concept} {platform} {sov_col.manifestation}", max_words=15).strip()
            except: pass
            
        full_para = base_para + moe_para
        if not full_para.endswith('.'): full_para += '.'
        
        resonance = 0.85 - (abs(math_col.nrci - target) * 2)
        return LanguageColumn(math_col.step_id, concept, full_para, len(full_para.split()), resonance, float(math_col.nrci), True)

# ─── TIER 5-8: AUDITORS & HARVESTERS ─────────────────────────────────────────

class TCTAuditor:
    def audit(self, math_col: MathColumn, py_col: PythonColumn, sov_col: SovereignColumn, platform: str):
        target_nrci = LEECH_PLATFORMS[platform]["target_nrci"]
        notes = []
        math_diff = abs(math_col.nrci - target_nrci)
        py_diff = abs(py_col.exec_nrci - target_nrci)
        
        passed = (math_diff <= 0.03 and py_diff <= 0.03 and sov_col.manifestation == "MANIFESTED")
        
        notes.append(f"{'PASS' if math_diff <= 0.03 else 'FAIL'}: Math NRCI Diff: {math_diff:.4f}")
        notes.append(f"{'PASS' if py_diff <= 0.03 else 'FAIL'}: Exec NRCI Diff: {py_diff:.4f}")
        notes.append(f"{'PASS' if sov_col.manifestation == 'MANIFESTED' else 'FAIL'}: Observer Status: {sov_col.manifestation}")
        
        alignment = (math_col.nrci + py_col.exec_nrci) / 2
        if alignment > 0.70 and sov_col.manifestation == "MANIFESTED":
            passed = True
            notes.append(f"AUTO-SNAP: High Alignment ({alignment:.4f}) and Manifestation triggered acceptance.")
            
        return passed, alignment, notes

class TGICRelationalAuditor:
    def __init__(self):
        self.tgic = TGICExactEngine() if ENGINES_OK else None

    def evaluate_manifold(self, steps: List[TCTStep]) -> Dict[str, Any]:
        if not self.tgic or not steps: return {"status": "TGIC Engine Unavailable"}
        S = {step.step_id: OffBit(tuple(step.math.vector), 0) for step in steps}
        total_energy = self.tgic.get_total_energy(S)
        return {"status": "SUCCESS", "total_manifold_energy": float(total_energy)}

class OntologicalHarvester:
    @staticmethod
    def harvest(steps: List[TCTStep], directive_hash: str, manifold_energy: float):
        if manifold_energy > 350.0: return 0
        if os.path.exists(LEARNING_FILE):
            with open(LEARNING_FILE, 'r') as f: learned_kb = json.load(f)
        else:
            learned_kb = {"_fields": ["ubp_id", "lexicon", "tags", "vector", "nrci_val"], "entries": {}}

        new_count = 0
        for step in steps:
            if step.accepted:
                uid = f"LEARNED_{step.step_title.upper()}_{directive_hash}"
                entry = [
                    uid, 
                    f"[Learned: {step.step_title}], {step.language.paragraph[:180]}...", 
                    ["LEARNED", "PURE_SWARM", datetime.now().strftime("%Y-%m-%d")], 
                    step.math.vector, 
                    round(step.math.nrci, 8)
                ]
                fp = hashlib.sha256(str(step.math.vector).encode()).hexdigest()
                if fp not in learned_kb["entries"]:
                    learned_kb["entries"][fp] = entry
                    new_count += 1
        if new_count > 0:
            with open(LEARNING_FILE, 'w') as f: json.dump(learned_kb, f, indent=2)
        return new_count

class Director:
    def synthesize(self, steps: List[TCTStep], tgic: Dict, directive: str, learned_count: int) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md = f"# TCT v5.5 Pure Sovereign Report — {directive}\n\n"
        md += f"**Generated:** {timestamp} | **Manifold Energy:** {tgic.get('total_manifold_energy', 0):.4f} | **Learned:** {learned_count}\n\n"
        for step in steps:
            md += f"### {step.step_title} ({step.platform} Platform)\n"
            md += f"{step.language.paragraph}\n\n"
            md += f"- **Math DNA:** `{step.math.math_dna}` | **Golay Address:** `{step.sovereign.golay_address}`\n"
            md += f"- **Observer:** `{step.sovereign.manifestation}` ({step.sovereign.soc_energy:,.0f} CU) | **Alignment:** {step.alignment_score:.4f}\n\n"
        return md

# ─── MAIN ORCHESTRATOR ───────────────────────────────────────────────────────

class UBPSwarmTCTv5_Pure:
    def __init__(self, directive: str, num_steps: int = 3):
        self.directive = directive
        self.num_steps = num_steps
        self.directive_hash = hashlib.sha256(directive.encode()).hexdigest()[:8]
        
        self.semantic = UBPSemanticEngine() if ENGINES_OK else None
        if self.semantic:
            self.semantic.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
            if os.path.exists(LEARNING_FILE):
                with open(LEARNING_FILE, 'r') as f: self._hydrate_learned(json.load(f))
        
        self.moe = MoECortex() if ENGINES_OK else None
        self.math_engine = MathArchitectEngine(self.semantic)
        self.sov_engine = SovereignPhysicist()
        self.py_engine = PythonCoderEngine()
        self.lang_engine = LanguageScribeEngine(self.moe)
        self.auditor = TCTAuditor()
        self.tgic_auditor = TGICRelationalAuditor()
        self.director = Director()

    def _hydrate_learned(self, data):
        fields = data.get("_fields", [])
        f_idx = {name: i for i, name in enumerate(fields)}
        for fp, entry_list in data.get("entries", {}).items():
            uid = entry_list[f_idx["ubp_id"]]
            entry = {"ubp_id": uid, "lexicon": entry_list[f_idx["lexicon"]], "vector": entry_list[f_idx["vector"]], "nrci_val": entry_list[f_idx["nrci_val"]]}
            self.semantic.all_kb[uid] = entry
            self.semantic.system_kb[uid] = entry
            if entry["vector"]: self.semantic._system_vectors[uid] = [(b*2)-1 for b in entry["vector"]]
        self.semantic._build_indexes()

    def run(self):
        logger.info(f"Starting UBP PURE SOVEREIGN SWARM v5.5 | Directive: {self.directive}")
        platforms = list(LEECH_PLATFORMS.keys())
        words = [w for w in self.directive.split() if len(w) > 4]
        
        final_steps = []
        for i in range(self.num_steps):
            concept = words[i % len(words)].capitalize() if words else f"Concept_{i+1}"
            platform = platforms[i % 3]
            sid = f"step{i+1:02d}"
            
            logger.info(f"Processing {sid}: {concept} [{platform}]")
            math_col = self.math_engine.build(concept, sid, platform)
            sov_col = self.sov_engine.prove(concept, math_col)
            py_col = self.py_engine.code_and_run(concept, math_col, sid, platform)
            lang_col = self.lang_engine.write(concept, math_col, sov_col, py_col, platform)
            
            accepted, alignment, notes = self.auditor.audit(math_col, py_col, sov_col, platform)
            for n in notes: logger.info(f"  {n}")
            
            step = TCTStep(sid, concept, platform, math_col, sov_col, py_col, lang_col, alignment, accepted, 1, notes)
            final_steps.append(step)

        tgic_report = self.tgic_auditor.evaluate_manifold(final_steps)
        learned_count = OntologicalHarvester.harvest(final_steps, self.directive_hash, tgic_report.get("total_manifold_energy", 0))
        
        report_md = self.director.synthesize(final_steps, tgic_report, self.directive, learned_count)
        with open("tct_v5_pure_report.md", "w", encoding="utf-8") as f: f.write(report_md)
        logger.info(f"✅ Pure Sovereign Report saved. Learned {learned_count} concepts.")

if __name__ == "__main__":
    # You can change this directive to test MathNet concepts or general physics
    orch = UBPSwarmTCTv5_Pure(directive="The optimal method of calculating numbers", num_steps=3)
    orch.run()