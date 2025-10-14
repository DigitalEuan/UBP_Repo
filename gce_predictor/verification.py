from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from .storage import load_jsonl, append_jsonl, default_predictions_path


def attach_verification(
    prediction_id: str,
    status: str,
    notes: Optional[str] = None,
    storage_path: Optional[str] = None,
) -> bool:
    """Append a verification record line adjacent to predictions.

    This does not mutate past lines; instead, it appends a new JSONL record
    of type 'verification' referencing the prediction_id, keeping an immutable log.
    """
    record: Dict = {
        "type": "verification",
        "prediction_id": prediction_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,  # e.g., 'observed', 'not_observed', 'inconclusive'
        "notes": notes,
    }
    append_jsonl(record, path=storage_path or default_predictions_path())
    return True


def summarize_verifications(storage_path: Optional[str] = None) -> Dict[str, int]:
    counts = {"observed": 0, "not_observed": 0, "inconclusive": 0}
    for rec in load_jsonl(storage_path or default_predictions_path()):
        if rec.get("type") == "verification":
            status = rec.get("status")
            if status in counts:
                counts[status] += 1
    return counts
