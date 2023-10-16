import pytest

from django_vite.templatetags.django_vite import DjangoViteAssetLoader
from django_vite.apps import check_loader_instance


def test_django_vite_asset_loader_cannot_be_instantiated():
    with pytest.raises(RuntimeError):
        DjangoViteAssetLoader()


def test_check_loader_instance_happy(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_MODE": False,
        }
    )
    DjangoViteAssetLoader._instance = None
    warnings = check_loader_instance()
    assert len(warnings) == 0


def test_check_loader_instance_warnings(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_MANIFEST_PATH": "fake.json",
        }
    )
    DjangoViteAssetLoader._instance = None
    warnings = check_loader_instance()
    assert len(warnings) == 1
    assert "Make sure you have generated a manifest file" in warnings[0].hint
