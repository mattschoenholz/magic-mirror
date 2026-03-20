# GitHub & version control

## Recommended layout

This project is designed as a **standalone repository**. The folder `magic-mirror/` can be:

1. **Moved** to its own directory (e.g. `~/Projects/magic-mirror`) and become the repo root, or  
2. **Initialized as a git repo here** and later pushed to GitHub (works if you do not mind path `magic-mirror/` at repo root).

Avoid mixing SailboatServer boat portal files with Magic Mirror history unless you intentionally want a monorepo.

---

## Local Git identity (before pushing to GitHub)

If this repo was bootstrapped with a placeholder email, set your real identity **in this repo** (or globally) before pushing:

```bash
cd magic-mirror   # or your moved repo root
git config user.name "Your Name"
git config user.email "you@users.noreply.github.com"
```

Amend the initial commit only if you care about author metadata on that first commit: `git commit --amend --reset-author --no-edit`.

---

## Initialize git (first time)

*(Skip if `.git` already exists.)*

From the directory you want as **repo root** (e.g. inside `magic-mirror/`):

```bash
git init
git add .
git commit -m "docs: initial Magic Mirror planning (FSD, agents, skills)"
```

Create an **empty** repository on GitHub (no README/license if you already have local files), then:

```bash
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## Branching (lightweight)

| Branch | Use |
|--------|-----|
| `main` | Stable docs + released software |
| `develop` | Optional integration branch if multiple contributors |
| `feature/*` | Short-lived features when coding starts |

Tags: `docs-v0.1`, `v1.0.0-mirror` for milestones.

---

## What must never be committed

- Home Assistant **long-lived tokens**, passwords, SSH private keys.
- `.env` with real values.
- Large mirror **binary assets** (videos, disk images) — use Git LFS or external storage if needed later.

`.gitignore` in this folder seeds common patterns; extend when you add code.

---

## Solid version control habits

- **Atomic commits:** one logical change per commit message.
- **FSD first:** behavior change → update `docs/FSD.md` version table → commit with docs.
- **PRs:** even solo — optional self-review checklist using `agents/tester.md`.

---

## Optional: GitHub features

- **Issues** mapped to FSD FR IDs (e.g. `FR-003`).
- **Projects** board: Backlog / In progress / Verifying / Done.
- **Releases** attaching SD card image checksums (when you ship hardware images).
