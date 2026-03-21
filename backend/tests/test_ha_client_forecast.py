"""Unit tests for HA weather forecast response normalization."""

from __future__ import annotations

from mirror_backend.ha_client import _extract_forecast_list


def test_extract_forecast_websocket_context_response_envelope() -> None:
    """HA WebSocket returns result = { context, response: { entity_id: { forecast } } }."""
    payload = {
        "context": {"id": "abc", "parent_id": None, "user_id": None},
        "response": {
            "weather.home": {
                "forecast": [
                    {"datetime": "2026-03-21T20:00:00+00:00", "temperature": 51, "condition": "sunny"}
                ]
            }
        },
    }
    rows = _extract_forecast_list(payload, "weather.home")
    assert len(rows) == 1
    assert rows[0]["temperature"] == 51


def test_extract_forecast_service_response_open_meteo_shape() -> None:
    payload = {
        "service_response": {
            "weather.home": {
                "forecast": [
                    {
                        "datetime": "2026-03-21T20:00:00+00:00",
                        "condition": "sunny",
                        "temperature": 51,
                    }
                ]
            }
        }
    }
    rows = _extract_forecast_list(payload, "weather.home")
    assert len(rows) == 1
    assert rows[0]["temperature"] == 51


def test_extract_forecast_top_level_forecast_list() -> None:
    payload = {
        "forecast": [
            {"datetime": "2026-03-21T15:00:00+00:00", "temperature": 55, "condition": "cloudy"}
        ]
    }
    rows = _extract_forecast_list(payload, "weather.home")
    assert len(rows) == 1
    assert rows[0]["temperature"] == 55


def test_extract_forecast_legacy_entity_key() -> None:
    payload = {
        "weather.pirateweather": {
            "forecast": [{"datetime": "2026-03-21T12:00:00+00:00", "temperature": 60}]
        }
    }
    rows = _extract_forecast_list(payload, "weather.pirateweather")
    assert len(rows) == 1
