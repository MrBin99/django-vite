import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_react_refresh_returns_script_tag():
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.script
    assert not script_tag.has_attr("src")
    assert script_tag.has_attr("type")
    assert script_tag["type"] == "module"
    assert "__vite_plugin_react_preamble_installed__" in script_tag.text
    assert "http://localhost:5173/static/@react-refresh" in script_tag.text


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_DEV_SERVER_PROTOCOL": "https",
            "DJANGO_VITE_DEV_SERVER_HOST": "127.0.0.2",
            "DJANGO_VITE_DEV_SERVER_PORT": "5174",
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix",
            "DJANGO_VITE_REACT_REFRESH_URL": "foo/bar",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "dev_server_protocol": "https",
                    "dev_server_host": "127.0.0.2",
                    "dev_server_port": "5174",
                    "static_url_prefix": "custom/prefix",
                    "react_refresh_url": "foo/bar",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_react_refresh_uses_correct_settings(patch_settings):
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert not script_tag.has_attr("src")
    assert script_tag.has_attr("type")
    assert script_tag["type"] == "module"
    assert "__vite_plugin_react_preamble_installed__" in script_tag.text
    assert "https://127.0.0.2:5174/static/custom/prefix/foo/bar" in script_tag.text


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_react_refresh_returns_nothing_with_dev_mode_false():
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_REACT_REFRESH_URL": "foobar",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "react_refresh_url": "foobar",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_react_refresh_url_setting(patch_settings):
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.script
    assert "http://localhost:5173/static/foobar" in script_tag.text


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_REACT_REFRESH_URL": "foobar",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "react_refresh_url": "foobar",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_react_refresh_uses_kwargs(patch_settings):
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh nonce="woo-nonce" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.script
    assert script_tag.has_attr("nonce")
    assert script_tag["nonce"] == "woo-nonce"
