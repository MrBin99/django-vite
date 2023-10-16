class DjangoViteManifestError(RuntimeError):
    """Manifest parsing failed."""

    pass


class DjangoViteAssetNotFoundError(RuntimeError):
    """Vite Asset could not be found."""

    pass


class DjangoViteConfigNotFoundError(RuntimeError):
    """DjangoViteConfig not found in DJANGO_VITE settings."""

    pass
