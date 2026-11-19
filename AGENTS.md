# Rules for coding agents

These rules are for AI coding agents (Claude Code, Codex, Copilot, ...) working on this Floorbit plugin.
Humans: the same rules apply to you in spirit.
`CLAUDE.md` imports this file.

## What this is

A plugin for [Floorbit](https://github.com/bitsandbricks-ch/floorbit), made from
bitsandbricks-ch/floorbit-plugin-template and released to the Floorbit Marketplace (bitsandbricks-ch/floorbit-plugins). The plugin is the repository's root:
`plugin.yaml`, `plugin.py` (the hosted part) and `agent.py` (the part on the local agent in the
hall). The [README](README.md) says how it is tested and released.

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
6. **Never merge** your own pull request, never force-push to a branch someone else works on, and
   never push a tag. Merging and releasing are the maintainer's call.
7. Keep the pull request description current when you push more commits.

## Rules

- **Ask, don't guess.** Never make up facts about the project, its users or its author (features,
  history, numbers, names). Leave a `TODO` and ask instead.
- **No secrets** in code, commits, screenshots, logs or docs. Use example values (`example.com`,
  `192.0.2.x`).
- **Names:** the brand is written "BitsAndBricks". Public text names the author as "Mike" only.
- **Releases:** a version goes into `plugin.yaml` and gets a `## <version>` section in
  `CHANGELOG.md`; the maintainer pushes the `v<version>` tag, and the workflow signs and releases it.
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
