"""Snapshot assembly: todo chain and HA-backed todo rows."""

from __future__ import annotations

from unittest.mock import patch

from mirror_backend.snapshot import _todo_entity_chain, build_snapshot


def test_todo_entity_chain_default() -> None:
    assert _todo_entity_chain({}) == ["todo.elliot"]


def test_todo_entity_chain_todo_list() -> None:
    cfg = {"entities": {"todo_list": "todo.custom"}}
    assert _todo_entity_chain(cfg) == ["todo.custom"]


def test_todo_entity_chain_todo_entities_wins() -> None:
    cfg = {"entities": {"todo_list": "todo.a", "todo_entities": ["todo.b", "todo.c"]}}
    assert _todo_entity_chain(cfg) == ["todo.b", "todo.c"]


def test_todo_entity_chain_skips_empty_list_entries() -> None:
    cfg = {"entities": {"todo_entities": ["", "  ", "todo.x"]}}
    assert _todo_entity_chain(cfg) == ["todo.x"]


@patch("mirror_backend.snapshot.ics_merge.get_merged_events")
@patch("mirror_backend.snapshot.read_ha_token")
@patch("mirror_backend.snapshot.ha_client.ha_get_todo_items")
@patch("mirror_backend.snapshot.ha_client.ha_get_forecasts")
@patch("mirror_backend.snapshot.ha_client.ha_get_state")
def test_build_snapshot_todos_from_ha(
    mock_state,
    mock_forecasts,
    mock_todo,
    mock_token,
    mock_merged,
) -> None:
    mock_merged.return_value = ([], [])
    mock_token.return_value = "secret"
    mock_state.return_value = {
        "state": "sunny",
        "attributes": {"temperature_unit": "°F", "apparent_temperature": 72},
    }
    mock_forecasts.return_value = []
    mock_todo.return_value = [
        {"uid": "1", "summary": "Math", "status": "needs_action"},
        {"title": "Reading", "status": "completed"},
    ]

    cfg = {
        "home_assistant": {"base_url": "http://ha.test"},
        "entities": {
            "weather_entities": ["weather.one"],
            "todo_list": "todo.elliot",
        },
        "school_calendar": {"feeds": [], "max_events_per_day": 4},
    }
    snap = build_snapshot(cfg)

    assert snap["todos"]["items"] == [
        {"text": "Math", "done": False},
        {"text": "Reading", "done": True},
    ]
    assert "ha:forecast_hourly_empty" in snap["errors"]
    mock_todo.assert_called()


@patch("mirror_backend.snapshot.ics_merge.get_merged_events")
@patch("mirror_backend.snapshot.read_ha_token")
@patch("mirror_backend.snapshot.ha_client.ha_get_todo_items")
@patch("mirror_backend.snapshot.ha_client.ha_get_forecasts")
@patch("mirror_backend.snapshot.ha_client.ha_get_state")
def test_build_snapshot_todos_over_six_shows_only_active(
    mock_state,
    mock_forecasts,
    mock_todo,
    mock_token,
    mock_merged,
) -> None:
    mock_merged.return_value = ([], [])
    mock_token.return_value = "secret"
    mock_state.return_value = {
        "state": "sunny",
        "attributes": {"temperature_unit": "°F", "apparent_temperature": 72},
    }
    mock_forecasts.return_value = []
    items = []
    for i in range(10):
        items.append(
            {
                "uid": str(i),
                "title": f"T{i}",
                "status": "completed" if i < 4 else "needs_action",
            }
        )
    mock_todo.return_value = items

    cfg = {
        "home_assistant": {"base_url": "http://ha.test"},
        "entities": {
            "weather_entities": ["weather.one"],
            "todo_list": "todo.elliot",
        },
        "school_calendar": {"feeds": [], "max_events_per_day": 4},
    }
    snap = build_snapshot(cfg)
    assert len(snap["todos"]["items"]) == 6
    assert all(not t["done"] for t in snap["todos"]["items"])
    assert [t["text"] for t in snap["todos"]["items"]] == [
        "T4",
        "T5",
        "T6",
        "T7",
        "T8",
        "T9",
    ]


@patch("mirror_backend.snapshot.ics_merge.get_merged_events")
@patch("mirror_backend.snapshot.read_ha_token")
@patch("mirror_backend.snapshot.ha_client.ha_get_todo_items")
@patch("mirror_backend.snapshot.ha_client.ha_get_forecasts")
@patch("mirror_backend.snapshot.ha_client.ha_get_state")
def test_build_snapshot_todo_entities_merge_dedupe(
    mock_state,
    mock_forecasts,
    mock_todo,
    mock_token,
    mock_merged,
) -> None:
    mock_merged.return_value = ([], [])
    mock_token.return_value = "secret"
    mock_state.return_value = {
        "state": "clear",
        "attributes": {"temperature_unit": "°F", "temperature": 70},
    }
    mock_forecasts.return_value = []

    def todo_side_effect(_base: str, _token: str, eid: str) -> list:
        if eid == "todo.first":
            return [{"uid": "a", "title": "One", "status": "needs_action"}]
        if eid == "todo.second":
            return [
                {"uid": "a", "title": "Dup", "status": "needs_action"},
                {"title": "Two", "status": "needs_action"},
            ]
        return []

    mock_todo.side_effect = todo_side_effect

    cfg = {
        "home_assistant": {"base_url": "http://ha.test"},
        "entities": {
            "weather_entities": ["weather.one"],
            "todo_entities": ["todo.first", "todo.second"],
        },
        "school_calendar": {"feeds": [], "max_events_per_day": 4},
    }
    snap = build_snapshot(cfg)

    assert snap["todos"]["items"] == [
        {"text": "One", "done": False},
        {"text": "Two", "done": False},
    ]
    assert "ha:forecast_hourly_empty" in snap["errors"]
