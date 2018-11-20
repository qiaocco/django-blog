import socket
from urllib import parse

from dotenv import load_dotenv

from .base import *  # NOQA

dotenv_path = os.path.join(BASE_DIR, ".envs", ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from .common import *  # NOQA

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

# ========== debug-toolbar
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1"]

# ========== END debug-toolbar
