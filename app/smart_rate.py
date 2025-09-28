
from __future__ import annotations
import os, json, hashlib, time, math
from pathlib import Path
from typing import Optional, Tuple

DEFAULT_STATS = {
    "overshoot": {},   # key: f"{encoder}|{container}" -> float
    "updated_at": 0
}

def _stats_path(base_dir: str | os.PathLike) -> str:
    base = Path(base_dir); base.mkdir(parents=True, exist_ok=True)
    return str(base / "encode_stats.json")

def cache_path(base_dir: str) -> str:
    base = Path(base_dir); base.mkdir(parents=True, exist_ok=True)
    return str(base / "encodes_cache.json")

def load_stats(base_dir: str) -> dict:
    path = _stats_path(base_dir)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return DEFAULT_STATS.copy()
            data.setdefault("overshoot", {})
            data.setdefault("updated_at", 0)
            return data
    except Exception:
        return DEFAULT_STATS.copy()

def save_stats(base_dir: str, data: dict) -> None:
    path = _stats_path(base_dir)
    data = dict(data or {})
    data.setdefault("overshoot", {})
    data["updated_at"] = int(time.time())
    tmp = path + ".tmp"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def get_dynamic_overshoot(stats: dict, encoder: str, container: str = "mp4", default: float = 1.03) -> float:
    key = f"{(encoder or 'x264').lower()}|{(container or 'mp4').lower()}"
    try:
        val = float(stats.get("overshoot", {}).get(key, default))
        if val <= 0.5 or val > 1.5:
            return default
        return val
    except Exception:
        return default

def update_overshoot(stats: dict, encoder: str, container: str, target_bytes: int, actual_bytes: int, lr: float = 0.1) -> dict:
    key = f"{(encoder or 'x264').lower()}|{(container or 'mp4').lower()}"
    try:

        ratio = max(0.95, min(1.10, actual_bytes / max(1, target_bytes)))
    except Exception:
        return stats
    cur = get_dynamic_overshoot(stats, encoder, container)
    target_factor = ratio

    new = (1.0 - lr) * cur + lr * target_factor
    new = max(1.00, min(1.08, new))

    stats.setdefault("overshoot", {})[key] = float(round(new, 4))
    return stats

def guardrail_adjust(actual_bytes: int, target_bytes: int, tol: float = 0.06) -> float | None:
    if actual_bytes > target_bytes * (1.0 + tol):
        return 0.9
    if actual_bytes < target_bytes * (1.0 - tol):
        return 1.1
    return None

def project_size_bytes(duration_sec: float, video_bps: int, audio_bps: int, container_overhead: float = 0.03) -> int:
    v = max(0, int(video_bps)); a = max(0, int(audio_bps))
    base = (v + a) / 8.0 * max(0.0, float(duration_sec))
    return int(base * (1.0 + max(0.0, float(container_overhead))))

def _hash_title(path: str) -> str:
    try:
        st = os.stat(path)
        h = hashlib.sha1()
        h.update(path.encode("utf-8", "ignore"))
        h.update(str(st.st_size).encode())
        h.update(str(int(st.st_mtime)).encode())
        return h.hexdigest()
    except Exception:
        import hashlib as _hashlib
        return _hashlib.sha1(path.encode("utf-8", "ignore")).hexdigest()

def cache_lookup(base_dir: str, input_path: str, target_mb: int, encoder: str) -> dict | None:
    
    try:
        with open(cache_path(base_dir), "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception:
        data = {}
    key = _hash_title(input_path)
    entry = data.get(key)
    if not isinstance(entry, dict):
        return None
    if entry.get("target_mb") != int(target_mb):
        return None
    if str(entry.get("encoder","")).lower() != str(encoder).lower():
        return None
    return entry

def cache_store(base_dir: str, input_path: str, target_mb: int, encoder: str, chosen_bitrate: int, width: int, fps: float, final_size: int) -> None:
    key = _hash_title(input_path)
    try:
        with open(cache_path(base_dir), "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception:
        data = {}
    data[key] = {
        "target_mb": int(target_mb),
        "encoder": encoder,
        "bitrate": int(chosen_bitrate),
        "width": int(width),
        "fps": float(fps),
        "final_size": int(final_size),
        "ts": int(time.time()),
    }
    tmp = cache_path(base_dir) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, cache_path(base_dir))

def pick_audio_bitrate(channels: int, sample_rate: int, fmt: str) -> int:
    
    fmt = (fmt or "aac").lower()

    if fmt == "opus":
        base = 64000 if channels <= 2 else 96000 + (channels-2)*24000
        floor = 48000
    else:
        base = 96000 if channels <= 2 else 128000 + (channels-2)*32000
        floor = 64000

    if (sample_rate or 48000) >= 48000:
        base = int(base * 1.05)
    return max(floor, base)

def choose_bitrates(duration_s: float,
                    target_bytes: int,
                    encoder: str = "x264",
                    container: str = "mp4",
                    channels: int = 2,
                    sample_rate: int = 48000,
                    audio_fmt: str = "aac",
                    stats_dir: str = ".smart"):
    
    stats = load_stats(stats_dir)

    ov_raw = get_dynamic_overshoot(stats, encoder, container, default=1.03)
    ov = max(1.00, min(1.08, float(ov_raw)))

    a_bps = pick_audio_bitrate(channels, sample_rate, audio_fmt)
    a_bytes = int((a_bps / 8.0) * max(1.0, duration_s))

    v_budget_nominal = max(int(target_bytes * 0.5), int(target_bytes - a_bytes))

    v_budget = int(v_budget_nominal / ov)

    v_bps = int((v_budget / max(1.0, duration_s)) * (8.0 / 1.03))

    if "265" in encoder.lower() or "hevc" in encoder.lower():
        v_bps = int(min(max(v_bps, 180_000), 12_000_000))
    elif "av1" in encoder.lower():
        v_bps = int(min(max(v_bps, 140_000), 10_000_000))
    else:  # x264 and friends
        v_bps = int(min(max(v_bps, 220_000), 16_000_000))

    return v_bps, a_bps, ov

def learn_from_result(stats_dir: str, encoder: str, container: str,
                      target_bytes: int, actual_bytes: int) -> None:
    s = load_stats(stats_dir)
    s = update_overshoot(s, encoder, container, target_bytes, actual_bytes, lr=0.25)
    save_stats(stats_dir, s)
