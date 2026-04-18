"""Spotify Web API: token refresh + currently-playing."""

from __future__ import annotations

import base64
import logging
import time
from typing import Any

import httpx

from mirror_backend.settings import secrets_dir

logger = logging.getLogger(__name__)

_TOKEN_URL = "https://accounts.spotify.com/api/token"
_NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
_QUEUE_URL = "https://api.spotify.com/v1/me/player/queue"

_access_token: str | None = None
_token_expires_at: float = 0.0


def _read_secret(name: str) -> str | None:
    path = secrets_dir() / name
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def _refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str | None:
    global _access_token, _token_expires_at
    creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    try:
        r = httpx.post(
            _TOKEN_URL,
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            headers={"Authorization": f"Basic {creds}"},
            timeout=8,
        )
        r.raise_for_status()
        data = r.json()
        _access_token = data["access_token"]
        _token_expires_at = time.monotonic() + data.get("expires_in", 3600) - 60
        return _access_token
    except Exception as exc:
        logger.warning("Spotify token refresh failed: %s", exc)
        return None


def _get_access_token() -> str | None:
    global _access_token, _token_expires_at
    client_id = _read_secret("spotify_client_id")
    client_secret = _read_secret("spotify_client_secret")
    refresh_token = _read_secret("spotify_refresh_token")
    if not (client_id and client_secret and refresh_token):
        return None
    if _access_token and time.monotonic() < _token_expires_at:
        return _access_token
    return _refresh_access_token(client_id, client_secret, refresh_token)


def get_now_playing() -> dict[str, Any]:
    """Return nowPlaying dict. Falls back to isIdle=True on any error or no playback."""
    idle: dict[str, Any] = {"title": "", "artist": "", "artworkUrl": "", "isIdle": True, "nextUp": None}
    token = _get_access_token()
    if not token:
        return idle
    try:
        r = httpx.get(
            _NOW_PLAYING_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=8,
        )
        if r.status_code == 204 or not r.content:
            return idle
        r.raise_for_status()
        data = r.json()
    except Exception as exc:
        logger.warning("Spotify now-playing fetch failed: %s", exc)
        return idle

    if not data or data.get("currently_playing_type") != "track":
        return idle
    item = data.get("item") or {}
    if not item:
        return idle

    title = item.get("name", "")
    artists = ", ".join(a.get("name", "") for a in item.get("artists", []))
    images = (item.get("album") or {}).get("images") or []
    artwork = images[0].get("url", "") if images else ""

    next_up = None
    try:
        q = httpx.get(_QUEUE_URL, headers={"Authorization": f"Bearer {token}"}, timeout=8)
        if q.status_code == 200 and q.content:
            queue = q.json().get("queue") or []
            if queue:
                nxt = queue[0]
                next_up = {
                    "title": nxt.get("name", ""),
                    "artist": ", ".join(a.get("name", "") for a in nxt.get("artists", [])),
                }
    except Exception as exc:
        logger.warning("Spotify queue fetch failed: %s", exc)

    return {"title": title, "artist": artists, "artworkUrl": artwork, "isIdle": False, "nextUp": next_up}
