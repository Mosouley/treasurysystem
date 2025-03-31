import socket
import threading
import time
from django.conf import settings
from contextlib import contextmanager
from django.db import connections
from django.db.utils import OperationalError

class DatabaseHealthChecker:
    _instance = None
    _lock = threading.Lock()
    _supabase_available = False
    _last_check = 0
    CHECK_INTERVAL = 30  # seconds

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def check_supabase_connection(self):
        current_time = time.time()
        if current_time - self._last_check < self.CHECK_INTERVAL:
            return self._supabase_available

        try:
            with connections['default'].cursor() as cursor:
                cursor.execute('SELECT 1')
                self._supabase_available = True
        except OperationalError:
            self._supabase_available = False
        
        self._last_check = current_time
        return self._supabase_available

    @contextmanager
    def database_context(self):
        """Context manager that determines which database to use"""
        try:
            if self.check_supabase_connection():
                # print('Using Supabase')
                yield 'default'
            else:
                print('Using default')
                yield 'local'
        except Exception:
            # print('Error occurred, using local')
            yield 'local'
