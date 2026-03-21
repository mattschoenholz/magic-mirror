"""FastAPI app: static `web/` + `/api/snapshot` (FR-006)."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from mirror_backend.settings import REPO_ROOT, load_runtime_config
from mirror_backend.snapshot import build_snapshot

logging.basicConfig(level=logging.INFO)

WEB_DIR = REPO_ROOT / "web"

app = FastAPI(title="Magic Mirror API", version="0.1.0")


@app.get("/api/snapshot")
def api_snapshot():
    cfg = load_runtime_config()
    return build_snapshot(cfg)


@app.get("/api/health")
def api_health():
    return {"ok": True}


# Register API routes before `/` mount. Starlette matches specific routes first.
if WEB_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(WEB_DIR), html=True),
        name="web",
    )
