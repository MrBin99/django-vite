from __future__ import annotations

from django.conf import settings
from django.contrib.staticfiles.finders import find as finders_find
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticRunserverCommand,
)
from django.shortcuts import redirect

from ...core.asset_loader import (
    DEFAULT_APP_NAME,
    DjangoViteAssetLoader,
)


class ViteAssetHandler(StaticFilesHandler):
    def _should_handle(self, path):
        """
        Check if path is under STATIC_URL or is a Vite-specific path.
        """
        if "__open-in-editor" in path:
            return True
        return super()._should_handle(path=path)

    def serve(self, request):
        client = DjangoViteAssetLoader.instance()._apps[DEFAULT_APP_NAME]
        vite_url = f"{client.dev_server_protocol}://{client.dev_server_host}:{client.dev_server_port}"

        # __open-in-editor always goes to vite
        if "__open-in-editor" in request.path:
            static_url = settings.STATIC_URL.strip("/")
            redirect_url = f"{vite_url}/{static_url}/{client.static_url_prefix}/__open-in-editor"
            if query := request.GET.urlencode():
                redirect_url += f"?{query}"
            return redirect(redirect_url)

        # Check if file exists on disk via Django staticfiles finders
        normalized_path = request.path.removeprefix(settings.STATIC_URL).lstrip("/")
        if finders_find(normalized_path):
            # File exists on disk — serve it via Django staticfiles
            return super().serve(request)

        # File doesn't exist on disk — proxy to Vite dev server
        redirect_url = f"{vite_url}{request.path}"
        if query := request.GET.urlencode():
            redirect_url += f"?{query}"
        return redirect(redirect_url)


class Command(StaticRunserverCommand):
    help = (
        "Starts a lightweight web server for development and "
        "also serves static files together with Vite assets."
    )

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--novite",
            action="store_false",
            dest="use_vite_handler",
            help="Tells Django to NOT automatically use handler that will serve Vite assets.",
        )

    def get_handler(self, *args, **options):
        """
        Return static file handler that will handle Vite assets together with handling
        open in editor from Vue browser plugin.
        """
        handler = super().get_handler(*args, **options)
        use_vite_handler = options["use_vite_handler"]
        if use_vite_handler:
            return ViteAssetHandler(handler)

        return handler
