from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .storage import load_jsonl, default_predictions_path


DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>UBP GCE Observatory</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    h1 { margin-bottom: 0; }
    .muted { color: #666; }
    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background: #f4f4f4; }
    code { background: #f9f9f9; padding: 2px 4px; }
  </style>
</head>
<body>
  <h1>UBP GCE Observatory</h1>
  <div class="muted">Updated: {{UPDATED}}</div>

  <h2>Predictions</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Timestamp</th>
        <th>Class</th>
        <th>Window</th>
        <th>Region</th>
        <th>Expected Ratios</th>
      </tr>
    </thead>
    <tbody>
      {{PRED_ROWS}}
    </tbody>
  </table>

  <h2>Verifications</h2>
  <table>
    <thead>
      <tr>
        <th>Prediction ID</th>
        <th>Status</th>
        <th>Timestamp</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      {{VER_ROWS}}
    </tbody>
  </table>

</body>
</html>
"""


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_dashboard_html(path: Optional[str] = None) -> str:
    recs = load_jsonl(path)
    preds = [r for r in recs if r.get("prediction_id")]
    vers = [r for r in recs if r.get("type") == "verification"]

    def row_pred(r: Dict) -> str:
        win = r.get("time_window", {})
        ratios = r.get("expected_geometric_signature", {}).get("ratios", [])
        return (
            f"<tr><td><code>{_escape(r.get('prediction_id',''))}</code></td>"
            f"<td>{_escape(r.get('timestamp',''))}</td>"
            f"<td>{_escape(r.get('trigger_class',''))}</td>"
            f"<td>{_escape(win.get('start',''))} → { _escape(win.get('end','')) }</td>"
            f"<td>{_escape(r.get('predicted_location',{}).get('region',''))}</td>"
            f"<td>{_escape(', '.join(map(str, ratios)))}</td></tr>"
        )

    def row_ver(v: Dict) -> str:
        return (
            f"<tr><td><code>{_escape(v.get('prediction_id',''))}</code></td>"
            f"<td>{_escape(v.get('status',''))}</td>"
            f"<td>{_escape(v.get('timestamp',''))}</td>"
            f"<td>{_escape(str(v.get('notes','')))}</td></tr>"
        )

    html = DASHBOARD_HTML
    html = html.replace("{{UPDATED}}", datetime.utcnow().isoformat() + "Z")
    html = html.replace("{{PRED_ROWS}}", "\n".join(row_pred(r) for r in preds[-200:]))
    html = html.replace("{{VER_ROWS}}", "\n".join(row_ver(v) for v in vers[-200:]))
    return html


def write_dashboard(output_file: str, path: Optional[str] = None) -> str:
    html = generate_dashboard_html(path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file
