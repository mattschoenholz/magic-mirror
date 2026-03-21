"""Home Assistant REST + WebSocket service calls (token from disk only)."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
import websocket

logger = logging.getLogger(__name__)


def ha_get_state(base_url: str, token: str, entity_id: str) -> dict[str, Any] | None:
    url = f"{base_url.rstrip('/')}/api/states/{entity_id}"
    try:
        r = httpx.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=30.0,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("HA get_state %s failed: %s", entity_id, e)
        return None


def ha_post_service(
    base_url: str,
    token: str,
    domain: str,
    service: str,
    body: dict[str, Any],
) -> Any:
    """POST /api/services/<domain>/<service>; return parsed JSON or None."""
    url = f"{base_url.rstrip('/')}/api/services/{domain}/{service}"
    try:
        r = httpx.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=body,
            timeout=45.0,
        )
        r.raise_for_status()
        if not r.content:
            return None
        return r.json()
    except Exception as e:
        logger.warning("HA POST %s.%s failed: %s", domain, service, e)
        return None


def _ws_url(base_url: str) -> str:
    b = base_url.rstrip("/")
    if b.startswith("https://"):
        return "wss://" + b[len("https://") :] + "/api/websocket"
    if b.startswith("http://"):
        return "ws://" + b[len("http://") :] + "/api/websocket"
    return "ws://" + b + "/api/websocket"


def ha_ws_call_service(
    base_url: str,
    token: str,
    domain: str,
    service: str,
    *,
    target_entity_id: str | None = None,
    service_data: dict[str, Any] | None = None,
    return_response: bool = False,
) -> dict[str, Any] | None:
    """Run a single service call over HA WebSocket; return `result` payload or None.

    Set ``return_response=True`` for services that return data (e.g. ``weather.get_forecasts``,
    ``todo.get_items``). Without it, HA omits ``service_response`` and forecast/todo lists stay empty.
    """
    ws_url = _ws_url(base_url)
    ws: websocket.WebSocket | None = None
    try:
        ws = websocket.create_connection(ws_url, timeout=45)
        while True:
            raw = ws.recv()
            if not raw:
                break
            msg = json.loads(raw)
            t = msg.get("type")
            if t == "auth_required":
                ws.send(json.dumps({"type": "auth", "access_token": token}))
            elif t == "auth_ok":
                break
            elif t == "auth_invalid":
                logger.error("HA WebSocket auth_invalid")
                return None
        req_id = 57
        payload: dict[str, Any] = {
            "id": req_id,
            "type": "call_service",
            "domain": domain,
            "service": service,
        }
        if target_entity_id:
            payload["target"] = {"entity_id": target_entity_id}
        if service_data:
            payload["service_data"] = service_data
        if return_response:
            payload["return_response"] = True
        ws.send(json.dumps(payload))
        while True:
            raw = ws.recv()
            if not raw:
                break
            msg = json.loads(raw)
            if msg.get("id") == req_id and msg.get("type") == "result":
                if not msg.get("success"):
                    logger.warning("HA service %s.%s failed: %s", domain, service, msg)
                    return None
                return msg.get("result")
    except Exception as e:
        logger.warning("HA ws %s.%s: %s", domain, service, e)
        return None
    finally:
        if ws:
            try:
                ws.close()
            except Exception:
                pass
    return None


def _unwrap_service_response(res: Any) -> Any:
    """HA 2024+ puts response-returning service data under `service_response`."""
    if isinstance(res, dict) and "service_response" in res:
        inner = res.get("service_response")
        if inner is not None:
            return inner
    return res


def _extract_forecast_list(res: Any, entity_id: str) -> list[dict[str, Any]]:
    """Normalize get_forecasts service response → list of forecast dicts."""
    if not res:
        return []
    # WebSocket call_service + return_response → { context, response: { weather.x: { forecast } } }
    if isinstance(res, dict) and "response" in res:
        return _extract_forecast_list(res.get("response"), entity_id)
    res = _unwrap_service_response(res)
    if isinstance(res, list):
        return [x for x in res if isinstance(x, dict)]
    if not isinstance(res, dict):
        return []
    top_fc = res.get("forecast")
    if isinstance(top_fc, list) and top_fc and isinstance(top_fc[0], dict):
        if "datetime" in top_fc[0] or "temperature" in top_fc[0]:
            return [x for x in top_fc if isinstance(x, dict)]
    block = res.get(entity_id)
    if isinstance(block, dict):
        for key in ("forecast", "native_forecast", "hourly"):
            fc = block.get(key)
            if isinstance(fc, list):
                return [x for x in fc if isinstance(x, dict)]
    for _k, block in res.items():
        if isinstance(block, dict):
            for key in ("forecast", "native_forecast", "hourly"):
                fc = block.get(key)
                if isinstance(fc, list):
                    return [x for x in fc if isinstance(x, dict)]
    return []


def ha_get_forecasts(base_url: str, token: str, entity_id: str) -> list[dict[str, Any]]:
    # HA services.yaml: target = weather entity; fields = { type } only — not entity_id in service_data.
    res = ha_ws_call_service(
        base_url,
        token,
        "weather",
        "get_forecasts",
        target_entity_id=entity_id,
        service_data={"type": "hourly"},
        return_response=True,
    )
    rows = _extract_forecast_list(res, entity_id)
    if rows:
        return rows
    res_legacy = ha_ws_call_service(
        base_url,
        token,
        "weather",
        "get_forecasts",
        service_data={"entity_id": entity_id, "type": "hourly"},
        return_response=True,
    )
    rows = _extract_forecast_list(res_legacy, entity_id)
    if rows:
        return rows
    rest = ha_post_service(
        base_url,
        token,
        "weather",
        "get_forecasts",
        {"entity_id": entity_id, "type": "hourly"},
    )
    return _extract_forecast_list(rest, entity_id)


def _extract_todo_items(res: Any, entity_id: str) -> list[dict[str, Any]]:
    """Normalize get_items response (shape varies by HA version)."""
    if not res:
        return []
    if isinstance(res, dict) and "service_response" in res:
        return _extract_todo_items(res.get("service_response"), entity_id)
    if isinstance(res, dict) and "response" in res:
        return _extract_todo_items(res.get("response"), entity_id)
    if isinstance(res, list):
        return [x for x in res if isinstance(x, dict)]
    if not isinstance(res, dict):
        return []
    top = res.get("items")
    if isinstance(top, list):
        return [x for x in top if isinstance(x, dict)]
    block = res.get(entity_id)
    if isinstance(block, dict):
        items = block.get("items")
        if isinstance(items, list):
            return [x for x in items if isinstance(x, dict)]
    for _k, block in res.items():
        if isinstance(block, dict):
            items = block.get("items")
            if isinstance(items, list):
                return [x for x in items if isinstance(x, dict)]
    return []


def ha_get_todo_items(base_url: str, token: str, entity_id: str) -> list[dict[str, Any]]:
    res = ha_ws_call_service(
        base_url,
        token,
        "todo",
        "get_items",
        target_entity_id=entity_id,
        return_response=True,
    )
    items = _extract_todo_items(res, entity_id)
    if items:
        return items
    res2 = ha_ws_call_service(
        base_url,
        token,
        "todo",
        "get_items",
        service_data={"entity_id": entity_id},
        return_response=True,
    )
    items = _extract_todo_items(res2, entity_id)
    if items:
        return items
    rest = ha_post_service(
        base_url,
        token,
        "todo",
        "get_items",
        {"entity_id": entity_id},
    )
    return _extract_todo_items(rest, entity_id)
