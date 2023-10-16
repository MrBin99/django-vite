import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template


def test_vite_hmr_client_returns_script_tag():
    template = Template(
        """
        {% load django_vite %}
        {% vite_hmr_client %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:3000/static/@vite/client"
    assert script_tag["type"] == "module"


def test_vite_hmr_client_kwargs():
    template = Template(
        """
        {% load django_vite %}
        {% vite_hmr_client blocking="render" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag.has_attr("blocking")
    assert script_tag["blocking"] == "render"


@pytest.mark.usefixtures("dev_mode_off")
def test_vite_hmr_client_returns_nothing_with_dev_mode_off():
    template = Template(
        """
        {% load django_vite %}
        {% vite_hmr_client %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


def test_vite_hmr_client_uses_correct_settings(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_SERVER_PROTOCOL": "https",
            "DJANGO_VITE_DEV_SERVER_HOST": "127.0.0.2",
            "DJANGO_VITE_DEV_SERVER_PORT": "5174",
            "DJANGO_VITE_STATIC_URL": "static/",
            "DJANGO_VITE_WS_CLIENT_URL": "foo/bar",
        }
    )

    template = Template(
        """
        {% load django_vite %}
        {% vite_hmr_client %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "https://127.0.0.2:5174/static/foo/bar"
