
import json
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.shortcuts import render
from .models import ExcelModel
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.db.models import Sum

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

class SegmentViewSet(viewsets.ModelViewSet):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer

class CcyViewSet(viewsets.ModelViewSet):
    queryset = Ccy.objects.all()
    serializer_class = CcySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
 
class SystemDailyRatesViewSet(viewsets.ModelViewSet):
    queryset = SystemDailyRates.objects.all().order_by('-last_updated')
    serializer_class = SystemDailyRatesSerializer
    lookup_field = 'ccy_code' 
   # http_method_names = ['get', 'post','head']  # to include specific accepted methods

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serialized_data = []
            for row in request.data:
                ccy, _ = Ccy.objects.get_or_create(code=row[0])
                serialized_data.append({
                    'ccy': ccy.id,
                    'rateLcy': row[1]
                })
            serializer = self.get_serializer(data=serialized_data, many=True)
            
        else:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
   
#    Overriding the get object to return objects based on different filters
    def retrieve(self, request, *args, **kwargs):
        lookup_value = kwargs.get(self.lookup_field)  # Get the value from the URL parameter
        queryset = self.filter_queryset(self.get_queryset())

        if lookup_value is not None:
            filtered_queryset = [
                obj for obj in queryset.order_by('-date', '-last_updated') if getattr(obj, self.lookup_field) == lookup_value
            ]
            # filtered_queryset = queryset.filter(
            #     Q(date=lookup_value) | Q(last_updated=lookup_value)
            # ).order_by('-date', '-last_updated')
           
            # instance = max(filtered_queryset, key=lambda obj: obj.date)
            # filtered_queryset = queryset.filter(
            #     Q(date=lookup_value) | Q(last_updated=lookup_value)
            # ).order_by('-date', '-last_updated')
            # instance = filtered_queryset.first()
            
            instance = filtered_queryset[0] if filtered_queryset else None
  
        else:
            # If the lookup value is not provided, fall back to the default behavior (get by ID)
            return super().retrieve(request, *args, **kwargs)
        if instance is None:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class TradeViewSet(viewsets.ModelViewSet):
    # queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    
    def get_queryset(self):
        # By default, let's assume you want to get trades for the last 30 days
        start_date = now() - timedelta(days=30)
        end_date = now()
        
        # Retrieve the start_date and end_date from query parameters if provided
        start_date_param = self.request.query_params.get('start_date', None)
        end_date_param = self.request.query_params.get('end_date', None)
        # print(start_date_param)
        # print(end_date_param)
        # Parse and validate the date parameters if provided
        if start_date_param:
            start_date = datetime.fromisoformat(start_date_param)
            # print( datetime.fromisoformat(start_date_param))
            # start_date = start_date_param
        if end_date_param:
            end_date = datetime.fromisoformat(end_date_param)
            # print(datetime.fromisoformat(end_date_param))
            # end_date = end_date_param
        # qs = Trade.objects.filter(date_created__range=(start_date, end_date)).values('ccy1__code').annotate(Sum('amount2'))
        print('Starting ', start_date)
        print('Ending ', end_date)
        # for item in qs:
        #     print(item[0], item[1])
        # Filter the queryset based on the provided date range
        queryset = Trade.objects.filter(date_created__range=(start_date, end_date)).order_by('-date_created')
        print(queryset.count())
        # print(queryset.values())
        return queryset

    def batch_destroy(self, request):
        ids = request.data.get('ids', [])
        self.queryset.filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def upload_excel(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        for row in data:
            ExcelModel.objects.create(
                field1=row[0], field2=row[1], field3=row[2]
            )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def my_endpoint(request):
    if request.method == 'POST':
        # get the JSON data from the POST request
        data = json.loads(request.body)
        for i in range(0,len(data)):
            for _, row in enumerate(data):
                ccy_model = Ccy.objects.get_or_create(code=row[0])
                my_model = SystemDailyRates(
                     ccy=ccy_model[0],
                     rateLcy=row[1]
                )
                my_model.save()       
      
        # # extract the table data from the JSON data
        #     table_data.insert(data[i])

        #     print(table_data)
        # create or update model instances for each row in the table data
        # for row in table_data:
        #     instance, created = SystemDailyRates.objects.update_or_create(
        #         id=row['id'],
        #         defaults={
        #             'rateLcy': row['rates'],
        #             'ccy': row['currency'],
        #             # ... add other columns as needed
        #         }
        #     )
        
        # return a JSON response indicating success
            return JsonResponse({'status': 'success'}, safe = False)
    else:
        # handle GET requests
        # ...
        return JsonResponse('I don`t know how what is the best', safe=False)

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        print('Printing the date in the request ')
        print(date_param)
        if date_param is not None:
            queryset = Position.objects.filter(date=date_param)

        return queryset