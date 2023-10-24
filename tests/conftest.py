from typing import Dict, Any
import pytest

from django_vite.core.asset_loader import DjangoViteAssetLoader

__PYTEST_EMPTY__ = "__PYTEST_EMPTY__"
__PYTEST_DELETE__ = "__PYTEST_DELETE__"


def reload_django_vite():
    DjangoViteAssetLoader._instance = None
    DjangoViteAssetLoader.instance()


@pytest.fixture()
def patch_settings(request, settings):
    """
    1. Patch new settings into django.conf.settings.
    2. Recreate DjangoViteAssetLoader._instance with new settings applied.
    3. Restore the original settings once the test is over.
    """

    original_settings_cache = {}

    def _patch_settings(new_settings: Dict[str, Any]):
        for key, value in new_settings.items():
            original_settings_cache[key] = getattr(settings, key, __PYTEST_EMPTY__)
            if value == __PYTEST_DELETE__:
                delattr(settings, key)
            else:
                setattr(settings, key, value)
        reload_django_vite()

    # Apply pytest.mark.parametrize params, if patch_settings was invoked from
    # @pytest.mark.parametrize("patch_settings", [param1, param2], indirect=True)
    if hasattr(request, "param"):
        yield _patch_settings(request.param)
    else:
        yield _patch_settings

    for key, value in original_settings_cache.items():
        if value == __PYTEST_EMPTY__:
            delattr(settings, key)
        else:
            setattr(settings, key, value)
    reload_django_vite()


@pytest.fixture()
def delete_settings(patch_settings):
    """
    Unset settings that are part of the default test settings.py
    """

    def _delete_settings(*settings_to_delete: str):
        new_settings = {key: __PYTEST_DELETE__ for key in settings_to_delete}
        return patch_settings(new_settings)

    return _delete_settings


@pytest.fixture(
    params=[
        {
            "DJANGO_VITE_DEV_MODE": False,
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                }
            }
        },
    ]
)
def dev_mode_false(request, patch_settings):
    """
    Run a test with dev_mode=False, parameterized to run under both versions of
    settings that we support.
    """
    return patch_settings(request.param)


@pytest.fixture(
    params=[
        {
            "DJANGO_VITE_DEV_MODE": True,
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                }
            }
        },
    ]
)
def dev_mode_true(request, patch_settings):
    """
    Run a test with dev_mode=True, parameterized to run under both versions of
    settings that we support.
    """
    return patch_settings(request.param)


@pytest.fixture(
    params=[
        {
            "DJANGO_VITE_DEV_MODE": True,
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                }
            }
        },
        {
            "DJANGO_VITE_DEV_MODE": False,
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                }
            }
        },
    ]
)
def dev_mode_all(request, patch_settings):
    """
    Run a test with dev_mode=True, parameterized to run under both versions of
    settings that we support.
    """
    return patch_settings(request.param)
