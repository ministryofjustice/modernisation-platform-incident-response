import logging
import os

from django.core.exceptions import ImproperlyConfigured
from response.slack.client import SlackClient

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "after_response",
    "bootstrap4",
    "response.apps.ResponseConfig",
    "rest_framework",
    'health_check',
    'social_django',
    'opgincidentresponse',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "opgincidentresponse.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ]
        },
    }
]

WSGI_APPLICATION = "opgincidentresponse.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOrganizationOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": " {levelname:5s} - {module:10.15s} - {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Markdown Filter

MARKDOWN_FILTER_WHITELIST_TAGS = [
    "a",
    "p",
    "code",
    "h1",
    "h2",
    "ul",
    "li",
    "strong",
    "em",
    "img",
]

MARKDOWN_FILTER_WHITELIST_ATTRIBUTES = ["src", "style"]

MARKDOWN_FILTER_WHITELIST_STYLES = [
    "width",
    "height",
    "border-color",
    "background-color",
    "white-space",
    "vertical-align",
    "text-align",
    "border-style",
    "border-width",
    "float",
    "margin",
    "margin-bottom",
    "margin-left",
    "margin-right",
    "margin-top",
]


def get_env_var(setting, warn_only=False):
    value = os.getenv(setting, None)

    if not value:
        error_msg = f"ImproperlyConfigured: Set {setting} environment variable"
        if warn_only:
            logger.warn(error_msg)
        else:
            raise ImproperlyConfigured(error_msg)
    else:
        value = value.replace('"', "")  # remove start/end quotes

    return value

# Environment variables

## Social auth (for GitHub login)

SOCIAL_AUTH_GITHUB_ORG_KEY = get_env_var("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_ORG_SECRET = get_env_var("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_ORG_NAME = "ministryofjustice"
SOCIAL_AUTH_GITHUB_ORG_SCOPE = ["read:org"]

## Slack

SLACK_TOKEN = get_env_var("SLACK_TOKEN")
SLACK_CLIENT = SlackClient(SLACK_TOKEN)

SLACK_SIGNING_SECRET = get_env_var("SLACK_SIGNING_SECRET")
SLACK_TEAM_ID = get_env_var("SLACK_TEAM_ID")

INCIDENT_CHANNEL_NAME = get_env_var("INCIDENT_CHANNEL_NAME")
INCIDENT_REPORT_CHANNEL_NAME = get_env_var("INCIDENT_REPORT_CHANNEL_NAME")
INCIDENT_BOT_NAME = get_env_var("INCIDENT_BOT_NAME")

INCIDENT_BOT_ID = os.getenv("INCIDENT_BOT_ID") or SLACK_CLIENT.get_user_id(INCIDENT_BOT_NAME)
INCIDENT_CHANNEL_ID = SLACK_CLIENT.get_channel_id(INCIDENT_CHANNEL_NAME)
INCIDENT_REPORT_CHANNEL_ID = SLACK_CLIENT.get_channel_id(INCIDENT_REPORT_CHANNEL_NAME)

## Statuspage

STATUSPAGEIO_API_KEY = get_env_var("STATUSPAGEIO_API_KEY")
STATUSPAGEIO_PAGE_ID = get_env_var("STATUSPAGEIO_PAGE_ID")

## PagerDuty

PAGERDUTY_API_KEY = get_env_var("PAGERDUTY_API_KEY")
PAGERDUTY_SERVICE = get_env_var("PAGERDUTY_SERVICE")
PAGERDUTY_EMAIL = get_env_var("PAGERDUTY_EMAIL")

LOGIN_URL = "/login/github-org"

# Whether to use https://pypi.org/project/bleach/ to strip potentially dangerous
# HTML input in string fields
RESPONSE_SANITIZE_USER_INPUT = True

# Whether users need to log in to access Response
RESPONSE_LOGIN_REQUIRED = True
