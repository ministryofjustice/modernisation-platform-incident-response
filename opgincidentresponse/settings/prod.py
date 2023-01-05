import os

from .base import *  # noqa: F401, F403

SITE_URL = os.environ.get("SITE_URL")

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "USER": os.environ.get("DB_USER"),
        "NAME": os.environ.get("DB_NAME"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "OPTIONS": {"sslmode": os.getenv("DB_SSL_MODE", "disable")},
    }
}

