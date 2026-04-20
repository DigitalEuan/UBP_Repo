"""
================================================================================
UBP SWARM ORCHESTRATOR v1.1 (Macro-Scale Document Synthesis)
================================================================================
Author: UBP Research Cortex v5.0, repaired for reproducible local execution
Date: 20 April 2026

This pipeline orchestrates a swarm of mini-MoE agents to construct a
geometrically coherent macro-document. It fractures a main directive into
sub-topics, assigns them to different Agent Personas, and enforces a strict
Geometric Feedback Loop: if an agent's draft drops the document's running
NRCI below the threshold, the draft is rejected and the agent must retry.
================================================================================
"""

import argparse
import json
import os
import random
import re
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

from core import GOLAY_ENGINE, LEECH_ENGINE
from ubp_moe_cortex_v2 import UBPMoECortexV2
from ubp_semantic_engine import UBPSemanticEngine

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_KB_PATH = Path(os.environ.get('UBP_SYSTEM_KB_PATH', BASE_DIR / 'ubp_system_kb.json'))
LANG_KB_PATH = Path(os.environ.get('UBP_LANG_KB_PATH', BASE_DIR / 'ubp_lang_kb_combined_v4.json'))


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


class SwarmAgent:
    def __init__(self, agent_id: int, role: str, moe_cortex: UBPMoECortexV2):
        self.agent_id = agent_id
        self.role = role
        self.moe = moe_cortex

    def investigate(self, topic: str, max_words: int = 15) -> str:
        print(f"\n  [Agent {self.agent_id} : {self.role}] Investigating '{topic}'...")
        return self.moe.research(topic, max_words=max_words)


class UBPOrchestrator:
    def __init__(self, seed: int = 24):
        self.seed = seed
        random.seed(seed)

        print("[Orchestrator] Booting Semantic Engine...")
        self.semantic = UBPSemanticEngine()
        self.semantic.load(str(SYSTEM_KB_PATH), str(LANG_KB_PATH))

        print("[Orchestrator] Booting MoE Cortex (Training Linguist)...")
        self.moe = UBPMoECortexV2()

        self.document_vector = [0] * 24
        self.document_sections: List[str] = []
        self.run_log: List[Dict] = []

    def _extract_sub_topics(self, main_directive: str, num_agents: int) -> List[str]:
        base_res = self.semantic.query(main_directive, top_k=num_agents)
        sub_topics = []
        for result in base_res:
            clean_topic = (
                result.lexicon
                .split(']')[0]
                .replace('[Word: ', '')
                .replace('[Operator: ', '')
                .replace('[Law: ', '')
                .replace('[Element: ', '')
                .replace('[Molecule: ', '')
                .strip()
            )
            if clean_topic:
                sub_topics.append(clean_topic)
        if not sub_topics:
            sub_topics = [main_directive] * num_agents
        return sub_topics

    def run_pipeline(
        self,
        main_directive: str,
        num_agents: int = 3,
        min_nrci: float = 0.65,
        max_retries: int = 3,
        output_file: str = 'macro_document_output.md',
        output_json: str = 'macro_document_output.json',
        sub_topics_override: List[str] | None = None,
    ) -> Dict:
        random.seed(self.seed)
        self.document_vector = [0] * 24
        self.document_sections = []
        self.run_log = []

        print(f"\n{'=' * 80}")
        print("UBP SWARM ORCHESTRATOR: MACRO-DOCUMENT SYNTHESIS")
        print(f"Directive: {main_directive.upper()}")
        print(f"Agents: {num_agents} | Target NRCI: {min_nrci} | Max Retries: {max_retries} | Seed: {self.seed}")
        print(f"{'=' * 80}")

        sub_topics = sub_topics_override or self._extract_sub_topics(main_directive, num_agents)
        roles = ["PHYSICIST", "LOGICIAN", "GEOMETRICIAN", "SEMANTICIST", "OBSERVER"]
        final_nrci = 0.0

        for i in range(num_agents):
            topic = sub_topics[i % len(sub_topics)]
            role = roles[i % len(roles)]
            agent = SwarmAgent(i + 1, role, self.moe)

            accepted = False
            attempts = 0
            current_topic = topic
            final_text = ""
            final_attempt_nrci = 0.0

            while not accepted and attempts < max_retries:
                attempts += 1
                draft_text = agent.investigate(current_topic, max_words=12 + (attempts * 2))
                draft_vec = text_to_vector(draft_text, self.semantic)

                combined_vec = [a ^ b for a, b in zip(self.document_vector, draft_vec)]
                snapped_doc, _, _ = GOLAY_ENGINE.decode(combined_vec)
                stable_doc = GOLAY_ENGINE.encode(snapped_doc)

                tax = LEECH_ENGINE.calculate_symmetry_tax(stable_doc)
                nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
                final_attempt_nrci = nrci

                print(f"    -> Attempt {attempts} | Document NRCI: {nrci:.4f}")

                if nrci >= min_nrci:
                    print("    -> ACCEPTED. Appending to macro-document.")
                    self.document_vector = stable_doc
                    final_text = draft_text
                    accepted = True
                    final_nrci = nrci
                else:
                    print("    -> REJECTED. NRCI too low. Trying a different semantic path...")
                    current_topic = f"{topic} {role.lower()} perspective retry {attempts}"

            status_tag = "" if accepted else " (UNSTABLE - MAX RETRIES REACHED)"
            if not final_text:
                final_text = f"No stable draft accepted for topic '{topic}'. Last NRCI={final_attempt_nrci:.4f}."
            self.document_sections.append(
                f"### Section {i + 1}: {role} Perspective on '{topic}'{status_tag}\n{final_text}\n"
            )
            self.run_log.append(
                {
                    'section': i + 1,
                    'role': role,
                    'topic': topic,
                    'accepted': accepted,
                    'attempts': attempts,
                    'final_nrci': final_attempt_nrci,
                    'text': final_text,
                }
            )

        final_doc = f"# UBP Macro-Document: {main_directive}\n\n"
        final_doc += f"**Final Geometric Stability (NRCI):** {final_nrci:.4f}\n\n"
        final_doc += f"**Seed:** {self.seed}  \n"
        final_doc += f"**System KB:** {SYSTEM_KB_PATH.name}  \n"
        final_doc += f"**Language KB:** {LANG_KB_PATH.name}\n\n"
        final_doc += "---\n\n"
        final_doc += "\n".join(self.document_sections)

        output_path = Path(output_file)
        output_path.write_text(final_doc, encoding='utf-8')

        result = {
            'directive': main_directive,
            'seed': self.seed,
            'num_agents': num_agents,
            'min_nrci': min_nrci,
            'max_retries': max_retries,
            'final_nrci': final_nrci,
            'output_markdown': str(output_path),
            'sub_topics': sub_topics,
            'sub_topics_source': 'override' if sub_topics_override else 'semantic_query',
            'sections': self.run_log,
        }
        Path(output_json).write_text(json.dumps(result, indent=2), encoding='utf-8')

        print(f"\n{'=' * 80}")
        print("ORCHESTRATION COMPLETE")
        print(f"Final Document NRCI: {final_nrci:.4f}")
        print(f"Saved to: '{output_path}'")
        print(f"Metadata: '{output_json}'")
        print(f"{'=' * 80}\n")
        return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run the UBP swarm orchestrator reproducibly.')
    parser.add_argument('--directive', default='Thermodynamics of Hexadecad elements')
    parser.add_argument('--num-agents', type=int, default=3)
    parser.add_argument('--min-nrci', type=float, default=0.65)
    parser.add_argument('--max-retries', type=int, default=3)
    parser.add_argument('--seed', type=int, default=24)
    parser.add_argument('--output-file', default='macro_document_output.md')
    parser.add_argument('--output-json', default='macro_document_output.json')
    parser.add_argument('--subtopics-file', default='')
    return parser


if __name__ == '__main__':
    args = build_parser().parse_args()
    sub_topics_override = None
    if args.subtopics_file:
        subtopics_path = Path(args.subtopics_file)
        if subtopics_path.exists():
            if subtopics_path.suffix.lower() == '.json':
                sub_topics_override = json.loads(subtopics_path.read_text(encoding='utf-8'))
            else:
                sub_topics_override = [line.strip() for line in subtopics_path.read_text(encoding='utf-8').splitlines() if line.strip()]
    orchestrator = UBPOrchestrator(seed=args.seed)
    orchestrator.run_pipeline(
        args.directive,
        num_agents=args.num_agents,
        min_nrci=args.min_nrci,
        max_retries=args.max_retries,
        output_file=args.output_file,
        output_json=args.output_json,
        sub_topics_override=sub_topics_override,
    )
