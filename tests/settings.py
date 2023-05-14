import os

BASE_DIR = os.path.dirname(__file__)

STATIC_URL = "static"
DJANGO_VITE_DEV_MODE = True
DJANGO_VITE_ASSETS_PATH = "/"
USE_TZ = True


INSTALLED_APPS = [
    "django_vite",
]

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
            "debug": TEMPLATE_DEBUG,
        },
    },
]
