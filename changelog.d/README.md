# Changelog fragments

Each pull request adds **one new file** here instead of editing `CHANGELOG.md`, so open pull
requests don't conflict on the changelog. Name it after the topic, e.g. `nan-readings.md`:

```markdown
### Fixed

- A reading of NaN is no reading.
```

Headings are the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) ones: Added, Changed,
Deprecated, Removed, Fixed, Security. Write for the crews who use the plugin: the text becomes the
release notes and the Marketplace's "what's new".

At release, `python scripts/changelog.py collect` merges every fragment into `CHANGELOG.md` under
`## [Unreleased]` and deletes the files; then `mason bump` sets the version in `plugin.yaml` and
turns `[Unreleased]` into that version's section. `python scripts/changelog.py preview` shows the
result without changing anything, and the workflow runs `python scripts/changelog.py check`.
