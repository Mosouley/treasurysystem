from decimal import Decimal
from rest_framework import serializers
from .models import Customer, Ccy, Segment, Product,Dealer,SystemDailyRates,Trade
from django.db import IntegrityError

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
import json

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
        # print(fields)

    # def get_ccy_entity(self):
    #     ccy = SystemDailyRates.objects.get(pk=self.id)
    #     print(ccy)
    #     return ccy

class TradeSerializer(serializers.ModelSerializer):
    # equivalent_lcy = serializers.SerializerMethodField()
    deal_pnl = serializers.ReadOnlyField()
    trade_id = serializers.ReadOnlyField()
    product = ProductSerializer(many=False, )
    trader = DealerSerializer(many=False, )
    customer = CustomerSerializer(many=False, )
    ccy1 = CcySerializer(many=False, )
    ccy2 = CcySerializer(many=False, )
    id = serializers.ReadOnlyField()

    
    class Meta:
        model = Trade
        # fields = '__all__'      
        fields = [ 'id', 'trade_id','tx_date', 'val_date', 'customer', 'product', 'trader', 'ccy1', 'ccy2', 'buy_sell',
                   'amount1', 'amount2', 'deal_rate', 'fees_rate', 'system_rate','equivalent_lcy', 'deal_pnl',
                   'tx_comments',  'status', 'date_created', 'last_updated','ccy1_rate','ccy2_rate']
        # read_only_fields = ('product', 'trader', 'ccy', 'customer',)
        # depth=1

    def create(self, validated_data):
  
        # Retrieve or create related objects
        product_data = validated_data.pop('product')
        product_name = product_data.pop('name')
        customer_data = validated_data.pop('customer',)
        trader_data = validated_data.pop('trader',)
        ccy1_data = validated_data.pop('ccy1',)
        ccy2_data = validated_data.pop('ccy2', )

        product_instance = Product.objects.get_or_create(name=product_name)[0]
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
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'update_group', {
                'type': 'send_update',
                'message': trade_instance.name,
            },
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

            print(instance)
            # Use existing or newly created instances when creating the Trade
       
            return instance
        except IntegrityError as e:
            # Handle uniqueness constraint violation
            raise serializers.ValidationError(e.args[0])



    # def get_equivalent_lcy(self, obj):  
    #     return Decimal(obj.amount1) * obj.deal_rate

    # def get_deal_pnl(self, obj):
    #     print(self)
    #     print(obj)
    #     return -self.amount1 * (self.deal_rate - self.system_rate) * obj.amount2

        # add transaction.atomic so that if error happened, it will rollback
    # @transaction.atomic
    # def create(self, validated_data):
    #     trade = Trade.objects.create(**validated_data)
    #     if "products" in self.initial_data:
    #         products = self.initial_data.get("products")
    #         for product in products:
    #             quantity = product.get("quantity")
    #             product = Product.objects.get(pk=id)
    #             Detail(order=order, product=product, quantity=quantity).save()
    #     order.save()
    #     return order