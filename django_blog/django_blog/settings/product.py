import raven
from dotenv import load_dotenv

from .base import *  # noqa

dotenv_path = os.path.join(os.path.dirname(BASE_DIR), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DEBUG = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog',
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
        'CONN_MAX_AGE': 60,
    }
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('LOCATION'),
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "PASSWORD": os.getenv('REDIS_PASSWORD'),
        }
    }
}

RAVEN_CONFIG = {
    'dsn': os.getenv('DSN'),
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
