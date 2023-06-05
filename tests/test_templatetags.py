import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template, TemplateSyntaxError


@pytest.fixture()
def override_setting(monkeypatch):
    def _override_setting(setting, value):
        monkeypatch.setattr(
            f"django_vite.templatetags.django_vite.{setting}",
            value,
        )

    return _override_setting


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


def test_vite_hmr_client_returns_nothing_with_dev_mode_off(settings, monkeypatch):
    settings.DJANGO_VITE_DEV_MODE = False
    monkeypatch.setattr(
        "django_vite.templatetags.django_vite.DJANGO_VITE_DEV_MODE",
        settings.DJANGO_VITE_DEV_MODE,
    )
    template = Template(
        """
        {% load django_vite %}
        {% vite_hmr_client %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


def test_vite_hmr_client_uses_correct_settings(override_setting):
    override_setting("DJANGO_VITE_DEV_SERVER_PROTOCOL", "https")
    override_setting("DJANGO_VITE_DEV_SERVER_HOST", "127.0.0.2")
    override_setting("DJANGO_VITE_DEV_SERVER_PORT", "5174")
    override_setting("DJANGO_VITE_STATIC_URL", "static/")
    override_setting("DJANGO_VITE_WS_CLIENT_URL", "foo/bar")

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


def test_vite_asset_returns_script_tags():
    template = Template(
        """
        {% load django_vite %}
        {% vite_asset "src/entry.tsx" %}
    """
    )
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:3000/static/src/entry.tsx"
    assert script_tag["type"] == "module"


def test_vite_asset_raises_without_path():
    with pytest.raises(TemplateSyntaxError):
        Template(
            """
            {% load django_vite %}
            {% vite_asset %}
        """
        )


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


def test_vite_react_refresh_returns_nothing_with_dev_mode_off(settings, monkeypatch):
    settings.DJANGO_VITE_DEV_MODE = False
    monkeypatch.setattr(
        "django_vite.templatetags.django_vite.DJANGO_VITE_DEV_MODE",
        settings.DJANGO_VITE_DEV_MODE,
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


def test_vite_react_refresh_url_setting(override_setting):
    override_setting("DJANGO_VITE_REACT_REFRESH_URL", "foobar")
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
