import pytest

from django_vite.core.asset_loader import DjangoViteConfig
from django_vite.templatetags.django_vite import DjangoViteAssetLoader


def test_django_vite_asset_loader_cannot_be_instantiated():
    with pytest.raises(RuntimeError):
        DjangoViteAssetLoader()


def test_check_loader_instance_happy(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_MODE": False,
        }
    )
    warnings = DjangoViteAssetLoader.instance().check()
    assert len(warnings) == 0


def test_check_loader_instance_warnings(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_MANIFEST_PATH": "fake.json",
        }
    )
    warnings = DjangoViteAssetLoader.instance().check()
    assert len(warnings) == 1
    assert "Make sure you have generated a manifest file" in warnings[0].hint


def test_apply_fallback(delete_settings):
    """
    Test that a fallback "default" app is made even when there are no DJANGO_VITE
    settings defined.
    """
    delete_settings("DJANGO_VITE_DEV_MODE")
    default_app = DjangoViteAssetLoader.instance()._apps["default"]
    assert default_app
    assert default_app._config == DjangoViteConfig()


def test_combined_settings(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE": {"default": {}},
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_ASSETS_PATH": "/",
        }
    )
    DjangoViteAssetLoader._instance = None

    with pytest.warns(DeprecationWarning) as record:
        DjangoViteAssetLoader.instance()

    assert (
        "You're mixing the new DJANGO_VITE setting with these legacy settings: "
        "[DJANGO_VITE_DEV_MODE, DJANGO_VITE_ASSETS_PATH]"
    ) in str(record[0].message)
