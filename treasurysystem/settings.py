"""
Django settings for treasurysystem project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from celery import Celery
from celery.schedules import crontab
import treasurysystem.tasks
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# For loading locally the dajngo and serving app from localhost

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-$4u@l48c^n9!hqd1%l$=!7(wg+*19uxnn%%*+8b51lz-_twr45'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
##### docker set up config elements #################################
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = bool(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: '
# DJANGO_ALLOWED_HOSTS='localhost'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS",'').split()


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', 
    'rest_framework',
    'fxapp',
    'contacts',
    'money_market',
    'django_filters'
]

ASGI_APPLICATION = 'treasurysystem.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   
]

ROOT_URLCONF = 'treasurysystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'treasurysystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_NAME',  'postgres'),
        'USER': os.environ.get('POSTGRES_USER','supabase_admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD',),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
          'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': int(os.environ.get('POSTGRES_CONNECT_TIMEOUT', 30)),
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
        },
        'CONN_MAX_AGE': 60,
    }
}
import logging
logger = logging.getLogger(__name__)
logger.info(f"Database host: {os.environ.get('POSTGRES_HOST')}")
# Verify required environment variables are set
required_env_vars = [
    'POSTGRES_NAME',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_HOST',
    'POSTGRES_PORT',
]

for var in required_env_vars:
    if not os.environ.get(var):
        raise ValueError(f'Required environment variable {var} is not set')
    

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# CORS_ORIGIN_ALLOW_ALL = True
# For local dev, localhost was not working but 127. was
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:4200",
    "http://localhost:4200",
  
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
ALLOWED_HOSTS =[
    'localhost',
    '127.0.0.1'
]


# Connect Celery to Redis
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


## settings.py
CHANNEL_LAYERS = {
    'default': {
  
        # Method 2: Via local Redis
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
             "hosts": [('redis', 6379)],
        },
    },
}

# PVZKPPNf2FmqHagUcU0JJVG5NIEDuxY0 API KEY APILAYER
CELERY_BEAT_SCHEDULE = {
 
    "send_email_report": {
        "task": "treasurysystem.tasks.send_email_report",
        "schedule": crontab(minute="*/10"),
    },
    'send_positions': {  
        'task': 'treasurysystem.tasks.send_position_updates',  
        'schedule': crontab(minute='*/1'),  # Every 5 minutes  
    }, 
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@email.com"
ADMINS = [("testuser", "test.user@email.com"), ]


# print("Database Configuration is here:", DATABASES)