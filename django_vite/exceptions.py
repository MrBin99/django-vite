class DjangoViteManifestError(RuntimeError):
    """Manifest parsing failed."""

    pass


class DjangoViteAssetNotFoundError(RuntimeError):
    """Vite Asset could not be found."""

    pass
