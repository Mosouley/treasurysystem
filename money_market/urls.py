from django.urls import path, include, re_path
from rest_framework import routers
from money_market import views
from . views import CounterpartyViewSet, LimitExceptionViewSet, LimitsViewSet, ExposuresViewSet, LimitTypeViewSet, ApprovalsViewSet, DealViewSet, ProductViewSet
from .views import ProductChoicesView

router = routers.SimpleRouter()
router.register(r'counterparties', CounterpartyViewSet, basename='counterparty')
router.register(r'limits', LimitsViewSet, basename='limits')
router.register(r'limitexception', LimitExceptionViewSet, basename='exception')
router.register(r'exposures', ExposuresViewSet, basename='exposures')
router.register(r'limit-type', LimitTypeViewSet, basename='limittype',)
router.register(r'approvals', ApprovalsViewSet, basename='approvals')
router.register(r'deals', DealViewSet, basename='deals')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('product-choices/', ProductChoicesView.as_view(), name='product-choices'),
]

urlpatterns += router.urls