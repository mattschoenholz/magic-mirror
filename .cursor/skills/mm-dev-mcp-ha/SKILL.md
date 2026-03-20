---
name: mm-dev-mcp-ha
description: >-
  Cursor + Home Assistant MCP for development only: verify entities and
  services while editing the Magic Mirror repo. Not used on the Pi at runtime.
---

# Magic Mirror — dev-only: HA MCP (Cursor)

## When to apply

- Editing `docs/`, FSD entity lists, or backend code **on your dev machine** with Cursor.
- Confirming `entity_id` spelling, service domains, or HA version behavior.

## Instructions

1. **Never** paste long-lived tokens into chat, prompts, or committed files.
2. Use MCP to **read** state or **invoke** dev-safe checks — mirror **production** behavior must match **`mm-home-assistant`** (REST/WebSocket on Pi).
3. If MCP and UI disagree, **HA official API docs** win.

## Anti-patterns

- Calling MCP from the Raspberry Pi mirror runtime.
- Encoding MCP server URLs or tokens in the mirror app.

## References

- `mm-home-assistant` for runtime integration.
- `docs/MIRROR_CONTEXT.md` for project boundaries.
