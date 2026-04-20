"""
================================================================================
UBP SWARM ORCHESTRATOR v3.0 (Grand-Scale Document Synthesis)
================================================================================
Author: Manus (UBP Research Cortex v6.0)
Date: 20 April 2026

ARCHITECTURE OVERVIEW
---------------------
This version implements a full multi-tier swarm with up to 30+ agents operating
in a hierarchical, iterative pipeline. The key innovations over v2 are:

1. SHARED CORTEX: All agents share a single pre-trained MoE instance to avoid
   repeated training overhead.

2. FIVE AGENT TIERS:
   - Tier 0: DIRECTOR (1 agent) - Parses directive, creates master outline.
   - Tier 1: SECTION ARCHITECTS (N agents) - Each designs a section's paragraph plan.
   - Tier 2: WRITERS (N*M agents) - Each writes a paragraph draft.
   - Tier 3: CRITICS (N*M agents) - Each evaluates a draft on NRCI + Resonance.
   - Tier 4: EDITORS (N agents) - Each synthesizes a section's paragraphs.

3. DUAL SCORING: Every draft is evaluated on:
   - Geometric Stability (NRCI >= threshold)
   - Semantic Resonance (Cosine similarity to section topic >= threshold)

4. ADAPTIVE FEEDBACK: Critics pass specific feedback tokens back to Writers.
   The Writer's next attempt incorporates the feedback as a modified objective.

5. DOCUMENT COHERENCE TRACKING: A running macro-document Golay vector is
   maintained. Each accepted paragraph is XOR-bridged into the macro vector,
   and the macro NRCI is tracked across the entire document.

6. MULTI-TOPIC SUPPORT: Can run across different directives in one session,
   reusing the trained cortex.

7. COMPREHENSIVE LOGGING: Full per-agent, per-attempt, per-paragraph logs.
================================================================================
"""

import argparse
import json
import math
import os
import random
import re
import sys
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core import GOLAY_ENGINE, LEECH_ENGINE
from ubp_moe_cortex_v2 import UBPMoECortexV2
from ubp_semantic_engine import UBPSemanticEngine

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_KB_PATH = Path(os.environ.get('UBP_SYSTEM_KB_PATH', BASE_DIR / 'ubp_system_kb.json'))
LANG_KB_PATH = Path(os.environ.get('UBP_LANG_KB_PATH', BASE_DIR / 'ubp_lang_kb_combined_v4.json'))


# ==============================================================================
# GEOMETRY UTILITIES
# ==============================================================================

def text_to_vector(text: str, semantic_engine: UBPSemanticEngine) -> List[int]:
    """Converts a block of text into a single 24-bit Golay codeword."""
    words = re.sub(r'[^a-z0-9 ]', '', text.lower()).split()
    vec_sum = [0.0] * 24
    count = 0
    for word in words:
        if len(word) < 3:
            continue
        res = semantic_engine.query(word, top_k=1)
        if res and res[0].resonance_score > 0.3:
            uid = res[0].ubp_id
            vector = semantic_engine.all_kb.get(uid, {}).get('vector')
            if vector:
                for i in range(24):
                    vec_sum[i] += vector[i]
                count += 1
    if count == 0:
        return [0] * 24
    bin_vec = [1 if x > (count / 2) else 0 for x in vec_sum]
    snapped, _, _ = GOLAY_ENGINE.decode(bin_vec)
    return GOLAY_ENGINE.encode(snapped)


def vector_nrci(vec: List[int]) -> float:
    """Calculates NRCI from a 24-bit vector."""
    snapped, _, _ = GOLAY_ENGINE.decode(vec)
    stable = GOLAY_ENGINE.encode(snapped)
    tax = LEECH_ENGINE.calculate_symmetry_tax(stable)
    return float(Fraction(10, 1) / (Fraction(10, 1) + tax))


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = sum(a ** 2 for a in v1) ** 0.5
    mag2 = sum(b ** 2 for b in v2) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def semantic_resonance(text: str, target: str, semantic_engine: UBPSemanticEngine) -> float:
    """Cosine resonance between text and target in the Golay space."""
    tv = text_to_vector(text, semantic_engine)
    rv = text_to_vector(target, semantic_engine)
    bipolar_tv = [(b * 2) - 1 for b in tv]
    bipolar_rv = [(b * 2) - 1 for b in rv]
    return cosine_similarity(bipolar_tv, bipolar_rv)


def xor_bridge(doc_vec: List[int], draft_vec: List[int]) -> Tuple[List[int], float]:
    """XOR bridge two vectors and return the stable result and its NRCI."""
    combined = [a ^ b for a, b in zip(doc_vec, draft_vec)]
    snapped, _, _ = GOLAY_ENGINE.decode(combined)
    stable = GOLAY_ENGINE.encode(snapped)
    tax = LEECH_ENGINE.calculate_symmetry_tax(stable)
    nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
    return stable, nrci


# ==============================================================================
# AGENT DEFINITIONS
# ==============================================================================

class BaseAgent:
    def __init__(self, agent_id: int, tier: int, role: str,
                 moe: UBPMoECortexV2, semantic: UBPSemanticEngine):
        self.agent_id = agent_id
        self.tier = tier
        self.role = role
        self.moe = moe
        self.semantic = semantic
        self.log: List[Dict] = []

    def _tag(self) -> str:
        return f"[T{self.tier}|A{self.agent_id:03d}|{self.role}]"


class DirectorAgent(BaseAgent):
    """Tier 0: Parses the main directive and creates the master outline."""

    def create_outline(self, directive: str, num_sections: int,
                       paragraphs_per_section: int) -> List[Dict]:
        print(f"\n{self._tag()} Creating master outline for: '{directive}'")

        # Query semantic engine for top-level section topics
        section_results = self.semantic.query(directive, top_k=num_sections * 3)
        section_topics = []
        seen = set()
        for r in section_results:
            raw = r.lexicon.split(']')[0]
            for prefix in ['[Word: ', '[Operator: ', '[Law: ', '[Element: ', '[Molecule: ', '[']:
                raw = raw.replace(prefix, '')
            topic = raw.strip().rstrip(']')
            if topic and topic not in seen:
                section_topics.append((topic, r.resonance_score))
                seen.add(topic)

        if not section_topics:
            section_topics = [(directive, 1.0)] * num_sections

        # Build outline
        outline = []
        roles_cycle = ["PHYSICIST", "LOGICIAN", "GEOMETRICIAN", "SEMANTICIST",
                       "OBSERVER", "ANALYST", "SYNTHESIST"]

        for s_idx in range(num_sections):
            s_topic, s_score = section_topics[s_idx % len(section_topics)]

            # Query for paragraph sub-topics within this section
            para_results = self.semantic.query(s_topic, top_k=paragraphs_per_section * 2)
            para_topics = []
            para_seen = set()
            for r in para_results:
                raw = r.lexicon.split(']')[0]
                for prefix in ['[Word: ', '[Operator: ', '[Law: ', '[Element: ', '[Molecule: ', '[']:
                    raw = raw.replace(prefix, '')
                pt = raw.strip().rstrip(']')
                if pt and pt not in para_seen and pt != s_topic:
                    para_topics.append(pt)
                    para_seen.add(pt)

            if not para_topics:
                para_topics = [f"{s_topic} aspect {p+1}" for p in range(paragraphs_per_section)]

            paragraphs = []
            for p_idx in range(paragraphs_per_section):
                paragraphs.append({
                    'para_num': p_idx + 1,
                    'topic': para_topics[p_idx % len(para_topics)],
                    'role': roles_cycle[(s_idx * paragraphs_per_section + p_idx) % len(roles_cycle)],
                })

            outline.append({
                'section_num': s_idx + 1,
                'section_topic': s_topic,
                'section_resonance': s_score,
                'paragraphs': paragraphs,
            })

        print(f"{self._tag()} Outline created: {num_sections} sections, "
              f"{paragraphs_per_section} paragraphs each.")
        return outline


class SectionArchitectAgent(BaseAgent):
    """Tier 1: Refines the paragraph plan for a specific section."""

    def refine_plan(self, section: Dict, directive: str) -> Dict:
        print(f"\n{self._tag()} Refining plan for Section {section['section_num']}: "
              f"'{section['section_topic']}'")
        # Enrich paragraph topics with semantic context
        enriched_paragraphs = []
        for para in section['paragraphs']:
            # Query for the paragraph topic to get the best UBP anchor
            res = self.semantic.query(para['topic'], top_k=1)
            anchor_id = res[0].ubp_id if res else "UNKNOWN"
            anchor_nrci = res[0].nrci if res else 0.5
            enriched_paragraphs.append({
                **para,
                'anchor_id': anchor_id,
                'anchor_nrci': anchor_nrci,
                'directive': directive,
            })
        return {**section, 'paragraphs': enriched_paragraphs}


class WriterAgent(BaseAgent):
    """Tier 2: Generates paragraph drafts."""

    def draft(self, topic: str, directive: str, max_words: int,
              feedback: str = "", attempt: int = 1) -> str:
        # Build objective from topic + feedback
        if feedback:
            objective = f"{topic} {feedback}"
        else:
            objective = topic
        print(f"\n{self._tag()} Drafting '{topic}' | Attempt {attempt} | "
              f"Words: {max_words}")
        return self.moe.research(objective, max_words=max_words)


class CriticAgent(BaseAgent):
    """Tier 3: Evaluates drafts on NRCI and Semantic Resonance."""

    def evaluate(self, text: str, topic: str, directive: str,
                 min_nrci: float, min_resonance: float,
                 doc_vec: List[int]) -> Dict:
        # Paragraph-level NRCI
        para_vec = text_to_vector(text, self.semantic)
        para_nrci = vector_nrci(para_vec)

        # Semantic resonance against the paragraph topic
        topic_resonance = semantic_resonance(text, topic, self.semantic)

        # Semantic resonance against the main directive
        directive_resonance = semantic_resonance(text, directive, self.semantic)

        # Macro-document integration NRCI (how well this fits the running doc)
        _, macro_nrci = xor_bridge(doc_vec, para_vec)

        accepted = (para_nrci >= min_nrci and topic_resonance >= min_resonance)

        # Build targeted feedback
        feedback_tokens = []
        if para_nrci < min_nrci:
            feedback_tokens.append("stable")
        if topic_resonance < min_resonance:
            feedback_tokens.append(topic.split()[0] if topic else "relevant")
        feedback = " ".join(feedback_tokens) if feedback_tokens else ""

        result = {
            'accepted': accepted,
            'para_nrci': para_nrci,
            'topic_resonance': topic_resonance,
            'directive_resonance': directive_resonance,
            'macro_nrci': macro_nrci,
            'feedback': feedback,
        }

        status = "APPROVED" if accepted else "REJECTED"
        print(f"\n{self._tag()} {status} | "
              f"NRCI: {para_nrci:.4f} (>{min_nrci}) | "
              f"TopicRes: {topic_resonance:.4f} (>{min_resonance}) | "
              f"MacroNRCI: {macro_nrci:.4f}")
        return result


class EditorAgent(BaseAgent):
    """Tier 4: Synthesizes accepted paragraphs into a cohesive section."""

    def synthesize(self, section_num: int, section_topic: str,
                   paragraphs: List[Dict]) -> str:
        print(f"\n{self._tag()} Synthesizing Section {section_num}: '{section_topic}'")
        lines = [f"### Section {section_num}: {section_topic.title()}\n"]
        for p in paragraphs:
            role = p.get('role', 'AGENT')
            text = p.get('text', '')
            status = p.get('status', '')
            nrci = p.get('final_nrci', 0.0)
            res = p.get('final_resonance', 0.0)
            lines.append(f"**[{role}]** *(NRCI: {nrci:.4f} | Res: {res:.4f})*  ")
            lines.append(f"{text}{status}\n")
        return "\n".join(lines)


# ==============================================================================
# ORCHESTRATOR V3
# ==============================================================================

class UBPOrchestratorV3:
    """
    Grand-Scale UBP Swarm Orchestrator.
    
    Deploys a full multi-tier agent swarm to generate large, geometrically
    coherent, and semantically relevant documents from a given directive.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.agent_counter = 0
        self.all_agents: List[BaseAgent] = []

        print("[Orchestrator V3] Booting Semantic Engine...")
        self.semantic = UBPSemanticEngine()
        self.semantic.load(str(SYSTEM_KB_PATH), str(LANG_KB_PATH))

        print("[Orchestrator V3] Booting MoE Cortex (shared across all agents)...")
        self.moe = UBPMoECortexV2()

    def _new_agent(self, tier: int, role: str, AgentClass) -> BaseAgent:
        self.agent_counter += 1
        agent = AgentClass(self.agent_counter, tier, role, self.moe, self.semantic)
        self.all_agents.append(agent)
        return agent

    def run_pipeline(
        self,
        directive: str,
        num_sections: int = 4,
        paragraphs_per_section: int = 3,
        min_nrci: float = 0.65,
        min_resonance: float = 0.3,
        max_retries: int = 5,
        words_per_paragraph: int = 25,
        output_prefix: str = 'doc_v3',
        results_dir: str = '.',
    ) -> Dict:
        random.seed(self.seed)
        self.agent_counter = 0
        self.all_agents = []
        doc_vec = [0] * 24
        macro_nrci = 0.0
        all_sections_text = []
        full_log = []
        t_start = time.time()

        results_path = Path(results_dir)
        results_path.mkdir(parents=True, exist_ok=True)

        total_expected = 1 + num_sections + (num_sections * paragraphs_per_section * 2) + num_sections
        print(f"\n{'=' * 80}")
        print("UBP SWARM ORCHESTRATOR V3: GRAND-SCALE DOCUMENT SYNTHESIS")
        print(f"Directive: {directive.upper()}")
        print(f"Sections: {num_sections} | Paragraphs/Sec: {paragraphs_per_section}")
        print(f"Expected Agents: ~{total_expected}")
        print(f"NRCI: {min_nrci} | Resonance: {min_resonance} | Retries: {max_retries}")
        print(f"Words/Para: {words_per_paragraph} | Seed: {self.seed}")
        print(f"{'=' * 80}")

        # ---- TIER 0: DIRECTOR ----
        director = self._new_agent(0, "DIRECTOR", DirectorAgent)
        outline = director.create_outline(directive, num_sections, paragraphs_per_section)

        # ---- TIER 1: SECTION ARCHITECTS ----
        enriched_outline = []
        for section in outline:
            arch = self._new_agent(1, "SECTION-ARCHITECT", SectionArchitectAgent)
            enriched_section = arch.refine_plan(section, directive)
            enriched_outline.append(enriched_section)

        # ---- TIER 2+3: WRITERS & CRITICS (per paragraph) ----
        # ---- TIER 4: EDITORS (per section) ----
        for section in enriched_outline:
            s_num = section['section_num']
            s_topic = section['section_topic']
            section_para_logs = []

            print(f"\n{'─' * 60}")
            print(f"Processing Section {s_num}: '{s_topic}'")
            print(f"{'─' * 60}")

            for para_meta in section['paragraphs']:
                p_num = para_meta['para_num']
                p_topic = para_meta['topic']
                p_role = para_meta['role']

                writer = self._new_agent(2, f"WRITER-{p_role}", WriterAgent)
                critic = self._new_agent(3, f"CRITIC-{p_role}", CriticAgent)

                accepted = False
                attempts = 0
                feedback = ""
                final_text = ""
                final_eval = {}

                while not accepted and attempts < max_retries:
                    attempts += 1
                    word_budget = words_per_paragraph + (attempts - 1) * 3

                    # Writer drafts
                    draft = writer.draft(p_topic, directive, word_budget, feedback, attempts)

                    # Critic evaluates
                    eval_result = critic.evaluate(draft, p_topic, directive,
                                                  min_nrci, min_resonance, doc_vec)

                    if eval_result['accepted']:
                        accepted = True
                        final_text = draft
                        final_eval = eval_result
                        # Integrate into macro document vector
                        para_vec = text_to_vector(draft, self.semantic)
                        doc_vec, macro_nrci = xor_bridge(doc_vec, para_vec)
                        print(f"  -> Macro NRCI updated: {macro_nrci:.4f}")
                    else:
                        feedback = eval_result['feedback']

                status_tag = "" if accepted else " [UNSTABLE]"
                if not final_text:
                    final_text = draft
                    final_eval = eval_result

                para_log = {
                    'section': s_num,
                    'section_topic': s_topic,
                    'paragraph': p_num,
                    'topic': p_topic,
                    'role': p_role,
                    'writer_id': writer.agent_id,
                    'critic_id': critic.agent_id,
                    'accepted': accepted,
                    'attempts': attempts,
                    'final_nrci': final_eval.get('para_nrci', 0.0),
                    'final_resonance': final_eval.get('topic_resonance', 0.0),
                    'directive_resonance': final_eval.get('directive_resonance', 0.0),
                    'macro_nrci_after': macro_nrci,
                    'text': final_text,
                    'status': status_tag,
                }
                section_para_logs.append(para_log)
                full_log.append(para_log)

            # Editor synthesizes the section
            editor = self._new_agent(4, "EDITOR", EditorAgent)
            section_text = editor.synthesize(s_num, s_topic, section_para_logs)
            all_sections_text.append(section_text)

        t_elapsed = time.time() - t_start
        total_words = sum(len(p['text'].split()) for p in full_log)
        accepted_count = sum(1 for p in full_log if p['accepted'])
        total_para = len(full_log)

        # ---- FINAL DOCUMENT ASSEMBLY ----
        final_doc = f"# UBP Macro-Document: {directive}\n\n"
        final_doc += f"| Metric | Value |\n"
        final_doc += f"|--------|-------|\n"
        final_doc += f"| Final Macro NRCI | {macro_nrci:.6f} |\n"
        final_doc += f"| Total Agents Deployed | {self.agent_counter} |\n"
        final_doc += f"| Total Paragraphs | {total_para} |\n"
        final_doc += f"| Accepted Paragraphs | {accepted_count}/{total_para} |\n"
        final_doc += f"| Total Words Generated | {total_words} |\n"
        final_doc += f"| Elapsed Time | {t_elapsed:.1f}s |\n"
        final_doc += f"| Seed | {self.seed} |\n\n"
        final_doc += "---\n\n"
        final_doc += "\n\n".join(all_sections_text)

        md_path = results_path / f"{output_prefix}.md"
        json_path = results_path / f"{output_prefix}.json"
        md_path.write_text(final_doc, encoding='utf-8')

        result = {
            'directive': directive,
            'seed': self.seed,
            'num_sections': num_sections,
            'paragraphs_per_section': paragraphs_per_section,
            'total_agents': self.agent_counter,
            'min_nrci': min_nrci,
            'min_resonance': min_resonance,
            'max_retries': max_retries,
            'words_per_paragraph': words_per_paragraph,
            'final_macro_nrci': macro_nrci,
            'total_paragraphs': total_para,
            'accepted_paragraphs': accepted_count,
            'total_words': total_words,
            'elapsed_seconds': t_elapsed,
            'outline': enriched_outline,
            'paragraphs': full_log,
        }
        json_path.write_text(json.dumps(result, indent=2), encoding='utf-8')

        print(f"\n{'=' * 80}")
        print("ORCHESTRATION COMPLETE")
        print(f"  Directive:          {directive}")
        print(f"  Total Agents:       {self.agent_counter}")
        print(f"  Total Paragraphs:   {total_para} ({accepted_count} accepted)")
        print(f"  Total Words:        {total_words}")
        print(f"  Final Macro NRCI:   {macro_nrci:.6f}")
        print(f"  Elapsed:            {t_elapsed:.1f}s")
        print(f"  Saved to:           {md_path}")
        print(f"{'=' * 80}\n")
        return result


# ==============================================================================
# EXPERIMENT RUNNER
# ==============================================================================

def run_experiments(orchestrator: UBPOrchestratorV3, configs: List[Dict],
                    results_dir: str = 'results_v3') -> List[Dict]:
    """Runs a batch of experiments using a shared orchestrator."""
    summary = []
    for cfg in configs:
        print(f"\n{'#' * 80}")
        print(f"EXPERIMENT: {cfg['name']}")
        print(f"{'#' * 80}")
        result = orchestrator.run_pipeline(
            directive=cfg['directive'],
            num_sections=cfg.get('num_sections', 3),
            paragraphs_per_section=cfg.get('paragraphs_per_section', 2),
            min_nrci=cfg.get('min_nrci', 0.65),
            min_resonance=cfg.get('min_resonance', 0.3),
            max_retries=cfg.get('max_retries', 4),
            words_per_paragraph=cfg.get('words_per_paragraph', 20),
            output_prefix=cfg['name'],
            results_dir=results_dir,
        )
        summary.append({
            'name': cfg['name'],
            'directive': cfg['directive'],
            'total_agents': result['total_agents'],
            'total_paragraphs': result['total_paragraphs'],
            'accepted_paragraphs': result['accepted_paragraphs'],
            'total_words': result['total_words'],
            'final_macro_nrci': result['final_macro_nrci'],
            'elapsed_seconds': result['elapsed_seconds'],
        })
    return summary


# ==============================================================================
# CLI
# ==============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='UBP Swarm Orchestrator V3 — Grand-Scale Document Synthesis')
    sub = parser.add_subparsers(dest='mode')

    # Single run
    single = sub.add_parser('run', help='Run a single directive')
    single.add_argument('--directive', required=True)
    single.add_argument('--sections', type=int, default=4)
    single.add_argument('--paragraphs', type=int, default=3)
    single.add_argument('--min-nrci', type=float, default=0.65)
    single.add_argument('--min-resonance', type=float, default=0.3)
    single.add_argument('--max-retries', type=int, default=5)
    single.add_argument('--words', type=int, default=25)
    single.add_argument('--seed', type=int, default=42)
    single.add_argument('--output-prefix', default='doc_v3')
    single.add_argument('--results-dir', default='results_v3')

    # Batch experiments
    batch = sub.add_parser('batch', help='Run a batch of experiments from a JSON config')
    batch.add_argument('--config', required=True, help='Path to JSON experiment config')
    batch.add_argument('--seed', type=int, default=42)
    batch.add_argument('--results-dir', default='results_v3')

    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == 'run':
        orch = UBPOrchestratorV3(seed=args.seed)
        orch.run_pipeline(
            directive=args.directive,
            num_sections=args.sections,
            paragraphs_per_section=args.paragraphs,
            min_nrci=args.min_nrci,
            min_resonance=args.min_resonance,
            max_retries=args.max_retries,
            words_per_paragraph=args.words,
            output_prefix=args.output_prefix,
            results_dir=args.results_dir,
        )
    elif args.mode == 'batch':
        with open(args.config, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        orch = UBPOrchestratorV3(seed=args.seed)
        summary = run_experiments(orch, configs, results_dir=args.results_dir)
        summary_path = Path(args.results_dir) / 'experiment_summary.json'
        Path(args.results_dir).mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
        print(json.dumps(summary, indent=2))
    else:
        parser.print_help()
