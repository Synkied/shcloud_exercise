from .base import *  # noqa

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plan_heure',
        'USER': 'plan_heure',
        'PASSWORD': '',
        'HOST': 'database',
        'PORT': '5432',
    }
}
