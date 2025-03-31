from django.conf import settings
from .settings_loader import is_online
import time
import logging

logger = logging.getLogger(__name__)

class AutoSwitchRouter:
    def db_for_read(self, model, **hints):
        if is_online():
            return 'default'  # Using Supabase
        logger.warning("System is offline, using local database")
        return 'local'  # Using local PostgreSQL

    def db_for_write(self, model, **hints):
        if is_online():
            return 'default'  # Using Supabase
        logger.warning("System is offline, using local database")
        return 'local'  # Using local PostgreSQL

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
