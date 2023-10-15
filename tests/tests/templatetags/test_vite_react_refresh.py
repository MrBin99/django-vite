from bs4 import BeautifulSoup
from django.template import Context, Template


def test_vite_react_refresh_happy_flow():
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
    assert "http://localhost:3000/static/@react-refresh" in script_tag.text


def test_vite_react_refresh_returns_nothing_with_dev_mode_off(patch_settings):
    patch_settings(
        {
            "DJANGO_VITE_DEV_MODE": False,
        }
    )
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


def test_vite_react_refresh_url_setting(patch_settings):
    patch_settings({"DJANGO_VITE_REACT_REFRESH_URL": "foobar"})
    template = Template(
        """
        {% load django_vite %}
        {% vite_react_refresh %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.script
    assert "http://localhost:3000/static/foobar" in script_tag.text
