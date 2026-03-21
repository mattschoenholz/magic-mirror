"""Load YAML config + secrets paths (no secret values in repo)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    """App root = parent of `backend/` (contains `web/`, `config/`). Override on Pi: `MIRROR_REPO_ROOT`."""
    env = os.environ.get("MIRROR_REPO_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    # Dev clone: .../magic-mirror/backend/mirror_backend/settings.py → repo root
    return Path(__file__).resolve().parents[2]


REPO_ROOT = repo_root()
EXAMPLE_CONFIG = REPO_ROOT / "config" / "mirror.runtime.example.yaml"
LOCAL_CONFIG = REPO_ROOT / "config" / "mirror.runtime.local.yaml"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_runtime_config() -> dict[str, Any]:
    with open(EXAMPLE_CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if LOCAL_CONFIG.is_file():
        with open(LOCAL_CONFIG, encoding="utf-8") as f:
            local = yaml.safe_load(f) or {}
        cfg = _deep_merge(cfg, local)
    ha_url = os.environ.get("MIRROR_HA_URL")
    if ha_url:
        cfg.setdefault("home_assistant", {})["base_url"] = ha_url.rstrip("/")
    return cfg


def secrets_dir() -> Path:
    env = os.environ.get("MIRROR_SECRETS_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".config" / "mirror"


def ha_token_path() -> Path:
    override = os.environ.get("MIRROR_HA_TOKEN_FILE")
    if override:
        return Path(override).expanduser()
    return secrets_dir() / "ha_token"


def read_ha_token() -> str | None:
    path = ha_token_path()
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8").strip()
    return raw or None
