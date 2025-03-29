from .db_health import DatabaseHealthChecker

class DatabaseHealthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.health_checker = DatabaseHealthChecker.get_instance()

    def __call__(self, request):
        # Check database health before each request
        self.health_checker.check_supabase_connection()
        response = self.get_response(request)
        return response
