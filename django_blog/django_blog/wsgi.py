"""
WSGI config for django_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

profile = os.environ.get('DJANGO_BLOG_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog.settings.{}".format(profile))

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog.settings")

application = get_wsgi_application()
