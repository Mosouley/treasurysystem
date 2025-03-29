import socket
from django.conf import settings
from .db_health import DatabaseHealthChecker

# This is the only router class we need
class AutoSwitchRouter:
    def __init__(self):
        self.health_checker = DatabaseHealthChecker.get_instance()

    def _get_db(self):
        with self.health_checker.database_context() as db:
            return db

    def db_for_read(self, model, **hints):
        return self._get_db()

    def db_for_write(self, model, **hints):
        return self._get_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
