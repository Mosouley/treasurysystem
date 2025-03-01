from django.contrib import admin

from .models import *

# admin.site.register(Ccy)
admin.site.register(Customer)
admin.site.register(Trade)
admin.site.register(Dealer)
admin.site.register(Product)
admin.site.register(Segment)
# admin.site.register(SystemDailyRates)
admin.site.register(Position)
# Customizing the admin interface for Ccy
@admin.register(Ccy)
class CcyAdmin(admin.ModelAdmin):
    list_display = ('code',)  # Fields to display in the admin list view
    search_fields = ('code',)  # Add a search bar for the code field
    ordering = ('code',)  # Default ordering

# Customizing the admin interface for SystemDailyRates
@admin.register(SystemDailyRates)
class SystemDailyRatesAdmin(admin.ModelAdmin):
    list_display = ('ccy', 'exchange_rate', 'date', 'last_updated')  # Fields to display
    list_filter = ('date', 'ccy')  # Add filter options for date and currency
    search_fields = ('ccy__code',)  # Enable searching by the related Ccy's code
    ordering = ('-date', 'ccy')  # Default ordering: latest date first
    date_hierarchy = 'date'  # Add a date hierarchy navigation bar

    # Optional: Custom form validation or behavior
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('ccy')  # Optimize queries by prefetching related fields
    
from django.contrib import admin
from django import forms
import pytz

class CountryConfigForm(forms.ModelForm):
    # Custom validation example
    def clean_affiliate_code(self):
        code = self.cleaned_data['affiliate_code']
        if len(code) < 3:
            raise forms.ValidationError("Affiliate code must be at least 3 characters")
        return code.upper()

    class Meta:
        model = CountryConfig
        fields = '__all__'

@admin.register(CountryConfig)
class CountryConfigAdmin(admin.ModelAdmin):
    form = CountryConfigForm
    list_display = ('country', 'base_currency', 'affiliate_name', 'timezone')
    search_fields = ('country__name', 'affiliate_name')
    list_filter = ('base_currency', 'timezone')
    autocomplete_fields = ['base_currency']
    
    # Group fields into sections
    fieldsets = (
        ('General', {
            'fields': ('country', 'affiliate_name', 'affiliate_code')
        }),
        ('Localization', {
            'fields': ('base_currency', 'timezone', 'fiscal_year_start')
        }),
        # ('Advanced', {
        #     'classes': ('collapse',),           
           
        #     'fields': ('additional_field_1', 'additional_field_2')
        # }),
    )

    # Add a custom widget for timezone selection
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'timezone':
            kwargs['widget'] = forms.Select(choices=[(tz, tz) for tz in pytz.all_timezones])
        return super().formfield_for_dbfield(db_field, **kwargs)