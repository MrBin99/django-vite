from typing import Dict, Any
import pytest
from importlib import reload
from django_vite.templatetags import django_vite


@pytest.fixture()
def patch_settings(settings):
    """
    1. Patch new settings into django.conf.settings.
    2. Reload django_vite module so that variables on the module level that use settings
    get recalculated.
    3. Restore the original settings once the test is over.

    TODO: refactor django_vite so that we don't set variables on the module level using
    settings.
    """
    __PYTEST_EMPTY__ = "__PYTEST_EMPTY__"
    original_settings_cache = {}

    def _patch_settings(new_settings: Dict[str, Any]):
        for key, value in new_settings.items():
            original_settings_cache[key] = getattr(settings, key, __PYTEST_EMPTY__)
            setattr(settings, key, value)

        reload(django_vite)
        django_vite.DjangoViteAssetLoader.instance()

    yield _patch_settings

    for key, value in original_settings_cache.items():
        if value == __PYTEST_EMPTY__:
            delattr(settings, key)
        else:
            setattr(settings, key, value)

    reload(django_vite)
    django_vite.DjangoViteAssetLoader.instance()
