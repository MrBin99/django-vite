import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template, TemplateSyntaxError
from django_vite.core.exceptions import DjangoViteAssetNotFoundError


def test_vite_asset_returns_dev_tags():
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.ts" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:3000/static/src/entry.ts"
    assert script_tag["type"] == "module"


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_asset_returns_production_tags():
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


def test_vite_asset_raises_without_path():
    with pytest.raises(TemplateSyntaxError):
        Template(
            """
            {% load django_vite %}
            {% vite_asset %}
        """
        )


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_asset_raises_nonexistent_entry():
    with pytest.raises(DjangoViteAssetNotFoundError):
        template = Template(
            """
            {% load django_vite %}
            {% vite_asset "src/fake.ts" %}
        """
        )
        template.render(Context({}))


@pytest.mark.parametrize("prefix", ["custom/prefix", "custom/prefix/"])
def test_vite_asset_dev_prefix(prefix, patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_STATIC_URL_PREFIX": prefix,
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
    assert (
        script_tag["src"] == "http://localhost:3000/static/custom/prefix/src/entry.ts"
    )
    assert script_tag["type"] == "module"


@pytest.mark.usefixtures("dev_mode_off")
@pytest.mark.parametrize("prefix", ["custom/prefix", "custom/prefix/"])
def test_vite_asset_production_prefix(prefix, patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_STATIC_URL_PREFIX": prefix,
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
    assert script_tag["src"] == "custom/prefix/assets/entry-29e38a60.js"
    assert script_tag["type"] == "module"
    links = soup.find_all("link")
    assert len(links) == 13


@pytest.mark.usefixtures("dev_mode_off")
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
