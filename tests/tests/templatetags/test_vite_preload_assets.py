from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.template import Context, Template

PRELOAD_MANIFEST_PATH = (
    Path(settings.BASE_DIR) / "data/staticfiles/preload-assets-manifest.json"
)


@pytest.fixture(autouse=True)
def patch_preload_settings(patch_settings):
    return patch_settings(
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": False,
                    "manifest_path": PRELOAD_MANIFEST_PATH,
                    "static_url_prefix": "dist/",
                }
            },
            "INSTALLED_APPS": [
                "django_vite",
                "django.contrib.staticfiles",
            ],
        }
    )


def test_preload_assets_ext_woff2_and_type_font():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-with-assets.js' file_ext='.woff2' as_type='font' crossorigin='anonymous' %}
    """)
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("link")
    assert link_tag["href"] == "/static/dist/assets/font.woff2"
    assert link_tag["rel"] == ["preload"]
    assert link_tag["as"] == "font"
    assert link_tag["type"] == "font/woff2"
    assert link_tag.has_attr("crossorigin")


def test_preload_assets_ext_oft_and_type_font():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-with-assets.js' file_ext='.otf' as_type='font' crossorigin='anonymous' %}
    """)
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("link")
    assert link_tag["href"] == "/static/dist/assets/font.otf"
    assert link_tag["type"] == "font/otf"


def test_preload_assets_image():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-with-assets.js' file_ext='.png' as_type='image' %}
    """)
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("link")
    assert link_tag["href"] == "/static/dist/assets/image.png"
    assert link_tag["rel"] == ["preload"]
    assert link_tag["as"] == "image"
    assert link_tag["type"] == "image/png"


def test_entry_not_found():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/non-existent-entry.js' file_ext='.otf' as_type='font' %}
    """)
    html = template.render(Context({}))
    assert html.strip() == ""


def test_entry_without_assets():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-without-assets.js' file_ext='.svg' as_type='image' %}
    """)
    html = template.render(Context({}))
    assert html.strip() == ""


def test_no_matching_assets():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-with-assets.js' file_ext='.svg' as_type='image' %}
    """)
    html = template.render(Context({}))
    assert html.strip() == ""


def test_unknown_mimetype():
    template = Template("""
    {% load django_vite %}
    {% vite_preload_assets 'src/entry-with-assets.js' file_ext='.unknown' as_type='object' %}
    """)
    html = template.render(Context({}))
    soup = BeautifulSoup(html, "html.parser")
    link_tag = soup.find("link")
    assert link_tag["rel"] == ["preload"]
    assert link_tag["href"] == "/static/dist/assets/data.unknown"
    assert link_tag["as"] == "object"
