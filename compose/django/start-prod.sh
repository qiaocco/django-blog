#!/usr/bin/env bash

APP_HOME=/code/django-blog
python $APP_HOME/manage.py collectstatic --noinput --clear
python $APP_HOME/manage.py migrate
/usr/local/bin/gunicorn --chdir=$APP_HOME -b 0.0.0.0:8000 -w 4 config.wsgi
