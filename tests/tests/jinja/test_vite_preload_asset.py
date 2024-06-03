import pytest
from bs4 import BeautifulSoup

from django_vite.core.exceptions import DjangoViteAssetNotFoundError


@pytest.mark.usefixtures("dev_mode_true")
def test_preload_vite_asset_returns_nothing_with_dev_mode_on(jinja_env):
    template = jinja_env.from_string(
        """
        {{ vite_preload_asset("src/entry.ts") }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    assert str(soup).strip() == ""


@pytest.mark.usefixtures("dev_mode_false")
def test_preload_vite_asset_returns_production_tags(jinja_env):
    template = jinja_env.from_string(
        """
        {{ vite_preload_asset("src/entry.ts") }}
    """
    )
    html = template.render({})
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("link")
    assert len(links) == 14
    first_link = links[0]
    assert first_link["href"] == "assets/entry-29e38a60.js"
    assert first_link["rel"] == ["modulepreload"]


@pytest.mark.usefixtures("dev_mode_false")
def test_vite_preload_asset_raises_nonexistent_entry(jinja_env):
    template = jinja_env.from_string(
        """
            {{ vite_preload_asset("src/fake.ts") }}
    """
    )
    with pytest.raises(DjangoViteAssetNotFoundError):
        template.render({})
