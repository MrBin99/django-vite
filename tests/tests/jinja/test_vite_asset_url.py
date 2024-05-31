import pytest
from bs4 import BeautifulSoup

from django_vite.core.exceptions import DjangoViteAssetNotFoundError


@pytest.mark.usefixtures("dev_mode_true")
def test_vite_asset_url_returns_dev_url(jinja_env):
    template = jinja_env.from_string(
        """
        <script src="{{ vite_asset_url('src/entry.ts') }}">
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "http://localhost:5173/static/src/entry.ts"


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_asset_url_returns_production_url(jinja_env):
    template = jinja_env.from_string(
        """
        <script src="{{ vite_asset_url('src/entry.ts') }}">
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    assert script_tag["src"] == "assets/entry-29e38a60.js"


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_asset_url_raises_nonexistent_entry(jinja_env):
    template = jinja_env.from_string(
        """
        <script src="{{ vite_asset_url('src/fake.ts') }}">
    """
    )
    with pytest.raises(DjangoViteAssetNotFoundError):
        template.render({})
