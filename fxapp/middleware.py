# middleware.py
from datetime import timezone
from django.conf import settings
import pytz

from fxapp.models import CountryConfig

class CountryConfigMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine country (could use geo-IP or user profile)
        country = self.determine_country(request)
        
        try:
            config = CountryConfig.objects.get(country=country)
        except CountryConfig.DoesNotExist:
            config = CountryConfig.objects.first()  # Fallback

        # Attach to request
        request.country_config = config
        
        # Set timezone
        timezone.activate(pytz.timezone(config.timezone))

        response = self.get_response(request)
        return response

    def determine_country(self, request):
        # Implement your country detection logic:
        # 1. User profile country
        # 2. Geo-IP lookup
        # 3. Browser Accept-Language header
        # 4. Default fallback
        return getattr(request.user, 'country', settings.DEFAULT_COUNTRY)