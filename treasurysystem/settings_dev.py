from .settings import *
from .settings_loader import load_settings


ENV_MODE = load_settings()
DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "dev_db"),
        "USER": os.getenv("POSTGRES_USER", "dev_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "dev_password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        'OPTIONS': {
            'sslmode': 'disable',  # Changed from 'disable' to 'prefer'
        },
    }
}