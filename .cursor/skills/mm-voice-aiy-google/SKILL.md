---
name: mm-voice-aiy-google
description: >-
  Google AIY Voice HAT + cloud voice (DEFERRED for v1 — Echo-only voice).
  Use only if the project adds mirror-mounted AIY / Assistant back to scope.
---

# Magic Mirror — AIY Voice + Google cloud

> **v1 project status:** Voice is **Echo Dot → HA** only; the Pi does **not** use the AIY HAT initially. Skip this skill unless you **reopen** AIY scope.

## When to apply

- You are adding **mirror-local** capture, wake, STT/TTS, or mapping phrases → HA **on the Pi**.
- Choosing HAT vs HDMI audio for **mirror** TTS.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, **`docs/FSD.md`** (voice table), **`docs/ARCHITECTURE.md`**.
2. Use **[reference.md](reference.md)** for bring-up links and patterns.
3. **Never** commit OAuth client secrets, refresh tokens, or API keys — device-local storage only.

## Outputs

- Architecture updates for chosen Assistant/software stack; FSD rows for intents VI-*; Tester cases for false triggers and cloud failure.
