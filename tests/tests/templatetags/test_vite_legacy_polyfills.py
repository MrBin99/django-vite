import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django_vite.core.exceptions import DjangoViteAssetNotFoundError


@pytest.mark.usefixtures("dev_mode_true")
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
def test_vite_legacy_polyfills_production(patch_manifest_path):
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


@pytest.fixture
def patch_manifest_path_custom_motif(request, settings, patch_settings):
    if request.param == "new_settings":
        return patch_settings(
            {
                "DJANGO_VITE_DEV_MODE": False,
                "DJANGO_VITE_LEGACY_POLYFILLS_MOTIF": "custom-motif",
                "DJANGO_VITE_MANIFEST_PATH": settings.STATIC_ROOT
                / "custom-motif-polyfills-manifest.json",
            }
        )
    elif request.param == "legacy_settings":
        return patch_settings(
            {
                "DJANGO_VITE": {
                    "default": {
                        "dev_mode": False,
                        "legacy_polyfills_motif": "custom-motif",
                        "manifest_path": settings.STATIC_ROOT
                        / "custom-motif-polyfills-manifest.json",
                    }
                }
            }
        )


@pytest.mark.parametrize(
    "patch_manifest_path_custom_motif",
    [
        "new_settings",
        "legacy_settings",
    ],
    indirect=True,
)
def test_vite_legacy_polyfills_custom_motif(patch_manifest_path_custom_motif):
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


@pytest.fixture
def patch_manifest_path_bad_motif(request, settings, patch_settings):
    if request.param == "new_settings":
        return patch_settings(
            {
                "DJANGO_VITE_DEV_MODE": False,
                "DJANGO_VITE_LEGACY_POLYFILLS_MOTIF": "fake-legacy-polyfills",
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
                        "legacy_polyfills_motif": "fake-legacy-polyfills",
                        "manifest_path": settings.STATIC_ROOT
                        / "polyfills-manifest.json",
                    }
                }
            }
        )


@pytest.mark.parametrize(
    "patch_manifest_path_bad_motif",
    [
        "new_settings",
        "legacy_settings",
    ],
    indirect=True,
)
def test_vite_legacy_polyfills_nonexistent_motif(patch_manifest_path_bad_motif):
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_legacy_polyfills %}
        """
        )
        template.render(Context({}))
