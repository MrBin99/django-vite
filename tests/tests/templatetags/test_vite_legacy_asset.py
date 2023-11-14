import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django_vite.core.exceptions import DjangoViteAssetNotFoundError


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_legacy_asset_returns_nothing_with_dev_mode_on():
    template = Template(
        """
        {% load django_vite %}
        {% vite_legacy_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


@pytest.fixture
def patch_manifest_path(request, settings, patch_settings):
    if request.param == "new_settings":
        return patch_settings(
            {
                "DJANGO_VITE_DEV_MODE": False,
                "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
                / "polyfills-manifest.json",
            }
        )
    elif request.param == "legacy_settings":
        return patch_settings(
            {
                "DJANGO_VITE": {
                    "default": {
                        "dev_mode": False,
                        "manifest_path": settings.STATIC_ROOT
                        / "polyfills-manifest.json",
                    }
                }
            }
        )


@pytest.mark.parametrize(
    "patch_manifest_path",
    [
        "new_settings",
        "legacy_settings",
    ],
    indirect=True,
)
def test_vite_legacy_asset_returns_production_tags(patch_manifest_path):
    template = Template(
        """
        {% load django_vite %}
        {% vite_legacy_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "assets/entry-2e8a3a7a.js"
    assert script_tag["nomodule"] == ""


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_legacy_asset_raises_nonexistent_entry():
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_legacy_asset "src/fake.ts" %}
        """
        )
        template.render(Context({}))
