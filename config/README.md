# Runtime config (mirror)

| File | In git? | Purpose |
|------|---------|---------|
| **`mirror.runtime.example.yaml`** | Yes | Default URLs, entity IDs, ICS list, intervals — **no secrets**. |
| **`mirror.runtime.local.yaml`** | **No** (gitignored) | Optional overrides on a dev machine (e.g. HA IP). **Do not** put tokens here; use Pi secrets dir per [docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md). |

Full semantics: **[docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md)**.
