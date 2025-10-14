"""
Prediction storage utilities (JSONL file).
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional

DEFAULT_PREDICTIONS_FILE = "/workspace/data/predictions/predictions.jsonl"


def default_predictions_path() -> str:
    return os.environ.get("GCE_PREDICTIONS_PATH", DEFAULT_PREDICTIONS_FILE)


def append_jsonl(record: Dict, path: Optional[str] = None) -> None:
    file_path = path or default_predictions_path()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_jsonl(path: Optional[str] = None) -> List[Dict]:
    file_path = path or default_predictions_path()
    if not os.path.exists(file_path):
        return []
    out: List[Dict] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def find_by_id(prediction_id: str, path: Optional[str] = None) -> Optional[Dict]:
    for rec in load_jsonl(path):
        if rec.get("prediction_id") == prediction_id:
            return rec
    return None
