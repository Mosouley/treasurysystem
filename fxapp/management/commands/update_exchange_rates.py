import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from fxapp.models import Ccy, CountryConfig, ReevaluationRates 


class Command(BaseCommand):
    help = 'Fetch exchange rates for all country base currencies'

    def handle(self, *args, **options):
        # Get all unique base currencies from country configs
        base_currencies = CountryConfig.objects.values_list(
            'base_currency__code', 
            flat=True
        ).distinct()
        # BASE_CURRENCY = 'USD'
        for base_ccy_code in base_currencies:
            try:
                base_ccy = Ccy.objects.get(code=base_ccy_code)
            except Ccy.DoesNotExist:
                self.stderr.write(f"Base currency {base_ccy_code} not found")
                continue

            # Fetch rates for this base currency
            API_URL = f'https://api.frankfurter.app/latest?from={base_ccy_code}'

         # Fetch rates from API
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'API request failed: {e}'))
            return

        # Extract data
        rates_date_str = data.get('date')
        rates = data.get('rates', {})
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
        base_ccy = Ccy.objects.get(code=base_ccy)
        currencies = Ccy.objects.exclude(code=base_ccy)
        print(currencies)
        print(base_ccy)
    

        # Create base currency rate (1.0)
        if not ReevaluationRates.objects.filter(date=rates_date, ccy=base_ccy).exists():
            ReevaluationRates.objects.create(
                date=rates_date,
                ccy=base_ccy,
                exchange_rate=1.0
            )
            processed += 1

        # Process other currencies
        for ccy in currencies:
            rate = rates.get(ccy.code)
            if not rate:
                self.stdout.write(self.style.WARNING(f'Rate not available for {ccy.code}'))
                skipped += 1
                continue

            # Check for existing entry
            if ReevaluationRates.objects.filter(date=rates_date, ccy=ccy).exists():
                skipped += 1
                continue

            # Create new entry
            ReevaluationRates.objects.create(
                date=rates_date,
                ccy=ccy,
                exchange_rate=rate
            )
            processed += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed {processed} rates ({skipped} skipped) '
            f'for {rates_date_str}'
        ))