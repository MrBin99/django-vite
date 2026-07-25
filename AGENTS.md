# django-vite

A Django package that integrates ViteJS frontend builds with Django static files.

## Project structure

- `django_vite/` — the package. Single app, no sub-packages.
  - `core/asset_loader.py` — heart of the library: `DjangoViteAssetLoader` (singleton), `DjangoViteAppClient`, `ManifestClient`, `DjangoViteConfig`. All template tag logic routes here.
  - `core/tag_generator.py` — HTML tag rendering helpers.
  - `core/exceptions.py` — three custom exceptions.
  - `templatetags/django_vite.py` — Django template tags (`vite_asset`, `vite_hmr_client`, `vite_legacy_asset`, etc.). Thin wrappers around `DjangoViteAssetLoader.instance()`.
  - `management/commands/runserver.py` — custom `runserver` that proxies static/Vite requests to the Vite dev server.
- `tests/` — pytest suite. Test settings at `tests/settings.py`, fixtures at `tests/conftest.py`.
- `tests/data/` — mock staticfiles and Vite manifest fixtures.

## Commands

```
pytest                          # run all tests (coverage auto-enabled via pyproject.toml addopts)
pytest tests/tests/foo.py       # single test file
pytest tests/tests/foo.py::bar  # single test

ruff check django_vite          # lint
black .                         # format
black --check --diff .          # style check only

tox                             # full matrix (Python 3.8-3.12 x Django 3.2-5.1+)
tox -e lint                     # ruff only
tox -e codestyle                # black check only
```

Test deps are installed via tox environments; for local dev install manually:
`pip install pytest pytest-django pytest-cov pytest-sugar beautifulsoup4`

## Testing quirks

- `DJANGO_SETTINGS_MODULE=tests.settings` is set in `pyproject.toml`.
- `DjangoViteAssetLoader` is a singleton. Tests **must** reset it between cases. Use the `reload_django_vite()` helper from `conftest.py`, or the `patch_settings` fixture which does it automatically.
- `patch_settings` fixture (from `conftest.py`) — the primary way tests swap config. It patches `django.conf.settings`, reloads the loader, and restores original values after the test.
- `delete_settings` fixture — unsets specific settings (useful for testing fallback behavior).
- `dev_mode_false`, `dev_mode_true`, `dev_mode_all` fixtures — parameterized to run under both legacy (`DJANGO_VITE_DEV_MODE`) and new (`DJANGO_VITE = {"default": {...}}`) config styles. New tests should use these.
- Manifest fixtures live under `tests/data/staticfiles/` and `tests/data/named_assets/`.

## Configuration

Two styles coexist (legacy is deprecated):

**New (preferred):**
```python
DJANGO_VITE = {
    "default": {"dev_mode": True},
    "other_app": {"dev_mode": False, "manifest_path": "/path/to/manifest.json"},
}
```

**Legacy (deprecated, triggers a warning):**
```python
DJANGO_VITE_DEV_MODE = True
DJANGO_VITE_MANIFEST_PATH = "/path/to/manifest.json"
```

Mixing both styles silently ignores legacy settings. `DjangoViteConfig` (from `django_vite`) is the type-safe way to define configs.

## Architecture notes

- `DjangoViteAssetLoader.instance()` is a singleton initialized on Django app ready. It caches parsed manifests in memory.
- In `dev_mode=False`, manifests are parsed at first access and cached. The `check()` method validates manifests and registers as a Django system check (`django_vite.W001`).
- Custom manifest loading (e.g. S3) is done by subclassing `ManifestClient` and setting `app_client_class` in config.
- The `runserver` management command wraps `ViteAssetHandler` around the default static files handler to proxy Vite-managed assets to the dev server.

## Code style

- Black: line-length 88 (default).
- Ruff: selects E, F, C, B, PT, SIM, DJ, I. Unfixable: F401 (unused import), F841 (unused variable).
- Pre-commit: black, ruff (via tox), plus standard hooks (toml, yaml, trailing-whitespace, line-ending).
