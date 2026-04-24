"""
================================================================================
UBP SWARM TCT — MathNet Investigation v4.0 "SELF-ORGANISING SUBSTRATE"
================================================================================
Author: UBP Research Cortex / Euan Craig Investigation
Date: April 2026

DESIGN PHILOSOPHY (v4.0):
--------------------------
This version removes ALL external LLM dependencies (no GPT, no OpenAI).
It removes numpy. It uses only the pure UBP substrate.

The key insight from v3.x: the system was using GPT to "solve" problems and
then claiming UBP credit for the result. That is not what this investigation
is about.

What this system ACTUALLY does — and what is genuinely interesting:
  1. Maps each MathNet problem's numerical structure to the 24D Leech Lattice
  2. Finds the governing UBP Law via cosine resonance search
  3. Runs a Density Mesh scan (n=1..24) across 4 agent species to find natural
     stability peaks in the UBP substrate
  4. Computes a TCT (Three Column Thinking) alignment across Math, Sovereign,
     and Language columns — using only UBP engines
  5. The MoE Cortex synthesises a UBP-native interpretation from topological
     neighbours — no external text generation

The "answer" is a TOPOLOGICAL SIGNATURE: a 24-bit address in the Leech Lattice,
a governing law, a stability landscape, and a UBP-native interpretation.

This is NOT a mathematical solver. It is a UBP substrate mapper.
The results are genuinely cryptic — that is a feature, not a bug.
The system is working with logic and geometry, not conventional arithmetic.

AGENTS AND THEIR SELF-DISCOVERED ROLES:
  - MathArchitect: builds 24-bit vectors from problem numbers via MathObjectV4
  - SovereignPhysicist: snaps to Leech Lattice, computes NRCI + SOC energy
  - DensityMeshScanner: scans n=1..24 with 4 metabolic species, finds peaks
  - SemanticResonator: finds governing UBP law via cosine similarity
  - MoESynthesist: generates UBP-native language from topological neighbours
  - TCTAuditor: checks cross-column alignment, accepts/rejects each step
  - OntologicalHarvester: stores accepted concepts in the learning KB
  - ShadowLens: background observer tracking noumenal drift

HONEST REPORTING:
  - No "CORRECT/INCORRECT" grading against reference answers
  - All raw UBP outputs are reported as-is
  - Interpretations are clearly labelled as UBP-substrate readings
  - Stability peaks are reported with their n-values and species
  - Cryptic MoE outputs are reported verbatim — the system is working with
    its own logic, not human-readable mathematics
================================================================================
"""

import os
import sys
import json
import re
import math
import hashlib
import logging
from fractions import Fraction
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional

# ─── PATH SETUP ──────────────────────────────────────────────────────────────
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("UBP_SWARM_v4")

# ─── ENGINE IMPORTS ──────────────────────────────────────────────────────────
ENGINES_OK = False
GOLAY_ENGINE = None
LEECH_ENGINE = None

try:
    from core import GOLAY_ENGINE, LEECH_ENGINE
    from ubp_semantic_engine import UBPSemanticEngine
    from ubp_observer_dynamics import ObserverDynamicsEngine
    from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
    from math_atlas import MathObjectV4
    from ubp_tgic_engine import TGICExactEngine, OffBit
    from ubp_py_runtime import UBPPyVM
    from ubp_moe_cortex_v2 import UBPMoECortexV2
    from ubp_fom_system import FOMManager, FrameOfMind
    ENGINES_OK = True
    logger.info("All UBP engines loaded successfully — pure substrate mode")
except ImportError as e:
    logger.error(f"Engine import failed: {e}")
    sys.exit(1)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
LEARNING_FILE = os.path.join(os.path.dirname(CORE_DIR), "results", "ubp_learned_kb.json")
LEECH_PLATFORMS = {
    "OCTAD":     {"min_nrci": Fraction(70, 100), "label": "High Coherence"},
    "DODECAD":   {"min_nrci": Fraction(65, 100), "label": "Mid Coherence"},
    "HEXADECAD": {"min_nrci": Fraction(0,  100), "label": "Low Coherence"},
}

# ─── DATA STRUCTURES ─────────────────────────────────────────────────────────

@dataclass
class MathColumn:
    """Column 1: Mathematical structure of the problem"""
    concept: str
    key_numbers: List[int]
    vector: List[int]
    nrci: float
    syndrome_weight: int
    platform: str
    math_dna: str  # hex fingerprint of the vector

@dataclass
class SovereignColumn:
    """Column 2: Physical/geometric properties in the Leech Lattice"""
    golay_address: int
    snapped_vector: List[int]
    soc_energy: float
    manifestation: str
    shadow_bits: List[int]  # first 12 bits — the noumenal shadow
    octad_similarity: float  # cosine similarity to nearest octad (0.0–1.0)
    octad_index: int         # index of nearest octad in the 759 octads
    correctable: bool        # whether the snap was within correction radius (<=3 errors)

@dataclass
class DensityMeshResult:
    """Column 3: Stability landscape from the Density Mesh scan"""
    peaks: List[Dict]          # n-values where NRCI > threshold
    dominant_species: str      # which metabolic species wins most often
    landscape: List[Dict]      # full n=1..24 scan
    peak_summary: str          # human-readable UBP description

@dataclass
class SemanticColumn:
    """Column 4: Governing UBP Law and topological neighbours"""
    governing_law: str
    law_resonance: float
    law_definition: str
    top_neighbours: List[Tuple[str, float]]

@dataclass
class LanguageColumn:
    """Column 5: MoE-synthesised UBP-native interpretation"""
    moe_synthesis: str
    synthesis_probe: str  # what the MoE was asked
    tct_alignment: float  # cross-column NRCI alignment

@dataclass
class TCTStep:
    """A complete TCT step — all five columns"""
    step_id: str
    problem_id: str
    domain: str
    math: MathColumn
    sovereign: SovereignColumn
    density: DensityMeshResult
    semantic: SemanticColumn
    language: LanguageColumn
    accepted: bool
    alignment_score: float
    audit_notes: List[str]

# ─── AGENT 1: MATH ARCHITECT ─────────────────────────────────────────────────

class MathArchitect:
    """
    Builds 24-bit vectors from problem numbers using MathObjectV4.
    Uses the D (Dimension) primitive for each key number.
    Self-discovered role: convert human numbers to UBP substrate coordinates.
    """
    def __init__(self):
        self.alu = GrandUnifiedEmlALU()

    def extract_numbers(self, text: str) -> List[int]:
        """Extract up to 6 unique positive integers from problem text."""
        nums = []
        for m in re.finditer(r'\b(\d+)\b', text):
            n = int(m.group(1))
            if 1 <= n <= 10000 and n not in nums:
                nums.append(n)
            if len(nums) >= 6:
                break
        return nums if nums else [1]

    def build(self, problem_id: str, domain: str, text: str) -> MathColumn:
        nums = self.extract_numbers(text)
        concept = f"{domain}_{problem_id}"

        # Build via MathObjectV4 D-primitives
        try:
            obj = MathObjectV4(problem_id, concept, domain[:3].upper(), f"math.{domain[:3].lower()}")
            # Use first number as primary D-path, rest as secondary
            path_steps = [('D', n % 24) for n in nums[:3]]
            path = obj.add_path(path_steps, "primary")
            vector = obj.get_vector()
            tax = path.tax
        except Exception as e:
            logger.warning(f"MathObjectV4 failed for {problem_id}: {e}, using Golay fallback")
            # Fallback: hash-based vector
            h = int(hashlib.sha256(text.encode()).hexdigest(), 16)
            vector = [(h >> i) & 1 for i in range(23, -1, -1)]
            tax = LEECH_ENGINE.calculate_symmetry_tax(vector)

        nrci = float(Fraction(10, 1) / (Fraction(10, 1) + Fraction(float(tax)).limit_denominator(1000)))

        # Golay snap for syndrome weight
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(vector)
        syndrome_weight = snap_info.get('syndrome_weight', 0)

        # Platform classification
        nrci_frac = Fraction(nrci).limit_denominator(100)
        if nrci_frac >= Fraction(70, 100):
            platform = "OCTAD"
        elif nrci_frac >= Fraction(65, 100):
            platform = "DODECAD"
        else:
            platform = "HEXADECAD"

        math_dna = hashlib.sha256(str(vector).encode()).hexdigest()[:12]

        return MathColumn(
            concept=concept,
            key_numbers=nums,
            vector=vector,
            nrci=nrci,
            syndrome_weight=syndrome_weight,
            platform=platform,
            math_dna=math_dna
        )

# ─── AGENT 2: SOVEREIGN PHYSICIST ────────────────────────────────────────────

class SovereignPhysicist:
    """
    Snaps the math vector to the Leech Lattice and computes physical metrics.
    Self-discovered role: determine the Observer Status and SOC energy of each problem.
    """
    def __init__(self):
        self.observer = ObserverDynamicsEngine()

    def prove(self, math_col: MathColumn) -> SovereignColumn:
        # Snap to Golay codeword
        snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(math_col.vector)

        # Golay codeword index — find position in sorted codeword list
        try:
            all_codewords = GOLAY_ENGINE.get_all_codewords()
            try:
                addr = all_codewords.index(snapped)
            except ValueError:
                # snapped not in list (returned as int 0 when uncorrectable)
                # Use syndrome weight as a proxy address
                addr = snap_info.get('syndrome_weight', 0)
        except Exception:
            addr = 0

        # Octad membership: is the original vector close to any of the 759 octads?
        octads = GOLAY_ENGINE.get_octads()
        bipolar_orig = [(b * 2) - 1 for b in math_col.vector]
        best_octad_sim = 0.0
        best_octad_idx = -1
        for oi, octad in enumerate(octads):
            bipolar_oct = [(b * 2) - 1 for b in octad]
            dot = sum(a * b for a, b in zip(bipolar_orig, bipolar_oct))
            m1 = sum(a**2 for a in bipolar_orig) ** 0.5
            m2 = sum(b**2 for b in bipolar_oct) ** 0.5
            sim = dot / (m1 * m2) if m1 * m2 > 0 else 0.0
            if sim > best_octad_sim:
                best_octad_sim = sim
                best_octad_idx = oi
        # Store octad info in the address field (octad index if member, else -1)
        if best_octad_sim >= 0.75:
            addr = best_octad_idx  # strong octad membership
        # Store octad similarity in snap_info for reporting
        snap_info['octad_similarity'] = best_octad_sim
        snap_info['octad_index'] = best_octad_idx
        snap_info['correctable'] = snap_info.get('correctable', False)

        # SOC energy and Observer status
        nrci_frac = Fraction(math_col.nrci).limit_denominator(1000)
        soc = self.observer.calculate_soc_energy(snapped, nrci_frac)
        read = self.observer.conscious_read(snapped, nrci_frac)
        manifestation = read.get('status', 'SUBLIMINAL')

        # Shadow bits: first 12 bits of the snapped vector
        shadow_bits = snapped[:12]

        return SovereignColumn(
            golay_address=addr,
            snapped_vector=snapped,
            soc_energy=float(soc),
            manifestation=manifestation,
            shadow_bits=shadow_bits,
            octad_similarity=snap_info.get('octad_similarity', 0.0),
            octad_index=snap_info.get('octad_index', -1),
            correctable=snap_info.get('correctable', False)
        )

# ─── AGENT 3: DENSITY MESH SCANNER ───────────────────────────────────────────

class DensityMeshScanner:
    """
    Scans n=1..24 with 4 metabolic species to find natural stability peaks.
    Based on the Master Crucible v12 approach — logarithmic metabolism (safe).
    Self-discovered role: find where the UBP substrate is naturally stable
    for this problem's numerical structure.
    """
    def __init__(self):
        self.alu = GrandUnifiedEmlALU()

    def _species_alpha(self, nums: List[int], n: int) -> Optional[List[int]]:
        """Logarithmic metabolism: n * ln(base)"""
        try:
            base = float(nums[0]) if nums else 2.0
            if base <= 0:
                base = 2.0
            log_mass = n * math.log(base)
            div = float(nums[1]) if len(nums) > 1 else 7.0
            # Use EML ALU: eml(log_mass, div)
            result = self.alu.eml(complex(log_mass), complex(div))
            mag = abs(result)
            # Map magnitude to 24-bit vector via modular hashing
            h = int(hashlib.sha256(f"alpha_{mag:.6f}".encode()).hexdigest(), 16)
            return [(h >> i) & 1 for i in range(23, -1, -1)]
        except (OverflowError, ValueError, ZeroDivisionError):
            return None

    def _species_beta(self, problem_id: str, nums: List[int], n: int) -> Optional[List[int]]:
        """Voxel path metabolism: MathObjectV4 D-path"""
        try:
            obj = MathObjectV4(f"{problem_id}_{n}", "density", "DM", "math.dm")
            base = nums[0] if nums else 2
            path = obj.add_path([('D', int(n % 24)), ('X', int(base % 8))], "density_beta")
            return obj.get_vector()
        except Exception:
            return None

    def _species_gamma(self, text: str, n: int) -> List[int]:
        """Bit-logic metabolism: SHA256 hash"""
        h = int(hashlib.sha256(f"{text}{n}".encode()).hexdigest(), 16)
        return [(h >> i) & 1 for i in range(23, -1, -1)]

    def _species_delta(self, nums: List[int], n: int) -> List[int]:
        """Harmonic rotation: pure trigonometric using EML ALU sin"""
        phase = Fraction(n, 12)  # rational phase
        vec = []
        for i in range(24):
            angle = float(phase) * math.pi + (i * 0.1)
            # Use Python math.sin (EML ALU sin is for complex Dual numbers)
            vec.append(1 if math.sin(angle) > 0 else 0)
        return vec

    def scan(self, problem_id: str, text: str, nums: List[int]) -> DensityMeshResult:
        landscape = []
        species_wins = {'Alpha': 0, 'Beta': 0, 'Gamma': 0, 'Delta': 0}

        for n in range(1, 25):
            candidates = []

            v_a = self._species_alpha(nums, n)
            if v_a:
                candidates.append(('Alpha', v_a))

            v_b = self._species_beta(problem_id, nums, n)
            if v_b:
                candidates.append(('Beta', v_b))

            v_c = self._species_gamma(text, n)
            candidates.append(('Gamma', v_c))

            v_d = self._species_delta(nums, n)
            candidates.append(('Delta', v_d))

            # Evaluate each species
            best_nrci = 0.0
            best_species = 'Gamma'
            best_friction = 999.0

            for species_name, vec in candidates:
                tax = float(LEECH_ENGINE.calculate_symmetry_tax(vec))
                nrci = float(Fraction(10, 1) / (Fraction(10, 1) + Fraction(tax).limit_denominator(1000)))
                snapped, snap_info = GOLAY_ENGINE.snap_to_codeword(vec)
                sw = snap_info.get('syndrome_weight', 0)
                friction = sw / (nrci if nrci > 0 else 1.0)
                score = nrci - (friction * 0.05)
                if score > (best_nrci - best_friction * 0.05):
                    best_nrci = nrci
                    best_species = species_name
                    best_friction = friction

            species_wins[best_species] += 1
            landscape.append({
                'n': n,
                'nrci': best_nrci,
                'friction': best_friction,
                'species': best_species
            })

        # Find peaks: NRCI > 0.80 and friction < 2.0
        peaks = [p for p in landscape if p['nrci'] > 0.80 and p['friction'] < 2.0]

        # Dominant species
        dominant = max(species_wins, key=lambda k: species_wins[k])

        # Peak summary (UBP-native language)
        if peaks:
            peak_ns = [p['n'] for p in peaks]
            peak_summary = (
                f"Natural stability peaks at n={peak_ns} via {dominant} metabolism. "
                f"Peak NRCI: {max(p['nrci'] for p in peaks):.4f}. "
                f"This indicates the UBP substrate resonates at these harmonic positions."
            )
        else:
            peak_summary = (
                f"No natural peaks found (threshold NRCI>0.80). "
                f"Dominant species: {dominant}. "
                f"The substrate is in a diffuse, non-localised state for this problem."
            )

        return DensityMeshResult(
            peaks=peaks,
            dominant_species=dominant,
            landscape=landscape,
            peak_summary=peak_summary
        )

# ─── AGENT 4: SEMANTIC RESONATOR ─────────────────────────────────────────────

class SemanticResonator:
    """
    Finds the governing UBP Law by cosine similarity search over the KB.
    Self-discovered role: identify which UBP law governs this problem's geometry.
    """
    def __init__(self, semantic: UBPSemanticEngine):
        self.semantic = semantic

    def find_law(self, vector: List[int]) -> SemanticColumn:
        bipolar = [(b * 2) - 1 for b in vector]
        best_law = "UNKNOWN"
        best_sim = -1.0
        top_neighbours = []

        for uid, kvec in self.semantic._system_vectors.items():
            if len(kvec) != len(bipolar):
                continue
            dot = sum(a * b for a, b in zip(bipolar, kvec))
            m1 = sum(a**2 for a in bipolar) ** 0.5
            m2 = sum(b**2 for b in kvec) ** 0.5
            sim = dot / (m1 * m2) if m1 * m2 > 0 else 0.0

            if sim > 0.35:
                top_neighbours.append((uid, sim))

            if sim > best_sim and uid.startswith("LAW_"):
                best_sim = sim
                best_law = uid

        top_neighbours.sort(key=lambda x: x[1], reverse=True)
        top_3 = top_neighbours[:3]

        # Get law definition from KB
        law_def = "Definition not found."
        entry = self.semantic.all_kb.get(best_law)
        if entry:
            law_def = entry.get('lexicon', 'Definition missing.')[:200]

        return SemanticColumn(
            governing_law=best_law,
            law_resonance=best_sim,
            law_definition=law_def,
            top_neighbours=top_3
        )

# ─── AGENT 5: MOE SYNTHESIST ──────────────────────────────────────────────────

class MoeSynthesist:
    """
    Generates UBP-native language from topological neighbours.
    Uses the MoE Cortex N-gram engine — no external LLM.
    Self-discovered role: translate geometric findings into UBP substrate language.
    The output is intentionally cryptic — it reflects the substrate's own logic.
    NOTE: Accepts a pre-trained MoE instance to avoid re-training on every problem.
    """
    def __init__(self, moe: UBPMoECortexV2):
        self.moe = moe

    def synthesise(self, semantic_col: SemanticColumn, domain: str,
                   peaks: List[Dict]) -> LanguageColumn:
        # Build probe from governing law + top neighbours
        law_short = semantic_col.governing_law.replace("LAW_", "").replace("_001", "").lower()
        neighbour_words = [n[0].replace("LAW_", "").replace("_001", "").lower()
                          for n in semantic_col.top_neighbours[:2]]
        probe = f"{domain.lower()} {law_short} {' '.join(neighbour_words)}"

        synthesis = ""
        try:
            synthesis = self.moe.research(probe, max_words=12)
        except Exception as e:
            synthesis = f"[MoE synthesis unavailable: {e}]"

        # TCT alignment: average NRCI of top neighbours
        if semantic_col.top_neighbours:
            avg_resonance = sum(r for _, r in semantic_col.top_neighbours) / len(semantic_col.top_neighbours)
        else:
            avg_resonance = 0.0

        return LanguageColumn(
            moe_synthesis=synthesis,
            synthesis_probe=probe,
            tct_alignment=avg_resonance
        )

# ─── AGENT 6: TCT AUDITOR ────────────────────────────────────────────────────

class TCTAuditor:
    """
    Checks cross-column alignment and accepts/rejects each TCT step.
    Self-discovered role: quality gate — only accept steps where the three
    columns (Math, Sovereign, Language) are genuinely aligned.
    """
    def __init__(self):
        self.tgic = TGICExactEngine()

    def audit(self, math_col: MathColumn, sov_col: SovereignColumn,
              lang_col: LanguageColumn) -> Tuple[bool, float, List[str]]:
        notes = []

        # Check 1: NRCI threshold
        nrci_pass = math_col.nrci >= 0.60
        notes.append(f"{'PASS' if nrci_pass else 'FAIL'}: NRCI={math_col.nrci:.4f} (threshold 0.60)")

        # Check 2: Observer manifestation
        manifest_pass = sov_col.manifestation in ('MANIFESTED', 'SUBLIMINAL')
        notes.append(f"{'PASS' if manifest_pass else 'FAIL'}: Observer={sov_col.manifestation}")

        # Check 3: TCT alignment
        align_pass = lang_col.tct_alignment >= 0.40
        notes.append(f"{'PASS' if align_pass else 'FAIL'}: TCT_alignment={lang_col.tct_alignment:.4f}")

        # Check 4: TGIC relational energy
        try:
            ob = OffBit(tuple(math_col.vector), 0)
            S = {'math': ob}
            energy = float(self.tgic.get_total_energy(S))
            tgic_pass = energy < 500.0
            notes.append(f"{'PASS' if tgic_pass else 'FAIL'}: TGIC_energy={energy:.2f}")
        except Exception as e:
            tgic_pass = False
            notes.append(f"FAIL: TGIC error: {e}")

        # Check 5: Shadow drift (noumenal coherence)
        shadow_sum = sum(sov_col.shadow_bits)
        drift = abs(6 - shadow_sum)  # ideal: 6 ones in first 12 bits
        drift_pass = drift <= 4
        notes.append(f"{'PASS' if drift_pass else 'FAIL'}: Shadow_drift={drift} (ideal=0)")

        # Overall alignment score
        passes = [nrci_pass, manifest_pass, align_pass, tgic_pass, drift_pass]
        alignment = sum(passes) / len(passes)
        accepted = alignment >= 0.60  # 3/5 checks must pass

        if accepted:
            notes.append(f"AUTO-SNAP: Accepted (alignment={alignment:.2f})")
        else:
            notes.append(f"REJECTED: Insufficient alignment ({alignment:.2f})")

        return accepted, alignment, notes

# ─── AGENT 7: ONTOLOGICAL HARVESTER ──────────────────────────────────────────

class OntologicalHarvester:
    """
    Stores accepted TCT steps in the learning KB.
    Self-discovered role: accumulate knowledge from successful substrate mappings.
    """
    @staticmethod
    def harvest(steps: List[TCTStep]) -> int:
        os.makedirs(os.path.dirname(LEARNING_FILE), exist_ok=True)

        if os.path.exists(LEARNING_FILE):
            with open(LEARNING_FILE, 'r') as f:
                learned_kb = json.load(f)
        else:
            learned_kb = {
                "_fields": ["ubp_id", "lexicon", "tags", "vector", "nrci_val"],
                "entries": {}
            }

        new_count = 0
        for step in steps:
            if step.accepted:
                uid = f"LEARNED_{step.problem_id}_{step.domain[:3].upper()}"
                fp = hashlib.sha256(str(step.math.vector).encode()).hexdigest()
                if fp not in learned_kb["entries"]:
                    entry = [
                        uid,
                        f"[{step.domain}] {step.semantic.governing_law}: {step.density.peak_summary[:120]}",
                        ["LEARNED", "MATHNET", "PURE_SWARM", datetime.now().strftime("%Y-%m-%d")],
                        step.math.vector,
                        round(step.math.nrci, 8)
                    ]
                    learned_kb["entries"][fp] = entry
                    new_count += 1

        if new_count > 0:
            with open(LEARNING_FILE, 'w') as f:
                json.dump(learned_kb, f, indent=2)

        return new_count

# ─── AGENT 8: SHADOW LENS ────────────────────────────────────────────────────

class ShadowLens:
    """
    Background observer tracking noumenal drift across all problems.
    Self-discovered role: monitor the aggregate coherence of the substrate.
    The shadow is the unmanifested half of the 24-bit vector.
    """
    def __init__(self):
        self.observations = []
        self.total_drift = 0.0

    def observe(self, problem_id: str, shadow_bits: List[int]):
        drift = abs(6 - sum(shadow_bits))
        self.total_drift += drift
        self.observations.append({
            'problem_id': problem_id,
            'shadow_sum': sum(shadow_bits),
            'drift': drift
        })

    def get_report(self) -> Dict:
        if not self.observations:
            return {"status": "No observations"}
        avg_drift = self.total_drift / len(self.observations)
        min_drift = min(o['drift'] for o in self.observations)
        max_drift = max(o['drift'] for o in self.observations)
        most_coherent = min(self.observations, key=lambda o: o['drift'])
        return {
            "total_observations": len(self.observations),
            "avg_noumenal_drift": avg_drift,
            "min_drift": min_drift,
            "max_drift": max_drift,
            "most_coherent_problem": most_coherent['problem_id'],
            "interpretation": (
                "Low drift indicates the substrate is near its ideal 6/12 shadow balance. "
                "This is a measure of noumenal coherence, not mathematical correctness."
            )
        }

# ─── DIRECTOR: REPORT SYNTHESISER ────────────────────────────────────────────

class Director:
    """Synthesises the final investigation report from all TCT steps."""

    def synthesise(self, steps: List[TCTStep], shadow_report: Dict,
                   learned_count: int) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accepted = [s for s in steps if s.accepted]

        md = "# UBP Swarm TCT v4.0 — MathNet Investigation Report\n\n"
        md += f"**Generated:** {timestamp}  \n"
        md += f"**Mode:** Pure UBP Substrate — No External LLMs  \n"
        md += f"**Problems processed:** {len(steps)}  \n"
        md += f"**Steps accepted:** {len(accepted)}/{len(steps)}  \n"
        md += f"**Concepts harvested:** {learned_count}  \n\n"

        md += "> **Important:** This system does not solve mathematical problems. "
        md += "It maps each problem's numerical structure to the 24-dimensional Leech Lattice "
        md += "and reports the resulting UBP substrate signature. The outputs are "
        md += "topological readings, not mathematical proofs.\n\n"

        md += "---\n\n"

        # Per-domain summary
        domains = {}
        for step in steps:
            if step.domain not in domains:
                domains[step.domain] = []
            domains[step.domain].append(step)

        md += "## Domain Summary\n\n"
        md += "| Domain | Problems | Accepted | Avg NRCI | Dominant Law |\n"
        md += "|--------|----------|----------|----------|--------------|\n"
        for domain, domain_steps in domains.items():
            avg_nrci = sum(s.math.nrci for s in domain_steps) / len(domain_steps)
            acc = sum(1 for s in domain_steps if s.accepted)
            # Find most common law
            laws = [s.semantic.governing_law for s in domain_steps]
            dominant_law = max(set(laws), key=laws.count)
            md += f"| {domain} | {len(domain_steps)} | {acc} | {avg_nrci:.4f} | `{dominant_law}` |\n"
        md += "\n"

        # Per-problem detail
        md += "## Problem-by-Problem Substrate Mappings\n\n"
        for step in steps:
            status_icon = "✓" if step.accepted else "○"
            md += f"### {status_icon} {step.problem_id} ({step.domain})\n\n"

            md += "**Mathematical Structure:**\n"
            md += f"- Key numbers: `{step.math.key_numbers}`\n"
            md += f"- Platform: `{step.math.platform}` | NRCI: `{step.math.nrci:.4f}`\n"
            md += f"- Math DNA: `{step.math.math_dna}` | Syndrome weight: `{step.math.syndrome_weight}`\n\n"

            md += "**Sovereign Physics:**\n"
            md += f"- Golay address: `{step.sovereign.golay_address}` | Correctable: `{step.sovereign.correctable}`\n"
            md += f"- Octad similarity: `{step.sovereign.octad_similarity:.4f}` (octad #{step.sovereign.octad_index})\n"
            md += f"- Observer status: `{step.sovereign.manifestation}` | SOC energy: `{step.sovereign.soc_energy:,.0f} CU`\n"
            md += f"- Shadow bits (noumenal): `{step.sovereign.shadow_bits}` (sum={sum(step.sovereign.shadow_bits)})\n"
            if not step.sovereign.correctable:
                md += f"  - *Note: Vector is beyond Golay correction radius (syndrome weight > 3). "
                md += f"This is an honest finding — the problem's numerical encoding does not naturally lie on the Golay code.*\n"
            md += "\n"

            md += "**Density Mesh Scan:**\n"
            if step.density.peaks:
                md += f"- Stability peaks at n={[p['n'] for p in step.density.peaks]}\n"
                md += f"- Dominant species: `{step.density.dominant_species}`\n"
            else:
                md += f"- No peaks found (diffuse state)\n"
                md += f"- Dominant species: `{step.density.dominant_species}`\n"
            md += f"- *{step.density.peak_summary}*\n\n"

            md += "**Semantic Resonance:**\n"
            md += f"- Governing law: `{step.semantic.governing_law}` (resonance: {step.semantic.law_resonance:.4f})\n"
            md += f"- Definition: *{step.semantic.law_definition[:120]}...*\n"
            if step.semantic.top_neighbours:
                nb_str = ", ".join(f"`{uid}` ({sim:.3f})" for uid, sim in step.semantic.top_neighbours)
                md += f"- Topological neighbours: {nb_str}\n\n"
            else:
                md += f"- No strong topological neighbours found\n\n"

            md += "**MoE Substrate Language:**\n"
            md += f"- Probe: `{step.language.synthesis_probe}`\n"
            md += f"- Synthesis: *\"{step.language.moe_synthesis}\"*\n"
            md += f"- TCT alignment: `{step.language.tct_alignment:.4f}`\n\n"

            md += "**TCT Audit:**\n"
            for note in step.audit_notes:
                md += f"- {note}\n"
            md += f"- **Overall alignment: {step.alignment_score:.2f}** ({'ACCEPTED' if step.accepted else 'REJECTED'})\n\n"
            md += "---\n\n"

        # Shadow Lens report
        md += "## Shadow Lens: Noumenal Coherence Report\n\n"
        md += "> *The Shadow Lens tracks the noumenal (unmanifested) half of each 24-bit vector. "
        md += "Drift from the ideal 6/12 balance is a measure of substrate coherence.*\n\n"
        for key, val in shadow_report.items():
            md += f"- **{key}:** {val}\n"
        md += "\n"

        return md

# ─── MAIN ORCHESTRATOR ───────────────────────────────────────────────────────

class UBPSwarmMathNetV4:
    """
    The main orchestrator for the UBP × MathNet v4.0 investigation.
    Runs all 8 agents in sequence for each problem, then synthesises the report.
    """

    def __init__(self):
        logger.info("Initialising UBP Swarm v4.0 — Pure Substrate Mode")

        # Load semantic engine once (shared)
        self.semantic = UBPSemanticEngine()
        self.semantic.load(
            os.path.join(CORE_DIR, 'ubp_system_kb.json'),
            os.path.join(CORE_DIR, 'ubp_lang_kb_combined_v4.json')
        )
        logger.info(f"Semantic KB: {len(self.semantic.all_kb)} entries loaded")

        # Initialise all agents
        self.math_architect = MathArchitect()
        self.sovereign = SovereignPhysicist()
        self.density_scanner = DensityMeshScanner()
        self.semantic_resonator = SemanticResonator(self.semantic)
        # Pre-train MoE once (2M iterations) — shared across all problems
        logger.info("Pre-training MoE Cortex N-gram linguist (this takes ~30s)...")
        self._moe = UBPMoECortexV2()
        logger.info("MoE Cortex ready")
        self.moe_synthesist = MoeSynthesist(self._moe)
        self.auditor = TCTAuditor()
        self.shadow_lens = ShadowLens()
        self.director = Director()

        logger.info("All 8 agents initialised — swarm ready")

    def process_problem(self, problem: Dict) -> TCTStep:
        pid = problem.get('id', 'UNKNOWN')
        domain = problem.get('domain', 'General')
        text = problem.get('problem', '')

        logger.info(f"Processing {pid} [{domain}]")

        # Column 1: Math Architect
        math_col = self.math_architect.build(pid, domain, text)
        logger.info(f"  Math: NRCI={math_col.nrci:.4f}, platform={math_col.platform}, "
                    f"nums={math_col.key_numbers[:4]}")

        # Column 2: Sovereign Physicist
        sov_col = self.sovereign.prove(math_col)
        logger.info(f"  Sovereign: addr={sov_col.golay_address}, "
                    f"manifestation={sov_col.manifestation}")

        # Column 3: Density Mesh Scanner
        density_col = self.density_scanner.scan(pid, text, math_col.key_numbers)
        peak_ns = [p['n'] for p in density_col.peaks]
        logger.info(f"  Density: peaks={peak_ns}, dominant={density_col.dominant_species}")

        # Column 4: Semantic Resonator
        semantic_col = self.semantic_resonator.find_law(sov_col.snapped_vector)
        logger.info(f"  Semantic: law={semantic_col.governing_law}, "
                    f"resonance={semantic_col.law_resonance:.4f}")

        # Column 5: MoE Synthesist
        lang_col = self.moe_synthesist.synthesise(semantic_col, domain, density_col.peaks)
        logger.info(f"  Language: probe='{lang_col.synthesis_probe}', "
                    f"alignment={lang_col.tct_alignment:.4f}")

        # Shadow Lens observation
        self.shadow_lens.observe(pid, sov_col.shadow_bits)

        # TCT Audit
        accepted, alignment, notes = self.auditor.audit(math_col, sov_col, lang_col)
        logger.info(f"  Audit: {'ACCEPTED' if accepted else 'REJECTED'} (alignment={alignment:.2f})")

        return TCTStep(
            step_id=f"step_{pid}",
            problem_id=pid,
            domain=domain,
            math=math_col,
            sovereign=sov_col,
            density=density_col,
            semantic=semantic_col,
            language=lang_col,
            accepted=accepted,
            alignment_score=alignment,
            audit_notes=notes
        )

    def run(self, problem_set_path: str, output_dir: str):
        # Load problems
        with open(problem_set_path, 'r') as f:
            raw = json.load(f)
        problems = raw.get('problems', raw) if isinstance(raw, dict) else raw
        logger.info(f"Loaded {len(problems)} problems from {problem_set_path}")

        # Process all problems
        steps = []
        for i, prob in enumerate(problems):
            logger.info(f"\n{'='*60}")
            logger.info(f"PROBLEM {i+1}/{len(problems)}")
            logger.info(f"{'='*60}")
            step = self.process_problem(prob)
            steps.append(step)

        # Ontological harvesting
        learned_count = OntologicalHarvester.harvest(steps)
        logger.info(f"\nHarvested {learned_count} new concepts to learning KB")

        # Shadow Lens report
        shadow_report = self.shadow_lens.get_report()

        # Generate report
        report_md = self.director.synthesise(steps, shadow_report, learned_count)

        # Save outputs
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_path = os.path.join(output_dir, f"ubp_mathnet_v4_report_{timestamp}.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)

        results_path = os.path.join(output_dir, f"ubp_mathnet_v4_results_{timestamp}.json")
        results_data = {
            "version": "4.0",
            "timestamp": timestamp,
            "mode": "pure_ubp_substrate",
            "external_llm": False,
            "numpy_used": False,
            "problems_processed": len(steps),
            "steps_accepted": sum(1 for s in steps if s.accepted),
            "learned_concepts": learned_count,
            "shadow_report": shadow_report,
            "steps": [asdict(s) for s in steps]
        }
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)

        logger.info(f"\n{'='*60}")
        logger.info(f"UBP SWARM v4.0 COMPLETE")
        logger.info(f"  Report: {report_path}")
        logger.info(f"  Results: {results_path}")
        logger.info(f"  Accepted: {sum(1 for s in steps if s.accepted)}/{len(steps)}")
        logger.info(f"  Learned: {learned_count} concepts")
        logger.info(f"  Shadow drift: {shadow_report.get('avg_noumenal_drift', 0):.2f}")
        logger.info(f"{'='*60}")

        return steps, report_path, results_path


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="UBP Swarm TCT v4.0 — MathNet Investigation")
    parser.add_argument("--problems", default="../data/ubp_mathnet_problem_set.json",
                        help="Path to problem set JSON")
    parser.add_argument("--output", default="../results",
                        help="Output directory for results")
    args = parser.parse_args()

    swarm = UBPSwarmMathNetV4()
    swarm.run(args.problems, args.output)
