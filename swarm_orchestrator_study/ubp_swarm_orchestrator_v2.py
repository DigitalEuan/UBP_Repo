"""
================================================================================
UBP SWARM ORCHESTRATOR v2.0 (Macro-Scale Document Synthesis)
================================================================================
Author: Manus (UBP Research Cortex v6.0)
Date: 20 April 2026

This advanced pipeline orchestrates a multi-tier swarm of mini-MoE agents to 
construct a geometrically coherent AND semantically relevant macro-document. 

Key Enhancements over v1.x:
1. Multi-Tier Swarm: Architect, Writers, Critics, Editors.
2. Dynamic Feedback Loop: Critics evaluate drafts on BOTH Geometric Stability 
   (NRCI) and Semantic Resonance (Cosine similarity to the directive/topic).
3. Scale: Employs significantly more agents (e.g., 15-30) to generate larger,
   more comprehensive documents.
4. Hierarchical Structure: Main Directive -> Sections -> Paragraphs.
================================================================================
"""

import argparse
import json
import os
import random
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

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


def get_semantic_resonance(text: str, target_topic: str, semantic_engine: UBPSemanticEngine) -> float:
    """Calculates semantic resonance (cosine similarity) between text and target topic."""
    text_vec = text_to_vector(text, semantic_engine)
    target_vec = text_to_vector(target_topic, semantic_engine)
    
    # Convert binary [0,1] to bipolar [-1,1] for cosine similarity
    bipolar_text = [(b * 2) - 1 for b in text_vec]
    bipolar_target = [(b * 2) - 1 for b in target_vec]
    
    return semantic_engine._cosine_similarity(bipolar_text, bipolar_target)


class SwarmAgent:
    def __init__(self, agent_id: int, role: str, moe_cortex: UBPMoECortexV2, semantic_engine: UBPSemanticEngine):
        self.agent_id = agent_id
        self.role = role
        self.moe = moe_cortex
        self.semantic = semantic_engine

    def draft(self, topic: str, max_words: int, feedback: str = "") -> str:
        print(f"\n  [Writer {self.agent_id} : {self.role}] Drafting '{topic}' (Max words: {max_words})...")
        if feedback:
            print(f"    -> Applying feedback: '{feedback}'")
            # Incorporate feedback into the MoE objective
            objective = f"{topic} {feedback}"
        else:
            objective = topic
            
        return self.moe.research(objective, max_words=max_words)
        
    def critique(self, text: str, target_topic: str, min_nrci: float, min_resonance: float) -> Tuple[bool, float, float, str]:
        print(f"\n  [Critic {self.agent_id} : {self.role}] Evaluating draft for '{target_topic}'...")
        
        # 1. Evaluate Geometric Stability (NRCI)
        draft_vec = text_to_vector(text, self.semantic)
        # Assuming isolated paragraph stability for the critique phase
        snapped_doc, _, _ = GOLAY_ENGINE.decode(draft_vec)
        stable_doc = GOLAY_ENGINE.encode(snapped_doc)
        tax = LEECH_ENGINE.calculate_symmetry_tax(stable_doc)
        nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
        
        # 2. Evaluate Semantic Resonance
        resonance = get_semantic_resonance(text, target_topic, self.semantic)
        
        print(f"    -> NRCI: {nrci:.4f} (Target: {min_nrci}) | Resonance: {resonance:.4f} (Target: {min_resonance})")
        
        accepted = nrci >= min_nrci and resonance >= min_resonance
        feedback = ""
        if not accepted:
            if nrci < min_nrci and resonance < min_resonance:
                feedback = "stable meaning"
            elif nrci < min_nrci:
                feedback = "stable"
            else:
                feedback = "meaning"
                
        return accepted, nrci, resonance, feedback


class UBPOrchestratorV2:
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

        print("[Orchestrator V2] Booting Semantic Engine...")
        self.semantic = UBPSemanticEngine()
        self.semantic.load(str(SYSTEM_KB_PATH), str(LANG_KB_PATH))

        print("[Orchestrator V2] Booting MoE Cortex (Training Linguist)...")
        self.moe = UBPMoECortexV2()

        self.document_vector = [0] * 24
        self.document_sections: List[str] = []
        self.run_log: List[Dict] = []
        self.agent_counter = 0

    def _create_agent(self, role: str) -> SwarmAgent:
        self.agent_counter += 1
        return SwarmAgent(self.agent_counter, role, self.moe, self.semantic)

    def _architect_outline(self, main_directive: str, num_sections: int, paragraphs_per_section: int) -> List[Dict]:
        """The Architect Agent breaks down the directive into a structured outline."""
        print(f"\n[Architect] Generating outline for: '{main_directive}'")
        base_res = self.semantic.query(main_directive, top_k=num_sections * 2)
        
        all_topics = []
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
            if clean_topic and clean_topic not in all_topics:
                all_topics.append(clean_topic)
                
        if not all_topics:
            all_topics = [main_directive]
            
        outline = []
        roles = ["PHYSICIST", "LOGICIAN", "GEOMETRICIAN", "SEMANTICIST", "OBSERVER"]
        
        for s in range(num_sections):
            section_topic = all_topics[s % len(all_topics)]
            paragraphs = []
            
            # Generate sub-topics for paragraphs
            sub_res = self.semantic.query(section_topic, top_k=paragraphs_per_section)
            sub_topics = []
            for result in sub_res:
                clean_topic = result.lexicon.split(']')[0].split(':')[-1].strip().replace('(', '').replace(')', '')
                if clean_topic:
                    sub_topics.append(clean_topic)
            
            if not sub_topics:
                sub_topics = [f"{section_topic} aspect {p+1}" for p in range(paragraphs_per_section)]
                
            for p in range(paragraphs_per_section):
                paragraphs.append({
                    'topic': sub_topics[p % len(sub_topics)],
                    'role': roles[(s + p) % len(roles)]
                })
                
            outline.append({
                'section_num': s + 1,
                'section_topic': section_topic,
                'paragraphs': paragraphs
            })
            
        return outline

    def run_pipeline(
        self,
        main_directive: str,
        num_sections: int = 3,
        paragraphs_per_section: int = 2,
        min_nrci: float = 0.65,
        min_resonance: float = 0.4,
        max_retries: int = 4,
        words_per_paragraph: int = 20,
        output_file: str = 'macro_document_v2.md',
        output_json: str = 'macro_document_v2.json'
    ) -> Dict:
        random.seed(self.seed)
        self.document_vector = [0] * 24
        self.document_sections = []
        self.run_log = []
        self.agent_counter = 0

        total_agents_expected = 1 + (num_sections * paragraphs_per_section * 2) + num_sections # Architect + (Writers + Critics) + Editors
        
        print(f"\n{'=' * 80}")
        print("UBP SWARM ORCHESTRATOR V2: MACRO-DOCUMENT SYNTHESIS")
        print(f"Directive: {main_directive.upper()}")
        print(f"Sections: {num_sections} | Paragraphs/Sec: {paragraphs_per_section} | Total Expected Agents: ~{total_agents_expected}")
        print(f"Target NRCI: {min_nrci} | Target Resonance: {min_resonance} | Max Retries: {max_retries} | Seed: {self.seed}")
        print(f"{'=' * 80}")

        # 1. Architect Phase
        outline = self._architect_outline(main_directive, num_sections, paragraphs_per_section)
        final_nrci = 0.0

        # 2. Writing & Critiquing Phase (Iterative Loop)
        for section in outline:
            section_content = []
            print(f"\n--- Processing Section {section['section_num']}: {section['section_topic']} ---")
            
            for p_idx, para_meta in enumerate(section['paragraphs']):
                topic = para_meta['topic']
                role = para_meta['role']
                
                writer = self._create_agent(f"WRITER-{role}")
                critic = self._create_agent(f"CRITIC-{role}")
                
                accepted = False
                attempts = 0
                feedback = ""
                final_text = ""
                final_para_nrci = 0.0
                final_para_res = 0.0
                
                while not accepted and attempts < max_retries:
                    attempts += 1
                    
                    # Writer drafts
                    draft_text = writer.draft(topic, max_words=words_per_paragraph + (attempts * 2), feedback=feedback)
                    
                    # Critic evaluates
                    accepted, nrci, resonance, new_feedback = critic.critique(draft_text, topic, min_nrci, min_resonance)
                    
                    final_para_nrci = nrci
                    final_para_res = resonance
                    
                    if accepted:
                        print("    -> CRITIC APPROVED. Appending to section.")
                        final_text = draft_text
                        
                        # Integrate into macro-document vector
                        draft_vec = text_to_vector(draft_text, self.semantic)
                        combined_vec = [a ^ b for a, b in zip(self.document_vector, draft_vec)]
                        snapped_doc, _, _ = GOLAY_ENGINE.decode(combined_vec)
                        self.document_vector = GOLAY_ENGINE.encode(snapped_doc)
                        
                        # Calculate running macro NRCI
                        tax = LEECH_ENGINE.calculate_symmetry_tax(self.document_vector)
                        final_nrci = float(Fraction(10, 1) / (Fraction(10, 1) + tax))
                        
                    else:
                        print(f"    -> CRITIC REJECTED. Providing feedback: '{new_feedback}'")
                        feedback = new_feedback
                        
                status_tag = "" if accepted else " (UNSTABLE - MAX RETRIES REACHED)"
                if not final_text:
                    final_text = draft_text # Use last attempt if failed
                    
                section_content.append(f"**[{role} Perspective]** {final_text}{status_tag}\n")
                
                self.run_log.append({
                    'section': section['section_num'],
                    'paragraph': p_idx + 1,
                    'role': role,
                    'topic': topic,
                    'accepted': accepted,
                    'attempts': attempts,
                    'final_nrci': final_para_nrci,
                    'final_resonance': final_para_res,
                    'text': final_text,
                })
                
            # 3. Editor Phase (Synthesizing Section)
            editor = self._create_agent("EDITOR")
            print(f"\n  [{editor.role} {editor.agent_id}] Synthesizing Section {section['section_num']}...")
            
            sec_text = f"### Section {section['section_num']}: {section['section_topic'].title()}\n\n"
            sec_text += "\n".join(section_content)
            self.document_sections.append(sec_text)

        # 4. Final Document Assembly
        final_doc = f"# UBP Macro-Document: {main_directive}\n\n"
        final_doc += f"**Final Macro Geometric Stability (NRCI):** {final_nrci:.4f}\n"
        final_doc += f"**Total Agents Deployed:** {self.agent_counter}\n"
        final_doc += f"**Seed:** {self.seed}\n\n"
        final_doc += "---\n\n"
        final_doc += "\n".join(self.document_sections)

        output_path = Path(output_file)
        output_path.write_text(final_doc, encoding='utf-8')

        result = {
            'directive': main_directive,
            'seed': self.seed,
            'num_sections': num_sections,
            'paragraphs_per_section': paragraphs_per_section,
            'total_agents': self.agent_counter,
            'min_nrci': min_nrci,
            'min_resonance': min_resonance,
            'max_retries': max_retries,
            'final_macro_nrci': final_nrci,
            'output_markdown': str(output_path),
            'outline': outline,
            'paragraphs': self.run_log,
        }
        Path(output_json).write_text(json.dumps(result, indent=2), encoding='utf-8')

        print(f"\n{'=' * 80}")
        print("ORCHESTRATION COMPLETE")
        print(f"Final Document NRCI: {final_nrci:.4f}")
        print(f"Total Agents: {self.agent_counter}")
        print(f"Saved to: '{output_path}'")
        print(f"Metadata: '{output_json}'")
        print(f"{'=' * 80}\n")
        return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run the UBP Swarm Orchestrator V2.')
    parser.add_argument('--directive', default='Thermodynamics of Hexadecad elements')
    parser.add_argument('--sections', type=int, default=3)
    parser.add_argument('--paragraphs', type=int, default=2)
    parser.add_argument('--min-nrci', type=float, default=0.65)
    parser.add_argument('--min-resonance', type=float, default=0.3)
    parser.add_argument('--max-retries', type=int, default=4)
    parser.add_argument('--words', type=int, default=20)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output-file', default='macro_document_v2.md')
    parser.add_argument('--output-json', default='macro_document_v2.json')
    return parser


if __name__ == '__main__':
    args = build_parser().parse_args()
    orchestrator = UBPOrchestratorV2(seed=args.seed)
    orchestrator.run_pipeline(
        main_directive=args.directive,
        num_sections=args.sections,
        paragraphs_per_section=args.paragraphs,
        min_nrci=args.min_nrci,
        min_resonance=args.min_resonance,
        max_retries=args.max_retries,
        words_per_paragraph=args.words,
        output_file=args.output_file,
        output_json=args.output_json
    )
