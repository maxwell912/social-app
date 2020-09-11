from .base import *

DEBUG = True
ENVIRONMENT = 'development'

ALLOWED_HOSTS = [ '*' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pycamp_socialapp_dev',
        'USER': 'pycamp_socialapp_dev',
        'PASSWORD': 'jK#p^KlFU*4uP*XH',
        'HOST': 'postgres1.saritasa.io',
        'PORT': '5432',
    }
}


INSTALLED_APPS += (
    'django_pdb',

)
