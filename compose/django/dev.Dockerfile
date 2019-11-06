FROM python:3.7.5

WORKDIR /code/django-blog

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

## Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

## --no-cache-dir
RUN pip install -r /requirements/develop.txt -i https://pypi.doubanio.com/simple

## 检查mysql是否可用
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

## celery
COPY ./compose/django/celery/worker/start.sh /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/django/celery/flower/start.sh /start-celeryflower.sh
RUN chmod +x /start-celeryflower.sh

# 运行
COPY ./compose/django/start-dev.sh /start-dev.sh
RUN chmod +x /start-dev.sh

ENTRYPOINT ["/entrypoint.sh"]
