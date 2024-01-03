from django.urls import path, include
from rest_framework import routers
from fxapp import views


router = routers.SimpleRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'segments', views.SegmentViewSet)
router.register(r'currencies', views.CcyViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'daily-rates', views.SystemDailyRatesViewSet)
router.register(r'trades', views.TradeViewSet)
router.register(r'dealers', views.DealerViewSet)
# router.register(r'daily-rates', views.my_endpoint, basename='fxapp')

urlpatterns = [
    # path('daily-rates-loading/', views.my_endpoint, name='daily-rates-loading'),
]
urlpatterns += router.urls