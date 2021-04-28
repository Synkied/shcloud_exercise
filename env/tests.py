"""
Tests settings
"""
from settings import *  # noqa

DEBUG = True

ENV_MODE = 'testing'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

LOGGING = {
    'version': 1,
    'loggers': {
        'django.request': {
            'level': 'ERROR',
        }
    }
}
