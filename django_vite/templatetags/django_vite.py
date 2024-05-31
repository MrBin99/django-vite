from django import template
from django.utils.safestring import mark_safe

from django_vite.templatetags.base import (
    vite_asset as base_vite_asset,
    vite_asset_url as base_vite_asset_url,
    vite_hmr_client as base_vite_hmr_client,
    vite_legacy_asset as base_vite_legacy_asset,
    vite_legacy_polyfills as base_vite_legacy_polyfills,
    vite_preload_asset as base_vite_preload_asset,
    vite_react_refresh as base_vite_react_refresh,
)

register = template.Library()

vite_hmr_client = register.simple_tag(mark_safe(base_vite_hmr_client))
vite_asset = register.simple_tag(mark_safe(base_vite_asset))
vite_preload_asset = register.simple_tag(mark_safe(base_vite_preload_asset))
vite_asset_url = register.simple_tag(base_vite_asset_url)
vite_legacy_polyfills = register.simple_tag(mark_safe(base_vite_legacy_polyfills))
vite_legacy_asset = register.simple_tag(mark_safe(base_vite_legacy_asset))
vite_react_refresh = register.simple_tag(mark_safe(base_vite_react_refresh))
