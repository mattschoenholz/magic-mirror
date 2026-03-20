---
name: mm-voice-aiy-google
description: >-
  Google AIY Voice HAT + cloud-backed voice for Magic Mirror: audio path,
  Assistant integration patterns, intent-to-HA mapping, credentials hygiene.
  Use when designing or implementing voice on the Pi.
---

# Magic Mirror — AIY Voice + Google cloud

## When to apply

- Voice capture, wake, STT/TTS routing, or mapping phrases → Home Assistant services.
- Choosing default audio output (HAT vs HDMI).

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, **`docs/FSD.md`** (voice table), **`docs/ARCHITECTURE.md`**.
2. Use **[reference.md](reference.md)** for bring-up links and patterns.
3. **Never** commit OAuth client secrets, refresh tokens, or API keys — device-local storage only.

## Outputs

- Architecture updates for chosen Assistant/software stack; FSD rows for intents VI-*; Tester cases for false triggers and cloud failure.
