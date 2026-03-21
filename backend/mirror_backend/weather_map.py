"""Map Home Assistant weather condition strings → UI icon keys + readable labels."""

from __future__ import annotations

# HA state → key used by web/js/weather-icons.js WEATHER_ICON_MAP
HA_STATE_TO_ICON: dict[str, str] = {
    "clear-night": "clear",
    "sunny": "clear",
    "clear": "clear",
    "partlycloudy": "partly-cloudy",
    "partly-cloudy": "partly-cloudy",
    "cloudy": "cloudy",
    "rainy": "rain",
    "rain": "rain",
    "pouring": "rain",
    "snowy": "snow",
    "snowy-rainy": "snow",
    "snow": "snow",
    "lightning": "thunderstorm",
    "lightning-rainy": "thunderstorm",
    "thunderstorm": "thunderstorm",
    "fog": "fog",
    "hail": "rain",
    "windy": "wind",
    "windy-variant": "wind",
    "exceptional": "cloudy",
}

# Human label (title case friendly)
HA_STATE_TO_LABEL: dict[str, str] = {
    "partlycloudy": "Partly cloudy",
    "clear-night": "Clear",
    "lightning-rainy": "Thunderstorm",
    "snowy-rainy": "Snow / rain",
    "windy-variant": "Windy",
}


def weather_state_usable(state: str | None) -> bool:
    if state is None:
        return False
    s = str(state).strip().lower()
    return s not in ("unknown", "unavailable", "none", "")


def condition_icon_key(ha_state: str | None) -> str:
    if not weather_state_usable(ha_state):
        return "partly-cloudy"
    s = str(ha_state).lower().strip()
    return HA_STATE_TO_ICON.get(s, s.replace("_", "-"))


def condition_label(ha_state: str | None) -> str:
    if not weather_state_usable(ha_state):
        return "—"
    s = str(ha_state).lower().strip()
    if s in HA_STATE_TO_LABEL:
        return HA_STATE_TO_LABEL[s]
    return s.replace("-", " ").replace("_", " ").title()


def fahrenheit_from_ha_attrs(attrs: dict, key: str) -> int | None:
    v = attrs.get(key)
    if v is None:
        return None
    try:
        t = float(v)
        unit = (attrs.get("temperature_unit") or "").upper().replace("℉", "F")
        # Pirate Weather / Met.no may use °F or native °C
        if "C" in unit and "F" not in unit:
            return round(t * 9 / 5 + 32)
        return round(t)
    except (TypeError, ValueError):
        return None


def first_fahrenheit_from_attrs(attrs: dict, keys: tuple[str, ...]) -> int | None:
    for k in keys:
        v = fahrenheit_from_ha_attrs(attrs, k)
        if v is not None:
            return v
    return None
