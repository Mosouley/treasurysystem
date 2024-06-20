from decimal import Decimal
from uuid import UUID
from rest_framework import serializers
from .models import Customer, Ccy, Segment, Product,Dealer,SystemDailyRates,Trade, Position
from django.db import IntegrityError

from rest_framework.fields import Field

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
import json



class UUIDField(Field):
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, UUID):
            return str(value)
        return value
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')
        extra_kwargs = {
            'user': {
                'validators': [],
            }
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
            }
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

class SystemDailyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemDailyRates
        fields = ('date', 'last_updated', 'rateLcy', 'ccy', 'ccy_code')
        

class TradeSerializer(serializers.ModelSerializer):
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
        # Convert UUID fields to strings
        for field in ['trade_id']:  # Replace with your UUID field names and other_uuid_field'
            if field in representation:
                representation[field] = str(representation[field])

        return representation

    def create(self, validated_data):
        # Retrieve or create related objects
        product_data = validated_data.pop('product')

        product_name = product_data['name']

        customer_data = validated_data.pop('customer')
        trader_data = validated_data.pop('trader')
        ccy1_data = validated_data.pop('ccy1')
        ccy2_data = validated_data.pop('ccy2')

        product_instance, is_created= Product.objects.get_or_create(name=product_name)
        customer_instance, _ = Customer.objects.get_or_create(**customer_data)
        trader_instance, _ = Dealer.objects.get_or_create(**trader_data)
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
      

    def update(self, instance, validated_data):
        try:
            product_data = validated_data.pop('product')
            product_name = product_data.pop('name')
            product = Product.objects.get_or_create(name=product_name)[0]
            instance.product = product

            customer_data = validated_data.pop('customer')
            trader_data = validated_data.pop('trader')
            ccy1_data = validated_data.pop('ccy1')
            ccy2_data = validated_data.pop('ccy2', )

            
            customer_instance, _ = Customer.objects.get_or_create(**customer_data)
            trader_instance, _ = Dealer.objects.get_or_create(**trader_data)
            ccy1_instance, _ = Ccy.objects.get_or_create(**ccy1_data)
            ccy2_instance, _ = Ccy.objects.get_or_create(**ccy2_data)

          
            # Use existing or newly created instances when creating the Trade
       
            return instance
        except IntegrityError as e:
            # Handle uniqueness constraint violation
            raise serializers.ValidationError(e.args[0])


class TradeCreateSerializer(serializers.ListSerializer):
    child = TradeSerializer()

    def create(self, validated_data):
        instances = [Trade(**item) for item in validated_data]
        return Trade.objects.bulk_create(instances)

class PositionSerializer(serializers.ModelSerializer):
    ccy__code = serializers.StringRelatedField(source='ccy.code')
    total_pos = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Position
        fields = ['date', 'ccy__code', 'total_pos']
    
    def get_total_pos(self, obj):
        return obj['total_pos']
    
class PositionSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    ccy__code = serializers.CharField(max_length=3)
    total_pos = serializers.FloatField(read_only=True)