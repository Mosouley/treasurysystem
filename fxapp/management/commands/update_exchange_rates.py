import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from fxapp.models import Ccy, CountryConfig, ReevaluationRates 
import os
from django.conf import settings

class ExchangeRatesAPI:
    def __init__(self):
        self.api_key = os.getenv('API_LAYER_KEY')
        self.base_url = 'https://api.apilayer.com/exchangerates_data/timeseries'

    def get_historical_rates(self, start_date, end_date, base_ccy_code):
        url = f'{self.base_url}?start_date={start_date}&end_date={end_date}&base={base_ccy_code}'
        headers = {
            'apikey': self.api_key
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'API request failed: {e}')
            return None

class Command(BaseCommand):
    help = 'Fetch exchange rates for all country base currencies'

    def handle(self, *args, **options):
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
                self.stderr.write(self.style.ERROR('No data received from any API endpoint'))
                return
        except Exception as e:
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