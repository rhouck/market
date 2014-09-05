"""
Django settings for gifts project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Use site-specific settings
from socket import gethostname
host = gethostname()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z0-j!_ilf$kx=imqpk*v+w0(6e_@ozbp2f$ou8o&co1%as35wh'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    "django_rq",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
     # custom processors 
    'market.context_processors.google_analytics',)

ROOT_URLCONF = 'market.urls'

WSGI_APPLICATION = 'market.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#highrise cms API
HIGHRISE_CONFIG = {'server': 'harmonyspence', 'auth': '8170f80eac5ace00364b8d81eac26dac', 'email': 'dropbox@35586853.harmonyspence.highrisehq.com'}


# register parse
from parse_rest.connection import register
register("mgMLgAozJz1ShdgEFs1w1huGDpfOKpVKuwydMKmz", "HxBvkqWCuoSDE4OUJLh2z9w3sJsFJLloCCTTEsNk")

# email setup
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'boostblocks@gmail.com'
EMAIL_HOST_PASSWORD = '_2nd&mission_'
DEFAULT_FROM_EMAIL = 'boostblocks@gmail.com'

# google analytics
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-54495948-1'
GOOGLE_ANALYTICS_DOMAIN = 'boostblocks.com'

# setup redis queue
RQ_QUEUES = {
    
    'default': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    }
}


if host == 'RYANs-MacBook-Air-3.local':
    from settings_local import *
    LIVE = False
else:
    from settings_live import *
    LIVE = True
