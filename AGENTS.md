# Rules for coding agents

These rules are for AI coding agents (Claude Code, Codex, Copilot, ...) working on this Floorbit plugin.
Humans: the same rules apply to you in spirit.
`CLAUDE.md` imports this file.

This repo follows the [BitsAndBricks handbook](https://github.com/bitsandbricks-ch/handbook),
profile **plugin** (see `.mason.toml`). Read its core chapters and the blocks that profile lists.
Where this file differs from the handbook, this file wins for this repo.

## What this is

The Zabbix plugin for [Floorbit](https://github.com/bitsandbricks-ch/floorbit) (id `zabbix`), released
to the Floorbit Marketplace (bitsandbricks-ch/floorbit-plugins). The plugin is the repository's root:
`plugin.yaml` and `plugin.py`, which Floorbit runs on the local agent in the hall. The [README](README.md) says how it is tested and released.

## Workflow

1. **Branch:** work on your own branch, never push to `main`. One topic per branch and pull request.
2. **Before you push**, run what CI runs and make it pass locally, with Floorbit checked out next to
   this repository at the commit in `FLOORBIT_REF`:
   - `ruff check --config ../floorbit/pyproject.toml --config 'lint.isort.known-third-party=["floorbit"]' .`
   - `PYTHONPATH=../floorbit python -m pytest -q tests`
3. **Pull request:** open it as a **draft** and fill in the template
   (`.github/pull_request_template.md`). Link the issue.
4. **CI:** wait for the checks. Fix failures yourself. Never skip, disable or weaken a check or a
   test to get green.
5. **Done** means the task is complete, the checklist is ticked and the checks are green: then mark
   the pull request ready for review. Leave it a draft only while work is open or you are blocked,
   and say why in the description.
6. **Auto-merge** (handbook decision 0017): once the pull request is ready, turn on squash auto-merge
   (`gh pr merge <n> --auto --squash`); GitHub merges it when the required check passes. Leave it off,
   for the maintainer to merge, on pull requests that touch keys, signing, sign-in, the plugin sandbox or
   release workflows, and on version pull requests from `mason bump`. Never merge by hand, never
   force-push to a branch someone else works on, never push a tag. Releasing is the maintainer's call.
7. Keep the pull request description current when you push more commits.

## Rules

- **Ask, don't guess.** Never make up facts about the project, its users or its author (features,
  history, numbers, names). Leave a `TODO` and ask instead.
- **No secrets** in code, commits, screenshots, logs or docs. Use example values (`example.com`,
  `192.0.2.x`).
- **Names:** the brand is written "BitsAndBricks". Public text names the author as "Mike" only.
- **Releases:** describe your change in a new `changelog.d/<topic>.md` fragment, not in
  `CHANGELOG.md` (see `changelog.d/README.md`). Don't change the version in `plugin.yaml`:
  `mason bump` does that, and the maintainer pushes the `v<version>` tag; the workflow signs and
  releases it.
- **Workflows:** pin every action to a full commit sha with the version as a comment
  (`uses: actions/checkout@<sha> # v7.0.1`), keep `permissions` minimal, and never put
  `${{ github.event.* }}` text straight into a `run:` script (pass it through `env:`).
- **Signing:** never touch the sign job, the `plugin-signing` environment or keys unless the
  maintainer asks.
- **Privacy:** only aggregates leave the event network for NetFlow, DNS and Wi-Fi; a plugin's
  `sends:` says what each kind of data is, and Floorbit refuses the rest.
- **Tests never talk to a real device or service:** use the fakes in `tests/`.
- **Dependencies:** add one only when it clearly pays for itself, and say why in the pull request.
- Write short comments that explain why, not what.
- Stay inside the repository. Ask before deleting files you didn't create.
