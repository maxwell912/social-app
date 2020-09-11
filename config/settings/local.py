from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_SILK = False


if DEBUG_TOOLBAR:
    INSTALLED_APPS = ['debug_toolbar'] + INSTALLED_APPS
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
elif DEBUG_SILK:
    INSTALLED_APPS = ['silk'] + INSTALLED_APPS
    MIDDLEWARE = ['silk.middleware.SilkyMiddleware'] + MIDDLEWARE
