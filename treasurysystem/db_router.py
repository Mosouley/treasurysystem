from django.conf import settings
import logging
from .settings_loader import EnvironmentManager

logger = logging.getLogger(__name__)

class AutoSwitchRouter:
    def _get_db(self):
        env_manager = EnvironmentManager.get_instance()
        is_online = env_manager.check_connectivity()
        
        # If we're online and supabase is configured, use it
        if is_online and hasattr(settings, 'DATABASES') and 'supabase' in settings.DATABASES:
            db = 'supabase'
        else:
            # Otherwise use the default (local) database
            db = 'default'
            
        logger.info(f"Using {db} database")
        return db

    def db_for_read(self, model, **hints):
        return self._get_db()

    def db_for_write(self, model, **hints):
        return self._get_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
