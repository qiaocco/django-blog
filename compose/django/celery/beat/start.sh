#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

sleep 3

rm -f './celerybeat.pid'
celery -A django_blog.taskapp beat -l INFO --workdir /code/django-blog