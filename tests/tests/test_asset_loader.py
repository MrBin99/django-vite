import pytest

from django_vite.core.asset_loader import (
    DjangoViteConfig,
    DjangoViteAssetLoader,
)
from pathlib import Path
from django.conf import settings
from django_vite.core.asset_loader import DjangoViteConfig
from django_vite.apps import check_loader_instance


def test_django_vite_asset_loader_cannot_be_instantiated():
    with pytest.raises(RuntimeError):
        DjangoViteAssetLoader()


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": False,
        },
        {
            "DJANGO_VITE_DEV_MODE": True,
        },
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_ASSETS_PATH": "/",
        },
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_ASSETS_PATH": "/",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                }
            }
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                }
            }
        },
        {
            "DJANGO_VITE": {
                "default": DjangoViteConfig(
                    dev_mode=False,
                )
            }
        },
        {
            "DJANGO_VITE": {
                "default": DjangoViteConfig(
                    dev_mode=True,
                )
            }
        },
    ],
    indirect=True,
)
def test_check_loader_instance_happy(patch_settings):
    warnings = check_loader_instance()
    assert len(warnings) == 0


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_MANIFEST_PATH": "fake.json",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "manifest_path": "fake.json",
                }
            }
        },
    ],
    indirect=True,
)
def test_check_loader_instance_warnings(patch_settings):
    warnings = check_loader_instance()
    assert len(warnings) == 1
    assert "Make sure you have generated a manifest file" in warnings[0].hint


def test_apply_fallback():
    """
    Test that a fallback "default" app is made even when there are no DJANGO_VITE
    settings defined.
    """
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


def test_parse_manifest_during_dev_mode(dev_mode_true):
    default_app = DjangoViteAssetLoader.instance()._apps["default"]
    manifest_client = default_app.manifest
    assert manifest_client._parse_manifest() == manifest_client.ParsedManifestOutput()


def test_parse_manifest_during_dev_mode(dev_mode_true):
    default_app = DjangoViteAssetLoader.instance()._apps["default"]
    manifest_client = default_app.manifest
    assert manifest_client._parse_manifest() == manifest_client.ParsedManifestOutput()


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_MANIFEST_PATH": Path(settings.STATIC_ROOT)
            / "dynamic-entry-manifest.json",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "manifest_path": Path(settings.STATIC_ROOT)
                    / "dynamic-entry-manifest.json",
                }
            }
        },
    ],
    indirect=True,
)
def test_load_dynamic_import_manifest(patch_settings):
    warnings = check_loader_instance()
    assert len(warnings) == 0
