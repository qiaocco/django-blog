import raven
from dotenv import load_dotenv

from .base import *  # noqa

dotenv_path = os.path.join(BASE_DIR, '.envs', '.env.product')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# general

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')

# db

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

# cache

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_LOCATION'),
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "PASSWORD": os.getenv('REDIS_PASSWORD'),
        }
    }
}

# raven
# https://docs.sentry.io/clients/python/integrations/django/

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

# put the middleware at the top, so that only 404s that bubbled all the way up get logged.
MIDDLEWARE = [
                 'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
                 'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
             ] + MIDDLEWARE

RAVEN_CONFIG = {
    'dsn': os.getenv('DSN'),
    'release': raven.fetch_git_sha(BASE_DIR),
}

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
