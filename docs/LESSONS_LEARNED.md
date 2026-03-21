# Lessons learned — Magic Mirror

Append entries **as you go**. Short bullets beat long narratives.

---

## Template (copy per entry)

```
### YYYY-MM-DD — <short title>
- **Context:** 
- **What happened:** 
- **Root cause (if known):** 
- **Fix / mitigation:** 
- **FSD/Doc update:** (link or section)
```

---

## Log

### 2026-03-20 — Snapshot weather, hourly forecasts, todos overflow, HA response shapes
- **Context:** Mirror showed wrong “current” condition at night (Open-Meteo); hourly/todos missing on Pi while ICS worked; HA WebSocket service responses easy to mis-parse.
- **What happened:** Field testing showed Pirate Weather more trustworthy for *now* + hourly; empty hourly/todos traced to missing `return_response`, wrong `get_forecasts` targeting, and stale Pi builds / browser cache.
- **Root cause (if known):** `weather.get_forecasts` requires **target** entity + `return_response`; forecast data arrives under **`result.response`** (WS) or **`service_response`** (REST). “Today” calendar filter + Open-Meteo state produced misleading night UX.
- **Fix / mitigation:** `weather_now_entities` + Pirate-first hourly chain (explicit or reorder); six slots **after** `now` with no duplicate “Now” row; todos **>6** → incomplete-only cap at 6; client unwrappers + deploy/build stamp checks.
- **FSD/Doc update:** [BACKEND_HA_INTEGRATION_2026-03.md](BACKEND_HA_INTEGRATION_2026-03.md), [MIRROR_RUNTIME.md](MIRROR_RUNTIME.md), [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md), `config/mirror.runtime.example.yaml`.

---

## Themes to watch (seeded from planning)

- Mirror glass contrast / font size too small for viewing distance.
- Microphone performance behind glass / in reflective cavity.
- Thermal throttling in sealed frame — ventilation underestimated.
- Voice false positives at night — need feedback + whitelist discipline.
- HA token leaked into repo or browser bundle — security incident pattern.
