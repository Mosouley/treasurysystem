from .db_health import DatabaseHealthChecker
from .settings_loader import EnvironmentManager

class DatabaseHealthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.health_checker = DatabaseHealthChecker.get_instance()
        self.env_manager = EnvironmentManager.get_instance()

    def __call__(self, request):
        # Check connectivity and database health before each request
        is_online = self.env_manager.check_connectivity()
        if is_online:
            # Only check Supabase connection if we're online
            self.health_checker.check_supabase_connection()
        
        response = self.get_response(request)
        return response

class EnvironmentSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.env_manager = EnvironmentManager.get_instance()

    def __call__(self, request):
        # Check connectivity and reload environment if needed
        self.env_manager.load_env_file()
        return self.get_response(request)
