from django.urls import path, include, re_path
from rest_framework import routers
from fxapp import views
from . views import TradeViewSet


router = routers.SimpleRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'segments', views.SegmentViewSet, basename='segment')
router.register(r'currencies', views.CcyViewSet, basename='ccy')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'daily-rates', views.SystemDailyRatesViewSet,basename='system-rates')
router.register(r'reeval-rates', views.ReevaluationRatesViewSet, basename='reeval-rate')
router.register(r'trades', TradeViewSet, basename='trades')
router.register(r'dealers', views.DealerViewSet, basename='dealer')

router.register(r'country-configs', views.CountryConfigViewSet, basename='country-config')
# router.register(r'positions-summary', PositionSummaryViewSet, basename='position-summary')
# router.register(r'daily-rates', views.my_endpoint, basename='fxapp')

urlpatterns = [
    path('', include(router.urls)),
    path('batch-destroy/',TradeViewSet.batch_destroy, name='batch_destroy'),
    # path('daily-rates-loading/', views.my_endpoint, name='daily-rates-loading'),
]

