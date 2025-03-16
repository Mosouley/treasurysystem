# Description: This file contains the settings for the Supabase database connection.
from . settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_NAME',  'postgres'),
        'USER': os.environ.get('POSTGRES_USER','supabase_admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD',),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '6543'),
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