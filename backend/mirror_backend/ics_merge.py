"""Fetch, cache, and merge school ICS feeds → calendar events for the UI."""

from __future__ import annotations

import logging
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import httpx
from icalendar import Calendar

logger = logging.getLogger(__name__)

LA = ZoneInfo("America/Los_Angeles")


@dataclass
class ICSCache:
    merged_events: list[dict[str, Any]] = field(default_factory=list)
    fetched_at: float = 0.0
    errors: list[str] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)


_cache = ICSCache()


def _ensure_la(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=LA)
    return dt.astimezone(LA)


def _normalize_vevent(component) -> list[dict[str, Any]]:
    """One VEVENT → one or more normalized dicts (v1: no RRULE expansion)."""
    out: list[dict[str, Any]] = []
    if "DTSTART" not in component:
        return out
    raw_uid = component.get("uid")
    uid = str(raw_uid).strip() if raw_uid is not None else ""
    summary = str(component.get("summary", "")).strip() or "Event"
    loc = component.get("location")
    location = str(loc).strip() if loc else ""

    start = component.decoded("DTSTART")
    end = component.decoded("DTEND") if "DTEND" in component else None

    if isinstance(start, datetime):
        start_la = _ensure_la(start)
        if end is None:
            end_la = start_la + timedelta(hours=1)
        elif isinstance(end, datetime):
            end_la = _ensure_la(end)
        else:
            end_la = start_la + timedelta(hours=1)
        out.append(
            {
                "uid": uid,
                "title": summary,
                "location": location,
                "start": start_la,
                "end": end_la,
                "all_day": False,
            }
        )
        return out

    # All-day: start is date. DTEND (date) is exclusive per RFC5545.
    d0 = start if isinstance(start, date) else start.date()
    if end is None:
        d1_exc = d0 + timedelta(days=1)
    elif isinstance(end, datetime):
        d1_exc = end.date()
    else:
        d1_exc = end
    last_inclusive = d1_exc - timedelta(days=1)
    if last_inclusive < d0:
        last_inclusive = d0
    out.append(
        {
            "uid": uid,
            "title": summary,
            "location": location,
            "start": d0,
            "end": last_inclusive,
            "all_day": True,
        }
    )
    return out


def _dates_for_event(ev: dict[str, Any]) -> list[tuple[date, bool, datetime | None]]:
    """(local_date, all_day, start_datetime or None for sort)."""
    start = ev["start"]
    all_day = ev["all_day"]
    if all_day:
        d0 = start if isinstance(start, date) else start.date()
        end = ev["end"]
        d1 = end if isinstance(end, date) else end.date()
        days: list[tuple[date, bool, datetime | None]] = []
        d = d0
        while d <= d1:
            days.append((d, True, None))
            d += timedelta(days=1)
        return days
    assert isinstance(start, datetime)
    sd = _ensure_la(start).date()
    return [(sd, False, _ensure_la(start))]


def _parse_calendar_bytes(data: bytes, source_name: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        cal = Calendar.from_ical(data)
    except Exception as e:
        logger.warning("ICS parse %s: %s", source_name, e)
        return events

    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        for ev in _normalize_vevent(component):
            ev["source"] = source_name
            events.append(ev)
    return events


def _fetch_feed(url: str, user_agent: str, referer: str | None = None) -> bytes | None:
    try:
        headers: dict[str, str] = {
            "User-Agent": user_agent,
            "Accept": "text/calendar,*/*;q=0.9",
        }
        if referer:
            headers["Referer"] = referer
        r = httpx.get(
            url,
            headers=headers,
            timeout=60.0,
            follow_redirects=True,
        )
        r.raise_for_status()
        return r.content
    except Exception as e:
        logger.warning("ICS fetch %s: %s", url, e)
        return None


def refresh_ics_cache(cfg: dict[str, Any]) -> None:
    sch = cfg.get("school_calendar") or {}
    feeds = sch.get("feeds") or []
    ua = sch.get("user_agent") or "MagicMirrorFamily/1.0"
    referer = sch.get("http_referer")
    errors: list[str] = []
    by_uid: dict[str, dict[str, Any]] = {}

    for feed in feeds:
        url = feed.get("url")
        name = feed.get("name") or url
        if not url:
            continue
        raw = _fetch_feed(url, ua, referer)
        if raw is None:
            errors.append(f"fetch:{name}")
            continue
        for ev in _parse_calendar_bytes(raw, name):
            uid = str(ev.get("uid") or "").strip()
            # Unique per feed+uid+start+title so blank/duplicate UIDs do not drop events across feeds.
            dedupe_key = f"{name}|{uid}|{ev['start']!s}|{ev['title']}"
            by_uid[dedupe_key] = ev

    merged = list(by_uid.values())
    with _cache.lock:
        _cache.merged_events = merged
        _cache.fetched_at = time.time()
        _cache.errors = errors


def get_merged_events(cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    sch = cfg.get("school_calendar") or {}
    interval = int(sch.get("refresh_seconds") or 900)
    with _cache.lock:
        age = time.time() - _cache.fetched_at
        stale = age > interval or _cache.fetched_at == 0.0
    if stale:
        refresh_ics_cache(cfg)
    with _cache.lock:
        return list(_cache.merged_events), list(_cache.errors)


def _format_time_ampm(dt: datetime) -> str:
    t = _ensure_la(dt)
    h24 = t.hour
    h12 = h24 % 12
    if h12 == 0:
        h12 = 12
    am = "AM" if h24 < 12 else "PM"
    return f"{h12}:{t.minute:02d} {am}"


def events_for_ui_window(
    merged: list[dict[str, Any]],
    now: datetime | None = None,
    *,
    max_per_day: int = 4,
) -> list[dict[str, Any]]:
    """Produce { offsetFromToday, time, title } for today..today+4 in LA."""
    now = now or datetime.now(LA)
    today = now.date()
    window_end = today + timedelta(days=4)
    rows: list[dict[str, Any]] = []
    cap = max(1, int(max_per_day))

    for ev in merged:
        title = ev["title"]
        if ev.get("location"):
            title = f"{title} — {ev['location']}"
        for d, all_day, start_dt in _dates_for_event(ev):
            if d < today or d > window_end:
                continue
            offset = (d - today).days
            if all_day:
                time_s = ""
                sort_key = (offset, 0)
            else:
                time_s = _format_time_ampm(start_dt) if start_dt else ""
                mm = start_dt.hour * 60 + start_dt.minute if start_dt else 0
                sort_key = (offset, mm)
            rows.append(
                {
                    "offsetFromToday": offset,
                    "time": time_s,
                    "title": title,
                    "_sk": sort_key,
                }
            )

    rows.sort(key=lambda x: (x["_sk"][0], x["_sk"][1], x["title"]))

    per_day: dict[int, int] = defaultdict(int)
    capped: list[dict[str, Any]] = []
    for r in rows:
        o = r["offsetFromToday"]
        if per_day[o] >= cap:
            continue
        per_day[o] += 1
        del r["_sk"]
        capped.append(r)
    return capped
