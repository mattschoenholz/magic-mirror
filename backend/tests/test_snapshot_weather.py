"""Snapshot weather: hourly strip after *now*, weather_now chain."""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import patch

from mirror_backend.snapshot import (
    LA,
    _hourly_strip_next_six,
    _hourly_strip_relaxed,
    _weather_now_entity_chain,
    build_snapshot,
)


def test_weather_now_entity_chain_default_order() -> None:
    assert _weather_now_entity_chain({}) == [
        "weather.pirateweather",
        "weather.home",
        "weather.forecast_home",
    ]


def test_weather_now_entity_chain_override() -> None:
    cfg = {"entities": {"weather_now_entities": ["weather.a", "weather.b"]}}
    assert _weather_now_entity_chain(cfg) == ["weather.a", "weather.b"]


def test_hourly_strip_next_six_skips_current_bucket() -> None:
    now = datetime.now(LA)
    rows = []
    for h in range(-1, 8):
        dt = now + timedelta(hours=h)
        rows.append(
            {
                "datetime": dt.isoformat(),
                "temperature": 60 + h,
                "condition": "clear",
            }
        )
    slots = _hourly_strip_next_six(rows, "°F", count=6)
    assert len(slots) == 6
    assert all(s["hourLabel"] != "Now" for s in slots)
    # First slot is first row strictly after `now`
    assert slots[0]["tempF"] == 60 + 1


def test_hourly_strip_relaxed_includes_recent_bucket() -> None:
    now = datetime.now(LA)
    rows = [
        {
            "datetime": (now - timedelta(minutes=30)).isoformat(),
            "temperature": 55,
            "condition": "rainy",
        },
        {
            "datetime": (now + timedelta(hours=2)).isoformat(),
            "temperature": 56,
            "condition": "clear",
        },
    ]
    slots = _hourly_strip_relaxed(rows, "°F", count=6)
    assert len(slots) >= 1
    assert slots[0]["hourLabel"] != "Now"


@patch("mirror_backend.snapshot.ics_merge.get_merged_events")
@patch("mirror_backend.snapshot.read_ha_token")
@patch("mirror_backend.snapshot.ha_client.ha_get_todo_items")
@patch("mirror_backend.snapshot.ha_client.ha_get_forecasts")
@patch("mirror_backend.snapshot.ha_client.ha_get_state")
def test_build_snapshot_hourly_from_forecast_after_now(
    mock_state,
    mock_forecasts,
    mock_todo,
    mock_token,
    mock_merged,
) -> None:
    mock_merged.return_value = ([], [])
    mock_token.return_value = "secret"
    mock_todo.return_value = []
    mock_state.return_value = {
        "state": "clear-night",
        "attributes": {"temperature_unit": "°F", "temperature": 58},
    }
    now = datetime.now(LA)
    mock_forecasts.return_value = [
        {
            "datetime": (now - timedelta(hours=1)).isoformat(),
            "temperature": 57,
            "condition": "clear",
        },
        {
            "datetime": (now + timedelta(hours=1)).isoformat(),
            "temperature": 59,
            "condition": "cloudy",
        },
        {
            "datetime": (now + timedelta(hours=2)).isoformat(),
            "temperature": 60,
            "condition": "cloudy",
        },
        {
            "datetime": (now + timedelta(hours=3)).isoformat(),
            "temperature": 61,
            "condition": "rainy",
        },
        {
            "datetime": (now + timedelta(hours=4)).isoformat(),
            "temperature": 62,
            "condition": "rainy",
        },
        {
            "datetime": (now + timedelta(hours=5)).isoformat(),
            "temperature": 63,
            "condition": "sunny",
        },
        {
            "datetime": (now + timedelta(hours=6)).isoformat(),
            "temperature": 64,
            "condition": "sunny",
        },
    ]
    cfg = {
        "home_assistant": {"base_url": "http://ha.test"},
        "entities": {
            "weather_now_entities": ["weather.pirateweather"],
            "forecast_weather_entities": ["weather.pirateweather"],
            "todo_list": "todo.elliot",
        },
        "school_calendar": {"feeds": [], "max_events_per_day": 4},
    }
    snap = build_snapshot(cfg)
    hourly = snap["weather"]["hourlyToday"]
    assert len(hourly) == 6
    assert hourly[0]["tempF"] == 59
    assert all(h["hourLabel"] != "Now" for h in hourly)
    assert snap["weather"]["today"]["icon"]  # from clear-night state
