import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from fxapp.models import Ccy, CountryConfig, ReevaluationRates 
import os

class Command(BaseCommand):
    help = 'Fetch exchange rates for all country base currencies'

    def handle(self, *args, **options):
        # Get the base currency code from the first country config
        base_ccy_code = CountryConfig.objects.all().first().base_currency.code
        print('the base is ',  base_ccy_code)

        # Set the start and end dates for the timeseries API request
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # API URL and headers
        API_URL = f'https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base={base_ccy_code}'
        headers = {
            'apikey': os.getenv('API_LAYER_KEY')
        }
         # Fetch rates from API
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'API request failed: {e}'))
            return

        # Extract data
        rates_date_str = end_date  # Use the end_date as the rates_date
        rates = data.get('rates', {}).get(end_date, {})
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
        print('the base is ', base_ccy)
        currencies = Ccy.objects.exclude(code=base_ccy_code)
        print('the currencies are ', currencies.values_list('code', flat=True))
    

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
            print('the rate is of ',ccy.code ,' is ', rate)
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

        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed {processed} rates ({skipped} skipped) '
            f'for {rates_date_str}'
        ))