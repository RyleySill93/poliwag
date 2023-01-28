"""
Django settings for poliwag project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta
from decouple import config
from pythonjsonlogger import jsonlogger
import logging.config
import sentry_sdk
import ddtrace
import dj_database_url
from datadog import initialize, statsd
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from poliwag.version import VERSION

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
QUERY_DEBUG = config("QUERY_DEBUG", default=False, cast=bool)
ENVIRONMENT = config("ENVIRONMENT", default="local")
IS_PRODUCTION = ENVIRONMENT == "production"
IS_SANDBOX = ENVIRONMENT == "sandbox"
IS_DEPLOYED_ENV = IS_PRODUCTION or IS_SANDBOX
SERVER_NAME = config("EC2_INSTANCE_ID", default="unknown")

ALLOWED_HOSTS = ["127.0.0.1"]
# CORS_ALLOW_HEADERS = ["*"]
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True

# Application definition{
INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "storages",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "poliwag.common",
    "poliwag.common.authentication",
    "poliwag.common.identity",
    "poliwag.common.documents",
    "poliwag.common.mailer",
    "poliwag.common.events",
    "poliwag.core",
    "poliwag.core.user",
]

# Django-request-logging settings
NO_REQUEST_ID = ""
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "poliwag.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "poliwag.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'poliwag.common.exceptions.api_exception_handler',
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}
if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
        "rest_framework.renderers.JSONRenderer",
    )

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
            "ATOMIC_REQUESTS": True,
        }
    }
else:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()

# CELERY_TASK_ALWAYS_EAGER = config("CELERY_TASK_ALWAYS_EAGER", default=True, cast=bool)
# CELERY_BROKER_URL = config("CELERY_BROKER_URL")
# CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
# CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"

# Django-storages
# DOCUMENT_MOCK_STORAGE = config("DOCUMENT_MOCK_STORAGE", cast=bool, default=False)
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_REGION_NAME = config("AWS_REGION_NAME")

# REDIS_PORT = config("REDIS_PORT", 6379)
# REDIS_HOST = config("REDIS_HOST", "localhost")

# Django channels
# ASGI_APPLICATION = "poliwag.common.sockets.routing.application"
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(REDIS_HOST, REDIS_PORT)],
#         },
#     }
# }

# Emails
DEV_EMAIL_BACKEND = "poliwag.common.mailer.backends.EmailToBrowserBackend"
DEV_EMAIL_FILE_PATH = config("DEV_EMAIL_FILE_PATH", default="file:")
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "tmp", "email")
EMAIL_BACKEND = config("EMAIL_BACKEND", default=DEV_EMAIL_BACKEND)

# SENDGRID_API_KEY = config("SENDGRID_API_KEY")
# EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_HOST_USER = "apikey"
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_SUPPORT_ADDRESS = 'team@poliwag.com'

COMPANY_NAME = "poliwag"
GENERIC_DOMAIN_NAME = config("GENERIC_DOMAIN_NAME")
APP_DOMAIN_NAME = config("APP_DOMAIN_NAME")
API_DOMAIN_NAME = config("API_DOMAIN_NAME")
AUTH_USER_MODEL = "identity.User"

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://{REDIS_HOST}:6379/1",
#         "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
#     }
# }

# EventProcessing
EVENT_PROCESSING_LISTENER_REGISTRY = [
    "poliwag.apps.events.EventSlackNotificationListener",
]

# Slack
# SLACK_EVENT_CHANNEL = config("SLACK_EVENT_CHANNEL", default="#bot-test")
# SLACK_BOT_TOKEN = config("SLACK_BOT_TOKEN", default=None)
# SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", default=None)
# SLACK_MOCK_CLIENT = config("SLACK_MOCK_CLIENT", cast=bool, default=False)

# Twilio
# TWILIO_MOCK_CLIENT = config("TWILIO_MOCK_CLIENT", cast=bool)
# TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default=None)
# TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default=None)
# TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='+5555555555')

# Sentry
SENTRY_DSN = config("SENTRY_DSN", default=None)
if IS_DEPLOYED_ENV:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        environment=ENVIRONMENT,
        server_name=SERVER_NAME,
        release=VERSION,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )


# DATADOG
DATADOG_AGENT_HOST = config("STATSD_HOST", default="localhost")
DATADOG_SERVICE = "poliwag"
DATADOG_APM_ENABLED = config("DATADOG_APM_ENABLED", cast=bool, default=False)
if IS_DEPLOYED_ENV and DATADOG_APM_ENABLED:
    ddtrace.config.env = ENVIRONMENT
    ddtrace.config.service = DATADOG_SERVICE
    ddtrace.config.version = VERSION

    # Django settings
    ddtrace.config.django["include_user_name"] = True
    ddtrace.config.django["analytics_enabled"] = True
    ddtrace.config.django["instrument_middleware"] = False

    # Celery integration documentation: https://ddtrace.readthedocs.io/en/stable/integrations.html#celery
    ddtrace.config.celery["distributed_tracing"] = True
    ddtrace.config.celery["worker_service_name"] = DATADOG_SERVICE

    # Tracer configuration documentation: https://ddtrace.readthedocs.io/en/stable/advanced_usage.html
    ddtrace.tracer.configure(hostname=DATADOG_AGENT_HOST)
    ddtrace.tracer.set_tags({"env": ENVIRONMENT.lower()})

    # ASGI is also wrapped in asgi.py otherwise traces will not show up
    ddtrace.config.asgi["analytics_enabled"] = True
    ddtrace.config.asgi["service_name"] = DATADOG_SERVICE

    # StatsD integration documentation: https://datadogpy.readthedocs.io/en/latest/
    initialize(statsd_host=DATADOG_AGENT_HOST)
    statsd.namespace = DATADOG_SERVICE

    # Patch to explicitly inject trace/span ids in datadog logs
    ddtrace.patch_all(logging=True)

else:
    ddtrace.tracer.enabled = False

# Empty default Django's logging config
LOGGING_CONFIG = None
LOG_HANDLER = "console"
if IS_DEPLOYED_ENV:
    # Json logging for datadog
    LOG_HANDLER = "json_handler"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(levelname)s %(asctime)s %(request_id)s-> "
            "[%(name)s][%(funcName)-2s][L%(lineno)s]: %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "deployed": {
            "()": jsonlogger.JsonFormatter,
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
            "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
            "dd.version=%(dd.version)s "
            "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"
            "- %(message)s",
        },
    },
    "filters": {
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
        "json_handler": {
            "class": "logging.StreamHandler",
            "formatter": "deployed",
            "filters": ["request_id"],
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "query_audit.log",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        # Default logger for any logger name
        "": {
            "level": "INFO",
            "handlers": [
                LOG_HANDLER,
            ],
            "propagate": False,
        },
        "poliwag": {
            "level": "DEBUG",
            "handlers": [
                LOG_HANDLER,
            ],
            "propagate": False,
        },
        # Logger for django server logs with django.server logger name
        "django.server": {
            "level": "DEBUG",
            "handlers": [
                LOG_HANDLER,
            ],
            "propagate": False,
        },
        "uvicorn": {
            "handlers": [
                LOG_HANDLER,
            ],
        },
        "datadog": {
            "handlers": [LOG_HANDLER],
            "level": "INFO",
            "propagate": True,
        },
        "ddtrace": {
            "handlers": [LOG_HANDLER],
            "level": "INFO",
            "propagate": True,
        },
    },
}
if QUERY_DEBUG:
    # Rich sql logging
    LOGGING["loggers"]["django.db.backends"] = {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file",
        ],
    }

logging.config.dictConfig(LOGGING)
