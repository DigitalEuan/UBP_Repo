# ══════════════════════════════════════════════════════════════════════════════
# §11  RUNTIME — THE ORCHESTRATOR (v3.7.6 Hardened)
# ══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import sys, os, json, time, re, hashlib
from typing import List, Dict, Optional, Tuple, Any

# IMPORT ALL MODULES
from GLM01_substrate import BLA, LEECH_ENGINE, _build_vocabulary, build_default_crg, WordEntry
from GLM02_constants import *
from GLM03_crg import auto_expand_crg, lattice_auto_link, _enhanced_query_type
from GLM04_number_vocab import inject_number_vocab
from GLM07_idea_manager import IdeaManager
from GLM08_idea_meta_graph import IdeaMetaGraph
from GLM09_tools import detect_compute, evaluate_numeric, detect_symbolic, evaluate_symbolic, ground_result
from GLM10_response_composer import compose_response
from GLM13_deliberative_reasoning import deliberate

class GLMRuntimeV37:
    def __init__(self, auto_expand: bool = True):
        print("[GLM] Booting stack...")
        self.vocab_dict = _build_vocabulary()
        self.crg = build_default_crg()
        
        # Inject Numbers
        inject_number_vocab(self.vocab_dict)
        
        # Expand Graph
        if auto_expand:
            auto_expand_crg(self.crg, self.vocab_dict)
            lattice_auto_link(self.crg, self.vocab_dict)
            
        # Wrap vocab for manager
        class Vocab:
            def __init__(self, d): self.words = d
        self.vocab = Vocab(self.vocab_dict)
        
        self.manager = IdeaManager(vocab=self.vocab, crg=self.crg)
        self.meta_graph = IdeaMetaGraph()
        self._turn = 0

    def chat(self, query: str) -> str:
        self._turn += 1
        active = self.manager.active
        resolved, subs = active.resolve_anaphora(query)
        
        # 1. Tools
        comp_res = None
        c_req = detect_compute(resolved)
        if c_req: 
            eval_res = evaluate_numeric(c_req)
            comp_res = {"computation": c_req, "result": eval_res, 
                        "grounded": ground_result(eval_res.get("approx", 0), self.vocab)}
        
        sym_res = None
        s_req = detect_symbolic(resolved)
        if s_req: 
            sym_res = {"computation": s_req, "result": evaluate_symbolic(s_req)}
        
        # 2. Deliberation
        delib_res = None
        if not comp_res and not sym_res:
            delib_res = deliberate(resolved)
            
        # 3. Linguistic Processing
        tokens = re.findall(r"\b\w+\b", resolved.lower())
        content = [(t, self.vocab_dict[t]) for t in tokens if t in self.vocab_dict]
        
        # SURGICAL FIX: Filter out function words from the Gap report
        unknown = [t for t in tokens if t not in self.vocab_dict and t not in FUNCTION_WORDS]
        
        # 4. Update Manager
        self.manager.update(content, self._turn)
        
        # 5. Compose (Pass delib_res here)
        return compose_response(
            query, content, unknown, self.manager.active, self.manager, self.vocab,
            _enhanced_query_type(query), comp_res, sym_res, deliberation=delib_res
        )

    def reset_idea(self):
        self.manager.reset()
        self._turn = 0

    def idea_state(self):
        return {"turn": self._turn, "zones": len(self.manager.zones), "meta": self.meta_graph.stats()}

    def mature(self, n: int = 3):
        self.manager.mature_all(n)