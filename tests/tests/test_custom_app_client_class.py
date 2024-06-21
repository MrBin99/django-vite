import pytest

from django_vite.core.asset_loader import (
    DjangoViteAppClient,
    DjangoViteAssetLoader,
    ManifestClient,
)


def mock_get_manifest_from_url():
    """
    Pretend that we're fetching manifest.json from an external source.
    """
    return {
        "src/mock_external_entry.js": {
            "css": ["assets/entry-0ed1a6fd.css"],
            "file": "assets/entry-5c085aac.js",
            "isEntry": True,
            "src": "entry.js",
        },
        "src/mock_external_entry.css": {
            "file": "assets/entry-0ed1a6fd.css",
            "src": "entry.css",
        },
    }


class CustomManifestClient(ManifestClient):
    """
    Custom ManifestClient that loads manifest.json from an external source.
    """

    def load_manifest(self):
        return mock_get_manifest_from_url()


class CustomAppClient(DjangoViteAppClient):
    """
    Custom AppClient with a Custom ManifestClient.
    """

    ManifestClient = CustomManifestClient


def test_app_client_class(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE": {
                "default": {
                    "app_client_class": "tests.tests.test_custom_app_client_class.CustomAppClient",
                }
            }
        }
    )
    DjangoViteAssetLoader._instance = None
    assert (
        "src/mock_external_entry.js"
        in DjangoViteAssetLoader.instance()._apps["default"].manifest._entries
    )


def test_invalid_app_client_class(patch_settings):
    with pytest.raises(ModuleNotFoundError):
        patch_settings(
            {
                "DJANGO_VITE": {
                    "default": {
                        "app_client_class": "django_vite.invalid.CustomAppClient",
                    }
                }
            }
        )
