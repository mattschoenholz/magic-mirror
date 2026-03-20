# Claude Code paths

- **`agents/`** — symlinks to `../agents/*.md` (same content includes YAML frontmatter: `name`, `description`, `skills: mm-mirror-context`).
- **`skills/mm-mirror-context`** — symlink to `../.cursor/skills/mm-mirror-context` (contains `SKILL.md`).

If symlinks are missing after clone (e.g. Windows without symlink support), recreate:

```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .claude/agents .claude/skills
for f in planner architect coder ux-designer tester; do
  ln -sf "../../agents/${f}.md" ".claude/agents/${f}.md"
done
ln -sf "../../.cursor/skills/mm-mirror-context" ".claude/skills/mm-mirror-context"
```

Or copy files instead of `ln -sf` if your environment disallows symlinks.
