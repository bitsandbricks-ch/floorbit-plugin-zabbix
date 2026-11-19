# Floorbit plugin template

[![Test and release](https://github.com/bitsandbricks-ch/floorbit-plugin-template/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/bitsandbricks-ch/floorbit-plugin-template/actions/workflows/release.yml?query=branch%3Amain)

The starting point for an official [Floorbit](https://github.com/bitsandbricks-ch/floorbit) plugin.
It holds a small working example: the local agent in the hall checks that a few services answer on
their TCP port, sends only how many did, and a dashboard tile shows it. How plugins work is in
Floorbit's [docs/plugins.md](https://github.com/bitsandbricks-ch/floorbit/blob/master/docs/plugins.md)
and [docs/marketplace.md](https://github.com/bitsandbricks-ch/floorbit/blob/master/docs/marketplace.md).

## What a plugin can ship

The full contract is Floorbit's [docs/plugin-spec.md](https://github.com/bitsandbricks-ch/floorbit/blob/master/docs/plugin-spec.md).
In short:

| Part | Where it runs | Can ship |
| --- | --- | --- |
| `plugin.yaml` | read before any code | id, version, Floorbit range, `uses:`, settings (secrets are write-only), actions, hooks, endpoints, dashboard tiles, right-click entries, an `icon:` from Floorbit's icon set, side panel boxes (`panels:` for a seat, switch or device), a floor plan layer (`layers:`), pages of its own in the sidebar (`pages:`, laid out from its tiles and actions), `schema:` for its data, the agent block |
| `plugin.py` | Floorbit | actions, tiles, endpoints, the Test button, data sources (inventory, monitoring, health, power, DNS, Wi-Fi, logs, ...), side panel boxes (`panel_<id>(target)`), seat colours for its layer (`layer_<id>()`), what it does with what the agent sends, 64 KB of state, JSON documents (`ctx.docs(...)`, up to 5 MB) and `migrate(from_schema, store)` when `schema:` goes up |
| `agent.py` | the local agent in the hall | collectors (`ctx.send`, each kind marked aggregate or device), listeners, read-only calls, actions the hall allows, device logins with lockout protection, its own health and metrics |
| `locales/de-CH.json` | with the plugin | German for its texts: `{"English": "Swiss German"}`, `{}` where a value goes; an older Floorbit ignores it |
| `*.py` helpers, `README.md`, `CHANGELOG.md` | with the part that imports them | helpers for `plugin.py` and `agent.py`; the README and changelog show on the Marketplace |

Never: JavaScript, CSS, HTML or other browser code (Floorbit draws every screen from data), native
code or extra Python packages, its own HTTP routes, database tables, roles or permissions, or env
variables other than `FLOORBIT_PLUGIN_<ID>_<KEY>`. Anything that talks to the event network goes
in `agent.py`. Floorbit refuses an unknown key in `plugin.yaml` and a bundle with refused files.

## A new plugin

1. **Use this template** on GitHub. Name the repository `floorbit-plugin-<id>` in
   bitsandbricks-ch: the Marketplace finds every public `floorbit-plugin-*` repository by itself.
2. Pick the id (lowercase letters, digits, dashes) and replace `example` with it in `plugin.yaml`,
   `agent.py` (the thread name) and `tests/`. Give it a name, description and homepage.
3. Replace the example code with yours, keep only the `uses:` you need, and update this README.
4. Add the environment `plugin-signing` with the secret `FLOORBIT_PLUGIN_SIGNING_KEY` (the
   plugin key's PEM), limited to `v*` tags. Nothing else needs it.

## What is where

| File | What |
| --- | --- |
| `plugin.yaml` | The manifest: settings, what it may touch, what the agent part sends. |
| `plugin.py` | The part that runs in Floorbit. |
| `agent.py` | The part that runs on the local agent in the hall. Leave it out if the plugin has none (and `agent` from `uses:`). |
| `locales/de-CH.json` | German for the plugin's texts. Add every new label, help text and message. |
| `tests/` | Tests, against Floorbit at the commit in `FLOORBIT_REF`. No network but localhost. |
| `.github/workflows/release.yml` | Tests every push and pull request; signs and releases a `v*` tag. |
| `.mason.toml` | Tells `mason bump` and `mason release tag` that the version lives in `plugin.yaml`. |
| `.gitattributes` | What stays out of the signed plugin (`export-ignore`): the files for people and agents. |

## Testing

```
git clone https://github.com/bitsandbricks-ch/floorbit ../floorbit
git -C ../floorbit checkout "$(cat FLOORBIT_REF)"
pip install -r ../floorbit/requirements.txt pytest ruff
ruff check --config ../floorbit/pyproject.toml --config 'lint.isort.known-third-party=["floorbit"]' .
PYTHONPATH=../floorbit python -m pytest -q tests
```

To try it in a running Floorbit, point `FLOORBIT_DEV_PLUGINS` at a folder holding this checkout
(never in production).

## Releasing

Put the new version into `plugin.yaml`, add a `## <version>` section to `CHANGELOG.md`, merge, then
push the tag:

```
git tag v0.1.0 && git push origin v0.1.0
```

The [workflow](.github/workflows/release.yml) tests it, signs `<id>-<version>.tar.gz` with the
Floorbit plugin key and attaches it to the GitHub release. The Marketplace picks it up within the
hour. A version is withdrawn in [floorbit-plugins](https://github.com/bitsandbricks-ch/floorbit-plugins)'
`plugins.yaml`, never by deleting the release.

The template itself is never released: it has no tags, so the Marketplace skips it.
