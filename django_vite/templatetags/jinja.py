from functools import wraps

from jinja2.ext import Extension
from markupsafe import Markup

from django_vite.templatetags.base import (
    vite_asset as base_vite_asset,
    vite_asset_url as base_vite_asset_url,
    vite_hmr_client as base_vite_hmr_client,
    vite_legacy_asset as base_vite_legacy_asset,
    vite_legacy_polyfills as base_vite_legacy_polyfills,
    vite_preload_asset as base_vite_preload_asset,
    vite_react_refresh as base_vite_react_refresh,
)


def mark_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Markup(func(*args, **kwargs))

    return wrapper


vite_hmr_client = mark_safe(base_vite_hmr_client)
vite_asset = mark_safe(base_vite_asset)
vite_preload_asset = mark_safe(base_vite_preload_asset)
vite_asset_url = base_vite_asset_url
vite_legacy_polyfills = mark_safe(base_vite_legacy_polyfills)
vite_legacy_asset = mark_safe(base_vite_legacy_asset)
vite_react_refresh = mark_safe(base_vite_react_refresh)


class DjangoViteExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        environment.globals.update(
            {
                "vite_hmr_client": vite_hmr_client,
                "vite_asset": vite_asset,
                "vite_preload_asset": vite_preload_asset,
                "vite_asset_url": vite_asset_url,
                "vite_legacy_polyfills": vite_legacy_polyfills,
                "vite_legacy_asset": vite_legacy_asset,
                "vite_react_refresh": vite_react_refresh,
            }
        )
