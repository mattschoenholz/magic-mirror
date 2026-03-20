# GitHub & version control

## Canonical location

| | |
|--|--|
| **Local path** | `~/Desktop/CurrentProjects/General/magic-mirror` |
| **Remote (`origin`)** | `https://github.com/mattschoenholz/magic-mirror.git` |
| **Web** | [github.com/mattschoenholz/magic-mirror](https://github.com/mattschoenholz/magic-mirror) |

This project is **standalone** — it is not part of SailboatServer or other repos.

**Multi-machine workflow:** Use **HTTPS** for `origin` so each laptop/desktop can authenticate with the same pattern (browser login or token via Git Credential Manager / `gh`), without copying SSH private keys.

---

## HTTPS + GitHub CLI (`gh`) — recommended on each machine

1. Install [GitHub CLI](https://cli.github.com/) (`brew install gh` on macOS).

2. Log in and choose **HTTPS** when prompted:

```bash
gh auth login
```

Select: **GitHub.com** → **HTTPS** → authenticate via **web browser** (or token if you prefer).

3. Optional but convenient — let Git use `gh` as the HTTPS credential helper (per machine):

```bash
gh auth setup-git
```

After that, `git push` / `git pull` to `https://github.com/...` reuse the same login.

---

## First push (repo empty on GitHub)

`origin` is preset to the HTTPS URL above. Create the **empty** GitHub repository (same name, under your user), then push `main`.

### Option A — GitHub website

1. [Create new repository](https://github.com/new): name `magic-mirror`, **Public**, **no** README / .gitignore / license (repo must stay empty).
2. From the project root:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
git push -u origin main
```

### Option B — GitHub CLI

```bash
gh auth login    # HTTPS
cd ~/Desktop/CurrentProjects/General/magic-mirror
gh repo create mattschoenholz/magic-mirror --public \
  --description "Wall magic mirror: Pi 4, AIY Voice HAT, Home Assistant"
git push -u origin main
```

`origin` is already set, so do **not** pass `--remote=origin` to `gh repo create` (avoids “remote already exists” errors).

---

## Git identity (per clone or global)

```bash
cd ~/path/to/magic-mirror
git config user.name "Matt Schoenholz"
git config user.email "mattschoenholz@users.noreply.github.com"
```

Use global `git config --global ...` if you want the same identity on that machine for all repos.

---

## Clone & daily sync (any machine)

```bash
git clone https://github.com/mattschoenholz/magic-mirror.git
cd magic-mirror
gh auth login          # once per machine, HTTPS
gh auth setup-git      # optional; wires credential helper
# … edit …
git add -A && git status
git commit -m "type: short description"
git pull --rebase origin main
git push origin main
```

---

## Create remote (if you only have local)

If you initialized git locally and have **no** `origin` yet:

```bash
git remote add origin https://github.com/mattschoenholz/magic-mirror.git
git branch -M main
git push -u origin main
```

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
