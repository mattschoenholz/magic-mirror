---
name: mm-home-assistant
description: >-
  Home Assistant REST and WebSocket integration for the Magic Mirror runtime
  on Raspberry Pi. Tokens, subscriptions, service calls, reconnection — no
  secrets in repo. Use when designing or coding HA client, proxy, or tests.
---

# Magic Mirror — Home Assistant integration

## When to apply

- Any code or architecture that reads/writes HA from the Pi **at runtime**.
- Defining entity lists, reconnect behavior, or FR-006 (token not in browser bundle).

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`** and **`docs/ARCHITECTURE.md`**.
2. Follow patterns in **[reference.md](reference.md)**; verify details against current HA docs (URLs inside reference).
3. **Never** commit long-lived tokens, `.env` with real values, or paste tokens into chat/MCP logs.

## Outputs

- Architecture updates, `.env.example` keys only, and Tester cases for HA up/down.

## Not in scope

- **MCP** for Cursor — use **`mm-dev-mcp-ha`** for editor-only workflows.
