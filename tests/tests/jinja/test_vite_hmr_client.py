import pytest
from bs4 import BeautifulSoup


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_hmr_client_returns_script_tag(jinja_env):
    template = jinja_env.from_string(
        """
        {{ vite_hmr_client() }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:5173/static/@vite/client"
    assert script_tag["type"] == "module"


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_hmr_client_kwargs(jinja_env):
    template = jinja_env.from_string(
        """
        {{ vite_hmr_client(blocking="render") }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag.has_attr("blocking")
    assert script_tag["blocking"] == "render"


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_hmr_client_returns_nothing_with_dev_mode_false(jinja_env):
    template = jinja_env.from_string(
        """
        {{ vite_hmr_client() }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


@pytest.mark.parametrize(
    "patch_settings",
    [
        {
            "DJANGO_VITE_DEV_MODE": True,
            "DJANGO_VITE_DEV_SERVER_PROTOCOL": "https",
            "DJANGO_VITE_DEV_SERVER_HOST": "127.0.0.2",
            "DJANGO_VITE_DEV_SERVER_PORT": "5174",
            "DJANGO_VITE_STATIC_URL_PREFIX": "custom/prefix",
            "DJANGO_VITE_WS_CLIENT_URL": "foo/bar",
        },
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "dev_server_protocol": "https",
                    "dev_server_host": "127.0.0.2",
                    "dev_server_port": "5174",
                    "static_url_prefix": "custom/prefix",
                    "ws_client_url": "foo/bar",
                }
            }
        },
    ],
    indirect=True,
)
def test_vite_hmr_client_uses_correct_settings(jinja_env, patch_settings):
    template = jinja_env.from_string(
        """
        {{ vite_hmr_client() }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "https://127.0.0.2:5174/static/custom/prefix/foo/bar"
