# AIY Voice HAT + Google cloud — reference

Project decision: **Google account + cloud** acceptable for v1; hardware is **Google AIY Voice Kit** (identify v1 vs v2 from board and [official kit docs](https://aiyprojects.withgoogle.com/voice)).

---

## Starting points (verify against current Google docs)

- [AIY Projects — Voice](https://aiyprojects.withgoogle.com/voice) — image, HAT tests, Assistant integration history.
- [Google Assistant library / device registration](https://developers.google.com/assistant) — product flows change; pin a working guide when implementation starts.

---

## Audio routing (Pi)

| Output | Notes |
|--------|--------|
| **HAT speaker** | Often default for Voice HAT images; good for quiet TTS / night mode |
| **HDMI → TV** | `aplay -l` / PulseAudio / PipeWire default sink; may be better for clarity at distance |

Document the **default** and any **night-mode** rule in `docs/ARCHITECTURE.md`. UX pairs voice state with **on-screen** feedback (see `agents/ux-designer.md`).

---

## Intent → Home Assistant

- Keep a **whitelist** of allowed HA `domain.service` calls (see `docs/FSD.md` §6).
- Avoid “full assistant” scope; prefer **fixed phrases** or small intent set mapped to **known** services.
- On cloud failure: fall back per Architecture (e.g. show error, disable mic until retry, or push-to-talk only).

---

## Credentials

- Store OAuth / device credentials under `/etc/...` or user config with strict perms; document path in README runbook, not in git.
- Rotate if leaked; update Pi config out-of-band.

---

## Tester notes

- Test with **TV on vs off** if audio uses HDMI.
- Test **reflection / room noise** for false triggers; align with FSD security rule for unknown commands.
