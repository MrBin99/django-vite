import pytest

from django_vite.templatetags.django_vite import DjangoViteAssetLoader


def test_django_vite_asset_loader_cannot_be_instantiated():
    with pytest.raises(RuntimeError):
        DjangoViteAssetLoader()
