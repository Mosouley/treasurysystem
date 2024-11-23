
import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .models import ExcelModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models, transaction
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.db.models import Sum
from django.core.exceptions import ValidationError
from collections import defaultdict
from typing import List, Dict, Tuple, Any

class AutoMappingBulkCreateViewSet(viewsets.ModelViewSet):
        lookup_field = 'id'
        exclude_fields = ['id']
        include_fields = None
        field_mappings = {}
        nested_create = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields_mapping = self.get_fields_mapping()

        def get_fields_mapping(self) -> Dict[str, Dict]:
            """Generate field mappings based on model fields and custom mappings."""
            model = self.serializer_class.Meta.model
            fields = model._meta.get_fields()
            mapping = {
                field.name: self.map_field(field)
                for field in fields if self.should_process_field(field.name)
            }
  
            return mapping

        def should_process_field(self, field_name: str) -> bool:
            """Check if the field should be processed based on include/exclude lists."""
            return field_name not in self.exclude_fields and (
                self.include_fields is None or field_name in self.include_fields
            )

        def map_field(self, field: models.Field) -> Dict[str, Any]:
            """Map a field to its corresponding type and lookup."""
            if field.name in self.field_mappings:
                return self.field_mappings[field.name]
            if isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                return self.map_related_field(field)
            return {'type': 'regular', 'field': field.name}

        def map_related_field(self, field: models.Field) -> Dict[str, Any]:
            """Map related fields (ForeignKey, ManyToMany) with lookup and type."""
            related_model = field.related_model
            lookup_fields = getattr(self, 'lookup_fields', {}).get(field.name, ['id'])
            return {
                'type': 'foreign_key' if isinstance(field, models.ForeignKey) else 'many_to_many',
                'model': related_model,
                'lookup_fields': lookup_fields
            }

        @transaction.atomic
        def create(self, request, *args, **kwargs):
            """Handle bulk creation with nested objects."""
            
            data = request.data if isinstance(request.data, list) else [request.data]
            serialized_data, errors = self.serialize_data(data)
            
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return self.perform_bulk_create(serialized_data)

        def serialize_data(self, data: List[Dict]) -> Tuple[List[Dict], List[str]]:
            """Process and serialize incoming data."""
            serialized_data = []
            errors = []
            for index, row in enumerate(data):
                try:
                    processed_data = self.process_row(row)
                    serialized_data.append(processed_data)
                except Exception as e:
                    errors.append(f"Error processing row {index}: {str(e)}")
            return serialized_data, errors

        def process_row(self, row: Dict) -> Dict[str, Any]:
            """Process an individual data row into a valid model instance."""
            if not isinstance(row, dict):
                raise ValueError("Row data must be a dictionary")

            regular_data, m2m_data = self.process_fields(row)
            return {'regular_data': regular_data, 'm2m_data': m2m_data}

        def process_fields(self, row_data: Dict) -> Tuple[Dict, Dict]:
            """Convert row data into the format required by the model."""
            processed_data = {}
            m2m_data = defaultdict(list)

            for field, mapping in self.fields_mapping.items():
                value = row_data.get(field)
                # print(' the field is ', field, ' and mapping -', mapping)
                if mapping['type'] == 'regular':
              
                    processed_data[field] = value
                elif mapping['type'] == 'foreign_key':
              
                    processed_data[field] = self.get_or_create_related_object(mapping, value)
                elif mapping['type'] == 'many_to_many':
               
                    m2m_data[field] = self.handle_many_to_many_field(mapping, value)

            return processed_data, m2m_data

        def get_or_create_related_object(self, mapping: Dict[str, Any], value: Any) -> models.Model:
            """Handle ForeignKey field value resolution."""
            related_model = mapping['model']
            lookup_fields = mapping['lookup_fields']
           
            if isinstance(value, dict):
                # Handle nested ForeignKey creation
                lookup_field, lookup_value = list(value.items())[0]
                return self.fetch_or_create_object(related_model, lookup_field, lookup_value)
            else:
                # Assume value is the ID or single lookup field
                for lookup_field in lookup_fields:
                    try:
                        return related_model.objects.get_or_create(**{lookup_field: value})[0]
                    except related_model.DoesNotExist:
                        continue
                raise ValueError(f"{related_model.__name__} object not found with provided lookup fields.")

        def handle_many_to_many_field(self, mapping: Dict[str, Any], values: List[Any]) -> List[models.Model]:
            """Process ManyToMany field data."""
            related_objs = []

            for value in values:
                related_obj = self.get_or_create_related_object(mapping, value)
                related_objs.append(related_obj)
            return related_objs

        def fetch_or_create_object(self, model: models.Model, field: str, value: Any) -> models.Model:
            """Fetch or create an object based on the lookup field."""
            obj, created = model.objects.get_or_create(**{field: value})
            return obj
        
        # def check_for_duplicates(self, data: Dict) -> bool:
        #     """Check if an object with unique fields already exists."""
        #     model = self.serializer_class.Meta.model
        #     unique_fields = ['cif', 'name']  # Adjust this for the unique fields of your model
        #     filter_kwargs = {field: data[field] for field in unique_fields if field in data}

        #     return model.objects.filter(**filter_kwargs).exists()

        def perform_bulk_create(self, serialized_data: List[Dict]) -> Response:
            """Perform bulk creation of instances."""
            model = self.serializer_class.Meta.model
            instances = []
            m2m_data = defaultdict(list)
            errors =[]
        
            for index, item in enumerate(serialized_data) :
                regular_data = item['regular_data']
                instance = model(**regular_data)
                # print('Index is -', index , 'Item is --', item)
                try:
                    instance.full_clean()
                    instances.append(instance)

                except ValidationError as e:
                    errors.append(f"Validation error for row {index}: {str(e)}")
                    continue

                for field, values in item['m2m_data'].items():
                    m2m_data[field].append((instance, values))

            # Perform bulk creation only if there are valid instances
            if instances:
                created_instances = model.objects.bulk_create(instances)
                self.handle_m2m_fields(m2m_data)

                serializer = self.get_serializer(created_instances, many=True)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            if errors:
                return Response({"errors": errors}, status=status.HTTP_417_EXPECTATION_FAILED)
            # If no errors and no instances, return an empty response (unlikely scenario)
            return Response({"errors": "No valid data to create instances."}, status=status.HTTP_400_BAD_REQUEST)

        def handle_m2m_fields(self, m2m_data: defaultdict) -> None:
            """Set ManyToMany field values for created instances."""
            for field, instance_values in m2m_data.items():
                for instance, values in instance_values:
                    getattr(instance, field).set(values)

class CustomerViewSet(AutoMappingBulkCreateViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_fields = {
        'user': ['username', 'id'],  # Lookup by username first, then id for the User model
        'segment': ['name', 'id'],   # Lookup by name first, then id for the Segment model
    }

class DealerViewSet(AutoMappingBulkCreateViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    lookup_fields = {
        'user': ['username', 'id'],  # Lookup by username first, then id for the User modells
        
    }
class SegmentViewSet(viewsets.ModelViewSet):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer

class CcyViewSet(viewsets.ModelViewSet):
    queryset = Ccy.objects.all()
    serializer_class = CcySerializer

class ProductViewSet(AutoMappingBulkCreateViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
 
class SystemDailyRatesViewSet(viewsets.ModelViewSet):
    queryset = SystemDailyRates.objects.all().order_by('-last_updated')
    serializer_class = SystemDailyRatesSerializer
    lookup_field = 'ccy_code' 
   # http_method_names = ['get', 'post','head']  # to include specific accepted methods––        

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serialized_data = []
        errors =[]
            # serialized_data = []
        for row in data:
            try:
                if isinstance(row, list):
                    if len(row) < 2:
                        raise ValueError('Each row must contain at least currency code and rate')
                    ccy_code, rate = row [0], row [1]
                elif isinstance(row, dict):
                    # Handle dict input
                    ccy_code = row.get('ccy_code')
                    rate = row.get('rateLcy')
                    if not ccy_code or rate is None:
                        raise ValueError("Missing ccy_code or rateLcy")
                else:
                    raise ValueError("Unsupported data format")
                ccy, _ = Ccy.objects.get_or_create(code=ccy_code)
                serialized_data.append({
                    'ccy': ccy.id,
                    'rateLcy': rate
                })
            
            except Exception as e:
                errors.append(f"Errorprocessing row {row}: {str(e)}")
            serializer = self.get_serializer(data=serialized_data, many=True)
            
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=serialized_data, many=True)
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

        if start_date_param and end_date_param:
            start_date = datetime.fromisoformat(start_date_param)
        if end_date_param:
            end_date = datetime.fromisoformat(end_date_param)
        queryset = Trade.objects.filter(tx_date__range=(start_date, end_date)).order_by('-date_created')
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
    
        # return a JSON response indicating success
            return JsonResponse({'status': 'success'}, safe = False)
    else:
        # handle GET requests
        # ...
        return JsonResponse('I don`t know how what is the best', safe=False)

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer     

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        ccy_param = self.request.query_params.get('ccy__code', None)

        queryset = super().get_queryset().values('date','ccy__code','intraday_pos').annotate(total_pos=Sum('intraday_pos'))

        result = Position.objects.values('date','ccy__code','intraday_pos' ).annotate(total_pos=Sum('intraday_pos'))

        if date_param is not None:
            result = queryset.filter(date=date_param)
        
        if ccy_param:
            result = result.filter(ccy__code=ccy_param)
        return result

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"detail": "No records found for the given date"}, status=404)
        serializer = PositionSerializer(queryset, many=True)
        return Response(serializer.data)
        

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     if not queryset.exists():
    #         return Response({"detail": "No records found for the given date"}, status=404)
        
    #     # Use `PositionSerializer` for serialization to include calculated fields.
    #     serializer = PositionSerializer(queryset, many=True)
    #     return Response(serializer.data)
    


@csrf_exempt
def import_excel_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            fields, relationships = extract_fields_and_relationships(data)
            create_model_with_relationships('ImportedModel', fields, relationships)
            run_migrations()
            return JsonResponse({'status': 'success', 'message': 'Model created successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def extract_fields_and_relationships(data):
    # Analyze data structure and map field types
    fields = {}
    relationships = {}
    for key in data[0].keys():  # Assume the first row represents the structure
        if key.endswith('_fk'):  # ForeignKey convention
            relationships[key] = 'RelatedModel'  # Replace with actual related model name
            fields[key] = 'ForeignKey'
        elif key.endswith('_m2m'):  # ManyToManyField convention
            relationships[key] = 'RelatedModel'
            fields[key] = 'ManyToManyField'
        else:
            fields[key] = 'CharField'
    return fields, relationships

def create_model_with_relationships(name, fields, relationships):
    class Meta:
        app_label = 'my_app'

    attrs = {
        '__module__': 'my_app.models',
        'Meta': Meta,
    }
    for field_name, field_type in fields.items():
        if field_type == 'ForeignKey':
            related_model = relationships.get(field_name)
            attrs[field_name] = models.ForeignKey(
                related_model, on_delete=models.CASCADE, null=True, blank=True
            )
        elif field_type == 'ManyToManyField':
            related_model = relationships.get(field_name)
            attrs[field_name] = models.ManyToManyField(related_model, blank=True)
        else:
            attrs[field_name] = models.CharField(max_length=255)

    new_model = type(name, (models.Model,), attrs)
    models.Model.add_to_class(name, new_model)
    return new_model