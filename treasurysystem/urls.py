from django.contrib import admin
from django.urls import re_path, include


urlpatterns = [
  re_path('admin/', admin.site.urls),
  re_path('api/contacts/', include('contacts.urls')),
  re_path('api/fx/', include('fxapp.urls')),
  re_path('api/alm/', include('money_market.urls')),
]