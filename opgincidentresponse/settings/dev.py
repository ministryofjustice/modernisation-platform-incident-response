import os

from .base import *  # noqa: F401, F403

SITE_URL = "http://localhost"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "USER": os.getenv("DB_USER", "postgres"),
        "NAME": os.getenv("DB_NAME", "postgres"),
    }
}

RESPONSE_LOGIN_REQUIRED = False

SLACK_API_MOCK = os.getenv("SLACK_API_MOCK", None)
