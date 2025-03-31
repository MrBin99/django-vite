from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.template import Context, Template, TemplateSyntaxError

from django_vite.core.exceptions import (
    DjangoViteAssetNotFoundError,
    DjangoViteConfigNotFoundError,
)


@pytest.mark.usefixtures("dev_mode_true")
@pytest.mark.parametrize("as_default", [True, False])
def test_vite_asset_returns_dev_tags(as_default):
    if as_default:
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/entry.ts" app="default" %}
        """
        )
    else:
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/entry.ts" %}
        """
        )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:5173/static/src/entry.ts"
    assert script_tag["type"] == "module"


@pytest.mark.usefixtures("dev_mode_false")
@pytest.mark.parametrize("as_default", [True, False])
def test_vite_asset_returns_production_tags(as_default):
    if as_default:
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/entry.ts" app="default" %}
        """
        )
    else:
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/entry.ts" %}
        """
        )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "assets/entry-29e38a60.js"
    assert script_tag["type"] == "module"
    links = soup.find_all("link")
    assert len(links) == 13


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_asset_raises_without_path():
    with pytest.raises(TemplateSyntaxError):
        Template(
            """
            {% load django_vite %}
            {% vite_asset %}
        """
        )


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_asset_raises_nonexistent_entry():
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/fake.ts" %}
        """
        )
        template.render(Context({}))


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix",
        },
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix/",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "static_url_prefix": "custom/prefix",
                }
            }
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "static_url_prefix": "custom/prefix/",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_asset_dev_prefix(patch_settings):
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert (
        script_tag["src"] == "http://localhost:5173/static/custom/prefix/src/entry.ts"
    )
    assert script_tag["type"] == "module"


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix",
        },
        {
            "DJANGO_VITE_DEV_MODE": False,
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix/",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "static_url_prefix": "custom/prefix",
                }
            }
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "static_url_prefix": "custom/prefix/",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_asset_production_prefix(patch_settings):
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "custom/prefix/assets/entry-29e38a60.js"
    assert script_tag["type"] == "module"
    links = soup.find_all("link")
    assert len(links) == 13


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_asset_production_staticfiles_storage(patch_settings):
    patch_settings(
        {
            "INSTALLED_APPS": ["django_vite", "django.contrib.staticfiles"],
        }
    )
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "/static/assets/entry-29e38a60.js"
    assert script_tag["type"] == "module"
    links = soup.find_all("link")
    assert len(links) == 13


@pytest.mark.usefixtures("dev_mode_all")
def test_vite_asset_override_default_attribute():
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" crossorigin="anonymous" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["crossorigin"] == "anonymous"


@pytest.mark.usefixtures("dev_mode_all")
def test_vite_asset_kebab_attribute():
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" data_item_track="reload" data_other="3" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")

    for script_tag in soup.find_all("script"):
        assert script_tag["data-item-track"] == "reload"
        assert script_tag["data-other"] == "3"

    for link in soup.find_all("link"):
        assert link["data-item-track"] == "reload"
        assert link["data-other"] == "3"


def test_vite_asset_custom_attributes(dev_mode_all):
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" foo="bar" hello="world" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["foo"] == "bar"
    assert script_tag["hello"] == "world"


def test_vite_asset_nonexistent_app(dev_mode_true):
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" app="bad_app" %}
    """
    )
    with pytest.raises(DjangoViteConfigNotFoundError) as error:
        template.render(Context({}))

    assert "Cannot find bad_app in DJANGO_VITE settings" in str(error)


@pytest.fixture()
def external_vue_app(patch_settings, settings):
    def _wrapper(dev_mode: bool):
        return patch_settings(
            {
                "DJANGO_VITE": {
                    "external_vue_app": {
                        "dev_mode": dev_mode,
                        "static_url_prefix": "custom/prefix",
                        "dev_server_port": 5555,
                        "manifest_path": settings.STATIC_ROOT.parent
                        / "external_vue_app"
                        / "manifest.json",
                    }
                }
            }
        )

    return _wrapper


def test_vite_asset_external_app_dev(external_vue_app):
    external_vue_app(dev_mode=True)
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.js" app="external_vue_app" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert (
        script_tag["src"] == "http://localhost:5555/static/custom/prefix/src/entry.js"
    )


def test_vite_asset_external_app_production(external_vue_app):
    external_vue_app(dev_mode=False)
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.js" app="external_vue_app" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "custom/prefix/assets/entry-5c085aac.js"


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "manifest_path": Path(settings.STATIC_ROOT)
                    / "circular-imports.json",
                }
            }
        },
    ],
    indirect=True,
)
def test_circular_js_imports(patch_settings):
    """
    Circular JS imports in a manifest should not cause an infinite recursion error.
    """
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset 'src/index.jsx' %}
    """
    )
    html = template.render(Context({}))
    assert html
