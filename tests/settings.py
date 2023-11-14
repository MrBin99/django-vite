import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STATIC_URL = "/static/"
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

STATIC_ROOT = BASE_DIR / "data" / "staticfiles"
