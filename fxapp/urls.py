from django.urls import path, include, re_path
from rest_framework import routers
from fxapp import views
from . views import TradeViewSet


router = routers.SimpleRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'segments', views.SegmentViewSet, basename='segment')
router.register(r'currencies', views.CcyViewSet, basename='ccy')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'daily-rates', views.SystemDailyRatesViewSet,)
router.register(r'trades', views.TradeViewSet, basename='trade')
router.register(r'dealers', views.DealerViewSet, basename='dealer')
router.register(r'positions', views.PositionViewSet, basename='position')
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