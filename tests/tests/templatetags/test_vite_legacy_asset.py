import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django_vite.exceptions import DjangoViteAssetNotFoundError


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


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_legacy_asset_returns_production_tags(patch_settings, settings):
    patch_settings(
        {
            "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
            / "polyfills-manifest.json",
        }
    )
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


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_legacy_asset_raises_nonexistent_entry():
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_legacy_asset "src/fake.ts" %}
        """
        )
        template.render(Context({}))
