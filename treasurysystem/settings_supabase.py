# Description: This file contains the settings for the Supabase database connection.
from .settings import *
from .settings_loader import load_settings


ENV_MODE = load_settings()
DEBUG = False

# Add this debugging section
db_params = {
    'ENGINE': os.environ.get('POSTGRES_ENGINE'),
    'NAME': os.getenv('POSTGRES_DB', ),
    'USER': os.getenv('POSTGRES_USER',),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'HOST': os.getenv('POSTGRES_HOST', ),
    'PORT': os.getenv('POSTGRES_PORT', ),
}


DATABASE_ROUTERS = ['treasurysystem.db_router.AutoSwitchRouter']

DATABASES = {
    'default': {
        **db_params,
        'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': 30,
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
            'client_encoding': 'UTF8',  # Add explicit client encoding
        },
    },
    'local': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'treasury_system'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'papaHaddy@?123'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'disable',
            'connect_timeout': 30,
            'client_encoding': 'UTF8',  # Add explicit client encoding
        },
    }
}

# Add this to force Django to print SQL queries
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
