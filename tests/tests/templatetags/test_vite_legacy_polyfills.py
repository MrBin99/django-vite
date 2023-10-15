import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django_vite.exceptions import DjangoViteAssetNotFoundError


def test_vite_legacy_polyfills_returns_nothing_with_dev_mode_on():
    template = Template(
        """
        {% load django_vite %}
        {% vite_legacy_polyfills %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_legacy_polyfills_production(patch_settings, settings):
    patch_settings(
        {
            "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
            / "polyfills-manifest.json",
        }
    )
    template = Template(
        """
        {% load django_vite %}
        {% vite_legacy_polyfills %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "assets/polyfills-legacy-f4c2b91e.js"
    assert script_tag["nomodule"] == ""


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_legacy_polyfills_custom_motif(patch_settings, settings):
    patch_settings(
        {
            "DJANGO_VITE_LEGACY_POLYFILLS_MOTIF": "custom-motif",
            "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
            / "custom-motif-polyfills-manifest.json",
        }
    )
    template = Template(
        """
        {% load django_vite %}
        {% vite_legacy_polyfills %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "assets/polyfills-legacy-6e7a4b9c.js"
    assert script_tag["nomodule"] == ""


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_legacy_polyfills_nonexistent_motif(patch_settings, settings):
    patch_settings(
        {
            "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
            / "polyfills-manifest.json",
            "DJANGO_VITE_LEGACY_POLYFILLS_MOTIF": "fake-legacy-polyfills",
        }
    )
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_legacy_polyfills %}
        """
        )
        template.render(Context({}))
