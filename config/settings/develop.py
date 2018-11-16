# DOCKER TRICK
import socket
from urllib import parse

from dotenv import load_dotenv

from .base import *  # NOQA

dotenv_path = os.path.join(BASE_DIR, ".envs", ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

# DB
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
        "CONN_MAX_AGE": 60,
        "ATOMIC_REQUESTS": True,
    }
}

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{host}:{port}/1".format(
            host=os.getenv("REDIS_HOST", "redis"), port=os.getenv("REDIS_PORT", "6379")
        ),
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "PASSWORD": os.getenv("REDIS_PASSWORD"),
        },
    }
}

# ========== debug-toolbar
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1"]

# ========== END debug-toolbar

# EMAIL CONFIGURATION
# TODO 监控.env。当.env变化时，django reload
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIME_LIMIT = 300

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_blog.taskapp.celery.CeleryAppConfig"]
CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/1".format(
    password=parse.quote(os.getenv("REDIS_PASSWORD")),
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_always_eager
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_IMPORTS = ("tasks",)

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
# CELERY_TASK_EAGER_PROPAGATES = True

# ========== END CELERY
