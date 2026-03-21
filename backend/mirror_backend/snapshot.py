"""Assemble `/api/snapshot` payload matching `web/js/demo-data.js` shape."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from mirror_backend import ha_client, ics_merge, weather_map
from mirror_backend.settings import read_ha_token

logger = logging.getLogger(__name__)

LA = ZoneInfo("America/Los_Angeles")


def _parse_forecast_dt(row: dict[str, Any]) -> datetime | None:
    raw_dt = row.get("datetime")
    if not raw_dt:
        return None
    try:
        if isinstance(raw_dt, datetime):
            dt = raw_dt
        else:
            s = str(raw_dt).replace("Z", "+00:00")
            dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=LA)
    return dt.astimezone(LA)


def _row_temp_f(row: dict[str, Any], entity_temp_unit: str | None) -> int | None:
    temp = row.get("temperature")
    if temp is None:
        temp = row.get("native_temperature")
    if temp is None:
        return None
    try:
        t = float(temp)
    except (TypeError, ValueError):
        return None
    u = (row.get("native_temperature_unit") or entity_temp_unit or "").upper().replace("℉", "F")
    if "C" in u and "F" not in u:
        return round(t * 9 / 5 + 32)
    return round(t)


def _hourly_strip_next_six(
    forecast: list[dict[str, Any]],
    temp_unit_hint: str | None,
    *,
    count: int = 6,
) -> list[dict[str, Any]]:
    """Six hourly slots after *now* — big card is “now”; strip starts at next forecast period (no ‘Now’ label)."""
    now = datetime.now(LA)
    slots: list[dict[str, Any]] = []
    for row in forecast[:72]:
        dt = _parse_forecast_dt(row)
        if dt is None:
            continue
        if dt <= now:
            continue
        temp_f = _row_temp_f(row, temp_unit_hint)
        if temp_f is None:
            continue
        cond = row.get("condition") or row.get("weather") or "cloudy"
        icon = weather_map.condition_icon_key(str(cond))
        h12 = dt.hour % 12 or 12
        label = f"{h12}:{dt.minute:02d} {'PM' if dt.hour >= 12 else 'AM'}"
        slots.append({"hourLabel": label, "tempF": temp_f, "icon": icon})
        if len(slots) >= count:
            break
    return slots


def _hourly_strip_relaxed(
    forecast: list[dict[str, Any]],
    temp_unit_hint: str | None,
    *,
    count: int = 6,
) -> list[dict[str, Any]]:
    """Fallback: next periods from ~1h ago (clock skew), still no ‘Now’ label."""
    now = datetime.now(LA)
    slots: list[dict[str, Any]] = []
    for row in forecast[:72]:
        dt = _parse_forecast_dt(row)
        if dt is None:
            continue
        if dt < now - timedelta(hours=1):
            continue
        temp_f = _row_temp_f(row, temp_unit_hint)
        if temp_f is None:
            continue
        cond = row.get("condition") or row.get("weather") or "cloudy"
        icon = weather_map.condition_icon_key(str(cond))
        h12 = dt.hour % 12 or 12
        label = f"{h12}:{dt.minute:02d} {'PM' if dt.hour >= 12 else 'AM'}"
        slots.append({"hourLabel": label, "tempF": temp_f, "icon": icon})
        if len(slots) >= count:
            break
    return slots


def _weather_entity_chain(cfg: dict[str, Any]) -> list[str]:
    ent = cfg.get("entities") or {}
    chain = ent.get("weather_entities")
    if isinstance(chain, list) and chain:
        return [str(x) for x in chain if x]
    primary = ent.get("weather") or "weather.pirateweather"
    return [str(primary)]


def _forecast_entity_chain(cfg: dict[str, Any]) -> list[str]:
    """Entities to try for `weather.get_forecasts` (hourly). Explicit list wins; else `weather_entities` with Pirate first if present."""
    ent = cfg.get("entities") or {}
    chain = ent.get("forecast_weather_entities")
    if isinstance(chain, list) and chain:
        out = [str(x).strip() for x in chain if x and str(x).strip()]
        if out:
            return out
    base = _weather_entity_chain(cfg)
    if "weather.pirateweather" in base:
        others = [x for x in base if x != "weather.pirateweather"]
        return ["weather.pirateweather", *others]
    return base


def _weather_now_entity_chain(cfg: dict[str, Any]) -> list[str]:
    """Large ‘current conditions’ tile — try in order (default: Pirate Weather first for accurate *now*)."""
    ent = cfg.get("entities") or {}
    chain = ent.get("weather_now_entities")
    if isinstance(chain, list) and chain:
        out = [str(x).strip() for x in chain if x and str(x).strip()]
        if out:
            return out
    return [
        "weather.pirateweather",
        "weather.home",
        "weather.forecast_home",
    ]


def _todo_entity_chain(cfg: dict[str, Any]) -> list[str]:
    """Ordered HA todo list entity_ids. Friendly HA names (e.g. Local To-do) are not entity_ids."""
    ent = cfg.get("entities") or {}
    chain = ent.get("todo_entities")
    if isinstance(chain, list) and chain:
        out = [str(x).strip() for x in chain if x and str(x).strip()]
        if out:
            return out
    single = ent.get("todo_list")
    if isinstance(single, str) and single.strip():
        return [single.strip()]
    return ["todo.elliot"]


def build_snapshot(cfg: dict[str, Any]) -> dict[str, Any]:
    token = read_ha_token()
    ha = cfg.get("home_assistant") or {}
    base_url = (ha.get("base_url") or "http://homeassistant.local:8123").rstrip("/")
    ent = cfg.get("entities") or {}
    todo_entity_ids = _todo_entity_chain(cfg)
    weather_ids = _weather_entity_chain(cfg)
    now_weather_ids = _weather_now_entity_chain(cfg)
    forecast_ids = _forecast_entity_chain(cfg)

    errors: list[str] = []
    weather_today: dict[str, Any] = {
        "condition": "—",
        "feelsLikeF": None,
        "precipChance": None,
        "icon": "partly-cloudy",
    }
    hourly_today: list[dict[str, Any]] = []
    todo_items: list[dict[str, Any]] = []

    sch = cfg.get("school_calendar") or {}
    max_per_day = int(sch.get("max_events_per_day") or 4)

    merged, ics_errors = ics_merge.get_merged_events(cfg)
    if ics_errors:
        errors.extend(ics_errors)

    calendar_events = ics_merge.events_for_ui_window(merged, max_per_day=max_per_day)

    if not token:
        errors.append("ha:no_token")
    else:
        chosen_state: dict[str, Any] | None = None
        chosen_eid: str | None = None
        for eid in now_weather_ids:
            st = ha_client.ha_get_state(base_url, token, eid)
            if not st:
                errors.append(f"ha:weather_now_missing:{eid}")
                continue
            state = st.get("state")
            if weather_map.weather_state_usable(state):
                chosen_state = st
                chosen_eid = eid
                break
            logger.info("Skipping weather_now entity %s state=%r", eid, state)

        if not chosen_state:
            for eid in weather_ids:
                st = ha_client.ha_get_state(base_url, token, eid)
                if not st:
                    errors.append(f"ha:weather_missing:{eid}")
                    continue
                state = st.get("state")
                if weather_map.weather_state_usable(state):
                    chosen_state = st
                    chosen_eid = eid
                    break
                logger.info("Skipping weather entity %s state=%r", eid, state)

        if chosen_state and chosen_eid:
            attrs = chosen_state.get("attributes") or {}
            state = chosen_state.get("state")
            weather_today["condition"] = weather_map.condition_label(state)
            weather_today["icon"] = weather_map.condition_icon_key(state)
            weather_today["feelsLikeF"] = weather_map.first_fahrenheit_from_attrs(
                attrs,
                ("apparent_temperature", "temperature", "native_temperature"),
            )

            fc: list[dict[str, Any]] = []
            forecast_eid: str | None = None
            for eid in forecast_ids:
                fc = ha_client.ha_get_forecasts(base_url, token, eid)
                if fc:
                    forecast_eid = eid
                    break
            if not fc:
                errors.append("ha:forecast_hourly_empty")
            fc_state = (
                ha_client.ha_get_state(base_url, token, forecast_eid)
                if forecast_eid
                else None
            )
            fc_attrs = (fc_state.get("attributes") or {}) if fc_state else {}
            temp_hint = fc_attrs.get("temperature_unit") or attrs.get("temperature_unit")
            hourly_today = _hourly_strip_next_six(fc, temp_hint, count=6)
            if fc and not hourly_today:
                hourly_today = _hourly_strip_relaxed(fc, temp_hint, count=6)
            for row in fc[:24]:
                for key in (
                    "precipitation_probability",
                    "precipitation",
                    "native_precipitation",
                    "native_precipitation_intensity",
                ):
                    p = row.get(key)
                    if p is not None:
                        try:
                            weather_today["precipChance"] = int(round(float(p)))
                            break
                        except (TypeError, ValueError):
                            pass
                if weather_today["precipChance"] is not None:
                    break
        else:
            errors.append("ha:weather_no_usable_entity")

        seen_keys: set[str] = set()
        todo_cap = 24
        for todo_entity in todo_entity_ids:
            raw_items = ha_client.ha_get_todo_items(base_url, token, todo_entity)
            for it in raw_items:
                summary = (
                    it.get("title")
                    or it.get("summary")
                    or it.get("name")
                    or it.get("subject")
                    or ""
                )
                if isinstance(summary, str):
                    summary = summary.strip()
                else:
                    summary = str(summary).strip()
                if not summary:
                    continue
                uid = str(it.get("uid") or it.get("id") or "").strip()
                dedupe = uid if uid else summary.lower()
                if dedupe in seen_keys:
                    continue
                seen_keys.add(dedupe)
                status = str(it.get("status") or "").lower()
                done = status in ("completed", "complete") or it.get("completed") is True
                todo_items.append({"text": summary, "done": done})
                if len(todo_items) >= todo_cap:
                    break
            if len(todo_items) >= todo_cap:
                break

        if len(todo_items) > 6:
            todo_items = [t for t in todo_items if not t["done"]][:6]

    # Hourly strip: six slots after *now*; empty list lets the UI show a friendly message.

    return {
        "source": "live" if token else "degraded",
        "errors": errors,
        "nowPlaying": {
            "title": "",
            "artist": "",
            "artworkUrl": "",
            "isIdle": True,
            "nextUp": None,
        },
        "weather": {
            "today": weather_today,
            "hourlyToday": hourly_today,
        },
        "calendar": {"events": calendar_events},
        "todos": {"items": todo_items},
        "videoRadar": {"videos": []},
    }
