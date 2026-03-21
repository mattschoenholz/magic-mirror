"""FastAPI app: static `web/` + `/api/snapshot` (FR-006)."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from mirror_backend.settings import REPO_ROOT, load_runtime_config
from mirror_backend.snapshot import build_snapshot

logging.basicConfig(level=logging.INFO)

WEB_DIR = REPO_ROOT / "web"

# Bump when deploying so `curl /api/health` confirms the Pi picked up new backend code.
MIRROR_BACKEND_BUILD = "20260320-weather-now-hourly-todos"


class _NoCacheStaticMiddleware(BaseHTTPMiddleware):
    """Kiosk Chromium caches aggressive defaults; force reload of HTML/JS/CSS after deploy."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        path = request.url.path
        if not path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, max-age=0, must-revalidate"
            response.headers["Pragma"] = "no-cache"
        return response


app = FastAPI(title="Magic Mirror API", version="0.1.0")
app.add_middleware(_NoCacheStaticMiddleware)


@app.get("/api/snapshot")
def api_snapshot():
    cfg = load_runtime_config()
    return build_snapshot(cfg)


@app.get("/api/health")
def api_health():
    return {"ok": True, "mirror_backend_build": MIRROR_BACKEND_BUILD}


# Register API routes before `/` mount. Starlette matches specific routes first.
if WEB_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(WEB_DIR), html=True),
        name="web",
    )
