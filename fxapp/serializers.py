import decimal
from uuid import UUID
from django_countries import countries
from rest_framework import serializers
from .models import Customer, Ccy, Segment, Product,Dealer,SystemDailyRates,Trade, Position, CountryConfig
from rest_framework.fields import Field
from decimal import Decimal



class UUIDField(Field):
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, UUID):
            return str(value)
        return value
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  # Retrieve username instead of user id
    segment = serializers.CharField(source='segment.name', read_only=True)  # Retrieve segment name instead of segment id
    class Meta:
        model = Customer
        fields = ('__all__')
        extra_kwargs = {
            'user': {
                'validators': [],
            },
            'cif': {'validators': []},  # Remove unique validation
            'name': {'validators': []},
        }

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('__all__')
        extra_kwargs = {
            'name': {
                'validators': [],
            },
            'user': {
                'validators': [],
            },
            'profile': {'validators': []},
        }

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['name', 'desc']

class CcySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ccy
        fields = ['code']
        extra_kwargs = {
            'code': {
                'validators': [],
            }
        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
        extra_kwargs = {
            'name': {
                'validators': [],
            }
        }

class CountryConfigSerializer(serializers.ModelSerializer):
    country = serializers.ChoiceField(choices=list(countries.countries.items()))
    base_currency = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Ccy.objects.all()
    )
    # print(countries.countries)
    class Meta:
        model = CountryConfig
        fields = '__all__'
        extra_kwargs = {

            'fiscal_year_start': {'format': '%Y-%m-%d'}
        }

class SystemDailyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemDailyRates
        fields = ('date', 'last_updated', 'exchange_rate', 'ccy_code')

        # def validate_exchange_rate(self, value):
        # # Ensure the value is rounded to 4 decimal places
        #     return Decimal(value).quantize(Decimal('0.0001'))
        

class TradeSerializer(serializers.ModelSerializer):
    try:
        # equivalent_lcy = serializers.SerializerMethodField()
        deal_pnl = serializers.ReadOnlyField()
        id = serializers.ReadOnlyField()
        product = ProductSerializer(many=False, )
        trader = DealerSerializer(many=False, )
        customer = CustomerSerializer(many=False, )
        ccy1 = CcySerializer(many=False, )
        ccy2 = CcySerializer(many=False, )

        # page_size = request.query_params.get('pageSize', 10) 
        
        class Meta:
            model = Trade
            # fields = '__all__'      
            fields = [  'id','tx_date', 'val_date', 'customer', 'product', 'trader', 'ccy1', 'ccy2', 'buy_sell',
                    'amount1', 'amount2', 'deal_rate', 'fees_rate', 'system_rate','equivalent_lcy', 'deal_pnl',
                    'tx_comments',  'status', 'date_created', 'last_updated','ccy1_rate','ccy2_rate']
            # read_only_fields = ('product', 'trader', 'ccy', 'customer',)
            # depth=1
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            uuid_fields = ['trade_id',]  # Replace with your actual UUID fields
            # Convert UUID fields to strings
            for field in uuid_fields :  # Replace with your UUID field names and other_uuid_field'
                if field in representation:
                    representation[field] = str(representation[field])

            # Convert Decimal fields to strings or floats
            decimal_fields = ['amount1', 'amount2', 'deal_rate', 'fees_rate', 
                            'system_rate', 'ccy1_rate', 'ccy2_rate', 'deal_pnl','equivalent_lcy']
            
            for field in decimal_fields:
                if field in representation and isinstance(representation[field], decimal.Decimal):
                    representation[field] = float(representation[field]) 
            return representation

        def create(self, validated_data):
            # Retrieve or create related objects
            product_data = validated_data.pop('product', None)

            product_name = product_data['name']

            customer_data = validated_data.pop('customer', None)
            trader_data = validated_data.pop('trader', None)
            ccy1_data = validated_data.pop('ccy1', None)
            ccy2_data = validated_data.pop('ccy2', None)

                # Handle missing related data
            
            if not (product_data and customer_data and trader_data and ccy1_data and ccy2_data):
                raise serializers.ValidationError("Missing required nested fields for related objects.")

            # Retrieve or create related instances
            product_instance, _= Product.objects.get_or_create(name=product_name)
            # Retrieve customer instance by unique identifier (e.g., 'cif') and create if not found
            # Check if a Customer with the same 'cif' exists, otherwise create
            customer_instance = Customer.objects.filter(cif=customer_data['cif']).first()
            # if not customer_instance:
            #     customer_instance = Customer.objects.create(**customer_data)
            
            # Check if a Trader with the same 'profile' exists, otherwise create
            trader_instance = Dealer.objects.filter(profile=trader_data['profile']).first()
            # if not trader_instance:
            #     trader_instance = Dealer.objects.create(**trader_data)
            

            ccy1_instance, _ = Ccy.objects.get_or_create(**ccy1_data)
            ccy2_instance, _ = Ccy.objects.get_or_create(**ccy2_data)

            # Use existing or newly created instances when creating the Trade
            trade_instance = Trade.objects.create(
            product=product_instance,
            customer=customer_instance,
            trader=trader_instance,
            ccy1=ccy1_instance,
            ccy2=ccy2_instance,
            **validated_data
        )
        
            return trade_instance
    except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")
      

class PositionSerializer(serializers.ModelSerializer):
    ccy__code = serializers.StringRelatedField(source='ccy.code')
    open_pos = serializers.SerializerMethodField()
    close_pos = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ['date', 'ccy__code', 'intraday_pos', 'open_pos', 'close_pos']

    def get_open_pos(self, obj):
        # Access the open_pos property on the Position instance
        return obj.open_pos

    def get_close_pos(self, obj):
        # Access the close_pos property on the Position instance
        return obj.close_pos

