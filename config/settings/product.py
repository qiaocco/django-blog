import logging
from urllib import parse

import raven
import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *  # noqa

dotenv_path = os.path.join(BASE_DIR, '.envs', '.env.product')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')

# DB
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT'),
        'CONN_MAX_AGE': 60,
    }
}

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{host}:{port}/1"
            .format(host=os.getenv("REDIS_HOST", "redis"),
                    port=os.getenv("REDIS_PORT", "6379")),
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "PASSWORD": os.getenv('REDIS_PASSWORD'),
        }
    }
}

# SENTRY
# https://docs.sentry.io/platforms/python/django/
# ------------------------------------------------------------------------------
SENTRY_DSN = os.getenv('SENTRY_DSN')
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()]
)

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=None  # Send no events from log messages
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s '
                      '%(process)d  %(thread)d  %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
# ========== END RAVEN

# EMAIL CONFIGURATION
# TODO 监控.env。当.env变化时，django reload
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIME_LIMIT = 300

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_blog.taskapp.celery.CeleryAppConfig']
CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/1".format(
    password=os.getenv("REDIS_PASSWORD"),
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# ========== END CELERY
