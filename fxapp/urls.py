from django.urls import path, include, re_path
from rest_framework import routers
from fxapp import views
from . views import TradeViewSet


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
    path('batch-destroy/',TradeViewSet.batch_destroy, name='batch_destroy'),
    # path('daily-rates-loading/', views.my_endpoint, name='daily-rates-loading'),
]
urlpatterns += [
    # path('daily-rates-loading/', views.my_endpoint, name='daily-rates-loading'),
    # re_path(r'(?P<path>.*)', views.my_endpoint, name='home')
]



urlpatterns += router.urls