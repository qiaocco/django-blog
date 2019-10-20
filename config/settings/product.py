import logging

from dotenv import load_dotenv

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import BASE_DIR, os

dotenv_path = os.path.join(BASE_DIR, ".envs", ".env.product")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from .common import *  # isort:skip

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

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
# https://cheat.readthedocs.io/en/latest/django/logging.html
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,  # 是否禁用已经存在的logger实例
    "formatters": {  # 日志格式
        "standard": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] %(pathname)s"
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
            "maxBytes": 1024 * 1024 * 5,  # 文件大小5M
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
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
# ========== END LOGGING
