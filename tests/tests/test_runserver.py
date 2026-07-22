import pytest
from pathlib import Path
from django.test import RequestFactory
from django.conf import settings
from django_vite.management.commands.runserver import ViteAssetHandler


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def vite_handler(patch_settings):
    """Return a ViteAssetHandler instance with default test config."""
    patch_settings(
        {
            "DJANGO_VITE": {
                "default": {
                    "dev_mode": True,
                    "dev_server_protocol": "http",
                    "dev_server_host": "localhost",
                    "dev_server_port": 5173,
                    "static_url_prefix": "vite",
                }
            },
            "STATIC_URL": "/static/",
            "STATICFILES_DIRS": [
                Path(settings.BASE_DIR) / "data" / "staticfiles",
            ],
        }
    )
    handler = ViteAssetHandler(None)
    return handler


class TestShouldHandle:
    def test_returns_true_for_static_url_path(self, vite_handler):
        assert vite_handler._should_handle("/static/some-file.js") is True

    def test_returns_true_for_open_in_editor(self, vite_handler):
        assert vite_handler._should_handle("/__open-in-editor?file=test.vue") is True

    def test_returns_false_for_non_static_path(self, vite_handler):
        assert vite_handler._should_handle("/admin/") is False

    def test_returns_false_for_unrelated_path(self, vite_handler):
        assert vite_handler._should_handle("/some/random/path") is False


class TestServe:
    def test_serves_existing_file_via_staticfiles(self, vite_handler, factory):
        request = factory.get("/static/assets/vendor.css")
        response = vite_handler.serve(request)
        assert response.status_code == 200

    def test_redirects_missing_file_to_vite(self, vite_handler, factory):
        request = factory.get("/static/vite/nonexistent.js")
        response = vite_handler.serve(request)
        assert response.status_code == 302
        assert response["Location"] == "http://localhost:5173/static/vite/nonexistent.js"

    def test_redirects_open_in_editor_to_vite(self, vite_handler, factory):
        request = factory.get("/__open-in-editor")
        response = vite_handler.serve(request)
        assert response.status_code == 302
        assert (
            response["Location"]
            == "http://localhost:5173/static/vite/__open-in-editor"
        )

    def test_preserves_query_params_in_redirect(self, vite_handler, factory):
        request = factory.get("/static/vite/nonexistent.js?foo=bar")
        response = vite_handler.serve(request)
        assert response.status_code == 302
        assert (
            response["Location"]
            == "http://localhost:5173/static/vite/nonexistent.js?foo=bar"
        )

    def test_preserves_query_params_for_open_in_editor(self, vite_handler, factory):
        request = factory.get("/__open-in-editor?file=Test.vue")
        response = vite_handler.serve(request)
        assert response.status_code == 302
        assert (
            response["Location"]
            == "http://localhost:5173/static/vite/__open-in-editor?file=Test.vue"
        )

    def test_uses_custom_static_url_prefix(self, vite_handler, factory):
        request = factory.get("/static/vite/entry.js")
        response = vite_handler.serve(request)
        assert response.status_code == 302
        assert (
            response["Location"]
            == "http://localhost:5173/static/vite/entry.js"
        )

    def test_uses_custom_dev_server_config(self, patch_settings, factory):
        patch_settings(
            {
                "DJANGO_VITE": {
                    "default": {
                        "dev_mode": True,
                        "dev_server_protocol": "https",
                        "dev_server_host": "vite.example.com",
                        "dev_server_port": 3000,
                        "static_url_prefix": "app",
                    }
                },
                "STATIC_URL": "/static/",
                "STATICFILES_DIRS": [
                    Path(settings.BASE_DIR) / "data" / "staticfiles",
                ],
            }
        )
        handler = ViteAssetHandler(None)
        request = factory.get("/static/app/bundle.js")
        response = handler.serve(request)
        assert response.status_code == 302
        assert (
            response["Location"]
            == "https://vite.example.com:3000/static/app/bundle.js"
        )
