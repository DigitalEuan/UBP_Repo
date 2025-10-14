from __future__ import annotations

import argparse
import json
from typing import Optional

from .predictor import run_prediction
from .storage import default_predictions_path, load_jsonl, find_by_id
from .verification import attach_verification, summarize_verifications
from .notify import notify_new_prediction
from .s2_scanner import scan_prediction, synthetic_fetcher
from .dashboard import write_dashboard


def cmd_predict(args: argparse.Namespace) -> int:
    pred = run_prediction(storage_path=args.path)
    if pred is None:
        print("No trigger at this time.")
        return 0
    print(json.dumps(pred, indent=2))
    if args.notify:
        res = notify_new_prediction(pred)
        print(f"Notifications sent: webhook={res['webhook']} email={res['email']}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    recs = load_jsonl(args.path)
    if not recs:
        print("No predictions found.")
        return 0
    for r in recs[-args.n:]:
        print(f"{r.get('prediction_id')} | {r.get('timestamp')} | class={r.get('trigger_class')} | region={r.get('predicted_location',{}).get('region')}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    rec = find_by_id(args.id, args.path)
    if not rec:
        print("Prediction not found.")
        return 1
    print(json.dumps(rec, indent=2))
    return 0

def cmd_verify(args: argparse.Namespace) -> int:
    ok = attach_verification(args.id, args.status, notes=args.notes, storage_path=args.path)
    if ok:
        print("Verification recorded.")
        return 0
    print("Failed to record verification.")
    return 1

def cmd_stats(args: argparse.Namespace) -> int:
    stats = summarize_verifications(args.path)
    print(json.dumps(stats, indent=2))
    return 0

def cmd_scan(args: argparse.Namespace) -> int:
    rec = find_by_id(args.id, args.path)
    if not rec:
        print("Prediction not found.")
        return 1
    # For now, use synthetic fetcher; can be swapped with real Sentinel-2 fetcher
    result = scan_prediction(rec, synthetic_fetcher)
    print(json.dumps(result, indent=2))
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gce-predictor", description="UBP GCE Predictor CLI")
    p.set_defaults(func=lambda _: 0)

    p.add_argument("--path", default=default_predictions_path(), help="Path to predictions JSONL")

    sub = p.add_subparsers()

    sp = sub.add_parser("predict", help="Check current solar data and store prediction if triggered")
    sp.set_defaults(func=cmd_predict)
    sp.add_argument("--notify", action="store_true", help="Send notifications if configured")

    sl = sub.add_parser("list", help="List recent predictions")
    sl.add_argument("-n", type=int, default=10, help="Number of records to show")
    sl.set_defaults(func=cmd_list)

    ss = sub.add_parser("show", help="Show a specific prediction by ID")
    ss.add_argument("id", help="Prediction ID")
    ss.set_defaults(func=cmd_show)

    sv = sub.add_parser("verify", help="Append a verification record for a prediction")
    sv.add_argument("id", help="Prediction ID")
    sv.add_argument("status", choices=["observed", "not_observed", "inconclusive"], help="Verification status")
    sv.add_argument("--notes", default=None, help="Optional notes")
    sv.set_defaults(func=cmd_verify)

    st = sub.add_parser("stats", help="Summarize verification outcomes")
    st.set_defaults(func=cmd_stats)

    sc = sub.add_parser("scan", help="Run Sentinel-2 pre/post anomaly scan (synthetic fetcher)")
    sc.add_argument("id", help="Prediction ID")
    sc.set_defaults(func=cmd_scan)

    db = sub.add_parser("dashboard", help="Generate static HTML dashboard")
    db.add_argument("--out", default="/workspace/data/predictions/dashboard.html", help="Output HTML file")
    def _cmd_db(args: argparse.Namespace) -> int:
        path = write_dashboard(args.out, args.path)
        print(f"Wrote dashboard to {path}")
        return 0
    db.set_defaults(func=_cmd_db)

    return p


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
