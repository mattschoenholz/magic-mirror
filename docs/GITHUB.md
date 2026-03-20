# GitHub & version control

## Canonical location

| | |
|--|--|
| **Local path** | `~/Desktop/CurrentProjects/General/magic-mirror` |
| **Remote** | `git@github.com:mattschoenholz/magic-mirror.git` |
| **Web** | [github.com/mattschoenholz/magic-mirror](https://github.com/mattschoenholz/magic-mirror) |

This project is **standalone** — it is not part of SailboatServer or other repos.

`origin` is preset to `git@github.com:mattschoenholz/magic-mirror.git`. Create the **empty** GitHub repository (same name, under your user), then push `main`.

### Option A — GitHub website

1. [Create new repository](https://github.com/new): name `magic-mirror`, **Public**, **no** README / .gitignore / license (repo must stay empty).
2. From the project root:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
git push -u origin main
```

### Option B — GitHub CLI (`gh`)

Install if needed: `brew install gh`. Then:

```bash
gh auth login
cd ~/Desktop/CurrentProjects/General/magic-mirror
gh repo create mattschoenholz/magic-mirror --public \
  --description "Wall magic mirror: Pi 4, AIY Voice HAT, Home Assistant"
git push -u origin main
```

`origin` is already set, so do **not** pass `--remote=origin` to `gh repo create` (avoids “remote already exists” errors).

---

## Git identity (before first push)

Set your real identity **in this repo** (or use global config):

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
git config user.name "Matt Schoenholz"
git config user.email "YOUR_EMAIL or GitHub noreply"
```

GitHub noreply format: `mattschoenholz@users.noreply.github.com` (if enabled in GitHub email settings).

---

## Clone & daily sync

```bash
git clone git@github.com:mattschoenholz/magic-mirror.git
cd magic-mirror
# … edit …
git add -A && git status
git commit -m "type: short description"
git pull --rebase origin main   # if collaborating
git push origin main
```

---

## Create remote (if you only have local)

If the GitHub repo did not exist yet, create an **empty** repo named `magic-mirror` under `mattschoenholz`, then:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
git remote add origin git@github.com:mattschoenholz/magic-mirror.git   # skip if already added
git branch -M main
git push -u origin main
```

With [GitHub CLI](https://cli.github.com/) (`gh`), from the repo root:

```bash
gh repo create mattschoenholz/magic-mirror --public --source=. --remote=origin --push
```

*(Fails if `origin` already exists — use `git remote -v` and adjust.)*

---

## Branching (lightweight)

| Branch | Use |
|--------|-----|
| `main` | Stable docs + released software |
| `develop` | Optional integration branch |
| `feature/*` | Short-lived features when coding starts |

Tags: `docs-v0.1`, `v1.0.0-mirror` for milestones.

---

## What must never be committed

- Home Assistant **long-lived tokens**, passwords, SSH private keys.
- `.env` with real values.
- Large **binary artifacts** (disk images, huge videos) — Git LFS or external storage if needed.

---

## Solid version control habits

- **Atomic commits:** one logical change per commit message.
- **FSD first:** behavior change → update `docs/FSD.md` version table → commit with docs.
- **PRs:** optional self-review using `agents/tester.md`.

---

## Optional: GitHub features

- **Issues** mapped to FSD FR IDs (e.g. `FR-003`).
- **Projects** board: Backlog / In progress / Verifying / Done.
- **Releases** with SD image checksums when you ship hardware images.
