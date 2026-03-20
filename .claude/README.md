# Claude Code paths

Symlinks point at the **canonical** files under `agents/` and `.cursor/skills/` so one edit updates both tools.

## Agents

`.claude/agents/*.md` → `../agents/*.md`

## Skills

| Symlink | Target |
|---------|--------|
| `mm-mirror-context` | `../.cursor/skills/mm-mirror-context` |
| `mm-home-assistant` | `../.cursor/skills/mm-home-assistant` |
| `mm-kiosk-pi` | `../.cursor/skills/mm-kiosk-pi` |
| `mm-voice-aiy-google` | `../.cursor/skills/mm-voice-aiy-google` |
| `mm-dev-mcp-ha` | `../.cursor/skills/mm-dev-mcp-ha` |

## Recreate (clone without symlinks)

```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .claude/agents .claude/skills
for f in planner architect coder ux-designer tester; do
  ln -sf "../../agents/${f}.md" ".claude/agents/${f}.md"
done
for s in mm-mirror-context mm-home-assistant mm-kiosk-pi mm-voice-aiy-google mm-dev-mcp-ha; do
  ln -sf "../../.cursor/skills/${s}" ".claude/skills/${s}"
done
```

Or copy instead of `ln -sf` if symlinks are unsupported.
