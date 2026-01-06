"""
UBP HexDictionary v4.x (Recursive Block Recovery)
=================================================

Author: Euan R A Craig, New Zealand
Date: 06 January 2026

"""
from __future__ import annotations
import hashlib
import json
import os
import re
from typing import Dict, List, Tuple, Optional, Any

class HexDictionaryV4Exact:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}   
        self.id_map: Dict[str, str] = {}                
        self.tag_index: Dict[str, set[str]] = {}        

    def load_memory(self, json_file: str = "ubp_system_kb.json", md_file: str = "ubp_system_kb.md"):
        """Scavenges all JSON blocks from the provided files."""
        target_files = [json_file, md_file, "ubp_hash_memory_kb.md"]
        for fname in target_files:
            if not os.path.exists(fname): continue
            
            with open(fname, 'r') as f:
                content = f.read()
            
            print(f"[MEMORY] Scavenging {fname}...")
            found_blocks = self._scavenge_json_blocks(content)
            
            if found_blocks:
                print(f"   ✅ Recovered {len(found_blocks)} data blocks from {fname}")
                for block in found_blocks:
                    if isinstance(block, dict):
                        # If it's a dict of objects (keyed by hash)
                        if all(isinstance(v, dict) for v in block.values()):
                            for _, entry in block.items():
                                self._register_entry(entry)
                        else:
                            # It's a single entry
                            self._register_entry(block)
            else:
                # Fallback to Markdown headers if no JSON found
                self._load_md_content(content)

    def _scavenge_json_blocks(self, text: str) -> List[Any]:
        """Finds all valid JSON objects within a string, even if malformed/concatenated."""
        results = []
        # Find all potential start braces
        starts = [m.start() for m in re.finditer('{', text)]
        
        last_end = 0
        for start in starts:
            if start < last_end: continue
            
            # Try to find the matching end brace by expanding outward
            for end in range(len(text), start, -1):
                if text[end-1] != '}': continue
                
                candidate = text[start:end]
                try:
                    data = json.loads(candidate)
                    results.append(data)
                    last_end = end
                    break
                except:
                    # If it fails, try a quick repair (missing closing brace)
                    try:
                        data = json.loads(candidate + "}")
                        results.append(data)
                        last_end = end
                        break
                    except:
                        continue
        return results

    def _load_md_content(self, content: str):
        entries = re.split(r'\n(?=###? UBP-)', content)
        for entry_text in entries:
            entry_text = entry_text.strip()
            if not entry_text.startswith("#"): continue
            lines = entry_text.split('\n')
            header = lines[0]
            match = re.search(r'UBP-([A-Z0-9_-]+):\s*(.*)', header)
            if not match: continue
            entry = {"ubp_id": f"UBP-{match.group(1)}", "name": match.group(2).strip(), "tags": []}
            for line in lines[1:]:
                line = line.strip()
                if "**Math**:" in line: entry["math"] = line.split(":", 1)[1].strip()
                elif "**Language**:" in line: entry["language"] = line.split(":", 1)[1].strip()
                elif "**Script**:" in line: entry["script"] = line.split(":", 1)[1].strip()
                elif "**Tags**:" in line:
                    entry["tags"] = [t.strip() for t in line.split(":", 1)[1].split(",")]
            self._register_entry(entry)

    def _register_entry(self, entry):
        if not isinstance(entry, dict) or "ubp_id" not in entry: return
        entry.setdefault("math", "0")
        entry.setdefault("language", "Void")
        entry.setdefault("script", "None")
        if "fingerprint" not in entry:
            entry["fingerprint"] = hashlib.sha256(f"{entry['math']}|{entry['language']}|{entry['script']}".encode()).hexdigest()
        f_print = entry["fingerprint"]
        self.registry[f_print] = entry
        self.id_map[entry["ubp_id"]] = f_print
        for tag in entry.get("tags", []):
            self.tag_index.setdefault(tag, set()).add(f_print)

HEX_DB_EXACT = HexDictionaryV4Exact()
