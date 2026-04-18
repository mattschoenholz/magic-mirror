"""YouTube Data API v3: subscriptions recent uploads for Video Radar."""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from mirror_backend.settings import secrets_dir

logger = logging.getLogger(__name__)

_TOKEN_URL = "https://oauth2.googleapis.com/token"
_ACTIVITIES_URL = "https://www.googleapis.com/youtube/v3/activities"
_SUBSCRIPTIONS_URL = "https://www.googleapis.com/youtube/v3/subscriptions"

_access_token: str | None = None
_token_expires_at: float = 0.0

# Cache results to avoid hammering the quota on every snapshot call.
_cache: list[dict[str, Any]] = []
_cache_until: float = 0.0
_CACHE_TTL = 900.0  # 15 minutes


def _read_secret(name: str) -> str | None:
    path = secrets_dir() / name
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def _get_access_token() -> str | None:
    global _access_token, _token_expires_at
    client_id = _read_secret("youtube_client_id")
    client_secret = _read_secret("youtube_client_secret")
    refresh_token = _read_secret("youtube_refresh_token")
    if not (client_id and client_secret and refresh_token):
        return None
    if _access_token and time.monotonic() < _token_expires_at:
        return _access_token
    try:
        r = httpx.post(
            _TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=8,
        )
        r.raise_for_status()
        data = r.json()
        _access_token = data["access_token"]
        _token_expires_at = time.monotonic() + data.get("expires_in", 3600) - 60
        return _access_token
    except Exception as exc:
        logger.warning("YouTube token refresh failed: %s", exc)
        return None


def _ago(published: str) -> str:
    """Human-readable age string from ISO 8601 timestamp."""
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            return "just now"
        if hours < 24:
            return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except Exception:
        return ""


def get_video_radar(max_results: int = 3) -> list[dict[str, Any]]:
    """Return list of recent subscription uploads for the Video Radar. Empty on any error."""
    global _cache, _cache_until
    if time.monotonic() < _cache_until:
        return _cache

    token = _get_access_token()
    if not token:
        return []

    headers = {"Authorization": f"Bearer {token}"}
    videos: list[dict[str, Any]] = []

    try:
        # Fetch subscribed channel IDs
        r = httpx.get(
            _SUBSCRIPTIONS_URL,
            params={"part": "snippet", "mine": "true", "maxResults": 20, "order": "relevance"},
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        channel_ids = [
            item["snippet"]["resourceId"]["channelId"]
            for item in r.json().get("items", [])
        ]

        # Fetch recent uploads from each channel
        for channel_id in channel_ids:
            if len(videos) >= max_results:
                break
            try:
                a = httpx.get(
                    _ACTIVITIES_URL,
                    params={
                        "part": "snippet,contentDetails",
                        "channelId": channel_id,
                        "maxResults": 1,
                        "type": "upload",
                    },
                    headers=headers,
                    timeout=8,
                )
                a.raise_for_status()
                items = a.json().get("items", [])
                for item in items:
                    snippet = item.get("snippet", {})
                    if snippet.get("type") != "upload":
                        continue
                    videos.append({
                        "title": snippet.get("title", ""),
                        "creator": snippet.get("channelTitle", ""),
                        "publishedAt": snippet.get("publishedAt", ""),
                        "ago": _ago(snippet.get("publishedAt", "")),
                    })
            except Exception as exc:
                logger.debug("YouTube activity fetch failed for %s: %s", channel_id, exc)

        # Filter to past 24 hours, sort by most recent
        from datetime import datetime, timezone, timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        videos = [
            v for v in videos
            if datetime.fromisoformat(v["publishedAt"].replace("Z", "+00:00")) > cutoff
        ]
        videos.sort(key=lambda v: v.get("publishedAt", ""), reverse=True)
        videos = videos[:max_results]

    except Exception as exc:
        logger.warning("YouTube video radar failed: %s", exc)
        return []

    _cache = videos
    _cache_until = time.monotonic() + _CACHE_TTL
    return videos
