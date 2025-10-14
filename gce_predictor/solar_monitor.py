"""
UBP Solar Monitor: fetches solar/geomagnetic data and classifies UBP triggers.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests

from .ubp_signatures import expected_signature_for_trigger

ELECTROMAGNETIC_CRV: float = 6.4846e11  # Hz
TOGGLE_PROB_EM: float = 3.1415926535 / 4.0


@dataclass
class TriggerReading:
    time: datetime
    xray_flux_wm2: Optional[float]
    kp_index: Optional[float]


class SolarMonitor:
    GOES_XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
    KP_OBSERVED_URL = "https://services.swpc.noaa.gov/json/kp/observed.json"

    XRAY_M5_THRESHOLD = 5e-5   # W/m^2
    XRAY_X1_THRESHOLD = 1e-4   # W/m^2
    KP_HIGH_THRESHOLD = 6
    KP_SEVERE_THRESHOLD = 8

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": "UBP-GCE-Predictor/1.0"})

    def fetch_goes_xray(self) -> List[Dict]:
        try:
            r = self.session.get(self.GOES_XRAY_URL, timeout=15)
            r.raise_for_status()
            data = r.json()
            # filter to short wavelength band 0.05-0.4nm if present
            filtered = [d for d in data if str(d.get("energy", "")).startswith("0.05")]
            return filtered or data
        except Exception:
            return []

    def fetch_kp_observed(self, hours_back: int = 24) -> List[Dict]:
            # returns last N hours observed Kp
        try:
            r = self.session.get(self.KP_OBSERVED_URL, timeout=15)
            r.raise_for_status()
            data = r.json()
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
            out: List[Dict] = []
            for d in data:
                tt = d.get("time_tag") or d.get("time")
                if not tt:
                    continue
                try:
                    t = datetime.fromisoformat(tt.replace("Z", "+00:00")).astimezone(timezone.utc)
                except Exception:
                    continue
                if t >= cutoff:
                    out.append({"time_tag": t, "kp": float(d.get("kp_index") or d.get("kp") or 0.0)})
            return out
        except Exception:
            return []

    def latest_xray_flux(self) -> Optional[float]:
        data = self.fetch_goes_xray()
        if not data:
            return None
        try:
            latest = max(data, key=lambda d: d.get("time_tag", ""))
            return float(latest.get("flux"))
        except Exception:
            return None

    def latest_kp(self) -> Optional[float]:
        data = self.fetch_kp_observed()
        if not data:
            return None
        try:
            latest = max(data, key=lambda d: d.get("time_tag"))
            return float(latest.get("kp"))
        except Exception:
            return None

    def classify_trigger(self, xray_flux: float, kp_index: float) -> str:
        is_x = xray_flux >= self.XRAY_X1_THRESHOLD
        is_m = xray_flux >= self.XRAY_M5_THRESHOLD
        is_kp_high = kp_index >= self.KP_HIGH_THRESHOLD
        is_kp_severe = kp_index >= self.KP_SEVERE_THRESHOLD

        if is_x and is_kp_severe:
            return "hybrid"
        if is_x or (is_m and not is_kp_high):
            return "c"
        if is_kp_high and not is_x:
            return "mu0"
        return "none"

    def generate_prediction(self, trigger_class: str) -> Dict:
        now = datetime.now(timezone.utc)
        sig = expected_signature_for_trigger(trigger_class)
        return {
            "prediction_id": f"UBP-GCE-{now.strftime('%Y%m%d-%H%M%S')}",
            "timestamp": now.isoformat().replace("+00:00", "Z"),
            "trigger_class": trigger_class,
            "time_window": {
                "start": (now + timedelta(hours=6)).isoformat().replace("+00:00", "Z"),
                "end": (now + timedelta(hours=54)).isoformat().replace("+00:00", "Z"),
            },
            "predicted_location": {
                "region": "Southern England",
                "coordinates": {"lat": 51.2, "lon": -1.8},
                "confidence": 0.85,
            },
            "expected_geometric_signature": sig,
            "nrci_threshold": 0.98,
            "ubp_realm": "Electromagnetic",
            "crv_hz": ELECTROMAGNETIC_CRV,
            "toggle_probability": TOGGLE_PROB_EM,
            "verification": {
                "status": "pending",
                "notes": None,
            },
        }

    def check_for_trigger(self) -> Optional[Dict]:
        x = self.latest_xray_flux()
        k = self.latest_kp()
        if x is None or k is None:
            return None
        tclass = self.classify_trigger(x, k)
        if tclass == "none":
            return None
        return self.generate_prediction(tclass)
