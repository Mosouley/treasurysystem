import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from fxapp.models import Ccy, CountryConfig, ReevaluationRates, RatesUpdateLog
import os
from django.conf import settings
from treasurysystem.utils import broadcast_data_sync, get_positions
import logging
import time

logger = logging.getLogger(__name__)

class ExchangeRatesAPI:
    def __init__(self):
        self.api_key = settings.API_LAYER_KEY
        self.endpoints = settings.API_SETTINGS['ENDPOINTS']
        self.timeout = settings.API_SETTINGS['TIMEOUT']
        self.max_retries = settings.API_SETTINGS['MAX_RETRIES']

    def get_historical_rates(self, start_date, end_date, base_ccy_code):
        for endpoint_name, base_url in self.endpoints.items():
            url = f'{base_url}/timeseries'
            params = {
                'start_date': start_date,
                'end_date': end_date,
                'base': base_ccy_code
            }
            headers = {'apikey': self.api_key}

            for attempt in range(self.max_retries):
                try:
                    logger.info(f"Trying endpoint: {endpoint_name}, attempt {attempt + 1}")
                    response = requests.get(
                        url, 
                        params=params,
                        headers=headers,
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    data = response.json()
                    if data and 'rates' in data:
                        logger.info(f"Successfully retrieved rates from {endpoint_name}")
                        self.last_successful_endpoint = endpoint_name
                        return data
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Failed to fetch from {endpoint_name}: {e}")
                    if attempt == self.max_retries - 1:
                        continue  # Try next endpoint
                    time.sleep(2 ** attempt)  # Exponential backoff
            
        logger.error("All endpoints failed")
        return None

class Command(BaseCommand):
    help = 'Fetch exchange rates once per day when online'

    def should_update(self):
        # Get last successful update
        last_update = RatesUpdateLog.objects.filter(success=True).last()
        
        if not last_update:
            return True

        # Check if last update was before today
        today = timezone.now().date()
        return last_update.last_update.date() < today

    def handle(self, *args, **options):
        if not self.should_update():
            self.stdout.write('Rates already updated today, skipping...')
            return

        # Get the base currency code from the first country config
        country_config = CountryConfig.objects.all().first()
        if country_config is None:
            self.stdout.write(self.style.ERROR('No CountryConfig found. Please add a record to the CountryConfig table.'))
            base_ccy_code = settings.DEFAULT_BASE_CURRENCY
        else:
            base_ccy_code = country_config.base_currency.code

        # If base_ccy_code is None, use the default base currency from settings
        if not base_ccy_code:
            base_ccy_code = settings.DEFAULT_BASE_CURRENCY
            self.stdout.write(self.style.ERROR('No Base Currency found. The system will use the default base currency.'))
        # Set the start and end dates for the timeseries API request
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Use the API client instead of direct requests
        api_client = ExchangeRatesAPI()
        try:
            data = api_client.get_historical_rates(start_date, end_date, base_ccy_code)

            if not data:
                RatesUpdateLog.objects.create(success=False)
                self.stderr.write(self.style.ERROR('Failed to fetch rates from all endpoints'))
                return
            
            # Log successful update
            RatesUpdateLog.objects.create(
                success=True,
                endpoint_used=api_client.last_successful_endpoint
            )
            
            # Log successful fetch
            self.stdout.write(self.style.SUCCESS('Successfully fetched rates from API'))
            
        except Exception as e:
            RatesUpdateLog.objects.create(success=False)
            self.stderr.write(self.style.ERROR(f'Failed to fetch rates: {e}'))
            return

        # Extract data
        rates_date_str = end_date  # Use the end_date as the rates_date
        rates = data.get('rates', {}).get(end_date, {})
        print('the rates are ', rates)
        if not rates_date_str or not rates:
            self.stderr.write(self.style.ERROR('Invalid API response format'))
            return

        # Convert API date to timezone-aware datetime
        try:
            rates_date_naive = datetime.strptime(rates_date_str, '%Y-%m-%d')
            rates_date = timezone.make_aware(rates_date_naive)
        except ValueError:
            self.stderr.write(self.style.ERROR('Invalid date format in API response'))
            return

        # Process currencies
        processed = 0
        skipped = 0
       
        base_ccy = Ccy.objects.get(code=base_ccy_code)
        # print('the base is ', base_ccy)
        currencies = Ccy.objects.exclude(code=base_ccy_code)
        # print('the currencies are ', currencies.values_list('code', flat=True))
    

        # Create base currency rate (1.0)
        if not ReevaluationRates.objects.filter(date=rates_date, base_ccy=base_ccy, target_ccy=base_ccy).exists():
            ReevaluationRates.objects.create(
                date=rates_date,
                target_ccy=base_ccy,
                base_ccy=base_ccy,
                exchange_rate=1.0
            )
            processed += 1

        # Process other currencies
        for ccy in currencies:
            rate = rates.get(ccy.code)
            # print('the rate is of ',ccy.code ,' is ', rate)
            if not rate:
                self.stdout.write(self.style.WARNING(f'Rate not available for {ccy.code}'))
                skipped += 1
                continue

            # Check for existing entry
            if ReevaluationRates.objects.filter(date=rates_date, target_ccy=ccy).exists():
                skipped += 1
                continue

            # Create new entry
            ReevaluationRates.objects.create(
                date=rates_date,
                base_ccy=base_ccy,
                target_ccy=ccy,
                exchange_rate=1 / rate if rate else 1.0
            )
            processed += 1

        # After processing rates, broadcast position updates
        positions_data = get_positions()
        broadcast_data_sync('position_updates', 'send_position_updates', positions_data)
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed {processed} rates ({skipped} skipped) '
            f'for {rates_date_str}'
        ))