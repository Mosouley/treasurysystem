from django.contrib import admin

from .models import *
admin.site.register(LimitType)
admin.site.register(Counterparty)
admin.site.register(Limits)
admin.site.register(Exposures)
admin.site.register(LimitException)
admin.site.register(Approvals)