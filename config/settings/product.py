import logging
from urllib import parse

import raven
import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *  # noqa

dotenv_path = os.path.join(BASE_DIR, ".envs", ".env.product")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

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

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_blog.taskapp.celery.CeleryAppConfig"]
CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/1".format(
    password=os.getenv("REDIS_PASSWORD"),
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

# ========== END CELERY

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # 我的邮箱账号
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True  # 开启安全链接
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER  # 设置发件人
EMAIL_TIME_LIMIT = 300

# SENTRY
# https://docs.sentry.io/platforms/python/django/
# ------------------------------------------------------------------------------
SENTRY_DSN = os.getenv("SENTRY_DSN")
sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=None,  # Send no events from log messages
)

# ========== END SENTRY


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {  # 日志格式
        "standard": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] "
            "[%(name)s:%(lineno)d] [%(module)s:%(funcName)s] "
            "[%(levelname)s]- %(message)s"
        }
    },
    "filters": {  # 过滤器
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "handlers": {  # 处理器
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "mail_admins": {  # 发送邮件通知管理员
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],  # 仅当 DEBUG = False 时才发送邮件
            "include_html": True,
        },
        "debug": {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log", "debug.log"),  # 日志输出文件
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份份数
            "formatter": "standard",  # 使用哪种formatters日志格式
        },
        "console": {  # 输出到控制台
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {  # logging管理器
        "django": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "django.request": {
            "handlers": ["debug", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
    },
}
# ========== END LOGGING
