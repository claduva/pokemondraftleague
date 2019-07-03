"""
Django settings for pokemondraftleague project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import socket

if (socket.gethostname().find("local")>-1):
    from .base_settings import *
    DEBUG = True
    SECRET_KEY = SECRET_KEY
    SENDGRID_API_KEY = SENDGRID_API_KEY
    AWS_ACCESS_KEY_ID = CLOUDCUBE_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = CLOUDCUBE_SECRET_ACCESS_KEY
    CLOUDCUBE_URL = CLOUDCUBE_URL
    CUBENAME=CUBENAME
    NAME=NAME
    USER=USER
    PASSWORD=PASSWORD
    HOST=HOST
else:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY','developmentkey')
    SENDGRID_API_KEY= os.environ.get('SENDGRID_API_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('CLOUDCUBE_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
    CLOUDCUBE_URL = os.environ.get('CLOUDCUBE_URL')
    CUBENAME = os.environ.get('CUBENAME')
    NAME=os.environ.get('NAME')
    USER=os.environ.get('USER')
    PASSWORD=os.environ.get('PASSWORD')
    HOST=os.environ.get('HOST')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
ALLOWED_HOSTS = ['0.0.0.0',"pokemondraftleague.herokuapp.com",'127.0.0.1',"pokemondraftleague.online"]

# Application definition
INSTALLED_APPS = [
    'dal',
    'dal_select2',
    #included django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #local apps
    'accounts.apps.AccountsConfig',
    'pokemonadmin.apps.PokemonadminConfig',
    'discordbot.apps.DiscordbotConfig',
    'individualleague.apps.IndividualleagueConfig',
    'leagues.apps.LeaguesConfig',
    'main.apps.MainConfig',
    'pokemondatabase.apps.PokemondatabaseConfig',
    'replayanalysis.apps.ReplayanalysisConfig',

    #third party apps
    'crispy_forms',
    'django_celery_beat',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #third-party middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'pokemondraftleague.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates"),os.path.join(BASE_DIR,"accounts/templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #custom
                'pokemondraftleague.processors.processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'pokemondraftleague.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,                      
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': '5432',
        'TEST': {
          'NAME': 'testdb',
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#other settings
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

#Crispy Forms Settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#Sendgrid Settings
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "accounts/sent_emails")
SENDGRID_SANDBOX_MODE_IN_DEBUG=False
EMAIL_USE_TLS= True
DEFAULT_FROM_EMAIL='pokemondraftleagueonline@gmail.com'

#AWS SETTINGS
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_LOCATION=f'{CUBENAME}/public/media'
AWS_DEFAULT_ACL='public-read'
AWS_STORAGE_BUCKET_NAME='cloud-cube'
AWS_QUERYSTRING_AUTH=False
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'pokemondraftleague/staticfiles')
STATIC_URL = '/static/' 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#Media files
PUBLIC_MEDIA_LOCATION = 'public/media'
MEDIA_URL = f'{CLOUDCUBE_URL}/{PUBLIC_MEDIA_LOCATION}/'

"""
#Redis
if (socket.gethostname().find("local")>-1):
    from pokemondraftleague.base_settings import *
    REDIS_URL=REDIS_URL
else:
    REDIS_URL=os.environ.get('REDIS_URL')
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": REDIS_URL,
    }
}
"""
#Celery
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "UTC"
