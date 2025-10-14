from __future__ import annotations

"""
Sentinel-2 pre/post anomaly scanner (pluggable fetcher).
This module provides the scanning and comparison logic; the image fetcher
is abstracted so we can plug in real APIs later (Sentinel Hub, Copernicus).
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from .verification import attach_verification


@dataclass
class Tile:
    acquired: datetime
    band_red: np.ndarray  # 2D arrays (same shape)
    band_nir: np.ndarray


Fetcher = Callable[[float, float, datetime, datetime], List[Tile]]


def compute_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    red = red.astype(np.float32)
    nir = nir.astype(np.float32)
    denom = (nir + red)
    denom[denom == 0] = 1e-6
    return (nir - red) / denom


def temporal_change_score(pre: np.ndarray, post: np.ndarray) -> float:
    """Compute a normalized change score between pre and post NDVI rasters."""
    # align shapes
    h = min(pre.shape[0], post.shape[0])
    w = min(pre.shape[1], post.shape[1])
    if h == 0 or w == 0:
        return 0.0
    a = pre[:h, :w]
    b = post[:h, :w]
    diff = np.abs(a - b)
    # robust percentile-based normalization
    p95 = np.percentile(diff, 95)
    if p95 <= 1e-6:
        return 0.0
    score = float(np.clip(diff.mean() / (p95 + 1e-6), 0.0, 1.0))
    return score


def scan_prediction(
    prediction: Dict,
    fetcher: Fetcher,
    pre_days: int = 7,
    post_days: int = 7,
    ndvi_drop_threshold: float = 0.15,
) -> Dict:
    """Run pre/post scan for a prediction using a tile fetcher.

    Returns a dict with summary change score and a boolean flag indicating
    whether an anomaly is likely present (candidate GCE).
    """
    lat = prediction.get("predicted_location", {}).get("coordinates", {}).get("lat")
    lon = prediction.get("predicted_location", {}).get("coordinates", {}).get("lon")
    if lat is None or lon is None:
        return {"success": False, "error": "Missing coordinates"}

    start = datetime.fromisoformat(prediction["time_window"]["start"].replace("Z", "+00:00")).astimezone(timezone.utc)
    end = datetime.fromisoformat(prediction["time_window"]["end"].replace("Z", "+00:00")).astimezone(timezone.utc)

    pre_start = start - timedelta(days=pre_days)
    pre_end = start
    post_start = start
    post_end = end + timedelta(days=post_days)

    pre_tiles = fetcher(lat, lon, pre_start, pre_end)
    post_tiles = fetcher(lat, lon, post_start, post_end)

    if not pre_tiles or not post_tiles:
        return {"success": False, "error": "No tiles fetched"}

    # Take median NDVI over pre and post windows
    def median_ndvi(tiles: List[Tile]) -> np.ndarray:
        ndvis = [compute_ndvi(t.band_red, t.band_nir) for t in tiles]
        stack = np.stack(ndvis, axis=0)
        return np.nanmedian(stack, axis=0)

    ndvi_pre = median_ndvi(pre_tiles)
    ndvi_post = median_ndvi(post_tiles)

    score = temporal_change_score(ndvi_pre, ndvi_post)

    # Convert NDVI absolute drop proxy
    abs_drop = float(np.clip((ndvi_pre.mean() - ndvi_post.mean()), 0.0, 1.0))
    anomaly = (abs_drop >= ndvi_drop_threshold) or (score >= 0.35)

    return {
        "success": True,
        "change_score": round(score, 3),
        "ndvi_drop": round(abs_drop, 3),
        "anomaly": anomaly,
        "pre_tiles": len(pre_tiles),
        "post_tiles": len(post_tiles),
    }


# Placeholder synthetic fetcher for testing the pipeline

def synthetic_fetcher(lat: float, lon: float, start: datetime, end: datetime) -> List[Tile]:
    rng = np.random.default_rng(seed=int(abs(lat * 1000) + abs(lon * 1000) + start.day + end.day))
    h, w = 256, 256
    # generate coherent fields; later window slightly lower NDVI
    base_red = rng.uniform(0.1, 0.3, size=(h, w)).astype(np.float32)
    base_nir = rng.uniform(0.3, 0.6, size=(h, w)).astype(np.float32)
    acquired = start + (end - start) / 2
    return [Tile(acquired=acquired, band_red=base_red, band_nir=base_nir)]
