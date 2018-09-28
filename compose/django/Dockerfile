FROM python:3.6

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1

## Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

## --no-cache-dir
RUN pip install -r /requirements/base.txt -i https://pypi.doubanio.com/simple
RUN pip install -r /requirements/develop.txt -i https://pypi.doubanio.com/simple
RUN pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2

# 检查mysql是否可用
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# celery
COPY ./compose/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/django/celery/flower/start.sh /start-celeryflower.sh
RUN sed -i 's/\r//' /start-celeryflower.sh
RUN chmod +x /start-celeryflower.sh

# 运行
COPY ./compose/django/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

WORKDIR /webapp

ENTRYPOINT ["/entrypoint.sh"]
