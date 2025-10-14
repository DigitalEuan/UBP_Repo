from __future__ import annotations

from typing import Dict, Optional

from .solar_monitor import SolarMonitor
from .storage import append_jsonl, default_predictions_path


def run_prediction(storage_path: Optional[str] = None, monitor: Optional[SolarMonitor] = None) -> Optional[Dict]:
    mon = monitor or SolarMonitor()
    pred = mon.check_for_trigger()
    if pred is None:
        return None
    append_jsonl(pred, path=storage_path or default_predictions_path())
    return pred
