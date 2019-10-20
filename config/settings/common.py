from .base import *  # noqa

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
        "OPTIONS": {"charset": "utf8mb4"},
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
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
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
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "Asia/Shanghai"
CELERYD_HIJACK_ROOT_LOGGER = False

# django-celery-results
# https://github.com/celery/django-celery-results
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

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
