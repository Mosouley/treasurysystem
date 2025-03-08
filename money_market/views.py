from django.shortcuts import render
from fxapp.views import AutoMappingBulkCreateViewSet
from .models import Counterparty, Limits, Exposures, LimitType, LimitException, Approvals, Deal, Product
from .serializers import CounterpartySerializer, LimitsSerializer, ExposuresSerializer, LimitTypeSerializer
from .serializers import LimitExceptionSerializer, ApprovalsSerializer, DealSerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class CounterpartyViewSet(AutoMappingBulkCreateViewSet):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer

class LimitsViewSet(AutoMappingBulkCreateViewSet):
    queryset = Limits.objects.all()
    serializer_class = LimitsSerializer
    lookup_fields = {
        'counterparty': ['short_name'], #here is the place to indicate unique values and avoid dubplicate errors
        'limit_type': ['short_name', 'id'], 
    }

class ExposuresViewSet(AutoMappingBulkCreateViewSet):
    queryset = Exposures.objects.all()
    serializer_class = ExposuresSerializer

class LimitTypeViewSet(AutoMappingBulkCreateViewSet):
    queryset = LimitType.objects.all()
    serializer_class = LimitTypeSerializer

class LimitExceptionViewSet(AutoMappingBulkCreateViewSet):
    queryset = LimitException.objects.all()
    serializer_class = LimitExceptionSerializer
  

class CounterpartyViewSet(AutoMappingBulkCreateViewSet):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer
    
class ApprovalsViewSet(AutoMappingBulkCreateViewSet):
    queryset = Approvals.objects.all()
    serializer_class = ApprovalsSerializer

    # lookup_fields = {
    #     'user': ['username', 'id'],  # Lookup by username first, then id for the User model
    #     'segment': ['name', 'id'],   # Lookup by name first, then id for the Segment model
    # }

class DealViewSet(AutoMappingBulkCreateViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class ProductViewSet(AutoMappingBulkCreateViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductChoicesView(APIView):
    def get(self, request):
        product_choices = [{'code': choice[0], 'label': choice[1]} for choice in Product.PRODUCT_CHOICES]
        days_convention_choices = [{'code': choice[0], 'label': choice[1]} for choice in Product.DAYS_CONVENTION]
        return Response({
            'product_choices': product_choices,
            'days_convention_choices': days_convention_choices
        })