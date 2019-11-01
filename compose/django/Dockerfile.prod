FROM python:3.7.5

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /code

# create the app user
RUN groupadd -r jasongroup \
    && useradd -r -g jasongroup jason

# create the appropriate directories
ENV HOME=/code
ENV APP_HOME=$HOME/django-blog
RUN mkdir $APP_HOME
# collect static files
RUN mkdir $HOME/static_files

WORKDIR $APP_HOME

## Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

## --no-cache-dir
RUN pip install -r /requirements/product.txt -i https://pypi.doubanio.com/simple

## 检查mysql是否可用
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

## celery
COPY ./compose/django/celery/worker/start.sh /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/django/celery/beat/start.sh /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY ./compose/django/celery/flower/start.sh /start-celeryflower.sh
RUN chmod +x /start-celeryflower.sh

# 启动脚本
COPY ./compose/django/start-prod.sh /start-prod.sh
RUN chmod +x /start-prod.sh

COPY . $APP_HOME

RUN chown -R jason:jasongroup /code

USER jason

ENTRYPOINT ["/entrypoint.sh"]
