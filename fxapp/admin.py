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