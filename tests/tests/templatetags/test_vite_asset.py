import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template, TemplateSyntaxError


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
