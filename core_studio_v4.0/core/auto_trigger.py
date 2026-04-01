"""
UBP Auto-Trigger v17.7 — Final Production + synth_context()
===============================================
Full semantic + extended Gray-code numeric + synthesized context block
"""

import json
import re
import os
import math
from typing import List, Dict, Any

# ===================================================================
# 1. LOAD BOTH KBs
# ===================================================================
with open('ubp_system_kb.json', 'r', encoding='utf-8') as f:
    KB_SYSTEM = json.load(f)
print(f"[Cortex] System KB: {len(KB_SYSTEM)} entries")

with open('ubp_lang_kb_combined_v4.json', 'r', encoding='utf-8') as f:
    KB_LANG = json.load(f)
print(f"[Cortex] Language KB: {len(KB_LANG)} semantic operators")

# ===================================================================
# 2. AUTO-BUILD RICH MAPS
# ===================================================================
ID_TO_KEY = {}
PHRASE_TO_KEY = {}
OPERATOR_TO_KEY = {}
OP_TRIGGER_WORDS = {}

for key, entry in KB_SYSTEM.items():
    uid = entry.get('ubp_id')
    if uid:
        ID_TO_KEY[uid] = key
    name = entry.get('lexicon', '').split(']')[0].strip('[]').split(':')[-1].strip()
    if name and name != "Unknown":
        PHRASE_TO_KEY[name.lower()] = key

for key, entry in KB_LANG.items():
    uid = entry.get('ubp_id')
    if uid and uid.startswith('OP_'):
        OPERATOR_TO_KEY[uid] = key
        lex = entry.get('lexicon', '').lower()
        for word in re.findall(r'\b\w{3,}\b', lex):
            if word not in ['the', 'and', 'for', 'with', 'operator', 'of']:
                OP_TRIGGER_WORDS[word] = key
                break

print(f"[Cortex] Rich trigger map built: {len(OP_TRIGGER_WORDS)} words → operators")

# ===================================================================
# 3. EXTENDED NUMERIC ENGINE (from GLM Study Step 5)
# ===================================================================
class MathStringParser:
    @staticmethod
    def parse(math_str: str) -> Dict[str, float]:
        if not math_str: return {}
        props = {}
        for pair in math_str.split('|'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                k = k.strip()
                v = v.strip()
                try:
                    if '/' in v:
                        num, den = v.split('/')
                        props[k] = float(num) / float(den)
                    else:
                        props[k] = float(v)
                except:
                    pass
        return props

class ExtendedMetricPreservingEncoder:
    def __init__(self):
        self.schema = {  # exact schema from chat simulation
            'Z': {'scale':'linear','bits':7,'min':0,'max':120},
            'M': {'scale':'log','bits':8,'min':0.5,'max':310},
            'BP':{'scale':'log','bits':8,'min':0.05,'max':7000},
            'MP':{'scale':'log','bits':8,'min':0.05,'max':4000},
            'EN':{'scale':'linear','bits':6,'min':0,'max':4.5},
            'Ion':{'scale':'log','bits':8,'min':50,'max':30000},
            'Rho':{'scale':'log','bits':8,'min':5e-5,'max':30},
            'Rad':{'scale':'linear','bits':7,'min':20,'max':310},
            'Valence_e':{'scale':'linear','bits':4,'min':0,'max':8},
            'Phase_STP':{'scale':'linear','bits':2,'min':0,'max':3},
            'Oxidation':{'scale':'linear','bits':5,'min':-4,'max':8},
            'Crystal':{'scale':'linear','bits':4,'min':0,'max':10},
            'Dipole':{'scale':'linear','bits':6,'min':0,'max':15},
            'Density':{'scale':'log','bits':7,'min':0.05,'max':50},
            'Phase':{'scale':'linear','bits':2,'min':0,'max':3},
            'pKa1':{'scale':'linear','bits':6,'min':-5,'max':20},
        }
        self.canonical_props = list(self.schema.keys())

    def _gray_encode(self, n: int, bits: int) -> List[int]:
        binary = n ^ (n >> 1)
        return [(binary >> (bits - 1 - i)) & 1 for i in range(bits)]

    def encode(self, props: Dict[str, float]) -> List[int]:
        vector = []
        for prop in self.canonical_props:
            spec = self.schema[prop]
            bits = spec['bits']
            val = props.get(prop)
            present = 1 if val is not None else 0
            vector.append(present)
            if present:
                v = max(spec['min'], min(spec['max'], val))
                if spec['scale'] == 'log':
                    log_min = max(spec['min'], 1e-12)
                    log_max = max(spec['max'], 1e-12)
                    norm = (math.log(max(v, 1e-12)) - math.log(log_min)) / (math.log(log_max) - math.log(log_min))
                else:
                    norm = (v - spec['min']) / (spec['max'] - spec['min']) if spec['max'] > spec['min'] else 0.0
                bin_idx = min(int(norm * (1 << bits)), (1 << bits) - 1)
                vector.extend(self._gray_encode(bin_idx, bits))
            else:
                vector.extend([0] * bits)
        return vector

encoder = ExtendedMetricPreservingEncoder()

# ===================================================================
# 4. NL-TO-MATH
# ===================================================================
def nl_to_math(nl_query: str) -> str:
    text = nl_query.lower()
    props = {}

    if any(w in text for w in ["gas", "gaseous", "vapour", "vapor"]): props["Phase"] = 1
    elif any(w in text for w in ["liquid", "solvent", "fluid", "aqueous"]): props["Phase"] = 2
    elif any(w in text for w in ["solid", "crystal", "powder", "crystalline"]): props["Phase"] = 3

    if m := re.search(r"(?:mass|molar mass|molecular weight)\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["M"] = float(m.group(1))
    if m := re.search(r"(?:boiling\s*point|bp)\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["BP"] = float(m.group(1))
    if m := re.search(r"(?:melting\s*point|mp)\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["MP"] = float(m.group(1))
    if m := re.search(r"(?:dipole)\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["Dipole"] = float(m.group(1))
    elif any(w in text for w in ["polar", "highly polar"]): props["Dipole"] = 2.0
    elif any(w in text for w in ["nonpolar", "apolar"]): props["Dipole"] = 0.0
    if m := re.search(r"(?:density)\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["Density"] = float(m.group(1))
    if m := re.search(r"pka\s*(?:of|around|about|~|≈)?\s*([0-9]+(?:\.[0-9]+)?)", text):
        props["pKa1"] = float(m.group(1))
    elif "acid" in text: props["pKa1"] = 5.0
    elif "base" in text: props["pKa1"] = 10.0

    return "|".join(f"{k}={v}" for k, v in props.items()) if props else ""

# ===================================================================
# 5. NUMERIC TRIGGER
# ===================================================================
def numeric_trigger(text: str) -> List[Dict]:
    math_str = nl_to_math(text)
    if not math_str:
        return []
    props = MathStringParser.parse(math_str)
    query_vec = encoder.encode(props)

    memories = []
    for key, entry in KB_SYSTEM.items():
        gray = entry.get('atlas', {}).get('gray_vector')
        if gray and len(gray) == len(query_vec):
            dist = sum(x != y for x, y in zip(query_vec, gray))
            if dist <= 14:
                memories.append({
                    "data": entry,
                    "match": "NUMERIC",
                    "boost": 3.5 - (dist / len(query_vec)),
                    "numeric_dist": dist,
                    "math_str": math_str
                })
    return sorted(memories, key=lambda x: x['boost'], reverse=True)[:12]

# ===================================================================
# 6. REFLEXIVE RECALL
# ===================================================================
def reflexive_recall(text: str):
    memories = {}
    input_lower = text.lower()

    # 1. Numeric (highest priority)
    for m in numeric_trigger(text):
        key = next((k for k, v in KB_SYSTEM.items() if v is m['data']), None)
        if key:
            memories[key] = m

    # 2. Operators
    for word, op_key in OP_TRIGGER_WORDS.items():
        if word in input_lower and op_key not in memories:
            if op_key in KB_LANG:
                memories[op_key] = {"data": KB_LANG[op_key], "match": "OPERATOR", "boost": 3.0}

    # 3. Phrase + ID
    for phrase, key in PHRASE_TO_KEY.items():
        if phrase in input_lower and key not in memories:
            memories[key] = {"data": KB_SYSTEM[key], "match": "PHRASE", "boost": 2.2}

    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        key = ID_TO_KEY.get(uid)
        if key and key not in memories:
            memories[key] = {"data": KB_SYSTEM[key], "match": "ID", "boost": 1.8}

    # 4. Keyword fallback (limited)
    if len(memories) < 12:
        words = re.findall(r'\b\w{4,}\b', input_lower)
        for word in words:
            for key, entry in list(KB_SYSTEM.items()) + list(KB_LANG.items()):
                if word in entry.get('lexicon', '').lower() and key not in memories:
                    memories[key] = {"data": entry, "match": "KEYWORD", "boost": 1.0}
                    if len(memories) > 20: break

    # Deduplicate + sort
    final_context = []
    seen = set()
    sorted_mem = sorted(memories.values(), key=lambda x: x.get('boost', 1.0), reverse=True)
    for m in sorted_mem:
        uid = m['data'].get('ubp_id')
        if uid and uid not in seen:
            seen.add(uid)
            entry = m['data']
            atlas = entry.get('atlas', {})
            final_context.append({
                "ubp_id": uid,
                "name": entry.get('lexicon', '').split(']')[0].strip('[]').split(':')[-1].strip(),
                "math": entry.get('math'),
                "hierarchy": atlas.get('hierarchy'),
                "nrci": str(atlas.get('nrci_score', 'N/A')),
                "match_type": m.get('match'),
                "numeric_dist": m.get('numeric_dist')
            })
            if len(final_context) >= 15:
                break
    return final_context

# ===================================================================
# 7. NEW: SYNTH_CONTEXT() — clean merged block for AI prompt
# ===================================================================
def synth_context(recall_list: List[Dict]) -> str:
    """Synthesizes a clean, readable context block from reflexive_recall() results."""
    if not recall_list:
        return "[No relevant context found]"

    lines = ["=== UBP Geometric Context ==="]

    # Group by type
    operators = [r for r in recall_list if r.get("match_type") == "OPERATOR"]
    numeric   = [r for r in recall_list if r.get("match_type") == "NUMERIC"]
    entities  = [r for r in recall_list if r.get("match_type") in ("PHRASE", "ID", "KEYWORD")]

    # 1. Operators (highest semantic value)
    if operators:
        lines.append("\n[SEMANTIC OPERATORS]")
        for r in operators[:3]:
            lines.append(f"• {r['ubp_id']}: {r['math']}")

    # 2. Numeric matches
    if numeric:
        lines.append("\n[NUMERIC PROPERTY MATCH]")
        for r in numeric[:2]:
            lines.append(f"• {r['ubp_id']} ({r['name']}) — dist={r['numeric_dist']} | {r['math_str']}")

    # 3. Entities
    if entities:
        lines.append("\n[RELEVANT ENTITIES]")
        for r in entities[:6]:
            short_math = r['math'][:120] + "..." if len(r['math']) > 120 else r['math']
            lines.append(f"• {r['name']} ({r['ubp_id']}) | {short_math}")

    lines.append("\n=== End Context ===")
    return "\n".join(lines)

# ===================================================================
# TEST
# ===================================================================
if __name__ == "__main__":
    query = "why does water dissolve sodium chloride"
    raw_context = reflexive_recall(query)
    synthesized = synth_context(raw_context)
    
    print(synthesized)
