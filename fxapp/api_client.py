import requests
from django.conf import settings

import logging

from treasurysystem.management.utils.rate_limiter import rate_limited

logger = logging.getLogger(__name__)

class ExchangeRatesAPI:
    ENDPOINTS = [
        "https://api.apilayer.com/exchangerates_data",
        "https://api.apilayer.com/fixer",
        "https://api.apilayer.com/currency_data"
    ]

    def __init__(self):
        self.api_key = settings.API_LAYER_KEY
        self.current_endpoint_index = 0

    def _get_current_endpoint(self):
        return self.ENDPOINTS[self.current_endpoint_index]

    def _rotate_endpoint(self):
        self.current_endpoint_index = (self.current_endpoint_index + 1) % len(self.ENDPOINTS)
        logger.info(f"Switching to endpoint: {self._get_current_endpoint()}")
        return self._get_current_endpoint()

    @rate_limited(calls_per_minute=25)
    def get_historical_rates(self, start_date, end_date, base_currency="KES"):
        headers = {"apikey": self.api_key}
        
        for attempt in range(len(self.ENDPOINTS)):
            current_endpoint = self._get_current_endpoint()
            try:
                response = requests.get(
                    f"{current_endpoint}/timeseries",
                    params={
                        "start_date": start_date,
                        "end_date": end_date,
                        "base": base_currency
                    },
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed for endpoint {current_endpoint}: {str(e)}")
                if response.status_code == 429 or response.status_code >= 500:
                    self._rotate_endpoint()
                    continue
                raise

        logger.error("All API endpoints exhausted")
        raise Exception("Unable to fetch exchange rates from any endpoint")
