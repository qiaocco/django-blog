# DOCKER TRICK
import socket

from .base import *

DEBUG = True

# db
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

# caching
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

# ========== debug-toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]


# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

# ========== END debug-toolbar
